# 最终批准 REQ-0053–REQ-0056：有界存储与低内存规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-014
Approval payload SHA-256: 5a7bb5fa40e257e14bbe05076ef61509583ebc145d8fdb88114dbfb21e1c31c6
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)
- **责任角色：** SQL Server、容量与存储责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-014` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0053 — 本规格是对既有 NewMesIngestContract 的资源与有界历史扩展；领域身份、完整 MesTas…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0053`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 本规格是对既有 NewMesIngestContract 的资源与有界历史扩展；领域身份、完整 MesTaskUnionRound、DemandSeries、ExternallyReadableDemandCatalog、CurrentIngestAttention 和 Watch 业务只读边界继续有效。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 146`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `d107150e4c12e80ddee918d236d9c776db57f519a021b19db2a5ea633e3822f5`。

### REQ-0054 — ADR-mes-0020 至 ADR-mes-0030 是本规格的设计权威。本规格补充可验收行为、默认配置、…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0054`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** ADR-mes-0020 至 ADR-mes-0030 是本规格的设计权威。本规格补充可验收行为、默认配置、切换步骤和门禁，不复制或重新解释 ADR 全文。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 147`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `4272bb5e6a4e0bc1fed39225fdfbf943d55862bb9699012a4b6c42c45f72c762`。

### REQ-0055 — SQL Server 常态 max server memory 默认 1536 MB，sqlservr 稳态…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0055`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** SQL Server 常态 max server memory 默认 1536 MB，sqlservr 稳态目标约不超过 2 GB。受控维护期上限为 2048 MB，结束后恢复常态；800 MB 是已知不可运行配置，必须拒绝。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 148`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `614b2b1afe350a62bfcaa621fd1cee82745988d8a729040cfb9ff9a5fb5f8635`。

### REQ-0056 — Host 轮询改为固定 60 秒 start-to-start 单飞调度。慢轮次不重叠、不补跑；连续失败使用…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0056`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Host 轮询改为固定 60 秒 start-to-start 单飞调度。慢轮次不重叠、不补跑；连续失败使用 60、120、300 秒退避，上限 300 秒，成功后恢复正常节奏。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 149`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `2068e5730014937b2a1ec1bcf5048b01014e87376c9736b5612869b0eb929b5e`。

## Required HITL resolution

- [ ] `REQ-0053`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0054`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0055`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0056`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0053`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0054`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0055`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0056`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-014`、Approval payload SHA-256 `5a7bb5fa40e257e14bbe05076ef61509583ebc145d8fdb88114dbfb21e1c31c6`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 又逐项展示推荐结论与取舍，只读复核未发现例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0053`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0054`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0055`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0056`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-014`、Approval payload SHA-256 `5a7bb5fa40e257e14bbe05076ef61509583ebc145d8fdb88114dbfb21e1c31c6`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-bounded-storage-low-memory/spec.md` 的 SHA-256 仍为 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`，第 146–149 行与四条候选规范文本逐字对应；候选总账当前 SHA-256 与票据绑定一致，批次清单 SHA-256 为 `51a0085acac307b6d28df8269b20fea88490f9265b7d1b175b4be67ec4223b05`，其中 `V1-APP-014` 的票据身份、四个候选 ID 与重算 Approval payload 均与本票一致。四条规范文本的 SHA-256 也已从候选总账文本独立重算并逐项一致；把认领前状态规范化为 `open` 后，本票初始内容 SHA-256 为清单登记的 `936df012e9bf21fc6d596c77d9527eacd84d6a2b7352f0557c9bcb0929f3ec62`。

`CONTEXT.md` 中 NewMesIngestContract、MesTaskUnionRound、DemandSeries、CurrentIngestAttention 与 ExternallyReadableDemandCatalog 的现有含义与本批一致。SQL Server 内存配置、Host 调度及 ADR 设计权威属于规范或实现决定，不是新的领域词汇。本批没有形成新领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、SQL Server 配置操作、数据库操作、外部权限或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
