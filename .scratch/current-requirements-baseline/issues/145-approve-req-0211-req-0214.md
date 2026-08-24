# 最终批准 REQ-0211–REQ-0214：决定同站多任务取消与人工选任务开门边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-057
Approval payload SHA-256: 8b83487d402bea0823c3be6c60b67c2a56494ca9fe970d7c1cccf03df6bc2017
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md](../../../.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-057` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0211 — 同站取消继续沿用既有 DemandId 与永久抑制边界。 操作员选择并取消一个 DemandId 对应的完整…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0211`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 同站取消继续沿用既有 DemandId 与永久抑制边界。 操作员选择并取消一个 DemandId 对应的完整运输需求；未装任务使用空范围完成，部分装或已自动提交任务必须清空该 LoadBatch 的全部目标仓位。取消对象不是单个仓位、SUBLOT 文本或整次停靠，完成后仍以 CANCELLED_BY_OPERATOR 终结 DemandId，并永久抑制对应 TransportDemandKey。同车其它 DemandId、Sublot 与仓位不受影响。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md](../../../.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md)；`决定同站多任务取消与人工选任务开门边界 > Answer; line 19`；来源 SHA-256 `e8b3f8bc7d13b15572736a339a3054e20add0d7189f1ca2a8c05155695c0a0c2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **决定／旧候选指针：** issues/67-decide-same-station-cancellation-and-operator-task-opening.md；R01-A0098 ／ R01-A0099 ／ R01-A0120 ／ R01-A0122。
- **规范文本 SHA-256：** `819faea0fea31dd4e0b3ed28ee1c082bf67773f6966aa0b07f7e784f180d3cbb`。

### REQ-0212 — 系统支持两种能力，但运行界面不同时提供两种入口。 服务端维护项目级、带版本的 LoadTaskEntryMo…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0212`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 系统支持两种能力，但运行界面不同时提供两种入口。 服务端维护项目级、带版本的 LoadTaskEntryMode，其值只能为：
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md](../../../.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md)；`决定同站多任务取消与人工选任务开门边界 > Answer; line 20`；来源 SHA-256 `e8b3f8bc7d13b15572736a339a3054e20add0d7189f1ca2a8c05155695c0a0c2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **决定／旧候选指针：** issues/67-decide-same-station-cancellation-and-operator-task-opening.md；R01-A0098 ／ R01-A0099 ／ R01-A0120 ／ R01-A0122。
- **规范文本 SHA-256：** `fe751a831208c8c48c687bce38a9b4e0b8d1dd2bdcbfa39e85df2072311f0584`。

### REQ-0213 — SUBLOT_ENTRY：车载界面只提供扫码或键盘输入 SUBLOT；

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0213`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** SUBLOT_ENTRY：车载界面只提供扫码或键盘输入 SUBLOT；
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md](../../../.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md)；`决定同站多任务取消与人工选任务开门边界 > Answer; line 21`；来源 SHA-256 `e8b3f8bc7d13b15572736a339a3054e20add0d7189f1ca2a8c05155695c0a0c2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **决定／旧候选指针：** issues/67-decide-same-station-cancellation-and-operator-task-opening.md；R01-A0098 ／ R01-A0099 ／ R01-A0120 ／ R01-A0122。
- **规范文本 SHA-256：** `510682357a09f5f0f6adc773faa13a4ad2178be442d8782bb04e3596d851fa22`。

### REQ-0214 — WORKLIST_SELECTION：车载界面只提供从最新 CurrentStopWorklist 选择待装…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0214`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** WORKLIST_SELECTION：车载界面只提供从最新 CurrentStopWorklist 选择待装 DemandId。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md](../../../.scratch/current-requirements-baseline/issues/67-decide-same-station-cancellation-and-operator-task-opening.md)；`决定同站多任务取消与人工选任务开门边界 > Answer; line 22`；来源 SHA-256 `e8b3f8bc7d13b15572736a339a3054e20add0d7189f1ca2a8c05155695c0a0c2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/67-decide-same-station-cancellation-and-operator-task-opening.md。
- **决定／旧候选指针：** issues/67-decide-same-station-cancellation-and-operator-task-opening.md；R01-A0098 ／ R01-A0099 ／ R01-A0120 ／ R01-A0122。
- **规范文本 SHA-256：** `952f918e43407fb6f9ed5d26979278f21873ff61fd9f2c0f4df4695fdb72ce5c`。

## Required HITL resolution

- [ ] `REQ-0211`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0212`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0213`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0214`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0211`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0212`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0213`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0214`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-057`、Approval payload SHA-256 `8b83487d402bea0823c3be6c60b67c2a56494ca9fe970d7c1cccf03df6bc2017`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
