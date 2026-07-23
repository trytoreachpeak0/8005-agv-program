$ErrorActionPreference = "Stop"
$roundDir = $PSScriptRoot
$labRoot = (Resolve-Path (Join-Path $roundDir "..\..\..")).Path
$e = Get-Content -LiteralPath (Join-Path $labRoot "environment.local.json") -Raw -Encoding UTF8 | ConvertFrom-Json
$outDir = Join-Path $roundDir "runs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
Add-Type -AssemblyName System.Net.Http
$c = [System.Net.Http.HttpClient]::new()
$key = $e.testVehicleKey
$map28 = 28
$map28Name = "新基测试2opt"
Write-Host "labRoot=$labRoot map=$map28Name($map28)"

function Invoke-Api([string]$method,[string]$url,[string]$json){
  $r=New-Object System.Net.Http.HttpRequestMessage
  $r.Method=[System.Net.Http.HttpMethod]::new($method)
  $r.RequestUri=$url
  [void]$r.Headers.TryAddWithoutValidation("Authorization","Bearer $($e.callApiKey)")
  if(-not [string]::IsNullOrEmpty($json)){ $r.Content=New-Object System.Net.Http.StringContent($json,[System.Text.Encoding]::UTF8,"application/json") }
  $resp=$c.SendAsync($r).GetAwaiter().GetResult()
  $body=[System.Text.Encoding]::UTF8.GetString($resp.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult())
  $parsed=$null; try{ $parsed=$body|ConvertFrom-Json }catch{}
  [pscustomobject]@{status=[int]$resp.StatusCode;body=$body;parsed=$parsed;url=$url;method=$method}
}
function Save($n,$o){ [System.IO.File]::WriteAllText((Join-Path $outDir $n), ($o|ConvertTo-Json -Depth 24), $utf8) }
function CodeOk($p){ return ($p -and ($p.code -eq '0' -or $p.code -eq 0)) }
function Preview($body,[int]$n=4000){
  if([string]::IsNullOrEmpty($body)){ return $body }
  if($body.Length -le $n){ return $body }
  return $body.Substring(0,$n) + "...(truncated)"
}
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
function Cancel-Order([string]$oid,$nid,[string]$reason){
  if($oid){
    return (Invoke-Api POST "$($e.baseUrl)/api/task/v1/order/command/$oid" "{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}")
  }
  if($nid){
    return (Invoke-Api POST "$($e.baseUrl)/api/order/v1/operate" "{`"orderId`":$nid,`"orderCommandDTO`":{`"commandType`":`"CMD_ORDER_CANCEL`",`"disableVehicle`":false,`"reason`":`"$reason`"}}")
  }
}

# ========== E0 ==========
"=== E0 BASELINE + stations/28 ==="
$base=Get-Snap $null
Save 'E0-baseline.json' $base
$st=Invoke-Api GET "$($e.baseUrl)/api/imap/v1/mapInfo/stations/$map28" $null
$stations=@()
if($st.parsed.result){
  foreach($s in $st.parsed.result){ $stations += [ordered]@{id=$s.id; name=$s.name; type=$s.type} }
}
Save 'E0-stations-28.json' ([ordered]@{code=$st.parsed.code; count=$stations.Count; stations=$stations; preview=(Preview $st.body 1500)})
Write-Host ("vehicle mapName={0} station={1} stations28={2}" -f $base.mapName,$base.station,$stations.Count)
$sampleIds = @()
foreach($id in @(1,2,3,4,5,6,7,8,10,15,20,28,33)){
  if($stations | Where-Object { $_.id -eq $id }){ $sampleIds += $id }
}
if($sampleIds.Count -lt 3 -and $stations.Count -ge 3){
  $sampleIds = @($stations[0].id, $stations[1].id, $stations[2].id)
}
Write-Host ("sample station ids: " + ($sampleIds -join ','))

# ========== R1 GET ==========
"=== R1 GET route / getCostUnit ==="
$rRoot=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/" $null
$rootKeys=@()
$rootCount=0
if($rRoot.parsed.result){
  $rootCount = @($rRoot.parsed.result.PSObject.Properties).Count
  foreach($p in @($rRoot.parsed.result.PSObject.Properties) | Select-Object -First 30){
    $rootKeys += [ordered]@{key=$p.Name; value=$p.Value}
  }
}
Save 'R1-route-root.json' ([ordered]@{
  url=$rRoot.url; status=$rRoot.status; code=$rRoot.parsed.code; message=$rRoot.parsed.message
  resultEntryCount=$rootCount; sampleEntries=$rootKeys; bodyPreview=(Preview $rRoot.body 5000)
})
Write-Host ("GET /route/ code={0} entries={1}" -f $rRoot.parsed.code,$rootCount)

$rUnit=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/getCostUnit" $null
$unitSummary=[ordered]@{mapCount=0; samples=@()}
if($rUnit.parsed.result){
  $maps=@($rUnit.parsed.result.PSObject.Properties)
  $unitSummary.mapCount=$maps.Count
  foreach($m in $maps | Select-Object -First 5){
    $inner=@($m.Value.PSObject.Properties)
    $unitSummary.samples += [ordered]@{
      mapKey=$m.Name
      edgeOrKeyCount=$inner.Count
      firstInnerKeys=@($inner | Select-Object -First 5 | ForEach-Object { $_.Name })
    }
  }
}
Save 'R1-getCostUnit.json' ([ordered]@{
  url=$rUnit.url; status=$rUnit.status; code=$rUnit.parsed.code; message=$rUnit.parsed.message
  summary=$unitSummary; bodyPreview=(Preview $rUnit.body 6000)
})
Write-Host ("GET getCostUnit code={0} mapKeys={1}" -f $rUnit.parsed.code,$unitSummary.mapCount)

# ========== R2 getRouteCostsBy ==========
"=== R2 getRouteCostsBy ==="
$costRuns=@()
foreach($sid in $sampleIds){
  $bodyObj=@{ mapId=$map28; stationId=$sid; deviceKeys=@($key) }
  $json=$bodyObj | ConvertTo-Json -Compress
  $r=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json
  $list=@()
  if($r.parsed.result -and $r.parsed.result.deviceCostsList){
    foreach($d in $r.parsed.result.deviceCostsList){
      $list += [ordered]@{deviceKey=$d.deviceKey; costs=$d.costs; message=$d.message}
    }
  }
  $costRuns += [ordered]@{
    req=$bodyObj; status=$r.status; code=$r.parsed.code; message=$r.parsed.message
    resultMapId=$r.parsed.result.mapId; resultStationId=$r.parsed.result.stationId
    deviceCosts=$list; bodyPreview=(Preview $r.body 2000)
  }
  Write-Host ("costs map28 st={0} -> {1}" -f $sid, (($list | ForEach-Object { "{0}:{1}" -f $_.costs,$_.message }) -join ';'))
}
#对照：当前图 map29 若车在 api测试
$ctrlMap = if($base.mapName -eq 'api测试'){29} else {$null}
if($ctrlMap){
  $json29 = (@{ mapId=$ctrlMap; stationId=1; deviceKeys=@($key) } | ConvertTo-Json -Compress)
  $r29=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $json29
  $list29=@()
  if($r29.parsed.result -and $r29.parsed.result.deviceCostsList){
    foreach($d in $r29.parsed.result.deviceCostsList){ $list29 += [ordered]@{deviceKey=$d.deviceKey; costs=$d.costs; message=$d.message} }
  }
  $costRuns += [ordered]@{
    tag='control-current-map'; req=(@{mapId=$ctrlMap;stationId=1;deviceKeys=@($key)}); status=$r29.status
    code=$r29.parsed.code; message=$r29.parsed.message; deviceCosts=$list29; bodyPreview=(Preview $r29.body 2000)
  }
  Write-Host ("costs control map{0} st=1 -> {1}" -f $ctrlMap, (($list29 | ForEach-Object { "{0}:{1}" -f $_.costs,$_.message }) -join ';'))
}
# 反例：非法站 / 空 deviceKeys
$neg=@()
$negBody1=(@{ mapId=$map28; stationId=999999; deviceKeys=@($key) } | ConvertTo-Json -Compress)
$rn1=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $negBody1
$neg += [ordered]@{case='bad-station'; req=$negBody1; code=$rn1.parsed.code; message=$rn1.parsed.message; bodyPreview=(Preview $rn1.body 1500)}
$negBody2=(@{ mapId=$map28; stationId=1; deviceKeys=@('BROKERX-DOES-NOT-EXIST-R15') } | ConvertTo-Json -Compress)
$rn2=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/getRouteCostsBy" $negBody2
$neg += [ordered]@{case='fake-device'; req=$negBody2; code=$rn2.parsed.code; message=$rn2.parsed.message; bodyPreview=(Preview $rn2.body 1500)}
Save 'R2-getRouteCostsBy.json' ([ordered]@{runs=$costRuns; negatives=$neg})

# ========== R3 queryNearEnd / queryNearestStart ==========
"=== R3 queryNearEnd / queryNearestStart ==="
$startId = $sampleIds[0]
$endCandidates = @($sampleIds | Select-Object -Skip 1)
if($endCandidates.Count -lt 2){ $endCandidates = @($stations | Select-Object -First 5 | ForEach-Object { $_.id }) }

$nearEndReq=@{ mapId=$map28; startStationId=$startId; endStationIds=$endCandidates }
$nearEndJson=$nearEndReq | ConvertTo-Json -Compress
$rne=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/queryNearEnd" $nearEndJson
Save 'R3-queryNearEnd.json' ([ordered]@{
  req=$nearEndReq; status=$rne.status; code=$rne.parsed.code; message=$rne.parsed.message
  result=$rne.parsed.result; bodyPreview=(Preview $rne.body 2000)
})
Write-Host ("queryNearEnd start={0} candidates=[{1}] -> result={2} code={3}" -f $startId,($endCandidates -join ','),$rne.parsed.result,$rne.parsed.code)

$endId = if($sampleIds.Count -gt 1){$sampleIds[-1]} else {$sampleIds[0]}
$startCandidates = @($sampleIds | Select-Object -First ([Math]::Max(1,$sampleIds.Count-1)))
$nearStartReq=@{ mapId=$map28; endStationId=$endId; startStationIds=$startCandidates }
$nearStartJson=$nearStartReq | ConvertTo-Json -Compress
$rns=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/queryNearestStart" $nearStartJson
Save 'R3-queryNearestStart.json' ([ordered]@{
  req=$nearStartReq; status=$rns.status; code=$rns.parsed.code; message=$rns.parsed.message
  result=$rns.parsed.result; bodyPreview=(Preview $rns.body 2000)
})
Write-Host ("queryNearestStart end={0} candidates=[{1}] -> result={2} code={3}" -f $endId,($startCandidates -join ','),$rns.parsed.result,$rns.parsed.code)

# 反例：空候选 / 非法 map
$nearNeg=@()
$nb1=(@{ mapId=$map28; startStationId=$startId; endStationIds=@() } | ConvertTo-Json -Compress)
$n1=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/queryNearEnd" $nb1
$nearNeg += [ordered]@{case='nearEnd-empty'; code=$n1.parsed.code; message=$n1.parsed.message; result=$n1.parsed.result; body=(Preview $n1.body 800)}
$nb2=(@{ mapId=999999; startStationId=1; endStationIds=@(2,3) } | ConvertTo-Json -Compress)
$n2=Invoke-Api POST "$($e.baseUrl)/api/task/v1/route/queryNearEnd" $nb2
$nearNeg += [ordered]@{case='nearEnd-badmap'; code=$n2.parsed.code; message=$n2.parsed.message; result=$n2.parsed.result; body=(Preview $n2.body 800)}
Save 'R3-near-negatives.json' $nearNeg

# ========== R4 curRemainCost ==========
"=== R4 curRemainCost ==="
$remain=@()
$bad=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/curRemainCost/order-DOES-NOT-EXIST-R15" $null
$remain += [ordered]@{case='fake-order'; code=$bad.parsed.code; message=$bad.parsed.message; result=$bad.parsed.result; body=(Preview $bad.body 800)}

# 若空闲且在当前图可建单，用当前图短距观测 remain（非 map28 物理移动）
$didOrder=$false
$snapNow=Get-Snap $null
if($snapNow.procState -eq 'IDLE' -and -not $snapNow.processingOrder -and $snapNow.enable -eq $true -and $snapNow.integrationLevel -eq 'ON_LINE'){
  $curMapId = if($snapNow.mapName -eq 'api测试'){29} elseif($snapNow.mapName -eq $map28Name){$map28} else {$null}
  $dest = $null
  if($curMapId -eq 29){
    $dest = if($snapNow.station -eq 1){2} elseif($snapNow.station -eq 2){1} else {2}
  } elseif($curMapId -eq $map28 -and $sampleIds.Count -ge 2){
    $dest = if($snapNow.station -eq $sampleIds[0]){$sampleIds[1]} else {$sampleIds[0]}
  }
  if($curMapId -and $dest){
    $ts=Get-Date -Format 'yyyyMMdd-HHmmss'
    $uid="riot-behavior-lab-R15-remain-$ts"
    $createJson="{`"appointVehicleKey`":`"$key`",`"isAppointEnable`":1,`"lockStatus`":0,`"orderName`":`"$uid`",`"upperId`":`"$uid`",`"mission`":[{`"type`":`"move`",`"mapId`":$curMapId,`"destination`":$dest}]}"
    $cr=Invoke-Api POST "$($e.baseUrl)/api/order/v1/add/byDefaultMissions" $createJson
    Save 'R4-create-for-remain.json' ([ordered]@{uid=$uid; mapId=$curMapId; dest=$dest; createCode=$cr.parsed.code; createBody=(Preview $cr.body 2000)})
    if(CodeOk $cr.parsed){
      $didOrder=$true
      $deadline=(Get-Date).AddSeconds(60)
      $samples=@()
      while((Get-Date) -lt $deadline){
        Start-Sleep -Milliseconds 800
        $s=Get-Snap $uid
        if($s.orderId){
          $rem=Invoke-Api GET "$($e.baseUrl)/api/task/v1/route/curRemainCost/$($s.orderId)" $null
          $samples += [ordered]@{
            at=$s.at; orderState=$s.orderState; station=$s.station; movementState=$s.movementState; procState=$s.procState
            remainCode=$rem.parsed.code; remainResult=$rem.parsed.result; remainMsg=$rem.parsed.message
          }
          if($s.orderState -eq 3 -and $samples.Count -ge 3){ break }
          if($s.orderState -in @(2,4,5,6) -and $samples.Count -ge 1){ break }
        }
      }
      Save 'R4-curRemainCost-samples.json' $samples
      $last=$samples[-1]
      if($last -and $s.orderState -in @(1,3,7)){
        $cancel=Cancel-Order $s.orderId $s.numericId 'R15-remain-cleanup'
        Save 'R4-cleanup.json' ([ordered]@{before=$s; cancelCode=$cancel.parsed.code; cancelBody=(Preview $cancel.body 800); after=(Get-Snap $uid)})
      }
      Write-Host ("curRemainCost samples={0} lastRemain={1}" -f $samples.Count, $last.remainResult)
    }
  } else {
    Write-Host "skip create for remain: cannot resolve current map/dest"
  }
} else {
  Write-Host ("skip create for remain: proc={0} enable={1} il={2}" -f $snapNow.procState,$snapNow.enable,$snapNow.integrationLevel)
}
Save 'R4-curRemainCost-fake.json' $remain

# ========== summary ==========
$final=Get-Snap $null
Save 'E9-final.json' $final
Write-Host ("DONE final proc={0} map={1} station={2} didOrder={3}" -f $final.procState,$final.mapName,$final.station,$didOrder)
$c.Dispose()
