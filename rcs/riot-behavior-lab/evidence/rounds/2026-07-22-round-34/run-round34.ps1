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
Write-Host "Round34 power-off-mid-exec phase=$phase key=$key mapId=$mapId"

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

function Get-RuntimeType(){
  $st=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/status/$key" $null
  if($st.parsed -and $st.parsed.result){ return [string]$st.parsed.result.type }
  return $null
}

function Get-Snap([string]$upperId){
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $v=$null; $vti=$null
  if($gi.parsed){ $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo }
  $det=$null
  if($upperId){
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$upperId" $null
    $det=$by.parsed.result
  }
  $rt=Get-RuntimeType
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    runtimeType=$rt
    station=$(if($v){$v.currentStation}else{$null})
    mapName=$(if($v -and $v.previousState){$v.previousState.mapName}else{$null})
    movementState=$(if($v){[string]$v.movementState}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    emergencyState=$(if($v){[string]$v.emergencyState}else{$null})
    breakSwitchState=$(if($v){[string]$v.breakSwitchState}else{$null})
    locationState=$(if($v){[string]$v.locationState}else{$null})
    speed=$(if($v){$v.speed}else{$null})
    faultCodes=$(if($v){$v.faultCodes}else{$null})
    lastErrorCode=$(if($v){$v.lastErrorCode}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    integrationLevel=$(if($vti){[string]$vti.integrationLevel}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    executingIndex=$(if($det){$det.executingIndex}else{$null})
    m0_resultCode=$(if($det -and $det.missions -and $det.missions.Count -gt 0){$det.missions[0].resultCode}else{$null})
    m0_resultStr=$(if($det -and $det.missions -and $det.missions.Count -gt 0){$det.missions[0].resultStr}else{$null})
  }
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
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CONTINUE_FROM_HANG`",`"disableVehicle`":false,`"reason`":`"R34-continue`"}"
  return [ordered]@{code=$r.parsed.code; message=$r.parsed.message; body=$r.body}
}

if($phase -eq 'baseline'){
  $s=Get-Snap $null
  Save 'E0-baseline.json' $s
  Write-Host ("BASE runtime={0} st={1} emerg={2} break={3} loc={4} proc={5}" -f $s.runtimeType,$s.station,$s.emergencyState,$s.breakSwitchState,$s.locationState,$s.procState)
  $http.Dispose(); return
}

if($phase -eq 'create-exec'){
  $waitSec = if($args.Count -ge 2){ [int]$args[1] } else { 120 }
  $base=Get-Snap $null
  Save 'S1-before.json' $base
  $legs=@(3,1,3,6,3,1,3,2,3)
  $missions=@()
  foreach($d in $legs){ $missions += @{type='move'; mapId=$mapId; destination=[int]$d} }
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R34-PoffRec-$ts"
  $payload=@{appointVehicleKey=$key; isAppointEnable=1; lockStatus=0; orderName=$uid; upperId=$uid; mission=$missions}
  $json=$payload|ConvertTo-Json -Depth 8 -Compress
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  Save 'S1-create.json' ([ordered]@{uid=$uid; legs=$legs; code=$cr.parsed.code; message=$cr.parsed.message; req=$json; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.parsed.code) $($cr.parsed.message)" }
  Write-Host "CREATED uid=$uid"
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($waitSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} runtime={3} proc={4} st={5}" -f $s.at,$s.orderState,$s.movementState,$s.runtimeType,$s.procState,$s.station)
    if($s.orderState -eq 3){ $hit=$true; break }
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save 'S1-to-exec-samples.json' $samples
  Save 'S1-exec-hit.json' ([ordered]@{hitExec=$hit; uid=$uid; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_EXEC'; $http.Dispose(); exit 2 }
  Write-Host "EXEC_REACHED uid=$uid"
  Write-Host 'HUMAN: turn knob to POWER OFF now'
  $http.Dispose(); return
}

if($phase -eq 'wait-power-off'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 180 }
  Write-Host "=== wait-power-off uid=$uid timeout=${timeoutSec}s ==="
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] runtime={1} order={2} move={3} proc={4} prog={5}" -f $s.at,$s.runtimeType,$s.orderState,$s.movementState,$s.procState,$s.progress)
    if($s.runtimeType -eq 'offline'){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save 'S2-wait-power-off.json' ([ordered]@{hit=$hit; uid=$uid; last=$samples[-1]; samples=$samples})
  if(-not $hit){ Write-Host 'NO_OFFLINE'; $http.Dispose(); exit 2 }
  Write-Host 'POWER_OFF_HIT'
  $http.Dispose(); return
}

if($phase -eq 'hang-watch'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 900 }
  Write-Host "=== hang-watch uid=$uid timeout=${timeoutSec}s ==="
  $samples=@(); $hitHang=$false; $offlineSeen=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  $lastSave=(Get-Date)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1500
    $s=Get-Snap $uid
    $samples += $s
    if($s.runtimeType -eq 'offline'){ $offlineSeen=$true }
    Write-Host ("[{0}] order={1} runtime={2} move={3} proc={4} prog={5} m0rc={6} fail={7}" -f $s.at,$s.orderState,$s.runtimeType,$s.movementState,$s.procState,$s.progress,$s.m0_resultCode,$s.failReason)
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -in @(2,4,5,6)){ break }
    if(((Get-Date)-$lastSave).TotalSeconds -ge 60){
      Save 'S3-hang-samples-partial.json' $samples
      $lastSave=Get-Date
    }
  }
  Save 'S3-hang-samples.json' $samples
  Save 'S3-hang-hit.json' ([ordered]@{hitHang=$hitHang; offlineSeen=$offlineSeen; uid=$uid; sampleCount=$samples.Count; last=$samples[-1]; first=$samples[0]; watchSec=$timeoutSec})
  if($hitHang){ Write-Host 'HANG_HIT' }
  else { Write-Host ("END order={0} offlineSeen={1} lastRuntime={2}" -f $samples[-1].orderState,$offlineSeen,$samples[-1].runtimeType) }
  $http.Dispose(); return
}

if($phase -eq 'wait-power-on'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 180 }
  Write-Host "=== wait-power-on uid=$uid timeout=${timeoutSec}s ==="
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] runtime={1} order={2} move={3} proc={4} prog={5}" -f $s.at,$s.runtimeType,$s.orderState,$s.movementState,$s.procState,$s.progress)
    if($s.runtimeType -eq 'online'){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save 'S4-wait-power-on.json' ([ordered]@{hit=$hit; uid=$uid; last=$samples[-1]; samples=$samples})
  if(-not $hit){ Write-Host 'NO_ONLINE'; $http.Dispose(); exit 2 }
  Write-Host 'POWER_ON_HIT'
  $http.Dispose(); return
}

if($phase -eq 'recover-watch'){
  # after power-on, do NOT cancel: watch order resume / HANG / SUCCESS / stuck
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 600 }
  Write-Host "=== recover-watch uid=$uid timeout=${timeoutSec}s (no cancel) ==="
  $samples=@(); $hitHang=$false; $hitSuccess=$false; $hitTerminal=$false
  $progStart=$null; $progMoved=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  $lastSave=(Get-Date)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1500
    $s=Get-Snap $uid
    $samples += $s
    if($null -eq $progStart){ $progStart=$s.progress }
    if($null -ne $s.progress -and $null -ne $progStart -and $s.progress -ne $progStart){ $progMoved=$true }
    Write-Host ("[{0}] order={1} runtime={2} move={3} proc={4} prog={5} m0rc={6}" -f $s.at,$s.orderState,$s.runtimeType,$s.movementState,$s.procState,$s.progress,$s.m0_resultCode)
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -eq 5){ $hitSuccess=$true; break }
    if($s.orderState -in @(2,4,6)){ $hitTerminal=$true; break }
    if(((Get-Date)-$lastSave).TotalSeconds -ge 60){
      Save 'S5-recover-samples-partial.json' $samples
      $lastSave=Get-Date
    }
  }
  $last=$samples[-1]
  Save 'S5-recover-samples.json' $samples
  Save 'S5-recover-summary.json' ([ordered]@{
    uid=$uid; hitHang=$hitHang; hitSuccess=$hitSuccess; hitTerminal=$hitTerminal
    progStart=$progStart; progEnd=$last.progress; progMoved=$progMoved
    finalOrderState=$last.orderState; finalRuntime=$last.runtimeType
    finalMove=$last.movementState; finalProc=$last.procState
    watchSec=$timeoutSec; sampleCount=$samples.Count; last=$last
  })
  Write-Host ("RESULT hang={0} success={1} terminal={2} progMoved={3} finalOrder={4}" -f $hitHang,$hitSuccess,$hitTerminal,$progMoved,$last.orderState)
  $http.Dispose(); return
}

if($phase -eq 'continue-probe'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $s=Get-Snap $uid
  Save 'S6-cont-before.json' $s
  if(-not $s.orderId){ throw 'no orderId' }
  $c=Continue-Hang $s.orderId
  Save 'S6-cont-call.json' $c
  Start-Sleep -Seconds 2
  $after=Get-Snap $uid
  Save 'S6-cont-after.json' $after
  Write-Host ("CONTINUE code={0} order={1}->{2} msg={3}" -f $c.code,$s.orderState,$after.orderState,$c.message)
  $http.Dispose(); return
}

if($phase -eq 'cleanup'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $s=Get-Snap $uid
  Save 'E9-cleanup-before.json' $s
  if($uid -and $s.orderId -and $s.orderState -in @(1,3,7,9)){
    Save 'E9-cleanup-cancel.json' (Cancel-Order $s.orderId $s.numericId 'R34-cleanup')
    Start-Sleep -Seconds 2
  }
  $final=Get-Snap $uid
  Save 'E9-final.json' $final
  Write-Host ("CLEANUP order={0} runtime={1} proc={2}" -f $final.orderState,$final.runtimeType,$final.procState)
  Write-Host 'HUMAN: turn knob back to POWER ON if still off'
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $name = if($args.Count -ge 3){ $args[2] } else { 'snap' }
  $s=Get-Snap $uid
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} runtime={1} proc={2} emerg={3}" -f $s.orderState,$s.runtimeType,$s.procState,$s.emergencyState)
  $http.Dispose(); return
}

throw "unknown phase $phase"


