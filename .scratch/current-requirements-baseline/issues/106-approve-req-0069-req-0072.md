# 最终批准 REQ-0069–REQ-0072：有界存储与低内存规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-018
Approval payload SHA-256: 2e1f8328ee2ac81de83012aea5e588782f001bd5073fdf71f552695ce7731352
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)
- **责任角色：** SQL Server、容量与存储责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-018` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0069 — 存储监控针对数据库实际数据卷。低于 15% 产生严重告警；低于 10% 在查询 MES 之前进入 Stora…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0069`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 存储监控针对数据库实际数据卷。低于 15% 产生严重告警；低于 10% 在查询 MES 之前进入 StoragePressurePause。暂停不取得新快照、不推进缺席、GONE 或归档判断。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 162`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `878504d14f78aceb78f86f1143e3d0c39f0880f93852e19b7bf9d4eac2dac577`。

### REQ-0070 — StoragePressurePause 期间 Watch 诊断与历史读取继续服务，ExternallyRe…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0070`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** StoragePressurePause 期间 Watch 诊断与历史读取继续服务，ExternallyReadableDemandCatalog 与执行承诺读取返回 503 INGEST_NOT_CURRENT。空间回升不自动恢复，恢复只由 MesIngestLocalAdministration 提交。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 163`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `a0b2bde85fd314c879631bc668ca6844d0a91cd963212a8da8bbcfebc34bb259`。

### REQ-0071 — MesIngestLocalAdministration 是数据库主机上的本地 CLI/PowerShell…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0071`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** MesIngestLocalAdministration 是数据库主机上的本地 CLI/PowerShell 管理边界。HistoryResetAcknowledgement 和 StoragePressurePause 恢复都记录执行身份、目标 HistoryEpoch、前后状态、原因和 Host UTC 时间；Watch 不提供写按钮或远程管理 API。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 164`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `8ff9286a297c100170311284ac40342b96b4022e1e0d95bb342ec91da3d2f24b`。

### REQ-0072 — 新库固定 SIMPLE 恢复且无数据库备份。系统仍监控 LDF 大小、增长与 log reuse wait；…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0072`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 新库固定 SIMPLE 恢复且无数据库备份。系统仍监控 LDF 大小、增长与 log reuse wait；禁止 FULL 恢复但不做日志备份的组合。
- **适用范围：** 8005 MesIngest 的 GONE 明细、错误历史、原始证据保留、恢复、容量及低内存存储边界
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-bounded-storage-low-memory/spec.md](../../../.scratch/mes-ingest-bounded-storage-low-memory/spec.md)；`MesIngest 有界存储与低内存运行规格书 > Implementation Decisions; line 165`；来源 SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅在声明范围内替代 L1；L1 其余领域语义继续有效。
- **首版前替代与冲突处置：** 仅在声明范围内替代 L1；L1 其余领域语义继续有效；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `3b7303c7cf36328e1864caaa04141be593e6a462916fca185fa8ec311bd51d1c`。

## Required HITL resolution

- [ ] `REQ-0069`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0070`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0071`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0072`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0069`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0070`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0071`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0072`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-018`、Approval payload SHA-256 `2e1f8328ee2ac81de83012aea5e588782f001bd5073fdf71f552695ce7731352`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 又逐项核对推荐结论、取舍与证据边界，只读复核未发现例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0069`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；存储压力暂停在查询 MES 前生效，不取得新快照，也不推进缺席、GONE 或归档判断。
- `REQ-0070`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；暂停期间 Watch 诊断和历史读取继续服务，外部当前目录与执行承诺读取按候选返回 503，且空间回升不构成自动恢复。
- `REQ-0071`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；恢复与历史重置确认只经数据库主机本地管理边界提交并完整审计，Watch 不取得写入或远程管理能力。
- `REQ-0072`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`，并确认应以来源决定的可观察状态、审计记录及边界案例形成逐项 Given/When/Then 验收。

本批准绑定批次 `V1-APP-018`、Approval payload SHA-256 `2e1f8328ee2ac81de83012aea5e588782f001bd5073fdf71f552695ce7731352`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-bounded-storage-low-memory/spec.md` 的 SHA-256 仍为 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`，Git blob 仍为 `099feeef433a0b356c41c90e221ee7d5bafcface`，第 162–165 行与四条候选规范文本逐字对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-018` 票据身份、责任角色、来源、四个候选 ID 与重算 Approval payload 均与本票一致。四条规范文本的 SHA-256 已从来源文本独立重算并逐项一致；把认领前状态规范化为 `open` 后，本票初始内容 SHA-256 为清单登记的 `7d06e2b7eb17bc71b1644d4337b0763df5bef64dfc445b2f39ef6e2dfea00cf5`。

`CONTEXT.md` 中 `StoragePressurePause`、`MesIngestLocalAdministration`、`HistoryResetAcknowledgement`、`HistoryEpoch` 与 `ExternallyReadableDemandCatalog` 的现有词义和本批一致。15%/10% 数据卷阈值、503 响应、SIMPLE 恢复模式、LDF 监控与无数据库备份属于本批运行规范和验证边界，不构成需要新增的领域词汇，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权实现、数据库配置变更、备份删除、外部权限、破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
