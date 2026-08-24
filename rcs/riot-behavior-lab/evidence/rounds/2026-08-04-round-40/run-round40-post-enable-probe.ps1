$ErrorActionPreference = 'Stop'
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir '..\..\..')).Path
$config = Get-Content -LiteralPath (Join-Path $labRoot 'environment.local.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$sourceSummary = Get-Content -LiteralPath (Join-Path $roundDir 'runs-attempt-3\999-summary.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir 'runs-attempt-3-post-enable'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
$expectedVehicleName = -join ([char[]]@(0x65B0,0x57FA,0x6D4B,0x8BD5,0x0033,0x0030,0x0030,0x0063,0x534F,0x4F5C,0x0031))
$key = [string]$config.testVehicleKey

Add-Type -AssemblyName System.Net.Http
$client = [System.Net.Http.HttpClient]::new()
$client.Timeout = [TimeSpan]::FromSeconds(20)
$sequence = 0

function Save-Json([string]$name, $value) {
  [System.IO.File]::WriteAllText((Join-Path $outDir $name), (ConvertTo-Json -InputObject $value -Depth 30), $utf8)
}

function Invoke-Get([string]$label, [string]$path) {
  $script:sequence++
  $url = "$($config.baseUrl)$path"
  $request = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::Get, $url)
  [void]$request.Headers.TryAddWithoutValidation('Authorization', "Bearer $($config.callApiKey)")
  try {
    $started = [DateTimeOffset]::Now
    $response = $client.SendAsync($request).GetAwaiter().GetResult()
    $body = [System.Text.Encoding]::UTF8.GetString($response.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
    foreach ($secret in @([string]$config.callApiKey, [string]$config.password)) {
      if (-not [string]::IsNullOrWhiteSpace($secret)) { $body = $body.Replace($secret, '<redacted>') }
    }
    $parsed = $null
    try { $parsed = $body | ConvertFrom-Json } catch {}
    $record = [ordered]@{
      at=$started.ToString('o')
      request=[ordered]@{method='GET';url=$url;headers=[ordered]@{Authorization='<redacted>'}}
      response=[ordered]@{httpStatus=[int]$response.StatusCode;body=$body;parsed=$parsed}
    }
    Save-Json ('{0:D3}-{1}.json' -f $script:sequence,$label) $record
    return $record
  } finally { $request.Dispose() }
}

if ([string]$config.testVehicleName -cne $expectedVehicleName) { throw 'Configured vehicle identity mismatch' }
$before = Invoke-Get 'before-vehicle' "/api/task/v1/task/getVehicleInfo/$key"
$v = $before.response.parsed.vehicle
$vti = $before.response.parsed.vehicleTaskInfo
if ([string]$v.name -cne $expectedVehicleName -or [string]$vti.procState -ne 'IDLE' -or [string]$vti.integrationLevel -ne 'ON_LINE' -or -not [bool]$vti.enable -or [string]$v.emergencyState -ne 'OK') {
  throw 'Vehicle is not in safe restored state'
}

$order = $sourceSummary.scenarios[0].order
$cases = @(
  [ordered]@{kind='orderId';value=[string]$order.orderId},
  [ordered]@{kind='numericId';value=[string]$order.numericId},
  [ordered]@{kind='upperId';value=[string]$order.upperId},
  [ordered]@{kind='unknown';value='riot-behavior-lab-R40-S1-offline-order-does-not-exist'}
)
$results = @()
foreach ($case in $cases) {
  $record = Invoke-Get "diagnostic-$($case.kind)" "/api/task/vehicles/queryVehicleNotAssignOrder/$key/$([Uri]::EscapeDataString($case.value))"
  $p = $record.response.parsed
  $results += [ordered]@{kind=$case.kind;value=$case.value;httpStatus=$record.response.httpStatus;code=$p.code;reason=$p.result.reason;suggestList=@($p.result.suggestList)}
}
$after = Invoke-Get 'after-vehicle' "/api/task/v1/task/getVehicleInfo/$key"
$summary = [ordered]@{
  completedAt=[DateTimeOffset]::Now.ToString('o')
  before=[ordered]@{name=$v.name;procState=$vti.procState;integrationLevel=$vti.integrationLevel;enable=$vti.enable;emergencyState=$v.emergencyState}
  results=$results
  after=[ordered]@{name=$after.response.parsed.vehicle.name;procState=$after.response.parsed.vehicleTaskInfo.procState;integrationLevel=$after.response.parsed.vehicleTaskInfo.integrationLevel;enable=$after.response.parsed.vehicleTaskInfo.enable;emergencyState=$after.response.parsed.vehicle.emergencyState}
}
Save-Json '999-summary.json' $summary
$client.Dispose()
Write-Host 'Round40 post-enable read-only probe complete'
