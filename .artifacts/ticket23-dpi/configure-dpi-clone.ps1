# Ticket 23 DPI validation, step 2: set the clone's scaling and restart it.
#
# PowerShell Direct is used only to write the setting and to confirm the VM came back.
# It is deliberately NOT the proof of effective DPI: per docs/agents/golden-renderer.md a
# registry value read this way does not establish what the interactive desktop actually
# renders at. The proof is the interactive environment report produced inside the run by
# Test-GoldenRendererEnvironment.ps1 with -ExpectedDpi.
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(120, 144)]
    [int]$Dpi,

    [string]$CloneVm = 'gpt_win11_ticket23_dpi'
)

$ErrorActionPreference = 'Stop'

$scalePercent = switch ($Dpi) { 120 { 125 } 144 { 150 } }

$credential = Import-Clixml -LiteralPath `
    "$env:LOCALAPPDATA\MesIngestWatch\gpt_win11.credential.xml"

function Wait-CloneSession {
    param([string]$Name, [int]$Minutes = 12)
    $deadline = (Get-Date).AddMinutes($Minutes)
    do {
        Start-Sleep -Seconds 5
        try { $s = New-PSSession -VMName $Name -Credential $credential -ErrorAction Stop }
        catch { $s = $null }
    } while ($null -eq $s -and (Get-Date) -lt $deadline)
    if ($null -eq $s) { throw "PowerShell Direct did not become available for $Name." }
    return $s
}

$clone = Get-VM -Name $CloneVm
if (@(Get-VMNetworkAdapter -VM $clone | Where-Object SwitchName).Count -ne 0) {
    throw 'Refusing to configure a clone that is connected to a virtual switch.'
}

$session = Wait-CloneSession -Name $CloneVm
try {
    Invoke-Command -Session $session -ScriptBlock {
        param($logPixels)
        $desktop = 'HKCU:\Control Panel\Desktop'
        Set-ItemProperty -LiteralPath $desktop -Name Win8DpiScaling -Type DWord -Value 1
        Set-ItemProperty -LiteralPath $desktop -Name LogPixels -Type DWord -Value $logPixels
        Restart-Computer -Force
    } -ArgumentList $Dpi
}
catch {
    # Restart-Computer tears the session down; that is expected and not a failure.
    Write-Host "restart issued (session dropped): $($_.Exception.Message)"
}
finally {
    Remove-PSSession $session -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 20
$probe = Wait-CloneSession -Name $CloneVm
try {
    $state = Invoke-Command -Session $probe -ScriptBlock {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
        $desktopKey = Get-ItemProperty -LiteralPath 'HKCU:\Control Panel\Desktop'
        [pscustomobject]@{
            Hostname         = $env:COMPUTERNAME
            ExplorerSessions = @(Get-Process explorer -ErrorAction SilentlyContinue |
                Select-Object -ExpandProperty SessionId)
            LogPixels        = $desktopKey.LogPixels
            Win8DpiScaling   = $desktopKey.Win8DpiScaling
        }
    }
}
finally {
    Remove-PSSession $probe
}

$record = [pscustomobject]@{
    CloneVm              = $CloneVm
    CloneId              = (Get-VM -Name $CloneVm).Id
    RequestedDpi         = $Dpi
    RequestedScalePercent = $scalePercent
    RegistryLogPixels    = $state.LogPixels
    RegistryWin8DpiScaling = $state.Win8DpiScaling
    ExplorerSessions     = $state.ExplorerSessions
    Hostname             = $state.Hostname
    NetworkConnected     = @(Get-VMNetworkAdapter -VMName $CloneVm | Where-Object SwitchName).Count -gt 0
    ConfiguredAt         = (Get-Date).ToString('o')
    EffectiveDpiProof    = 'Pending: the interactive environment report inside the run is the proof, not this record.'
}

if ($record.RegistryLogPixels -ne $Dpi) {
    throw "Clone LogPixels is $($record.RegistryLogPixels), expected $Dpi."
}
if (@($record.ExplorerSessions).Count -eq 0) {
    throw 'Clone has no Explorer session after the DPI restart.'
}

$out = "C:\Users\szy\Desktop\8005---AGV\.artifacts\ticket23-dpi\clone-configured-$Dpi.json"
$record | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $out -Encoding utf8
Get-Content -LiteralPath $out
