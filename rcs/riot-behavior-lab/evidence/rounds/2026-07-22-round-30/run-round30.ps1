$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$http = [System.Net.Http.HttpClient]::new()
$http.Timeout = [TimeSpan]::FromSeconds(25)
$key = 'BROKERX-aee2f93d717546cf9510c98c854fe83e'
$mapId = 30
$phase = if($args.Count -ge 1){ $args[0] } else { 'baseline' }
Write-Host "Round30 loc/far-path phase=$phase key=$key mapId=$mapId"

function Invoke-Api([string]$method,[string]$url,[string]$json){
  $r=New-Object System.Net.Http.HttpRequestMessage
  $r.Method=[System.Net.Http.HttpMethod]::new($method)
  $r.RequestUri=$url
  [void]$r.Headers.TryAddWithoutValidation("Authorization","Bearer $($e.callApiKey)")
  if(-not [string]::IsNullOrEmpty($json)){ $r.Content=New-Object System.Net.Http.StringContent($json,[System.Text.Encoding]::UTF8,"application/json") }
  try {
    $resp=$http.SendAsync($r).GetAwaiter().GetResult()
    $body=[System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
    $parsed=$null; try{ $parsed=$body|ConvertFrom-Json }catch{}
    return [pscustomobject]@{ok=$true; status=[int]$resp.StatusCode; body=$body; parsed=$parsed; error=$null}
  } catch {
    return [pscustomobject]@{ok=$false; status=0; body=$null; parsed=$null; error=$_.Exception.Message}
  }
}
function Save($n,$o){ [System.IO.File]::WriteAllText((Join-Path $outDir $n), ($o|ConvertTo-Json -Depth 24), $utf8) }
function CodeOk($p){ return ($p -and ($p.code -eq '0' -or $p.code -eq 0)) }

function Get-Snap([string]$upperId){
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $v=$null; $vti=$null
  if($gi.parsed){ $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo }
  $det=$null; $missions=$null
  if($upperId){
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$upperId" $null
    $det=$by.parsed.result
    if($det -and $det.orderId){
      $mi=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/missionList/$($det.orderId)" $null
      $missions=$mi.parsed.result
    }
  }
  $x=$null; $y=$null; $theta=$null; $conf=$null; $noStation=$null
  if($v){
    $x=$v.x; $y=$v.y; $theta=$v.theta; $conf=$v.confidence; $noStation=$v.noStation
    if($null -eq $x -and $v.previousState){ $x=$v.previousState.x; $y=$v.previousState.y; $theta=$v.previousState.theta }
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$(if($v){$v.currentStation}else{$null})
    noStation=$noStation
    mapName=$(if($v -and $v.previousState){$v.previousState.mapName}else{$null})
    x=$x; y=$y; theta=$theta; confidence=$conf
    movementState=$(if($v){[string]$v.movementState}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    emergencyState=$(if($v){[string]$v.emergencyState}else{$null})
    breakSwitchState=$(if($v){[string]$v.breakSwitchState}else{$null})
    locationState=$(if($v){[string]$v.locationState}else{$null})
    faultCodes=$(if($v){$v.faultCodes}else{$null})
    speed=$(if($v){$v.speed}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    integrationLevel=$(if($vti){[string]$vti.integrationLevel}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    appointVehicleKey=$(if($det){$det.appointVehicleKey}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    missions=$missions
  }
}

function Pick-Dest($cur){
  foreach($sid in @(3,2,1,5,6,4)){
    if($null -ne $cur -and $sid -eq $cur){ continue }
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)}|ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$null; $msg=$null
    if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
    if($c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){ return [pscustomobject]@{dest=[int]$sid; cost=$c0; message=$msg} }
  }
  return [pscustomobject]@{dest=3; cost=-1; message='fallback'}
}

function New-Move([string]$tag,$dest){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R30-$tag-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$dest}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  return [pscustomobject]@{uid=$uid; dest=$dest; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body; parsed=$cr.parsed; req=$json}
}

function Cancel-Order([string]$oid,$nid,[string]$reason){
  $attempts=@()
  if($oid){
    $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
    $attempts += [ordered]@{api='command'; code=$cmd.parsed.code; message=$cmd.parsed.message}
  }
  if($nid){
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" "{`"orderId`":$nid,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $attempts += [ordered]@{api='operate'; code=$op.parsed.code; message=$op.parsed.message}
  }
  return $attempts
}

function Continue-Hang([string]$oid){
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CONTINUE_FROM_HANG`",`"disableVehicle`":false,`"reason`":`"R30-continue`"}"
  return [ordered]@{code=$r.parsed.code; message=$r.parsed.message; body=$r.body}
}

function Invoke-StopLocation(){
  $url="$($e.baseUrl)/api/task/vehicles/stopLocation?vehicleKey=$([uri]::EscapeDataString($key))"
  $r=Invoke-Api POST $url $null
  return [ordered]@{url=$url; status=$r.status; code=$r.parsed.code; message=$r.parsed.message; body=$r.body; error=$r.error}
}

function Invoke-StartLocation([string]$stationNo){
  $url="$($e.baseUrl)/api/task/vehicles/startLocation?vehicleKey=$([uri]::EscapeDataString($key))&stationNo=$stationNo"
  $r=Invoke-Api POST $url $null
  return [ordered]@{url=$url; stationNo=$stationNo; status=$r.status; code=$r.parsed.code; message=$r.parsed.message; body=$r.body; error=$r.error}
}

if($phase -eq 'baseline'){
  $s=Get-Snap $null
  Save 'E0-baseline.json' $s
  Write-Host ("BASE st={0} loc={1} emerg={2} break={3} proc={4} processing={5} xy=({6},{7})" -f $s.station,$s.locationState,$s.emergencyState,$s.breakSwitchState,$s.procState,$s.processingOrder,$s.x,$s.y)
  $http.Dispose(); return
}

if($phase -eq 'wait-condition'){
  $kind = if($args.Count -ge 2){ $args[1] } else { throw 'need kind L|D' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 180 }
  Write-Host "=== wait-condition kind=$kind timeout=${timeoutSec}s ==="
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    $s=Get-Snap $null
    $samples += $s
    Write-Host ("[{0}] loc={1} ctrl={2} st={3} xy=({4},{5}) proc={6}" -f $s.at,$s.locationState,$s.controlState,$s.station,$s.x,$s.y,$s.procState)
    if($kind -eq 'L' -and $s.locationState -and $s.locationState -ne 'LOCATION_STATE_RUNNING'){ $hit=$true; break }
    if($kind -eq 'D'){
      # D: still localized, but human confirms far-from-path; we detect stable localized + wait for external confirm via arg
      # Here we just wait until localized remains and user has had time; caller sets short timeout after human says ready
      if($s.locationState -eq 'LOCATION_STATE_RUNNING'){ $hit=$true; break }
    }
    Start-Sleep -Milliseconds 800
  }
  Save ("$kind-wait-condition.json") ([ordered]@{hit=$hit; kind=$kind; last=$samples[-1]; samples=$samples})
  if(-not $hit){ Write-Host 'NO_CONDITION'; $http.Dispose(); exit 2 }
  Write-Host 'CONDITION_HIT'
  $http.Dispose(); return
}

if($phase -eq 'api-stop'){
  $before=Get-Snap $null
  Save 'L-api-stop-before.json' $before
  $r=Invoke-StopLocation
  Save 'L-api-stop-call.json' $r
  Start-Sleep -Seconds 2
  $after=Get-Snap $null
  Save 'L-api-stop-after.json' $after
  Write-Host ("stopLocation code={0} loc={1}->{2}" -f $r.code,$before.locationState,$after.locationState)
  $http.Dispose(); return
}

if($phase -eq 'api-start'){
  $stationNo = if($args.Count -ge 2){ $args[1] } else { '1' }
  $before=Get-Snap $null
  Save 'L-api-start-before.json' $before
  $r=Invoke-StartLocation $stationNo
  Save 'L-api-start-call.json' $r
  Start-Sleep -Seconds 3
  $after=Get-Snap $null
  Save 'L-api-start-after.json' $after
  Write-Host ("startLocation code={0} loc={1}->{2} st={3}" -f $r.code,$before.locationState,$after.locationState,$after.station)
  $http.Dispose(); return
}

if($phase -eq 'create-watch'){
  $tag = if($args.Count -ge 2){ $args[1] } else { throw 'need tag' }
  $watchSec = if($args.Count -ge 3){ [int]$args[2] } else { 120 }
  $before=Get-Snap $null
  Save ("$tag-before-create.json") $before
  $pick=Pick-Dest $before.station
  Save ("$tag-dest.json") $pick
  Write-Host ("dest={0} cost={1} loc={2} st={3} xy=({4},{5})" -f $pick.dest,$pick.cost,$before.locationState,$before.station,$before.x,$before.y)
  $cr=New-Move $tag $pick.dest
  Save ("$tag-create.json") ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.code) $($cr.message)" }
  Write-Host "CREATED uid=$($cr.uid)"
  $samples=@()
  $hitExec=$false; $hitHang=$false; $hitTerminal=$false
  $deadline=(Get-Date).AddSeconds($watchSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 900
    $s=Get-Snap $cr.uid
    $samples += $s
    $m0=$null
    if($s.missions -and $s.missions.Count -gt 0){ $m0=$s.missions[0] }
    Write-Host ("[{0}] order={1} execKey={2} loc={3} proc={4} fail={5} mResult={6}" -f $s.at,$s.orderState,$s.executeVehicleKey,$s.locationState,$s.procState,$s.failReason,$(if($m0){$m0.resultCode}else{$null}))
    if($s.orderState -eq 3){ $hitExec=$true }
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -in @(2,4,5,6)){ $hitTerminal=$true; break }
  }
  $last=$samples[-1]
  $summary=[ordered]@{
    tag=$tag; uid=$cr.uid
    beforeLoc=$before.locationState; beforeStation=$before.station; beforeXY=@($before.x,$before.y)
    dest=$pick.dest; destCost=$pick.cost
    createCode=$cr.code
    hitExec=$hitExec; hitHang=$hitHang; hitTerminal=$hitTerminal
    stayedQueueing = ($last.orderState -eq 1)
    finalOrderState=$last.orderState
    finalExecKey=$last.executeVehicleKey
    finalLoc=$last.locationState
    finalProc=$last.procState
    finalFail=$last.failReason
    watchSec=$watchSec
  }
  Save ("$tag-watch-samples.json") $samples
  Save ("$tag-summary.json") $summary
  Write-Host ("RESULT hitExec={0} hitHang={1} stayedQueue={2} finalOrder={3}" -f $hitExec,$hitHang,$summary.stayedQueueing,$last.orderState)
  $http.Dispose(); return
}

if($phase -eq 'create-then-wait-exec'){
  # create while normal, wait until EXECUTING then return uid for mid-exec trigger
  $tag = if($args.Count -ge 2){ $args[1] } else { throw 'need tag' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 60 }
  $before=Get-Snap $null
  Save ("$tag-exec-before.json") $before
  $pick=Pick-Dest $before.station
  Save ("$tag-exec-dest.json") $pick
  $cr=New-Move $tag $pick.dest
  Save ("$tag-exec-create.json") ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.code) $($cr.message)" }
  Write-Host "CREATED uid=$($cr.uid) dest=$($pick.dest)"
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} loc={2} move={3} proc={4}" -f $s.at,$s.orderState,$s.locationState,$s.movementState,$s.procState)
    if($s.orderState -eq 3){ $hit=$true; break }
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save ("$tag-exec-wait-samples.json") $samples
  Save ("$tag-exec-wait-summary.json") ([ordered]@{uid=$cr.uid; hitExec=$hit; finalOrderState=$samples[-1].orderState})
  if(-not $hit){ Write-Host 'NO_EXEC'; $http.Dispose(); exit 2 }
  Write-Host "EXEC_HIT uid=$($cr.uid)"
  $http.Dispose(); return
}

if($phase -eq 'hang-watch'){
  $tag = if($args.Count -ge 2){ $args[1] } else { throw 'need tag' }
  $uid = if($args.Count -ge 3){ $args[2] } else { throw 'need uid' }
  $watchSec = if($args.Count -ge 4){ [int]$args[3] } else { 180 }
  Write-Host "=== hang-watch tag=$tag uid=$uid sec=$watchSec ==="
  $samples=@(); $hitHang=$false; $hitTerminal=$false
  $deadline=(Get-Date).AddSeconds($watchSec)
  while((Get-Date) -lt $deadline){
    $s=Get-Snap $uid
    $samples += $s
    $m0=$null
    if($s.missions -and $s.missions.Count -gt 0){ $m0=$s.missions[0] }
    Write-Host ("[{0}] order={1} loc={2} proc={3} fail={4} mResult={5} progress={6}" -f $s.at,$s.orderState,$s.locationState,$s.procState,$s.failReason,$(if($m0){$m0.resultCode}else{$null}),$s.progress)
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -in @(2,4,5,6)){ $hitTerminal=$true; break }
    Start-Sleep -Milliseconds 1000
  }
  $last=$samples[-1]
  Save ("$tag-hang-samples.json") $samples
  Save ("$tag-hang-summary.json") ([ordered]@{
    tag=$tag; uid=$uid; hitHang=$hitHang; hitTerminal=$hitTerminal
    finalOrderState=$last.orderState; finalLoc=$last.locationState
    finalFail=$last.failReason; finalProc=$last.procState; watchSec=$watchSec
  })
  Write-Host ("RESULT hitHang={0} finalOrder={1}" -f $hitHang,$last.orderState)
  $http.Dispose(); return
}

if($phase -eq 'continue-probe'){
  $tag = if($args.Count -ge 2){ $args[1] } else { throw 'need tag' }
  $uid = if($args.Count -ge 3){ $args[2] } else { throw 'need uid' }
  $s=Get-Snap $uid
  Save ("$tag-cont-before.json") $s
  if(-not $s.orderId){ throw 'no orderId' }
  $c=Continue-Hang $s.orderId
  Save ("$tag-cont-call.json") $c
  Start-Sleep -Seconds 2
  $after=Get-Snap $uid
  Save ("$tag-cont-after.json") $after
  Write-Host ("CONTINUE code={0} order={1}->{2} msg={3}" -f $c.code,$s.orderState,$after.orderState,$c.message)
  $http.Dispose(); return
}

if($phase -eq 'cleanup'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'X' }
  $uid = if($args.Count -ge 3){ $args[2] } else { $null }
  $s=Get-Snap $uid
  Save ("$tag-cleanup-before.json") $s
  if($uid -and $s.orderId -and $s.orderState -in @(1,3,7,9)){
    Save ("$tag-cleanup-cancel.json") (Cancel-Order $s.orderId $s.numericId "R30-$tag")
    Start-Sleep -Seconds 2
  }
  $final=Get-Snap $null
  Save ("$tag-cleanup-after.json") $final
  Write-Host ("CLEANUP loc={0} proc={1} order={2}" -f $final.locationState,$final.procState,$(if($uid){(Get-Snap $uid).orderState}else{'n/a'}))
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $name = if($args.Count -ge 2){ $args[1] } else { 'snap' }
  $uid = if($args.Count -ge 3){ $args[2] } else { $null }
  $s=Get-Snap $uid
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} loc={1} st={2} xy=({3},{4}) proc={5}" -f $s.orderState,$s.locationState,$s.station,$s.x,$s.y,$s.procState)
  $http.Dispose(); return
}

throw "unknown phase $phase"
