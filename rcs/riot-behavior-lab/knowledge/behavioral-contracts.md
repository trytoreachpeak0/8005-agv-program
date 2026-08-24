# 已验证行为契约

本文件只收录能够指向证据的结论。静态 schema 描述但尚未现场观察的内容，不写入本文件。

## BC-AUTH-001 登录成败不能只看 HTTP 状态

- 结论：`POST /api/auth/v1/admin/login` 在密码错误时仍可能返回 HTTP 200；客户端必须检查响应业务 `code`。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-15
- 正例证据：[`../evidence/rounds/2026-07-15-round-1/runs/A1-login-success.json`](../evidence/rounds/2026-07-15-round-1/runs/A1-login-success.json)
- 反例证据：[`../evidence/rounds/2026-07-15-round-1/runs/A1-login-invalid-password.json`](../evidence/rounds/2026-07-15-round-1/runs/A1-login-invalid-password.json)
- 已观测结果：
  - 正确密码：HTTP 200，业务 `code=0`，返回 `tokenHead` 与 `token`。
  - 错误密码：HTTP 200，业务 `code=2009`，`message=密码不正确`，无可用 token。
- 适用范围：目前只直接证明登录接口。其他 RIoT 模块是否完全一致仍是待验证问题。
- 消费影响：`riot-sdk` 鉴权客户端应在 HTTP 成功后继续校验业务码。

## BC-AUTH-002 网页调用密钥可直接作为 Bearer 访问业务接口

- 结论：RIoT 网页「调用密钥设置」中的长期密钥，可作为 `Authorization: Bearer <callApiKey>` 访问业务只读接口；**不必**每次先调用 `POST /api/auth/v1/admin/login` 换取短时 token。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 正例证据：
  - [`../evidence/rounds/2026-07-20-round-2/runs/A2-map-success.json`](../evidence/rounds/2026-07-20-round-2/runs/A2-map-success.json)
  - [`../evidence/rounds/2026-07-20-round-2/runs/A2-devices-success.json`](../evidence/rounds/2026-07-20-round-2/runs/A2-devices-success.json)
- 反例证据：
  - [`../evidence/rounds/2026-07-20-round-2/runs/A2-map-no-auth.json`](../evidence/rounds/2026-07-20-round-2/runs/A2-map-no-auth.json)
  - [`../evidence/rounds/2026-07-20-round-2/runs/A2-map-invalid-key.json`](../evidence/rounds/2026-07-20-round-2/runs/A2-map-invalid-key.json)
- 已观测结果：
  - 正例（imap `mapInfo/all`、device `devices`）：HTTP 200，业务 `code=0`，返回业务数据；全程未登录。
  - 反例（无 Authorization / 伪造 Bearer）：HTTP **401**，响应 `code=401`，`message=暂未登录或token已经过期`，无业务数据。
- 适用范围：已直接证明 imap 与 device 只读探针。写接口、权限范围、密钥轮换/过期仍属开放边界。
- 消费影响：调度客户端默认鉴权路径可采用静态 `callApiKey`；`admin/login` 降为备用。业务接口鉴权失败应按 HTTP 401 处理，不要套用 BC-AUTH-001 的「登录失败仍可能 HTTP 200」特例。

## BC-VEH-001 可调度车辆清单不能直接用 devices 接口

- 结论：`GET /api/device/v1/devices` 返回的是**全部设备**（含门、电梯、风淋门等），不能当作车辆列表。可调度车辆应以 task 侧接口为准。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 正例/对照证据：
  - [`../evidence/rounds/2026-07-20-round-3/runs/B1-devices-all.json`](../evidence/rounds/2026-07-20-round-3/runs/B1-devices-all.json)（32 台，含非车）
  - [`../evidence/rounds/2026-07-20-round-3/runs/B1-getAllVehicleKeys.json`](../evidence/rounds/2026-07-20-round-3/runs/B1-getAllVehicleKeys.json)（18）
  - [`../evidence/rounds/2026-07-20-round-3/runs/B1-getAllVehicleSimpleInfo.json`](../evidence/rounds/2026-07-20-round-3/runs/B1-getAllVehicleSimpleInfo.json)（18）
  - [`../evidence/rounds/2026-07-20-round-3/runs/B1-vehicle-vs-device-diff.json`](../evidence/rounds/2026-07-20-round-3/runs/B1-vehicle-vs-device-diff.json)
- 已观测结果：
  - devices=32，task 车辆=18，交集=18；仅存在于 devices 的 14 台均为非车（自动门/电梯/风淋门等）。
  - 本现场可调度车观测特征：`deviceType=1` 且 `productKey=standard.oasis.300ul`（旁证，不单独作为过滤硬规则写入客户端，除非后续再验证）。
  - 分页旁证：`current+size` 翻页可能重复第 1 页；`current=1&pageSize=100` 可一次拉全。
- 适用范围：本现场实例；其他工厂设备构成可能不同，但“devices 含非车”结论应默认警惕。
- 消费影响：派车前车辆发现优先 `getAllVehicleSimpleInfo` / `getAllVehicleKeys`，不要把非车 key 填进 `appointVehicleKey`。

## BC-VEH-002 可用车辆名经 simpleInfo 解析 deviceKey

- 结论：`GET /api/task/vehicles/getAllVehicleSimpleInfo` 返回 `{deviceKey, deviceName}` 对；客户端可用**精确匹配** `deviceName` 得到 `deviceKey`，无需先登录换短时 token（配合 BC-AUTH-002）。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 正例证据：[`../evidence/rounds/2026-07-20-round-3/runs/B1-name-to-deviceKey.json`](../evidence/rounds/2026-07-20-round-3/runs/B1-name-to-deviceKey.json)
- 已观测结果：
  - `新基测试300c协作1` → 唯一 `BROKERX-aee2f93d717546cf9510c98c854fe83e`（与环境测试车 key 一致）。
  - 不存在的车名 → 0 命中。
  - 本轮 18 个车辆名全部唯一。
- 适用范围：已证明该只读解析路径；若出现重名必须失败而不是任选一台。写路径是否接受该 `deviceKey` 作为 `appointVehicleKey` 仍待建单实验。
- 消费影响：业务配置可存车辆显示名，运行时经 simpleInfo 解析 key；解析失败则拒绝下单。

## BC-MAP-001 可用 mapInfo 接口枚举现场地图

- 结论：现场有效地图可通过 imap 只读接口枚举；`mapId` = 返回项的 `id`，可读名为 `name`。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 正例证据：
  - [`../evidence/rounds/2026-07-20-round-4/runs/C1-mapInfo-all.json`](../evidence/rounds/2026-07-20-round-4/runs/C1-mapInfo-all.json)
  - [`../evidence/rounds/2026-07-20-round-4/runs/C1-mapInfo-excludeMapJson.json`](../evidence/rounds/2026-07-20-round-4/runs/C1-mapInfo-excludeMapJson.json)
- 已观测结果：
  - `GET /api/imap/v1/mapInfo/all`：HTTP 200，`code=0`，本现场 **18** 张地图。
  - `GET /api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson`：同样 18 张，适合日常枚举。
  - 两接口均可用调用密钥访问（衔接 BC-AUTH-002）。
- 适用范围：已证明枚举路径；**车辆当前绑定 mapId** 本轮未能从 `getVehicleInfo` / `getAllTaskVehicles` 对象直接读出（见 Round 4 线索文件），选图仍需业务确认。
- 消费影响：调度客户端应缓存/现查地图清单；建单前 `appointMapId`（或等价字段）必须来自该清单且经人工或规则选定。

## BC-MAP-002 可用 stations/{mapId} 枚举单图站点

- 结论：单图有效站点通过 `GET /api/imap/v1/mapInfo/stations/{mapId}` 枚举；本现场站点主键字段为 `id`，可读名为 `name`（即业务上的 stationId / stationName）。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 正例证据：
  - [`../evidence/rounds/2026-07-20-round-5/runs/C2-stations-map-29.json`](../evidence/rounds/2026-07-20-round-5/runs/C2-stations-map-29.json)
  - [`../evidence/rounds/2026-07-20-round-5/runs/C2-stations-overview.json`](../evidence/rounds/2026-07-20-round-5/runs/C2-stations-overview.json)
- 反例证据：[`../evidence/rounds/2026-07-20-round-5/runs/C2-stations-map-0-invalid.json`](../evidence/rounds/2026-07-20-round-5/runs/C2-stations-map-0-invalid.json)
- 已观测结果：
  - 成功：HTTP 200，`code=0`，`result` 为站点数组。
  - 字段：`id`、`name`、`type`、`pos.x`/`pos.y`/`pos.yaw`、`edge_id` 等。
  - 单站：`GET /api/imap/v1/mapInfo/{mapId}/{stationId}` 可用（例：29/1 → 站点1）。
  - 非法 mapId `0`：仍 `code=0`，但空数组——**不能**只凭业务成功码认定有站。
  - 候选图站点数：api测试(29)=2；新基测试1(26)=4；新基测试2(27)=31；新基测试2opt(28)=33。
- 适用范围：已证明读站路径；`stationId` 跨地图是否唯一未证明（四图均有 id=1）。建单目的站字段是否接受该 `id` 仍待写实验。
- 消费影响：MES/客户端应按 `(mapId, stationId)` 成对使用；先校验 stations 列表非空再派车。

## BC-STATE-001 车辆/设备状态应组合采样，勿只用 runtime/status

- 结论：读取“车在哪张图 / 哪一站 / 调度态”时，至少组合：
  1. `GET /api/task/v1/task/getVehicleInfo/{deviceKey}`（调度态；地图名在 `vehicle.previousState.mapName`）
  2. `GET /api/device/v1/runtime/properties/{deviceKey}`（物模型运行属性，含 `mapName`/`stationNo`/`sysState` 等）
  - **不要**把 `GET /api/device/v1/runtime/status/{deviceKey}` 当作主状态源（仅 online/timestamp）。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 证据：[`../evidence/rounds/2026-07-20-round-6/`](../evidence/rounds/2026-07-20-round-6/)
- 已观测：测试车 `mapName=api测试` → 反查 mapId=29；同日曾观测在站（`currentStation`/`stationNo`=1）与离站（见 BC-STATE-002）。
- 消费影响：选图可用 `mapName`↔地图清单 `name` 精确匹配；B2 实验卡应同时覆盖上述两面。

## BC-STATE-002 车不在站点时站号读成 0，不是丢图也不是失败

- 结论：车辆离开站点后，站归属字段会读成 **0**，并伴随 `noStation=true`；**地图名与坐标仍可读**。客户端必须把「站号=0」解释为**当前未归属任何站点**，不得当成站名“站点0”，也不得当成定位丢失或接口失败。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 在站对照：同日较早快照 `currentStation=1` / `stationNo=1` / `noStation=false`，`mapName=api测试`（见 Round6 前半段证据）
- 离站证据：[`../evidence/rounds/2026-07-20-round-6/runs/B2-off-station-snapshot.json`](../evidence/rounds/2026-07-20-round-6/runs/B2-off-station-snapshot.json)
- 已观测离站读数（测试车，map `api测试`）：
  - `getVehicleInfo`：`currentStation=0`，`currentNode=0`，`noStation=true`，`noNode=true`；`previousState.mapName` 仍为 `api测试`；`precisePosition` 仍有坐标（例 x=133,y=-258）；`procState=IDLE`，在线。
  - `runtime/properties`：`stationNo=0`；`mapName` 仍为 `api测试`；`currentPosition` 仍有坐标。
- 适用范围：已在本测试车、本地图上观察到“在站→离站”字段变化；其它车型/图需继续抽样，但客户端应默认按此语义处理 0。
- 消费影响：
  - “是否在站”：看 `currentStation`/`stationNo` 是否为 **正整数**，并交叉 `noStation`。
  - “在哪张图”：继续用 `mapName`，**不要**因站号为 0 清空地图。
  - “在哪里”：离站时用坐标（`precisePosition` / `currentPosition`），不要只依赖站名。

## BC-ORDER-001 最小移动单用 byDefaultMissions，不用 task/v1/order

- 结论：本现场创建指定车、单段 `move` 订单，应使用 `POST /api/order/v1/add/byDefaultMissions`；`POST /api/task/v1/order` 实测持续 NPE，不能作为建单主路径。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 正例证据：
  - [`../evidence/rounds/2026-07-20-round-7/runs/E1-retry-I-bdm-lock0.json`](../evidence/rounds/2026-07-20-round-7/runs/E1-retry-I-bdm-lock0.json)（站→2，最终 SUCCESS）
  - [`../evidence/rounds/2026-07-20-round-7/runs/E1b-create-2to1.json`](../evidence/rounds/2026-07-20-round-7/runs/E1b-create-2to1.json)（站2→1）
  - [`../evidence/rounds/2026-07-20-round-7/runs/E2-poll-samples-2to1.json`](../evidence/rounds/2026-07-20-round-7/runs/E2-poll-samples-2to1.json)
- 反例证据：`E1-create-order-attempt.json`、`E1-variant-*`、`E1-retry-*`（`task/v1/order` → `code=00002` NPE，未落库）
- 最小成功 body（已观测）：
  ```json
  {
    "appointVehicleKey": "<testVehicleKey>",
    "isAppointEnable": 1,
    "lockStatus": 0,
    "orderName": "riot-behavior-lab-...",
    "upperId": "riot-behavior-lab-...",
    "mission": [{ "type": "move", "mapId": 29, "destination": 1 }]
  }
  ```
- 前置：`vehicleTaskInfo.integrationLevel=ON_LINE` 且 `enable=true`（可用 BC-VEH-003：`serviceId=enable` 达成；网页亦可）。
- 消费影响：调度客户端建单默认走 order `byDefaultMissions`；不要把 task `v1/order` 当主路径，除非后续契约修复并有新证据。

## BC-ORDER-002 appointVehicleKey 会绑到本车执行

- 结论：在 BC-ORDER-001 路径下，请求里的 `appointVehicleKey` 会在执行期回写为同一车的 `executeVehicleKey`；本轮两笔成功单均未派到其它车。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 证据：Round 7 上述 SUCCESS 订单详情与 E2 轮询（`executeVehicleKey` 始终为测试车 key）。
- 消费影响：写单必须显式带测试/目标车 key；可用 `executeVehicleKey` 做安全校验。

## BC-STATE-003 成功移动单的状态并行轨迹（到站早于 SUCCESS）

- 结论：指定车单段 `move` 成功路径上，可稳定观测：
  - `orderState`：`1 QUEUEING` → `3 EXECUTING` → `5 SUCCESS`
  - `missionState`：`0` → `1` → `2`（完成时常伴 `resultCode=900`）
  - 车侧：`IDLE` → `PROCESSING_ORDER`+`MT_RUNNING`+站号0 →（到站）`AWAITING_ORDER`+`MT_FINISHED`+目的站 → `IDLE`
  - **物理到站信号早于 `orderState=5`**；`progress` 在 EXECUTING 期间不可用作路程进度。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 证据：[`../evidence/rounds/2026-07-20-round-8/runs/E2-dense-samples.json`](../evidence/rounds/2026-07-20-round-8/runs/E2-dense-samples.json)
- 适用范围：本测试车、map29、成功路径；取消/失败路径未覆盖。
- 消费影响：业务“到站”应交叉车侧站号/运动态；“可再派”应等订单 SUCCESS + 车 IDLE，勿把到站瞬间的 `AWAITING_ORDER` 当成可立即发下一单的充分条件。

## BC-ORDER-003 纯 move 执行中用 CMD_ORDER_CANCEL；interrupt 不可用

- 结论：
  1. **取消主路径**：对执行中（`orderState=3`）的单段 `move` 订单，调用 `POST /api/task/v1/order/command/{orderId}`，body `{"commandType":"CMD_ORDER_CANCEL","disableVehicle":false}`，可把订单打到 `orderState=2 CANCELLED`（`missionState=4`），车侧回到 `IDLE`。
  2. **`interrupt` 不适用于当前纯 move 子任务**：`POST /api/task/v1/order/interrupt` 无论 `pause=true/false` 均返回 `code=100036`（`中断订单的当前子任务索引不为移动任务`），订单与车运动态不变（Round 9/10）。
  3. 取消后即使 `currentStation=0`（离站），只要 `IDLE` 且非 `processingOrder`，仍可再派并 SUCCESS。
  4. **等价取消路径**：`POST /api/order/v1/operate`，body `{ "orderId": <数值id>, "orderCommandDTO": { "commandType":"CMD_ORDER_CANCEL", "disableVehicle":false } }`，效果与 command 路径等价（Round 10）。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 证据：[`../evidence/rounds/2026-07-20-round-9/`](../evidence/rounds/2026-07-20-round-9/)，[`../evidence/rounds/2026-07-20-round-10/`](../evidence/rounds/2026-07-20-round-10/)
- 消费影响：业务取消移动单走 `command/CMD_ORDER_CANCEL` 或 `operate`（注意 path 用字符串 orderId、operate 用数值 id）；不要对纯 move 单依赖 `interrupt` 做暂停。

## BC-ORDER-004 相同 upperId 重复提交被拒绝（订单已存在）

- 结论：`byDefaultMissions` 在相同 `upperId` 已存在时（含 SUCCESS 终态与 EXECUTING 中）返回业务失败 `code=0610008`，`message=订单已存在`，**不**创建第二单，也**不**回传原订单对象。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 证据：[`../evidence/rounds/2026-07-20-round-10/runs/Q004-A-resubmit-after-success.json`](../evidence/rounds/2026-07-20-round-10/runs/Q004-A-resubmit-after-success.json)，[`../evidence/rounds/2026-07-20-round-10/runs/Q004-B-resubmit-while-executing.json`](../evidence/rounds/2026-07-20-round-10/runs/Q004-B-resubmit-while-executing.json)
- 消费影响：客户端可把 `upperId` 当防重键；丢响应后应先 `detailByUpperId` 再决定是否新建（新建同 id 会失败）。

## BC-ORDER-005 标识：upperId / 字符串 orderId / 数值 id

- 结论：建单返回的字符串 `orderId`（形如 `order-...`）与 `detailByUpperId` / `detailByOrderId` 一致；数值主键 `id` 可用于 `GET /orderRecord/{id}` 与 `POST /order/v1/operate`。
- 证据等级：`OBSERVED`
- 证据：[`../evidence/rounds/2026-07-20-round-10/runs/ID-cross-query.json`](../evidence/rounds/2026-07-20-round-10/runs/ID-cross-query.json)

## BC-ORDER-006 HELD / CONTINUE_FROM_HELD 可暂停并恢复移动单

- 结论：
  1. 执行中 `CMD_ORDER_HELD` → `orderState=7`，`procState=USER_FORCE_IDLE`，`movementState=MT_PAUSED`；`CMD_ORDER_CONTINUE_FROM_HELD` 可回 EXECUTING 并 **SUCCESS**（Round10；Round36 map30 复核）。
  2. **HELD 后可 CANCEL** → `CANCELLED(2)`，车 `IDLE`（Round36 P2）。
  3. **命令配对**：EXECUTING 时 `CONTINUE_FROM_HELD` → `100020`；HELD 时 `CONTINUE_FROM_HANG` → `100021`（Round36 P3）。
  4. **HELD 占用中**同车再建单 → 新单长期 **QUEUEING**，`execute=--`（Round36 P4）。
  5. **单机暂停 ≠ RIoT HELD**（Round37）：单机点暂停 → 车 `MT_PAUSED`，订单可仍 `EXECUTING(3)`；`CONTINUE_FROM_HELD/HANG` 无效（`100020`/`100021`）。**仅单机恢复即可自行回 `MT_RUNNING` 并 SUCCESS**（Round37 B）。若订单已被打成 RIoT HELD(7)，则需单机恢复后再 `CONTINUE_FROM_HELD`。
- 证据等级：`OBSERVED`
- 证据：Round10；Round36 [`../evidence/rounds/2026-07-22-round-36/`](../evidence/rounds/2026-07-22-round-36/)；单机暂停 Round37 [`../evidence/rounds/2026-07-22-round-37/`](../evidence/rounds/2026-07-22-round-37/)
- 消费影响：暂停用 HELD/CONTINUE_FROM_HELD；勿与 HANG 混用；单机暂停要看 `movementState`，不能只看 `orderState==7`。

## BC-ORDER-007 建单反例：假/缺 appointVehicleKey 会进 QUEUEING

- 结论：
  1. 伪造或不存在的 `appointVehicleKey`：**建单仍成功**（`code=0`），进入 `QUEUEING`，短时 `execute=--`（Round10/11）。
  2. **省略** `appointVehicleKey`：同样成功；且 **会自动派车**——Round11 观测约 5s 内派到空闲测试车并 `EXECUTING`（BC-ORDER-008）。
  3. 非法 `mapId` / `destination`：拒绝 `code=0660003`（目的地站点不存在），未落库。
- 证据等级：`OBSERVED`
- 证据：Round 10 `NEG-create-results.json`；Round 11 `S1-*`
- 消费影响：**硬性**校验 key 且禁止省略指定车。

## BC-ORDER-008 省略 appointVehicleKey 会自动选车

- 结论：省略指定车时，调度器可把订单派给当时可调度车辆（本轮为测试车）；不能假设“不指定就不执行”。
- 证据：[`../evidence/rounds/2026-07-20-round-11/runs/S1-nokey-watch.json`](../evidence/rounds/2026-07-20-round-11/runs/S1-nokey-watch.json)

## BC-ORDER-009 多段 move→move 可用

- 结论：`mission` 含两段 `move` 时可顺序执行（`executingIndex` 0→1）并 `orderState=5`；完成后可再派。
- 证据：Round 11 `S3-multimove-samples.json`

## BC-ORDER-010 执行中 move 上 REJECTED/HANG 命令族不可用

- 结论：`CMD_ORDER_REJECTED`→`10015`；`CONTINUE_FROM_REJECTED`→`10016`；`CONTINUE/JUMP_FROM_HANG`→`100021`；状态不变。暂停用 HELD，取消用 CANCEL。
- 证据：Round 11 `S4-*`

## BC-ORDER-011 interrupt 对等待类 act 也不可用

- 结论：`actionId=129`（等待）执行中（含 move+act 的 act 段、act-only）`interrupt` 仍 `100036`。
- 证据：Round 11 `S5-*` / `S5b-*`

## BC-VEH-003 调度上线/下线：updateVehicleIntegrationLevel + serviceId enable/disable

- 结论：
  1. `POST /api/task/vehicles/updateVehicleIntegrationLevel`，body 仅需：
     ```json
     {"deviceKeys":["<deviceKey>"],"serviceId":"enable"}
     ```
     成功后：`vehicleTaskInfo.enable=true`，`integrationLevel=ON_LINE`。
  2. `serviceId":"disable"` → `enable=false`，`integrationLevel=OFF_LINE`。
  3. 调用密钥（callApiKey）即可，不必网页 admin token。
  4. **禁止**把 `serviceId` 填成 `ON_LINE`/`OFF_LINE`/`1`/`online` 等——会 `code=00002` 且可能破坏调度态（Round7/11）。
- 证据等级：`OBSERVED`（UI 抓包 + callApiKey 往返验证）
- 环境时间：2026-07-20
- 证据：[`../evidence/rounds/2026-07-20-round-12/`](../evidence/rounds/2026-07-20-round-12/)
- 消费影响：无人值守建单前可先 `enable`；收尾或隔离车用 `disable`。`deviceKeys` 必须只含目标车。

## BC-VEH-004 OFF_LINE 不挡建单；执行中 disable 不自动停单

- 结论：
  1. 车已 `disable`/`OFF_LINE` 时，`byDefaultMissions` 仍可 `code=0` 建单并进 `QUEUEING`。
  2. 订单执行中再 `disable`：`enable/integrationLevel` 变下线，但当前单可继续 `EXECUTING`+`MT_RUNNING`，不自动变为 CANCELLED/FAILED。
  3. 业务隔离策略：建单前自检 `ON_LINE`；要停当前任务须显式 `CMD_ORDER_CANCEL`（再 disable）。
- 证据：[`../evidence/rounds/2026-07-20-round-13/`](../evidence/rounds/2026-07-20-round-13/)

## BC-ORDER-012 不可达目的站：可建单，短时挂 QUEUEING（非自动 FAILED）

- 结论：路由代价 `costs=-1`（unreachable）时仍可建单；观察窗口内保持 `QUEUEING`/`execute=--`，未进入 `orderState=4`。清理靠 cancel。
- 证据：Round 13 `S3-*`
- 消费影响：不可把“建单成功”当成“路径可达”；建单前应用 `getRouteCostsBy`（或等价）自检。

## BC-ORDER-013 按车查积压订单与清队后再派

- 结论：
  1. 用 `GET /api/order/v1/orderRecord?pageNum&pageSize&filterByState=1|3|7|9` 取非终态订单。
  2. **不要只按 `executeVehicleKey` 查本车积压**：QUEUEING 单的 `executeVehicleKey` 常为 `"--"`，会被漏掉；该过滤适合已进入执行/HELD（已有执行车）的单。
  3. **不要依赖查询参数 `appointVehicleKey`**：SCHEMA 未声明；本现场传入后仍可能返回其它车非终态（参数等同无效）。
  4. 业务侧应按 `appointVehicleKey == 本车 || executeVehicleKey == 本车` 做客户端过滤。
  5. 对过滤出的 `QUEUEING(1)` / `HELD(7)`（按需含 `EXECUTING(3)`）逐单 `CMD_ORDER_CANCEL`；等车 `IDLE` 且非 `processingOrder` 后，新单可立即进入 `EXECUTING`。
- 证据等级：`OBSERVED`
- 环境时间：2026-07-20
- 证据：[`../evidence/rounds/2026-07-20-round-14/`](../evidence/rounds/2026-07-20-round-14/)（`S2-lists-while-backlog.json`、`S3-cancel-backlog.json`、`S3-N-executing.json`）
- 消费影响：MES「清积压再下新单」必须覆盖 `execute=--` 的队列单；清队后先确认 IDLE 再发单。

## BC-ROUTE-001 Route Controller GET/POST 使用场景（map28/29）

- 结论：
  1. **`POST /api/task/v1/route/getRouteCostsBy`** `{mapId,stationId,deviceKeys}`：返回每车 `costs`（mm）与 `message`。可达为非负 + `ok`；不可达（含车不在该图）为 `costs=-1` + unreachable 文案；外层业务码仍常为 `0`。
  2. **`POST .../queryNearEnd`** / **`queryNearestStart`**：返回路径代价最近的 **stationId**；纯拓扑，车可不在该图。空候选列表会 `00002` NPE。
  3. **`GET /api/task/v1/route/`**、**`GET .../getCostUnit`**：动态代价缓存/因子只读；可为空。
  4. **`GET .../curRemainCost/{orderKey}`**：
     - QUEUEING/假单：哨兵 `Long.MAX_VALUE`
     - EXECUTING：真实剩余代价，阶梯下降（Round16：`6280→6030→5070→4120→3180→1370`）
  5. Route **DELETE** 未测。
- 证据：Round15、Round16
- 消费影响：建单前用 `getRouteCostsBy`；多站择优用 Near*；进度可用 remain，但需过滤 MAX 哨兵，且为阶梯更新。

## BC-ORDER-014 队列单优先执行 orderRecordPriorityExec

- 结论：`POST /api/order/v1/orderRecordPriorityExec?orderTaskKey=<字符串orderId>` 可将 QUEUEING 单插队；取消当前执行单后，被优先的单会先于同车其它 QUEUEING 单进入 EXECUTING。
- 证据等级：`OBSERVED`
- 证据：[`../evidence/rounds/2026-07-20-round-16/runs/S2-priority-calls.json`](../evidence/rounds/2026-07-20-round-16/runs/S2-priority-calls.json)，[`../evidence/rounds/2026-07-20-round-16/runs/S2-watch-after-cancelA.json`](../evidence/rounds/2026-07-20-round-16/runs/S2-watch-after-cancelA.json)
- 消费影响：清积压之外的另一选择——保留队列、只提升目标单优先级。`orderTaskKey` 使用字符串 `orderId`。

## BC-VEH-005 急停检测、软件下发与解除

- 结论：
  1. **检测**：`GET .../getVehicleInfo/{deviceKey}` → `vehicle.emergencyState`；正常 `OK`，可恢复急停为 **`CAN_RECOVER`**（伴随 `controlState=CONTROL_STATE_ERR`）。物模型属性 `emergencyState`：`1`→`3`。
  2. **软件下急停**：`POST /api/device/v1/command/sync/service/{deviceKey}/triggerEmergency`
  3. **解除**：`POST .../cancelEmergency`
  4. 两者 body 相同（UI）：
     ```json
     {"messageId":848312,"mqCallback":{"tag":"string","topic":"string"},"thingsProperties":{}}
     ```
     （`messageId` 为数字；`thingsProperties` 可空对象。）
  5. **反例**：body `{}` → sync **`00002` NPE**。
  6. 以车态为准：触发后应见 `CAN_RECOVER`；解除后 `emergencyState=OK`（`controlState` 可能短暂 `ERR` 后回 `OK`）。
  7. Round19：**S4** `callApiKey` 完整 trigger→cancel 往返均为业务 **`code=0`**；**S3** 解除后可再派至 `SUCCESS`。
- 证据等级：`OBSERVED`
- 证据：[`../evidence/rounds/2026-07-20-round-19/`](../evidence/rounds/2026-07-20-round-19/)（`S2d-*`、`S4-*`）
- 消费影响：调用方可软件急停/解除；body 勿发空对象；成功以车态确认。

## BC-ORDER-015 执行中异常进入 HANG 与 CONTINUE 判别（Round27；Round31 修订）

- 结论：
  1. **进 HANG**：单机取消（E）、解抱闸（F）。急停 A/B 不单独进 HANG。**执行中关机（P）**：offline 保持 EXECUTING；**开机不取消 → HANG**（Round34 定位准；Round35 未定位同）。
  2. **CONTINUE**：E/F/P 在真 HANG 时可 `0`；P+未定位时回 EXECUTING 但常不跑，需先定位。
  3. **单机去站点占用时**（Round38）：HANG 中单机仍在跑时 CONTINUE 可 `code=0` 但订单**仍 HANG**（上一任务在运行）；须单机 `MT_FINISHED` 后再 CONTINUE 才回 EXECUTING。
  4. **旁证**：Round33 `320025`；**错定位**不测、人工判断（Q-038）。
- 证据：Round27/28/31/32/34/35/38；偶发 Round33
- 消费影响：关机恢复后若 HANG → CONTINUE；并检查 `locationState`；若车在跑单机任务，CONTINUE 成功码不可当已恢复，应等单机结束再发或重试。

## BC-ORDER-016 本体异常时空闲建单滞留 QUEUEING（Round29/30）

- 结论：车 `IDLE` 但处于硬件急停 / 软件急停 / 解抱闸（`UNMOVABLE`）/ **旋钮关机**（`runtime/status=offline`）时，`byDefaultMissions` 仍 `code=0`，订单约 90s 内保持 **`QUEUEING(1)`** 且 `executeVehicleKey=--`，**不进入 EXECUTING**；车侧保持 IDLE。关机用例下路由仍可达，可排除「过远」混杂。
- 证据等级：`OBSERVED`
- 证据：Round29 [`../evidence/rounds/2026-07-22-round-29/`](../evidence/rounds/2026-07-22-round-29/)；关机 Round30 P [`../evidence/rounds/2026-07-22-round-30/`](../evidence/rounds/2026-07-22-round-30/)
- 消费影响：建单前除 ON_LINE/定位/可达外，还应检查 `emergencyState`、`breakSwitchState`、`runtime/status`；异常时勿期望立刻执行。

## BC-ORDER-017 未定位 / 离路线过远建单滞留 QUEUEING（Round30）

- 结论：
  1. **未定位**（`locationState=ERROR`）：建单 `code=0` → 长期 **`QUEUEING`**，非 `HANG`（Round23；Round30 L 约 120s）。
  2. **离路线过远**（仍 `LOCATION_STATE_RUNNING`，但 `getRouteCostsBy` → `costs=-1` unreachable）：同上，约 120s 一直 QUEUEING（Round30 D2）。
  3. **陷阱**：仅 `currentStation=0` 仍可能路由可达并 EXECUTING（Round30 D1）；勿用离站代替「过远」。
- 证据等级：`OBSERVED`
- 证据：[`../evidence/rounds/2026-07-22-round-30/`](../evidence/rounds/2026-07-22-round-30/)
- 消费影响：建单前用 `locationState` + `getRouteCostsBy` 判可走；不可走时期望 QUEUEING 滞留，勿当 HANG 处理。

## BC-ORDER-018 单机「去站点」与 RIoT 订单交互（Round38）

- 结论：
  1. **单机去站点过程中建单**：成功进 **`QUEUEING`**，不抢占；单机到站后才 **`EXECUTING`**。
  2. **HANG + 单机去站点过程中 CONTINUE**：接口可成功，订单可仍 HANG（上一任务占用）；单机结束后再 CONTINUE 可恢复并 SUCCESS。
- 证据等级：`OBSERVED`
- 证据：[`../evidence/rounds/2026-07-22-round-38/`](../evidence/rounds/2026-07-22-round-38/)
- 消费影响：单机导航占用时勿期望新单立刻执行或 HANG 立刻恢复；以 `movementState`/`procState` 空闲后再下发或重试 CONTINUE。

## BC-ORDER-019 QUEUEING 原因诊断的身份、短路与安全边界（Round39/40）

- 结论：
  1. `GET /api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey}` 的项目 `orderKey` 使用字符串 `orderId`。车辆恢复可分配后，已取消订单的字符串 `orderId` 仍得到“订单是非可调度状态”，而数值记录 id、`upperId` 与随机 key 均为“订单不存在”。
  2. 诊断按内部优先级短路：车辆 OFF_LINE 时，真实三种身份、随机 key 和已取消订单都会先返回“车辆处于调度下线状态”，因此该分支不能证明 `orderKey` 有效，也不会因订单取消立即改变。
  3. `code=0` 表示成功返回诊断，不表示车辆或订单存在，也不表示可以执行建议。结果只有自由文本 `reason` 与 `suggestList`，没有原因码、枚举、状态版本或观测时间。
  4. 软件急停 `CAN_RECOVER` 下的实测原因是宽泛的“车辆处于非空闲的状态,不可分配订单”，同时公开 `procState` 仍为 IDLE；文本不能独立识别急停或授权解除。
  5. `suggestList` 可建议系统级“重启 RIoT”。8005 绝不直接执行建议；只保留原文，并以独立状态、安全事实、动作来源和既有白名单决定自动恢复或人工升级。
  6. 车辆仍定位但人工移离路线、map 30 六个站点均为 `costs=-1/unreachable` 时，实时 QUEUEING 诊断稳定返回“以车当前的坐标为起点,以订单目的地为终点,无法规划路径”。其建议包含人工移回路网或取消重发，但8005只保持阻断并转人工；诊断不授权自动移动、取消、重建或换号。
- 证据等级：`OBSERVED`
- 证据：[`../evidence/rounds/2026-08-04-round-39/`](../evidence/rounds/2026-08-04-round-39/)、[`../evidence/rounds/2026-08-04-round-40/`](../evidence/rounds/2026-08-04-round-40/)、[`../evidence/rounds/2026-08-04-round-41/`](../evidence/rounds/2026-08-04-round-41/)
- 消费影响：先验证字符串 `orderId` 与订单归属，再把诊断与独立车态共同解释；未知文本、短路结果或身份不一致一律阻断转人工。

## BC-VEH-006 全车快照可证明已在桩占用，但不能证明无外部在途目标（Round42）

- 结论：
  1. build `2.2.0.30` 上，`GET /api/task/vehicles?pageNum=1&pageSize=100` 与独立 `getAllVehicleKeys` 同为 18 个唯一 key，其中 17 辆不是本地测试车；分页参数生效，但响应没有 total、cursor、服务端快照版本或观测时间。
  2. 三辆其它项目车辆持续以 `batteryState=CHARGING` 出现在独立地图元数据标识的充电站点。占用身份必须使用 `(currentMap,currentPosition)`，不能使用跨地图裸站点号。
  3. `currentPosition=0` 同时出现在在线离站、移动和断线/定位错误车辆上；`0`、缺字段、失败或错误状态只能判未知，不能判空闲。
  4. 普通任务完成后 `taskType/orderTaskId/endStationNo` 在一次约 5 秒轮询间隔内清空；但 24 轮没有 `taskType=CHARGE` 在途样本，正在充电车辆的任务字段均为空，不能证明外部车辆的充电目标覆盖或 CHARGE 清除时序。
  5. 5 秒串行轮询 24/24 成功，p95 168 ms、约 15.7 KB/次；没有服务端资源指标。测试环境的保守上限为 12 次快照/分钟，另加每分钟 1 次 key 完整性核对，不构成生产授权。
- 证据等级：`OBSERVED`，仅 `RIOT-CROSS-PROJECT-TEST` / build `2.2.0.30`；不是 `RIOT-8005-RUNTIME v2.2.0.14` 实测。
- 证据：[Round 42](../evidence/rounds/2026-08-04-round-42/)
- 消费影响：该接口可辅助证明“已经占用”，不能把未见本地预占解释为“空闲且无人正前往”；外部目标不可确认时必须 fail-closed，等待专用订阅、物理占用/人工确认或目标环境补证。

## 待晋升条件

以下内容目前不能写成已验证契约：

- 所有模块都以 `code=0` 表示成功。
- 所有鉴权失败都以 HTTP 401 表现（登录接口已证明例外）。
- 调用密钥对全部写接口与 admin 同等权限。
- `POST /api/task/v1/order` 在其它 body/版本下可用。
- 车辆对象上存在数值型当前 `mapId` 字段（本现场观测到的是 **mapName**）。
- `stationId` 跨地图全局唯一。
- `orderState=5` 必然等价于车辆已物理到站（本轮有物理到站旁证，但未证明恒等）。
- `procState=IDLE` 必然表示车辆任务队列为空（Round14：清完本车非终态后观测到 IDLE，但未证明全局恒等）。
- `orderState=4 FAILED` 的完整触发集合（现场经验：系统/地图异常、极少见；见 Q-024，不阻塞对接）。
- 非等待类 act（顶升/同步旋转等）的 interrupt 行为。

它们必须先在 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) 中获得相应现场证据。
