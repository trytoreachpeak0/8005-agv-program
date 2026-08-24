# 最终批准 REQ-0285–REQ-0288：决定充电阈值、配置变更与异常生命周期

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-078
Approval payload SHA-256: 506b95a3fa5f1d2f0aa2e4047b43ba7dbb6694dbf1ff164747addaa9c67bd604
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-078` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0285 — 已确认中断和无进展均采用双向临时隔离。 已确认正在充电但在完成阈值前、无正常停止命令时非预期停止，形成 Co…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0285`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 已确认中断和无进展均采用双向临时隔离。 已确认正在充电但在完成阈值前、无正常停止命令时非预期停止，形成 ConfirmedChargingInterruption；持续 batteryState=CHARGING 但经 ChargingProgressObservationPolicy 完整稳定期和观察窗口仍未取得最小电量增量，形成 ConfirmedChargingNoProgress。两者都同时触发 ChargingStationAllocationHold 与 VehicleChargingEligibilityHold，不在原桩重启、不换桩试充，结束并核验旧订单后清桩；结果未知时保持原位、预占与两侧暂停。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 40`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `22cf9ccf9503f68342fa063d703bfc345f4e2286c1c21f70f5693878c2f33a55`。

### REQ-0286 — 中断结果与根因归属分离。 人为关闭、物理急停、车辆问题、充电桩问题或外部供电都可能产生同一中断结果；原因未知…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0286`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 中断结果与根因归属分离。 人为关闭、物理急停、车辆问题、充电桩问题或外部供电都可能产生同一中断结果；原因未知时不得自动归责。车辆与充电桩按各自现场证据独立恢复，避免故障车辆逐桩试错并依次暂停全部充电桩。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 41`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `44eaa7da69e1a388eb168d09d35bda7dfb1c85036aa08dd0b2c19e5e494f0e5e`。

### REQ-0287 — “车辆失联”按观测来源分开。 VehicleConnectionSession 失效只阻断车辆新业务并继续通…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0287`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** “车辆失联”按观测来源分开。 VehicleConnectionSession 失效只阻断车辆新业务并继续通过 RIoT 观察；ChargingRIoTVehicleObservationLoss 保持原桩预占、按车辆仍可能占桩处理且不盲发停止、重启或移动命令；ChargingBatteryTelemetryLoss 暂停完成阈值和无进展判断，恢复后以新鲜连续样本重新观察。任何失联或遥测缺失的持续超时都只升级告警和现场响应，永不自动结束订单、释放资源、改派、移动或登记桩故障。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 42`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `0eeb31f158c8faa31df24e5d1394201278b42ef775063cac44606a5fcf1096e9`。

### REQ-0288 — 维修使用暂停分配而非临时删除身份。 维护管理员或系统管理员用 ChargingStationAllocati…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0288`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 维修使用暂停分配而非临时删除身份。 维护管理员或系统管理员用 ChargingStationAllocationHold 使待维修充电桩退出运行时候选，同时保留 ProjectExclusiveChargingStationRegistry 中的稳定身份；已有车辆且无紧急风险时等待当前周期正常完成后维修，有安全风险时任何现场人员可直接操作物理急停并按中断流程收敛。维修完成后通过 ChargingStationRecoveryConfirmation 恢复资格；只有永久拆除、改名、换地图或退出 8005 才修改名册。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md](../../../.scratch/current-requirements-baseline/issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)；`决定充电阈值、配置变更与异常生命周期 > Answer; line 43`；来源 SHA-256 `eba12b25f07fad34fa9c7f20c661d35231d05011ac04b291ad076c6af263317b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md。
- **决定／旧候选指针：** issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md；R03-A1672 ／ R03-A1673 ／ R03-A1711 ／ R03-A1712 ／ R03-A1749 ／ R03-A1758。
- **规范文本 SHA-256：** `24ee5df007acc4f156fd4a191623c442ee630ef11164187c6fde0a3e718254d0`。

## Required HITL resolution

- [ ] `REQ-0285`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0286`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0287`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0288`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0285`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0286`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0287`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0288`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-078`、Approval payload SHA-256 `506b95a3fa5f1d2f0aa2e4047b43ba7dbb6694dbf1ff164747addaa9c67bd604`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
