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
Write-Host "Round17 map28 closed-loop SUCCESS"

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
  $remain=$null; $remainCode=$null
  if($det -and $det.orderId){
    $rem=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/curRemainCost/$($det.orderId)" $null
    $remain=$rem.parsed.result; $remainCode=$rem.parsed.code
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
    missionResultCode=$(if($m0){$m0.resultCode}else{$null})
    progress=$(if($det){$det.progress}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    executeVehicleKey=$(if($det){$det.executeVehicleKey}else{$null})
    finalState=$(if($det){$det.finalState}else{$null})
    remainCost=$remain; remainCode=$remainCode
    upperId=$(if($det){$det.upperId}else{$upperId})
  }
}

@'
# Round 17（2026-07-20）
补测 Q-028：map28（新基测试2opt）完整跑单到 SUCCESS。
目的站优先选代价较短且可达的站（预检 getRouteCostsBy）。
'@ | Set-Content -Encoding UTF8 (Join-Path $roundDir 'round-plan.md')

"=== E0 ==="
$base=Get-Snap $null
Save 'E0-baseline.json' $base
if($base.mapName -notmatch '2opt'){ throw "not on map28: $($base.mapName)" }
if($base.enable -ne $true -or $base.integrationLevel -ne 'ON_LINE'){ throw 'not online' }
Write-Host ("base st={0} proc={1} move={2}" -f $base.station,$base.procState,$base.movementState)

# choose destination: prefer station 1 if cost>0 and ok; else 33/31
$cands=@(1,33,31,29,8)
$chosen=$null; $chosenCost=$null
$costRows=@()
foreach($sid in $cands){
  $json=(@{mapId=28; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
  $c0=$null; $msg=$null
  if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
  $costRows += [ordered]@{stationId=$sid; costs=$c0; message=$msg}
  if($null -eq $chosen -and $c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){ $chosen=$sid; $chosenCost=$c0 }
}
Save 'E0-cost-candidates.json' $costRows
if($null -eq $chosen){ throw 'no reachable positive-cost destination' }
Write-Host ("chosen dest={0} cost={1}" -f $chosen,$chosenCost)

"=== S1 create and watch to SUCCESS ==="
$ts=Get-Date -Format 'yyyyMMdd-HHmmss'
$uid="riot-behavior-lab-R17-success-$ts"
$json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":28,`"destination`":$chosen}]}"
$cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
Save 'S1-create.json' ([ordered]@{uid=$uid; dest=$chosen; req=$json; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body})
if(-not (CodeOk $cr.parsed)){ throw "create failed: $($cr.body)" }

$samples=@()
$deadline=(Get-Date).AddSeconds(600)
$prevRemain=$null
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 1000
  $s=Get-Snap $uid
  $samples += $s
  $flag=''
  if($s.remainCost -ne $prevRemain){ $flag=' *remain*'; $prevRemain=$s.remainCost }
  Write-Host ("[{0}] order={1} mission={2} proc={3} move={4} st={5} remain={6}{7}" -f $s.at,$s.orderState,$s.missionState,$s.procState,$s.movementState,$s.station,$s.remainCost,$flag)
  if($s.orderState -eq 5){ break }
  if($s.orderState -in @(2,4,6)){ break }
}
Save 'S1-dense-samples.json' $samples
$final=Get-Snap $uid
Save 'S1-final-order.json' $final
$veh=Get-Snap $null
Save 'S1-final-vehicle.json' $veh
Write-Host ("FINAL orderState={0} station={1} proc={2} finalState={3}" -f $final.orderState,$veh.station,$veh.procState,$final.finalState)

if($final.orderState -in @(1,3,7,9)){
  $cxl=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$($final.orderId)" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"R17-timeout-cancel`"}"
  Save 'S1-timeout-cancel.json' ([ordered]@{code=$cxl.parsed.code; message=$cxl.parsed.message; body=$cxl.body})
  Write-Host ("timeout cancel code={0}" -f $cxl.parsed.code)
}

# if SUCCESS, optional re-dispatch check to nearest cheap station
if($final.orderState -eq 5){
  $deadline=(Get-Date).AddSeconds(60)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $veh=Get-Snap $null
    if($veh.procState -eq 'IDLE' -and -not $veh.processingOrder){ break }
  }
  Save 'S1-post-success-idle.json' $veh
  # second short order: prefer station 30 if cost ok else 33
  $dest2=$null
  foreach($sid in @(30,33,31,28,1)){
    if($sid -eq $chosen){ continue }
    $json=(@{mapId=28; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$r.parsed.result.deviceCostsList[0].costs
    $msg=$r.parsed.result.deviceCostsList[0].message
    if($c0 -ne $null -and $c0 -ge 0 -and $msg -eq 'ok' -and $c0 -lt 12000){ $dest2=$sid; break }
  }
  if($dest2){
    $ts2=Get-Date -Format 'yyyyMMdd-HHmmss'
    $uid2="riot-behavior-lab-R17-redispatch-$ts2"
    $json2="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid2`",`"upperId`":`"$uid2`",`"mission`":[{`"type`":`"move`",`"mapId`":28,`"destination`":$dest2}]}"
    $cr2=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json2
    Save 'S2-redispatch-create.json' ([ordered]@{uid=$uid2; dest=$dest2; code=$cr2.parsed.code; body=$cr2.body})
    $samples2=@()
    $deadline=(Get-Date).AddSeconds(420)
    while((Get-Date) -lt $deadline){
      Start-Sleep -Milliseconds 1000
      $s=Get-Snap $uid2
      $samples2 += $s
      Write-Host ("[R] order={0} proc={1} st={2} remain={3}" -f $s.orderState,$s.procState,$s.station,$s.remainCost)
      if($s.orderState -in @(2,4,5,6)){ break }
    }
    Save 'S2-redispatch-samples.json' $samples2
    $f2=Get-Snap $uid2
    Save 'S2-redispatch-final.json' $f2
    if($f2.orderState -in @(1,3,7,9)){
      $cxl2=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$($f2.orderId)" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"R17-S2-cleanup`"}"
      Save 'S2-cleanup.json' ([ordered]@{code=$cxl2.parsed.code})
    }
  }
}

Save 'E9-final.json' (Get-Snap $null)
$http.Dispose()
Write-Host DONE
