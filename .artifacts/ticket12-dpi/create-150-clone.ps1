$ErrorActionPreference = 'Stop'

$sourceVm = 'gpt_win11'
$cloneVm = 'gpt_win11_ticket12_dpi150'
$exportRoot = 'F:\ticket12-dpi150-export-20260810-0950'
$importRoot = 'F:\ticket12-dpi150-import-20260810-0950'

if (Get-VM -Name $cloneVm -ErrorAction SilentlyContinue) {
    throw "Clone VM already exists: $cloneVm"
}
if (Test-Path -LiteralPath $exportRoot) {
    throw "Export path already exists: $exportRoot"
}
if (Test-Path -LiteralPath $importRoot) {
    throw "Import path already exists: $importRoot"
}

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
# The source VM is exported live and has installation media attached. The clone must
# cold-boot without inheriting either the saved runtime state or the host-user ISO path.
Get-VMDvdDrive -VMName $cloneVm -ErrorAction SilentlyContinue |
    Set-VMDvdDrive -Path $null
if ((Get-VM -Name $cloneVm).State -eq 'Saved') {
    Remove-VMSavedState -VMName $cloneVm
}
Start-VM -Name $cloneVm

[pscustomobject]@{
    CloneVm = $cloneVm
    State = (Get-VM -Name $cloneVm).State.ToString()
    ExportRoot = $exportRoot
    ImportRoot = $importRoot
    NetworkConnected = @(Get-VMNetworkAdapter -VMName $cloneVm |
        Where-Object SwitchName).Count -gt 0
}
