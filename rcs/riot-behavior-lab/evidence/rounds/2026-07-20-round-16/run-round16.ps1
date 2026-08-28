$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$http = [System.Net.Http.HttpClient]::new()
$key = $e.testVehicleKey
$mapId = 28
Write-Host "labRoot=$labRoot mapId=$mapId key=$key"

function Invoke-Api([string]$method,[string]$url,[string]$json){
  $r=New-Object System.Net.Http.HttpRequestMessage
  $r.Method=[System.Net.Http.HttpMethod]::new($method)
  $r.RequestUri=$url
  [void]$r.Headers.TryAddWithoutValidation("Authorization","Bearer $($e.callApiKey)")
  if(-not [string]::IsNullOrEmpty($json)){ $r.Content=New-Object System.Net.Http.StringContent($json,[System.Text.Encoding]::UTF8,"application/json") }
  $resp=$http.SendAsync($r).GetAwaiter().GetResult()
  $body=[System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
  $parsed=$null; try{ $parsed=$body|ConvertFrom-Json }catch{}
  [pscustomobject]@{status=[int]$resp.StatusCode;body=$body;parsed=$parsed}
}
function Save($n,$o){ [System.IO.File]::WriteAllText((Join-Path $outDir $n), ($o|ConvertTo-Json -Depth 24), $utf8) }
function Preview($body,[int]$n=2500){ if([string]::IsNullOrEmpty($body)){return $body}; if($body.Length -le $n){return $body}; return $body.Substring(0,$n)+'...(truncated)' }
function CodeOk($p){ return ($p -and ($p.code -eq '0' -or $p.code -eq 0)) }
function Get-Snap([string]$upperId){
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo
  $det=$null
  if($upperId){
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$upperId" $null
    $det=$by.parsed.result
  }
  $m0=$null
  if($det -and $det.missions -and $det.missions.Count -gt 0){ $m0=$det.missions[0] }
  $remain=$null
  if($det -and $det.orderId){
    $rem=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/curRemainCost/$($det.orderId)" $null
    $remain=[ordered]@{code=$rem.parsed.code; result=$rem.parsed.result; message=$rem.parsed.message}
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$v.currentStation; noStation=$v.noStation
    mapName=$(if($v.previousState){$v.previousState.mapName}else{$null})
    procState=$vti.procState; processingOrder=$vti.processingOrder
    movementState=[string]$v.movementState
    enable=$vti.enable; integrationLevel=[string]$vti.integrationLevel
    orderState=$(if($det){$det.orderState}else{$null})
    missionState=$(if($m0){$m0.missionState}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    appointVehicleKey=$(if($det){$det.appointVehicleKey}else{$null})
    finalState=$(if($det){$det.finalState}else{$null})
    remainCost=$(if($remain){$remain.result}else{$null})
    remainCode=$(if($remain){$remain.code}else{$null})
    upperId=$(if($det){$det.upperId}else{$upperId})
  }
}
function New-Move([int]$dest,[string]$tag){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-$tag-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$dest}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  [pscustomobject]@{uid=$uid; request=$json; create=$cr}
}
function Cancel-Order([string]$oid,$nid,[string]$reason){
  $attempts=@()
  $cmdOk=$false
  if($oid){
    $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
    $attempts += [ordered]@{api='command'; orderId=$oid; code=$cmd.parsed.code; message=$cmd.parsed.message}
    $cmdOk=CodeOk $cmd.parsed
  }
  if($nid -and -not $cmdOk){
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" "{`"orderId`":$nid,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $attempts += [ordered]@{api='operate'; numericId=$nid; code=$op.parsed.code; message=$op.parsed.message}
  }
  return $attempts
}
function Wait-Idle([int]$sec=180){
  $deadline=(Get-Date).AddSeconds($sec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $s=Get-Snap $null
    if($s.procState -eq 'IDLE' -and -not $s.processingOrder -and $s.movementState -eq 'MT_FINISHED'){ return $s }
  }
  return (Get-Snap $null)
}
function Clear-MyNonFinal([string]$reason){
  $list=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord?pageNum=1&pageSize=100&filterByState=1&filterByState=3&filterByState=7&filterByState=9" $null
  $done=@()
  if($list.parsed.result.records){
    foreach($rec in $list.parsed.result.records){
      if($rec.appointVehicleKey -eq $key -or $rec.executeVehicleKey -eq $key){
        $done += [ordered]@{orderId=$rec.orderId; state=$rec.orderState; cancel=(Cancel-Order $rec.orderId $rec.id $reason)}
      }
    }
  }
  return $done
}

@'
# Round 16（2026-07-20）
1. curRemainCost @ EXECUTING（map28）
2. map28 完整跑单闭环 28→1
4. orderRecordPriorityExec 优先执行
不测：order/route、currentMapExistNotFinalOrderTask（已挪到以后可能需要）
'@ | Set-Content -Encoding UTF8 (Join-Path $roundDir 'round-plan.md')

"=== E0 ==="
$base=Get-Snap $null
Save 'E0-baseline.json' $base
if($base.mapName -notmatch '2opt'){ throw "not on map28: $($base.mapName)" }
if($base.procState -ne 'IDLE' -or $base.processingOrder){ 
  $pre=Clear-MyNonFinal 'R16-E0-preclear'
  Save 'E0-preclear.json' $pre
  $base=Wait-Idle 120
  Save 'E0-after-preclear.json' $base
}
if($base.enable -ne $true -or $base.integrationLevel -ne 'ON_LINE'){ throw 'not online' }
Write-Host ("OK map={0} station={1}" -f $base.mapName,$base.station)

"=== R0 same-map costs ==="
$costTargets=@(1,3,4,29)
$costs=@()
foreach($sid in $costTargets){
  $json=(@{mapId=28; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
  $c0=$null; $msg=$null
  if($r.parsed.result.deviceCostsList -and $r.parsed.result.deviceCostsList.Count -gt 0){
    $c0=$r.parsed.result.deviceCostsList[0].costs
    $msg=$r.parsed.result.deviceCostsList[0].message
  }
  $costs += [ordered]@{stationId=$sid; costs=$c0; message=$msg; code=$r.parsed.code}
  Write-Host ("cost st={0} -> {1} ({2})" -f $sid,$c0,$msg)
}
Save 'R0-same-map28-costs.json' $costs

# pick dest with positive cost; prefer station 1 if ok
$dest1=1
$cost1=($costs | Where-Object { $_.stationId -eq 1 } | Select-Object -First 1)
if(-not $cost1 -or $cost1.costs -lt 0){ $dest1=29 }

"=== S1 map28 closed-loop + remain 28->$dest1 ==="
$ord=New-Move $dest1 'R16-S1-loop'
Save 'S1-create.json' $ord
if(-not (CodeOk $ord.create.parsed)){ throw "S1 create failed: $($ord.create.body)" }

$samples=@()
$deadline=(Get-Date).AddSeconds(300)
$gotExec=$false
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 900
  $s=Get-Snap $ord.uid
  $samples += $s
  Write-Host ("[{0}] order={1} proc={2} move={3} st={4} remain={5}" -f $s.at,$s.orderState,$s.procState,$s.movementState,$s.station,$s.remainCost)
  if($s.orderState -eq 3){ $gotExec=$true }
  if($s.orderState -eq 5){ break }
  if($s.orderState -in @(2,4,6)){ break }
}
Save 'S1-dense-samples.json' $samples
$s1final=Get-Snap $ord.uid
Save 'S1-final.json' $s1final
Write-Host ("S1 final orderState={0} remainSamplesExec={1}" -f $s1final.orderState, (($samples | Where-Object { $_.orderState -eq 3 -and $_.remainCost -ne $null }).Count))

if($s1final.orderState -in @(1,3,7,9)){
  $cxl=Cancel-Order $s1final.orderId $s1final.numericId 'R16-S1-timeout-cancel'
  Save 'S1-timeout-cancel.json' $cxl
}
$idle1=Wait-Idle 180
Save 'S1-idle.json' $idle1

"=== S2 priorityExec ==="
# Create A longish to dest 3 or 4, then B and C queue, priority C, cancel A, see who runs
$destA=3
$costA=($costs | Where-Object { $_.stationId -eq 3 } | Select-Object -First 1)
if(-not $costA -or $costA.costs -lt 0){ $destA=4 }
$destB=1
$destC=29
if($idle1.station -eq 1){ $destA=3; $destB=29; $destC=4 }

$ordA=New-Move $destA 'R16-S2-A'
Save 'S2-A-create.json' $ordA
if(-not (CodeOk $ordA.create.parsed)){ throw "A create failed" }

# wait EXECUTING
$deadline=(Get-Date).AddSeconds(90)
$snapA=$null
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 700
  $snapA=Get-Snap $ordA.uid
  if($snapA.orderState -eq 3){ break }
  if($snapA.orderState -in @(2,4,5,6)){ break }
}
Save 'S2-A-executing.json' $snapA
Write-Host ("A state={0} oid={1}" -f $snapA.orderState,$snapA.orderId)
if($snapA.orderState -ne 3){ throw "A not EXECUTING" }

$ordB=New-Move $destB 'R16-S2-B'
Start-Sleep -Milliseconds 400
$ordC=New-Move $destC 'R16-S2-C'
Save 'S2-BC-create.json' ([ordered]@{B=$ordB; C=$ordC})
Start-Sleep -Seconds 2
$snapB=Get-Snap $ordB.uid
$snapC=Get-Snap $ordC.uid
Save 'S2-BC-before-priority.json' ([ordered]@{B=$snapB; C=$snapC})
Write-Host ("B state={0} C state={1}" -f $snapB.orderState,$snapC.orderState)

# priority C — try orderId string as orderTaskKey
$prioUrl="$($e.baseUrl)/api/order/v1/orderRecordPriorityExec?orderTaskKey=$([uri]::EscapeDataString($snapC.orderId))"
$prio1=Invoke-Api POST $prioUrl $null
$prioAttempts=@([ordered]@{via='orderId-string'; url=$prioUrl; code=$prio1.parsed.code; message=$prio1.parsed.message; body=(Preview $prio1.body)})
Start-Sleep -Seconds 1
$afterPrio1=[ordered]@{A=(Get-Snap $ordA.uid); B=(Get-Snap $ordB.uid); C=(Get-Snap $ordC.uid)}

# if failed, try numeric id and upperId
if(-not (CodeOk $prio1.parsed)){
  $prioUrl2="$($e.baseUrl)/api/order/v1/orderRecordPriorityExec?orderTaskKey=$($snapC.numericId)"
  $prio2=Invoke-Api POST $prioUrl2 $null
  $prioAttempts += [ordered]@{via='numericId'; url=$prioUrl2; code=$prio2.parsed.code; message=$prio2.parsed.message; body=(Preview $prio2.body)}
  Start-Sleep -Seconds 1
  $afterPrio1=[ordered]@{A=(Get-Snap $ordA.uid); B=(Get-Snap $ordB.uid); C=(Get-Snap $ordC.uid)}
}
$lastPrio=$prioAttempts[-1]
$lastOk = ($lastPrio.code -eq '0' -or $lastPrio.code -eq 0)
if(-not $lastOk){
  $prioUrl3="$($e.baseUrl)/api/order/v1/orderRecordPriorityExec?orderTaskKey=$([uri]::EscapeDataString($ordC.uid))"
  $prio3=Invoke-Api POST $prioUrl3 $null
  $prioAttempts += [ordered]@{via='upperId'; url=$prioUrl3; code=$prio3.parsed.code; message=$prio3.parsed.message; body=(Preview $prio3.body)}
  Start-Sleep -Seconds 1
  $afterPrio1=[ordered]@{A=(Get-Snap $ordA.uid); B=(Get-Snap $ordB.uid); C=(Get-Snap $ordC.uid)}
}
Save 'S2-priority-calls.json' ([ordered]@{attempts=$prioAttempts; after=$afterPrio1})
Write-Host ("priority C last via={0} code={1} msg={2} C.state={3}" -f $prioAttempts[-1].via,$prioAttempts[-1].code,$prioAttempts[-1].message,$afterPrio1.C.orderState)

# cancel A to free vehicle, watch B vs C
$cxlA=Cancel-Order $snapA.orderId $snapA.numericId 'R16-S2-cancel-A'
Save 'S2-cancel-A.json' $cxlA
$watch=@()
$deadline=(Get-Date).AddSeconds(120)
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 800
  $wa=[ordered]@{at=(Get-Date -Format 'HH:mm:ss.fff'); A=(Get-Snap $ordA.uid); B=(Get-Snap $ordB.uid); C=(Get-Snap $ordC.uid); veh=(Get-Snap $null)}
  $watch += $wa
  Write-Host ("[{0}] A={1} B={2} C={3} proc={4}" -f $wa.at,$wa.A.orderState,$wa.B.orderState,$wa.C.orderState,$wa.veh.procState)
  if(($wa.B.orderState -in @(3,5) -or $wa.C.orderState -in @(3,5)) -and $watch.Count -ge 5){ 
    # keep a bit more
    if($watch.Count -ge 12){ break }
  }
  if($wa.B.orderState -in @(2,5) -and $wa.C.orderState -in @(2,5) -and $wa.veh.procState -eq 'IDLE'){ break }
}
Save 'S2-watch-after-cancelA.json' $watch

# cleanup remaining
$cleanup=Clear-MyNonFinal 'R16-S2-final-cleanup'
Save 'S2-final-cleanup.json' $cleanup
$idle2=Wait-Idle 180
Save 'S2-final-idle.json' $idle2

# if needed, wait for whichever of B/C is executing to finish or cancel
Save 'E9-final.json' (Get-Snap $null)
Write-Host ("DONE final proc={0} station={1}" -f $idle2.procState,$idle2.station)
$http.Dispose()
