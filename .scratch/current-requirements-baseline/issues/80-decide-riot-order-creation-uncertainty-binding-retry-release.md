# 决定 RIoT 建单未确认时任务绑定、重试与释放边界

Type: grilling
Status: resolved
Blocked by: 63

## Question

TransportDemand 已选中车辆并建立本地绑定、但 RIoT 常规建单没有得到可确认结果时，明确拒绝、传输超时、结果未知及按稳定 upperId 对账得到已存在或不存在分别应如何影响任务状态；何时保留原绑定并以同一业务意图重试，何时允许释放回调度或重新选车，任务何时才可进入“进行中”，以及如何防止重复订单、双重派车并保留完整审计？

## Evidence rows

`R03-A1571`，并继承[决定 RIoT 项目 API 白名单与调用安全边界](37-decide-riot-api-allowlist-and-call-safety-boundary.md)已批准的稳定 upperId、先对账后重试及结果未知时阻断规则。

## Answer

用户本人作为当前需求基线最终批准人，确认一个 TransportDemand 选定 AGV 并建立本地绑定后，先进入“建单确认中”。该状态独占 TransportDemand、AGV 和当前 DispatchGeneration 的稳定 `upperId`；该需求与车辆都不参与其它派发，不得换号、换车、重复建单或提前标记为“进行中”。

### 明确拒绝

建单被明确拒绝后仍须按原 `upperId` 确认订单不存在，再按原因分流：

1. 临时服务或容量问题，且原派发前提仍成立：保留绑定，在同一 DispatchGeneration 中以原 `upperId` 有限重试。
2. 仅当前车辆已不符合资格：在确认无 RIoT 订单后释放原车，TransportDemand 退回调度；若改选其它车辆，建立新 DispatchGeneration 和新 `upperId`。
3. 需求、端点、契约或鉴权问题：释放车辆但阻断该 TransportDemand，修复前不自动重派。

### 超时、结果未知与对账

建单超时或返回结果无法确认时，只使用原 `upperId` 对账：

- 查到订单时，只有存在唯一非终态订单，且其 `upperId`、指定车辆及当前 AgvLifecycleGeneration、地图、起终点均与原意图一致，并已取得完整 OrderRef 时，才完成 RIoT 订单接管确认并转为“进行中”。HTTP 或业务响应成功本身不足以转态。
- 查到多单、字段不一致或无法完整核验时，继续阻断，不得接管、释放或重派。
- 可靠确认订单不存在时，在原前提仍成立的范围内保留绑定，以原 `upperId` 有限重试；次数和退避时长仍留给正式 spec 配置。
- 建单调用和对账结果同时未知时，进入“建单结果双重未知”：继续保留全部绑定并升级告警，不因时间、重试次数或任何管理员操作强制释放。维护管理员或系统管理员只能查看审计、重新对账、暂停后续调用，或登记经独立核验的 RIoT 结果，不能把未知强制视为不存在。

若同号有限重试已耗尽，且最新对账仍可靠确认订单不存在，进入“建单重试暂停”：释放车辆，但 TransportDemand 不直接退回自动调度，并保留原业务意图和 `upperId`。只有 RIoT 服务恢复、全部派发前提重新通过后才可受控恢复；若需改选车辆，则闭合原代次并建立新代次。

### 对账时已是订单终态

若首次可靠对账已发现匹配订单为 `SUCCESS`、`FAILED`、`CANCELLED` 或 `DELETED`，不先标记“进行中”，也不直接重派，而是进入订单终态对账。`SUCCESS` 必须核对车辆实际位置、目标站点及后续业务事实；其它终态必须核对车辆位置、运动和安全状态、订单名额已释放以及 TransportDemand 仍有效。若最终允许重新派发，必须创建新 DispatchGeneration 和新 `upperId`，并保留与旧 OrderRef 的关联。

### 唯一性与审计

每个 DemandId 同时最多一个未闭合 DispatchGeneration，每辆 AGV 同时最多一个本项目未确认或未终结订单占用，每个 DispatchGeneration 只有一个不可变 `upperId`。并发竞争失败者不得覆盖已有绑定，必须重新读取当前事实。

每个 DispatchGeneration 形成不可改写的派发审计链，至少记录 DemandId、TransportDemandKey、DispatchGeneration、`upperId`、AGV 身份和生命周期、地图与起终点、派发前提快照、每次调用/对账/重试的结果、状态转换、释放或重派原因，以及人工证据的提交人和来源。审计用于追溯，不代替 RIoT 状态核验，也不作为请求重放源。
