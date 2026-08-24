# 最终批准 REQ-0106–REQ-0109：Watch AREA 实时同步规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-028
Approval payload SHA-256: a56dc83f7a1c09a4fdafe3193c48c3d71163f7ae0847cd6fb64c2027a4f01fa2
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)
- **责任角色：** MesIngestWatch 产品、现场运维责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-028` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0106 — 文件内容变化——无论来自本页编辑器还是外部程序——永远不自动改变显示范围

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0106`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 文件内容变化——无论来自本页编辑器还是外部程序——永远不自动改变显示范围
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 显示范围快照; line 141`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `18d20e88ba272a3ca197c478b907ae2c3cb5bb005e971c3a71289bdb2b83c88c`。

### REQ-0107 — 只有应用动作才把解析结果写入快照

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0107`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 只有应用动作才把解析结果写入快照
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 通过隔离配置目录、可注入时钟与公开 WatchAreaFilterProfileStore／会话 seam，证明文件编辑、外部同步、非法化和删除均不改写活动快照，只有显式应用动作原子持久化解析后的 AREA 序列
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 显示范围快照; line 142`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `139f573ea9d1a526bbf69d7512820270b1d28d3db9264039f75ab71ef5b9bed8`。

### REQ-0108 — 快照不依赖文件存在或合法，进程重启后仍然有效

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0108`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 快照不依赖文件存在或合法，进程重启后仍然有效
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 通过公开 WatchAreaFilterProfileStore seam 在文件存在、非法、删除及重新创建 Store／进程重启场景中读回 .active-profile，证明最后已应用 AREA 快照保持有效；不得用 SQL Server 或 Oracle 结果替代本地活动标记证据
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 显示范围快照; line 143`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `0f11b0725bad4fb5eec841c87ec8bb197209aae0ef6abe6285ba4b5ad576c917`。

### REQ-0109 — 漂移判定比较解析后的 AREA 序列而非原始文本，因此仅修改注释或空行不算漂移

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0109`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 漂移判定比较解析后的 AREA 序列而非原始文本，因此仅修改注释或空行不算漂移
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 显示范围快照; line 144`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `a1d07211bd72c1bfaeae749a3dc62769ee534556a74cf7c2cfc180a2e32dcf3f`。

## Required HITL resolution

- [ ] `REQ-0106`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0107`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0108`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0109`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0106`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0107`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0108`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0109`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-028`、Approval payload SHA-256 `a56dc83f7a1c09a4fdafe3193c48c3d71163f7ae0847cd6fb64c2027a4f01fa2`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Comments

### 2026-08-24 — 自动批准暂停：REQ-0107／REQ-0108 验证方法与被验证边界不一致

本票已按编号顺序认领，并对来源文本、来源 SHA-256、Git blob、候选总账、规范文本 SHA-256、批次清单、Approval payload 与 `CONTEXT.md` 词汇完成只读复核。以下绑定均一致：来源 `.scratch/mes-ingest-watch-area-live-sync/spec.md` 的 SHA-256 为 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`、Git blob 为 `c6050a6102abc6b24f330187af7010fad15736b4`；候选总账 SHA-256 为 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`；四条规范文本哈希逐项匹配；按生成器算法独立重算的本批 Approval payload 为 `d1f3065a6d1200d3768f24ad4b9c6d28d6638b5d590c652feb21dca0ac0b349a`；批次 `V1-APP-028` 的来源、责任角色、票据身份及 `REQ-0106`～`REQ-0109` 成员均匹配。

但 `REQ-0107` 与 `REQ-0108` 当前绑定的验证方法不能安全按推荐批准。候选生成器 `verification_for` 仅因规范文本命中“快照”或“持久”关键词，就分配“生产 Host／真实 SQL Server／正式 API／现场 Oracle 探针”这一通用方法；来源规格第 90、139、177–179 行及现有 `MesIngest.Watch/WatchAreaFilterProfiles.cs` 则把被验证状态明确放在本地 `WatchAreaFilterProfileStore` 的 `.active-profile` 活动标记与公开存储／会话 seam。Host、SQL Server、API 和 Oracle 路径既不承载该快照，也不能证明“只有应用动作才写入”或“文件不存在／非法及进程重启后仍有效”。因此，批准当前精确验证方法会留下不可执行或不相关的验收绑定，属于不能安全自动采用推荐值的异常。

建议把两条验证方法修订为以下方向后重新生成候选、批次 payload 并重新批准；这只是建议，尚未替用户选择“修订”：

- `REQ-0107`：通过隔离配置目录、可注入时钟与公开 `WatchAreaFilterProfileStore`／会话 seam，证明文件编辑、外部同步、非法化和删除均不改写活动快照，只有显式应用动作原子持久化解析后的 AREA 序列。
- `REQ-0108`：通过同一公开存储 seam 在文件存在、非法、删除及重新创建 store／进程重启场景中读回 `.active-profile`，证明最后已应用 AREA 快照保持有效；不得用 SQL Server 或 Oracle 结果替代本地活动标记证据。

`REQ-0106` 的 WPF／会话 seam 方法与 `REQ-0109` 的可观察状态、边界案例及待确认 Given/When/Then 方法未发现同类不一致，但本票要求四项各自获得明确结论，故本轮没有批准任何一项、没有记录 `## Answer`、没有设为 `resolved`。`CONTEXT.md` 的 `AreaFilterProfile` 定义与四条规范的作用域一致；在修订决定尚未取得前不写入新的领域词汇。规划核对未运行产品测试或 Golden WPF 验证。

### 2026-08-24 — 用户授权修订并继续串行接力

用户明确授权采用上一轮给出的完整建议：修订 `REQ-0107`、`REQ-0108` 的验证方法为本地 `WatchAreaFilterProfileStore`／`.active-profile` seam 验证，`REQ-0106`、`REQ-0109` 采用推荐值，并按治理规则重新生成候选总账和批准批次、重新批准所有因候选总账 SHA-256 改变而失效的既有批次，然后继续串行接力完成全部票据。完整审计同时发现 `REQ-0091` 的本地跨进程锁文件因“事务”关键词遭到同类误分类，已用相同证据边界修正；该旧批准随全局总账哈希变化重新开放，不在本票中越票批准。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction
用户本人作为当前基线最终批准人，已于 2026-08-24 对本批四项作出明确选择。修订后的精确候选、适用范围、验证方法、来源与批次身份已经重新完整展示并完成失败式核验，未再发现哈希、来源、批次、权限、路线图范围或领域词义例外，因此结论如下：

- `REQ-0106`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；文件内容变化，无论来自本页编辑器或外部程序，均不得自动改变显示范围。
- `REQ-0107`：批准本票所列精确规范文本、适用范围及修订后的本地存储／会话 seam 验证方法进入 `v1.0.0`；只有显式应用动作才把解析后的 AREA 序列原子写入活动快照。
- `REQ-0108`：批准本票所列精确规范文本、适用范围及修订后的 `.active-profile` 读回验证方法进入 `v1.0.0`；最后已应用快照不依赖配置文件继续存在或保持合法，并在 Store 重建／进程重启后继续有效。
- `REQ-0109`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`；漂移只比较解析后的 AREA 序列，纯注释或空行变化不构成漂移。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0106`：Given 当前已应用 AREA 快照，When 编辑器保存、外部程序改写、文件事件同步或全量重扫观察到文件内容变化，Then DemandSeries 与资格审计页面继续使用原显示范围，直至用户显式应用新的合法内容。
- `REQ-0107`：Given 活动快照为 AREA 序列 `[A, B]`，When 文件被编辑、外部同步、变为非法或删除，Then `.active-profile` 仍保持 `[A, B]`；When 用户对合法序列 `[C, D]` 执行显式应用，Then 解析结果才原子持久化为 `[C, D]`。
- `REQ-0108`：Given 已持久化活动快照 `[A, B]`，When 对应文件变为非法、被删除，或销毁并重新创建 `WatchAreaFilterProfileStore`／重启进程，Then `LoadApplied()` 仍从 `.active-profile` 读回 `[A, B]`；不得用 SQL Server、API 或 Oracle 结果替代这项本地证据。
- `REQ-0109`：Given 当前文件解析为 AREA 序列 `[A, B]` 且与活动快照一致，When 只修改注释或空行，Then 解析序列仍为 `[A, B]` 且不标记漂移；When AREA 值或顺序变化导致解析序列不同，Then 标记待重新应用，但仍不自动改变显示范围。

本批准绑定批次 `V1-APP-028`、修订后 Approval payload SHA-256 `a56dc83f7a1c09a4fdafe3193c48c3d71163f7ae0847cd6fb64c2027a4f01fa2`、修订后候选总账 SHA-256 `4d102c2723d12c44bcd1e9c26a52170bbf0c27872b0e33b53c9f171d3d95a838`，以及本票逐条列出的规范文本 SHA-256。来源文件 SHA-256 仍为 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`、Git blob 仍为 `c6050a6102abc6b24f330187af7010fad15736b4`，来源第 141–144 行未变化。

确定性重建与独立复核确认：候选仍为 348 个连续唯一身份；95 张批准批次成员零遗漏零重复；修订后的批次 manifest SHA-256 为 `606d77938942f542e95a7215270268634370e536e598b2822b4848ba14fde454`；全部 95 张票的初始内容哈希均与 manifest 匹配。旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 下的批准记录已保留为 `Superseded Answer` 历史证据，但不再表示当前 resolved 决定；对应 Map 决定索引已撤回，后续从最早重新开放票据继续逐票批准。

domain-modeling 核对后，`CONTEXT.md` 的 `AreaFilterProfile` 已补记：显示范围以显式应用时持久化的 AREA 序列快照为权威，文件编辑、非法、删除或进程重启均不自行改变范围，漂移按解析序列判定。该补记不改变 `WatchDemandProjection`、外部可读资格、`ExternallyReadableDemandCatalog` 或 Dispatch 的 AREA 范围。

本票只记录需求批准和治理修正；未授权或执行产品实现、外部权限、数据库操作、文件删除或其它破坏性动作，也未运行产品测试或 Golden WPF 验证。
