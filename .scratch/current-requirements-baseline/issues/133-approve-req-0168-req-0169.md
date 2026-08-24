# 最终批准 REQ-0168–REQ-0169：决定 QUEUEING 滞留与下单前清积压策略

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-045
Approval payload SHA-256: 57fec533c8e53ea63f5274e510a21a0eb9f07ce781e8c52e3ee295b5e2479832
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 2 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-045` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0168 — RIoT 原生 QUEUEING 诊断只提供证据，不提供动作授权。 用户指定 GET /api/task/v…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0168`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** RIoT 原生 QUEUEING 诊断只提供证据，不提供动作授权。 用户指定 GET /api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey} 作为长期 QUEUEING 原因诊断；本地静态契约显示其返回自由文本 reason 和字符串数组 suggestList。8005须保留原始返回，只有经目标 build 实测、纳入项目批准映射并通过独立状态与安全核验的已知原因才可触发相应自动恢复；未知、变化或无法独立验证的文本只告警转人工，绝不直接执行 suggestList。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)；`决定 QUEUEING 滞留与下单前清积压策略 > Answer; line 29`；来源 SHA-256 `95595bee7b79285ebf6e72f52ff5b4cf38965bdc942dcf8edcca0c852fa811fd`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **决定／旧候选指针：** issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md；R09-A0001 ／ R09-A0002 ／ R09-A0003 ／ R09-A0004 ／ R09-A0005 ／ R09-A0006 ／ R09-A0007 ／ R09-A0008 ／ R09-A0009 ／ R09-A0010。
- **规范文本 SHA-256：** `915ec2a68d0c9aac93a8945e20869c06a4ddc321d0aa0683ca4c126fed471a3f`。

### REQ-0169 — 低电量只触发防御性升级，不产生越权恢复。 既有充电触发阈值和最低接单电量阈值继续承担正常能源调度与候选过滤职…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0169`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 低电量只触发防御性升级，不产生越权恢复。 既有充电触发阈值和最低接单电量阈值继续承担正常能源调度与候选过滤职责；订单阻断期间电量下降只提高告警等级和响应紧迫度，不授权取消 QUEUEING 订单、改派充电、重建订单或绕过安全门槛。若诊断指向8005缺陷或原因未知，必须保留订单、诊断和上下文作为故障现场，不能用自动防御掩盖 bug；确实无法安全移动时车辆就不应移动。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)；`决定 QUEUEING 滞留与下单前清积压策略 > Answer; line 30`；来源 SHA-256 `95595bee7b79285ebf6e72f52ff5b4cf38965bdc942dcf8edcca0c852fa811fd`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **决定／旧候选指针：** issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md；R09-A0001 ／ R09-A0002 ／ R09-A0003 ／ R09-A0004 ／ R09-A0005 ／ R09-A0006 ／ R09-A0007 ／ R09-A0008 ／ R09-A0009 ／ R09-A0010。
- **规范文本 SHA-256：** `1659088a5a8131aa603ea601392bb34021f2a49d3cb0fc4325a665edcc6b6eb7`。

## Required HITL resolution

- [ ] `REQ-0168`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0169`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0168`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0169`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-045`、Approval payload SHA-256 `57fec533c8e53ea63f5274e510a21a0eb9f07ce781e8c52e3ee295b5e2479832`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
