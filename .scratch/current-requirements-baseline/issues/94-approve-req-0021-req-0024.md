# 最终批准 REQ-0021–REQ-0024：新版 MesIngest 当前规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-006
Approval payload SHA-256: 115809e553becc7853d1e689921481825d97d07ebda0077c15c8c54a1b0516c5
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)
- **责任角色：** MesIngest 产品、数据契约责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-006` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0021 — SeriesErrorCatalog 由领域契约版本化发布。第一版五个代码和四个主分类固定；代码可以新增或 …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0021`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** SeriesErrorCatalog 由领域契约版本化发布。第一版五个代码和四个主分类固定；代码可以新增或 deprecated，但不得换义、复用、改主分类、改作用域或回扫重写旧历史。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以至少两个连续领域契约／Host／API 版本及真实 SQL Server 升级验收，先写入第一版五个代码、四个主分类和历史错误证据，再经生产 Host／领域入口、正式 API/OpenAPI 与 Watch 查询核对新增和 deprecated 行为；证明已发布代码的含义、主分类、作用域与严重度均未改变或复用，旧历史未被回扫重写，任何非法换义、复用、重分类或改作用域的契约变更都由兼容性门禁失败阻止
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 213`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `fcb14ad1b347e6d038f27d302166ec9b19fdcfa485a85ec3a53ed143d1d15afd`。

### REQ-0022 — DemandSeriesCurrentCondition 是 DemandSeriesEvent 的当前投影…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0022`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** DemandSeriesCurrentCondition 是 DemandSeriesEvent 的当前投影，不是聚合根；IngestAlert 也不再拥有 Series 错误的独立 incident 生命周期。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化完整 SUCCESS 轮次经生产 Host／领域入口产生、更新、清除并复发 Series 错误事件，在真实 SQL Server 中核对 DemandSeriesEvent 与 DemandSeriesCurrentCondition，并通过正式 API 及 Watch 查询读回；证明当前条件可由事件确定性重建且不拥有独立聚合身份、修订序列或 incident 生命周期，IngestAlert 不再为 Series 错误另建、续期或关闭独立 incident
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 214`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `6af3d78fb54a634113b7de5ec105532caba8a349dcd93bae6df5556c903a8e11`。

### REQ-0023 — DemandSeriesErrorPeriod 从事件推导并永久保留。Demand 级错误不得跨 Deman…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0023`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** DemandSeriesErrorPeriod 从事件推导并永久保留。Demand 级错误不得跨 DemandId 延续，Series 级错误可以跨世代但必须保留逐世代证据。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化完整 SUCCESS 轮次经生产 Host／领域入口驱动错误出现、证据变化、条件消失、复发、Demand 世代更替与服务重启，在真实 SQL Server 中核对 DemandSeriesEvent、DemandSeriesErrorPeriod 和逐世代证据，并通过正式 API 及 Watch 查询读回；证明期间由事件确定性推导且结束后永久保留，Demand 级期间绝不跨 DemandId，Series 级期间可以跨世代但每个涉及世代都有可读证据
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 215`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `daec23d067e60521425e8e43f99a65625903457e0c6b29f2373c35df154e322f`。

### REQ-0024 — Series 错误证据使用 Host 在完整成功轮次中的 UTC 时间；不使用 MesSourceDate …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0024`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Series 错误证据使用 Host 在完整成功轮次中的 UTC 时间；不使用 MesSourceDate 或 Watch 本机时间确定期间边界。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以可控时钟为 Host 完整 SUCCESS 轮次注入与 MesSourceDate、Watch 本机时区／时间彼此不同的时间值，经生产 Host／领域入口写入真实 SQL Server，并通过正式 API、错误期间历史与 Watch 查询读回；证明期间开始、证据与结束边界只等于 Host 轮次 UTC，失败或不完整轮次不产生边界，服务重启和 Watch 时区变化不改变既有边界；公开 WPF／会话 seam 仅补充 Watch 可观察行为，涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 216`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `f5b4627e73b1a38efa589856d26025c64b1c507868a6901c260e2a9ec553a59e`。

## Required HITL resolution

- [ ] `REQ-0021`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0022`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0023`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0024`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0021`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0022`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0023`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0024`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-006`、Approval payload SHA-256 `115809e553becc7853d1e689921481825d97d07ebda0077c15c8c54a1b0516c5`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值；本次又指示“继续完成下一票”。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定，只读复核未发现例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0021`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0022`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0023`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0024`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-006`、Approval payload SHA-256 `cc575809a014a8bd435d574df3ad2150e131b62590052aabcf86d16a686c1781`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 213–216 行与四条候选规范文本对应；候选总账当前 SHA-256 与票据绑定一致，初始票据 SHA-256 为 `930a74254d9741566419dbf4428ff7d4f392bc53dffe31b9947601c1740dc820`，批次清单中的身份、四个候选 ID 与 Approval payload 也与本票一致。`CONTEXT.md` 对 SeriesErrorCatalog、DemandSeriesCurrentCondition、DemandSeriesErrorPeriod、SeriesErrorScope 和 SeriesErrorEvidenceTime 的现有定义与本批无冲突。批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。

本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，不触发产品测试。

## Comments

### 2026-08-24 — 当前总账重批时发现验证方法阻塞

重新认领本票后，已对当前候选总账、批准批次、来源和领域词汇执行只读复核：候选总账 SHA-256 为 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f`，95 批 manifest SHA-256 为 `3b5838d19e3f46b52909a9fc2b97ac2c2d73cfd7cb3b72636ba579fa88c1818f`，`V1-APP-006` 当前 Approval payload SHA-256 为 `cc575809a014a8bd435d574df3ad2150e131b62590052aabcf86d16a686c1781`；两个确定性生成器的 `--verify-only` 均通过，95 批覆盖 348/348、零重复、零遗漏。来源 `.scratch/new-mes-ingest/spec.md` SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 213–216 行与四条规范文本一致，`CONTEXT.md` 相关词汇无冲突。

但本票当前验证方法与被验证对象不一致，不能按默认推荐安全批准：

- `REQ-0021` 当前仅用 HTTP/OpenAPI 契约与运行时响应核对，不能证明已发布错误码在升级后不换义、不复用、不改主分类/作用域/严重度，也不能证明不回扫重写旧历史。
- `REQ-0022` 当前方法仍要求“最终批准批次需补充或确认逐项 Given/When/Then”，本票没有给出可执行的逐项验收，不能证明当前条件只由事件投影且不具有独立聚合根/incident 生命周期。
- `REQ-0023` 同样仍是待补充的占位方法，不能证明 Demand 级期间不跨 DemandId、Series 级期间跨世代时保留逐世代证据，以及期间从事件推导并永久保留。
- `REQ-0024` 当前只用公开 WPF/会话 seam 验证，无法证明期间边界实际取自 Host 完整成功轮次 UTC，而不是 `MesSourceDate` 或 Watch 本机时间。

建议经用户授权后修正为：`REQ-0021` 增加跨契约版本/部署升级的 Host、真实 SQL Server、正式 API 与历史读回验收；`REQ-0022` 用脚本化成功轮次经生产 Host/领域入口驱动事件并从真实 SQL Server、正式 API 与 Watch 读回，证明当前条件只是事件投影且不存在独立 incident 生命周期；`REQ-0023` 用跨 Demand 世代、条件消失/复发、服务重启的脚本化轮次验证期间推导、永久保留、Demand/Series 作用域和逐世代证据；`REQ-0024` 注入彼此不同的 Host UTC、`MesSourceDate` 与 Watch 本机时间，经生产 Host/领域入口、真实 SQL Server、正式 API 与 Watch 读回证明边界只采用 Host 完整成功轮次 UTC，失败/不完整轮次不产生边界，公开 WPF/会话 seam 只补充 Watch 可观察行为，涉及视觉时另走 Golden WPF 用户预览批准。

以上修正会改变候选总账与批准 payload 身份，须在用户明确授权后确定性重新生成并重新批准。当前 `Superseded Answer` 仍仅作旧哈希历史证据；本票保持 `claimed`，未写入当前 `## Answer`，未设为 `resolved`，未修改 map，也未创建下一任务。
