$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$c = [System.Net.Http.HttpClient]::new()
$key = $e.testVehicleKey

function Invoke-Api([string]$method,[string]$url,[string]$json){
  $r=New-Object System.Net.Http.HttpRequestMessage
  $r.Method=[System.Net.Http.HttpMethod]::new($method)
  $r.RequestUri=$url
  [void]$r.Headers.TryAddWithoutValidation("Authorization","Bearer $($e.callApiKey)")
  if(-not [string]::IsNullOrEmpty($json)){ $r.Content=New-Object System.Net.Http.StringContent($json,[System.Text.Encoding]::UTF8,"application/json") }
  $resp=$c.SendAsync($r).GetAwaiter().GetResult()
  $body=[System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
  $parsed=$null; try{ $parsed=$body|ConvertFrom-Json }catch{}
  [pscustomobject]@{status=[int]$resp.StatusCode;body=$body;parsed=$parsed;url=$url}
}
function Save($n,$o){ [System.IO.File]::WriteAllText((Join-Path $outDir $n), ($o|ConvertTo-Json -Depth 24), $utf8) }
function Preview($body,[int]$n=3000){ if($body.Length -le $n){$body}else{$body.Substring(0,$n)+'...(truncated)'} }
function Get-Snap([string]$upperId){
  $gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo
  $det=$null
  if($upperId){
    $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$upperId" $null
    $det=$by.parsed.result
  }
  [ordered]@{
    at=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss.fff')
    station=$v.currentStation; noStation=$v.noStation
    mapName=$(if($v.previousState){$v.previousState.mapName}else{$null})
    procState=$vti.procState; processingOrder=$vti.processingOrder
    movementState=[string]$v.movementState
    enable=$vti.enable; integrationLevel=[string]$vti.integrationLevel
    orderState=$(if($det){$det.orderState}else{$null})
    orderId=$(if($det){$det.orderId}else{$null})
    numericId=$(if($det){$det.id}else{$null})
    upperId=$(if($det){$det.upperId}else{$upperId})
  }
}

"=== R2b control map29 costs ==="
$s0=Get-Snap $null
Save 'R2b-baseline.json' $s0
$ctrl=@()
foreach($sid in @(1,2)){
  $json=(@{mapId=29; stationId=$sid; deviceKeys=@($key)} | ConvertTo-Json -Compress)
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
  $list=@()
  if($r.parsed.result.deviceCostsList){
    foreach($d in $r.parsed.result.deviceCostsList){ $list += [ordered]@{deviceKey=$d.deviceKey; costs=$d.costs; message=$d.message} }
  }
  $ctrl += [ordered]@{req=@{mapId=29;stationId=$sid}; code=$r.parsed.code; deviceCosts=$list; body=(Preview $r.body)}
  Write-Host ("map29 st={0} -> {1}" -f $sid, (($list|%{ "$($_.costs):$($_.message)" }) -join ';'))
}
Save 'R2b-map29-costs.json' $ctrl

"=== R4b curRemainCost with short order on map29 ==="
# ensure online
if(-not ($s0.enable -eq $true -and $s0.integrationLevel -eq 'ON_LINE')){
  $en=Invoke-Api POST "$($e.baseUrl)/api/task/vehicles/updateVehicleIntegrationLevel" "{`"deviceKeys`":[`"$key`"],`"serviceId`":`"enable`"}"
  Save 'R4b-enable.json' ([ordered]@{code=$en.parsed.code; body=(Preview $en.body); after=(Get-Snap $null)})
  Start-Sleep -Seconds 1
}
$s1=Get-Snap $null
$dest = if($s1.station -eq 1){2} elseif($s1.station -eq 2){1} else {2}
$ts=Get-Date -Format 'yyyyMMdd-HHmmss'
$uid="riot-behavior-lab-R15-remain-$ts"
$createJson="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":29,`"destination`":$dest}]}"
$cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $createJson
Save 'R4b-create.json' ([ordered]@{uid=$uid; dest=$dest; code=$cr.parsed.code; body=(Preview $cr.body)})
Write-Host ("create code={0} dest={1}" -f $cr.parsed.code,$dest)

$samples=@()
$deadline=(Get-Date).AddSeconds(75)
$oid=$null; $nid=$null
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 700
  $s=Get-Snap $uid
  if($s.orderId){ $oid=$s.orderId; $nid=$s.numericId }
  if($oid){
    $rem=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/curRemainCost/$oid" $null
    $samples += [ordered]@{
      at=$s.at; orderState=$s.orderState; station=$s.station; movementState=$s.movementState; procState=$s.procState
      remainCode=$rem.parsed.code; remainResult=$rem.parsed.result; remainMsg=$rem.parsed.message; remainBody=(Preview $rem.body 500)
    }
    if($s.orderState -eq 3 -and $samples.Count -ge 5){ break }
    if($s.orderState -in @(2,4,5,6)){ break }
  }
}
Save 'R4b-curRemainCost-samples.json' $samples
Write-Host ("remain samples={0}" -f $samples.Count)
if($samples.Count -gt 0){
  $samples | Select-Object -First 8 | ForEach-Object {
    Write-Host ("  state={0} move={1} remain={2} code={3}" -f $_.orderState,$_.movementState,$_.remainResult,$_.remainCode)
  }
}

# cleanup cancel if still active
$s2=Get-Snap $uid
if($s2.orderState -in @(1,3,7,9)){
  $cancel=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$($s2.orderId)" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"R15-R4b-cleanup`"}"
  Save 'R4b-cleanup.json' ([ordered]@{before=$s2; cancelCode=$cancel.parsed.code; after=(Get-Snap $uid)})
  Write-Host ("cleanup cancel code={0}" -f $cancel.parsed.code)
} else {
  Save 'R4b-final-order.json' $s2
}
Save 'R4b-final-vehicle.json' (Get-Snap $null)
$c.Dispose()
Write-Host DONE
