# Round 15 执行日志（2026-07-20）

## 环境

- baseUrl: `http://172.10.1.72:8888`
- 研究地图：**新基测试2opt / mapId=28**（33 站，用户授权）
- 测试车：`新基测试300c协作1`（当时实际在 **api测试/map29**，离站 `station=0`）
- 禁止：一切 Route `DELETE`
- 脚本：`run-round15.ps1` / `run-round15-resume.ps1` / `run-round15-probe2.ps1`

## 接口一览与使用场景（本轮结论）

| API | 方法 | 本轮结果摘要 | 使用场景（推断 + 观测） |
|---|---|---|---|
| `/api/task/v1/route/` | GET | `code=0`，`result={}` 空 | 查看**当前动态路由代价缓存**（全局）。空=当前无动态代价条目。偏运维/调试，不是建单前置。 |
| `/api/task/v1/route/getCostUnit` | GET | `code=0`，`result={}` 空 | 查看动态代价的**因子单元**（schema：`doAction/emergencyStop/obstacles/orderHang/traffic` 等）。空=无活跃单元。偏运维；与 DELETE 清缓存成对。 |
| `/api/task/v1/route/getRouteCostsBy` | POST | map28 全站 `costs=-1` unreachable；map29 站1=`2210`、站2=`250` ok | **建单前可达性/选站代价**：按「车当前位置 → 指定 map 的 station」算路径代价（mm）。`-1`=不可达。MES 选站、跨图校验应用此接口。 |
| `/api/task/v1/route/queryNearEnd` | POST | map28：`start=1, ends=[2,3,4]→2`；`[2,33]→33`；空候选 NPE | **图上选最近终点**：给定起点 + 候选终点列表，返回路径代价最小的终点 stationId。**不依赖车在哪**，纯地图拓扑。适合多卸货点/多终点择优。 |
| `/api/task/v1/route/queryNearestStart` | POST | map28：`end=4, starts=[1,2,3]→3` | **图上选最近起点**：给定终点 + 候选起点，返回最近起点。适合多发车点/就近取货。 |
| `/api/task/v1/route/curRemainCost/{orderKey}` | GET | 假单/QUEUEING 均返回 `Long.MAX_VALUE`；本轮未进 EXECUTING | **执行中订单剩余路径代价**。未开始移动时哨兵值 `9223372036854775807`，**不能**当真实剩余距离。 |

未测（用户禁止）：`DELETE .../dynamicRouteCost`、`DELETE .../dynamicRouteCostByVehicle`。

## 详细观测

### E0

- 车：`mapName=api测试`，`station=0` 离站，`IDLE`/`ON_LINE`
- map28 站点 33 个（与 Round5 一致）

### R1 动态代价只读

- `GET /route/`、`GET getCostUnit` 均成功但空对象 → 现场当时无动态代价数据可展示。

### R2 getRouteCostsBy

- body：`{mapId, stationId, deviceKeys:[本车]}`
- **车在 map29 时查 map28**：所有抽检站 `costs=-1`，`message=vehicle route to station unreachable`（HTTP/业务仍 `code=0`）
- **对照 map29**：站1=`2210 ok`，站2=`250 ok`（离站仍可按当前位置估代价）
- 假 deviceKey / 非法站：见 `R2-getRouteCostsBy.json` negatives

### R3 queryNear*（map28，纯拓扑）

- `queryNearEnd` / `queryNearestStart` **不需要车在该图**，均可 `code=0` 返回 int stationId
- 路径代价最近 ≠ 欧氏最近：`1→[2,33]` 选了 **33** 而非 2
- 空 `endStationIds` → `code=00002` NPE；非法 mapId=999999 → `code=0` 但 `result=null`

证据：`R3-*.json`、`R3b-near-tight.json`

### R4 curRemainCost

- 假 orderKey：`code=0`，`result=9223372036854775807`（Long.MAX）
- 本轮两次 map29 短距建单均长时间停在 `QUEUEING` + `execute=--`（车离站 IDLE），未能采到 EXECUTING 剩余代价
- **结论**：QUEUEING/无效单的 remain 是哨兵最大值；EXECUTING 下的递减轨迹本轮未观测（记入开放点）

## 对 MES 的直接建议

1. **跨图/可达性**：建单前调 `getRouteCostsBy`；`costs==-1` 不要发单（与 BC-ORDER-012 一致）。
2. **多候选站择优**：用 `queryNearEnd` / `queryNearestStart`（只传 mapId+站列表，与车当前图无关）。
3. **进度条**：不要用 `curRemainCost` 的 MAX_VALUE；仅在确认订单 EXECUTING 且值合理后再用。
4. **动态代价 GET**：空结果常见；非业务闭环必需。
5. **不要调 DELETE**（本轮禁止；清全局/按车缓存有副作用风险）。

## 证据文件

- `runs/E0-*.json`、`R1-*.json`、`R2*.json`、`R3*.json`、`R4*.json`
- schema 摘录：`_schemas-route.json`
