# 票 12 决议：`RouteGraphSnapshot` 引擎已落地，双周期刷新 ＋ fail-closed

Resolved: 2026-09-07
Resolves: `12-route-graph-snapshot-engine.md`

## 结论一句话

**引擎建成并接进派车链路**：自持一份某张 Map 的有向站点图，回答「站 A 到站 B 的代价」与
「站 B 从站 A 可不可达」，双周期刷新，陈旧即本轮不派车。

证据：**L1 361 passed / 0 failed**（新增 27 条）；**L2 `route-graph-engine` PASS**，
`normal-load` 与 `three-synthetic-peers` 回归 PASS。`src/` 下 `.Raw` 与
`queryNearEnd`／`queryNearestStart` 均为**零命中**。

## 落在哪

| 层 | 内容 |
| --- | --- |
| `ControlServer.Domain` | `RouteGraph`（有向图 ＋ Dijkstra ＋ 移除集）、`RouteGraphStationPlacement` |
| `ControlServer.Application` | `RouteGraphPorts.cs` —— `IRouteGraphSource`，引擎自己的端口 |
| `ControlServer.Infrastructure` | `HttpRouteGraphSource` —— 五个具名 Facade |
| `ControlServer.Host/Runtime/RouteGraph` | `RouteGraphRefresher`、`RouteGraphAccess`、`RouteGraphOptions` |
| `Runtime/Dispatch` | `RouteGraphReachabilityCriterion`（Order 95）、`RouteGraphCostRanker` |

**端口没进 `Ports.cs`。**票 06 为并行独占那个文件，而这个端口只属引擎一条轨，所以它在自己的
文件里。它落在 Application 而不是 Host，是因为实现它的适配器在 Infrastructure，而
**Infrastructure 不能引用 Host**——这一点是编译器教的，我最初把接口放在了 Host。

## 本票最要紧的一处设计：`REQ-0207` 的两半是两个东西

条目原文把两种情形分得很清楚，实现也必须分开：

| 情形 | 处置 | 落在哪 |
| --- | --- | --- |
| 无法确认车辆到下一站可达 | **该车退出本轮候选** | 判据（阻断） |
| 可达已确认，但成本缺失／过期／不可比 | **保留车辆**，跳过该比较组的成本层 | 排序器（回退 first-seen） |

把它们合成一个可空的数值，会在第一个调用点就丢掉这个区分——一个 `null` 到底该踢掉候选还是
只跳过一层排序，读代码的人无从判断。所以判据返回阻断原因、排序器读一个独立的
`GraphTraversalCostMm`，两条路径互不相干。

## 命名纪律靠两条架构测试守，不靠自觉

票 12 要求「自建图的输出在代码、日志与证据里都不叫 `RouteCost`」。这句话只写在文档里会烂掉，
所以有两条测试：

1. **扫引擎全部源码**，代码行里出现 `RouteCost` 即失败（`DynamicRouteCost` 例外，那是 RIoT
   自己的端点名）。**注释里可以出现**——要说清楚「这不是 RouteCost」就必须提它。
2. **扫 `Math.Sqrt`**，禁止任何直线距离混进可达性路径。唯一合法的欧氏距离在
   `RouteGraphStationPlacement` 里，那是把站点放到 RIoT 已经告诉我们它所在的那条边上，不是
   可达性判断——所以那个文件不在扫描范围内，这条豁免写在测试注释里。

`REQ-0207` 的「禁止用直线距离或其它弱替代证明可达」因此是可执行的，不是一句期望。

## 三种陈旧触发，其中一条要了一次 SDK 往返

| 触发 | 实现 |
| --- | --- |
| 设计态过期 | `gmtUpdate` ＋ 10 分钟 TTL 兜底 |
| 运行态过期 | 独立 10 秒周期，预算 45 秒（校验器强制预算 > 周期） |
| 边组指纹变化 | 与上一次指纹比对 |
| 动态代价由空变非空 | 读 `GET /api/task/v1/route/` |
| （另加）刷新失败 | 任何一段读失败即标陈旧，旧快照不再算数 |

**最后那条不在票据里，是我加的**：一张十分钟前正确的图不是关于现在的证据，而引擎存在的全部
意义就是证据断了就停。

**动态代价这条要了一次 SDK 发版**。它读的 `GET /api/task/v1/route/` 本来就在 `REQ-0146` 的
具名清单里（`CP-0001` 之前就有），但 SDK 没有封装它，而产品代码不得用 `.Raw`。所以：

- SDK 新增 `ReadDynamicRouteCostPresenceAsync`，**只报告存在性与条目数，不报值**——这个端点
  在所有观测里都答 `"result":{}`（测试 RCS 的 Round 15、生产的 Round 43），**它的非空形态没有
  人见过**。给一个没人观测过的形状编一个类型，是猜测穿了领域模型的外衣。
- `ImapWire` 随之**改名 `RiotWire`**：它做的是「手写读 RIoT 响应体」，而 task 模块也有一个同样
  读不了的端点，名字里带 imap 已经不准确。两端同步改名，行为一字未变。**票 07 答案里提到的
  `ImapWire.cs` 现在叫 `RiotWire.cs`。**
- SDK 发 **`0.2.0-fp.3`**，control-server 升包。

## 一处 fail-closed 当场证明了自己

第一次跑 L2 时场景红了，backlog 里是 `ROUTE_GRAPH_REFRESH_FAILED`：**假 RIoT 没有
`GET /api/task/v1/route/`，404 → 刷新失败 → 快照标陈旧 → 本轮不派车。**

这不是缺陷，是设计在工作：引擎读不到就不派车，一次没有。补上假 RIoT 那个端点（它属于票 03 的
能力面，写票 03 时我还不知道引擎会读它）后场景转绿。

**这也是为什么引擎的出口必须有 L2**：L1 里这条链路是通的，因为 L1 用的是假的 source；只有真的
把服务端跑起来打真的假 RIoT，才会发现装置少了一个端点。

## 几处自行定案

1. **图每次读都重建，不缓存。**map25 是 403 边 206 站，重建的开销在一轮的 I/O 面前微不足道，
   而缓存需要一条失效规则——那条规则可能与陈旧规则不一致，「这份还新鲜吗」有两个答案就多了一个。
2. **代价按整数比较与累加。**浮点求和出来的最短路，事后从证据里复算不出同一个结果；而亚毫米
   精度对一台车没有意义。
3. **不可达的站点在单源结果里直接缺席，不给哨兵值。**哨兵正是 `REQ-0207` 禁止被当作成本去比较
   的那种值。
4. **新建快照默认陈旧**（`ROUTE_GRAPH_NEVER_REFRESHED`）。「还没取过」绝不能读成「一张可用的
   空图」。
5. **引擎默认关闭，关闭时判据放行。**关闭是「这套部署还没启用它」，不是一个路由判决；既有场景
   面对的仍是引擎出现之前的那台服务端。
6. **边组指纹的首次为空不算变化。**map25 一个边组都没有，首个指纹就是空串；把它当变化会让引擎
   在第一个 tick 就陈旧——在这个项目真正跑的那张图上。有一条测试专门守这个回归。

## 验收清单

- [x] 设计态与运行态双周期各自刷新，周期与 TTL 可配置（并有启动期校验：预算必须大于周期）
- [x] `mapEdgeGroup` 指纹变化即进陈旧态；动态代价由空变非空即进陈旧态
- [x] 陈旧态下本轮不派车，且阻断原因可追溯到引擎而非笼统的「无候选」
      （判据返回引擎自己的 `ROUTE_GRAPH_*` 原因，写进 `JourneyBacklog`）
- [x] 站到站代价与可达性两项能力各自具名，可达性不可用时不退化为成本估算
- [x] 自建图的输出在代码、日志与证据里都不叫 `RouteCost`——**两条架构测试守着**
- [x] `REQ-0207`：不可达车辆退出本轮候选；直线距离等弱替代在代码里不存在（架构测试）
- [x] 五个 `imap` 端点全部经具名 Facade 调用，`.Raw` 零命中（排除注释后实测 0）
- [x] L1 新增覆盖：双周期刷新、三种陈旧触发、可达与不可达的判定各有测试（27 条）
- [x] 无新增 migration（表由票 06 提供）

**表述纪律**：`CP-0001` 已于 2026-09-07 批准（票 04），所以本票的证据可以直接写「符合
`REQ-0298`（v1.1.0）」，不必再按规格 8.8 第 3 条记偏离。引用基线时带上版本号——同一条 ID 在
v1.0.0 与 v1.1.0 里文义不同。

## 两处如实记的边界

1. **L2 没有不可达的负例。**合成种子的图是个环，任意两站互相可达，做不出反例；要在 L2 造一个
   得给假 RIoT 加一条「把某条边下线」的控制命令，那是把装置越造越像被测物。分层清楚：**L2 证
   这条链路真的接通了，L1 证判定本身对不对**（可达、不可达、位置未知、陈旧、引擎关闭五种都有）。
2. **`MapEdge.CostMm` 与 `getRouteCostsBy` 同量纲仍是推断。**Round 43 没在同一对起终点上同时
   取过两者。引擎内部只用自己的图比较自己的代价，所以这条推断目前不承重；票 13 把两个证据源
   放在一起比较时，它就承重了。

## 给下游票的指针

**票 13（`FP-C13` 建单前置门禁）**——门禁是一条判据，位置在 `StationResolutionCriterion` 之后
（要 route）、`SlotCapacityCriterion` 之前（不必为一个到不了的站读 box count）；Order 取 96
即可插在可达性判据之后。`CreateGateAuditRow` 里两个证据源已经分别具名
（`RiotRouteCostMm` 与 `GraphTraversalCostMm`），**两者分歧时阻断建单并告警**，别取其一。

**票 09（B2 多车）**——引擎已经是按车问的：判据读的是
`evaluation.Vehicle.Vehicle.CurrentStationId`，也就是本轮正在决策的那台车。多车下不用改引擎，
把 `DispatchVehicleKeys()` 换掉即可。

**票 18（轨 B 出口）**——引擎的 L2 场景是 `route-graph-engine`，setup 里 `RouteGraph.Enabled`
打开即可；编排器已支持把 `RouteGraph:*` 注入服务端环境。

## 遗留

- 改动提交在本地 worktree：`riot-sdk` 的 `d9462a6`，`8005-agv-control-server` 的 `646624a`，均未推送。
