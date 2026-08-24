$ErrorActionPreference = 'Stop'

$credential = Import-Clixml -LiteralPath "$env:LOCALAPPDATA\MesIngestWatch\gpt_win11.credential.xml"
$session = New-PSSession -VMName 'gpt_win11' -Credential $credential
$guestRoot = 'C:\MesIngest\Ticket11\run-wpf-ui-20260810-0405-v26-normalized'

try {
    Invoke-Command -Session $session -ScriptBlock {
        param($root)

        if (Test-Path -LiteralPath $root) {
            throw "Run directory already exists: $root"
        }

        New-Item -ItemType Directory -Path $root | Out-Null
        Copy-Item -LiteralPath 'C:\MesIngest\Ticket11\run-wpf-ui-20260810-0330-v24-styled\Source' `
            -Destination $root -Recurse
        Copy-Item -LiteralPath 'C:\MesIngest\Ticket11\run-wpf-ui-20260810-0330-v24-styled\run-xaml-stability.ps1' `
            -Destination $root
        New-Item -ItemType Directory -Path (Join-Path $root 'Results') | Out-Null
        $baseline = Join-Path $root 'Source\mes\ingest\csharp\MesIngest.Watch.UiTests\Baselines\SelectedUi'
        Get-ChildItem -LiteralPath $baseline -Filter '*.received.*' -File -ErrorAction SilentlyContinue |
            Remove-Item -Force
    } -ArgumentList $guestRoot

    $localProject = 'C:\Users\szy\Desktop\8005---AGV\mes\ingest\csharp\MesIngest.Watch.UiTests'
    $guestProject = Join-Path $guestRoot 'Source\mes\ingest\csharp\MesIngest.Watch.UiTests'
    Copy-Item -ToSession $session -LiteralPath (Join-Path $localProject 'WatchVisualCaptureConverter.cs') `
        -Destination (Join-Path $guestProject 'WatchVisualCaptureConverter.cs') -Force
    Copy-Item -ToSession $session -LiteralPath (Join-Path $localProject 'WatchVisualCaptureConverterTests.cs') `
        -Destination (Join-Path $guestProject 'WatchVisualCaptureConverterTests.cs') -Force
    Get-ChildItem -LiteralPath (Join-Path $localProject 'Baselines\SelectedUi') `
            -Filter '*.verified.*' -File |
        ForEach-Object {
            Copy-Item -ToSession $session -LiteralPath $_.FullName `
                -Destination (Join-Path $guestProject 'Baselines\SelectedUi' $_.Name) -Force
        }

    Invoke-Command -Session $session -ScriptBlock {
        param($root)

        $taskName = 'MesIngestWatch-Ticket11-v26-xaml'
        $runner = Join-Path $root 'run-xaml-stability.ps1'
        $arguments = "-NoProfile -ExecutionPolicy Bypass -STA -File `"$runner`" -Root `"$root`""
        $action = New-ScheduledTaskAction `
            -Execute 'C:\Program Files\PowerShell\7\pwsh.exe' `
            -Argument $arguments
        $principal = New-ScheduledTaskPrincipal `
            -UserId 'GPT-WIN11\gpt' `
            -LogonType Interactive `
            -RunLevel Highest
        Register-ScheduledTask -TaskName $taskName -Action $action -Principal $principal -Force | Out-Null
        Start-ScheduledTask -TaskName $taskName
        [pscustomobject]@{
            Task = $taskName
            Root = $root
            Baselines = (Get-ChildItem -LiteralPath (
                Join-Path $root 'Source\mes\ingest\csharp\MesIngest.Watch.UiTests\Baselines\SelectedUi') `
                -Filter '*.verified.*').Count
        }
    } -ArgumentList $guestRoot
}
finally {
    Remove-PSSession $session
}
