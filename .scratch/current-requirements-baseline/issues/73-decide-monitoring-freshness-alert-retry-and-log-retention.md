# 决定监控新鲜度、告警升级、重试与日志留存规则

Type: grilling
Status: resolved
Blocked by: 63

## Question

车队/仓位看板的刷新和过期阈值、站点等待和无车可派等告警的触发/去重/升级对象、下发与轮询失败的重试次数和间隔、人工重试入口，以及业务与审计日志留存期限应如何分层；哪些参数必须是业务批准值，哪些可作为可调运维配置但仍需上下限和审计？

## Evidence rows

`R01-A0119`、`R01-A1913`、`R01-A1915`、`R01-A1923`、`R01-A2951`、`R01-A3047`、`R03-A0677`、`R03-A1505`、`R03-A1561`、`R03-A3078`、`R03-A3080`。

## Comments

- 2026-08-06：用户要求 MES 相关策略待定，原因是另一分支已有对应定义。此前讨论的 MES 轮询等待、失败重试和恢复条件全部撤回，不构成当前基线批准；当前实现中的默认值也不得反推为需求。待另一分支定义回流并核对后再决定 `R01-A2951` 及本票中的 MES 相关范围。已批准的车队/仓位看板 2 秒刷新规则不属于本次撤回范围。
- 2026-08-06：用户确认告警触发、去重、恢复和升级也由另一分支定义。已定位 `origin/codex/factory-validation` 下的「MesIngestWatch V2 产品与交互规格路线图」，其中「定义端到端延迟可观测契约」「定义 Alert、Demand 诊断与导出边界」「定义流畅刷新、游标分页与取消模型」仍为开放票据；本票不提前采纳其 Notes、原型或实现默认值，待对应决定关闭并回流后再核对。当前已批准的车队/仓位看板规则明确不适用于 MesIngestWatch 页面。
- 2026-08-06：用户批准将 MesIngest 告警的触发、去重、恢复、确认、关闭、升级、诊断和留存整体交由上述 MesIngestWatch V2 地图决定并回流；本票只固定全系统告警的可见对象，不对该分支范围形成平行定义。
- 2026-08-06：用户批准本票不制定通用的“下发/轮询重试 N 次”参数。空闲返回的导航/监听失败恢复及其相关人工入口由「决定空闲返回、停靠点资格与调度竞争边界」收敛；普通 RIoT 建单的明确拒绝、超时、结果未知、原 upperId 对账、重试与释放由「决定 RIoT 建单未确认时任务绑定、重试与释放边界」收敛。既有 `RIoTRetryReconciliation` 继续禁止不同副作用调用共用盲目重试次数。

## Answer

用户于 2026-08-06 逐项批准并最终确认以下监控展示、告警可见对象、重试决策边界和日志留存规则：

1. **车队与仓位看板采用统一的 2 秒刷新节奏。** 看板每 2 秒从 ControlServer 获取一次最新状态并支持人工刷新；2 秒是界面更新节奏，不是设备读取周期或读取超时。设备读取尚未结束时不得因为经过一个刷新周期就判定失败，也不得启动重叠读取。该规则不适用于 MesIngestWatch 页面。
2. **不可取得当前事实时直接表达原因，不引入“已过期”展示状态。** 对应设备连接失败时显示“设备连接失败”，连接正常但当前信息无法取得时显示“信息读取失败”；主看板不得继续把最后一次成功值呈现为当前值。最后一次成功值只可在排障详情中连同采集时间查看。TCP 明确断开仍立即按既有连接存活策略判定失联；其它连接失效继续沿用已批准的合法消息存活边界。
3. **告警可见对象按当前访问模型收敛。** 与当前 AGV、当前停靠或当前操作直接相关的告警显示在对应 OnboardHmi；全部 8005 告警集中显示在 ControlServer，维护管理员和系统管理员均可查看。查看告警不扩大其处置权限；第一版不发送短信、邮件或企业微信，也不恢复 R-12/R-13 为系统授权角色。
4. **服务端业务与管理员审计至少在线保留 180 天。** BusinessAuditRecord 与 AdministratorActionAuditRecord 在期限内必须可查询、导出，容量限制不得导致提前删除。超过 180 天后的继续保留、归档或清理由系统管理员配置，变更本身必须形成管理员操作审计记录。
5. **车载技术日志至少保留 30 天。** OnboardTechnicalLog 覆盖 IO 通信、信号变化、安全判断、执行阶段、配置、重启恢复和本地异常；车载存储须按验收负载配置到足以满足该期限，容量限制不得提前覆盖。关键安全与业务事件仍须实时摘要到 ControlServer，并按 180 天业务审计规则保存。
6. **MesIngest/MesIngestWatch 运维定义不在本票形成平行结论。** MES 轮询、刷新、告警触发与生命周期、诊断和本机日志留存等待 `origin/codex/factory-validation` 的「MesIngestWatch V2 产品与交互规格路线图」中相关开放票据关闭后，由[回流并核对 MesIngestWatch V2 运维定义](81-reconcile-mes-ingest-watch-v2-operability-definitions.md)逐项核对回流。当前定位的分支提交为 `a115ed4ac7de804b92ffaba8a9da8f0e6515dfc4`；其 Notes、原型、代码和实现默认值在票据未解决时均不构成当前基线批准。
7. **不制定跨调用通用的“重试 N 次”。** 空闲返回导航/监听失败及其人工恢复入口由[决定空闲返回、停靠点资格与调度竞争边界](76-decide-idle-return-parking-point-eligibility-and-arbitration.md)收敛；RIoT 常规建单的拒绝、超时、结果未知、原 upperId 对账、重试、人工入口与绑定释放由[决定 RIoT 建单未确认时任务绑定、重试与释放边界](80-decide-riot-order-creation-uncertainty-binding-retry-release.md)收敛。普通查询继续遵守既有 RIoTRetryReconciliation 的有限退避与固定错误不盲重试边界，具体次数和间隔属于正式 spec 的按调用配置，而不是本票的统一业务参数。
8. **已批准的相邻业务规则继续作为触发边界。** 站点离站等待、部分装货无进展和无车可派分别沿用既有 StationDepartureWaitPolicy、PartialLoadInactivity、StructuralDispatchBlock 与 DispatchStarvationPromotion 规则；本票只补足展示、可见对象和留存，不重新定义这些业务状态的触发阈值。

以上规则已同步写入根 [`CONTEXT.md`](../../../CONTEXT.md) 的 `MonitoringDashboardRefreshPolicy`、`MonitoringDataUnavailable`、`AlertAudiencePolicy`、`BusinessAuditRetentionPolicy` 与 `OnboardTechnicalLogRetentionPolicy`。
