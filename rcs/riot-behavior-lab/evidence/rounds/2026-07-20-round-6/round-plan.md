# Round 6（2026-07-20）

## 1. 研究目标

- 复核：先前用哪条 API 读设备/车辆状态，信息是否足够（尤其当前地图）。
- 对照探测更完整的 device runtime / detail 接口。

## 2. 范围

- 只读；无写操作。
- 测试车：`新基测试300c协作1` / `BROKERX-aee2f93d717546cf9510c98c854fe83e`

## 3. 状态

| 项 | 状态 |
|---|---|
| 复核 getVehicleInfo 字段深度 | 通过 |
| 对照 runtime/status | 通过（信息不足） |
| 对照 runtime/properties | 通过（含 mapName） |
| 其它 device 查询对照 | 通过 |

## 4. 结论摘要

- 先前主用：`GET /api/task/v1/task/getVehicleInfo/{deviceKey}`——调度态够用，但 Round4 漏读了嵌套的 `vehicle.previousState.mapName`。
- 更完整的设备物模型态：`GET /api/device/v1/runtime/properties/{deviceKey}`（含 `mapName`/`stationNo`/`sysState` 等）。
- `runtime/status` 仅 online，不够。
- 当前车 `mapName=api测试` → 对应 **mapId=29**。
