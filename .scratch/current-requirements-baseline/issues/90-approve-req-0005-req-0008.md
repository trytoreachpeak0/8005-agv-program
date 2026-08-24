# 最终批准 REQ-0005–REQ-0008：新版 MesIngest 当前规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-002
Approval payload SHA-256: 120bac052cfcd00795ce13e515a4819675acf4e6c7c637d0b8771940ac9ea07d
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)
- **责任角色：** MesIngest 产品、数据契约责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-002` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0005 — PollTraceId 及其规范化内容摘要构成轮次幂等边界；相同 id、相同内容不产生副作用，相同 id、不…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0005`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** PollTraceId 及其规范化内容摘要构成轮次幂等边界；相同 id、相同内容不产生副作用，相同 id、不同内容是契约冲突。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 197`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `d302477b3e8e88816f6af5422b5c93a7fc005e027a3d8ece4cc6cf06c8f95db6`。

### REQ-0006 — 每个 SUCCESS 使用一个 ProjectionCommit 原子提交轮次涉及的 PollTrace、D…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0006`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 每个 SUCCESS 使用一个 ProjectionCommit 原子提交轮次涉及的 PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化 SUCCESS 轮次进入生产 Host/领域入口，在真实 SQL Server 的 ProjectionCommit 多个阶段注入失败并经正式 API 读回，证明 PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision 共同提交或共同回滚；重试同一完整轮次只能提交一次
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 198`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `1cb94db1ab7aa6a6c2636b1bc9a5aa2bd2af378c582c82a923842541e6df7236`。

### REQ-0007 — 原始行按稳定规范化内容排序后作为多重集合比较；数据库返回顺序本身不构成业务变化。

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0007`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 原始行按稳定规范化内容排序后作为多重集合比较；数据库返回顺序本身不构成业务变化。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 199`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `dedecfe214b71fd3e275199b6eb671bf6a233368b42a20a83451425d97c3289d`。

### REQ-0008 — 缺少 SUBLOT 或 TASK_TYPE 的行形成 UnassignedMesObservation 并归…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0008`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 缺少 SUBLOT 或 TASK_TYPE 的行形成 UnassignedMesObservation 并归 PollRun 所有；其它可识别行继续投影，不能因为局部坏行把完整成功轮次降级成部分失败。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 200`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `76e6de3ce2b28bd53255b5e556cd88384b89e8b7dbab94f987f845f20f6c44f9`。

## Required HITL resolution

- [ ] `REQ-0005`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0006`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0007`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0008`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中明确授权：后续 HITL 在代理逐项展示推荐结论、取舍与证据边界后，默认采用所展示的推荐值。用户本次指示“继续完成下一票”；本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定，且核查未发现需例外处理的来源漂移、术语冲突或范围扩张，因此按该持续授权逐项记录以下最终选择：

- `REQ-0005`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0006`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0007`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0008`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-002`、Approval payload SHA-256 `6ac0580f25b3aa50815fccccc769fbcde6fb1756f5e850718c828bf22074c7b6`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 197–200 行与四条候选规范文本一致；候选总账当前 SHA-256 与票据绑定一致，批次清单中的身份、四个候选 ID 与 approval payload 也与本票一致。批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。

本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，不触发产品测试。

## Comments

### 2026-08-24 — 重新批准核验阻塞

本票已按修订后的候选总账重新认领，并依 `grilling`、`domain-modeling` 与地图持续授权逐项核对推荐值，但尚不能记录新的最终批准：

- 候选总账实际 SHA-256 为 `c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0`，批准批次 manifest 实际 SHA-256 为 `6b2c2ea1785cc385fe73ecb8d367f10e2b4ee6c4501088bbe954e63494287fe9`；`V1-APP-002`、payload `6ac0580f25b3aa50815fccccc769fbcde6fb1756f5e850718c828bf22074c7b6` 及 `REQ-0005`～`REQ-0008` 覆盖均一致。
- 来源 `.scratch/new-mes-ingest/spec.md` 实际 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 197–200 行与四条规范文本一致；四条规范文本 SHA-256 与候选总账和本票一致。
- `CONTEXT.md` 中 `PollTrace`、`DemandSeriesEvent`、`CatalogRevision` 与 `UnassignedMesObservation` 的现有词义未与本批发生冲突，本批也没有形成新领域词汇。
- **阻塞异常：** `REQ-0006` 要求每个 `SUCCESS` 以一个 `ProjectionCommit` 原子提交 PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision；当前验证方法却只要求 HTTP/OpenAPI 字段、边界、排序、分页、错误、鉴权及运行时响应核对，不能证明多投影同事务、失败回滚或无半提交。
- 来源第 15、36、181、184、249、253–254 行明确把原子事务纳入生产 Host → 真实 SQL Server → 正式 API 的主要验收 seam，并要求在成功事务多个阶段注入 SQL 失败，证明 Rollback 后各投影均无半提交且同一完整轮次重试只提交一次。因此不能仅靠批准票补写 Given/When/Then，把现有 HTTP/OpenAPI 方法解释为已经覆盖事务原子性。
- 该不一致来自候选总账生成器 `verification_for(...)`：`REQ-0006` 文本含 `CatalogRevision`，先命中 API/OpenAPI 分支，而未进入后续的事务/轮次/持久化分支。修订验证方法会改变候选总账 SHA-256、`V1-APP-002` payload 和 manifest，必须重新生成并重新批准；先前对 `REQ-0002` 复合技术栈映射的定向修订授权不自动授权这项新修订。

因此本票保持 `Status: claimed`，未追加新的 `## Answer`，地图 `Decisions so far` 未新增本票记录，也未创建后续接力任务。等待用户明确决定是否授权修订 `REQ-0006` 的验证方法与生成规则、重新生成受影响身份，并继续串行重新批准。

### 2026-08-24 — 用户授权修订并继续串行接力

用户明确授权按推荐方案修订 `REQ-0006` 的验证方法与生成规则、重新生成受影响身份，并继续当前票的串行重新批准。修订仅把原子事务候选映射到来源已经规定的生产 Host、真实 SQL Server 失败注入与正式 API 读回验收 seam，没有改变规范文本、适用范围、领域词义或路线图范围。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已于 2026-08-24 对本批四项采用完整展示的推荐值。重新生成与失败式复核未发现来源、范围、批次、领域词义或验证对象不一致，逐项结论如下：

- `REQ-0005`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`PollTraceId` 与规范化内容摘要共同形成轮次幂等边界，相同 id／相同内容无副作用，相同 id／不同内容属于契约冲突。
- `REQ-0006`：批准本票所列精确规范文本、适用范围及修订后的原子事务验证方法进入 `v1.0.0`；一个 `ProjectionCommit` 涉及的全部投影必须共同提交或共同回滚，同一完整轮次重试只能提交一次。
- `REQ-0007`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；原始行以稳定规范化内容排序后按多重集合比较，返回顺序变化本身不产生业务变化。
- `REQ-0008`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；缺少 SUBLOT 或 TASK_TYPE 的行保存为所属 PollRun 的 `UnassignedMesObservation`，其它可识别行继续投影，完整成功轮次不因局部坏行降级为部分失败。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0005`：Given 已提交一个带稳定 `PollTraceId` 和规范化内容摘要的完整轮次，When 以相同 id／相同内容重放，Then PollTrace、事件、投影和 CatalogRevision 均不重复产生副作用；When 以相同 id／不同内容重放，Then 整次操作以契约冲突失败且既有持久化状态不变。
- `REQ-0006`：Given 一个会更新本条所列全部投影的脚本化 `SUCCESS` 轮次，When 在真实 SQL Server 的 `ProjectionCommit` 多个阶段分别注入失败并经正式 API 读回，Then PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision 均共同回滚、无半提交；When 重试同一完整轮次，Then 全部投影共同提交且只提交一次。
- `REQ-0007`：Given 内容及重复次数相同但返回顺序为 A/B 与 B/A 的原始行，When 两轮分别进入生产 Host seam，Then 规范化多重集合摘要相同且不产生业务变化；Given 任一行内容或重复次数变化，Then 摘要变化并按真实差异进入后续投影判断。
- `REQ-0008`：Given 同一完整 `SUCCESS` 轮次同时含缺少 SUBLOT／TASK_TYPE 的行与可识别行，When 轮次进入生产 Host、真实 SQL Server 并经正式 API 读回，Then 坏行完整保存为 PollRun 所有的 `UnassignedMesObservation`、不猜测生成 DemandSeries，可识别行正常投影且轮次仍保持完整 `SUCCESS` 语义。

本批准绑定批次 `V1-APP-002`、Approval payload SHA-256 `120bac052cfcd00795ce13e515a4819675acf4e6c7c637d0b8771940ac9ea07d`、候选总账 SHA-256 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9`，以及本票四条规范文本 SHA-256。来源 `.scratch/new-mes-ingest/spec.md` SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 197–200 行与规范文本一致；批准批次 manifest SHA-256 为 `9dd633ccb90be9cd0fac7bf78df01a0f9cdb7178cbb97fc7bb35a68e3334c613`，95 批覆盖 348/348 且零重复、零遗漏。

旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838` 与 `c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0` 下的批准均只作历史证据，不表示当前批准。本批未形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；未运行产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中授权：后续 HITL 在代理完整展示每项推荐结论、取舍与证据边界后默认采用推荐值。本次串行接力又明确授权在修正验证方法后重新批准全部失效票。依该授权，本票完整复核四项当前候选后，未发现来源漂移、批次不一致、领域词义冲突、验证对象错配、外部权限、破坏性操作或路线图范围扩张，逐项最终选择如下：

- `REQ-0005`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`PollTraceId` 与规范化内容摘要共同形成轮次幂等边界，相同 id／相同内容无副作用，相同 id／不同内容属于契约冲突。
- `REQ-0006`：批准本票所列精确规范文本、适用范围与修正后的原子提交验证方法进入 `v1.0.0`；每个 `SUCCESS` 的一个 `ProjectionCommit` 必须使所列全部投影共同提交或共同回滚，重试同一完整轮次只能提交一次。
- `REQ-0007`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；原始行按稳定规范化内容排序后以多重集合比较，数据库返回顺序本身不构成业务变化。
- `REQ-0008`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；缺少 `SUBLOT` 或 `TASK_TYPE` 的行成为所属 `PollRun` 的 `UnassignedMesObservation`，其它可识别行继续投影，完整成功轮次不因局部坏行降级为部分失败。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0005`：Given 已提交一个带稳定 `PollTraceId` 与规范化内容摘要的完整轮次，When 以相同 id／相同内容重放，Then PollTrace、事件、投影和 CatalogRevision 均不重复产生副作用；When 以相同 id／不同内容重放，Then 整次操作以契约冲突失败且既有持久化状态不变。
- `REQ-0006`：Given 一个会更新本条所列全部投影的脚本化 `SUCCESS` 轮次，When 经生产 Host／领域入口在真实 SQL Server 的 `ProjectionCommit` 多个阶段分别注入失败并通过正式 API 读回，Then PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision 均共同回滚、无半提交；When 重试同一完整轮次，Then 全部投影共同提交且只提交一次。
- `REQ-0007`：Given 内容及重复次数相同、仅返回顺序不同的原始行集合，When 分别进入生产 Host／领域入口，Then 稳定规范化多重集合摘要相同且不产生业务变化；Given 任一行内容或重复次数变化，Then 摘要变化并按真实差异进入后续投影判断。
- `REQ-0008`：Given 同一完整 `SUCCESS` 轮次同时含缺少 `SUBLOT`／`TASK_TYPE` 的行和可识别行，When 经生产 Host／领域入口、真实 SQL Server 持久化并由正式 API 读回，Then 坏行完整保存为 PollRun 所有的 `UnassignedMesObservation`、不猜测生成 DemandSeries，可识别行正常投影且轮次保持完整 `SUCCESS` 语义；现场 Oracle 事实只由受控探针证明。

本批准绑定批次 `V1-APP-002`、Approval payload SHA-256 `120bac052cfcd00795ce13e515a4819675acf4e6c7c637d0b8771940ac9ea07d`、候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c`，以及规范文本 SHA-256：`REQ-0005` 为 `d302477b3e8e88816f6af5422b5c93a7fc005e027a3d8ece4cc6cf06c8f95db6`、`REQ-0006` 为 `1cb94db1ab7aa6a6c2636b1bc9a5aa2bd2af378c582c82a923842541e6df7236`、`REQ-0007` 为 `dedecfe214b71fd3e275199b6eb671bf6a233368b42a20a83451425d97c3289d`、`REQ-0008` 为 `76e6de3ce2b28bd53255b5e556cd88384b89e8b7dbab94f987f845f20f6c44f9`。来源 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 197–200 行与四条规范文本一致；当前批准批次 manifest SHA-256 为 `f3583631c65c383919bce4b95ca146dcae5344bc1ef0754b85cc9a23a9963283`，95 批覆盖 348/348，零重复、零遗漏。候选总账及批准批次生成器的 `--verify-only` 均通过。

旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`、`c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0` 与 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9` 下的批准均只作历史证据，不表示当前批准。逐项词汇核对与 `CONTEXT.md` 一致，本批未形成新领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；本票只记录规划批准，未运行产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值。本次串行接力又明确授权在修正验证方法后重新批准全部失效票。本票已完整展示四项当前候选及其独立批准／拒绝／修订选择；重新扫描、独立 SHA-256 复算及两套确定性生成器的 `--verify-only` 核验均未发现来源漂移、批次错配、范围扩张、领域词义冲突或验证方法与被验证对象不一致，因此按该持续授权逐项记录当前最终选择：

- `REQ-0005`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`PollTraceId` 与规范化内容摘要共同构成轮次幂等边界，相同 id／相同内容无副作用，相同 id／不同内容属于契约冲突。
- `REQ-0006`：批准本票所列精确规范文本、适用范围及修正后的原子提交验证方法进入 `v1.0.0`；每个 `SUCCESS` 的一个 `ProjectionCommit` 必须使所列全部投影共同提交或共同回滚，重试同一完整轮次只能提交一次。
- `REQ-0007`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；原始行按稳定规范化内容排序后以多重集合比较，数据库返回顺序本身不构成业务变化。
- `REQ-0008`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；缺少 `SUBLOT` 或 `TASK_TYPE` 的行成为所属 `PollRun` 的 `UnassignedMesObservation`，其它可识别行继续投影，完整成功轮次不因局部坏行降级为部分失败。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0005`：Given 已提交一个带稳定 `PollTraceId` 与规范化内容摘要的完整轮次，When 以相同 id／相同内容重放，Then PollTrace、事件、投影和 CatalogRevision 均不重复产生副作用；When 以相同 id／不同内容重放，Then 整次操作以契约冲突失败且既有持久化状态不变。
- `REQ-0006`：Given 一个会更新本条所列全部投影的脚本化 `SUCCESS` 轮次，When 经生产 Host／领域入口在真实 SQL Server 的 `ProjectionCommit` 多个阶段分别注入失败并通过正式 API 读回，Then PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision 均共同回滚、无半提交；When 重试同一完整轮次，Then 全部投影共同提交且只提交一次。
- `REQ-0007`：Given 内容及重复次数相同、仅返回顺序不同的原始行集合，When 分别进入生产 Host／领域入口，Then 稳定规范化多重集合摘要相同且不产生业务变化；Given 任一行内容或重复次数变化，Then 摘要变化并按真实差异进入后续投影判断。
- `REQ-0008`：Given 同一完整 `SUCCESS` 轮次同时含缺少 `SUBLOT`／`TASK_TYPE` 的行和可识别行，When 经生产 Host／领域入口、真实 SQL Server 持久化并由正式 API 读回，Then 坏行完整保存为 PollRun 所有的 `UnassignedMesObservation`、不猜测生成 DemandSeries，可识别行正常投影且轮次保持完整 `SUCCESS` 语义；现场 Oracle 事实只由受控探针证明。

本批准绑定批次 `V1-APP-002`、Approval payload SHA-256 `120bac052cfcd00795ce13e515a4819675acf4e6c7c637d0b8771940ac9ea07d`、候选总账 SHA-256 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f`，以及规范文本 SHA-256：`REQ-0005` 为 `d302477b3e8e88816f6af5422b5c93a7fc005e027a3d8ece4cc6cf06c8f95db6`、`REQ-0006` 为 `1cb94db1ab7aa6a6c2636b1bc9a5aa2bd2af378c582c82a923842541e6df7236`、`REQ-0007` 为 `dedecfe214b71fd3e275199b6eb671bf6a233368b42a20a83451425d97c3289d`、`REQ-0008` 为 `76e6de3ce2b28bd53255b5e556cd88384b89e8b7dbab94f987f845f20f6c44f9`。来源 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 197–200 行与四条规范文本一致；当前批准批次 manifest SHA-256 为 `3b5838d19e3f46b52909a9fc2b97ac2c2d73cfd7cb3b72636ba579fa88c1818f`，95 批覆盖 348/348，零重复、零遗漏。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准。

旧候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c`、`c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`、`c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0` 及 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9` 下的批准只作 Superseded 历史证据，不表示当前批准。本批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，未运行产品测试或 Golden WPF 验证。

## Answer

用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值；本次串行接力又明确授权在修正验证方法后重新批准全部失效票。本票已完整展示四项当前候选及其独立批准／拒绝／修订选择。重新扫描、独立 SHA-256 复算、来源与领域词汇核对，以及候选总账和批准批次两套确定性生成器的 `--verify-only` 均未发现来源漂移、批次错配、范围扩张、领域词义冲突或验证方法与被验证对象不一致，因此按该持续授权逐项记录当前最终选择：

- `REQ-0005`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`PollTraceId` 与规范化内容摘要共同构成轮次幂等边界，相同 id／相同内容无副作用，相同 id／不同内容属于契约冲突。
- `REQ-0006`：批准本票所列精确规范文本、适用范围及修正后的原子提交验证方法进入 `v1.0.0`；每个 `SUCCESS` 的一个 `ProjectionCommit` 必须使所列全部投影共同提交或共同回滚，重试同一完整轮次只能提交一次。
- `REQ-0007`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；原始行按稳定规范化内容排序后以多重集合比较，数据库返回顺序本身不构成业务变化。
- `REQ-0008`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；缺少 `SUBLOT` 或 `TASK_TYPE` 的行成为所属 `PollRun` 的 `UnassignedMesObservation`，其它可识别行继续投影，完整成功轮次不因局部坏行降级为部分失败。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0005`：Given 已提交一个带稳定 `PollTraceId` 与规范化内容摘要的完整轮次，When 以相同 id／相同内容重放，Then PollTrace、事件、投影和 CatalogRevision 均不重复产生副作用；When 以相同 id／不同内容重放，Then 整次操作以契约冲突失败且既有持久化状态不变。
- `REQ-0006`：Given 一个会更新本条所列全部投影的脚本化 `SUCCESS` 轮次，When 经生产 Host／领域入口在真实 SQL Server 的 `ProjectionCommit` 多个阶段分别注入失败并通过正式 API 读回，Then PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision 均共同回滚、无半提交；When 重试同一完整轮次，Then 全部投影共同提交且只提交一次。
- `REQ-0007`：Given 内容及重复次数相同、仅返回顺序不同的原始行集合，When 分别进入生产 Host／领域入口，Then 稳定规范化多重集合摘要相同且不产生业务变化；Given 任一行内容或重复次数变化，Then 摘要变化并按真实差异进入后续投影判断。
- `REQ-0008`：Given 同一完整 `SUCCESS` 轮次同时含缺少 `SUBLOT`／`TASK_TYPE` 的行和可识别行，When 经生产 Host／领域入口、真实 SQL Server 持久化并由正式 API 读回，Then 坏行完整保存为 PollRun 所有的 `UnassignedMesObservation`、不猜测生成 DemandSeries，可识别行正常投影且轮次保持完整 `SUCCESS` 语义；现场 Oracle 事实只由受控探针证明。

本批准绑定批次 `V1-APP-002`、Approval payload SHA-256 `120bac052cfcd00795ce13e515a4819675acf4e6c7c637d0b8771940ac9ea07d`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `14872f749075e7b725ded665afb6124ab47a678e4908cfe72aecd0885a75a4b1`，以及规范文本 SHA-256：`REQ-0005` 为 `d302477b3e8e88816f6af5422b5c93a7fc005e027a3d8ece4cc6cf06c8f95db6`、`REQ-0006` 为 `1cb94db1ab7aa6a6c2636b1bc9a5aa2bd2af378c582c82a923842541e6df7236`、`REQ-0007` 为 `dedecfe214b71fd3e275199b6eb671bf6a233368b42a20a83451425d97c3289d`、`REQ-0008` 为 `76e6de3ce2b28bd53255b5e556cd88384b89e8b7dbab94f987f845f20f6c44f9`。来源 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 197–200 行与四条规范文本一致；95 批覆盖 348/348，零重复、零遗漏。

旧候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c`、`c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`、`c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0`、`96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9` 与 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f` 下的批准全部只作 Superseded 历史证据，不表示当前批准。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准。

本批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。逐项词汇核对与 `CONTEXT.md` 一致，本批未形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录规划批准，未运行产品测试或 Golden WPF 验证。
