# Ticket 23 DPI validation, step 4: destroy the disposable clone and its exact working
# directories, then re-verify the calibrated VM.
#
# Scoping matters here. The live gpt_win11 disk sits under F:\ticket23-font-import-20260818
# (today's golden machine IS the promoted clone from the earlier font session), so a broad
# "remove the clone directories" would destroy the golden machine. This script removes only
# the two paths it created, and refuses if the live VM has any disk underneath them.
param(
    [string]$CloneVm = 'gpt_win11_ticket23_dpi',
    [string]$SourceVm = 'gpt_win11',
    [string]$ExportRoot = 'F:\ticket23-dpi-export-20260819',
    [string]$ImportRoot = 'F:\ticket23-dpi-import-20260819',

    # Distinguishes this attempt's record. Evidence is never overwritten - the first run of
    # this script clobbered the committed clone-cleanup.json of the earlier 1440x900 DPI
    # phase, which had to be restored from git.
    [string]$Label = ''
)

$ErrorActionPreference = 'Stop'

$sourceDisks = @(Get-VMHardDiskDrive -VMName $SourceVm | Select-Object -ExpandProperty Path)
foreach ($root in @($ExportRoot, $ImportRoot)) {
    foreach ($disk in $sourceDisks) {
        if ($disk.StartsWith($root, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to delete $root - the live $SourceVm has a disk under it: $disk"
        }
    }
}

$removed = [ordered]@{}

$clone = Get-VM -Name $CloneVm -ErrorAction SilentlyContinue
if ($null -ne $clone) {
    $removed['CloneId'] = $clone.Id.ToString()
    if ($clone.State -ne 'Off') {
        Stop-VM -Name $CloneVm -TurnOff -Force
    }
    $waited = 0
    while ((Get-VM -Name $CloneVm).State -ne 'Off' -and $waited -lt 60) {
        Start-Sleep -Seconds 2
        $waited += 2
    }
    Remove-VM -Name $CloneVm -Force
    $removed['CloneRemoved'] = $true
} else {
    $removed['CloneRemoved'] = 'already absent'
}

foreach ($root in @($ExportRoot, $ImportRoot)) {
    if (Test-Path -LiteralPath $root) {
        Remove-Item -LiteralPath $root -Recurse -Force
    }
    $removed[$root] = -not (Test-Path -LiteralPath $root)
}

# The calibrated VM must be untouched: still running, still offline, still on its own disks.
$source = Get-VM -Name $SourceVm
$sourceState = [pscustomobject]@{
    Name             = $source.Name
    Id               = $source.Id
    State            = $source.State.ToString()
    ProcessorCount   = $source.ProcessorCount
    NetworkConnected = @(Get-VMNetworkAdapter -VM $source | Where-Object SwitchName).Count -gt 0
    Disks            = @(Get-VMHardDiskDrive -VMName $SourceVm | Select-Object -ExpandProperty Path)
    DisksPresent     = @(Get-VMHardDiskDrive -VMName $SourceVm |
        ForEach-Object { Test-Path -LiteralPath $_.Path })
}

$record = [pscustomobject]@{
    CleanedAt        = (Get-Date).ToString('o')
    CloneVm          = $CloneVm
    Removed          = $removed
    SourceVm         = $sourceState
    RemainingDpiVms  = @(Get-VM | Where-Object Name -like '*ticket23_dpi*' |
        Select-Object -ExpandProperty Name)
}

$suffix = if ([string]::IsNullOrWhiteSpace($Label)) { '' } else { "-$Label" }
$out = "C:\Users\szy\Desktop\8005---AGV\.artifacts\ticket23-dpi\clone-cleanup$suffix.json"
if (Test-Path -LiteralPath $out) {
    throw "Refusing to overwrite existing evidence: $out"
}
$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $out -Encoding utf8
Get-Content -LiteralPath $out
