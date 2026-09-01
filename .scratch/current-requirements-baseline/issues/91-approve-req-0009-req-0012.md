# 最终批准 REQ-0009–REQ-0012：新版 MesIngest 当前规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-003
Approval payload SHA-256: 0b2369fe61a0f03016b22892949fa328142bcdd68919200156457470f5e27b6f
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)
- **责任角色：** MesIngest 产品、数据契约责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-003` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0009 — DemandSeries 由大小写与空白规则明确的 TransportDemandKey（SUBLOT + …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0009`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** DemandSeries 由大小写与空白规则明确的 TransportDemandKey（SUBLOT + WorkType）唯一标识。实现必须在契约中固定比较规则，Host、SQL 唯一约束和 Watch 查询使用同一规则，不在各层自行正规化。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以同一组由版本化契约明确给出的大小写与空白等价／非等价表驱动样例，经生产 Host／领域入口、真实 SQL Server 唯一约束与排序规则、正式 API 及 Watch 查询读回，证明 TransportDemandKey 在各层作出相同的合并或区分且无层内自行正规化；任一层结果不一致即失败
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 201`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `36897f75f5fecacb8c3b00853f111e01f5780dcfe1ee55edbf843bf0dd626da3`。

### REQ-0010 — DemandSeries 第一次本地观察时开始，稳定 SeriesId 永不因 GONE、重现或归档后可见而…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0010`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** DemandSeries 第一次本地观察时开始，稳定 SeriesId 永不因 GONE、重现或归档后可见而更换。Series 内事件按单调 SeriesSequence 排序。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 202`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `1f6d2f931568fc88bce8c5d2c5a633f1ed150a8e54bc9138f6c0374808a1e672`。

### REQ-0011 — TransportDemand 是 DemandSeries 内的一代实例。当前 Demand GONE 后…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0011`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** TransportDemand 是 DemandSeries 内的一代实例。当前 Demand GONE 后，归档前再次观察同键创建下一代 DemandId；原 Demand 永久保留并由 predecessor 关系连接。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 203`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `c66d65fef09b670a2fb86e36dfac25ad7ae54d09b78cdc545413a180145a6280`。

### REQ-0012 — 当前 VISIBLE Demand 的唯一原始行实时形成 LiveMesFieldSet；AREA、EQP、…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0012`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 当前 VISIBLE Demand 的唯一原始行实时形成 LiveMesFieldSet；AREA、EQP、STEP、DATES、PACKAGE 每次有意义变化都更新当前值并写事件。新版不保留 FrozenMesFieldSet 或 FIELD_DRIFT 语义。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 204`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `3d96b51f0283d71f2096046af1eb33253e68b7c559ac519701bf37f0dca575a2`。

## Required HITL resolution

- [ ] `REQ-0009`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0010`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0011`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0012`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在地图 Notes 中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值；本次串行接力又明确授权在修正验证方法并使旧批准失效后，继续按当前身份重新批准剩余票。本轮 `grilling` 已把四个彼此独立的批准／拒绝／修订选择作为同一 frontier 完整展示；重新扫描、来源核对、独立 SHA-256 复算、两套确定性生成器的 `--verify-only` 核验和 `domain-modeling` 词义核对均未发现来源漂移、批次错配、验证方法与对象不一致、领域词义冲突、外部权限、破坏性操作或路线图范围扩张，因此按该持续授权逐项记录当前最终选择：

- `REQ-0009`：批准本票所列精确规范文本、适用范围，以及当前跨层一致性验证方法进入 `v1.0.0`。验证必须使用同一组由版本化契约明确给出的大小写与空白等价／非等价表驱动样例，经生产 Host／领域入口、真实 SQL Server 唯一约束与排序规则、正式 API 及 Watch 查询读回；任一层结果不一致即失败。
- `REQ-0010`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0011`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0012`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-003`、Approval payload SHA-256 `0b2369fe61a0f03016b22892949fa328142bcdd68919200156457470f5e27b6f`、候选总账 SHA-256 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f`、当前 95 批 manifest SHA-256 `3b5838d19e3f46b52909a9fc2b97ac2c2d73cfd7cb3b72636ba579fa88c1818f`，以及规范文本 SHA-256：`REQ-0009` 为 `36897f75f5fecacb8c3b00853f111e01f5780dcfe1ee55edbf843bf0dd626da3`、`REQ-0010` 为 `1f6d2f931568fc88bce8c5d2c5a633f1ed150a8e54bc9138f6c0374808a1e672`、`REQ-0011` 为 `c66d65fef09b670a2fb86e36dfac25ad7ae54d09b78cdc545413a180145a6280`、`REQ-0012` 为 `3d96b51f0283d71f2096046af1eb33253e68b7c559ac519701bf37f0dca575a2`。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准；全部 `Superseded Answer` 仅保留旧总账身份下的历史证据。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 201–204 行与四条规范文本逐字一致；候选总账中的四个候选 ID、文本、范围、验证方法、来源身份和文本哈希均与本票一致；批次清单中的 `V1-APP-003`、四个候选 ID 与 approval payload 均与本票一致。候选总账生成器的 `--verify-only` 报告 348 个候选、12,452 条旧来源、363 条可追指针、来源身份漂移 0、旧来源批准升级 0；批准批次生成器的 `--verify-only` 报告 95 批覆盖 348/348、零重复、零遗漏、批准升级 0，且 manifest 身份一致。

`domain-modeling` 对照根 `CONTEXT.md` 后确认 DemandSeries、TransportDemandKey、WorkType、TransportDemand、DemandId、LiveMesFieldSet、GONE、VISIBLE、FrozenMesFieldSet 与 FIELD_DRIFT 的既有词义没有冲突；本批没有形成新词汇或改变既有词义，因此无需修改 `CONTEXT.md`。本票只记录规划与最终批准，不触发产品测试。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在本地图 Notes 中明确授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后，默认采用所展示的推荐值。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及当前批次绑定；本轮重新核验未发现来源漂移、批次不一致、领域词义冲突、验证对象错配、外部权限、破坏性操作或路线图范围扩张等例外，因此逐项记录以下最终选择：

- `REQ-0009`：批准本票所列精确规范文本、适用范围，以及经用户授权修正后的跨层一致性验证方法进入 `v1.0.0`。验证必须使用同一组由版本化契约明确给出的大小写与空白等价／非等价表驱动样例，经生产 Host／领域入口、真实 SQL Server 唯一约束与排序规则、正式 API 及 Watch 查询读回；任一层结果不一致即失败。
- `REQ-0010`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0011`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0012`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-003`、Approval payload SHA-256 `0b2369fe61a0f03016b22892949fa328142bcdd68919200156457470f5e27b6f`、候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c`、当前 95 批 manifest SHA-256 `f3583631c65c383919bce4b95ca146dcae5344bc1ef0754b85cc9a23a9963283`，以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准；下方所有 `Superseded Answer` 只保留旧总账身份下的历史证据。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 201–204 行与四条候选规范文本一致；候选总账中的四个候选 ID、文本、范围、验证方法、来源身份和文本哈希均与本票一致；批次清单中的 `V1-APP-003`、四个候选 ID 与 approval payload 均与本票一致。候选总账和批次生成器的 `--verify-only` 均通过，确认 348 个候选、95 批覆盖 348/348、零重复、零遗漏、来源身份漂移为 0、旧来源批准升级为 0。

`grilling` 的四个逐项决定已由上述持续授权采用完整展示的推荐值；`domain-modeling` 对照根 `CONTEXT.md` 后确认 DemandSeries、TransportDemandKey、TransportDemand、DemandId、SeriesId、LiveMesFieldSet、FrozenMesFieldSet 与 FIELD_DRIFT 的既有词义没有冲突，本批没有形成新词汇或改变既有词义，因此无需修改 `CONTEXT.md`。本票只记录规划与最终批准，不触发产品测试。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中明确授权：后续 HITL 在代理逐项展示推荐结论、取舍与证据边界后，默认采用所展示的推荐值。用户本次指示“继续完成下一票”；本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定，且核查未发现需例外处理的来源漂移、术语冲突或范围扩张，因此按该持续授权逐项记录以下最终选择：

- `REQ-0009`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0010`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0011`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0012`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-003`、Approval payload SHA-256 `3738ed17ff547e2b7c001c04c403a814c1a41577887950474e1fa343f6dfe40d`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 201–204 行与四条候选规范文本一致；候选总账当前 SHA-256 与票据绑定一致，批次清单中的身份、四个候选 ID 与 approval payload 也与本票一致。批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。

本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，不触发产品测试。

## Comments

### 2026-08-24 当前候选总账重批核验阻塞

本轮已核对批次 `V1-APP-003`、当前 Approval payload SHA-256 `3738ed17ff547e2b7c001c04c403a814c1a41577887950474e1fa343f6dfe40d`、当前候选总账 SHA-256 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9`、批次 manifest SHA-256 `9dd633ccb90be9cd0fac7bf78df01a0f9cdb7178cbb97fc7bb35a68e3334c613`、来源文件 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`、来源第 201–204 行、四个规范文本 SHA-256 及 `CONTEXT.md` 的 DemandSeries、TransportDemandKey、TransportDemand、DemandId、LiveMesFieldSet 等词义；上述身份和词义均一致，95 批仍覆盖 348/348，零重复、零遗漏。

但 `REQ-0009` 要求在契约中固定 TransportDemandKey 的大小写与空白比较规则，并证明 Host、SQL 唯一约束和 Watch 查询使用同一规则；当前绑定的验证方法仅为“以公开 WPF/会话 seam 验证可观察行为”。生成器 `verification_for` 会在文本含 `watch` 时先返回 WPF 方法，然后才检查 `sql`，因此本条的 SQL/跨层契约对象没有得到充分且相称的验证边界。这属于“验证方法与被验证对象不一致”，按用户授权边界不能代为决定修订方法，也不能沿用任何 Superseded Answer 批准。

本票保持 `claimed`；本轮不追加新 `## Answer`、不修改 map 的 Decisions so far、不解决第二票、不创建下一接力任务。继续前需由用户决定是否授权为 `REQ-0009` 生成能直接核对契约正规化、Host 键比较、真实 SQL Server 唯一约束/排序规则及 Watch 查询一致性的新验证方法，并据此重算候选总账、批次 payload 与 manifest 后重新批准。

## Answer

用户本人作为当前基线最终批准人，已在地图 Notes 中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值；本次串行接力又明确授权在修正验证方法并使旧批准失效后，继续按当前身份重新批准剩余票。本轮 `grilling` 已把四个彼此独立的批准／拒绝／修订选择作为同一 frontier 完整展示。重新扫描、独立 SHA-256 复算、来源与领域词汇核对，以及候选总账和批准批次两套确定性生成器的 `--verify-only` 均未发现来源漂移、批次错配、范围扩张、领域词义冲突或验证方法与被验证对象不一致，因此按该持续授权逐项记录当前最终选择：

- `REQ-0009`：批准本票所列精确规范文本、适用范围，以及当前跨层一致性验证方法进入 `v1.0.0`；同一组由版本化契约明确给出的大小写与空白等价／非等价样例必须经生产 Host／领域入口、真实 SQL Server 唯一约束与排序规则、正式 API 及 Watch 查询得到一致的合并或区分结果，任一层自行正规化或结果不一致即失败。
- `REQ-0010`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；DemandSeries 第一次本地观察时开始，稳定 SeriesId 不因 GONE、重现或归档后可见而更换，Series 内事件按单调 SeriesSequence 排序。
- `REQ-0011`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；当前 Demand GONE 后、Series 归档前再次观察同键时创建下一代 DemandId，原 Demand 永久保留并以 predecessor 关系连接。
- `REQ-0012`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；当前 VISIBLE Demand 的唯一原始行形成实时 LiveMesFieldSet，有意义变化更新当前值并写事件，不保留 FrozenMesFieldSet 或 FIELD_DRIFT 语义。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0009`：Given 版本化契约明确列出大小写与空白的等价／非等价表驱动样例，When 同一组样例经生产 Host／领域入口、真实 SQL Server 唯一约束与排序规则、正式 API 及 Watch 查询读回，Then 各层对 TransportDemandKey 作出完全相同的合并或区分且无层内自行正规化；任一层不一致即失败。
- `REQ-0010`：Given 同一 TransportDemandKey 首次观察、GONE、重现、归档及归档后可见的连续场景，When 经生产 Host／领域入口投影并由持久化审计、正式 API 与 Watch 查询观察，Then SeriesId 全程不变，事件 SeriesSequence 严格单调且稳定排序。
- `REQ-0011`：Given 当前 Demand 已 GONE 但所属 DemandSeries 尚未归档，When 同一 TransportDemandKey 再次进入完整成功轮次，Then 创建新的 DemandId，原 Demand 永久保留，且新旧世代由 predecessor 关系可核查连接。
- `REQ-0012`：Given 当前 VISIBLE Demand 具有唯一原始行，When AREA、EQP、STEP、DATES 或 PACKAGE 发生有意义变化或变为真实 NULL，Then LiveMesFieldSet 更新当前值并写入变化事件；不得冻结首次值、以旧值补空或产生 FrozenMesFieldSet／FIELD_DRIFT 语义。

本批准绑定批次 `V1-APP-003`、Approval payload SHA-256 `0b2369fe61a0f03016b22892949fa328142bcdd68919200156457470f5e27b6f`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `14872f749075e7b725ded665afb6124ab47a678e4908cfe72aecd0885a75a4b1`，以及规范文本 SHA-256：`REQ-0009` 为 `36897f75f5fecacb8c3b00853f111e01f5780dcfe1ee55edbf843bf0dd626da3`、`REQ-0010` 为 `1f6d2f931568fc88bce8c5d2c5a633f1ed150a8e54bc9138f6c0374808a1e672`、`REQ-0011` 为 `c66d65fef09b670a2fb86e36dfac25ad7ae54d09b78cdc545413a180145a6280`、`REQ-0012` 为 `3d96b51f0283d71f2096046af1eb33253e68b7c559ac519701bf37f0dca575a2`。来源 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 201–204 行与四条规范文本逐字一致；95 批覆盖 348/348，零重复、零遗漏。

旧候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c`、`c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`、`c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0`、`96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9` 与 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f` 下的批准全部只作 Superseded 历史证据，不表示当前批准。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准。

本批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。`domain-modeling` 对照根 `CONTEXT.md` 后确认 DemandSeries、TransportDemandKey、WorkType、TransportDemand、DemandId、SeriesId、SeriesSequence、LiveMesFieldSet、GONE、VISIBLE、FrozenMesFieldSet 与 FIELD_DRIFT 的既有词义没有冲突；本批没有形成新词汇或改变既有词义，因此无需修改 `CONTEXT.md`。这里只记录规划批准，未运行产品测试或 Golden WPF 验证。
