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
Write-Host "Round36 HELD-supplement phase=$phase"

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
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    failReason=$(if($det){$det.failReason}else{$null})
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

function New-Move([string]$tag,$dest,[int]$legs=1){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R36-$tag-$ts"
  $missions=@()
  $seq=@($dest,1,$dest,2,$dest)
  $n=[Math]::Max(1,[Math]::Min($legs,$seq.Count))
  for($i=0;$i -lt $n;$i++){ $missions += @{type='move'; mapId=$mapId; destination=[int]$seq[$i]} }
  $payload=@{appointVehicleKey=$key; isAppointEnable=1; lockStatus=0; orderName=$uid; upperId=$uid; mission=$missions}
  $json=$payload|ConvertTo-Json -Depth 8 -Compress
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  return [pscustomobject]@{uid=$uid; dest=$dest; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body; parsed=$cr.parsed; req=$json}
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

function Wait-Exec([string]$uid,[int]$sec=90){
  $samples=@(); $hit=$false
  $deadline=(Get-Date).AddSeconds($sec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3}" -f $s.at,$s.orderState,$s.movementState,$s.procState)
    if($s.orderState -eq 3){ $hit=$true; break }
    if($s.orderState -in @(2,4,5,6,9)){ break }
  }
  return [pscustomobject]@{hit=$hit; samples=$samples; last=$samples[-1]}
}

if($phase -eq 'baseline'){
  $s=Get-Snap $null
  Save 'E0-baseline.json' $s
  Write-Host ("BASE st={0} loc={1} emerg={2} break={3} proc={4} processing={5}" -f $s.station,$s.locationState,$s.emergencyState,$s.breakSwitchState,$s.procState,$s.processingOrder)
  if($s.locationState -ne 'LOCATION_STATE_RUNNING'){ Write-Host 'NEED_LOCALIZE'; $http.Dispose(); exit 2 }
  $http.Dispose(); return
}

if($phase -eq 'p1'){
  # HELD -> CONTINUE -> watch SUCCESS
  $before=Get-Snap $null
  Save 'P1-before.json' $before
  $pick=Pick-Dest $before.station
  $cr=New-Move 'P1' $pick.dest 3
  Save 'P1-create.json' ([ordered]@{uid=$cr.uid; dest=$cr.dest; code=$cr.code; message=$cr.message; req=$cr.req})
  if(-not (CodeOk $cr.parsed)){ throw "create $($cr.code)" }
  Write-Host "CREATED $($cr.uid)"
  $w=Wait-Exec $cr.uid 90
  Save 'P1-exec-samples.json' $w.samples
  if(-not $w.hit){ throw 'no exec' }
  Start-Sleep -Seconds 2
  $held=Send-Cmd $w.last.orderId 'CMD_ORDER_HELD' 'R36-P1-held'
  Save 'P1-held-call.json' $held
  Start-Sleep -Seconds 2
  $afterHeld=Get-Snap $cr.uid
  Save 'P1-after-held.json' $afterHeld
  Write-Host ("HELD code={0} order={1} proc={2} move={3}" -f $held.code,$afterHeld.orderState,$afterHeld.procState,$afterHeld.movementState)
  $cont=Send-Cmd $afterHeld.orderId 'CMD_ORDER_CONTINUE_FROM_HELD' 'R36-P1-cont'
  Save 'P1-cont-call.json' $cont
  Start-Sleep -Seconds 2
  $samples=@(); $hitSuccess=$false; $hitHang=$false
  $deadline=(Get-Date).AddSeconds(300)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1200
    $s=Get-Snap $cr.uid
    $samples += $s
    Write-Host ("[{0}] order={1} move={2} proc={3} prog={4}" -f $s.at,$s.orderState,$s.movementState,$s.procState,$s.progress)
    if($s.orderState -eq 5){ $hitSuccess=$true; break }
    if($s.orderState -eq 9){ $hitHang=$true; break }
    if($s.orderState -in @(2,4,6)){ break }
  }
  Save 'P1-watch-samples.json' $samples
  Save 'P1-summary.json' ([ordered]@{uid=$cr.uid; heldCode=$held.code; contCode=$cont.code; afterHeldOrder=$afterHeld.orderState; hitSuccess=$hitSuccess; hitHang=$hitHang; final=$samples[-1]})
  Write-Host ("P1 RESULT success={0} finalOrder={1}" -f $hitSuccess,$samples[-1].orderState)
  if(-not $hitSuccess -and $samples[-1].orderState -in @(1,3,7,9)){
    Save 'P1-cleanup.json' (Cancel-Order $samples[-1].orderId $samples[-1].numericId 'R36-P1')
  }
  $http.Dispose(); return
}

if($phase -eq 'p2'){
  # HELD then CANCEL
  $before=Get-Snap $null
  $pick=Pick-Dest $before.station
  $cr=New-Move 'P2' $pick.dest 5
  Save 'P2-create.json' ([ordered]@{uid=$cr.uid; code=$cr.code; message=$cr.message})
  if(-not (CodeOk $cr.parsed)){ throw "create $($cr.code)" }
  $w=Wait-Exec $cr.uid 90
  Save 'P2-exec-samples.json' $w.samples
  if(-not $w.hit){ throw 'no exec' }
  Start-Sleep -Seconds 2
  $held=Send-Cmd $w.last.orderId 'CMD_ORDER_HELD' 'R36-P2-held'
  Save 'P2-held-call.json' $held
  Start-Sleep -Seconds 2
  $afterHeld=Get-Snap $cr.uid
  Save 'P2-after-held.json' $afterHeld
  $can=Cancel-Order $afterHeld.orderId $afterHeld.numericId 'R36-P2'
  Save 'P2-cancel-call.json' $can
  Start-Sleep -Seconds 3
  $final=Get-Snap $cr.uid
  $veh=Get-Snap $null
  Save 'P2-final.json' ([ordered]@{order=$final; vehicle=$veh})
  Save 'P2-summary.json' ([ordered]@{uid=$cr.uid; heldOrder=$afterHeld.orderState; cancel=$can; finalOrder=$final.orderState; finalProc=$veh.procState})
  Write-Host ("P2 RESULT finalOrder={0} proc={1}" -f $final.orderState,$veh.procState)
  $http.Dispose(); return
}

if($phase -eq 'p3'){
  # wrong CONTINUE commands
  $before=Get-Snap $null
  $pick=Pick-Dest $before.station
  $cr=New-Move 'P3' $pick.dest 5
  Save 'P3-create.json' ([ordered]@{uid=$cr.uid; code=$cr.code})
  if(-not (CodeOk $cr.parsed)){ throw "create $($cr.code)" }
  $w=Wait-Exec $cr.uid 90
  if(-not $w.hit){ throw 'no exec' }
  $oid=$w.last.orderId
  $wrongHeld=Send-Cmd $oid 'CMD_ORDER_CONTINUE_FROM_HELD' 'R36-P3-wrong-held-while-exec'
  Save 'P3-contHeld-while-exec.json' $wrongHeld
  Start-Sleep -Seconds 1
  $s1=Get-Snap $cr.uid
  Save 'P3-after-wrong-held.json' $s1
  Write-Host ("while EXEC CONTINUE_FROM_HELD code={0} order={1}" -f $wrongHeld.code,$s1.orderState)
  $held=Send-Cmd $oid 'CMD_ORDER_HELD' 'R36-P3-held'
  Save 'P3-held-call.json' $held
  Start-Sleep -Seconds 2
  $s2=Get-Snap $cr.uid
  Save 'P3-after-held.json' $s2
  $wrongHang=Send-Cmd $oid 'CMD_ORDER_CONTINUE_FROM_HANG' 'R36-P3-wrong-hang-while-held'
  Save 'P3-contHang-while-held.json' $wrongHang
  Start-Sleep -Seconds 1
  $s3=Get-Snap $cr.uid
  Save 'P3-after-wrong-hang.json' $s3
  Write-Host ("while HELD CONTINUE_FROM_HANG code={0} order={1}" -f $wrongHang.code,$s3.orderState)
  # recover properly then cancel to cleanup
  $ok=Send-Cmd $oid 'CMD_ORDER_CONTINUE_FROM_HELD' 'R36-P3-ok'
  Save 'P3-cont-ok.json' $ok
  Start-Sleep -Seconds 2
  $s4=Get-Snap $cr.uid
  Save 'P3-cleanup.json' (Cancel-Order $s4.orderId $s4.numericId 'R36-P3')
  Start-Sleep -Seconds 2
  $final=Get-Snap $cr.uid
  Save 'P3-summary.json' ([ordered]@{
    uid=$cr.uid
    contHeldWhileExec=$wrongHeld
    orderAfterWrongHeld=$s1.orderState
    held=$held
    orderAfterHeld=$s2.orderState
    contHangWhileHeld=$wrongHang
    orderAfterWrongHang=$s3.orderState
    contOk=$ok
    finalOrder=$final.orderState
  })
  Write-Host 'P3 DONE'
  $http.Dispose(); return
}

if($phase -eq 'p4'){
  # while HELD, create second order
  $before=Get-Snap $null
  $pick=Pick-Dest $before.station
  $cr1=New-Move 'P4a' $pick.dest 5
  Save 'P4a-create.json' ([ordered]@{uid=$cr1.uid; code=$cr1.code})
  if(-not (CodeOk $cr1.parsed)){ throw "create1 $($cr1.code)" }
  $w=Wait-Exec $cr1.uid 90
  if(-not $w.hit){ throw 'no exec' }
  $held=Send-Cmd $w.last.orderId 'CMD_ORDER_HELD' 'R36-P4-held'
  Save 'P4-held-call.json' $held
  Start-Sleep -Seconds 2
  $heldSnap=Get-Snap $cr1.uid
  Save 'P4-held-snap.json' $heldSnap
  Write-Host ("HELD order={0}" -f $heldSnap.orderState)
  $pick2=Pick-Dest $heldSnap.station
  $cr2=New-Move 'P4b' $pick2.dest 1
  Save 'P4b-create.json' ([ordered]@{uid=$cr2.uid; code=$cr2.code; message=$cr2.message})
  if(-not (CodeOk $cr2.parsed)){ throw "create2 $($cr2.code)" }
  $samples=@()
  $deadline=(Get-Date).AddSeconds(60)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1000
    $a=Get-Snap $cr1.uid
    $b=Get-Snap $cr2.uid
    $samples += [ordered]@{at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff'); a=$a; b=$b}
    Write-Host ("[{0}] A order={1} B order={2} execB={3}" -f (Get-Date -Format 'HH:mm:ss'),$a.orderState,$b.orderState,$b.executeVehicleKey)
    if($b.orderState -eq 3){ break }
  }
  Save 'P4-watch-samples.json' $samples
  $last=$samples[-1]
  Save 'P4-summary.json' ([ordered]@{
    uidA=$cr1.uid; uidB=$cr2.uid
    heldA=$heldSnap.orderState
    finalA=$last.a.orderState; finalB=$last.b.orderState
    bExecKey=$last.b.executeVehicleKey
  })
  # cleanup both
  $fa=Get-Snap $cr1.uid; $fb=Get-Snap $cr2.uid
  Save 'P4-cleanup-A.json' (Cancel-Order $fa.orderId $fa.numericId 'R36-P4a')
  Save 'P4-cleanup-B.json' (Cancel-Order $fb.orderId $fb.numericId 'R36-P4b')
  Start-Sleep -Seconds 2
  Write-Host ("P4 RESULT A={0} B={1}" -f $last.a.orderState,$last.b.orderState)
  $http.Dispose(); return
}

if($phase -eq 'snapshot'){
  $uid = if($args.Count -ge 2){ $args[1] } else { $null }
  $name = if($args.Count -ge 3){ $args[2] } else { 'snap' }
  $s=Get-Snap $uid
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP order={0} loc={1} proc={2} move={3}" -f $s.orderState,$s.locationState,$s.procState,$s.movementState)
  $http.Dispose(); return
}

throw "unknown phase $phase"
