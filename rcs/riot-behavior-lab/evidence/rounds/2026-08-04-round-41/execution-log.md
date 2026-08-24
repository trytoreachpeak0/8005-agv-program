# Round 41 执行日志（2026-08-04）

## 当前状态

`COMPLETED`

用户已确认测试车人工移离路线并保持静止。脚本将先验证车辆安全状态和六个站点全部不可达；不满足时不创建订单。

## 执行结果

- 前置车辆为“新基测试300c协作1”，`IDLE / ON_LINE / OK / MOVABLE / CONTROL_STATE_OK / LOCATION_STATE_RUNNING / MT_FINISHED`，速度 0，本车非终态订单为 0。
- map 30 的站点 1～6 在建单前及订单 QUEUEING 期间均为 `costs=-1`、`vehicle route to station unreachable`，满足“仍定位但离路线过远”的独立证据。
- 绑定测试车的单段 move 成功创建并保持 `QUEUEING(1)`；字符串 `orderId` 连续三次得到 HTTP 200 / `code=0`，原因稳定为“以车当前的坐标为起点,以订单目的地为终点,无法规划路径”。
- `suggestList` 包含检查地图、人工把车移到可达路网、或取消后重发可规划订单。它只作诊断证据：8005 不自动移动实体车，不因该建议自动取消、重建或换号。
- 测试订单已取消并确认终态；最终车辆仍静止、IDLE、ON_LINE、OK、LOCATION_STATE_RUNNING，本车非终态订单为 0，`safeFinal=true`。

## 映射

| 原因 | 独立核验 | 项目处理 |
|---|---|---|
| 以车当前的坐标为起点,以订单目的地为终点,无法规划路径 | 当前订单仍 QUEUEING；目标地图/站点与车辆身份匹配；`getRouteCostsBy` 对候选站为 `-1/unreachable`；车辆保持定位但静止 | 保持下单阻断并转人工，把车辆安全恢复到可达路网后重新核验。诊断本身不授权自动 Cancel、重建、PriorityExec 或任何移动。 |

## 尚待完成

测试车物理位置仍在路线外。用户需人工把车辆恢复到地图路线并保持静止；随后只读复核至少一个安全站点恢复 `costs>0 / message=ok`、车辆状态正常且无非终态订单，Round 41 才可关闭。

## 第一次恢复复核

用户回复已恢复到路线并静止后，GET 前置门禁显示车辆确实静止、IDLE、ON_LINE、急停 OK 且保持定位，但 `breakSwitchState=UNMOVABLE`、`controlState=CONTROL_STATE_ERR`，因此脚本在任何路线探针之前停止。没有创建订单或执行状态写入。用户仍需把解抱闸/控制开关恢复为正常可移动状态，再做只读复核。

用户随后回复“已恢复 MOVABLE，车辆静止”；第二次只读复核写入 `runs-restore-attempt-2/`，不覆盖首次门禁证据。

第二次复核通过：车辆为 `MOVABLE / CONTROL_STATE_OK / IDLE / ON_LINE / emergencyState=OK / LOCATION_STATE_RUNNING / MT_FINISHED`，速度 0，本车非终态订单为 0；map 30 的站点 1～6 全部恢复 `costs>0 / message=ok`（分别为 5142、3802、5952、250、1411、4031）。车辆已从人工离路线场景完整恢复。
