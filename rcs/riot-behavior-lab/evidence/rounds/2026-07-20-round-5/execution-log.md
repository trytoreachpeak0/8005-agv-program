# Round 5 执行日志

## C2 站点清单（候选测试图）

- 时间：`2026-07-20T10:19:23+08:00`
- 接口：`GET /api/imap/v1/mapInfo/stations/{mapId}` + Bearer `callApiKey`
- 证据：
  - [`runs/C2-stations-map-29.json`](./runs/C2-stations-map-29.json)
  - [`runs/C2-stations-map-26.json`](./runs/C2-stations-map-26.json)
  - [`runs/C2-stations-map-27.json`](./runs/C2-stations-map-27.json)
  - [`runs/C2-stations-map-28.json`](./runs/C2-stations-map-28.json)
  - [`runs/C2-stations-overview.json`](./runs/C2-stations-overview.json)
  - [`runs/_stations-summary.txt`](./runs/_stations-summary.txt)

### 观察事实

| mapId | 地图名 | 站点数 | 含 id=1 |
|---|---|---|---|
| 29 | api测试 | **2** | 是（站点1、站点2） |
| 26 | 新基测试1 | **4** | 是 |
| 27 | 新基测试2 | **31** | 是（含发车点/卸货点等） |
| 28 | 新基测试2opt | **33** | 是 |

- 成功判定：HTTP 200 + 业务 `code=0`，`result` 为**站点数组**。
- 字段契约（本现场）：**`stationId` = `id`，站名 = `name`**；另有 `type`、`pos.x`/`pos.y`/`pos.yaw`、`edge_id` 等。
- 车辆线索 `currentStation=1` 在四张候选图中**都存在** id=1，**不能**单靠站号反推绑图。

### map 29 全量站点（最适合作短距 lab）

| stationId (id) | name |
|---|---|
| 1 | 站点1 |
| 2 | 站点2 |

## C2 反例：非法 mapId=0

- 证据：[`runs/C2-stations-map-0-invalid.json`](./runs/C2-stations-map-0-invalid.json)
- 观察：HTTP 200，`code=0`，`message=成功`，**站点数组为空**（不是 4xx，也不是业务失败码）。
- 含义：客户端不能只看 `code==0` 就认为有站；必须检查列表长度，并确认 mapId 来自有效地图清单。

## C2 单图 / 单站探针

- [`runs/C2-mapInfo-29.json`](./runs/C2-mapInfo-29.json)：`GET /api/imap/v1/mapInfo/29`
- [`runs/C2-mapInfo-29-station-1.json`](./runs/C2-mapInfo-29-station-1.json)：`GET /api/imap/v1/mapInfo/29/1` → `id=1` / `name=站点1`，含坐标

## 本轮结论

- `Q-019` → **`SUPPORTED`**
- 推荐读站：`GET /api/imap/v1/mapInfo/stations/{mapId}`
- **建议 lab 短距图**：`mapId=29`（api测试，仅 2 站）；目的站候选：从当前站换到另一站（1↔2）。
- **仍需你确认**：测试车实际所在图；以及写单前的安全目的站。
- 与假设关系：站点枚举路径成立；绑图问题仍开放（四图都有站 1）
