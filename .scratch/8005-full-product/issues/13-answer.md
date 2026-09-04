# 票 13 决议：六类 MES 运输任务的执行范围，及其对 348 行剖面的影响

日期：2026-09-03。批准人：用户（本图默认且唯一最终批准人）。

## 一句话结论

六类任务的执行能力**一次建齐**，但**投运范围由现场绑定逐类 fail-closed 决定**；承载它的不是新需求，
而是 348 行里被误判为「批次 0 已覆盖」的 17 条公共站点绑定条目——**这是本图第四次遇到「能力藏在
批次 0、实现是退化形态」，也是最严重的一次：整簇零实现**。`STAGING_TO_WIRE` 因方向反转撞上一条
代码强制的隐含契约，单列后一批，并据此认下**第六条架构不变量 I6**。

## 一、事实基础

本票开工前查了两轮事实，其中三条直接改变了问题的形态。

### 1.1 六类的真名（推翻票据正文与 map Notes 的一处措辞）

六个 `TASK_TYPE` 是工厂 IT 统一 SQL 里六个 `UNION ALL` 分支各自的硬编码字面量
`SELECT '<literal>' AS TASK_TYPE`，**不来自任何表的列值**——MES 表里没有 `TASK_TYPE` 这个概念，
它是这份 SQL 合成出来的分支标签。

| `TASK_TYPE` | 路线（SQL 注释） | AREA 端是 | 固定端功能 | 位置 |
| --- | --- | --- | --- | --- |
| `DIE_TO_WIRE_STAGING` | 装片机台 → 焊线派工待送区 | 起点 | 派工待送 | `query.sql:13` |
| `DIE_TO_OVEN` | 装片机台 → 烘箱间 | 起点 | 烘箱 | `query.sql:54` |
| `WIRE_TO_GATE` | 焊线机台 → 人工质检关卡区 | 起点 | 关卡 | `query.sql:95` |
| `WIRE_TO_OPTICAL` | 焊线机台 → 三光区 | 起点 | 三光 | `query.sql:136` |
| `STAGING_TO_WIRE` | 焊线派工待送区 → 指定焊线机台 | **终点** | 派工待送 | `query.sql:177` |
| `WIRE_TO_NITROGEN` | 焊线机台 → 固定氮气柜 | 起点 | 氮气柜 | `query.sql:196` |

来源：`8005-mes-ingest/queries/mes-task-union/query.sql`，实测 SHA-256
`54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae` 与 `REQ-0157` 记载**完全吻合**。
输出列顺序另有 `query.toml:7` 佐证。

**纠正一处措辞。**票据正文与 map Notes 都写着「`WIRE_TO_GATE` 是 MVP 阶段的命名而非基线任务类型名」。
前半句不对：它**就是** MES 的真实 `TASK_TYPE` 之一。准确的表述是：基线正文只点了 `STAGING_TO_WIRE`
一个名字（因为只有它方向反、需要单独说明），其余五类的名字基线没写，但它们同样是 MES 的真名。
`WIRE_TO_GATE_MVP` 那个 `profileId` 才是 8005 自造的命名。

**五个固定端点正好是 `REQ-0324` 那句「派工待送、烘箱、关卡、三光和氮气柜」。**基线模型与工厂 SQL
完全闭环，无一多余无一缺失。派工待送被两类共用、一类作终点一类作起点——这正是 `REQ-0343` 要
`TaskTypePublicStationRuleVersion` 记录「及其在运输中是起点还是终点」的原因，也是 `REQ-0334`
「同一 Station 不得同时承担多个 `PublicStationFunction`」（反过来，同一 function 可被多个
`TASK_TYPE` 引用）的原因。

### 1.2 摄取侧无事可做：本票是「只加执行」

`8005-mes-ingest` **已经全量摄取六类，管线里没有任何 `TASK_TYPE` 过滤**：

- 投影入口 `MesTaskUnionPollRunner.cs:26-32` 原封不动交给 `RoundIngestor.cs:16-22`，后者只做 null 检查。
- Oracle 读取 `OracleMesTaskUnionRoundSource.cs:385-416` 无条件映射每一行。
- 唯一的行级判定是 `SqlServerMesIngestProjection.cs:1160-1161` 的
  `!IsNullOrWhiteSpace(WorkType) && !IsNullOrWhiteSpace(Sublot)`——**空值判定，不是取值白名单**。
- `TaskTypeProtection` 的 WorkType 集合是**运行时发现**的（`:1264-1279` 由本轮观测 `GroupBy(WorkType)`
  与库中已存 keys 求并集），新 WorkType 自动获得保护状态，无需改代码。
- 对外目录接口明确拒绝过滤，OpenAPI 原文：`"A full-range catalog resource. It accepts no query parameters."`
  （`NewMesIngestOpenApi.cs:320`），并有专门的 400 码 `CATALOG_QUERY_NOT_SUPPORTED`。
- `WorkType` 全链是自由 `string`（`MesTaskUnionRound.cs:17`、`ProjectionModels.cs:193`、
  `ExternallyReadableDemandCatalog.cs:116`），全仓 `enum .*WorkType` 零命中，只有 128 字符长度上限。

**`WIRE_TO_GATE` 在 MesIngest 生产服务代码（Core / Host / Infrastructure）里出现 0 次**，唯二两处在
WPF 客户端的双语文案查表（`WatchTextCatalog.Overview.cs:115`、`:386`），且是六个平级 case 之一，
未知值 fallback 到「未知工序（请升级应用）」。

**结论：本票是「只加执行」，不是「加摄取 + 加执行」。**`8005-mes-ingest` 不因本票产生任何改动需求。

### 1.3 控制服务端的锁死点（穷举）

**其余五类的名字在 `8005-agv-control-server` 全仓（含 `evidence/`）零命中**——连测试夹具都没有。
它们现在被静默丢弃，且**不留任何证据**：没有任何记录能证明被丢了多少条。这对完整产品的迁移验收
是一个真实缺口（无法用「放开前后的执行量差」来验证放开是否符合预期）。

三条关键事实：

1. **`allowedWorkTypes` 是冗余配置，改它无效。**真正的锁死点在
   `JourneyRuntimeEngine.cs:165-166`——配置检查后面还 `||` 了一个字面量相等
   `!string.Equals(candidate.WorkType, "WIRE_TO_GATE", Ordinal)` → `OUT_OF_SCOPE_WORK_TYPE`。
   反向地，`JourneyRuntimeOptions.cs:74-75` **要求**配置里必须含 `WIRE_TO_GATE`，否则启动即失败——
   一个只跑其余五类的部署起不来。
2. **journey 不知道自己是哪类任务。**`workType` 从 MES 一路保留到 `AcceptedDemandRow` 与对端投影
   （12 个环节），唯独在 `JourneyExecutionPlan`（`WireToGateModels.cs:174-194`）和 `JourneyRuntimeRow`
   （`ControlServerDbContext.cs:449-493`）这两层被丢弃，下游要用得回查表（四处 `SingleAsync`）。
   「另一端按 `TASK_TYPE` 配置固定站」的前提是先把类型塞进 plan，连带新迁移和
   `WireToGateStore.cs:1834-1853` 幂等比较的字段扩展。
3. **终点解析发生在知道任务类型之前。**`JourneyRuntimeEngine.cs:58-59` 的
   `RequireFixedStation(currentMap, GateStationRiotId, GateStationId)` 在 `DiscoverAndAcceptAsync`
   之前、每轮一次执行，此时还没有任何候选。按类型选固定站必须重排这个顺序，或预解析全部固定站。

工程量粗判：改一行配置 1 处、改类型定义 4 处、改逻辑分支约 12 处、**需要新抽象 3 处**。

### 1.4 公共站点绑定治理：整簇零实现

控制服务端 `src/` 实测：

```
PublicStationFunction             : 0 个文件
FixedTaskStation                  : 0 个文件
PublicStationBindingSetVersion    : 0 个文件
TaskTypePublicStationRuleVersion  : 0 个文件
MapPublicStationRequirementSet    : 0 个文件
PublicStationBindingHold          : 0 个文件
MapStationCatalogSnapshot         : 34 个文件   ← 只有这个真存在
```

而这 17 条（`REQ-0184`、`REQ-0187`、`REQ-0304`、`REQ-0324`、`REQ-0334`~`REQ-0338`、
`REQ-0340`~`REQ-0345`、`REQ-0347`、`REQ-0348`）在剖面里**全部标着「批次 0 已覆盖」**，
`ControlServerImpact` 列还是同一句复制的「解析机台与关卡绑定，持久化配置/建单对账」——**簇级粗粒度
描述，不是逐条判定**。这与票 03 发现 `REQ-0190`／`REQ-0194` 的情形同构，但规模大得多。

**这是本图第四次「能力藏在批次 0、实现是退化形态」，而且是最严重的一次。**前三次（多车、车辆准入、
六类任务）至少还有一个单一形态的实现；这次是**整簇零实现**，被一个 `gateStationId` 标量在事实上顶替了
「每 Map 每功能一个绑定 + 版本化 + 暂停 + 回滚 + 180 天审计」的全部内容。

**票据正文担心的「62 条里没有任何一簇承载执行其余五类」，答案是：承载它的条目存在，被误归批次 0 了。**

## 二、逐问决议

### Q1 — 六类各自的执行范围

**能力一次建齐，投运逐类 fail-closed 放行。**六类走**同一套配置驱动机制**，不是六份代码分支——
`REQ-0343` 的 `TaskTypePublicStationRuleVersion` 已经规定了「每个受支持 `TASK_TYPE` 使用的
`PublicStationFunction` 及其在运输中是起点还是终点」，方向是规则里的一个字段而不是 `if/else`。
基线还自带了逐类投运的准入不变量：

- `REQ-0335`：任务类型只有在**全部**需求功能具有有效绑定后才可投运；不为缺失功能填默认站点。
- `REQ-0343`：规则与绑定在同一发布门禁内校验，**不允许先放行缺失固定站点的 `TASK_TYPE`**。

**因此「哪几类进完整产品」不是一个代码问题，是一个现场绑定问题。**现场补完测绘、录入绑定，
该类即可投运，**不改代码**。

**分批见 Q5**：`STAGING_TO_WIRE` 因方向反转单列后一批。

**现场事实（用户 2026-09-03 确认）**：烘箱间、三光区、氮气柜、派工待送区物理存在（MES 六类工序真实
在跑），但 AGV 路网当前只测绘了焊线区到关卡这一段——`mapId` 25 的 206 个站 = 205 个 AREA 命名机台
+ 1 个关卡（`evidence/g3/20260827-map25-dynamic-gates-refresh/result.json`，全仓三份证据同值）。
所以放开六类后，**在现场补测绘之前，其余五类会被 `REQ-0335` 正确地挡在投运之外**——这是设计行为，
不是缺陷。

### Q2 — `FixedTaskStation` 的按类配置形态

**取乙档：做数据模型与 fail-closed 校验，运维治理面延后。**

| 落地（FP-C9a，7 条） | 延后（FP-C9b，9 条，与 FP-C7 同批） |
| --- | --- |
| `REQ-0184` AREA 端点方向 + 按类型配固定站 | `REQ-0304` 目录变化不自动替换绑定 |
| `REQ-0187` AREA→EQP 唯一性不按工序过滤 | `REQ-0336` 核对与激活的两级管理员职责 |
| `REQ-0324` 五个 `PublicStationFunction` | `REQ-0337` `PublicStationBindingSetVersion` 整图原子激活 |
| `REQ-0334` 绑定键 `mapId + PublicStationFunction` | `REQ-0340` `PublicStationBindingHold` 立即暂停 |
| `REQ-0335` 缺功能不投运 | `REQ-0341` 目录变化按身份与语义风险分类 |
| `REQ-0338` 完整性校验（触发时机见下） | `REQ-0342` 变化影响范围收敛 |
| `REQ-0343` `TaskTypePublicStationRuleVersion` | `REQ-0345` 已存在 RIoT 订单不被配置变化取消 |
| `REQ-0344` Demand 冻结规则/站点/版本 | `REQ-0347` 激活结果未知不猜测生效版本 |
| | `REQ-0348` 180 天不可改写审计 |

**`REQ-0338` 的处理需要说清楚**：它的**校验内容**（同图、同功能唯一、同一 Station 不复用多功能、
当前需求功能完整、目录新鲜）进 C9a，**触发时机从「激活候选版本」下调为部署与启动期**；
「激活」这个动作面本身随 C9b。这不是 `证据受限实施`——证据是可得的，是治理动作面缩小了。

**不取丙档的理由**：丙档（`appsettings.json` 里一张静态表、重启生效）等于把 `gateStationId` 从标量
改成字典，六类能跑，但 `REQ-0338` 的 fail-closed 完整性校验没了——一个配错的站点会静默把货送到
错误的公共点，而基线专门为此写了这一条。丙档省下的是 C9a 里最不该省的那一半。

**不取甲档的理由**：版本化、暂停、回滚、审计是**运维治理面**，它与票 05 的 `REQ-0339`／`REQ-0346`
是同一批动作，应与票 05 的治理决定一起走，不由本票单独定档。

**给票 05 的硬约束**：`REQ-0339`（敏感生效动作要求新鲜二次认证）的动作面原文包含「激活新版本、
重新激活被暂停绑定、回滚，以及移除当前生效绑定或**缩改任务类型范围**」——**它不只是权限条目，
它是公共站点绑定激活的安全前提**。map Notes 里「用户倾向不做运行期权限管理」若延伸到砍 `REQ-0339`，
会同时挖空 FP-C9b。票 05 判 `REQ-0339` 去留时必须把 FP-C9b 一并计入，与已记的
`REQ-0311`／`REQ-0266`／`REQ-0346` 两簇耦合并列。

### Q3 — 剖面影响与复核口径

**复核口径**：以基线正文关键词分层筛选，而非全部 186 条平铺重看。四组关键词（任务类型面、
方向端点面、公共站点面、准入面、AREA 解析面）命中批次 0 条目 **71 条**，其中**一级候选 37 条**
（明确提及 `TASK_TYPE` 或公共站点功能）逐条读规范文本判定，**二级候选 34 条**按条目主题判定。
分层依据是「批次 0 判定是否可能因为只存在单一任务类型而不成立」——这是本票要找的那类缺陷，
与其他类型的剖面缺陷（例如某标识符零命中但与任务类型无关）分开处置。

**表达形态**：改 `FullProductCluster` 与 `ClusterBasis` 列，**并新增第 11 列 `Batch0FormNote`**，
写明「批次 0 的判定在什么形态下成立、完整产品差什么」。348 行逐条一行的零遗漏口径不变。
新增这一列的理由是：单改簇归属会丢失「MVP 剖面当时的判定没错，是形态变了」这个信息——而这恰恰是
本图已经踩到四次的坑，值得在剖面里留痕给票 09 与票 10。

**改判结果**（`evidence/full-product-implementation-profile-draft.tsv`，348 行不变，
新 SHA-256 `09cb9c912cff4aa9cc3f01d2f07206453449576f8dd6450b2164e213dae9e765`）：

| 簇 | 变化 | 条数 |
| --- | --- | --- |
| `FP-B0` 批次 0 | 186 → **167** | −19 |
| `FP-C9a` 六类任务执行与公共站点绑定 | 新建 | **8** |
| `FP-C9b` 公共站点绑定运维治理 | 新建 | **9** |
| `FP-C2` 多车与多任务调度 | 10 → **11**（+`REQ-0205`） | +1 |
| `FP-C4` 空闲返回与等待点 | 8 → **9**（+`REQ-0204`） | +1 |

**本图待排期的条目总数由 62 条增至 81 条。**

另有 **4 条留在批次 0 但加了形态注记**：`REQ-0190`（依赖六类，`agvId × taskType` 在单类型下退化为
常量维度）、`REQ-0191`（AREA 执行白名单退化为 `Area.StartsWith('N')` 硬编码前缀）、`REQ-0193`
（票 11 的跨图判定不受影响，但「按 `TASK_TYPE` + `mapId` 配 `FixedTaskStation`」这一半零实现）、
`REQ-0199`（范围边界声明而非功能条目，归属正确，但它列举的四项配置面中三项零命中）。

### Q4 — 协议影响（输出清单给票 06，本票不改 schema）

四处焊死，全部 breaking：

| 位置 | 现状 | 本票的建议取值 |
| --- | --- | --- |
| `envelope.schema.json:14` 等 56 个文件、58 处 | `profileId` `const "WIRE_TO_GATE_MVP"` | **改名**。解除单类型后这个名字名不副实；协议 v2 本就一次性 breaking，趁票 06 那一次改完 |
| `CurrentStopWorklistSnapshot.schema.json:87-91` | `workType` `const "WIRE_TO_GATE"` | 解除为六值 enum，**用 MES 原始字面值** |
| `CurrentStopWorklistSnapshot.schema.json:92-98` | `stopRole` enum `["PICKUP","GATE"]` | **拆开**：`["PICKUP","DROPOFF"]` + 独立的站点功能字段取 `REQ-0324` 五值 |
| `UpcomingStopPlanSnapshot.schema.json:75-81` | `legType` enum `["TO_PICKUP","TO_GATE"]` | 同理改 `["TO_PICKUP","TO_DROPOFF"]` |

**枚举值用 MES 原始字面值**（`DIE_TO_WIRE_STAGING`、`DIE_TO_OVEN`、`WIRE_TO_GATE`、
`WIRE_TO_OPTICAL`、`STAGING_TO_WIRE`、`WIRE_TO_NITROGEN`）：`REQ-0003` 说正式 SQL 是六类任务的唯一
查询原稿、不得复制会漂移的副本，自己起名等于凭空造一层需要同步维护的映射。

**`stopRole` 必须拆**：它现在混了两个正交概念——停靠的业务角色（取货/卸货）与站点的功能身份
（机台/关卡）。`STAGING_TO_WIRE` 方向反转后，`GATE` 既不是它的终点也不是它的角色，硬凑只会让
枚举成为六类端点组合的笛卡尔积。

服务端侧的联动：`ProtocolCandidateIdentity.cs:6` 的 `const string ProfileId`（强制点三处：
`OnboardMessageProcessor.cs:479`、`:498`、`WireToGateStore.cs:2012`）。另发现一处**代码事实**：
`appsettings.json:9` 的 `ProtocolCandidate.profileId` 在 `src/` 内**查不到任何绑定或读取**，
代码一律用编译期常量——**这两份值可能静默漂移**。归票 06 或实施图，本票只记录。

### Q5 — `STAGING_TO_WIRE` 与其余四类分批

**分两批。**第一批：`WIRE_TO_GATE`（已有）+ 四类同方向（`DIE_TO_WIRE_STAGING`、`DIE_TO_OVEN`、
`WIRE_TO_OPTICAL`、`WIRE_TO_NITROGEN`）。第二批：`STAGING_TO_WIRE`。

**分批依据不是省事，是风险隔离。**同方向四类与 `WIRE_TO_GATE` 的形状完全一致——AREA 机台取货、
固定站卸货，放开它们等于删一个谓词 + 把终点标量换成按类型的映射。`STAGING_TO_WIRE` 反方向，
要做的是**方向中立化**，而其中一处会静默出错：

`MapStationResolver.cs:52-71` 的 `BuildRouteEvidenceId(catalog, pickup, gate, area, eqp)` 规范串按
**pickup 在前、gate 在后**拼接（`:59-67`）。两个参数同类型，**位置互换编译期完全静默**，但哈希会变 →
`RouteEvidenceId` 变 → `WireToGateStore.cs:1841` 的幂等重放相等比较失配。把它和「多四类任务类型」
混在一批里，出问题时分不清是哪一半引起的。

代价是 plan/runtime 加字段那次迁移要分两次准备，可接受。

### Q6 — 批次归属与不变量判定

**同方向四类是纯增量**，不推翻任何一条不变量：每条 Demand 仍是两段固定行程（I3 不动）、占用仍由
Demand 引起（I1 不动）、不需要多车（I2 不动）、不引入站点独占（I4 不动）、车载仍只读（I5 不动）。
它的合法增量形态是「在既有 fail-closed 资格链上放宽一个谓词」，正是票 02 定义的两种之一。

**`STAGING_TO_WIRE` 是重构类**，推翻新认下的 **I6**。

**认下第六条架构不变量 I6：站点任务类型准入必在装货腿检查并冻结。**

代码强制点：
- `WireToGateStore.cs:795-800` 明文 `"Only LOAD may carry a complete station/task admission identity."`
- 准入决策快照只在 LOAD 路径冻结（`WireToGateStore.cs:852-871`，键 `SlotOperationAttemptId`）
- UNLOAD 发布**不传**准入参数（`JourneyRuntimeEngine.cs:751-765`）
- 而 `StationTaskTypeAdmission` 的键是**站点 × 任务类型**（`ControlServerDbContext.cs:116` 复合主键），
  站点侧是 AREA 机台站——准入检查发生在 `route.PickupStationId` 上（`JourneyRuntimeEngine.cs:234-239`、
  `:793-798`、`:721-722`）

`STAGING_TO_WIRE` 下 AREA 机台站是**卸货端**。准入该查的那一腿，恰恰是被代码禁止携带准入身份的
那一腿。这不是参数顺序问题，是一条隐含契约。

**认下 I6 的理由**：票 02 的排序规则是「每条增量不早于它所依赖的那条不变量的推翻」。不认 I6，
`STAGING_TO_WIRE` 就是一条无依赖的普通增量，票 09 可能把它排得很前，而它实际上要先重做准入归属。
**不认这条不变量，票 09 就拿不到正确的排序输入。**

`CONTEXT.md` 里 `AllocationArchitectureInvariant` 的原文是「完整产品语境下**已识别**五条」——
措辞不是穷举封闭的，因此这是补充识别而非推翻票 02。这也是本图第二次发现票 02 的判据集不完整
（第一次是票 02 自己查出 B2 无需求条目载体）。票 02 决议已加修订说明。

**排序位置**：FP-C9a 与 B2（多车）**正交**，可并行；它不依赖多车，多车也不依赖它。
但 FP-C9a **必须先于** `STAGING_TO_WIRE` 那一批，且 `REQ-0204` 归 B4 后，B4 的落地必须覆盖公共业务点。

### Q7 — 验收边界的输入（给票 08）

**验收期只有 `WIRE_TO_GATE` 一类能在现场真实触发。**其余五类的固定端点（派工待送、烘箱、三光、
氮气柜）当前不在 `mapId` 25 的 206 个站里，按 `REQ-0335` 它们会被正确地挡在投运之外。

**因此票 08 要为 FP-C9a 定的是「机制正确性」的验收出口，不是「六类都跑通」**：

1. **fail-closed 的正确拒绝**：为一个缺绑定的 `TASK_TYPE` 提交 Demand，证明它被 `REQ-0335` 挡住
   且原因精确。这条能在现场取到证据。
2. **绑定完备时的正确放行**：只能靠双 Fake 联调或在现场补一个测试绑定取证。
3. **`REQ-0187` 唯一性跨类型生效**：需要构造同一 AREA 在两个 `TASK_TYPE` 下出现的观测，
   现场自然发生的概率取决于工序排布，可能需要造。

**注意这与票 14 的 `证据受限实施` 不是一回事**：这里的证据不可得是**现场尚未测绘**造成的，
补测绘后无需改代码即自动可取证；而条目本身是完整实现，门禁两侧都能验证（只是放行侧要靠联调）。
**票 09 与票 10 不得把 FP-C9a 归入 `证据受限实施`、延后或范围外。**

### Q8 — 与票 03 已定四条的衔接

四条**实施形态都不需要改**，但各有一处补充：

- **`REQ-0202`（任务类型初始优先级带）**：`STAGING_TO_WIRE` 单独处于最高初始带、其余五类同处普通带。
  本票确认它随六类成为活代码。**分批的影响**：第一批（五类）全部落在普通带，优先级带在第一批**没有
  可观测行为**——最高带是空的。这条的现场验收要等 `STAGING_TO_WIRE` 那一批，票 08 须知。
- **`REQ-0203`（防饥饿阈值按 DispatchZone 现场标定）**：`DispatchZone` 按 **AREA 归属**划分
  （`REQ-0191`），与 `TASK_TYPE` **正交**。当前 `appsettings.json:55` 的
  `dispatchZone: "MAP-25-WIRE_TO_GATE"` 把任务类型编进了分区名，那是 MVP 的命名产物、不是模型要求。
  六类共用同一套分区，**分区不按任务类型重划**。分区名是否改名属实施图，改名会牵动
  `allowedDispatchZones`、`admissionPolicyDeploymentId` 与既有证据。
- **`REQ-0189`（`SublotTaskTypeConflict`）**：确认因本决定成为活代码——单类型下同一 SUBLOT
  不可能命中多类，该分支永假。它与 `REQ-0152`（MesIngest 侧的同一件事）是被剖面劈开的一对；
  `REQ-0152` 留批次 0 是对的（MesIngest 摄取六类，那侧确已实现）。
- **`REQ-0190`（`agvId × taskType` 表）**：票 03 已判它归 B2 的多车工程量。本票补充：它**同时**依赖
  六类——单一任务类型下 `taskType` 是常量维度。两个依赖都满足前，这张表没有可配置的内容。

## 三、对其他票据的影响

| 票据 | 影响 |
| --- | --- |
| **票 05**（治理面）| **新增硬约束**：`REQ-0339` 是 FP-C9b 的安全前提，砍它会同时挖空公共站点绑定治理。FP-C9b 的 9 条与 FP-C7 的 6 条同批判档 |
| **票 06**（协议 v2）| 四处 breaking 的清单与建议取值见 Q4。`stopRole`／`legType` 的拆分与票 03 说的「不因 B3 而改」不冲突——理由不同，是六类端点功能多样化 |
| **票 12**（等待点与 B4）| `REQ-0204` 已并入 FP-C4。**B4 的落地形态必须同时覆盖公共业务点独占，不能只做等待点** |
| **票 08**（验收边界）| Q7 的三条验收出口；`REQ-0202` 的优先级带在第一批不可观测 |
| **票 09**（批次与依赖）| 待排期条目 62 → **81**；I6 是新的排序依据；FP-C9a 与 B2 正交可并行，但必须先于 `STAGING_TO_WIRE` 批 |
| **票 10**（汇编）| 348 行剖面新增第 11 列；新增两个簇编号；`REQ-0298` 冲突（见下）必须在汇编前有结论 |
| **票 03**（已闭）| `REQ-0205` 并入 FP-C2，落在已定的 B2 全开范围内，定案不变，加注记即可 |
| **票 02**（已闭）| 决议加修订说明：识别第六条不变量 I6 |

## 四、新开票据：`REQ-0298` 与 `RouteGraphSnapshot` 的冲突

**本票复核的副产品，超出本票范围，另开票 15。**

`REQ-0298`（批次 0）原文：「当前产品只同步 Map/Station 目录，不同步本地路网。……**Edge、几何路网、
本地最短路与动态交通状态均不进入本产品事实**；派车可达性和路径成本继续使用已批准的实时 RIoT
RouteCost 证据边界。」

票 14 定下的 `RouteGraphSnapshot` **四项全中，逐字冲突**：取全图边表（Edge）、本地跑最短路、
同步运行态移除集（动态交通状态）、可达性权威迁到自建图。`14-answer.md` 全文未提及 `REQ-0298`。

这不能用票 11 那种「判 out of scope」化解——票 14 已把引擎定为完整产品的**硬依赖**（快照陈旧即本轮
不派车），它在 Destination 之内。这是 map 的「完整产品是否需要新的需求基线版本」那条迷雾的**第二个
具体实例**，而且是第一个可能真的需要走需求变更流程的。归票 15。

## 五、未证明项

1. **装片机台的 AREA 前缀。**`JourneyRuntimeEngine.cs:177-180` 有
   `if (!candidate.LiveMesFields.Area.StartsWith('N')) → OUT_OF_SCOPE_AREA`，而 `mapId` 25 上 11 个
   AREA 全部 N 开头。**若装片机台的 AREA 不是 N 前缀，`DIE_TO_WIRE_STAGING` 与 `DIE_TO_OVEN` 两类
   在这一关就被挡掉，与固定端点在不在图上无关。**这决定 `REQ-0191` 是否也要移出批次 0。
   现场事实，本工作区查不到。
2. **`WIRE_TO_NITROGEN` 分支的 SQL 内部不一致。**注释写「焊线1机台 → 固定氮气柜」（`query.sql:195`），
   但 WHERE 条件筛的是 `step = '焊线2'`（`query.sql:223`）。属工厂 IT 的 SQL，8005 无权改；
   若该分支的语义与注释不符，`REQ-0184` 的方向判定不受影响（AREA 仍是起点），但现场验收要注意。
3. **`REQ-0157` 的身份绑定断裂。**该条绑定的 commit `420c96c2f961aaffa42a5443fa42e6585b1c993f`
   在 `8005-mes-ingest` 对象库中**不存在**（2026-09-02 拆仓时历史被重写），且基线记的路径
   `mes/queries/mes-task-union/` 与实际路径 `queries/mes-task-union/` 不一致（README 里还有第三个
   路径 `service/queries/mes-task-union/`）。**SHA-256 仍完全吻合**，故内容身份未断，断的是 commit
   指针与路径。与票 10 悬着的 `requirements-baseline-v1.0.0` tag 缺失问题同类，一并归票 10。
4. **其余五类被丢弃的量不可观测。**控制服务端对它们零记录，无法用「放开前后的执行量差」验证放开
   是否符合预期。若需要这个基线数，要在放开前先加一段观测——属实施图。

## 六、复核副产品（与任务类型无关，点名给票 09）

以下标识符在控制服务端 `src/` 零命中，均属批次 0 条目引用的能力，**与本票的任务类型问题无关**，
本票不改判它们，仅记录以备票 09 复核：

- `TransportDemandSuppression`（`REQ-0155` 本地取消抑制）
- `LoadPreparationAlert`（`REQ-0186` 容量规则未覆盖告警）
- `UnassignedDemandBacklog`（`REQ-0205` 任务老化队列）
- `AreaEqpUniquenessMonitor`（`REQ-0187` 独立唯一性监视器，当前是从 MES 观测行推导）
- `DispatchZoneAreaAssignment`（`REQ-0191` AREA→分区映射，当前是 N 前缀硬编码）
- `EnRoutePickupDeliveryDelay`（`REQ-0199`／`REQ-0205` 分区顺路延迟参数）

**「零命中」不等于「未实现」**（可能换了命名），但六个标识符全部零命中、且都指向配置与告警面，
提示批次 0 的判定在这一片可能整体偏松。这是「假定还有第五次退化」的最强线索。
