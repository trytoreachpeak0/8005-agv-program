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
Write-Host "Round37 onboard-pause phase=$phase"

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
    faultCodes=$(if($v){$v.faultCodes}else{$null})
    lastErrorCode=$(if($v){$v.lastErrorCode}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
    m0_resultCode=$(if($det -and $det.missions -and $det.missions.Count -gt 0){$det.missions[0].resultCode}else{$null})
    m0_resultStr=$(if($det -and $det.missions -and $det.missions.Count -gt 0){$det.missions[0].resultStr}else{$null})
  }
}

function Pick-Dest($cur){
  $best=$null
  foreach($sid in @(5,2,6,1,3,4)){
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

function New-LongMove([string]$tag,$dest){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R37-$tag-$ts"
  $missions=@(
    @{type='move'; mapId=$mapId; destination=[int]$dest},
    @{type='move'; mapId=$mapId; destination=1},
    @{type='move'; mapId=$mapId; destination=[int]$dest},
    @{type='move'; mapId=$mapId; destination=2},
    @{type='move'; mapId=$mapId; destination=[int]$dest}
  )
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

if($phase -eq 'baseline'){
  $s=Get-Snap $null
  Save 'E0-baseline.json' $s
  Write-Host ("BASE st={0} loc={1} emerg={2} break={3} proc={4}" -f $s.station,$s.locationState,$s.emergencyState,$s.breakSwitchState,$s.procState)
  $http.Dispose(); return
}

if($phase -eq 'create-exec'){
  $before=Get-Snap $null
  Save 'S1-before.json' $before
  $pick=Pick-Dest $before.station
  $cr=New-LongMove 'OnboardPause' $pick.dest
  Save 'S1-create.json' ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req})
  if(-not (CodeOk $cr.parsed)){ throw "create $($cr.code) $($cr.message)" }
  Write-Host "CREATED $($cr.uid) dest=$($pick.dest)"
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds(90)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3} speed={4}" -f $s.at,$s.orderState,$s.movementState,$s.procState,$s.speed)
    if($s.orderState -eq 3 -and $s.movementState -eq 'MT_RUNNING'){ $hit=$true; break }
    if($s.orderState -eq 3 -and $s.procState -eq 'PROCESSING_ORDER'){ $hit=$true; break }
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save 'S1-exec-samples.json' $samples
  Save 'S1-exec-hit.json' ([ordered]@{hitExec=$hit; uid=$cr.uid; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_EXEC'; $http.Dispose(); exit 2 }
  Write-Host "EXEC_REACHED uid=$($cr.uid)"
  Write-Host 'HUMAN: pause on ONBOARD AGV UI now (not RIoT HELD)'
  $http.Dispose(); return
}

if($phase -eq 'wait-pause'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 180 }
  Write-Host "=== wait-pause uid=$uid timeout=${timeoutSec}s ==="
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3} speed={4} emerg={5}" -f $s.at,$s.orderState,$s.movementState,$s.procState,$s.speed,$s.emergencyState)
    # heuristics: paused movement, speed 0 while still processing, or state change from RUNNING
    if($s.movementState -eq 'MT_PAUSED'){ $hit=$true; break }
    if($s.orderState -eq 7){ $hit=$true; break }
    if($s.orderState -eq 9){ $hit=$true; break }
    if($s.procState -eq 'INNER_PAUSE' -or $s.procState -eq 'USER_FORCE_IDLE'){ $hit=$true; break }
    if($s.orderState -eq 3 -and $s.speed -eq 0 -and $s.movementState -and $s.movementState -ne 'MT_RUNNING' -and $s.movementState -ne 'MT_WAIT_FOR_START'){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save 'S2-wait-pause.json' ([ordered]@{hit=$hit; uid=$uid; last=$samples[-1]; samples=$samples})
  if(-not $hit){ Write-Host 'NO_PAUSE_SIGNAL'; $http.Dispose(); exit 2 }
  Write-Host 'PAUSE_SIGNAL_HIT'
  $http.Dispose(); return
}

if($phase -eq 'probe'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $before=Get-Snap $uid
  Save 'S3-before-probe.json' $before
  if(-not $before.orderId){ throw 'no orderId' }
  $probes=@()
  foreach($cmd in @('CMD_ORDER_CONTINUE_FROM_HELD','CMD_ORDER_CONTINUE_FROM_HANG','CMD_ORDER_HELD')){
    $c=Send-Cmd $before.orderId $cmd "R37-$cmd"
    Start-Sleep -Seconds 2
    $after=Get-Snap $uid
    $probes += [ordered]@{cmd=$cmd; call=$c; after=$after}
    Save ("S3-probe-$cmd.json") ([ordered]@{call=$c; after=$after})
    Write-Host ("PROBE {0} code={1} order={2}->{3} move={4} proc={5}" -f $cmd,$c.code,$before.orderState,$after.orderState,$after.movementState,$after.procState)
    $before=$after
    # if recovered to running, stop further probes
    if($after.orderState -eq 3 -and $after.movementState -eq 'MT_RUNNING'){ break }
    if($after.orderState -eq 5){ break }
  }
  Save 'S3-probe-summary.json' ([ordered]@{uid=$uid; probes=$probes; final=$before})
  $http.Dispose(); return
}

if($phase -eq 'watch'){
  $uid = if($args.Count -ge 2){ $args[1] } else { throw 'need uid' }
  $timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 180 }
  $samples=@()
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1200
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3} prog={4} speed={5}" -f $s.at,$s.orderState,$s.movementState,$s.procState,$s.progress,$s.speed)
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  Save 'S4-watch-samples.json' $samples
  Save 'S4-watch-summary.json' ([ordered]@{uid=$uid; final=$samples[-1]; sampleCount=$samples.Count})
  Write-Host ("WATCH finalOrder={0}" -f $samples[-1].orderState)
  $http.Dispose(); return
}

if($phase -eq 'cleanup'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $s=Get-Snap $uid
  Save 'E9-before.json' $s
  if($uid -and $s.orderId -and $s.orderState -in @(1,3,7,9)){
    Save 'E9-cancel.json' (Cancel-Order $s.orderId $s.numericId 'R37-cleanup')
    Start-Sleep -Seconds 2
  }
  $final=Get-Snap $uid
  Save 'E9-final.json' $final
  Write-Host ("CLEANUP order={0} proc={1} move={2}" -f $final.orderState,$final.procState,$final.movementState)
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $name = if($args.Count -ge 3){ $args[2] } else { 'snap' }
  $s=Get-Snap $uid
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} move={1} proc={2} speed={3}" -f $s.orderState,$s.movementState,$s.procState,$s.speed)
  $http.Dispose(); return
}

throw "unknown phase $phase"
