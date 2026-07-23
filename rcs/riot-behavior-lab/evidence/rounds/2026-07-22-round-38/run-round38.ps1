$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$http = [System.Net.Http.HttpClient]::new()
$http.Timeout = [TimeSpan]::FromSeconds(30)
$key = 'BROKERX-aee2f93d717546cf9510c98c854fe83e'
$mapId = 30
$phase = if($args.Count -ge 1){ $args[0] } else { 'baseline' }
Write-Host "Round38 onboard-move phase=$phase"

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
    movementState=$(if($v){[string]$v.movementState}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    emergencyState=$(if($v){[string]$v.emergencyState}else{$null})
    breakSwitchState=$(if($v){[string]$v.breakSwitchState}else{$null})
    locationState=$(if($v){[string]$v.locationState}else{$null})
    speed=$(if($v){$v.speed}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
    m0_resultCode=$(if($det -and $det.missions -and $det.missions.Count -gt 0){$det.missions[0].resultCode}else{$null})
    m0_resultStr=$(if($det -and $det.missions -and $det.missions.Count -gt 0){$det.missions[0].resultStr}else{$null})
  }
}

function Pick-Dest($cur){
  $best=$null
  foreach($sid in @(5,1,3,6,4,2)){
    if($null -ne $cur -and $sid -eq $cur){ continue }
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)}|ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$null; $msg=$null
    if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
    if($c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){
      if($null -eq $best -or $c0 -lt $best.cost){ $best=[pscustomobject]@{dest=[int]$sid; cost=$c0} }
    }
  }
  if($best){ return $best }
  return [pscustomobject]@{dest=5; cost=-1}
}

function New-Move([string]$tag,$dest,[int]$legs=1){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R38-$tag-$ts"
  $missions=@()
  $seq=@([int]$dest,1,[int]$dest,2,[int]$dest)
  $n=[Math]::Max(1,[Math]::Min($legs,$seq.Count))
  for($i=0;$i -lt $n;$i++){ $missions += @{type='move'; mapId=$mapId; destination=$seq[$i]} }
  $payload=@{appointVehicleKey=$key; isAppointEnable=1; lockStatus=0; orderName=$uid; upperId=$uid; mission=$missions}
  $json=$payload|ConvertTo-Json -Depth 8 -Compress
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  return [pscustomobject]@{uid=$uid; dest=$dest; code=$cr.parsed.code; message=$cr.parsed.message; parsed=$cr.parsed; req=$json; body=$cr.body}
}

function Send-Cmd([string]$oid,[string]$cmdType,[string]$reason){
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"$cmdType`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
  return [ordered]@{commandType=$cmdType; code=$r.parsed.code; message=$r.parsed.message; body=$r.body}
}

function Cancel-Order([string]$oid,$nid,[string]$reason){
  $attempts=@()
  if($oid){ $attempts += (Send-Cmd $oid 'CMD_ORDER_CANCEL' $reason) }
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
  Write-Host ("BASE st={0} loc={1} emerg={2} proc={3}" -f $s.station,$s.locationState,$s.emergencyState,$s.procState)
  $http.Dispose(); return
}

if($phase -eq 'clear'){
  $r=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/clearVehicleAndCancelOrderTask/$key" $null
  Save 'E0-clear.json' ([ordered]@{code=$r.parsed.code; message=$r.parsed.message; body=$r.body})
  Start-Sleep -Seconds 2
  $s=Get-Snap $null
  Save 'E0-after-clear.json' $s
  Write-Host ("CLEAR code={0} proc={1} loc={2} st={3}" -f $r.parsed.code,$s.procState,$s.locationState,$s.station)
  $http.Dispose(); return
}

# M1: wait until onboard motion detected, then create RIoT order mid-move
if($phase -eq 'm1-wait-moving'){
  $before=Get-Snap $null
  Save 'M1-before.json' $before
  if($before.locationState -ne 'LOCATION_STATE_RUNNING'){ Write-Host 'NEED_LOCALIZE'; $http.Dispose(); exit 2 }
  Write-Host ("READY st={0} move={1} proc={2}" -f $before.station,$before.movementState,$before.procState)
  Write-Host 'HUMAN: start ONBOARD go-to-station NOW (pick a farther station for longer window)'
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds(180)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $null
    $samples += $s
    Write-Host ("[{0}] move={1} speed={2} st={3} proc={4}" -f $s.at,$s.movementState,$s.speed,$s.station,$s.procState)
    $spd=0.0; try{ $spd=[double]$s.speed }catch{}
    if($s.movementState -eq 'MT_RUNNING' -or $spd -gt 0.01){ $hit=$true; break }
  }
  Save 'M1-wait-moving.json' $samples
  if(-not $hit){ Write-Host 'NO_MOVE'; $http.Dispose(); exit 2 }
  Write-Host 'MOVE_DETECTED'
  $http.Dispose(); return
}

if($phase -eq 'm1-create'){
  $moving=Get-Snap $null
  Save 'M1-pre-create.json' $moving
  $pick=Pick-Dest $moving.station
  $cr=New-Move 'M1' $(if($pick.dest){$pick.dest}else{5}) 1
  Save 'M1-create.json' ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; destCost=$pick.cost; preMove=$moving.movementState; preSpeed=$moving.speed; req=$cr.req})
  if(-not (CodeOk $cr.parsed)){ throw "create $($cr.code)" }
  Write-Host "CREATED $($cr.uid) while move=$($moving.movementState) speed=$($moving.speed)"
  Start-Sleep -Seconds 1
  $s=Get-Snap $cr.uid
  Save 'M1-after-create.json' $s
  Write-Host ("order={0} exec={1} move={2} speed={3} proc={4}" -f $s.orderState,$s.executeVehicleKey,$s.movementState,$s.speed,$s.procState)
  Write-Host "UID $($cr.uid)"
  $http.Dispose(); return
}

if($phase -eq 'm1-watch'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 120 }
  $samples=@(); $hitExec=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1000
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} exec={2} move={3} speed={4} proc={5} st={6}" -f $s.at,$s.orderState,$s.executeVehicleKey,$s.movementState,$s.speed,$s.procState,$s.station)
    if($s.orderState -eq 3){ $hitExec=$true }
    if($s.orderState -in @(2,4,5,6,9)){ break }
    if($hitExec -and $s.orderState -eq 5){ break }
  }
  Save 'M1-watch-samples.json' $samples
  Save 'M1-summary.json' ([ordered]@{uid=$uid; hitExec=$hitExec; final=$samples[-1]})
  Write-Host ("M1 RESULT hitExec={0} finalOrder={1}" -f $hitExec,$samples[-1].orderState)
  $http.Dispose(); return
}

if($phase -eq 'h1-create-exec'){
  $before=Get-Snap $null
  Save 'H1-before.json' $before
  if($before.locationState -ne 'LOCATION_STATE_RUNNING'){ Write-Host 'NEED_LOCALIZE'; $http.Dispose(); exit 2 }
  $pick=Pick-Dest $before.station
  $cr=New-Move 'H1' $pick.dest 5
  Save 'H1-create.json' ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; req=$cr.req})
  if(-not (CodeOk $cr.parsed)){ throw "create $($cr.code)" }
  Write-Host "CREATED $($cr.uid)"
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds(90)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3}" -f $s.at,$s.orderState,$s.movementState,$s.procState)
    if($s.orderState -eq 3){ $hit=$true; break }
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save 'H1-exec-samples.json' $samples
  if(-not $hit){ Write-Host 'NO_EXEC'; $http.Dispose(); exit 2 }
  Write-Host "EXEC_REACHED uid=$($cr.uid)"
  Write-Host 'HUMAN: cancel move on ONBOARD to cause HANG'
  $http.Dispose(); return
}

if($phase -eq 'h1-wait-hang'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 180 }
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3} m0rc={4}" -f $s.at,$s.orderState,$s.movementState,$s.procState,$s.m0_resultCode)
    if($s.orderState -eq 9){ $hit=$true; break }
    if($s.orderState -in @(2,4,5,6)){ break }
    Start-Sleep -Milliseconds 800
  }
  Save 'H1-hang-samples.json' $samples
  Save 'H1-hang-hit.json' ([ordered]@{hitHang=$hit; uid=$uid; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_HANG'; $http.Dispose(); exit 2 }
  Write-Host 'HANG_HIT'
  Write-Host 'HUMAN: start ONBOARD go-to-station while HANG; tell me when moving'
  $http.Dispose(); return
}

if($phase -eq 'h1-wait-moving'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds(180)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} speed={3} proc={4}" -f $s.at,$s.orderState,$s.movementState,$s.speed,$s.procState)
    $spd=0.0; try{ $spd=[double]$s.speed }catch{}
    if($s.movementState -eq 'MT_RUNNING' -or $spd -gt 0.01){ $hit=$true; break }
  }
  Save 'H1-wait-moving.json' $samples
  if(-not $hit){ Write-Host 'NO_MOVE'; $http.Dispose(); exit 2 }
  Write-Host 'MOVE_DETECTED_WHILE_HANG'
  $http.Dispose(); return
}

if($phase -eq 'h1-continue'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $before=Get-Snap $uid
  Save 'H1-before-cont.json' $before
  if(-not $before.orderId){ throw 'no orderId' }
  $c=Send-Cmd $before.orderId 'CMD_ORDER_CONTINUE_FROM_HANG' 'R38-H1-cont'
  Save 'H1-cont-call.json' $c
  Start-Sleep -Seconds 2
  $after=Get-Snap $uid
  Save 'H1-after-cont.json' $after
  Write-Host ("CONTINUE code={0} order={1}->{2} move={3} proc={4}" -f $c.code,$before.orderState,$after.orderState,$after.movementState,$after.procState)
  $samples=@(); $hitSuccess=$false
  $deadline=(Get-Date).AddSeconds(180)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1200
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3} prog={4} speed={5}" -f $s.at,$s.orderState,$s.movementState,$s.procState,$s.progress,$s.speed)
    if($s.orderState -eq 5){ $hitSuccess=$true; break }
    if($s.orderState -in @(2,4,6)){ break }
    if($s.orderState -eq 9 -and ((Get-Date)-[datetime]::ParseExact($after.at,'yyyy-MM-dd HH:mm:ss.fff',$null)).TotalSeconds -gt 30){ break }
  }
  Save 'H1-after-cont-watch.json' $samples
  Save 'H1-summary.json' ([ordered]@{uid=$uid; cont=$c; before=$before; afterCont=$after; hitSuccess=$hitSuccess; final=$samples[-1]})
  Write-Host ("H1 RESULT contCode={0} hitSuccess={1} finalOrder={2}" -f $c.code,$hitSuccess,$samples[-1].orderState)
  $http.Dispose(); return
}

if($phase -eq 'cleanup'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $s=Get-Snap $uid
  Save 'E9-before.json' $s
  if($uid -and $s.orderId -and $s.orderState -in @(1,3,7,9)){
    Save 'E9-cancel.json' (Cancel-Order $s.orderId $s.numericId 'R38-cleanup')
    Start-Sleep -Seconds 2
  }
  $final=Get-Snap $null
  Save 'E9-final.json' $final
  Write-Host ("CLEANUP order={0} loc={1} proc={2}" -f $(if($uid){(Get-Snap $uid).orderState}else{'n/a'}),$final.locationState,$final.procState)
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $name = if($args.Count -ge 3){ $args[2] } else { 'snap' }
  $s=Get-Snap $uid
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} loc={1} move={2} speed={3} proc={4}" -f $s.orderState,$s.locationState,$s.movementState,$s.speed,$s.procState)
  $http.Dispose(); return
}

throw "unknown phase $phase"
