$ErrorActionPreference = "Stop"
$credential = Import-Clixml -LiteralPath "$env:LOCALAPPDATA\MesIngestWatch\gpt_win11.credential.xml"
$session = New-PSSession -VMName "gpt_win11" -Credential $credential
$root = "C:\MesIngest\Ticket11\run-wpf-ui-20260810-0340-v25-candidate-verify"
$taskName = "MesIngestWatch-Ticket11-v25-xaml"
try {
    Invoke-Command -Session $session -ArgumentList $root, $taskName -ScriptBlock {
        param($root, $taskName)
        Remove-Item -LiteralPath (Join-Path $root "xaml-stability-result.json") -Force -ErrorAction SilentlyContinue
        $action = New-ScheduledTaskAction `
            -Execute "C:\Program Files\PowerShell\7\pwsh.exe" `
            -Argument ('-NoProfile -ExecutionPolicy Bypass -STA -File "{0}" -Root "{1}"' -f (Join-Path $root "run-xaml-stability.ps1"), $root) `
            -WorkingDirectory $root
        $principal = New-ScheduledTaskPrincipal `
            -UserId "GPT-WIN11\gpt" `
            -LogonType Interactive `
            -RunLevel Highest
        $settings = New-ScheduledTaskSettingsSet `
            -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
            -AllowStartIfOnBatteries `
            -DontStopIfGoingOnBatteries
        Register-ScheduledTask `
            -TaskName $taskName `
            -Action $action `
            -Principal $principal `
            -Settings $settings `
            -Force | Out-Null
        Start-ScheduledTask -TaskName $taskName
        Get-ScheduledTask -TaskName $taskName | Select-Object TaskName, State
    }
} finally {
    Remove-PSSession $session
}
