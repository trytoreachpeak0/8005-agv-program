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

# 仅本轮借用；此后禁止使用此车
$key = 'BROKERX-52501bcbe60f4723bc815f24fc763c1e'
$mapId = 11
$dest = 16
$phase = if($args.Count -ge 1){ $args[0] } else { 'baseline' }
$timeoutSec = if($args.Count -ge 2 -and $phase -ne 'success-watch'){ [int]$args[1] } else { 600 }
Write-Host "Round25 charge-SUCCESS-only key=$key mapId=$mapId dest=$dest phase=$phase"

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
  $curM=$null; $mTypes=@(); $execIdx=$null
  $m0=$null; $m1=$null; $m2=$null
  if($det){
    $execIdx=$det.executingIndex
    if($det.missions){
      foreach($m in $det.missions){ $mTypes += $m.type }
      if($det.missions.Count -gt 0){ $m0=$det.missions[0] }
      if($det.missions.Count -gt 1){ $m1=$det.missions[1] }
      if($det.missions.Count -gt 2){ $m2=$det.missions[2] }
      if($null -ne $execIdx -and $execIdx -ge 0 -and $execIdx -lt $det.missions.Count){
        $curM=$det.missions[[int]$execIdx]
      }
    }
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    deviceName=$(if($v){$v.name}else{$null})
    station=$(if($v){$v.currentStation}else{$null})
    battery=$(if($v){$v.battery}else{$null})
    batteryState=$(if($v){[string]$v.batteryState}else{$null})
    locationState=$(if($v){[string]$v.locationState}else{$null})
    actionState=$(if($v){[string]$v.actionState}else{$null})
    movementState=$(if($v){[string]$v.movementState}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    breakSwitchState=$(if($v){[string]$v.breakSwitchState}else{$null})
    emergencyState=$(if($v){[string]$v.emergencyState}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executingIndex=$execIdx
    missionTypes=$mTypes
    missionCount=$(if($det -and $det.missions){$det.missions.Count}else{0})
    curMissionType=$(if($curM){$curM.type}else{$null})
    curMissionState=$(if($curM){$curM.missionState}else{$null})
    curActionId=$(if($curM){$curM.actionId}else{$null})
    curResultCode=$(if($curM){$curM.resultCode}else{$null})
    curResultStr=$(if($curM){$curM.resultStr}else{$null})
    m0_type=$(if($m0){$m0.type}else{$null}); m0_dest=$(if($m0){$m0.destination}else{$null}); m0_state=$(if($m0){$m0.missionState}else{$null})
    m1_type=$(if($m1){$m1.type}else{$null}); m1_dest=$(if($m1){$m1.destination}else{$null}); m1_state=$(if($m1){$m1.missionState}else{$null})
    m2_type=$(if($m2){$m2.type}else{$null}); m2_actionId=$(if($m2){$m2.actionId}else{$null}); m2_state=$(if($m2){$m2.missionState}else{$null})
    m2_resultCode=$(if($m2){$m2.resultCode}else{$null}); m2_resultStr=$(if($m2){$m2.resultStr}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
  }
}

function New-ChargeOrder([string]$tag){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R25-$tag-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$dest},{`"type`":`"act`",`"actionId`":78,`"actionParam1`":1,`"actionParam2`":0,`"actionName`":`"charge`"}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  return [pscustomobject]@{uid=$uid; dest=$dest; req=$json; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body; parsed=$cr.parsed}
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

if($phase -eq 'baseline'){
  $s=Get-Snap $null
  Save 'E0-baseline.json' $s
  $costJson=(@{mapId=$mapId; stationId=$dest; deviceKeys=@($key)} | ConvertTo-Json -Compress)
  $cost=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $costJson
  Save 'E0-route-to-16.json' ([ordered]@{req=$costJson; body=$cost.body; parsed=$cost.parsed})
  $c0=$null; $msg=$null
  if($cost.parsed.result.deviceCostsList){ $c0=$cost.parsed.result.deviceCostsList[0].costs; $msg=$cost.parsed.result.deviceCostsList[0].message }
  Write-Host ("BASE name={0} st={1} bat={2}/{3} loc={4} ctrl={5} break={6} proc={7} enable={8}" -f $s.deviceName,$s.station,$s.battery,$s.batteryState,$s.locationState,$s.controlState,$s.breakSwitchState,$s.procState,$s.enable)
  Write-Host ("ROUTE dest=16 costs={0} msg={1}" -f $c0,$msg)
  $http.Dispose(); return
}

if($phase -eq 'success-create'){
  "=== R25 SUCCESS path: create move(16)+charge ==="
  $base=Get-Snap $null
  Save 'S1-before.json' $base
  if($base.procState -ne 'IDLE'){ Write-Host 'WARN not IDLE' }
  if($base.locationState -ne 'LOCATION_STATE_RUNNING'){ Write-Host 'WARN not localized' }
  if($base.breakSwitchState -ne 'MOVABLE'){ Write-Host 'WARN brake not released' }
  $cr=New-ChargeOrder 'ok'
  Save 'S1-create.json' ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.code) $($cr.message)" }
  Write-Host ("CREATED uid={0} dest={1}" -f $cr.uid,$cr.dest)
  $samples=@()
  $hitAct=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1000
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} idx={2}/{3} cur={4}/{5} actId={6} vAct={7} bat={8}/{9} st={10} proc={11}" -f $s.at,$s.orderState,$s.executingIndex,$s.missionCount,$s.curMissionType,$s.curMissionState,$s.curActionId,$s.actionState,$s.battery,$s.batteryState,$s.station,$s.procState)
    if($s.orderState -eq 9){ Save 'S1-watch-to-act-samples.json' $samples; Write-Host 'EARLY_HANG'; $http.Dispose(); exit 3 }
    if($s.orderState -in @(2,4,5,6)){ Save 'S1-watch-to-act-samples.json' $samples; Write-Host ("EARLY_TERMINAL order={0}" -f $s.orderState); $http.Dispose(); exit 4 }
    # act segment: type=act OR last mission executing with actionId 78
    if($s.curMissionType -eq 'act' -or $s.curActionId -eq 78 -or ($s.m2_type -eq 'act' -and $s.m2_state -eq 1) -or ($s.executingIndex -ge 2 -and $s.missionCount -ge 3)){
      $hitAct=$true; break
    }
  }
  Save 'S1-watch-to-act-samples.json' $samples
  Save 'S1-act-hit.json' ([ordered]@{hitAct=$hitAct; uid=$cr.uid; last=$samples[-1]})
  if(-not $hitAct){ Write-Host 'NO_ACT'; $http.Dispose(); exit 2 }
  Write-Host "ACT_REACHED uid=$($cr.uid)"
  Write-Host 'HUMAN: please connect manual charger NOW'
  $http.Dispose(); return
}

if($phase -eq 'success-watch'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $watchSec = if($args.Count -ge 3){ [int]$args[2] } else { 600 }
  "=== R25 watch after human charge uid=$uid timeout=${watchSec}s ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds($watchSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1000
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} idx={2} cur={3}/{4} vAct={5} bat={6}/{7} m2rc={8} st={9}" -f $s.at,$s.orderState,$s.executingIndex,$s.curMissionType,$s.curMissionState,$s.actionState,$s.battery,$s.batteryState,$s.m2_resultCode,$s.station)
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save 'S2-after-charge-samples.json' $samples
  Save 'S2-final.json' ([ordered]@{last=$samples[-1]})
  $last=$samples[-1]
  if($last.orderState -eq 5){ Write-Host 'SUCCESS_HIT' }
  elseif($last.orderState -eq 9){ Write-Host 'HANG_HIT' }
  else { Write-Host ("END order={0}" -f $last.orderState) }
  if($last.orderState -in @(1,3,7,9)){
    $cxl=Cancel-Order $last.orderId $last.numericId 'R25-ok-cleanup'
    Save 'S2-cleanup.json' $cxl
  }
  Save 'E9-final.json' (Get-Snap $null)
  $http.Dispose(); Write-Host DONE; return
}

if($phase -eq 'cancel'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $s=Get-Snap $uid
  Save 'CXL-before.json' $s
  $cxl=Cancel-Order $s.orderId $s.numericId 'R25-manual-cancel'
  Save 'CXL-result.json' $cxl
  Start-Sleep -Seconds 2
  Save 'CXL-after.json' (Get-Snap $uid)
  Write-Host ("CANCELLED attempts; last orderState={0}" -f (Get-Snap $uid).orderState)
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $s=Get-Snap $uid
  $name = if($args.Count -ge 3){ $args[2] } else { 'snap' }
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} idx={1} cur={2} act={3} bat={4}/{5}" -f $s.orderState,$s.executingIndex,$s.curMissionType,$s.actionState,$s.battery,$s.batteryState)
  $http.Dispose(); return
}

throw "unknown phase $phase"
