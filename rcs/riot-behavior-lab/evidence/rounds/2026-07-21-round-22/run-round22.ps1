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
$label = if($args.Count -ge 2){ $args[1] } else { 'boot' }
$timeoutSec = if($args.Count -ge 3){ [int]$args[2] } else { 180 }
Write-Host "Round22 knob phase=$phase label=$label"

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
function Get-KnobSnap {
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $st=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/status/$key" $null
  $prop=Invoke-Api GET "$($e.baseUrl)/api/device/v1/runtime/properties/$key" $null
  $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo
  $res=$prop.parsed.result
  $prev=$null; if($v){ $prev=$v.previousState }
  $vh=$null; if($v){ $vh=$v.vehicleHardware }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    label=$label
    apiReachable=$st.ok
    apiError=$st.error
    statusHttp=$st.status
    statusType=$(if($st.parsed.result){$st.parsed.result.type}else{$null})
    statusOk=$st.ok
    station=$(if($v){$v.currentStation}else{$null})
    procState=$(if($vti){$vti.procState}else{$null})
    enable=$(if($vti){$vti.enable}else{$null})
    integrationLevel=$(if($vti){[string]$vti.integrationLevel}else{$null})
    breakSwitchState=$(if($v){[string]$v.breakSwitchState}else{$null})
    mode=$(if($v){[string]$v.mode}else{$null})
    controlState=$(if($v){[string]$v.controlState}else{$null})
    hardwareState=$(if($v){[string]$v.hardwareState}else{$null})
    powerMode=$(if($v){[string]$v.powerMode}else{$null})
    emergencyState=$(if($v){[string]$v.emergencyState}else{$null})
    movementState=$(if($v){[string]$v.movementState}else{$null})
    prop_breakSwState=(PropVal $res 'breakSwState')
    prop_operationState=(PropVal $res 'operationState')
    prop_sysState=(PropVal $res 'sysState')
    prop_powerState=(PropVal $res 'powerState')
    prop_hstate=(PropVal $res 'hstate')
    prev_operationState=$(if($prev){$prev.operationState}else{$null})
    prev_sysState=$(if($prev){$prev.sysState}else{$null})
    hw_breakSwState=$(if($vh){$vh.breakSwState}else{$null})
    hw_powerState=$(if($vh){$vh.powerState}else{$null})
  }
}

function Test-Target($s, $target){
  switch($target){
    'boot' {
      return ($s.apiReachable -and $s.statusType -eq 'online' -and $s.breakSwitchState -eq 'MOVABLE' -and ($s.prop_breakSwState -eq 1 -or $s.prop_breakSwState -eq '1') -and $s.controlState -eq 'CONTROL_STATE_OK')
    }
    'release-brake' {
      return ($s.apiReachable -and $s.statusType -eq 'online' -and $s.breakSwitchState -eq 'UNMOVABLE' -and ($s.prop_breakSwState -eq 2 -or $s.prop_breakSwState -eq '2'))
    }
    'power-off' {
      # key: API still reachable AND status offline (5G independent power)
      return ($s.apiReachable -and $s.statusType -eq 'offline')
    }
    default { return $false }
  }
}

if($phase -eq 'baseline'){
  $s=Get-KnobSnap
  Save 'E0-boot-baseline.json' $s
  Write-Host ("BASE api={0} status={1} break={2} bProp={3} control={4}" -f $s.apiReachable,$s.statusType,$s.breakSwitchState,$s.prop_breakSwState,$s.controlState)
  if(-not (Test-Target $s 'boot')){ Write-Host 'WARN not in boot signature'; }
  $http.Dispose(); return
}

if($phase -eq 'wait'){
  $target = $label
  "=== wait target=$target timeout=${timeoutSec}s ==="
  $samples=@()
  $deadline=(Get-Date).AddSeconds($timeoutSec)
  $hit=$false
  while((Get-Date) -lt $deadline){
    $s=Get-KnobSnap
    $samples += $s
    Write-Host ("[{0}] api={1} status={2} break={3} bProp={4} control={5}" -f $s.at,$s.apiReachable,$s.statusType,$s.breakSwitchState,$s.prop_breakSwState,$s.controlState)
    if(Test-Target $s $target){ $hit=$true; break }
    Start-Sleep -Milliseconds 800
  }
  Save ("S-watch-$target-samples.json") $samples
  Save ("S-hit-$target.json") ([ordered]@{hit=$hit; target=$target; last=$samples[-1]})
  if(-not $hit){ Write-Host 'NO_TARGET'; $http.Dispose(); exit 2 }
  Write-Host 'TARGET_HIT'
  $settle=@()
  $d2=(Get-Date).AddSeconds(8)
  while((Get-Date) -lt $d2){
    Start-Sleep -Milliseconds 700
    $settle += (Get-KnobSnap)
  }
  Save ("S-settle-$target.json") $settle
  $http.Dispose(); return
}

if($phase -eq 'redispatch'){
  $base=Get-KnobSnap
  Save 'S4-before-redispatch.json' $base
  if(-not (Test-Target $base 'boot')){ Write-Host 'WARN not full boot signature; continuing if online' }
  if($base.statusType -ne 'online'){ throw 'not online' }
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
  $uid="riot-behavior-lab-R22-after-boot-$ts"
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
    $row=[ordered]@{at=(Get-Date -Format 'HH:mm:ss.fff'); orderState=$det.orderState; proc=$vti.procState; st=$v.currentStation; break=[string]$v.breakSwitchState}
    $samples += $row
    Write-Host ("[{0}] order={1} proc={2} st={3}" -f $row.at,$row.orderState,$row.proc,$row.st)
    if($row.orderState -in @(2,4,5,6)){ break }
  }
  Save 'S4-samples.json' $samples
  $final=$samples[-1]
  if($final.orderState -in @(1,3,7,9)){
    $det=(Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null).parsed.result
    $cxl=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$($det.orderId)" '{"commandType":"CMD_ORDER_CANCEL","disableVehicle":false,"reason":"R22-timeout"}'
    Save 'S4-cleanup.json' ([ordered]@{code=$cxl.parsed.code})
  }
  Save 'E9-final.json' (Get-KnobSnap)
  $http.Dispose(); Write-Host DONE; return
}

throw "unknown phase $phase"
