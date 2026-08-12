$ErrorActionPreference = "Stop"
$credential = Import-Clixml -LiteralPath "$env:LOCALAPPDATA\MesIngestWatch\gpt_win11.credential.xml"
$session = New-PSSession -VMName "gpt_win11" -Credential $credential
$oldRoot = "C:\MesIngest\Ticket11\run-wpf-ui-20260810-0330-v24-styled"
$root = "C:\MesIngest\Ticket11\run-wpf-ui-20260810-0340-v25-candidate-verify"
try {
    Invoke-Command -Session $session -ArgumentList $oldRoot, $root -ScriptBlock {
        param($oldRoot, $root)
        New-Item -ItemType Directory -Path $root -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $oldRoot "Source") -Destination $root -Recurse
        Copy-Item `
            -LiteralPath (Join-Path $oldRoot "run-xaml-stability.ps1") `
            -Destination (Join-Path $root "run-xaml-stability.ps1")
        New-Item -ItemType Directory -Path (Join-Path $root "Results") -Force | Out-Null
        $candidate = Join-Path $root "Candidate-run-1"
        Copy-Item `
            -LiteralPath (Join-Path $oldRoot "Results\xaml-stability-diagnostics\run-1") `
            -Destination $candidate `
            -Recurse
        $baseline = Join-Path $root "Source\mes\ingest\csharp\MesIngest.Watch.UiTests\Baselines\SelectedUi"
        $resolved = [IO.Path]::GetFullPath($baseline)
        if (-not $resolved.StartsWith($root, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Unsafe baseline path: $resolved"
        }
        Get-ChildItem -LiteralPath $baseline -Filter "*.received.*" -File | Remove-Item -Force
        Get-ChildItem -LiteralPath $baseline -Filter "*.verified.*" -File | Remove-Item -Force
        foreach ($file in Get-ChildItem -LiteralPath $candidate -Filter "*.received.*" -File) {
            $name = $file.Name -replace "\.received\.", ".verified."
            Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $baseline $name)
        }
        [pscustomobject]@{
            VerifiedPng = @(Get-ChildItem $baseline -Filter "*.verified.png").Count
            VerifiedXml = @(Get-ChildItem $baseline -Filter "*.verified.xml").Count
            Received = @(Get-ChildItem $baseline -Filter "*.received.*").Count
            CandidateFiles = @(Get-ChildItem $candidate -File).Count
        }
    }
} finally {
    Remove-PSSession $session
}
