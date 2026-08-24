# 最终批准 REQ-0017–REQ-0020：新版 MesIngest 当前规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-005
Approval payload SHA-256: cdf5b1adfbe042fdad4d96c33f508bb707461ebcf445c83c4ef676e3c6fd4193
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)
- **责任角色：** MesIngest 产品、数据契约责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-005` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0017 — PausedZeroDrop / TaskTypeProtection 沿用每 WorkType 健康非零基…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0017`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** PausedZeroDrop / TaskTypeProtection 沿用每 WorkType 健康非零基线和连续两轮健康非零恢复规则；保护解除后的下一完整轮才恢复该类型的缺席权威。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 209`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `ee6a51a243e4daa236ee9e6f0aac78dfc8ac273ecbaa0a1a82810d65aa1192ce`。

### REQ-0018 — 有缺席权威的首个完整成功缺席轮次即把当前 Demand 标为 GONE；不再沿用旧版“连续两轮缺席才 GON…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0018`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 有缺席权威的首个完整成功缺席轮次即把当前 Demand 标为 GONE；不再沿用旧版“连续两轮缺席才 GONE”的实现。DemandLastSeenAt 保持最后真实看见时间，GoneConfirmedAt 单独记录。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 210`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `684b2656d83d2ece31e39e4598400e4c552ae574762d071e0d57364356cc6a51`。

### REQ-0019 — DemandSeries 从 GoneConfirmedAt 起连续 GONE 满 12 小时后，只能在后续…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0019`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** DemandSeries 从 GoneConfirmedAt 起连续 GONE 满 12 小时后，只能在后续有缺席权威的完整成功轮次中归档。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 211`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `8e3ac06a4e8b3eb21792c1ec3f0cb9bed5811c407e07a35c949de25cf237cf0d`。

### REQ-0020 — 归档是不可逆生命周期转换。归档后重现继续原 Series 并创建新的 Watch Demand 世代，但产生…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0020`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 归档是不可逆生命周期转换。归档后重现继续原 Series 并创建新的 Watch Demand 世代，但产生 LONG_GONE_BUT_VISIBLE 且永久阻断该 Demand 外部读取。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化完整 SUCCESS 轮次经生产 Host／领域入口，在真实 SQL Server 中驱动同一 TransportDemandKey 由 GONE 满 12 小时归档后再次出现，并通过正式 API、ExternallyReadableDemandCatalog 与 Watch 查询读回，证明原 SeriesId 不变、新建 Demand 世代、产生 LONG_GONE_BUT_VISIBLE，且该 Demand 在后续轮次与服务重启后仍不进入外部可读目录；公开 WPF／会话 seam 仅补充 Watch 可观察行为，涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 212`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `923995b3d707c9353f3c31c339e8b020eb6cb7ecf5e011f46fe415551466b73a`。

## Required HITL resolution

- [ ] `REQ-0017`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0018`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0019`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0020`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0017`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0018`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0019`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0020`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-005`、Approval payload SHA-256 `cdf5b1adfbe042fdad4d96c33f508bb707461ebcf445c83c4ef676e3c6fd4193`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在地图 Notes 中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值；本次串行接力又明确授权在修正验证方法并使旧批准失效后，继续按当前身份重新批准剩余票。本轮 `grilling` 已把四个彼此独立的批准／拒绝／修订选择作为同一 frontier 完整展示；重新扫描、来源核对、独立 SHA-256 复算、两套确定性生成器的 `--verify-only` 核验和 `domain-modeling` 词义核对均未发现来源漂移、批次错配、验证方法与对象不一致、领域词义冲突、外部权限、破坏性操作或路线图范围扩张，因此按该持续授权逐项记录当前最终选择：

- `REQ-0017`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；PausedZeroDrop／TaskTypeProtection 按 WorkType 保留健康非零基线，以连续两轮健康非零解除保护，并从解除后的下一完整轮恢复该类型的缺席权威。
- `REQ-0018`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；有缺席权威的首个完整成功缺席轮次即把当前 Demand 标为 GONE，DemandLastSeenAt 保留最后真实看见时间，GoneConfirmedAt 独立记录确认时间。
- `REQ-0019`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；DemandSeries 只有从 GoneConfirmedAt 起连续 GONE 满 12 小时后，才能在后续有缺席权威的完整成功轮次中归档。
- `REQ-0020`：批准本票所列精确规范文本、适用范围与修正后的验证方法进入 `v1.0.0`；归档不可逆，同键重现沿用原 Series、新建 Watch Demand 世代、产生 `LONG_GONE_BUT_VISIBLE`，并永久阻断该 Demand 外部读取。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0017`：Given 某 WorkType 已建立健康非零基线，When 完整 `SUCCESS` 轮次中该类型突然降为零并触发 PausedZeroDrop／TaskTypeProtection，Then 该类型不得推进缺席、GONE 或归档；When 随后出现连续两轮健康非零完整结果，Then 第二轮只解除保护，下一完整轮才恢复该类型的缺席权威，并由生产 Host／领域入口、真实 SQL Server、正式 API、Watch 查询和审计事件共同证明进入、持续与解除边界。
- `REQ-0018`：Given 当前 VISIBLE Demand 已有真实 DemandLastSeenAt 且轮次具备该 WorkType 的缺席权威，When 首个未观察到该键的完整 `SUCCESS` 轮次经生产 Host／领域入口写入真实 SQL Server，Then 当前 Demand 当轮即为 GONE、GoneConfirmedAt 独立记录该轮确认时间、DemandLastSeenAt 仍为最后真实看见时间；正式 API 与 Watch 查询读回必须一致，不得等待第二个缺席轮次。
- `REQ-0019`：Given DemandSeries 已从 GoneConfirmedAt 起持续 GONE，When 未满 12 小时、轮次不完整或不具备缺席权威，Then 不得归档；When 已满 12 小时后的首个有缺席权威完整 `SUCCESS` 轮次经生产 Host／领域入口提交，Then 在真实 SQL Server 中归档，并由正式 API 与 Watch 查询读回同一生命周期结果。
- `REQ-0020`：Given 同一 TransportDemandKey 的 Series 已由 GONE 满 12 小时并在有缺席权威完整 `SUCCESS` 轮次归档，When 后续脚本化完整 `SUCCESS` 轮次经生产 Host／领域入口再次观察该键，Then 真实 SQL Server、正式 API、ExternallyReadableDemandCatalog 与 Watch 查询共同证明原 SeriesId 不变、新建 Demand 世代、产生 `LONG_GONE_BUT_VISIBLE`，且该 Demand 在后续轮次与服务重启后仍不进入外部可读目录；公开 WPF／会话 seam 只补充 Watch 可观察行为，涉及视觉、DPI 或控件布局时须另按 Golden WPF 流程取得用户预览批准。

本批准绑定批次 `V1-APP-005`、Approval payload SHA-256 `cdf5b1adfbe042fdad4d96c33f508bb707461ebcf445c83c4ef676e3c6fd4193`、候选总账 SHA-256 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f`、当前 95 批 manifest SHA-256 `3b5838d19e3f46b52909a9fc2b97ac2c2d73cfd7cb3b72636ba579fa88c1818f`，以及规范文本 SHA-256：`REQ-0017` 为 `ee6a51a243e4daa236ee9e6f0aac78dfc8ac273ecbaa0a1a82810d65aa1192ce`、`REQ-0018` 为 `684b2656d83d2ece31e39e4598400e4c552ae574762d071e0d57364356cc6a51`、`REQ-0019` 为 `8e3ac06a4e8b3eb21792c1ec3f0cb9bed5811c407e07a35c949de25cf237cf0d`、`REQ-0020` 为 `923995b3d707c9353f3c31c339e8b020eb6cb7ecf5e011f46fe415551466b73a`。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准；全部 `Superseded Answer` 只保留旧总账身份下的历史证据。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 209–212 行与四条候选规范文本逐字一致；候选总账中的四个候选 ID、文本、范围、验证方法、来源身份和文本哈希均与本票一致；批次清单中的 `V1-APP-005`、四个候选 ID 与 approval payload 均与本票一致。候选总账生成器的 `--verify-only` 报告 348 个候选、12,452 条旧来源、363 条可追指针、来源身份漂移 0、旧来源批准升级 0；批准批次生成器的 `--verify-only` 报告 95 批覆盖 348/348、零重复、零遗漏、批准升级 0，且 manifest 身份一致。

`domain-modeling` 对照根 `CONTEXT.md` 后确认 PausedZeroDrop、TaskTypeProtection、DemandSeries、DemandLastSeenAt、LongGoneButVisible、TransportDemand、ExternallyReadableDemand 与外部可读目录的既有词义没有冲突。本批没有形成新词汇或改变既有词义，因此无需修改 `CONTEXT.md`；本票只记录规划与最终批准，不触发产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，在本票完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定后，明确回复“全部采用推荐之”。该回复按其明确语义记录为逐条采用本批全部推荐值：

- `REQ-0017`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0018`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0019`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0020`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-005`、Approval payload SHA-256 `d0442c7b75909ad4b9c9bba4bf3f0c790eecdf83f679e65c426310173437c6de`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 209–212 行与四条候选规范文本对应；候选总账当前 SHA-256 与票据绑定一致，批次清单中的身份、四个候选 ID 与 Approval payload 也与本票一致。批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。

本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，不触发产品测试。

## Comments

### 2026-08-24 — 当前总账重批阻塞复核

本轮按当前候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c` 与当前 95 批 manifest SHA-256 `f3583631c65c383919bce4b95ca146dcae5344bc1ef0754b85cc9a23a9963283` 重新核对。候选总账与批准批次生成器的 `--verify-only` 均通过；来源 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 209–212 行、四条规范文本 SHA-256、批次 `V1-APP-005` 和 Approval payload SHA-256 `d0442c7b75909ad4b9c9bba4bf3f0c790eecdf83f679e65c426310173437c6de` 均与当前票据及总账一致。`CONTEXT.md` 中的 PausedZeroDrop、DemandSeries、DemandLastSeenAt、LongGoneButVisible、TransportDemand 与外部可读语义没有发现词义冲突，本批无需更新领域词汇。

但 `REQ-0020` 出现验证方法与被验证对象不一致：其规范和适用范围覆盖生产 Host／领域投影、SQL Server、正式 API、MesIngestWatch 与外部可读目录，要求证明归档不可逆、归档后重现沿用原 Series 并创建新 Watch Demand 世代、产生 `LONG_GONE_BUT_VISIBLE`，且永久阻断该 Demand 外部读取；当前验证方法却只要求通过公开 WPF／会话 seam 验证可观察行为，不能证明服务端生命周期转换、持久化、正式 API 与外部可读资格各层的一致结果。依据本轮明确的失败式接力规则，这不是可自动采用推荐值的普通批准项。

因此本票保持 `Status: claimed`，不记录当前 `## Answer`、不设为 `resolved`，也不沿用旧候选总账下的 `Superseded Answer`。在最终批准人明确决定是否授权修正 `REQ-0020` 的验证方法并按新身份重新生成相关治理资产前，本票和串行接力均停在这里；本轮不处理或认领下一票，也不创建下一任务。

### 2026-08-24 — 用户授权修正后重建完成

用户明确回复“授权修正”。`REQ-0020` 的规范文本、适用范围、来源及永久需求身份均未改变；验证方法已修正为：以脚本化完整 SUCCESS 轮次经生产 Host／领域入口，在真实 SQL Server 中驱动同一 TransportDemandKey 由 GONE 满 12 小时归档后再次出现，并通过正式 API、ExternallyReadableDemandCatalog 与 Watch 查询读回，证明原 SeriesId 不变、新建 Demand 世代、产生 `LONG_GONE_BUT_VISIBLE`，且该 Demand 在后续轮次与服务重启后仍不进入外部可读目录；公开 WPF／会话 seam 仅补充 Watch 可观察行为，涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准。

确定性重建后的候选总账 SHA-256 为 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f`，当前 95 批 manifest SHA-256 为 `3b5838d19e3f46b52909a9fc2b97ac2c2d73cfd7cb3b72636ba579fa88c1818f`；仍覆盖 348/348，零重复、零遗漏。批次 `V1-APP-005` 的当前 Approval payload SHA-256 为 `cdf5b1adfbe042fdad4d96c33f508bb707461ebcf445c83c4ef676e3c6fd4193`。候选总账与批准批次生成器的 `--verify-only` 复核必须在接力前再次通过。

总账身份变化使此前 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c` 及更早总账身份下的全部批准失效；生成器已把 95 张批准票统一恢复为 `Status: open` 并保留旧批准为 `Superseded Answer` 历史证据。map 已移除失效批准的 Decisions-so-far 索引。重新扫描时必须从实际第一张未认领、未阻塞票开始，不得直接续批本票。

本次只修正验证证据边界，没有形成新领域词汇或改变既有词义，因此不修改 `CONTEXT.md`；没有运行产品测试。
