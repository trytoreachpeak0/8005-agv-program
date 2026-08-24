# 最终批准 REQ-0193–REQ-0196：决定复合运输、分区与多 SUBLOT 组合边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-052
Approval payload SHA-256: b006e063eaf246b5c8cb1ab7161e955b372f26fd1836c8533abc0f8b2a31c10a
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-052` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0193 — 固定站点不得跨图。 FixedTaskStation 按 TASK_TYPE + mapId 配置；Dema…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0193`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 固定站点不得跨图。 FixedTaskStation 按 TASK_TYPE + mapId 配置；Demand 的 AREA 经分区确定 Map 后，另一端必须使用同一 Map 上的固定站点，禁止跨 Map 运输。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 23`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `bd4f6b1c15bb6819ba72bdc4fe8fc1730adbae45ac1fcb26ac3214a39af3c77a`。

### REQ-0194 — 分区车辆策略同时具有硬准入与软偏好。 DispatchZoneVehicleAdmission 定义允许服务…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0194`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 分区车辆策略同时具有硬准入与软偏好。 DispatchZoneVehicleAdmission 定义允许服务本区的车辆硬集合；DispatchZoneVehiclePreference 只在该集合内表达优先车辆和回退次序，不能扩大准入。只配置所需硬集合即可实现纯强制分区；无合格车辆时不得自动跨区借车。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 24`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `56da43726e7c46d7365a783f899370dee96c482d179d799e5288684b6b951c9c`。

### REQ-0195 — 同图跨区允许，但不得往返摆动。 一辆车同时获准多个同图分区时，可以在同一计划承载这些分区的 Demand，无…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0195`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 同图跨区允许，但不得往返摆动。 一辆车同时获准多个同图分区时，可以在同一计划承载这些分区的 Demand，无需分区配对表；各分区 Demand 必须形成连续区段，允许 A→A→B→B，禁止离开后再次返回的 A→B→A。精确路线成本、评分权重与饥饿避免由《决定派车评分、路网成本与无车响应升级规则》承接。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 25`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `9e8295647fe59e6292bddb22e727fd412f71628d628e2e1615a97e2d16e270c3`。

### REQ-0196 — 执行途中只允许受控追加。 新 TransportDemand 可以在车辆执行中经过完整准入后加入其后的未执行…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0196`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 执行途中只允许受控追加。 新 TransportDemand 可以在车辆执行中经过完整准入后加入其后的未执行停靠；车辆正在驶向的当前下一站是已承诺停靠，不得因新 Demand 改变。空仓或距离近只是候选事实，不能绕过 Map、分区、车辆任务类型、取货合法性、容量、取消、分区连续性和延迟门禁。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 26`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `19db7616154dcffa9b773c8714d8c71d6703ee32aad90ff7e5f307a8f16a1a31`。

## Required HITL resolution

- [ ] `REQ-0193`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0194`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0195`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0196`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0193`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0194`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0195`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0196`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-052`、Approval payload SHA-256 `b006e063eaf246b5c8cb1ab7161e955b372f26fd1836c8533abc0f8b2a31c10a`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
