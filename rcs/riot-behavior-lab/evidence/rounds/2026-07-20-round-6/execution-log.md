# Round 6 执行日志

## 问题

Round 4/5 选图困难，用户指出：读取设备状态的 API 可能信息不够。

## 先前实际使用的 API

- **主路径**：`GET /api/task/v1/task/getVehicleInfo/{deviceKey}`
- **对照失败**：`GET /api/task/vehicles/getVehicleInfoByDeviceKey?deviceKey=...` → `code=00002` 内部错误

Round 4 当时只扫描了 `vehicle` 顶层字段名含 `map` 的项，**漏掉了嵌套字段**。

## 复核 getVehicleInfo（深度字段）

- 证据：[`runs/B2-getVehicleInfo-map-fields.json`](./runs/B2-getVehicleInfo-map-fields.json)、[`runs/B2-getVehicleInfo-full.json`](./runs/B2-getVehicleInfo-full.json)
- 发现：
  - `vehicle.previousState.mapName` = **`api测试`**
  - `vehicle.previousState.stationNo` = 1
  - `vehicle.plantModel` 字符串亦为 `api测试`
  - 顶层仍有 `currentStation=1`、`procState=IDLE` 等

## 对照其它状态面

证据目录：`runs/B2-status-*.json`，对照摘要 [`runs/_status-api-compare.txt`](./runs/_status-api-compare.txt)

| API | 结果 | 对“当前地图”是否有用 |
|---|---|---|
| `GET /api/device/v1/runtime/status/{deviceKey}` | `code=0`，仅 `online`+timestamp | **不够** |
| `GET /api/device/v1/runtime/properties/{deviceKey}` | `code=0`，含物模型属性袋 | **有用**：含 `mapName`、`stationNo`、`sysState`、`movementState`、`multiLoadState` 等 |
| `queryDeviceByDeviceKey` / `devices/detail` | 偏静态档案 | 不足以替代运行态 |
| `frontQueryDeviceProperties` / `queryDevicesProperties` | 大体量属性 | 与 runtime/properties 同类，偏重 |

`runtime/properties` 精选字段：[`runs/B2-device-runtime-properties-picked.json`](./runs/B2-device-runtime-properties-picked.json)

- `mapName` = `api测试`
- `stationNo` = 1
- `sysState` = 2
- `batteryPercentage` = 35

## 结论

1. 先前 API **不是完全没有地图信息**，而是读浅了；`getVehicleInfo` 里地图名在 `previousState.mapName`。
2. 若要设备物模型运行态，应加读 **`runtime/properties`**；`runtime/status` 不能当状态主源。
3. 名称 `api测试` 与 C1 清单对齐 → **mapId=29**（与 Round5 候选短距 lab 图一致）。

## 建议后续默认状态采样

- 调度/任务：`getVehicleInfo`
- 设备物模型：`runtime/properties`
- 地图枚举仍用 mapInfo；用 `mapName`→`mapId` 反查（本现场名称唯一于清单）

## 补记：离站读数（同日稍后）

- 证据：[`runs/B2-off-station-snapshot.json`](./runs/B2-off-station-snapshot.json)
- 观察：车仍在 `api测试`，但 `currentStation=0` / `stationNo=0` / `noStation=true`，坐标仍可读。
- 已晋升契约：**BC-STATE-002**（站号 0 = 未在站，不是丢图）。
