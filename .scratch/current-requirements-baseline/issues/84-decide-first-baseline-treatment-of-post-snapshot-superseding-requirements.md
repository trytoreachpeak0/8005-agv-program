# 决定首版基线如何处理初始快照后的替代性需求

Type: grilling
Status: resolved
Blocked by: 81

## Question

初始需求证据快照固定于 2026-08-03、但首个 `v1.0.0` 当前基线尚未发布时，仓库又形成了明确整体替换旧 MesIngest 数据库、契约、Watch 和 `IngestAlert` 生命周期语义的《新版 MesIngest 整体替换规格书》；首版基线应如何保持“当前”且不破坏已批准的不可变版本与变更门禁：是为这些快照后材料建立补充证据快照、验证来源与最终批准后直接纳入 `v1.0.0`，还是先把原快照路线发布为历史版本并立即以受控主版本替代，或采用其它可审计的版本边界？

决定必须同时固定：

- 哪些快照后材料属于首版候选，哪些只作实现或历史证据；
- 《新版 MesIngest 整体替换规格书》的具名批准人、批准时间、适用范围、Git/blob/SHA-256 身份和与旧 V2 的替代关系；
- 旧 V2 中已被新版明确废弃的 `IngestAlert` incident、365 天保留、可选自动刷新和旧 cursor/Feed 规则不得在哪个基线版本继续作为当前要求；
- 若首版不直接吸收新版，如何避免把明知已被替代的旧语义对外标记为“当前基线”；
- 新增、修改、废弃需求如何生成永久需求 ID、`Supersedes` 关系、精确差异和批准记录。

## Evidence

- [MesIngestWatch V2 运维定义回流核对](../evidence/mes-ingest-watch-v2-operability-reconciliation-2026-08-24.md)
- 初始快照基点：`1469d6309d00b0abb792f6cd686aed68286e638e`
- 本问题浮现时 HEAD：`4e2205ad5fde874c320ef90b7148ee99121d4129`
- 《新版 MesIngest 整体替换规格书》：`.scratch/new-mes-ingest/spec.md`，blob `9104575426c60f71ed8020d3d231c3332e2c0589`，SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`
- 既有治理决定：[确定版本化基线模式](08-versioned-baseline-model.md)、[决定基线版本的存储与变更治理形式](09-baseline-release-storage-and-change-governance.md)、[固定初始需求证据快照](10-capture-initial-evidence-snapshot.md)

## Answer

用户本人作为[当前需求基线默认且唯一的最终批准人](03-final-baseline-approver.md)，于 2026-08-24T12:44:57+08:00 对本票第一轮全部推荐值明确回复“全部用推荐值，后续也全部用推荐值”。该授权允许本票其余依赖分支在逐项明确展示结论、取舍与证据边界后继续采用推荐值；它不扩张到新增外部权限、破坏性操作或路线图范围变化。

### 首版与补充快照边界

- 首个正式批准基线尚未发布，因此截至首版候选冻结点的最新获批要求直接进入 `v1.0.0`。语义版本号比较正式批准基线，不比较证据快照、规格草稿或实现提交；不得先发布一个明知已过时的历史 `v1.0.0` 再立即以 `v2.0.0` 纠正。
- 初始证据快照保持不可变。另建一份 **PreReleaseSupplementalEvidenceSnapshot（首版发布前补充证据快照）**，宽口径捕获 2026-08-03 初始快照之后至补充快照截止点新增或变化的全部需求性材料，并记录截止时间、Git/工作区身份、逐文件 SHA-256、来源和分类；补拍本身不构成批准。
- 补充快照截止后出现或变化的材料不得静默进入冻结的 `v1.0.0` 候选：要么在最终批准前显式重开补充快照、重新核验受影响差异并取得绑定身份的批准，要么按正式发布后的变更门禁进入后续版本。

### 首版候选、支持证据与历史材料

补充快照必须宽口径盘点；当前已经明确可进入首版规范候选的来源层如下，最终仍须拆成可独立批准的原子需求，而不是整份文件自动成为一个批准单元：

1. [《新版 MesIngest 整体替换规格书》](../../new-mes-ingest/spec.md)作为新版 MesIngest 的基础来源。
2. [《MesIngest 有界存储与低内存运行规格书》](../../mes-ingest-bounded-storage-low-memory/spec.md)作为对基础来源中永久详细历史、恢复和存储边界的后续替代层。
3. [《AREA 筛选页实时同步与显示范围快照》](../../mes-ingest-watch-area-live-sync/spec.md)作为 `AreaFilterProfile` 编辑、同步和删除后范围快照行为的后续替代层。
4. [《DemandSeries 单实例 Inspector：E 世代调查工作台》](../../demand-series-inspector-e/spec.md)作为 DemandSeries 旧内联详情信息架构的后续替代层。
5. [回流并核对 MesIngestWatch V2 运维定义](81-reconcile-mes-ingest-watch-v2-operability-definitions.md)中已确认的跨版本一致边界。

ADR、原型选择、视觉批准记录和其它决定记录作为来源、取舍、适用范围或批准证据，不能因文档类型自动整篇升级为需求。实现票、代码、测试结果、发布包和黄金机产物只作实现或验收证据。旧 Phase 1、旧 V2、旧实现规格及已被替代内容只作历史证据；其中仍有效的义务只能通过上列跨版本核对或当前候选的明确证据链进入首版。

### 绑定批准身份与适用范围

用户本次批准绑定以下当前文件字节；Git 作者和提交只证明来源，不能单独代替本批准记录：

| 来源 | Git blob | SHA-256 |
| --- | --- | --- |
| `.scratch/new-mes-ingest/spec.md` | `9104575426c60f71ed8020d3d231c3332e2c0589` | `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f` |
| `.scratch/mes-ingest-bounded-storage-low-memory/spec.md` | `099feeef433a0b356c41c90e221ee7d5bafcface` | `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6` |
| `.scratch/mes-ingest-watch-area-live-sync/spec.md` | `c6050a6102abc6b24f330187af7010fad15736b4` | `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0` |
| `.scratch/demand-series-inspector-e/spec.md` | `2b4a2b326a3df2635e56977b22feb8686d0c0cca` | `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657` |

批准范围限定为 8005 的 MesIngest Windows Service、Host/领域投影、SQL Server 持久化、版本化 API/OpenAPI、MesIngestWatch，以及 MesIngest 对外可读目录边界；不扩张到 Dispatch 执行、OnboardHmi 业务、修改客户 Oracle SQL/DDL 或自动删除现场数据库。整份规格绑定批准只确认其可作为首版候选来源及相互替代顺序；实际基线仍须按原子粒度形成规范文本、证据和条目批准记录。

### 来源层叠与旧语义处置

1. 《新版 MesIngest 整体替换规格书》整体替代旧数据库、旧契约、旧 Watch 数据模型和旧 `IngestAlert` incident。
2. 《MesIngest 有界存储与低内存运行规格书》只进一步替代其中 GONE 明细、错误历史、关键原文永久保留以及相关恢复/容量边界；其余新版领域语义继续有效。
3. AREA 实时同步规格只替代 `AreaFilterProfile` 的编辑、同步、冲突和删除后范围快照行为。
4. Inspector E 规格只替代 DemandSeries 旧内联详情信息架构，不改变 DemandSeries、Demand 世代或事件领域契约。
5. 旧 V2 的六类 `IngestAlert` incident、已解除告警 365 天保留、可选自动刷新、旧 DemandChangeFeed/high-watermark/410 cursor 规则不得在 `v1.0.0` 中继续作为当前义务；只有单 Host 业务只读、会话/查询/请求代次隔离、失败保留并标记最后成功快照、告警不可处置及 Watch 故障不成为业务告警等已核对的一致边界继续有效。

这一关系称为 **PreBaselineSourceSupersession（首版前来源替代）**：替代必须由绑定版本、范围、精确差异和本次批准证明，不能只因材料时间较新而推定。

### 永久需求身份与差异规则

- `v1.0.0` 相对“无正式前版”的当前有效要求全部记为 `Added` 并取得新的永久 `REQ-NNNN`。
- 首版前多份来源逐步修订同一义务时，只形成一个最终有效规范条目；其 Evidence 保存每层来源、逐层精确差异、适用范围、冲突处置和本票批准记录。
- `Supersedes` 只连接已经建立的永久 REQ。不得为从未进入正式基线的旧规格语句虚构 deprecated REQ；这类关系记录为来源层的 PreBaselineSourceSupersession。
- `v1.0.0` 发布后，纯新增取得新 ID；普通语义修改保留原 ID并记录精确差异；本质替代取得新 ID、以 `Supersedes` 指向旧 ID并把旧 ID 标记 deprecated；单纯废弃保留旧 ID并标记 deprecated。所有 ID 永不回收或复用。

本决定不直接生成补充快照或首版文件；这些是后续任务。`CONTEXT.md` 已即时加入上述两个治理术语，未写入任何实现细节或把未批准材料升级为需求。
