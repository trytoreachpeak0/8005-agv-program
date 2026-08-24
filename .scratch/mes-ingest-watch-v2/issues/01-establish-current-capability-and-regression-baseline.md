# 建立现有能力与回归边界

Type: task
Status: resolved
Blocked by: None

## Question

现有 MesIngest Host、MesIngestWatch、规格/ADR、测试以及当前工作树中的在途改动，哪些能力应保留复用、哪些应由 V2 替换、哪些构成不得回退的兼容与验收边界？

## Answer

V2 采用“保留 MesIngest 领域核心与 Host 只读契约，增量重做 MesIngestWatch 产品壳和观测能力”的路线；不另建第二套投影真相，也不以新 UI 反向重写已经稳定的接入语义。依据为 `CONTEXT.md`、ADR-mes-0006～0009、`mes-ingest-phase-1`、`mes-ingest-watch-operations`、后续 review-remediation/test-reliability 票据、当前代码与测试。

### 必须保留复用

- **边界与权威**：MesIngest 继续只轮询只读 MES 完整快照、对账并投影 TransportDemand；不读取调度侧取消抑制，不建业务任务、不派车。MesIngestWatch 继续是单 Host、只读薄客户端，关闭 Watch 不影响 Host。（ADR-mes-0006、ADR-mes-0007）
- **TransportDemand 语义**：DemandId 是稳定实例标识；TransportDemandKey 是 `TASK_TYPE + SUBLOT` 且同键最多一条 VISIBLE；首次投影冻结 MES 字段；完整成功轮次才推进缺失；默认连续两轮缺失转 GONE；同键跨 GONE 再现创建新 DemandId 并保留旧实例；字段漂移、重复键、行级不完整、PAUSED_ZERO_DROP、重启首轮屏障与上线基线过滤不得回退。
- **持久化与读取模型**：Oracle 仍提供完整活动快照；SQL Server 只写本轮差异，GONE 永久保留但退出热路径；schema 升级保持事务化和数据不丢失。（ADR-mes-0008）
- **Host 只读 API**：保留 `/api/contract`、`/api/demands`、`/api/demands/{demandId}`、`/api/alerts`、`/api/poll-health`、`/api/demand-changes` 及运行时/离线 OpenAPI。Demand 与 Alert 继续服务端筛选、全部可见列稳定排序、keyset cursor 分页，非法查询稳定返回 400；契约不兼容时 Watch 必须明确报错而不是空白。
- **DemandChangeFeed**：CREATED/GONE 与 Demand 同事务写入单调 sequence；默认有限保留，过期 cursor 返回 `410 SYNC_CURSOR_EXPIRED`；消费者用“全部 VISIBLE + 最近 24 小时 GONE + high watermark”权威替换后追增量。（ADR-mes-0009）
- **IngestAlert**：保持可追踪问题实例、同因累计与解除时间，不退回逐轮重复消息。Alert 与 WatchConnectionEvent 继续分离；REAPPEAR 的旧/新 DemandId、详情、精确定位和历史提示继续可用。
- **Watch 可靠性底座**：各资源保留最后成功窗口；请求失败、慢 Host、过期 cursor、刷新冲突均不得清空或混排数据。Demand/Alert 浏览状态与 cursor 独立；当前页窗口可重建；过期响应不得覆盖新状态；本地连接/延迟日志 IO 失败不得改变成功 HTTP 刷新结果，日志保留有界且秘密必须脱敏。
- **既有操作能力**：所有可见列的服务端排序、Load more、组合筛选、单元格/整行复制、Alert 非模态详情、REAPPEAR 旧/新实例操作、可调窗格和本地布局偏好均作为 V2 功能下限，不因换导航或视觉体系消失。

### 允许由 V2 替换或升级

- 现有单窗格 Demand/Alert 盯盘布局、控件样式、颜色、密度、信息层级和文案可由六区域导航整体替换；旧 XAML 不是视觉兼容契约。
- 现有全局定时刷新可替换为“默认手动、按页可选自动刷新、只刷新当前页”的模型，但必须继续满足单飞、可取消、不排队、状态变更请求可最终执行、过期响应隔离和最后成功窗口保留。
- 当前以 Watch 本地文本日志为主的延迟取证可降为辅助证据；Host/SQL Server 中的结构化 poll/trace、阶段耗时、聚合和保留将成为权威观测面。`MesCurrentStepEnteredAt` 仍只表示 MES 数据年龄，不能改称链路耗时。
- 当前横幅与状态栏的具体展示规则可重新编排，但连接失败、Host poll 失败/未就绪、PAUSED_ZERO_DROP、陈旧数据和恢复状态都必须在约 10 秒健康判断路径中可见；IngestAlert 不得被混成 Watch 自身连接故障。
- 当前 xUnit v2 单项目中的轻量 WPF 测试可迁入独立 xUnit v3 UI 测试项目；核心/Host 合约测试继续保留。新增 FlaUI.UIA3 真实旅程和 Verify.Xaml 快照后，旧测试只有在等价或更强覆盖已落地时才能删除。

### 当前工作树的处理

当前未提交改动新增 SoftwareOnly/Auto 渲染配置、可配置 Watch 日志目录、Alert 详情显式按钮与 FlaUI UIA3 旅程，并把活动 IngestAlert 从通知横幅移回 Alerts 网格。这些是需要保留且不得覆盖的在途候选实现，不自动成为 V2 最终产品规则；横幅归属、默认渲染模式和日志目录最终写入规格时仍须与原型、自动化和现场环境一起确认。V2 规划不得重置或改写这些文件。

### 验收基线

- 2026-08-04 在当前工作树执行 `dotnet test MesIngest.sln --configuration Release --no-restore`：四个项目均完成 Release 编译；406 通过、7 失败、19 跳过。7 个失败均发生在受限执行环境：2 个 `HttpListener` 返回“句柄无效”，5 个启动测试无法读取用户 `%LocalAppData%` 布局文件；19 个为未提供 SQL Server/LocalDB 条件的持久化测试。它们是 runner 环境要求，不作为 V2 可接受的产品失败。
- 当前新增 `MainWindowUiAutomationTests.Alert_details_control_opens_detail_window_through_flaui_uia3` 单独运行 1/1 通过，证明 Alert 详情按钮可经真实 UIA3 调用打开正确详情窗。
- V2 合并门禁的最低线是：现有 Core/Host/HTTP/Watch 非回归套件全绿；SQL Server 场景在具备 LocalDB/SQL Server 的 runner 全跑；UIA/截图测试在固定交互式 Windows runner 运行。任何外部 API/DTO、cursor、ChangeFeed、schema 或时间语义变化都必须显式版本化、提供升级路径，并用运行时与离线 OpenAPI 同步验收。
