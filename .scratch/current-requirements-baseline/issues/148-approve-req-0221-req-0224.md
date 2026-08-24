# 最终批准 REQ-0221–REQ-0224：决定到站拒收、取消与完工后纠错边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-060
Approval payload SHA-256: 0f515b4a5c1edfc6ad369156d16348bae573e96073d5d35a2e21c15e6d2a2999
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-060` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0221 — 8005 不建立目的站接收确认、暂不收货、拒收或稍后接收状态。车辆到达目的站并满足既有卸货安全条件后直接开始…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0221`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 8005 不建立目的站接收确认、暂不收货、拒收或稍后接收状态。车辆到达目的站并满足既有卸货安全条件后直接开始开仓卸货；目的站人员后续是否以及何时执行其自身流程不构成 8005 的任务门禁。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)；`决定到站拒收、取消与完工后纠错边界 > Answer; line 19`；来源 SHA-256 `f3fd0eaaa801187ea8672be7fdf90d2e3834deac775386bdfdea7e2784a48cd8`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **决定／旧候选指针：** issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md；R01-A1903 ／ R01-A1909 ／ R01-A1911。
- **规范文本 SHA-256：** `902e2401e23a5d0407b73744f66dbf03f64edc752658f6eaf5c8489cb4462d0e`。

### REQ-0222 — 不提供操作员到站取消入口。卸货开始后必须完成全部目标仓位取空、仓门锁闭与开锁输出复位；人员尚未取货时保持卸货…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0222`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 不提供操作员到站取消入口。卸货开始后必须完成全部目标仓位取空、仓门锁闭与开锁输出复位；人员尚未取货时保持卸货未完成并禁止车辆离开，只允许安全暂停与故障恢复。RIoT 移动订单按实际状态收敛，不因人员未取货而撤销。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)；`决定到站拒收、取消与完工后纠错边界 > Answer; line 20`；来源 SHA-256 `f3fd0eaaa801187ea8672be7fdf90d2e3834deac775386bdfdea7e2784a48cd8`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **决定／旧候选指针：** issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md；R01-A1903 ／ R01-A1909 ／ R01-A1911。
- **规范文本 SHA-256：** `46e5f50a29feda09e8109f27dd9f93068e0686e00846731931225004e6dc14f2`。

### REQ-0223 — 普通操作员只在当前 OperationSession 内、StopClosureCommit 前，可以开关本…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0223`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 普通操作员只在当前 OperationSession 内、StopClosureCommit 前，可以开关本次停靠中待处理或正在处理 Sublot 所关联的仓位；处理顺序和重复开关次数不限，整车其它仓位及窗口外仓位不得凭普通操作权限开启。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)；`决定到站拒收、取消与完工后纠错边界 > Answer; line 21`；来源 SHA-256 `f3fd0eaaa801187ea8672be7fdf90d2e3834deac775386bdfdea7e2784a48cd8`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **决定／旧候选指针：** issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md；R01-A1903 ／ R01-A1909 ／ R01-A1911。
- **规范文本 SHA-256：** `7cdb746e14d15b38332420d366748f80963ba72613090844d933976fd80fcf98`。

### REQ-0224 — 本地完成后发现拿错、漏拿或存错，不重开、回滚或改写原任务，不在 8005 内重送，也不生成新的 MES 运输…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0224`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 本地完成后发现拿错、漏拿或存错，不重开、回滚或改写原任务，不在 8005 内重送，也不生成新的 MES 运输需求；由现场既有流程处理，原任务终态与审计保持不变。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)；`决定到站拒收、取消与完工后纠错边界 > Answer; line 22`；来源 SHA-256 `f3fd0eaaa801187ea8672be7fdf90d2e3834deac775386bdfdea7e2784a48cd8`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **决定／旧候选指针：** issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md；R01-A1903 ／ R01-A1909 ／ R01-A1911。
- **规范文本 SHA-256：** `9615a77e93df9e7c25f5e6ad3ad6fa2d4bccc53d483d3af99d8de927a7313dae`。

## Required HITL resolution

- [ ] `REQ-0221`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0222`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0223`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0224`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0221`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0222`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0223`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0224`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-060`、Approval payload SHA-256 `0f515b4a5c1edfc6ad369156d16348bae573e96073d5d35a2e21c15e6d2a2999`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
