# 最终批准 REQ-0229–REQ-0231：决定到站拒收、取消与完工后纠错边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-062
Approval payload SHA-256: 67952d3e38d778c6f08fa48dc629687c251ad4f963502a184ff52e13e71798bf
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-062` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0229 — 维护开门模式期间整车停站，阻止移动和新仓位作业，但保留已有任务与有料仓位绑定；退出前必须证明全部已开仓门锁闭…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0229`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 维护开门模式期间整车停站，阻止移动和新仓位作业，但保留已有任务与有料仓位绑定；退出前必须证明全部已开仓门锁闭、开锁输出复位且安全状态有效，退出后重新通过 PreDepartureSafetyCheck 才能继续原计划。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)；`决定到站拒收、取消与完工后纠错边界 > Answer; line 27`；来源 SHA-256 `f3fd0eaaa801187ea8672be7fdf90d2e3834deac775386bdfdea7e2784a48cd8`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **决定／旧候选指针：** issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md；R01-A1903 ／ R01-A1909 ／ R01-A1911。
- **规范文本 SHA-256：** `bb99c321dce355c2f363df3703c1b48b52750a42e55dd2b3106a53335e677b54`。

### REQ-0230 — 确认发生遗留物漏检后，立即把该仓位标记为不可操作并排除后续分配；只有 R-11 设备/电气维护人员完成检查、…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0230`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 确认发生遗留物漏检后，立即把该仓位标记为不可操作并排除后续分配；只有 R-11 设备/电气维护人员完成检查、有效信号验证和 HardwareRecoveryConfirmation 后才能恢复。若无法证明故障仅限该仓位，则整车进入 VehicleRecoveryRequired；其它仓位安全可独立证明时只隔离故障仓位。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)；`决定到站拒收、取消与完工后纠错边界 > Answer; line 28`；来源 SHA-256 `f3fd0eaaa801187ea8672be7fdf90d2e3834deac775386bdfdea7e2784a48cd8`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **决定／旧候选指针：** issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md；R01-A1903 ／ R01-A1909 ／ R01-A1911。
- **规范文本 SHA-256：** `122f2db0779144f2df059de69622d299bdcf0e6e6e5352f7cafe0cb90b53cef8`。

### REQ-0231 — 上述所有处置都不修改 MES，不等待或推动 MES 状态变化，也不把 8005 本地终态解释为 MES 完成…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0231`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 上述所有处置都不修改 MES，不等待或推动 MES 状态变化，也不把 8005 本地终态解释为 MES 完成，继续遵守《决定当前 MES 只读与卸货、完工回写边界》。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md](../../../.scratch/current-requirements-baseline/issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md)；`决定到站拒收、取消与完工后纠错边界 > Answer; line 29`；来源 SHA-256 `f3fd0eaaa801187ea8672be7fdf90d2e3834deac775386bdfdea7e2784a48cd8`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md。
- **决定／旧候选指针：** issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md；R01-A1903 ／ R01-A1909 ／ R01-A1911。
- **规范文本 SHA-256：** `1eeb58ed81bddcfa9902eb3758e86288dafea9d4339b1856fadd1053afd4824f`。

## Required HITL resolution

- [ ] `REQ-0229`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0230`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0231`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0229`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0230`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0231`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-062`、Approval payload SHA-256 `67952d3e38d778c6f08fa48dc629687c251ad4f963502a184ff52e13e71798bf`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
