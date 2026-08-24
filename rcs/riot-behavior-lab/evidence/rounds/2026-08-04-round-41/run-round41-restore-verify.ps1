$ErrorActionPreference = 'Stop'
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir '..\..\..')).Path
$config = Get-Content -LiteralPath (Join-Path $labRoot 'environment.local.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir 'runs-restore-attempt-2'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
$expectedVehicleName = -join ([char[]]@(0x65B0,0x57FA,0x6D4B,0x8BD5,0x0033,0x0030,0x0030,0x0063,0x534F,0x4F5C,0x0031))
$expectedMapName = 'api' + (-join ([char[]]@(0x6D4B,0x8BD5,0x0032)))
$key = [string]$config.testVehicleKey
$mapId = 30
$sequence = 0

Add-Type -AssemblyName System.Net.Http
$client = [System.Net.Http.HttpClient]::new()
$client.Timeout = [TimeSpan]::FromSeconds(20)

function Save-Json([string]$name, $value) {
  [System.IO.File]::WriteAllText((Join-Path $outDir $name), (ConvertTo-Json -InputObject $value -Depth 30), $utf8)
}

function Invoke-Recorded([string]$label, [string]$method, [string]$path, $body = $null) {
  $script:sequence++
  $url = "$($config.baseUrl)$path"
  $request = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::new($method), $url)
  [void]$request.Headers.TryAddWithoutValidation('Authorization', "Bearer $($config.callApiKey)")
  $requestBody = $null
  if ($null -ne $body) {
    $requestBody = ConvertTo-Json -InputObject $body -Depth 12 -Compress
    $request.Content = [System.Net.Http.StringContent]::new($requestBody,[System.Text.Encoding]::UTF8,'application/json')
  }
  try {
    $started = [DateTimeOffset]::Now
    $response = $client.SendAsync($request).GetAwaiter().GetResult()
    $responseBody = [System.Text.Encoding]::UTF8.GetString($response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
    foreach ($secret in @([string]$config.callApiKey,[string]$config.password)) {
      if (-not [string]::IsNullOrWhiteSpace($secret)) { $responseBody = $responseBody.Replace($secret,'<redacted>') }
    }
    $parsed = $null
    try { $parsed = $responseBody | ConvertFrom-Json } catch {}
    $record = [ordered]@{
      at=$started.ToString('o')
      request=[ordered]@{method=$method;url=$url;headers=[ordered]@{Authorization='<redacted>'};body=$requestBody}
      response=[ordered]@{httpStatus=[int]$response.StatusCode;body=$responseBody;parsed=$parsed}
    }
    Save-Json ('{0:D3}-{1}.json' -f $script:sequence,$label) $record
    return $record
  } finally { $request.Dispose() }
}

function Get-Snapshot([string]$label) {
  $record = Invoke-Recorded "$label-vehicle" 'GET' "/api/task/v1/task/getVehicleInfo/$key"
  $v=$record.response.parsed.vehicle;$vti=$record.response.parsed.vehicleTaskInfo
  [ordered]@{name=[string]$v.name;mapName=[string]$v.previousState.mapName;station=$v.currentStation;speed=$v.speed;movementState=[string]$v.movementState;controlState=[string]$v.controlState;emergencyState=[string]$v.emergencyState;breakSwitchState=[string]$v.breakSwitchState;locationState=[string]$v.locationState;procState=[string]$vti.procState;processingOrder=[bool]$vti.processingOrder;enable=[bool]$vti.enable;integrationLevel=[string]$vti.integrationLevel}
}

$before = Get-Snapshot 'before'
if ([string]$config.testVehicleName -cne $expectedVehicleName -or $before.name -cne $expectedVehicleName) { throw 'Vehicle identity mismatch' }
if ($before.mapName -cne $expectedMapName -or $before.procState -ne 'IDLE' -or $before.processingOrder -or $before.integrationLevel -ne 'ON_LINE' -or -not $before.enable -or $before.emergencyState -ne 'OK' -or $before.breakSwitchState -ne 'MOVABLE' -or $before.controlState -ne 'CONTROL_STATE_OK' -or $before.locationState -ne 'LOCATION_STATE_RUNNING' -or [double]$before.speed -ne 0 -or $before.movementState -ne 'MT_FINISHED') { throw 'Vehicle is not in restored safe state' }

$orders = Invoke-Recorded 'nonfinal-orders' 'GET' '/api/order/v1/orderRecord?pageNum=1&pageSize=100&filterByState=1&filterByState=3&filterByState=7&filterByState=9'
$active = @()
foreach ($order in @($orders.response.parsed.result.records)) {
  if ($order.appointVehicleKey -eq $key -or $order.executeVehicleKey -eq $key) { $active += [ordered]@{orderId=$order.orderId;orderState=$order.orderState;upperId=$order.upperId} }
}
Save-Json 'test-vehicle-nonfinal.json' $active
if ($active.Count -ne 0) { throw 'Test vehicle has non-final orders' }

$routes = @()
foreach ($stationId in 1..6) {
  $body=[ordered]@{mapId=$mapId;stationId=$stationId;deviceKeys=@($key)}
  $record=Invoke-Recorded "route-station-$stationId" 'POST' '/api/task/v1/route/getRouteCostsBy' $body
  $item=@($record.response.parsed.result.deviceCostsList)[0]
  $routes += [ordered]@{stationId=$stationId;costs=$item.costs;message=$item.message}
}
Save-Json 'route-summary.json' $routes
$reachable=@($routes|Where-Object{[int64]$_.costs -gt 0 -and [string]$_.message -eq 'ok'})
if ($reachable.Count -eq 0) { throw 'No station is reachable after physical restore' }

$after=Get-Snapshot 'after'
$restored = $after.name -ceq $expectedVehicleName -and $after.procState -eq 'IDLE' -and -not $after.processingOrder -and $after.movementState -eq 'MT_FINISHED' -and [double]$after.speed -eq 0 -and $after.emergencyState -eq 'OK' -and $after.locationState -eq 'LOCATION_STATE_RUNNING'
Save-Json '999-summary.json' ([ordered]@{completedAt=[DateTimeOffset]::Now.ToString('o');before=$before;activeOrders=$active;routes=$routes;reachableStations=$reachable;after=$after;restored=$restored})
$client.Dispose()
if (-not $restored) { exit 3 }
Write-Host ("Round41 restore verified: reachableStations={0}" -f $reachable.Count)
