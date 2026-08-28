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

# 仅测试车
$key = 'BROKERX-aee2f93d717546cf9510c98c854fe83e'
if($e.testVehicleKey -and $e.testVehicleKey -ne $key){
  Write-Host "WARN env.testVehicleKey=$($e.testVehicleKey) ; script forces $key"
}
$mapId = 29
$phase = if($args.Count -ge 1){ $args[0] } else { 'baseline' }
Write-Host "Round27 HANG-discriminate phase=$phase key=$key mapId=$mapId"

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
  $curM=$null; $execIdx=$null; $m0=$null
  if($det -and $det.missions){
    $execIdx=$det.executingIndex
    if($det.missions.Count -gt 0){ $m0=$det.missions[0] }
    if($null -ne $execIdx -and $execIdx -ge 0 -and $execIdx -lt $det.missions.Count){
      $curM=$det.missions[[int]$execIdx]
    }
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    apiOk=$gi.ok
    station=$(if($v){$v.currentStation}else{$null})
    noStation=$(if($v){$v.noStation}else{$null})
    movementState=$(if($v){[string]$v.movementState}else{$null})
    actionState=$(if($v){[string]$v.actionState}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    emergencyState=$(if($v){[string]$v.emergencyState}else{$null})
    breakSwitchState=$(if($v){[string]$v.breakSwitchState}else{$null})
    locationState=$(if($v){[string]$v.locationState}else{$null})
    hardwareState=$(if($v){[string]$v.hardwareState}else{$null})
    faultCodes=$(if($v){$v.faultCodes}else{$null})
    lastErrorCode=$(if($v){$v.lastErrorCode}else{$null})
    speed=$(if($v){$v.speed}else{$null})
    battery=$(if($v){$v.battery}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    executingIndex=$execIdx
    curMissionType=$(if($curM){$curM.type}else{$null})
    curMissionState=$(if($curM){$curM.missionState}else{$null})
    curResultCode=$(if($curM){$curM.resultCode}else{$null})
    curResultStr=$(if($curM){$curM.resultStr}else{$null})
    m0_state=$(if($m0){$m0.missionState}else{$null})
    m0_resultCode=$(if($m0){$m0.resultCode}else{$null})
    m0_resultStr=$(if($m0){$m0.resultStr}else{$null})
  }
}

function Pick-Dest($curStation){
  $chosen=$null; $chosenCost=$null
  foreach($sid in @(1,2,3,4,5,6,7,8,9,10)){
    if($null -ne $curStation -and $sid -eq $curStation){ continue }
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$null; $msg=$null
    if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
    if($c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){
      # prefer longer routes for human reaction time (cost >= 3000 if available)
      if($null -eq $chosen){ $chosen=$sid; $chosenCost=$c0 }
      elseif($c0 -ge 3000 -and ($chosenCost -lt 3000 -or $c0 -lt $chosenCost)){ $chosen=$sid; $chosenCost=$c0 }
      elseif($chosenCost -lt 3000 -and $c0 -gt $chosenCost){ $chosen=$sid; $chosenCost=$c0 }
    }
  }
  if($null -eq $chosen){ throw 'no dest' }
  return [pscustomobject]@{dest=[int]$chosen; cost=$chosenCost}
}

function New-MoveOrder([string]$tag, $dest, $curStation){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R27-$tag-$ts"
  # 多段往返，拉长 EXECUTING 窗口便于人工触发
  $homeStation = if($null -ne $curStation -and $curStation -gt 0){ [int]$curStation } else { 1 }
  $missions = @(
    @{type='move'; mapId=$mapId; destination=[int]$dest},
    @{type='move'; mapId=$mapId; destination=$homeStation},
    @{type='move'; mapId=$mapId; destination=[int]$dest}
  )
  $payload = @{
    appointVehicleKey=$key; isAppointEnable=1; lockStatus=0
    orderName=$uid; upperId=$uid; mission=$missions
  }
  $json = $payload | ConvertTo-Json -Depth 6 -Compress
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  return [pscustomobject]@{uid=$uid; dest=$dest; home=$homeStation; req=$json; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body; parsed=$cr.parsed}
}

function Cancel-Order([string]$oid,$nid,[string]$reason){
  $attempts=@()
  if($oid){
    $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
    $attempts += [ordered]@{api='command'; orderId=$oid; code=$cmd.parsed.code; message=$cmd.parsed.message}
  }
  if($nid){
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" "{`"orderId`":$nid,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $attempts += [ordered]@{api='operate'; numericId=$nid; code=$op.parsed.code; message=$op.parsed.message}
  }
  return $attempts
}

function Invoke-EmergService([string]$serviceId){
  $mid = [int](Get-Random -Minimum 100000 -Maximum 999999)
  $body = "{`"messageId`":$mid,`"mqCallback`":{`"tag`":`"string`",`"topic`":`"string`"},`"thingsProperties`":{}}"
  $url = "$($e.baseUrl)/api/device/v1/command/sync/service/$key/$serviceId"
  $r=Invoke-Api POST $url $body
  return [ordered]@{serviceId=$serviceId; messageId=$mid; req=$body; code=$r.parsed.code; message=$r.parsed.message; body=$r.body; parsed=$r.parsed}
}

function Send-Continue([string]$oid,[string]$cmdType){
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"$cmdType`",`"disableVehicle`":false,`"reason`":`"R27-$cmdType`"}"
  return [ordered]@{commandType=$cmdType; orderId=$oid; code=$r.parsed.code; message=$r.parsed.message; body=$r.body}
}

if($phase -eq 'baseline'){
  $s=Get-Snap $null
  Save 'E0-baseline.json' $s
  Write-Host ("BASE st={0} move={1} emerg={2} break={3} ctrl={4} proc={5} loc={6} bat={7}" -f $s.station,$s.movementState,$s.emergencyState,$s.breakSwitchState,$s.controlState,$s.procState,$s.locationState,$s.battery)
  if($s.procState -ne 'IDLE'){ Write-Host 'WARN not IDLE' }
  if($s.emergencyState -ne 'OK'){ Write-Host 'WARN emergency not OK' }
  if($s.breakSwitchState -ne 'MOVABLE'){ Write-Host 'WARN break not MOVABLE' }
  if($s.locationState -ne 'LOCATION_STATE_RUNNING'){ Write-Host 'WARN not localized' }
  $http.Dispose(); return
}

if($phase -eq 'create-exec'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'X' }
  $waitSec = if($args.Count -ge 3){ [int]$args[2] } else { 90 }
  $base=Get-Snap $null
  Save ("$tag-before.json") $base
  $pick=Pick-Dest $base.station
  Save ("$tag-dest.json") $pick
  Write-Host ("dest={0} cost={1}" -f $pick.dest,$pick.cost)
  $cr=New-MoveOrder $tag $pick.dest $base.station
  Save ("$tag-create.json") ([ordered]@{uid=$cr.uid; dest=$cr.dest; home=$cr.home; code=$cr.code; message=$cr.message; req=$cr.req; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.code) $($cr.message)" }
  Write-Host ("CREATED uid={0}" -f $cr.uid)
  $samples=@(); $hitExec=$false
  $deadline=(Get-Date).AddSeconds($waitSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} st={3} proc={4} emerg={5}" -f $s.at,$s.orderState,$s.movementState,$s.station,$s.procState,$s.emergencyState)
    if($s.orderState -eq 3){ $hitExec=$true; break }
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save ("$tag-to-exec-samples.json") $samples
  Save ("$tag-exec-hit.json") ([ordered]@{hitExec=$hitExec; uid=$cr.uid; last=$samples[-1]})
  if(-not $hitExec){ Write-Host 'NO_EXEC'; $http.Dispose(); exit 2 }
  Write-Host "EXEC_REACHED uid=$($cr.uid)"
  Write-Host "HUMAN: trigger scenario $tag now (A=hw-estop / E=onboard-cancel / F=brake-knob)"
  $http.Dispose(); return
}

if($phase -eq 'hang-watch'){
  $tag = if($args.Count -ge 2){ $args[1] } else { throw 'need tag' }
  $uid = if($args.Count -ge 3){ $args[2] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 4){ [int]$args[3] } else { 180 }
  "=== hang-watch tag=$tag uid=$uid timeout=${timeoutSec}s ==="
  $samples=@(); $hitHang=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} emerg={3} break={4} ctrl={5} proc={6} m0rc={7}" -f $s.at,$s.orderState,$s.movementState,$s.emergencyState,$s.breakSwitchState,$s.controlState,$s.procState,$s.m0_resultCode)
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -in @(2,4,5,6)){ break }
  }
  Save ("$tag-hang-samples.json") $samples
  Save ("$tag-hang-hit.json") ([ordered]@{hitHang=$hitHang; uid=$uid; last=$samples[-1]})
  if($hitHang){ Write-Host 'HANG_HIT' } else { Write-Host ("END order={0}" -f $samples[-1].orderState) }
  $http.Dispose(); return
}

if($phase -eq 'continue-probe'){
  $tag = if($args.Count -ge 2){ $args[1] } else { throw 'need tag' }
  $uid = if($args.Count -ge 3){ $args[2] } else { throw 'need uid' }
  $mode = if($args.Count -ge 4){ $args[3] } else { 'plain' } # plain | after-cancel-emerg
  $before=Get-Snap $uid
  Save ("$tag-cont-before.json") $before
  if(-not $before.orderId){ throw 'no orderId' }

  $steps=@()
  if($mode -eq 'after-cancel-emerg'){
    $ce=Invoke-EmergService 'cancelEmergency'
    Save ("$tag-cancelEmergency.json") $ce
    $steps += [ordered]@{step='cancelEmergency'; code=$ce.code; message=$ce.message}
    Start-Sleep -Seconds 2
    $mid=Get-Snap $uid
    Save ("$tag-cont-after-cancel-emerg.json") $mid
    $steps += [ordered]@{step='snap-after-cancel-emerg'; orderState=$mid.orderState; emergencyState=$mid.emergencyState}
  }

  $c1=Send-Continue $before.orderId 'CMD_ORDER_CONTINUE_FROM_HANG'
  Save ("$tag-CONTINUE_FROM_HANG.json") $c1
  $steps += $c1
  Start-Sleep -Seconds 2
  $after1=Get-Snap $uid
  Save ("$tag-cont-after-CONTINUE.json") $after1
  $steps += [ordered]@{step='snap-after-CONTINUE'; orderState=$after1.orderState; emergencyState=$after1.emergencyState; procState=$after1.procState; movementState=$after1.movementState}

  $c2=Send-Continue $before.orderId 'CMD_ORDER_JUMP_FROM_HANG'
  Save ("$tag-JUMP_FROM_HANG.json") $c2
  $steps += $c2
  Start-Sleep -Seconds 1
  $after2=Get-Snap $uid
  Save ("$tag-cont-after-JUMP.json") $after2

  $summary=[ordered]@{
    tag=$tag; uid=$uid; mode=$mode
    beforeOrder=$before.orderState; beforeEmerg=$before.emergencyState; beforeBreak=$before.breakSwitchState
    continueCode=$c1.code; continueMessage=$c1.message
    afterContinueOrder=$after1.orderState; afterContinueEmerg=$after1.emergencyState
    jumpCode=$c2.code; jumpMessage=$c2.message
    afterJumpOrder=$after2.orderState
    continueRecovered = (CodeOk ([pscustomobject]@{code=$c1.code}) -and $after1.orderState -ne 9)
    steps=$steps
  }
  Save ("$tag-cont-summary.json") $summary
  Write-Host ("CONTINUE code={0} msg={1} afterOrder={2} recovered={3}" -f $c1.code,$c1.message,$after1.orderState,$summary.continueRecovered)
  $http.Dispose(); return
}

if($phase -eq 'trigger-sw-estop'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'B' }
  $before=Get-Snap $null
  Save ("$tag-sw-before.json") $before
  $tr=Invoke-EmergService 'triggerEmergency'
  Save ("$tag-triggerEmergency.json") $tr
  Start-Sleep -Seconds 1
  $after=Get-Snap $null
  Save ("$tag-sw-after.json") $after
  Write-Host ("trigger code={0} emerg={1}->{2}" -f $tr.code,$before.emergencyState,$after.emergencyState)
  $http.Dispose(); return
}

if($phase -eq 'cancel-emergency'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'X' }
  $ce=Invoke-EmergService 'cancelEmergency'
  Save ("$tag-cancelEmergency-manual.json") $ce
  Start-Sleep -Seconds 1
  $s=Get-Snap $null
  Save ("$tag-after-cancel-emerg-manual.json") $s
  Write-Host ("cancelEmerg code={0} emerg={1}" -f $ce.code,$s.emergencyState)
  $http.Dispose(); return
}

if($phase -eq 'cleanup'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'X' }
  $uid = if($args.Count -ge 3){ $args[2] } else { $null }
  $s=Get-Snap $uid
  Save ("$tag-cleanup-before.json") $s
  if($s.orderState -in @(1,3,7,9) -or ($uid -and $s.orderId)){
    $cxl=Cancel-Order $s.orderId $s.numericId "R27-$tag-cleanup"
    Save ("$tag-cleanup-cancel.json") $cxl
    Start-Sleep -Seconds 2
  }
  # if still emergency, try cancel
  $s2=Get-Snap $null
  if($s2.emergencyState -and $s2.emergencyState -ne 'OK'){
    $ce=Invoke-EmergService 'cancelEmergency'
    Save ("$tag-cleanup-cancelEmerg.json") $ce
    Start-Sleep -Seconds 2
  }
  $final=Get-Snap $null
  Save ("$tag-cleanup-after.json") $final
  Write-Host ("CLEANUP proc={0} emerg={1} break={2} order={3}" -f $final.procState,$final.emergencyState,$final.breakSwitchState,$(if($uid){(Get-Snap $uid).orderState}else{'n/a'}))
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $tag = if($args.Count -ge 2){ $args[1] } else { 'snap' }
  $uid = if($args.Count -ge 3){ $args[2] } else { $null }
  $s=Get-Snap $uid
  Save ("SNAP-$tag.json") $s
  Write-Host ("SNAP order={0} move={1} emerg={2} break={3} proc={4}" -f $s.orderState,$s.movementState,$s.emergencyState,$s.breakSwitchState,$s.procState)
  $http.Dispose(); return
}

throw "unknown phase $phase"
