# 决定 Demand 受理、执行身份与完成后防重边界

Type: grilling
Status: resolved
Blocked by: 01

## Question

MVP 如何从 MesIngest `ExternallyReadableDemandCatalog` 发现一个 `WIRE_TO_GATE` 候选，在最终读取时固定 AcceptedDemandSnapshot、CatalogRevision、DemandId、DemandRevision 和 TransportDemandKey，创建唯一本地执行身份，并在现场卸货后防止 MesIngest 仍可见、GONE／再现或服务重启造成重复派车？

决策必须分开 MesIngest 的只读事实、ControlServer 的执行承诺与完成事实，明确成功完成、操作员取消、异常终止和单纯 MES 消失各自使用 DemandId 还是 TransportDemandKey 作为幂等与抑制边界。

## Answer

用户于 2026-08-25 采用推荐值，确认以下 WIRE_TO_GATE MVP 边界：

1. **发现不构成执行承诺。** ControlServer 可以缓存完整 `ExternallyReadableDemandCatalog` 来发现 `WorkType = WIRE_TO_GATE` 的候选，但缓存可随时丢弃，不产生业务任务、车辆绑定、RIoT 调用或本地完成事实。候选选择顺序另由“决定单 Demand 选择、并发与等待策略”收口。
2. **承诺点必须无条件最终重读。** 在创建任何业务执行或远程副作用之前，ControlServer 无条件读取最新完整目录，不以发现时 ETag 获得的 `304` 代替承诺证据，并按原 `DemandId` 找回候选。按原 DemandId 已找不到时视为候选退出目录而不受理；最终目录的 `HistoryEpoch` 与发现目录不同时一律重新决策。找到且处于同一 HistoryEpoch 时，必须逐项比较完整 `ExternallyReadableDemandSnapshot` 决定元组：`SeriesId`、TransportDemandKey、世代、`DemandRevision`、`CreatedAt`、`ValueObservedAt`、值对应的 PollTrace／ProjectionCommit 身份及全部 `LiveMesFields`。任一项变化都不受理并重新决策；若只有无关候选使全局 `CatalogRevision` 前进，而该元组完全不变，则可以受理，并保存最终读取所得的新 `CatalogRevision`。
3. **受理事务冻结事实并先挡重复。** 同一持久化事务先确认该 `DemandId` 没有既有执行承诺、该 TransportDemandKey 没有活动本地任务、`TransportDemandSuppression` 或 `TransportDemandCompletion`，再原子保存完整不可变 `AcceptedDemandSnapshot`、最终 `HistoryEpoch + CatalogRevision`、接受时间、`DemandId`、接受时 `DemandRevision`、TransportDemandKey 与初始本地任务状态。任一唯一性冲突都返回已有事实或拒绝，不创建第二个执行；旧纪元缓存、snapshot 或目录身份不得跨纪元复用。
4. **`DemandId` 就是本地业务任务实例身份。** ControlServer、OnboardHmi、协议、审计与恢复都以 MesIngest 分配且不复用的 `DemandId` 精确引用该次执行，不再另造 `stationTaskId` 或平行的业务任务 ID；TransportDemandKey 只承担跨 Demand 世代的业务键与永久防重边界。每个 RIoT 移动、车载命令或其它外部副作用仍须在该 DemandId 下拥有各自稳定、持久化的幂等身份，不能拿 CatalogRevision 或 DemandRevision 充当远程调用键。
5. **承诺后的 MES 变化不改写本地事实。** 一旦受理，后续目录字段变化、退出目录、`GONE` 或新 Demand 世代都不能改写 `AcceptedDemandSnapshot`，也不自动取消、完成或重建任务；ControlServer 只把变化保留为来源漂移／对账证据，并按同一 DemandId 继续既有执行、恢复或人工处置。单纯 `MES_DISAPPEARED`／`GONE` 不写 `TransportDemandSuppression` 或 `TransportDemandCompletion`。
6. **正常成功使用独立的完成事实。** 在“决定机台取货、多仓装货、关卡卸货与成功边界”规定的现场卸货和安全闭环全部满足后，ControlServer 将该 DemandId 的本地成功终态与新的 `TransportDemandCompletion` 原子提交。`TransportDemandCompletion` 以 TransportDemandKey 为永久键并引用完成的 DemandId、接受时 DemandRevision、完成时间与完成证据；同键继续可见、GONE 后生成新 DemandId 或服务重启都不得再次受理、恢复或派发，不同 WorkType 形成不同键而不受影响。
7. **完成与取消保持不同语义。** 正常成功不写 `TransportDemandSuppression`。操作员取消、装货补偿取消、本站结束取消等既有取消原因继续将具体终态挂在 DemandId，并把对应 TransportDemandKey 的 `TransportDemandSuppression` 与终态原子提交；已完成具名货物交接的不可恢复故障终止同样按既有 `TERMINATED_BY_FAULT_CARGO_HANDOFF` 与永久抑制边界处理。
8. **可恢复异常不伪造终态。** 远程结果未知、断联、重启、车辆故障但尚未形成具名货物交接，以及能够证明未装货且可安全重派的异常，都保留原 DemandId 和原 AcceptedDemandSnapshot 收敛；不写完成或抑制、不创建新业务任务。只有既有恢复规则证明安全并收敛远程副作用后，才可在同一 DemandId 下继续或重派。
9. **MesIngest 始终只拥有只读来源事实。** `TransportDemandCompletion`、`TransportDemandSuppression`、本地任务终态和全部远程幂等状态都归 ControlServer；它们不回写、不隐藏也不修改 MesIngest 的 TransportDemand、DemandSeries、目录资格或告警。

由于当前 MES 没有可靠的业务发生编号，`TransportDemandCompletion` 当前永久且无解除入口。未来若需允许同一 TransportDemandKey 表示新的合法运输，必须先引入可靠的 MES 搬运发生身份，或另行批准具名授权且完整审计的解除机制，不能根据时间、GONE、新 DemandId 或人工猜测自动放行。
