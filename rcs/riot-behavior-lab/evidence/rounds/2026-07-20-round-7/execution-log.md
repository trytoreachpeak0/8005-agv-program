# Round 7 执行日志

## 环境

- 测试车：`新基测试300c协作1` / `BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：mapId=29（`api测试`），用户确认车在站点1
- 目标：站点2（短距；D1 路径代价 **1040**，`message=ok`）
- 鉴权：`callApiKey`；**未使用车辆组**

## 步骤 0：基线

- `currentStation=1`，`mapName=api测试`，`procState=IDLE`，`connected=true`
- **调度态异常**：`vehicleTaskInfo.enable=false`，`integrationLevel=OFF_LINE`（随后多次上线失败探测后读成 `null`），`fleetMode=FLEET_MODE_OFFLINE`
- 对照：同现场约 16 台车为 `ON_LINE` + `enable=true`
- 设备侧 `devices.enable=true`、`runtime/status=online`——**设备在线 ≠ 调度在线**
- 证据：`runs/E0-baseline-before-online.json`，`runs/E0-vehicle-now.json`

## 步骤 1：单车切 ON_LINE（失败）

- 接口：`POST /api/task/vehicles/updateVehicleIntegrationLevel`
- Swagger body 仅有 `deviceKeys` + `serviceId`（疑似契约不完整）
- 实测多种 body/query（`integrationLevel`/`serviceId`/`status`/`level`/路径参数等）均返回业务 `code=00002`，`NullPointerException` @ `AbstractVehicleTaskInfoSupport.updateIntegrationLevel`
- **未观察到其它车状态被改动**（`deviceKeys` 仅含本车）
- 证据：`runs/E0-online-attempt-*.json`

## 步骤 1b：旁路尝试

- `POST /api/device/v1/command/properties/{deviceKey}` 设 `fleetMode=2` → `code=0`，但属性仍读 `fleetMode=1`，车侧 `FLEET_MODE_OFFLINE` 不变
- 结论：物模型 `fleetMode` **不能**替代调度 `integrationLevel` 上线

## 步骤 D1：路径代价（成功，只读）

- `POST /api/task/v1/route/getRouteCostsBy`，body：`{mapId:29, stationId:2, deviceKeys:[测试车]}`
- 结果：`code=0`，`costs=1040`，`message=ok`
- 证据：`runs/D1-route-cost-correct.json`
- 含义：**站1→站2 在地图上可达**；挡单的不是路径，是调度态

## 步骤 E1：建单（失败，无落库）

候选 body（与现场 SUCCESS 订单 mission 旁证一致）：

```json
{
  "appointVehicleKey": "<testVehicleKey>",
  "appointMapId": 29,
  "orderType": "NORMAL",
  "orderName": "riot-behavior-lab-E1-...",
  "upperId": "riot-behavior-lab-E1-...",
  "mission": [{ "type": "move", "mapId": 29, "destination": 2 }]
}
```

- `POST /api/task/v1/order` 多种变体均 `code=00002`，NPE @ `OrderTaskServiceImpl.createOrderTask`（`ConcurrentHashMap.put` null key）
- `detailByUpperId` 无订单；测试车 `orderRecord` 仍为空 → **未产生遗留订单，未派到其它车**
- `POST /api/order/v1/add/byDefaultMissions` 亦失败（JSON parseInt / 未继续深挖）
- 证据：`runs/E1-*.json`

## 当前阻断

| 项 | 状态 |
|---|---|
| 路径可达（D1） | 通过 |
| 调度上线 API | **失败**（契约不明 / 服务端 NPE） |
| E1 建单 | **失败**（疑与 OFF_LINE / enable=false / integrationLevel=null 相关） |
| 误派他车 | 未发生 |
| 遗留订单 | 无 |

## 需要人工干预

请在 RIoT **网页**对 **仅**「新基测试300c协作1」执行「调度上线 / ON_LINE / 启用接单」（界面用词以现场为准），使：

- `vehicleTaskInfo.integrationLevel == ON_LINE`
- `vehicleTaskInfo.enable == true`
- （期望）`vehicle.fleetMode` 不再是 `FLEET_MODE_OFFLINE`

完成后回复「已上线」，本轮继续 E1→E2（站1→站2）。

若网页上线时浏览器 Network 里能看到 `updateVehicleIntegrationLevel` 的真实请求 body，请把该 JSON（可打码 key）发我，便于补齐 API 契约。
