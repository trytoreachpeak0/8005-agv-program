# MesIngestWatch V2 产品与交互规格路线图

## Destination

形成一份经简化交互原型评审确认、可直接交给实现阶段的《MesIngestWatch V2 产品与交互规格》：以当前系统真实的六类 MES 任务、TransportDemand 投影和六类 IngestAlert 为核心，明确单 Host 只读查看、刷新分页、WPF 视觉体系及自动化验收标准。

## Notes

- 首要用户是现场实施与运维工程师；MesIngestWatch 不是生产操作 HMI、调度台或数据编辑器。
- 启动页须在约 10 秒内回答接入是否健康、当前活动 IngestAlert 和当前 VISIBLE TransportDemand。
- 信息架构只围绕概览、MES 任务/TransportDemand、IngestAlert 和必要设置；左侧导航，默认浅色工业运维风格。
- 一次只连接一个 Host；Watch 只通过现有只读业务 API 查询 TransportDemand、IngestAlert 和 PollHealth。
- MES 原始任务行是 `TASK_TYPE/SUBLOT/AREA/EQP/STEP/DATES/PACKAGE`；页面必须区分 MES 输入字段与本地投影字段，并正确解释 `DATES` 与 `STEP`。
- 所有数据页默认手动刷新；按页可选自动刷新和频率，只刷新当前页。VISIBLE/GONE 各自保留筛选与游标分页状态。
- 查询显式提交；请求可取消、不重入、不排队，过期响应不得覆盖新结果。慢 Host 时 UI 必须保持可操作。
- Alert 只读查看，不提供确认、指派、备注或手工关闭；页面只能展示 Core 实际产生的 code，不得把原型占位事件冒充 IngestAlert。
- 继续使用 .NET 8 WPF。原六页原型已因范围收缩而失效；正式实现前必须重新通过以 MES 任务和 IngestAlert 为中心的简化原型评审，并建立可在本机交互式 Windows 会话串行运行的 WPF UI 自动化与截图视觉回归验收；本期不建设 GitHub CI。
- 相关会话优先使用 `prototype`、`domain-modeling`、`codebase-design` 与 `tdd` 技能；外部事实研究使用 `research`。
- 当前工作树含用户的 MesIngest.Watch 在途改动；只读分析并保留，不覆盖或重置。

## Decisions so far

<!-- Closed ticket decisions are indexed here; detail lives in each ticket. -->

- [建立现有能力与回归边界](issues/01-establish-current-capability-and-regression-baseline.md) — V2 保留 MesIngest 领域核心、Host 只读契约和 Watch 可靠性/浏览能力，增量替换产品壳，并以版本化迁移和分层 Windows 门禁防回退。
- [选择 WPF 自动化与视觉回归测试栈](issues/02-choose-wpf-automation-and-visual-regression-stack.md) — 真实旅程采用 FlaUI.UIA3，确定性页面快照采用 Verify.Xaml，固定交互式 Windows runner 校准后再把全窗口像素回归升为门禁。
- [识别现有 IngestAlert 与 MES 任务形态](issues/07-define-alert-demand-diagnostics-and-export-boundary.md) — Core 实际产生 6 类 IngestAlert，`MES_TASK_UNION` 实际输出 6 类、7 列 MES 任务；已固定告警触发条件、任务含义与 TransportDemand 投影形态。
- [验证以 MES 任务与 IngestAlert 为中心的简化 WPF 原型](issues/13-validate-task-and-alert-centered-wpf-prototype.md) — 选择 A「健康优先四页」作为产品壳；B/C 的任务与告警入口仅吸收到对应页面，不保留全局常驻侧栏。
- [定义流畅刷新、游标分页与取消模型](issues/08-define-responsive-refresh-paging-and-cancellation-model.md) — 四个视图采用独立单页 cursor 状态、显式查询和成功窗口原子提交，以用户优先单飞、Host/请求代次及有界恢复保证慢 Host 下不串页、不清空、不被过期响应覆盖。
- [固定 WPF 截图基线与 Windows CI 证据规则](issues/11-lock-wpf-screenshot-baselines-and-windows-ci-evidence-rules.md) — V2 只要求本机交互式 Windows 自动化验收，固定双视口 Verify.Xaml 基线、五个 FlaUI 终态、失败证据、基线复核与 flaky-test 治理，不建设 GitHub CI。
- [汇编 V2 产品与交互规格](issues/09-assemble-v2-product-and-interaction-specification.md) — 已形成单一交接候选，收口四页产品壳、领域与只读契约、浏览状态机、页面行为及本机自动化验收，并以 `100+` 诚实表达无总数列表。
- [确认 V2 实现交接](issues/10-accept-v2-implementation-handoff.md) — 最终人工评审已批准 V2 规格，消除范围、概览并发刷新和告警时间筛选歧义，可进入独立生产实现规划。

## Not yet specified

<!-- 当前没有仍处于雾中的范围；新浮现且已可精确定义的问题均已毕业为票据。 -->

## Out of scope

- 性能分析页、诊断页、链路 trace/百分位/PerformanceState、Watch 遥测上报、诊断包及其保留/存储/API；范围收缩后不再进入 V2 规格。先前的[图表组件选择](issues/03-choose-wpf-chart-and-design-system-components.md)、[六区域原型](issues/04-validate-six-area-wpf-interaction-prototype.md)、[六页视觉行为](issues/05-lock-page-interaction-and-visual-behavior.md)、[延迟可观测契约](issues/06-define-end-to-end-latency-observability-contract.md)与[可观测存储/API DTO](issues/12-lock-observability-storage-and-versioned-api-dtos.md)决定均不进入新目标。
- 生产代码实现、实现票据拆分、发布迁移和现场部署；这些在 V2 规格获准后另行规划。
- 多 Host 汇总监控、跨站点集中大盘或 Host 自动发现。
- 调度、派车、装卸、生产操作命令，以及 TransportDemand 的创建、修改或删除。
- IngestAlert 的人工确认、指派、备注、手工关闭或另建工单系统。
- Web、WinUI 或其它 UI 技术迁移；本路线继续使用 WPF。
- 修改客户 Oracle 查询、增加 Oracle DDL/索引/CDC，或把 `DATES` 当作系统事件时间。
- GitHub Actions、自托管或云端 CI runner、分支保护和专用常开测试 VM；本期只交付本机自动化验收契约，未来需要持续集成时再另行规划。
