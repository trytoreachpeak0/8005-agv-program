# Ticket 26 — 工厂验收与发布证据闭环

**结论：PASSED_WITH_NAMED_SKIPS**（2026-08-20 02:53:18 +08:00）

`MESINGEST_FACTORY_ACCEPTANCE_PASSED_WITH_NAMED_SKIPS`

一次运行覆盖票 26 全部 11 条：发布包身份、Oracle 只读接入、多轮完整
`MesTaskUnionRound`、SQL Server 持久化、版本化 API、Watch 八个入口与关闭 Watch 后的
Service 独立性，汇总为可复核的验收摘要。22 项声明检查中 **20 项 PASSED、2 项具名
skip、0 项 FAILED**。

- 运行标识：`factory-acceptance-20260819T184944Z-45ae5a0e`
- 执行机：`LAB-WIN-01`，操作员 `LAB-WIN-01\szy`
- 时钟：本机 `2026-08-20T02:49:44+08:00`（UTC+08:00，China Standard Time）
- 入口：`validation\Invoke-FactoryAcceptance.ps1 -RoundCount 3 -IncludePackagedWatch`

完整逐项结论见 [`factory-acceptance-summary.md`](factory-acceptance-summary.md)。

## 这次运行是什么、不是什么（先读这段）

| 事实 | 说明 |
| --- | --- |
| **Oracle 是真实工厂 MES 库** | Thin 探针 `execution_scope=LIVE_ORACLE`、`connection_attempted=true`，读回 560 行真实业务数据。全程只读。 |
| **SQL Server 是实验室实例** | `LAB-WIN-01\MSSQLSERVER` 上的一次性空库 `MesIngest_Ticket26_Factory`，主版本 16、兼容级别 160。它证明的是**兼容 SQL Server 上的持久化行为**，不是工厂那台生产 SQL Server。 |
| **执行机是实验室工作站** | `LAB-WIN-01` 与票 25 切换演练同一台机器，位于可访问工厂 Oracle 的网络内。它不是工厂产线机；`-Site` 参数只是操作员填写的元数据，不构成证据。 |
| **Watch 核验在真实交互桌面** | 打包 Watch 连真实 Host（真实 Oracle 数据 + 真实 SQL Server 投影），八个入口逐一渲染。 |

因此本次证据可以支持"最终包装在真实 Oracle 数据上端到端可用"这一结论，**不能**替代在工厂
生产 SQL Server 与产线机上的部署验收。后者若要求，需要在那台机器上重跑同一脚本。

## 发布包身份：它是什么产物

| 事实 | 实测 |
| --- | --- |
| 包内 914 个文件与 `RELEASE-MANIFEST.json` 逐字节一致 | `Identical=True`，`Missing/Mismatched/Unexpected` 均为 0 |
| 源提交 | `3b7c8f1ab0cfda09197112c81f7c7ee83c2e70ef`，`sourceDirty=false` |
| 清单自身哈希 | `433bc430ea8a377c…` |
| 现场新增文件 | 只有 `service/appsettings.Local.json`（operator-supplied，单列不计入 unexpected） |

**准确说法**：这不是票 25 那次构建出来的 zip，而是**票 25 冻结的发布契约**在票 26 提交上
重新构建的产物——票 26 只往 `validation/` 里加了验收脚本，并把它们列入
`Test-ReleasePackage.ps1` 的必需文件。契约本身未动，可核对的锚点是：

- 正式查询 `MES_TASK_UNION/sha256:54a140a…e439ae`（票 25 起冻结，未变）
- 契约版本 `2026.08.new-mes-ingest.v2.0`、`schemaVersion=17`（未变）
- OpenAPI `openapi/v2.json` 与 Service/Watch 共享契约程序集哈希由
  `Test-ReleasePackage.ps1` 在打包时核对（未变）

`Test-PackageIdentity` 证明的是**磁盘上的包与它自己的清单一致**（防止现场被改动），
外部锚点是清单里记录的 `sourceCommit` 加上"源树不干净就不许打包"这条构建规则。

## Oracle 只读接入（第 2、3 条）

只读在三处被证明，而不是被声明：

1. **脚本自己不连 Oracle。** 验收脚本只发 HTTP GET 与 SQL Server 只读查询；唯一接触
   Oracle 的是包内 Host。
2. **唯一可执行语句被哈希锁定。** 包内确有且只有一个 `.sql`，摘要显示
   `1 statement / 6 TASK_TYPE branches / 5 UNION ALL / 0 write keywords`。写关键字扫描
   剥离注释后进行——该产物的头注释本身写着"严禁 INSERT/UPDATE/DELETE"，不剥离就会把
   规则本身当成违规。
3. **探针身份完整。** `execution_scope=LIVE_ORACLE`、`connection_attempted=true`、
   `requested=actual=Thin`、driver `Oracle.ManagedDataAccess.Core`、`outcome=Success`、
   `row_count=560`、`duration=2716ms`、`commandTimeout=30s`。见
   [`probe-thin.txt`](probe-thin.txt) 与 [`oracle-probe-state.json`](oracle-probe-state.json)。

三轮完整轮次全部 SUCCESS，全部落在同一正式 query version：

| 轮 | outcome | rowCount | contentDigest | catalogRevision | 可读 Demand |
| --- | --- | --- | --- | --- | --- |
| 1 | SUCCESS | 560 | `6acde081b9dd2503…` | 1 | 258 |
| 2 | SUCCESS | 561 | `3bad448a2822cf4e…` | 2 | 257 |
| 3 | SUCCESS | 561 | `3bad448a2822cf4e…` | 2 | 257 |

第 2、3 轮规范摘要相同、CatalogRevision 未前进：同一份 Oracle 快照重复出现时不产生新的
业务修订，这正是内容寻址提交边界应有的行为。

## SQL Server 持久化（第 4 条）

目标库 `LAB-WIN-01\MSSQLSERVER / MesIngest_Ticket26_Factory`，**bootstrap 前 0 张用户表**。

| 检查 | 实测 |
| --- | --- |
| ProjectionCommit 原子持久化 | 突然 kill 后重启，257 条 Demand 于 catalogRevision 2 两次读取完全一致（静默 Host，ETag 相同），`projectionCommitId=491a7112…` |
| RestartBarrier | 新 Host 会话 `fee894a7…` 取代 `ba961774…`，记录 `RESTART_BARRIER_ENTERED`，phase=`BARRIER`，`absenceAuthorityAvailable=False` |
| TaskTypeProtection | 6 个 workType 全部 `MONITORING`，无一扣留 absence authority |
| CatalogRevision 单调 | `1 → 2 → 2`，无回退 |
| 读取快照不撕裂 | 同一 `snapshotReference` 在后续轮次提交之后再读，50/561 条内容与总数完全一致 |

预检使用**包内 Host 自己的 SQL 驱动**（`Microsoft.Data.SqlClient`）而不是 PowerShell 默认的
遗留驱动——两者协商不同，遗留驱动连得上而 Host 连不上的目标必须在启动前就被拒绝。

## 版本化 API 与数据访问保护（第 5 条）

- 契约发现：`contractVersion=2026.08.new-mes-ingest.v2.0`、`schemaVersion=17`、
  9 个 capability、全部 GET。
- ExternallyReadableDemandCatalog 首次完整正文 257 条，`catalogRevision=2`，
  ETag `W/"catalog-r2"`；同 Revision 条件读取返回 **304 且无正文**。
- 主要读取面全部 200 且带 `X-Correlation-Id`：DemandSeries、资格审计、错误检索、
  当前接入关注、Watch 概览（见 [`read-surfaces.json`](read-surfaces.json)）。
- 受限原始证据：**无密钥 403、错误密钥 403、正确密钥读到一个真实存在的证据资源（200）**。
  正向路径从现场错误检索结果里解析出真实 seriesId + evidenceId + snapshot；用占位路由的话，
  查询校验会在鉴权之前就拒绝，只能证明两条拒绝路径。
- 远程绑定缺少共享密钥：**启动即拒绝**（退出码非零，stderr 核对为 `MesIngest:SharedSecret`），
  Kestrel 未绑定。

## Watch 与 Service 生命周期（第 6、7 条）

打包 Watch 连真实 Host：

- 冷启动到主窗口 **1290.7 ms**；
- 八个入口全部渲染真实 Host 数据：概览、需求系列、资格审计、错误检索、AREA 筛选、
  接入告警、设置、紧凑 Host 状态；
- 契约匹配：Watch 客户端强制响应契约版本一致，状态显示 `Host 已连接`；
- 自动刷新：45 秒内概览客户端读取时间前进 3 次；
- **详情选择**在真实行上实测；**跨页下钻**由接入告警项进入错误检索实测；
- **分页**在真实数据上实测（第 1 页 → 第 2 页）；
- **失败保留**：停掉 Service 后，紧凑 Host 状态变为
  `Host 状态：Host 已连接 · 读取失败；打开连接设置`，需求系列已加载的 4 行**全部保留**，
  随后 Service 在同一地址恢复；
- 关闭 Watch 后 Service 继续：Watch 退出码 0，Host 未退出，PollTrace 高水位 `9 → 11`，
  继续写 SQL Server 并在 revision 3 提供目录。

见 [`watch/watch-pages.json`](watch/watch-pages.json)。窗口截图共 8 张，**留在执行机**
`.runtime/ticket26-acceptance/run-10/watch/`，不进仓库——它们含客户原始行。

## 第 8 条：不重复票 23 的视觉门禁

本次只证明最终打包与现场连接。票 23 的像素候选、10 次稳定、基线提升与 DPI clone
保持有效，因为本票没有改动 XAML、UI Automation 或 DPI 行为。运行中没有观察到 UI、
UI Automation 或 DPI 回归，因此没有场景被退回票 23。

驱动 Watch 的过程记录了它当前 UI Automation 表面的三个**观察**（不是本票引入的改动）：
导航项不暴露 Invoke 模式、需求系列与错误检索页的根 Grid 不在 control view 内、
导航栏比还原态窗口高。

## 具名 skip（第 10、11 条）

| 名称 | 责任方 | 需要什么才能补跑 | 留下的 gate |
| --- | --- | --- | --- |
| `LIVE_ORACLE_THICK_MODE_REVERIFICATION` | plant IT / release owner | Oracle Instant Client + 已注册 ODBC 驱动，然后以 `-OracleMode Thick` 重跑本脚本 | `FACTORY_ORACLE_ACCEPTANCE` |
| `NON_SUCCESS_ROUNDS_PRESERVE_PROJECTION` | release owner | 一个真的产生 FAILURE 或 INCOMPLETE 轮次的现场窗口（例如运行期间 Oracle 中断） | `FACTORY_ORACLE_ACCEPTANCE` |

第二项值得说明：本窗口三轮全部成功，**没有失败轮次可供检查**。把它记成 PASSED 会被读成
"已证明失败轮次不动投影"，而本次窗口无法证明这一点。判定规则本身由仓库测试
（`Test-NonSuccessRoundsPreservedProjection`：一个改动了 catalogRevision 或 demandCount 的
非 SUCCESS 轮次会被判为缺陷）覆盖。

汇总状态因此是 `PASSED_WITH_NAMED_SKIPS` 而不是 `PASSED`：脚本用不同的状态值区分
"全跑通"和"跑通但有未执行项"。

## 剩余风险

- Thick 模式未复验（具名 skip）。
- 失败/不完整轮次的投影保护未在现场窗口实测（具名 skip）。
- SQL Server 是实验室实例、执行机是实验室工作站；工厂生产 SQL Server 与产线机上的部署
  验收未覆盖。
- 逐 TASK_TYPE 的 DATES/STEP 业务语义仍是人工确认项，留在
  `validation/execution-log.md`，本次自动化不替代它。
- 已发布证据是计数、身份、修订号与哈希；API 响应正文与 Watch 截图留在执行机，
  异地复核者看不到原始行。这是脱敏要求的直接代价。
- 现场 SQL Server 的 TLS 预登录握手很慢（`Encrypt=False` + `Connect Timeout=60` 下约 4.5 s，
  默认 15 s 超时会失败）。连接串必须显式放宽超时，否则 Host 起不来。

## 回退准备度

回退仍然是票 25 的演练：停新版 Service → 用 `scripts\cutover\Invoke-CutoverRollback.ps1`
从独立备份恢复旧库 → 旧程序指向恢复出来的旧库。不支持新旧混跑。

## 达成过程：9 轮红，全部是真问题

第 10 次运行才是本索引记录的验收运行。此前每一次红都定位到具体缺陷并逐条修复：

1. **preflight 用错驱动**（`df7a756`）。preflight 用 `System.Data.SqlClient` 连上了目标，
   包内 Host 用 `Microsoft.Data.SqlClient` 在预登录 TLS 握手超时——preflight 放行了一个
   Host 根本连不上的目标。同一次还暴露了中止的代价：脚本死在检查之间会丢掉整份摘要，
   所有 gate 状态不明；现在中止运行会把未跑到的检查按红证据关闭并写明原因。
2. **按契约实际形状读取**（`b0b8ab0`）。空库刚 bootstrap 时读取面返回 409 被当成缺陷而不是
   等待；`/api/v2/absence-authority` 返回的是当前 Host 会话而不是列表；分页面的契约版本挂在
   snapshot 身份上、总数字段是 `exactTotalCount`、错误检索按 cursor 分页而不是页码。
3. **按操作员的方式驱动 Watch**（`9735770`）。导航项不暴露 Invoke/SelectionItem 模式，
   只用模式驱动会"成功"但什么都没动；UI Automation 的 control view 不含纯布局面板，需求
   系列与错误检索页的根 Grid 从进程外根本不可寻址；导航栏比还原态窗口高，设置与紧凑
   Host 状态落在窗口下沿之外没有可点击点；`if` 表达式返回空数组会展开成 `$null`。
4. **报告没写运行标识**（`3286b04`）。
5. **验收在没实测的项目上写了 PASSED**（`e2fc8fe`，由代码审查发现）。受限证据的正向路径
   打的是占位路由，被查询校验在鉴权之前拒绝；Watch 的分页、详情、跨页下钻只写进自由文本
   而没有断言，失败保留根本没做；没有失败轮次的窗口被记成"已验证失败轮次无害"。
6. **失败读取的信号找错了地方**（`8c7a802`）。刷新失败不会断开连接，Watch 把它追加在
   紧凑 Host 状态上（`Host 已连接 · 读取失败`），而承载完整措辞的页面 InfoBar 在折叠时
   根本不在自动化树里。
7. **分页判定过早**（`d7f5738`、`3b7c8f1`）。560 个 Series 分 6 页的现场快照不会在固定
   暂停内翻页；而且下一页控件在首份快照回来之前是禁用的，先读它会把六页的快照记成
   "只有一页"——一个声称了现场数据没说过的事的具名 skip。

第 3 次运行中 `/api/v2/error-search?page=1&pageSize=100` 曾返回一次 HTTP 500。事后用同一
发布包对同一实例复现，`page=1`（不支持的参数）稳定返回 400、`pageSize=100` 返回 200，
未再复现 500；当时正值 SQL 慢握手窗口，最可能是一次瞬时 provider 失败。本索引把它按
**一次性观察**记录，不作为验收结论，也不宣称已定位。若再次出现，`host-stage-log.txt`
现在会带着 correlation id 与 stage 一起留证。

## 证据文件

| 文件 | 内容 |
| --- | --- |
| [`factory-acceptance-summary.md`](factory-acceptance-summary.md) | 逐项结论、具名 skip、剩余风险、回退准备度 |
| [`factory-acceptance-summary.json`](factory-acceptance-summary.json) | 同上的机器可读版本，含运行上下文与清理记录 |
| [`package-identity.json`](package-identity.json) | 包与 RELEASE-MANIFEST 的逐文件比对结果 |
| [`probe-thin.txt`](probe-thin.txt) / [`oracle-probe-state.json`](oracle-probe-state.json) | 只读探针原始输出（已脱敏）与判定状态 |
| [`rounds.json`](rounds.json) | 三轮 PollTrace 身份、规范摘要、行数、投影结果 |
| [`read-surfaces.json`](read-surfaces.json) | 主要读取面的状态码、条数、耗时、correlation id |
| [`absence-authority.json`](absence-authority.json) | 重启后的会话、阶段与屏障事件 |
| [`task-type-protections.json`](task-type-protections.json) | 6 个 workType 的保护相位 |
| [`environment.json`](environment.json) | 机器、时钟、时区、SQL 目标身份、所用 SQL 驱动 |
| [`host-stage-log.txt`](host-stage-log.txt) | Host 自身的 stage/correlation 行（已两次脱敏） |
| [`watch/watch-pages.json`](watch/watch-pages.json) | Watch 走查结果、Host 状态、自动刷新与逐项交互实测 |
| [`evidence-hashes.json`](evidence-hashes.json) | 全部证据文件的 SHA-256 |

`evidence-hashes.json` 覆盖运行目录中的全部文件，包括留在执行机的 8 张截图，
因此异地复核者可以核对现场持有的截图未被替换。
