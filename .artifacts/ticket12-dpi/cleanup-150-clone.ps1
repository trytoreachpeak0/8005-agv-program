$ErrorActionPreference = 'Stop'

$cloneVm = 'gpt_win11_ticket12_dpi150'
$exportRoot = 'F:\ticket12-dpi150-export-20260810-0950'
$importRoot = 'F:\ticket12-dpi150-import-20260810-0950'
$credential = Import-Clixml -LiteralPath `
    "$env:LOCALAPPDATA\MesIngestWatch\gpt_win11.credential.xml"

$session = New-PSSession -VMName $cloneVm -Credential $credential
try {
    $guestCleanup = Invoke-Command -Session $session -ScriptBlock {
        $tasks = @(Get-ScheduledTask |
            Where-Object TaskName -Like 'MesIngestWatch-Golden-12-dpi150-*')
        foreach ($task in $tasks) {
            if ($task.State -eq 'Running') {
                Stop-ScheduledTask -TaskName $task.TaskName -ErrorAction SilentlyContinue
            }
            Unregister-ScheduledTask -TaskName $task.TaskName -Confirm:$false
        }
        Get-Process -Name 'MesIngest.Watch', 'testhost', 'vstest.console' `
            -ErrorAction SilentlyContinue | Stop-Process -Force
        [pscustomobject]@{
            TasksRemoved = $tasks.Count
            ResidualProcesses = @(Get-Process -Name `
                'MesIngest.Watch', 'testhost', 'vstest.console' `
                -ErrorAction SilentlyContinue).Count
        }
    }
}
finally {
    Remove-PSSession $session
}

$vm = Get-VM -Name $cloneVm
if ($vm.State -ne 'Off') {
    Stop-VM -Name $cloneVm -Force
}
Remove-VM -Name $cloneVm -Force

foreach ($path in @($exportRoot, $importRoot)) {
    $resolved = (Resolve-Path -LiteralPath $path).Path
    if ($resolved -notlike 'F:\ticket12-dpi150-*20260810-0950') {
        throw "Refusing to remove unexpected clone path: $resolved"
    }
    Remove-Item -LiteralPath $resolved -Recurse -Force
}

[pscustomobject]@{
    GuestTasksRemoved = $guestCleanup.TasksRemoved
    GuestResidualProcesses = $guestCleanup.ResidualProcesses
    CloneRemoved = -not [bool](Get-VM -Name $cloneVm -ErrorAction SilentlyContinue)
    ExportRemoved = -not (Test-Path -LiteralPath $exportRoot)
    ImportRemoved = -not (Test-Path -LiteralPath $importRoot)
}
