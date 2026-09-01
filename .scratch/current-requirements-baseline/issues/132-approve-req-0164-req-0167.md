# 最终批准 REQ-0164–REQ-0167：决定 QUEUEING 滞留与下单前清积压策略

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-044
Approval payload SHA-256: 02cd2a80eadd9ac909231bff89182e2bd5cd81634a1c6ffdcdb1ae43b4213394
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-044` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0164 — UC-008 的“0/1”是8005的硬下单门禁，不是自动清理目标。 8005 按下单时的 appointV…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0164`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** UC-008 的“0/1”是8005的硬下单门禁，不是自动清理目标。 8005 按下单时的 appointVehicleKey 保证同车至多一个未明确终结的本项目 RIoT 订单；下新单前必须确认没有占用名额的 QUEUEING、EXECUTING、PAUSED、HELD、HANG、SUSPENDED、优先队列或未知状态订单，也没有未结写调用或结果未知。发现非8005、来源不明或归属不可证明的相关订单时同样阻断并告警，8005不得擅自处理。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)；`决定 QUEUEING 滞留与下单前清积压策略 > Answer; line 23`；来源 SHA-256 `95595bee7b79285ebf6e72f52ff5b4cf38965bdc942dcf8edcca0c852fa811fd`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **决定／旧候选指针：** issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md；R09-A0001 ／ R09-A0002 ／ R09-A0003 ／ R09-A0004 ／ R09-A0005 ／ R09-A0006 ／ R09-A0007 ／ R09-A0008 ／ R09-A0009 ／ R09-A0010。
- **规范文本 SHA-256：** `2f24a72ae3e3a3515f975cbc030659c63e2b60a8367b3409303f7d11f56a62a9`。

### REQ-0165 — 正常 QUEUEING 是短暂过渡，QueueingStall 才是异常滞留。 可执行订单通常很快进入 EX…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0165`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 正常 QUEUEING 是短暂过渡，QueueingStall 才是异常滞留。 可执行订单通常很快进入 EXECUTING，轮询周期较长时可能完全观察不到 QUEUEING；长期可见通常表示车辆距可执行路线过远、车辆状态不允许执行、车辆未启用或其它执行前置不成立。长期 QUEUEING 不会自行变成 FAILED，也不能仅凭停留时间推定订单已经失效。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)；`决定 QUEUEING 滞留与下单前清积压策略 > Answer; line 24`；来源 SHA-256 `95595bee7b79285ebf6e72f52ff5b4cf38965bdc942dcf8edcca0c852fa811fd`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **决定／旧候选指针：** issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md；R09-A0001 ／ R09-A0002 ／ R09-A0003 ／ R09-A0004 ／ R09-A0005 ／ R09-A0006 ／ R09-A0007 ／ R09-A0008 ／ R09-A0009 ／ R09-A0010。
- **规范文本 SHA-256：** `e20d6903e957c0c7733be044ba8c17e79b44f7c3c0dd5aa9706b2a8c8bbcf28f`。

### REQ-0166 — 各终态不等同于可再派。 SUCCESS 后仍须确认车辆 IDLE 并重新通过完整派车检查；CANCELLED…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0166`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 各终态不等同于可再派。 SUCCESS 后仍须确认车辆 IDLE 并重新通过完整派车检查；CANCELLED 或 DELETED 只表示旧订单已终结，后续仍须按其受控终止流程重新判断。FAILED 通常指向 RIoT 内部故障，虽然订单已成终态，但形成车辆级失败订单派车阻断，必须提示管理员诊断并解决，不能直接下下一单。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)；`决定 QUEUEING 滞留与下单前清积压策略 > Answer; line 26`；来源 SHA-256 `95595bee7b79285ebf6e72f52ff5b4cf38965bdc942dcf8edcca0c852fa811fd`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **决定／旧候选指针：** issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md；R09-A0001 ／ R09-A0002 ／ R09-A0003 ／ R09-A0004 ／ R09-A0005 ／ R09-A0006 ／ R09-A0007 ／ R09-A0008 ／ R09-A0009 ／ R09-A0010。
- **规范文本 SHA-256：** `bc1921eac7a9e99c10a9fd06936afb386af894cbb810dc24a1ee02dc354a2f39`。

### REQ-0167 — 可证明的暂时阻断应自动恢复。 8005应自动恢复由自身造成、原因已经消除且安全事实可独立证明的临时 Disp…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0167`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 可证明的暂时阻断应自动恢复。 8005应自动恢复由自身造成、原因已经消除且安全事实可独立证明的临时 DispatchDisable，并逐次回查 ON_LINE；8005自己触发的软件急停在进入 CAN_RECOVER、原原因消除且全部安全条件通过时应自动调用 cancelEmergency 并回查 emergencyState=OK。人工、外部系统或来源未知的禁用/急停，以及 CAN_NOT_RECOVER、物理不可移动或安全不可证明的情况保持阻断并转人工。该批准不自动扩展到 OrderContinue、HangContinue 或其它未具名恢复动作，它们继续遵守既有独立规则。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md](../../../.scratch/current-requirements-baseline/issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)；`决定 QUEUEING 滞留与下单前清积压策略 > Answer; line 28`；来源 SHA-256 `95595bee7b79285ebf6e72f52ff5b4cf38965bdc942dcf8edcca0c852fa811fd`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md。
- **决定／旧候选指针：** issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md；R09-A0001 ／ R09-A0002 ／ R09-A0003 ／ R09-A0004 ／ R09-A0005 ／ R09-A0006 ／ R09-A0007 ／ R09-A0008 ／ R09-A0009 ／ R09-A0010。
- **规范文本 SHA-256：** `b8003a84e33f8a9626bcbc5752d4909a4cca1b1f30fb2b94ffbbacf8127abd04`。

## Required HITL resolution

- [ ] `REQ-0164`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0165`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0166`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0167`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0164`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0165`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0166`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0167`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-044`、Approval payload SHA-256 `02cd2a80eadd9ac909231bff89182e2bd5cd81634a1c6ffdcdb1ae43b4213394`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
