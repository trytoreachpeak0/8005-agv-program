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
$phase = if($args.Count -ge 1){ $args[0] } else { 'watch' }
Write-Host "Round19 emergency phase=$phase key=$key"

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

function Get-EmergSnap{
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo
  $prop=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/properties/$key" $null
  $emergProp=$null; $breakProp=$null; $sysProp=$null
  $res=$prop.parsed.result
  if($res){
    # result may be flat object of property bags
    if($res.emergencyState){ $emergProp=$res.emergencyState }
    if($res.breakSwState){ $breakProp=$res.breakSwState }
    if($res.sysState){ $sysProp=$res.sysState }
    if($res.PSObject.Properties.Name -contains 'emergencyState'){ $emergProp=$res.emergencyState }
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    emergencyState=$v.emergencyState
    breakSwitchState=$v.breakSwitchState
    controlState=$v.controlState
    hardwareState=$v.hardwareState
    movementState=[string]$v.movementState
    agvInfoState=$v.agvInfoState
    faultCodes=$v.faultCodes
    lastErrorCode=$v.lastErrorCode
    station=$v.currentStation; noStation=$v.noStation
    mapName=$(if($v.previousState){$v.previousState.mapName}else{$null})
    procState=$vti.procState; processingOrder=$vti.processingOrder
    enable=$vti.enable; integrationLevel=[string]$vti.integrationLevel
    propEmergency=$(if($emergProp -is [psobject] -and $emergProp.value -ne $null){$emergProp.value}else{$emergProp})
    propBreakSw=$(if($breakProp -is [psobject] -and $breakProp.value -ne $null){$breakProp.value}else{$breakProp})
    propSysState=$(if($sysProp -is [psobject] -and $sysProp.value -ne $null){$sysProp.value}else{$sysProp})
  }
}

function Invoke-DeviceService([string]$serviceId,[string]$mode){
  # mode: sync | async
  # UI body shape (Round19 Network): messageId(number) + mqCallback placeholders + empty thingsProperties
  $path = if($mode -eq 'async'){ "command/service" } else { "command/sync/service" }
  $url = "$($e.baseUrl)/api/device/v1/$path/$key/$serviceId"
  $mid = [int](Get-Random -Minimum 100000 -Maximum 999999)
  $uiBody = "{`"messageId`":$mid,`"mqCallback`":{`"tag`":`"string`",`"topic`":`"string`"},`"thingsProperties`":{}}"
  $attempts=@()
  foreach($body in @($uiBody,'{"thingsProperties":{}}','{}')){
    $r=Invoke-Api POST $url $body
    $attempts += [ordered]@{body=$body; status=$r.status; code=$r.parsed.code; message=$r.parsed.message; result=$r.parsed.result; preview=$r.body.Substring(0,[Math]::Min(1200,$r.body.Length))}
    if(CodeOk $r.parsed){ break }
  }
  return $attempts
}

if($phase -eq 'baseline'){
  $s=Get-EmergSnap
  Save 'E0-baseline.json' $s
  Write-Host ("BASE emerg={0} break={1} control={2} proc={3} st={4}" -f $s.emergencyState,$s.breakSwitchState,$s.controlState,$s.procState,$s.station)
  $http.Dispose(); return
}

if($phase -eq 'watch'){
  "=== S1 watch for emergency (timeout 180s) ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds(180)
  $hit=$false
  while((Get-Date) -lt $deadline){
    $s=Get-EmergSnap
    $samples += $s
    Write-Host ("[{0}] emerg={1} break={2} control={3} move={4} proc={5} propEmerg={6}" -f $s.at,$s.emergencyState,$s.breakSwitchState,$s.controlState,$s.movementState,$s.procState,$s.propEmergency)
    if($s.emergencyState -and $s.emergencyState -ne 'OK'){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save 'S1-watch-samples.json' $samples
  Save 'S1-hit.json' ([ordered]@{hit=$hit; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_EMERGENCY_WITHIN_TIMEOUT'; $http.Dispose(); exit 2 }
  Write-Host 'EMERGENCY_DETECTED'
  $http.Dispose(); return
}

if($phase -eq 'cancel'){
  "=== S2 cancelEmergency ==="
  $before=Get-EmergSnap
  Save 'S2-before-cancel.json' $before
  Write-Host ("before emerg={0}" -f $before.emergencyState)

  $syncAttempts=Invoke-DeviceService 'cancelEmergency' 'sync'
  Save 'S2-cancel-sync-attempts.json' $syncAttempts
  Write-Host ("sync last code={0} msg={1}" -f $syncAttempts[-1].code,$syncAttempts[-1].message)

  $afterSamples=@()
  $deadline=(Get-Date).AddSeconds(60)
  $cleared=$false
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 700
    $s=Get-EmergSnap
    $afterSamples += $s
    Write-Host ("[{0}] emerg={1} break={2} control={3}" -f $s.at,$s.emergencyState,$s.breakSwitchState,$s.controlState)
    if($s.emergencyState -eq 'OK'){ $cleared=$true; break }
  }
  Save 'S2-after-cancel-samples.json' $afterSamples

  if(-not $cleared){
    Write-Host 'sync cancel did not clear; try async'
    $asyncAttempts=Invoke-DeviceService 'cancelEmergency' 'async'
    Save 'S2-cancel-async-attempts.json' $asyncAttempts
    $deadline=(Get-Date).AddSeconds(45)
    while((Get-Date) -lt $deadline){
      Start-Sleep -Milliseconds 700
      $s=Get-EmergSnap
      $afterSamples += $s
      Write-Host ("[A] emerg={0}" -f $s.emergencyState)
      if($s.emergencyState -eq 'OK'){ $cleared=$true; break }
    }
    Save 'S2-after-cancel-samples.json' $afterSamples
  }

  Save 'S2-cancel-summary.json' ([ordered]@{cleared=$cleared; before=$before; after=$afterSamples[-1]})
  Write-Host ("CLEARED={0}" -f $cleared)
  $http.Dispose()
  if(-not $cleared){ exit 3 }
  return
}

if($phase -eq 'redispatch'){
  "=== S3 short redispatch after clear ==="
  $base=Get-EmergSnap
  Save 'S3-before-create.json' $base
  if($base.emergencyState -ne 'OK'){ throw "still emergency: $($base.emergencyState)" }
  if($base.enable -ne $true -or $base.integrationLevel -ne 'ON_LINE'){ throw 'not online' }

  # map30 stations: pick nearest other than current
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
  $uid="riot-behavior-lab-R19-after-e-stop-$ts"
  $json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$mapId,`"destination`":$chosen}]}"
  $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
  Save 'S3-create.json' ([ordered]@{uid=$uid; dest=$chosen; cost=$chosenCost; code=$cr.parsed.code; body=$cr.body})
  if(-not (CodeOk $cr.parsed)){ throw "create failed $($cr.body)" }

  $samples=@()
  $deadline=(Get-Date).AddSeconds(180)
  while((Get-Date) -lt $deadline){
    Start-Sleep -Milliseconds 800
    $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null
    $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo; $det=$by.parsed.result
    $row=[ordered]@{at=(Get-Date -Format 'HH:mm:ss.fff'); orderState=$det.orderState; proc=$vti.procState; st=$v.currentStation; emerg=$v.emergencyState}
    $samples += $row
    Write-Host ("[{0}] order={1} proc={2} st={3} emerg={4}" -f $row.at,$row.orderState,$row.proc,$row.st,$row.emerg)
    if($row.orderState -in @(2,4,5,6)){ break }
  }
  Save 'S3-samples.json' $samples
  $final=$samples[-1]
  if($final.orderState -in @(1,3,7,9)){
    $oid=(Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null).parsed.result.orderId
    $cxl=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" '{"commandType":"CMD_ORDER_CANCEL","disableVehicle":false,"reason":"R19-S3-timeout"}'
    Save 'S3-cleanup.json' ([ordered]@{code=$cxl.parsed.code})
  }
  Save 'E9-final.json' (Get-EmergSnap)
  $http.Dispose()
  Write-Host DONE
  return
}

throw "unknown phase: $phase"
