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
Write-Host "Round31 SW-estop-long phase=$phase key=$key mapId=$mapId"

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
    speed=$(if($v){$v.speed}else{$null})
    faultCodes=$(if($v){$v.faultCodes}else{$null})
    lastErrorCode=$(if($v){$v.lastErrorCode}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
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

if($phase -eq 'create-exec'){
  $waitSec = if($args.Count -ge 2){ [int]$args[1] } else { 120 }
  $base=Get-Snap $null
  Save 'S1-before.json' $base
  $legs=@(3,1,3,6,3,1,3,2,3)
  $missions=@()
  foreach($d in $legs){ $missions += @{type='move'; mapId=$mapId; destination=[int]$d} }
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R31-Bsw-$ts"
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
    Write-Host ("[{0}] order={1} move={2} emerg={3} proc={4} st={5}" -f $s.at,$s.orderState,$s.movementState,$s.emergencyState,$s.procState,$s.station)
    if($s.orderState -eq 3){ $hit=$true; break }
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save 'S1-to-exec-samples.json' $samples
  Save 'S1-exec-hit.json' ([ordered]@{hitExec=$hit; uid=$uid; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_EXEC'; $http.Dispose(); exit 2 }
  Write-Host "EXEC_REACHED uid=$uid"
  $http.Dispose(); return
}

if($phase -eq 'trigger-sw'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $before=Get-Snap $uid
  Save 'S2-before-trigger.json' $before
  $tr=Invoke-Emerg 'triggerEmergency'
  Save 'S2-triggerEmergency.json' $tr
  Start-Sleep -Seconds 2
  $after=Get-Snap $uid
  Save 'S2-after-trigger.json' $after
  Write-Host ("trigger code={0} emerg={1}->{2} order={3}" -f $tr.code,$before.emergencyState,$after.emergencyState,$after.orderState)
  $http.Dispose(); return
}

if($phase -eq 'hang-watch'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 900 }
  Write-Host "=== hang-watch uid=$uid timeout=${timeoutSec}s ==="
  $samples=@(); $hitHang=$false; $emergSeen=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  $lastSave=(Get-Date)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1500
    $s=Get-Snap $uid
    $samples += $s
    if($s.emergencyState -eq 'CAN_RECOVER'){ $emergSeen=$true }
    Write-Host ("[{0}] order={1} emerg={2} move={3} break={4} proc={5} prog={6} m0rc={7}" -f $s.at,$s.orderState,$s.emergencyState,$s.movementState,$s.breakSwitchState,$s.procState,$s.progress,$s.m0_resultCode)
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -in @(2,4,5,6)){ break }
    if(((Get-Date)-$lastSave).TotalSeconds -ge 60){
      Save 'S3-hang-samples-partial.json' $samples
      $lastSave=Get-Date
    }
  }
  Save 'S3-hang-samples.json' $samples
  Save 'S3-hang-hit.json' ([ordered]@{hitHang=$hitHang; emergSeen=$emergSeen; uid=$uid; sampleCount=$samples.Count; last=$samples[-1]; first=$samples[0]; watchSec=$timeoutSec})
  if($hitHang){ Write-Host 'HANG_HIT' }
  else { Write-Host ("END order={0} emergSeen={1} lastEmerg={2}" -f $samples[-1].orderState,$emergSeen,$samples[-1].emergencyState) }
  $http.Dispose(); return
}

if($phase -eq 'cleanup'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $s=Get-Snap $uid
  Save 'E9-cleanup-before.json' $s
  if($uid -and $s.orderId -and $s.orderState -in @(1,3,7,9)){
    Save 'E9-cleanup-cancel.json' (Cancel-Order $s.orderId $s.numericId 'R31-cleanup')
    Start-Sleep -Seconds 2
  }
  $ce=Invoke-Emerg 'cancelEmergency'
  Save 'E9-cancelEmergency.json' $ce
  Start-Sleep -Seconds 2
  $final=Get-Snap $uid
  Save 'E9-final.json' $final
  Write-Host ("CLEANUP order={0} emerg={1} proc={2}" -f $final.orderState,$final.emergencyState,$final.procState)
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $name = if($args.Count -ge 3){ $args[2] } else { 'snap' }
  $s=Get-Snap $uid
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} emerg={1} proc={2} break={3}" -f $s.orderState,$s.emergencyState,$s.procState,$s.breakSwitchState)
  $http.Dispose(); return
}

throw "unknown phase $phase"
