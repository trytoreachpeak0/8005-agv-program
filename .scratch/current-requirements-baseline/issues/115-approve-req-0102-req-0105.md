# 最终批准 REQ-0102–REQ-0105：Watch AREA 实时同步规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-027
Approval payload SHA-256: e55bbcc94a24a1d78d8f62f5a018ed7f6e1c24b0ca1a491e02c362064a6ea01d
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)
- **责任角色：** MesIngestWatch 产品、现场运维责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-027` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0102 — 有；干净；静默重载，保持光标、选区、滚动位置

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0102`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 有；干净；静默重载，保持光标、选区、滚动位置
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 编辑器同步模型; line 126`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `50b53563b02fd1a575c919dad1d2e80fc688f71adaa5c5bf896370d172e195d5`。

### REQ-0103 — 有；脏；保留本地输入；落盘时指纹不匹配则提示冲突

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0103`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 有；脏；保留本地输入；落盘时指纹不匹配则提示冲突
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 编辑器同步模型; line 127`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `894522a1fb5a3da533b3343aa0b5bb58b7a2e9d9c5b13ea8eb4f9e882f7a6fb6`。

### REQ-0104 — 有；内容与缓冲逐字节相同；不动，避免光标无谓跳动

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0104`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 有；内容与缓冲逐字节相同；不动，避免光标无谓跳动
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 编辑器同步模型; line 128`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `b519e7790785a6d98d361929187fed2d20fdd4c042992d9276b323a212f537f5`。

### REQ-0105 — 无；任意；无操作

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0105`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 无；任意；无操作
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 编辑器同步模型; line 129`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `8b9e23074b02c001beb7d6a5fd94095b064af84ac7400b1f5dc8068189b460b2`。

## Required HITL resolution

- [ ] `REQ-0102`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0103`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0104`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0105`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0102`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0103`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0104`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0105`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-027`、Approval payload SHA-256 `e55bbcc94a24a1d78d8f62f5a018ed7f6e1c24b0ca1a491e02c362064a6ea01d`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 将四项独立批准作为同一轮决策 frontier，逐项核对推荐结论、取舍与证据边界，未发现依赖分支或例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0102`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；磁盘文件存在且编辑器干净时静默重载，并保持光标、选区和滚动位置。
- `REQ-0103`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；磁盘文件存在且编辑器为脏时保留本地输入，落盘时若指纹不匹配则提示冲突。
- `REQ-0104`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；磁盘内容与编辑器缓冲逐字节相同时不执行重载或其它动作，避免光标无谓跳动。
- `REQ-0105`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；磁盘文件不存在时，无论编辑器缓冲状态如何均不执行操作。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0102`：Given 目标文件存在且编辑器缓冲干净，When 实时同步确认磁盘内容发生变化并成功读取，Then 静默重载磁盘内容，同时保持既有光标、选区与滚动位置，不把重载表现为用户编辑。
- `REQ-0103`：Given 目标文件存在且编辑器缓冲为脏，When 实时同步观察到磁盘变化，Then 保留本地输入而不以磁盘内容覆盖；When 随后尝试落盘且当前磁盘指纹与编辑基点不匹配，Then 提示冲突并不得静默覆盖外部修改。
- `REQ-0104`：Given 目标文件存在且磁盘内容与编辑器缓冲逐字节相同，When 文件事件或全量重扫再次观察该内容，Then 不重载、不改写缓冲，也不移动光标、选区或滚动位置。
- `REQ-0105`：Given 目标文件不存在且编辑器缓冲可处于任意状态，When 文件事件或全量重扫评估编辑器同步行为，Then 不执行操作，不因本条自行清空、重载或改写缓冲。

本批准绑定批次 `V1-APP-027`、Approval payload SHA-256 `e55bbcc94a24a1d78d8f62f5a018ed7f6e1c24b0ca1a491e02c362064a6ea01d`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-watch-area-live-sync/spec.md` 的 SHA-256 仍为 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`，Git blob 仍为 `c6050a6102abc6b24f330187af7010fad15736b4`，第 126–129 行分别与四条候选规范文本对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-027` 票据身份、责任角色、来源和四个候选 ID 均与本票一致；四条规范文本 SHA-256 与 Approval payload 已按生成器算法从总账字段独立重算并全部一致。清单中的 `ee15585b2eb531102fca55b8c35f25c67dca61a51c49d4c418cb933c482e5d4a` 经表头确认是 `initial_ticket_sha256`，把认领状态规范化为 `open` 后本票初始内容哈希与之相同，并非候选总账哈希。

domain-modeling 核对确认 `CONTEXT.md` 中 `AreaFilterProfile` 已固定为本地命名显示范围配置，且明确不改变 `WatchDemandProjection`、外部可读资格、`ExternallyReadableDemandCatalog` 或 Dispatch 的 AREA 范围，与本批作用域及首版前替代边界一致。干净／脏缓冲、静默重载、指纹冲突及无操作是编辑器同步机制，不改变既有领域词义，也没有产生应写入纯领域词汇表的新领域概念，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权新增外部权限、产品实现、文件删除、数据库操作、其它破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
