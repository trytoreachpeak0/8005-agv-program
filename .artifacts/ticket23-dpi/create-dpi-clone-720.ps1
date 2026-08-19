# Ticket 23, 720 epx DPI validation: export the calibrated VM live, import a disposable
# clone with a new VM ID, then free the memory the clone needs by shutting the calibrated
# VM down gracefully.
#
# Ordering is deliberate. The export runs while gpt_win11 is up, so the golden machine is
# only offline for the part that genuinely needs its 4 GB. The host has ~1.9 GB free and
# the clone needs 4 GB, so the two cannot run together.
#
# The calibrated desktop is never re-scaled; 125% and 150% exist only inside this clone,
# which is destroyed by cleanup-dpi-clone.ps1 afterwards.
param(
    [string]$SourceVm = 'gpt_win11',
    [string]$CloneVm = 'gpt_win11_ticket23_dpi720',
    [string]$ExportRoot = 'F:\ticket23-dpi720-export-20260819',
    [string]$ImportRoot = 'F:\ticket23-dpi720-import-20260819'
)

$ErrorActionPreference = 'Stop'

$source = Get-VM -Name $SourceVm
if ($source.State -ne 'Running') {
    throw "Source VM must be running for a live export; actual state: $($source.State)."
}
if (@(Get-VMNetworkAdapter -VM $source | Where-Object SwitchName).Count -ne 0) {
    throw 'Source VM must remain disconnected from every virtual switch.'
}
if (Get-VM -Name $CloneVm -ErrorAction SilentlyContinue) {
    throw "Clone VM already exists: $CloneVm"
}
foreach ($path in @($ExportRoot, $ImportRoot)) {
    if (Test-Path -LiteralPath $path) {
        throw "Clone working path already exists: $path"
    }
}

$sourceId = $source.Id
$sourceDisks = @(Get-VMHardDiskDrive -VMName $SourceVm | Select-Object -ExpandProperty Path)

Write-Host "exporting $SourceVm (live) to $ExportRoot ..."
Export-VM -Name $SourceVm -Path $ExportRoot

$configuration = @(Get-ChildItem -LiteralPath $ExportRoot -Filter '*.vmcx' -Recurse -File |
    Where-Object DirectoryName -Like '*\Virtual Machines')
if ($configuration.Count -ne 1) {
    throw "Expected one exported VMCX, found $($configuration.Count)."
}

New-Item -ItemType Directory -Path $ImportRoot | Out-Null
Write-Host "importing a new-ID copy to $ImportRoot ..."
$imported = Import-VM `
    -Path $configuration[0].FullName `
    -Copy `
    -GenerateNewId `
    -VirtualMachinePath (Join-Path $ImportRoot 'Virtual Machines') `
    -VhdDestinationPath (Join-Path $ImportRoot 'Virtual Hard Disks') `
    -SnapshotFilePath (Join-Path $ImportRoot 'Snapshots')

Rename-VM -VM $imported -NewName $CloneVm
Set-VM -Name $CloneVm -AutomaticStartAction Nothing -AutomaticStopAction ShutDown
Get-VMNetworkAdapter -VMName $CloneVm -ErrorAction SilentlyContinue |
    Disconnect-VMNetworkAdapter
Get-VMDvdDrive -VMName $CloneVm -ErrorAction SilentlyContinue |
    Set-VMDvdDrive -Path $null
if ((Get-VM -Name $CloneVm).State -eq 'Saved') {
    Remove-VMSavedState -VMName $CloneVm
}

$clone = Get-VM -Name $CloneVm
if ($clone.Id -eq $sourceId) {
    throw 'Imported clone retained the source VM ID.'
}
if (@(Get-VMNetworkAdapter -VM $clone | Where-Object SwitchName).Count -ne 0) {
    throw 'Imported clone is connected to a virtual switch.'
}

# The clone must not read or write the live VM's disks.
$cloneDisks = @(Get-VMHardDiskDrive -VMName $CloneVm | Select-Object -ExpandProperty Path)
foreach ($disk in $cloneDisks) {
    if ($sourceDisks -contains $disk) {
        throw "Clone shares a disk with the source VM: $disk"
    }
    if (-not $disk.StartsWith($ImportRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Clone disk is outside the import root: $disk"
    }
}

# Only now, with an isolated copy on disk, give up the calibrated VM's memory.
Write-Host "stopping $SourceVm gracefully to free memory for the clone ..."
Stop-VM -Name $SourceVm
$deadline = (Get-Date).AddMinutes(10)
while ((Get-VM -Name $SourceVm).State -ne 'Off' -and (Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 5
}
if ((Get-VM -Name $SourceVm).State -ne 'Off') {
    throw "$SourceVm did not shut down; refusing to start the clone."
}

Start-VM -Name $CloneVm | Out-Null
$clone = Get-VM -Name $CloneVm

$identity = [pscustomobject]@{
    Purpose          = '720 epx minimum width at 125% and 150%'
    SourceVm         = $SourceVm
    SourceId         = $sourceId
    SourceState      = (Get-VM -Name $SourceVm).State.ToString()
    SourceDisks      = $sourceDisks
    CloneVm          = $CloneVm
    CloneId          = $clone.Id
    CloneState       = $clone.State.ToString()
    CloneDisks       = $cloneDisks
    ExportRoot       = $ExportRoot
    ImportRoot       = $ImportRoot
    NetworkConnected = @(Get-VMNetworkAdapter -VM $clone | Where-Object SwitchName).Count -gt 0
    CreatedAt        = (Get-Date).ToString('o')
}

$out = 'C:\Users\szy\Desktop\8005---AGV\.artifacts\ticket23-dpi\clone-identity-720.json'
$identity | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $out -Encoding utf8
Get-Content -LiteralPath $out
