# 最终批准 REQ-0124–REQ-0127：Demand Series Inspector E 规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-033
Approval payload SHA-256: f9b8c34f83fe6dff6d5ee829fe5c29b05a6314dc09b06a3d4b184e8735f2eed5
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)
- **责任角色：** MesIngestWatch 产品、现场运维责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-033` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0124 — Ordinary DemandSeries navigation opens only the list. …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0124`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Ordinary DemandSeries navigation opens only the list. Precise navigation targets originating elsewhere locate the target Series, create or show the Inspector, and carry source-snapshot comparison plus optional FocusedDemandId.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 100`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `df6d174232e77b0d1525f4092a7496cd3e08899bc636872ed81f4d069cd22287`。

### REQ-0125 — The top of the Inspector uses one compact Series conte…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0125`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** The top of the Inspector uses one compact Series context, including stable Series identity (SUBLOT + WorkType), lifecycle/current presence, frozen snapshot identity/time, and stale or source-comparison state. It does not repeat large “Series 调查工作台” and DemandId title rows.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 101`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `696466ab98cd8bebb96a96fc1816ea3250cfb598dedb15cbb11ec504242a74d7`。

### REQ-0126 — “世代分析”和“事件” are first-level sibling tabs sharing the s…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0126`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** “世代分析”和“事件” are first-level sibling tabs sharing the same Series context. Generation evidence and events are never permanently split side by side.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 102`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `297b4bc96a1e13fee972f4aed190d42131a7dd451fdb6e59f9105a924ffc33f4`。

### REQ-0127 — A vertical, virtualizable generation list is the sole …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0127`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** A vertical, virtualizable generation list is the sole generation navigator. Current-generation state and selected-generation state are distinct visual properties.
- **适用范围：** 8005 MesIngestWatch 的 DemandSeries 单实例 Inspector E 信息架构
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/demand-series-inspector-e/spec.md](../../../.scratch/demand-series-inspector-e/spec.md)；`DemandSeries 单实例 Inspector：E 世代调查工作台 > Implementation Decisions; line 103`；来源 SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变。
- **首版前替代与冲突处置：** 仅替代 L1/既有 ADR 中 DemandSeries 旧内联详情信息架构；领域契约不变；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `1e36b0a2628aeb1b2efc081e34c7bf716a8beb34e5c19ae6ef0ad8c9139851c6`。

## Required HITL resolution

- [ ] `REQ-0124`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0125`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0126`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0127`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0124`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0125`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0126`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0127`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-033`、Approval payload SHA-256 `f9b8c34f83fe6dff6d5ee829fe5c29b05a6314dc09b06a3d4b184e8735f2eed5`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
