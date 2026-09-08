# 票 06 决议：轨 B 持久化地基已落地，15 张表在一个 migration 里

Resolved: 2026-09-07
Resolves: `06-track-b-persistence-foundation.md`

## 结论一句话

**四条能力轨的全部持久化结构在一个 migration 里落齐**（15 张表、2 个新列、10 个索引），端口
在 `Ports.cs` 里一次定齐，**票 09／10／11／12／13 从此零 migration、零 `Ports.cs` 改动**。

证据：**L1 325 passed / 0 failed**（原 308 ＋ 新增 17），**三条 L2 合成场景全 PASS**，行为断言
一条未改。

## 落了什么

| 能力轨 | 表 |
| --- | --- |
| B2 多车（票 09） | `VehicleTaskTypeAdmissions`、`DispatchZoneVehicles`、`VehicleDispatchBudgets`，＋ `OrderIntents` 上的占用唯一性 |
| 引擎（票 12） | `RouteGraphSnapshots`、`RouteGraphEdges`、`RouteGraphStations`、`RouteGraphRemovedEdges`、`RouteGraphRemovedStations`、`RouteGraphEdgeGroups` |
| `FP-C11`（票 10／11） | `VehicleFaultStates`、`FaultedVehicleCargo`、`RiotOrderCommandAudit` |
| `FP-C13`（票 13） | `MapStationCatalogStates`、`FrozenDemandStations`、`CreateGateAudit` |

代码落在三个新文件 ＋ 两处接线，`DbContext` 只多了 15 个 `DbSet` 与一行
`Batch2CapabilityModel.Configure(modelBuilder)`：

- `src/ControlServer.Domain/Batch2CapabilityEnums.cs` — 五个跨层枚举
- `src/ControlServer.Infrastructure/Persistence/Batch2CapabilityRows.cs` — 实体与模型配置
- `src/ControlServer.Infrastructure/Persistence/Batch2CapabilityStores.cs` — 五个 Store ＋ 边组指纹
- `src/ControlServer.Application/Ports.cs` — 五个端口与它们的 DTO（263 行 → 661 行）
- `tests/ControlServer.Tests/Batch2CapabilityStoresTests.cs` — 17 条 L1

**只有结构、端口与存取实现。**没有刷新循环、没有陈旧判定、没有准入规则、没有升级判据——那些
在各轨自己的票里。

## 三处必须记下来的事

### 一、`DispatchUniquenessGuard` 不存在

票 06 与票 09 的验收都写着「`DispatchUniquenessGuard` 源码零改动且其测试仍绿」，规格 5.1 也
写着「下移之后 `DispatchUniquenessGuard` 一字不改仍成立」。

**它在 `8005-agv-control-server` 里搜不到**——`src/`、`tests/`、全仓 `.cs` 与 `.md` 全部零命中。
整个工作区里它只出现在完整产品规格与那批票据答案的文本里，**从来没有对应的代码**。

所以这条验收无从执行：既没有源码可保持不变，也没有「其测试」可保持绿。**这不阻塞落地**，因为
它想保护的不变量是真实存在的，只是由别的东西承载：`VehicleDispatchLeaseRow` 上的
`HasIndex(VehicleKey).IsUnique().HasFilter("ReleasedAt IS NULL")`——一台车同时只能持有一个未
释放的 lease。

**建议**：把票 09 的那条验收改写为「lease 表的唯一索引与 `VehicleDispatchLeaseRow` 的用法零
改动，其现有测试仍绿」，或者在写票 09 时确认那个名字指的到底是什么。**不要照着一个不存在的
符号写验收。**

### 二、唯一性下移的实际形态与规格 5.1 有一处不同，是有意的

规格说「唯一性从 lease 表下移到 `OrderIntents`」。直译的做法是在 `OrderIntents` 上加
`HasIndex(VehicleKey).IsUnique()`，**那样 migration 当场就会失败**：`OrderIntents` 保留历史行，
同一台车早已出现在很多行上。

实际形态：

```csharp
modelBuilder.Entity<OrderIntentRow>()
    .HasIndex(row => row.VehicleKey)
    .IsUnique()
    .HasFilter("VehicleOccupancyClaimedAt IS NOT NULL AND VehicleOccupancyReleasedAt IS NULL");
```

配两个新列 `VehicleOccupancyClaimedAt` 与 `VehicleOccupancyReleasedAt`。两个后果：

1. **现在没有任何代码写 `ClaimedAt`，所以每一行都落在索引之外，行为一字未变**——正是票 06
   自己要求的「无业务行为变更」。有一条 L1 专门证明这点：三条同车 `OrderIntent` 共存不冲突。
2. **票 09 只要开始写这两个时刻，约束就自然生效，不需要再改 schema。**端口
   `TryClaimVehicleOccupancyAsync` 已经就位，靠唯一索引判定而不是读后写。

**lease 表自己的唯一索引保留不动。**删掉它会构成本批次承诺不会有的行为变更，而两者并不冲突：
lease 是一个 Demand 的占用，occupancy 是一台车的在途订单。

### 三、票据说「现有 28 张表」，实测 29 张

落地前 `ControlServerDbContext` 有 **29** 个 `DbSet`，不是 28。落地后 44。这不影响任何判断，
但下一个人按 28 去核对会以为少了一张。

## 几处自行定案

规格没规定，按「设计细节自行定案」处理：

1. **边组的主键是 `(MapId, GroupName, EdgeId)` 而不是 `(GroupName, EdgeId)`。**Round 43 实测
   一个组名可以跨多张地图——「老厂电梯」同时属于 map14 与 map19——所以组名不能单独标识一个组。
2. **新建的路网快照头默认是 stale**（`StaleReason = "SNAPSHOT_NEVER_REFRESHED"`）。「没有快照」
   绝不能读成「一张可用的空图」，而引擎是 fail-closed 的硬依赖。
3. **新建的目录状态默认不是 `Fresh`**（`RefreshFailed` ＋ `CATALOG_NEVER_CONFIRMED`）。同一个
   理由：`REQ-0302` 把「没有已批准且已确认的目录」定为硬阻断，初始状态不能读起来像可用。
4. **`MarkStaleAsync` 第一个原因保留 `StaleSince`。**第二个触发只更新原因不重置时钟——否则
   一个不断被重新触发的陈旧快照永远显得「刚刚才陈旧」。
5. **`RecordFailureAsync` 不碰 `LastCompleteConfirmationAt`。**`REQ-0302` 的新鲜度按最近一次
   **完整确认**算，失败的尝试不是确认，不能延长新鲜度。有 L1 覆盖。
6. **边组指纹用长度前缀而不是分隔符。**组名可以包含任何人能打出来的字符，任何分隔符都可能出现
   在字段内部，让两份不同的成员关系规范化成同一个串；长度前缀不会。
7. **故障事实的 `FaultGeneration` 是并发令牌，带陈旧 generation 的写入直接抛。**一次
   episode 的证据不能贴到另一次的故障上。有 L1 覆盖。

## 验收清单

- [x] 四条能力轨的全部新表在**一个** migration 里，模型快照一次更新
      （`20260907133250_Batch2CapabilityFoundation`：15 张表、2 列、10 索引）
- [~] 唯一性约束下移到 `OrderIntents` ✅；`DispatchUniquenessGuard` 源码零改动且其测试仍绿
      **无法执行**——那个符号不存在，见上文第一条
- [x] `Ports.cs` 一次定齐四条轨需要的存取端口，签名不留半成品
- [x] 存取实现有 L1 覆盖：15 张新表每张至少一条写入与读回
- [x] migration 可正向应用到现有数据库，且现有表的数据不丢——有一条测试先迁到
      `ManualChargingReturnToService`、插入两条同车 `OrderIntent`、再迁到最新，两条都还在
- [x] 无业务行为变更：**L1 325 passed / 0 failed**，**L2 三条合成场景全 PASS**，行为断言一条未改

L2 证据在 `8005-agv-control-server` 的
`evidence/l2/20260907-ticket06-{normal-load,session-established-while-moving,load-result-requires-recovery}-001`。
真装置的三条场景需要真车与 Modbus IO，不在本票范围内。

## 给下游票的指针

**票 09（B2 多车）**——`IVehicleDispatchPolicyStore` 就位。`ReadPolicyAsync` 一次读全策略（按轮
读一次，一轮内配置一致）。三处 fail-closed 是构造性的：车不在列表里、任务类型不在允许集里、
区不在 `ZoneVehicles` 里，都是「不允许」，没有宽松的默认可退。占用约束的开关就是写
`TryClaimVehicleOccupancyAsync`／`ReleaseVehicleOccupancyAsync`。

**票 10（命令面）**——`IRiotOrderCommandAuditStore.ArmAttemptAsync` 在**发出之前**调用：一条停在
`Pending` 的记录正是「可能发出去了但不知道结果」这个状态。`ReadAttemptsAsync` 让「调了一次还是
三次」可判定，唯一索引是 `(CommandType, TargetUpperId, AttemptNumber)`——重试是新的 attempt，
绝不是覆盖。

**票 11（故障隔离）**——两级模型的 generation 语义已定：从 `None` 进入开新 generation，级内升级
保持同一个，所以货物绑定与命令审计始终挂在同一次 episode 上。`StopProven` 只存结论与时刻，
**组合证据的规则（`REQ-0247`）由票 11 自己写**——存储层不替它判。

**票 12（引擎）**——`ReadStateAsync` 把设计态与运行态一次读出，调用方不会混周期。
`ReplaceDesignStateAsync` 是整体替换并返回新 revision：边表是快照不是日志，半张图读起来是一条
错误的最短路而不是一次可见的失败。**注意 `EdgeGroupFingerprint` 为空串表示「没有边组」，而
`EdgeGroupRefreshedAt` 为 null 才表示「没取过」**——map25 当前正是前者，陈旧判定必须能区分。

**票 13（`FP-C13`）**——`FreezeDemandStationsAsync` 幂等，但**改写已冻结的端点会抛**
`InvalidOperationException`：`REQ-0305` 不允许后续目录重写已建任务的端点，静默改掉一个任务的
目的地比报错糟糕得多。`CreateGateAuditRow` 里两个证据源分别具名（`RiotRouteCostMm` 与
`GraphTraversalCostMm`），**自建图的值在任何地方都不叫 RouteCost**——`REQ-0207` 与 `CP-0001`
修订文末句。

## 遗留

- `8005-agv-control-server` 的改动只提交在本地 worktree（`f5d90ed`、`2331dc8`），未推送。
