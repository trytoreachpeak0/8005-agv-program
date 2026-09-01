# 最终批准 REQ-0261–REQ-0264：决定仓位模型与 IO 映射配置、验证和启用门禁

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-071
Approval payload SHA-256: 7439b089818b63f6181b1bc9a97e408bb15ca8edf6e44ea559ef1800758a4608
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-071` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0261 — 只有硬件相关变更进入整车维护。 仓位集合、物理编号、SlotPosition、IO 点位、信号极性、传感器或…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0261`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 只有硬件相关变更进入整车维护。 仓位集合、物理编号、SlotPosition、IO 点位、信号极性、传感器或脉冲参数变化属于 SlotHardwareConfigurationChange。即使只改一仓，目标车辆也必须整体进入 VehicleConfigurationMaintenance，阻断全车新任务和移动；普通单仓管理禁用不足以替代该隔离。正常进入前必须确认车辆停稳、整车空仓、没有活动仓位操作、任务或预留。有货、状态未知或存在未结操作时必须先按既有异常处置闭环，不能借配置维护态绕过。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 23`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `48fa868258c5f7599572b228847ddcbf151613b9bc2021d74a8fd5e567c4389e`。

### REQ-0262 — 维护和测试依赖服务端在线。 服务端必须在线核验进入门禁并持久化整车配置维护态；车载端不能在断线时自行进入。维…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0262`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 维护和测试依赖服务端在线。 服务端必须在线核验进入门禁并持久化整车配置维护态；车载端不能在断线时自行进入。维护连接中断后，编辑提交、实际测试与激活全部暂停，车辆继续保持隔离，重连并完成状态对账后才可继续。车载端只执行服务端下发候选版本的本机兼容性检查、实际 IO 动作、结果采集和原子激活。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 24`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `b29858d96987f6ea5d7d9ca77be66129087179e1d9ed734af0387cd1395df3ed`。

### REQ-0263 — 任何硬件相关变化都重新核验整车。 SlotConfigurationVerification 必须逐仓确认开…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0263`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 任何硬件相关变化都重新核验整车。 SlotConfigurationVerification 必须逐仓确认开锁输出作用于正确物理仓门、输出按规定复位、锁反馈和仓内光幕语义正确、通道唯一且与目标模型版本一致；不允许只测改动仓位或抽样测试。任一仓位未通过都会阻断整个候选版本。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 25`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `e9975bd3c952361d267b62c46684c962b0654314d97e857b0d8ca9c1fc0e9bf4`。

### REQ-0264 — 整车配置只能原子激活。 ActiveSlotConfiguration 由一个已发布 SlotModelVe…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0264`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 整车配置只能原子激活。 ActiveSlotConfiguration 由一个已发布 SlotModelVersion 与完整 SlotIoBinding 集合共同组成，不允许逐仓生效或混用新旧版本。全部核验通过后一次切换；任一检查、写入或激活失败继续使用上一已知可用版本。断线、重启或结果未知时保持配置维护态，必须依据车载端上报的实际版本、指纹和能力对账，不能猜测成功。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 26`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `a4b79f81f1d09a947a69b50258e2f8aa2be1faebf71fb9c85d18139c46e338bc`。

## Required HITL resolution

- [ ] `REQ-0261`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0262`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0263`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0264`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0261`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0262`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0263`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0264`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-071`、Approval payload SHA-256 `7439b089818b63f6181b1bc9a97e408bb15ca8edf6e44ea559ef1800758a4608`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
