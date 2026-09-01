# 最终批准 REQ-0200–REQ-0203：决定派车评分、路网成本与无车响应升级规则

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-054
Approval payload SHA-256: 6e5425cfbec39a879cedc731353a43339364341a3e22be9508dc2f0b598a41b4
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-054` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0200 — 采用任务优先的分层字典序，不采用综合加权总分。 每轮先执行全部任务、车辆、站点和安全硬准入，再按任务层级确定…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0200`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 采用任务优先的分层字典序，不采用综合加权总分。 每轮先执行全部任务、车辆、站点和安全硬准入，再按任务层级确定最高优先的单个 TransportDemand 或已批准复合任务集合，最后只为该任务选择车辆；不得先挑空闲车辆再从附近任务中反向选单。高层结论不能被低层数值抵消，取消自由数值形式的车辆调度权重。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 19`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `f5171672b8d97c27927e6ab846e2f5dd14513fdf913aa8e45d51299218238b3c`。

### REQ-0201 — 任务年龄只使用本地连续等待时间。 TransportDemandWaitingAge 从本地首次创建 Tra…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0201`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 任务年龄只使用本地连续等待时间。 TransportDemandWaitingAge 从本地首次创建 TransportDemand 起持续累积，任何业务门禁、车辆短缺或资源占用都不暂停或重置；门禁不满足时任务仍不能派发，但恢复后携带原等待年龄重新参与。MES DATES 因不同查询来源字段和语义不一致、非单调且存在历史状态长期停留，只保留展示、审计和数据质量调查，不参与自动派车排序。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 20`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `a22bb3971c8436bac506143c138f0b93a34925188872c9f5e2facca7eb464dc4`。

### REQ-0202 — 任务类型使用初始优先级带。 STAGING_TO_WIRE 单独处于最高初始带，其余五类任务同处普通带且不再…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0202`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 任务类型使用初始优先级带。 STAGING_TO_WIRE 单独处于最高初始带，其余五类任务同处普通带且不再凭类型细分；同层按 TransportDemandWaitingAge 从长到短排序。普通任务达到防饥饿阈值后进入高于所有未超时任务类型带的超时层，因此可以越过尚未超时的 STAGING_TO_WIRE；超时任务之间仍按本地等待时长排序，任何升级均不得绕过硬门禁。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 21`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `52816c6a67563c58e228fc3bf816ebff31fbf35496e9ad5ca916389899ddf41f`。

### REQ-0203 — 防饥饿阈值须按 DispatchZone 现场标定并批准。 不采用原草稿的默认 1～3 分钟，也不提供通用默…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0203`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 防饥饿阈值须按 DispatchZone 现场标定并批准。 不采用原草稿的默认 1～3 分钟，也不提供通用默认值。同一区全部任务类型共用一个阈值；标定须覆盖车辆从接受任务到再次具备接单资格的完整周期，包含空驶、运输和全部人工装卸，并同时报告完整周期与本地建单至成功绑车等待的中位数、P95、最大值，以及采样期车辆数、任务量和人工装卸情况。系统只提供证据，不自动套统计公式；最终值由当前基线最终批准人选择。未批准阈值时继续累计等待年龄，但不执行跨任务类型升级。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 22`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `05a42531b1fcac06bf0fca65514eedb5c605e88f8f290118fd91bd533da725f0`。

## Required HITL resolution

- [ ] `REQ-0200`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0201`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0202`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0203`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0200`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0201`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0202`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0203`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-054`、Approval payload SHA-256 `6e5425cfbec39a879cedc731353a43339364341a3e22be9508dc2f0b598a41b4`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
