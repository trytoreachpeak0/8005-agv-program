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
$phase = if($args.Count -ge 1){ $args[0] } else { 'baseline' }
$timeoutSec = if($args.Count -ge 2){ [int]$args[1] } else { 180 }
# 本轮测试车绑图为 api测试2 → map30（env.candidateMapId 可能仍是 29）
$mapId = 30
Write-Host "Round23 location phase=$phase key=$key mapId=$mapId"

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
function PropVal($res, $name){
  if(-not $res){ return $null }
  $p = $res.$name
  if($null -eq $p){ return $null }
  if($p -is [psobject] -and ($p.PSObject.Properties.Name -contains 'value')){ return $p.value }
  return $p
}

function Get-LocSnap {
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $st=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/status/$key" $null
  $prop=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/properties/$key" $null
  $v=$null; $vti=$null
  if($gi.parsed){ $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo }
  $res=$prop.parsed.result
  $prev=$null; if($v){ $prev=$v.previousState }
  $pos=$null
  if($prev -and $prev.currentPosition){ $pos=$prev.currentPosition }
  elseif($v -and $v.precisePosition){ $pos=$v.precisePosition }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    apiOk=$gi.ok
    statusType=$(if($st.parsed.result){$st.parsed.result.type}else{$null})
    locationState=$(if($v){[string]$v.locationState}else{$null})
    confidence=$(if($v){$v.confidence}else{$null})
    prop_locationState=(PropVal $res 'locationState')
    station=$(if($v){$v.currentStation}else{$null})
    noStation=$(if($v){$v.noStation}else{$null})
    currentNode=$(if($v){$v.currentNode}else{$null})
    mapName=$(if($prev){$prev.mapName}else{$null})
    prev_locationState=$(if($prev){$prev.locationState}else{$null})
    posX=$(if($pos){$pos.x}else{$null})
    posY=$(if($pos){$pos.y}else{$null})
    posConf=$(if($pos){$pos.confidence}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    integrationLevel=$(if($vti){[string]$vti.integrationLevel}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    movementState=$(if($v){[string]$v.movementState}else{$null})
    mode=$(if($v){[string]$v.mode}else{$null})
    connected=$(if($v){$v.connected}else{$null})
    state=$(if($v){[string]$v.state}else{$null})
  }
}

function Is-Localized($s){
  if(-not $s){ return $false }
  if($s.locationState -eq 'LOCATION_STATE_RUNNING'){ return $true }
  if($s.prop_locationState -eq 3 -or $s.prop_locationState -eq '3'){ return $true }
  return $false
}
function Is-Unlocalized($s){
  if(-not $s){ return $false }
  if(-not $s.apiOk){ return $false }
  if($s.locationState -eq 'LOCATION_STATE_RUNNING'){ return $false }
  if($s.prop_locationState -eq 3 -or $s.prop_locationState -eq '3'){ return $false }
  # treat ERROR / UNKNOWN / other numeric / null-as-changed as unlocalized candidate
  if($s.locationState -and $s.locationState -ne 'LOCATION_STATE_RUNNING'){ return $true }
  if($null -ne $s.prop_locationState -and $s.prop_locationState -ne 3 -and $s.prop_locationState -ne '3'){ return $true }
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
  $s=Get-LocSnap
  Save 'E0-localized-baseline.json' $s
  Write-Host ("BASE loc={0} propLoc={1} conf={2} st={3} map={4} status={5} control={6}" -f $s.locationState,$s.prop_locationState,$s.confidence,$s.station,$s.mapName,$s.statusType,$s.controlState)
  if(-not (Is-Localized $s)){ Write-Host 'WARN not LOCATION_STATE_RUNNING'; $http.Dispose(); exit 2 }
  $http.Dispose(); return
}

if($phase -eq 'watch-unlocalized'){
  "=== S1 watch UNLOCALIZED (timeout ${timeoutSec}s) ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  $hit=$false
  while((Get-Date) -lt $deadline){
    $s=Get-LocSnap
    $samples += $s
    Write-Host ("[{0}] loc={1} prop={2} conf={3} st={4} map={5} control={6}" -f $s.at,$s.locationState,$s.prop_locationState,$s.confidence,$s.station,$s.mapName,$s.controlState)
    if(Is-Unlocalized $s){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save 'S1-watch-unlocalized-samples.json' $samples
  Save 'S1-hit-unlocalized.json' ([ordered]@{hit=$hit; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_UNLOCALIZED'; $http.Dispose(); exit 2 }
  Write-Host 'UNLOCALIZED_HIT'
  $settle=@()
  $d2=(Get-Date).AddSeconds(6)
  while((Get-Date) -lt $d2){
    Start-Sleep -Milliseconds 700
    $settle += (Get-LocSnap)
  }
  Save 'S1-settle-unlocalized.json' $settle
  $http.Dispose(); return
}

if($phase -eq 'probe-unlocalized'){
  "=== S2 probe while unlocalized ==="
  $before=Get-LocSnap
  Save 'S2-before.json' $before
  if(Is-Localized $before){ Write-Host 'WARN still localized; continuing probe anyway' }

  $routeProbes=@()
  foreach($sid in @(1,2,3,4,5)){
    $json=(@{mapId=$mapId; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
    $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
    $c0=$null; $msg=$null
    if($r.parsed.result.deviceCostsList){ $c0=$r.parsed.result.deviceCostsList[0].costs; $msg=$r.parsed.result.deviceCostsList[0].message }
    $routeProbes += [ordered]@{stationId=$sid; code=$r.parsed.code; costs=$c0; message=$msg}
  }
  Save 'S2-route-costs.json' $routeProbes

  $dest=1
  $okRoute=$routeProbes | Where-Object { $_.costs -ne $null -and $_.costs -gt 0 -and $_.message -eq 'ok' } | Select-Object -First 1
  if($okRoute){ $dest=[int]$okRoute.stationId }
  $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
  $uid="riot-behavior-lab-R23-unloc-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$dest}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  Save 'S2-create.json' ([ordered]@{uid=$uid; dest=$dest; mapId=$mapId; code=$cr.parsed.code; message=$cr.parsed.message; body=$cr.body})

  $samples=@()
  $deadline=(Get-Date).AddSeconds(25)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 900
    $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null
    $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo; $det=$by.parsed.result
    $row=[ordered]@{
      at=(Get-Date -Format 'HH:mm:ss.fff')
      orderState=$det.orderState; orderId=$det.orderId; id=$det.id
      proc=$(if($vti){$vti.procState}else{$null})
      loc=$(if($v){[string]$v.locationState}else{$null})
      conf=$(if($v){$v.confidence}else{$null})
      st=$(if($v){$v.currentStation}else{$null})
    }
    $samples += $row
    Write-Host ("[{0}] order={1} proc={2} loc={3} conf={4}" -f $row.at,$row.orderState,$row.proc,$row.loc,$row.conf)
    if($row.orderState -in @(2,3,4,5,6)){ break }
  }
  Save 'S2-samples.json' $samples

  $last=$samples[-1]
  if($last -and $last.orderState -in @(1,3,7,9)){
    $cxl=Cancel-Order $last.orderId $last.id 'R23-unloc-cleanup'
    Save 'S2-cleanup.json' $cxl
  }
  Save 'S2-after.json' (Get-LocSnap)
  $http.Dispose(); Write-Host DONE; return
}

if($phase -eq 'watch-localized'){
  "=== S3 watch LOCALIZED again (timeout ${timeoutSec}s) ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  $hit=$false
  while((Get-Date) -lt $deadline){
    $s=Get-LocSnap
    $samples += $s
    Write-Host ("[{0}] loc={1} prop={2} conf={3} st={4} map={5} control={6}" -f $s.at,$s.locationState,$s.prop_locationState,$s.confidence,$s.station,$s.mapName,$s.controlState)
    if(Is-Localized $s){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save 'S3-watch-localized-samples.json' $samples
  Save 'S3-hit-localized.json' ([ordered]@{hit=$hit; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_LOCALIZED'; $http.Dispose(); exit 2 }
  Write-Host 'LOCALIZED_HIT'
  $settle=@()
  $d2=(Get-Date).AddSeconds(6)
  while((Get-Date) -lt $d2){
    Start-Sleep -Milliseconds 700
    $settle += (Get-LocSnap)
  }
  Save 'S3-settle-localized.json' $settle
  $http.Dispose(); return
}

if($phase -eq 'api-stop'){
  "=== API stopLocation probe ==="
  $before=Get-LocSnap
  Save 'API-stop-before.json' $before
  $url="$($e.baseUrl)/api/task/vehicles/stopLocation?vehicleKey=$([uri]::EscapeDataString($key))"
  $r=Invoke-Api POST $url $null
  Save 'API-stop-call.json' ([ordered]@{url=$url; status=$r.status; code=$r.parsed.code; message=$r.parsed.message; body=$r.body; error=$r.error})
  Start-Sleep -Seconds 2
  $after=Get-LocSnap
  Save 'API-stop-after.json' $after
  Write-Host ("stopLocation code={0} locBefore={1} locAfter={2}" -f $r.parsed.code,$before.locationState,$after.locationState)
  $http.Dispose(); return
}

if($phase -eq 'api-start'){
  $stationNo = if($args.Count -ge 2){ $args[1] } else { '1' }
  "=== API startLocation stationNo=$stationNo ==="
  $before=Get-LocSnap
  Save 'API-start-before.json' $before
  $url="$($e.baseUrl)/api/task/vehicles/startLocation?vehicleKey=$([uri]::EscapeDataString($key))&stationNo=$stationNo"
  $r=Invoke-Api POST $url $null
  Save 'API-start-call.json' ([ordered]@{url=$url; stationNo=$stationNo; status=$r.status; code=$r.parsed.code; message=$r.parsed.message; body=$r.body; error=$r.error})
  Start-Sleep -Seconds 2
  $after=Get-LocSnap
  Save 'API-start-after.json' $after
  Write-Host ("startLocation code={0} locBefore={1} locAfter={2}" -f $r.parsed.code,$before.locationState,$after.locationState)
  $http.Dispose(); return
}

if($phase -eq 'redispatch'){
  $base=Get-LocSnap
  Save 'S4-before-redispatch.json' $base
  if(-not (Is-Localized $base)){ throw 'not localized' }
  if($base.statusType -ne 'online'){ throw 'not online' }
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
  $uid="riot-behavior-lab-R23-after-loc-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$chosen}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  Save 'S4-create.json' ([ordered]@{uid=$uid; dest=$chosen; cost=$chosenCost; code=$cr.parsed.code; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed" }
  $samples=@()
  $deadline=(Get-Date).AddSeconds(120)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null
    $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo; $det=$by.parsed.result
    $row=[ordered]@{at=(Get-Date -Format 'HH:mm:ss.fff'); orderState=$det.orderState; proc=$vti.procState; loc=[string]$v.locationState; st=$v.currentStation}
    $samples += $row
    Write-Host ("[{0}] order={1} proc={2} loc={3} st={4}" -f $row.at,$row.orderState,$row.proc,$row.loc,$row.st)
    if($row.orderState -in @(2,4,5,6)){ break }
  }
  Save 'S4-samples.json' $samples
  $final=$samples[-1]
  if($final.orderState -in @(1,3,7,9)){
    $det=(Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null).parsed.result
    $cxl=Cancel-Order $det.orderId $det.id 'R23-timeout'
    Save 'S4-cleanup.json' $cxl
  }
  Save 'E9-final.json' (Get-LocSnap)
  $http.Dispose(); Write-Host DONE; return
}

if($phase -eq 'snapshot'){
  $s=Get-LocSnap
  $name = if($args.Count -ge 2){ $args[1] } else { 'snap' }
  Save ("SNAP-$name.json") $s
  Write-Host ("SNAP loc={0} prop={1} conf={2} st={3}" -f $s.locationState,$s.prop_locationState,$s.confidence,$s.station)
  $http.Dispose(); return
}

throw "unknown phase $phase"
