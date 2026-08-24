# 最终批准 REQ-0204–REQ-0207：决定派车评分、路网成本与无车响应升级规则

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-055
Approval payload SHA-256: 851bd4e0a1d215a43ca21c674912ad8fbe2d6d97ff1998b28919832c37904a46
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-055` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0204 — 固定公共站点维持单点与单车位边界。 每张 Map 的每种 PublicStationFunction 只配置…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0204`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 固定公共站点维持单点与单车位边界。 每张 Map 的每种 PublicStationFunction 只配置一个 FixedTaskStation；一个站点同时只能由一台已到达车辆占用或由一台已承诺前往的车辆预占，其他车辆不得承接下一站为该点的新任务。若货物实际取货起点就是该公共站点，已经在点且通过全部硬准入的车辆取得一个选车软层；公共点只是任务终点时不适用，该车不合格时自然比较其他车辆。货物不会因车辆位置改变取货点。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 23`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `01a44d21304392245016377fd8067b148ffea39fc61f4462b7d9604c7a64d0fe`。

### REQ-0205 — 空闲车与可合法追加的在途车共同竞争。 在途车辆只有通过容量、Map、分区连续性、VehicleTaskTyp…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0205`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 空闲车与可合法追加的在途车共同竞争。 在途车辆只有通过容量、Map、分区连续性、VehicleTaskTypeAdmission、EnRoutePickupDeliveryDelay 和其它全部追加门禁时才能参加；空闲或在途身份本身不产生优先级。当前不能合法承接或追加时，不给忙车预绑定或建立专属队列，任务留在 UnassignedDemandBacklog 持续老化，任一车辆状态或容量变化后重新执行任务优先选择。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 24`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `66f44dce3e6f3faba56bf0af8c4636486348df3da902dc85e4049e47d943a5c0`。

### REQ-0206 — 车辆主要按新增行程成本比较。 VehicleMarginalRouteCost 表示加入已选任务相对车辆原计…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0206`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 车辆主要按新增行程成本比较。 VehicleMarginalRouteCost 表示加入已选任务相对车辆原计划增加的预计行程代价；公共取货点在点软层之后，明显更低的新增成本优先。同一 DispatchZone 可现场批准 RouteCostEquivalenceBand；带内先比较 DispatchZoneVehiclePreference，再选择从未成功接单或距离上次成功接单时间最久的车辆，最后才以预计任务后剩余电量较高者裁决。未批准非零容差时采用零容差，不阻断派车，只有成本完全相同才进入后续层。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 25`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `603cae6f86c6322f4bc19d93a238e8f312cdd418e7a8e0011ea063023712964d`。

### REQ-0207 — 路径证据区分可达性与排序成本。 无法确认车辆到下一站可达时，该车退出本轮候选，禁止用直线距离或其它弱替代证明…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0207`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 路径证据区分可达性与排序成本。 无法确认车辆到下一站可达时，该车退出本轮候选，禁止用直线距离或其它弱替代证明可达；可达性已经确认，但本轮候选的新增行程成本缺失、过期或不可比较时，保留相关车辆、对该比较组跳过路径成本层并记录原因，继续比较后续层。任何弱替代值都不得冒充 RIoT RouteCost；该分支只用于少见的异常边界，不作为常态运行方式。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 26`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `d4a6f9aebec7d1bc68174a794407b84622e93e7f0164f074608808d1270cb441`。

## Required HITL resolution

- [ ] `REQ-0204`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0205`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0206`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0207`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0204`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0205`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0206`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0207`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-055`、Approval payload SHA-256 `851bd4e0a1d215a43ca21c674912ad8fbe2d6d97ff1998b28919832c37904a46`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
