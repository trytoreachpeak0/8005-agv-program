# 最终批准 REQ-0094–REQ-0097：Watch AREA 实时同步规范

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-025
Approval payload SHA-256: 791617e60455fba202396511934ebf19fbf265db9129ce2fe3edcca805ff97df
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)
- **责任角色：** MesIngestWatch 产品、现场运维责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-025` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0094 — 删除延迟确认；Deleted 事件不立即视为删除；延迟确认后文件仍不存在才判定为真删除，期间同名文件重新出现…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0094`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 删除延迟确认；Deleted 事件不立即视为删除；延迟确认后文件仍不存在才判定为真删除，期间同名文件重新出现则视为内容更新
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 111`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `3150a7d85b5f58270b20cc275f3f4c29bbd00d16f1bfaf2182af8023127e56bc`。

### REQ-0095 — 改名跟随；Renamed 视为改名而非删除；正在编辑的文件跟随到新名字

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0095`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 改名跟随；Renamed 视为改名而非删除；正在编辑的文件跟随到新名字
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 112`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `a9ebf195683c5fe3d12bea0e284d5ec5ad7979c3774b741af4f50560d3cd280e`。

### REQ-0096 — 自身写入抑制；落盘时记录路径与指纹，命中的事件丢弃。不做抑制会导致「落盘 → 事件 → 重载 → 光标跳回开…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0096`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 自身写入抑制；落盘时记录路径与指纹，命中的事件丢弃。不做抑制会导致「落盘 → 事件 → 重载 → 光标跳回开头」
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 113`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `b76f8bbdbf1bf594e705a0ad6789610be0812e74a84501d67907054760e670cd`。

### REQ-0097 — 伴生文件过滤；只接受扩展名为 TXT 且文件名不以点开头的项。FileSystemWatcher 的扩展名过…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0097`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 伴生文件过滤；只接受扩展名为 TXT 且文件名不以点开头的项。FileSystemWatcher 的扩展名过滤会匹配 8.3 短名，因此回调内必须二次校验
- **适用范围：** 8005 MesIngestWatch 的 AreaFilterProfile 编辑、实时同步、冲突与删除后显示范围快照
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/mes-ingest-watch-area-live-sync/spec.md](../../../.scratch/mes-ingest-watch-area-live-sync/spec.md)；`AREA 筛选页实时同步与显示范围快照 > Implementation Decisions > 事件解释规则; line 114`；来源 SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- **来源批准边界：** 用户本人；票据 84 将该精确文件身份批准为首版候选来源；issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md。
- **形成与 AI 边界：** `table-row-preserved`；AI 参与 `none`；来源层差异：仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围。
- **首版前替代与冲突处置：** 仅替代 L1 的 AreaFilterProfile 行为；不改变外部资格、CatalogRevision 或 Dispatch 范围；按票据 84 的绑定层叠关系处置；旧来源与未批准声明保留在来源去留账，不自动合并。
- **决定／旧候选指针：** issues/84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `bbabe3e5eb494d6429ec735a35447560ce45b856cbb2f1c79123b09a6f7ab381`。

## Required HITL resolution

- [ ] `REQ-0094`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0095`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0096`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0097`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0094`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0095`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0096`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0097`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-025`、Approval payload SHA-256 `791617e60455fba202396511934ebf19fbf265db9129ce2fe3edcca805ff97df`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。

## Superseded Answer — 2026-08-24 candidate-ledger SHA correction

本节批准绑定旧候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049`，已因验证方法生成规则修正而失效；原文保留为历史证据，不再表示当前 resolved 决定。


用户本人作为当前基线最终批准人，已于 2026-08-24 明确授权后续 HITL 对话默认采用代理完整展示的推荐值，并明确要求 Wayfinder 串行接力继续处理下一票。本票已完整展示四个候选的精确规范文本、适用范围、验证方法、来源与 SHA-256、来源批准边界、AI 形成边界、替代与冲突处置、永久身份及批次绑定；本轮 grilling 将四项独立批准作为同一轮决策 frontier，逐项核对推荐结论、取舍与证据边界，未发现依赖分支或例外，因此按用户的默认推荐授权记录为逐条采用本批全部推荐值：

- `REQ-0094`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；`Deleted` 事件须经延迟确认，延迟期间同名文件重现按内容更新处理。
- `REQ-0095`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；`Renamed` 按改名处理，正在编辑的文件跟随新名字而不进入删除分支。
- `REQ-0096`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；自身落盘须记录路径与指纹并丢弃命中事件，避免自身写入触发重载与光标跳回开头。
- `REQ-0097`：批准本票所列精确文本、适用范围与验证方法进入 `v1.0.0`；回调内二次校验只接受扩展名为 TXT 且文件名不以点开头的项，封闭 `FileSystemWatcher` 对 8.3 短名的过宽匹配。

逐项 Given/When/Then 验收边界确认如下：

- `REQ-0094`：Given store 收到目标文件的 `Deleted` 事件，When 删除确认延迟尚未结束，Then 不得对外形成真删除；When 延迟结束且文件仍不存在，Then 才形成真删除；When 同名文件在延迟期间重新出现，Then 按内容更新处理。
- `REQ-0095`：Given 当前编辑会话指向一个配置文件，When store 收到该文件的 `Renamed` 事件，Then 文件与编辑会话跟随到新名字，且不得把该事件解释为删除。
- `REQ-0096`：Given Watch 自身落盘时已记录路径与指纹，When 随后目录事件同时命中该路径与指纹，Then 丢弃该事件且不得触发重载或光标跳回；未命中者不得借自身写入抑制而被静默丢弃。
- `REQ-0097`：Given watcher 回调收到候选文件事件，When 文件扩展名不是 TXT、文件名以点开头，或只是扩展名过滤因 8.3 短名产生的过宽匹配，Then 回调内二次校验必须拒绝该项；只有满足本条两个接受条件的项才进入后续处理。以公开 WPF/会话 seam 验证可观察行为，若涉及视觉、DPI 或控件布局则另按 Golden WPF 流程取得用户预览批准。

本批准绑定批次 `V1-APP-025`、Approval payload SHA-256 `791617e60455fba202396511934ebf19fbf265db9129ce2fe3edcca805ff97df`、候选总账 SHA-256 `c54e39a3d058ae5bcf10230f52cbaf24835365a083f18880a2bba3ec0ccea049` 以及本票逐条列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

只读复核确认来源文件 `.scratch/mes-ingest-watch-area-live-sync/spec.md` 的 SHA-256 仍为 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`，Git blob 仍为 `c6050a6102abc6b24f330187af7010fad15736b4`，第 111–114 行分别与四条候选规范文本对应；候选总账当前包含 348 条且 SHA-256 与票据绑定一致。批次清单中的 `V1-APP-025` 票据身份、责任角色、来源和四个候选 ID 均与本票一致；四条规范文本 SHA-256 与 Approval payload 已按生成器算法从总账字段独立重算并全部一致。清单中的 `8082e56e9bcba1323e07a59e0de563f375ea13a96e8ea98155b20f4648adb02f` 经表头确认是 `initial_ticket_sha256`，把认领前状态规范化为 `open` 后本票初始内容哈希与之相同，并非候选总账哈希。

domain-modeling 核对确认 `CONTEXT.md` 中 `AreaFilterProfile` 已固定为本地命名显示范围配置，且明确不改变 `WatchDemandProjection`、外部可读资格、`ExternallyReadableDemandCatalog` 或 Dispatch 的 AREA 范围，与本批作用域及首版前替代边界一致。删除延迟确认、改名跟随、自身写入抑制和伴生文件过滤均是文件同步交互机制，不改变既有领域词义，也没有产生应写入纯领域词汇表的新领域概念，因此无需修改 `CONTEXT.md`。

本批批准不把来源文档其它内容整篇升级为需求，不改变首版前来源替代关系，也不授权新增外部权限、产品实现、文件删除、数据库操作、其它破坏性操作或路线图范围扩张。这里只记录需求批准，不触发产品测试或 Golden WPF 验证。
