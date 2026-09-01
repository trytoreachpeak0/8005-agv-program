# Round 40（2026-08-04）— 实时 QUEUEING 诊断：调度下线与软件急停

## 用户授权

用户于 2026-08-04 确认唯一测试车是 **新基测试300c协作1**，并明确同意开始受控实验。授权范围来自前一轮提出的：绑定测试车建单、取消、调度上下线、软件急停与解除，以及前后校验和自动善后。

## 环境与实时边界

- 环境：`RIOT-CROSS-PROJECT-TEST`，RIoT build `2.2.0.30`。
- 车辆：只允许 `environment.local.json` 中名称精确等于 `新基测试300c协作1` 的 `testVehicleKey`。
- 实时地图：Round 39 观测为 `api测试2`，沿用既有已验证映射 mapId 30；配置文件里的 map 29 视为旧信息。
- 仅当车辆为 `IDLE`、无 processingOrder、无本车非终态订单、`ON_LINE`、`emergencyState=OK`、`breakSwitchState=MOVABLE`、`controlState=CONTROL_STATE_OK`、`locationState=LOCATION_STATE_RUNNING` 时开始。

## 场景

### S1 调度未启用

1. 将唯一测试车调度状态设为 `OFF_LINE` 并回查。
2. 创建只绑定该车、map 30、站点 1/3 的单段 move。
3. 确认订单保持 `QUEUEING(1)`，立即用字符串 `orderId`、数值 id、`upperId` 调用诊断，并对有效口径重复三次。
4. 先取消订单并确认终态，再恢复 `ON_LINE`。

### S2 可恢复软件急停

1. 空闲基线下调用该车 `triggerEmergency` 并回查 `CAN_RECOVER`。
2. 创建同类绑定订单并确认保持 `QUEUEING(1)`。
3. 同样探测三类 `orderKey` 并重复有效口径。
4. 先取消订单并确认终态，再调用 `cancelEmergency` 并回查 `OK`。

## 停止与善后

- 任一步车辆名称、地图、前置状态、订单归属或响应不符，立即停止后续场景。
- `finally` 只清理本轮创建且身份已保存的订单；不处理其它订单。
- 善后顺序：取消本轮订单 → `CAN_RECOVER` 时解除软件急停 → 恢复 `ON_LINE` → 回查 `IDLE/OK/ON_LINE` 与无本车非终态订单。
- 本轮不制造离路线过远、未定位、硬件急停、解抱闸或其它物理状态。
