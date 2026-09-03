# 票 03 决议：多车并发、车辆占用与 Worklist 执行模型的重做范围

Status: closed
Resolved: 2026-09-03
批准人: 用户（Zhengyu Shao），三轮共 11 问，10 问按推荐值、Q9 改判为档 ii。

## 一句话结论

完整产品把选择与分配核心重做到 **B2 全开 + B3 档 2 + B5 幅度 1**：多车真实并发（3 车可配置、
按 RIoT 真实路径成本选车）、一车可在**首次派车时**组多 Demand 计划（途中追加与成本换序建门禁
但受 RIoT 能力不足恒拒）、车载只推翻「选择」而保留「不发现、不绑定」。本票 16 条全部有归属，
**9 条重构、7 条增量**，无一条延后到本图之外。

另外本票问出了一个超出自身范围的范围决策：**完整产品要执行全部六类 MES 运输任务，不止
`WIRE_TO_GATE` 一类**（Q9 = 档 ii）。它牵动的条目不在 62 条里而在 186 条「批次 0 已覆盖」里，
已拆出为**票 13**。

## 决定本票档位的外部事实：RIoT 给不了什么

三个 `Explore` 子 agent 分别勘察了 ControlServer 分配核心、计划形状与协议契约、RIoT SDK。
**档位边界不是主观选择，是 RIoT API 面决定的。**

| 查询 | 能力 | 证据 |
| --- | --- | --- |
| 车当前位置 → 某站的数值成本 | **能**，`costs` 单位 mm，`-1` = 不可达 | `riot-sdk` `csharp/RIoT.Sdk.Facade/TaskClient.cs:52`；`csharp/RIoT.Sdk.Core/RouteCost.cs:3-10` |
| 一次查多台车到同一站 | **协议支持**（`deviceKeys` 是数组），Facade 硬编码单元素 | `TaskClient.cs:65`（`DeviceKeys = [deviceKey]`）；逃逸口 `TaskClient.cs:244` |
| **站 A → 站 B 的成本数值** | **不能**。`getRouteCostsBy` 入参只有 `mapId`/`stationId`/`deviceKeys`，**无起点字段**，起点恒为车的当前位置 | `riot-sdk` `specs/task.json` 的「申请车辆列表到达站点代价」 |
| 候选站里挑最近的一个 | 能，但**只回 stationId、不回数值**；纯拓扑，与车无关 | `TaskClient.cs:93`（`QueryNearestEndAsync`）、`:131`（`QueryNearestStartAsync`），返回 `Task<int>` |
| 预计到达**时间** | **不存在**。全量 schema 扫描 `Eta`/`ETA`/`Duration`/「预计时间」零命中 | `riot-sdk` `specs/task.json` |
| 成本可加性 | **无任何说明**；且有动态代价因子 `traffic`/`obstacles`/`orderHang`/`doAction`/`emergencyStop` | `specs/task.json` 的 `CostUnit.costFactor` |

由此得到三条推论，它们划出了 B3 的档位：

**推论一 —— 途中追加做不了。**`REQ-0198` 把 `EnRoutePickupDeliveryDelay` 定义为「对任一既有
Demand **预计到达终点时间**造成的最大增量」。RIoT 连站→站的**距离**都查不到，**时间**更没有。
而该条原文自带出口：**「任一增量无法可靠计算时不得追加」**。所以 `REQ-0196` 实现出来的运行时
行为恒为「不追加」——完全合规，零价值。`REQ-0197` 的换序半同理（其前提也是「满足延迟保护」）。

**推论二 —— 首次组多 Demand 计划做得了。**站点顺序可用 `queryNearEnd` 贪心最近邻（纯拓扑，
不需数值）；`REQ-0195` 的分区连续性是纯标签序列检查；`REQ-0197` 的删除半是纯业务规则。而
WIRE_TO_GATE 的**终点固定是关卡**（`appsettings.json:53` `gateStationId` 为「关卡」），多 Demand
只有起点不同，进一步简化排序。

**推论三 —— 选车成本可算且精确。**同一个 Demand 对所有候选车而言 pickup→gate 段是常量，
车间比较时抵消，于是精确归约为「各车 → 取货站」单段——正好是 `getRouteCostsBy` 一次批量调用
的能力。注意这个归约**只在一车至多一个活跃 Demand 或多 Demand 计划首站相同时成立**；在途车
的边际成本仍然算不出来，那正是推论一。

## 逐问决议

### Q1 — 一车同时承载多个 Demand：**档 2**

首次派车时可组多 Demand 计划。`REQ-0189`、`REQ-0195` **完整实现**；`REQ-0196`、`REQ-0197`
的换序半、`REQ-0198` **以 fail-closed 形态实施**——门禁与代码路径建好，因证据不足恒走拒绝分支，
RIoT 将来补上站→站成本即自动生效，无需改代码。

不选档 1（不做多 Demand）的原因：worklist 会恒为单元素，B5 随之失去意义，`FP-C3` 6 条一并落空。
不选档 3（推动 RIoT 补接口）的原因：前置是外部团队的接口，本图不该把批次序列挂在它上面。

**代价必须写进规格**：验收时 `REQ-0196` 与 `REQ-0198` 只能证明「门禁正确拒绝」，无法证明
「正确追加」。这与票 08 已知的「3 车 3 桩凑不出充电争用」是同类问题，证据形态归票 08 判，
**不得默认「不触发即通过」**。

### Q2 — 多车选车规则：**档 β**

引入 `getRouteCostsBy` 批量查「各候选车 → 取货站」作为主排序层，**零容差**运行
（`REQ-0206` 明文「未批准非零容差时采用零容差，不阻断派车」），后续层用
`DeterministicDispatchTieBreak`。`RouteCostEquivalenceBand` 与 `DispatchZoneVehiclePreference`
**暂不建**——两者都要「现场批准值」，3 车规模下收益极小。

**实现约束**：必须绕过 Facade 走 `Raw`（`TaskClient.cs:244`），因为 Facade 把 `deviceKeys`
写死成单元素（`TaskClient.cs:65`）；逐车调用会让每个选车轮次的 RIoT 往返数随车数线性增长。

当前基线是**一层都没有**：排序键只有 `FirstSeenAt` → `Snapshot.CreatedAt` → `DemandId`，
无任何车辆维度（`ControlServer.Host/Runtime/JourneyRuntimeEngine.cs:297-301`）。

### Q3 — 防饥饿（`REQ-0203`）：**实施机制、阈值留空**

建等待年龄计算、按 `DispatchZone` 的阈值配置位与升级排序层；阈值不填，按 `REQ-0203` 原文
「未批准阈值时继续累计等待年龄，但不执行跨任务类型升级」运行。标定采样放到批次 1 落地后的
现场运行期，**不阻塞实施、不进批次依赖**。

这条需求自带「未批准时的行为」，所以「机制已实施 + 阈值未批准」是合规终态而非半成品。

当前基线：`JourneyBacklogRow.FirstSeenAt` 首见时写入、此后**永不更新**
（`JourneyRuntimeEngine.cs:1105-1116` 新建分支写入，`:1118-1127` 更新分支不碰它），
只作排序首键。全仓**无任何时间型升级代码**，无被注释或开关关闭的痕迹，**无等待年龄阈值配置项**。

### Q4 — 共晶排除区（`REQ-0185`）：**复用 `AdmissionPolicy` 版本化机制，部署期配置**

把 `TransportExecutionExcludedArea` 做成同一策略版本里的一张表，改动经既有的
`AdmissionPolicyState` + `AdmissionPolicyAudit` + `admissionPolicyVersion` 与
`admissionPolicyDeploymentId` 路径，**不建新治理面**。

**运行期能否由管理员在线修改，归票 05 判**——那属权限与配置生效治理，本票只定「用哪套机制承载」。

### Q5 — N 车配置形态：**甲（`vehicles` 数组）**

`JourneyRuntime` 段改成 `vehicles` 数组，每车带自己的 `agvId`、`vehicleKey`、
`agvLifecycleGeneration`、`minimumBatteryPercent`、`allowedWorkTypes`、`allowedDispatchZones`，
仍是部署期配置文件。不选「车辆准入进数据库表」，因为 `REQ-0259` 要求的是**车辆生命周期**门禁
（整车达 `SlotConfigurationReadiness` 才取得业务就绪），不是准入表的动态性；3 车规模下为一年
动不了几次的配置建治理面不划算。

### Q6 — B5 推翻 I5 的幅度：**幅度 1，只推翻 select**

`NEVER_DISCOVER_SELECT_OR_BIND_DEMAND` 是三个动词的合取。`WORKLIST_SELECTION` 只需要
**select**：清单仍由服务端下发（不 discover），绑定仍由服务端按 `REQ-0218` 以最新
`worklistRevision` 复核后决定（不 bind）。

**关键认识：这不是新范式。**现有的 `SublotSubmitted` 就是「车载发起、服务端复核」——车载扫码
提交一个 SUBLOT，服务端裁决。选任务是它的姊妹消息，把「提交扫到的 SUBLOT」换成「提交选中的
DemandId」，结构同构。而 `REQ-0216`（操作员权限与核验）与 `REQ-0218`（服务端最终门禁）
**都已在批次 0**，安全链现成。

不选幅度 2（select + bind）：会让已在批次 0 的 `REQ-0218` 失效。
不选幅度 3（三个全推翻）：违反 `docs/adr/cross/` 已接受的「服务端任务与仓位集决策权」边界。

`REQ-0212` 原文已回答「并存还是替换」：两种能力都要支持，界面按项目级带版本的
`LoadTaskEntryMode` 二选一。

### Q7 — 多车推进模型与唯一性约束

**上半：模型甲 + 每车推进超时预算。**`ExecuteOnceAsync` 内按车串行循环 N 次，每车套一个
`CancellationTokenSource(budget)`，超时跳到下一台、下一 tick 重试。

不选「N 个 worker 并发」：会引入 SQLite 并发写，而当前连接串**没有 `busy_timeout`、没有
`Mode=`**，全仓 `IsolationLevel` **零命中**，源码里也**没有任何 PRAGMA**（运行时那句
`PRAGMA journal_mode = 'wal'` 是 EF 迁移自己发的，不在仓库代码里）。补齐这批 SQLite 并发工程是
独立批次的量，3 车规模不值得。甲的饿死风险（一台车的 RIoT 调用超时 30 秒且
`HttpClientName = "ControlServer.RIoT.NoRetry"` 明确不重试）用超时预算即可封住。

**附带须确认**：`PeriodicTimer` 是固定周期语义，一轮超过 `PollInterval` 会立即返回；多车下
要判定这是想要的行为，还是改成「上一轮结束后再等一个周期」。

**下半：唯一性下移一层。**下面这条索引**必须删除**，它禁止一车持有两个活跃 Demand，
正是档 2 要推翻的：

```sql
CREATE UNIQUE INDEX "IX_VehicleDispatchLeases_VehicleKey"
ON "VehicleDispatchLeases" ("VehicleKey") WHERE ReleasedAt IS NULL;
```

改在 `OrderIntents` 上按 `VehicleKey` 建过滤唯一索引（未终结订单每车至多一条）。
`PK_VehicleDispatchLeases(DemandId)`（挡一 Demand 两承诺）、`PK_AcceptedDemands(DemandId)`、
`IX_AcceptedDemands_TransportDemandKey` **全部保留不动**。

这样 `CONTEXT.md` 的 `DispatchUniquenessGuard` **一字不改仍然成立**——它约束的本来就是「订单」
不是「Demand」（「每辆 AGV 同时只能被一个未确认或未终结的本项目订单占用」），之前只是因为
一车一 Demand 才由 lease 索引顺带保证了。**一车活跃 Demand 数不超过 8 个仓位**是容量约束、
归应用层，不是唯一性约束能表达的。

**模型甲是上述唯一性推理的前提，不是可选项。**最终目录重读在事务**外**
（`ControlServer.Application/WireToGateOrchestration.cs:53`），事务到
`ControlServer.Infrastructure/Persistence/WireToGateStore.cs:255` 才开，中间的 lease 前置检查
（`:256-265`）是事务内**纯读**、非 `SELECT ... FOR UPDATE`。单 worker 串行下这没问题；票 09
排批次时不得把模型甲当作可替换的实现细节。

### Q8 — `REQ-0328` 换车的资格判定：**集合 B，且仅对尚未取货的 Demand 生效**

集合 B = 车辆下线／失联／急停 + 电量跌破 `minimumBatteryPercent` + `DispatchZoneVehicleAdmission`
或 `VehicleTaskTypeAdmission` 配置变更致该车不再获准 + `SlotConfigurationReadiness` 失效
（`REQ-0259`）。检查时机跟随每车推进循环，不新增触发路径。

不取集合 C（含「出现了明显更优的车」的成本驱动主动改派）：`REQ-0328` 措辞是「**仅**当前车辆
已不符合资格」；且成本驱动改派与 `REQ-0197`「已经装车的 Demand 不得从计划丢弃」及 `REQ-0198`
的延迟保护正面冲突，而后者在档 2 下恒为拒绝——即「无法证明改派不伤害既有 Demand」，
按 fail-closed 就是不改派。

不取集合 A（仅下线／失联／急停）：会漏掉配置变更与 `SlotConfigurationReadiness` 失效两类真实
场景，而它们正是 Q5 的 `vehicles` 数组改配置后必然出现的。

### Q9 — 完整产品执行几类 MES 运输任务：**档 ii，全部六类**

**用户改判，未采纳本会话推荐的档 i。**

此问由核实 `REQ-0202` 价值时撞出：`REQ-0003`、`REQ-0150`、`REQ-0181`、`REQ-0184` 都写着**六类**
MES 运输任务，`TransportDemandKey` 即 `TASK_TYPE + SUBLOT`；四条在剖面里全标
`FP-B0 批次 0（MVP 已覆盖）`，但 `ControlServerImpact` 列写的是「执行 **WIRE_TO_GATE** 字段、
站点和容量准入」——**只覆盖六分之一**。62 条里没有任何一簇承载「执行其余五类」。

**这是本图第三次遇到同一现象**：能力藏在「批次 0 已覆盖」的条目里，实现却是单一形态的退化版。
前两次是多车（票 02 查出「348 条里无一条要求多辆车」）与 `REQ-0190` 及 `REQ-0194`（见下节）。

档 ii 对本票四条的影响是**从「机制建好不激活」变成活代码**：`REQ-0202` 的优先级带真有两个带
（`STAGING_TO_WIRE` 最高带 + 其余五类普通带）、`REQ-0203` 的跨任务类型升级有对象、
`REQ-0189` 的 `SublotTaskTypeConflict` 会真触发、`REQ-0190` 的 `agvId × taskType` 表真正多维。

档 ii 牵动的其余工程**不在本票**，已拆出为**票 13**。

### Q10 — `REQ-0219` 责任链的证据要求：**证据档 II**

车载在选任务请求里回传 `demandId` + `worklistRevision` + **它实际展示给操作员的五个字段的回显**
（完整 SUBLOT、任务类型、起点、终点、`ExpectedBasketCount`）。服务端逐字段比对：不一致即拒绝
开门并归类为系统控制失败；一致则控制链的服务端半段证明完整。

这把 `REQ-0217` 要求的「完整展示」从不可验证的实现要求变成**可验证的契约**，且**完全不规定
车载怎么画界面**——只规定回传什么，守住了本票的跨端边界（车载端归 Kun Wang，其仓库对本工作区
只读）。

不取档 I（只回传 `demandId` 与 revision）：`REQ-0219` 的系统责任划分无法落地，出了
`OperatorConfirmationMismatch` 时说不清是系统展示错还是操作员放错货，而那正是这条要区分的东西。
不取档 III（加界面截图或渲染哈希）：直接违反 `REQ-0220` 原文「结构化事实足以复核，
**不强制保存界面截图或录像**」。

### Q11 — `OperationSession` 在一站多 Demand 时的粒度：**粒度 a，每 Demand 一个**

保持 `OperationSessionId` 由 `DemandId` 派生这条已实施的关系
（`JourneyRuntimeEngine.cs:1265` 的 `StableGuid(demandId, purpose)`）不变；协议
`CurrentStopWorklistSnapshot.operationSessionId` 从 payload **顶层下移到 `items[]` 每项**。

理由：`REQ-0215` 要求「入口模式按**装货开始**边界冻结」，而装货是逐 Sublot 开始的——每 Demand
一个 session 才能逐条冻结，每停靠一个会把整站绑成一个冻结单元。且 `REQ-0220` 把
`OperationSession`、`DemandId`、完整 SUBLOT 三者并列记录时不会出现「一个 session 对多个
Demand」的歧义。

## 本票 16 条的逐条归属

沿用票 02 的判据（推翻五条架构不变量之一即为重构类）。**9 条重构、7 条增量**，与票 02 传下来的
计数一致。

### `FP-C2` 多车与多任务调度（10 条）

| 条目 | 类 | 判据 | 本票决议下的实施形态 |
| --- | --- | --- | --- |
| `REQ-0189` 多 Sublot 不合并 Demand | 重构 | B3 | 档 2 **完整实现**；`SublotTaskTypeConflict` 因 Q9=ii 成为活代码 |
| `REQ-0195` 同图跨区连续性 | 重构 | B3 | 档 2 **完整实现**（纯标签序列检查，不需成本） |
| `REQ-0196` 执行途中受控追加 | 重构 | B3 | 档 2 **fail-closed**，门禁建好恒拒 |
| `REQ-0197` 后续停靠删除或换序 | 重构 | B3 | 档 2 **删除半完整实现、换序半 fail-closed** |
| `REQ-0198` 顺路取货延迟约束 | 重构 | B3 | 档 2 **fail-closed**；它本身就是 0196 与 0197 换序的门禁 |
| `REQ-0206` 车辆按新增行程成本比较 | 重构 | B2 | 档 β：成本层 + 零容差 + 确定性裁决；等价带与分区偏好延后 |
| `REQ-0328` 当前车辆不合格时换车 | 重构 | B2 | 集合 B，仅未取货 Demand |
| `REQ-0185` 共晶与低温共晶排除 | 增量 | 无 | 复用 `AdmissionPolicy` 版本化，部署期配置 |
| `REQ-0202` 任务类型初始优先级带 | 增量 | 无 | **因 Q9=ii 成为活代码**，两个带都有对象 |
| `REQ-0203` 防饥饿阈值现场标定 | 增量 | 依赖 B2 | 机制实施、阈值留空；跨类升级因 Q9=ii 有对象 |

### `FP-C3` 车载 Worklist 选任务模式（6 条）

| 条目 | 类 | 判据 | 本票决议下的实施形态 |
| --- | --- | --- | --- |
| `REQ-0212` 两种入口模式不同时提供 | 重构 | B5 | `LoadTaskEntryMode` 项目级带版本，复用 `AdmissionPolicy` 版本化 |
| `REQ-0214` `WORKLIST_SELECTION` | 重构 | B5 | 幅度 1，只推翻 select |
| `REQ-0215` 按装货开始边界冻结 | 增量 | 依赖 B5 | 粒度 a，逐 Demand 冻结 |
| `REQ-0217` 禁止一点即开门 | 增量 | 依赖 B5 | 五字段回显即其可验证形态 |
| `REQ-0219` 责任按可证明控制链划分 | 增量 | 依赖 B5 | 证据档 II |
| `REQ-0220` 不可修改的业务审计 | 增量 | 依赖 B5 | 需求原文已列全字段，无额外决策 |

## B2、B3、B5 的工程内容（票 09 输入）

### B2 车辆集合语义 —— **比票 02 列的三条多得多**

票 02 列了三条（options 改 N 车、拆 `active.Length > 1`、排序键加车辆维度）并判「持久化层不必动」。
本票查实后补齐：

| # | 工程项 | 当前位置 |
| --- | --- | --- |
| 1 | `JourneyRuntimeOptions` 单车标量 → `vehicles` 数组 | `ControlServer.Host/Runtime/JourneyRuntimeOptions.cs:9-34`；`appsettings.json:44-63` |
| 2 | 拆掉单车断言 | `JourneyRuntimeEngine.cs:84-87`（`BusinessIdentityConflictException`） |
| 3 | 排序键加车辆维度（档 β 的成本层） | `JourneyRuntimeEngine.cs:297-301` |
| 4 | **`OnboardPeer.Attach` 硬拒第二条车载连接 → N 会话** | `ControlServer.Host/Transport/OnboardPeer.cs:11-22` |
| 5 | `JourneyRuntimes` 查询加 `AgvId` 过滤，`active[0]` → 按车推进 | `JourneyRuntimeEngine.cs:80-83`、`:108` |
| 6 | 孤儿检测按车分组 | `JourneyRuntimeEngine.cs:90-103` |
| 7 | `ReadVehicleAsync` 单车 → N 车 | `JourneyRuntimeEngine.cs:129-130` |
| 8 | lease 前置门从「整轮 return」→「该车退出本轮候选」 | `JourneyRuntimeEngine.cs:290-295` |
| 9 | 推进模型甲 + 每车超时预算 | `JourneyRuntimeWorker.cs` 全文 |
| 10 | **RIoT 交管等待识别**：`MT_WAIT_FOR_CHECKPOINT` 当前未识别 | `HttpRiotMovementGateway.cs:246`（只认 `MT_RUNNING`）、`:266`（要 `MT_FINISHED`） |
| 11 | `REQ-0190` 的 `agvId × taskType` 表 | 当前只有 `StationTaskTypeAdmission`（**站点维度**），车辆侧是标量白名单 |
| 12 | `REQ-0194` 的区→车硬集合 | 当前 `allowedDispatchZones` 是**车→区**，方向相反；软偏好完全不存在 |
| 13 | 走 `Raw` 做多车批量成本查询 | Facade 硬编码单元素，`riot-sdk` `TaskClient.cs:65` |

**第 11、12 项要单独说明，因为它们会被剖面误导。**`REQ-0190` 与 `REQ-0194` 在剖面里标
`FP-B0 批次 0（MVP 已覆盖）`，`map.md` 的 Notes 也写着「已由 `REQ-0259`、`REQ-0190`、`REQ-0194`
覆盖，不派生新需求」。两句话都没错，但合起来会被读成「已实施、无需排期」。事实是：

- `VehicleTaskTypeAdmission`、`DispatchZoneVehicleAdmission`、`DispatchZoneVehiclePreference`
  三个标识符在 `8005-agv-control-server` **全仓零命中**；
- 实际存在的是 `StationTaskTypeAdmission(StationId, TaskType)`，**站点维度、无车辆维度**，
  且 `taskType` 在 `JourneyRuntimeEngine.cs:75` 硬编码为 `WIRE_TO_GATE`；
- 需求层面确实已覆盖（**不派生新需求成立**），实现层面是**单车退化形态**——只有一个 `agvId`
  时「那台车的 workType 白名单」与「`agvId × taskType` 表」同构；`REQ-0194` 更明显，配置里是
  车→区，需求要的是区→车集合。

**B2 在 348 行剖面里仍不产生新行**（票 02 已定），但它的工程内容包含第 11、12 项。票 09 单列
B2 时必须把它们算进去，不能因为两条标着批次 0 就跳过。

### B3 计划形状

| # | 工程项 | 当前位置 |
| --- | --- | --- |
| 1 | `JourneyExecutionPlan` 20 字段单 Demand record → 多 Demand 计划 | `ControlServer.Domain/WireToGateModels.cs:174-194` |
| 2 | **`JourneyRuntimeStage` 8 值从「每车一个」降格为「每停靠或每 Demand 一个」** | `WireToGateModels.cs:162-172`；转移集中在 `JourneyRuntimeEngine.AdvanceAsync` 的 switch（`:367`）与 `OnboardRecoveryCoordinator` 三处 |
| 3 | `Worklist(...)` 恒单元素 → 多元素 | `JourneyRuntimeEngine.cs:1213-1228`（单元素集合表达式是唯一元素来源） |
| 4 | `PickupPlan` 与 `GatePlan` 恒 2 leg → N leg | `JourneyRuntimeEngine.cs:1230-1244`（`sequence` 是字面量 1 与 2） |
| 5 | 删 lease 表的 `VehicleKey` 过滤唯一索引，改在 `OrderIntents` 建 | `ControlServerDbContext.cs:45-48` |
| 6 | `queryNearEnd` 贪心最近邻做站点排序 | 当前选站靠站点名正则，`MapStationResolver.cs:10-12`、`:33-50` |
| 7 | `REQ-0198` fail-closed 门禁 | 不存在 |

**第 2 项是 B3 的真实体量，票 03 原正文低估了。**8 个阶段是**每车一个**的线性生命周期
（`AwaitingPickupArrival` → `AwaitingSublot` → `AwaitingLoadResult` → `AwaitingDepartureSafety`
→ `AwaitingGateArrival` → `AwaitingUnloadResult` → `Completed` 或 `Blocked`）。一车拉两个 Demand 时，
「车处于 `AwaitingLoadResult`」这句话就不成立了。

### B5 车载选择 Demand

| # | 工程项 |
| --- | --- |
| 1 | `LoadTaskEntryMode` 项目级带版本配置（复用 `AdmissionPolicy` 版本化） |
| 2 | 新增选任务请求与裁决消息对，与 `SublotSubmitted`、`SublotRejected` 同构 |
| 3 | 五字段回显比对（证据档 II） |
| 4 | `REQ-0220` 审计表 |

`WORKLIST_SELECTION` 这个标识符在 `8005-agv-control-server` 与 `8005-agv-protocol` **两仓零命中**，
是纯需求概念，B5 从零建。

## 必须由协议承载的能力清单（票 06 输入）

本票不改协议消息面，只输出清单。**票 02 说 B3 要动「五处硬约束加一条 G1 断言」，本票查实后
有两处纠正**。

### `UpcomingStopPlanSnapshot`

| # | 改动 | 当前值与位置 |
| --- | --- | --- |
| 1 | `legs.maxItems` 2 → **9** | `schemas/messages/UpcomingStopPlanSnapshot.schema.json:116` |
| 2 | `sequence.maximum` 2 → **9** | 同文件 `:82-86` |
| 3 | **顶层 `demandId`（单数）语义失效**，须下移到每个 leg 或去掉 | 同文件 payload 顶层；C# 侧 `UpcomingStopPlanProjection` 见 `WireToGateModels.cs:118-121` |
| 4 | `businessDedupKeys` 由 `["demandId"]` 变更（dedup 键变更是 breaking） | `manifest/release.json:234-248` |

上限 9 的推导：一车至多 8 个仓位（`SlotNo` 的 `maximum: 8`，`schemas/common/types.schema.json:55`），
一个 Demand 至少占 1 个花篮，故至多 8 个取货停靠加 1 个关卡停靠。

**纠正一：`legType` 的 enum `["TO_PICKUP","TO_GATE"]` 不因 B3 而改。**档 2 下每一段仍是「去某个
取货点」或「去关卡」。票 12（等待点）与票 04（充电）会给这个 enum 加值，但那是它们的要求，
不是 B3 的。

### `CurrentStopWorklistSnapshot`

| # | 改动 | 当前值与位置 |
| --- | --- | --- |
| 5 | `items.maxItems` 1 → **8** | `schemas/messages/CurrentStopWorklistSnapshot.schema.json:115` |
| 6 | 顶层 `operationSessionId` **下移到 `items[]`**（Q11 粒度 a） | 同文件 payload 顶层 |
| 7 | `workType` 的 `const` 由 `WIRE_TO_GATE` **解除为六类 enum**（Q9=ii） | 同文件 `:87-91` |

**纠正二：`stopRole` 的 enum `["PICKUP","GATE"]` 不因 B3 而改**，理由同 `legType`。

注：`items` 当前**没有 `minItems`**，只有 `maxItems: 1`，所以空数组本来就合法——多 Demand 化
不需要为「空清单」另做处理。

### B5 新增

| # | 改动 |
| --- | --- |
| 8 | 新增车载 → 服务端的选任务请求消息，载 `demandId` + `worklistRevision` + 五字段回显 |
| 9 | 新增服务端裁决消息（接受或拒绝 + 拒绝原因码） |
| 10 | `W2G-IS-01` 的 `ownerResponsibilities.onboardHmi` 里 `NEVER_DISCOVER_SELECT_OR_BIND_DEMAND` **字面必须改** |
| 11 | 向量 `CV-DEMAND-ACCEPT-TO-PICKUP` 的 `forbiddenSideEffects` 里 `onboard-demand-selection` 须改 |

第 10、11 项的联动面：该 token 被 `schemas/governance/integration-slice-index.schema.json:108`
的 `const` 锁死、被 `tools/g1-validate.mjs:22-23` 逐字断言、出现在
`integration-slices/index.json:65` 与 `vectors/CV-DEMAND-ACCEPT-TO-PICKUP/expected.json:36`
——**改一个字符 G1 就红，四处要同步动**。

**`onboardMode` 的 `READ_ONLY_COMMITTED_PROJECTION` 语义仍成立，token 可不改**：投影依然只读，
新增的是一条车载到服务端的请求，与既有 `SublotSubmitted` 同构。

### 不进协议的

**B2 不进协议 v2**（票 02 已定，本票复核确认）：信封的 `agvId` 必填且**无 `const`、`enum`、
`pattern`**，对 54 条消息 schema 的 `agvId` 属性块逐个筛查这三个关键字**零命中**，
从未限制车辆总数为 1，三车三会话即可。

### 一条票 06 必须知道的工程量事实

**54 条消息 schema 各自内联复制了一份信封，没有任何一条 `$ref` 引用 `envelope.schema.json`**
（对 `schemas/messages/` 的 grep 零命中），且各自按需收紧（两个快照消息把 `correlationId`
收成 `"type": "null"`）。**票 06 若要动信封，等于改 54 个文件。**

## 对其他票据的影响

| 票据 | 影响 |
| --- | --- |
| **票 06**（协议 v2 冻结） | 接上节 11 项清单；另加 Q9=ii 的 `workType` const 解除，以及 `profileId` 的 `const` 值 `WIRE_TO_GATE_MVP` 是否随之改名 |
| **票 07**（切片家族） | `W2G-IS-01` 的 token、schema `const` 与向量四处联动改动 |
| **票 08**（验收边界） | `REQ-0196` 与 `REQ-0198` 只能证明「门禁正确拒绝」，与 3 车 3 桩凑不出充电争用同类，**不得默认「不触发即通过」** |
| **票 09**（批次划分） | B2 单列时须含第 11、12 项工程；模型甲是唯一性推理的前提不是可选项；Q9=ii 使 348 行批次列大改 |
| **票 12**（等待点独占） | `legType` enum 扩值由票 12 与票 04 提出，**不是 B3 的要求**，两票不要相互推诿 |
| **票 13**（新建，六类任务） | Q9=ii 拆出 |

## 已知风险与未决项

1. **`riot-sdk` 仓库 HEAD 与生产二进制不是同一个 API 面。**控制服务端链接的是 vendored
   `RIoT.Sdk.Facade 0.1.0-controlserver.2`（`Directory.Packages.props:13`，是 `PackageReference`
   非项目引用），其中 `ListStationsStrictAsync`、`GetVehicleCardAsync`、`FindOrderByUpperIdAsync`、
   `ListOrdersByStatesAsync`、`GetVehicleExecutionFactsAsync` **在仓库源码里不存在**
   （`git log -S` 全为空），来源 commit `e708f874` 因历史重写已消失。本票的档 β 要走 `Raw`，
   而 `Raw` 的可用性取决于 vendored 包而非仓库源码。**属实施图前置，本票不处理。**
2. **`REQ-0196`、`REQ-0198` 与 `REQ-0197` 换序半恒 fail-closed**，解除条件是 RIoT 侧新增站→站
   路径成本查询（或等价的时间估计），属外部团队，不在本工作区控制范围。
3. **`WIRE_TO_GATE` 在 v1.0.0 基线里出现 0 次。**它是 MVP 阶段的命名（协议 `profileId` 与
   `workType`），不是基线的任务类型名；基线里六类只有 `STAGING_TO_WIRE` 有名字，其余五类的
   名字在工厂 IT 的 `MES_TASK_UNION` SQL 里。**票 13 的第一件事就是把它们查出来。**
4. `PeriodicTimer` 的固定周期语义在多车下是否合适，待实施图确认。

## 三个子 agent 的原始报告

未落盘。要点已浓缩进本文件的证据列。可复现——重新派 `Explore` 子 agent 即可，prompt 骨架是
「逐条回答 + 每条带 `文件路径:行号` + 找不到就明说不存在 + 只给事实不给建议」。三份分别覆盖：
ControlServer 分配核心（10 节）、计划形状与协议契约（跨 `8005-agv-control-server` 与
`8005-agv-protocol` 两仓 10 节）、RIoT 路径成本能力（跨 `riot-sdk` 与控制服务端 10 节）。
