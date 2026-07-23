$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$http = [System.Net.Http.HttpClient]::new()
$key = $e.testVehicleKey

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
function Save($n,$o){ [System.IO.File]::WriteAllText((Join-Path $outDir $n), ($o|ConvertTo-Json -Depth 20), $utf8) }

"=== R3b tighter near queries ==="
$cases=@(
  @{name='nearEnd-1to234'; body='{"mapId":28,"startStationId":1,"endStationIds":[2,3,4]}'},
  @{name='nearEnd-1to2vs33'; body='{"mapId":28,"startStationId":1,"endStationIds":[2,33]}'},
  @{name='nearEnd-1to2only'; body='{"mapId":28,"startStationId":1,"endStationIds":[2]}'},
  @{name='nearStart-4from123'; body='{"mapId":28,"endStationId":4,"startStationIds":[1,2,3]}'},
  @{name='nearStart-4from23'; body='{"mapId":28,"endStationId":4,"startStationIds":[2,3]}'}
)
$out=@()
foreach($cse in $cases){
  $api = if($cse.name -like 'nearEnd*'){ 'queryNearEnd' } else { 'queryNearestStart' }
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/$api" $cse.body
  $out += [ordered]@{name=$cse.name; api=$api; req=$cse.body; code=$r.parsed.code; result=$r.parsed.result; message=$r.parsed.message}
  Write-Host ("{0} -> {1} (code={2})" -f $cse.name,$r.parsed.result,$r.parsed.code)
}
Save 'R3b-near-tight.json' $out

"=== R4c try remain while EXECUTING ==="
$gi=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
$v=$gi.parsed.vehicle; $vti=$gi.parsed.vehicleTaskInfo
$base=[ordered]@{station=$v.currentStation; mapName=$v.previousState.mapName; proc=$vti.procState; enable=$vti.enable; il=[string]$vti.integrationLevel; move=[string]$v.movementState}
Save 'R4c-baseline.json' $base
Write-Host ("veh station={0} proc={1} il={2}" -f $base.station,$base.proc,$base.il)

$list=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord?pageNum=1&pageSize=50&filterByState=1&filterByState=3&filterByState=7&filterByState=9" $null
$cleared=@()
if($list.parsed.result.records){
  foreach($rec in $list.parsed.result.records){
    if($rec.appointVehicleKey -eq $key -or $rec.executeVehicleKey -eq $key){
      $cmd=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$($rec.orderId)" '{"commandType":"CMD_ORDER_CANCEL","disableVehicle":false,"reason":"R15-R4c-preclear"}'
      $cleared += [ordered]@{orderId=$rec.orderId; state=$rec.orderState; code=$cmd.parsed.code}
    }
  }
}
Save 'R4c-preclear.json' $cleared
Start-Sleep -Seconds 2

$dest=2
$ts=Get-Date -Format 'yyyyMMdd-HHmmss'
$uid="riot-behavior-lab-R15-remain2-$ts"
$json="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":29,`"destination`":$dest}]}"
$cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $json
Save 'R4c-create.json' ([ordered]@{uid=$uid; code=$cr.parsed.code; body=$cr.body.Substring(0,[Math]::Min(1500,$cr.body.Length))})
Write-Host ("create {0}" -f $cr.parsed.code)

$samples=@(); $oid=$null; $nid=$null; $lastState=$null
$deadline=(Get-Date).AddSeconds(90)
while((Get-Date) -lt $deadline){
  Start-Sleep -Milliseconds 600
  $by=Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null
  $det=$by.parsed.result
  $gi2=Invoke-Api GET "$($e.baseUrl)/api/task/v1/task/getVehicleInfo/$key" $null
  $v2=$gi2.parsed.vehicle; $vti2=$gi2.parsed.vehicleTaskInfo
  if($det){ $oid=$det.orderId; $nid=$det.id; $lastState=$det.orderState }
  $remainResult=$null; $remainCode=$null
  if($oid){
    $rem=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/curRemainCost/$oid" $null
    $remainResult=$rem.parsed.result; $remainCode=$rem.parsed.code
  }
  $row=[ordered]@{
    at=(Get-Date -Format 'HH:mm:ss.fff')
    orderState=$(if($det){$det.orderState}else{$null})
    execute=$(if($det){$det.executeVehicleKey}else{$null})
    station=$v2.currentStation; proc=$vti2.procState; move=[string]$v2.movementState
    remainCode=$remainCode; remain=$remainResult
  }
  $samples += $row
  Write-Host ("[{0}] order={1} exec={2} proc={3} move={4} remain={5}" -f $row.at,$row.orderState,$row.execute,$row.proc,$row.move,$row.remain)
  if($row.orderState -eq 3 -and ($samples | Where-Object { $_.orderState -eq 3 }).Count -ge 6){ break }
  if($row.orderState -in @(2,4,5,6)){ break }
}
Save 'R4c-samples.json' $samples

if($oid){
  $det2=(Invoke-Api GET "$($e.baseUrl)/api/order/v1/orderRecord/detailByUpperId/$uid" $null).parsed.result
  if($det2 -and $det2.orderState -in @(1,3,7,9)){
    $cancel=Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" '{"commandType":"CMD_ORDER_CANCEL","disableVehicle":false,"reason":"R15-R4c-cleanup"}'
    Start-Sleep -Seconds 2
    Save 'R4c-cleanup.json' ([ordered]@{beforeState=$det2.orderState; code=$cancel.parsed.code; message=$cancel.parsed.message})
    Write-Host ("cleanup code={0}" -f $cancel.parsed.code)
  } else {
    Save 'R4c-final-order.json' $det2
  }
}
Save 'R4c-final-vehicle.json' (Get-Snap $null)
$c.Dispose()
Write-Host DONE
