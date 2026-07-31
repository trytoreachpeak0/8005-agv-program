# MesIngest Watch Operations and Scalable Read Model

Status: ready-for-agent

## Problem Statement

MesIngest Phase 1 已能从客户批准的只读 Oracle 查询生成 TransportDemand，并由 WPF Watch 展示，但当前运维与读取路径存在可用性和规模问题：时间显示混用 UTC/默认格式；Watch HTTP 超时写死且故障易闪逝；Demand 列表缺少可扩展分页、DemandId 快速查询和完整表格交互；Alert 只有通用 Message 且同一持续问题每轮重复插入；SQL Server 每轮删除重建全部投影并把永久 GONE 历史带入热路径；未来持有本地镜像的下游程序无法可靠增量获得 CREATED/GONE。

客户 MES SQL 与 Oracle 结构不属于本系统控制范围。MesIngest 必须继续只读执行批准的完整活动快照，不修改 SQL、不执行 DDL；性能改进集中在本地 SQL Server 投影、API、Watch 和可观测性。

## Solution

将 MesIngest 的“完整源快照语义”与“本地增量持久化/有界读取”分开：Reconciler 仍以完整成功快照判断存在与消失，SQL Server 只写本轮差异并让永久 GONE 退出热路径；列表 API 使用服务端筛选、稳定排序、索引和游标分页；另提供持久化 DemandChangeFeed 供下游镜像同步 CREATED/GONE。Watch 同步升级为分页薄客户端，并补齐一致时间显示、复制、可调布局、结构化 Alert 详情、底部状态栏、可靠横幅、连接事件日志和 Swagger 人工测试入口。

## Confirmed Domain Semantics

- **MesCurrentStepEnteredAt** 对应 MES/API 字段 `DATES`：产品进入当前工序的时间；`STEP` 指下一工序，不是 DATES 所属工序。
- TransportDemand 首次创建后冻结 TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE 等业务字段。
- API 与 Watch 默认按 `DATES DESC, DemandId ASC` 排序；`MesLastSeenAt` 只表示 Host 最近一次观察到该 Demand。
- 所有 VISIBLE 都属于下游当前镜像，不受 DATES 是否超过 24 小时限制。
- GONE 的“最近 24 小时”按 `GoneAt` 计算，不按 DATES。
- GONE TransportDemand 永久保留并可按 DemandId 查询，但不再每轮加载、更新或重写。
- DemandChangeFeed 只发布 CREATED/GONE，不发布每轮 MesLastSeenAt、DisappearCount 等观察变化。
- PausedZeroDrop 是重大故障；进入、持续和解除属于同一个 ERROR IngestAlert 生命周期。

## Functional Requirements

### 1. Time contract and display

- Core、Host DTO、Watch DTO 和 SQL Server 时间列统一使用 `DateTimeOffset` / `DATETIMEOFFSET`。
- Host 生成的 CreatedAt、GoneAt、Alert、PollHealth、连接事件等时间以 UTC 生成和保存。
- Oracle/CSV 不带时区的 DATES 按工厂 UTC+08:00 解释；原始时间点不得误当 UTC。
- Watch 读取运行电脑的系统时区，显示前转换为本机时区，统一格式 `yyyy-MM-dd HH:mm:ss zzz`。
- Watch 底部状态栏明确显示系统时区名称与 UTC 偏移；排序使用时间值，不使用格式化字符串。
- Watch 列名使用“当前工序进入时间 (DATES)”；STEP 保留为原始投影字段，但不是默认排序或主要交互字段。

### 2. Watch HTTP reliability and local event journal

- 新增 `Watch:RequestTimeoutSeconds`，默认 30，可配置范围 1–300；JSON 与 `MesIngestWatch__RequestTimeoutSeconds` 环境变量均可覆盖。
- 非法配置阻止启动并给出明确错误，不静默回退。
- 单次刷新不立即重试；下一次正常定时刷新就是重试，继续保持 single-flight。
- 任一端点失败时保留最后成功数据，状态栏显示最后成功刷新时间和陈旧时长；错误必须包含失败端点、阶段和配置超时。
- WatchConnectionEvent 写入 `%LocalAppData%\MesIngest.Watch\logs\` 的按日 JSON Lines：首次失败立即记录，持续故障每 5 分钟摘要一次，恢复时记录总持续时间和失败次数。
- Watch 本地日志默认保留 30 天且目录上限 100 MB，以先达到者为准；两者可配置。

### 3. Incremental SQL Server projection

- 禁止成功轮询后 `DELETE` 并逐条重建全部 TransportDemands/TaskTypePauses。
- 本轮新 Demand 执行 INSERT；状态、last-seen、消失计数或 pause 状态变化执行必要 UPDATE/UPSERT；未变化记录不写。
- GONE 转换与对应 DemandChangeFeed 记录必须在同一 SQL Server 事务中提交。
- 正常对账只加载当前 VISIBLE 与必需 pause 状态；检查 reappear 时按 TASK_TYPE+SUBLOT 使用索引查询历史，不加载全部 GONE。
- GONE 行形成后保持不可变业务字段，不在后续轮询中反复更新。
- 为 Status+DATES+DemandId、TASK_TYPE+SUBLOT、GoneAt+DemandId 等已确认访问路径建立经执行计划验证的索引；具体 INCLUDE 列由实现测试决定。

### 4. Paginated read API

- 现有 `/api/demands` 可直接升级为分页响应；当前没有需兼容旧裸数组格式的外部消费者。
- 响应至少包含 `items`、`nextCursor`、`hasMore`；不得提供不受限“返回全部”模式。
- 默认 `status=VISIBLE`、`sortBy=dates`、`direction=desc`；DemandId 是稳定次排序键。
- 支持 status、TASK_TYPE、SUBLOT、DATES 范围、GoneAt 范围和允许列的服务端筛选/排序；列头排序必须对完整查询集生效，不只是当前页。
- `/api/demands/{demandId}` 保持完整 DemandId 精确查询。
- DemandId 列表筛选只支持完整精确匹配或至少 6 位十六进制前缀；拒绝任意 `%fragment%` 扫描。输入统一小写且不在数据库列上套 LOWER/CAST。
- GONE 历史默认 `GoneAt >= now-24h`，允许调用方显式扩大范围；所有 VISIBLE 无时间窗口。
- Watch、Swagger 和外部程序共用同一分页契约；Watch 必须通过契约/集成测试证明能分页加载、重新筛选和保持排序。

### 5. DemandChangeFeed and authoritative bootstrap

- SQL Server 持久化单调 BIGINT sequence 的 Demand 变更账本；记录 CREATED/GONE、DemandId、ChangedAt 和稳定的变化后业务载荷。
- Demand 变化与账本追加在同一事务中；API 按 `afterSequence` + `limit` 顺序返回，消费者按 sequence 幂等应用并独立保存检查点。
- ChangeFeed 不包含 last-seen、DisappearCount、PollHealth 或 Alert。
- 默认保留 48 小时，可配置；API 暴露最早可用 sequence 和 high watermark。
- 游标早于最早可用 sequence 时返回 HTTP 410 与稳定错误码 `SYNC_CURSOR_EXPIRED`，不得静默跳过。
- Bootstrap 是权威重建：取得一致 high watermark、分页读取全部 VISIBLE 与 `GoneAt >= now-24h` 的 GONE，用结果替换本地当前镜像，再消费 high watermark 之后的变化。
- 下游旧镜像中的 Demand 若不在权威 VISIBLE 集合中，不能因简单 merge 而继续保持 VISIBLE。

### 6. Demand table interaction

- Watch 增加 DemandId 输入框，完整 ID 精确、至少 6 位十六进制前缀查询；输入约 300ms 防抖。
- TASK_TYPE、SUBLOT、status 与 DemandId 可组合，筛选/排序变化时重置到第一页。
- TransportDemands 与 Alerts 所有可见列支持列头升降序，并显示方向箭头；一次每表一列，刷新后保持当前列和方向。
- 删除原 sort 下拉框和 asc 复选框；TransportDemands 默认 DATES 降序，Alerts 默认活动 ERROR 优先、LastSeenAt 降序。
- 相同值使用 DemandId/AlertId 稳定排序。
- 两表支持 Ctrl+C 与右键：复制单元格、复制整行、复制整行（含列名）。整行使用 Tab 分隔；空值复制字面量 `null`；时间复制当前本机显示文本。

### 7. Resizable layout and status bar

- TransportDemands/Alerts 使用垂直 GridSplitter，共同填满剩余空间；默认 70/30，均有最小高度。
- Watch 本地保存分隔比例并在下次启动恢复；双击 splitter 恢复 70/30。
- Health 从顶部移至底部状态栏，分别显示 Watch 最近成功刷新与 Host 最近 MES 轮询完成时间、连接/陈旧状态、Host outcome、行数、耗时、活动 Alert 数、PausedZeroDrop 类型数和本机时区。
- BaseUrl、开始时间和长错误放入 tooltip/详情，不让状态栏失控增长。

### 8. IngestAlert incident model

- IngestAlert 是可聚合、可解除的问题实例，不是每轮消息；公共字段至少包含 AlertId、Code、Severity、TaskType、Sublot、DemandId、Message、Details JSON、FirstSeenAt、LastSeenAt、OccurrenceCount、IsActive、ResolvedAt。
- 相同 Code + 业务身份 + 详情指纹持续存在时只更新 LastSeenAt/OccurrenceCount；详情指纹改变时结束旧实例并创建新实例；恢复时写 ResolvedAt。
- Severity：POLL_FAILURE、POLL_INCOMPLETE、DUPLICATE_RECONCILE_KEY、PAUSED_ZERO_DROP、FIELD_DRIFT 均为 ERROR；REAPPEAR_AFTER_GONE 为 WARNING。
- PausedZeroDrop 的解除是同一 ERROR 实例的 RESOLVED 生命周期记录，不创建新的活动错误。
- FIELD_DRIFT 对所有冻结字段一视同仁；Details 列出字段、冻结值和观测值。
- DUPLICATE_RECONCILE_KEY Details 列出重复数量和冲突行；POLL_FAILURE/INCOMPLETE 保存失败阶段、超时、耗时和清理敏感信息后的原因；REAPPEAR 保存旧/新 DemandId；PausedZeroDrop 保存健康数量、阈值和恢复轮次。
- 活动 Alert 永不清理；已解除 Alert 默认保留 365 天，可配置，0 表示永久。
- Alert API 支持活动状态、时间范围、服务端排序和游标分页。

### 9. Alert/event UX and banners

- 双击 Alert、Enter 或右键“查看详情”打开非模态窗口，主 Watch 继续刷新。
- 详情窗口展示生命周期、结构化键值/字段差异、相关 Demand 定位，并支持复制摘要、详情 JSON 和 DemandId。
- Watch 提供统一事件查看入口，但明确区分 SQL Server IngestAlert 与本机 WatchConnectionEvent 来源。
- 红/橙横幅只代表当前活动状态：ERROR 红、WARNING 橙；故障至少显示 5 秒，恢复后自动消失并保留历史。
- 短暂恢复在状态栏显示“已恢复”；不得要求人工关闭已经恢复的横幅。

### 10. Swagger/OpenAPI

- Host 提供 `/swagger` 与 `/openapi/v1.json`，远程绑定时也默认启用文档。
- Swagger/OpenAPI 文档本身可打开；实际 `/api/*` 请求始终要求现有 Bearer SharedSecret（非 localhost 绑定），UI 提供 Authorize。
- 发布包包含静态 OpenAPI JSON，供无法访问工厂 Host 的合作者查看/导入。
- 文档覆盖分页、游标、筛选、DATES/MesLastSeenAt/CreatedAt/GoneAt 语义、时区、错误码、示例和 ChangeFeed/Bootstrap。
- MesIngest 仍只有正式只读 GET API；不得为了 Swagger 测试增加制造假 Demand/Alert 或修改状态的写接口。

### 11. Performance observability and immutable MES source boundary

- 客户批准的 `mes-task-union/query.sql` 保持只读原样，不重写性能逻辑、不增加时间谓词、不创建 Oracle 索引/视图/DDL。
- 保持单次完整活动快照与 single-flight；完整快照是 GONE 缺失判断的必要输入，不能用“只查新增”替代，除非未来另有经客户确认的删除/变化契约。
- 分别记录 Watch→Host 各端点、Host API、SQL Server 操作和 Oracle 整轮查询耗时、结果量、超时阶段与 correlation id。
- Oracle 慢查询明确归因为 `stage=ORACLE_QUERY` 并交客户 IT；本项目只优化 SQL Server/API/Watch 路径。

## Defaults (Tunable)

- Watch request timeout: 30s，合法范围 1–300s。
- Watch refresh: 保持现有可配置值；无单次立即重试。
- Watch connection summary interval: 5min。
- Watch local event retention: 30 days / 100 MB。
- Banner minimum visibility: 5s。
- Resolved IngestAlert retention: 365 days；0=永久。
- GONE default browse window: 24h by GoneAt；GONE 本体永久。
- DemandChangeFeed retention: 48h。
- DemandId partial search: minimum 6 lowercase hex prefix characters。
- List/change page sizes and maxima: implementation defaults，必须有硬上限并可经性能测试调整。

## Testing Decisions

- API contract tests覆盖分页 envelope、稳定 cursor、全局排序、组合筛选、DemandId 精确/前缀、非法 cursor、410 过期和旧裸数组契约已移除。
- Watch 集成测试使用真实 HTTP DTO 契约，证明新分页接口成功对接；不得只测本地 projector。
- SQL Server 集成测试覆盖增量 INSERT/UPDATE、GONE 不重写、事务内 ChangeFeed、索引查询路径和并发 API 不见半状态。
- ChangeFeed 测试覆盖 CREATED/GONE only、重复读取幂等、离线追赶、过期 cursor、Bootstrap high-watermark 期间并发变化不丢失。
- Alert 测试覆盖持续条件聚合、详情指纹变化、解除、严重等级和清理策略。
- 时间测试固定多个 offset，验证 UTC 保存、本机显示与按时间值排序。
- WPF 以 ViewModel/投影测试覆盖状态和复制文本；对 DataGrid/Splitter/非模态窗口保留轻量 UI smoke/manual acceptance，不绑定脆弱控件树。
- 工厂人工验证只采集批准 SQL 的时间语义、耗时和网络/数据库阶段证据，不修改 MES SQL。

## Out of Scope

- 修改、重写或为客户 MES Oracle 查询增加索引、视图、DDL、增量 CDC。
- 派车、装载、运送、人工创建/修改 TransportDemand。
- MesIngest 写 API、测试写接口或清理当前业务状态的命令。
- 用 DATES 作为 ChangeFeed sequence，或把 last-seen 每轮更新发布给下游。
- 为 STEP 建立新的路线推导或主要 UI 流程；路线继续按 TASK_TYPE 解释。
- 第一版引入 Kafka/RabbitMQ；ChangeFeed 由 SQL Server + HTTP 提供。

## Documentation Outputs

- Domain terms: PausedZeroDrop、IngestAlert、MesCurrentStepEnteredAt、DemandChangeFeed in `CONTEXT.md`。
- ADR-mes-0008: 完整源快照与增量本地投影/分页读取分离。
- ADR-mes-0009: DemandChangeFeed 与有限保留 Bootstrap 契约。
- Implementation tickets under `.scratch/mes-ingest-watch-operations/issues/`。

