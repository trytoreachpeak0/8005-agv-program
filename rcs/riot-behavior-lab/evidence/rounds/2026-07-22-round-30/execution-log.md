# Round 30 执行日志 — 未定位 / 离路线过远 → QUEUEING

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
- 澄清（现场）：两种情况都是**长期 QUEUEING**，不是 `HANG(9)`

## L 未定位（IDLE 下停定位后建单）

- `stopLocation` → `locationState=ERROR`
- 建单 `code=0`，uid `…R30-L-20260722-090950`
- 监视约 **120s**：一直 **`QUEUEING(1)`**，`executeVehicleKey=--`，车 `IDLE`
- **未进 HANG / EXECUTING**
- 清场后 `startLocation stationNo=1` → 恢复 `LOCATION_STATE_RUNNING`

## D 离路线过远

### D1（对照 / 未真正过远）

- 当时路由仍可达（例 dest=3 `costs=250`）
- 建单后约数秒进 **`EXECUTING`**，后被取消（`orderState=2`）
- **不能**当作「离路线过远」证据

### D2（真过远，重测）

- 路由探针：站 1～6 均为 `costs=-1`，`message=vehicle route to station unreachable`
- 仍 `locationState=LOCATION_STATE_RUNNING`、`proc=IDLE`
- 建单 `code=0`，uid `…R30-D2-20260722-092054`
- 监视约 **120s**：一直 **`QUEUEING(1)`**，`executeVehicleKey=--`，车 `IDLE`
- **未进 HANG / EXECUTING**
- 已 cancel 清场

## P 旋钮关机（IDLE + `runtime/status=offline` 后建单）

- 建单前：`runtime/status.type=offline`，API 仍可达（5G 独立供电）；路由 dest=3 `costs=7791`（**可达**，排除「过远」混杂）
- 建单 `code=0`，uid `…R30-P-20260722-093619`
- 监视约 **90s**：一直 **`QUEUEING(1)`**，`executeVehicleKey=--`，车 `IDLE`
- **未进 HANG / EXECUTING**
- 已 cancel 清场

## 结论

| 条件 | 建单 | 订单表现 | 旁证 |
|------|------|----------|------|
| 未定位 `locationState=ERROR` | `code=0` | 长期 QUEUEING | Round23 / 本轮 L |
| 离路线过远（仍定位） | `code=0` | 长期 QUEUEING | 本轮 D2；`getRouteCostsBy` → `-1` unreachable |
| 旋钮关机 `runtime/status=offline` | `code=0` | 长期 QUEUEING | 本轮 P（路由仍可达） |
| 解抱闸 `UNMOVABLE` | `code=0` | 长期 QUEUEING | Round29 F |
| 仅离站 `station=0` 但仍可达 | `code=0` | 可 EXECUTING | 本轮 D1 |

与 Round29 本体异常、Q-032 未定位同类：**不可走时新单进队不执行**，不要当成 `HANG(9)`。
