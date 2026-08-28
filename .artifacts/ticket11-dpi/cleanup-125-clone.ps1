$ErrorActionPreference = 'Stop'

$cloneVm = 'gpt_win11_ticket11_dpi125'
$exportRoot = 'F:\ticket11-dpi125-export-20260810-0252'
$importRoot = 'F:\ticket11-dpi125-import-20260810-0252'
$credential = Import-Clixml -LiteralPath `
    "$env:LOCALAPPDATA\MesIngestWatch\gpt_win11.credential.xml"

$taskCounts = @{}
foreach ($vmName in @('gpt_win11', $cloneVm)) {
    $session = New-PSSession -VMName $vmName -Credential $credential
    try {
        $taskCounts[$vmName] = Invoke-Command -Session $session -ScriptBlock {
            $tasks = @(Get-ScheduledTask |
                Where-Object TaskName -Like 'MesIngestWatch-Ticket11*')
            foreach ($task in $tasks) {
                if ($task.State -eq 'Running') {
                    Stop-ScheduledTask -TaskName $task.TaskName -ErrorAction SilentlyContinue
                }
                Unregister-ScheduledTask -TaskName $task.TaskName -Confirm:$false
            }
            $tasks.Count
        }
    }
    finally {
        Remove-PSSession $session
    }
}

$vm = Get-VM -Name $cloneVm
if ($vm.State -ne 'Off') {
    Stop-VM -Name $cloneVm -Force
}
Remove-VM -Name $cloneVm -Force

foreach ($path in @($exportRoot, $importRoot)) {
    $resolved = (Resolve-Path -LiteralPath $path).Path
    if ($resolved -notlike 'F:\ticket11-dpi125-*20260810-0252') {
        throw "Refusing to remove unexpected clone path: $resolved"
    }
    Remove-Item -LiteralPath $resolved -Recurse -Force
}

[pscustomobject]@{
    OriginalTasksRemoved = $taskCounts['gpt_win11']
    CloneTasksRemoved = $taskCounts[$cloneVm]
    CloneRemoved = -not [bool](Get-VM -Name $cloneVm -ErrorAction SilentlyContinue)
    ExportRemoved = -not (Test-Path -LiteralPath $exportRoot)
    ImportRemoved = -not (Test-Path -LiteralPath $importRoot)
}
