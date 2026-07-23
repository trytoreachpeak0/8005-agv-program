$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$http = [System.Net.Http.HttpClient]::new()
$http.Timeout = [TimeSpan]::FromSeconds(20)
$key = $e.testVehicleKey
$mapId = 30
$phase = if($args.Count -ge 1){ $args[0] } else { 'baseline' }
$timeoutSec = if($args.Count -ge 2){ [int]$args[1] } else { 180 }
Write-Host "Round24 charge-order phase=$phase key=$key mapId=$mapId"

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
  $m0=$null; $m1=$null
  if($det){
    $execIdx=$det.executingIndex
    if($det.missions){
      foreach($m in $det.missions){ $mTypes += $m.type }
      if($det.missions.Count -gt 0){ $m0=$det.missions[0] }
      if($det.missions.Count -gt 1){ $m1=$det.missions[1] }
      if($null -ne $execIdx -and $execIdx -ge 0 -and $execIdx -lt $det.missions.Count){
        $curM=$det.missions[[int]$execIdx]
      }
    }
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$(if($v){$v.currentStation}else{$null})
    noStation=$(if($v){$v.noStation}else{$null})
    battery=$(if($v){$v.battery}else{$null})
    batteryState=$(if($v){[string]$v.batteryState}else{$null})
    locationState=$(if($v){[string]$v.locationState}else{$null})
    actionState=$(if($v){[string]$v.actionState}else{$null})
    actionTaskNo=$(if($v){$v.actionTaskNo}else{$null})
    movementState=$(if($v){[string]$v.movementState}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executingIndex=$execIdx
    missionTypes=$mTypes
    curMissionType=$(if($curM){$curM.type}else{$null})
    curMissionState=$(if($curM){$curM.missionState}else{$null})
    curActionId=$(if($curM){$curM.actionId}else{$null})
    curResultCode=$(if($curM){$curM.resultCode}else{$null})
    curResultStr=$(if($curM){$curM.resultStr}else{$null})
    m0_state=$(if($m0){$m0.missionState}else{$null})
    m1_type=$(if($m1){$m1.type}else{$null})
    m1_state=$(if($m1){$m1.missionState}else{$null})
    m1_actionId=$(if($m1){$m1.actionId}else{$null})
    m1_resultCode=$(if($m1){$m1.resultCode}else{$null})
    m1_resultStr=$(if($m1){$m1.resultStr}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
  }
}

function Pick-Dest($curStation){
  $chosen=$null; $chosenCost=$null
  foreach($sid in @(1,2,3,4,5,6,7)){
    if($null -ne $curStation -and $sid -eq $curStation){ continue }
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$null; $msg=$null
    if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
    if($c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){
      if($null -eq $chosen -or $c0 -lt $chosenCost){ $chosen=$sid; $chosenCost=$c0 }
    }
  }
  # 若已在站且无其它可达站，退回当前站（仍可发 move+act，move 可能很快结束）
  if($null -eq $chosen -and $null -ne $curStation -and $curStation -gt 0){
    return [pscustomobject]@{dest=[int]$curStation; cost=0; note='same-station-fallback'}
  }
  if($null -eq $chosen){ throw 'no dest' }
  return [pscustomobject]@{dest=[int]$chosen; cost=$chosenCost; note='ok'}
}

function New-ChargeOrder([string]$tag, $dest){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R24-$tag-$ts"
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
  Write-Host ("BASE st={0} bat={1}/{2} loc={3} proc={4} act={5}" -f $s.station,$s.battery,$s.batteryState,$s.locationState,$s.procState,$s.actionState)
  if($s.locationState -ne 'LOCATION_STATE_RUNNING'){ Write-Host 'WARN not localized' }
  if($s.procState -ne 'IDLE'){ Write-Host 'WARN not IDLE' }
  $http.Dispose(); return
}

if($phase -eq 'fail'){
  "=== S1 FAIL path: move+charge, expect HANG ==="
  $base=Get-Snap $null
  Save 'S1-before.json' $base
  $pick=Pick-Dest $base.station
  Save 'S1-dest.json' $pick
  Write-Host ("dest={0} cost={1} note={2}" -f $pick.dest,$pick.cost,$pick.note)
  $cr=New-ChargeOrder 'fail' $pick.dest
  Save 'S1-create.json' ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.code) $($cr.message)" }
  $uid=$cr.uid
  $samples=@()
  $hitHang=$false; $hitAct=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 900
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} idx={2} cur={3}/{4} actId={5} vAct={6} bat={7} proc={8} m1={9}" -f $s.at,$s.orderState,$s.executingIndex,$s.curMissionType,$s.curMissionState,$s.curActionId,$s.actionState,$s.battery,$s.procState,$s.m1_state)
    if($s.curMissionType -eq 'act' -or ($s.executingIndex -eq 1)){ $hitAct=$true }
    # 9=HANG; also capture long EXECUTING on act as soft hang signal
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -in @(2,4,5,6)){ break }
  }
  Save 'S1-samples.json' $samples
  Save 'S1-hit.json' ([ordered]@{hitHang=$hitHang; hitAct=$hitAct; last=$samples[-1]})
  if($hitHang){ Write-Host 'HANG_HIT' }
  elseif($hitAct -and $samples[-1].orderState -eq 3){
    Write-Host 'ACT_STUCK_EXECUTING (no HANG yet within timeout)'
  } else {
    Write-Host ("END order={0}" -f $samples[-1].orderState)
  }
  $last=$samples[-1]
  if($last.orderState -in @(1,3,7,9)){
    $cxl=Cancel-Order $last.orderId $last.numericId 'R24-fail-cleanup'
    Save 'S1-cleanup.json' $cxl
    Start-Sleep -Seconds 2
  }
  Save 'S1-after.json' (Get-Snap $null)
  $http.Dispose(); Write-Host DONE; return
}

if($phase -eq 'success-create'){
  "=== S2 SUCCESS path: create move+charge ==="
  $base=Get-Snap $null
  Save 'S2-before.json' $base
  if($base.procState -ne 'IDLE'){ Write-Host 'WARN not IDLE' }
  $pick=Pick-Dest $base.station
  Save 'S2-dest.json' $pick
  $cr=New-ChargeOrder 'ok' $pick.dest
  Save 'S2-create.json' ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.code) $($cr.message)" }
  Write-Host ("CREATED uid={0} dest={1}" -f $cr.uid,$cr.dest)
  # wait until act segment
  $samples=@()
  $hitAct=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} idx={2} cur={3}/{4} vAct={5} bat={6}/{7}" -f $s.at,$s.orderState,$s.executingIndex,$s.curMissionType,$s.curMissionState,$s.actionState,$s.battery,$s.batteryState)
    if($s.orderState -eq 9){ Save 'S2-watch-to-act-samples.json' $samples; Write-Host 'EARLY_HANG'; $http.Dispose(); exit 3 }
    if($s.orderState -in @(2,4,5,6)){ Save 'S2-watch-to-act-samples.json' $samples; Write-Host ("EARLY_TERMINAL order={0}" -f $s.orderState); $http.Dispose(); exit 4 }
    if($s.curMissionType -eq 'act' -or $s.executingIndex -eq 1 -or ($s.m1_state -eq 1)){
      $hitAct=$true; break
    }
  }
  Save 'S2-watch-to-act-samples.json' $samples
  Save 'S2-act-hit.json' ([ordered]@{hitAct=$hitAct; uid=$cr.uid; last=$samples[-1]})
  if(-not $hitAct){ Write-Host 'NO_ACT'; $http.Dispose(); exit 2 }
  Write-Host "ACT_REACHED uid=$($cr.uid)"
  Write-Host 'HUMAN: please simulate charge with manual charger now'
  $http.Dispose(); return
}

if($phase -eq 'success-watch'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $watchSec = if($args.Count -ge 3){ [int]$args[2] } else { 300 }
  "=== S2 watch after human charge uid=$uid timeout=${watchSec}s ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds($watchSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 900
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} idx={2} cur={3}/{4} vAct={5} bat={6}/{7} m1rc={8}" -f $s.at,$s.orderState,$s.executingIndex,$s.curMissionType,$s.curMissionState,$s.actionState,$s.battery,$s.batteryState,$s.m1_resultCode)
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save 'S2-after-charge-samples.json' $samples
  Save 'S2-final.json' ([ordered]@{last=$samples[-1]})
  $last=$samples[-1]
  if($last.orderState -eq 5){ Write-Host 'SUCCESS_HIT' }
  elseif($last.orderState -eq 9){ Write-Host 'HANG_HIT' }
  else { Write-Host ("END order={0}" -f $last.orderState) }
  if($last.orderState -in @(1,3,7,9)){
    $cxl=Cancel-Order $last.orderId $last.numericId 'R24-ok-cleanup'
    Save 'S2-cleanup.json' $cxl
  }
  Save 'E9-final.json' (Get-Snap $null)
  $http.Dispose(); Write-Host DONE; return
}

if($phase -eq 'snapshot'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $s=Get-Snap $uid
  $name = if($args.Count -ge 3){ $args[2] } else { 'snap' }
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} idx={1} cur={2} act={3} bat={4}" -f $s.orderState,$s.executingIndex,$s.curMissionType,$s.actionState,$s.battery)
  $http.Dispose(); return
}

throw "unknown phase $phase"
