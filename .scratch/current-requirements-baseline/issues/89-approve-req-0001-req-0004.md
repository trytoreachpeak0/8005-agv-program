# 最终批准 REQ-0001–REQ-0004：新版 MesIngest 当前规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-001
Approval payload SHA-256: f28dc8d7b5dc2f3c2fee8d06ef2f0afddcb497017f84f11d6fdb62995f1cfb1f
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)
- **责任角色：** MesIngest 产品、数据契约责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-001` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0001 — 遵循 ADR-mes-0006 的边界：MesIngest 只拥有 MES 接入事实和外部可读目录，不拥有 …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0001`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 遵循 ADR-mes-0006 的边界：MesIngest 只拥有 MES 接入事实和外部可读目录，不拥有 DispatchTask、取消抑制、车辆、站点、路线、RIoT Order 或派车决策。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 193`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `0d08739c845dcf6e4c256f9118e7dcd7dd31d5aaf6cc32a04d6330d1c63e0eb8`。

### REQ-0002 — 遵循 ADR-mes-0007 的技术栈：全 C#、.NET 8 Windows Service、WPF 薄…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0002`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 遵循 ADR-mes-0007 的技术栈：全 C#、.NET 8 Windows Service、WPF 薄客户端、SQL Server 投影、Kestrel API；Oracle 默认 Thin，Thick + Instant Client 仅为配置切换。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以发布包与启动／集成验收核对全 C#、.NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API；Oracle 源用 fake executor 验证单条 SQL、列／类型映射、Thin／Thick 配置切换与凭据脱敏，并以受控工厂 Oracle 11g Thin 探针、必要时 Thick 复验；未执行现场项必须明确为 skip，不得宣称已通过
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 194`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `b2dd2a4471f2e14e140e3a7c1c1608547b9450f97feb3a402410160ab9072390`。

### REQ-0003 — 正式 MES_TASK_UNION 仍是六类任务的开发与发布唯一查询原稿；生产代码不得复制一份会漂移的 SQ…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0003`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 正式 MES_TASK_UNION 仍是六类任务的开发与发布唯一查询原稿；生产代码不得复制一份会漂移的 SQL，也不得按六个分支分别查询。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 195`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `4ef2f8701a3bab61aa93cc99dc01d06e089aa12a55d224acad69ea36a028e2bc`。

### REQ-0004 — MesTaskUnionRound 只有 SUCCESS、FAILURE、INCOMPLETE 三类结果。只…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0004`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** MesTaskUnionRound 只有 SUCCESS、FAILURE、INCOMPLETE 三类结果。只有 SUCCESS 能进入业务投影事务；字段值异常属于 SUCCESS 数据证据，而不是 INCOMPLETE。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 196`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `dfbb40591c27ac779b4cb82c93f01f001788235e1dbdee1980bb50bd93870d42`。

## Required HITL resolution

- [ ] `REQ-0001`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0002`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0003`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0004`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中明确授权：后续 HITL 在代理逐项展示推荐结论、取舍与证据边界后，默认采用所展示的推荐值。用户本次指示继续完成下一票；本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定，且核查未发现需例外处理的来源漂移、术语冲突或范围扩张，因此按该持续授权逐项记录以下最终选择：

- `REQ-0001`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0002`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0003`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0004`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-001`、Approval payload SHA-256 `966e6554d8567600e4c4526921eece9c704cc16e639e832fc75407084c67f294`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 193–196 行与四条候选规范文本一致；批次清单中的身份与本票一致。批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。

本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，不触发产品测试。

## Comments

### 2026-08-24 — 重新批准核验阻塞

本票已按修订后的候选总账重新认领并执行只读核验，但尚不能记录新的最终批准：

- 候选总账实际 SHA-256 为 `4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`，批准批次 manifest 实际 SHA-256 为 `606d77938942f542e95a7215270268634370e536e598b2822b4848ba14fde454`；`V1-APP-001`、payload `966e6554d8567600e4c4526921eece9c704cc16e639e832fc75407084c67f294` 及 `REQ-0001`～`REQ-0004` 覆盖均一致。
- 来源 `.scratch/new-mes-ingest/spec.md` 实际 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 193–196 行与四条规范文本一致；四条规范文本 SHA-256 与候选总账和本票一致。
- `CONTEXT.md` 中 `MesIngest` 与 `MesTaskUnionRound` 的职责和结果词义与 `REQ-0001`、`REQ-0003`、`REQ-0004` 一致，没有形成新术语或词义变化。
- **阻塞异常：** `REQ-0002` 要批准的是完整技术栈（全 C#、.NET 8 Windows Service、WPF 薄客户端、SQL Server 投影、Kestrel API、Oracle Thin/Thick 配置切换），当前验证方法却仅要求 HTTP/OpenAPI 字段、边界、排序、分页、错误和鉴权测试，不能验证 WPF、Service/runtime、SQL Server 投影或 Oracle provider 切换。来源第 263、271、273 行分别要求 Oracle fake executor/Thin-Thick 配置测试、发布包组成与独立启动验证、以及工厂 Oracle Thin/必要时 Thick 探针，证明当前方法与被验证对象不一致。
- 该不一致来自候选总账生成器 `verification_for(...)` 对含 `api` 的文本先命中 HTTP/OpenAPI 分支；它不是来源身份或上下文省略问题。修订验证方法会改变 `REQ-0002` 候选记录、候选总账 SHA-256、`V1-APP-001` payload 和 manifest，必须重新生成并重新批准，不能沿用本票的旧 `Superseded Answer` 或当前 payload。

因此本票保持 `Status: claimed`，未追加新的 `## Answer`，地图 `Decisions so far` 未新增本票记录，也未创建后续接力任务。等待用户明确决定是否授权修订 `REQ-0002` 的验证方法并重新生成受影响身份。

### 2026-08-24 — 用户授权修订并继续串行接力

用户明确授权按推荐方案修订 `REQ-0002` 的验证方法、更新生成规则、重新生成候选总账、批准 payload 与 manifest，并使旧哈希下全部批准失效后按既定串行流程重新批准。修订限定为 `ADR-mes-0007` 复合技术栈候选的精确验证映射，没有扩大路线图、外部权限或产品实现范围。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已于 2026-08-24 对本批四项采用完整展示的推荐值。重新生成与只读复核未发现来源、范围、批次、领域词义或验证对象不一致，逐项结论如下：

- `REQ-0001`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；MesIngest 只拥有 MES 接入事实和外部可读目录，不取得 DispatchTask、取消抑制、车辆、站点、路线、RIoT Order 或派车决策职责。
- `REQ-0002`：批准本票所列精确规范文本、适用范围及修订后的复合技术栈验证方法进入 `v1.0.0`；发布包、启动／集成、Oracle fake executor 与受控工厂探针共同覆盖完整被验证对象，未执行现场项必须明确为 skip。
- `REQ-0003`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；正式 `MES_TASK_UNION` 是六类任务唯一查询原稿，生产代码不得复制或拆成六次查询。
- `REQ-0004`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；只有完整 `SUCCESS` 可进入业务投影事务，字段值异常仍是 `SUCCESS` 数据证据。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0001`：Given MesIngest 接入、投影和只读目录运行，When 调度、取消抑制、车辆、站点、路线、RIoT Order 或派车决定发生变化，Then MesIngest 只发布自身事实且不创建、拥有或改写这些外部职责。
- `REQ-0002`：Given 按发布配置构建部署包，When 执行组成、独立启动和集成核验，Then 可证明 .NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API 均属于同一全 C# 技术栈；When 切换 Oracle provider，Then fake executor 覆盖单条 SQL、映射、Thin／Thick 配置与脱敏，工厂以 Thin 探针、必要时 Thick 复验，未执行项明确为 skip。
- `REQ-0003`：Given 一次六类任务轮询，When 进入生产 Host seam，Then 只执行发布包中的唯一正式 `MES_TASK_UNION` 原稿，并由同一轮次写入真实 SQL Server、经正式 API 读回；不得调用六个独立查询或另一份复制 SQL。
- `REQ-0004`：Given 可控 `SUCCESS`、`FAILURE`、`INCOMPLETE` 轮次及字段值异常行，When 轮次进入生产 Host／领域入口，Then 只有 `SUCCESS` 原子提交投影；`FAILURE`／`INCOMPLETE` 保持业务投影不变，字段异常行则作为 `SUCCESS` 数据证据保留并可经持久化与 API 读回。

本批准绑定批次 `V1-APP-001`、Approval payload SHA-256 `f28dc8d7b5dc2f3c2fee8d06ef2f0afddcb497017f84f11d6fdb62995f1cfb1f`、候选总账 SHA-256 `c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0`，以及本票四条规范文本 SHA-256。来源 `.scratch/new-mes-ingest/spec.md` SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 193–196 行与规范文本一致；批准批次 manifest SHA-256 为 `6b2c2ea1785cc385fe73ecb8d367f10e2b4ee6c4501088bbe954e63494287fe9`，95 批覆盖 348/348 且零重复、零遗漏。

旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 与 `4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838` 下的批准均只作历史证据，不表示当前批准。本批未形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；未运行产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中明确授权：后续 HITL 在代理逐项展示推荐结论、取舍与证据边界后，默认采用所展示的推荐值。本票已经完整展示四项当前候选及其独立批准／拒绝／修订选择；重新生成后的只读与失败式核验未发现来源漂移、批次错配、范围扩张、领域词义冲突或验证方法与被验证对象不一致，因此按该持续授权逐项记录以下最终选择：

- `REQ-0001`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；MesIngest 只拥有 MES 接入事实和外部可读目录，不取得 DispatchTask、取消抑制、车辆、站点、路线、RIoT Order 或派车决策职责。
- `REQ-0002`：批准本票所列精确规范文本、适用范围及复合技术栈验证方法进入 `v1.0.0`；发布包与启动／集成验收核对全 C#、.NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API，Oracle fake executor 覆盖单条 SQL、列／类型映射、Thin／Thick 配置切换与凭据脱敏，受控工厂以 Oracle 11g Thin 探针、必要时 Thick 复验，未执行现场项明确为 skip 且不得宣称已通过。
- `REQ-0003`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；正式 `MES_TASK_UNION` 是六类任务唯一查询原稿，生产代码不得复制或拆成六次查询。
- `REQ-0004`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`MesTaskUnionRound` 只有 `SUCCESS`、`FAILURE`、`INCOMPLETE` 三类结果，只有完整 `SUCCESS` 可进入业务投影事务，字段值异常仍是 `SUCCESS` 数据证据。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0001`：Given MesIngest 接入、投影和只读目录运行，When 调度、取消抑制、车辆、站点、路线、RIoT Order 或派车决定发生变化，Then MesIngest 只发布自身事实且不创建、拥有或改写这些外部职责。
- `REQ-0002`：Given 按发布配置构建部署包，When 执行组成、独立启动和集成核验，Then 可证明 .NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API 均属于同一全 C# 技术栈；When 切换 Oracle provider，Then fake executor 覆盖单条 SQL、映射、Thin／Thick 配置与脱敏，工厂以 Thin 探针、必要时 Thick 复验，未执行项明确为 skip。
- `REQ-0003`：Given 一次六类任务轮询，When 进入生产 Host／领域入口，Then 只执行发布包中的唯一正式 `MES_TASK_UNION` 原稿，并由同一轮次写入真实 SQL Server、经正式 API 读回；不得调用六个独立查询或另一份复制 SQL，现场 Oracle 事实只由受控探针证明。
- `REQ-0004`：Given 可控 `SUCCESS`、`FAILURE`、`INCOMPLETE` 轮次及字段值异常行，When 轮次进入生产 Host／领域入口，Then 只有 `SUCCESS` 原子提交业务投影并可经真实 SQL Server 与正式 API 读回；`FAILURE`／`INCOMPLETE` 保持业务投影不变，字段异常行作为 `SUCCESS` 数据证据保留。

本批准绑定批次 `V1-APP-001`、Approval payload SHA-256 `f28dc8d7b5dc2f3c2fee8d06ef2f0afddcb497017f84f11d6fdb62995f1cfb1f`、候选总账 SHA-256 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9`，以及本票四条规范文本 SHA-256。来源 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 193–196 行与四条规范文本一致；批准批次 manifest SHA-256 为 `9dd633ccb90be9cd0fac7bf78df01a0f9cdb7178cbb97fc7bb35a68e3334c613`，95 批覆盖 348/348 且零重复、零遗漏。票据 88 及本票 Superseded Answer 中的旧总账和 manifest 哈希只保留为历史生成与批准证据，不表示当前批准。

本批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，未运行产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本轮明确授权修正 `REQ-0009` 的验证方法并重算当前候选总账、批次 payload 与 manifest；候选总账身份变化使旧总账下的批准全部失效。用户本人仍是当前基线最终批准人，且已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中授权：后续 HITL 在逐项完整展示推荐结论、取舍和证据边界后默认采用推荐值。本票已完整展示四项当前候选，重新生成、独立哈希复算及两套失败式 `--verify-only` 核验未发现来源漂移、批次错配、范围扩张、领域词义冲突或验证方法与对象不一致，因此逐项记录当前最终选择：

- `REQ-0001`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；MesIngest 只拥有 MES 接入事实和外部可读目录，不取得 DispatchTask、取消抑制、车辆、站点、路线、RIoT Order 或派车决策职责。
- `REQ-0002`：批准本票所列精确规范文本、适用范围及完整复合技术栈验证方法进入 `v1.0.0`；发布包与启动／集成验收核对全 C#、.NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API，Oracle fake executor 覆盖单条 SQL、列／类型映射、Thin／Thick 配置切换与凭据脱敏，受控工厂以 Oracle 11g Thin 探针、必要时 Thick 复验，未执行现场项必须明确为 skip，不得宣称已通过。
- `REQ-0003`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；正式 `MES_TASK_UNION` 是六类任务唯一查询原稿，生产代码不得复制或拆成六次查询。
- `REQ-0004`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`MesTaskUnionRound` 只有 `SUCCESS`、`FAILURE`、`INCOMPLETE` 三类结果，只有完整 `SUCCESS` 可进入业务投影事务，字段值异常仍是 `SUCCESS` 数据证据。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0001`：Given MesIngest 接入、投影和只读目录运行，When 调度、取消抑制、车辆、站点、路线、RIoT Order 或派车决定发生变化，Then MesIngest 只发布自身事实且不创建、拥有或改写这些外部职责。
- `REQ-0002`：Given 按发布配置构建部署包，When 执行组成、独立启动和集成核验，Then 可证明 .NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API 均属于同一全 C# 技术栈；When 切换 Oracle provider，Then fake executor 覆盖单条 SQL、映射、Thin／Thick 配置与脱敏，工厂以 Thin 探针、必要时 Thick 复验，未执行项明确为 skip。
- `REQ-0003`：Given 一次六类任务轮询，When 进入生产 Host／领域入口，Then 只执行发布包中的唯一正式 `MES_TASK_UNION` 原稿，由同一轮次写入真实 SQL Server 并经正式 API 读回；不得调用六个独立查询或另一份复制 SQL，现场 Oracle 事实只由受控探针证明。
- `REQ-0004`：Given 可控 `SUCCESS`、`FAILURE`、`INCOMPLETE` 轮次及字段值异常行，When 轮次进入生产 Host／领域入口，Then 只有 `SUCCESS` 原子提交业务投影并可经真实 SQL Server 与正式 API 读回；`FAILURE`／`INCOMPLETE` 保持业务投影不变，字段异常行作为 `SUCCESS` 数据证据保留。

本批准绑定批次 `V1-APP-001`、Approval payload SHA-256 `f28dc8d7b5dc2f3c2fee8d06ef2f0afddcb497017f84f11d6fdb62995f1cfb1f`、候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c` 及本票四条规范文本 SHA-256。来源 `.scratch/new-mes-ingest/spec.md` SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 193–196 行与规范文本一致；当前批次 manifest SHA-256 为 `f3583631c65c383919bce4b95ca146dcae5344bc1ef0754b85cc9a23a9963283`，95 批覆盖 348/348，零重复、零遗漏。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`、`c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0` 及 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9` 下的批准均只作 Superseded 历史证据，不表示当前批准。本批未形成新的领域词汇或改变既有词义，无需修改 `CONTEXT.md`；未运行产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值。本票已完整展示四项当前候选及其独立批准／拒绝／修订选择；重新扫描、独立 SHA-256 复算及两套确定性生成器的 `--verify-only` 核验均未发现来源漂移、批次错配、范围扩张、领域词义冲突或验证方法与被验证对象不一致，因此按该持续授权逐项记录当前最终选择：

- `REQ-0001`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；MesIngest 只拥有 MES 接入事实和外部可读目录，不取得 DispatchTask、取消抑制、车辆、站点、路线、RIoT Order 或派车决策职责。
- `REQ-0002`：批准本票所列精确规范文本、适用范围及完整复合技术栈验证方法进入 `v1.0.0`；发布包与启动／集成验收核对全 C#、.NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API，Oracle fake executor 覆盖单条 SQL、列／类型映射、Thin／Thick 配置切换与凭据脱敏，受控工厂以 Oracle 11g Thin 探针、必要时 Thick 复验，未执行现场项必须明确为 skip，不得宣称已通过。
- `REQ-0003`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；正式 `MES_TASK_UNION` 是六类任务唯一查询原稿，生产代码不得复制或拆成六次查询。
- `REQ-0004`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`MesTaskUnionRound` 只有 `SUCCESS`、`FAILURE`、`INCOMPLETE` 三类结果，只有完整 `SUCCESS` 可进入业务投影事务，字段值异常仍是 `SUCCESS` 数据证据。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0001`：Given MesIngest 接入、投影和只读目录运行，When 调度、取消抑制、车辆、站点、路线、RIoT Order 或派车决定发生变化，Then MesIngest 只发布自身事实且不创建、拥有或改写这些外部职责。
- `REQ-0002`：Given 按发布配置构建部署包，When 执行组成、独立启动和集成核验，Then 可证明 .NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API 均属于同一全 C# 技术栈；When 切换 Oracle provider，Then fake executor 覆盖单条 SQL、映射、Thin／Thick 配置与脱敏，工厂以 Thin 探针、必要时 Thick 复验，未执行项明确为 skip 且不得宣称已通过。
- `REQ-0003`：Given 一次六类任务轮询，When 进入生产 Host／领域入口，Then 只执行发布包中的唯一正式 `MES_TASK_UNION` 原稿，由同一轮次写入真实 SQL Server 并经正式 API 读回；不得调用六个独立查询或另一份复制 SQL，现场 Oracle 事实只由受控探针证明。
- `REQ-0004`：Given 可控 `SUCCESS`、`FAILURE`、`INCOMPLETE` 轮次及字段值异常行，When 轮次进入生产 Host／领域入口，Then 只有 `SUCCESS` 原子提交业务投影并可经真实 SQL Server 与正式 API 读回；`FAILURE`／`INCOMPLETE` 保持业务投影不变，字段异常行作为 `SUCCESS` 数据证据保留。

本批准绑定批次 `V1-APP-001`、Approval payload SHA-256 `f28dc8d7b5dc2f3c2fee8d06ef2f0afddcb497017f84f11d6fdb62995f1cfb1f`、候选总账 SHA-256 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f` 及本票四条规范文本 SHA-256。来源 `.scratch/new-mes-ingest/spec.md` SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 193–196 行与规范文本一致；当前批准批次 manifest SHA-256 为 `3b5838d19e3f46b52909a9fc2b97ac2c2d73cfd7cb3b72636ba579fa88c1818f`，95 批覆盖 348/348，零重复、零遗漏。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准。

旧候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c`、`c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`、`c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0` 及 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9` 下的批准只作 Superseded 历史证据，不表示当前批准。本批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，未运行产品测试或 Golden WPF 验证。

## Answer

用户本轮已明确授权修正 `REQ-0021`～`REQ-0024` 的验证方法并继续串行接力；候选总账身份变化使此前所有批准失效。用户本人仍是当前基线最终批准人，且已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值。本票已完整展示四项当前候选，重新扫描、独立 SHA-256 复算及两个确定性生成器的 `--verify-only` 核验均未发现来源漂移、批次错配、范围扩张、领域词义冲突或验证方法与被验证对象不一致，因此逐项记录当前最终选择：

- `REQ-0001`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；MesIngest 只拥有 MES 接入事实和外部可读目录，不取得 DispatchTask、取消抑制、车辆、站点、路线、RIoT Order 或派车决策职责。
- `REQ-0002`：批准本票所列精确规范文本、适用范围及完整复合技术栈验证方法进入 `v1.0.0`；发布包与启动／集成验收核对全 C#、.NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API，Oracle fake executor 覆盖单条 SQL、列／类型映射、Thin／Thick 配置切换与凭据脱敏，受控工厂以 Oracle 11g Thin 探针、必要时 Thick 复验，未执行现场项必须明确为 skip，不得宣称已通过。
- `REQ-0003`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；正式 `MES_TASK_UNION` 是六类任务唯一查询原稿，生产代码不得复制或拆成六次查询。
- `REQ-0004`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`MesTaskUnionRound` 只有 `SUCCESS`、`FAILURE`、`INCOMPLETE` 三类结果，只有完整 `SUCCESS` 可进入业务投影事务，字段值异常仍是 `SUCCESS` 数据证据。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0001`：Given MesIngest 接入、投影和只读目录运行，When 调度、取消抑制、车辆、站点、路线、RIoT Order 或派车决定发生变化，Then MesIngest 只发布自身事实且不创建、拥有或改写这些外部职责。
- `REQ-0002`：Given 按发布配置构建部署包，When 执行组成、独立启动和集成核验，Then 可证明 .NET 8 Windows Service、WPF、SQL Server 投影和 Kestrel API 均属于同一全 C# 技术栈；When 切换 Oracle provider，Then fake executor 覆盖单条 SQL、映射、Thin／Thick 配置与脱敏，工厂以 Thin 探针、必要时 Thick 复验，未执行项明确为 skip 且不得宣称已通过。
- `REQ-0003`：Given 一次六类任务轮询，When 进入生产 Host／领域入口，Then 只执行发布包中的唯一正式 `MES_TASK_UNION` 原稿，由同一轮次写入真实 SQL Server 并经正式 API 读回；不得调用六个独立查询或另一份复制 SQL，现场 Oracle 事实只由受控探针证明。
- `REQ-0004`：Given 可控 `SUCCESS`、`FAILURE`、`INCOMPLETE` 轮次及字段值异常行，When 轮次进入生产 Host／领域入口，Then 只有 `SUCCESS` 原子提交业务投影并可经真实 SQL Server 与正式 API 读回；`FAILURE`／`INCOMPLETE` 保持业务投影不变，字段异常行作为 `SUCCESS` 数据证据保留。

本批准绑定批次 `V1-APP-001`、Approval payload SHA-256 `f28dc8d7b5dc2f3c2fee8d06ef2f0afddcb497017f84f11d6fdb62995f1cfb1f`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646` 及本票四条规范文本 SHA-256。来源 `.scratch/new-mes-ingest/spec.md` SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 193–196 行与规范文本一致；当前批准批次 manifest SHA-256 为 `14872f749075e7b725ded665afb6124ab47a678e4908cfe72aecd0885a75a4b1`，95 批覆盖 348/348、零重复、零遗漏。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准；全部 `Superseded Answer` 只保留旧总账身份下的历史证据。

本批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，未运行产品测试或 Golden WPF 验证。
