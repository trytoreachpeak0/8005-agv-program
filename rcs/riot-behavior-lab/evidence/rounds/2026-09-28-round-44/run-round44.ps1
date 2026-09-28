#Requires -Version 7
<#
Round 44: HELD order + software emergency trigger/cancel on the 8005 production RIoT, map 26, spare car only.

One phase per invocation. Every phase prints a verdict and exits:
  0 = matched the expectation written in round-plan.md
  3 = did not match (stop and report; do not run the next phase)
  4 = refused before sending anything (guard failed)

Every HTTP exchange is appended in full to runs/http.ndjson (the bearer token is never written).
Every state sample is appended to runs/samples.ndjson with the phase name.

Safety reflex (approved as part of the plan): whenever a sample taken while the order is
supposed to be stopped shows motion, the phase sends triggerEmergency at once and exits 3.
#>
param(
    [Parameter(Mandatory)][ValidateSet('agv02', 'agv03')][string]$Vehicle,
    [Parameter(Mandatory)]
    [ValidateSet('baseline', 'routecheck', 'create', 'held', 'trigger', 'continue-in-emergency',
        'release', 'observe', 'continue', 'run-to-end', 'cancel-order', 'stop-now', 'final')]
    [string]$Phase,
    [string]$Run = 'A',
    [int]$Destination = 0,
    [int[]]$Candidates = @(),
    [int]$ObserveSeconds = 60,
    [switch]$ExpectResumeAfterRelease
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$BaseUrl = 'http://172.19.206.222:8888'
$MapId = 26
$MapName = '老厂前线new_wk'
$Keys = @{
    agv02 = 'BROKERX-f38975561adf46ccb1d2f23833c7d0e4'
    agv03 = 'BROKERX-7daca4ee91da498d8026c68b7b941127'
}
# agv01 must never be addressed. Refuse it by value, not only by omission from $Keys.
$ForbiddenKeys = @('BROKERX-0c20ff0600d644869a6a80c186065d85')
$Key = $Keys[$Vehicle]
if (-not $Key -or $Key -in $ForbiddenKeys) { Write-Host "REFUSED vehicle key"; exit 4 }

$Token = $env:CONTROL_SERVER_RIOT_CALL_API_KEY
if (-not $Token) { Write-Host 'REFUSED no CONTROL_SERVER_RIOT_CALL_API_KEY'; exit 4 }

$route = Find-NetRoute -RemoteIPAddress 172.19.206.222 | Select-Object -First 1
if ($route.InterfaceAlias -match 'Clash') { Write-Host 'REFUSED route goes through Clash'; exit 4 }

$RunsDir = Join-Path $PSScriptRoot 'runs'
New-Item -ItemType Directory -Force -Path $RunsDir | Out-Null
$HttpLog = Join-Path $RunsDir 'http.ndjson'
$SampleLog = Join-Path $RunsDir 'samples.ndjson'
$StateFile = Join-Path $RunsDir "state-$Run.json"
$PhaseTag = "$Run-$Phase"

function Now { (Get-Date).ToString('yyyy-MM-ddTHH:mm:ss.fffzzz') }

function Write-Line([string]$path, $obj) {
    Add-Content -LiteralPath $path -Value ($obj | ConvertTo-Json -Depth 30 -Compress) -Encoding utf8NoBOM
}

function Invoke-Riot([string]$Method, [string]$Path, [string]$Body = $null) {
    foreach ($fk in $ForbiddenKeys) { if ($Path.Contains($fk) -or ($Body -and $Body.Contains($fk))) { throw 'forbidden vehicle key in request' } }
    if ($Method -ne 'GET' -and -not ($Path.Contains($Key) -or ($Body -and $Body.Contains($Key)) -or $Path -like '/api/task/v1/order/command/*' -or $Path -eq '/api/task/v1/route/getRouteCostsBy')) {
        throw "write request does not name the test vehicle: $Path"
    }
    $sent = Now
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $p = @{ Uri = "$BaseUrl$Path"; Method = $Method; Headers = @{ Authorization = "Bearer $Token" }; SkipHttpErrorCheck = $true; TimeoutSec = 15; NoProxy = $true }
    if ($Body) { $p.Body = [Text.Encoding]::UTF8.GetBytes($Body); $p.ContentType = 'application/json' }
    $status = 0; $text = $null; $err = $null
    try { $r = Invoke-WebRequest @p; $status = [int]$r.StatusCode; $text = $r.Content }
    catch { $err = $_.Exception.Message }
    $sw.Stop()
    $parsed = $null; if ($text) { try { $parsed = $text | ConvertFrom-Json } catch {} }
    Write-Line $HttpLog ([ordered]@{
        phase = $PhaseTag; sentAt = $sent; ms = $sw.ElapsedMilliseconds; method = $Method; path = $Path
        headers = 'Authorization: Bearer <redacted>'; requestBody = $Body
        status = $status; responseBody = $text; error = $err
        code = $parsed.code; message = $parsed.message
    })
    return [pscustomobject]@{ status = $status; parsed = $parsed; error = $err; code = [string]$parsed.code; message = $parsed.message }
}

function Save-State($s) { $s | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $StateFile -Encoding utf8NoBOM }
function Read-State { if (Test-Path $StateFile) { Get-Content $StateFile -Raw | ConvertFrom-Json } else { $null } }

$script:LastPos = $null
function Get-Sample([string]$UpperId, [string]$Event = 'poll') {
    $gi = Invoke-Riot GET "/api/task/v1/task/getVehicleInfo/$Key"
    $card = Invoke-Riot GET "/api/task/vehicles/getVehicleInfoByDeviceKey?key=$Key"
    $det = $null
    if ($UpperId) { $det = (Invoke-Riot GET "/api/order/v1/orderRecord/detailByUpperId/$UpperId").parsed.result }
    $v = $gi.parsed.vehicle; $t = $gi.parsed.vehicleTaskInfo; $c = $card.parsed.result
    $x = $c.position.x; $y = $c.position.y
    $moved = $null
    if ($null -ne $x -and $null -ne $script:LastPos) { $moved = [int][math]::Sqrt([math]::Pow($x - $script:LastPos[0], 2) + [math]::Pow($y - $script:LastPos[1], 2)) }
    if ($null -ne $x) { $script:LastPos = @($x, $y) }
    $s = [ordered]@{
        at = Now; event = $Event; phase = $PhaseTag
        correlation = [ordered]@{ upperId = $UpperId; orderId = $det.orderId; numericId = $det.id; vehicleAlias = $Vehicle }
        observations = [ordered]@{
            readOk = ($gi.status -eq 200 -and $null -ne $v -and $card.code -eq '0')
            orderState = $det.orderState; executingIndex = $det.executingIndex; executeVehicleKey = $det.executeVehicleKey; failReason = $det.failReason
            procState = $t.procState; processingOrder = $t.processingOrder
            emergencyState = $v.emergencyState; controlState = $v.controlState; movementState = $v.movementState
            locationState = $v.locationState; breakSwitchState = $v.breakSwitchState; currentStation = $v.currentStation
            cardSpeed = $c.speed; infoSpeed = $v.speed; x = $x; y = $y; movedMmSincePrev = $moved
            currentMap = $c.currentMap; cardProcState = $c.procState; sysState = $c.sysState; status = $c.status
            cardOrderTaskId = $c.orderTaskId
        }
    }
    Write-Line $SampleLog $s
    $o = $s.observations
    Write-Host ("[{0}] order={1} proc={2} emerg={3} move={4} speed={5}/{6} dxy={7} st={8}" -f $s.at, $o.orderState, $o.procState, $o.emergencyState, $o.movementState, $o.cardSpeed, $o.infoSpeed, $o.movedMmSincePrev, $o.currentStation)
    return $s
}

function Test-Moving($s) {
    $o = $s.observations
    return (($null -ne $o.cardSpeed -and [math]::Abs([double]$o.cardSpeed) -gt 0.005) -or
        ($null -ne $o.infoSpeed -and [math]::Abs([double]$o.infoSpeed) -gt 0.005) -or
        ($null -ne $o.movedMmSincePrev -and $o.movedMmSincePrev -gt 50))
}

function Invoke-DeviceService([string]$ServiceId) {
    $mid = Get-Random -Minimum 100000 -Maximum 999999
    $body = "{`"messageId`":$mid,`"mqCallback`":{`"tag`":`"string`",`"topic`":`"string`"},`"thingsProperties`":{}}"
    return Invoke-Riot POST "/api/device/v1/command/sync/service/$Key/$ServiceId" $body
}

function Stop-Now([string]$Why) {
    Write-Host "SAFETY STOP: $Why -> triggerEmergency"
    $r = Invoke-DeviceService 'triggerEmergency'
    Write-Host "triggerEmergency code=$($r.code) msg=$($r.message)"
    for ($i = 0; $i -lt 10; $i++) { Start-Sleep -Milliseconds 800; $s = Get-Sample $st.upperId 'safety-stop'; if ($s.observations.emergencyState -eq 'CAN_RECOVER') { break } }
    exit 3
}

function Send-OrderCommand([string]$OrderId, [string]$Type) {
    $body = "{`"commandType`":`"$Type`",`"disableVehicle`":false,`"reason`":`"riot-behavior-lab-R44-$PhaseTag`"}"
    return Invoke-Riot POST "/api/task/v1/order/command/$OrderId" $body
}

function Verdict([bool]$ok, [string]$text) {
    Write-Host ("VERDICT {0} {1}: {2}" -f $PhaseTag, ($ok ? 'MATCH' : 'MISMATCH'), $text)
    exit ($ok ? 0 : 3)
}

function Test-Precondition($s) {
    $o = $s.observations
    $bad = @()
    if (-not $o.readOk) { $bad += 'read failed' }
    if ($o.currentMap -ne $MapName) { $bad += "currentMap=$($o.currentMap)" }
    if ($o.locationState -ne 'LOCATION_STATE_RUNNING') { $bad += "locationState=$($o.locationState)" }
    if ($o.emergencyState -ne 'OK') { $bad += "emergencyState=$($o.emergencyState)" }
    if ($o.breakSwitchState -ne 'MOVABLE') { $bad += "breakSwitchState=$($o.breakSwitchState)" }
    if ($o.status -ne 1) { $bad += "status=$($o.status)" }
    if ($o.procState -ne 'IDLE' -or $o.processingOrder) { $bad += "procState=$($o.procState) processing=$($o.processingOrder)" }
    if (-not $o.currentStation -or $o.currentStation -eq 0) { $bad += 'not on a station' }
    if (Test-Moving $s) { $bad += 'moving' }
    return $bad
}

function Get-OpenOrdersForVehicle {
    $r = Invoke-Riot GET '/api/order/v1/orderRecord?pageNum=1&pageSize=200&filterByState=1&filterByState=3&filterByState=7&filterByState=9'
    return @($r.parsed.result.records | Where-Object { $_.appointVehicleKey -eq $Key -or $_.executeVehicleKey -eq $Key })
}

$st = Read-State
Write-Host "Round44 vehicle=$Vehicle run=$Run phase=$Phase route=$($route.InterfaceAlias)"

switch ($Phase) {
    'baseline' {
        $s = Get-Sample $null 'baseline'
        $open = Get-OpenOrdersForVehicle
        $card = (Invoke-Riot GET "/api/task/vehicles/getVehicleInfoByDeviceKey?key=$Key").parsed.result
        $bad = @(Test-Precondition $s)
        if ($open.Count -gt 0) { $bad += "open orders on vehicle: $($open.orderId -join ',')" }
        if (@($card.existedInGroup).Count -gt 0) { $bad += "vehicle is in a dispatch group" }
        Verdict ($bad.Count -eq 0) ($bad.Count ? ($bad -join '; ') : "idle at station $($s.observations.currentStation) on $MapName, no open orders")
    }
    'routecheck' {
        $s = Get-Sample $null 'routecheck'
        $from = $s.observations.currentStation
        foreach ($sid in $Candidates) {
            $r = Invoke-Riot POST '/api/task/v1/route/getRouteCostsBy' (@{ mapId = $MapId; stationId = $sid; deviceKeys = @($Key) } | ConvertTo-Json -Compress)
            $c = @($r.parsed.result.deviceCostsList)[0]
            Write-Host ("from {0} to {1}: costs={2} message={3}" -f $from, $sid, $c.costs, $c.message)
        }
        Verdict $true 'route costs recorded'
    }
    'create' {
        $s = Get-Sample $null 'pre-create'
        $bad = @(Test-Precondition $s)
        if ((Get-OpenOrdersForVehicle).Count -gt 0) { $bad += 'open orders on vehicle' }
        if ($Destination -le 0 -or $Destination -eq $s.observations.currentStation) { $bad += "bad destination $Destination" }
        if ($bad.Count) { Write-Host "REFUSED: $($bad -join '; ')"; exit 4 }
        $uid = "riot-behavior-lab-R44-$Run-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        $payload = @{ appointVehicleKey = $Key; isAppointEnable = 1; lockStatus = 0; orderName = $uid; upperId = $uid
            mission = @(@{ type = 'move'; mapId = $MapId; destination = $Destination }) } | ConvertTo-Json -Depth 6 -Compress
        $cr = Invoke-Riot POST '/api/order/v1/add/byDefaultMissions' $payload
        Save-State ([ordered]@{ upperId = $uid; from = $s.observations.currentStation; destination = $Destination; createdAt = Now; createCode = $cr.code })
        if ($cr.code -ne '0') { Verdict $false "create code=$($cr.code) $($cr.message)" }
        # Expect EXECUTING and real motion (speed or position change) within 90 s.
        $deadline = (Get-Date).AddSeconds(90); $exec = $false; $movedTotal = 0; $last = $null
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 800
            $last = Get-Sample $uid
            $o = $last.observations
            if ($o.executeVehicleKey -and $o.executeVehicleKey -ne '--' -and $o.executeVehicleKey -ne $Key) { Stop-Now "order executed by another vehicle $($o.executeVehicleKey)" }
            if ($o.orderState -in 2, 4, 5, 6) { break }
            if ($o.orderState -eq 3) { $exec = $true; if ($o.movedMmSincePrev) { $movedTotal += $o.movedMmSincePrev } }
            if ($exec -and $movedTotal -ge 300 -and (Test-Moving $last)) { break }
        }
        $st2 = Read-State; $st2 | Add-Member -NotePropertyName orderId -NotePropertyValue $last.correlation.orderId -Force
        $st2 | Add-Member -NotePropertyName numericId -NotePropertyValue $last.correlation.numericId -Force
        Save-State $st2
        Verdict ($exec -and $movedTotal -ge 300) "orderState=$($last.observations.orderState) movedMm=$movedTotal"
    }
    'held' {
        $r = Send-OrderCommand $st.orderId 'CMD_ORDER_HELD'
        Write-Host "HELD code=$($r.code) msg=$($r.message)"
        if ($r.code -ne '0') { Verdict $false "HELD code=$($r.code) $($r.message)" }
        # Expect orderState=7 and standstill within 15 s, then 5 s of stable standstill.
        $deadline = (Get-Date).AddSeconds(15); $okSince = $null; $last = $null
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 800
            $last = Get-Sample $st.upperId
            $o = $last.observations
            if ($o.orderState -eq 7 -and -not (Test-Moving $last)) { $okSince ??= Get-Date; if (((Get-Date) - $okSince).TotalSeconds -ge 5) { break } } else { $okSince = $null }
        }
        $o = $last.observations
        if ($o.orderState -eq 7 -and (Test-Moving $last)) { Stop-Now 'HELD but still moving after 15 s' }
        Verdict ($null -ne $okSince -and ((Get-Date) - $okSince).TotalSeconds -ge 5) "orderState=$($o.orderState) proc=$($o.procState) move=$($o.movementState) speed=$($o.cardSpeed)"
    }
    'trigger' {
        $r = Invoke-DeviceService 'triggerEmergency'
        Write-Host "triggerEmergency code=$($r.code) msg=$($r.message)"
        $deadline = (Get-Date).AddSeconds(15); $last = $null
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 800
            $last = Get-Sample $st.upperId
            if (Test-Moving $last) { Stop-Now 'motion while HELD and emergency requested' }
            if ($last.observations.emergencyState -eq 'CAN_RECOVER') { break }
        }
        # Hold the latched state for 10 s and keep sampling.
        $end = (Get-Date).AddSeconds(10)
        while ((Get-Date) -lt $end) { Start-Sleep -Milliseconds 1000; $last = Get-Sample $st.upperId; if (Test-Moving $last) { Stop-Now 'motion while latched' } }
        $o = $last.observations
        Verdict ($r.code -eq '0' -and $o.emergencyState -eq 'CAN_RECOVER' -and $o.orderState -eq 7) "code=$($r.code) emergency=$($o.emergencyState) orderState=$($o.orderState)"
    }
    'continue-in-emergency' {
        # Run B only: CONTINUE_FROM_HELD while CAN_RECOVER. Any code is a finding; motion is not allowed.
        $r = Send-OrderCommand $st.orderId 'CMD_ORDER_CONTINUE_FROM_HELD'
        Write-Host "CONTINUE_FROM_HELD (latched) code=$($r.code) msg=$($r.message)"
        $end = (Get-Date).AddSeconds(20); $last = $null
        while ((Get-Date) -lt $end) { Start-Sleep -Milliseconds 1000; $last = Get-Sample $st.upperId; if (Test-Moving $last) { Stop-Now 'motion after CONTINUE while latched' } }
        $o = $last.observations
        $st | Add-Member -NotePropertyName continueInEmergency -NotePropertyValue ([ordered]@{ code = $r.code; message = $r.message; orderStateAfter = $o.orderState }) -Force; Save-State $st
        Verdict ($o.emergencyState -eq 'CAN_RECOVER') "code=$($r.code) orderStateAfter=$($o.orderState) emergency=$($o.emergencyState) (any code is a finding)"
    }
    'release' {
        $r = Invoke-DeviceService 'cancelEmergency'
        Write-Host "cancelEmergency code=$($r.code) msg=$($r.message)"
        $deadline = (Get-Date).AddSeconds(15); $last = $null; $okAt = $null
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 800
            $last = Get-Sample $st.upperId
            if (-not $ExpectResumeAfterRelease) {
                if (Test-Moving $last) { Stop-Now 'HELD order moved after cancelEmergency' }
                if ($null -ne $last.observations.orderState -and $last.observations.orderState -ne 7) { Stop-Now "orderState left 7 after cancelEmergency: $($last.observations.orderState)" }
            }
            if ($last.observations.emergencyState -eq 'OK') { $okAt = Now; break }
        }
        $st | Add-Member -NotePropertyName releasedAt -NotePropertyValue $okAt -Force; Save-State $st
        Verdict ($r.code -eq '0' -and $null -ne $okAt) "code=$($r.code) emergency=$($last.observations.emergencyState) orderState=$($last.observations.orderState)"
    }
    'observe' {
        # After release: order must stay 7 and the vehicle must stay still for the whole window.
        $end = (Get-Date).AddSeconds($ObserveSeconds); $last = $null; $n = 0; $states = @{}
        while ((Get-Date) -lt $end) {
            Start-Sleep -Milliseconds 1000
            $last = Get-Sample $st.upperId 'observe'; $n++
            $states["$($last.observations.orderState)"] = 1 + ($states["$($last.observations.orderState)"] ?? 0)
            if (Test-Moving $last) { Stop-Now 'HELD order moved during post-release observation' }
            if ($last.observations.orderState -ne 7) { Stop-Now "orderState left 7 during observation: $($last.observations.orderState)" }
            if ($last.observations.emergencyState -ne 'OK') { Verdict $false "emergencyState=$($last.observations.emergencyState)" }
        }
        Verdict $true "samples=$n orderStates=$(($states.GetEnumerator() | ForEach-Object { "$($_.Key):$($_.Value)" }) -join ',') all still"
    }
    'continue' {
        $r = Send-OrderCommand $st.orderId 'CMD_ORDER_CONTINUE_FROM_HELD'
        Write-Host "CONTINUE_FROM_HELD code=$($r.code) msg=$($r.message)"
        $deadline = (Get-Date).AddSeconds(20); $last = $null; $moved = 0
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 800
            $last = Get-Sample $st.upperId
            if ($last.observations.movedMmSincePrev) { $moved += $last.observations.movedMmSincePrev }
            if ($last.observations.orderState -eq 3 -and $moved -ge 300) { break }
            if ($last.observations.orderState -in 2, 4, 5, 6) { break }
        }
        Verdict ($r.code -eq '0' -and $last.observations.orderState -eq 3 -and $moved -ge 300) "code=$($r.code) orderState=$($last.observations.orderState) movedMm=$moved"
    }
    'run-to-end' {
        $deadline = (Get-Date).AddSeconds(240); $last = $null
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 1200
            $last = Get-Sample $st.upperId
            if ($last.observations.orderState -in 2, 4, 5, 6, 7, 9) { break }
        }
        $o = $last.observations
        Verdict ($o.orderState -eq 5 -and $o.currentStation -eq $st.destination) "orderState=$($o.orderState) station=$($o.currentStation) dest=$($st.destination)"
    }
    'cancel-order' {
        $r = Send-OrderCommand $st.orderId 'CMD_ORDER_CANCEL'
        Write-Host "CANCEL code=$($r.code) msg=$($r.message)"
        Start-Sleep -Seconds 3
        $last = Get-Sample $st.upperId 'post-cancel'
        Verdict ($last.observations.orderState -eq 2) "orderState=$($last.observations.orderState) proc=$($last.observations.procState)"
    }
    'stop-now' { Stop-Now 'manual safety stop' }
    'final' {
        $s = Get-Sample $st.upperId 'final'
        $open = Get-OpenOrdersForVehicle
        $o = $s.observations
        Verdict ($open.Count -eq 0 -and $o.emergencyState -eq 'OK' -and $o.procState -eq 'IDLE' -and -not (Test-Moving $s)) "open=$($open.Count) emergency=$($o.emergencyState) proc=$($o.procState) station=$($o.currentStation)"
    }
}
