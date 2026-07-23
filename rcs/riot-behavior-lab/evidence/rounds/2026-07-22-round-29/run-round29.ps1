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
Write-Host "Round29 body-state-create phase=$phase key=$key mapId=$mapId"

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
  $det=$null
  if($upperId){
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$upperId" $null
    $det=$by.parsed.result
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$(if($v){$v.currentStation}else{$null})
    mapName=$(if($v -and $v.previousState){$v.previousState.mapName}else{$null})
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
  }
}

function Pick-Dest($cur){
  foreach($sid in @(3,2,1,5,6,4)){
    if($null -ne $cur -and $sid -eq $cur){ continue }
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)}|ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$null; $msg=$null
    if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
    if($c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){ return [pscustomobject]@{dest=[int]$sid; cost=$c0} }
  }
  # fallback: station may be 0 but map reachable
  return [pscustomobject]@{dest=3; cost=-1}
}

function New-Move([string]$tag,$dest){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R29-$tag-$ts"
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

function Invoke-Emerg([string]$serviceId){
  $mid=[int](Get-Random -Minimum 100000 -Maximum 999999)
  $body="{`"messageId`":$mid,`"mqCallback`":{`"tag`":`"string`",`"topic`":`"string`"},`"thingsProperties`":{}}"
  $r=Invoke-Api POST "$($e.baseUrl)/api/device/v1/command/sync/service/$key/$serviceId" $body
  return [ordered]@{serviceId=$serviceId; code=$r.parsed.code; message=$r.parsed.message; body=$r.body}
}

if($phase -eq 'baseline'){
  $s=Get-Snap $null
  Save 'E0-baseline.json' $s
  Write-Host ("BASE st={0} emerg={1} break={2} loc={3} proc={4} processing={5}" -f $s.station,$s.emergencyState,$s.breakSwitchState,$s.locationState,$s.procState,$s.processingOrder)
  $http.Dispose(); return
}

if($phase -eq 'wait-abnormal'){
  # wait until vehicle matches expected abnormal signature
  $kind = if($args.Count -ge 2){ $args[1] } else { throw 'need kind A|B|F' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 120 }
  Write-Host "=== wait-abnormal kind=$kind timeout=${timeoutSec}s ==="
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    $s=Get-Snap $null
    $samples += $s
    Write-Host ("[{0}] emerg={1} break={2} ctrl={3} proc={4}" -f $s.at,$s.emergencyState,$s.breakSwitchState,$s.controlState,$s.procState)
    if($kind -eq 'A' -and $s.emergencyState -and $s.emergencyState -ne 'OK'){ $hit=$true; break }
    if($kind -eq 'B' -and $s.emergencyState -eq 'CAN_RECOVER'){ $hit=$true; break }
    if($kind -eq 'F' -and $s.breakSwitchState -eq 'UNMOVABLE'){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save ("$kind-wait-abnormal.json") ([ordered]@{hit=$hit; kind=$kind; last=$samples[-1]; samples=$samples})
  if(-not $hit){ Write-Host 'NO_ABNORMAL'; $http.Dispose(); exit 2 }
  Write-Host 'ABNORMAL_HIT'
  $http.Dispose(); return
}

if($phase -eq 'create-watch'){
  $tag = if($args.Count -ge 2){ $args[1] } else { throw 'need tag' }
  $watchSec = if($args.Count -ge 3){ [int]$args[2] } else { 90 }
  $before=Get-Snap $null
  Save ("$tag-before-create.json") $before
  $pick=Pick-Dest $before.station
  Save ("$tag-dest.json") $pick
  Write-Host ("dest={0} cost={1} emerg={2} break={3} proc={4}" -f $pick.dest,$pick.cost,$before.emergencyState,$before.breakSwitchState,$before.procState)
  $cr=New-Move $tag $pick.dest
  Save ("$tag-create.json") ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.code) $($cr.message)" }
  Write-Host "CREATED uid=$($cr.uid)"
  $samples=@()
  $hitExec=$false; $stayedQueue=$true
  $deadline=(Get-Date).AddSeconds($watchSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 900
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} execKey={2} emerg={3} break={4} proc={5} move={6}" -f $s.at,$s.orderState,$s.executeVehicleKey,$s.emergencyState,$s.breakSwitchState,$s.procState,$s.movementState)
    if($s.orderState -eq 3){ $hitExec=$true; $stayedQueue=$false; break }
    if($s.orderState -eq 9){ $stayedQueue=$false; break }
    if($s.orderState -in @(2,4,5,6)){ $stayedQueue=$false; break }
  }
  $last=$samples[-1]
  $summary=[ordered]@{
    tag=$tag; uid=$cr.uid
    beforeEmerg=$before.emergencyState; beforeBreak=$before.breakSwitchState; beforeProc=$before.procState
    createCode=$cr.code
    hitExec=$hitExec
    stayedQueueing = ($last.orderState -eq 1)
    finalOrderState=$last.orderState
    finalExecKey=$last.executeVehicleKey
    finalEmerg=$last.emergencyState
    finalBreak=$last.breakSwitchState
    finalProc=$last.procState
    watchSec=$watchSec
  }
  Save ("$tag-watch-samples.json") $samples
  Save ("$tag-summary.json") $summary
  Write-Host ("RESULT hitExec={0} stayedQueue={1} finalOrder={2}" -f $hitExec,$summary.stayedQueueing,$last.orderState)
  $http.Dispose(); return
}

if($phase -eq 'trigger-sw-estop'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'B' }
  $before=Get-Snap $null
  Save ("$tag-sw-before.json") $before
  $tr=Invoke-Emerg 'triggerEmergency'
  Save ("$tag-triggerEmergency.json") $tr
  Start-Sleep -Seconds 1
  $after=Get-Snap $null
  Save ("$tag-sw-after.json") $after
  Write-Host ("trigger code={0} emerg={1}->{2}" -f $tr.code,$before.emergencyState,$after.emergencyState)
  $http.Dispose(); return
}

if($phase -eq 'cleanup'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'X' }
  $uid = if($args.Count -ge 3){ $args[2] } else { $null }
  $s=Get-Snap $uid
  Save ("$tag-cleanup-before.json") $s
  if($uid -and $s.orderId -and $s.orderState -in @(1,3,7,9)){
    Save ("$tag-cleanup-cancel.json") (Cancel-Order $s.orderId $s.numericId "R29-$tag")
    Start-Sleep -Seconds 2
  }
  if($s.emergencyState -and $s.emergencyState -ne 'OK'){
    $ce=Invoke-Emerg 'cancelEmergency'
    Save ("$tag-cleanup-cancelEmerg.json") $ce
    Start-Sleep -Seconds 2
  }
  $final=Get-Snap $null
  Save ("$tag-cleanup-after.json") $final
  Write-Host ("CLEANUP emerg={0} break={1} proc={2} order={3}" -f $final.emergencyState,$final.breakSwitchState,$final.procState,$(if($uid){(Get-Snap $uid).orderState}else{'n/a'}))
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $name = if($args.Count -ge 2){ $args[1] } else { 'snap' }
  $uid = if($args.Count -ge 3){ $args[2] } else { $null }
  $s=Get-Snap $uid
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} emerg={1} break={2} proc={3}" -f $s.orderState,$s.emergencyState,$s.breakSwitchState,$s.procState)
  $http.Dispose(); return
}

throw "unknown phase $phase"
