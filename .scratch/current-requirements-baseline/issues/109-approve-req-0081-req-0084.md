# 最终批准 REQ-0081–REQ-0084：有界存储与低内存规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-021
Approval payload SHA-256: d764f1a7f3fc154d6a9ecd22c4ed42709bbf45fa8a0e1e23b8f8231762f62c30
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)
- **责任角色：** SQL Server、容量与存储责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-021` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0081 — 切换顺序固定为：只读重建旧环境反馈环；在独立空库验证新包、快速容量预测和加速并发稳定性；按风险信号或用户明确…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0081`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 切换顺序固定为：只读重建旧环境反馈环；在独立空库验证新包、快速容量预测和加速并发稳定性；按风险信号或用户明确要求升级完整规模/长时间验证；计划 30–60 分钟停机；停止旧 Host；创建新库与 HistoryEpoch；播种并证明墓碑；启动精确新包；连续完成三轮成功投影；验证 contract/schema、主要 Watch API、ExternallyReadableDemandCatalog 和 reference consumer；验证精确旧库身份；生成外部证据；自动删除旧库；撤销临时权限并结束运行。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 174`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `50c61baf313822888b05717c24bb5bcc43bd2b102100019effeb8fb0366dacf9`。

### REQ-0082 — MesIngestCutoverRun 必须由唯一 CutoverRunId 标识，且全部门禁、证据与删除属…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0082`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** MesIngestCutoverRun 必须由唯一 CutoverRunId 标识，且全部门禁、证据与删除属于同一运行。日常 Host 不包含、调用或持有删库能力。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 175`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `16001ca45c32ce722fca8df09b24f65ad2bfe3e2753840ff8eac2455220f3f98`。

### REQ-0083 — 删除目标必须同时满足：显式旧库名；不是系统库或新库；匹配预期旧 schema/contract；数据文件位于…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0083`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 删除目标必须同时满足：显式旧库名；不是系统库或新库；匹配预期旧 schema/contract；数据文件位于解析后的预期 SQL 数据目录；旧 Host 已停止且没有业务连接；墓碑数量与稳定哈希一致；所有门禁属于当前 CutoverRunId。禁止通配、前缀和自动猜测。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 176`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `c8cc43b63db18781403c686301ff6b23a2f2387ea2255194c6700b9eb40be1dd`。

### REQ-0084 — 任一切换门禁失败都禁止删除、保留新旧库、以失败退出且不后台重试。删除失败同样保留可检查状态；再次尝试必须由操…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0084`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 任一切换门禁失败都禁止删除、保留新旧库、以失败退出且不后台重试。删除失败同样保留可检查状态；再次尝试必须由操作员发起新的明确 MesIngestCutoverRun。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 177`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `5393ec76b7d6579fe1c8a445435400c323c147616eec02acac187d0ec5e53602`。

## Required HITL resolution

- [ ] `REQ-0081`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0082`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0083`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0084`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0081`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0082`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0083`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0084`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-021`、Approval payload SHA-256 `d764f1a7f3fc154d6a9ecd22c4ed42709bbf45fa8a0e1e23b8f8231762f62c30`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 将四项独立批准作为同一轮决策 frontier，逐项核对推荐结论、取舍与证据边界，未发现依赖分支或例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0081`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；切换按只读反馈环、独立空库验证、风险升级验证、停机、停旧 Host、建新库/纪元、墓碑证明、精确新包、三轮成功投影、契约/API/消费者核验、旧库身份与外部证据、旧库删除和临时权限撤销的固定顺序执行。
- `REQ-0082`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；一次切换由唯一 `CutoverRunId` 贯穿全部门禁、证据和删除，日常 Host 不得包含、调用或持有删库能力。
- `REQ-0083`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；只有显式旧库身份、非系统/新库、预期 schema/contract、解析后 SQL 数据目录、旧 Host 停止且无业务连接、墓碑数量与稳定哈希、当前运行归属七项门禁同时成立才可删除，并禁止通配、前缀或猜测。
- `REQ-0084`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；任一门禁或删除失败均保留可检查的新旧库状态、失败退出且不后台重试，再试必须由操作员发起新的明确切换运行。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0081`：Given 已绑定旧/新库身份、精确包和计划停机窗口，When 执行切换，Then 各阶段必须按规范文本顺序完成，且三轮成功投影、契约/API/目录/消费者、旧库身份与外部证据门禁全部成立后才进入删除与撤权。
- `REQ-0082`：Given 操作员发起具名 `MesIngestCutoverRun`，When 产生任一门禁、证据或删除动作，Then 它们均归属同一唯一 `CutoverRunId`；When 日常 Host 运行，Then 不存在可由其包含、调用或持有的删库能力。
- `REQ-0083`：Given 存在待删除的明确旧库，When 评估删除资格，Then 七项合取门禁必须全部通过；任一项不成立或目标来自通配、前缀、猜测时，Then 不得执行删除。
- `REQ-0084`：Given 当前切换的任一门禁或删除动作失败，When 该运行退出，Then 新旧库与失败状态保持可检查且没有后台重试；When 需要再次尝试，Then 必须由操作员发起具有新身份的明确 `MesIngestCutoverRun`。

本批准绑定批次 `V1-APP-021`、Approval payload SHA-256 `d764f1a7f3fc154d6a9ecd22c4ed42709bbf45fa8a0e1e23b8f8231762f62c30`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-bounded-storage-low-memory/spec.md` 的 SHA-256 仍为 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`，Git blob 仍为 `099feeef433a0b356c41c90e221ee7d5bafcface`，第 174–177 行与四条候选规范文本逐字对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-021` 票据身份、责任角色、来源、四个候选 ID 与按生成器算法重算的 Approval payload 均与本票一致。四条规范文本的 SHA-256 已从总账规范文本独立重算并逐项一致；把认领前状态规范化为 `open` 后，本票初始内容 SHA-256 为清单登记的 `ad1a1e796ce5b2b22b0e9b8a5e498e545d3101dd1b591a0bdc23329aa053c971`。

domain-modeling 核对确认 `CONTEXT.md` 中 `MesIngestCutoverRun` 已固定唯一 `CutoverRunId`、一次性受控运行、旧库自动删除、临时权限失效及禁止无人值守重试/前缀删库的边界；`HistoryEpoch`、`ArchivedDemandKeyTombstone` 与 `ExternallyReadableDemandCatalog` 的既有词义也与本批切换、墓碑证明及目录验证一致。本批没有改变既有领域词义，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实际数据库切换、删库、权限授予、产品实现、破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
