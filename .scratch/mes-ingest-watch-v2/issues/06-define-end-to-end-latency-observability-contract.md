# 定义端到端延迟可观测契约

Type: grilling
Status: resolved
Blocked by: 01

## Question

怎样定义轮询与 Watch 请求的结构化 trace、阶段边界、correlation、数据年龄、阈值、P50/P95/最大值、30 天原始与 365 天聚合保留及只读查询契约，才能准确分析 MES→MesIngestWatch 延迟，又不把统计异常混入 IngestAlert？

## Comments

- 2026-08-07：用户确认将链路建模为相互独立但显式关联的 `PollTrace` 与 `WatchRefreshTrace`。Watch 响应引用实际读取到的 PollTrace；`ProjectionVisibilityLag` 按同一 PollTrace 的投影提交至页面呈现计算，无法关联时为未知；`MesDataAge` 独立按 `MesCurrentStepEnteredAt` 计算，不属于系统链路耗时。
- 2026-08-07：用户确认长期稳定的一级阶段。PollTrace 为 `MES_READ`、`INGEST_RECONCILE`、`PROJECTION_COMMIT`；WatchRefreshTrace 为 `WATCH_REQUEST`、`HOST_QUERY`、`WATCH_DECODE`、`WATCH_PRESENT`。SQL open/query/transaction、连接与超时等保留为可扩展诊断子阶段；根耗时与阶段耗时分别统计，嵌套或并行阶段不得简单求和。
- 2026-08-07：用户确认分层 correlation：轮询使用持久化 `PollTraceId`，一次页面刷新共享 `WatchRefreshTraceId`，每个 HTTP 请求另有唯一 `RequestSpanId`；阶段记录 Trace/Span/ParentSpan 关系。读取投影的响应返回 `ObservedPollTraceId` 与 `ProjectionCommittedAt`；`X-Correlation-Id` 作为 WatchRefreshTraceId 的兼容映射保留。一次刷新读到多个 PollTrace 时记录“跨轮次读取”，不宣称单一一致快照。
- 2026-08-07：用户确认增加唯一的非业务写入口 `POST /api/telemetry/watch-traces`，用于受控、追加式、异步批量接收 WatchRefreshTrace。入口沿用 Host 访问控制并限制 DTO、大小和批量条数；不得上传任意日志、敏感信息或修改 TransportDemand、IngestAlert、PollHealth/投影。上报失败不得阻塞 Watch；除该遥测入口外，正式业务 API 继续只读 GET。
- 2026-08-07：用户确认以 UTC 5 分钟左闭右开桶，按 TraceType、一级阶段、页面/端点模板、Outcome 分组；根 trace 与子阶段、成功/失败/超时/用户取消分开统计。保存样本/结果计数、P50、P95、精确最大值及可合并分布；30 天内从原始 span 得出精确百分位，之后以 5 分钟可合并直方图得出标注“约”的百分位，禁止平均各桶 P95。少于 20 个样本标记不足且不驱动性能状态。ProjectionVisibilityLag 仅纳入成功、同 PollTrace 可关联样本；MesDataAge 使用独立指标族。
- 2026-08-07：用户确认独立的 `PerformanceState`，状态为 HEALTHY/DEGRADED/CRITICAL/INSUFFICIENT_DATA。每 5 分钟用最近 30 分钟 P95 评估，至少 20 个有效样本；连续 2 个窗口超阈值进入降级/严重，连续 3 个窗口低于警告阈值恢复。Max 只作诊断；失败/超时/离线由既有即时状态表达，用户取消不算失败；慢成功只写可查询性能评估记录，绝不生成 IngestAlert。评估保留阈值版本、窗口、样本数和触发指标。
- 2026-08-07：用户确认首版可配置 P95 阈值（DEGRADED/CRITICAL）：PollTrace 总耗时 15s/25s，MES_READ 8s/20s，INGEST_RECONCILE 500ms/2s，PROJECTION_COMMIT 10s/20s，WatchRefreshTrace 总耗时 3s/8s，WATCH_REQUEST 2s/5s，HOST_QUERY 1.5s/4s，WATCH_DECODE 200ms/750ms，WATCH_PRESENT 250ms/1s；配置必须 warning < critical 且版本化。自动刷新 ProjectionVisibilityLag 阈值为刷新间隔+3s/两倍刷新间隔+8s，手动刷新不据等待时间降级；MesDataAge 不设全局性能阈值。多项越界显示最高状态与最具体阶段。
- 2026-08-07：用户确认原始 trace/span 默认保留 30 天、5 分钟聚合与性能评估默认 365 天，时间或容量先到者为准。SQL 遥测默认总预算 2 GiB（可配 256 MiB–20 GiB），其中 Poll 原始 512 MiB、Watch 原始 1 GiB、聚合/评估 512 MiB；只清理已聚合关闭桶，依次清理最旧 Watch 原始、Poll 原始、最后聚合，绝不触碰业务数据。查询暴露 earliest available、实际保留、容量截断和清理结果；容量/迟到/丢弃属于诊断而非 IngestAlert。Watch 本机日志维持独立的 30 天/100 MiB 默认限制。
- 2026-08-07：用户确认跨机时间模型：阶段 duration 只用进程内单调时钟，UTC 只作排序/取证。Host 响应返回 ServerObservedAt、ServerProcessingMs、ProjectionCommittedAt、ObservedPollTraceId；Watch 以客户端往返减服务端处理估算网络往返，并用中点法估算时钟偏移和误差。误差 ≤500ms 才计算/聚合 ProjectionVisibilityLag，超限则未知且不进入百分位/PerformanceState；时钟偏移绝对值 >2s 显示诊断警告但不建 IngestAlert。MesDataAge 由 Host 计算返回，Watch 不以本机时钟重算。
- 2026-08-07：用户确认 Watch 遥测采用本机持久化队列的至少一次发送与 Host 幂等接收；队列默认 50 MiB/24h，淘汰最旧并计数。后台批次最多 100 span/256 KiB，不参与刷新完成；Host 以 (TraceId, SpanId) 去重并分别返回 accepted/duplicate/rejected 与稳定原因码，单条无效不连累同批有效项。接受原始 30 天窗内迟到数据，客户端时间超 Host 当前时间 5 分钟则拒绝统计并标记时钟异常；离线指数退避、恢复从最旧未确认项继续。记录客户端观察与 Host 接收时间，失败不阻塞 UI、不建 IngestAlert。
- 2026-08-07：用户确认只读查询资源：`GET /api/observability/status`（当前性能/阈值/数据质量），`series`（默认 30m，精确原始最长 30d、近似聚合最长 365d），`traces`（白名单筛选、默认 100/最大 500、StartedAt DESC + TraceId ASC 稳定游标），`traces/{traceId}`（waterfall 与关联），`retention`（可用边界/容量/清理/丢弃）。超保留边界返回 410 TELEMETRY_WINDOW_EXPIRED，游标/筛选错误返回稳定 400；不支持任意 SQL、任意排序或全文日志。Demand/Alert/PollHealth 版本化补充观察元数据，所有契约进入 OpenAPI 与 `/api/contract` 门禁。
- 2026-08-07：用户确认结构化记录采用字段白名单：版本、Trace/Span/Parent/Linked/ObservedPoll 标识，组件/阶段，起止/单调时长，Outcome/稳定 FailureCode，随机实例标识，页面/方法/路由模板/状态码，行数/字节数，投影/服务端时间、时钟校准及统计资格。禁止密钥、连接串、凭证、SQL/参数、完整 URL/查询值、正文、SUBLOT/DemandId/AlertId/设备号、用户名/机器名/IP/路径、原始堆栈与未白名单异常消息。具体 Demand/Alert 关联留给诊断边界票。

## Answer

MesIngestWatch V2 采用两条独立但显式关联的因果链：`PollTrace` 覆盖 MES 快照读取至投影提交，一级阶段为 `MES_READ`、`INGEST_RECONCILE`、`PROJECTION_COMMIT`；`WatchRefreshTrace` 覆盖刷新触发至首次可见呈现，一级阶段为 `WATCH_REQUEST`、`HOST_QUERY`、`WATCH_DECODE`、`WATCH_PRESENT`。轮询、刷新和请求 span 分别使用 PollTraceId、WatchRefreshTraceId、RequestSpanId，并以 Parent/Linked/ObservedPoll 关系关联；一次刷新读到不同 PollTrace 时必须标明跨轮次，不宣称一致快照。`X-Correlation-Id` 仅作为 WatchRefreshTraceId 的兼容映射。

`ProjectionVisibilityLag` 只按可关联同一 PollTrace、跨机校准误差不超过 500ms 的成功刷新计算；跨轮次、无法关联或误差超限均为未知并排除统计。阶段 duration 使用进程内单调时钟，UTC 只作排序/取证；Host–Watch 偏移超过 2s 显示诊断警告。`MesDataAge` 由 Host 以 MesCurrentStepEnteredAt 计算，是独立业务年龄指标，不属于链路性能。

原始 span 以 UTC 5 分钟左闭右开桶，按 TraceType、一级阶段、页面/端点模板和 Outcome 分组。成功、失败、超时、用户取消及根/子阶段分别统计，保留样本/结果计数、P50、P95、精确 Max 与可合并分布；30 天内提供精确百分位，30 天后从 5 分钟直方图提供标注“约”的可合并百分位，禁止平均各桶 P95。少于 20 个样本为 `INSUFFICIENT_DATA`。

`PerformanceState` 独立于 IngestAlert，使用最近 30 分钟 P95、每 5 分钟评估：连续 2 个窗口越界进入 DEGRADED/CRITICAL，连续 3 个窗口低于警告线恢复。慢成功只产生版本化性能评估；失败、超时和离线仍由 PollHealth/连接故障即时表达。首版 P95 警告/严重阈值为：PollTrace 15s/25s、MES_READ 8s/20s、INGEST_RECONCILE 500ms/2s、PROJECTION_COMMIT 10s/20s、WatchRefreshTrace 3s/8s、WATCH_REQUEST 2s/5s、HOST_QUERY 1.5s/4s、WATCH_DECODE 200ms/750ms、WATCH_PRESENT 250ms/1s。自动刷新 ProjectionVisibilityLag 使用“间隔+3s”/“两倍间隔+8s”；手动刷新等待和 MesDataAge 不触发性能降级。

Host/SQL Server 保存权威结构化遥测。为保存客户端阶段，允许唯一非业务写入口 `POST /api/telemetry/watch-traces`（见 [ADR-mes-0010](../../../docs/adr/mes/0010-watch-business-read-only-with-telemetry-ingest.md)）：严格白名单、追加式、受访问控制且不得修改任何业务投影。Watch 以 50 MiB/24h 本机持久队列至少一次发送，单批最多 100 span/256 KiB；Host 以 `(TraceId, SpanId)` 幂等去重并逐项返回 accepted/duplicate/rejected。上传离线、迟到、丢弃或时钟异常不阻塞 UI、不形成 IngestAlert。

原始 trace 默认保留 30 天，5 分钟聚合/性能评估默认 365 天；时间或容量先到者为准。SQL 遥测默认预算 2 GiB（Poll 原始 512 MiB、Watch 原始 1 GiB、聚合 512 MiB，可配 256 MiB–20 GiB），只清理已聚合关闭桶且绝不触碰业务数据。API 必须公开最早可用时间、实际保留、容量截断、聚合/清理和丢弃状态。

只读查询面固定为 `/api/observability/status`、`series`、`traces`、`traces/{traceId}`、`retention`；采用白名单筛选、稳定游标、显式 Exact/Approximate 与稳定 400/410 错误。Demand、Alert、PollHealth 响应版本化补充 ObservedPollTraceId、ProjectionCommittedAt 和服务端计时。结构化 span 只允许确认的标识、阶段、计时、Outcome、安全维度和统计资格字段；密钥、连接串、SQL、请求/响应正文、业务标识、机器/用户身份及未白名单异常内容一律禁止。具体物理 schema、索引、聚合/清理作业和版本化 DTO 由后续[固定可观测数据物理存储与版本化 API DTO](12-lock-observability-storage-and-versioned-api-dtos.md)继续决定。
