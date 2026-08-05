# MesIngestWatch V2 产品与交互规格路线图

## Destination

形成一份经交互原型评审确认、可直接交给实现阶段的《MesIngestWatch V2 产品与交互规格》：明确单 Host 只读运维台的信息架构、Demand/Alert/链路延迟分析、流畅刷新与游标分页、诊断导出、WPF 视觉体系及自动化验收标准。

## Notes

- 首要用户是现场实施与运维工程师；MesIngestWatch 不是生产操作 HMI、调度台或数据编辑器。
- 启动页须在约 10 秒内回答接入是否健康、当前异常、当前 VISIBLE TransportDemand 和最新链路耗时。
- 固定区域为：概览、运输需求、告警分析、性能分析、诊断、设置；左侧导航，默认浅色工业运维风格。
- 一次只连接一个 Host；Host/SQL Server 保存权威结构化遥测，Watch 通过只读 API 查询，文本日志只作取证。
- 区分“链路耗时”与 `MesCurrentStepEnteredAt (DATES)` 的“MES 数据年龄”。链路分为 MES 读取、接入处理、本地投影、Watch 展示四组，可下钻细阶段。
- 所有数据页默认手动刷新；按页可选自动刷新和频率，只刷新当前页。VISIBLE/GONE 各自保留筛选与游标分页状态。
- 查询显式提交；请求可取消、不重入、不排队，过期响应不得覆盖新结果。慢 Host 时 UI 必须保持可操作。
- Alert 只读分析，不提供确认、指派、备注或手工关闭。支持脱敏诊断包。
- 原始链路追踪默认保留 30 天，5 分钟聚合默认保留 365 天，Watch 本机事件默认保留 30 天；均可配置且有容量上限。
- 继续使用 .NET 8 WPF。正式实现前必须通过假数据交互原型评审；实现必须建立 WPF UI 自动化、截图视觉回归和 Windows CI 门禁。
- 相关会话优先使用 `prototype`、`domain-modeling`、`codebase-design` 与 `tdd` 技能；外部事实研究使用 `research`。
- 当前工作树含用户的 MesIngest.Watch 在途改动；只读分析并保留，不覆盖或重置。

## Decisions so far

<!-- Closed ticket decisions are indexed here; detail lives in each ticket. -->

- [建立现有能力与回归边界](issues/01-establish-current-capability-and-regression-baseline.md) — V2 保留 MesIngest 领域核心、Host 只读契约和 Watch 可靠性/浏览能力，增量替换产品壳与结构化观测面，并以版本化迁移和分层 Windows 门禁防回退。
- [选择 WPF 自动化与视觉回归测试栈](issues/02-choose-wpf-automation-and-visual-regression-stack.md) — 真实旅程采用 FlaUI.UIA3，确定性页面快照采用 Verify.Xaml，固定交互式 Windows runner 校准后再把全窗口像素回归升为门禁。
- [选择 WPF 图表与设计系统组件](issues/03-choose-wpf-chart-and-design-system-components.md) — 只新增 ScottPlot.WPF 并置于项目适配器后；其余设计系统、瀑布/时间线与虚拟化表格使用原生 WPF 实现。
- [验证六区域 WPF 交互原型](issues/04-validate-six-area-wpf-interaction-prototype.md) — 采用 A 全局态势主壳，将 C 证据时间线限定在诊断/性能页，并将 B 事件队列限定在告警分析页。

## Not yet specified

- 遥测契约确定后才能固定的 SQL Server 物理 schema、索引、聚合任务和只读 API DTO/版本迁移。
- 自动化框架研究与原型完成后才能固定的截图基线尺寸、CI 运行拓扑、失败证据和 flaky-test 治理规则。

## Out of scope

- 生产代码实现、实现票据拆分、发布迁移和现场部署；这些在 V2 规格获准后另行规划。
- 多 Host 汇总监控、跨站点集中大盘或 Host 自动发现。
- 调度、派车、装卸、生产操作命令，以及 TransportDemand 的创建、修改或删除。
- IngestAlert 的人工确认、指派、备注、手工关闭或另建工单系统。
- Web、WinUI 或其它 UI 技术迁移；本路线继续使用 WPF。
- 修改客户 Oracle 查询、增加 Oracle DDL/索引/CDC，或把 `DATES` 当作系统事件时间。
