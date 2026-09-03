# 票 14 决议：依 Round 43 实测定途中追加与换序的形态

日期：2026-09-03
票据：[14-decide-en-route-append-and-resequencing-form-from-round-43.md](14-decide-en-route-append-and-resequencing-form-from-round-43.md)
前置：[票 03 决议](03-answer.md) 的 Q12／Q13，`rcs/riot-behavior-lab/evidence/rounds/2026-09-03-round-43/`

## 一句话结论

Round 43 判定边表可用，故 `REQ-0196`／`REQ-0198`／`REQ-0197` 三条**全部按完整能力实施**，
`证据受限实施` 形态在本簇**清零**；新增工程大件 **`RouteGraphSnapshot` 路网成本引擎**，它以
**计划锚**给出精确边际成本、以**自建图**作为可达性唯一权威，因此 `getRouteCostsBy` 与
`queryNearEnd` **一律退出产品代码路径**，票 03 的 Q2 档 β 随之升级为全自算。

## 落笔时新查到的事实（决定了下面若干问题的形态）

| 事实 | 来源 |
| --- | --- |
| 控制服务端**今天零调用** `queryNearEnd`／`queryNearestStart`／`getRouteCostsBy`，也不拉边表；`MapIdentity` 只是字符串 `老厂前线new`，连 mapId 25 这个数字都不在配置里 | `grep` `8005-agv-control-server/src/` |
| 车辆投影已带 `CurrentStationId`（`ControlServer.Application/Ports.cs:224-225`）且已读 `LocationState`（`HttpRiotMovementGateway.cs:264`），**没有** `CurrentNode` | 同上 |
| RIoT `Vehicle` 有 `currentNode`／`currentStation`／`noNode`／`noStation`／`precisePosition`，**全部无 description**；`currentNode` 与 `Edge.s_node` 是否同 id 空间**未测** | `riot-sdk/specs/task.json` |
| `getALLMapInfoExcludeMapJson` 30 ms／1835 B，每图带 `gmtUpdate`；但**7 张图的 `gmtUpdate` 完全相同**（`2026-08-29 19:33:23`），更像批量同步戳而非单图编辑戳 | Round 43 `runs/002-map-list.json` |
| 全图刷新 = 5 个只读调用：`edges` 39 ms/140 KB、`stations` 30 ms/96 KB、`removed*` 三个各 14～72 ms/67 B。整图重拉 ≈ 200 ms，远小于 2 秒节拍 | Round 43 `runs/003`～`007` |
| **图上不可达是常态**：每个站点节点可达的其它站点数中位 **185 / 206**，站 170 与任何站互不可达 | Round 43 `execution-log.md:94-101` |

最后一条直接冲击 `CONTEXT.md` 原 `RouteCostEvidenceBoundary` 那句「路径证据缺失只作为少见
异常边界而非常态降级路径」，见 Q2。

## 逐问决议

### Q1 — 边际成本的起点锚：**计划锚**

`VehicleMarginalRouteCost` 的增量**自插入位的前一站起算**，不自车辆物理位置起算；无既有计划的
车辆锚在其 `CurrentStationId`。

**这不是近似，是精确值。**在途车的真实增量里，「车当前位置 → 计划下一站」这一段在插入前后
**完全相同**——`PlannedStopMutationBoundary` 明文禁止改车辆正在驶向的当前下一站——所以那一段
在做差时**恒被抵消**。计划锚算出的差值与物理锚算出的差值**相等**。

因此全部计算都是站→站，落在自建图的 206 个站点节点之间。连带收掉三个麻烦：

1. **单一成本源**，`Edge.cost` 与 `getRouteCostsBy` 的 `costs` 的量纲一致性从必答题降为无关项（见 Q5）。
2. **不必绕 Facade 走 `Raw` 查成本**（票 03 Q2 记的 `TaskClient.cs:65` 把 `deviceKeys` 写死成单元素、
   逐车调用使 RIoT 往返随车数线性增长——这个约束随本决议消失）。
3. **不依赖任何未证明的 id 空间假设**（`currentNode` 与 `Edge.s_node` 是否同空间，本方案不需要知道）。

不取物理锚：它要新增 `currentNode` 投影，先得验证 id 空间，且 `noNode=true` 时仍要退回
`getRouteCostsBy`，把已经消掉的量纲问题又请回来——换来的精度增益是**零**（见上面的抵消论证）。
不取混合：同上，且引入两个成本源。

**唯一缺口**：空闲车停在非站点位置（刚被手动移动、停在路中间）时，该车本项证据缺失，按
`RouteCostEvidenceBoundary` 跳过成本排序层继续比较后续层。这是**成本缺失**不是**不可达**，
不影响该车参与派车。

### Q2 — 可达性判定的权威：**迁到自建图，并拆分 `RouteCostEvidenceBoundary`**

可达性由 `RouteGraphSnapshot` 上的有向图判定，Dijkstra 无路即不可达。RIoT 的
`getRouteCostsBy`（`costs:-1` + `"vehicle route to station unreachable"`，Round 41 实测）与
`queryNearEnd` 都**不进产品代码路径**。

**原词条把两个正交概念揉在了一起，必须拆开**，因为 Round 43 证实图上不可达在 mapId 25 上根本
不是少见情况：

| 概念 | 语义 | 处置 | 频率 |
| --- | --- | --- | --- |
| **`StationReachability` 不可达** | 图给出的**确定结论**：确实没有路 | 该候选静默退出本轮，**不告警** | **常态**（可达中位 185/206） |
| **成本证据缺失** | 图**本身**不可用或该车锚不到站点 | 保留该车，跳过成本排序层，记录原因 | 异常 |

`CONTEXT.md` 的改动见本文件末尾一节。

**一个必须点名的后果：引擎成为派车链路的硬依赖。**`RouteCostEvidenceBoundary` 的
_Avoid_ 里本就写着「可达性未知仍派车」，所以 `RouteGraphSnapshot` 整体陈旧时可达性无法确认，
**本轮不派车**。这是 fail-closed，是原词条本来就要求的语义，不是本票新加的负担——但本票把
可达性的**唯一来源**定成了引擎，所以要如实记一笔。

**它没有引入新的故障源。**引擎的输入（边表）来自 RIoT，而派车本来就要向 RIoT 下单：RIoT 不可达
则派车本来就做不成。真正新增的故障窗口只有「RIoT 可达但 imap 边表接口异常」这一种，且被 Q3 的
长 TTL 兜底覆盖。

### Q3 — 图快照的缓存与失效：**双周期 + fail-closed**

`RouteGraphSnapshot` 由两部分合成，**各自刷新**：

| 部分 | 内容 | 刷新触发 |
| --- | --- | --- |
| **设计态** | `edges/{mapId}`、`stations/{mapId}`、站点→节点定位、`mapEdgeGroup/all`、动态代价探测 | `getALLMapInfoExcludeMapJson` 的 `gmtUpdate` 变化即整体重拉；**另加长 TTL 兜底（默认 10 分钟）** |
| **运行态** | `removedEdge/{mapId}`、`removedEdgeDetail/{mapId}`、`removedStation/{mapId}` | 独立周期，**默认 10 秒** |

三条约束：

1. **TTL 兜底是必需而非冗余。**7 张图的 `gmtUpdate` 同值这一实测事实说明它很可能是批量同步戳，
   **它能否反映单图编辑未经验证**，所以不能只靠它做失效判据。
2. **重拉失败即 fail-closed。**快照进入陈旧态，成本层整体缺失、可达性无法确认（后果见 Q2），
   **不得静默继续用旧图算**——旧图算出的成本会冒充有效证据，正是 `RouteCostEvidenceBoundary` 禁的事。
3. **不得把设计态与运行态同周期刷新。**`removedEdge` 反映的是现场的运行期移除操作，它变而边表不变；
   边表 140 KB 而移除集 67 B，同周期意味着要么运行态太迟钝，要么每次都白拉 236 KB。

> **本条有一处是落笔时的细化，未经第二轮提问，请留意：**第二轮我说运行态「语义上应跟随调度节拍
> 刷新」，落地时定为**独立周期默认 10 秒**而非每个 2 秒 tick。理由是每 tick 3 次 RIoT 往返会侵蚀
> 票 03 Q7 定的每车超时预算，而 `removedEdge` 反映的是人工现场操作，秒级精度没有业务意义。
> 若你认为应当严格跟随节拍，这一条可以当场推翻，不影响其余决议。

### Q4 — `REQ-0197` 的删除半与换序半：**合并，在 348 行剖面里给一行**

两半都是完整实现，分开表述的唯一理由（一半完整、一半证据受限）已随 Round 43 消失。而且
`PlannedStopMutationBoundary` 本来就把「尚未取货且已取消的 Demand 可以移除」与「其后的未执行
停靠可在满足门禁时调整」写在同一条边界里，分开表述反与领域模型脱节。

**票 09 按一条完整实现排期，不再需要「一条需求两半两种形态」的表述口径。**

### Q5 — 「量纲是推断」这个未证明项：**失去承载，降为条件性遗留**

先厘清 Round 43 到底证明了什么：

- **已直测**：`Edge.cost` = 边的欧氏长度（403 条逐条比对，中位偏差 0.012 mm，仅 28 条 > 1 mm）。
- **未直测**：`Edge.cost` 与 `getRouteCostsBy` 的 `costs` 同量纲（段二未采）。

Q1 选计划锚后 `getRouteCostsBy` 已不在成本路径上，**未直测的那一项失去了承载**。

规格里的表述口径写死为两句：

1. `EnRoutePickupDeliveryDelay` 的现场标定值以**自建图代价单位**表达，而该单位经 Round 43 直测
   **等于毫米**——现场可以直接用尺子的量纲标定。这比票 03 Q13 定案时预期的「一个抽象代价单位」
   好得多。
2. **「两种成本能否混用」这个问题是被取消了，不是被回答了。**必须这么写：一旦将来重新引入
   `getRouteCostsBy`（例如要补 Q1 的缺口场景），**补跑 Round 43 段二重新成为前置**。
   不得表述为「量纲问题已解决」。

票 03 Q13 定的「代价单位而非时间」不变；「与基线文字的『预计到达终点时间』有出入，属实施口径
而非需求变更，`REQ-0198` Lifecycle 仍是 `active`」这一句原样继承。

### Q6 — `mapEdgeGroup` 与动态代价两项未测：**不纳入算法，作为引擎自检条件**

Round 43 的一致性证据（23/23）是**在「`mapEdgeGroup` 内容 = 当前值、动态代价 = 空」这个条件下**
取得的。条件变了，证据就不再覆盖。

因此引擎在**设计态**刷新时比对两项，越界即进入陈旧态并告警，等人重新取证：

- 动态代价（`GET /api/task/v1/route/`、`getCostUnit`）**由 `{}` 变为非空**；
- `mapEdgeGroup/all` 的**内容指纹变化**（它现在就非空，所以判据是变化而非非空）。

不取「纳入算法」：那是在没有证据的情况下猜 RIoT 的实现，正是本图 Notes 里那条教训的反面。
不取「忽略」：会让引擎在失去证据支撑之后继续给出一个看起来有效的数。

**注意 `mapEdgeGroup` 用 camelCase（`edgeId`／`gmtCreate`），与同一 RIoT 的 `edges`／`stations`
的 snake_case 不同**，自定义反序列化须按接口区分（Round 43 `execution-log.md:113-122`）。

### Q7 — 引擎在 B3 内排在哪：**先行，且可与 B2 并行**

Q1 选计划锚之后，引擎的接口面收缩成一个**纯函数**——输入 `(起站, 终站)`，输出代价或
「不可达」。它不碰 B3 的计划数据模型、不碰 B2 的车辆集合语义、不碰任何持久化。

**因此它不依赖任何架构不变量被推翻，是整条重构链上少见的、可以第一天就并行开工的大件**，
且它有自己独立的验收证据（Q8 的对照集），不必等计划形状落地才能验。

**这是排期上的真实提前量，票 09 漏掉就白白串行了。**票 02 定的重构顺序
`B2 → (B1+B4) → B3 → B5` 不变——引擎不是它的一环，它是一条旁路。

但 Q2 的后果同时给了一个**下界**：引擎必须**先于任何多车派车能力上线**，因为可达性判定是派车的
必要条件，而 B2（车辆集合语义）一旦推翻就会有多车进入候选比较。

### Q8 — 验收证据形态：**把 Round 43 的对照集固化为回归门禁**

三条按完整能力验收。Q2 把可达性权威迁到自建图之后，「凭什么信自建图」成了验收的核心，答案是
一个**可重跑的只读脚本**：在生产 RIoT 上采 N 组 `queryNearEnd`／`queryNearestStart` 对照，
自建图复现，**全中才算通过**。Round 43 的 23 组与 `runs/799-control-set-plan.json` 的确定性
生成规则就是范本。

三条边界必须写清：

1. **对照取证调 `queryNearEnd`，产品代码路径不调。**取证是为了拿 RIoT 的答案当基准；产品侧按 Q2
   已决定不依赖它。这个区分不写清，就会有人把 `queryNearEnd` 写进产品。
2. **取证脚本必须先用自建图过滤不可达候选**，否则撞 BC-ROUTE-002 的 kernel NPE
   （`NullPointerException at WorldRoute.java:293`）——Round 43 前两次执行就是这么失败的。
3. **`REQ-0198` 的顺路取货与「3 车 3 桩凑不出充电争用」同类。**3 车规模下途中追加可能整个试运行期
   都不自然发生，**不得默认「不触发即通过」**。

另需票 08 覆盖一条 Q2 派生的路径：**`RouteGraphSnapshot` 陈旧 → 本轮不派车且告警**。这是本票
新增的 fail-closed 门禁，它的证据形态只能证明「正确拒绝」。

## 三条需求的最终形态

| 需求 | 形态 | 说明 |
| --- | --- | --- |
| `REQ-0196` 执行途中受控追加 | **完整实现** | 引擎给出真实边际成本，门禁真实放行与拒绝 |
| `REQ-0198` 顺路取货按最大晚到量约束 | **完整实现** | `EnRoutePickupDeliveryDelay` = 计划锚代价增量，单位 mm；需求自带的「无法可靠计算时不得追加」在快照陈旧时生效 |
| `REQ-0197` 删除半 + 换序半 | **完整实现，合一行** | 见 Q4 |

**`证据受限实施` 在本簇清零。**票 03 原判的 fail-closed 形态**全部撤销**——票 09 与票 10 不得再
把这三条按该形态排期或表述。该词条本身仍然有效（`CONTEXT.md` 保留），只是本簇不再有它的实例。

## 票 03 的 Q2：**升级，且升级幅度大于票 14 正文的预设**

票 14 正文预设的升级是「用引擎算在途车的真实增量」，风险是「把选车路径也压在自建引擎上」。
实际定案更进一步：**选车整体从 RIoT 迁到引擎**，连档 β 原本要用的「各车→取货站」单段批量查询
也自算。

正文担心的那个风险**部分不成立**：引擎不可用时选车**不会失效**，只会失去成本排序层，按
`RouteCostEvidenceBoundary` 保留全部车辆并退到 `DeterministicDispatchTieBreak`——与档 β 下
`getRouteCostsBy` 不可用的后果**完全一样**。升级没有加重成本层的降级后果。

**真正加重的是可达性那一半**，见 Q2 的「引擎成为派车链路的硬依赖」。

票 03 Q2 的其余结论不变：零容差运行、`RouteCostEquivalenceBand` 与
`DispatchZoneVehiclePreference` 暂不建、后续层用 `DeterministicDispatchTieBreak`。
**作废的只有那条实现约束**（绕 Facade 走 `Raw` 查 `getRouteCostsBy`）。

## 路网成本引擎的边界（票 09 输入）

- **输入**：`(mapId, 起站 stationId, 终站 stationId)`。
- **输出**：代价（mm）或 `不可达`；快照陈旧时不输出任何一种。
- **不做**：不调 `queryNearEnd`／`queryNearestStart`／`getRouteCostsBy`；不解释
  `mapEdgeGroup` 约束；不解释动态代价；不持久化（进程内快照即可，重启重拉 200 ms）。
- **必须自定义反序列化**：现场是 snake_case 且是 `s_node`／`e_node`（**连下划线位置都与 Kiota 的
  `snode`／`enode` 不同**）、`is_back_edge`、`limit_v`；站点侧键名字面带点（`pos.x`、
  `enter_pos.yaw`）。Kiota 生成层不可直接使用。`mapEdgeGroup` 另按 camelCase 处理。
- **必须按有向图算**：403 条有向边 / 307 节点，403 个有序对中只有 148 个有反向边；当无向图算会错。
- **站点→节点定位用坐标投影**：`station_offset` 在 206 个站点上全为 0（废字段）；投影后垂距
  中位 0.0 mm、max 4.0 mm，且只落在 t=0（96 个）或 t=1（110 个）两端，206 站点 → 206 个互不相同
  的节点，零冲突。
- **规模与预算**：403 边 / 307 节点 / 206 站点，全源 Dijkstra 毫秒级，**不影响票 03 Q7 定的
  2 秒轮询节拍与单 worker 串行推进**。

## 对其他票据的影响

- **票 08**（验收边界）：Q8 的三条边界 + `RouteGraphSnapshot` 陈旧即停派这条 fail-closed 门禁的
  证据形态；`REQ-0198` 与充电排队同属「现场可能不自然触发」，一并定验收出口。
- **票 09**（批次与依赖）：引擎是可与 B2 并行的旁路大件（提前量），但必须先于多车派车上线（下界）；
  三条按完整实现排期，`证据受限实施` 在本簇清零；`REQ-0197` 一行不两行。
- **票 06**（协议 v2）：**无新增**。本票不改协议消息面，`legs`／`items` 上限仍是票 03 定的 9／8。
- **票 03**：Q2 升级如上；其 Q13 的代价单位口径不变但获得了「= 毫米」这个直测事实。

## `CONTEXT.md` 变更（已写回）

**新增两条**（`实施范围与顺序` 一节）：`RouteGraphSnapshot（路网图快照）`、
`StationReachability（站点可达性）`。

**修订两条**：

- `VehicleMarginalRouteCost` —— 加入计划锚语义与抵消论证，`_Avoid_` 增「以车辆物理位置为锚」。
- `RouteCostEvidenceBoundary` —— 可达性移交 `StationReachability`；把「图上不可达」（常态、
  不告警）与「成本证据缺失」（异常）拆开；补上快照陈旧即本轮不派车。

`EnRoutePickupDeliveryDelay` **不改**——它的「预计到达终点时间」是基线文字，代价单位是实施口径，
票 03 已定该出入写进最终规格而非改词典，本票不重开。

## 未证明项与遗留（如实继承）

1. **`Edge.cost` 与 `getRouteCostsBy` 的 `costs` 同量纲**——未直测，因 Q1 已失去承载；
   若将来重新引入 `getRouteCostsBy`，补跑 Round 43 段二重新成为前置。
2. **`mapEdgeGroup` 约束是否影响规划结果**——未测；按 Q6 转为引擎自检条件。
3. **动态代价非空时是否进入边权**——未测；同上。
4. **`getALLMapInfoExcludeMapJson` 的 `gmtUpdate` 能否反映单图编辑**——未测（7 图同值）；
   由 Q3 的长 TTL 兜底覆盖，不阻塞实施。
5. **`Vehicle.currentNode` 与 `Edge.s_node` 是否同 id 空间**——未测；本方案不需要它，仅在
   将来要走物理锚时才成为前置。
6. **vendored `RIoT.Sdk.Facade 0.1.0-controlserver.2` 是否含 `EdgesRequestBuilder`**——票 03 记
   vendored `RIoT.Sdk.Generated.dll` 含 `EdgesRequestBuilder` 与 `ResponseMsg_Of_List_Of_Edge`，
   但仓库 HEAD 与生产二进制不是同一 API 面。**本票已把风险权重降低**：引擎必须自定义反序列化，
   所以它需要的只是一条能发 HTTP GET 的通道，不依赖生成层的类型。
