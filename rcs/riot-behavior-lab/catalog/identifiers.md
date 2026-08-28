# 跨接口标识关系

本文件记录标识的职责和待验证关系。除明确标记外，当前内容来自静态 schema，证据等级为 `SCHEMA`。

## 订单与实验

- `localExperimentId`：行为实验室生成，只用于组织证据，不发送给 RIoT。
- `upperId`：上层系统订单唯一标识；本现场 `byDefaultMissions` 下具有唯一约束——重复提交返回 `0610008`（BC-ORDER-004，`OBSERVED`）。
- `orderId`（字符串）：形如 `order-...`，建单返回；用于 `detailByOrderId` 与 `task/.../command/{orderId}`（BC-ORDER-005）。
- `id`（数值）：订单记录主键；用于 `GET /orderRecord/{id}` 与 `POST /order/v1/operate` 的 `orderId` 字段。
- `orderKey`：command 路径参数与字符串 `orderId` 在本现场为同一值（`OBSERVED` Round 9/10）。

## 车辆与设备

- `deviceKey`：device/物模型视角的设备标识；也可出现在 task `getAllVehicleSimpleInfo` 中。
- `deviceName`：车辆/设备显示名；本现场可用其在 `getAllVehicleSimpleInfo` 中精确解析到 `deviceKey`（见 BC-VEH-002）。
- `vehicleKey`：task 调度视角的车辆标识（部分接口 path/字段名使用该称呼）。
- `appointVehicleKey`：建单时指定执行车辆的字段。
- `executeVehicleKey`：订单实际执行车辆的字段；QUEUEING 未派执行时常为 `"--"`（Round14 `OBSERVED`）。
- `vehicleTaskInfo.key` / `vehicleTaskInfo.name`：`getAllTaskVehicles` 富对象中的标识/名称字段（`OBSERVED` 于 Round 3）。

当前已观测（Round 3）：

- task 车辆清单中的 key 与 devices 中对应车的 `deviceKey` 一致（18/18 交集）。
- devices 另含 14 台非车设备，不得用于派车（BC-VEH-001）。

已验证（Round 7/10）：合法 `appointVehicleKey` 执行期回写为同一 `executeVehicleKey`（BC-ORDER-002）。  
反例（Round 10）：伪造/缺失 `appointVehicleKey` 仍可进 QUEUEING（BC-ORDER-007）——业务层必须自行校验。

列表查询（Round14 / BC-ORDER-013）：

- SCHEMA 支持 `executeVehicleKey` 过滤；**不能**单独用它枚举本车 QUEUEING 积压。
- 查询参数 `appointVehicleKey` **不可靠**（未声明且实测可串其它车）。
- 按车积压：`filterByState` 非终态 + 客户端用 `appointVehicleKey`/`executeVehicleKey` 匹配本车。

## 地图与站点

- `mapId`：地图标识；本现场取自 mapInfo 返回项的 `id`（BC-MAP-001，`OBSERVED`）。
- `mapName` / `name`：地图可读名；与 `mapId` 成对出现在 mapInfo 列表中。
- `stationId`：地图中的站点标识；本现场 stations 接口字段名为 **`id`**（BC-MAP-002，`OBSERVED`）。
- `stationName`：业务可读站点名称；本现场 stations 接口字段名为 **`name`**。
- `currentStation` / `stationNo`：车辆**当前归属站号**（调度面 / 物模型面）。
  - 正整数：通常对应该图 `stations` 列表中的 `id`。
  - **`0` + `noStation=true`**：表示**当前不在任何站点上**（BC-STATE-002，`OBSERVED`）；不要当成站点 id=0。
- `destination`：mission 中的目的站字段，静态说明指向站点 ID。

`stationId` 是否跨地图唯一：本现场至少四张候选图都存在 `id=1`，**跨图不唯一**（`OBSERVED`）。每轮证据必须同时保存 `mapId` 和 `stationId`。

Round 6：可用 **`mapName`** 读出当前图再反查 `mapId`：

- `getVehicleInfo` → `vehicle.previousState.mapName`（亦见 `vehicle.plantModel` 字符串）
- `runtime/properties` → 属性 `mapName` / `stationNo` / `sysState` 等
- 测试车观测：`mapName=api测试` → mapId **29**
- 离站时 `mapName` 仍可读，仅站号变 0

注意：`runtime/status` 只有在线心跳，不能代替上述状态源。

## 物模型动作

- `services[].identifier`：TSL 中的动作服务标识。
- `serviceId`：device command API 使用的服务标识。
- `functionKey`：order mission 关联物模型动作的字段。
- `actionId`：task 或车端动作使用的数字标识。

这四者的映射不能仅靠名称猜测。每个已确认映射必须指向具体 `productKey`、物模型版本和现场实验。

## 关联记录要求

每个写实验至少保存：

```text
localExperimentId
→ upperId
→ RIoT 返回的 orderId/orderKey
→ appointVehicleKey/executeVehicleKey
→ mapId/destination
```

字段缺失时写 `UNKNOWN`，不要用另一个字段的值代填。
