# 一次冻结协议 v2 消息面、错误码与向量范围

Type: grilling
Status: closed
Blocked by: 03, 04, 05, 12, 13
Blocks: 07, 09

## Question

以票 03～05 输出的「必须由协议承载的业务能力」清单为输入，一次性冻结 `8005-agv-protocol` v2 的完整设计面。

这一票必须一次做完。逐条加需求逐次发 release 会反复作废两端已有的 G2 证据——协议是 Kun Wang 那侧构建的契约，一次补丁发布同时作废两端受影响的 G1/G2/G3 证据。当前状态是 `ProtocolVersion` 1、`WireToGateMvpProtocolProfile` allowlist、明文期、两端无协商无降级。

须回答：

1. **消息面**：v2 的完整 `messageType` allowlist。哪些 v1 消息沿用、哪些扩展字段、哪些新增、哪些废弃。多车并发、Worklist 选任务入口、自动充电周期、充电失败与清桩、治理面（若票 05 判定需要）各自需要哪些消息。
2. **错误码与交付类别**：v2 的完整错误码表，以及每个消息的交付类别归属。MVP 用的是五类交付 + 通用 ACK + 业务幂等 + 五步恢复对账，v2 是沿用这套还是需要扩展。
3. **测试向量范围**：v2 的一致性测试向量覆盖哪些场景，`vectorId` 命名与编号规则，以及向量与切片（票 07）的绑定方式。合法与非法消息样例的覆盖标准是什么。
4. **v1 与 v2 的版本关系**：并存、替换还是版本协商。当前明文期两端无协商无降级、版本错配的表现是连接被拒而不是一条说明原因的错误——v2 是否引入协商能力，若不引入，两端升级的切换方式是什么（同时替换？CD 的 WIRE_TO_GATE 两端打进一个包这一现有约束在 v2 下是否仍然成立）。
5. **冻结的强度**：本票的产出是「v2 设计面已冻结、可据以实施」还是「v2 已可发布」。二者的区别在于是否需要写出 Schema、样例与向量文件本身——那属于实施，不属于本图。本票须明确交付物的边界，以及实施图拿到本票产出后还需补什么才能切一个 `ProtocolRelease`。
6. **发布与通知**：v2 的正式 release 仍受 `docs/release-governance.md` 约束，须两名产品负责人签名，AI 与 CI 不能批准。本票须写明：本图不产生 release，本票的结论推送后按 notify-after-change 规则开 issue @`SocialKKKK`，说明改了什么、触及哪些 `W2G-IS-*` 切片、以及他的 `ONBOARD_HMI_G2` 证据是否作废。

### 票 03 定下的协议清单（本票的输入，不要重新推导）

[票 03 决议](03-answer.md)输出了 B3 与 B5 必须由协议承载的能力，并**纠正了票 02 的两处判断**。

`UpcomingStopPlanSnapshot`：

| # | 改动 | 当前值与位置 |
| --- | --- | --- |
| 1 | `legs.maxItems` 2 → **9** | `schemas/messages/UpcomingStopPlanSnapshot.schema.json:116` |
| 2 | `sequence.maximum` 2 → **9** | 同文件 `:82-86` |
| 3 | **顶层 `demandId`（单数）语义失效**，须下移到每个 leg 或去掉 | 同文件 payload 顶层 |
| 4 | `businessDedupKeys` 由 `["demandId"]` 变更（dedup 键变更是 breaking） | `manifest/release.json:234-248` |

`CurrentStopWorklistSnapshot`：

| # | 改动 | 当前值与位置 |
| --- | --- | --- |
| 5 | `items.maxItems` 1 → **8** | `schemas/messages/CurrentStopWorklistSnapshot.schema.json:115` |
| 6 | 顶层 `operationSessionId` **下移到 `items[]`** | 同文件 payload 顶层 |
| 7 | `workType` 的 `const` 由 `WIRE_TO_GATE` **解除为六类 enum** | 同文件 `:87-91`；来自票 13 |

B5 新增：

| # | 改动 |
| --- | --- |
| 8 | 新增车载 → 服务端的选任务请求消息，载 `demandId` + `worklistRevision` + **五字段回显**（完整 SUBLOT、任务类型、起点、终点、`ExpectedBasketCount`） |
| 9 | 新增服务端裁决消息（接受或拒绝 + 拒绝原因码） |
| 10 | `W2G-IS-01` 的 `ownerResponsibilities.onboardHmi` 里 `NEVER_DISCOVER_SELECT_OR_BIND_DEMAND` **字面必须改** |
| 11 | 向量 `CV-DEMAND-ACCEPT-TO-PICKUP` 的 `forbiddenSideEffects` 里 `onboard-demand-selection` 须改 |

上限 9 与 8 的推导：一车至多 8 个仓位（`SlotNo` 的 `maximum: 8`，
`schemas/common/types.schema.json:55`），一个 Demand 至少占 1 个花篮，故至多 8 个待装条目、
8 个取货停靠加 1 个关卡停靠。

**票 02 的两处判断已被纠正，本票不要照旧执行：**

1. **`legType` 的 enum 不因 B3 而改。**档 2 下每一段仍是「去某个取货点」或「去关卡」。
   给它加值的是**票 12（等待点）与票 04（充电）**，两票不要与本节相互推诿。
2. **`stopRole` 的 enum 不因 B3 而改**，理由同上。

**B2 不进协议 v2**（票 02 已定，票 03 复核确认）：信封的 `agvId` 必填且**无 `const`、`enum`、
`pattern`**，对 54 条消息 schema 逐个筛查这三个关键字**零命中**，从未限制车辆总数为 1，
三车三会话即可。

### 一条本票必须先知道的工程量事实

**54 条消息 schema 各自内联复制了一份信封，没有任何一条 `$ref` 引用 `envelope.schema.json`**
（对 `schemas/messages/` 的 grep 零命中），且各自按需收紧（两个快照消息把 `correlationId`
收成 `"type": "null"`、`sessionGeneration` 去掉 null 分支、`messageType` 加 `const`）。
**本票若要动信封，等于改 54 个文件。**`profileId` 当前 `const` 为 `WIRE_TO_GATE_MVP`，
完整产品是否随之改名同样牵动这 54 份副本。

另：`CurrentStopWorklistSnapshot` 的 `items` 当前**没有 `minItems`**，只有 `maxItems: 1`，
空数组本来就合法——多 Demand 化不需要为「空清单」另做处理。

### 已知边界

- 本票不写 Schema、样例或向量文件，不改 `8005-agv-protocol` 仓库内容，不打 tag，不切 release。
- 本票不代 Kun Wang 批准跨端契约。单人批准的是本图的设计决定；正式 release 的双人签名门禁不变。
- 本票不决定批次归属与顺序，那是票 09；不决定切片编号，那是票 07。
- 冻结范围以票 03～05 的业务决定为准。若发现某项业务能力在票 03～05 中未决定而协议无法冻结，应回到对应票补齐，不在本票替它做业务决定。

## 来自票 13 的输入（2026-09-03）

六类任务执行放开后，协议有**四处焊死**必须解除，全部是 breaking。票 13 只输出清单与建议取值，
不改 schema。

| 位置 | 现状 | 票 13 的建议取值 |
| --- | --- | --- |
| `envelope.schema.json:14` 等 **56 个文件、58 处** | `profileId` `const "WIRE_TO_GATE_MVP"` | **改名**——解除单类型后名不副实，趁一次性 breaking 改完 |
| `messages/CurrentStopWorklistSnapshot.schema.json:87-91` | `workType` `const "WIRE_TO_GATE"` | 解除为六值 enum，**用 MES 原始字面值** |
| `messages/CurrentStopWorklistSnapshot.schema.json:92-98` | `stopRole` enum `["PICKUP","GATE"]` | **拆开**：`["PICKUP","DROPOFF"]` + 独立的站点功能字段取五值 |
| `messages/UpcomingStopPlanSnapshot.schema.json:75-81` | `legType` enum `["TO_PICKUP","TO_GATE"]` | 同理改 `["TO_PICKUP","TO_DROPOFF"]` |

**六个 MES 原始字面值**：`DIE_TO_WIRE_STAGING`、`DIE_TO_OVEN`、`WIRE_TO_GATE`、`WIRE_TO_OPTICAL`、
`STAGING_TO_WIRE`、`WIRE_TO_NITROGEN`。用原值而非自造命名的理由是 `REQ-0003`——正式 SQL 是六类任务
的唯一查询原稿，自造一层映射就要同步维护。

**五个站点功能值**（`REQ-0324`）：派工待送、烘箱、关卡、三光、氮气柜。

**`stopRole` 必须拆的理由**：它现在混了两个正交概念——停靠的业务角色（取货/卸货）与站点的功能身份
（机台/关卡）。`STAGING_TO_WIRE` 方向反转后 `GATE` 既不是它的终点也不是它的角色，不拆就会让枚举
退化成六类端点组合的笛卡尔积。**这与票 03 说的「`legType` 与 `stopRole` 的 enum 不因 B3 而改」
不冲突**——理由不同，是六类端点功能多样化，不是 B3。

**另记一处代码事实**：`8005-agv-control-server` 的 `appsettings.json:9` 有
`ProtocolCandidate.profileId`，但 `src/` 内**查不到任何绑定或读取**（无 `GetSection("ProtocolCandidate")`、
无 options 类），代码一律用 `ProtocolCandidateIdentity.cs:6` 的编译期常量——**这两份值可能静默漂移**。
本票或实施图择一处置。

详见 [票 13 决议](13-answer.md) 的 Q4。

## 来自票 12 的输入（2026-09-03）

**新增第三个正交维度：停靠目的类别 `StopPurposeCategory`，三值 `BUSINESS`／`WAITING_POINT`／`CHARGER`。**

票 13 已要求把 `stopRole`／`legType` 拆开「取货/卸货」与「站点功能」两个正交概念。等待点两个
维度都不属于——它既不装卸，也不是五个 `PublicStationFunction` 之一。票 12 据此加第三个维度。

| 项 | 内容 |
| --- | --- |
| 新增维度 | `StopPurposeCategory`，三值 `BUSINESS`／`WAITING_POINT`／`CHARGER` |
| 位置 | `schemas/messages/UpcomingStopPlanSnapshot.schema.json:75-81`（现 `legType`）与 `schemas/messages/CurrentStopWorklistSnapshot.schema.json:92-98`（现 `stopRole`） |
| 正交性 | 与票 13 要求的两个维度正交：取货/卸货与站点功能**只在 `BUSINESS` 下有意义**，等待点与充电桩停靠两者皆无 |
| `CHARGER` 值 | **由票 12 定，票 04 不再向本票提第四个值** |
| 计划上限 | 票 03 定 `legs.maxItems` 9／`sequence.maximum` 9／`items.maxItems` 8。**等待点停靠不叠加上限**——它是行程收敛之后的独立承诺，不与业务停靠同时在计划里 |

**当前 enum 实测值**（本票冻结前的起点）：`legType: ["TO_PICKUP", "TO_GATE"]`、
`stopRole: ["PICKUP", "GATE"]`、`sequence.maximum: 2`。两处 enum 在整个 `schemas/` 下各只
出现一次。按 `docs/release-governance.md:11`，enum 变更是 breaking。

**为什么等待点必须进计划而不是另开一条消息**：`REQ-0292` 的原话是「形成承诺后，返回成为
车辆**当前已承诺下一站**，沿用 `PlannedStopMutationBoundary`」。「已承诺下一站」与
`PlannedStopMutationBoundary` 两个词都是计划语义，基线已经把空闲返回放进计划里了。

**这条同时是 B1 在协议上的实质表达：计划里可以有不由 `TransportDemand` 引起的停靠。**票 03
定的 `MultiStopExecutionPlan` 此前每个停靠都对应至少一条 Demand，等待点停靠是第一个反例，
充电桩停靠是第二个。本票冻结时须确认消息 schema 不再假定「每个停靠必有 Demand 引用」。

**一处措辞纠正，与协议无关但会影响本票读基线**：`byDefaultMissions` 是 **URL 路径段**
（`POST /api/order/v1/add/byDefaultMissions`），不是请求体字段。请求体字段叫 `mission`
（单数、数组、必填），响应侧才叫 `missions`。基线 `REQ-0294` 与 `CONTEXT.md:751` 都写
「创建 `byDefaultMissions` 单段 move」，在代码语境下会被读成字段名。

详见 [票 12 决议](12-answer.md) 的 Q5。

## 来自票 04 的输入（2026-09-04）

**充电簇要求协议承载的能力，确定清单如下（五项）。**

**一、两对新消息（4 条），形状照抄 v1 已有的范式。**票 04 的分端判据是「动作的对象里有没有车」：
有车说明人在现场、在车旁、要看着那台车那个桩，走车载 HMI；只有桩说明车可能不在，走 ControlServer。

| 动作 | 对象 | 落点 |
| --- | --- | --- |
| `UnableToChargeFieldConfirmation`（充不上现场确认，`REQ-0176`） | 车 + 桩 | **车载 HMI，一对请求/结果** |
| `ManualStationClearanceConfirmation`（人工清桩确认，`REQ-0179`） | 车 + 桩 | **车载 HMI，一对请求/结果** |
| `ChargingStationAllocationHold`（授权维修触发的暂停，`REQ-0288`） | 只有桩 | ControlServer 侧，**不进协议** |
| `ChargingStationRecoveryConfirmation`（桩恢复确认，`REQ-0288`） | 只有桩 | ControlServer 侧，**不进协议** |

范式是 `ManualChargingReturnToServiceRequested` 的 payload：`requestId`（幂等）+ `administrator`
（`OperatorContext`）+ `administratorRole`（enum `MAINTENANCE_ADMINISTRATOR`／`SYSTEM_ADMINISTRATOR`）
+ `reason`，`correlationId: null` 表示发起方向为车载 → 服务端。

**二、`legType` 增 `TO_CHARGING_STATION`**（`schemas/messages/UpcomingStopPlanSnapshot.schema.json:75-81`，
当前 `["TO_PICKUP","TO_GATE"]`）；**`stopRole` 增充电桩取值**
（`schemas/messages/CurrentStopWorklistSnapshot.schema.json:92-98`，当前 `["PICKUP","GATE"]`）。
`StopPurposeCategory` 的 `CHARGER` 值由票 12 定，**本簇不再提第四个值**。

**三、不要改 `manualChargingHold` 的含义。**票 04 的 Q3 把「充电桩名册为空」定为**退化到
`ManualChargingHold` + `ManualChargingReturnToService`**（即 MVP 现有那条路），因为桩物理上还没
安装、名册为空是投运第一天的真实状态。该字段因此**保留原义作为那一态的载体**，充电周期状态
**另立字段**。含义变更在字段名不变时两端都静默编译，是最坏的一种 breaking，本票已避开它——
票 06 不要把它改回去。

**四、`ManualChargingReturnToServiceRequested`／`Result` 在 v1 的 54 条消息面之内**
（`manifest/release.json` 的 `denylistedMessageTypes` 11 条里没有它们），**有完整正反向量**，
而控制服务端 `src/` 与 `tests/` 对它们**零命中**。冻结 v2 时须决定：实现，还是进 denylist。
按第三点，票 04 的定案要求**保留并实现**。

**五、`batteryState` 当前枚举 `SUFFICIENT`／`LOW`／`UNKNOWN` 三值是否够用**，请连同第三点的
新增充电周期状态字段一并判。协议无可选字段（`compatibility/report.json:11`），两处都是 breaking。

详见 [票 04 决议](04-answer.md) 的 Q8、Q3 与第三节。
## 来自票 05 的输入（2026-09-04）

**本票要冻结的协议增量多了三项，全部是 breaking。**

1. **`CapabilitySnapshot` 缺「指纹」字段。**现有 payload 必填 7 项：`capabilityVersion`、`observedAt`、
   `slotModelVersion`、`activeSlotConfigurationVersion`、`slotStates`、`supportsBatchUnlock`、
   `onboardJournalFormatVersion`。而 `REQ-0316` 要「`SlotModelVersion`、IO 配置版本**与指纹**及完整
   `OnboardCapabilitySnapshot` 与归档前记录完全一致」，`REQ-0266` 要「模板、模型和 IO 候选/生效版本**及指纹**」。
   **全部 54 个 schema 里 `fingerprint` 零命中。**

   **这一项需要本票自己判一次**：`REQ-0316` 本身已由票 05 判**延后**，但协议一次冻结、不接受分批——
   延后的能力现在不加字段，将来就要再发一次 breaking release，代价是两端 G1/G2/G3 证据全部作废。

2. **配置激活的一对新消息（服务端→车载）。**`REQ-0264`（整车配置只能原子激活）与 `REQ-0266`
   （要记「激活请求、车载实际结果和最终对账结论」）需要它，**协议 54 条消息里没有任何配置类消息**。
   票 05 已把 `REQ-0264` 与另外 7 条仓位配置权威条目改判进 `FP-C7`，本期实施，所以这一项不是可选的。

3. **告警上报消息。**`REQ-0270`（全部 8005 告警集中显示在 ControlServer）需要车载告警上报，
   **协议 schema 里 `Alarm`／`Alert` 零命中**。票 05 已把 `REQ-0270` 改判进 `FP-C8`，本期实施。

**一项明确不进协议的判定，请采信**：`REQ-0268` 看板的数据源走控制服务端新增的**只读 HTTP 查询接口**，
不进协议 v2。协议是控制端↔车载端的 NDJSON 会话协议，看板读的是服务端自己的持久化状态，不在那条线上。

**两条不需要改协议的定案**：`REQ-0254` 的 `administratorRole` 两值枚举**保持原义不动**——票 05 判它
「部分实施」，枚举模型已冻结且服务端已在校验，身份自报那一半随 `FP-C10` 延后，**不做含义变更**
（含义变更在字段名不变时两端都静默编译，是最坏的一种）。`REQ-0339` 的二次认证同样不引入协议字段。

**一条有界观察，本票可判可不判**：`slotStates` 定死 `minItems: 8, maxItems: 8`。八仓位是 `REQ-0267`
已批准的硬件事实，故当前正确；但 `REQ-0261` 把「仓位集合」变化列为硬件配置变更，定长数组下这类变化
不可表达。票 05 只记未判。

详见 [票 05 决议](05-answer.md) 的 1.4、1.6 与第三节。
