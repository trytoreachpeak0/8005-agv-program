# 票 05 决议：派车决策链已拆开，行为一字未变

Resolved: 2026-09-07
Resolves: `05-dispatch-decision-chain-prefactor.md`

## 结论一句话

**`DiscoverAndAcceptAsync` 那 255 行拆成了按车迭代骨架、10 条判据的 fail-closed 链、一个排序
器。** 票 09／12／13 从此各加一个判据文件 ＋ 注册表一行，**冲突面收缩到一行**。

行为等价的证据：**L1 325 passed / 0 failed**，与重构前逐条一致（同一个 325，没有测试被删改
断言）；**L2 `normal-load` 连续三次 PASS**，另两条合成场景各一次 PASS。

## 落在哪

主循环**不在 Application 层，在 Host 层**：`src/ControlServer.Host/Runtime/JourneyRuntimeEngine.cs`
的 `DiscoverAndAcceptAsync`。拆出来的东西在新目录 `src/ControlServer.Host/Runtime/Dispatch/`：

| 文件 | 内容 |
| --- | --- |
| `DispatchAdmission.cs` | 判据契约、评估上下文、链、排序器接口与当前实现 |
| `Criteria/DispatchAdmissionCriteria.cs` | **注册表——唯一装配点**，含 DI 扩展 |
| `Criteria/*.cs`（9 个） | 10 条判据，每条一个文件 |

`JourneyRuntimeEngine` 从 1379 行降到 1261 行，新目录 12 个文件共 770 行。

判据按运行顺序：

| Order | 判据 | 阻断原因 |
| --- | --- | --- |
| 10 | `AlreadyAcceptedCriterion` | `DEMAND_ALREADY_ACCEPTED` |
| 20 | `WorkTypeScopeCriterion` | `OUT_OF_SCOPE_WORK_TYPE` |
| 30 | `RequiredMesFactsCriterion` | `REQUIRED_MES_FACT_MISSING` |
| 40 | `AreaScopeCriterion` | `OUT_OF_SCOPE_AREA` |
| 50 | `AreaEqpUniqueCriterion` | `AREA_EQP_NOT_UNIQUE` |
| 60 | `StationResolutionCriterion` | 解析器自己的 reason code／`DISPATCH_ZONE_VEHICLE_ADMISSION_MISSING`／`ROUTE_EVIDENCE_MISSING` |
| 70 | `PackageCapacityCriterion` | `PACKAGE_CAPACITY_NOT_UNIQUE` |
| 80 | `VehicleDynamicFactsCriterion` | 10 个各自具名的原因 |
| 90 | `StationTaskTypeAdmissionCriterion` | `TASK_TYPE_NOT_ALLOWED_AT_STATION` |
| 100 | `SlotCapacityCriterion` | `SUBLOT_BOX_COUNT_UNAVAILABLE`／`EXPECTED_BASKET_COUNT_OUT_OF_RANGE`／`SLOT_CAPACITY_TEMPORARILY_UNAVAILABLE` |

**一处与票据不同**：票据说「每条准入判据是一个独立类、独立文件」，我把 `ValidateStaticRoute`
的两条（调度区准入、路线证据）**留在了 `StationResolutionCriterion` 里**而没有另立两个文件。
它们校验的是这条判据刚刚构造出来的那个 route 的属性，拆出去意味着下一条判据重新推导上一条
已经知道的东西。

## 两个规格符号在代码里不存在

**这是本票最需要记下来的事**，而且它是第二次出现——票 06 已经报过一个。

| 规格／票据里的名字 | 代码里的实际东西 |
| --- | --- |
| `DispatchUniquenessGuard` | `VehicleDispatchLeases` 上的唯一索引 `HasIndex(VehicleKey).IsUnique().HasFilter("ReleasedAt IS NULL")`，加主循环里那句 `AnyAsync(row => row.VehicleKey == ... && row.ReleasedAt == null)` |
| `DeterministicDispatchTieBreak` | 主循环里那三级排序 `OrderBy(FirstSeenAt).ThenBy(CreatedAt).ThenBy(DemandId, Ordinal)` |

两个都是**全仓零命中**——`src/`、`tests/`、`.md` 全部搜不到，只活在完整产品规格与那批票据
答案的文本里。

票 05 说「排序器：当前实现是既有的 `DeterministicDispatchTieBreak`，原样搬过来即可」。我按
**它指的那段实际代码**原样搬进了 `FirstSeenDispatchCandidateRanker`，语义一字未动。

**建议**：写票 09／12 时不要照着这两个名字写验收，先确认它指的是哪段代码。规格描述的心智
模型与代码的结构对得上，**但符号名对不上**。

## 一处票据没预料到的结构：判据不是独立谓词

票 05 给判据定的契约是「给定候选与快照事实，返回通过或一条阻断原因」。实际那 255 行**不是
一组独立谓词**，是一条**带累积状态的管线**：站点解析产出 `route`，包装容量判据冻结
`packageCapacity`，槽位判据据此算出 `expectedBasketCount` 并选出 `targetSlots`——后面的判据要
用前面的产物。

所以契约多了一个可变的评估上下文 `DispatchCandidateEvaluation`：判据读它、也往里写自己解析
出的事实。这不是把状态偷渡进纯函数——链是短路的，**一条判据只会在它依赖的东西全部确立之后
才运行**，这个不变量由顺序保证，也写进了契约的文档注释。

## 按车迭代：接缝在哪

```csharp
private IReadOnlyList<string> DispatchVehicleKeys() => [runtimeOptions.VehicleKey];
```

**这一行就是票 09 要换掉的全部。**车辆集合当前来自现有单车配置，`N=1` 时执行路径与重构前
完全等价：原来在 `foreach candidate` 之前读一次 onboard 与 vehicle，现在在按车循环内读一次
——单车下就是同一次。

原来 `eligible.Count == 0` 与「车已被占用」是整个方法 `return`，现在是这台车这一轮结束
（`DispatchForVehicleAsync` 返回），下一台车继续。单车下两者等价。

## 两处顺带修正了本可以漂移的东西

1. **最终动态事实复检不再复述十条判断。**原来 `FinalDynamicFactsReadyAsync` 调
   `ValidateDynamicFacts`，两者共用同一个私有方法；拆开后如果各写各的，判据链与建单前复检就
   可能分叉。现在复检调用 `VehicleDynamicFactsCriterion.Evaluate` 这个静态方法，**两者从此不
   可能不一致**。
2. **车辆绑定校验从 `runtimeOptions.VehicleKey` 换成本轮正在决策的那台车**
   （`DispatchVehicleFacts.VehicleKey`）。单车下是同一个字符串，所以行为不变；多车下这正是
   「一台车的观测不能放行另一台」的那道闸。

## 验收清单

- [x] 主循环按车迭代，车辆集合当前来自现有单车配置，`N=1` 行为与重构前等价
- [x] 准入判据全部搬进判据链，每条一个文件（一处例外见上），注册表是唯一装配点
- [x] 排序器独立，当前行为仍是既有的确定性 tie-break（三级，含 `DemandId` 兜底）
- [x] 判据链是 fail-closed：任一判据不通过即阻断本轮，阻断原因可追到具体判据
      （每条判据返回自己的 reason code，写进 `JourneyBacklog`）
- [x] 新接口在独立新文件里，`Ports.cs` **零改动**（`git diff` 实测为空）
- [x] L1 全绿且无测试被删改语义——**325 passed，与重构前同一个数字**，只改了测试里的构造点
- [x] L2 既有场景连续三次通过——`normal-load` ×3 全 PASS，另两条合成场景各一次 PASS
- [x] 无新增数据库表、无新增 migration（实测 `git status` 里没有 migration 文件）

L2 证据在 `evidence/l2/20260907-ticket05-normal-load-{001,002,003}` 与
`20260907-ticket05-{session-established-while-moving,load-result-requires-recovery}-001`。

## 给下游票的指针

**票 09（B2 多车）**——换掉 `DispatchVehicleKeys()` 那一行即可，循环骨架不用动。两条车辆过滤
判据（`agvId × taskType`、区→车）各写一个判据文件、注册表加一行，用票 06 的
`IVehicleDispatchPolicyStore`。**每车超时预算**要包住 `DispatchForVehicleAsync` 的调用，那是
「一台车卡住不拖垮其余车」的位置。

**票 12（引擎）**——可达性判据与成本排序器是两件事，分别对应链和 `IDispatchCandidateRanker`。
排序器换实现时链不用动，这正是把它们分开的理由。注意 `REQ-0207`：不可达车辆退出本轮候选是
**判据**（阻断），不是排序时排到后面。

**票 13（`FP-C13`）**——建单前置 `RouteCost` 门禁是一条判据，位置应在
`StationResolutionCriterion` 之后（它要 route）、`SlotCapacityCriterion` 之前（不必为一个到不
了的站去读 box count）。Order 取 95 即可插进现有序列。

## 遗留

- 改动只提交在本地 worktree（`b2e5237`），未推送。
