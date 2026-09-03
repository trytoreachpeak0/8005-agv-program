# Round 43 执行日志（2026-09-03）

## 环境

- 目标：**8005 生产 RIoT `http://172.19.206.222:8888`**，mapId **25**（`老厂前线new`）。
  与 Round 1～42 的跨项目测试环境 `172.10.1.72:8888` **不是同一套 RIoT**。
- 凭据：环境变量 `CONTROL_SERVER_RIOT_CALL_API_KEY`（与控制服务端同源），
  未改动 `environment.local.json`。
- **通道验证**：控制端到 `172.19.206.222` 的路由**走 Clash TUN**
  （`Find-NetRoute` → `InterfaceAlias = Clash`，`src=198.18.0.1`）。按 round-plan 的设计，
  这不构成停止条件——失真的是**可达性探测**（TUN 自答 ICMP、本地完成握手），
  而 TUN 不伪造 HTTP 响应体，且 Clash 规则把 `172.16.0.0/12` 送回 DIRECT。
  改用**内容自证**：`getALLMapInfoExcludeMapJson` 返回 7 张地图且含
  `id=25 name=老厂前线new`，与控制服务端 `appsettings.json` 的 `mapIdentity` 吻合。
  **通道为真，未改动任何系统路由。**
- 执行：段一 33 个请求全部成功；段二（`getRouteCostsBy` 量纲对照）**未采**——
  未提供 `-VehicleKey`，按 round-plan 整段跳过，不为取证干预任何车辆。
  另补 4 个单变量对照请求（034～037）。
- 全程只读，未建单、未取消订单、未移动车辆、未改配置、未编辑地图。

## 结论摘要

### 1) 线格式 —— snake_case，Kiota 生成层不可直接使用

`edges/25` 的原始 body：

```json
{"cost":15450.0,"cx":0,"cy":0,"desc":"","direction":1,"dx":0,"dy":0,
 "e_facing":1570.7963267948965,"e_node":1,"ex":-18410,"ey":40340,"id":1,
 "is_back_edge":false,"limit_v":0,"limit_w":0,"param":255,"radius":0,
 "robot_direction":1,"rotate_direction":1,"s_facing":1570.7963267948965,
 "s_node":2,"sx":-18410,"sy":24890,"type":1,"user_define_properties":{}}
```

对照 `riot-sdk` 的 `csharp/RIoT.Sdk.Generated/Imap/Models/Edge.cs:104-124`，
其反序列化键是 `cost`／`snode`／`enode`／`isBackEdge`／`limitV`／`limitW`。
**复合词全部对不上**——现场是 `s_node`／`e_node`（**连下划线位置都与 `snode`／`enode` 不同**）、
`is_back_edge`、`limit_v`、`limit_w`、`robot_direction`、`rotate_direction`、
`e_facing`／`s_facing`、`user_define_properties`。只有 `cost`／`id`／`type`／`param`／`desc`／
`direction`／`radius` 与坐标字段 `sx`／`sy`／`ex`／`ey`／`cx`／`cy`／`dx`／`dy` 一致。

站点侧同样，且更麻烦——**键名字面上带点**：`pos.x`、`check_pos.x`、`pgv_offset.x`、
`enter_pos.yaw`。它们不是嵌套对象，是带点的属性名。

**结论：走 `Raw` 拉边表必须自定义反序列化，Kiota 的 `Edge`／`Station` 模型会得到一片 null。**
这是确定的工程结论，不是失败。

### 2) 站点定位 —— `station_offset` 无用，坐标投影完美

- `station_offset` 在 **206 个站点上全部为 0**，无法用于区分同边站点。
- 改用坐标投影：站点 `pos.x/pos.y` 到其 `edge_id` 所指边的垂距
  **中位 0.0、P95 0.0、最大 4.0 mm**。
- 投影参数 t 只有两个取值：**t=1（边终点）110 个、t=0（边起点）96 个，没有一个在边中间**。
- 因此映射规则是：**比较站点坐标到边两端的距离，近者即为该站所在节点**。
- 结果：**206 个站点落到 206 个互不相同的节点，零冲突**。
- 一条边挂 2 个站点的边只有 4 条，且两站分居两端，例如
  `edge 187 [s_node=76 e_node=75]: 站1(N1-1) t=1.000 | 站2(N1-2) t=0.000`。
- 关卡站（`id=210`，控制服务端 `gateStationRiotId`）落在 **node 20**。

### 3) `Edge.cost` 的量纲 —— 就是边的欧氏长度（mm）

对 403 条边逐条比较 `cost` 与端点欧氏距离：

```
|cost - 欧氏距离| : 中位 0.012 mm, P95 33.8 mm, max 112.6 mm
偏差 > 1 mm 的边: 28 / 403
```

例：`id=1` `cost=15450.0`，`sy=24890 → ey=40340`，差 **15450**；
`id=2` `cost=11660.0`，`40340 → 52000`，差 **11660**。

坐标单位与 `getRouteCostsBy` 的 `costs`（spec 明写「单位mm」）一致，
故 `Edge.cost` 与 `costs` **同量纲**。

**注意这是推断而非直接实测**：段二未采集，本轮没有在同一对起终点上同时取到
`Edge.cost` 累加值与 `getRouteCostsBy` 的返回值。**不得用 Round 16 的数字替代**
（那是另一套 RIoT 的 map28）。直接实测留待后续轮次或实施阶段。

### 4) 算法一致性 —— 23 / 23 全中

自建有向图跑 Dijkstra，复现 RIoT 的 `queryNearEnd`／`queryNearestStart` 选择：

| 类别 | 组数 | 结果 |
| --- | --- | --- |
| `queryNearEnd`（5 候选） | 6 | 全中 |
| `queryNearestStart`（5 候选） | 6 | 全中 |
| `queryNearEnd`（2 候选，两两对决） | 11 | 全中 |

**23 组全部命中，且 RIoT 选中的站在自算排序里全部位列第一。**
对照集站点 `10, 25, 37, 74, 95, 119`，由本轮实采边表离线选出（两两可达）。

按 round-plan 的门槛（全中且 ≥5 组）：**判定为「自算与 RIoT 规划一致」**。

### 5) 图的性质

- **有向图**：403 条有向边，307 个节点；`direction` 全为 1，`is_back_edge` 全为 false；
  **403 个有序对中只有 148 个存在反向边**。最短路必须按有向图算。
- 出度为 0 的节点 3 个，入度为 0 的节点 2 个。
- 站点占用 206 个节点，其中**没有一个能到达全部其它站点节点**；
  每个站点节点可达的其它站点节点数中位为 185（共 206）。
- **站 170（node 257）到任何站点都不可达，也没有任何站点能到它。**

### 6) 需要扣除的资源 —— 全空

`removedEdge/25`、`removedEdgeDetail/25`、`removedStation/25` 三者
**均返回 `"result":[]`**。当前图不需要扣除任何边或站点。

### 7) 动态路由代价 —— 空

`GET /api/task/v1/route/` 与 `getCostUnit` **均返回 `"result":{}`**，
与测试环境 Round 15 的观测一致。当前无动态代价数据。

### 8) 边组合 —— 非空，且序列化风格与 imap 其余接口不同

`GET /api/imap/v1/mapEdgeGroup/all` 返回非空，外层 key 是**边组合名称**：

```json
{"老厂电梯":[{"edgeId":8,"gmtCreate":"2024-06-26 10:57:58","gmtUpdate":"2024-06-26 10:57:58","id":223,...
```

**注意这个接口用 camelCase（`edgeId`／`gmtCreate`），与同一 RIoT 的 `edges`／`stations`
的 snake_case 不同。**同一服务里混了两套序列化风格，自定义反序列化时须按接口区分。

### 9) 新发现：`queryNearEnd` 遇不可达站点抛 kernel NPE

本轮前两次执行连续失败，栈帧为：

```
java.lang.NullPointerException
	at sr.riot.dispatch.kernel.route.WorldRoute.queryNearestEnd(WorldRoute.java:293)
	at sr.riot.dispatch.service.impl.RouteServiceImpl.queryNearestEnd(RouteServiceImpl.java:86)
```

**与 Round 15 记载的「空候选列表 NPE」不是同一个失败点**——那次在
`RouteServiceImpl.java:87`，这次深入到了 kernel 的 `WorldRoute`。

单变量对照（034～037，唯一变量是已知不可达的站 170 是否在参数里）：

| 请求 | 参数 | 结果 |
| --- | --- | --- |
| 034 | `start=10, ends=[25,37,74,95,119]` | `code=0, result=25` |
| 035 | `start=10, ends=[25,37,74,95,119,170]` | `code=00002` NPE |
| 036 | `start=10, ends=[170]` | `code=00002` NPE |
| 037 | `start=170, ends=[10,25]` | `code=00002` NPE |

**结论：候选集合或起点中只要含有一个在有向图上不可达的站点，整个查询抛 NPE，
既不跳过该站也不返回结构化错误码。**

**消费影响**：调用方在把候选列表交给 `queryNearEnd` 之前必须自己先过滤掉不可达站点，
否则一个坏站点会让整轮择优失败。这也意味着**调用方无论如何都需要自己的路网图**——
仅靠 `queryNearEnd` 无法安全使用。

## 判定结果

| round-plan 的判定项 | 结果 |
| --- | --- |
| 线格式 | snake_case，Kiota 不可直接用（确定工程结论） |
| 站点定位 | **可行**，坐标投影，206→206 零冲突 |
| 算法一致性 | **一致**，23/23 全中 |
| 量纲 | `cost` = 欧氏边长（mm），与 `costs` 同量纲——**推断，段二未采，非直接实测** |

**总判定：路网边表可以支撑站到站路径代价自算。**三个障碍中两个解除、一个（线格式）
转为确定的工程量。

## 证据

`runs/` 下 37 个文件。主要：

- `003-edges-map-25.json`（403 条边，140572 bytes）
- `004-stations-map-25.json`（206 个站点，96226 bytes）
- `011`～`033`：对照集 23 组
- `034`～`037`：NPE 成因的单变量对照
- `799-control-set-plan.json`：对照集站点的来源与规则

## 未采与遗留

- **段二未采**：`getRouteCostsBy` 与自算值的直接量纲比对留待后续。
- `mapEdgeGroup` 的约束（`SINGLE_VEHICLE_ONLY`／`SAME_DIRECTION_ONLY`／
  `OUTSIDE_TRAFFIC_EMPTY`）是否影响规划结果**未测**——本轮对照全中说明在当前
  数据下它们没有改变最短路结果，但这不等于它们永远不影响。
- 动态代价当前为空，**非空时是否进入最短路的边权未测**。
- 地图被现场编辑后，边表缓存的失效策略未涉及。
