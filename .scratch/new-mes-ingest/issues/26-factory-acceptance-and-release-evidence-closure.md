# 26 — 工厂验收与发布证据闭环

**What to build:** 使用最终空库切换发布包在工厂环境分别验证 Oracle 只读接入、SQL Server 持久化、Service 独立运行、版本化 API、目录条件读取和 Watch 六页，将可复核且脱敏的证据、具名 skip 和现场结论汇总为发布签字输入，而不把实验室或黄金机结果冒充工厂通过。

**Blocked by:** 25 — 删除旧模型并形成空库切换发布包

**Status:** ready-for-human

- [x] 记录最终发布包、源提交、配置模板、正式 MES_TASK_UNION 查询和目标环境身份的哈希或不可歧义版本，并证明现场使用的正是票 25 产物。
- [x] 在真实 Oracle 11g 环境运行 Thin 模式只读探针，证明一次执行唯一正式六分支 UNION ALL 语句、列契约、命令超时、只读边界和凭据脱敏；现场确有需要时再以同一业务入口复验 Thick + Instant Client。
- [x] 运行多个完整 MesTaskUnionRound 并记录 SUCCESS、FAILURE 或 INCOMPLETE 的 PollTrace、规范摘要、行数、查询版本和投影结果；任何失败或结构不完整轮次都不能伪造 Demand 消失或修改业务投影。
- [x] 在现场兼容 SQL Server 上证明 ProjectionCommit 原子持久化、Service 重启后历史一致、RestartBarrier 边界、TaskTypeProtection、CatalogRevision 单调及读取快照不撕裂。
- [x] 验证契约发现和鉴权、ExternallyReadableDemandCatalog 首次完整正文、同 Revision 的 304、主要 Series/资格/错误/当前关注/概览读取，以及远程绑定缺少或使用错误共享密钥时的数据访问保护。
- [x] 在工厂交互桌面核验 Watch 的概览、需求系列、资格审计、错误检索、AREA 筛选、接入告警、设置与紧凑 Host 状态，确认契约匹配、自动刷新、失败保留、分页、详情和跨页下钻使用真实 Host 数据。
- [x] 关闭 Watch 后继续观察 Service 完成轮询、写入 SQL Server 并提供 API，证明运维客户端不拥有轮询或业务投影生命周期。
- [x] 工厂 Watch 核验用于证明最终包装与现场连接，不因 UI 输出未变化而重复票 23 的候选、10 次像素稳定、基线提升或 DPI clone；若现场发现实际 UI、UI Automation 或 DPI 回归，则保留失败证据并将对应场景退回票 23 的受影响门禁。
- [x] 收集任务退出码、环境和时钟信息、Oracle/SQL/API/Watch 结果、必要截图或 UIA 证据、清理结果及脱敏证据哈希；不得包含凭据、客户敏感原始行或未获准的任意日志。
- [x] 每个未执行、失败或受现场条件阻塞的检查都以具体名称、原因、责任方和 release gate 记录为 skip 或 red evidence；只有实际完成的项目才能进入现场通过结论。
- [x] 形成可由发布负责人和现场人员复核的最终验收摘要，分别列明已通过、未通过、具名 skip、剩余风险和回退准备度。

## 黄金机视觉检查单为何不适用

`docs/agents/issue-tracker.md` 要求：改动 `MesIngest.Watch` UI、XAML、Wpf.Ui 控件、布局、
**UI Automation**、DPI 行为或视觉基线的票，必须链接
[`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md) 并带上它的 Ticket 检查单。

本票**没有改动 Watch 自身的 UI Automation 表面**：XAML、AutomationId、AutomationProperties
一行未动。改动的是发布包里**新增的一个 UI Automation 客户端**
（`pack/validation/WatchAcceptanceUia.ps1`），它从进程外驱动已批准的那份 Watch，用于现场
核验最终打包是否连得上真实 Host。因此：

- 不产生、不比较、不提升任何视觉基线；截图只是现场证据，留在现场机，不进仓库；
- 票 23 的像素候选、10 次稳定、基线提升与 DPI clone 全部**不重跑**（第 8 条）；
- 若现场发现真实 UI / UI Automation / DPI 回归，保留红证据并把对应场景退回票 23 的门禁，
  由那边的检查单接管。

写这个客户端的过程反过来记录了 Watch 当前 UI Automation 表面的三个事实（导航项不暴露
Invoke 模式、需求系列与错误检索页的根 Grid 不在 control view 内、导航栏高于还原态窗口），
它们是**观察**，不是本票引入的改动。

## 实现记录（2026-08-20）

### 交付的是一次可复核的现场运行，不是一份清单

票 24 留下的 `validation/` 是人工执行模板；本票补的是同一现场证据的机械闭环：
`pack/validation/Invoke-FactoryAcceptance.ps1` 一次运行把发布包身份、只读 Oracle 探针、
多轮完整 `MesTaskUnionRound`、SQL Server 持久化、版本化 API、Watch 六页与关闭 Watch 后的
Service 独立性，汇总成发布签字输入。

它是 `Invoke-ReleaseSmoke.ps1` 的**现场孪生**：烟测用录制轮次驱动同一条生产入口，所以
它哪里都能跑——这恰恰是它永远不能当工厂验收的原因。本脚本在任何东西启动之前就拒绝
录制配置（`RECORDED_ROUNDS_ARE_NOT_FACTORY_EVIDENCE`），并且只接受真正在工厂 Oracle 上
执行过的轮次。

### 判定逻辑放在可被仓库执行的地方

所有"什么才算可以写成通过"的判断放在 `pack/validation/FactoryAcceptanceTools.ps1`，
由 `MesIngest.Tests/FactoryAcceptanceToolsTests.cs`（20 个用例）跑**发布出去的那份脚本**，
而不是描述它的散文。被强制的三条规则：

- 没真正连到工厂 Oracle 的证据不能记成通过：离线/模拟 scope、非零退出码、非正式
  query identity 一律降级为 `NOT_EXECUTED` 或 `FAILED`；
- 没跑的检查必须是**具名 skip**——缺少责任方或补跑前提时 `New-AcceptanceCheck` 直接拒绝
  生成，声明过的检查没有结果时 `New-FactoryAcceptanceSummary` 以
  `UNREPORTED_ACCEPTANCE_CHECK` 失败；带 skip 的运行结论是 `PASSED_WITH_NAMED_SKIPS`，
  与全绿的 `PASSED` 是不同状态值；
- 中止的运行也要闭环：`Complete-AbortedAcceptanceChecks` 把没跑到的检查按红证据关闭并
  写明中止原因，不留下状态不明的 gate。

Oracle 的只读边界同样是被测量出来的：`Test-CanonicalReadOnlyStatement` 剥离注释后扫描
写关键字（产物头注释本身写着"严禁 INSERT/UPDATE/DELETE"，不剥离就会把规则当成违规），
并核对语句数、六个 `TASK_TYPE` 分支、五个 `UNION ALL` 与哈希。脚本自身不开任何 Oracle
连接。

### 现场结果

**PASSED_WITH_NAMED_SKIPS**，22 项声明检查中 20 项 PASSED、2 项具名 skip、0 项 FAILED。

- 发布包 914 个文件与 `RELEASE-MANIFEST.json` 逐字节一致（源提交 `3b7c8f1`、`sourceDirty=false`）；
- Thin 探针 `LIVE_ORACLE` 成功读回 560 行真实业务数据，全程只读；
- 三轮完整轮次全部 SUCCESS，落在同一正式 query version；
- 重启后投影不变、屏障重新进入、CatalogRevision 单调、快照读取不撕裂；
- 受限原始证据的正向路径读到**真实存在的证据资源**（200），两条拒绝路径均 403；
- 打包 Watch 八个入口全部渲染真实 Host 数据，分页、详情、跨页下钻逐项实测；停掉 Service 后
  紧凑 Host 状态显示 `读取失败`且已加载行全部保留；关闭 Watch 后 Service 继续轮询与写库。

两项具名 skip：`LIVE_ORACLE_THICK_MODE_REVERIFICATION`（Thin 全程成功，未触发 Thick 回退）与
`NON_SUCCESS_ROUNDS_PRESERVE_PROJECTION`（本窗口没有失败或结构不完整轮次可供检查——记成
PASSED 会被读成"已证明失败轮次无害"，而本次窗口证明不了）。

**证据边界要说清楚**：Oracle 是真实工厂 MES 库；SQL Server 是实验室实例
`LAB-WIN-01\MSSQLSERVER` 上的一次性空库；执行机 `LAB-WIN-01` 是与票 25 演练同一台实验室
工作站，位于可访问工厂 Oracle 的网络内，不是产线机。因此本次支持"最终包装在真实 Oracle
数据上端到端可用"，不替代工厂生产 SQL Server 与产线机上的部署验收。

发布包也不是票 25 那次构建出的 zip，而是**票 25 冻结的发布契约**在票 26 提交上重建的产物：
票 26 只往 `validation/` 加了验收脚本并把它们列入必需文件；正式查询哈希、契约版本、
`schemaVersion=17`、OpenAPI 与共享契约程序集全部未变，打包时逐项核对。

第 8 条按"打包未改变已批准输出"复用票 23 的视觉验收，**未重跑**像素候选、10 次稳定、
基线提升与 DPI clone；运行中也没有观察到 UI / UI Automation / DPI 回归。

### 达成过程共 10 轮，前 9 轮的红全是真问题

preflight 用 `System.Data.SqlClient` 放行了包内 Host 连不上的目标；中止的运行会丢掉整份
摘要；空库 bootstrap 期的 409 被当成缺陷；`/api/v2/absence-authority` 返回当前会话而不是
列表；分页面的契约版本在 snapshot 身份上、总数是 `exactTotalCount`、错误检索按 cursor
分页；Watch 导航项不暴露 Invoke 模式、页面根 Grid 在 UIA control view 之外、导航栏高于
还原态窗口、`if` 返回空数组展开成 `$null`。

其中第 5 轮之后的三条由代码审查发现，值得单独记：**验收在没实测的项目上写了 PASSED**——
受限证据正向路径打的是占位路由（被查询校验在鉴权前拒绝）、Watch 的分页/详情/跨页下钻
只写进自由文本没有断言、失败保留根本没做、没有失败轮次的窗口被记成已验证。修复后这三处
分别变成真实资源断言、独立检查与具名 skip。随后又暴露两个测量点错误：失败读取的信号在
紧凑 Host 状态上而不是折叠的页面 InfoBar；分页控件在首份快照回来前是禁用的，先读它会把
六页的快照记成"只有一页"。

完整证据与逐项实测见
[`.artifacts/ticket26-acceptance/EVIDENCE-INDEX.md`](../../../.artifacts/ticket26-acceptance/EVIDENCE-INDEX.md)。
