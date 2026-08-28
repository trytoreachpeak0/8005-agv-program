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
Write-Host "labRoot=$labRoot"

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
    missionResultCode=$(if($m0){$m0.resultCode}else{$null})
    missionResultStr=$(if($m0){$m0.resultStr}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    appointVehicleKey=$(if($det){$det.appointVehicleKey}else{$null})
    finalState=$(if($det){$det.finalState}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    upperId=$(if($det){$det.upperId}else{$upperId})
  }
}
function Set-IL([string]$serviceId){
  $body="{`"deviceKeys`":[`"$key`"],`"serviceId`":`"$serviceId`"}"
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/vehicles/updateVehicleIntegrationLevel" $body
  Start-Sleep -Seconds 1
  [pscustomobject]@{req=$body; code=$r.parsed.code; message=$r.parsed.message; body=$r.body; after=(Get-Snap $null)}
}
function New-Move([int]$mapId,[int]$dest,[string]$tag){
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-$tag-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$dest}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  [pscustomobject]@{uid=$uid; request=$json; create=$cr}
}
function Cancel-Order([string]$oid,$nid,[string]$reason){
  $attempts=@()
  if($oid){
    $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
    $attempts += [ordered]@{api='command'; code=$cmd.parsed.code; message=$cmd.parsed.message; body=$cmd.body}
  }
  if($nid){
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" "{`"orderId`":$nid,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $attempts += [ordered]@{api='operate'; code=$op.parsed.code; message=$op.parsed.message; body=$op.body}
  }
  return $attempts
}
function Wait-Idle([int]$sec=120){
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

# plan
@'
# Round 13（2026-07-20）
1. disable 后建单是否被拒
3. 失败路径：跨图不可达目的站建单/执行
4. 执行中 disable 的订单与车态
不做充电/停靠
'@ | Set-Content -Encoding UTF8 (Join-Path $roundDir 'round-plan.md')

"=== E0 BASELINE ==="
$base=Get-Snap $null
Save 'E0-baseline.json' $base
"BASE enable=$($base.enable) integ=$($base.integrationLevel) proc=$($base.procState) st=$($base.station)"
if($base.procState -ne 'IDLE' -or $base.processingOrder){ throw 'not idle' }
Ensure-Online | Out-Null

$cur=[int]$base.station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$other = if($cur -eq 2){1}else{2}

# ========== S1 disable then create ==========
"=== S1 disable then create ==="
$dis1=Set-IL 'disable'
Save 'S1-disable.json' $dis1
"DISABLED enable=$($dis1.after.enable) integ=$($dis1.after.integrationLevel)"
if($dis1.after.integrationLevel -ne 'OFF_LINE'){ throw 'disable did not take effect' }

$o1=New-Move 29 $other 'R13-S1-offcreate'
Save 'S1-create-while-offline.json' ([ordered]@{
  uid=$o1.uid; req=$o1.request; http=$o1.create.status
  code=$o1.create.parsed.code; message=$o1.create.parsed.message
  msgDetail=$o1.create.parsed.msgDetail; result=$o1.create.parsed.result; body=$o1.create.body
})
"S1 CREATE code=$($o1.create.parsed.code) msg=$($o1.create.parsed.message) orderId=$($o1.create.parsed.result.orderId)"

# if unexpectedly created, cancel and flag
if((CodeOk $o1.create.parsed) -and $o1.create.parsed.result.orderId){
  "S1 UNEXPECTED order created while OFF_LINE - cancel"
  Cancel-Order $o1.create.parsed.result.orderId $o1.create.parsed.result.id 'riot-lab-R13-S1-cleanup' | Out-Null
  Start-Sleep -Seconds 2
  Save 'S1-unexpected-created-final.json' (Get-Snap $o1.uid)
}

$en1=Ensure-Online
Save 'S1-restore-online.json' $en1
Wait-Idle 60 | Out-Null

# ========== S3 failure: unreachable cross-map ==========
"=== S3 unreachable create (map26 while on map29) ==="
# confirm route cost
$rc=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" "{`"mapId`":26,`"stationId`":1,`"deviceKeys`":[`"$key`"]}"
Save 'S3-route-cost-map26.json' ([ordered]@{code=$rc.parsed.code; message=$rc.parsed.message; result=$rc.parsed.result})
"ROUTE26 costs=$($rc.parsed.result.deviceCostsList[0].costs) msg=$($rc.parsed.result.deviceCostsList[0].message)"

$o3=New-Move 26 1 'R13-S3-unreachable'
Save 'S3-create-unreachable.json' ([ordered]@{
  uid=$o3.uid; req=$o3.request; code=$o3.create.parsed.code; message=$o3.create.parsed.message
  msgDetail=$o3.create.parsed.msgDetail; result=$o3.create.parsed.result; body=$o3.create.body
})
"S3 CREATE code=$($o3.create.parsed.code) msg=$($o3.create.parsed.message) orderId=$($o3.create.parsed.result.orderId) state=$($o3.create.parsed.result.orderState)"

$s3samples=@()
if((CodeOk $o3.create.parsed) -and $o3.create.parsed.result.orderId){
  $uid3=$o3.uid; $oid3=$o3.create.parsed.result.orderId; $nid3=$o3.create.parsed.result.id
  $deadline=(Get-Date).AddSeconds(90)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 1000
    $s=Get-Snap $uid3
    $s3samples += $s
    "S3POLL order=$($s.orderState) proc=$($s.procState) move=$($s.movementState) ms=$($s.missionState) rc=$($s.missionResultCode) rs=$($s.missionResultStr)"
    if($s.orderState -in @(2,4,5,6)){ break }
  }
  Save 'S3-unreachable-samples.json' ([ordered]@{samples=$s3samples; final=$s3samples[-1]})
  $last3=$s3samples[-1]
  if($last3.orderState -notin @(2,4,5,6)){
    Cancel-Order $oid3 $nid3 'riot-lab-R13-S3-cleanup' | Out-Null
    Save 'S3-cleanup-after.json' (Get-Snap $uid3)
  }
} else {
  Save 'S3-rejected-at-create.json' ([ordered]@{note='create failed - failure at create gate'})
}
Ensure-Online | Out-Null
Wait-Idle 90 | Out-Null

# ========== S4 disable while executing ==========
"=== S4 disable while EXECUTING ==="
$cur=[int](Get-Snap $null).station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$other = if($cur -eq 2){1}else{2}
$o4=New-Move 29 $other 'R13-S4-dis-exec'
Save 'S4-create.json' ([ordered]@{uid=$o4.uid; code=$o4.create.parsed.code; result=$o4.create.parsed.result; req=$o4.request})
if(-not (CodeOk $o4.create.parsed)){ throw "S4 create failed: $($o4.create.body)" }
$uid4=$o4.uid; $oid4=$o4.create.parsed.result.orderId; $nid4=$o4.create.parsed.result.id
$exec4=Wait-Executing $uid4 90
Save 'S4-before-disable.json' $exec4
"BEFORE disable order=$($exec4.orderState) proc=$($exec4.procState) move=$($exec4.movementState)"
if($exec4.orderState -ne 3){
  "did not reach EXECUTING (state=$($exec4.orderState)) - still attempt disable for evidence"
}

$dis4=Set-IL 'disable'
Save 'S4-disable-call.json' $dis4
"DISABLE-during code=$($dis4.code) after enable=$($dis4.after.enable) integ=$($dis4.after.integrationLevel) proc=$($dis4.after.procState)"

$s4samples=@()
for($i=0;$i -lt 20;$i++){
  Start-Sleep -Milliseconds 900
  $s=Get-Snap $uid4
  $s4samples += $s
  "S4#$i order=$($s.orderState) proc=$($s.procState) move=$($s.movementState) enable=$($s.enable) integ=$($s.integrationLevel) ms=$($s.missionState) rc=$($s.missionResultCode)"
  if($s.orderState -in @(2,4,5,6) -and $s.procState -eq 'IDLE' -and -not $s.processingOrder){ break }
}
Save 'S4-after-disable-samples.json' ([ordered]@{samples=$s4samples; final=$s4samples[-1]})

# cleanup order if still active, then enable
$last4=$s4samples[-1]
if($last4.orderState -notin @(2,4,5,6)){
  Cancel-Order $oid4 $nid4 'riot-lab-R13-S4-cleanup' | Out-Null
  Start-Sleep -Seconds 2
}
$en4=Ensure-Online
Save 'S4-restore-online.json' $en4
$idle4=Wait-Idle 120
Save 'S4-post-idle.json' $idle4

# recovery success control
"=== ER recovery move ==="
$cur=[int]$idle4.station
if($cur -ne 1 -and $cur -ne 2){ $cur=1 }
$other = if($cur -eq 2){1}else{2}
$oR=New-Move 29 $other 'R13-ER-recovery'
Save 'ER-create.json' ([ordered]@{uid=$oR.uid; code=$oR.create.parsed.code; result=$oR.create.parsed.result})
$uidR=$oR.uid
$erSamples=@()
$deadline=(Get-Date).AddMinutes(3)
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 1000
  $s=Get-Snap $uidR
  $erSamples += $s
  "ER order=$($s.orderState) proc=$($s.procState) st=$($s.station)"
  if($s.orderState -in @(2,4,5,6) -and $s.procState -eq 'IDLE'){ break }
}
Save 'ER-samples.json' ([ordered]@{samples=$erSamples; final=$erSamples[-1]})

$final=Wait-Idle 60
Save 'E0-final.json' $final
"FINAL enable=$($final.enable) integ=$($final.integrationLevel) proc=$($final.procState) st=$($final.station)"
$c.Dispose()
"ALL_DONE"
