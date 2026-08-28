$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$c = [System.Net.Http.HttpClient]::new()
$key = $e.testVehicleKey
$mapId = 29
Write-Host "labRoot=$labRoot key=$key"

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
  $m0=$null
  if($det -and $det.missions -and $det.missions.Count -gt 0){ $m0=$det.missions[0] }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$v.currentStation; noStation=$v.noStation
    procState=$vti.procState; processingOrder=$vti.processingOrder
    movementState=[string]$v.movementState
    enable=$vti.enable; integrationLevel=[string]$vti.integrationLevel
    orderState=$(if($det){$det.orderState}else{$null})
    missionState=$(if($m0){$m0.missionState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    appointVehicleKey=$(if($det){$det.appointVehicleKey}else{$null})
    finalState=$(if($det){$det.finalState}else{$null})
    upperId=$(if($det){$det.upperId}else{$upperId})
  }
}
function Set-IL([string]$serviceId){
  $body="{`"deviceKeys`":[`"$key`"],`"serviceId`":`"$serviceId`"}"
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/vehicles/updateVehicleIntegrationLevel" $body
  Start-Sleep -Seconds 1
  [pscustomobject]@{req=$body; code=$r.parsed.code; message=$r.parsed.message; body=$r.body; after=(Get-Snap $null)}
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
    $attempts += [ordered]@{api='command'; orderId=$oid; code=$cmd.parsed.code; message=$cmd.parsed.message; body=$cmd.body}
    $cmdOk=CodeOk $cmd.parsed
  }
  if($nid -and -not $cmdOk){
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" "{`"orderId`":$nid,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $attempts += [ordered]@{api='operate'; numericId=$nid; code=$op.parsed.code; message=$op.parsed.message; body=$op.body}
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
function Wait-Executing([string]$uid,[int]$sec=90){
  $deadline=(Get-Date).AddSeconds($sec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-Snap $uid
    if($s.orderState -eq 3){ return $s }
    if($s.orderState -in @(2,4,5,6)){ return $s }
  }
  return (Get-Snap $uid)
}
function Ensure-Online(){
  $s=Get-Snap $null
  if($s.enable -eq $true -and $s.integrationLevel -eq 'ON_LINE'){ return $s }
  $en=Set-IL 'enable'
  Save 'RECOVER-enable.json' $en
  $s2=Get-Snap $null
  if($s2.enable -ne $true -or $s2.integrationLevel -ne 'ON_LINE'){ throw 'cannot restore ON_LINE' }
  return $s2
}
function Summarize-Records($parsed){
  $page=$parsed.result
  $records=@()
  if($page -and $page.records){
    foreach($r in $page.records){
      $records += [ordered]@{
        id=$r.id; orderId=$r.orderId; upperId=$r.upperId; orderName=$r.orderName
        orderState=$r.orderState; finalState=$r.finalState
        appointVehicleKey=$r.appointVehicleKey; executeVehicleKey=$r.executeVehicleKey
        executeVehicleName=$r.executeVehicleName
        createTime=$r.createTime; endStationNo=$r.endStationNo
      }
    }
  }
  [ordered]@{
    code=$parsed.code; message=$parsed.message
    total=$(if($page){$page.total}else{$null})
    current=$(if($page){$page.current}else{$null})
    size=$(if($page){$page.size}else{$null})
    count=$records.Count
    records=$records
  }
}
function Query-OrderRecord([hashtable]$qs){
  $parts=@("pageNum=1","pageSize=50")
  foreach($k in $qs.Keys){
    $v=$qs[$k]
    if($null -eq $v){ continue }
    if($v -is [System.Array]){
      foreach($item in $v){ $parts += ("{0}={1}" -f $k,[uri]::EscapeDataString([string]$item)) }
    } else {
      $parts += ("{0}={1}" -f $k,[uri]::EscapeDataString([string]$v))
    }
  }
  $url="$($e.baseUrl)/api/order/v1/orderRecord?" + ($parts -join '&')
  $r=Invoke-Api GET $url $null
  [pscustomobject]@{url=$url; status=$r.status; summary=(Summarize-Records $r.parsed); rawPreview=$r.body.Substring(0,[Math]::Min(2500,$r.body.Length))}
}
function Client-Filter($summary){
  $hit=@()
  foreach($r in $summary.records){
    if($r.appointVehicleKey -eq $key -or $r.executeVehicleKey -eq $key){ $hit += $r }
  }
  return $hit
}

# ---------- E0 ----------
"=== E0 BASELINE ==="
$online=Ensure-Online
Save 'E0-online.json' $online
$base=Get-Snap $null
Save 'E0-baseline.json' $base
$e0list=Query-OrderRecord @{ executeVehicleKey=$key; filterByState=@('1','3','7','9') }
Save 'E0-list-nonfinal-by-execute.json' $e0list
Write-Host ("baseline proc={0} nonfinal-by-execute total={1}" -f $base.procState,$e0list.summary.total)

# cancel any leftover non-final for this vehicle first
$leftovers=@()
foreach($r in $e0list.summary.records){
  if($r.orderState -in @(1,3,7,9)){
    $leftovers += [ordered]@{ before=$r; cancel=(Cancel-Order $r.orderId $r.id 'R14-E0-cleanup') }
  }
}
if($leftovers.Count -gt 0){
  Save 'E0-cleanup.json' $leftovers
  $idle0=Wait-Idle 120
  Save 'E0-after-cleanup-idle.json' $idle0
}

# ---------- S1 probe filters ----------
"=== S1 FILTER PROBES ==="
$probes=@()
$probes += [ordered]@{name='by-execute'; q=(Query-OrderRecord @{ executeVehicleKey=$key; pageSize=20 })}
$probes += [ordered]@{name='by-execute+states-137'; q=(Query-OrderRecord @{ executeVehicleKey=$key; filterByState=@('1','3','7') })}
$probes += [ordered]@{name='by-appoint-undoc'; q=(Query-OrderRecord @{ appointVehicleKey=$key; filterByState=@('1','3','7') })}
$probes += [ordered]@{name='by-state1-global'; q=(Query-OrderRecord @{ filterByState=@('1'); pageSize=50 })}
$probes += [ordered]@{name='by-executeName'; q=(Query-OrderRecord @{ executeVehicleName=$e.testVehicleName; filterByState=@('1','3','7') })}
Save 'S1-filter-probes.json' $probes
foreach($p in $probes){
  Write-Host ("S1 {0}: code={1} total={2}" -f $p.name,$p.q.summary.code,$p.q.summary.total)
}

# ---------- S2 manufacture backlog ----------
"=== S2 BACKLOG ==="
# pick destinations based on current station
$cur=$base.station
if($null -eq $cur -or $cur -eq 0){ $destA=2; $destB=1; $destC=2 } elseif($cur -eq 1){ $destA=2; $destB=1; $destC=2 } else { $destA=1; $destB=2; $destC=1 }

$ordA=New-Move $destA 'R14-A-exec'
Save 'S2-A-create.json' $ordA
if(-not (CodeOk $ordA.create.parsed)){ throw "A create failed: $($ordA.create.body)" }
$snapA=Wait-Executing $ordA.uid 90
Save 'S2-A-executing.json' $snapA
Write-Host ("A state={0} oid={1}" -f $snapA.orderState,$snapA.orderId)

$ordB=New-Move $destB 'R14-B-queue'
Save 'S2-B-create.json' $ordB
Start-Sleep -Milliseconds 500
$ordC=New-Move $destC 'R14-C-queue'
Save 'S2-C-create.json' $ordC
Start-Sleep -Seconds 2
$snapB=Get-Snap $ordB.uid
$snapC=Get-Snap $ordC.uid
Save 'S2-BC-snaps.json' ([ordered]@{B=$snapB;C=$snapC;A=(Get-Snap $ordA.uid)})
Write-Host ("B state={0} C state={1}" -f $snapB.orderState,$snapC.orderState)

$listExec=Query-OrderRecord @{ executeVehicleKey=$key; filterByState=@('1','3','7','9') }
$listAppoint=Query-OrderRecord @{ appointVehicleKey=$key; filterByState=@('1','3','7','9') }
$listState1=Query-OrderRecord @{ filterByState=@('1'); pageSize=100 }
$clientHits=Client-Filter $listState1.summary
Save 'S2-lists-while-backlog.json' ([ordered]@{
  byExecute=$listExec
  byAppointUndoc=$listAppoint
  byState1Global=$listState1
  clientFilterAppointOrExecute=$clientHits
  expectedUids=@($ordA.uid,$ordB.uid,$ordC.uid)
})
Write-Host ("list byExecute total={0} byAppoint total={1} state1-global total={2} clientHits={3}" -f `
  $listExec.summary.total,$listAppoint.summary.total,$listState1.summary.total,$clientHits.Count)

# optional HELD on executing A (to test hung/paused cancel path) — only if still EXECUTING
$held=$null
$aNow=Get-Snap $ordA.uid
if($aNow.orderState -eq 3){
  $heldCmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$($aNow.orderId)" "{`"commandType`":`"CMD_ORDER_HELD`",`"disableVehicle`":false,`"reason`":`"R14-held`"}"
  Start-Sleep -Seconds 1
  $held=[ordered]@{code=$heldCmd.parsed.code; message=$heldCmd.parsed.message; body=$heldCmd.body; after=(Get-Snap $ordA.uid)}
  Save 'S2-A-held.json' $held
  Write-Host ("HELD code={0} A.state={1}" -f $held.code,$held.after.orderState)
}

$listAfterHeld=Query-OrderRecord @{ executeVehicleKey=$key; filterByState=@('1','3','7','9') }
Save 'S2-list-after-held.json' $listAfterHeld

# ---------- S3 clear QUEUEING/HELD and verify new order ----------
"=== S3 CLEAR + NEW ==="
$toCancel=@()
# refresh details for A/B/C
foreach($uid in @($ordA.uid,$ordB.uid,$ordC.uid)){
  $s=Get-Snap $uid
  if($s.orderState -in @(1,7,9)){ $toCancel += $s }
  elseif($s.orderState -eq 3 -and $held -and (CodeOk ([pscustomobject]@{code=$held.code}))){
    # if A was held successfully, cancel it too for clear path; if still EXECUTING keep for now
  }
}
# also from list
foreach($r in $listAfterHeld.summary.records){
  if($r.orderState -in @(1,7,9)){
    if(-not ($toCancel | Where-Object { $_.orderId -eq $r.orderId })){
      $toCancel += [ordered]@{orderId=$r.orderId; numericId=$r.id; orderState=$r.orderState; upperId=$r.upperId}
    }
  }
}
# Always cancel QUEUEING B/C; cancel HELD A if held; if A still EXECUTING, cancel A too so queue clears for new order demo
$cancelResults=@()
foreach($uid in @($ordB.uid,$ordC.uid,$ordA.uid)){
  $s=Get-Snap $uid
  if($s.orderState -in @(1,3,7,9)){
    $cr=Cancel-Order $s.orderId $s.numericId 'R14-S3-clear'
    $cancelResults += [ordered]@{uid=$uid; beforeState=$s.orderState; orderId=$s.orderId; cancel=$cr; after=(Get-Snap $uid)}
  }
}
Save 'S3-cancel-backlog.json' $cancelResults
$idle1=Wait-Idle 180
Save 'S3-after-clear-idle.json' $idle1
$listCleared=Query-OrderRecord @{ executeVehicleKey=$key; filterByState=@('1','3','7','9') }
Save 'S3-list-after-clear.json' $listCleared
Write-Host ("after clear idle={0} nonfinal={1}" -f $idle1.procState,$listCleared.summary.total)

# new order should execute
$destNew = if($idle1.station -eq 1){2} elseif($idle1.station -eq 2){1} else {2}
$ordN=New-Move $destNew 'R14-N-after-clear'
Save 'S3-N-create.json' $ordN
$snapN=Wait-Executing $ordN.uid 90
Save 'S3-N-executing.json' $snapN
Write-Host ("N state={0}" -f $snapN.orderState)
# let it finish or cancel after brief observation
Start-Sleep -Seconds 3
$cancelN=Cancel-Order $snapN.orderId $snapN.numericId 'R14-S3-N-cleanup'
Save 'S3-N-cleanup.json' ([ordered]@{before=$snapN; cancel=$cancelN; after=(Get-Snap $ordN.uid)})
$idle2=Wait-Idle 120
Save 'S3-final-idle.json' $idle2

# ---------- S4 final list ----------
"=== S4 FINAL ==="
$finalList=Query-OrderRecord @{ executeVehicleKey=$key; filterByState=@('1','3','7','9') }
Save 'S4-final-nonfinal-list.json' $finalList
$finalSnap=Get-Snap $null
Save 'S4-final-snap.json' $finalSnap
Write-Host ("DONE final proc={0} nonfinal={1}" -f $finalSnap.procState,$finalList.summary.total)
$c.Dispose()
