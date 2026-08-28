[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ProposalDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName PresentationCore

function Read-Bitmap {
    param([Parameter(Mandatory = $true)][string]$Path)

    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $decoder = [System.Windows.Media.Imaging.PngBitmapDecoder]::new(
            $stream,
            [System.Windows.Media.Imaging.BitmapCreateOptions]::PreservePixelFormat,
            [System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad)
        $decoder.Frames[0]
    } finally {
        $stream.Dispose()
    }
}

function Write-ContactSheet {
    param(
        [Parameter(Mandatory = $true)][System.IO.DirectoryInfo[]]$Scenarios,
        [Parameter(Mandatory = $true)][string]$ImageName,
        [Parameter(Mandatory = $true)][string]$Output
    )

    $width = 1920
    $height = 1000
    $columns = 4
    $rows = 5
    $cellWidth = $width / $columns
    $cellHeight = $height / $rows
    $visual = [System.Windows.Media.DrawingVisual]::new()
    $drawing = $visual.RenderOpen()
    try {
        $drawing.DrawRectangle(
            [System.Windows.Media.Brushes]::White,
            $null,
            [System.Windows.Rect]::new(0, 0, $width, $height))
        for ($index = 0; $index -lt $Scenarios.Count; $index++) {
            $scenario = $Scenarios[$index]
            $column = $index % $columns
            $row = [math]::Floor($index / $columns)
            $left = $column * $cellWidth + 8
            $top = $row * $cellHeight + 26
            $bitmap = Read-Bitmap -Path (Join-Path $scenario.FullName $ImageName)
            $maxWidth = $cellWidth - 16
            $maxHeight = $cellHeight - 34
            $scale = [math]::Min($maxWidth / $bitmap.PixelWidth, $maxHeight / $bitmap.PixelHeight)
            $drawWidth = $bitmap.PixelWidth * $scale
            $drawHeight = $bitmap.PixelHeight * $scale
            $drawing.DrawImage(
                $bitmap,
                [System.Windows.Rect]::new(
                    $left + ($maxWidth - $drawWidth) / 2,
                    $top + ($maxHeight - $drawHeight) / 2,
                    $drawWidth,
                    $drawHeight))
            $label = [System.Windows.Media.FormattedText]::new(
                $scenario.Name,
                [Globalization.CultureInfo]::InvariantCulture,
                [System.Windows.FlowDirection]::LeftToRight,
                [System.Windows.Media.Typeface]::new('Consolas'),
                13,
                [System.Windows.Media.Brushes]::Black,
                1)
            $drawing.DrawText($label, [System.Windows.Point]::new($left, $row * $cellHeight + 5))
        }
    } finally {
        $drawing.Close()
    }

    $render = [System.Windows.Media.Imaging.RenderTargetBitmap]::new(
        $width,
        $height,
        96,
        96,
        [System.Windows.Media.PixelFormats]::Pbgra32)
    $render.Render($visual)
    $encoder = [System.Windows.Media.Imaging.PngBitmapEncoder]::new()
    $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($render))
    $stream = [System.IO.File]::Create($Output)
    try {
        $encoder.Save($stream)
    } finally {
        $stream.Dispose()
    }
}

$root = [System.IO.Path]::GetFullPath($ProposalDirectory)
$scenarios = @(Get-ChildItem -LiteralPath $root -Directory | Sort-Object Name)
if ($scenarios.Count -ne 19) {
    throw "Expected 19 scenario proposals; found $($scenarios.Count)."
}

foreach ($name in @('before', 'after', 'diff')) {
    Write-ContactSheet `
        -Scenarios $scenarios `
        -ImageName ($name + '.png') `
        -Output (Join-Path $root ($name + '-contact-sheet.png'))
}

Write-Host "WATCH_XAML_CONTACT_SHEETS_CREATED: 3"
