$ErrorActionPreference = 'Stop'
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir '..\..\..')).Path
$config = Get-Content -LiteralPath (Join-Path $labRoot 'environment.local.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir 'runs'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
$expectedVehicleName = -join ([char[]]@(0x65B0,0x57FA,0x6D4B,0x8BD5,0x0033,0x0030,0x0030,0x0063,0x534F,0x4F5C,0x0031))
$expectedMapName = 'api' + (-join ([char[]]@(0x6D4B,0x8BD5,0x0032)))
$key = [string]$config.testVehicleKey
$mapId = 30
$sequence = 0
$trackedOrder = $null
$runError = $null

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
    $requestBody = if ($body -is [string]) { $body } else { ConvertTo-Json -InputObject $body -Depth 12 -Compress }
    $request.Content = [System.Net.Http.StringContent]::new($requestBody, [System.Text.Encoding]::UTF8, 'application/json')
  }
  $started = [DateTimeOffset]::Now
  $watch = [System.Diagnostics.Stopwatch]::StartNew()
  try {
    $response = $client.SendAsync($request).GetAwaiter().GetResult()
    $responseBody = [System.Text.Encoding]::UTF8.GetString($response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
    foreach ($secret in @([string]$config.callApiKey,[string]$config.password)) {
      if (-not [string]::IsNullOrWhiteSpace($secret)) { $responseBody = $responseBody.Replace($secret,'<redacted>') }
    }
    $parsed = $null
    try { $parsed = $responseBody | ConvertFrom-Json } catch {}
    $watch.Stop()
    $record = [ordered]@{
      at=$started.ToString('o')
      elapsedMs=$watch.ElapsedMilliseconds
      request=[ordered]@{method=$method;url=$url;headers=[ordered]@{Authorization='<redacted>'};body=$requestBody}
      response=[ordered]@{httpStatus=[int]$response.StatusCode;body=$responseBody;parsed=$parsed}
    }
    Save-Json ('{0:D3}-{1}.json' -f $script:sequence,$label) $record
    return $record
  } finally { $request.Dispose() }
}

function Code-Ok($parsed) { $null -ne $parsed -and [string]$parsed.code -eq '0' }

function Get-Vehicle([string]$label) {
  $record = Invoke-Recorded "$label-vehicle-raw" 'GET' "/api/task/v1/task/getVehicleInfo/$key"
  $v = $record.response.parsed.vehicle
  $vti = $record.response.parsed.vehicleTaskInfo
  if ($null -eq $v -or $null -eq $vti) { throw "Vehicle response missing fields at $label" }
  $snapshot = [ordered]@{
    at=$record.at
    name=[string]$v.name
    station=$v.currentStation
    mapName=[string]$v.previousState.mapName
    movementState=[string]$v.movementState
    controlState=[string]$v.controlState
    emergencyState=[string]$v.emergencyState
    breakSwitchState=[string]$v.breakSwitchState
    locationState=[string]$v.locationState
    speed=$v.speed
    procState=[string]$vti.procState
    processingOrder=[bool]$vti.processingOrder
    enable=[bool]$vti.enable
    integrationLevel=[string]$vti.integrationLevel
  }
  Save-Json "$label-vehicle-snapshot.json" $snapshot
  return $snapshot
}

function Get-ActiveOrders([string]$label) {
  $record = Invoke-Recorded "$label-nonfinal-raw" 'GET' '/api/order/v1/orderRecord?pageNum=1&pageSize=100&filterByState=1&filterByState=3&filterByState=7&filterByState=9'
  $hits = @()
  foreach ($order in @($record.response.parsed.result.records)) {
    if ($order.appointVehicleKey -eq $key -or $order.executeVehicleKey -eq $key) {
      $hits += [ordered]@{id=$order.id;orderId=$order.orderId;upperId=$order.upperId;orderState=$order.orderState;appointVehicleKey=$order.appointVehicleKey;executeVehicleKey=$order.executeVehicleKey}
    }
  }
  Save-Json "$label-test-vehicle-nonfinal.json" $hits
  return @($hits)
}

function Get-RouteCosts([string]$label) {
  $results = @()
  foreach ($stationId in 1..6) {
    $body = [ordered]@{mapId=$mapId;stationId=$stationId;deviceKeys=@($key)}
    $record = Invoke-Recorded "$label-route-station-$stationId" 'POST' '/api/task/v1/route/getRouteCostsBy' $body
    if (-not (Code-Ok $record.response.parsed)) { throw "Route probe failed for station $stationId" }
    $item = @($record.response.parsed.result.deviceCostsList)[0]
    $results += [ordered]@{stationId=$stationId;deviceKey=$item.deviceKey;costs=$item.costs;message=$item.message}
  }
  Save-Json "$label-route-summary.json" $results
  return $results
}

function Assert-SafeTooFarBaseline([string]$label) {
  if ([string]$config.testVehicleName -cne $expectedVehicleName) { throw 'Configured vehicle name mismatch' }
  $snap = Get-Vehicle $label
  $active = @(Get-ActiveOrders $label)
  if ($snap.name -cne $expectedVehicleName) { throw 'Live vehicle name mismatch' }
  if ($snap.mapName -cne $expectedMapName) { throw "Live map mismatch: $($snap.mapName)" }
  if ($snap.procState -ne 'IDLE' -or $snap.processingOrder) { throw 'Vehicle not IDLE' }
  if ($snap.integrationLevel -ne 'ON_LINE' -or -not $snap.enable) { throw 'Vehicle not ON_LINE/enabled' }
  if ($snap.emergencyState -ne 'OK' -or $snap.breakSwitchState -ne 'MOVABLE' -or $snap.controlState -ne 'CONTROL_STATE_OK') { throw 'Vehicle physical/control state not safe' }
  if ($snap.locationState -ne 'LOCATION_STATE_RUNNING') { throw 'Vehicle localization is not running' }
  if ([double]$snap.speed -ne 0 -or $snap.movementState -ne 'MT_FINISHED') { throw 'Vehicle is not stationary/finished' }
  if ($active.Count -ne 0) { throw 'Test vehicle has pre-existing non-final orders' }
  $routes = @(Get-RouteCosts "$label-too-far")
  if ($routes.Count -ne 6) { throw 'Incomplete route probe' }
  foreach ($route in $routes) {
    if ([int64]$route.costs -ne -1 -or [string]$route.message -ne 'vehicle route to station unreachable') { throw "Station $($route.stationId) is still reachable" }
  }
  return [ordered]@{vehicle=$snap;routes=$routes}
}

function New-Move($baseline) {
  $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $upperId = "riot-behavior-lab-R41-too-far-$timestamp"
  $body = [ordered]@{
    appointVehicleKey=$key
    isAppointEnable=1
    lockStatus=0
    orderName=$upperId
    upperId=$upperId
    mission=@([ordered]@{type='move';mapId=$mapId;destination=3})
  }
  $record = Invoke-Recorded 'S1-create' 'POST' '/api/order/v1/add/byDefaultMissions' $body
  if (-not (Code-Ok $record.response.parsed)) { throw 'Create failed' }
  $order = $record.response.parsed.result
  if ($order.appointVehicleKey -ne $key) { throw 'Created order is not bound to the test vehicle' }
  $tracked = [pscustomobject]@{upperId=[string]$order.upperId;orderId=[string]$order.orderId;numericId=[string]$order.id;active=$true}
  $script:trackedOrder = $tracked
  Start-Sleep -Seconds 1
  $detail = Invoke-Recorded 'S1-detail-queueing' 'GET' "/api/order/v1/orderRecord/detailByUpperId/$([Uri]::EscapeDataString($tracked.upperId))"
  if ([int]$detail.response.parsed.result.orderState -ne 1) { throw 'Order did not remain QUEUEING' }
  $afterVehicle = Get-Vehicle 'S1-after-create'
  if ($afterVehicle.movementState -ne 'MT_FINISHED' -or [double]$afterVehicle.speed -ne 0 -or $afterVehicle.procState -ne 'IDLE') { throw 'Vehicle changed movement state unexpectedly' }
  return $tracked
}

function Probe-Diagnostic($order) {
  $results = @()
  for ($index = 1; $index -le 3; $index++) {
    $record = Invoke-Recorded "S1-diagnostic-$index" 'GET' "/api/task/vehicles/queryVehicleNotAssignOrder/$key/$([Uri]::EscapeDataString($order.orderId))"
    $p = $record.response.parsed
    $results += [ordered]@{index=$index;httpStatus=$record.response.httpStatus;code=$p.code;message=$p.message;reason=$p.result.reason;suggestList=@($p.result.suggestList);resultFields=@($p.result.PSObject.Properties.Name)}
    Start-Sleep -Seconds 1
  }
  Save-Json 'S1-diagnostic-summary.json' $results
  return $results
}

function Cancel-Order([string]$label, $order) {
  if ($null -eq $order -or -not $order.active) { return }
  $body = [ordered]@{commandType='CMD_ORDER_CANCEL';disableVehicle=$false;reason="riot-behavior-lab-R41-$label-cleanup"}
  $record = Invoke-Recorded "$label-cancel" 'POST' "/api/task/v1/order/command/$([Uri]::EscapeDataString($order.orderId))" $body
  if (-not (Code-Ok $record.response.parsed)) {
    $fallbackBody = [ordered]@{orderId=[int64]$order.numericId;orderCommandDTO=$body}
    $fallback = Invoke-Recorded "$label-cancel-fallback" 'POST' '/api/order/v1/operate' $fallbackBody
    if (-not (Code-Ok $fallback.response.parsed)) { throw 'Both cancel paths failed' }
  }
  Start-Sleep -Seconds 1
  $detail = Invoke-Recorded "$label-detail-after-cancel" 'GET' "/api/order/v1/orderRecord/detailByUpperId/$([Uri]::EscapeDataString($order.upperId))"
  if ([int]$detail.response.parsed.result.orderState -notin @(2,5,6)) { throw 'Order not terminal after cancel' }
  $order.active = $false
}

try {
  $baseline = Assert-SafeTooFarBaseline 'E0'
  $trackedOrder = New-Move $baseline
  $diagnostics = Probe-Diagnostic $trackedOrder
  $routesWhileQueueing = @(Get-RouteCosts 'S1-queueing')
  foreach ($route in $routesWhileQueueing) {
    if ([int64]$route.costs -ne -1) { throw "Route became reachable for station $($route.stationId)" }
  }
  Cancel-Order 'S1' $trackedOrder
} catch {
  $runError = $_.Exception.Message
  Save-Json 'run-error.json' ([ordered]@{at=[DateTimeOffset]::Now.ToString('o');message=$runError;stack=$_.ScriptStackTrace})
} finally {
  if ($null -ne $trackedOrder -and $trackedOrder.active) {
    try { Cancel-Order 'finally' $trackedOrder } catch { Save-Json 'cleanup-error.json' ([ordered]@{message=$_.Exception.Message}) }
  }
  $finalVehicle = $null
  $finalActive = @()
  try { $finalVehicle=Get-Vehicle 'E9-final';$finalActive=@(Get-ActiveOrders 'E9-final') } catch { Save-Json 'final-error.json' ([ordered]@{message=$_.Exception.Message}) }
  $safeFinal = $null -ne $finalVehicle -and $finalVehicle.name -ceq $expectedVehicleName -and $finalVehicle.procState -eq 'IDLE' -and -not $finalVehicle.processingOrder -and $finalVehicle.movementState -eq 'MT_FINISHED' -and [double]$finalVehicle.speed -eq 0 -and $finalActive.Count -eq 0
  Save-Json '999-summary.json' ([ordered]@{completedAt=[DateTimeOffset]::Now.ToString('o');runError=$runError;baseline=$baseline;order=$trackedOrder;diagnostics=$diagnostics;routesWhileQueueing=$routesWhileQueueing;finalVehicle=$finalVehicle;finalActiveOrders=$finalActive;safeFinal=$safeFinal;physicalRestoreRequired=$true})
  $client.Dispose()
}

if ($runError) { Write-Host "Round41 stopped: $runError"; exit 2 }
$summary = Get-Content -LiteralPath (Join-Path $outDir '999-summary.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $summary.safeFinal) { Write-Host 'Round41 cleanup verification failed'; exit 3 }
Write-Host 'Round41 complete: too-far diagnostic captured, order cancelled, vehicle stationary'
