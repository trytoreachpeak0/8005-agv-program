# Round 41（2026-08-04）— 离路线过远的实时 QUEUEING 原因

## 人工前置

用户于 2026-08-04 回复“已移离路线，车辆静止”，表示已将唯一测试车 **新基测试300c协作1** 人工移离地图路线并保持静止。

## 自动前置门禁

只有以下条件全部成立才创建订单：

- 实时车辆名称精确等于“新基测试300c协作1”。
- 地图为 `api测试2`（mapId 30）。
- `IDLE`、无 processingOrder、无本车非终态订单、速度 0、`movementState=MT_FINISHED`。
- `ON_LINE`、启用、`emergencyState=OK`、`breakSwitchState=MOVABLE`、`controlState=CONTROL_STATE_OK`、`locationState=LOCATION_STATE_RUNNING`。
- `getRouteCostsBy` 对 map 30 的站点 1～6 均返回 `costs=-1` 与 `vehicle route to station unreachable`。

## 实验步骤

1. 保存车辆、订单和六个路线代价的前置证据。
2. 创建只绑定测试车、map 30、目的站 3 的单段 move。
3. 确认订单保持 `QUEUEING(1)`，不进入 EXECUTING。
4. 使用已经确认的字符串 `orderId` 调用原因诊断，重复三次；同时再次核对路线仍不可达。
5. 立即取消本轮订单并确认 `CANCELLED(2)`。
6. 确认车辆仍静止、IDLE、无本车非终态订单。

## 异常善后

- 任一前置不符，不创建订单。
- 创建后任一异常均在 `finally` 中只取消本轮已保存身份的订单。
- 本轮不改变定位、急停、抱闸、调度上下线或地图；车辆物理位置由用户在实验结束后人工恢复到路线。
