# MesIngestWatch V2 产品与交互规格

状态：已最终交接确认  
目标版本：V2  
适用范围：`.NET 8` WPF 客户端 `MesIngest.Watch`  
最后汇编：2026-08-07

## 1. 产品目标

MesIngestWatch V2 是面向现场实施与运维工程师的只读 MES 接入运维台。V2 必须让用户在启动后约 10 秒内回答三件事：

1. 当前单个 Host 是否可连接、契约是否兼容、最近一次 MesIngest 轮询是否健康；
2. 当前是否存在活动 IngestAlert，严重问题是什么；
3. 当前有哪些 VISIBLE TransportDemand，需要查看哪条 MES 输入与本地投影。

V2 不拥有投影真相，不执行调度或生产操作，也不把 Watch 自身故障写成 IngestAlert。它复用现有 MesIngest Core、SQL Server 投影和 Host 只读契约，增量替换现有 Watch 产品壳与页面状态模型。

V2 是长期 MesIngestWatch 产品概念的当前范围子集；长期领域词汇中保留的链路延迟分析能力不进入本期交付。

### 1.1 成功标准

- 使用左侧导航的四页产品壳：概览、MES 任务 / TransportDemand、IngestAlert、设置；启动进入概览。
- 一个运行实例一次只连接一个 Host；切换 Host 后不得继续显示旧 Host 的业务数据。
- 六类生产 `TASK_TYPE`、七个 MES 输入字段、TransportDemand 投影字段和六类生产 IngestAlert 均可被准确查看。
- 刷新、查询、排序、分页、取消、失败和页面切换均不造成错页、串页、旧响应覆盖或成功窗口被清空。
- 固定 100 行单页窗口；服务端筛选、稳定排序和 keyset cursor 分页；不下载全量历史在本地分页。
- 正式实现通过本规格定义的本机 Windows 功能、UIA 和视觉验收。

## 2. 范围边界

### 2.1 本期范围

- Host 连接、契约兼容性和最近轮询健康的只读查看；
- VISIBLE 与 GONE TransportDemand 的筛选、排序、游标分页、详情和复制；
- 活动与已解除 IngestAlert 的筛选、排序、游标分页、详情和关联 Demand 定位；
- 按视图手动刷新、可选自动刷新、请求取消、超时和陈旧结果表达；
- 单元格复制、整行复制、非模态详情、可调详情区和明确的本机偏好；
- 本机交互式 Windows 自动化、确定性 XAML/PNG 基线和少量真实窗口终态基线。

### 2.2 明确不做

- TransportDemand 的创建、修改、删除、派车、装卸、调度或其它生产命令；
- IngestAlert 的确认、指派、备注、手工关闭或工单化；
- 性能分析页、诊断页、PollTrace、WatchRefreshTrace、PerformanceState、遥测上报、诊断包和诊断导出；
- 多 Host 汇总、跨站点大盘和 Host 自动发现；
- 修改 Oracle 查询、增加 Oracle DDL/索引/CDC，或用 `DATES` 作为系统事件时间；
- Web、WinUI、深色主题或 WPF 以外的 UI 技术迁移；
- GitHub Actions、自托管/云端 CI runner、分支保护和专用常开测试 VM。

ADR-mes-0010 允许受限 WatchTelemetryIngest，但本规格不使用该通道；这不是对 ADR 的否定，只是 V2 当前目标不需要它。

## 3. 领域事实与显示语义

### 3.1 必须使用的概念

- **MesIngest**：轮询只读 MES 完整快照、对账并投影 TransportDemand；不读取调度侧取消抑制，不决定派车。
- **MesIngestWatch**：单 Host 的只读运维台；关闭 Watch 不影响 Host。
- **TransportDemandKey**：大小写敏感且不归一化的 `TASK_TYPE + SUBLOT`；同键同时最多一条 VISIBLE。
- **DemandId**：TransportDemand 本地实例的稳定标识；同键 GONE 后再现会得到新的 DemandId。
- **IngestAlert**：MesIngest 检出的可追踪问题实例；持续同因更新次数和最后发现时间，解除后保留历史。
- **WatchConnectionEvent**：Watch 与 Host 之间的连接、超时或契约问题；不属于 IngestAlert。
- **MesCurrentStepEnteredAt**：由 MES 字段 `DATES` 提供，表示产品进入当前工序的时间；不是 Host 观测时间或链路耗时。

### 3.2 MES 输入与 TransportDemand 投影

MES 输入固定为七列，详情中必须单独成组并保持原始字段名：

| 字段 | 含义 |
| --- | --- |
| `TASK_TYPE` | 六类搬运候选之一，也是 TransportDemandKey 的一部分 |
| `SUBLOT` | 批次标识，也是 TransportDemandKey 的一部分 |
| `AREA` | MES 区域原值，可为空或触发本地位置风险 |
| `EQP` | 来源或目标设备，具体方向由 TASK_TYPE 决定 |
| `STEP` | 下一工序标签，不是 `DATES` 所属的当前工序 |
| `DATES` | 产品进入当前 MES 工序的时间；首次投影后冻结 |
| `PACKAGE` | MES 封装信息原值 |

本地投影字段必须作为另一组显示，不能混成 MES 原始列：

| 字段 | 显示语义 |
| --- | --- |
| `DemandId` | 本地稳定实例 id，可复制 |
| `status` | 仅 `VISIBLE` 或 `GONE` |
| `mesLastSeenAt` | Host 最近一次在健康快照中观察到该实例的时间 |
| `disappearCount` | 连续健康快照缺失轮数 |
| `locationRisk` / `locationRiskCode` | `AREA_EMPTY` 或 `AREA_UNPARSEABLE` 属于 Demand 风险，不是 IngestAlert |
| `createdAt` | 本地实例创建时间 |
| `goneAt` | 本地实例转为 GONE 的时间；VISIBLE 时为空 |

`DATES`、`AREA`、`EQP`、`STEP` 和 `PACKAGE` 在实例首次创建时冻结；`FIELD_DRIFT` 不得悄悄覆盖这些值。

### 3.3 六类 TASK_TYPE

| TASK_TYPE | 搬运含义 |
| --- | --- |
| `DIE_TO_WIRE_STAGING` | 装片机台 → 焊线/键合派工待送区 |
| `DIE_TO_OVEN` | 装片机台 → 烘箱间 |
| `WIRE_TO_GATE` | 焊线/键合机台 → 人工质检关卡区 |
| `WIRE_TO_OPTICAL` | 焊线/键合机台 → 三光区 |
| `STAGING_TO_WIRE` | 焊线/键合派工待送区 → 指定焊线/键合机台 |
| `WIRE_TO_NITROGEN` | WireBond1 机台 → 固定氮气柜；不含键合 |

界面不得把 WireBond1 的 MES step 写成“焊线1”；MES 实际 step 是“焊线”。`WIRE_TO_NITROGEN` 的下一工序是 `焊线2`。

### 3.4 六类 IngestAlert

界面只允许把以下 code 作为 IngestAlert 显示：

| Code | Severity | 触发与影响摘要 |
| --- | --- | --- |
| `POLL_FAILURE` | `ERROR` | MES 快照读取失败；当轮投影不变 |
| `POLL_INCOMPLETE` | `ERROR` | 缺列或必需行值无效，无法形成完整快照；当轮投影不变 |
| `DUPLICATE_RECONCILE_KEY` | `ERROR` | 同快照内业务键重复；阻断该键对账，其它键继续 |
| `PAUSED_ZERO_DROP` | `ERROR` | 某 TASK_TYPE 从健康非零基线骤降为零；暂停该类型 GONE 判定 |
| `FIELD_DRIFT` | `ERROR` | 同一 VISIBLE 键的冻结 MES 字段发生漂移；保留原投影 |
| `REAPPEAR_AFTER_GONE` | `WARNING` | 同键在 GONE 后再现；新建 DemandId 并保留旧实例引用 |

`DUPLICATE_ACTIVE_KEY`、`MES_DATA_STALE` 和 `HOST_UNREACHABLE` 不是生产 IngestAlert code，不得出现在告警列表；Host 不可达只能显示为 Watch 连接状态。

## 4. 产品壳与视觉体系

### 4.1 页面结构

左侧导航固定为：

1. 概览
2. MES 任务 / TransportDemand
3. IngestAlert
4. 设置

不保留全局常驻 TASK_TYPE 栏或活动告警侧栏。导航中可以用克制的状态点或 `100+` 徽标提示当前缓存状态，但不得为了展示徽标额外启动后台刷新。

每页共享顶部上下文区：当前 Host（不显示凭据）、页面标题、最后成功时间、手动刷新/取消、当前页自动刷新开关与间隔。连接或契约错误使用全局横幅；业务 IngestAlert 留在概览和告警页，不混入连接横幅。

### 4.2 视觉与布局

- 默认且唯一主题为浅色工业运维风格，中文环境；状态颜色必须同时配文字或图标，不能只靠颜色表达。
- `1440×900` 是最低主基线：左侧导航保持可用；宽表允许水平滚动；选中行详情位于独立的可调区域，不随横向滚动消失。
- `2560×1440` 利用额外空间扩展表格和详情，但不改变信息层级或操作位置。
- 窗口变小时优先保住导航、页面状态、刷新/取消和详情；不得把错误、最后成功时间或当前查询隐藏到只能悬停的位置。
- 时间默认转为 Watch 本机时区显示，并提供包含偏移量的完整值用于复制；相对“多久以前”只能作辅助，不能替代绝对时间。
- 所有按钮、标签页、表头、筛选项、行和详情操作必须有稳定、语义化的 UI Automation 名称；不能依赖屏幕坐标完成关键旅程。

## 5. Host 契约与客户端 seam

### 5.1 只读接口

V2 只通过现有接口读取：

| 接口 | 用途 |
| --- | --- |
| `GET /api/contract` | 启动和新 Host 会话的契约兼容检查 |
| `GET /api/poll-health` | 最近轮询、行数、耗时、结果和 TASK_TYPE pause 状态 |
| `GET /api/demands` | VISIBLE/GONE 的服务端筛选、排序和 cursor 分页 |
| `GET /api/demands/{demandId}` | 精确 Demand 详情和 Alert → Demand 定位 |
| `GET /api/alerts` | 活动/已解除告警的服务端筛选、排序和 cursor 分页 |

`GET /api/demand-changes` 继续是既有外部同步契约，但 V2 页面不持有下游镜像，不消费 DemandChangeFeed，也不得把其 `410 SYNC_CURSOR_EXPIRED` 当成列表分页错误。

### 5.2 客户端模块接口原则

页面只面对一个按 Host 会话工作的只读查询模块。该模块的接口须统一承担鉴权、30 秒默认超时、correlation id、契约/HTTP/解码错误分类、取消、cursor 错误识别和 DTO 映射；页面不得各自拼接认证头或解释 Host 错误体。请求调度与浏览状态分别集中在单一模块内，避免四页各自实现一套过期响应判断。

测试通过与生产相同的查询和浏览接口注入 fake Host adapter；不得为测试另开会绕过取消、代次或原子提交规则的页面接口。

### 5.3 列表响应和概览计数

列表响应只有 `items`、`nextCursor`、`hasMore`，没有总数。概览不得从第一页伪造精确总量：

- `hasMore=false` 时显示本页精确数量；
- `hasMore=true` 时显示 `100+`；
- 卡片必须可下钻到相应默认查询；
- `PollHealth.rowCount` 标为“最近 MES 快照行数”，不得冒充当前 VISIBLE Demand 总数。

## 6. 共享浏览与刷新状态模型

### 6.1 Host 会话

应用新的 Host 地址或凭据即创建新 Host 会话：

1. 取消全部旧请求并永久作废旧会话的请求代次；
2. 清空概览、VISIBLE、GONE、IngestAlert 的业务缓存、cursor 路径、选择、详情、最后成功时间和旧 Host 错误；
3. 保留纯本机偏好；
4. 回到概览，先验证 `/api/contract`，再执行首次加载。

新 Host 失败或契约不兼容时必须明确显示原因，绝不继续展示旧 Host 数据。

### 6.2 四个独立视图

概览、VISIBLE、GONE、IngestAlert 各自持有：已提交查询、草稿查询、最后成功单页窗口、cursor 路径、当前页、稳定 ID 选择、详情、最后成功时间、刷新状态和自动刷新偏好。

同一次 Watch 运行期间，返回有缓存视图立即显示该视图缓存；只有其自动刷新开启时才同时重取。首次进入无缓存视图立即加载。Watch 重启后查询、页码、cursor、列表、选择和详情全部复位。

### 6.3 用户优先单飞

- 任一时刻只允许当前可见视图有一个刷新操作在执行。概览刷新操作可并发读取 PollHealth、活动 IngestAlert 与 VISIBLE TransportDemand；这些只读子请求共享取消、Host 会话和请求代次，但仍按资源独立原子提交。
- 自动刷新到点而已有请求时跳过，不排队。
- 手动刷新、翻页、提交查询、表头排序或切换页面会取消旧请求并立即开始新请求。
- 每个结果必须同时匹配当前 Host 会话、视图和请求代次；被取消、被取代或属于旧 Host 的结果不得改变列表、详情、状态栏或横幅。
- 用户主动取消显示中性“已取消”，保留成功窗口且不记连接故障；导航导致的自动取消不额外提示。

### 6.4 成功窗口原子提交

- 刷新当前页时保留最后成功数据，叠加非阻塞“刷新中”和取消入口；成功后一次性替换数据与元数据。
- 超时或失败保留旧数据，显示失败、最后成功时间和陈旧程度。
- 翻页、查询、重置或排序只有请求成功后才一起提交查询、页码、数据和 cursor 路径；失败仍停在旧页。
- 当前页刷新按 DemandId/AlertId 保持选择并更新详情；所选项不再存在时清空选择与详情并提示。
- 翻页或新查询成功后默认不选中，绝不携带上一窗口详情。

概览的多资源读取可在同一个刷新操作内并发执行，共享取消与请求代次，但各资源独立原子提交。成功卡片可以更新，失败卡片保留自己的最后成功值与时间；页面标为“部分失败”，不得把不同时间的数据伪装为同一快照。全部资源成功才标为“整体最新”。

### 6.5 自动刷新与超时

- 自动刷新默认关闭；概览、VISIBLE、GONE、IngestAlert 各自持久化开关和间隔。
- 开启时默认 10 秒，可选 10/30/60/300 秒；只有当前可见视图运行计时器。
- 切回已开启自动刷新的视图立即刷新一次；启动后的概览首次加载始终立即执行。
- 成功、失败、超时或主动取消后，从请求终止时重新等待完整间隔；手动刷新也重置计时。
- 自动失败不立即重试，不做指数退避。
- 全局请求超时默认 30 秒，设置合法范围 1–300 秒；变更只影响后续请求。
- 超时属于真实连接失败：保留旧数据，显示 endpoint、等待时长、最后成功时间和 correlation id，并写入既有连接事件日志。

### 6.6 分页和 cursor 恢复

- VISIBLE、GONE、IngestAlert 固定 `limit=100`，使用“上一页 / 第 N 页 / 下一页”；不显示未知总页数，不提供任意跳页或页大小选择器。
- 第 1 页的到达 cursor 为空；下一页使用当前成功响应的 `nextCursor`；上一页重放客户端保存的到达 cursor。
- 仅当 `hasMore=true` 且 `nextCursor` 非空时启用下一页。
- 当前页任何成功重取都会丢弃该页之后的旧前进路径，以新 `nextCursor` 为准。
- cursor 类 `400` 清空该查询的页路径并仅自动重试一次第 1 页；成功后提示“数据已变化，已返回第 1 页”。再次失败时保留旧窗口，不循环重试。
- 筛选、时间范围、排序或 limit 等其它 `400` 原样显示具体错误，不自动恢复。

## 7. 页面规格

### 7.1 概览

概览按从上到下的优先级展示：

1. **Host 接入状态**：Host 地址、连接/鉴权/契约状态、最近成功连接时间；错误横幅提供设置入口和 correlation id。
2. **最近轮询健康**：`success/outcome`、`endedAt`、`durationMs`、最近 MES 快照 `rowCount`、`failureStage`（有值时）和 PAUSED_ZERO_DROP 的 TASK_TYPE。未有 PollHealth 时明确显示“尚无成功轮询”，不能显示绿色健康。
3. **活动 IngestAlert**：默认 `active=true`、Host 默认优先级的第一页，显示精确 `0..100` 或 `100+`；突出 ERROR，展示前三条的 code、scope、最后发现时间，点击进入告警页同一默认查询。
4. **VISIBLE TransportDemand**：默认 VISIBLE 查询第一页，显示精确 `0..100` 或 `100+`；按六类 TASK_TYPE 汇总当前窗口并标明“当前页”，点击进入任务页 VISIBLE 默认查询。

健康结论必须区分：连接失败、契约不兼容、尚无轮询、最近轮询失败、PAUSED_ZERO_DROP、存在活动 ERROR、仅 WARNING、健康和部分失败。当前连接失败不得清除上次成功业务值，但所有保留值都必须标记各自最后成功时间与“陈旧”。

### 7.2 MES 任务 / TransportDemand

#### 结构

- 页内以 `VISIBLE`、`GONE` 两个标签页分隔；二者是完全独立的浏览视图。
- 上方为显式筛选区和当前已提交查询摘要；中部为单页表格；下方或右侧为可调详情区。
- `1440×900` 下详情区必须持续可见，表格可水平滚动。

#### 默认查询

- VISIBLE：`status=VISIBLE&sortBy=dates&direction=desc&limit=100`，无时间窗。
- GONE：`status=GONE&goneAtFrom=<当前时刻-24h>&sortBy=goneAt&direction=desc&limit=100`。
- 服务端始终以 DemandId 作为稳定次排序键；客户端不得重新排序当前页来冒充全局排序。

#### 筛选

- TASK_TYPE：六类精确选择，可清空；
- SUBLOT：文本；
- DemandId：完整值或 6–32 位小写十六进制前缀；客户端先校验并转小写；
- VISIBLE 提供 `DATES` 起止；GONE 提供 `goneAt` 起止；
- 筛选输入是草稿。点击“查询”并通过本地校验后请求第 1 页；成功才提交。
- “重置”恢复当前标签默认查询并立即请求第 1 页。

#### 表格和排序

表格显示并允许复制：DemandId、TASK_TYPE、SUBLOT、AREA、EQP、STEP、当前工序进入时间 `DATES`、PACKAGE、status、mesLastSeenAt、disappearCount、locationRisk/locationRiskCode、createdAt、goneAt。只有 Host allow-list 中的 DemandId、TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE、status、mesLastSeenAt、disappearCount、locationRisk、createdAt、goneAt 提供服务端排序；`locationRiskCode` 只显示和复制，不显示可排序手势。点击可排序表头是一次显式查询，切换升/降序并回第 1 页。

默认固定 DemandId、TASK_TYPE、SUBLOT 和 DATES 的识别优先级；其余列可横向查看。长值省略时必须能通过详情和复制得到完整内容。

#### 详情与操作

- 详情明确分为“MES 输入（创建时冻结）”和“本地 TransportDemand 投影”两组。
- 支持双击/显式“查看详情”、右键复制当前单元格、复制整行和复制 DemandId；右键菜单不得用复制动作替代查看详情。
- 详情只读；没有任何编辑、创建、删除或派车入口。
- GONE 后同键再现不自动追踪到其它实例；用户可从 `REAPPEAR_AFTER_GONE` 告警的明确操作查看旧/新 DemandId。

### 7.3 IngestAlert

#### 默认查询与筛选

- 默认 `active=true&limit=100`，不显式传 `sortBy`，沿用 Host 的 ERROR→WARNING、同级 lastSeenAt 倒序优先级。
- 提供活动/已解除切换，以及 code、severity（ERROR/WARNING）和 `lastSeenAt` 时间范围；现有 `/api/alerts?from=&to=` 只按最后发现时间过滤。`firstSeenAt` 保留显示与排序，但不作为 V2 筛选条件。所有输入遵循草稿—查询—成功提交模型。
- “重置”恢复活动告警默认查询；点击可排序表头改为 Host allow-list 排序并回第 1 页。

#### 表格和排序

显示 AlertId、Code、Severity、TASK_TYPE、SUBLOT、DemandId、Message、FirstSeenAt、LastSeenAt、OccurrenceCount、IsActive、ResolvedAt。Code、Severity、AlertId、LastSeenAt、FirstSeenAt、TASK_TYPE、SUBLOT、DemandId、Message 通过 Host allow-list 服务端排序；其它列不显示可排序手势。

#### 详情与关联 Demand

非模态详情完整显示 `alertId/code/severity/taskType/sublot/demandId/message/details/firstSeenAt/lastSeenAt/occurrenceCount/isActive/resolvedAt/createdAt`。详情和列表全程只读。

- 有 DemandId：提供“查看 TransportDemand”，先用 `/api/demands/{demandId}` 精确读取，再进入实际 status 标签，以 DemandId 查询第 1 页并选中该行。
- `REAPPEAR_AFTER_GONE` 的 details 同时包含旧 GONE id 与新 DemandId 时，两者分别提供复制和精确查看动作，并明确标注“先前 GONE”“当前再现”。
- 无 DemandId 但有 TASK_TYPE + SUBLOT：提供“按业务键查任务”，由用户明确触发后进入 VISIBLE 标签并提交这两个筛选；不得宣称已定位唯一历史实例。
- 无任何 Demand 关联信息：不显示不可用的跳转按钮。

### 7.4 设置

设置页只包含：

- 单个 Host 基址；
- 只读 API 凭据输入与应用；凭据始终掩码，不回显到日志、错误或证据包；
- 全局请求超时（默认 30 秒，1–300 秒）；
- 概览、VISIBLE、GONE、IngestAlert 的自动刷新开关和 10/30/60/300 秒间隔；
- 明确的本机布局偏好（窗口大小、详情分隔位置等）及“恢复默认布局”；
- “测试连接”只执行契约和健康读取，不建立第二个并行 Host 会话。用户点击“应用”即开始新 Host 会话：先取消并作废旧会话、清除旧 Host 业务状态，再验证新 Host；验证失败时停留在无旧业务数据的新会话错误状态。

不出现性能阈值、trace、遥测存储、保留期、诊断导出、告警处置或多 Host 配置。

## 8. 错误、陈旧与空状态

| 状态 | 必须行为 |
| --- | --- |
| 首次加载 | 显示页面骨架、忙碌和取消；不借用其它视图数据 |
| 空结果 | 显示“当前查询无结果”和已提交查询摘要；不是连接错误 |
| 手动刷新 | 保留成功窗口并显示刷新中 |
| 用户取消 | 保留成功窗口，显示中性已取消，不记故障 |
| 超时/网络/鉴权 | 保留成功窗口；显示 endpoint、等待时长、最后成功和 correlation id |
| 契约不兼容 | 阻止业务数据读取，显示本地/Host 契约版本和设置入口 |
| 非 cursor 400 | 显示 Host 具体校验错误，保留原已提交查询和窗口 |
| cursor 400 | 仅一次自动回第 1 页；失败后保留旧窗口 |
| 选择项消失 | 清空选择和详情并给出一次性提示 |
| 部分概览失败 | 每张卡显示自己的最后成功时间；整页标为部分失败 |

状态栏与横幅不能闪逝到无法阅读。WatchConnectionEvent 本地记录失败不得改变 HTTP 成功结果，也不得阻塞后续刷新；本地日志有界保留并脱敏。

## 9. 本地持久化与安全

允许跨 Watch 重启保存：Host 基址、凭据的既有安全引用方式、全局超时、四个自动刷新偏好、窗口尺寸和详情分隔位置。

禁止跨重启保存：业务列表、详情、选择、查询草稿/提交值、cursor、页码、最后成功业务时间和 Host 错误。应用新 Host 时同样清除这些 Host 相关状态。

测试和视觉证据只能使用假数据；日志、截图、UIA tree、fake Host 时间线和异常文本不得含明文凭据或生产数据。

## 10. 可验证验收标准

### 10.1 功能与流畅性

- Host 人为延迟 30 秒时，触发刷新后 250 ms 内出现忙碌状态和取消入口。
- 请求等待期间，导航、筛选输入和取消在 500 ms 内获得界面反馈。
- 被取消、被取代和旧 Host 响应最终返回时，均不能改变可见状态。
- 收到 100 行响应后 1 秒内完成可交互呈现。
- VISIBLE、GONE、IngestAlert 分别验证前进两页、返回、当前页重取后前进路径更新、cursor 失效一次恢复和导航失败留在原页。
- 查询失败不提交草稿；排序、重置和翻页仅在成功后改变已提交状态。
- 当前页刷新保持稳定 ID 选择；选择项消失时清空详情；新查询和翻页不继承详情。
- 新 Host 会话不能短暂或永久显示旧 Host 的列表、详情、错误或最后成功时间。
- 概览卡片在 `hasMore=true` 时显示 `100+`，不得显示伪精确总数。
- 连接失败、PollHealth 失败、PAUSED_ZERO_DROP 和活动 ERROR IngestAlert 的视觉与术语互不混淆。

### 10.2 自动化栈

正式实现采用独立 xUnit v3 UI 测试项目：

- `FlaUI.UIA3 5.0.0`：真实关键旅程；
- `Verify.Xaml 4.2.1`：确定性 WPF 页面 XAML/PNG 快照；
- 少量真实窗口截图：高价值终态视觉回归；
- Core、Host、HTTP 和 Watch 非回归测试继续保留；SQL Server 场景在具备 LocalDB/SQL Server 的本机环境运行。

统一的本机入口必须在已登录的交互式 Windows 会话中串行运行 `watch-vm-tests`、`watch-xaml-visual`、`watch-ui-journeys`、`watch-window-visual`。入口先校验活动桌面、分辨率、DPI、浅色主题、中文区域、字体和渲染模式；环境不符时停止视觉套件并报告差异，不生成新基线。程序集和桌面交互均不得并行。

### 10.3 视觉基线

`Verify.Xaml` 在 100% DPI、浅色主题、中文环境下：

- `1440×900`：概览健康、退化/活动告警、离线陈旧；任务 VISIBLE 已选、GONE 已选、空、加载、失败保留旧结果；告警活动已选、已解除、空、加载、失败保留旧结果；设置默认、校验错误。
- `2560×1440`：概览、任务、告警、设置各一个正常已加载页面。
- 假数据覆盖六类 TASK_TYPE、七个 MES 字段、全部投影字段、六类生产 IngestAlert 和中文长文本。

FlaUI 真实窗口固定五个 `1440×900` 客户区终态：冷启动概览、VISIBLE/GONE 分页及任务详情、Alert → Demand 定位、慢请求取消并保留旧结果、离线后恢复连接。125%/150% DPI 只做布局和 UIA 烟测，不作像素比较；深色主题不进入 V2。

### 10.4 基线与 flaky 治理

- 基线只能通过显式本机流程生成；同一快照连续 10 次完全一致后才能提出更新。
- 更新包含原因、关联规格/票据、before/after/diff 和环境清单；由非提交者复核，交互/文案/层级/状态色变化还需产品或业务确认。
- 测试首次失败保持失败；重跑只用于诊断。成为本机发布门禁前连续通过 50 次。
- 同一测试连续 20 次中有 2 次、或滚动 100 次中有 3 次非产品失败即判 flaky；隔离必须有负责人、修复票和最长 7 天期限。
- 禁止全局像素容差和大面积 mask；修复后连续通过 50 次才恢复门禁。
- 失败证据包包含 expected/actual/diff PNG、Verify received XAML、关键步骤截图、UIA tree、Watch 日志和标准输出/错误、fake Host 请求时间线与脱敏摘要、步骤/异常/超时及环境清单；仅崩溃或无响应时附 dump。

## 11. 实现交接边界

本规格定义产品行为和可验证接口，不把现有 throwaway 原型直接提升为生产实现。实现规划可以重构现有 Watch XAML、页面状态和客户端模块，但必须：

- 保留 MesIngest 领域核心、Host 只读契约、DemandChangeFeed 外部契约和现有数据语义；
- 不另建投影真相，不把页面缓存提升为业务状态；
- 不删除既有能力，除非本规格提供等价或更强的替代并已有测试覆盖；
- 对外 API/DTO、cursor、schema 或时间语义若确需不兼容变化，必须另行版本化、提供升级路径，并同步运行时与离线 OpenAPI；
- 保留当前工作树中的用户在途改动，不重置或覆盖；实现时逐项判断其是否满足本规格。

## 12. 决策追溯

- [建立现有能力与回归边界](issues/01-establish-current-capability-and-regression-baseline.md)
- [选择 WPF 自动化与视觉回归测试栈](issues/02-choose-wpf-automation-and-visual-regression-stack.md)
- [识别现有 IngestAlert 与 MES 任务形态](issues/07-define-alert-demand-diagnostics-and-export-boundary.md)
- [定义流畅刷新、游标分页与取消模型](issues/08-define-responsive-refresh-paging-and-cancellation-model.md)
- [固定 WPF 截图基线与 Windows CI 证据规则](issues/11-lock-wpf-screenshot-baselines-and-windows-ci-evidence-rules.md)
- [验证以 MES 任务与 IngestAlert 为中心的简化 WPF 原型](issues/13-validate-task-and-alert-centered-wpf-prototype.md)
- ADR-mes-0006：MesIngest 与调度拆开
- ADR-mes-0007：Service + WPF + SQL Server
- ADR-mes-0008：完整源快照与本地增量投影/有界读取分离
- ADR-mes-0009：DemandChangeFeed 与权威 Bootstrap
- ADR-mes-0010：Watch 业务只读，可选受限遥测追加

## 13. 最终交接检查表

- [x] 产品/业务确认四页信息架构、页面字段、文案和范围边界；
- [x] 实现负责人确认现有 Host 契约能支撑全部查询和跳转；
- [x] 测试负责人确认本机环境、四套入口、视觉矩阵和证据规则可落地；
- [x] 规格歧义已在最终评审中消除，且没有需要另开的拟议契约变化；
- [x] [确认 V2 实现交接](issues/10-accept-v2-implementation-handoff.md) 完成最终人工评审。
