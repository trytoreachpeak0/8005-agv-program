# Round 15（2026-07-20）— Route Controller GET/POST（mapId=28 新基测试2opt）

## 问题

- **Q-026**：Route Controller 各 GET/POST 的请求/响应形态、可达性语义与业务使用场景是什么？

## 范围

- 地图：`新基测试2opt` / **mapId=28**（用户授权）
- 允许：
  - `GET /api/task/v1/route/`
  - `GET /api/task/v1/route/getCostUnit`
  - `GET /api/task/v1/route/curRemainCost/{orderKey}`
  - `POST /api/task/v1/route/getRouteCostsBy`
  - `POST /api/task/v1/route/queryNearEnd`
  - `POST /api/task/v1/route/queryNearestStart`
- **禁止**：一切 `DELETE`（含 `dynamicRouteCost*`）
- 车辆：仅测试车 key；`getRouteCostsBy` 的 `deviceKeys` 只含本车
- 本轮**不**为测路由而把车物理切到 map28（除非 API 纯拓扑可算）；若 `getRouteCostsBy` 因车不在该图返回 -1，记为观测

## 步骤

1. E0：车态 + 拉 map28 站点清单
2. R1：GET `/route/`、`/route/getCostUnit`
3. R2：POST `getRouteCostsBy`（map28 多站；可选 map29 对照）
4. R3：POST `queryNearEnd` / `queryNearestStart`（map28）
5. R4：`curRemainCost`（无效 key；若车空闲可在**当前图**短距建单观测后 cancel）
6. 落证据与使用场景结论
