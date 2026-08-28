$ErrorActionPreference = 'Stop'

$sourceVm = 'gpt_win11'
$cloneVm = 'gpt_win11_ticket11_dpi125'
$exportRoot = 'F:\ticket11-dpi125-export-20260810-0252'
$importRoot = 'F:\ticket11-dpi125-import-20260810-0252'

if (Get-VM -Name $cloneVm -ErrorAction SilentlyContinue) {
    throw "Clone VM already exists: $cloneVm"
}
if (Test-Path -LiteralPath $importRoot) {
    throw "Clone import path already exists: $importRoot"
}

if (-not (Test-Path -LiteralPath $exportRoot)) {
    Write-Output "EXPORT_START $sourceVm -> $exportRoot"
    Export-VM -Name $sourceVm -Path $exportRoot
    Write-Output 'EXPORT_DONE'
}
else {
    Write-Output "EXPORT_REUSE $exportRoot"
}

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
Start-VM -Name $cloneVm

[pscustomobject]@{
    CloneVm = $cloneVm
    State = (Get-VM -Name $cloneVm).State.ToString()
    ExportRoot = $exportRoot
    ImportRoot = $importRoot
    NetworkConnected = @(Get-VMNetworkAdapter -VMName $cloneVm |
        Where-Object SwitchName).Count -gt 0
}
