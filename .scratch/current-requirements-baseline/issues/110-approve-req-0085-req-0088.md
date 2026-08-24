# 最终批准 REQ-0085–REQ-0088：有界存储与低内存规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-022
Approval payload SHA-256: e84ec20e23a41c9f570adcb3df97b3cfd1f1302ae5dfda4f61b54255a2e9e4da
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)
- **责任角色：** SQL Server、容量与存储责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-022` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0085 — 删除前在数据库外写不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志，记录实例、旧/…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0085`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 删除前在数据库外写不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志，记录实例、旧/新库身份、HistoryEpoch、版本、墓碑证明、三轮投影、接口检查、执行账号和时间。证据不得包含业务原文，也不构成备份。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 178`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `f8ecd12228c30a9d9df77f1cebdad451c9d14a795279aad19186d755e50935f7`。

### REQ-0086 — 旧库删除后没有历史或版本回滚路径，后续故障只在新库与新契约上向前修复。

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0086`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 旧库删除后没有历史或版本回滚路径，后续故障只在新库与新契约上向前修复。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 179`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `983626d25bf69e78c3b167ab8f44f012423e6c716520dee0c13cec21a2f11b41`。

### REQ-0087 — 运行遥测至少覆盖：SQL Server 配置与进程内存、workspace/grant、Error 701、…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0087`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 运行遥测至少覆盖：SQL Server 配置与进程内存、workspace/grant、Error 701、RESOURCE_SEMAPHORE、spill、当前态逻辑读、查询延迟、轮询节奏与退避、清理进度与失败、最早可用历史、HistoryEpoch、StoragePressurePause、数据库逻辑已用空间、MDF/NDF/LDF 物理大小、压缩状态与 log reuse wait。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 180`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `ed62e5630dbb3a775a73d93a72ec7c19cdcecd52c66371c54e3a308c1daad5f7`。

### REQ-0088 — 默认发布门禁固定为：代表性压缩负载下常用 Watch API P95 < 2 秒、P99 < 5 秒；没有 …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0088`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 默认发布门禁固定为：代表性压缩负载下常用 Watch API P95 < 2 秒、P99 < 5 秒；没有 Error 701、持续 RESOURCE_SEMAPHORE 或不可接受 spill；当前态逻辑读不随代表性历史规模增长；30–45 分钟高强度并发压力和加速 24 小时逻辑周期稳定；带 30% 安全余量的 30 天预测满足逻辑已用空间 ≤ 12 GB、物理数据库文件 ≤ 16 GB、LDF 目标 ≤ 2 GB。任一预测达到对应门槛的 70%、增长呈非线性、证据不完整，或压力运行出现持续资源斜率、清理积压、延迟恶化时，必须升级完整规模或 4/24 小时 soak；用户也可在正式现场切换前明确要求升级。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 181`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `cb77017fdbb1c2056f5fd877078c7b15722d5664c918094ece56747f87ac323e`。

## Required HITL resolution

- [ ] `REQ-0085`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0086`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0087`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0088`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0085`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0086`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0087`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0088`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-022`、Approval payload SHA-256 `e84ec20e23a41c9f570adcb3df97b3cfd1f1302ae5dfda4f61b54255a2e9e4da`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 将四项独立批准作为同一轮决策 frontier，逐项核对推荐结论、取舍与证据边界，未发现依赖分支或例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0085`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；旧库删除前必须在数据库外形成不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志，完整绑定规定的切换身份与核验证据，同时不包含业务原文且不冒充备份。
- `REQ-0086`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；旧库删除后不存在历史或版本回滚路径，后续故障只允许基于新库与新契约向前修复。
- `REQ-0087`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；运行遥测至少覆盖票列 SQL Server 内存与资源、查询与轮询、清理与历史、存储压力、文件空间、压缩及日志复用等待指标。
- `REQ-0088`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；默认发布门禁采用规定的 API 延迟、资源异常、逻辑读稳定性、并发与加速周期、30 天容量预测阈值，并在达到任一风险触发器、证据不足或用户明确要求时升级完整规模或长时间 soak。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0085`：Given 当前切换已绑定实例、旧/新库、HistoryEpoch、版本、墓碑证明、三轮投影、接口检查、执行账号和时间，When 进入旧库删除前门禁，Then 必须在数据库外写出不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志；证据不得包含业务原文，也不得被解释为备份。
- `REQ-0086`：Given 旧库已经按门禁删除，When 后续发生故障或版本问题，Then 不得尝试历史或版本回滚，只能在新库与新契约上向前修复。
- `REQ-0087`：Given 生产 Host、真实 SQL Server 持久化与正式 API 处于运行或受控验证轮次，When 采集和读回运行遥测，Then 本票规范文本列出的 SQL Server、资源、查询、轮询、清理、历史、暂停、空间、压缩与日志指标必须全部可核对；现场 Oracle 事实只能由受控探针证明。
- `REQ-0088`：Given 代表性压缩负载与规定的并发、加速周期和容量预测证据，When 评估发布资格，Then 所列延迟、资源、逻辑读、稳定性及容量门槛必须全部满足；When 任一预测达到对应门槛 70%、增长非线性、证据不完整，或压力运行出现持续资源斜率、清理积压、延迟恶化，Then 必须升级完整规模或 4/24 小时 soak；模拟结果不得冒充现场通过。

本批准绑定批次 `V1-APP-022`、Approval payload SHA-256 `e84ec20e23a41c9f570adcb3df97b3cfd1f1302ae5dfda4f61b54255a2e9e4da`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-bounded-storage-low-memory/spec.md` 的 SHA-256 仍为 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`，Git blob 仍为 `099feeef433a0b356c41c90e221ee7d5bafcface`，第 178–181 行与四条候选规范文本逐字对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-022` 票据身份、责任角色、来源、四个候选 ID 与按生成器算法重算的 Approval payload 均与本票一致。四条规范文本的 SHA-256 已从总账规范文本独立重算并逐项一致；把认领前状态规范化为 `open` 后，本票初始内容 SHA-256 为清单登记的 `874356689d473b0896d38f53b2108e11b63f0a80f395ae4f6aee875d7c246b71`。

domain-modeling 核对确认 `CONTEXT.md` 中 `MesIngestCutoverRun` 已固定一次性受控运行、旧库自动删除与禁止无人值守重试的边界，`HistoryEpoch` 与 `StoragePressurePause` 的既有词义也与本批证据、遥测及发布门禁一致。本批没有改变既有领域词义，也没有产生应写入词汇表的新领域概念，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实际数据库切换、删库、权限授予、产品实现、破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
