$ErrorActionPreference = 'Stop'
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir '..\..\..')).Path
$config = Get-Content -LiteralPath (Join-Path $labRoot 'environment.local.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir 'runs-attempt-3'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false

Add-Type -AssemblyName System.Net.Http
$client = [System.Net.Http.HttpClient]::new()
$client.Timeout = [TimeSpan]::FromSeconds(20)
$expectedVehicleName = -join ([char[]]@(0x65B0,0x57FA,0x6D4B,0x8BD5,0x0033,0x0030,0x0030,0x0063,0x534F,0x4F5C,0x0031))
$key = [string]$config.testVehicleKey
$mapId = 30
$expectedMapName = 'api' + (-join ([char[]]@(0x6D4B,0x8BD5,0x0032)))
$discriminatorOnly = $true
$sequence = 0
$createdOrders = [System.Collections.Generic.List[object]]::new()
$scenarioResults = [System.Collections.Generic.List[object]]::new()

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
    $bytes = $response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
    $responseBody = [System.Text.Encoding]::UTF8.GetString($bytes)
    foreach ($secret in @([string]$config.callApiKey, [string]$config.password)) {
      if (-not [string]::IsNullOrWhiteSpace($secret)) { $responseBody = $responseBody.Replace($secret, '<redacted>') }
    }
    $parsed = $null
    try { $parsed = $responseBody | ConvertFrom-Json } catch {}
    $watch.Stop()
    $record = [ordered]@{
      at = $started.ToString('o')
      elapsedMs = $watch.ElapsedMilliseconds
      request = [ordered]@{ method = $method; url = $url; headers = [ordered]@{ Authorization = '<redacted>' }; body = $requestBody }
      response = [ordered]@{ httpStatus = [int]$response.StatusCode; contentType = [string]$response.Content.Headers.ContentType; body = $responseBody; parsed = $parsed }
    }
    Save-Json ('{0:D3}-{1}.json' -f $script:sequence, $label) $record
    return $record
  } finally {
    $request.Dispose()
  }
}

function Code-Ok($parsed) { $null -ne $parsed -and ([string]$parsed.code -eq '0') }

function Get-Vehicle([string]$label) {
  $record = Invoke-Recorded "$label-vehicle-raw" 'GET' "/api/task/v1/task/getVehicleInfo/$key"
  $v = $record.response.parsed.vehicle
  $vti = $record.response.parsed.vehicleTaskInfo
  if ($null -eq $v -or $null -eq $vti) { throw "Vehicle response missing expected fields at $label" }
  $snapshot = [ordered]@{
    at = $record.at
    name = [string]$v.name
    station = $v.currentStation
    mapName = [string]$v.previousState.mapName
    movementState = [string]$v.movementState
    controlState = [string]$v.controlState
    emergencyState = [string]$v.emergencyState
    breakSwitchState = [string]$v.breakSwitchState
    locationState = [string]$v.locationState
    speed = $v.speed
    procState = [string]$vti.procState
    processingOrder = [bool]$vti.processingOrder
    enable = [bool]$vti.enable
    integrationLevel = [string]$vti.integrationLevel
  }
  Save-Json "$label-vehicle-snapshot.json" $snapshot
  return $snapshot
}

function Get-TestVehicleActiveOrders([string]$label) {
  $record = Invoke-Recorded "$label-nonfinal-raw" 'GET' '/api/order/v1/orderRecord?pageNum=1&pageSize=100&filterByState=1&filterByState=3&filterByState=7&filterByState=9'
  $hits = @()
  foreach ($order in @($record.response.parsed.result.records)) {
    if ($order.appointVehicleKey -eq $key -or $order.executeVehicleKey -eq $key) {
      $hits += [ordered]@{ id=$order.id; orderId=$order.orderId; upperId=$order.upperId; orderState=$order.orderState; appointVehicleKey=$order.appointVehicleKey; executeVehicleKey=$order.executeVehicleKey }
    }
  }
  Save-Json "$label-test-vehicle-nonfinal.json" $hits
  return @($hits)
}

function Assert-SafeBaseline([string]$label) {
  $snap = Get-Vehicle $label
  $active = @(Get-TestVehicleActiveOrders $label)
  if ([string]$config.testVehicleName -ne $expectedVehicleName) { throw "Configured test vehicle name mismatch" }
  if ($snap.name -ne $expectedVehicleName) { throw "Live vehicle name mismatch" }
  if ($snap.mapName -ne $expectedMapName) { throw "Live map mismatch: $($snap.mapName)" }
  if ($snap.station -notin @(1,2,3)) { throw "Unexpected current station: $($snap.station)" }
  if ($snap.procState -ne 'IDLE' -or $snap.processingOrder) { throw "Vehicle is not idle" }
  if ($snap.integrationLevel -ne 'ON_LINE' -or -not $snap.enable) { throw "Vehicle is not ON_LINE/enabled" }
  if ($snap.emergencyState -ne 'OK') { throw "Vehicle emergency state is not OK" }
  if ($snap.breakSwitchState -ne 'MOVABLE' -or $snap.controlState -ne 'CONTROL_STATE_OK') { throw "Vehicle is not movable/control-ok" }
  if ($snap.locationState -ne 'LOCATION_STATE_RUNNING') { throw "Vehicle localization is not running" }
  if ($active.Count -ne 0) { throw "Test vehicle has pre-existing non-final orders" }
  return $snap
}

function Wait-Vehicle([string]$label, [scriptblock]$predicate, [int]$attempts = 12) {
  for ($index = 1; $index -le $attempts; $index++) {
    Start-Sleep -Milliseconds 750
    $snap = Get-Vehicle ("$label-$index")
    if (& $predicate $snap) { return $snap }
  }
  throw "Vehicle condition not reached: $label"
}

function Set-Integration([string]$label, [ValidateSet('enable','disable')][string]$serviceId) {
  $body = [ordered]@{ deviceKeys = @($key); serviceId = $serviceId }
  $record = Invoke-Recorded $label 'POST' '/api/task/vehicles/updateVehicleIntegrationLevel' $body
  if (-not (Code-Ok $record.response.parsed)) { throw "Integration update failed: $serviceId" }
  return $record
}

function Invoke-Emergency([string]$label, [ValidateSet('triggerEmergency','cancelEmergency')][string]$serviceId) {
  $body = [ordered]@{ messageId = Get-Random -Minimum 100000 -Maximum 999999; mqCallback = [ordered]@{ tag='string'; topic='string' }; thingsProperties = [ordered]@{} }
  $record = Invoke-Recorded $label 'POST' "/api/device/v1/command/sync/service/$key/$serviceId" $body
  if (-not (Code-Ok $record.response.parsed)) { throw "Emergency service failed: $serviceId" }
  return $record
}

function New-QueuedMove([string]$scenario, $baseline) {
  $destination = if ([int]$baseline.station -eq 3) { 1 } else { 3 }
  $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $upperId = "riot-behavior-lab-R40-$scenario-$timestamp"
  $body = [ordered]@{
    appointVehicleKey = $key
    isAppointEnable = 1
    lockStatus = 0
    orderName = $upperId
    upperId = $upperId
    mission = @([ordered]@{ type='move'; mapId=$mapId; destination=$destination })
  }
  $record = Invoke-Recorded "$scenario-create" 'POST' '/api/order/v1/add/byDefaultMissions' $body
  if (-not (Code-Ok $record.response.parsed)) { throw "Create failed in $scenario" }
  $order = $record.response.parsed.result
  if ($order.appointVehicleKey -ne $key) { throw "Created order is not bound to test vehicle" }
  $tracked = [pscustomobject]@{ scenario=$scenario; upperId=[string]$order.upperId; orderId=[string]$order.orderId; numericId=[string]$order.id; active=$true }
  $createdOrders.Add($tracked)
  Start-Sleep -Seconds 1
  $detail = Invoke-Recorded "$scenario-detail-queueing" 'GET' "/api/order/v1/orderRecord/detailByUpperId/$([Uri]::EscapeDataString($tracked.upperId))"
  if ([int]$detail.response.parsed.result.orderState -ne 1) { throw "Order did not remain QUEUEING in $scenario" }
  return $tracked
}

function Get-DiagnosticSummary($record) {
  $parsed = $record.response.parsed
  [ordered]@{
    httpStatus = $record.response.httpStatus
    code = $parsed.code
    message = $parsed.message
    reason = $parsed.result.reason
    suggestList = @($parsed.result.suggestList)
    topLevelFields = @($parsed.PSObject.Properties.Name)
    resultFields = @($parsed.result.PSObject.Properties.Name)
  }
}

function Probe-Diagnostic([string]$scenario, $order) {
  $summaries = @()
  foreach ($kind in @('orderId','numericId','upperId')) {
    $value = [string]$order.$kind
    $record = Invoke-Recorded "$scenario-diagnostic-$kind" 'GET' "/api/task/vehicles/queryVehicleNotAssignOrder/$key/$([Uri]::EscapeDataString($value))"
    $summaries += [ordered]@{ keyKind=$kind; keyValue=$value; response=Get-DiagnosticSummary $record }
  }
  for ($index = 1; $index -le 3; $index++) {
    Start-Sleep -Seconds 1
    $record = Invoke-Recorded "$scenario-diagnostic-orderId-repeat-$index" 'GET' "/api/task/vehicles/queryVehicleNotAssignOrder/$key/$([Uri]::EscapeDataString($order.orderId))"
    $summaries += [ordered]@{ keyKind='orderId-repeat'; repeat=$index; keyValue=$order.orderId; response=Get-DiagnosticSummary $record }
  }
  $unknownValue = "riot-behavior-lab-R40-$scenario-order-does-not-exist"
  $unknown = Invoke-Recorded "$scenario-diagnostic-unknown-while-active" 'GET' "/api/task/vehicles/queryVehicleNotAssignOrder/$key/$([Uri]::EscapeDataString($unknownValue))"
  $summaries += [ordered]@{ keyKind='unknown-while-active'; keyValue=$unknownValue; response=Get-DiagnosticSummary $unknown }
  Save-Json "$scenario-diagnostic-summary.json" $summaries
  return $summaries
}

function Cancel-TrackedOrder([string]$label, $order) {
  if (-not $order.active) { return }
  $body = [ordered]@{ commandType='CMD_ORDER_CANCEL'; disableVehicle=$false; reason="riot-behavior-lab-R40-$label-cleanup" }
  $record = Invoke-Recorded "$label-cancel" 'POST' "/api/task/v1/order/command/$([Uri]::EscapeDataString($order.orderId))" $body
  if (-not (Code-Ok $record.response.parsed)) {
    $fallbackBody = [ordered]@{ orderId=[int64]$order.numericId; orderCommandDTO=$body }
    $fallback = Invoke-Recorded "$label-cancel-fallback-operate" 'POST' '/api/order/v1/operate' $fallbackBody
    if (-not (Code-Ok $fallback.response.parsed)) { throw "Both cancel paths failed for $($order.orderId)" }
  }
  Start-Sleep -Seconds 1
  $detail = Invoke-Recorded "$label-detail-after-cancel" 'GET' "/api/order/v1/orderRecord/detailByUpperId/$([Uri]::EscapeDataString($order.upperId))"
  if ([int]$detail.response.parsed.result.orderState -notin @(2,5,6)) { throw "Order not terminal after cancel" }
  $order.active = $false
  $postCancel = @()
  foreach ($kind in @('orderId','numericId','upperId')) {
    $value = [string]$order.$kind
    $diagnostic = Invoke-Recorded "$label-diagnostic-after-cancel-$kind" 'GET' "/api/task/vehicles/queryVehicleNotAssignOrder/$key/$([Uri]::EscapeDataString($value))"
    $postCancel += [ordered]@{ keyKind=$kind; keyValue=$value; response=Get-DiagnosticSummary $diagnostic }
  }
  Save-Json "$label-diagnostic-after-cancel-summary.json" $postCancel
}

function Try-Cleanup {
  $cleanup = [System.Collections.Generic.List[object]]::new()
  foreach ($order in $createdOrders) {
    if (-not $order.active) { continue }
    try { Cancel-TrackedOrder "$($order.scenario)-finally" $order; $cleanup.Add([ordered]@{ action='cancel'; scenario=$order.scenario; ok=$true }) }
    catch { $cleanup.Add([ordered]@{ action='cancel'; scenario=$order.scenario; ok=$false; error=$_.Exception.Message }) }
  }
  try {
    $snap = Get-Vehicle 'cleanup-pre-emergency'
    if ($snap.emergencyState -eq 'CAN_RECOVER') {
      Invoke-Emergency 'cleanup-cancelEmergency' 'cancelEmergency' | Out-Null
      Wait-Vehicle 'cleanup-wait-emergency-ok' { param($s) $s.emergencyState -eq 'OK' } | Out-Null
      $cleanup.Add([ordered]@{ action='cancelEmergency'; ok=$true })
    } elseif ($snap.emergencyState -ne 'OK') {
      $cleanup.Add([ordered]@{ action='cancelEmergency'; ok=$false; error="unexpected state $($snap.emergencyState), no automatic physical override" })
    }
  } catch { $cleanup.Add([ordered]@{ action='cancelEmergency'; ok=$false; error=$_.Exception.Message }) }
  try {
    $snap = Get-Vehicle 'cleanup-pre-integration'
    if ($snap.integrationLevel -ne 'ON_LINE' -or -not $snap.enable) {
      Set-Integration 'cleanup-enable' 'enable' | Out-Null
      Wait-Vehicle 'cleanup-wait-online' { param($s) $s.integrationLevel -eq 'ON_LINE' -and $s.enable } | Out-Null
      $cleanup.Add([ordered]@{ action='enable'; ok=$true })
    }
  } catch { $cleanup.Add([ordered]@{ action='enable'; ok=$false; error=$_.Exception.Message }) }
  Save-Json 'cleanup-actions.json' $cleanup
  return $cleanup
}

$runError = $null
try {
  if ([string]$config.testVehicleName -ne $expectedVehicleName) { throw 'Refusing to run: configured vehicle name mismatch' }
  $baseline = Assert-SafeBaseline 'E0'

  Set-Integration 'S1-disable' 'disable' | Out-Null
  Wait-Vehicle 'S1-wait-offline' { param($s) $s.integrationLevel -eq 'OFF_LINE' -and -not $s.enable } | Out-Null
  $s1Order = New-QueuedMove 'S1-offline' $baseline
  $s1Diagnostics = Probe-Diagnostic 'S1-offline' $s1Order
  $scenarioResults.Add([ordered]@{ scenario='vehicle-not-enabled'; order=$s1Order; diagnostics=$s1Diagnostics })
  Cancel-TrackedOrder 'S1-offline' $s1Order
  Set-Integration 'S1-enable' 'enable' | Out-Null
  Wait-Vehicle 'S1-wait-online' { param($s) $s.integrationLevel -eq 'ON_LINE' -and $s.enable -and $s.procState -eq 'IDLE' } | Out-Null
  $afterS1 = Assert-SafeBaseline 'S1-after'

  if (-not $discriminatorOnly) {
    Invoke-Emergency 'S2-triggerEmergency' 'triggerEmergency' | Out-Null
    Wait-Vehicle 'S2-wait-can-recover' { param($s) $s.emergencyState -eq 'CAN_RECOVER' -and $s.procState -eq 'IDLE' } | Out-Null
    $s2Order = New-QueuedMove 'S2-software-emergency' $afterS1
    $s2Diagnostics = Probe-Diagnostic 'S2-software-emergency' $s2Order
    $scenarioResults.Add([ordered]@{ scenario='recoverable-software-emergency'; order=$s2Order; diagnostics=$s2Diagnostics })
    Cancel-TrackedOrder 'S2-software-emergency' $s2Order
    Invoke-Emergency 'S2-cancelEmergency' 'cancelEmergency' | Out-Null
    Wait-Vehicle 'S2-wait-emergency-ok' { param($s) $s.emergencyState -eq 'OK' -and $s.procState -eq 'IDLE' } | Out-Null
  }
} catch {
  $runError = $_.Exception.Message
  Save-Json 'run-error.json' ([ordered]@{ at=[DateTimeOffset]::Now.ToString('o'); message=$runError; stack=$_.ScriptStackTrace })
} finally {
  $cleanup = Try-Cleanup
  $final = $null
  $finalActive = @()
  try { $final = Get-Vehicle 'E9-final'; $finalActive = @(Get-TestVehicleActiveOrders 'E9-final') } catch { Save-Json 'final-snapshot-error.json' ([ordered]@{ message=$_.Exception.Message }) }
  $safeFinal = $null -ne $final -and $final.name -eq $expectedVehicleName -and $final.procState -eq 'IDLE' -and -not $final.processingOrder -and $final.integrationLevel -eq 'ON_LINE' -and $final.enable -and $final.emergencyState -eq 'OK' -and $finalActive.Count -eq 0
  $summary = [ordered]@{
    completedAt=[DateTimeOffset]::Now.ToString('o')
    authorizedVehicle=$expectedVehicleName
    runError=$runError
    scenarios=$scenarioResults
    cleanup=$cleanup
    finalVehicle=$final
    finalActiveOrders=$finalActive
    safeFinal=$safeFinal
  }
  Save-Json '999-summary.json' $summary
  $client.Dispose()
}

if ($runError) { Write-Host "Round40 stopped: $runError"; exit 2 }
if (-not $summary.safeFinal) { Write-Host 'Round40 cleanup verification failed'; exit 3 }
Write-Host ("Round40 complete: vehicle={0}, scenarios={1}, safeFinal={2}" -f $expectedVehicleName, $summary.scenarios.Count, $summary.safeFinal)
