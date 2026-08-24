# 最终批准 REQ-0049–REQ-0052：新版 MesIngest 当前规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-013
Approval payload SHA-256: f9f2738669b6c3255ea00d0f976db69a8179a7ba6da26ef761b102de1132dfa9
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)
- **责任角色：** MesIngest 产品、数据契约责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-013` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0049 — 新系统不迁移旧 TransportDemand、冻结字段、IngestAlert incident、Dema…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0049`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 新系统不迁移旧 TransportDemand、冻结字段、IngestAlert incident、DemandChangeFeed、PollHealth 或历史 DTO。首个完整 SUCCESS 是所有新 Series 与错误 bootstrap 的最早可证明起点。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 241`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `da75ea83eb7cb76dd08c0be0756aced37f9be5cbe45d8f2c6e104db6edeb41af`。

### REQ-0050 — 回退是部署级整体恢复：停止新版，恢复旧程序、旧配置和独立旧数据库备份；不允许新程序连接旧库或旧程序连接新库。

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0050`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 回退是部署级整体恢复：停止新版，恢复旧程序、旧配置和独立旧数据库备份；不允许新程序连接旧库或旧程序连接新库。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 242`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `e36dd52dbdd70f5107e23264028ab5b5c4cbf6e79ce5392ebe0f39a0dd8eb763`。

### REQ-0051 — 安全边界延续本机默认绑定、远程绑定强制共享密钥、凭据外置、日志脱敏和工厂返回包脱敏；OpenAPI 文档可独…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0051`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 安全边界延续本机默认绑定、远程绑定强制共享密钥、凭据外置、日志脱敏和工厂返回包脱敏；OpenAPI 文档可独立发布，但业务数据端点必须遵循访问控制。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 243`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `ef3c7f12a13e66f72c75e97796c0c0773733dbea3dba4ab751ef17bb977b05cc`。

### REQ-0052 — 数据持续增长通过 SQL Server 差异写入、必要索引、事件不可变追加、当前投影表和有界查询控制；不得每…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0052`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 数据持续增长通过 SQL Server 差异写入、必要索引、事件不可变追加、当前投影表和有界查询控制；不得每轮加载/重写全部历史或在 Watch 本地分页。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 244`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `b895209ce190b0716c3907a370902630f66e815febdd0b8fb24c15c1d1d44c41`。

## Required HITL resolution

- [ ] `REQ-0049`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0050`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0051`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0052`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0049`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0050`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0051`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0052`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-013`、Approval payload SHA-256 `f9f2738669b6c3255ea00d0f976db69a8179a7ba6da26ef761b102de1132dfa9`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 又逐项展示推荐结论与取舍，只读复核未发现例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0049`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0050`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0051`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0052`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-013`、Approval payload SHA-256 `f9f2738669b6c3255ea00d0f976db69a8179a7ba6da26ef761b102de1132dfa9`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 241–244 行与四条候选规范文本逐字对应；候选总账当前 SHA-256 与票据绑定一致，批次清单 SHA-256 为 `51a0085acac307b6d28df8269b20fea88490f9265b7d1b175b4be67ec4223b05`，其中 `V1-APP-013` 的票据身份、四个候选 ID 与重算 Approval payload 均与本票一致。四条规范文本的 SHA-256 也已从候选总账文本独立重算并逐项一致；把认领前状态规范化为 `open` 后，本票初始内容 SHA-256 为清单登记的 `f0811523895c38134507eb5752627aadd80afeb889933e349fc94653e5d216ef`。

`CONTEXT.md` 中 MesIngest、TransportDemand、MesIngestWatch、NewMesIngestContract、WatchTelemetryIngest、IngestAlert 与 MesIngestCutoverRun 的现有含义与本批一致。部署级整体回退与受控切换运行是不同阶段：前者恢复旧程序、旧配置与独立旧库备份并禁止跨代混接，后者只描述计划停机窗口中的一次性新库切换；二者不构成词义冲突。安全边界批准也不授予新外部权限。

本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、数据库操作、外部权限或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
