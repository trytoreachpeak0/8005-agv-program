# 决定单 Demand 选择、并发与等待策略

Type: grilling
Status: resolved
Blocked by: 01, 02

## Question

在只有一台指定 AGV、同一时刻只运行一个 `WIRE_TO_GATE` TransportDemand 的 MVP 中，多个合格 Demand 同时存在时如何稳定选择，什么时候得以承诺给该 AGV，忙碌、低电量、配置缺失、结果未知或当前任务未收敛时如何保留等待与告警事实，且不引入多车评分、复合运输或预绑忙车？

## Answer

用户于 2026-08-25 明确回复“全部使用推荐值”，逐项采用本票 grilling 前沿 Q1～Q3 的推荐值，并确认以下 `WIRE_TO_GATE` MVP 边界：

1. **单车、单 Demand 是从受理到收敛的排他边界。** MVP 只处理 MesIngest 发布的完整 `WIRE_TO_GATE` WorkType，只使用一台指定 AGV；同一时刻最多有一个已经受理但尚未收敛并释放车辆占用的 DemandId。一个 Sublot 可以一次使用多个安全可用仓位，但不得把多个 Demand、多个 Sublot 或其它 WorkType 合并到同一执行，不得途中追加新 Demand、建立复合运输或借本票引入换车逻辑。多个合格候选可以同时保留在 ControlServer 的共享未分配集合中，但不因此成为已接受任务或车辆计划。
2. **候选先经过完整硬准入，再进入稳定排序。** ControlServer 只从当前 `ExternallyReadableDemandCatalog` 中考虑 `WorkType = WIRE_TO_GATE`、未被既有 DemandId 执行承诺占用、且其 TransportDemandKey 未命中活动任务、`TransportDemandSuppression` 或 `TransportDemandCompletion` 的候选。未映射 AREA 表示不属于 8005 执行范围，继续静默跳过且不报警；已经进入本 MVP 执行范围的 Demand 若缺少必要站点、车辆或策略配置，则按结构性阻断处理，不能把两者混为一类。
3. **保留两层静态硬白名单，不实现多车策略面。** 指定 AGV 必须具有显式 `(agvId, WIRE_TO_GATE)` `VehicleTaskTypeAdmission`，并且对 Demand 所属 DispatchZone 具有显式 `DispatchZoneVehicleAdmission`；缺失、未知或未配置均默认拒绝。MVP 可以使用受控的预置配置，不要求为这两类关系建设配置 UI；`DispatchZoneVehiclePreference`、多车回退、车辆公平性、`VehicleMarginalRouteCost`、`RouteCostEquivalenceBand` 和其它多车评分层全部不进入首期。
4. **指定 AGV 必须当前即可合法承接，才有资格被承诺。** 至少同时满足：AREA 能唯一落入预期 DispatchZone 和 Map；固定关卡站点存在且与机台端点同图；车辆当前 Map 明确且一致；到下一站可达性有可信证据；车辆处于 `VehicleBusinessReadiness`；没有未终结 Demand、DispatchGeneration、RIoT 订单占用、仓位操作或结果未知事实；仓位配置已就绪，当前能力、管理可用性及安全可用仓位足以完整容纳该 Sublot；当前电量和预计任务后余量通过已批准电量策略。距离近、空仓较多、等待较久或人工选择都不能覆盖任一硬门禁。可达性已确认但单车排序不需要的新增行程成本缺失时，不单独阻断本 MVP。
5. **多个合格 Demand 使用任务优先的确定性顺序。** 全部任务先通过硬门禁，再按 `TransportDemandWaitingAge` 从长到短选择；MVP 只有一个 WorkType，因此不实现跨任务类型优先级带。等待年龄相同或业务层全部相同时，按本地创建时间从早到晚、再按 DemandId 稳定升序裁决。不得使用 MES `DATES`、随机数、数据库未声明顺序、距离或车辆评分改变该顺序。`TransportDemandWaitingAge` 从 TransportDemand 在本地首次创建起连续累积，任何业务门禁、车辆忙碌或资源占用都不暂停或重置。
6. **排序结果在最终重读和原子承诺前仍只是候选。** ControlServer 选出当前第一名后，必须执行“决定 Demand 受理、执行身份与完成后防重边界”规定的无条件最终完整目录重读。最终目录仍处于发现时 `HistoryEpoch`，且候选仍存在并通过完整 `ExternallyReadableDemandSnapshot` 决定元组核对时，才在一个持久化事务中冻结 `AcceptedDemandSnapshot` 与最终 `HistoryEpoch + CatalogRevision`，并建立 DemandId 的唯一本地执行事实、指定 AGV 的排他占用、当前 DispatchGeneration／远程副作用意图及必要唯一性约束；事务成功前不得调用 RIoT、向车载端下发新操作或把任务显示为已接受。跨纪元、决定元组变化或并发唯一性冲突时不得勉强接受，必须重新读取当前事实并重新选择。
7. **忙碌和暂时资源不足进入共享 backlog，不预绑指定 AGV。** 指定 AGV 正在执行或收敛原任务、尚未取得 `VehicleBusinessReadiness`、仓位暂满或站点暂被占用时，所有未接受 Demand 保持 `UnassignedDemandBacklog`，继续累计原等待年龄；不得为忙车建立专属队列、未来预留、影子绑定或候补任务。相关车辆、仓位、站点或恢复事实变化后，ControlServer 重新执行完整 `TaskFirstDispatchSelection`，届时任何仍合格 Demand 都可以按稳定顺序成为第一名。
8. **低电量或电量未知是可恢复等待，不是任务级结构性无解。** 在已经存在有效、经批准电量策略的前提下，指定 AGV 当前电量不足、预计任务后余量不足或电量未知时，车辆退出本轮候选，Demand 保持 `UnassignedDemandBacklog` 并继续老化；系统形成可诊断的车辆级电量不足或电量未知提示，引导既有人工充电边界处理。人工充电或可信遥测恢复后重新执行选择，不取消、不抑制、不跳过原 Demand。MVP 不建设自动充电、充电排队或备用桩改派。若缺少的是投运所需的已批准电量策略或阈值配置，则属于必要配置缺失，按 `StructuralDispatchBlock` 处理。
9. **结构性无解立即告警，正常等待不使用未批准的时间阈值。** 地图不一致、固定站点缺失、全部可信路线不可达、必要车辆／分区／电量／仓位配置缺失等使该 Demand 不存在任何潜在合法执行路径时，立即形成按 DemandId 与稳定原因去重的 `StructuralDispatchBlock` 告警；同一原因持续存在只更新既有告警，不在每轮选择中重复新建。忙碌、暂时容量不足、站点暂占和有效策略下的低电量／电量未知仍是正常 backlog。MVP 不要求在首期标定或启用 `DispatchStarvationPromotion` 阈值；未有当前批准阈值时只累计并展示等待年龄，不产生时间型升级或跨任务类型提权，结构性阻断仍即时告警。阻断原因经重新核验确已消失后，当前告警停止持续并保留历史证据，Demand 以原等待年龄重新参与选择。
10. **已经承诺后的未知结果继续占住原 Demand 和车辆。** RIoT 建单、移动、车载命令、仓位结果、断联恢复或重启对账出现结果未知时，保留原 DemandId、AcceptedDemandSnapshot、AGV 绑定、DispatchGeneration、upperId／仓位操作尝试编号及全部幂等事实；不得释放车辆、创建第二个 Demand 执行、换号重试或把未知猜成失败。双重未知或事实冲突按既有恢复规则升级执行告警并继续对账；其它候选只因车辆被占用而留在正常 backlog，不为每个等待 Demand 复制同一执行异常告警。只有既有规则可靠证明原副作用不存在或已安全收敛，并重新通过全部派发前提后，才允许同一 DemandId 继续或按批准边界重新参加选择。
11. **ControlServer 拥有等待、排序、承诺和告警事实。** OnboardHmi 在承诺前不得把候选或 backlog 项表现为已接任务，也不得自行从 MesIngest 选单、按距离改序或判断结构性阻断；它只消费服务端已经承诺的当前唯一 Demand，以及后续协议票批准的车辆就绪、等待或阻断摘要。精确消息字段、页面文案、只读运维入口和告警展示由“决定 ControlServer／OnboardHmi 职责与 MVP 消息面”和原型票继续收口，不在本票扩张。

### MVP 明确收窄与排除

- 保留 DemandId 独立身份、同键冲突／完成／取消防重、硬准入、连续等待年龄、共享 backlog、结构性阻断、结果未知占用和恢复后重选。
- 不采用当前基线允许的同车多 Demand／多 Sublot 并存、途中追加、后续停靠换序、跨分区组合、换车、多车竞争、车辆软偏好、路径成本比较、综合评分或车辆公平性。
- 不启用未标定的防饥饿阈值；不把“等待较久”解释为可以绕过 Map、站点、电量、仓位、安全、业务就绪或恢复门禁。
- 不建设自动充电及其排队、预占、改桩能力；本票只决定普通搬运派车的电量硬准入和人工恢复后的重新选择。
- 不因本票修改 MesIngest 投影、已发布需求基线或长期产品范围；这些收窄仅构成当前 `WIRE_TO_GATE` 单场景 MVP 的实施适用性决定。

### Key evidence

- [WIRE_TO_GATE 单场景 MVP 与双仓库协作路线图](../map.md) — 单车、单 Demand、允许多仓位及多车／自动充电排除边界。
- [决定 Demand 受理、执行身份与完成后防重边界](02-decide-demand-acceptance-execution-identity-and-completion-deduplication.md) — 最终重读、原子冻结、DemandId 执行身份、完成／抑制与未知结果边界。
- [MVP 需求适用性证据矩阵摘要](../evidence/requirement-applicability-matrix-summary.md) — `REQ-0189`、`REQ-0194`、`REQ-0205`、`REQ-0328` 的单场景收窄提示；矩阵本身只是候选路由。
- [当前需求基线 v1.0.0](../../../requirements/baselines/current-requirements-v1.0.0.md) — `REQ-0189`～`REQ-0210`、`REQ-0328` 的已批准硬准入、排序、backlog、告警与结果未知规则。
- [决定复合运输、分区与多 SUBLOT 组合边界](../../current-requirements-baseline/issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md) 与 [决定派车评分、路网成本与无车响应升级规则](../../current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md) — 用户批准的分区、车辆白名单、任务优先、等待年龄、确定性并列和结构性阻断来源。
- [决定 RIoT 建单未确认时任务绑定、重试与释放边界](../../current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md) — 已绑定 Demand／AGV 在明确拒绝、超时和双重未知时的占用、对账与重派边界。
- [`CONTEXT.md`](../../../CONTEXT.md) — `VehicleBusinessReadiness`、`TaskFirstDispatchSelection`、`UnassignedDemandBacklog`、`StructuralDispatchBlock`、`DispatchBatteryEligibility` 等现有统一词汇。
- [ADR-cross-0014](../../../docs/adr/cross/0014-durable-command-acceptance-and-same-operation-reconciliation.md)、[ADR-cross-0028](../../../docs/adr/cross/0028-connected-session-requires-explicit-business-readiness.md)、[ADR-cross-0029](../../../docs/adr/cross/0029-unified-five-step-recovery-handshake.md)、[ADR-cross-0043](../../../docs/adr/cross/0043-server-enforces-global-sublot-reservation.md) — 未知结果不释放、业务就绪、恢复握手与全局占用约束。
