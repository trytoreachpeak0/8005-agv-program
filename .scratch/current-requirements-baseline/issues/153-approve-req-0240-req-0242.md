# 最终批准 REQ-0240–REQ-0242：决定故障车辆隔离、货物处置与人工越权边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-065
Approval payload SHA-256: a66010dbd25763921ab33d4d7b7586ae2f64b46596cd0be7e5213cc804b3ba35
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-065` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0240 — 正常受控取货以电子物理闭环和具名交接终止业务。 车辆须已停稳且当前订单已 HELD/终结；结果未知时先完成断…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0240`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 正常受控取货以电子物理闭环和具名交接终止业务。 车辆须已停稳且当前订单已 HELD/终结；结果未知时先完成断电、抱闸或等效机械隔离。全部目标仓位达到 EMPTY + 锁闭 + 开锁输出复位 且产品由具名人员接管后，系统自动形成 FaultCargoRecoveryRecord，与原任务 TERMINATED_BY_FAULT_CARGO_HANDOFF 终态及对应 TransportDemandKey 的永久抑制原子提交。记录只证明取出和责任交接，不表示 8005 或 MES 已完成运输；8005 不创建人工运输任务、不等待 MES 扫码。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 55`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `6d7a594d6775f4685c8defeef07497be9888d7fe3fb6f00ab06c7faf38740103`。

### REQ-0241 — 极端锁和传感器故障使用强制机械取出。 锁无法经 DO 弹开，或锁反馈、光幕、占用检测等事实已经失真时，先完成…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0241`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 极端锁和传感器故障使用强制机械取出。 锁无法经 DO 弹开，或锁反馈、光幕、占用检测等事实已经失真时，先完成断电、抱闸或等效机械隔离，再由具备现场作业资质者以应急机械方式开锁或拆卸；系统停止重复发送开锁 DO，将可证明的受影响仓位或 IO 模块标为物理状态未知，影响范围无法确定时隔离整车。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 56`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `3439d1eff8925c8035d241349a000ddaec5c22443fbc307f33b411e4a41ddc3c`。

### REQ-0242 — 货物业务闭环与设备恢复闭环分离。 强制取出后，产品身份明确且完成具名交接时，ForcedCargoHando…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0242`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 货物业务闭环与设备恢复闭环分离。 强制取出后，产品身份明确且完成具名交接时，ForcedCargoHandoffRecord 可以证明货物已经救出和责任交接，允许终止对应任务并写入抑制，但不能证明电子空仓、仓门安全或车辆恢复。产品身份不明时只记录实物，相关任务保持待盘点，不猜测绑定。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 57`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `8ec0aa963bfd86f179744a83e08a02a3a9b2fa7eec3f1958dde837e38a51fee9`。

## Required HITL resolution

- [ ] `REQ-0240`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0241`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0242`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0240`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0241`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0242`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-065`、Approval payload SHA-256 `a66010dbd25763921ab33d4d7b7586ae2f64b46596cd0be7e5213cc804b3ba35`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
