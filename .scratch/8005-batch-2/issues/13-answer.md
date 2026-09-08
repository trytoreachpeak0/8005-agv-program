# 票 13 决议：`FP-C13` 建单前置门禁落地，硬阻断的负向证据在 L2 里

Resolved: 2026-09-08
Resolves: `13-fp-c13-catalog-availability-and-create-gate.md`

## 结论一句话

**建单这一步现在有两道判据**：目录不可用不解析站点（Order 55），RIoT 说这台车到不了那个站
就不建单（Order 96）；建单那一刻两个端点被冻结，后续目录改不了已建的单。

证据：**L1 388 passed / 0 failed**（新增 27）；**L2 七条场景全 PASS**，其中
`create-gate-unapproved` 是规格 8.6 要的**负向证据**——把 `REQ-0302` 的两个参数拿掉，服务端
照常启动而一张单都不建。`src/` 下 `queryNearEnd`／`queryNearestStart` 仍为**零命中**（架构测试
守着）。无新增 migration（`dotnet ef migrations has-pending-model-changes` 实测无变更）。

## 落在哪

| 层 | 内容 |
| --- | --- |
| `ControlServer.Domain` | `CreateGateVerdict` 新增两个成员（见下「两处自行扩了票 06 的定义」） |
| `ControlServer.Application` | `CreateGatePorts.cs` —— `IRiotRouteCostProbe` 与 `RiotRouteCost` |
| `ControlServer.Infrastructure` | `HttpRiotRouteCostProbe` —— 具名 Facade，`.Raw` 零命中 |
| `Host/Runtime/CreateGate/` | `MapStationCatalogOptions`（＋校验器）、`CatalogAvailabilityAccess`（＋`CatalogAlarmLedger`）、`PreCreateGate` |
| `Runtime/Dispatch/Criteria` | `CatalogAvailabilityCriterion`（Order 55）、`PreCreateGateCriterion`（Order 96） |
| `Program.cs` | `GET /api/runtime/catalog-availability` —— `REQ-0308` 的展示面 |
| `tools/ControlServer.FakeRiot` | `POST /api/task/v1/route/getRouteCostsBy` |

判据链现在 12 条。插入位置与 `12-answer.md` 给的指针一致，**只是多了一条**：

| Order | 判据 | 为什么在这 |
| --- | --- | --- |
| 55 | `CatalogAvailabilityCriterion` | **在站点解析（60）之前** |
| 95 | `RouteGraphReachabilityCriterion` | 票 12 |
| 96 | `PreCreateGateCriterion` | 在引擎之后（要两个源）、在 box count（100）之前 |

## 本票最要紧的三处设计

### 一、`REQ-0302` 没有开关，而「未批准」不是启动失败

引擎（票 12）有 `Enabled`，因为一套部署可以合理地还没采用它。**这道门禁不能有**：规格 8.6 把
`REQ-0302` 列为硬阻断，一个能把它关掉的开关就是那条需求禁止的那种配置，只是穿了功能的外衣。

所以「未批准」的唯一表达方式是**两个值都不配置**，而且那**不是启动失败**——`REQ-0303` 明写
「系统仍可启动并展示、诊断和重试同步」。是启动失败的是**配置了但配错**：只配一个（批准做了
一半）、最大未确认时长不大于同步周期。两者是不同的事，代码里也是两条不同的路径。

这一条只写在文档里会烂掉，所以它有两处可执行的守卫：`MapStationCatalogOptionsValidator` 的
三条测试，加 L2 的 `create-gate-unapproved`——那条场景断言服务端**起来了**、backlog 里写着
`CATALOG_PARAMETERS_NOT_APPROVED`、`JourneyRuntimes`／`OrderIntents`／`AcceptedDemands`／
`FrozenDemandStations`／`CreateGateAudit` **五张表全空**。最后一条尤其要紧：`REQ-0303` 禁的是
「为新 TransportDemand **解析**执行站点」，不是「解析完再丢掉」，所以判据必须在解析之前跑。

### 二、只比可达性，不比两个代价的数值

`06-answer.md` 末尾留了一句：「`MapEdge.CostMm` 与 `getRouteCostsBy` 同量纲仍是推断……票 13
把两个证据源放在一起比较时，它就承重了。」

**结论是不让它承重。**门禁只比较两个源对「可达」的判断：

| 图 | RIoT | 裁决 |
| --- | --- | --- |
| 说可达 | 说可达 | `Allowed` |
| 说可达 | 说不可达 | **`BlockedEvidenceConflict`** ＋ Error 级告警 |
| 没答（引擎关着） | 说不可达 | `BlockedUnreachable` |
| 任意 | 调不通 | `BlockedRouteCostUnavailable` |

两个数值差多少都不是分歧——有一条 L1 专门钉这个（RIoT 21500 mm 对图的 3 mm，仍然放行）。
Round 43 没在同一对起终点上同时取过两者，拿一个没人测过的等价关系去阻断生产，是把推断
当事实。两个数**并排写进审计**（`RiotRouteCostMm` 与 `GraphTraversalCostMm`），这才是让那条
推断日后能从真实流量里核对的做法。

「图没答」为什么不算分歧：引擎的判据在 Order 95，**它判不可达时车已经退出本轮候选了**，所以
走到 96 的候选要么带着图的代价（第二个「可以」），要么根本没被图judge过。一个源不会和自己分歧。

### 三、`REQ-0305` 的「每次尚未创建的新 move 订单」是两个调用点

条目原文是「**每次**尚未创建的新 RIoT move 订单仍须确认冻结的 mapId + stationId 存在于当前
新鲜快照并通过 RouteCost」。这条产品一趟有两个 move 订单：取货腿（建单时）与关卡腿（装载完、
安全放行之后）。只做前者等于把这条需求做了一半。

所以门禁有两个入口：判据链里的 Order 96（取货腿），和 `JourneyRuntimeEngine.GateLegAsync`
（关卡腿，在 `AwaitingDepartureSafety` 创建 `GateIntent` 之前）。关卡腿多做一件事——**核对
冻结的端点还在当前新鲜快照里**，不在就 `BlockedFrozenStationAbsent`，绝不换站、换图或按相似
名称重映射。

关卡腿**只有一个证据源**（不问自建图）。这不是更弱的门禁，是更窄的问题：图在选车阶段的作用是
把候选站点互相比较，而这里没有可比的——目的地在建单那一刻就定死了。

## 几处自行定案

1. **目录修订从内容哈希推导，不是计数器。**`RiotMapStationCatalogSnapshot.ContentSha256` 前
   8 字节取非负 long。`REQ-0305` 冻结「当时的目录修订」是为了让后来的刷新能被认出是另一份
   目录——内容推导的号正好做到这件事（同一份目录两次读到同一个号，任何改动换一个号），而且
   **事后能从证据重算**，计数器不能。它不单调，代码里也没有任何地方把它当序。
2. **审计按裁决去重。**`REQ-0308` 禁止「为每轮轮询或每个等待任务重复制造告警」，而门禁每轮
   为每个开放需求跑一次。同一裁决重复不写行，变化才写——`ReadLastVerdictAsync` 是为这个加的。
3. **告警日志的去重放在一个单例 `CatalogAlarmLedger` 里。**`CatalogAvailabilityAccess` 是
   scoped，每轮一个新实例，成员变量记不住上一轮说过什么。持久化的那半（一张图一行、原地更新）
   由票 06 的表天然满足；日志这半没有，1 Hz 的轮询会把同一句话写几万遍。
4. **`BuildIncompatible` 不看新鲜度，直接阻断。**`REQ-0303`：「错误环境、未批准 build 或接口
   契约不兼容产生同一业务门禁」。一份三秒前的快照仍然可能是关于另一套系统的。
5. **窗口内的刷新失败不阻断，但状态行上留着失败原因。**`REQ-0302` 明文允许继续用最后已知有效
   快照，条件是「明确标记」且「不得把失败描述为已经取得最新 RIoT 目录」。标记就是那一行的
   `State` ＋ `LastFailureReason`，加 `CatalogAvailability.DegradedReason`。
6. **假 RIoT 的 `getRouteCostsBy` 不从自己的边表算最短路，按站点查表答。**门禁只比可达性、
   不比数值，算出来的数会显得比它实际承载的意义更多；而且**查表是让两个源在 L2 里能分歧的
   唯一办法**——算出来的代价与自建图必然一致，分歧那条路在 L2 就不可测了。

## 两处自行扩了票 06 的定义

票 06 说「`Ports.cs` 一次定齐四条轨需要的存取端口」，票 13 各加了一处，都记在这里：

1. **`ICatalogAvailabilityStore.ReadLastVerdictAsync`**（`Ports.cs`，FP-C13 段内）。审计去重要
   读「当前站着的裁决」，票 06 没有这个读法。它落在 Infrastructure 时踩了一个坑：**SQLite 不能
   `ORDER BY` `DateTimeOffset`**，所以过滤在库里做、排序在内存里做——去重本身保证了行数很少。
2. **`CreateGateVerdict` 新增 `BlockedRouteCostUnavailable` 与 `BlockedFrozenStationAbsent`。**
   前者是「调不通」，它绝不能记成 `BlockedUnreachable`——那会把一句没人说过的、关于地图的断言
   写进审计。后者是 `REQ-0308` 的任务级 `StructuralDispatchBlock`。枚举以字符串存储，**不产生
   migration**（已用 `has-pending-model-changes` 实测）。

## 一处票据没预料到的：判据不能只加在链尾

票据说「门禁以判据文件的形式加进票 05 的判据链」，读起来像加一条。实际是**两条，而且其中一条
必须在既有判据的中间**：`REQ-0303` 禁的是解析动作本身，所以目录判据要在 `StationResolution`
（60）之前。这不影响「注册表一行」的成立——Order 写在判据自己身上，注册顺序不改变链的顺序。

## 一处顺带修正的数字

`LargeCatalogBatchesBacklogPersistenceBeforeAcceptingEligibleJourney` 的 SaveChanges 预算从
10 放宽到 13，并在断言旁写清了为什么。FP-C13 给**接单的那一轮**加了正好三次写（目录确认、
走到门禁的那一个需求的裁决、端点冻结），**每个候选零次**——251 个候选仍然是常数次写，这条
测试要钉的性质没有变。

## 验收清单

- [x] 新鲜度按最近一次**完整确认**计算，不按最近一次尝试
      （`FreshnessRunsFromTheLastCompleteConfirmationNotTheLastAttempt`，＋运行时那条
      `TheCatalogIsConfirmedOnAWholeReadAndOnlyOnAWholeRead`）
- [x] 两个参数从配置读入，且启动时校验「最大未确认时长 > 同步周期」，不满足即拒绝启动
      （另加：只配一个也拒绝启动）
- [x] 未配置已批准值时，依赖 Map/Station 的业务确实不启用——**负向测试有两级**：L1 的
      `WithoutApprovedValuesEverythingMapAndStationDependentIsBlocked` 与
      `AnUncommissionedCatalogCreatesNothingAtAll`，L2 的 `create-gate-unapproved`
- [x] `TransportDemand` 建单时冻结已解析站点，后续目录刷新不重写已建任务的端点
      （`AcceptingADemandFreezesBothEndpointsAndALaterRenameDoesNotRewriteThem`，＋ L2-CG-04/05/06）
- [x] 目录级状态与任务级阻断是两套状态，各自有独立的产生条件与解除条件
      （`ATaskLevelBlockLeavesTheCatalogStateAlone` 与 `ACatalogLevelFailureProducesNoGateAuditAtAll`
      两个方向各一条）
- [x] 建单前置调 `getRouteCostsBy` 确认该车到该站可达，不可达即拒绝建单
      （`AnUnreachablePickupIsRefusedACreateAndSaysWhy`，运行时级）
- [x] 两个证据源分歧时阻断建单并告警，不静默取其一
      （`WhenTheTwoSourcesDisagreeTheCreateIsBlockedAndNeitherSourceWins`）
- [x] `queryNearEnd`／`queryNearestStart` 仍为零命中（`TheNearStationQueriesAreStillAZeroHitInProductCode`
      扫 `src/` 全部 `.cs`，注释除外）
- [x] L1 新增覆盖：新鲜度边界（三点参数化：299／300／301 秒）、冻结不被重写、两类失败分层、
      分歧阻断各有测试 —— **新增 27 条，388 passed**
- [x] 无新增 migration（`has-pending-model-changes` 回答 no changes）

L2 证据在 `8005-agv-control-server` 的
`evidence/l2/20260908-ticket13-{create-gate-002,create-gate-unapproved-001,normal-load-001,route-graph-engine-001,session-established-while-moving-001,load-result-requires-recovery-001,three-synthetic-peers-001}`。
（`create-gate-001` 是加展示面断言之前的那次跑，一并留着，证据不覆盖。）

## 与规格的冲突

无。`REQ-0302` 正文里有一句票据没引的话，实现按正文走：「暂时刷新失败但仍处于允许时长内时，
可以明确标记使用最后已知有效快照，并继续由实时 RouteCost 完成建单前可达性校验」。票据的验收
清单只说了新鲜度边界，照字面做会把窗口内的刷新失败也阻断掉，比条目严——所以按条目实现，并为
它加了测试（见自行定案第 5 条）。

## 给下游票的指针

**票 09（B2 多车）**——两条判据都已经是按车问的：门禁读 `evaluation.Vehicle.VehicleKey`，
目录判据与车无关。多车下不用改，换掉 `DispatchVehicleKeys()` 即可。注意 `CreateGateAuditRow`
的 `AgvId` 目前取自 `JourneyRuntimeOptions.AgvId`（单车配置），**多车时要改成本轮那台车的
AgvId**——审计行上的车必须是被判定的那台。

**票 11（故障隔离）**——`CreateGateVerdict` 的四个 Blocked 是**任务级**阻断，与车辆故障的两级
模型是不同的轴：一个说「这个需求现在不能建单」，另一个说「这台车不能接活」。同一台车可以
同时处在 `None` 故障级与一堆任务级阻断里。

**票 18（轨 B 出口）**——门禁的 L2 场景是 `create-gate` 与 `create-gate-unapproved`。后者必须
在出口证据里，规格 8.6 的负向证据要求指的就是它；编排器已支持 `CatalogApproved = $false`。
注意**两个已批准值现在是每条 L2 场景的基线环境**（`MapStationCatalog__*`），新写场景不必管。

**票 17（`FP-IS-00`～`07` 重证）**——服务端多了一个 HTTP 端点
`GET /api/runtime/catalog-availability`。它不上协议线、不影响任何 `vectorId`，但重证时如果有
端点清单要更新它。

## 遗留

- 改动提交在本地 worktree：`8005-agv-control-server` 的 `1964874` 与 `09c7ff9`，未推送。
- **假 RIoT 的 `getRouteCostsBy` 是按站点查表答的，不区分 deviceKey。**多车场景要让两台车对
  同一个站得到不同答案时，键要扩成 `"{mapId}:{stationId}:{deviceKey}"`。现在没有场景需要。
- `CatalogAlarmLedger` 是进程内的，重启后第一条重复日志会再写一次。持久化那半（表）不受影响。
