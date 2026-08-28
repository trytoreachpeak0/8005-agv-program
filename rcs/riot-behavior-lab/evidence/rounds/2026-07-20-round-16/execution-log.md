# Round 16 执行日志（2026-07-20）

## 环境

- 测试车在 **新基测试2opt / mapId=28 / station=28**，`ON_LINE` + `IDLE`
- 测项：1 `curRemainCost`@EXECUTING；2 map28 闭环；4 `orderRecordPriorityExec`
- 不测：3 `order/route/{vehicleKey}`、5 `currentMapExistNotFinalOrderTask`（已挪入「以后可能需要」）

## 结论摘要

### 1) `curRemainCost`（EXECUTING）

- QUEUEING：`result = 9223372036854775807`（Long.MAX）
- EXECUTING + `MT_RUNNING`：出现真实剩余代价，且**阶梯下降**（非每秒平滑递减）  
  观测序列：`6280 → 6030 → 5070 → 4120 → 3180 → 1370`
- 单位与 `getRouteCostsBy` 的 costs 同为路径代价量级（mm）

### 2) map28 同图跑单

- 同图代价（站28出发）：1=`8220`，3=`28720`，4=`30302`，29=`11190`（均 ok）
- 建单 `28→1`：可进入 `EXECUTING`，车 `PROCESSING_ORDER` + `MT_RUNNING`
- **5 分钟内未到 SUCCESS**：后期长期停在 `remain=1370`、`station=0`（疑近终点受阻/等待），超时后 cancel 成功，车回 `IDLE`
- 结论：map28 **可派可跑**；本轮未采到完整到站 SUCCESS（与 map29 Round8 不同）

### 4) `orderRecordPriorityExec`

- 用法：`POST /api/order/v1/orderRecordPriorityExec?orderTaskKey={字符串orderId}`
- `orderTaskKey` 用字符串 `order-...` 即可，`code=0`
- 制造 A(EXECUTING)+B/C(QUEUEING) 后优先 C，再 cancel A：
  - **C 先进入 EXECUTING**，B 仍停留 QUEUEING
- 优先调用后 C 的 `orderState` 仍为 `1`（未见稳定停留在 `10`）；优先效果体现在**后续出队顺序**

## 证据

- `R0-same-map28-costs.json`
- `S1-dense-samples.json` / `S1-final.json`
- `S2-priority-calls.json` / `S2-watch-after-cancelA.json`
- `S2-final-cleanup.json` / `S2-final-idle.json`
