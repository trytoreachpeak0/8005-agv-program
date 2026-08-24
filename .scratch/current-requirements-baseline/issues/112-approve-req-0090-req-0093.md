# 最终批准 REQ-0090–REQ-0093：Watch AREA 实时同步规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-024
Approval payload SHA-256: a572ecb4391c0ee2dc45f4c50b3d92a6b4243836db275d85584666e43309da73
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)
- **责任角色：** MesIngestWatch 产品、现场运维责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-024` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0090 — 乐观并发：Save 接受 expectedFingerprint，Rename 与 Delete 接受 ex…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0090`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 乐观并发：Save 接受 expectedFingerprint，Rename 与 Delete 接受 expectedSourceFingerprint。Fingerprint 由文件最后写入时刻的 ticks 与内容 SHA-256 组合而成。这就是冲突检测的依据，不新增 baseline 机制。
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 复用既有机制，不重造; line 92`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `6d0b3089580b8e3299167ae52dafb06bbe46092fb2fd722067604addb6642918`。

### REQ-0091 — 跨进程事务锁：目录内的锁文件，所有读写操作都在锁内进行。多实例并发已被覆盖，不新增锁。

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0091`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 跨进程事务锁：目录内的锁文件，所有读写操作都在锁内进行。多实例并发已被覆盖，不新增锁。
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 以隔离配置目录中的真实锁文件和并发进程／Store 实例验证所有读写均受同一跨进程事务锁保护，并覆盖竞争、超时、异常释放与恢复；不得用 SQL Server 事务替代文件锁证据
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 复用既有机制，不重造; line 93`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `82c0c1bb9eae3620e900b30cfc6271d1e29b7bba8777b777111bd5c6432f0208`。

### REQ-0092 — 可注入时钟：TimeProvider 已是构造参数，去抖与延迟确认直接用它。

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0092`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 可注入时钟：TimeProvider 已是构造参数，去抖与延迟确认直接用它。
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 复用既有机制，不重造; line 94`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `c4c9b3a5360a738a6b92872ffda20ff18a7e4c30acfb19512d7b5707e82f31f1`。

### REQ-0093 — 去抖；同一路径的连续事件在一个短窗口内合并为一次

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0093`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 去抖；同一路径的连续事件在一个短窗口内合并为一次
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 110`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `c2c37274a7550fe5d42b94c969ef3570a7e440767888f65e396b945344260f54`。

## Required HITL resolution

- [ ] `REQ-0090`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0091`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0092`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0093`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0090`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0091`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0092`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0093`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-024`、Approval payload SHA-256 `a572ecb4391c0ee2dc45f4c50b3d92a6b4243836db275d85584666e43309da73`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 将四项独立批准作为同一轮决策 frontier，逐项核对推荐结论、取舍与证据边界，未发现依赖分支或例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0090`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；Save、Rename 与 Delete 以各自 expected fingerprint 实施乐观并发，fingerprint 由文件最后写入 ticks 与内容 SHA-256 组成，不新增 baseline 机制。
- `REQ-0091`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；所有目录读写继续在既有跨进程事务锁内进行，多实例并发不再新增第二套锁。
- `REQ-0092`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；去抖与延迟确认直接使用既有可注入 `TimeProvider`。
- `REQ-0093`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；同一路径的连续文件事件在一个短窗口内合并为一次。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0090`：Given 编辑端持有已加载配置的 fingerprint，When Save、Rename 或 Delete 携带对应 expected fingerprint，Then 仅在当前文件最后写入 ticks 与内容 SHA-256 仍匹配时提交；不匹配时形成可观察冲突，且不得引入另一套 baseline 身份。
- `REQ-0091`：Given 同一配置目录可能被多个 Watch 实例并发访问，When 任一实例执行读取或写入，Then 操作必须在目录既有锁文件代表的跨进程事务锁内完成；脚本化生产 Host/领域入口、真实 SQL Server 与正式 API 读回仍按本票绑定的验证边界核对，现场 Oracle 事实不得由非受控证据替代。
- `REQ-0092`：Given 测试或运行实例注入既定 `TimeProvider`，When 去抖或删除延迟确认计时，Then 两者必须直接由该时钟驱动，并可通过可观察状态、审计和边界案例形成逐项验收。
- `REQ-0093`：Given 同一路径在短窗口内连续产生多个原始目录事件，When store 解释事件流，Then 对外只形成一次合并后的变更；以公开 WPF/会话 seam 验证行为，若涉及视觉、DPI 或控件布局则另按 Golden WPF 流程取得用户预览批准。

本批准绑定批次 `V1-APP-024`、Approval payload SHA-256 `979f928ede84c1e7797295ea818ba5a7338994046bc4155510d5e7a54e53cecf`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-watch-area-live-sync/spec.md` 的 SHA-256 仍为 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`，Git blob 仍为 `c6050a6102abc6b24f330187af7010fad15736b4`，第 92、93、94 与 110 行与四条候选规范文本逐字对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-024` 票据身份、责任角色、来源、四个候选 ID 与按生成器算法重算的 Approval payload 均与本票一致；清单中的 `ec71063f017a24219882c12a427e9b2d757e32e4e8a1e9032c24744c22812255` 经表头确认是 `initial_ticket_sha256`，把认领前状态规范化为 `open` 后本票初始内容哈希与之相同，并非候选总账哈希。四条规范文本的 SHA-256 已从总账规范文本独立重算并逐项一致。

domain-modeling 核对确认 `CONTEXT.md` 中 `AreaFilterProfile` 已固定为本地命名显示范围配置，且明确不改变 `WatchDemandProjection`、外部可读资格、`ExternallyReadableDemandCatalog` 或 Dispatch 的 AREA 范围，与本批作用域及首版前替代边界一致。Fingerprint、跨进程锁、`TimeProvider` 与去抖均为实现或交互机制，不应写入纯领域词汇表；本批没有改变既有领域词义，也没有产生应写入词汇表的新领域概念，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权新增外部权限、产品实现、文件删除、数据库操作、其它破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
