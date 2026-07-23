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
$mapId = 30
Write-Host "Round18 map30 closed-loop SUCCESS"

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
function Wait-Idle([int]$sec=120){
  $deadline=(Get-Date).AddSeconds($sec)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $s=Get-Snap $null
    if($s.procState -eq 'IDLE' -and -not $s.processingOrder -and $s.movementState -eq 'MT_FINISHED'){ return $s }
  }
  return (Get-Snap $null)
}

@'
# Round 18（2026-07-20）
补测 Q-028：改用 map30（api测试2）完整跑单到 SUCCESS。
Round16/17 在 map28 可派可跑但未到站；本轮换图短距闭环。
'@ | Set-Content -Encoding UTF8 (Join-Path $roundDir 'round-plan.md')

"=== E0 ==="
$base=Get-Snap $null
Save 'E0-baseline.json' $base
# resolve mapId from live mapName (avoid script-file encoding issues with Chinese literals)
$maps=Invoke-Api GET "$($e.baseUrl)/api/imap/v1/mapInfo/all" $null
$resolvedMapId=$null; $resolvedMapName=$null
if($maps.parsed.result){
  foreach($m in $maps.parsed.result){
    if($m.name -eq $base.mapName){ $resolvedMapId=$m.id; $resolvedMapName=$m.name; break }
  }
}
Save 'E0-map-resolve.json' ([ordered]@{vehicleMapName=$base.mapName; resolvedMapId=$resolvedMapId; resolvedMapName=$resolvedMapName; expectMapId=$mapId})
if($resolvedMapId -ne $mapId){ throw "not on map30: mapName=$($base.mapName) resolvedMapId=$resolvedMapId" }
if($base.enable -ne $true -or $base.integrationLevel -ne 'ON_LINE'){ throw 'not online' }
if($base.procState -ne 'IDLE' -or $base.processingOrder){
  $pre=Clear-MyNonFinal 'R18-E0-preclear'
  Save 'E0-preclear.json' $pre
  $base=Wait-Idle 120
  Save 'E0-after-preclear.json' $base
}
Write-Host ("base st={0} proc={1} move={2} map={3}" -f $base.station,$base.procState,$base.movementState,$base.mapName)

# choose cheapest positive reachable dest among 1..7
$cands=@(1,2,3,4,5,6,7)
$costRows=@()
foreach($sid in $cands){
  $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
  $c0=$null; $msg=$null
  if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
  $costRows += [ordered]@{stationId=$sid; costs=$c0; message=$msg}
  Write-Host ("cost st={0} -> {1} ({2})" -f $sid,$c0,$msg)
}
Save 'E0-cost-candidates.json' $costRows

$reachable = @($costRows | Where-Object { $_.costs -ne $null -and $_.costs -ge 0 -and $_.message -eq 'ok' } | Sort-Object costs)
if($reachable.Count -eq 0){ throw 'no reachable destination on map30' }

# prefer short positive cost; if currently on a station, skip same station (cost 0)
$chosen=$null; $chosenCost=$null
foreach($row in $reachable){
  if($base.station -and $row.stationId -eq $base.station -and $row.costs -eq 0){ continue }
  if($row.costs -eq 0 -and $base.station -eq $row.stationId){ continue }
  $chosen=$row.stationId; $chosenCost=$row.costs; break
}
if($null -eq $chosen){
  # fallback: any reachable different from current
  foreach($row in $reachable){
    if($base.station -and $row.stationId -eq $base.station){ continue }
    $chosen=$row.stationId; $chosenCost=$row.costs; break
  }
}
if($null -eq $chosen){ throw 'no suitable destination (all same station?)' }
Write-Host ("chosen dest={0} cost={1}" -f $chosen,$chosenCost)

"=== S1 create and watch to SUCCESS ==="
$ts=Get-Date -Format 'yyyyMMdd-HHmmss'
$uid="riot-behavior-lab-R18-m30-$ts"
$json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$chosen}]}"
$cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
Save 'S1-create.json' ([ordered]@{uid=$uid; dest=$chosen; cost=$chosenCost; req=$json; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body})
if(-not (CodeOk $cr.parsed)){ throw "create failed: $($cr.body)" }

$samples=@()
$deadline=(Get-Date).AddSeconds(300)
$prevRemain=$null
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 800
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
  $cxl=Cancel-Order $final.orderId $final.numericId 'R18-timeout-cancel'
  Save 'S1-timeout-cancel.json' $cxl
  Write-Host ("timeout cancel done")
}

# optional redispatch if SUCCESS
if($final.orderState -eq 5){
  $idle=Wait-Idle 90
  Save 'S1-post-success-idle.json' $idle
  $dest2=$null; $cost2=$null
  foreach($sid in @(1,2,3,4,5,6,7)){
    if($sid -eq $chosen){ continue }
    if($idle.station -and $sid -eq $idle.station){ continue }
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$r.parsed.result.deviceCostsList[0].costs
    $msg=$r.parsed.result.deviceCostsList[0].message
    if($c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){
      if($null -eq $dest2 -or $c0 -lt $cost2){ $dest2=$sid; $cost2=$c0 }
    }
  }
  if($dest2){
    $ts2=Get-Date -Format 'yyyyMMdd-HHmmss'
    $uid2="riot-behavior-lab-R18-redispatch-$ts2"
    $json2="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid2`",`"upperId`":`"$uid2`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$dest2}]}"
    $cr2=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json2
    Save 'S2-redispatch-create.json' ([ordered]@{uid=$uid2; dest=$dest2; cost=$cost2; code=$cr2.parsed.code; body=$cr2.body})
    $samples2=@()
    $deadline=(Get-Date).AddSeconds(300)
    while((Get-Date) -lt $deadline){
      Start-Sleep -Milliseconds 800
      $s=Get-Snap $uid2
      $samples2 += $s
      Write-Host ("[R] order={0} proc={1} st={2} remain={3}" -f $s.orderState,$s.procState,$s.station,$s.remainCost)
      if($s.orderState -in @(2,4,5,6)){ break }
    }
    Save 'S2-redispatch-samples.json' $samples2
    $f2=Get-Snap $uid2
    Save 'S2-redispatch-final.json' $f2
    if($f2.orderState -in @(1,3,7,9)){
      $cxl2=Cancel-Order $f2.orderId $f2.numericId 'R18-S2-cleanup'
      Save 'S2-cleanup.json' $cxl2
    }
  }
}

Save 'E9-final.json' (Get-Snap $null)
$http.Dispose()
Write-Host DONE
