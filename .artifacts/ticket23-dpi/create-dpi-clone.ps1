# Ticket 23 DPI validation, step 1: export the calibrated VM and import a disposable
# clone with a new VM ID, offline. The calibrated gpt_win11 desktop is never re-scaled;
# 125% and 150% are exercised only inside this clone, which is destroyed afterwards.
$ErrorActionPreference = 'Stop'

$sourceVm = 'gpt_win11'
$cloneVm = 'gpt_win11_ticket23_dpi'
$exportRoot = 'F:\ticket23-dpi-export-20260819'
$importRoot = 'F:\ticket23-dpi-import-20260819'

$source = Get-VM -Name $sourceVm
if ($source.State -ne 'Running') {
    throw "Source VM must be running before a live export; actual state: $($source.State)."
}
if (@(Get-VMNetworkAdapter -VM $source | Where-Object SwitchName).Count -ne 0) {
    throw 'Source VM must remain disconnected from every virtual switch.'
}
if (Get-VM -Name $cloneVm -ErrorAction SilentlyContinue) {
    throw "Clone VM already exists: $cloneVm"
}
foreach ($path in @($exportRoot, $importRoot)) {
    if (Test-Path -LiteralPath $path) {
        throw "Clone working path already exists: $path"
    }
}

$sourceId = $source.Id
$sourceDisks = @(Get-VMHardDiskDrive -VMName $sourceVm | Select-Object -ExpandProperty Path)

Export-VM -Name $sourceVm -Path $exportRoot

$configuration = @(Get-ChildItem -LiteralPath $exportRoot -Filter '*.vmcx' -Recurse -File |
    Where-Object DirectoryName -Like '*\Virtual Machines')
if ($configuration.Count -ne 1) {
    throw "Expected one exported VMCX, found $($configuration.Count)."
}

New-Item -ItemType Directory -Path $importRoot | Out-Null
$imported = Import-VM `
    -Path $configuration[0].FullName `
    -Copy `
    -GenerateNewId `
    -VirtualMachinePath (Join-Path $importRoot 'Virtual Machines') `
    -VhdDestinationPath (Join-Path $importRoot 'Virtual Hard Disks') `
    -SnapshotFilePath (Join-Path $importRoot 'Snapshots')

Rename-VM -VM $imported -NewName $cloneVm
Set-VM -Name $cloneVm -AutomaticStartAction Nothing -AutomaticStopAction ShutDown
Get-VMNetworkAdapter -VMName $cloneVm -ErrorAction SilentlyContinue |
    Disconnect-VMNetworkAdapter
Get-VMDvdDrive -VMName $cloneVm -ErrorAction SilentlyContinue |
    Set-VMDvdDrive -Path $null
if ((Get-VM -Name $cloneVm).State -eq 'Saved') {
    Remove-VMSavedState -VMName $cloneVm
}

$clone = Get-VM -Name $cloneVm
if ($clone.Id -eq $sourceId) {
    throw 'Imported clone retained the source VM ID.'
}
if (@(Get-VMNetworkAdapter -VM $clone | Where-Object SwitchName).Count -ne 0) {
    throw 'Imported clone is connected to a virtual switch.'
}

# The clone must not read or write the live VM's disks.
$cloneDisks = @(Get-VMHardDiskDrive -VMName $cloneVm | Select-Object -ExpandProperty Path)
foreach ($disk in $cloneDisks) {
    if ($sourceDisks -contains $disk) {
        throw "Clone shares a disk with the source VM: $disk"
    }
    if (-not $disk.StartsWith($importRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Clone disk is outside the import root: $disk"
    }
}

Start-VM -Name $cloneVm | Out-Null
$clone = Get-VM -Name $cloneVm

$identity = [pscustomobject]@{
    SourceVm         = $sourceVm
    SourceId         = $sourceId
    SourceDisks      = $sourceDisks
    CloneVm          = $cloneVm
    CloneId          = $clone.Id
    CloneState       = $clone.State.ToString()
    CloneDisks       = $cloneDisks
    ExportRoot       = $exportRoot
    ImportRoot       = $importRoot
    NetworkConnected = @(Get-VMNetworkAdapter -VM $clone | Where-Object SwitchName).Count -gt 0
    CreatedAt        = (Get-Date).ToString('o')
}

$out = 'C:\Users\szy\Desktop\8005---AGV\.artifacts\ticket23-dpi\clone-identity.json'
$identity | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $out -Encoding utf8
Get-Content -LiteralPath $out
