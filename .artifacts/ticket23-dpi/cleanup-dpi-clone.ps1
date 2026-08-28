# Ticket 23 DPI validation, step 4: destroy the disposable clone and its exact working
# directories, then record the calibrated VM's state.
#
# Scoping matters here. The live gpt_win11 disk sits under F:\ticket23-font-import-20260818
# (today's golden machine IS the promoted clone from the earlier font session), so a broad
# "remove the clone directories" would destroy the golden machine. This script removes only
# the two roots it is given, and refuses if the live VM has any disk underneath them.
#
# The target is mandatory rather than defaulted. Defaults here named one specific attempt's
# clone and roots, so a later run would either silently do nothing or, worse, aim at the
# wrong attempt. Naming the target is the point of the script.
param(
    [Parameter(Mandatory = $true)][string]$CloneVm,
    [Parameter(Mandatory = $true)][string]$ExportRoot,
    [Parameter(Mandatory = $true)][string]$ImportRoot,
    [string]$SourceVm = 'gpt_win11',

    # Distinguishes this attempt's record. Evidence is never overwritten - the first rerun of
    # this script clobbered the committed clone-cleanup.json of the earlier 1440x900 DPI
    # phase, which had to be restored from git.
    [string]$Label = ''
)

$ErrorActionPreference = 'Stop'

# Decide where the record goes and refuse a collision BEFORE destroying anything. The first
# version of this guard sat at the end, so it would have thrown only after the VM and both
# directories were gone - losing the record of the very thing it had just done.
$suffix = if ([string]::IsNullOrWhiteSpace($Label)) { '' } else { "-$Label" }
$out = "C:\Users\szy\Desktop\8005---AGV\.artifacts\ticket23-dpi\clone-cleanup$suffix.json"
if (Test-Path -LiteralPath $out) {
    throw "Refusing to overwrite existing evidence: $out. Pass a -Label for this attempt."
}

function Test-PathContains {
    # Prefix comparison on a directory boundary. A bare StartsWith would let a root of
    # 'F:\ticket23-dpi' claim a disk sitting in 'F:\ticket23-dpi-export-...'.
    param([string]$Root, [string]$Candidate)

    $normalized = [IO.Path]::GetFullPath($Root).TrimEnd([IO.Path]::DirectorySeparatorChar) +
        [IO.Path]::DirectorySeparatorChar
    return [IO.Path]::GetFullPath($Candidate).StartsWith(
        $normalized, [StringComparison]::OrdinalIgnoreCase)
}

$sourceDisks = @(Get-VMHardDiskDrive -VMName $SourceVm | Select-Object -ExpandProperty Path)
foreach ($root in @($ExportRoot, $ImportRoot)) {
    foreach ($disk in $sourceDisks) {
        if (Test-PathContains -Root $root -Candidate $disk) {
            throw "Refusing to delete $root - the live $SourceVm has a disk under it: $disk"
        }
    }
}

# The clone must actually live under the roots being deleted, otherwise this invocation is
# pointed at the wrong attempt and would remove a VM while leaving its disks behind.
$clonePreflight = Get-VM -Name $CloneVm -ErrorAction SilentlyContinue
if ($null -ne $clonePreflight) {
    foreach ($disk in @(Get-VMHardDiskDrive -VMName $CloneVm | Select-Object -ExpandProperty Path)) {
        if (-not (Test-PathContains -Root $ImportRoot -Candidate $disk)) {
            throw "Refusing to proceed - $CloneVm has a disk outside $ImportRoot`: $disk"
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

# The calibrated VM must be untouched: still disconnected, still on its own disks. Its power
# state is recorded rather than asserted - the 720 epx phase deliberately left it Off,
# because the host cannot hold two 4 GB VMs at once.
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

$record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $out -Encoding utf8
Get-Content -LiteralPath $out
