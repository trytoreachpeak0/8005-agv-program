# 最终批准 REQ-0293–REQ-0296：决定空闲返回、停靠点资格与调度竞争边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-080
Approval payload SHA-256: 0548ff695070487d1fdd9cf9d538b3e9d92bc2f7b4c1ff12469489641d6efe27
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-080` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0293 — 等待点实行从在途预占到在点占用的连续单车独占。 选择候选前必须重新核验当前地图、专用角色、车辆适用范围、身份…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0293`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 等待点实行从在途预占到在点占用的连续单车独占。 选择候选前必须重新核验当前地图、专用角色、车辆适用范围、身份有效、RouteCost 可达、未被其它车辆占用或预占以及数据新鲜度；候选计算不等于取得资源。到点后 WaitingPointExclusiveClaim 从预占转为占用，车辆在完整收敛后释放 IDLE_RETURN VehiclePurposeClaim 并可再次参加搬运或强制充电选择，但等待点独占只有在确认车辆实际离点后才释放，不能在下达离点订单时提前释放。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 23`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `b3cd47068da77876f7aff68b0e8e094556036a55b8cec39ddcdc3d687b92a554`。

### REQ-0294 — 空闲返回只使用已批准的通用单段移动能力。 生成的 RIoT“一键停靠”和 parkConfig 客户端不构成…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0294`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 空闲返回只使用已批准的通用单段移动能力。 生成的 RIoT“一键停靠”和 parkConfig 客户端不构成授权，现有白名单也明确禁止这些调用。空闲返回必须通过 RoutineOrderCreationCall，使用稳定 upperId、已核验车辆/地图/目标站点和 RIoT 单车订单名额创建 byDefaultMissions 单段 move，并完整继承 RIoTRetryReconciliation；结果未知时保持车辆、目标点、用途占有和等待点独占，不换号、不换点、不重复建单、不表示已经出发或到达。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 24`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `476a8f374f450007b8eaeb5887763857924b9d7dcaa1579afbea77e2d07ec006`。

### REQ-0295 — 到点必须由一致证据组合确认。 单值 currentPosition 不得独自证明角色到达；至少要求本次稳定 …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0295`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 到点必须由一致证据组合确认。 单值 currentPosition 不得独自证明角色到达；至少要求本次稳定 upperId/订单的目标与预占等待点一致、车辆 currentMap + currentPosition 精确匹配该专用站点、车辆已停止、订单达到相容的已确认终态，且全部证据新鲜无冲突。任一字段缺失、过期或冲突都保持在途承诺并对账，不按超时释放车辆或等待点。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 25`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `422de160a18e226c9d20eeb494323c256c9e3ab76d11d6965ff2daa3f6b13e87`。

### REQ-0296 — 失败按“是否可能已有订单或仍在运动”分流。 首次外部建单前重新核验失败，或明确拒绝且已证明没有活动订单、车辆…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0296`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 失败按“是否可能已有订单或仍在运动”分流。 首次外部建单前重新核验失败，或明确拒绝且已证明没有活动订单、车辆未开始移动时，可以释放本次 VehiclePurposeClaim 与 WaitingPointExclusiveClaim，车辆回到重新评估；只有在取得新鲜资格/路径变化后才能开始新尝试。建单结果未知、订单存在、车辆可能移动、导航进入未知/HANG 或监听丢失时，必须保持原承诺和独占，按通用订单规则对账、告警并在必要时转人工，不盲选其它等待点。已确认失败只可在排除原失败点并重新通过全部门禁后建立新的独立承诺。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 26`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `804b6bb8e7c7ae8d54509faf7d04317e3bcc64bfc1fa8b401aee7239652f356c`。

## Required HITL resolution

- [ ] `REQ-0293`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0294`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0295`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0296`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0293`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0294`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0295`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0296`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-080`、Approval payload SHA-256 `0548ff695070487d1fdd9cf9d538b3e9d92bc2f7b4c1ff12469489641d6efe27`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
