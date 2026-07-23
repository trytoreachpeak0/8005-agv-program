# Round 10 执行日志（2026-07-20）

## 0. 基线

- 测试车站 2，`procState=IDLE`，`vehicleTaskInfo.enable=true`，`integrationLevel=ON_LINE`，`movementState=MT_FINISHED`
- 注：`enable`/`integrationLevel` 在 **`vehicleTaskInfo`**，不在 `vehicle` 顶层；本轮 `vehicle.fleetMode=FLEET_MODE_OFFLINE` 仍可接单

## 1. 标识关联（ID-01）

建单 `byDefaultMissions` 后交叉查询：

| 标识 | 值（本轮样例） | 来源一致 |
|---|---|---|
| `upperId` | `riot-behavior-lab-R10-id-success-...` | create / detailByUpperId |
| 字符串 `orderId` | `order-2079069119654789120` | create / detailByUpperId / detailByOrderId |
| 数值 `id` | `488020` | detailByUpperId / detailByOrderId / `GET .../orderRecord/{id}` |
| `appointVehicleKey` | 测试车 key | create 回写 |

结论：`upperId` ↔ 字符串 `orderId` ↔ 数值 `id` 一致；`task/.../command/{orderKey}` 使用**字符串** `orderId`；`order/v1/operate` 使用**数值** `orderId`（见 §4）。

证据：`runs/ID-create.json`，`runs/ID-cross-query.json`

## 2. Q-004 幂等

| 场景 | 结果 |
|---|---|
| SUCCESS 后再提交相同 `upperId` | **拒绝** `code=0610008`，`message=订单已存在`；无新 `orderId` |
| EXECUTING 中再提交相同 `upperId` | **同上拒绝** `0610008` |

结论：本现场 `byDefaultMissions` 对相同 `upperId` **不创建第二单**（业务拒绝，非返回原单）。

证据：`runs/Q004-A-resubmit-after-success.json`，`runs/Q004-B-resubmit-while-executing.json`

## 3. 建单反例（NEG）

| 用例 | 结果 | 备注 |
|---|---|---|
| 伪造 `appointVehicleKey` | **意外成功** `code=0`，进入 `orderState=1 QUEUEING`，`execute=--` | 未派到真实车；本轮立即 cancel → `orderState=2` |
| 缺省 `appointVehicleKey` | **意外成功** `code=0`，QUEUEING，`appoint=""`，`execute=--` | 同上，有被调度器后派风险；已 cancel |
| `mapId=999999` | 拒绝 `0660003` 目的地站点不存在 | 未落库 |
| `destination=999999` | 拒绝 `0660003` | 未落库 |
| OFF_LINE 建单 | **SKIP** | API 无法可靠切 OFF_LINE（Q-020） |

**重大发现**：非法/缺失指定车 key **不会在建单接口拒绝**，会进队列；业务侧必须自己校验，且禁止省略 `appointVehicleKey`。

证据：`runs/NEG-create-results.json`，`runs/MESSAGES-utf8.json`（终态复查）

## 4. Q-006 续

### 4.1 `interrupt(pause=false)`

- 纯 move 执行中：仍 `code=100036`（与 `pause=true` 相同），订单继续跑。
- 证据：`Q006-pauseFalse-*`

### 4.2 `CMD_ORDER_HELD` / `CMD_ORDER_CONTINUE_FROM_HELD`

- HELD 成功 → `orderState=7`（PAUSED），`procState=USER_FORCE_IDLE`，`movementState=MT_PAUSED`，站号可变为 0
- CONTINUE_FROM_HELD 成功 → 回到 `orderState=3` / `PROCESSING_ORDER` / `MT_RUNNING`，最终 `orderState=5 SUCCESS`
- 证据：`Q006-held-*`，`Q006-continue-*`

### 4.3 `order/v1/operate` 取消

- body：`{ orderId: <数值id>, orderCommandDTO: { commandType: CMD_ORDER_CANCEL, disableVehicle: false } }`
- 成功，效果与 `task/v1/order/command/{stringOrderId}` 取消等价（本轮 `orderState=2`，车 `IDLE`）
- 证据：`Q006-operate-*`

### 4.4 含 `act` 的 interrupt

- `type=act`（`actionId=0`）可建单；`move+act` 可建单并进入执行（测试车）
- 在 **move 段** interrupt 仍 `100036`；本轮**未观测到 act 段正在执行时的 interrupt**（act-only 停留 QUEUEING/`execute=--` 后被 cancel）
- 状态：含 act 执行中 interrupt → 仍开放（需安全动作目录）

证据：`ACT-probe-results.json`

## 5. 收尾

- 最终：站 2，`IDLE`，`enable=true`，`ON_LINE`
- 脚本：`run-round10.ps1`
