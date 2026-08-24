# 最终批准 REQ-0013–REQ-0016：新版 MesIngest 当前规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-004
Approval payload SHA-256: 8a46395cc69140bb99ba4d43dd93b71d0b406b2d962d031522850619bac131d8
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)
- **责任角色：** MesIngest 产品、数据契约责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-004` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0013 — DuplicateTransportDemandKeyObservation 保存同键的全部规范化原始行，不…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0013`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** DuplicateTransportDemandKeyObservation 保存同键的全部规范化原始行，不选主行、不拼接字段、不生成多条 Demand；恢复唯一时继续当前 Demand 世代。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 205`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `ce8de0b5a8e2005a53542be1e0cf3535cf897f2360fedddc9de5ac0d93695b6d`。

### REQ-0014 — WorkType 来自 TASK_TYPE 并参与业务键；同一 SUBLOT 多 WorkType 各自形成…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0014`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** WorkType 来自 TASK_TYPE 并参与业务键；同一 SUBLOT 多 WorkType 各自形成独立 Series，同时在全部受影响当前 Demand 上形成冲突证据。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 206`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `971d5388ff9bf40391962740c6fcb72c7ac48d4382d80e9d5b074956cc36668e`。

### REQ-0015 — Demand 缺席只能由模块根据完整 SUCCESS、RestartBarrier 和 TaskTypePr…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0015`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Demand 缺席只能由模块根据完整 SUCCESS、RestartBarrier 和 TaskTypeProtection 内部计算权威；任何调用方均不得传入可绕过保护的 absenceAuthority 布尔值。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 207`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `d8d26d01aa75cbed37d459504673be99963062620b4625c25bea5b47ffaff30e`。

### REQ-0016 — 服务启动进入两轮重启保护：第一轮完整结果建立基线，第二轮结束保护，下一轮才拥有缺席权威。保护阶段仍可创建/更…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0016`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 服务启动进入两轮重启保护：第一轮完整结果建立基线，第二轮结束保护，下一轮才拥有缺席权威。保护阶段仍可创建/更新可见 Demand，但不能推进 GONE 或归档。
- **适用范围：** 8005 MesIngest Windows Service、Host/领域投影、SQL Server、版本化 API/OpenAPI、MesIngestWatch 与外部可读目录
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/new-mes-ingest/spec.md](../../../.scratch/new-mes-ingest/spec.md)；`新版 MesIngest 整体替换规格书 > Implementation Decisions; line 208`；来源 SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84。
- **首版前替代与冲突处置：** 整体替代旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 当前语义；精确边界见票据 84；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `41a0938badcf8ebdd8bc0b8215799a48e704dc1c12d5bde3cb0980155bdb42a7`。

## Required HITL resolution

- [ ] `REQ-0013`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0014`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0015`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0016`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在地图 Notes 中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值；本次串行接力又明确授权在修正验证方法并使旧批准失效后，继续按当前身份重新批准剩余票。本轮 `grilling` 已把四个彼此独立的批准／拒绝／修订选择作为同一 frontier 完整展示；重新扫描、来源核对、独立 SHA-256 复算、两套确定性生成器的 `--verify-only` 核验和 `domain-modeling` 词义核对均未发现来源漂移、批次错配、验证方法与对象不一致、领域词义冲突、外部权限、破坏性操作或路线图范围扩张，因此按该持续授权逐项记录当前最终选择：

- `REQ-0013`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；同一规范化 TransportDemandKey 的重复观测只生成一个当前 Demand，保存全部规范化原始行，不选主行、不拼接字段，恢复唯一时延续同一 Demand 世代。
- `REQ-0014`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`WorkType` 取自 `TASK_TYPE` 并参与业务键，同一 `SUBLOT` 的不同 WorkType 各自形成独立 Series，且全部受影响当前 Demand 都保留冲突证据。
- `REQ-0015`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；缺席权威只能由模块依据完整 `SUCCESS`、`RestartBarrier` 与 `TaskTypeProtection` 内部推导，调用方不得以 `absenceAuthority` 布尔值绕过保护。
- `REQ-0016`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；启动后第一轮完整结果建立基线、第二轮结束重启保护、下一轮才取得缺席权威，保护期间允许创建或更新可见 Demand，但不得推进 `GONE` 或归档。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0013`：Given 一个完整 `SUCCESS` 轮次含同一规范化 TransportDemandKey 的多条原始行，When 经生产 Host／领域入口写入真实 SQL Server 并由正式 API 与 Watch 查询读回，Then 只存在一个 Series 和一个当前 Demand，`DuplicateTransportDemandKeyObservation` 保存全部规范化原始行且没有主行选择、字段拼接或额外 Demand；When 后续完整轮次恢复唯一行，Then 重复条件关闭并继续同一当前 DemandId／世代。
- `REQ-0014`：Given 同一 `SUBLOT` 同时出现两个不同 `TASK_TYPE`，When 同一完整轮次经生产 Host／领域入口、真实 SQL Server、正式 API 与 Watch 查询读回，Then 两个 WorkType 形成两个不同 TransportDemandKey 和独立 Series，并在两个受影响当前 Demand 上均可见冲突证据；不得按 `SUBLOT` 合并为一个 Series。
- `REQ-0015`：Given 完整／非完整轮次以及 RestartBarrier、TaskTypeProtection 分别成立与解除的表驱动组合，When 通过生产 Host／领域入口处理并检查发布契约和正式 API 结果，Then 缺席权威只由模块从这些事实推导，受保护或非完整组合不得推进缺席生命周期，且任何生产调用面均不存在可传入并绕过保护的 `absenceAuthority` 布尔参数。
- `REQ-0016`：Given 重启前真实 SQL Server 中存在当前可见 Demand，When 服务重启后连续提交三个缺少该 Demand 的完整 `SUCCESS` 轮次并逐轮通过正式 API 与 Watch 查询读回，Then 第一轮只建立基线、第二轮只结束保护、第三轮才允许按缺席权威推进 `GONE`，前两轮不得推进 `GONE` 或归档；Given 保护期间出现新行或已有行变化，Then 对应可见 Demand 仍可创建或更新。

本批准绑定批次 `V1-APP-004`、Approval payload SHA-256 `8a46395cc69140bb99ba4d43dd93b71d0b406b2d962d031522850619bac131d8`、候选总账 SHA-256 `e9354a4382490876e28b878695cd840327375a4aba92e05eaacce83ad975474f`、当前 95 批 manifest SHA-256 `3b5838d19e3f46b52909a9fc2b97ac2c2d73cfd7cb3b72636ba579fa88c1818f`，以及规范文本 SHA-256：`REQ-0013` 为 `ce8de0b5a8e2005a53542be1e0cf3535cf897f2360fedddc9de5ac0d93695b6d`、`REQ-0014` 为 `971d5388ff9bf40391962740c6fcb72c7ac48d4382d80e9d5b074956cc36668e`、`REQ-0015` 为 `d8d26d01aa75cbed37d459504673be99963062620b4625c25bea5b47ffaff30e`、`REQ-0016` 为 `41a0938badcf8ebdd8bc0b8215799a48e704dc1c12d5bde3cb0980155bdb42a7`。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准；全部 `Superseded Answer` 只保留旧总账身份下的历史证据。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 205–208 行与四条候选规范文本逐字一致；候选总账中的四个候选 ID、文本、范围、验证方法、来源身份和文本哈希均与本票一致；批次清单中的 `V1-APP-004`、四个候选 ID 与 approval payload 均与本票一致。候选总账生成器的 `--verify-only` 报告 348 个候选、12,452 条旧来源、363 条可追指针、来源身份漂移 0、旧来源批准升级 0；批准批次生成器的 `--verify-only` 报告 95 批覆盖 348/348、零重复、零遗漏、批准升级 0，且 manifest 身份一致。

`domain-modeling` 对照根 `CONTEXT.md` 后确认 DuplicateTransportDemandKeyObservation、WorkType、TransportDemandKey、DemandSeries、Demand、GONE、RestartBarrier 与 TaskTypeProtection 的既有词义没有冲突。本批没有形成新词汇或改变既有词义，因此无需修改 `CONTEXT.md`；本票只记录规划与最终批准，不触发产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已在本地图 Notes 中明确授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后，默认采用所展示的推荐值。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及当前批次绑定；本轮重新核验未发现来源漂移、批次不一致、领域词义冲突、验证对象错配、外部权限、破坏性操作或路线图范围扩张等例外，因此逐项记录以下最终选择：

- `REQ-0013`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；同键重复观测只保存一个当前 Demand 的全部规范化原始行，不选主行、不拼接字段、不拆成多个 Demand，恢复唯一时延续当前 Demand 世代。
- `REQ-0014`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`WorkType` 取自 `TASK_TYPE` 并参与业务键，同一 `SUBLOT` 的不同 WorkType 各自形成 Series，且全部受影响当前 Demand 都保留冲突证据。
- `REQ-0015`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；缺席权威只能由模块依据完整 `SUCCESS`、`RestartBarrier` 与 `TaskTypeProtection` 内部推导，调用方不得以 `absenceAuthority` 布尔值绕过保护。
- `REQ-0016`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；启动后第一轮完整结果建立基线、第二轮结束重启保护、下一轮才取得缺席权威，保护期间允许创建或更新可见 Demand，但不得推进 `GONE` 或归档。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0013`：Given 一个完整 `SUCCESS` 轮次含同一规范化 TransportDemandKey 的多条原始行，When 经生产 Host／领域入口写入真实 SQL Server 并由正式 API 与 Watch 查询读回，Then 只存在一个 Series 和一个当前 Demand，`DuplicateTransportDemandKeyObservation` 保存全部规范化原始行且没有主行选择、字段拼接或额外 Demand；When 后续完整轮次恢复唯一行，Then 重复条件关闭并继续同一当前 DemandId／世代。
- `REQ-0014`：Given 同一 `SUBLOT` 同时出现两个不同 `TASK_TYPE`，When 同一完整轮次经生产 Host／领域入口、真实 SQL Server、正式 API 与 Watch 查询读回，Then 两个 WorkType 形成两个不同 TransportDemandKey 和独立 Series，并在两个受影响当前 Demand 上均可见冲突证据；不得按 `SUBLOT` 合并为一个 Series。
- `REQ-0015`：Given 完整／非完整轮次以及 RestartBarrier、TaskTypeProtection 分别成立与解除的表驱动组合，When 通过生产 Host／领域入口处理并检查发布契约和正式 API 结果，Then 缺席权威只由模块从这些事实推导，受保护或非完整组合不得推进缺席生命周期，且任何生产调用面均不存在可传入并绕过保护的 `absenceAuthority` 布尔参数。
- `REQ-0016`：Given 重启前真实 SQL Server 中存在当前可见 Demand，When 服务重启后连续提交三个缺少该 Demand 的完整 `SUCCESS` 轮次并逐轮通过正式 API 与 Watch 查询读回，Then 第一轮只建立基线、第二轮只结束保护、第三轮才允许按缺席权威推进 `GONE`，前两轮不得推进 `GONE` 或归档；Given 保护期间出现新行或已有行变化，Then 对应可见 Demand 仍可创建或更新。

本批准绑定批次 `V1-APP-004`、Approval payload SHA-256 `8a46395cc69140bb99ba4d43dd93b71d0b406b2d962d031522850619bac131d8`、候选总账 SHA-256 `b239e6ea87b79d394b7cf5ec2ed6d28a4e63119584dbfdf0156b1d71331e553c`、当前 95 批 manifest SHA-256 `f3583631c65c383919bce4b95ca146dcae5344bc1ef0754b85cc9a23a9963283`，以及规范文本 SHA-256：`REQ-0013` 为 `ce8de0b5a8e2005a53542be1e0cf3535cf897f2360fedddc9de5ac0d93695b6d`、`REQ-0014` 为 `971d5388ff9bf40391962740c6fcb72c7ac48d4382d80e9d5b074956cc36668e`、`REQ-0015` 为 `d8d26d01aa75cbed37d459504673be99963062620b4625c25bea5b47ffaff30e`、`REQ-0016` 为 `41a0938badcf8ebdd8bc0b8215799a48e704dc1c12d5bde3cb0980155bdb42a7`。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 205–208 行与四条候选规范文本一致；候选总账中的四个候选 ID、文本、范围、验证方法、来源身份和文本哈希均与本票一致；批次清单中的 `V1-APP-004`、四个候选 ID与 approval payload 均与本票一致。候选总账和批次生成器的 `--verify-only` 均通过，确认 348 个候选、95 批覆盖 348/348、零重复、零遗漏、来源身份漂移为 0、旧来源批准升级为 0。

旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`、`4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`、`c3a3db495a6ea0335049c2cebe73540c456dc7e606a0a737ba83f8db0e9de5c0` 与 `96d06b87db07fc9c0e32d00c3ae96b2162cf6b2c931a155d70fb1c77875cdce9` 下的批准均只作 Superseded 历史证据，不表示当前批准。`grilling` 的四个逐项决定已由上述持续授权采用完整展示的推荐值；`domain-modeling` 对照根 `CONTEXT.md` 后确认 DuplicateTransportDemandKeyObservation、WorkType、TransportDemandKey、DemandSeries、Demand、GONE、RestartBarrier 与 TaskTypeProtection 的既有词义没有冲突。本批没有形成新词汇或改变既有词义，因此无需修改 `CONTEXT.md`；本票只记录规划与最终批准，不触发产品测试或 Golden WPF 验证。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中明确授权：后续 HITL 在代理逐项展示推荐结论、取舍与证据边界后，默认采用所展示的推荐值。用户本次指示“继续完成下一票”；本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定，且核查未发现需例外处理的来源漂移、术语冲突或范围扩张，因此按该持续授权逐项记录以下最终选择：

- `REQ-0013`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0014`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0015`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0016`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-004`、Approval payload SHA-256 `8a46395cc69140bb99ba4d43dd93b71d0b406b2d962d031522850619bac131d8`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 仍为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 205–208 行与四条候选规范文本对应；候选总账当前 SHA-256 与票据绑定一致，批次清单中的身份、四个候选 ID 与 approval payload 也与本票一致。批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、外部权限、破坏性操作或路线图范围扩张。

本批没有形成新的领域词汇或改变既有词义，因此无需修改 `CONTEXT.md`；这里只记录需求批准，不触发产品测试。

## Answer

用户本人作为当前基线最终批准人，已在地图 Notes 中授权：后续 HITL 在代理逐项完整展示推荐结论、取舍与证据边界后默认采用推荐值；本次串行接力又明确授权在修正验证方法并使旧批准失效后，继续按当前身份重新批准剩余票。本轮 `grilling` 已把四个彼此独立的批准／拒绝／修订选择作为同一 frontier 完整展示；重新扫描、来源核对、独立 SHA-256 复算、两套确定性生成器的 `--verify-only` 核验和 `domain-modeling` 词义核对均未发现来源漂移、批次错配、验证方法与对象不一致、领域词义冲突、外部权限、破坏性操作或路线图范围扩张，因此按该持续授权逐项记录当前最终选择：

- `REQ-0013`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；同一规范化 TransportDemandKey 的重复观测只生成一个当前 Demand，保存全部规范化原始行，不选主行、不拼接字段，恢复唯一时延续同一 Demand 世代。
- `REQ-0014`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；`WorkType` 取自 `TASK_TYPE` 并参与业务键，同一 `SUBLOT` 的不同 WorkType 各自形成独立 Series，且全部受影响当前 Demand 都保留冲突证据。
- `REQ-0015`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；缺席权威只能由模块依据完整 `SUCCESS`、`RestartBarrier` 与 `TaskTypeProtection` 内部推导，调用方不得以 `absenceAuthority` 布尔值绕过保护。
- `REQ-0016`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；启动后第一轮完整结果建立基线、第二轮结束重启保护、下一轮才取得缺席权威，保护期间允许创建或更新可见 Demand，但不得推进 `GONE` 或归档。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0013`：Given 一个完整 `SUCCESS` 轮次含同一规范化 TransportDemandKey 的多条原始行，When 经生产 Host／领域入口写入真实 SQL Server 并由正式 API 与 Watch 查询读回，Then 只存在一个 Series 和一个当前 Demand，`DuplicateTransportDemandKeyObservation` 保存全部规范化原始行且没有主行选择、字段拼接或额外 Demand；When 后续完整轮次恢复唯一行，Then 重复条件关闭并继续同一当前 DemandId／世代。
- `REQ-0014`：Given 同一 `SUBLOT` 同时出现两个不同 `TASK_TYPE`，When 同一完整轮次经生产 Host／领域入口、真实 SQL Server、正式 API 与 Watch 查询读回，Then 两个 WorkType 形成两个不同 TransportDemandKey 和独立 Series，并在两个受影响当前 Demand 上均可见冲突证据；不得按 `SUBLOT` 合并为一个 Series。
- `REQ-0015`：Given 完整／非完整轮次以及 RestartBarrier、TaskTypeProtection 分别成立与解除的表驱动组合，When 通过生产 Host／领域入口处理并检查发布契约和正式 API 结果，Then 缺席权威只由模块从这些事实推导，受保护或非完整组合不得推进缺席生命周期，且任何生产调用面均不存在可传入并绕过保护的 `absenceAuthority` 布尔参数。
- `REQ-0016`：Given 重启前真实 SQL Server 中存在当前可见 Demand，When 服务重启后连续提交三个缺少该 Demand 的完整 `SUCCESS` 轮次并逐轮通过正式 API 与 Watch 查询读回，Then 第一轮只建立基线、第二轮只结束保护、第三轮才允许按缺席权威推进 `GONE`，前两轮不得推进 `GONE` 或归档；Given 保护期间出现新行或已有行变化，Then 对应可见 Demand 仍可创建或更新。

本批准绑定批次 `V1-APP-004`、Approval payload SHA-256 `8a46395cc69140bb99ba4d43dd93b71d0b406b2d962d031522850619bac131d8`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `14872f749075e7b725ded665afb6124ab47a678e4908cfe72aecd0885a75a4b1`，以及规范文本 SHA-256：`REQ-0013` 为 `ce8de0b5a8e2005a53542be1e0cf3535cf897f2360fedddc9de5ac0d93695b6d`、`REQ-0014` 为 `971d5388ff9bf40391962740c6fcb72c7ac48d4382d80e9d5b074956cc36668e`、`REQ-0015` 为 `d8d26d01aa75cbed37d459504673be99963062620b4625c25bea5b47ffaff30e`、`REQ-0016` 为 `41a0938badcf8ebdd8bc0b8215799a48e704dc1c12d5bde3cb0980155bdb42a7`。任一当前绑定字段变化均使本批准失效并要求重新生成、重新批准；全部 `Superseded Answer` 只保留旧总账身份下的历史证据。

只读复核确认来源文件 `.scratch/new-mes-ingest/spec.md` 的 SHA-256 为 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`，第 205–208 行与四条候选规范文本逐字一致；候选总账中的四个候选 ID、文本、范围、验证方法、来源身份和文本哈希均与本票一致；批次清单中的 `V1-APP-004`、四个候选 ID 与 approval payload 均与本票一致。候选总账生成器的 `--verify-only` 报告 348 个候选、12,452 条旧来源、363 条可追指针、来源身份漂移 0、旧来源批准升级 0；批准批次生成器的 `--verify-only` 报告 95 批覆盖 348/348、零重复、零遗漏、批准升级 0，且 manifest 身份一致。

`domain-modeling` 对照根 `CONTEXT.md` 后确认 DuplicateTransportDemandKeyObservation、WorkType、TransportDemandKey、DemandSeries、TransportDemand、GONE、RestartBarrier 与 TaskTypeProtection 的现有语义和用法没有冲突。本批没有形成新词汇或改变既有词义，因此无需修改 `CONTEXT.md`；本票只记录规划与最终批准，不触发产品测试或 Golden WPF 验证。
