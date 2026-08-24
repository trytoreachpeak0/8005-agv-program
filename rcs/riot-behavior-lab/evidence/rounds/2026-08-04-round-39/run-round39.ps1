$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$repoRoot = (Resolve-Path (Join-Path $labRoot "..\..")).Path
$configPath = Join-Path $labRoot "environment.local.json"
$envConfig = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false

Add-Type -AssemblyName System.Net.Http
$client = [System.Net.Http.HttpClient]::new()
$client.Timeout = [TimeSpan]::FromSeconds(15)

function Save-Json([string]$name, $value) {
  $path = Join-Path $outDir $name
  [System.IO.File]::WriteAllText($path, (ConvertTo-Json -InputObject $value -Depth 30), $utf8)
}

function Invoke-RecordedGet([string]$name, [string]$url, [ValidateSet('valid','none','invalid')][string]$auth = 'valid') {
  $request = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::Get, $url)
  if ($auth -eq 'valid') {
    [void]$request.Headers.TryAddWithoutValidation('Authorization', "Bearer $($envConfig.callApiKey)")
  } elseif ($auth -eq 'invalid') {
    [void]$request.Headers.TryAddWithoutValidation('Authorization', 'Bearer riot-lab-invalid-token-round39')
  }

  $started = [DateTimeOffset]::Now
  $watch = [System.Diagnostics.Stopwatch]::StartNew()
  try {
    $response = $client.SendAsync($request).GetAwaiter().GetResult()
    $bytes = $response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
    $body = [System.Text.Encoding]::UTF8.GetString($bytes)
    $parsed = $null
    try { $parsed = $body | ConvertFrom-Json } catch {}
    $watch.Stop()
    $record = [ordered]@{
      at = $started.ToString('o')
      elapsedMs = $watch.ElapsedMilliseconds
      request = [ordered]@{
        method = 'GET'
        url = $url
        headers = [ordered]@{ Authorization = $(if ($auth -eq 'none') { '<omitted>' } else { '<redacted>' }) }
        authCase = $auth
      }
      response = [ordered]@{
        httpStatus = [int]$response.StatusCode
        contentType = [string]$response.Content.Headers.ContentType
        body = $body
        parsed = $parsed
      }
    }
    Save-Json $name $record
    return $record
  } catch {
    $watch.Stop()
    $record = [ordered]@{
      at = $started.ToString('o')
      elapsedMs = $watch.ElapsedMilliseconds
      request = [ordered]@{
        method = 'GET'
        url = $url
        headers = [ordered]@{ Authorization = $(if ($auth -eq 'none') { '<omitted>' } else { '<redacted>' }) }
        authCase = $auth
      }
      error = [ordered]@{ type = $_.Exception.GetType().FullName; message = $_.Exception.Message }
    }
    Save-Json $name $record
    return $record
  } finally {
    $request.Dispose()
  }
}

function Get-ResponseSummary($record) {
  $parsed = $record.response.parsed
  [ordered]@{
    httpStatus = $record.response.httpStatus
    code = $(if ($null -ne $parsed) { $parsed.code } else { $null })
    message = $(if ($null -ne $parsed) { $parsed.message } else { $null })
    msgDetail = $(if ($null -ne $parsed) { $parsed.msgDetail } else { $null })
    tid = $(if ($null -ne $parsed) { $parsed.tid } else { $null })
    hasResult = ($null -ne $parsed -and $null -ne $parsed.result)
    reason = $(if ($null -ne $parsed -and $null -ne $parsed.result) { $parsed.result.reason } else { $null })
    suggestList = $(if ($null -ne $parsed -and $null -ne $parsed.result) { @($parsed.result.suggestList) } else { @() })
    topLevelFields = $(if ($null -ne $parsed) { @($parsed.PSObject.Properties.Name) } else { @() })
    resultFields = $(if ($null -ne $parsed -and $null -ne $parsed.result) { @($parsed.result.PSObject.Properties.Name) } else { @() })
  }
}

function Read-HistoricalOrder([string]$relativePath, [string]$scenario) {
  $path = Join-Path $repoRoot $relativePath
  $json = Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
  $body = $json.body
  if (-not $body -and $json.create) { $body = $json.create.body }
  if (-not $body) { throw "No response body in $relativePath" }
  $parsed = $body | ConvertFrom-Json
  $order = $parsed.result
  [ordered]@{
    scenario = $scenario
    source = $relativePath.Replace('\','/')
    orderId = [string]$order.orderId
    numericId = [string]$order.id
    upperId = [string]$order.upperId
    originalOrderState = $order.orderState
  }
}

function Encode-Segment([string]$value) { [Uri]::EscapeDataString($value) }

$binding = [ordered]@{
  recordedAt = [DateTimeOffset]::Now.ToString('o')
  environmentId = 'RIOT-CROSS-PROJECT-TEST'
  baseUrl = $envConfig.baseUrl
  riotBuild = '2.2.0.30'
  buildEvidence = '.scratch/current-requirements-baseline/evidence/riot-interface/riot-environment-and-snapshot-user-confirmation-2026-08-03.md'
  vehicleName = $envConfig.testVehicleName
  vehicleKey = $envConfig.testVehicleKey
  authentication = 'Authorization: Bearer <CallApiKey redacted>'
  schemaEvidence = @(
    [ordered]@{ path = 'rcs/riot_swagger/task.json'; sha256 = '050A612E21EBE01B95D6FA35CA54D592BD83E108B69F5EB0703D8B903274D6D1'; sourceBuild = 'v2.2.0.14' },
    [ordered]@{ path = 'rcs/riot-behavior-lab/evidence/rounds/2026-07-20-round-7/runs/swagger-task.json'; sha256 = '53CDA75CDEF0DF07C8FCBD476ACB540C90B2A2A02DF9839680CB49D9360F56BD'; observedEnvironmentBuild = '2.2.0.30' }
  )
  endpoint = 'GET /api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey}'
  declaredResult = [ordered]@{ reason = 'string/free text'; suggestList = 'string[]/no enum' }
  writeOperationsAuthorized = @()
}
Save-Json '00-environment-binding.json' $binding

$vehicleUrl = "$($envConfig.baseUrl)/api/task/v1/task/getVehicleInfo/$(Encode-Segment $envConfig.testVehicleKey)"
$queueUrl = "$($envConfig.baseUrl)/api/order/v1/orderRecord?pageNum=1&pageSize=100&filterByState=1"
$beforeVehicle = Invoke-RecordedGet '01-before-vehicle.json' $vehicleUrl
$beforeQueue = Invoke-RecordedGet '02-before-global-queueing.json' $queueUrl

$currentQueueing = @()
if ($beforeQueue.response.parsed.result.records) {
  foreach ($record in $beforeQueue.response.parsed.result.records) {
    if ($record.appointVehicleKey -eq $envConfig.testVehicleKey -or $record.executeVehicleKey -eq $envConfig.testVehicleKey) {
      $currentQueueing += [ordered]@{
        scenario = 'current-test-vehicle-queueing'
        source = 'live pre-snapshot'
        orderId = [string]$record.orderId
        numericId = [string]$record.id
        upperId = [string]$record.upperId
        originalOrderState = $record.orderState
      }
    }
  }
}
Save-Json '03-current-test-vehicle-queueing.json' $currentQueueing

$history = @(
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-20-round-13\runs\S1-create-while-offline.json' 'vehicle-not-enabled'),
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-20-round-13\runs\S3-create-unreachable.json' 'route-unreachable-cross-map'),
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-22-round-29\runs\A-create.json' 'hardware-emergency'),
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-22-round-29\runs\B-create.json' 'recoverable-software-emergency'),
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-22-round-29\runs\F-create.json' 'vehicle-state-unmovable'),
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-22-round-30\runs\D2-create.json' 'vehicle-too-far-from-route'),
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-22-round-30\runs\L-create.json' 'vehicle-unlocalized'),
  (Read-HistoricalOrder 'rcs\riot-behavior-lab\evidence\rounds\2026-07-22-round-30\runs\P-create.json' 'vehicle-powered-off')
)
Save-Json '04-historical-candidates.json' $history

$candidates = @($currentQueueing) + @($history)
$probeSummaries = @()
$probeNumber = 0
foreach ($candidate in $candidates) {
  foreach ($kind in @('orderId','numericId','upperId')) {
    $value = [string]$candidate[$kind]
    if ([string]::IsNullOrWhiteSpace($value)) { continue }
    $probeNumber++
    $url = "$($envConfig.baseUrl)/api/task/vehicles/queryVehicleNotAssignOrder/$(Encode-Segment $envConfig.testVehicleKey)/$(Encode-Segment $value)"
    $fileName = ('10-probe-{0:D2}-{1}-{2}.json' -f $probeNumber, $candidate.scenario, $kind)
    $result = Invoke-RecordedGet $fileName $url
    $probeSummaries += [ordered]@{
      file = $fileName
      scenarioLabel = $candidate.scenario
      scenarioLabelWarning = 'Historical label identifies the original round only; it is not evidence that the live diagnostic evaluated that historical state.'
      keyKind = $kind
      keyValue = $value
      response = Get-ResponseSummary $result
    }
  }
}

$anchor = $history[0]
$unknownOrder = 'riot-lab-round39-order-does-not-exist'
$unknownVehicle = 'riot-lab-round39-vehicle-does-not-exist'
$negativeCases = @(
  [ordered]@{ name = 'unknown-order'; vehicle = $envConfig.testVehicleKey; order = $unknownOrder; auth = 'valid' },
  [ordered]@{ name = 'unknown-vehicle'; vehicle = $unknownVehicle; order = $anchor.orderId; auth = 'valid' },
  [ordered]@{ name = 'no-auth'; vehicle = $envConfig.testVehicleKey; order = $anchor.orderId; auth = 'none' },
  [ordered]@{ name = 'invalid-auth'; vehicle = $envConfig.testVehicleKey; order = $anchor.orderId; auth = 'invalid' }
)
$negativeSummaries = @()
$negativeNumber = 0
foreach ($case in $negativeCases) {
  $negativeNumber++
  $url = "$($envConfig.baseUrl)/api/task/vehicles/queryVehicleNotAssignOrder/$(Encode-Segment $case.vehicle)/$(Encode-Segment $case.order)"
  $fileName = ('50-negative-{0:D2}-{1}.json' -f $negativeNumber, $case.name)
  $result = Invoke-RecordedGet $fileName $url $case.auth
  $negativeSummaries += [ordered]@{ file = $fileName; case = $case.name; response = Get-ResponseSummary $result }
}

$successful = @($probeSummaries | Where-Object { $_.response.httpStatus -eq 200 -and [string]$_.response.code -eq '0' -and $_.response.hasResult })
$repeatSummaries = @()
if ($successful.Count -gt 0) {
  $chosen = $successful[0]
  $url = "$($envConfig.baseUrl)/api/task/vehicles/queryVehicleNotAssignOrder/$(Encode-Segment $envConfig.testVehicleKey)/$(Encode-Segment $chosen.keyValue)"
  for ($index = 1; $index -le 3; $index++) {
    Start-Sleep -Seconds 1
    $fileName = ('60-repeat-{0}.json' -f $index)
    $result = Invoke-RecordedGet $fileName $url
    $repeatSummaries += [ordered]@{ file = $fileName; index = $index; response = Get-ResponseSummary $result }
  }
}

$afterVehicle = Invoke-RecordedGet '90-after-vehicle.json' $vehicleUrl
$afterQueue = Invoke-RecordedGet '91-after-global-queueing.json' $queueUrl
$afterCurrentQueueing = @()
if ($afterQueue.response.parsed.result.records) {
  foreach ($record in $afterQueue.response.parsed.result.records) {
    if ($record.appointVehicleKey -eq $envConfig.testVehicleKey -or $record.executeVehicleKey -eq $envConfig.testVehicleKey) {
      $afterCurrentQueueing += [string]$record.orderId
    }
  }
}

$beforeCurrentIds = @($currentQueueing | ForEach-Object { [string]$_.orderId } | Sort-Object)
$afterCurrentIds = @($afterCurrentQueueing | Sort-Object)
$summary = [ordered]@{
  completedAt = [DateTimeOffset]::Now.ToString('o')
  readOnlyRequestsOnly = $true
  currentQueueingCountBefore = $beforeCurrentIds.Count
  currentQueueingCountAfter = $afterCurrentIds.Count
  currentQueueingOrderIdsBefore = $beforeCurrentIds
  currentQueueingOrderIdsAfter = $afterCurrentIds
  queueingIdentitySetUnchanged = (($beforeCurrentIds -join '|') -eq ($afterCurrentIds -join '|'))
  probeSummaries = $probeSummaries
  negativeSummaries = $negativeSummaries
  successfulCombinationCount = $successful.Count
  repeatSummaries = $repeatSummaries
  freshnessFieldsDeclaredOrObserved = @($repeatSummaries | ForEach-Object { $_.response.resultFields } | Sort-Object -Unique)
  caveat = 'GET plus unchanged before/after observable state is evidence of no observed business-state mutation, not a proof of internal side-effect freedom.'
}
Save-Json '99-summary.json' $summary

$client.Dispose()
Write-Host ("Round39 complete: probes={0}, successful={1}, currentQueueingBefore={2}, currentQueueingAfter={3}" -f $probeSummaries.Count, $successful.Count, $beforeCurrentIds.Count, $afterCurrentIds.Count)
