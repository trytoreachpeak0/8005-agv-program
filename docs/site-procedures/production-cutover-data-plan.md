# 生产切换数据方案（切换-03，program#170）

本文回答规格 `docs/specs/full-product-scope-and-sequence-v2.md` 第 14 节第 6 项：切到 v2（v3 协议）时，需求与在途订单怎么处理，硬件事实、已批准参数与逐仓核对结果怎么进 v2 的新库，三台车车载端的本地状态怎么清，回滚时数据怎么办。

**它不另起一套顺序。**切换的总步骤是 control-server PR #677（cs#564）分支上的 `docs/production-cutover-mode-plan.md`（下称「cs#564 方案」），本文的步骤号都写成「cs#564 第 N 步」，阶段沿用它的 S1（只有 `agv02`）、S2（加 `agv01`）、S3（加 `agv03`，起 `DIE_ATTACH` 区）、S4（放开一车多需求）。本文只补 cs#564 方案里「以 program#170 为准」的数据部分。

文中「读到的」指在下列提交上实读的代码与文件：control-server `fp/v2-impl@4d7e0e07`（含 cs#44 光幕极性、cs#609 持货 5 分钟、cs#669 切换定义）、control-server `ControlServer_MVP@670bdd45`（只读代码，不碰 MVP 服务与库）、onboard-hmi `w2g/fp-v2-impl` 与 `w2g/field-agv01-6b8a0b0`、`8005-workspace@origin/main`；「推的」指由读到的事实推出、没有实测的结论。

标记沿用 cs#564 方案：**【执行前问用户】**＝碰 `agv01`、factory01 上的 MVP 服务与库（含只读查询）、生产 MesIngest（工作区「Ask first」第 2 类）；**【逐次授权·现场有人】**＝会让车动或发急停（第 1 类）。

## 0. 先说结论

- **需求与在途订单不迁移**（用户 2026-10-10 定：先排空再切）。MVP 停派单、在途清零之后 v2 才开始受理；v2 用自己新库里的 `AcceptedDemands` 判「做过没有」，不看 MVP 库，所以「不重复」只能靠时间上不重叠，这一点在第 1 节论证。
- **v2 新库里的每一项受治理数据都有一条可执行的来路**，第 2.1 节逐项列出：来源、FieldOps 动词或文件、批准人、要不要现场重核。所有点名的 FieldOps 动词都在 `fp/v2-impl@4d7e0e07` 的 `tools/ControlServer.FieldOps/Program.cs` 动词表里实读确认存在。
- **硬件事实不从 MVP 库搬。**已批准的八仓硬件事实（含光幕极性新值 `UNLOCK_OUTPUT_ACTIVE_HIGH;LOCK_FEEDBACK_LOCKED_HIGH;LIGHT_CURTAIN_OBJECT_LOW`）写在 v2 代码里（`src/ControlServer.Domain/SlotConfigurationModels.cs:153`），由 `seed-approved-facts` 与 `bind-io` 写进新库；**MVP 库里的 W1 逐仓核对结果一条也不搬**，试跑段不做逐仓核对（模拟 IO 下没有意义），生产段换新库 B 后按 `REQ-0263` 每车逐仓重新核验（`verify` → `release`）。
- **三车车载端的日志簿与发件箱在同一个文件里**（`%LOCALAPPDATA%\SQCD\8005AGV\onboard-journal.db`，车上交互用户名下），规则是「先让原主人收完，再整目录改名留存」。`agv01` 的原主人是 MVP，所以它的发件箱必须在 MVP 停服之前送完；`agv02`、`agv03` 的原主人是 v2 旧库，必须在 cs#564 第 7 步停旧库之前送完。
- **发现一个 cs#564 方案的缺口**：它的备份清单（第 7 节）写 `agv01` 的 `C:\8005\OnboardHmi`「含日志簿、发件箱」，但读到的事实是日志簿不在安装目录里，而在 `%LOCALAPPDATA%\SQCD\8005AGV\`；而且现场线与 v2 用**同一个路径、同名的四张表**。漏改名的话，v3 车载端会直接打开 MVP 时代的日志簿：MVP 欠送的结果被 v2 当历史行确认后丢掉，旧计划快照与新库同号不同内容被拒（`SNAPSHOT_REVISION_CONTENT_CONFLICT`）。第 3 节把它写进步骤，回滚时也要把这个目录换回去。
- **用户 2026-10-13 已定第 6 节 U1～U8 全部按建议**（https://github.com/trytoreachpeak0/8005-agv-program/issues/170#issuecomment-6138103462），`agv03` 在 S1、S2 停在站 222（第 3.4 节）。
- 下午装机直接用的是**第 2.2 节（试跑段新库 A 的导入单）和第 3 节（三车车载端）**。

## 1. 需求与在途订单（用户已定：先排空再切，不迁移数据）

操作步骤就是 cs#564 第 2～4 步，本节不重写，只补它留给本票的数据部分。

### 1.1 怎么停 MVP 派新单

读到的：MVP 的两道闸门 `JourneyRuntime.enabled`（受理）与 `RiotCreateDispatch.enabled`（建单、动车）只在启动时读，改了要重启服务，没有不停服务的运行时开关（`8005-workspace` 的 `remote-ops/factory-server/scripts/control-server/Set-JourneyRuntime.ps1` 说明，cs#564 方案第 1 节表）。所以停派单＝cs#564 第 2 步：等 `agv01` 当前这趟 `Completed`，用 `13-close-gates-when-idle.ps1` 关两道闸门（它在服务器上 250 ms 盯着，完成即停服务再写 `-Off`）。停服务的影响：MVP 停服期间 `agv01` 没有任何服务端，车停在站上不动；不能在装货后、卸货前关。【执行前问用户】

### 1.2 怎么确认在途为零（三处都为零才算排空）

这是 cs#564 第 3 步的判据。三处的读法如下，每一处都属于【执行前问用户】（读 MVP 库、读 `agv01`）。

| 处 | 看什么 | 为零的含义 |
| --- | --- | --- |
| MVP 库 `C:\ProgramData\8005\ControlServer\data\controlserver.db`（停服后复制一份再读，不读运行中的库） | `JourneyRuntimes` 里非终态的旅程、`AcceptedDemands` 里没有对应完成或抑制的需求（对照 `TransportDemandCompletions`、`TransportDemandSuppressions`）、`OrderIntents` 里未结的 RIoT 订单意图、`VehicleDispatchLeases` 里仍持有的车辆租约、`ProtocolOutbox` 里 `AcknowledgedAt IS NULL` 的行 | 没有受理未完成的需求、没有未终结旅程、没有未结订单、没有欠车载端的消息。表名读自 `ControlServer_MVP@670bdd45` 的 `ControlServerDbContext.cs`；状态列的具体取值在执行当天按同一提交的代码核一遍再写查询 |
| RIoT | `agv01`（`riotId=58`）名下没有未结订单 | 车不会被一张遗留的单带走 |
| `agv01` 车载端 | 日志簿 `WireToGateDurableOutbox` 里未确认且未放弃的行为 0；`WireToGateRecoveryState.ContentJson` 里 `loadsOnBoard` 为空（查询见第 3.2 节） | 车载端不再欠 MVP 任何结果，车上没有在载货物 |

任何一处不为零就停在这一步，不往下走。

### 1.3 MesIngest 侧为什么不会重复受理

- 读到的：MesIngest 只读、没有认领语义，MVP 与 v2 看到的是同一份需求目录（工作区 `CLAUDE.md` v2 隔离表；control-server#535）。所以「不重复」不能靠认领。
- 读到的：v2 只按**自己库里**的 `AcceptedDemands` 判「已受理」（`AlreadyAcceptedCriterion.cs:7-15,35-38`、`DispatchAdmission.cs:23-25`），完全不看 MVP 库，也不依赖 MES 侧状态变化。
- 推的：所以 MVP 已受理、尚未完成的需求，v2 新库看来就是一条全新的需求，会再受理一次。**不重复的唯一保证是时间上不重叠**：
  - 时点甲：MVP 两道闸门关闭、服务停止，且第 1.2 节三处为零（cs#564 第 2、3 步；现场执行，用户授权，调度把原话记进 cs#564）。
  - 时点乙：v2 第一次以运行时打开的定义启动、读生产 MesIngest（cs#564 第 11 步）。
  - 要求：甲早于乙，中间没有 MVP 已受理未完成的需求。cs#564 第 8 步首装的是运行时关的定义，第 11 步之前 v2 不读需求，顺序天然成立；第 1.2 节的三处为零就是甲成立的证据。
- 已完成的需求：MVP 已经送完的需求，若 MES 目录里还挂着（实物已动、MES 尚未更新），v2 会把它当新需求再送一次。推的：MVP 送完时实物已到站，MES 侧通常随实物移动更新；但这依赖 MES 的行为，代码里没有保证。**缺口**：排空完成到 v2 开运行时之间，没有一个机制核对「MVP 刚做完的需求已离开目录」。建议见第 6 节 U7。

### 1.4 回滚

步骤见 cs#564 方案第 7 节；回滚时数据怎么办见本文第 4 节。

## 2. 硬件事实与已批准参数

### 2.1 逐项清单

「重核」一列回答 `REQ-0263`：硬件相关的事实（仓位模型、IO 绑定、核对结果）只能由现场整车逐仓核验建立，不能靠搬记录。下表里**没有一项的来源是 MVP 库**。

| # | 数据 | 来源 | 进 v2 新库的方式 | 批准人与出处 | 重核 |
| --- | --- | --- | --- | --- | --- |
| 1 | 已批准八仓硬件事实（仓位模型 `8005-eight-slot` v1：DO1–DO8 开锁、DI1–DI8 锁反馈、DI9–DI16 光幕、500 ms 复位、极性新值） | v2 代码内置 `ApprovedSlotHardwareFacts`，极性 `SlotConfigurationModels.cs:153`（cs#44 合入，`4d7e0e07`） | FieldOps `seed-approved-facts --database <库>`；幂等 | 已批准（`REQ-0267`；极性由 cs#44、hmi#294 定）。不需要再批 | 它是被核的对象，本身不「核」；生产段对每车按它逐仓核验（第 9 行） |
| 2 | 每车 IO 绑定 | 同上 `ApprovedSlotHardwareFacts.IoBindings`；车上报的声明永不采信（`REQ-0258`，`Program.cs` `BindIoAsync` 注释） | FieldOps `bind-io --database <库> --agv <agvId>`，三车各一次。先跑第 1 行，否则报 `run seed-approved-facts first` | 同上 | 试跑段不核；生产段核（第 9 行） |
| 3 | 车队表（三车专车专用、`zones`、`allowedTaskTypes`） | PR #676 切换定义 `instance-factory01-v2.cutover-two-zones*.json`，按阶段裁剪（cs#564 第 7a 步、第 8 节表） | 不在库里，是部署配置：19 号脚本带 `-ProductionCutover` | 用户 2026-10-10（专车专用）、2026-10-12（区名）；每份定义的 `productionCutover.approvalRecord` 写执行当天的授权 | 否 |
| 4 | 等待时长：离站 `00:05:00`、持货 `00:05:00` | 切换定义 | 部署配置，19 号脚本 | 用户 2026-10-13（cs#564 D9） | 否；装后实读 `C:\Program Files\8005 AGV\ControlServer.V2\appsettings.Production.json` |
| 5 | `REQ-0302` 两个值（同步周期 `00:00:30`、最大未确认 `00:05:00`） | 切换定义 `mapStationCatalog` | 部署配置，19 号脚本 | 用户 2026-10-09（cs#531） | 否 |
| 6 | 准入策略（站名 × 可执行任务类型，版本 6） | 切换定义 `admissionPolicyVersion: 6` | 新库上第一次运行时打开时自动首绑（cs#669 README「实例、数据目录……都不变」） | 已批准版本，`AdmissionPolicyVersionGuardTests` 历史表 | 否 |
| 7 | RIoT 26 号图站点目录（导入等待点、名册、站点绑定时要用的 `--catalog`） | RIoT 只读 GET | `scripts/field/Export-RiotStationCatalog.ps1`，每次换库现取 | — | 每次现取，不沿用旧文件 |
| 8 | 任务类型站点绑定（六类：210、217、218、219、220、221） | 包内预置 `task-type-stations.map-26.settings.json`（空库上装成第一版）＋ `scripts/parallel/task-type-stations.map-26.candidate.json` | FieldOps `activate-task-type-stations --database <库> --input <candidate> --catalog <目录>`，先 `--dry-run`。不重新激活，生产来源下没绑的类型判 `TASK_TYPE_BINDING_MISSING`、一单不派 | 用户 2026-10-10，`siteVerificationRef` 为 `MAP-26-<类型>-SITE-20261010` | 地图站点的用途核对，不是车辆硬件。建议沿用，见第 6 节 U1 |
| 9 | 逐仓核对结果 | **不搬。**MVP 库里的 W1 结果（2026-09-13，做在生产 v0.3.0 库上）作废 | 生产段：每车现场逐仓核对、填记录（模板 `scripts/field/templates/vehicle.json`），FieldOps `verify --database <库> --record <记录.json>`，再 `release --agv <agvId> --model <slotModelVersionId>`，`status` 回读 `ready=true`。抽样会被整批拒绝 | 现场核对人签记录，证据进 `evidence/field/<日期>-W3-S0-<车>/`（cs#565） | **必须**，整车逐仓（`REQ-0263`） |
| 10 | 等待点登记（214、215、216） | `docs/field/waiting-points-map26.csv`（control-server 仓，10-11 两次换库用的同一份） | FieldOps `import-waiting-points --database <库> --input <csv> --catalog <目录>`，先 `--dry-run`。**必须在运行时打开之前导入**：车队表有 N 台车而等待点不足 N 个时，服务启动被 9401 `WAITING_POINTS_FEWER_THAN_VEHICLES` 拒绝（10-11 现场踩过，`evidence/field/20261011-W2-prep6-two-car/12-v2-start-failed-log.txt`）。三车三点，正好够 | 用户（`REQ-0289`，批次 8）；出处执行前从 control-server `docs/field/batch-8-waiting-point-registration.md` 核 | 否 |
| 11 | 充电名册 | `docs/field/charger-roster-map26-station211.json`（站 211、进出 212）或 `charger-roster-empty.json` | FieldOps `import-charger-roster --database <库> --input <json> --catalog <目录>` | 用户；文件里的 `approvalBasis` 写的是 09-29 开窗授权。切换后登记 211 要新的一句授权，见第 6 节 U3 | 否 |
| 12 | 充电策略 v1（`ChargingPolicyVersion`；20／30／80，内容 SHA `5d34c605…`） | `docs/field/charging-policy-map26.json` | FieldOps `import-charging-policy --input <json> --fleet <vehicleKey,…>` → `approve-charging-policy` → `activate-charging-policy`；`charging-policy --fleet …` 回读每车 `commissioned=true` | 内容：用户 2026-09-29（cs#400）。每个新库都要重新批准一次，批准记录写授权原话，见第 6 节 U4 | 否 |
| 13 | 分区归属表（含开门侧列 `slot_position`） | v2 工作区 `field-prep/`（不在 git）：S1、S2 用 `area-assignments-N-WIRE_BONDING.csv`（217 行，SHA-256 `daa29557…`）；S3 起用 `area-assignments-merged-N-T.csv`（316 行，SHA-256 `d0414e28…`） | 拷到 `D:\zhengyushao\control-server-v2-ops\` 并核哈希；先离线比区名（`Test-ParallelInstance.ps1 -AreaAssignmentPath`），再 FieldOps `import-area-assignments --database <库> --input <csv> --dry-run`，最后正式导入。**整表替换**；前提是该区已由派车轮写进 `DispatchZoneVehicles`，否则 `DISPATCH_ZONE_NOT_FOUND`（cs#669 README） | 用户 2026-10-12（区名，「N开头的都是WIre Bonding的，T开头的都是Die attaching里的」）；T 区开门侧由用户填（`area-assignments-T-filled-by-user.csv`） | 否 |
| 14 | 每区参数 `REQ-0198`（途中追加最大增量）、`REQ-0203`（防饥饿阈值） | 试跑段：**不导入**（用户已定 `REQ-0198` 为 0 或不导入；cs#219 未标定） | 需要时 FieldOps `import-dispatch-zone-parameters --input <csv>`，整表替换，两个区写在同一张表；回读 `dispatch-zone-parameters` | 用户（cs#219） | 否 |
| 15 | 现场人员角色 | `D:\zhengyushao\control-server-v2-ops\field-operator-roles.json`（定义里的路径） | 不在库里，沿用运维目录的文件 | 已有 | 否 |

不需要的动词：`enable-gate` 只写一条审计、不拦车（`Program.cs` `EnableGateAsync` 注释），本方案不用；`accept-map-name` 只在启动日志报地图名基线不符时用；`release-station-exclusivity`、`rollback-task-type-stations` 等是故障处置用的，不属于导入。

### 2.2 试跑段：新库 A 的导入单（下午装机用）

时机对齐 cs#564：第 7 步（V2 数据目录改名、建空目录、**不起服**）→ 第 8 步（19 号以切换模式首装 S1 运行时关的定义，服务首次启动时自动建表）→ **本单第 1～8 条（即 cs#564 第 10 步）** → cs#564 第 11 步（换装运行时开的定义）→ 本单第 9～11 条（cs#564 第 12～14 步）。

FieldOps 必须是与服务端同一提交构建的那一份（control-server `docs/field/batch-8-waiting-point-registration.md`「部署机上的工具从哪来」），放在 `D:\zhengyushao\control-server-v2-ops\fieldops-<提交前 8 位>\`。中文 `agvId` 经 ssh 传会乱码，命令写进 UTF-8 脚本再在服务器上执行（10-09 现场记录）。每条命令的输出整段存进证据目录。

| # | 命令（`--database C:\ProgramData\8005\ControlServer.V2\data\controlserver.db` 省略不写） | 判据 |
| --- | --- | --- |
| 1 | `Export-RiotStationCatalog.ps1` 导出 26 号图站点目录 | 读到 217 个站，文件路径记下，后面 `--catalog` 用它 |
| 2 | `seed-approved-facts` | `outcome=OK`、`slotCount=8`；记下 `slotModelVersionId` |
| 3 | `bind-io --agv 老厂前线新多仓位2`；`bind-io --agv 老厂前线新多仓位1`；`bind-io --agv 老厂前线新多仓位3` | 各 `boundSlots=8`。三车一次绑完，换阶段时不必再回来做；绑定只是库里的行，不碰车 |
| 4 | `activate-task-type-stations --input task-type-stations.map-26.candidate.json --catalog <目录> --dry-run`，无违例后去掉 `--dry-run` | 六类都在 `changes` 里；回读 `task-type-stations` 当前版本含六类 |
| 5 | `import-waiting-points --input waiting-points-map26.csv --catalog <目录> --dry-run`，再正式 | `coverage.sufficient=true`，214～216 三点 |
| 6 | `import-charger-roster --input <名册> --catalog <目录>`。按 U3 已定：用 `charger-roster-map26-station211.json`，`approvalBasis` 改写为切换授权的原话出处 | 回读 `charger-roster`：站 211、进出 212 |
| 7 | `import-charging-policy --input charging-policy-map26.json --fleet <当前阶段车队的 vehicleKey>` → `approve-charging-policy`（批准依据引用 U4 的授权：https://github.com/trytoreachpeak0/8005-agv-program/issues/170#issuecomment-6138103462） → `activate-charging-policy` | `charging-policy --fleet …` 回读 `activeVersion=1`、每车 `commissioned=true`。换阶段加车后再回读一次，新车不是 `true` 就重做第 7 条 |
| 8 | `status` | 三车都是 `SLOT_CONFIGURATION_NEVER_VERIFIED`、`slotsMissingBinding=[]`。试跑段就停在这个状态（不做逐仓核对） |
| 9 | （cs#564 第 11 步之后）`import-area-assignments --input area-assignments-N-WIRE_BONDING.csv --dry-run` | 不报 `DISPATCH_ZONE_NOT_FOUND`、`errorCount=0` |
| 10 | 每区参数：**不导入**（第 2.1 节第 14 行） | `dispatch-zone-parameters` 回读为空 |
| 11 | `import-area-assignments --input area-assignments-N-WIRE_BONDING.csv` | `entryCount=217`；回读 `area-assignments`。**导入后表里的 AREA 立刻可被受理** |

换阶段（cs#564 第 16a 步）时：S2 不改归属表；S3 用 `area-assignments-merged-N-T.csv` 重做第 9、11 条（整表替换，不要先 N 后 T 分两次导）。

试跑段的已知状态：仓位就绪判定是「从未核验」。读到的：`SlotConfigurationReadinessGate.IsSlotConfigurationConfirmedAsync` 在 `src/` 里没有生产调用点，派车不看它，所以这个状态不挡试跑；也意味着生产段的逐仓重核只靠流程保证（第 7 节 G2）。

### 2.3 生产段：新库 B

对齐 cs#564 第 17～22 步：

1. 第 18 步换新库 B，库 A 改名留存（它是试跑证据）。试跑期间在库 A 里受理过的需求会被永久判为已受理，所以库 A 不能带进生产（cs#564 方案第 5 节）。
2. 第 19 步装生产段 S1 定义后，按第 2.2 节第 1～8 条**原样重做**。第 7 条重新批准充电策略；第 6 条名册按 U3 的结论。
3. 第 20 步各车 IO 从模拟器切回真模块（`09-switch-io-module.ps1`）。
4. **第 21 步逐仓重核**：每车按第 2.1 节第 9 行 `verify` → `release` → `status` 回读 `ready=true`、`slotsMissingVerification=[]`。哪台车没过就不进它所在的阶段。不使用 MVP 库里 W1 的任何记录。
5. 然后第 2.2 节第 9～11 条（归属表），每区参数按用户届时的批准（S1～S3 `REQ-0198` 仍为 0 或不导入，S4 导入批准值，cs#564 方案第 8 节）。

## 3. 三车车载端的本地状态

### 3.1 车上有什么

读到的（onboard-hmi `w2g/fp-v2-impl` 与 `w2g/field-agv01-6b8a0b0` 的 `SqliteWireToGateJournal.cs`、`Configuration.cs`）：

- **日志簿与发件箱是同一个 SQLite 文件** `%LOCALAPPDATA%\SQCD\8005AGV\onboard-journal.db`（车上交互用户名下，不在安装目录 `C:\8005\OnboardHmi` 里），四张表：`WireToGateJournalMetadata`（日志簿纪元）、`WireToGateRecoveryState`（含 `loadsOnBoard`）、`WireToGateDurableOutbox`（发件箱）、`WireToGateAppliedJourneySnapshots`（已应用的计划快照）。
- **`agv01` 的现场线与 v2 车载端用同一个路径、同样四张表。**所以 `agv01` 换装 v3 车载端时若不先改名，新程序会直接接着用 MVP 时代的那份。
- 本地仓位配置 `active-slot-configuration.json` 是相对路径（`Configuration.cs:342`），推的：随进程工作目录落在安装目录里；它是服务端下发的副本（`REQ-0258`，服务端是唯一权威），`bind-io` 之后由新库重新下发，不需要单独清。

为什么要清：日志簿绑着某一份服务端库。换库后计划快照修订号从 1 重来，旧日志簿里同号不同内容的快照会让车载端拒收（`SNAPSHOT_REVISION_CONTENT_CONFLICT`，10-09 现场踩过）；发件箱里欠旧主人的结果若发给新库，会被回 `DurableAck`、记成历史行，车载端随之丢掉这一行，原主人永远收不到（cs#481 的裁定）。

### 3.2 只读检查（每车）

车载端停栈（`10-start-onboard-stack.ps1 -SshAlias <车> -Stop`）后，在车上以只读方式开库查三项：

```sql
-- 欠送：必须为 0
SELECT COUNT(*) FROM WireToGateDurableOutbox WHERE Acknowledged = 0 AND AbandonedReasonCode IS NULL;
-- 分组记录（进证据）：已确认、已放弃各多少
SELECT Acknowledged, AbandonedReasonCode, COUNT(*) FROM WireToGateDurableOutbox GROUP BY 1, 2;
-- 车上在载货物：loadsOnBoard 必须为空或 null
SELECT ContentJson FROM WireToGateRecoveryState WHERE Id = 1;
```

以往现场用车上的 Python 读这几张表（`evidence/field/20261011-W2-prep3-newdb/05-agv02-journal-before-rename.txt`）。没有专门脚本，见第 7 节 G3。

### 3.3 顺序（总原则：先让原主人收完，再停栈、核为零、整目录改名留存，最后在新库就绪后起栈）

| 车 | 原主人 | 什么时候送完 | 什么时候改名 | 对齐 cs#564 |
| --- | --- | --- | --- | --- |
| `agv01` | MVP（现场线） | MVP 闸门关、这趟 `Completed` 之后、**MVP 停服之前**：车载端仍连着 MVP，等欠送行被 MVP 确认 | MVP 停服、备份之后，部署 v3 车载端之前 | 第 3 步核为零；第 5 步备份时连同 `%LOCALAPPDATA%\SQCD\8005AGV\` 一起另存；第 9 步（S2 之前）改名后部署 |
| `agv02` | v2 旧库（今天在跑 `STAGING_TO_WIRE`） | v2 旧库实例**停服之前**：闸门关、无在途，车载端仍连着它，等欠送行被确认 | 停栈、核为零后，cs#564 第 7 步之前 | 第 7 步之前插入；第 9 步部署 v3 车载端 |
| `agv03` | v2 旧库（10-11 两车实验时连过；今天不在旧库的车队表里） | 同 `agv02`；若有欠送，按第 6 节 U6（已定）存证后改名留存、不再送 | 同 `agv02` | 第 7 步之前核查；S1、S2 期间停在站 222（第 3.4 节）；第 9 步（S3 之前）部署 |

每车的步骤（`agv01` 每一步【执行前问用户】）：

1. 确认原主人这边无在途：MVP 见第 1.2 节；v2 旧库用 20 号脚本 `-State Closed`（有未完成旅程会被拒，`GATE_CLOSE_REFUSED_IN_FLIGHT`）。
2. 车载端仍连着原主人，等发件箱送完（第 3.2 节第一条查询在停栈后读；若不为 0，起栈让它连回原主人再等，不要在不为 0 时改名）。
3. `10-start-onboard-stack.ps1 -SshAlias <车> -Stop`；确认车上没有 `SQCD*` 进程。
4. 第 3.2 节三条查询，输出进证据。欠送为 0、`loadsOnBoard` 为空，才往下。
5. 把整个 `%LOCALAPPDATA%\SQCD\8005AGV` 改名为 `8005AGV.pre-cutover-<阶段>-<日期>`（例如 `8005AGV.pre-cutover-trial-20261013`）留存，不删。`agv01` 另外按 cs#564 第 5 步把 `C:\8005\OnboardHmi` 另存。
6. 按 cs#565 部署 v3 车载端（`06-deploy-onboard-hmi.ps1 -OnboardPort 58105 -HealthPort 58107`，两个端口都要给），IO 指向模拟器（试跑段）或真模块（生产段）。`agv01` 先把 `site-agv01.json` 的 `controlServerLine` 改为 `"v2"`。
7. 新库就绪（第 2.2 节第 1～8 条做完）之后再起栈：`10-start-onboard-stack.ps1 -SshAlias <车>`（试跑段加载模拟器；`-SimulatorOnly` 以外都是起会动车的程序，按 cs#564 的标记授权）。

验证做成了：

- 车上出现新的 `onboard-journal.db`，`WireToGateJournalMetadata.JournalEpoch` 与改名留存那份不同；发件箱只有新会话产生的行。
- 车载端握手 `Ready`，服务端日志没有 `SNAPSHOT_REVISION_CONTENT_CONFLICT`，也没有收到不认识的结果而记成历史行（日志 1106／2132）。
- 服务端 FieldOps `status` 里该车 `slotsMissingBinding=[]`。

**试跑转生产（cs#564 第 18～20 步）再做一遍**：库 A 是试跑期车载端的原主人，所以要在第 17 步关闸、无在途之后、第 18 步换库 B 之前，按上面第 2～5 步对三车各做一次（改名后缀用 `pre-cutover-production-<日期>`）。

### 3.4 `agv03` 在 S1、S2 的停放点：26 号图站 222（用户 2026-10-13 定）

S1、S2 的车队表里没有 `agv03`，v2 不管它，它要停在一个不碍事的地方，直到 S3 换装三车定义。

- 什么时候停过去：cs#564 第 7 步之前，`agv03` 车载端停栈、日志簿改名之后，由用户或现场在 RIoT 上把它挪到站 222 定位（会让车动，【逐次授权·现场有人】）。
- 为什么这里不碍事（读到的）：222 不在 v2 管的任何登记里：不是等待点（214～216）、不是充电桩与进桩路径（211、212）、不是六类任务的固定站（210、217～221）。所以 v2 不会把别的车派到 222 上去。
- **要现场核的两点（推的）**：一是 10-11 的 26 号图站点目录快照（control-server `evidence/field/20261011-B10-05-map26-task-type-stations/catalog-26.json`，216 个站）里没有 222，推测是之后新建的站。第 2.2 节第 1 条导出目录时确认 222 在目录里、名字与用户说的一致。二是 v2 不知道 222 上停着车：路网引擎只看自己车队的车，`agv02`、`agv01` 的路线若经过 222 旁的通道，RIoT 层面的避让由 RIoT 负责。请用户确认 222 停车不挡 `agv02` 去 217 与 N 区、`agv01` 去 210、219、221 与 N 区的通道。
- S3 换装三车定义前：`agv03` 部署 v3 车载端（第 3.3 节第 6 步）、起栈、握手 `Ready`，此时它从 222 出发由 v2 调度（属于 S3 那次开闸的授权）。
- 生产段（新库 B）若再走 S1、S2，同样停在 222。

## 4. 回滚时数据怎么办

步骤是 cs#564 方案第 7 节。本节补数据：

1. **MVP 的库就是切换前备份的那份**（cs#564 第 4 步复制、记 SHA-256）。试跑段 MVP 停着没人动，哈希一致就不需要还原。
2. **`agv01` 车载端连同日志簿一起换回**：cs#564 第 7 节回滚第 2 步只换了 `C:\8005\OnboardHmi`。还要把车上当前的 `%LOCALAPPDATA%\SQCD\8005AGV` 改名留存（它属于 v2），再把 `8005AGV.pre-cutover-trial-<日期>` 改回 `8005AGV`。不换回的话，现场线程序会打开 v2 时代的日志簿，与 MVP 库同样同号不同内容。
3. **v2 新库不删**：停服、设 Manual、数据目录原样留存，作为切换期间的证据。
4. **对 MES 交代**：
   - 读到的：v2 对 MesIngest 只读，不写 MES（工作区 `CLAUDE.md` v2 隔离表）。所以 v2 期间没有任何东西需要从 MES 撤回。
   - 试跑段：仓位是模拟器、实物没动，v2 「完成」的需求在 MES 里仍挂着、物理上没人送（用户 10-12 已确认符合预期）。回到 MVP 后由 MVP 照常受理，正确。
   - 生产段：v2 真送过的需求，若回滚时 MES 目录里还挂着（MES 尚未随实物更新），MVP 的备份库不知道它们做过，会再送一次。MVP 代码不能改，所以只能在流程上挡：回滚前从 v2 库导出已完成需求清单（FieldOps `export-audit --stream business --format csv --output <文件> --since <切换时刻>`；推的：业务审计里有完成记录，执行前核一次导出内容够不够），MVP 开受理闸门之前逐条确认它们已离开 MesIngest 目录。读生产 MesIngest 属于【执行前问用户】。没离开的那几条怎么办，见第 6 节 U8。
   - v2 在途的单：回滚第 1 步先关 v2 闸门、等在途 `Completed` 再停（cs#564 第 17 步同法），不留在途单；做不到（例如车故障停在半路）时停在这一步问用户，不要带着在途单切回 MVP。

## 5. 要用户授权的读取

本票没有做任何下列读取。执行时由调度向用户要授权、把原话记进 cs#564 或本票：

| # | 读什么 | 为什么要读 | 属于 |
| --- | --- | --- | --- |
| R1 | MVP 库（停服后的副本）：第 1.2 节那几张表 | 证明排空（cs#564 第 3 步） | 「Ask first」第 2 类 |
| R2 | `agv01` 车上日志簿的第 3.2 节三条查询 | 证明 `agv01` 不欠 MVP 结果、车上无货 | 第 2 类（碰 `agv01`） |
| R3 | RIoT 上 `agv01`（`riotId=58`）名下的订单 | 证明无未结单 | 第 2 类（按碰 `agv01` 从严处理） |
| R4 | 生产 MesIngest 的需求目录（只读） | 生产段回滚前核对 v2 已完成需求是否已离开目录（第 4 节第 4 条）；以及 U7 的核对 | 第 2 类 |

**不需要读**：MVP 库里的 W1 逐仓核对结果、硬件事实、参数。它们一律不进 v2 新库，读了也用不上。

## 6. 用户的决定（原「用户未定」）

**2026-10-13 已定**：U1～U8 全部按下表的建议执行，用户原话「就这么推进吧」（经调度 Coordinator 10，记录在 program#170 评论 https://github.com/trytoreachpeak0/8005-agv-program/issues/170#issuecomment-6138103462）。U4 的授权即「切换期间在新库 A、B 上批准并激活与现行 v1 逐字相同的充电策略」，第 2.2 节第 7 条 `approve-charging-policy` 的批准依据两次都引用这条评论。同日用户另定 `agv03` 在 S1、S2 的停放点是 26 号图站 222（第 3.4 节）。

下表保留原建议与理由，「建议」一列即已定做法。

| # | 问题 | 建议 | 理由 |
| --- | --- | --- | --- |
| U1 | 哪些事实直接导入、哪些必须现场重核 | **直接导入**：第 2.1 节第 1、2 行（代码内置的已批准硬件事实与 IO 绑定）、第 8 行（任务类型站点绑定，沿用 2026-10-10 的站点用途核对）、第 10～13 行。**必须现场重核**：第 9 行，生产段每车整车逐仓。**试跑段不做逐仓核对** | 第 1、2 行不是从 MVP 库搬的记录，是代码里的已批准内容（`REQ-0267`），导入本身不构成「核验」，核验由第 9 行完成；第 8 行核的是地图站点用途，不是车辆硬件，`REQ-0263` 管不到它。模拟 IO 下逐仓核对验不到真硬件，做了反而会留下一份看起来像核验的记录 |
| U2 | 试跑段 `REQ-0203`（防饥饿阈值）导不导 | **不导**，每区参数整份不导入 | 用户已定 `REQ-0198` 为 0 或不导入；`REQ-0203` 同样未标定（cs#219）。两个值在同一张整表里，只导一个也要整表维护；不导时防饥饿只计龄不升级，不挡派车 |
| U3 | 试跑段登记充电桩 211 吗 | **登记**（`charger-roster-map26-station211.json`，`approvalBasis` 改写为切换授权的原话） | MVP 停后 `agv01` 归 v2，不再有两条线抢桩的问题（09-29 置空名册的理由消失）；名册空则三车都不会自动充电，试跑跑久了车会没电 |
| U4 | 充电策略 v1 每个新库都要重新批准，批准依据写什么 | 用户一次授权「切换期间在新库 A、新库 B 上批准并激活与 SHA `5d34c605…` 逐字相同的充电策略 v1」，两次导入都引用这句原话 | 内容 09-29 已批，10-08～10-11 每次换库都重批过同一份；每次再问一遍不增加决定，只增加等待 |
| U5 | 试跑段等待时长用 5 分钟／5 分钟，还是 cs#564 第 15 步写的「试跑调短」（10-11 定稿的离站 1 分 30 秒、持货 2 分钟） | **5 分钟／5 分钟**，与切换定义一致，试跑不手改 | 调度本次转达的口径就是 5／5；手改已装文件不经过部署校验，19 号重装会被写回（10-12 踩过）；生产段本来就是 5／5，试跑用同一值，跑出来的节奏就是生产的节奏 |
| U6 | `agv02`、`agv03` 发件箱若有欠送行，怎么处理 | `agv02`：连回 v2 旧库实例送完再改名。`agv03`：先读；若有欠送，把行内容存进证据后改名留存，不再送 | `agv02` 的原主人仍在跑、车队表里有它，能收；`agv03` 不在旧库当前车队表里，它的行来自 10-11 两车实验，当时需求来自假 MesIngest（`evidence/field/20261011-W2-prep6-two-car/03-fake-mes-cleared.txt`），丢掉不影响真实需求 |
| U7 | 排空到 v2 开运行时之间，要不要核对「MVP 最后做完的需求已离开 MES 目录」 | **要**：cs#564 第 3 步记下 MVP 最后完成的几条需求的 DemandId，第 11 步之前读一次生产 MesIngest 确认它们已不在目录里 | v2 不看 MVP 库，只要 MES 还挂着就会再送一次（第 1.3 节）；成本是一次只读查询（R4） |
| U8 | 生产段回滚时，v2 已完成但 MES 目录里还挂着的需求怎么办 | MVP 开受理闸门前，这几条由现场人工确认实物位置，必要时请 MES 侧处理到离开目录再开闸；不改 MVP 代码 | MVP 代码不再改（规格第 8.4.2 节），MVP 库也不能手改；能挡住重复的只有「开闸前它们已不在目录里」 |


## 7. 要开发的与缺口

本票不写代码。下面是读码发现的缺口，交调度决定是否开票、何时做：

| # | 缺口 | 影响 | 本方案怎么绕 |
| --- | --- | --- | --- |
| G1 | FieldOps 没有作废需求、重置需求状态的动词（调度 C10 10-12 结论） | 试跑库不能带进生产 | 换新库（第 2.3 节）。不建议开发：手改约 50 张表风险更大 |
| G2 | 仓位就绪门禁没有接入派车：`IsSlotConfigurationConfirmedAsync` 在 `src/` 里没有生产调用点（读到的，`fp/v2-impl@4d7e0e07`） | 生产段某车漏做逐仓重核，系统照样给它派单；`REQ-0263` 只靠流程保证 | 第 2.3 节第 4 条把「`status` 回读 `ready=true`」写成进阶段的判据 |
| G3 | 车载端日志簿／发件箱没有只读检查与归档脚本 | 每次靠手写 Python／SQL，三车 × 两次（试跑、生产）容易漏 `loadsOnBoard` 或在欠送不为零时改名 | 第 3.2 节的三条查询。建议在 `8005-workspace` 的 `remote-ops/onboard-hmi/scripts/` 加一个脚本：只读查三项、欠送不为零或有货就拒绝、改名留存、输出证据 |
| G4 | 没有 FieldOps 动词写 `DispatchZoneVehicles` | 区要靠一轮派车轮写进库（cs#669 已记） | cs#564 第 11 步 |
| G5 | 没有「导出某时段已完成需求」的专门动词 | 生产段回滚对账要靠 `export-audit` 的业务审计 | 第 4 节第 4 条；执行前核导出内容是否够用 |

**FieldOps 动词核对结果**：本文点名的 `seed-approved-facts`、`bind-io`、`verify`、`release`、`status`、`activate-task-type-stations`、`task-type-stations`、`import-waiting-points`、`read-waiting-points`、`import-charger-roster`、`charger-roster`、`import-charging-policy`、`approve-charging-policy`、`activate-charging-policy`、`charging-policy`、`import-area-assignments`、`area-assignments`、`import-dispatch-zone-parameters`、`dispatch-zone-parameters`、`export-audit`，全部在 `fp/v2-impl@4d7e0e07` 的 `tools/ControlServer.FieldOps/Program.cs` 分派表（`Main` 末尾的 `switch`）及同目录 `Program.*.cs` 的常量里实读确认存在。没有点名任何不存在的动词。

## 8. 出处

- 票：program#170 正文与两条评论（调度 C10 10-12 读码结论；cs#669 区名步骤）。
- cs#564 方案：control-server PR #677 分支 `docs/cs564-cutover-mode-plan` 的 `docs/production-cutover-mode-plan.md`。
- cs#669：control-server `fp/v2-impl` 的 `scripts/parallel/README.md`「切换用定义」、`instance-factory01-v2.cutover-two-zones*.json`。
- cs#565 票面（三车车载端步骤表）。
- 10-11 两次换库的现场证据：control-server `evidence/field/20261011-W2-prep3-newdb/`、`20261011-W2-prep4-fast-newdb/`、`20261011-W2-prep6-two-car/`。
