$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$http = [System.Net.Http.HttpClient]::new()
$http.Timeout = [TimeSpan]::FromSeconds(15)
$key = $e.testVehicleKey
$phase = if($args.Count -ge 1){ $args[0] } else { 'watch-offline' }
Write-Host "Round20 device-offline phase=$phase key=$key"

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

function Get-OfflineSnap {
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $st=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/status/$key" $null
  $v=$null; $vti=$null
  if($gi.parsed){ $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo }
  $statusType=$null; $statusTs=$null
  if($st.parsed -and $st.parsed.result){
    $statusType=$st.parsed.result.type
    $statusTs=$st.parsed.result.timestamp
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    statusOk=$st.ok; statusHttp=$st.status; statusCode=$(if($st.parsed){$st.parsed.code}else{$null})
    statusType=$statusType; statusTs=$statusTs; statusError=$st.error
    vehicleOk=$gi.ok; vehicleHttp=$gi.status; vehicleError=$gi.error
    station=$(if($v){$v.currentStation}else{$null})
    noStation=$(if($v){$v.noStation}else{$null})
    mapName=$(if($v -and $v.previousState){$v.previousState.mapName}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    processingOrder=$(if($vti){$vti.processingOrder}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    integrationLevel=$(if($vti){[string]$vti.integrationLevel}else{$null})
    movementState=$(if($v){[string]$v.movementState}else{$null})
    emergencyState=$(if($v){$v.emergencyState}else{$null})
    controlState=$(if($v){$v.controlState}else{$null})
    hardwareState=$(if($v){$v.hardwareState}else{$null})
  }
}

function Is-DeviceOffline($s){
  if(-not $s){ return $false }
  if($s.statusType -and $s.statusType -ne 'online'){ return $true }
  if(-not $s.statusOk){ return $true }
  return $false
}

function Cancel-Order([string]$oid,$nid,[string]$reason){
  $attempts=@()
  if($oid){
    $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}"
    $attempts += [ordered]@{api='command'; orderId=$oid; code=$cmd.parsed.code; message=$cmd.parsed.message}
  }
  if($nid){
    $op=Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" "{`"orderId`":$nid,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason-op`"}}"
    $attempts += [ordered]@{api='operate'; numericId=$nid; code=$op.parsed.code; message=$op.parsed.message}
  }
  return $attempts
}

if($phase -eq 'baseline'){
  $s=Get-OfflineSnap
  Save 'E0-baseline.json' $s
  Write-Host ("BASE status={0} enable={1} il={2} proc={3} st={4} emerg={5}" -f $s.statusType,$s.enable,$s.integrationLevel,$s.procState,$s.station,$s.emergencyState)
  if($s.statusType -ne 'online'){ Write-Host 'WARN already not online'; $http.Dispose(); exit 2 }
  $http.Dispose(); return
}

if($phase -eq 'watch-offline'){
  "=== S1 watch for device OFFLINE (timeout 300s) ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds(300)
  $hit=$false
  while((Get-Date) -lt $deadline){
    $s=Get-OfflineSnap
    $samples += $s
    Write-Host ("[{0}] status={1} enable={2} il={3} proc={4} move={5} emerg={6}" -f $s.at,$s.statusType,$s.enable,$s.integrationLevel,$s.procState,$s.movementState,$s.emergencyState)
    if(Is-DeviceOffline $s){ $hit=$true; break }
    Start-Sleep -Milliseconds 900
  }
  Save 'S1-watch-offline-samples.json' $samples
  Save 'S1-offline-hit.json' ([ordered]@{hit=$hit; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_OFFLINE_WITHIN_TIMEOUT'; $http.Dispose(); exit 2 }
  Write-Host 'DEVICE_OFFLINE_DETECTED'
  $http.Dispose(); return
}

if($phase -eq 'probe-while-offline'){
  "=== S2 probe create while device offline ==="
  $before=Get-OfflineSnap
  Save 'S2-before-create.json' $before
  if(-not (Is-DeviceOffline $before)){ Write-Host 'WARN device appears online; still probing' }

  $mapId=30
  $dest=1
  if($before.station -and $before.station -ne 0){
    foreach($sid in @(1,2,3,4,5,6,7)){ if($sid -ne $before.station){ $dest=$sid; break } }
  }
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R20-offline-create-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$dest}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  Save 'S2-create-while-offline.json' ([ordered]@{uid=$uid; dest=$dest; req=$json; ok=$cr.ok; status=$cr.status; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body; error=$cr.error})
  Write-Host ("create code={0} msg={1}" -f $cr.parsed.code,$cr.parsed.message)

  $samples=@()
  $deadline=(Get-Date).AddSeconds(45)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 900
    $s=Get-OfflineSnap
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null
    $det=$by.parsed.result
    $row=[ordered]@{
      at=$s.at; statusType=$s.statusType; enable=$s.enable; il=$s.integrationLevel; proc=$s.procState
      orderState=$(if($det){$det.orderState}else{$null})
      execute=$(if($det){$det.executeVehicleKey}else{$null})
      orderId=$(if($det){$det.orderId}else{$null})
      numericId=$(if($det){$det.id}else{$null})
    }
    $samples += $row
    Write-Host ("[{0}] status={1} order={2} exec={3} proc={4}" -f $row.at,$row.statusType,$row.orderState,$row.execute,$row.proc)
  }
  Save 'S2-samples.json' $samples
  $last=$samples[-1]
  if($last.orderState -in @(1,3,7,9)){
    $cxl=Cancel-Order $last.orderId $last.numericId 'R20-offline-cleanup'
    Save 'S2-cleanup.json' $cxl
    Write-Host 'cleanup cancel done'
  }
  Save 'S2-after.json' (Get-OfflineSnap)
  $http.Dispose(); return
}

if($phase -eq 'watch-online'){
  "=== S3 watch for device ONLINE (timeout 300s) ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds(300)
  $hit=$false
  while((Get-Date) -lt $deadline){
    $s=Get-OfflineSnap
    $samples += $s
    Write-Host ("[{0}] status={1} enable={2} il={3} proc={4} emerg={5}" -f $s.at,$s.statusType,$s.enable,$s.integrationLevel,$s.procState,$s.emergencyState)
    if($s.statusType -eq 'online' -and $s.statusOk){ $hit=$true; break }
    Start-Sleep -Milliseconds 900
  }
  Save 'S3-watch-online-samples.json' $samples
  Save 'S3-online-hit.json' ([ordered]@{hit=$hit; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_ONLINE_WITHIN_TIMEOUT'; $http.Dispose(); exit 2 }
  Write-Host 'DEVICE_ONLINE_DETECTED'
  $http.Dispose(); return
}

if($phase -eq 'redispatch'){
  "=== S4 short redispatch after online ==="
  $base=Get-OfflineSnap
  Save 'S4-before-create.json' $base
  if($base.statusType -ne 'online'){ throw "not online: $($base.statusType)" }
  if($base.enable -ne $true -or $base.integrationLevel -ne 'ON_LINE'){
    Write-Host ("WARN schedule not ON_LINE enable={0} il={1}" -f $base.enable,$base.integrationLevel)
  }

  $mapId=30
  $chosen=$null; $chosenCost=$null
  foreach($sid in @(1,2,3,4,5,6,7)){
    if($base.station -and $sid -eq $base.station){ continue }
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$null; $msg=$null
    if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
    if($c0 -ne $null -and $c0 -gt 0 -and $msg -eq 'ok'){
      if($null -eq $chosen -or $c0 -lt $chosenCost){ $chosen=$sid; $chosenCost=$c0 }
    }
  }
  if($null -eq $chosen){ throw 'no dest' }
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R20-after-online-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$chosen}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  Save 'S4-create.json' ([ordered]@{uid=$uid; dest=$chosen; cost=$chosenCost; code=$cr.parsed.code; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.body)" }

  $samples=@()
  $deadline=(Get-Date).AddSeconds(180)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null
    $st=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/status/$key" $null
    $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo; $det=$by.parsed.result
    $row=[ordered]@{
      at=(Get-Date -Format 'HH:mm:ss.fff')
      orderState=$det.orderState; proc=$vti.procState; st=$v.currentStation
      statusType=$st.parsed.result.type; enable=$vti.enable; il=[string]$vti.integrationLevel
    }
    $samples += $row
    Write-Host ("[{0}] order={1} proc={2} st={3} status={4}" -f $row.at,$row.orderState,$row.proc,$row.st,$row.statusType)
    if($row.orderState -in @(2,4,5,6)){ break }
  }
  Save 'S4-samples.json' $samples
  $final=$samples[-1]
  if($final.orderState -in @(1,3,7,9)){
    $det=(Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null).parsed.result
    $cxl=Cancel-Order $det.orderId $det.id 'R20-S4-timeout'
    Save 'S4-cleanup.json' $cxl
  }
  Save 'E9-final.json' (Get-OfflineSnap)
  $http.Dispose()
  Write-Host DONE
  return
}

throw "unknown phase: $phase"
