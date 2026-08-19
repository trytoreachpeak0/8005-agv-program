# Ticket 26 — 工厂验收与发布证据闭环

**结论：PASSED_WITH_NAMED_SKIPS**（2026-08-20 01:57:52 +08:00）

`MESINGEST_FACTORY_ACCEPTANCE_PASSED_WITH_NAMED_SKIPS`

一次运行覆盖票 26 全部 11 条：发布包身份、Oracle 只读接入、多轮完整
`MesTaskUnionRound`、SQL Server 持久化、版本化 API、Watch 六页与关闭 Watch 后的
Service 独立性，汇总为可复核的验收摘要。20 项声明检查中 **19 项 PASSED、1 项具名
skip、0 项 FAILED**。

- 运行标识：`factory-acceptance-20260819T175432Z-380c08a5`
- 现场机：`LAB-WIN-01`，操作员 `LAB-WIN-01\szy`，站点 `SUQIAN-PLANT`
- 时钟：本机 `2026-08-20T01:54:32+08:00`（UTC+08:00，China Standard Time）
- 入口：`validation\Invoke-FactoryAcceptance.ps1 -RoundCount 3 -IncludePackagedWatch`

完整逐项结论见 [`factory-acceptance-summary.md`](factory-acceptance-summary.md)。

## 现场用的确实是发布包

| 事实 | 实测 |
| --- | --- |
| 包内 914 个文件与 `RELEASE-MANIFEST.json` 逐字节一致 | `Identical=True`，`Missing/Mismatched/Unexpected` 均为 0 |
| 源提交 | `3286b04ed39ee1199ce67e9b3091062c2b4fc565`，`sourceDirty=false` |
| 清单自身哈希 | `RELEASE-MANIFEST.json` SHA-256 记录于 [`package-identity.json`](package-identity.json) |
| 正式查询 | 唯一 `.sql` 产物，`MES_TASK_UNION/sha256:54a140a…e439ae` |
| 配置模板 | 现场只新增 `service/appsettings.Local.json`，作为 operator-supplied 单列，不计入 unexpected |

发布包由票 25 的 `pack/Publish-MesIngest.ps1` 产出并通过 `Test-ReleasePackage.ps1`。
现场只填了 Oracle 凭据模板，二进制、脚本、OpenAPI、查询产物全部未改。

## Oracle 只读接入（第 2、3 条）

只读在三处被证明，而不是被声明：

1. **脚本自己不连 Oracle。** 验收脚本只发 HTTP GET 与 SQL Server 只读查询；唯一接触
   Oracle 的是包内 Host。
2. **唯一可执行语句被哈希锁定。** 包内确有且只有一个 `.sql`，摘要显示
   `1 statement / 6 TASK_TYPE branches / 5 UNION ALL / 0 write keywords`。写关键字扫描
   剥离注释后进行——该产物的头注释本身写着"严禁 INSERT/UPDATE/DELETE"，不剥离就会把
   规则本身当成违规。
3. **探针身份完整。** `execution_scope=LIVE_ORACLE`、`connection_attempted=true`、
   `requested=actual=Thin`、driver `Oracle.ManagedDataAccess.Core`、
   `outcome=Success`、`row_count=597`、`duration=3001ms`、`commandTimeout=30s`。
   见 [`probe-thin.txt`](probe-thin.txt) 与 [`oracle-probe-state.json`](oracle-probe-state.json)。

三轮完整轮次全部 SUCCESS，全部落在同一正式 query version：

| 轮 | outcome | rowCount | contentDigest | catalogRevision | 可读 Demand |
| --- | --- | --- | --- | --- | --- |
| 1 | SUCCESS | 602 | `21c904efccc79082…` | 1 | 262 |
| 2 | SUCCESS | 601 | `7afb0f18efdcf5d2…` | 2 | 260 |
| 3 | SUCCESS | 602 | `ce2b6843a526f6ba…` | 2 | 260 |

本窗口内没有出现 FAILURE 或 INCOMPLETE 轮次，因此
`NON_SUCCESS_ROUNDS_PRESERVE_PROJECTION` 记录的是"未出现"而不是"已验证失败轮次不动
投影"——判定逻辑本身由仓库测试覆盖（一个改动了 catalogRevision 或 demandCount 的非
SUCCESS 轮次会被判为缺陷）。

## SQL Server 持久化（第 4 条）

目标库 `LAB-WIN-01\MSSQLSERVER / MesIngest_Ticket26_Factory`，SQL Server 主版本 16、
兼容级别 160，**bootstrap 前 0 张用户表**。

| 检查 | 实测 |
| --- | --- |
| ProjectionCommit 原子持久化 | 突然 kill 后重启，260 条 Demand 于 catalogRevision 2 两次读取完全一致（静默 Host，ETag 相同） |
| RestartBarrier | 新 Host 会话 `d541cef7…` 取代 `638737fa…`，记录 `RESTART_BARRIER_ENTERED`，phase=`BARRIER`，`absenceAuthorityAvailable=False` |
| TaskTypeProtection | 6 个 workType 全部 `MONITORING`，无一扣留 absence authority |
| CatalogRevision 单调 | `1 → 2 → 2`，无回退 |
| 读取快照不撕裂 | 同一 `snapshotReference` 在后续轮次提交之后再读，50/602 条内容与总数完全一致 |

## 版本化 API 与数据访问保护（第 5 条）

- 契约发现：`contractVersion=2026.08.new-mes-ingest.v2.0`、`schemaVersion=17`、
  9 个 capability、全部 GET。
- ExternallyReadableDemandCatalog 首次完整正文 260 条，`catalogRevision=2`，
  ETag `W/"catalog-r2"`；同 Revision 条件读取返回 **304 且无正文**。
- 主要读取面全部 200 且带 `X-Correlation-Id`：DemandSeries、资格审计、错误检索、
  当前接入关注、Watch 概览（见 [`read-surfaces.json`](read-surfaces.json)）。
- 受限原始证据：无密钥 403、错误密钥 403、正确密钥非 403。
- 远程绑定缺少共享密钥：**启动即拒绝**（退出码非零，stderr 核对为 `MesIngest:SharedSecret`），
  Kestrel 未绑定，任何数据都没有暴露到 loopback 之外。

## Watch 与 Service 生命周期（第 6、7 条）

在工厂交互桌面用包内 Watch 连真实 Host：

- 打包 Watch 冷启动到主窗口 **1408.6 ms**；
- 八个入口全部渲染真实 Host 数据：概览、需求系列、资格审计、错误检索、AREA 筛选、
  接入告警、设置、紧凑 Host 状态；
- 契约匹配：Watch 客户端强制响应契约版本一致，状态显示 `Host 已连接`；
- 自动刷新：45 秒内概览客户端读取时间前进 3 次；
- 详情选择在 4 条真实行上实测；跨页下钻由接入告警项进入错误检索实测；
- 分页因当次快照只有一页而 **未实测**，按原样记录，不算通过；
- 关闭 Watch 后 Service 继续：Watch 退出码 0，Host 未退出，PollTrace 高水位
  `10 → 11`，继续写 SQL Server 并在 revision 7 提供目录。

见 [`watch/watch-pages.json`](watch/watch-pages.json)。窗口截图共 8 张，**留在现场机**
`.runtime/ticket26-acceptance/run-05/watch/`，不进仓库——它们含客户原始行。

## 第 8 条：不重复票 23 的视觉门禁

本次只证明最终打包与现场连接。票 23 的像素候选、10 次稳定、基线提升与 DPI clone
保持有效，因为本票没有改动 XAML、UI Automation 或 DPI 行为。现场没有观察到 UI、
UI Automation 或 DPI 回归，因此没有场景被退回票 23。

## 具名 skip（第 10、11 条）

| 名称 | 责任方 | 需要什么才能补跑 | 留下的 gate |
| --- | --- | --- | --- |
| `LIVE_ORACLE_THICK_MODE_REVERIFICATION` | plant IT / release owner | Oracle Instant Client + 已注册 ODBC 驱动，然后 `-OracleMode Thick` 重跑 | `FACTORY_ORACLE_ACCEPTANCE` |

票面写的是"现场确有需要时再以同一业务入口复验 Thick"。Thin 探针与三轮全部成功，
没有触发 Thick 回退，因此按未执行记录，不按通过记录。

汇总状态因此是 `PASSED_WITH_NAMED_SKIPS` 而不是 `PASSED`：脚本用不同的状态值区分
"全跑通"和"跑通但有未执行项"，避免后者被读成前者。

## 剩余风险

- Thick 模式未复验（同上具名 skip）。
- 逐 TASK_TYPE 的 DATES/STEP 业务语义仍是人工确认项，留在
  `validation/execution-log.md`，本次自动化不替代它。
- 已发布证据是计数、身份、修订号与哈希；API 响应正文与 Watch 截图留在现场机，
  异地复核者看不到原始行。这是脱敏要求的直接代价。
- 现场 SQL Server 的 TLS 预登录握手很慢（`Encrypt=False` + `Connect Timeout=60`
  下约 4.5 s，默认 15 s 超时会失败）。连接串必须显式放宽超时，否则 Host 起不来。

## 回退准备度

回退仍然是票 25 的演练：停新版 Service → 用 `scripts\cutover\Invoke-CutoverRollback.ps1`
从独立备份恢复旧库 → 旧程序指向恢复出来的旧库。不支持新旧混跑。

## 达成过程：4 轮红，全部是真问题

第 5 次运行才是本索引记录的验收运行。前 4 次的红都不是环境噪声：

1. **preflight 用错驱动**（提交 `df7a756`）。preflight 用 `System.Data.SqlClient` 连上了
   现场库，包内 Host 用 `Microsoft.Data.SqlClient` 在预登录 TLS 握手超时——preflight
   放行了一个 Host 根本连不上的目标。现在 preflight 加载包内客户端，用同一个驱动失败。
   同一次运行还暴露了中止的代价：脚本死在检查之间会丢掉整份摘要，所有 gate 状态不明。
   现在中止的运行会把未跑到的检查按红证据关闭并写明中止原因。
2. **按契约实际形状读取**（提交 `b0b8ab0`）。空库刚 bootstrap 时读取面返回 409，脚本
   把这个启动窗口当成缺陷而不是等待；`/api/v2/absence-authority` 返回的是当前 Host
   会话而不是列表；分页面的契约版本挂在 snapshot 身份上、总数字段是 `exactTotalCount`、
   错误检索按 cursor 分页而不是页码。
3. **按操作员的方式驱动 Watch**（提交 `9735770`）。导航项不暴露 Invoke/SelectionItem
   模式，只用模式驱动会"成功"但什么都没动；UI Automation 的 control view 不含纯布局
   面板，需求系列与错误检索页的根 Grid 从进程外根本不可寻址；导航栏比还原态窗口高，
   设置与紧凑 Host 状态落在窗口下沿之外没有可点击点；`if` 表达式返回空数组会展开成
   `$null`，数行数时抛异常而不是报告空快照。
4. **报告没写运行标识**（提交 `3286b04`）。摘要里的 run id 被转义成了字面量，复核者
   无法把摘要对回证据目录。

第 3 次运行中 `/api/v2/error-search?page=1&pageSize=100` 曾返回一次 HTTP 500。事后用
同一发布包对同一实例复现，`page=1`（不支持的参数）稳定返回 400、`pageSize=100` 返回
200，三次尝试均未复现 500；当时正值现场 SQL 慢握手窗口，最可能是一次瞬时 provider
失败。本索引把它按**一次性观察**记录，不作为验收结论，也不宣称已定位。若再次出现，
`host-stage-log.txt` 现在会带着 correlation id 与 stage 一起留证。

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
| [`watch/watch-pages.json`](watch/watch-pages.json) | Watch 走查结果、Host 状态、自动刷新与交互实测 |
| [`evidence-hashes.json`](evidence-hashes.json) | 全部证据文件的 SHA-256 |

`evidence-hashes.json` 覆盖运行目录中的全部文件，包括留在现场机的 8 张截图，
因此异地复核者可以核对现场持有的截图未被替换。
