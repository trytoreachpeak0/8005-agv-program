# 最终批准 REQ-0132–REQ-0135：Demand Series Inspector E 规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-035
Approval payload SHA-256: 33fe072b6b526ba74acc26cc84ed18f24227c2ae5996f3fc073ee4d8199ab4d1
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)
- **责任角色：** MesIngestWatch 产品、现场运维责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-035` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0132 — Production status vocabulary remains authoritative, in…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0132`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Production status vocabulary remains authoritative, including LONG_GONE_BUT_VISIBLE. Prototype-only status names and event types are forbidden.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 108`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `cbeb5c38263773f14f57ae7a309f422447b3b6c6c9bc38d6bff2a8d0df801285`。

### REQ-0133 — The event tab renders only real immutable DemandSeries…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0133`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** The event tab renders only real immutable DemandSeriesEvent values from the frozen snapshot. It must not invent convenience events such as DEMAND_REAPPEARED or SNAPSHOT_COMMITTED when those are not production event types.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 109`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `efd5e40eb4b9fbb8880ea0567dbde409994e250577cd2e734eb417a9f816542d`。

### REQ-0134 — Event filtering is local and non-destructive. “相关事件” s…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0134`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Event filtering is local and non-destructive. “相关事件” selects the event tab and filters by the selected DemandId; the user can return to all Series events without another Host request.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 110`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `381a8d282ee04191be88925b0381cdd307eb2dd2564fa6a14aae5370a28da465`。

### REQ-0135 — Boundary MES evidence comes from DemandRawObservationS…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0135`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Boundary MES evidence comes from DemandRawObservationSnapshot grouped by its actual PollTrace/commit and assignment. Raw duplicates remain separate rows in ordinal order.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 111`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `45252b201aca71195362c2d167a87779e7621a795ead22b2fb5bff2cbca9e5a1`。

## Required HITL resolution

- [ ] `REQ-0132`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0133`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0134`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0135`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0132`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0133`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0134`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0135`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-035`、Approval payload SHA-256 `33fe072b6b526ba74acc26cc84ed18f24227c2ae5996f3fc073ee4d8199ab4d1`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
