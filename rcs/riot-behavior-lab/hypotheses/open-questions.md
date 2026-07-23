# 未决问题与验证优先级

这里记录“需要回答的问题”，实验目录记录“怎样获取证据”。问题得到足够证据后，将结论迁入 `knowledge/`，不要直接删除历史问题。

状态取值：`OPEN` / `TESTING` / `SUPPORTED` / `REFUTED` / `BLOCKED`。

P0 目标：指定测试车短距建单与到站观测（mapId=29）——Round 7 建单打通；**Round 8 拉长站距后完整状态轨迹已观测**。

建议验证顺序：… → Round16 完成（remain@EXECUTING、map28 派跑、优先执行）。3/5 对应 API 已入「以后可能需要」。Q-028 已在 map30（api测试2）闭环 SUCCESS（Round18）。

> **2026-07-20 P0**：鉴权 → 车辆 → 地图 → 站点 → **指定车建单（完成）**。

## P0：鉴权、车辆、地图与站点

### Q-015 网页「调用密钥设置」中的密钥能否直接访问 RIoT

- 状态：`SUPPORTED`
- 结论（已迁入 [`../knowledge/behavioral-contracts.md`](../knowledge/behavioral-contracts.md) BC-AUTH-002）：
  - 使用网页调用密钥作为 `Authorization: Bearer <callApiKey>`，**无需**每次调用 `admin/login`，即可访问至少 imap / device / task 只读业务接口。
  - 缺失或伪造密钥时，业务探针返回 HTTP `401`，响应 `code=401`，`message=暂未登录或token已经过期`。
- 证据轮次：[`../evidence/rounds/2026-07-20-round-2/`](../evidence/rounds/2026-07-20-round-2/)

### Q-016 如何列出系统中的车辆，并排除非车辆设备

- 状态：`SUPPORTED`
- 结论（已迁入 [`../knowledge/behavioral-contracts.md`](../knowledge/behavioral-contracts.md) BC-VEH-001）：
  - `GET /api/device/v1/devices` 会返回非车设备，**不能**直接当车辆列表。
  - 可调度车辆应以 task 侧清单为准；本现场 `getAllVehicleKeys` / `getAllVehicleSimpleInfo` / `getAllTaskVehicles` 均为 **18** 台，且为 devices 的真子集。
- 证据轮次：[`../evidence/rounds/2026-07-20-round-3/`](../evidence/rounds/2026-07-20-round-3/)

### Q-017 如何用车辆名解析到 `deviceKey`

- 状态：`SUPPORTED`
- 结论（已迁入 BC-VEH-002）：
  - 推荐 `GET /api/task/vehicles/getAllVehicleSimpleInfo`，按 `deviceName` 精确匹配得到 `deviceKey`。
  - 本现场测试车名 `新基测试300c协作1` 唯一映射到已知测试 key；不存在的车名 0 命中；18 个车名无重名。
- 证据轮次：[`../evidence/rounds/2026-07-20-round-3/`](../evidence/rounds/2026-07-20-round-3/)
- 仍开放的边界：若未来出现重名，禁止只按名称派车；写路径字段等价性另证。

### Q-018 现场有哪些有效地图，如何得到 mapId

- 状态：`SUPPORTED`
- 结论（已迁入 [`../knowledge/behavioral-contracts.md`](../knowledge/behavioral-contracts.md) BC-MAP-001）：
  - `GET /api/imap/v1/mapInfo/all` 与 `GET /api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson` 均可列出有效地图；本现场均为 **18** 张，`mapId` 即返回对象的 `id`，名称字段为 `name`。
  - 证据应剥离 `mapJson` 几何。
- 证据轮次：[`../evidence/rounds/2026-07-20-round-4/`](../evidence/rounds/2026-07-20-round-4/)
- 补记（Round 6）：测试车当前地图**可以**从状态接口读出地图名再反查 `mapId`：
  - `GET /api/task/v1/task/getVehicleInfo/{deviceKey}` → `vehicle.previousState.mapName`（Round4 因只扫顶层而漏读）
  - `GET /api/device/v1/runtime/properties/{deviceKey}` → 属性 `mapName`
  - 本现场测试车 `mapName=api测试` → **mapId=29**
  - `runtime/status` 仅 online，信息不够，不能当主状态源
  - 离站时站号为 **0**（`noStation=true`），地图名与坐标仍在（BC-STATE-002）
- 证据：[`../evidence/rounds/2026-07-20-round-6/`](../evidence/rounds/2026-07-20-round-6/)

### Q-019 如何读取单图站点清单（stationId ↔ 站名）

- 状态：`SUPPORTED`
- 结论（已迁入 [`../knowledge/behavioral-contracts.md`](../knowledge/behavioral-contracts.md) BC-MAP-002）：
  - `GET /api/imap/v1/mapInfo/stations/{mapId}` 返回站点数组；本现场 **`id`=stationId，`name`=站名**。
  - 非法 `mapId=0` 仍可能 `code=0` 但空数组——必须校验列表非空。
  - 候选测试图站点数：29→2，26→4，27→31，28→33。
- 证据轮次：[`../evidence/rounds/2026-07-20-round-5/`](../evidence/rounds/2026-07-20-round-5/)
- 仍开放：测试车实际绑图；写单前安全目的站需人工确认（`currentStation=1` 无法唯一反推 mapId）。

### Q-001 哪个 API 面适合创建本项目移动任务

- 状态：`SUPPORTED`（本现场最小移动单）
- 结论（已迁入 BC-ORDER-001）：
  - **可用**：`POST /api/order/v1/add/byDefaultMissions`，显式 `appointVehicleKey`，`mission=[{type:move,mapId,destination}]`，不用车辆组。
  - **不可用（本现场）**：`POST /api/task/v1/order` 在多种合法 body 下均服务端 NPE（`code=00002`），未落库。
  - 前置：测试车需 `integrationLevel=ON_LINE` 且 `enable=true`（`serviceId=enable` 或网页上线）。
- 证据轮次：[`../evidence/rounds/2026-07-20-round-7/`](../evidence/rounds/2026-07-20-round-7/)

### Q-020 如何把单车从 OFF_LINE 切到 ON_LINE（调度上线）

- 状态：`SUPPORTED`
- 结论（BC-VEH-003）：
  - API：`POST /api/task/vehicles/updateVehicleIntegrationLevel`
  - body：`{"deviceKeys":["<deviceKey>"],"serviceId":"enable"}` → `enable=true`，`integrationLevel=ON_LINE`
  - 下线：同接口 `serviceId":"disable"` → `enable=false`，`integrationLevel=OFF_LINE`
  - **callApiKey 可用**（不必 admin 网页 token）
  - 错误用法：把 `serviceId` 设成 `ON_LINE`/`1`/`online` 等会 `00002` 且可能副作用（Round7/11）
- 证据：网页抓包（用户）；Round 12 `E2-disable.json` / `E3-enable-restore.json`
- 来源：UI Network 中 `serviceId` 为字面量 `enable`/`disable`，非 integrationLevel 枚举名。

### Q-011 `appointVehicleKey` 是否真正绑车

- 状态：`SUPPORTED`
- 结论（已迁入 BC-ORDER-002）：建单后 `executeVehicleKey` 回写为同一测试车 key；轮询期间未见派到其它车。
- 证据：Round 7 `E1-bdm-I-detailByUpperId.json`，`E1b-create-2to1.json`，`E2-poll-samples-2to1.json`

### Q-002 / Q-005 到站与可再派

- 状态：`SUPPORTED`（成功路径，单图短距拉长后）
- 结论（已迁入 [`../knowledge/state-model.md`](../knowledge/state-model.md) Round 8 轨迹）：
  - **物理到站** ≠ **订单完成**：先观测到 `currentStation=目的站` + `MT_FINISHED` + `procState=AWAITING_ORDER`，随后才 `orderState=5` / `missionState=2` / `procState=IDLE`。
  - **可再派**建议：订单终态 `orderState=5` 且车侧 `IDLE`、非 `processingOrder`；不要仅凭短暂的 `AWAITING_ORDER`。
  - **`progress` 不能表示路程**：EXECUTING 起即 100。
- 证据：[`../evidence/rounds/2026-07-20-round-8/runs/E2-dense-samples.json`](../evidence/rounds/2026-07-20-round-8/runs/E2-dense-samples.json)
- 仍开放：其它地图成功路径复现。`orderState=4 FAILED` 见 Q-024（非常规，不作为必测）。

## P1：异常与恢复

### Q-004 相同 `upperId` 重复提交的行为

- 状态：`SUPPORTED`
- 结论（BC-ORDER-004）：SUCCESS 后与 EXECUTING 中再次 `byDefaultMissions` 同 `upperId`，均 `code=0610008`（订单已存在），不建第二单、不回传原单。
- 证据：[`../evidence/rounds/2026-07-20-round-10/`](../evidence/rounds/2026-07-20-round-10/) `Q004-A-*` / `Q004-B-*`

### Q-003 / Q-013 标识关联（upperId / orderId / 数值 id）

- 状态：`SUPPORTED`（本现场 order 读写路径）
- 结论（BC-ORDER-005）：字符串 `orderId`、数值 `id`、`upperId` 交叉一致；command 用字符串，operate 用数值。
- 证据：Round 10 `ID-cross-query.json`

### Q-006 cancel、interrupt、pause 和 hang 的真实差异

- 状态：`SUPPORTED`（含真 HANG 进入与 CONTINUE；见 Q-035）
- Round 9–11 观测：
  - **`interrupt`（pause=true/false）**：纯 move 与 **act 等待段**（`actionId=129`）均 `code=100036`，状态不变。
  - **`cancel`**：`CMD_ORDER_CANCEL` / `order/v1/operate` 可用。
  - **`CMD_ORDER_HELD` / `CONTINUE_FROM_HELD`**：可用（Round10；Round36 复核；Round37：单机暂停≠HELD，见下）。
  - **单机暂停**（Round37）：车 `MT_PAUSED`、订单可仍 EXECUTING；RIoT CONTINUE 无效；**仅单机恢复即可跑完 SUCCESS**；若已打成 RIoT HELD 则需再 `CONTINUE_FROM_HELD`。
  - **`CMD_ORDER_REJECTED` / `CONTINUE_FROM_REJECTED`**：执行中 move 拒绝 `10015`/`10016`。
  - **`CONTINUE_FROM_HANG` / `JUMP_FROM_HANG`**：非 HANG 态下拒绝 `100021`。
- Round27：真 `orderState=9` 下 CONTINUE 可成功（E；拨回开机后的 F）；解抱闸未拨回时 `14013`。软件急停进 HANG 的旧结论已由 Round31 修订（见 Q-035）。
- Round36/37 证据：[`../evidence/rounds/2026-07-22-round-36/`](../evidence/rounds/2026-07-22-round-36/)；[`../evidence/rounds/2026-07-22-round-37/`](../evidence/rounds/2026-07-22-round-37/)
- 证据：Round 9–11；Round27 [`../evidence/rounds/2026-07-21-round-27/`](../evidence/rounds/2026-07-21-round-27/)

### Q-012 取消主路径及取消后何时可再派

- 状态：`SUPPORTED`（本现场最小移动单）
- 结论（BC-ORDER-003）：
  - 主路径：`POST /api/task/v1/order/command/{orderId}`，`commandType=CMD_ORDER_CANCEL`，`disableVehicle=false`。
  - 等价：`POST /api/order/v1/operate`（数值 `orderId`）。
  - `{orderId}`（command）使用字符串订单号（如 `order-...`），与建单返回/`detailByUpperId` 的 `orderId` 一致。
  - 取消后：`orderState=2`；车侧回到 `IDLE` 且非 `processingOrder` 即可再派（即使离站站号为 0）。
- 证据：Round 9 `EC-*`、`ER-*`；Round 10 `Q006-operate-*`

### Q-021 建单反例：假/缺 appointVehicleKey、非法站

- 状态：`SUPPORTED`（升级：后派行为）
- 结论（BC-ORDER-007 / BC-ORDER-008）：
  - 假 key：可进 QUEUEING，短时不后派。
  - **省略 key：会自动派车**（本轮派到空闲测试车并 EXECUTING）。
  - 非法 map/站：`0660003`。
- 证据：Round 10 `NEG-*`；Round 11 `S1-*`

### Q-022 多段 move→move

- 状态：`SUPPORTED`
- 结论：`mission=[{move,d1},{move,d2}]` 可 SUCCESS；`executingIndex` 从 0→1；完成后可再派。
- 证据：Round 11 `S3-*`

### Q-023 disable/OFF_LINE 与建单、执行中订单

- 状态：`SUPPORTED`
- 结论（BC-VEH-004 / BC-ORDER-012）：
  1. **OFF_LINE 后仍可建单**：`byDefaultMissions` 返回成功，进 `QUEUEING`（不在建单口拒绝）。
  2. **跨图不可达**：路由代价 `-1` 仍可建单；短时保持 `QUEUEING`，**未观测到自动 `FAILED(4)`**。
  3. **执行中 disable**：车变 `OFF_LINE`，当前单可继续 `EXECUTING`/`MT_RUNNING`，不自动 cancel/fail。
- 证据：[`../evidence/rounds/2026-07-20-round-13/`](../evidence/rounds/2026-07-20-round-13/)
- 仍开放：无（FAILED 另见 Q-024）。

### Q-024 `orderState=4 FAILED` 的触发条件

- 状态：`OPEN`（**低优先级 / 不阻塞对接**）
- 现场经验（用户 2026-07-20）：FAILED 极少见，已知多与**系统异常**或**地图异常**相关，不是常规业务失败路径。
- Round13 尝试：OFF_LINE 建单、跨图不可达 → 均未进入 FAILED（建单成功或挂 QUEUEING）。
- 策略：业务异常处理优先覆盖 `CANCELLED`、QUEUEING 滞留、建单业务码；**不把 FAILED 当必测闭环**。若日后现场偶发，再抓证据补契约。
- 证据：Round 13；用户经验（待现场偶发样本晋升为 `OBSERVED`）

### Q-025 如何按车获取积压订单并清队后让新单生效

- 状态：`SUPPORTED`
- 结论（BC-ORDER-013）：
  1. 列表主接口：`GET /api/order/v1/orderRecord`（`pageNum`/`pageSize` + `filterByState`）。
  2. **仅** `executeVehicleKey=本车` **会漏掉 QUEUEING**：队列单 `executeVehicleKey="--"`，积压时只能看到已派执行/已 HELD 的单。
  3. 查询参数 **`appointVehicleKey` 不可靠**（SCHEMA 未声明；实测会被忽略，可能串出其它车非终态）。
  4. 推荐：按 `filterByState=1,3,7,9` 取非终态，再客户端过滤 `appointVehicleKey==本车 || executeVehicleKey==本车`。
  5. 对 QUEUEING/HELD 发 `CMD_ORDER_CANCEL` 可清队；清完车 `IDLE` 后新单可立即 `EXECUTING`。
- 证据：[`../evidence/rounds/2026-07-20-round-14/`](../evidence/rounds/2026-07-20-round-14/)

### Q-026 Route Controller（GET/POST）行为与使用场景

- 状态：`SUPPORTED`
- 结论（BC-ROUTE-001）：
  1. **`getRouteCostsBy`**：车→站路径代价（mm）；跨图/不可达 `costs=-1`；同图可达为正值。建单前可达性检查主接口。
  2. **`queryNearEnd` / `queryNearestStart`**：纯地图拓扑择站；不要求车在该图。
  3. **`GET /route/`、`getCostUnit`**：动态代价缓存/因子只读；可为空。
  4. **`curRemainCost/{orderKey}`**：
     - QUEUEING/假单：`Long.MAX_VALUE`
     - EXECUTING：真实剩余代价，**阶梯下降**（Round16：`6280→6030→5070→4120→3180→1370`）
  5. Route **DELETE**：按用户要求未测，保留在研究范围但本轮不碰。
- 证据：Round15（map28 拓扑/跨图）；Round16（EXECUTING remain）

### Q-027 `orderRecordPriorityExec` 能否让队列单插队

- 状态：`SUPPORTED`
- 结论（BC-ORDER-014）：
  - `POST /api/order/v1/orderRecordPriorityExec?orderTaskKey=<字符串orderId>` 成功（`code=0`）
  - 在 A 执行、B/C 排队时优先 C，再取消 A 后：**C 先于 B 进入 EXECUTING**
  - 优先后 C 未见稳定变为 `orderState=10`，仍可能为 `1`；效果看后续出队顺序
- 证据：[`../evidence/rounds/2026-07-20-round-16/`](../evidence/rounds/2026-07-20-round-16/) `S2-*`

### Q-028 换图最小跑单闭环（map28 受阻 → map30 SUCCESS）

- 状态：`SUPPORTED`
- map28（新基测试2opt，Round16/17）：可派可跑；窗口内近终点卡在 `remain` 不归零，未采到完整 SUCCESS。
- map30（api测试2，Round18）：`5→6` 约 33s 到 `SUCCESS`（`finalState=true`，车在站6）；再派 `6→5` 亦 SUCCESS。
- 轨迹同构于 map29：`QUEUEING→EXECUTING→SUCCESS`；执行中 `curRemainCost` 阶梯下降至 0 后回哨兵。
- 证据：[`../evidence/rounds/2026-07-20-round-18/`](../evidence/rounds/2026-07-20-round-18/)；旁证 Round16 `S1-*`

### Q-029 急停如何检测、软件下发与解除

- 状态：`SUPPORTED`
- 检测：`getVehicleInfo.emergencyState`：`OK` → **`CAN_RECOVER`**；伴随 `controlState=CONTROL_STATE_ERR`；物模型属性 `3`
- 下急停：`POST .../command/sync/service/{deviceKey}/triggerEmergency`  
  body：`{"messageId":<number>,"mqCallback":{"tag":"string","topic":"string"},"thingsProperties":{}}`  
  Round19 **S4**（callApiKey）：**`code=0`**，约 1s 后 `CAN_RECOVER`
- 解除：同路径 `cancelEmergency` + 同 body；S2d/S4：**`code=0`** → `OK`
- 反例：空 `{}` → sync `00002` NPE
- 解除后可再派：Round19 S3 短距 `SUCCESS`
- 证据：[`../evidence/rounds/2026-07-20-round-19/`](../evidence/rounds/2026-07-20-round-19/) `S2d-*` / `S4-*`

### Q-030 设备断连离线如何检测、离线建单与恢复后再派

- 状态：`SUPPORTED`
- 检测：`GET /api/device/v1/runtime/status/{deviceKey}` → `result.type`：`online` → **`offline`**
- 设备离线时调度 `enable`/`integrationLevel=ON_LINE` **可不变**（与 Round13 调度 `disable` 正交）
- 离线建单：`byDefaultMissions` 仍 `code=0`，挂 `QUEUEING`，短时不执行
- 恢复上线后可再派并进 `EXECUTING`（Round20 S4；完整 SUCCESS 非本轮必达）
- 证据：[`../evidence/rounds/2026-07-20-round-20/`](../evidence/rounds/2026-07-20-round-20/)

### Q-031 旋钮三档（开机 / 解抱闸 / 关机）如何判定

- 状态：`SUPPORTED`（Round22 在 5G 独立供电下复验）
- **开机**：`status=online`，`breakSwState=1(OFF)`，`breakSwitchState=MOVABLE`，`controlState=OK`
- **解抱闸**：`status=online`，`breakSwState=2(ON)`，`breakSwitchState=UNMOVABLE`（命名与直觉相反），`controlState` 常 `ERR`
- **关机**：`runtime/status=offline`；属性可能空；调度 `ON_LINE` 可不变
- 不要用 `mode` 区分（多为 `MODE_AUTO`）
- **Round21**：关机时客户端 API 超时，因车端停供 5G（访问路径断），不是字段滞后
- **Round22**：5G 独立供电后，关机时 **API 仍可达** + `status=offline`（干净复验）
- **Round30 P**：关机态建单（路由仍可达）→ 约 90s 一直 `QUEUEING`，不进 EXECUTING（见 Q-036）
- 关机→开机：可出现短暂 `break=UNKNOWN` / `breakSwState=0`；恢复后 `station` 可能为 0 且路由 `costs=-1`（需重定位后再派）
- 证据：[`../evidence/rounds/2026-07-21-round-22/`](../evidence/rounds/2026-07-21-round-22/)；旁证 Round21；建单 Round30 P

### Q-032 定位 / 未定位如何判定，未定位建单与重定位后再派

- 状态：`SUPPORTED`
- 检测：
  - **已定位**：`getVehicleInfo.vehicle.locationState=LOCATION_STATE_RUNNING`，物模型 `locationState=3`
  - **未定位（人工停止定位）**：`locationState=ERROR`，物模型 `locationState=1`；常伴 `controlState=CONTROL_STATE_ERR`、聚合 `state=ERROR`
  - 重定位过渡曾见物模型 `2`、`4`，稳态回到 `3`
- 旁证与陷阱：
  - `confidence` 未定位时仍可保持原值（本轮 58），**不可单独**判定位
  - `currentStation=0` / `noStation=true` = 离站（BC-STATE-002），**不等于**未定位（本轮 E0 即离站但仍 RUNNING）
  - 未定位时 `status=online`、调度 `ON_LINE`、`mapName`/坐标仍可读
- 未定位建单：`byDefaultMissions` 仍 `code=0`，挂 `QUEUEING`，短时不执行；路由常 `costs=-1` / 不可达
- Round30 L 复核：未定位约 **120s** 一直 `QUEUEING(1)` / `executeVehicleKey=--`，**不是** `HANG(9)`
- 恢复：重定位后可短距再派并 `SUCCESS`（Round23 S4，map30 站3）
- 证据：[`../evidence/rounds/2026-07-21-round-23/`](../evidence/rounds/2026-07-21-round-23/)；Round30 L [`../evidence/rounds/2026-07-22-round-30/`](../evidence/rounds/2026-07-22-round-30/)

### Q-033 订单模板「移动 + 充电(act 78)」成败如何表现

- 状态：`SUPPORTED`
- 建单：
  - 普通单 `move(目标站)+act(78,1,0)` 即可；目标站需 `type=2` 或配置 `user_define_properties.enter_exit`（例：map30 站6→`"8"`；华士老厂站16→`"26"`）
  - 无进入退出点 → `10008`；有配置后 RIoT **自动展开**为 `move(进入点) → move(目标站) → act(78)`
- **失败**（不接充电器，Round24）：
  - act `resultCode=407802`（文案含「导致订单挂起」）
  - 失败后会 **重试**：多次回到 move 再进 act（约 2～3 轮），最终 `orderState=9 HANG`，`proc=INNER_FORCE_IDLE`
- **成功**（接充电器，Round25）：
  - act 中 `batteryState` → `CHARGING`，`actionState=AT_FINISHED`，订单 **`orderState=5 SUCCESS`**
  - act `resultCode=0`；`resultStr` 文案可能仍含「挂起」字样，以 orderState/resultCode 为准
  - 借用车 `BROKERX-52501…` / 华士老厂站16 **仅本轮**；此后禁止再用此车
- **有线充电态（只读，无订单，Round24）**：
  - `batteryState=CHARGING`；车 `IDLE` / `MT_FINISHED`
- **MES/现场业务约定（2026-07-21 用户确认，未再测）**：
  - **何时离桩**：再下订单即可；系统会在该订单任务列表**最前面自动插入** `act(78, param1=2, param2=0)` = **结束充电**，然后再执行业务任务，车离开充电位
  - **充满阈值**：按 **100%** 视为充满
  - **充电失败 HANG 后**：只能人工排查故障，不走自动恢复策略
  - **低电量**：本体电量到 **10% 会自动关机**；MES 下单前须保证电量 **>10%**
  - **RIoT 自动充电**：现场功能已关掉、**未启用**；不会自动派车去充电，充电须由 MES 订单触发
  - **act 78 参数约定**：
    | 含义 | actionId | actionParam1 | actionParam2 |
    |------|----------|--------------|--------------|
    | 开始充电 | 78 | 1 | 0 |
    | 结束充电 | 78 | 2 | 0 |
- 证据：失败 [`../evidence/rounds/2026-07-21-round-24/`](../evidence/rounds/2026-07-21-round-24/)；成功 [`../evidence/rounds/2026-07-21-round-25/`](../evidence/rounds/2026-07-21-round-25/)

### Q-034 如何判断车是否处于交管等待（等别的车让路）

- 状态：`SUPPORTED`
- 说明：交管算法为 RIoT 内部机制；MES 只需识别「是否在交管等待」，不干预解除。
- **等待中**：
  - 主信号：`getVehicleInfo` → `movementState=MT_WAIT_FOR_CHECKPOINT`（订单执行中、`speed=0`）
  - 辅：`GET /api/task/v1/traffic/appliedResource` 含本车；本车通常不在 `lockedResource`
  - 原因：`GET .../traffic/checkFailDetail/{deviceKey}`（如 `type=edgeGroup` + `lockedVehicleIds`）
- **解除后**：
  - `movementState` → `MT_RUNNING`（本轮观测）；本车从 `appliedResource` 消失
  - 行驶中出现 `lockedEdge/lockedNode` 属正常占路权，**不等于**交管等待
  - `checkFailDetail` 可变为 `result=null`
- 证据：[`../evidence/rounds/2026-07-21-round-26/`](../evidence/rounds/2026-07-21-round-26/)

### Q-035 执行中异常如何进入 HANG，CONTINUE 能否区分可恢复

- 状态：`SUPPORTED`（Round27；**Round31 修订软件急停**）
- **进入 HANG（`orderState=9`）**：
  | 场景 | 是否进 HANG | 车态要点 | CONTINUE / 恢复 |
  |------|-------------|----------|-----------------|
  | A 硬件急停 | **不会单独进 HANG**（Round27；Round28 约14min 仍 EXECUTING） | `CAN_NOT_RECOVER`；物理松开 | 非 HANG 时 CONTINUE→`100021`；用急停车态判人工 |
  | B 软件急停 | **不会单独进 HANG**（**Round31 约15min 仍 EXECUTING**；修订 Round27「延迟进 HANG」） | `CAN_RECOVER`；进度冻结 | `cancelEmergency` 后订单可继续；不依赖 HANG/CONTINUE |
  | P 旋钮关机（执行中） | **关机期间不进 HANG**（Round32）；**拨回开机且不取消 → 进 HANG**（Round34 定位准；**Round35 未定位同**） | offline 时 EXECUTING；开机后 `HANG`+`INNER_FORCE_IDLE` | CONTINUE→`0` 可回 EXECUTING；**未定位时**回到 3 但常 `AWAITING_ORDER`/不跑，需先定位；准确定位见 Round34 |
  | E 单机取消移动 | **会**（较快） | 急停 OK；`resultCode=901`「订单被取消…」 | CONTINUE → `0`，可 SUCCESS |
  | F 解抱闸 | **会** | `break=UNMOVABLE` / `control=ERR`；文案可同 901 | 未拨回 → `14013`；拨回开机后再 CONTINUE → `0` |
- **判别建议（调用方）**：
  1. 等 `orderState=9` 再试 `CMD_ORDER_CONTINUE_FROM_HANG`（真 HANG：E/F；充电失败等）
  2. `code=0` → 可软件恢复（E；或 F 在拨回开机之后）
  3. `14013` → 查 `breakSwitchState`（解抱闸）等车态，需人工拨回后再 CONTINUE
  4. `100021` → 车辆原因仍不可继续，或订单根本不在 HANG
  5. **A/B 急停**：急停期间**不会单独**进 HANG。**P 执行中关机**：offline 期间保持 EXECUTING；**拨回开机且不取消 → 进 HANG**（Round34 定位准；Round35 未定位同）；CONTINUE 可 `0` 回 EXECUTING——未定位时往往仍不跑（`AWAITING_ORDER`），需先定位。Round33 电机故障见旁证；错定位见 Q-038。
- 证据：Round27；A Round28；B Round31；P Round32/34/35；偶发 Round33；错定位 Q-038

### Q-036 本体异常（急停/解抱闸/关机）时空闲建新单是否执行

- 状态：`SUPPORTED`
- 结论（Round29 + Round30 P，map30，车 IDLE）：
  - **硬件急停** `CAN_NOT_RECOVER`：建单 `code=0` → 约 90s **一直 `QUEUEING`**，`executeVehicleKey=--`，车保持 IDLE
  - **软件急停** `CAN_RECOVER`：同上
  - **解抱闸** `breakSwitchState=UNMOVABLE`：同上
  - **旋钮关机** `runtime/status=offline`（Round30 P；路由仍可达 `costs>0`）：约 **90s 一直 `QUEUEING`**，同上
- 与已有「未定位 / 断连 / OFF_LINE / 离路线过远 → QUEUEING 滞留」同类：**本体不可走时新单进队不执行**，不会立刻 EXECUTING
- 证据：Round29 [`../evidence/rounds/2026-07-22-round-29/`](../evidence/rounds/2026-07-22-round-29/)；关机建单 Round30 P [`../evidence/rounds/2026-07-22-round-30/`](../evidence/rounds/2026-07-22-round-30/)

### Q-037 离路线过远时空闲建新单是否执行

- 状态：`SUPPORTED`
- 结论（Round30 D2，map30，仍定位 `LOCATION_STATE_RUNNING`）：
  - 旁证：`getRouteCostsBy` 对各可达站均为 `costs=-1` / `vehicle route to station unreachable`
  - 建单 `code=0` → 约 **120s 一直 `QUEUEING(1)`**，`executeVehicleKey=--`，车 `IDLE`；**不是** `HANG(9)`
- 对照（Round30 D1）：仅 `station=0` 但路由仍可达（`costs>0`）时，订单可进 **EXECUTING**——「离站」≠「离路线过远」
- 与 Q-032 未定位、Q-036 本体异常同类：**不可走时新单进队不执行**
- 证据：[`../evidence/rounds/2026-07-22-round-30/`](../evidence/rounds/2026-07-22-round-30/)

### Q-038 定位错误（定错位置）如何处理

- 状态：`SUPPORTED`（现场约定，**不做专项 API 测**）
- 结论：
  1. **错位置仍在路线附近**且车可执行：订单仍可进 EXECUTING，但车会往错误地方走。
  2. **错位置离路线过远**：同 Q-037 → 长期 QUEUEING。
  3. 「是否定错」只能**人工判断**；API 上仍可能是 `LOCATION_STATE_RUNNING`，无法与正确定位可靠区分。
- 消费影响：不建自动纠错；靠现场确认定位，必要时停定位重定或人工介入。
- 证据：现场约定（2026-07-22）；过远行为旁证 Q-037 / Round30 D2

### Q-039 单机「去站点」过程中建单 / HANG 时 CONTINUE

- 状态：`SUPPORTED`
- 前提：单机「去站点」要求已定位且在路线/站点上（未定位/过远/急停等无法操作）。
- 结论（Round38，map30）：
  1. **单机去站点过程中 RIoT 建单**：建单成功但长期 **`QUEUEING`**；单机到站 `MT_FINISHED` 后才进 **`EXECUTING`**。
  2. **HANG 中单机去站点时 CONTINUE**：接口可 `code=0`，但订单**仍 HANG**，`failReason≈启动移动任务时,上一个任务在运行`；**单机到位后再 CONTINUE** 可 `9→3` 并 SUCCESS。
- 证据：[`../evidence/rounds/2026-07-22-round-38/`](../evidence/rounds/2026-07-22-round-38/)

### Q-007 RIoT 通用成功与错误判定规则

- 状态：`TESTING`
- 已观测：
  - 登录错误密码返回 HTTP 200、业务 `code=2009`（A1）。
  - 业务只读接口缺/假 token 返回 HTTP **401**、业务 `code=401`（A2 / Q-015），与登录失败形态不同。
  - imap/device/task 成功路径业务 `code=0`（A2 / Round 3 B1 / Round 4 C1 的 mapInfo 接口）。
  - 旁证：`GET /api/task/v1/task/getVehicleInfo/{deviceKey}` 本轮返回顶层 `{vehicle,vehicleTaskInfo}`，未见标准 `{code,result}` 包装（Round 4）。
  - 写接口：`byDefaultMissions` 成功 `code=0`；`task/v1/order` 失败 `code=00002`（内部 NPE，HTTP 仍 200）。
  - 订单业务码：`0610008` 订单已存在；`0660003` 目的地站点不存在；`100036` interrupt 拒绝；`10015`/`10016` REJECTED 族；`100021` HANG 跳过/继续拒绝。
  - Round13：OFF_LINE / 不可达 **不**产生建单失败码（仍 `code=0` 进队列）；也**未**诱导出 `orderState=4`。
  - Round15：`getRouteCostsBy` 不可达仍 `code=0` + `costs=-1`；`queryNearEnd` 空候选 `00002`；非法 map 近邻查询 `code=0` 且 `result=null`；`curRemainCost` 假单/QUEUEING 为 `code=0` + `Long.MAX_VALUE`。
- 未知：其余模块是否统一。
- 说明：鉴权失败与登录失败必须分开建模；部分 task 接口响应形态可能与通用包装不一致；FAILED 见 Q-024。

## P2：多仓位与物模型

### Q-008 `multiLoadState` 的实际取值与变化条件

- 状态：`NA`（不纳入本项目对接）
- 原因（2026-07-21 用户确认）：多仓位机构**不直接与 RCS 通讯**，业务不依赖 `multiLoadState`；无需再测该字段取值。

### Q-009 动作服务返回 `code` 的含义

- 状态：`BLOCKED`
- 原因：物模型中多个服务返回裸整数，当前禁止业务依赖。
- 解锁条件：厂商返回码文档，或足够的正反例观测。
