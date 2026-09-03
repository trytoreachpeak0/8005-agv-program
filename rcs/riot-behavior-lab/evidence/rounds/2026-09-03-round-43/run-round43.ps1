#Requires -Version 7
<#
Round 43 (2026-09-03) - Can the map edge table support station-to-station route cost?

Target: 8005 PRODUCTION RIoT (172.19.206.222:8888), mapId 25. Three AGVs are running
real transport jobs there. Everything here is a read-only query; see round-plan.md for
the approved scope, the stop conditions and the decision thresholds.

Section one touches no vehicle at all. Section two needs one vehicle key and is skipped
unless that vehicle happens to be idle and docked on this map.

Credentials come from $env:CONTROL_SERVER_RIOT_CALL_API_KEY (same source as the control
server). environment.local.json is bound to the test RIoT and is deliberately not touched.
#>
param(
  [ValidateRange(1, 400)][int]$MapId = 25,
  [string]$VehicleKey,
  [switch]$SkipVehicleSection
)

$ErrorActionPreference = 'Stop'
$roundDir = $PSScriptRoot
$outDir = Join-Path $roundDir 'runs'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$baseUrl = 'http://172.19.206.222:8888'
$targetHost = '172.19.206.222'

$callApiKey = $env:CONTROL_SERVER_RIOT_CALL_API_KEY
if ([string]::IsNullOrWhiteSpace($callApiKey)) {
  throw 'CONTROL_SERVER_RIOT_CALL_API_KEY is not set. Round 43 reads the production RIoT key from that variable.'
}

# Clash TUN answers ICMP itself and completes TCP handshakes locally, so a probe through it
# is fiction. Refuse to run rather than collect evidence that means nothing.
$route = Find-NetRoute -RemoteIPAddress $targetHost -ErrorAction Stop | Select-Object -First 1
if ($route.InterfaceAlias -match 'Clash') {
  throw "Route to $targetHost goes through '$($route.InterfaceAlias)'. Install the bypass route first (remote-ops/factory-server/scripts/01-control-host-route.ps1); evidence collected through Clash TUN is fiction."
}
Write-Host "[route] $targetHost via $($route.InterfaceAlias)"

$utf8 = [System.Text.UTF8Encoding]::new($false)
$client = [System.Net.Http.HttpClient]::new()
$client.Timeout = [TimeSpan]::FromSeconds(30)
$script:consecutiveFailures = 0
$script:step = 0

function Save-Json([string]$name, $value) {
  $path = Join-Path $outDir $name
  $json = ConvertTo-Json -InputObject $value -Depth 60
  if (-not [string]::IsNullOrWhiteSpace($callApiKey)) { $json = $json.Replace($callApiKey, '<redacted>') }
  [System.IO.File]::WriteAllText($path, $json, $utf8)
}

function Assert-CanContinue {
  if ($script:consecutiveFailures -ge 3) {
    throw 'Three consecutive failures; stopping per round-plan stop condition.'
  }
}

function Invoke-Recorded {
  param(
    [Parameter(Mandatory)][string]$Name,
    [Parameter(Mandatory)][ValidateSet('GET', 'POST')][string]$Method,
    [Parameter(Mandatory)][string]$PathAndQuery,
    $Body = $null
  )
  Assert-CanContinue
  $script:step++
  $url = "$baseUrl$PathAndQuery"
  $request = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::new($Method), $url)
  [void]$request.Headers.TryAddWithoutValidation('Authorization', "Bearer $callApiKey")
  $bodyJson = $null
  if ($null -ne $Body) {
    $bodyJson = ConvertTo-Json -InputObject $Body -Depth 10 -Compress
    $request.Content = [System.Net.Http.StringContent]::new($bodyJson, [System.Text.Encoding]::UTF8, 'application/json')
  }
  $started = [DateTimeOffset]::Now
  $watch = [System.Diagnostics.Stopwatch]::StartNew()
  $record = $null
  try {
    $response = $client.SendAsync($request).GetAwaiter().GetResult()
    $bytes = $response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
    $watch.Stop()
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    $parsed = $null
    try { $parsed = $text | ConvertFrom-Json } catch { }
    # Raw body is the point of this round: field naming (camelCase vs snake_case) is
    # barrier #1 and only survives verbatim.
    $record = [ordered]@{
      at        = $started.ToString('o')
      elapsedMs = $watch.ElapsedMilliseconds
      request   = [ordered]@{
        method  = $Method
        url     = $url
        body    = $bodyJson
        headers = [ordered]@{ Authorization = '<redacted>' }
      }
      response  = [ordered]@{
        httpStatus  = [int]$response.StatusCode
        bytes       = $bytes.Length
        contentType = [string]$response.Content.Headers.ContentType
        rawBody     = $text
        parsed      = $parsed
      }
    }
    if ([int]$response.StatusCode -eq 200 -and $null -ne $parsed -and [string]$parsed.code -eq '0') {
      $script:consecutiveFailures = 0
    } else {
      $script:consecutiveFailures++
    }
  } catch {
    $watch.Stop()
    $script:consecutiveFailures++
    $record = [ordered]@{
      at        = $started.ToString('o')
      elapsedMs = $watch.ElapsedMilliseconds
      request   = [ordered]@{ method = $Method; url = $url; body = $bodyJson }
      error     = $_.Exception.Message
    }
  }
  Save-Json ('{0:d3}-{1}.json' -f $script:step, $Name) $record
  $status = if ($null -ne $record.response) { $record.response.httpStatus } else { 'ERR' }
  Write-Host ('[{0:d3}] {1} {2} -> {3}' -f $script:step, $Method, $PathAndQuery, $status)
  return $record
}

# ============================ SECTION ONE: no vehicle ========================

Invoke-Recorded -Name 'build' -Method GET -PathAndQuery '/api/task/v1/system/build' | Out-Null

$edges = Invoke-Recorded -Name "edges-map-$MapId" -Method GET -PathAndQuery "/api/imap/v1/mapInfo/edges/$MapId"
$stations = Invoke-Recorded -Name "stations-map-$MapId" -Method GET -PathAndQuery "/api/imap/v1/mapInfo/stations/$MapId"

Invoke-Recorded -Name "removed-edge-map-$MapId" -Method GET -PathAndQuery "/api/imap/v1/mapResource/removedEdge/$MapId" | Out-Null
Invoke-Recorded -Name "removed-edge-detail-map-$MapId" -Method GET -PathAndQuery "/api/imap/v1/mapResource/removedEdgeDetail/$MapId" | Out-Null
Invoke-Recorded -Name "removed-station-map-$MapId" -Method GET -PathAndQuery "/api/imap/v1/mapResource/removedStation/$MapId" | Out-Null
Invoke-Recorded -Name 'edge-group-all' -Method GET -PathAndQuery '/api/imap/v1/mapEdgeGroup/all' | Out-Null
Invoke-Recorded -Name 'dynamic-route-cost' -Method GET -PathAndQuery '/api/task/v1/route/' | Out-Null
Invoke-Recorded -Name 'cost-unit' -Method GET -PathAndQuery '/api/task/v1/route/getCostUnit' | Out-Null

# --- self-made control set ---------------------------------------------------
# mapId 25's station ids are not known before this round (map28's are on a different
# RIoT), so the pairs are derived from the station list just fetched, by a deterministic
# rule, and written into the evidence.
$stationIds = @()
$picks = @()
$result = $stations.response.parsed.result
if ($result -is [array]) {
  $stationIds = @($result | ForEach-Object { [int]$_.id } | Sort-Object -Unique)
}

if ($stationIds.Count -lt 4) {
  Save-Json '800-control-set-skipped.json' ([ordered]@{
      at     = [DateTimeOffset]::Now.ToString('o')
      reason = "only $($stationIds.Count) station ids parsed; need at least 4 to build a control set"
      note   = 'Station payload may use snake_case keys that ConvertFrom-Json exposes differently; inspect rawBody of the stations request offline.'
    })
  Write-Host "[skip] control set: only $($stationIds.Count) station ids parsed"
} else {
  # Spread the picks across the id range rather than taking the first few, so the pairs
  # are unlikely to all sit on one edge.
  $n = $stationIds.Count
  $picks = @(0, [int]($n * 0.2), [int]($n * 0.4), [int]($n * 0.6), [int]($n * 0.8), $n - 1) |
    ForEach-Object { $stationIds[$_] } | Sort-Object -Unique
  Save-Json '799-control-set-plan.json' ([ordered]@{
      at              = [DateTimeOffset]::Now.ToString('o')
      stationIdCount  = $n
      pickedStationIds = $picks
      rule            = 'indices 0, 20%, 40%, 60%, 80%, last of the sorted unique station id list'
    })

  $i = 0
  foreach ($start in $picks) {
    $ends = @($picks | Where-Object { $_ -ne $start })
    if ($ends.Count -lt 2) { continue }
    $i++
    $body = [ordered]@{ mapId = $MapId; startStationId = $start; endStationIds = $ends }
    Invoke-Recorded -Name ('near-end-{0:d2}-from-{1}' -f $i, $start) -Method POST `
      -PathAndQuery '/api/task/v1/route/queryNearEnd' -Body $body | Out-Null
  }

  $i = 0
  foreach ($end in $picks) {
    $starts = @($picks | Where-Object { $_ -ne $end })
    if ($starts.Count -lt 2) { continue }
    $i++
    $body = [ordered]@{ mapId = $MapId; endStationId = $end; startStationIds = $starts }
    Invoke-Recorded -Name ('near-start-{0:d2}-to-{1}' -f $i, $end) -Method POST `
      -PathAndQuery '/api/task/v1/route/queryNearestStart' -Body $body | Out-Null
  }

  # Pairwise two-candidate cases pin the ordering down harder than one wide list:
  # each answer is a direct A-vs-B verdict for the offline reproduction to match.
  $i = 0
  for ($a = 0; $a -lt $picks.Count - 1; $a++) {
    for ($b = $a + 1; $b -lt $picks.Count; $b++) {
      if ($a -eq 0 -and $b -eq 1) { $start = $picks[$picks.Count - 1] } else { $start = $picks[0] }
      if ($start -eq $picks[$a] -or $start -eq $picks[$b]) { continue }
      $i++
      $body = [ordered]@{ mapId = $MapId; startStationId = $start; endStationIds = @($picks[$a], $picks[$b]) }
      Invoke-Recorded -Name ('near-end-pair-{0:d2}' -f $i) -Method POST `
        -PathAndQuery '/api/task/v1/route/queryNearEnd' -Body $body | Out-Null
    }
  }
}

# ==================== SECTION TWO: one vehicle, opportunistic ================

$skipReason = $null
if ($SkipVehicleSection) {
  $skipReason = 'skipped by -SkipVehicleSection'
} elseif ([string]::IsNullOrWhiteSpace($VehicleKey)) {
  $skipReason = 'no -VehicleKey given'
}

if ($null -eq $skipReason -and $picks.Count -lt 2) {
  $skipReason = 'no control-set stations were picked; nothing to compare against'
}

if ($null -eq $skipReason) {
  $snapshot = Invoke-Recorded -Name 'vehicle-snapshot' -Method GET `
    -PathAndQuery "/api/task/v1/task/getVehicleInfo/$VehicleKey"
  $vehicle = $snapshot.response.parsed.result
  if ($null -eq $vehicle) {
    $skipReason = 'vehicle snapshot unavailable'
  } elseif ([string]$vehicle.procState -eq 'PROCESSING_ORDER') {
    $skipReason = 'vehicle is executing an order; not disturbing it'
  } else {
    $stationNo = $vehicle.previousState.stationNo
    if ($null -eq $stationNo -or [int]$stationNo -eq 0) {
      $skipReason = 'vehicle not docked at a station (stationNo=0 means no station, not station zero)'
    }
  }
}

if ($null -ne $skipReason) {
  Save-Json '900-route-cost-skipped.json' ([ordered]@{
      at     = [DateTimeOffset]::Now.ToString('o')
      reason = $skipReason
      note   = 'Dimensional comparison is NOT proven this round. Do not substitute Round 16 numbers: those came from a different RIoT (172.10.1.72, map28).'
    })
  Write-Host "[skip] getRouteCostsBy control set: $skipReason"
} else {
  foreach ($target in $picks) {
    $body = [ordered]@{ mapId = $MapId; stationId = $target; deviceKeys = @($VehicleKey) }
    Invoke-Recorded -Name ('route-cost-station-{0}' -f $target) -Method POST `
      -PathAndQuery '/api/task/v1/route/getRouteCostsBy' -Body $body | Out-Null
  }
}

# ================================ summary ====================================

$edgeResult = $edges.response.parsed.result
Save-Json '999-summary.json' ([ordered]@{
    at             = [DateTimeOffset]::Now.ToString('o')
    baseUrl        = $baseUrl
    mapId          = $MapId
    requests       = $script:step
    edgeCount      = if ($edgeResult -is [array]) { $edgeResult.Count } else { $null }
    stationIdCount = $stationIds.Count
    routeCostSkip  = $skipReason
    note           = 'Shortest-path reproduction is offline; see round-plan.md decision thresholds.'
  })

$client.Dispose()
Write-Host ''
Write-Host "Round 43 collection finished. $($script:step) requests. Evidence in: $outDir"
Write-Host 'Next: offline shortest-path reproduction against the queryNearEnd answers, then write execution-log.md.'
