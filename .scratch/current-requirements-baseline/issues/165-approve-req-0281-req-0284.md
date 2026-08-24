# 最终批准 REQ-0281–REQ-0284：决定充电阈值、配置变更与异常生命周期

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-077
Approval payload SHA-256: 4e93e2533fd9153c09fdb7b0b8131eef309b5283e7949b7ad429b18dbf9c29c6
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-077` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0281 — 三个电量阈值具有不同判定时点并满足硬关系。 DispatchBatteryEligibility 使用预计任…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0281`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 三个电量阈值具有不同判定时点并满足硬关系。 DispatchBatteryEligibility 使用预计任务完成后的最低电量余量；MandatoryChargeEntryThreshold 是空闲车辆停止承接普通新任务并进入待充电流程的当前电量门槛；ChargingCompletionThreshold 是开始正常结束本次充电的目标电量。配置必须满足 ChargingCompletionThreshold > MandatoryChargeEntryThreshold >= 最低任务后电量余量。正在执行的任务途中越过充电入口阈值不被中断，完成后立即进入待充电流程；达到完成阈值不等于订单收敛、车辆离桩或预占释放。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 36`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `3f6c38ad74914fa53774ce31a86d1a3451f4cd19e2fa4691042be6d5a5782597`。

### REQ-0282 — ChargingPolicyVersion 受证据批准且按周期冻结。 需求基线只固定语义、关系与治理，不虚构…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0282`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** ChargingPolicyVersion 受证据批准且按周期冻结。 需求基线只固定语义、关系与治理，不虚构具体百分比、稳定期、观察时长或最小增量，也不允许开发默认值；参数须依据车辆电池规格、任务耗电、最远安全返回距离、遥测精度、正常充电曲线和现场测试在投运前批准，无已批准版本的车辆不得投运。编辑、保存和激活不要求先禁用车辆；新版本只作用于新派车判断和新充电周期，既有任务、排队、预占、建单与充电周期继续使用原策略快照。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 37`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `8f3291a811e20babcc827c678d9330ceabd4542f6bd31114fc7756ab5bb35fb8`。

### REQ-0283 — 充电建单不建立专属重试制度。 充电移动订单继承 RoutineOrderCreationCall 与 RIo…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0283`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 充电建单不建立专属重试制度。 充电移动订单继承 RoutineOrderCreationCall 与 RIoTRetryReconciliation，结果未确认时保持车辆、充电意图、目标桩与预占绑定，不换 upperId、不换桩、不重复建单、不释放预占，也不表示已经前往或开始充电；电量下降只升级告警。绑定、同号重试与释放的通用边界由决定 RIoT 建单未确认时任务绑定、重试与释放边界统一收敛。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 38`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `87e9ba79e14101a40b9d28104d806b3a99b8f44120a2972ac8fdd217c0c4121c`。

### REQ-0284 — 严格确认无法开始充电后，8005 原桩追加重试为 0。 RIoT 已完成自身内部重试后仍以经验证失败和最终 …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0284`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 严格确认无法开始充电后，8005 原桩追加重试为 0。 RIoT 已完成自身内部重试后仍以经验证失败和最终 HANG 形成 ConfirmedUnableToCharge，即暂停原桩、清桩并进入统一电量队列；超时或结果未知不构成确认失败，须保持预占并先对账。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 39`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `7059191b26717d68b48f323d6452d4414bc7d47af5a48a5e8406b56d3bc95a1f`。

## Required HITL resolution

- [ ] `REQ-0281`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0282`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0283`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0284`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0281`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0282`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0283`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0284`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-077`、Approval payload SHA-256 `4e93e2533fd9153c09fdb7b0b8131eef309b5283e7949b7ad429b18dbf9c29c6`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
