# Round 4 执行日志

## C1 mapInfo/all

- 时间：`2026-07-20T10:14:12+08:00`
- 请求：`GET /api/imap/v1/mapInfo/all` + Bearer `callApiKey`
- 证据：[`runs/C1-mapInfo-all.json`](./runs/C1-mapInfo-all.json)
- 观察事实：HTTP 200，`code=0`，**18** 张地图；证据已剥离 `mapJson`。
- 与假设关系：`SUPPORTED`（Q-018 主路径）

### 地图清单（id → name）

| mapId | name | floor |
|---|---|---|
| 6 | 尊阳电镀线 | 0 |
| 7 | 华士新厂南侧2楼电梯 | 2 |
| 8 | 华士新厂南侧1楼电梯 | 1 |
| 9 | 二楼连廊 | 2 |
| 11 | 华士老厂 | 1 |
| 12 | 华士新厂 | 1 |
| 13 | 电镀plus | 1 |
| 14 | 尊阳电镀线opt | 1 |
| 16 | 新潮尊阳测试 | 0 |
| 17 | 2 | 0 |
| 18 | 3opt | 0 |
| 19 | ZY_WB_Map | 0 |
| 21 | 长廊 | 0 |
| 25 | ZY_WB_MapF | 0 |
| 26 | 新基测试1 | 0 |
| 27 | 新基测试2 | 0 |
| 28 | 新基测试2opt | 0 |
| 29 | api测试 | 0 |

## C1 轻量对照 getALLMapInfoExcludeMapJson

- 证据：[`runs/C1-mapInfo-excludeMapJson.json`](./runs/C1-mapInfo-excludeMapJson.json)
- 观察事实：同样 `code=0`，**18** 张，数组形态；适合日常枚举（本就不带/少带几何）。
- 与假设关系：`SUPPORTED`（可作为 mapInfo/all 的轻量等价枚举路径）

## C1 测试车地图线索

- 证据：[`runs/C1-test-vehicle-map-clues.json`](./runs/C1-test-vehicle-map-clues.json)
- 观察事实：
  - `getVehicleInfo/{deviceKey}` 返回顶层 `{vehicle, vehicleTaskInfo}`，**无**标准 `{code,result}` 包装（记入 Q-007 旁证）。
  - `vehicle` / `vehicleTaskInfo` **均无 mapId/mapName 字段**。
  - 可见位置线索：`currentStation=1`，`currentNode=1`，在线，电量约 36–37%，`procState=IDLE`，但 `vehicleTaskInfo.enable=false`。
  - `getVehicleInfoByDeviceKey` 本轮返回业务 `code=00002`（内部错误），不作主路径。
  - 按命名，与测试车相关的候选图：`26 新基测试1` / `27 新基测试2` / `28 新基测试2opt` / `29 api测试`——**需用户确认或后续用站点交叉验证**，本轮不选定。
- 与假设关系：地图清单已支持；“车当前在哪张图”仍开放

## 本轮结论

- `Q-018`（有哪些地图 / 如何取 mapId）→ **`SUPPORTED`**
- 推荐枚举：`GET /api/imap/v1/mapInfo/all` 或 `getALLMapInfoExcludeMapJson`
- 下一步：请你指定（或确认）派车使用的 `mapId`，再做 C2 站点列表
- 摘要：[`runs/_map-summary.txt`](./runs/_map-summary.txt)
