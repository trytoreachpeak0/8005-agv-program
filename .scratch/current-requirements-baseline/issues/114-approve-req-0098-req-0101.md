# 最终批准 REQ-0098–REQ-0101：Watch AREA 实时同步规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-026
Approval payload SHA-256: 51bc22ed356fe21e631fe0acdd902559917510158fa22d48be471a6c909ee6c8
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)
- **责任角色：** MesIngestWatch 产品、现场运维责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-026` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0098 — 溢出兜底；订阅 Error 事件；触发时全量重扫目录并重建 watcher

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0098`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 溢出兜底；订阅 Error 事件；触发时全量重扫目录并重建 watcher
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 115`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `0cbbfbe8393741d2c91f04d3fd56350e07eaff9b6931d56bd356224c69984f51`。

### REQ-0099 — 读取重试；文件可能正被外部写入，读取失败按退避重试若干次后才报错

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0099`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 读取重试；文件可能正被外部写入，读取失败按退避重试若干次后才报错
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 116`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `ee25da3b3ac707a2746b7754f4e5eb69cb1211113eb9fdce5a6eaba5940bd68a`。

### REQ-0100 — 线程；事件在线程池线程触发，界面更新前必须切回 UI 线程

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0100`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 线程；事件在线程池线程触发，界面更新前必须切回 UI 线程
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 117`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `7be1ca0ee088913673aaca179a33baf02e4c58915f763c1930da16163432ff4e`。

### REQ-0101 — 目录失效；目录被删除或改名时停止 watcher 并定时重建，界面显示降级提示

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0101`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 目录失效；目录被删除或改名时停止 watcher 并定时重建，界面显示降级提示
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 118`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `0fef616ae2767b9b400fa28950b50cc09dafbcb0ff541e628926cd952bf5fa35`。

## Required HITL resolution

- [ ] `REQ-0098`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0099`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0100`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0101`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0098`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0099`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0100`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0101`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-026`、Approval payload SHA-256 `51bc22ed356fe21e631fe0acdd902559917510158fa22d48be471a6c909ee6c8`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 将四项独立批准作为同一轮决策 frontier，逐项核对推荐结论、取舍与证据边界，未发现依赖分支或例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0098`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；watcher 的 `Error` 事件触发全量目录重扫并重建 watcher，以兜底事件溢出。
- `REQ-0099`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；外部写入期间的读取失败须先按退避重试若干次，只有重试仍失败才报错。
- `REQ-0100`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；线程池上的文件事件在更新界面前必须切回 UI 线程。
- `REQ-0101`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；目录删除或改名后停止旧 watcher、定时重建，并在恢复前显示降级提示。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0098`：Given watcher 因事件缓冲区溢出等原因发出 `Error`，When store 处理该事件，Then 全量重扫目标目录并重建 watcher，后续对外状态以重扫结果为准，不能继续假定丢失前的增量事件链完整。
- `REQ-0099`：Given 目标文件可能正在被外部进程写入，When 一次读取失败但本轮退避重试尚未耗尽，Then 按退避继续重试且不得立即报错；When 在这些重试内成功，Then 使用成功读取结果；只有若干次退避重试仍全部失败后才报告读取错误，不在本票中臆造未由来源规定的固定次数。
- `REQ-0100`：Given 文件系统事件在线程池线程触发，When 处理结果将改变界面可观察状态，Then 必须先调度回 UI 线程再更新界面，不能从事件线程直接操作 UI。
- `REQ-0101`：Given 被监视目录被删除或改名，When store 观察到目录身份失效，Then 停止旧 watcher、显示降级提示并按周期尝试重建；When 目录重新可用且 watcher 重建成功，Then 恢复正常同步状态。以公开 WPF/会话 seam 验证可观察行为，若涉及视觉、DPI 或控件布局则另按 Golden WPF 流程取得用户预览批准。

本批准绑定批次 `V1-APP-026`、Approval payload SHA-256 `51bc22ed356fe21e631fe0acdd902559917510158fa22d48be471a6c909ee6c8`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-watch-area-live-sync/spec.md` 的 SHA-256 仍为 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`，Git blob 仍为 `c6050a6102abc6b24f330187af7010fad15736b4`，第 115–118 行分别与四条候选规范文本对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-026` 票据身份、责任角色、来源和四个候选 ID 均与本票一致；四条规范文本 SHA-256 与 Approval payload 已按生成器算法从总账字段独立重算并全部一致。清单中的 `64524f2bc3d38140d340ba3ea08d69344ed06c1231b2cb7ed4dd2ee748aee442` 经表头确认是 `initial_ticket_sha256`，把认领前状态规范化为 `open` 后本票初始内容哈希与之相同，并非候选总账哈希。

domain-modeling 核对确认 `CONTEXT.md` 中 `AreaFilterProfile` 已固定为本地命名显示范围配置，且明确不改变 `WatchDemandProjection`、外部可读资格、`ExternallyReadableDemandCatalog` 或 Dispatch 的 AREA 范围，与本批作用域及首版前替代边界一致。溢出兜底、读取重试、UI 线程切换和目录失效恢复均是文件同步交互机制，不改变既有领域词义，也没有产生应写入纯领域词汇表的新领域概念，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权新增外部权限、产品实现、文件删除、数据库操作、其它破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
