# 最终批准 REQ-0077–REQ-0080：有界存储与低内存规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-020
Approval payload SHA-256: 0f1edc076c3aa16483a7ca13412ac4e653127ade0fa88b98223fb50df30116a7
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)
- **责任角色：** SQL Server、容量与存储责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-020` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0077 — 首版不建设 ObservationPayload、ObservationSet 或 Span 内容寻址层。只…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0077`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 首版不建设 ObservationPayload、ObservationSet 或 Span 内容寻址层。只有 30 天容量或当前态逻辑读门禁失败，才以新的证据和 ADR 重新开启该设计。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 170`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `fdd0d0834bc4fe2c181e92aa6c958fe87f579ff1280cc5c7d678c599eb341574`。

### REQ-0078 — 同时提升 NewMesIngestContract 的精确 contractVersion 与 schema…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0078`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 同时提升 NewMesIngestContract 的精确 contractVersion 与 schemaVersion，并更新完整 capability ID/version 集合与 OpenAPI。继续只发布唯一 /api/v2 和 /openapi/v2.json，不提供长期并行 V3。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 171`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `c46648218e2f6157acbefb2e1743b76bd2aab43aed3e1eef924ee4244b75a8c0`。

### REQ-0079 — Host、Watch 与 reference consumer 必须以精确版本整包切换。任何 contrac…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0079`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Host、Watch 与 reference consumer 必须以精确版本整包切换。任何 contract、schema 或 capability 身份不一致都在业务读取前失败，不能做缺字段或旧 DTO 降级。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 172`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `e8700a37674a6061757cbf8ede8246d4ebbb53ea56eabb802ebdf304a0ff89b3`。

### REQ-0080 — 新库不迁移旧当前投影、PollTrace、DemandRawObservation、DemandSeries…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0080`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 新库不迁移旧当前投影、PollTrace、DemandRawObservation、DemandSeries、事件或错误历史；计划切换只从旧库播种已归档 TransportDemandKey 的 ArchivedDemandKeyTombstone。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 173`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `3c0a883d420a4eaf354e549f4e812aff8941bbe640e9cc2f8f18b1f6af26714f`。

## Required HITL resolution

- [ ] `REQ-0077`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0078`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0079`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0080`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0077`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0078`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0079`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0080`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-020`、Approval payload SHA-256 `0f1edc076c3aa16483a7ca13412ac4e653127ade0fa88b98223fb50df30116a7`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 将四项独立批准作为同一轮决策 frontier，逐项核对推荐结论、取舍与证据边界，未发现依赖分支或例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0077`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；首版不建设 ObservationPayload、ObservationSet 或 Span 内容寻址层，只有容量或当前态逻辑读门禁失败时才凭新证据和 ADR 重新开启。
- `REQ-0078`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；同步提升 NewMesIngestContract 的精确 contractVersion 与 schemaVersion，更新完整 capability 集合和 OpenAPI，并维持唯一 V2、无长期并行 V3。
- `REQ-0079`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；Host、Watch 与 reference consumer 按精确版本整包切换，任一 contract、schema 或 capability 身份不一致均在业务读取前失败，禁止旧 DTO 或缺字段降级。
- `REQ-0080`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；新库不迁移旧当前投影和详细历史，计划切换仅从旧库播种已归档 TransportDemandKey 的 ArchivedDemandKeyTombstone。

本批准绑定批次 `V1-APP-020`、Approval payload SHA-256 `0f1edc076c3aa16483a7ca13412ac4e653127ade0fa88b98223fb50df30116a7`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-bounded-storage-low-memory/spec.md` 的 SHA-256 仍为 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`，Git blob 仍为 `099feeef433a0b356c41c90e221ee7d5bafcface`，第 170–173 行与四条候选规范文本逐字对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-020` 票据身份、责任角色、来源、四个候选 ID 与重算 Approval payload 均与本票一致。四条规范文本的 SHA-256 已从总账规范文本独立重算并逐项一致；把认领前状态规范化为 `open` 后，本票初始内容 SHA-256 为清单登记的 `c4acf7f1e5e61c3e946eb57cd564407c799d397a21d13480f3ae6c439f46e66b`。

domain-modeling 核对确认 `CONTEXT.md` 中 `NewMesIngestContract` 已固定 Host、Watch 与 reference consumer 共用唯一 V2、精确 contract/schema/capability 身份和业务读取前失败边界；`PollTrace`、`DemandRawObservation`、`DemandSeries`、`TransportDemandKey` 与 `ArchivedDemandKeyTombstone` 的既有词义也与不迁移旧详细历史、仅播种最小归档墓碑的边界一致。ObservationPayload、ObservationSet、Span 内容寻址层属于本批暂不采用的设计机制，不形成新的领域对象；本批没有改变既有领域词义，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、数据库迁移、数据删除、外部权限、破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
