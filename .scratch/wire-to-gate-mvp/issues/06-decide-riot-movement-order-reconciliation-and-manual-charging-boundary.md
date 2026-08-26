# 决定 MVP RIoT 移动、建单对账与人工充电边界

Type: grilling
Status: resolved
Blocked by: 02, 03, 05

## Question

MVP 在 RIoT 中如何为指定 AGV 建立去机台取货和去关卡卸货的最小可恢复移动链，固定 OrderIntent、幂等键、车辆与目标绑定、建单结果未知对账、到站确认、移动安全撤销与重启恢复？

不实施自动充电时，还需决定什么电量事实阻断新任务、如何提示现场人工充电、充电后如何重新获得业务就绪，且不偷渡充电桩选择、排队或改派逻辑。

## Answer

用户本人作为 WIRE_TO_GATE MVP 产品范围批准人，于 2026-08-25 明确批准本票全部推荐值。

1. **一个 Demand 使用两段严格串行的单段移动。** `WIRE_TO_GATE` 固定为 `TO_PICKUP`（去已冻结机台站）和 `TO_GATE`（去已冻结关卡站）两个 WireToGateMovementLeg。接受 Demand 时冻结 `agvId + AgvLifecycleGeneration`、Map、机台 Station 与关卡 Station；每段分别拥有不可变的 MovementLegId、DispatchGeneration、OrderIntent 和稳定 `upperId`，任一时刻最多只有一段未收敛。`TO_PICKUP` 的 OrderIntent 随 Demand 承诺事务可靠保存；`TO_GATE` 只在机台 LoadBatch 和 StopClosureCommit 已成功、当前站物理操作全部安全收敛后另行可靠保存，不能提前向 RIoT 建单。两段不得共用 `upperId`，也不得合并成多站 RIoT 订单。

2. **车辆和目标绑定不能因外部登记变化而漂移。** 每次调用 `RoutineOrderCreationCall` 前，ControlServer 必须重新核验当前 RiotVehicleBinding、AgvLifecycleGeneration、Map、目标 Station、RouteCost、VehicleBusinessReadiness、RIoT 车辆订单名额及本段 PreDepartureSafetyCheck。OrderIntent 保存稳定的本地 AGV 身份、生命周期、预期 RIoT 绑定版本及精确目标；调用时的绑定缺失、换代或与冻结事实不一致一律阻断并进入对账，不得静默改用新的 `deviceKey`、车辆、地图或目标。远程调用只能在本地意图已持久化之后进行。

3. **可信到站采用完整站点作业门禁。** `ArrivalAtStation` 只作为进度和界面提示，不能单独开放扫码、装货或自动卸货。只有对应订单已独立回查为 `SUCCESS`、车辆为 `IDLE`、无未结调用、结果未知或失败订单阻断，OrderRef 目标与冻结目标一致，当前 Map/Station 可与目标一致解释，并取得新鲜停稳与安全证据时，才通过 StationOperationArrivalGate。机台通过后才能进入扫码与装货；关卡通过后才按当前任务与在车业务状态自动开始批量卸货。订单成功但位置、目标或停稳事实矛盾时 fail-closed；缺少证据时不得用同坐标、距离接近或单独的 `currentPosition` 猜测站点角色，MVP 配置不得使用无法可靠区分的同坐标多角色站点。

4. **未知、撤销和重启都沿用原意图收敛，不自动制造替代移动。** 建单或查询未知时继续独占原 DemandId、AGV、MovementLegId、DispatchGeneration、OrderIntent 和 `upperId`；可靠证明订单不存在后，才可在原前提仍成立时用原号有限重试。安全许可失效或行驶中车载断联时，已知本系统订单先执行 OrderHold 并核验停车；只有恢复对账完成、取得新的 PreDepartureSafetyCheck 且服务端明确授权后，才可对同一订单执行 OrderContinue。来源未知或非本系统订单按既有分层取消并在失败时升级 EmergencyStop。`FAILED`、`CANCELLED`、`DELETED`、目标不一致、双重未知或事实冲突均阻断后续移动段并进入既有恢复边界，不自动创建新 DispatchGeneration、换车或换号。ControlServer 重启后必须从持久化意图、OrderRef、RIoT 当前订单、车辆位置与运动状态、车载安全状态和未结保护动作重建唯一结论；内存阶段、旧 ArrivalAtStation 或单次接口成功都不能推动状态机。

5. **人工充电入口区分已知低电和事实未知。** 空闲车辆当前电量达到或低于 MandatoryChargeEntryThreshold，或预计执行候选 Demand 后无法满足最低任务后余量时，阻断普通新任务并在 ControlServer 与 OnboardHmi 明确提示“需要人工充电”；已经执行中的运输不中断，完成关卡卸货及本地成功提交后再进入 ManualChargingHold。电量未知或过期时同样 fail-closed，但提示为“电量事实未知，需要恢复遥测”，不得冒充低电或充电完成。MVP 不选择充电桩、不建立充电移动 OrderIntent、不排队、不预占、不改派，也不控制或判断充电过程。

6. **人工充电后必须显式且完整地重新投运。** 维护管理员或系统管理员须以个人账号提交“人工充电完成并请求重新投运”；普通操作员和电量遥测上升都不能单独解除 ManualChargingHold。ControlServer 随后必须确认电量遥测新鲜且达到 ChargingCompletionThreshold、`batteryState != CHARGING`、车辆 `IDLE` 且有可信停稳事实、Map 与位置可解释、无活动或结果未知的 RIoT 订单、全部 StationOperationGuard 和仓位操作已收敛，并完成 RecoveryHandshake 或等价的能力、未结操作、业务、物理与安全状态对账。全部通过后才重新授予 VehicleBusinessReadiness；积压 Demand 仍须重新执行完整 DispatchBatteryEligibility，人工重新投运不保证某个具体 Demand 必然可派。

本决定只定义普通搬运的两段移动和人工充电隔离边界，不授权自动充电、充电站点管理、外部系统绕过 RIoT 控车、人工把未知事实改写为安全，也不改变已接受的建单未知、移动安全介入、RIoT 调用确认和异常恢复规则。
