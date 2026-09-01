[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$candidatePath = Join-Path $PSScriptRoot 'requirement-applicability-matrix.tsv'
$finalPath = Join-Path $PSScriptRoot 'final-requirement-applicability-profile.tsv'
$summaryPath = Join-Path $PSScriptRoot 'final-requirement-applicability-profile-summary.md'
$baselinePath = Join-Path $repoRoot 'requirements\baselines\current-requirements-v1.0.0.md'
$expectedBaselineSha = '5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba'

if ((Get-FileHash -LiteralPath $baselinePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedBaselineSha) {
    throw 'Baseline SHA-256 no longer matches the approved v1.0.0 identity.'
}

$overrides = @{
    'REQ-0069' = @('MVP 交互／安全依赖', 'MesIngest 数据卷低空间门禁决定目录是否仍可作为当前执行来源；MVP 不建设该监控面，但不得绕过其暂停结果。')
    'REQ-0070' = @('MVP 交互／安全依赖', 'StoragePressurePause 时执行承诺读取必须以 503 fail-closed；ControlServer 不得沿用旧目录受理 Demand。')
    'REQ-0071' = @('MVP 交互／安全依赖', '暂停恢复与 HistoryResetAcknowledgement 属 MesIngest 本地管理边界；MVP 只消费其受审计结果，不实现远程恢复旁路。')
    'REQ-0073' = @('MVP 交互／安全依赖', '重建产生新 HistoryEpoch 且未确认时禁止外部当前读取，是最终重读和跨纪元防重成立的上游门禁。')
    'REQ-0074' = @('MVP 直接必须', 'Demand 发现、最终重读、AcceptedDemandSnapshot 与重启对账都必须绑定 HistoryEpoch，旧纪元缓存和快照不得复用。')
    'REQ-0190' = @('MVP 直接必须', '指定 AGV 必须具有显式 (agvId, WIRE_TO_GATE) VehicleTaskTypeAdmission；未配置即拒绝，首期用受控预置配置。')
    'REQ-0194' = @('MVP 交互／安全依赖', 'DispatchZoneVehicleAdmission 硬集合直接保留；多车软偏好、回退次序和跨车策略不进入首期。')
    'REQ-0199' = @('MVP 交互／安全依赖', 'MVP 消费 Map→DispatchZone→AREA、任务类型白名单和分区硬准入的受控配置身份；评分、拓扑设计和配置 UI 延后。')
    'REQ-0205' = @('MVP 交互／安全依赖', '多车及在途追加竞争不适用，但不预绑忙车、共享 UnassignedDemandBacklog、持续老化和事实变化后重选必须保留。')
    'REQ-0236' = @('本场景不适用', '本条按 R-09/R-11/R-13 或逐人附加权限授权的模型不用于 MVP；REQ-0253 与票据 05 已改用两个管理员角色，现场资质仍单独强制。')
    'REQ-0251' = @('MVP 交互／安全依赖', 'SystemAdministrator 的角色身份、异常恢复资格和不得覆盖安全事实的边界适用；完整账号、配置、版本维护产品面首期延后。')
    'REQ-0252' = @('MVP 直接必须', '试运行和最小异常恢复至少需要一个不共享的个人管理员账号；一人一号、单活动会话和替换审计直接适用。')
    'REQ-0253' = @('MVP 直接必须', '最小 ExceptionRecoverySession 明确由 MaintenanceAdministrator 或 SystemAdministrator 以个人账号独立操作，普通操作员无权恢复。')
    'REQ-0254' = @('本场景不适用', '充不上现场确认、人工清桩和充电桩恢复属于自动充电/充电桩产品面；MVP 仅保留人工充电 Hold 与重新投运。')
    'REQ-0258' = @('MVP 交互／安全依赖', 'MVP 必须消费服务端发布的仓位模型/配置身份并禁止车载平行改业务模型；ConfigurationMaintenanceConsole 编辑、复制、提交和激活 UI 不进入首期。')
    'REQ-0276' = @('MVP 交互／安全依赖', '预建个人管理员账号仍须遵守已批准的基础密码有效性；可配置增强、找回和完整账号生命周期产品面延后。')
    'REQ-0278' = @('MVP 交互／安全依赖', '目标硬件操作和异常处置使用真实管理员登录，会话只能沿已批准明确边界结束；首期不另造自动超时语义。')
    'REQ-0279' = @('MVP 交互／安全依赖', '最小 ExceptionRecoverySession 必须跨短暂断线保留原人员、事件与范围并继续对账，不能因空闲超时释放安全阻断。')
    'REQ-0307' = @('MVP 交互／安全依赖', 'FactoryPilotConfigurationSnapshot、运行证据和活动 Demand 引用的 MapStationCatalogSnapshot 修订必须可追溯；完整长期清理管理面延后。')
}

$rows = @(Import-Csv -LiteralPath $candidatePath -Delimiter "`t")
if ($rows.Count -ne 348) { throw "Expected 348 candidate rows, got $($rows.Count)." }

$expectedIds = 1..348 | ForEach-Object { 'REQ-{0:D4}' -f $_ }
$actualIds = @($rows.RequirementId)
if ((Compare-Object $expectedIds $actualIds).Count -ne 0 -or ($actualIds | Select-Object -Unique).Count -ne 348) {
    throw 'Candidate IDs are not exactly REQ-0001 through REQ-0348 once each.'
}

$finalRows = foreach ($row in $rows) {
    $override = $overrides[$row.RequirementId]
    $classification = if ($null -ne $override) { $override[0] } else { $row.CandidateClassification }
    $reason = if ($null -ne $override) {
        $override[1]
    } else {
        "复核 02～11 票最终决议后保留候选结论：$($row.CandidateReason)"
    }

    [pscustomobject][ordered]@{
        RequirementId = $row.RequirementId
        Source = $row.Source
        Title = $row.Title
        OriginalScope = $row.OriginalScope
        CandidateClassification = $row.CandidateClassification
        FinalClassification = $classification
        FinalReason = $reason
        DependencyChain = $row.DependencyChain
        MisclassificationRisk = $row.MisclassificationRisk
        ControlServerImpact = $row.ControlServerImpact
        OnboardHmiImpact = $row.OnboardHmiImpact
        SharedProtocolImpact = $row.SharedProtocolImpact
        DecisionBasis = $row.PendingHitlDecision
    }
}

$allowed = @('MVP 直接必须', 'MVP 交互／安全依赖', '首期延后', '本场景不适用')
foreach ($row in $finalRows) {
    if ($row.FinalClassification -notin $allowed) { throw "Invalid classification for $($row.RequirementId)." }
}

$finalRows | Export-Csv -LiteralPath $finalPath -Delimiter "`t" -NoTypeInformation -Encoding utf8
$roundTrip = @(Import-Csv -LiteralPath $finalPath -Delimiter "`t")
if ($roundTrip.Count -ne 348 -or ($roundTrip.RequirementId | Select-Object -Unique).Count -ne 348) {
    throw 'Final TSV round-trip coverage check failed.'
}
foreach ($id in $expectedIds) {
    if (@($roundTrip | Where-Object RequirementId -eq $id).Count -ne 1) { throw "$id is not classified exactly once." }
}

function Compress-RequirementIds {
    param([string[]]$Ids)
    $numbers = @($Ids | ForEach-Object { [int]$_.Substring(4) } | Sort-Object)
    $parts = [System.Collections.Generic.List[string]]::new()
    if ($numbers.Count -eq 0) { return '' }
    $start = $numbers[0]
    $previous = $numbers[0]
    for ($index = 1; $index -le $numbers.Count; $index++) {
        $current = if ($index -lt $numbers.Count) { $numbers[$index] } else { $null }
        if ($null -ne $current -and $current -eq ($previous + 1)) {
            $previous = $current
            continue
        }
        if ($start -eq $previous) {
            $parts.Add(('REQ-{0:D4}' -f $start))
        } else {
            $parts.Add(('REQ-{0:D4}～REQ-{1:D4}' -f $start, $previous))
        }
        if ($null -ne $current) { $start = $current; $previous = $current }
    }
    return ($parts -join '、')
}

$counts = [ordered]@{}
$lists = [ordered]@{}
foreach ($classification in $allowed) {
    $ids = @($finalRows | Where-Object FinalClassification -eq $classification | Select-Object -ExpandProperty RequirementId)
    $counts[$classification] = $ids.Count
    $lists[$classification] = Compress-RequirementIds $ids
}
$tsvSha = (Get-FileHash -LiteralPath $finalPath -Algorithm SHA256).Hash.ToLowerInvariant()
$changed = @($finalRows | Where-Object { $_.CandidateClassification -ne $_.FinalClassification })

$summary = [System.Collections.Generic.List[string]]::new()
$summary.Add('# WIRE_TO_GATE MVP 最终需求适用性清单')
$summary.Add('')
$summary.Add("- Baseline: ``current-requirements-v1.0.0.md`` / SHA-256 ``$expectedBaselineSha``")
$summary.Add("- Final TSV: [final-requirement-applicability-profile.tsv](final-requirement-applicability-profile.tsv) / SHA-256 ``$tsvSha``")
$summary.Add('- Coverage: `REQ-0001`～`REQ-0348`，348 条，零遗漏、零重复、每条恰好一个最终分类。')
$summary.Add('- Approval basis: 依据用户对本 Wayfinder 后续各票采用推荐值的明确授权；只批准 MVP 实施适用性，不修改 v1.0.0 Lifecycle。')
$summary.Add('')
$summary.Add('## 四类精确清单')
$summary.Add('')
foreach ($classification in $allowed) {
    $summary.Add("### $classification（$($counts[$classification]) 条）")
    $summary.Add('')
    $summary.Add($lists[$classification])
    $summary.Add('')
}
$summary.Add('## 相对 01 票候选矩阵的分类调整')
$summary.Add('')
$summary.Add('| Requirement | 候选 | 最终 | 理由 |')
$summary.Add('| --- | --- | --- | --- |')
foreach ($row in $changed) {
    $safeReason = $row.FinalReason.Replace('|', '\|')
    $summary.Add("| $($row.RequirementId) | $($row.CandidateClassification) | $($row.FinalClassification) | $safeReason |")
}
$summary.Add('')
$summary.Add('## 分类语义与限界')
$summary.Add('')
$summary.Add('- `MVP 直接必须`：精确条目直接约束本场景实现或验收，不能以其它能力替代。')
$summary.Add('- `MVP 交互／安全依赖`：不要求首期重建条目全部产品面，但其中的来源事实、门禁、安全、恢复、身份或审计语义必须被消费或保留。')
$summary.Add('- `首期延后`：本场景首期不实现；原条目仍为 v1.0.0 active，不代表永久废弃。')
$summary.Add('- `本场景不适用`：对单车、单图、单 Demand、WIRE_TO_GATE 旅程不适用；不从已发布基线删除。')
$summary.Add('- 车载端开发同事对原型票的豁免不延伸到生产实现、ProtocolReleaseIdentity、G0～G3、现场试运行或最终交接批准。')
$summary.Add('- 本清单没有发布协议、运行门禁、取得真实凭证/物料/现场证据，也没有代替另一名开发者或第三方确认。')

Set-Content -LiteralPath $summaryPath -Value ($summary -join "`r`n") -Encoding utf8
Write-Output "Wrote $($finalRows.Count) rows; direct=$($counts['MVP 直接必须']), dependency=$($counts['MVP 交互／安全依赖']), deferred=$($counts['首期延后']), notApplicable=$($counts['本场景不适用']), changed=$($changed.Count)."
