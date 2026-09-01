# 最终批准 REQ-0189–REQ-0192：决定复合运输、分区与多 SUBLOT 组合边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-051
Approval payload SHA-256: 5b69f3c7cdcc84a87aa661380e3933ab338f01d80a8446074d4415cec69bd4a6
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-051` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0189 — 多 Sublot 不合并 Demand。 一辆 AGV 可以同时承载多个 Sublot 和多个独立 Tran…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0189`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 多 Sublot 不合并 Demand。 一辆 AGV 可以同时承载多个 Sublot 和多个独立 TransportDemand；每个 Demand 保留自身任务类型、起终点、状态、取消、仓位和审计边界。同一 Sublot 同一时刻只能对应一种任务类型；同一完整 MES 快照中同时命中多种任务类型属于 SublotTaskTypeConflict，该 Sublot 的全部候选均阻断，不建立“上下游正常并存或等待”状态。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 19`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `1f2a19d8014461671dab4dbf2e9191856bb01a488d72da0c93006eaee85fbba3`。

### REQ-0190 — 车辆任务类型采用默认拒绝的白名单。 VehicleTaskTypeAdmission 以 agvId + t…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0190`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 车辆任务类型采用默认拒绝的白名单。 VehicleTaskTypeAdmission 以 agvId + taskType 明确车辆可承载的任务类型；未配置即不进入候选。车辆获准的多个类型可以同时承载，不再维护任务类型两两配对表；具体 DemandId 仍由调度分配，不写入长期准入配置。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 20`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `543d858df98c72f84c8a8e4dc8d3668db140220f5bd586664322fc79fdc1f9ee`。

### REQ-0191 — Map、DispatchZone 与 AREA 形成单一正向执行链。 每个 DispatchZone 只归属…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0191`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Map、DispatchZone 与 AREA 形成单一正向执行链。 每个 DispatchZone 只归属一个以 mapId 标识的 RIoT Map；每个有效 DispatchZoneAreaAssignment 把一个 MES AREA 归入一个分区。该映射同时是唯一 AREA 执行白名单：未映射 AREA 的 TransportDemand 仍保留在全厂投影中，但在选任务时静默跳过、不执行也不报警。原 OldFactoryExecutionAreaRegistry 与 TransportExecutionExcludedArea 均并入本映射；共晶、低温共晶等不执行 AREA 通过不配置映射表达。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 21`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `a65946be1f447736ecbdd00244dd935517ff203339289d38f61134c6b91bee19`。

### REQ-0192 — 车辆必须实际位于任务所属 Map。 Demand 所属分区的 mapId 必须等于车辆当前 Map，才能进入…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0192`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 车辆必须实际位于任务所属 Map。 Demand 所属分区的 mapId 必须等于车辆当前 Map，才能进入候选；无法确认车辆当前 Map 时，该车退出全部派车候选并产生车辆级状态提示，恢复取得明确 Map 后重新参与。距离近、路线可达、空仓、任务类型或分区授权均不能覆盖地图不一致或未知。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md](../../../.scratch/current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)；`决定复合运输、分区与多 SUBLOT 组合边界 > Answer; line 22`；来源 SHA-256 `225defcb356f9f595f5c9a162257bdab8a8282ab3099319102629eddf7ac5c87`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md。
- **决定／旧候选指针：** issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md；R01-A0096 ／ R01-A0097 ／ R01-A0296 ／ R01-A0604 ／ R01-A1891 ／ R02-A0234 ／ R02-A0242 ／ R02-A0987 ／ R03-A1529。
- **规范文本 SHA-256：** `e679ff03addf718d1af0b9a3d62ae215093c7132a44b80d1d6bb02a87e16668a`。

## Required HITL resolution

- [ ] `REQ-0189`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0190`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0191`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0192`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0189`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0190`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0191`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0192`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-051`、Approval payload SHA-256 `5b69f3c7cdcc84a87aa661380e3933ab338f01d80a8446074d4415cec69bd4a6`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
