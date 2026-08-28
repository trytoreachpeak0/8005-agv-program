$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$envPath = Join-Path $labRoot "environment.local.json"
$e = Get-Content -LiteralPath $envPath -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
Write-Host "labRoot=$labRoot"
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$c = [System.Net.Http.HttpClient]::new()
$key = $e.testVehicleKey

function Invoke-Api([string]$method,[string]$url,[string]$json){
  $r=New-Object System.Net.Http.HttpRequestMessage
  $r.Method=[System.Net.Http.HttpMethod]::new($method)
  $r.RequestUri=$url
  [void]$r.Headers.TryAddWithoutValidation("Authorization","Bearer $($e.callApiKey)")
  if(-not [string]::IsNullOrEmpty($json)){ $r.Content=New-Object System.Net.Http.StringContent($json,[System.Text.Encoding]::UTF8,"application/json") }
  $sw=[System.Diagnostics.Stopwatch]::StartNew()
  $resp=$c.SendAsync($r).GetAwaiter().GetResult()
  $sw.Stop()
  $body=[System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
  $parsed=$null; try{ $parsed=$body|ConvertFrom-Json }catch{}
  [pscustomobject]@{status=[int]$resp.StatusCode;elapsedMs=$sw.ElapsedMilliseconds;body=$body;parsed=$parsed}
}
function Save($n,$o){ [System.IO.File]::WriteAllText((Join-Path $outDir $n), ($o|ConvertTo-Json -Depth 20), $utf8) }
function CodeOk($p){ return ($p.code -eq '0' -or $p.code -eq 0) }
function Get-Snap([string]$upperId=$null){
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key"
  $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo
  $det=$null; $by=$null
  if($upperId){
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$upperId"
    $det=$by.parsed.result
  }
  $m0=$null
  if($det -and $det.missions -and $det.missions.Count -gt 0){ $m0=$det.missions[0] }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$v.currentStation; noStation=$v.noStation
    procState=$vti.procState; processingOrder=$vti.processingOrder
    movementState=[string]$v.movementState
    enable=$vti.enable; integrationLevel=[string]$vti.integrationLevel
    fleetMode=[string]$v.fleetMode
    orderState=$(if($det){$det.orderState}else{$null})
    missionState=$(if($m0){$m0.missionState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    orderUuid=$(if($det){$det.orderUuid}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    appointVehicleKey=$(if($det){$det.appointVehicleKey}else{$null})
    upperId=$(if($det){$det.upperId}else{$upperId})
    progress=$(if($det){$det.progress}else{$null})
    rawDetail=$det
  }
}
function Wait-Executing([string]$upperId,[int]$timeoutSec=90){
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $upperId
    if($s.orderState -eq 3 -and $s.movementState -eq 'MT_RUNNING'){ return $s }
    if($s.orderState -in @(5,2,4)){ return $s }
  }
  return (Get-Snap $upperId)
}
function Wait-Terminal([string]$upperId,[int]$timeoutSec=180){
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 900
    $s=Get-Snap $upperId
    if($s.orderState -in @(5,2,4,6)){ return $s }
  }
  return (Get-Snap $upperId)
}
function Wait-Idle([int]$timeoutSec=120){
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $s=Get-Snap $null
    if($s.procState -eq 'IDLE' -and -not $s.processingOrder -and $s.movementState -eq 'MT_FINISHED'){ return $s }
  }
  return (Get-Snap $null)
}
function New-MoveOrder([int]$dest,[string]$tag,[string]$fixedUpperId=$null){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid = if($fixedUpperId){ $fixedUpperId } else { "riot-behavior-lab-$tag-$ts" }
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":29,`"destination`":$dest}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  [pscustomobject]@{uid=$uid; create=$cr; dest=$dest; request=$json}
}
function Cancel-Order([string]$orderIdStr,[int]$numericId,[string]$reason){
  $attempts=@()
  $cmdBody="{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
  $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$orderIdStr" $cmdBody
  $attempts += [ordered]@{api="task/command"; orderId=$orderIdStr; req=$cmdBody; http=$cmd.status; code=$cmd.parsed.code; message=$cmd.parsed.message; body=$cmd.body}
  if(-not (CodeOk $cmd.parsed) -and $numericId){
    $opBody="{`"orderId`":$numericId,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" $opBody
    $attempts += [ordered]@{api="order/operate"; orderId=$numericId; req=$opBody; http=$op.status; code=$op.parsed.code; message=$op.parsed.message; body=$op.body}
  }
  return $attempts
}
function Assert-NoWrongVehicle($snap,$context){
  $ev=$snap.executeVehicleKey
  if($ev -and $ev -ne '--' -and $ev -ne '' -and $ev -ne $key){
    Save "CRITICAL-wrong-vehicle-$context.json" $snap
    throw "CRITICAL wrong executeVehicleKey=$ev context=$context"
  }
}

# ========== E0 BASELINE ==========
"=== E0 BASELINE ==="
$base=Get-Snap $null
Save "E0-baseline.json" $base
"BASELINE station=$($base.station) proc=$($base.procState) enable=$($base.enable) integration=$($base.integrationLevel) move=$($base.movementState)"
if(-not $base.enable -or $base.integrationLevel -ne 'ON_LINE'){ throw "not online" }
if($base.procState -ne 'IDLE' -or $base.processingOrder){ throw "not idle" }

$cur=[int]$base.station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$otherDest = if($cur -eq 2){1}else{2}

# ========== ID-01 Identifier association (during create+SUCCESS short path) ==========
"=== ID-01 + Q-004 path A: create then SUCCESS then resubmit ==="
$oA=New-MoveOrder $otherDest "R10-id-success"
Save "ID-create.json" ([ordered]@{uid=$oA.uid; dest=$otherDest; req=$oA.request; http=$oA.create.status; code=$oA.create.parsed.code; message=$oA.create.parsed.message; result=$oA.create.parsed.result})
if(-not (CodeOk $oA.create.parsed)){ throw "ID create failed: $($oA.create.body)" }
$uidA=$oA.uid
$createResult=$oA.create.parsed.result
$orderIdA=$createResult.orderId

# Cross-query identifiers
$byUpper=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uidA"
$byOrderId=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByOrderId/$orderIdA"
$numericIdA=$byUpper.parsed.result.id
$byNumeric=$null
if($numericIdA){ $byNumeric=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/$numericIdA" }
Save "ID-cross-query.json" ([ordered]@{
  createResultKeys=@($createResult.PSObject.Properties.Name)
  createResult=$createResult
  byUpper=@{http=$byUpper.status; code=$byUpper.parsed.code; result=$byUpper.parsed.result}
  byOrderId=@{http=$byOrderId.status; code=$byOrderId.parsed.code; result=$byOrderId.parsed.result}
  byNumeric=@{numericId=$numericIdA; http=$(if($byNumeric){$byNumeric.status}else{$null}); code=$(if($byNumeric){$byNumeric.parsed.code}else{$null}); result=$(if($byNumeric){$byNumeric.parsed.result}else{$null})}
  consistency=[ordered]@{
    upperId_match=($createResult.upperId -eq $uidA -and $byUpper.parsed.result.upperId -eq $uidA)
    orderId_string_match=($createResult.orderId -eq $byUpper.parsed.result.orderId -and $createResult.orderId -eq $byOrderId.parsed.result.orderId)
    numeric_id_match=($byUpper.parsed.result.id -eq $byOrderId.parsed.result.id)
    appoint_match=($createResult.appointVehicleKey -eq $key)
  }
})
"ID create orderId=$orderIdA numericId=$numericIdA upper=$uidA"

$termA=Wait-Terminal $uidA 180
Assert-NoWrongVehicle $termA "ID-success"
Save "ID-terminal.json" $termA
"ID terminal order=$($termA.orderState) st=$($termA.station) proc=$($termA.procState)"
$idleA=Wait-Idle 120
Save "ID-post-idle.json" $idleA

# Q-004-A: resubmit same upperId after SUCCESS
"=== Q-004-A resubmit after SUCCESS ==="
$dupA=New-MoveOrder $cur "R10-idem-A" $uidA
# note: dest flipped to avoid same-station edge; same upperId
Save "Q004-A-resubmit-after-success.json" ([ordered]@{
  originalUpperId=$uidA
  originalOrderId=$orderIdA
  originalFinalState=$termA.orderState
  resubmitReq=$dupA.request
  http=$dupA.create.status
  code=$dupA.create.parsed.code
  message=$dupA.create.parsed.message
  result=$dupA.create.parsed.result
  msgDetail=$dupA.create.parsed.msgDetail
})
"Q004-A code=$($dupA.create.parsed.code) msg=$($dupA.create.parsed.message) newOrderId=$($dupA.create.parsed.result.orderId)"

# If new order created, cancel/wait and record critical non-idempotent
$dupOrderId=$dupA.create.parsed.result.orderId
$needCleanupDup=$false
if((CodeOk $dupA.create.parsed) -and $dupOrderId -and $dupOrderId -ne $orderIdA){
  $needCleanupDup=$true
  "Q004-A NON-IDEMPOTENT: new order created $dupOrderId"
  Assert-NoWrongVehicle (Get-Snap $uidA) "Q004-A"
  # detail may now point to newest or oldest — capture both queries
  $afterDup=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uidA"
  Save "Q004-A-detail-after-dup.json" ([ordered]@{code=$afterDup.parsed.code; result=$afterDup.parsed.result})
  $attempts=Cancel-Order $dupOrderId ([int]$dupA.create.parsed.result.id) "riot-lab-Q004-A-cleanup"
  Save "Q004-A-cleanup.json" ([ordered]@{attempts=$attempts})
  Wait-Idle 120 | Out-Null
} elseif((CodeOk $dupA.create.parsed) -and $dupOrderId -eq $orderIdA){
  "Q004-A returned same orderId (idempotent reuse)"
} else {
  "Q004-A rejected resubmit"
}

$idleB=Wait-Idle 90
$cur=[int]$idleB.station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$otherDest = if($cur -eq 2){1}else{2}

# ========== Q-004-B: resubmit while EXECUTING ==========
"=== Q-004-B resubmit while EXECUTING ==="
$oB=New-MoveOrder $otherDest "R10-idem-B"
Save "Q004-B-create.json" ([ordered]@{uid=$oB.uid; code=$oB.create.parsed.code; result=$oB.create.parsed.result; req=$oB.request})
if(-not (CodeOk $oB.create.parsed)){ throw "Q004-B create failed" }
$uidB=$oB.uid
$orderIdB=$oB.create.parsed.result.orderId
$execB=Wait-Executing $uidB 90
Save "Q004-B-before-dup.json" $execB
"Q004-B before dup order=$($execB.orderState) move=$($execB.movementState)"

$dupB=New-MoveOrder $cur "R10-idem-B-dup" $uidB
Save "Q004-B-resubmit-while-executing.json" ([ordered]@{
  originalUpperId=$uidB; originalOrderId=$orderIdB; originalState=$execB.orderState
  resubmitReq=$dupB.request; http=$dupB.create.status; code=$dupB.create.parsed.code
  message=$dupB.create.parsed.message; result=$dupB.create.parsed.result
})
"Q004-B code=$($dupB.create.parsed.code) msg=$($dupB.create.parsed.message) newOrderId=$($dupB.create.parsed.result.orderId)"

# Let original finish or cancel both if needed
if((CodeOk $dupB.create.parsed) -and $dupB.create.parsed.result.orderId -and $dupB.create.parsed.result.orderId -ne $orderIdB){
  "Q004-B created SECOND order while first executing — cancel both"
  $nid2=$dupB.create.parsed.result.id
  Cancel-Order $dupB.create.parsed.result.orderId ([int]$nid2) "riot-lab-Q004-B-dup-cleanup" | Out-Null
  Cancel-Order $orderIdB ([int]$execB.numericId) "riot-lab-Q004-B-orig-cleanup" | Out-Null
} else {
  # wait original or cancel
  $tB=Wait-Terminal $uidB 120
  if($tB.orderState -notin @(5,2,4)){
    Cancel-Order $orderIdB ([int]$execB.numericId) "riot-lab-Q004-B-orig-cleanup" | Out-Null
  }
}
Save "Q004-B-after.json" (Get-Snap $uidB)
$idleC=Wait-Idle 120
Save "Q004-B-post-idle.json" $idleC

# ========== NEG negative creates ==========
"=== NEG create boundaries ==="
$negResults=@()
function Try-Neg([string]$name,[string]$json){
  $resp=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  $row=[ordered]@{
    name=$name; req=$json; http=$resp.status; code=$resp.parsed.code
    message=$resp.parsed.message; msgDetail=$resp.parsed.msgDetail
    result=$resp.parsed.result; body=$resp.body
  }
  # safety: if somehow created, cancel and flag
  if((CodeOk $resp.parsed) -and $resp.parsed.result.orderId){
    $row.UNEXPECTED_CREATED=$true
    $ev=$resp.parsed.result.executeVehicleKey
    $row.executeVehicleKey=$ev
    if($ev -and $ev -ne $key -and $ev -ne '--' -and $ev -ne ''){
      $row.CRITICAL_WRONG_VEHICLE=$true
    }
    Cancel-Order $resp.parsed.result.orderId ([int]$resp.parsed.result.id) "riot-lab-NEG-cleanup-$name" | Out-Null
  }
  return $row
}

$tsN=Get-Date -Format 'yyyyMMdd-HHmmss'
$negResults += Try-Neg "fake-vehicleKey" "{`"appointVehicleKey`":`"BROKERX-DOES-NOT-EXIST-riot-lab`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"riot-lab-NEG-fakeveh-$tsN`",`"upperId`":`"riot-lab-NEG-fakeveh-$tsN`",`"mission`":[{`"type`":`"move`",`"mapId`":29,`"destination`":2}]}"
$negResults += Try-Neg "bad-mapId" "{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"riot-lab-NEG-badmap-$tsN`",`"upperId`":`"riot-lab-NEG-badmap-$tsN`",`"mission`":[{`"type`":`"move`",`"mapId`":999999,`"destination`":1}]}"
$negResults += Try-Neg "bad-destination" "{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"riot-lab-NEG-badst-$tsN`",`"upperId`":`"riot-lab-NEG-badst-$tsN`",`"mission`":[{`"type`":`"move`",`"mapId`":29,`"destination`":999999}]}"
$negResults += Try-Neg "missing-appointVehicleKey" "{`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"riot-lab-NEG-nokey-$tsN`",`"upperId`":`"riot-lab-NEG-nokey-$tsN`",`"mission`":[{`"type`":`"move`",`"mapId`":29,`"destination`":2}]}"
Save "NEG-create-results.json" ([ordered]@{at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff'); results=$negResults})
foreach($n in $negResults){ "NEG $($n.name) code=$($n.code) msg=$($n.message) unexpected=$($n.UNEXPECTED_CREATED) critical=$($n.CRITICAL_WRONG_VEHICLE)" }
if($negResults | Where-Object { $_.CRITICAL_WRONG_VEHICLE }){ throw "CRITICAL: negative create dispatched wrong vehicle - STOP" }

$idleD=Wait-Idle 60
$cur=[int]$idleD.station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$otherDest = if($cur -eq 2){1}else{2}

# ========== Q006: pause=false ==========
"=== Q006 pause=false interrupt ==="
$oI=New-MoveOrder $otherDest "R10-irq-false"
Save "Q006-pauseFalse-create.json" ([ordered]@{uid=$oI.uid; code=$oI.create.parsed.code; result=$oI.create.parsed.result})
if(-not (CodeOk $oI.create.parsed)){ throw "pauseFalse create failed" }
$uidI=$oI.uid; $orderIdI=$oI.create.parsed.result.orderId
$execI=Wait-Executing $uidI 90
Save "Q006-pauseFalse-before.json" $execI
$irqBody="{`"orderId`":`"$orderIdI`",`"pause`":false}"
$irq=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/interrupt" $irqBody
Save "Q006-pauseFalse-call.json" ([ordered]@{req=$irqBody; http=$irq.status; code=$irq.parsed.code; message=$irq.parsed.message; body=$irq.body})
"IRQ pause=false code=$($irq.parsed.code) msg=$($irq.parsed.message)"
$irqSamples=@()
for($i=0;$i -lt 8;$i++){ Start-Sleep -Milliseconds 800; $irqSamples += ,(Get-Snap $uidI); "IRQF$i order=$($irqSamples[-1].orderState) proc=$($irqSamples[-1].procState) move=$($irqSamples[-1].movementState)" }
Save "Q006-pauseFalse-samples.json" ([ordered]@{samples=$irqSamples})
$lastI=$irqSamples[-1]
if($lastI.orderState -notin @(5,2,4,6)){
  Cancel-Order $orderIdI ([int]$execI.numericId) "riot-lab-Q006-pauseFalse-cleanup" | Out-Null
}
$idleE=Wait-Idle 120
Save "Q006-pauseFalse-post-idle.json" $idleE

# ========== Q006: HELD + CONTINUE ==========
$cur=[int]$idleE.station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$otherDest = if($cur -eq 2){1}else{2}
"=== Q006 HELD + CONTINUE ==="
$oH=New-MoveOrder $otherDest "R10-held"
Save "Q006-held-create.json" ([ordered]@{uid=$oH.uid; code=$oH.create.parsed.code; result=$oH.create.parsed.result})
if(-not (CodeOk $oH.create.parsed)){ throw "held create failed" }
$uidH=$oH.uid; $orderIdH=$oH.create.parsed.result.orderId
$execH=Wait-Executing $uidH 90
Save "Q006-held-before.json" $execH
$heldBody='{"commandType":"CMD_ORDER_HELD","disableVehicle":false,"reason":"riot-lab-R10-held"}'
$held=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$orderIdH" $heldBody
Save "Q006-held-call.json" ([ordered]@{req=$heldBody; http=$held.status; code=$held.parsed.code; message=$held.parsed.message; body=$held.body})
"HELD code=$($held.parsed.code) msg=$($held.parsed.message)"
$heldSamples=@()
for($i=0;$i -lt 10;$i++){ Start-Sleep -Milliseconds 900; $heldSamples += ,(Get-Snap $uidH); $s=$heldSamples[-1]; "HELD$i order=$($s.orderState) proc=$($s.procState) move=$($s.movementState) st=$($s.station)" }
Save "Q006-held-samples.json" ([ordered]@{samples=$heldSamples})

$contBody='{"commandType":"CMD_ORDER_CONTINUE_FROM_HELD","disableVehicle":false,"reason":"riot-lab-R10-continue"}'
$cont=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$orderIdH" $contBody
Save "Q006-continue-call.json" ([ordered]@{req=$contBody; http=$cont.status; code=$cont.parsed.code; message=$cont.parsed.message; body=$cont.body})
"CONTINUE code=$($cont.parsed.code) msg=$($cont.parsed.message)"
$contSamples=@()
for($i=0;$i -lt 12;$i++){
  Start-Sleep -Milliseconds 900
  $contSamples += ,(Get-Snap $uidH)
  $s=$contSamples[-1]
  "CONT$i order=$($s.orderState) proc=$($s.procState) move=$($s.movementState) st=$($s.station)"
  if($s.orderState -in @(5,2,4,6) -and $s.procState -eq 'IDLE'){ break }
}
Save "Q006-continue-samples.json" ([ordered]@{samples=$contSamples})
$lastH=$contSamples[-1]
if($lastH.orderState -notin @(5,2,4,6)){
  Cancel-Order $orderIdH ([int]$execH.numericId) "riot-lab-Q006-held-cleanup" | Out-Null
}
$idleF=Wait-Idle 120
Save "Q006-held-post-idle.json" $idleF

# ========== Q006: operate cancel equivalence ==========
$cur=[int]$idleF.station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$otherDest = if($cur -eq 2){1}else{2}
"=== Q006 operate cancel ==="
$oO=New-MoveOrder $otherDest "R10-operate-cancel"
Save "Q006-operate-create.json" ([ordered]@{uid=$oO.uid; code=$oO.create.parsed.code; result=$oO.create.parsed.result})
if(-not (CodeOk $oO.create.parsed)){ throw "operate create failed" }
$uidO=$oO.uid; $orderIdO=$oO.create.parsed.result.orderId
$execO=Wait-Executing $uidO 90
Save "Q006-operate-before.json" $execO
$numO=[int]$execO.numericId
$opBody="{`"orderId`":$numO,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"riot-lab-R10-operate-cancel`"}}"
$op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" $opBody
Save "Q006-operate-cancel-call.json" ([ordered]@{req=$opBody; http=$op.status; code=$op.parsed.code; message=$op.parsed.message; body=$op.body; numericId=$numO; stringOrderId=$orderIdO})
"OPERATE cancel code=$($op.parsed.code) msg=$($op.parsed.message)"
$opSamples=@()
for($i=0;$i -lt 15;$i++){
  Start-Sleep -Milliseconds 900
  $opSamples += ,(Get-Snap $uidO)
  $s=$opSamples[-1]
  "OP$i order=$($s.orderState) proc=$($s.procState) move=$($s.movementState)"
  if($s.orderState -in @(2,5,4,6) -and $s.procState -eq 'IDLE' -and -not $s.processingOrder){ break }
}
Save "Q006-operate-samples.json" ([ordered]@{samples=$opSamples})
if($opSamples[-1].orderState -notin @(2,5,4,6)){
  Cancel-Order $orderIdO $numO "riot-lab-R10-operate-fallback-cmd" | Out-Null
}
$idleG=Wait-Idle 120
Save "Q006-operate-post-idle.json" $idleG

# ========== ACT probe (safe) ==========
"=== ACT mission create probe ==="
$tsA=Get-Date -Format 'yyyyMMdd-HHmmss'
$uidAct="riot-behavior-lab-R10-act-$tsA"
# try act alone then move+act; cancel immediately if created
$actBodies=@(
  @{name="act-only-actionId0"; json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uidAct-a`",`"upperId`":`"$uidAct-a`",`"mission`":[{`"type`":`"act`",`"actionId`":0,`"mapId`":29,`"destination`":$cur}]}"},
  @{name="move-then-act"; json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uidAct-b`",`"upperId`":`"$uidAct-b`",`"mission`":[{`"type`":`"move`",`"mapId`":29,`"destination`":$otherDest},{`"type`":`"act`",`"actionId`":0}]}"},
  @{name="act-functionKey-empty"; json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uidAct-c`",`"upperId`":`"$uidAct-c`",`"mission`":[{`"type`":`"act`",`"functionKey`":`"`",`"actionId`":0}]}"}
)
$actResults=@()
foreach($ab in $actBodies){
  $resp=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $ab.json
  $row=[ordered]@{name=$ab.name; req=$ab.json; http=$resp.status; code=$resp.parsed.code; message=$resp.parsed.message; result=$resp.parsed.result}
  if((CodeOk $resp.parsed) -and $resp.parsed.result.orderId){
    $row.created=$true
    $oid=$resp.parsed.result.orderId
    $nid=$resp.parsed.result.id
    # if executing, try interrupt once then cancel
    Start-Sleep -Milliseconds 1200
    $snap=Get-Snap ($resp.parsed.result.upperId)
    $row.snapAfterCreate=$snap
    if($snap.orderState -eq 3){
      $irqA=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/interrupt" "{`"orderId`":`"$oid`",`"pause`":true}"
      $row.interruptWhilePossible=@{code=$irqA.parsed.code; message=$irqA.parsed.message; body=$irqA.body}
    }
    Cancel-Order $oid ([int]$nid) "riot-lab-ACT-probe-cleanup" | Out-Null
    Wait-Idle 90 | Out-Null
  } else {
    $row.created=$false
  }
  $actResults += $row
  "ACT $($ab.name) code=$($row.code) msg=$($row.message) created=$($row.created)"
}
Save "ACT-probe-results.json" ([ordered]@{results=$actResults})

$final=Wait-Idle 60
Save "E0-final.json" $final
"FINAL station=$($final.station) proc=$($final.procState) enable=$($final.enable) integration=$($final.integrationLevel)"

$c.Dispose()
"ALL_DONE"
