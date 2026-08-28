$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
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
  $resp=$c.SendAsync($r).GetAwaiter().GetResult()
  $body=[System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
  $parsed=$null; try{ $parsed=$body|ConvertFrom-Json }catch{}
  [pscustomobject]@{status=[int]$resp.StatusCode;body=$body;parsed=$parsed}
}
function Save($n,$o){ [System.IO.File]::WriteAllText((Join-Path $outDir $n), ($o|ConvertTo-Json -Depth 22), $utf8) }
function CodeOk($p){ return ($p.code -eq '0' -or $p.code -eq 0) }
function Get-Snap([string]$upperId){
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo
  $det=$null
  if($upperId){
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$upperId" $null
    $det=$by.parsed.result
  }
  $m0=$null; $mTypes=@(); $execIdx=$null
  if($det){
    $execIdx=$det.executingIndex
    if($det.missions){
      foreach($m in $det.missions){ $mTypes += $m.type }
      if($det.missions.Count -gt 0){
        $idx=0
        if($null -ne $execIdx -and $execIdx -ge 0 -and $execIdx -lt $det.missions.Count){ $idx=[int]$execIdx }
        $m0=$det.missions[$idx]
      }
    }
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$v.currentStation; noStation=$v.noStation
    procState=$vti.procState; processingOrder=$vti.processingOrder
    movementState=[string]$v.movementState
    enable=$vti.enable; integrationLevel=[string]$vti.integrationLevel
    fleetMode=[string]$v.fleetMode
    orderState=$(if($det){$det.orderState}else{$null})
    missionState=$(if($m0){$m0.missionState}else{$null})
    missionType=$(if($m0){$m0.type}else{$null})
    missionTypes=$mTypes
    executingIndex=$execIdx
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    appointVehicleKey=$(if($det){$det.appointVehicleKey}else{$null})
    upperId=$(if($det){$det.upperId}else{$upperId})
    progress=$(if($det){$det.progress}else{$null})
  }
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
function Wait-Executing([string]$upperId,[int]$timeoutSec=90){
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $upperId
    if($s.orderState -eq 3){ return $s }
    if($s.orderState -in @(5,2,4)){ return $s }
  }
  return (Get-Snap $upperId)
}
function New-Order([string]$tag,$missionArr){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-$tag-$ts"
  $missionsJson = ($missionArr | ConvertTo-Json -Depth 6 -Compress)
  if($missionArr.Count -eq 1){ $missionsJson = "[$missionsJson]" }
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":$missionsJson}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  [pscustomobject]@{uid=$uid; create=$cr; request=$json}
}
function Cancel-Order([string]$orderIdStr,$numericId,[string]$reason){
  $attempts=@()
  if($orderIdStr){
    $cmdBody="{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
    $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$orderIdStr" $cmdBody
    $attempts += [ordered]@{api="task/command"; code=$cmd.parsed.code; message=$cmd.parsed.message; body=$cmd.body}
  }
  if($numericId){
    $opBody="{`"orderId`":$numericId,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" $opBody
    $attempts += [ordered]@{api="order/operate"; code=$op.parsed.code; message=$op.parsed.message; body=$op.body}
  }
  return $attempts
}
function Send-Cmd([string]$orderIdStr,[string]$cmdType,[string]$reason){
  $body="{`"commandType`":`"$cmdType`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$orderIdStr" $body
  [pscustomobject]@{req=$body; code=$r.parsed.code; message=$r.parsed.message; body=$r.body}
}

"=== RESUME check online ==="
$base=Get-Snap $null
Save "E0-baseline-resume.json" $base
"RESUME st=$($base.station) proc=$($base.procState) enable=$($base.enable) integ=$($base.integrationLevel)"
if(-not $base.enable -or $base.integrationLevel -ne 'ON_LINE'){ throw "still not online - need human" }
if($base.procState -ne 'IDLE' -or $base.processingOrder){ throw "not idle" }

$cur=[int]$base.station
if($cur -ne 1 -and $cur -ne 2){ $cur=2 }

# S3 multimove
"=== S3 multi move ==="
$d1 = if($cur -eq 2){1}else{2}
$d2 = $cur
$missions = @(@{type='move'; mapId=29; destination=$d1}, @{type='move'; mapId=29; destination=$d2})
$o3=New-Order "R11-multimove" $missions
Save "S3-multimove-create.json" ([ordered]@{uid=$o3.uid; req=$o3.request; code=$o3.create.parsed.code; message=$o3.create.parsed.message; result=$o3.create.parsed.result})
if(-not (CodeOk $o3.create.parsed)){ throw "multimove create failed" }
$uid3=$o3.uid
$samples3=@(); $prevSig=$null; $transitions3=@()
$deadline=(Get-Date).AddMinutes(4)
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 900
  $s=Get-Snap $uid3
  $samples3 += $s
  $sig="o=$($s.orderState)|idx=$($s.executingIndex)|mt=$($s.missionType)|ms=$($s.missionState)|proc=$($s.procState)|move=$($s.movementState)|st=$($s.station)"
  if($sig -ne $prevSig){ $transitions3 += [ordered]@{at=$s.at; sig=$sig; orderState=$s.orderState; executingIndex=$s.executingIndex; missionType=$s.missionType; missionState=$s.missionState; procState=$s.procState; movementState=$s.movementState; station=$s.station}; $prevSig=$sig; "MM-TRANS $sig" } else { "MM $sig" }
  if($s.executeVehicleKey -and $s.executeVehicleKey -ne '--' -and $s.executeVehicleKey -ne $key -and $s.executeVehicleKey -ne ''){ throw "CRITICAL wrong vehicle" }
  if($s.orderState -in @(5,2,4,6)){ break }
}
Save "S3-multimove-samples.json" ([ordered]@{upperId=$uid3; transitions=$transitions3; samples=$samples3; final=$samples3[-1]})
$idle3=Wait-Idle 90
Save "S3-post-idle.json" $idle3

# S4 REJECTED
"=== S4 REJECTED ==="
$cur=[int](Get-Snap $null).station
if($cur -ne 1 -and $cur -ne 2){ $cur=2 }
$other = if($cur -eq 2){1}else{2}
$o4=New-Order "R11-rejected" @(@{type='move'; mapId=29; destination=$other})
Save "S4-create.json" ([ordered]@{uid=$o4.uid; code=$o4.create.parsed.code; result=$o4.create.parsed.result})
if(-not (CodeOk $o4.create.parsed)){ throw "S4 create failed" }
$uid4=$o4.uid; $oid4=$o4.create.parsed.result.orderId; $nid4=$o4.create.parsed.result.id
$exec4=Wait-Executing $uid4 90
Save "S4-before-rejected.json" $exec4
$rej=Send-Cmd $oid4 "CMD_ORDER_REJECTED" "riot-lab-R11-rejected"
Save "S4-rejected-call.json" $rej
"REJECTED code=$($rej.code) msg=$($rej.message)"
$rejSamples=@()
for($i=0;$i -lt 8;$i++){ Start-Sleep -Milliseconds 900; $rejSamples += ,(Get-Snap $uid4); "REJ$i order=$($rejSamples[-1].orderState) proc=$($rejSamples[-1].procState) move=$($rejSamples[-1].movementState)" }
Save "S4-rejected-samples.json" ([ordered]@{samples=$rejSamples})
$contRej=Send-Cmd $oid4 "CMD_ORDER_CONTINUE_FROM_REJECTED" "riot-lab-R11-cont-rej"
Save "S4-continue-rejected-call.json" $contRej
"CONT_REJECTED code=$($contRej.code) msg=$($contRej.message)"
$contRejSamples=@()
for($i=0;$i -lt 6;$i++){ Start-Sleep -Milliseconds 800; $contRejSamples += ,(Get-Snap $uid4); "CREJ$i order=$($contRejSamples[-1].orderState) proc=$($contRejSamples[-1].procState)" }
Save "S4-continue-rejected-samples.json" ([ordered]@{samples=$contRejSamples})
$hangProbe=@()
foreach($cmd in @('CMD_ORDER_CONTINUE_FROM_HANG','CMD_ORDER_JUMP_FROM_HANG')){
  $r=Send-Cmd $oid4 $cmd "riot-lab-R11-$cmd"
  $hangProbe += [ordered]@{cmd=$cmd; code=$r.code; message=$r.message; body=$r.body; snap=(Get-Snap $uid4)}
  "HANGPROBE $cmd code=$($r.code) order=$($hangProbe[-1].snap.orderState)"
}
Save "S4-hang-probes.json" ([ordered]@{probes=$hangProbe})
$last4=Get-Snap $uid4
if($last4.orderState -notin @(5,2,4,6)){ Cancel-Order $oid4 $nid4 "riot-lab-R11-S4-cleanup" | Out-Null }
$idle4=Wait-Idle 120
Save "S4-post-idle.json" $idle4

# S5 act wait interrupt
"=== S5 act wait interrupt ==="
$cur=[int](Get-Snap $null).station
if($cur -ne 1 -and $cur -ne 2){ $cur=2 }
$other = if($cur -eq 2){1}else{2}
$missions5 = @(@{type='move'; mapId=29; destination=$other}, @{type='act'; actionId=129; actionParam1=15; actionName='wait15s'})
$o5=New-Order "R11-act-irq" $missions5
Save "S5-create.json" ([ordered]@{uid=$o5.uid; req=$o5.request; code=$o5.create.parsed.code; message=$o5.create.parsed.message; result=$o5.create.parsed.result})
if(-not (CodeOk $o5.create.parsed)){ throw "S5 create failed" }
$uid5=$o5.uid; $oid5=$o5.create.parsed.result.orderId; $nid5=$o5.create.parsed.result.id
$actReached=$false; $preSamples=@()
$deadline=(Get-Date).AddMinutes(3)
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 700
  $s=Get-Snap $uid5
  $preSamples += $s
  "ACTWAIT order=$($s.orderState) idx=$($s.executingIndex) mt=$($s.missionType) types=$($s.missionTypes -join ',') proc=$($s.procState) move=$($s.movementState) st=$($s.station)"
  if($s.orderState -eq 3 -and ($s.missionType -eq 'act' -or ([int]$s.executingIndex -ge 1))){ $actReached=$true; break }
  if($s.orderState -in @(5,2,4,6)){ break }
}
Save "S5-before-interrupt.json" ([ordered]@{actReached=$actReached; samples=$preSamples; last=$preSamples[-1]})
$irq=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/interrupt" "{`"orderId`":`"$oid5`",`"pause`":true}"
Save "S5-interrupt-call.json" ([ordered]@{actReached=$actReached; code=$irq.parsed.code; message=$irq.parsed.message; body=$irq.body})
"ACT-IRQ actReached=$actReached code=$($irq.parsed.code) msg=$($irq.parsed.message)"
$irqSamples=@()
for($i=0;$i -lt 12;$i++){
  Start-Sleep -Milliseconds 900
  $irqSamples += ,(Get-Snap $uid5)
  $s=$irqSamples[-1]
  "AI$i order=$($s.orderState) idx=$($s.executingIndex) mt=$($s.missionType) proc=$($s.procState) move=$($s.movementState)"
  if($s.orderState -in @(5,2,4,6,7,8,9) -and $s.procState -eq 'IDLE'){ break }
}
Save "S5-after-interrupt-samples.json" ([ordered]@{samples=$irqSamples})
$last5=$irqSamples[-1]
if($last5.orderState -notin @(5,2,4,6) -or $last5.processingOrder -or $last5.procState -ne 'IDLE'){
  Cancel-Order $oid5 $nid5 "riot-lab-R11-S5-cleanup" | Out-Null
}
$idle5=Wait-Idle 120

"=== S5b act-only ==="
$missions5b = @(@{type='act'; actionId=129; actionParam1=5; actionName='wait5s'; mapId=29; destination=$idle5.station})
$o5b=New-Order "R11-actonly" $missions5b
Save "S5b-create.json" ([ordered]@{uid=$o5b.uid; req=$o5b.request; code=$o5b.create.parsed.code; message=$o5b.create.parsed.message; result=$o5b.create.parsed.result})
if(CodeOk $o5b.create.parsed){
  $uid5b=$o5b.uid; $oid5b=$o5b.create.parsed.result.orderId; $nid5b=$o5b.create.parsed.result.id
  $actOnlySamples=@(); $didIrq=$false
  $deadline=(Get-Date).AddSeconds(30)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 500
    $s=Get-Snap $uid5b
    $actOnlySamples += $s
    "AO order=$($s.orderState) mt=$($s.missionType) proc=$($s.procState) exec=$($s.executeVehicleKey)"
    if(-not $didIrq -and $s.orderState -eq 3){
      $irq2=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/interrupt" "{`"orderId`":`"$oid5b`",`"pause`":true}"
      Save "S5b-interrupt-call.json" ([ordered]@{code=$irq2.parsed.code; message=$irq2.parsed.message; body=$irq2.body})
      "AO-IRQ code=$($irq2.parsed.code)"
      $didIrq=$true
    }
    if($s.orderState -in @(5,2,4,6)){ break }
  }
  Save "S5b-samples.json" ([ordered]@{samples=$actOnlySamples})
  $lf=Get-Snap $uid5b
  if($lf.orderState -notin @(5,2,4,6)){ Cancel-Order $oid5b $nid5b "riot-lab-R11-S5b-cleanup" | Out-Null }
}
$final=Wait-Idle 90
Save "E0-final.json" $final
"FINAL st=$($final.station) proc=$($final.procState) enable=$($final.enable) integ=$($final.integrationLevel)"
$c.Dispose()
"ALL_DONE"
