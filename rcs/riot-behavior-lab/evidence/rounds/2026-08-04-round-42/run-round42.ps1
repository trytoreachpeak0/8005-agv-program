param(
  [ValidateRange(1, 120)][int]$PollCount = 24,
  [ValidateRange(1, 60)][int]$PollIntervalSeconds = 5
)

$ErrorActionPreference = 'Stop'
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir '..\..\..')).Path
$configPath = Join-Path $labRoot 'environment.local.json'
$config = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
$expectedBaseUrl = 'http://172.10.1.72:8888'
if ([string]$config.baseUrl -ne $expectedBaseUrl) {
  throw "Round 42 is bound to $expectedBaseUrl; configured baseUrl differs."
}

$outDir = Join-Path $roundDir 'runs'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = [System.Text.UTF8Encoding]::new($false)
$client = [System.Net.Http.HttpClient]::new()
$client.Timeout = [TimeSpan]::FromSeconds(15)
$consecutiveFailures = 0

function Save-Json([string]$name, $value) {
  $path = Join-Path $outDir $name
  $json = ConvertTo-Json -InputObject $value -Depth 40
  foreach ($secret in @([string]$config.callApiKey, [string]$config.password)) {
    if (-not [string]::IsNullOrWhiteSpace($secret)) { $json = $json.Replace($secret, '<redacted>') }
  }
  [System.IO.File]::WriteAllText($path, $json, $utf8)
}

function Invoke-RecordedGet([string]$name, [string]$pathAndQuery) {
  $url = "$($config.baseUrl)$pathAndQuery"
  $request = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::Get, $url)
  [void]$request.Headers.TryAddWithoutValidation('Authorization', "Bearer $($config.callApiKey)")
  $started = [DateTimeOffset]::Now
  $watch = [System.Diagnostics.Stopwatch]::StartNew()
  try {
    $response = $client.SendAsync($request).GetAwaiter().GetResult()
    $bytes = $response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
    $watch.Stop()
    $body = [System.Text.Encoding]::UTF8.GetString($bytes)
    $parsed = $null
    try { $parsed = $body | ConvertFrom-Json } catch {}
    $record = [ordered]@{
      at = $started.ToString('o')
      elapsedMs = $watch.ElapsedMilliseconds
      request = [ordered]@{ method = 'GET'; url = $url; headers = [ordered]@{ Authorization = '<redacted>' } }
      response = [ordered]@{
        httpStatus = [int]$response.StatusCode
        bytes = $bytes.Length
        contentType = [string]$response.Content.Headers.ContentType
        parsed = $parsed
      }
    }
    if ([int]$response.StatusCode -eq 200 -and $null -ne $parsed -and [string]$parsed.code -eq '0') {
      $script:consecutiveFailures = 0
    } else {
      $script:consecutiveFailures++
    }
    Save-Json $name $record
    if ($script:consecutiveFailures -ge 3) { throw 'Three consecutive API failures; stopping Round 42.' }
    return $record
  } catch {
    $watch.Stop()
    $script:consecutiveFailures++
    $record = [ordered]@{
      at = $started.ToString('o')
      elapsedMs = $watch.ElapsedMilliseconds
      request = [ordered]@{ method = 'GET'; url = $url; headers = [ordered]@{ Authorization = '<redacted>' } }
      error = [ordered]@{ type = $_.Exception.GetType().FullName; message = $_.Exception.Message }
    }
    Save-Json $name $record
    if ($script:consecutiveFailures -ge 3) { throw 'Three consecutive API failures; stopping Round 42.' }
    return $record
  } finally {
    $request.Dispose()
  }
}

function Get-Items($record) {
  if ($null -eq $record.response -or $null -eq $record.response.parsed) { return @() }
  return @($record.response.parsed.result)
}

function Get-Percentile([long[]]$values, [double]$fraction) {
  if ($values.Count -eq 0) { return $null }
  $sorted = @($values | Sort-Object)
  $index = [Math]::Ceiling($fraction * $sorted.Count) - 1
  if ($index -lt 0) { $index = 0 }
  return $sorted[$index]
}

$binding = [ordered]@{
  recordedAt = [DateTimeOffset]::Now.ToString('o')
  authorization = 'User explicitly directed use of the test environment on 2026-08-04 because RIOT-8005-RUNTIME is unreachable.'
  environmentId = 'RIOT-CROSS-PROJECT-TEST'
  expectedBaseUrl = $expectedBaseUrl
  expectedBuild = '2.2.0.30'
  sourceSchema = [ordered]@{ environment = 'RIOT-8005-RUNTIME'; build = 'v2.2.0.14'; path = 'rcs/riot_swagger/task.json' }
  evidenceBoundary = 'Proxy behavior evidence only; not a live observation of RIOT-8005-RUNTIME v2.2.0.14.'
  pollCount = $PollCount
  pollIntervalSeconds = $PollIntervalSeconds
  writeOperationsAuthorized = @()
}
Save-Json '000-environment-binding.json' $binding

$build = Invoke-RecordedGet '001-build.json' '/api/version/v1/infos'
$allKeysRecord = Invoke-RecordedGet '002-all-vehicle-keys.json' '/api/task/vehicles/getAllVehicleKeys'

$pageCases = @(
  [ordered]@{ name = '010-default.json'; query = '/api/task/vehicles' },
  [ordered]@{ name = '011-page-1-size-1.json'; query = '/api/task/vehicles?pageNum=1&pageSize=1' },
  [ordered]@{ name = '012-page-2-size-1.json'; query = '/api/task/vehicles?pageNum=2&pageSize=1' },
  [ordered]@{ name = '013-page-1-size-5.json'; query = '/api/task/vehicles?pageNum=1&pageSize=5' },
  [ordered]@{ name = '014-page-2-size-5.json'; query = '/api/task/vehicles?pageNum=2&pageSize=5' },
  [ordered]@{ name = '015-page-1-size-100.json'; query = '/api/task/vehicles?pageNum=1&pageSize=100' }
)
$pageRecords = @()
foreach ($case in $pageCases) {
  $record = Invoke-RecordedGet $case.name $case.query
  $items = @(Get-Items $record)
  $pageRecords += [ordered]@{
    file = $case.name
    query = $case.query
    httpStatus = $record.response.httpStatus
    code = $record.response.parsed.code
    count = $items.Count
    deviceKeys = @($items | ForEach-Object { [string]$_.deviceKey })
    topLevelFields = $(if ($null -ne $record.response.parsed) { @($record.response.parsed.PSObject.Properties.Name) } else { @() })
    elapsedMs = $record.elapsedMs
    bytes = $record.response.bytes
  }
}
Save-Json '019-pagination-summary.json' $pageRecords

$map19 = Invoke-RecordedGet '020-map-19-stations.json' '/api/imap/v1/mapInfo/stations/19'
$map14 = Invoke-RecordedGet '021-map-14-stations.json' '/api/imap/v1/mapInfo/stations/14'
$stationMaps = @{
  'ZY_WB_Map' = @{}
  '尊阳电镀线opt' = @{}
}
foreach ($station in @(Get-Items $map19)) { $stationMaps['ZY_WB_Map'][[string]$station.id] = $station }
foreach ($station in @(Get-Items $map14)) { $stationMaps['尊阳电镀线opt'][[string]$station.id] = $station }

$pollRecords = @()
for ($index = 1; $index -le $PollCount; $index++) {
  if ($index -gt 1) { Start-Sleep -Seconds $PollIntervalSeconds }
  $fileName = ('100-poll-{0:D3}.json' -f $index)
  $record = Invoke-RecordedGet $fileName '/api/task/vehicles?pageNum=1&pageSize=100'
  $items = @(Get-Items $record)
  $pollRecords += [ordered]@{
    file = $fileName
    at = $record.at
    elapsedMs = $record.elapsedMs
    bytes = $record.response.bytes
    succeeded = ($record.response.httpStatus -eq 200 -and [string]$record.response.parsed.code -eq '0')
    vehicles = @($items | ForEach-Object {
      [ordered]@{
        deviceKey = [string]$_.deviceKey
        deviceName = [string]$_.deviceName
        status = $_.status
        enable = $_.enable
        currentMap = $_.currentMap
        currentPosition = $_.currentPosition
        batteryState = $_.batteryState
        locationState = $_.locationState
        procState = $_.procState
        movementState = $_.movementState
        taskType = $_.taskType
        orderTaskId = $_.orderTaskId
        startStationNo = $_.startStationNo
        startStationName = $_.startStationName
        endStationNo = $_.endStationNo
        endStationName = $_.endStationName
      }
    })
  }
}
Save-Json '190-poll-projections.json' $pollRecords

$referenceKeys = @((Get-Items $allKeysRecord) | ForEach-Object { [string]$_ } | Sort-Object -Unique)
$largePage = @($pageRecords | Where-Object { $_.file -eq '015-page-1-size-100.json' } | Select-Object -First 1)
$largePageKeys = @($largePage.deviceKeys | Sort-Object -Unique)
$missingFromLargePage = @($referenceKeys | Where-Object { $_ -notin $largePageKeys })
$unexpectedInLargePage = @($largePageKeys | Where-Object { $_ -notin $referenceKeys })

$occupancyObservations = @()
$targetObservations = @()
$unknownObservations = @()
$taskByVehicle = @{}
$taskClearTransitions = @()
foreach ($poll in $pollRecords) {
  foreach ($vehicle in $poll.vehicles) {
    $station = $null
    if ($stationMaps.ContainsKey([string]$vehicle.currentMap)) {
      $station = $stationMaps[[string]$vehicle.currentMap][[string]$vehicle.currentPosition]
    }
    if ($null -ne $station -and [string]$station.name -match '充电|charge' -and [string]$vehicle.batteryState -eq 'CHARGING') {
      $occupancyObservations += [ordered]@{
        at = $poll.at
        deviceKey = $vehicle.deviceKey
        deviceName = $vehicle.deviceName
        map = $vehicle.currentMap
        stationId = $vehicle.currentPosition
        stationName = $station.name
        stationType = $station.type
        batteryState = $vehicle.batteryState
      }
    }
    if ([string]$vehicle.taskType -eq 'CHARGE' -and -not [string]::IsNullOrWhiteSpace([string]$vehicle.orderTaskId)) {
      $targetObservations += [ordered]@{
        at = $poll.at
        deviceKey = $vehicle.deviceKey
        deviceName = $vehicle.deviceName
        orderTaskId = $vehicle.orderTaskId
        currentMap = $vehicle.currentMap
        endStationNo = $vehicle.endStationNo
        endStationName = $vehicle.endStationName
        procState = $vehicle.procState
      }
    }
    if ([int]$vehicle.status -eq 0 -or [string]$vehicle.locationState -eq 'ERROR' -or [int]$vehicle.currentPosition -eq 0) {
      $unknownObservations += [ordered]@{
        at = $poll.at
        deviceKey = $vehicle.deviceKey
        deviceName = $vehicle.deviceName
        status = $vehicle.status
        locationState = $vehicle.locationState
        currentPosition = $vehicle.currentPosition
      }
    }
    $previousTask = $taskByVehicle[$vehicle.deviceKey]
    $currentTask = [string]$vehicle.orderTaskId
    if (-not [string]::IsNullOrWhiteSpace([string]$previousTask) -and [string]::IsNullOrWhiteSpace($currentTask)) {
      $taskClearTransitions += [ordered]@{ at = $poll.at; deviceKey = $vehicle.deviceKey; deviceName = $vehicle.deviceName; previousOrderTaskId = $previousTask }
    }
    $taskByVehicle[$vehicle.deviceKey] = $currentTask
  }
}

$successfulPolls = @($pollRecords | Where-Object { $_.succeeded })
$latencies = [long[]]@($successfulPolls | ForEach-Object { [long]$_.elapsedMs })
$sizes = [long[]]@($successfulPolls | ForEach-Object { [long]$_.bytes })
$distinctOccupancy = @($occupancyObservations | Group-Object { "$($_.deviceKey)|$($_.stationId)" } | ForEach-Object { $_.Group[0] })
$distinctTargets = @($targetObservations | Group-Object { "$($_.deviceKey)|$($_.orderTaskId)" } | ForEach-Object { $_.Group[0] })
$distinctUnknowns = @($unknownObservations | Group-Object { "$($_.deviceKey)|$($_.status)|$($_.locationState)|$($_.currentPosition)" } | ForEach-Object { $_.Group[0] })
$observedKeys = @($successfulPolls.vehicles.deviceKey | Sort-Object -Unique)
$nonTestVehicleKeys = @($observedKeys | Where-Object { $_ -ne [string]$config.testVehicleKey })

$summary = [ordered]@{
  completedAt = [DateTimeOffset]::Now.ToString('o')
  environmentId = 'RIOT-CROSS-PROJECT-TEST'
  expectedBuild = '2.2.0.30'
  proxyEvidenceOnly = $true
  readOnlyRequestsOnly = $true
  pagination = $pageRecords
  coverage = [ordered]@{
    referenceKeyCount = $referenceKeys.Count
    largePageUniqueKeyCount = $largePageKeys.Count
    missingFromLargePage = $missingFromLargePage
    unexpectedInLargePage = $unexpectedInLargePage
    equalToIndependentKeySet = ($missingFromLargePage.Count -eq 0 -and $unexpectedInLargePage.Count -eq 0)
    observedPollKeyCount = $observedKeys.Count
    nonTestVehicleCount = $nonTestVehicleKeys.Count
  }
  polling = [ordered]@{
    requestedPolls = $PollCount
    successfulPolls = $successfulPolls.Count
    failureCount = ($PollCount - $successfulPolls.Count)
    failureRate = $(if ($PollCount -gt 0) { [double]($PollCount - $successfulPolls.Count) / $PollCount } else { $null })
    intervalSeconds = $PollIntervalSeconds
    latencyMs = [ordered]@{ min = Get-Percentile $latencies 0.0; median = Get-Percentile $latencies 0.5; p95 = Get-Percentile $latencies 0.95; max = Get-Percentile $latencies 1.0 }
    responseBytes = [ordered]@{ min = Get-Percentile $sizes 0.0; median = Get-Percentile $sizes 0.5; p95 = Get-Percentile $sizes 0.95; max = Get-Percentile $sizes 1.0 }
  }
  occupiedChargingStations = $distinctOccupancy
  chargeTargetObservations = $distinctTargets
  taskClearTransitions = $taskClearTransitions
  unknownStateExamples = $distinctUnknowns
  limits = @(
    'No server-side CPU, database, queue, or saturation metrics were available; client latency and failure rate do not prove absence of server resource impact.',
    'No state-changing action was used to manufacture a CHARGE or terminal transition sample.',
    'Results are from build 2.2.0.30 and cannot be promoted to a live v2.2.0.14 observation without target-environment confirmation.'
  )
}
Save-Json '999-summary.json' $summary

$client.Dispose()
Write-Host ("Round 42 complete: polls={0}/{1}, vehicles={2}, occupied={3}, chargeTargets={4}, clears={5}" -f $successfulPolls.Count,$PollCount,$observedKeys.Count,$distinctOccupancy.Count,$distinctTargets.Count,$taskClearTransitions.Count)
