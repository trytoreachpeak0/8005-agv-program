[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$CandidateDirectory,
    [Parameter(Mandatory = $true)][string]$HistoricalDirectory,
    [Parameter(Mandatory = $true)][string]$OutputDirectory,
    [ValidateRange(1, 19)][int]$ExpectedCount = 19
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName PresentationCore

function Read-PngPixels {
    param([Parameter(Mandatory = $true)][string]$Path)

    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $decoder = [System.Windows.Media.Imaging.PngBitmapDecoder]::new(
            $stream,
            [System.Windows.Media.Imaging.BitmapCreateOptions]::PreservePixelFormat,
            [System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad)
        $converted = [System.Windows.Media.Imaging.FormatConvertedBitmap]::new(
            $decoder.Frames[0],
            [System.Windows.Media.PixelFormats]::Bgra32,
            $null,
            0)
        $stride = $converted.PixelWidth * 4
        $pixels = [byte[]]::new($stride * $converted.PixelHeight)
        $converted.CopyPixels($pixels, $stride, 0)
        [pscustomobject]@{
            Width = $converted.PixelWidth
            Height = $converted.PixelHeight
            Stride = $stride
            Pixels = $pixels
        }
    } finally {
        $stream.Dispose()
    }
}

function Write-PngDiff {
    param(
        [Parameter(Mandatory = $true)][string]$Before,
        [Parameter(Mandatory = $true)][string]$After,
        [Parameter(Mandatory = $true)][string]$Output
    )

    $beforeImage = Read-PngPixels -Path $Before
    $afterImage = Read-PngPixels -Path $After
    if ($beforeImage.Width -ne $afterImage.Width -or
        $beforeImage.Height -ne $afterImage.Height) {
        throw "PNG dimensions differ: $Before / $After"
    }

    $pixels = [byte[]]::new($beforeImage.Pixels.Length)
    $changed = 0L
    for ($index = 0; $index -lt $pixels.Length; $index += 4) {
        $same = $beforeImage.Pixels[$index] -eq $afterImage.Pixels[$index] -and
            $beforeImage.Pixels[$index + 1] -eq $afterImage.Pixels[$index + 1] -and
            $beforeImage.Pixels[$index + 2] -eq $afterImage.Pixels[$index + 2] -and
            $beforeImage.Pixels[$index + 3] -eq $afterImage.Pixels[$index + 3]
        if ($same) {
            $pixels[$index] = 245
            $pixels[$index + 1] = 245
            $pixels[$index + 2] = 245
        } else {
            $changed++
            $pixels[$index] = 255
            $pixels[$index + 1] = 0
            $pixels[$index + 2] = 255
        }
        $pixels[$index + 3] = 255
    }

    $bitmap = [System.Windows.Media.Imaging.BitmapSource]::Create(
        $beforeImage.Width,
        $beforeImage.Height,
        96,
        96,
        [System.Windows.Media.PixelFormats]::Bgra32,
        $null,
        $pixels,
        $beforeImage.Stride)
    $encoder = [System.Windows.Media.Imaging.PngBitmapEncoder]::new()
    $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($bitmap))
    $stream = [System.IO.File]::Create($Output)
    try {
        $encoder.Save($stream)
    } finally {
        $stream.Dispose()
    }

    [pscustomobject]@{
        Width = $beforeImage.Width
        Height = $beforeImage.Height
        ChangedPixels = $changed
        TotalPixels = [long]$beforeImage.Width * $beforeImage.Height
    }
}

$candidateRoot = [System.IO.Path]::GetFullPath($CandidateDirectory)
$historicalRoot = [System.IO.Path]::GetFullPath($HistoricalDirectory)
$outputRoot = [System.IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $outputRoot) {
    throw "OutputDirectory must not already exist: $outputRoot"
}
New-Item -ItemType Directory -Path $outputRoot | Out-Null

$candidatePngs = @(Get-ChildItem -LiteralPath $candidateRoot -Filter "*.received.png" -File | Sort-Object Name)
$candidateXmls = @(Get-ChildItem -LiteralPath $candidateRoot -Filter "*.received.xml" -File)
if ($candidatePngs.Count -ne $ExpectedCount -or $candidateXmls.Count -ne $ExpectedCount) {
    throw "Expected $ExpectedCount candidate PNG and XML files; found $($candidatePngs.Count) and $($candidateXmls.Count)."
}

$manifest = foreach ($candidatePng in $candidatePngs) {
    $name = $candidatePng.Name -replace '\.received\.png$', ''
    $candidateXml = Join-Path $candidateRoot ($name + '.received.xml')
    $historicalPng = Join-Path $historicalRoot ($name + '.verified.png')
    $historicalXml = Join-Path $historicalRoot ($name + '.verified.xml')
    if (-not (Test-Path -LiteralPath $candidateXml -PathType Leaf) -or
        -not (Test-Path -LiteralPath $historicalPng -PathType Leaf) -or
        -not (Test-Path -LiteralPath $historicalXml -PathType Leaf)) {
        throw "Incomplete proposal inputs for $name"
    }

    $proposal = Join-Path $outputRoot $name
    New-Item -ItemType Directory -Path $proposal | Out-Null
    Copy-Item -LiteralPath $historicalPng -Destination (Join-Path $proposal 'before.png')
    Copy-Item -LiteralPath $candidatePng.FullName -Destination (Join-Path $proposal 'after.png')
    Copy-Item -LiteralPath $historicalXml -Destination (Join-Path $proposal 'before.xml')
    Copy-Item -LiteralPath $candidateXml -Destination (Join-Path $proposal 'after.xml')
    $diff = Write-PngDiff -Before $historicalPng -After $candidatePng.FullName -Output (Join-Path $proposal 'diff.png')

    [pscustomobject]@{
        Scenario = $name
        Width = $diff.Width
        Height = $diff.Height
        ChangedPixels = $diff.ChangedPixels
        ChangedPercent = [math]::Round(100 * $diff.ChangedPixels / $diff.TotalPixels, 4)
        BeforePngSha256 = (Get-FileHash -LiteralPath $historicalPng -Algorithm SHA256).Hash
        AfterPngSha256 = (Get-FileHash -LiteralPath $candidatePng.FullName -Algorithm SHA256).Hash
        BeforeXmlSha256 = (Get-FileHash -LiteralPath $historicalXml -Algorithm SHA256).Hash
        AfterXmlSha256 = (Get-FileHash -LiteralPath $candidateXml -Algorithm SHA256).Hash
        ReviewState = 'PENDING_SCENARIO_REVIEW'
    }
}

$manifest | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $outputRoot 'proposal-manifest.json') -Encoding utf8
$manifest | Export-Csv -LiteralPath (Join-Path $outputRoot 'proposal-manifest.csv') -NoTypeInformation -Encoding utf8
Write-Host "WATCH_XAML_PROPOSALS_CREATED: $($manifest.Count)"
