# Round 44 执行日志（2026-09-28）

## 记录规则

- 未执行步骤保持未执行，不提前填写结果。
- 时间使用带时区的 ISO 8601 格式（`+08:00`）。
- 原始请求与响应全文在 `runs/http.ndjson`（一行一次调用，凭据写作 `<redacted>`）；状态采样在 `runs/samples.ndjson`（一行一次采样，字段见 `runner/README.md` 的统一采样记录）。两个文件都按 `phase` 字段区分阶段。
- 人工动作与现场口头报告按收到的时间写进同一时间轴，注明经谁转达。

## 环境

- RIoT：`http://172.19.206.222:8888`，凭据取自 `CONTROL_SERVER_RIOT_CALL_API_KEY`。
- 路由：每次脚本启动都核对，全程 `InterfaceAlias=Wi-Fi`，不经 Clash。
- 执行者：Claude 实现会话（经 Coordinator 8 与现场用户沟通）。

## 授权记录

| 时间 | 来源 | 内容 |
| --- | --- | --- |
| 2026-09-28 下午 | 用户（人在现场）经 Coordinator 8 转达 | 原话「RIoT 做吧」：同意做这项实测，不是放行每一步 |
| 2026-09-28 约 15:4x | 调度 | 车定为 `agv03`；`agv02` 归 `hmi#170`，不碰 |
| 2026-09-28 约 15:5x | 用户经调度逐项确认 | 运行 A 确认，含中止条件 1 的自动再急停；运行 B 做，并同意「锁住期间 CONTINUE 被接受就让它沿原路走完」（前提是运行 A 全部符合预期）；每个会让车动的命令前先要一句「就位」 |
| 2026-09-28 约 16:0x | 用户经调度逐项确认 | 路段 N19 通道：A 走 101→99，B 走 99→97；通道现场没人、没障碍；`speed=0.3` 同意（建单被拒就停，实际更快不中止、记为发现）；HELD 由脚本在车确实走起来时自动发 |
| 2026-09-28 稍后 | 用户经调度 | **改选选段一，N19 作废**：S=`T05-06`（151），D=`T06-02_T07-02_T07-03`（155），A 走 S→D，B 走 D→S；`speed=0.3` 照旧。用户手动把车挪到 151 定位并确认两条通道没人没车；拿到确认、S↔D 路径代价核对通过、调度回「用户已确认，可以开始」并转来第一个「就位」之后才建单 |

## 时间轴

### 只读准备（不在 `runs/` 的部分）

15:34 前后在 scratchpad 做过一次只读探测（车辆详情、全车列表、地图列表、25/26 号图站点与边表、未完成订单、路径代价），用来选车选段；结论已写进 `round-plan.md` §4，原始文件未入库。

### `pre-baseline`（`runs/` 中 `phase=pre-baseline`）

| 时间 | 车 | 结果 |
| --- | --- | --- |
| 15:38:59 / 15:39:01 | agv02 / agv03 | 脚本首版有缺陷（`$x?.y` 被 PowerShell 当成变量名 `x?`），读数全空，判 `MISMATCH`。修脚本时这两次的 `runs/` 输出被整个删除后重跑，**这两行不在 `runs/` 里**；它们不含车的状态，只是 5 个只读 GET |
| 15:39:17 | agv02 | `MISMATCH`：`locationState=ERROR`，不在站上（此时已切到 26 号图） |
| 15:39:20 | agv03 | `MISMATCH`：`currentMap=老厂前线new`（25 号图），不在站上 |
| 15:41:21 | agv02 | `MISMATCH`：不在站上，且在移动（现场操作中） |
| 15:41:22 | agv03 | `MISMATCH`：26 号图、已定位，但不在站上 |
| 15:50:29 | agv03 | `MATCH`：26 号图、已定位、站 212（充电准备点1）、`OK`、`IDLE`、名下无单。该站不作起点，见 `round-plan.md` §4.2 |

`-Ready` 闸门自检（15:5x，`-Run gatecheck`）：`create` 不带 `-Ready` → `REFUSED`，退出码 4，未发出任何请求。

### 运行 A

#### A0 `baseline`（16:06:15，`phase=A-baseline`）— `MATCH`

agv03：`currentMap=老厂前线new_wk`，`LOCATION_STATE_RUNNING`（置信度 63%），`currentStation=151`（`T05-06`），坐标 `(-63559, -35704)`，`emergencyState=OK`，`breakSwitchState=MOVABLE`，`controlState=CONTROL_STATE_OK`，`status=1`，`procState=IDLE`，`processingOrder=false`，`movementState=MT_FINISHED`，两个接口车速均 `0.0`，电量 92%，`loadState=0`，`existedInGroup=[]`，名下未完成订单 0。

#### A1 `routecheck`（16:06:18，`phase=A-routecheck`）— 超出事先阈值，停

请求 `POST /api/task/v1/route/getRouteCostsBy` `{"mapId":26,"stationId":155,"deviceKeys":["BROKERX-7daca4ee…1127"]}`，返回 `costs=32270`、`message=ok`。

事先写的判据是「与自算 31021 相差 ≤1000」，实查多 **1249 mm**，超出，按计划停下报调度，未建单。

- 读到的：自算值是路网边表上 151→155 最短路 14 条边的 `cost` 之和，等于这些边的欧氏长度之和（31021 mm）。
- 推的：这不是另一条路线——去掉最短路上任一条边后，151→155 的最短路是 84795 mm，与 32270 相去甚远。差值更像是 RIoT 的代价比纯边长多计了一部分（这条路有两处 90° 拐角）。`BC-MAP-003` 里「`Edge.cost` 与 `getRouteCostsBy` 同量纲」原本就标为推断、没在同一对起终点上直接对比过；本次是第一次对比，差 4%。
- 阈值是本轮自定的，用来发现「RIoT 规划了另一条路」；是否在这个解释下继续，交用户决定。

#### 授权（约 16:07，经调度）

用户同意在上述解释下按 32270 继续；运行 B 的 D→S 阈值改为「差值 ≤2000 mm 且不超过次短路径」。调度转来 `用户已确认，可以开始` 与第一个「就位」（用户在车旁，手能碰到物理急停）。

#### A2 `create` + 自动 `held`（`phase=A-create` / `A-held`）— `MATCH`

- 16:08:26 `POST /api/order/v1/add/byDefaultMissions`，body `{"appointVehicleKey":"BROKERX-7daca4ee…1127","mission":[{"type":"move","mapId":26,"destination":155,"speed":0.3}],"orderName"/"upperId":"riot-behavior-lab-R44-A-20260928-160825","isAppointEnable":1,"lockStatus":0}` → `code=0`，`orderId=order-2104483377808801792`，数值 `id=1733821`；回显的 mission 带 `"speed":0.3`。
- 16:08:31 `orderState=3`、`PROCESSING_ORDER`、`MT_RUNNING`，车速 0.019。
- 16:08:33 两个接口车速均 **0.3**，累计位移 301 mm → 脚本自动 `POST /api/task/v1/order/command/order-2104483377808801792` `{"commandType":"CMD_ORDER_HELD",...}` → `code=0`。
- 16:08:34 `orderState=7`、`USER_FORCE_IDLE`、`MT_PAUSED`、车速 0；该采样与上一采样间位移 316 mm（制动过程）。
- 16:08:35 位移 3 mm；16:08:37～16:08:40 位移均为 0，车速 0。稳定 ≥5 秒，判 `MATCH`。
- 附带发现：mission 的 `speed` 字段**生效**——下单 0.3，行驶中读到的车速就是 0.3（此前仅 `SCHEMA`）。

#### A2'（约 16:09，经调度）

用户口头报：车停稳了，没有蠕动。

#### A3 `trigger`（`phase=A-trigger`）— `MATCH`

- 16:09:36 `POST /api/device/v1/command/sync/service/BROKERX-7daca4ee…1127/triggerEmergency`，body `{"messageId":768210,"mqCallback":{"tag":"string","topic":"string"},"thingsProperties":{}}`，213 ms → `code=0`，`data.responseState=RESPONSE_OK`。
- 16:09:37 首次回读即 `emergencyState=CAN_RECOVER`。
- 16:09:37～16:09:48 共 8 次采样：`orderState=7`、`USER_FORCE_IDLE`、`MT_PAUSED`、车速 0、位移 0，全程不变。

#### A4 `release`（`phase=A-release`，经调度转来「就位」后带 `-Ready`）— `MATCH`

- 16:10:52 `POST /api/device/v1/command/sync/service/BROKERX-7daca4ee…1127/cancelEmergency`（body 形状同 A3，`messageId=801016`），474 ms → `code=0`。
- 16:10:54、16:10:55、16:10:56 回读仍 `CAN_RECOVER`；16:10:57 读到 `OK`（发出到解开约 5 秒）。其间 `orderState=7`、车速 0、位移 0。

#### A5 `observe`（`phase=A-observe`）— `MATCH`

- 16:11:00～16:11:59 共 42 次采样：`orderState` 42 次均为 `7`，`USER_FORCE_IDLE`、`MT_PAUSED`、`emergencyState=OK`，两个接口车速均 0。
- 16:10:57（A4 末次）到 16:11:00（A5 首次）之间约 3 秒无采样（两阶段衔接），前后读数相同。
- 16:11:44、16:11:45 两次坐标变化 6 mm、5 mm（车速 0），下一采样即回 0。推的：定位读数抖动；远低于中止判据 50 mm，照实记录。

#### A5'（约 16:12，经调度）

用户在现场确认车没动过；同时给出 A6 的「就位」。

#### A6 `continue`（`phase=A-continue`，带 `-Ready`）— `MATCH`

- 16:13:06 `POST /api/task/v1/order/command/order-2104483377808801792` `{"commandType":"CMD_ORDER_CONTINUE_FROM_HELD","disableVehicle":false,"reason":"riot-behavior-lab-R44-A-continue"}`，161 ms → `code=0`。
- 16:13:07 首次回读即 `orderState=3`、`PROCESSING_ORDER`、`MT_RUNNING`；**但车速 0、坐标不变，车辆卡片 `sysState=PAUSE`、车辆详情 `state=PAUSE`、`paused=true`，持续到 16:13:21**。
- 16:13:22 `state`/`sysState` 变 `EXECUTING`；16:13:23 车速 0.3、位移 234 mm。从命令到真正起步约 16 秒，在事先时限 20 秒内。

#### A7 `run-to-end`（`phase=A-run-to-end`）— `MATCH`

- 16:16:13 `orderState=5`、`currentStation=155`、`IDLE`、`MT_FINISHED`。行驶车速 0.3。
- 行驶中车速为 0 的停顿（`orderState` 始终 3，`movementState` 始终 `MT_RUNNING`）：
  | 时间 | 位置 | 朝向 | `state` | 解读 |
  | --- | --- | --- | --- | --- |
  | 16:13:45～16:13:52 | 拐角 `(-56630, -35670)` | 12 → 1572 | 先 `PAUSE` 约 2 秒，后 `EXECUTING` | 原地转向（朝向在变）；其前约 2 秒的 `PAUSE` 原因未明（未询问） |
  | 16:14:08～16:14:13 | 拐角 `(-56634, -31256)` | 1575 → 3140 | `EXECUTING` | 原地转向 |
  | **16:14:53～16:15:29** | **直道中段 `(-65590, -31227)`，站 159/160 附近** | **3140 不变** | **`PAUSE`，`paused=true`** | **现场人员靠近导致避障暂停**（用户口述，经调度转达），`sysState=PAUSE`，无故障码，`emergencyState=OK`，本实验此时无任何写请求 |
  | 16:15:48～16:15:54 | 直道 | 不变 | `PAUSE` | 自停约 6 秒，原因未明（未询问） |
- `controlState` 从 16:08:31 订单开始执行起一直是 `CONTROL_STATE_ERR`，到 16:16:13 到站才回 `OK`；它**早于**急停出现，不能把上述停顿归因于急停。`paused` 字段在基线空闲时也是 `true`，不能单独用。
- 以上停顿中 `movementState` 始终是 `MT_RUNNING`，显示暂停的是 `state`/`sysState`。

#### A8 `final`（`phase=A-final`）— `MATCH`

16:16:15：名下无未完成订单，`OK`，`IDLE`，静止，`currentStation=155`。

### 运行 B

#### B0 `baseline` + `routecheck`（`phase=B-baseline` / `B-routecheck`）— `MATCH`

- B0：`currentStation=155`，26 号图，已定位，`OK`，`IDLE`，名下无单。
- 16:17:08 `getRouteCostsBy` `{"mapId":26,"stationId":151,...}` → `costs=32060`、`ok`。自算 31060，差 1000 mm（阈值 ≤2000）；155→151 在路网上只有一条路（去掉其上任一条边即不可达），判为同一路线。

#### 授权（约 16:19，经调度）

运行 B 建单的「就位」：用户在车旁。

#### B1 `create` + 自动 `held`（`phase=B-create` / `B-held`）— `MATCH`

- 16:20:00 建单 155→151，`speed=0.3` → `code=0`（`orderId`/`upperId` 见 `runs/state-B.json`）。
- 16:20:05 `orderState=3`；16:20:07 车速 0.3、累计位移 315 mm → 自动 `CMD_ORDER_HELD` → `code=0`。
- 16:20:08 `orderState=7`、`USER_FORCE_IDLE`、`MT_PAUSED`、车速 0（该采样位移 166 mm，制动过程）；16:20:09～16:20:15 位移 0。
- 判据要求 HELD `code=0` 且 `orderState=7` 且静止 5 秒，避障停车（订单仍 3）不会满足。

#### B1'（约 16:20，经调度）

用户确认车停稳、没有蠕动。

#### B2 `trigger`（`phase=B-trigger`）— `MATCH`

- 16:20:58 `triggerEmergency`（messageId=867375），129ms → `code=0`。
- 16:21:00 首次回读即 `CAN_RECOVER`；16:21:00～16:21:10 共 10 次采样：`orderState=7`、`USER_FORCE_IDLE`、`MT_PAUSED`、车速 0、位移 0。

#### B3 `continue-in-emergency`（`phase=B-continue-in-emergency`，经调度转来「就位」后带 `-Ready`）— 无事先预期，记为发现

- 16:24:06.888 `POST /api/task/v1/order/command/order-2104486291436601344` `{"commandType":"CMD_ORDER_CONTINUE_FROM_HELD",...}`，173 ms → HTTP 200、**`code=0`**。
- 16:24:08～16:24:27 共 17 次采样：**`orderState=3`、`PROCESSING_ORDER`**，`emergencyState=CAN_RECOVER`，`movementState=MT_PAUSED`，车速 0，位移 0。
- 即：急停锁住期间 `CONTINUE_FROM_HELD` 被接受，订单立即由 `HELD(7)` 回到 `EXECUTING(3)`；此后让车停着的只有急停。

#### B4 改做法（约 16:25，经调度）

原方案 B4 是「解除急停，允许车自己沿原路走完」。用户改为**先取消这张单、再解除急停，不让车自己走**，按 `round-plan.md` §9 的中止收尾顺序。因此「B3 被接受后解除急停，车会不会自己走」这一格**本轮没有做**。

#### B4-1 `cancel-order`（`phase=B-cancel-order`）— `MATCH`

- 16:25:49.940 `POST /api/task/v1/order/command/order-2104486291436601344` `{"commandType":"CMD_ORDER_CANCEL",...}`，93 ms → `code=0`。
- 16:25:53 `orderState=2`、`IDLE`、`MT_FINISHED`、`emergencyState=CAN_RECOVER`、车速 0；`currentStation=0`（两站之间）。
- 16:25:54 以 `final` 阶段只读复读一次（`phase=B-final`，此时急停仍锁，故该阶段判 `MISMATCH` 是预期的，不是异常）：名下无未完成订单，读数同上。
- 附带：急停锁住时 `CMD_ORDER_CANCEL` 可用。
- 脚本改动（**本轮临时加的，原计划没有**）：`release`/`observe` 原写死「订单保持 7，否则立即再急停」。订单已取消成 2 后照原样跑会误触发急停，所以增加 `-ExpectOrderState`（默认 7），B4-2 传 2。运动判据（车速 >0.005 或位移 >50 mm 即再急停）不变。调度确认过这个改动。

#### B4-2 `release` + `observe`（`phase=B-release` / `B-observe`，经调度转来「就位」后带 `-Ready`，`-ExpectOrderState 2`，不带 `-ExpectResumeAfterRelease`）— `MATCH`

- 16:26:57.963 `cancelEmergency`（`messageId=346496`），161 ms → `code=0`。16:26:59～16:27:01 仍 `CAN_RECOVER`，16:27:02 读到 `OK`。
- 16:27:04～16:28:03 共 50 次采样：`orderState=2`、`IDLE`、`MT_FINISHED`、`emergencyState=OK`、车速 0，位移全部为 0。

#### B5 `final`（`phase=B-end-final`）— `MATCH`

16:28:05：agv03 名下无未完成订单，`OK`，`IDLE`，静止，`currentStation=0`（站 155 与 151 之间）。车回原位由用户手动处理，本轮不再发单。

#### 收尾后的人工事件（用户口述，经调度转达）

- 用户目视确认：B4-2 解除急停后车没动。
- 此后用户**手动**把 agv03 开回原位。车在 16:28:05 之后的任何位置变化都来自这次手动操作，不属于本轮观测；本轮没有再读取车辆状态。

### 旁证与核对

- **没有任何请求发给 agv01**：`runs/http.ndjson` 中 agv01 的 `deviceKey` 只出现在两次全场未完成订单列表 GET 的**响应**里（`A-baseline` 16:06:15、`A-create` 16:08:25），是 agv01 自己的在途单 `order-2104482765746601984`（25 号图，目的站 81 `N15-1_N16-1`，坐标约 `(-33360, 32980)`，与本轮的环在 y 方向相距 60 米以上）。
- 凭据：959 次调用的认证头全部写作 `<redacted>`；以密钥中段 12 与 20 字符子串检索本目录所有文件均 0 命中。
- 全部写请求：A 建单、A HELD、A 急停、A 解除、A CONTINUE；B 建单、B HELD、B 急停、B 锁住期间 CONTINUE、B 取消、B 解除。共 11 个，全部指向 agv03 的 `deviceKey` 或本轮自建的两张订单。

## 本轮结论

每一格各观测 1 次（格 1 为 A、B 各 1 次）。RIoT 生产实例，地图 26，agv03，2026-09-28。

| # | 格 | 结果 | 等级 |
| --- | --- | --- | --- |
| 1 | `HELD(7)` 时 `triggerEmergency` | 急停锁住 `CAN_RECOVER`；订单仍 7、`USER_FORCE_IDLE`、`MT_PAUSED`，车静止 | 读到的（A3、B2） |
| 2 | 接着 `cancelEmergency` | 约 5 秒读到 `OK`；之后 60 秒订单一直是 7、车速 0、坐标不变，现场确认没动。**HELD 在急停解除后保持，车不会自己走** | 读到的（A4、A5） |
| 3 | 解除后 `CONTINUE_FROM_HELD` | `code=0`，订单立即 3，跑到 `SUCCESS`；**但约 16 秒后车才起步**，其间订单 3、`MT_RUNNING`、车速 0、`state=PAUSE` | 读到的（A6、A7） |
| 4 | 急停锁住期间 `CONTINUE_FROM_HELD` | **被接受**，`code=0`，订单 7→3；急停挡住，20 秒内车不动 | 读到的（B3） |
| 5 | 格 4 之后解除急停，车会不会自己走 | **本轮没做**（用户决定先取消订单）。按 Round31「EXECUTING 时急停，解除后自行继续」推断会走 | 推的 |
| 6 | 急停锁住时 `CMD_ORDER_CANCEL` | `code=0`，订单 2；之后解除急停，车不动 | 读到的（B4） |
| 7 | mission `speed` 字段 | 下单 0.3，行驶车速读到 0.3，生效 | 读到的（A、B） |
| 8 | `getRouteCostsBy` 与边表长度之和 | 151→155 实查 32270 / 边长和 31021；155→151 实查 32060 / 31060，均为唯一或远优于次短的同一路线 | 读到的 |
| 9 | 行驶中的自停 | 人员靠近时避障暂停 36 秒（用户口述）：订单 3、`MT_RUNNING`，只有 `state/sysState=PAUSE`；另两次短停原因未明 | 读到的 + 用户口述 |
| 10 | `controlState` | 订单执行期间一直 `CONTROL_STATE_ERR`（从执行开始，早于急停），到站回 `OK` | 读到的 |

对 `8005-agv-control-server#335` 的推论（推的）：先 `OrderHold` 再急停，门锁恢复后自动 `cancelEmergency` 本身不会让车动；是否继续由之后是否发 `CONTINUE_FROM_HELD` 单独决定。**顺序必须是先解除急停并回读到 `OK`，再发 CONTINUE**；急停锁住期间绝不能发 CONTINUE（格 4、5）。CONTINUE 之后不能以 `orderState=3` 判定车已在走（格 3）。

- 已回答问题：见上表 1～4、6～10。
- 仍未回答问题：格 5；格 3 的 16 秒起步延迟是否与刚解除过急停有关（Round36 未记录车速/坐标，无对照）；样本量均为 1。
- 与历史轮次差异：`BC-VEH-005` 记「`controlState` 可能短暂 `ERR` 后回 `OK`」；本轮执行期间 `ERR` 持续整个订单，与急停无关。`BC-MAP-003` 的「`Edge.cost` 与 `getRouteCostsBy` 同量纲」首次直接对比：同量纲，但后者多约 1 米（3%～4%）。
- 新增风险：急停锁住期间 CONTINUE 被接受，会把「解除急停」变成事实上的「放车走」。
- 建议下一实验：格 5（空载、现场确认后）；HELD→CONTINUE 无急停的起步延迟对照。
