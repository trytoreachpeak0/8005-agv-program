# 最终批准 REQ-0178–REQ-0180：决定无联网充电桩的充电失败确认与暂停触发边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-048
Approval payload SHA-256: 4ce27ab90472bc3dc2d88a82870a4f7fb93b903d998dde080c2c636d28e43556
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-048` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0178 — 失败后进入单一“清桩中”闭环。 旧充电订单必须在清桩前确认取消终态，取消结果未知时继续对账而不完成清桩。正常…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0178`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 失败后进入单一“清桩中”闭环。 旧充电订单必须在清桩前确认取消终态，取消结果未知时继续对账而不完成清桩。正常任务完成、充电完成和充电失败共用地图等待点集合；即使当前只有一个点也按集合建模，只选当前地图上身份有效、路线可达且未被占用或预占的点，多车原子预占；无合格点时原地排队并告警，不猜测其它站点。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)；`决定无联网充电桩的充电失败确认与暂停触发边界 > Answer; line 36`；来源 SHA-256 `3cc41b2331675a2c3ed12295668b2e67b50691932a18aceafa8d9df079b8db9e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **决定／旧候选指针：** issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `e5ecc9730cfc5a4ce86ee6822be452845e35c53dc60a5a3095006d5cef441afe`。

### REQ-0179 — 清桩有两种可替代的完成证明。 系统确认车辆已到地图等待点，或取得人工清桩确认：车辆已移至安全位置且原桩已腾空…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0179`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 清桩有两种可替代的完成证明。 系统确认车辆已到地图等待点，或取得人工清桩确认：车辆已移至安全位置且原桩已腾空。“人工清桩”权限初始授予 R-11 与 R-13，任一具备权限者均可以个人身份单独提交；协助者另行记录，普通操作员不可确认。记录至少包含确认人、时间、车辆、充电桩、车辆最终位置和旧订单处置状态。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)；`决定无联网充电桩的充电失败确认与暂停触发边界 > Answer; line 37`；来源 SHA-256 `3cc41b2331675a2c3ed12295668b2e67b50691932a18aceafa8d9df079b8db9e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **决定／旧候选指针：** issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `06d8ea2d5623fa90637ba6dc07c39ba645cc3ae92d102ba6c9128bcb7cc6c2d9`。

### REQ-0180 — 人工清桩不自动恢复或阻断车辆。 若车辆已到地图等待点，且位置有效、旧订单已终结、车辆状态正常并通过常规派车检…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0180`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 人工清桩不自动恢复或阻断车辆。 若车辆已到地图等待点，且位置有效、旧订单已终结、车辆状态正常并通过常规派车检查，不需要进入维护/禁止派车。只有人工推车、拖车、断电移车影响未收敛，或位置、定位、订单、运动、安全状态任一未知时，才禁止派车直至对账完成。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)；`决定无联网充电桩的充电失败确认与暂停触发边界 > Answer; line 38`；来源 SHA-256 `3cc41b2331675a2c3ed12295668b2e67b50691932a18aceafa8d9df079b8db9e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **决定／旧候选指针：** issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `cf7be9d94fe776fe6a20702c6b5264769e9714a0f605875a0c3646a0588c3a71`。

## Required HITL resolution

- [ ] `REQ-0178`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0179`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0180`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0178`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0179`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0180`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-048`、Approval payload SHA-256 `4ce27ab90472bc3dc2d88a82870a4f7fb93b903d998dde080c2c636d28e43556`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
