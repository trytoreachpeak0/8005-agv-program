# WIRE_TO_GATE 自动化场景测试方案

**动机：** 2026-09-03 的现场联调花了一个下午，跑到装载环节因为一次操作超时而停摆。事后复盘，
那天暴露的三个缺陷**全部不需要真车就能复现**——但当时没有一个能跑异常场景的环境，只能在车前
一层层手工挖。这份文档要解决的就是这件事：把「必须有人站在车前」的验证，尽可能变成一条命令。

范围是 WIRE_TO_GATE MVP 的跨端行为。不覆盖真实 IO 模块、接线、锁、光幕的硬件资格——那部分
`RELEASE-CANDIDATE.md` 第 11 节已经写死，模拟器 PASS 不代表硬件合格。

---

## 1. 三层测试，各管一段

| 层 | 组成 | 跑在哪 | 管什么 | 现状 |
| --- | --- | --- | --- | --- |
| **L1** 进程内 | 全替身 | CI（self-hosted runner） | 状态机、协议编解码、边界条件 | **已有**：ControlServer 255 项、模拟器 18+14 项、车载端单元测试 |
| **L2** 半实物 | 真 ControlServer + 真车载端 WPF + 真模拟器 + **假 RIoT** | 一台带桌面会话的机器 | **跨端时序、异常注入、恢复路径** | **不存在，本方案的主体** |
| **L3** 现场 | 真车 + 真 RIoT + 真 MesIngest + 模拟或真 IO | 厂区 | 真实硬件契约、最终确认 | 已跑通一次（2026-09-03，止于装载） |

核心判断：**L2 是投入产出比最高的一层**。它不需要真车、不需要现场授权、不占用生产 AGV，却能
覆盖绝大多数跨端缺陷。2026-09-03 的三个缺陷全部落在 L2 的能力范围内：

| 缺陷 | L1 能发现吗 | L2 能发现吗 |
| --- | --- | --- |
| `IsFresh` 对时钟偏差零容差 | 不能（替身共用一个时钟） | **能**——把两端时钟拨开 100 ms |
| 安全快照只在会话建立时发一次，引擎读到陈旧值 | ~~不能~~ **能**（见下） | **能**——假 RIoT 报 MOVING 再报 STOPPED |
| `Blocked` 是终态且永久占用 active 位 | ~~勉强~~ **能**（见下） | **能**——不放货，等装载超时 |

**这张表的 L1 列在 2026-09-03 修复时被推翻了两格**，如实记在这里。原来判「单元测试不会让车
动起来」，实际上不需要让车动——把 `SafetyStateChanged` 直接写进 `ProtocolInbox` 就复现了，
两条测试各几十行。`Blocked` 那格同理，构造超时只是「结果不完美」的一种，`ApplyOperationResultAsync`
对任何非完美结果都走 `RecoveryRequired`。

教训是：**判断某一层「发现不了」之前，先花十分钟真写一条试试。**低估 L1 会把本该几秒钟的
回归推到需要一整套半实物环境。这不改变 L2 的价值判断——L2 覆盖的是真实两端的时序与恢复路径，
那是替身做不到的；改变的是「哪些东西应该先在 L1 试一次」。

L3 保留给「真实硬件契约」：车真的会动、RIoT 真的会派单、真实 IO 真的会锁。它应该只跑正常路径
的确认，**不应该拿来跑异常场景**——今天的教训是，在车前调试的每一分钟成本都极高。

---

## 2. 现有能力盘点

### 模拟器（`slots-simulator`）：够用，设计得很好

loopback HTTP 控制面 `127.0.0.1:58006/api/v1`，权威文档是该仓库的
`docs/EXTERNAL_AUTOMATION_CONTROL_API.md`。

| 能力 | 端点 |
| --- | --- |
| 状态查询 | `GET /snapshot`、`GET /health` |
| 新建轮次 | `POST /reset` |
| 模拟放货取货 | `PUT /slots/{n}/cargo` (`EMPTY`/`OCCUPIED`) |
| 模拟关门 | `POST /slots/{n}/close-door` |
| 锁反馈故障 | `PUT /slots/{n}/lock-feedback-override` (`AUTO`/`FIXED_0`/`FIXED_1`) |
| 光幕故障 | `PUT /slots/{n}/light-curtain-override` (`AUTO`/`FIXED_0`/`FIXED_1`) |
| Modbus 通信故障 | `PUT /faults/modbus` (`NORMAL`/`NO_RESPONSE`/`DISCONNECT`/`DELAY`) |

工程质量高，可以直接依赖：`runId` + `commandId` 幂等、`expectedRevision` 乐观并发、稳定
`reasonCode`（不是中文字符串）、机器可读的 `openapi.json`、明确的 revision 递增规则。

**它的边界是刻意的，不要试图绕过**：HTTP 不提供开锁和开门，开锁必须由 HMI 写 Modbus DO 触发。
这条保证了测试验证的是真实的 HMI→IO 通路，而不是测试脚本自己摆出来的状态。

### ControlServer：三个替身

- `tools/ControlServer.FakeOnboard` — 假车载端，用于服务端侧测试
- `tools/ControlServer.Conformance` — 协议一致性
- `tools/ControlServer.FakeRiot` — 假 RIoT，**已建**（`9ec81fa`），见下

### 车载端：没有任何自动化入口

条码输入是纯 UI：`MainWindow.xaml` 的 `ScanTextBox`（绑定 `ScanText`，
`UpdateSourceTrigger=PropertyChanged`），Enter 触发 `ScannerSubmitCommand`，另有「手动提交」
按钮绑 `ManualSubmitCommand`，`IsEnabled` 绑 `CanSubmit`。

好消息是控件有 `x:Name`、命令绑定清晰，**UI Automation 可行**，短期不必等对方改代码。

---

## 3. 四个缺口和对策

### 缺口 1：没有假 RIoT —— ~~自己建~~ **已建**（`8005-agv-control-server@9ec81fa`）

`tools/ControlServer.FakeRiot`，用法与契约见该目录的 `README.md` 与 `openapi.json`。下面是当初
的需求描述，落地时全部满足，只有两处按实际情况收紧了，记在本节末尾。

L2 的成败在这里。需要一个进程，实现 ControlServer 实际调用的那几个 RIoT 端点，并且状态可被
测试脚本驱动：

```
GET  /api/task/vehicles/getVehicleInfoByDeviceKey?key={vehicleKey}
GET  /api/order/v1/orderRecord/detailByUpperId/{upperId}
GET  /api/order/v1/orderRecord?pageNum=&pageSize=&filterByState=...
GET  /api/imap/v1/mapInfo/stations/{mapId}
POST （建单端点，见 HttpRiotMovementGateway 的 CREATE 路径）
```

真实响应结构已经在 2026-09-03 抓到，可直接作为夹具（fixture）——车辆卡片含
`status/enable/procState/currentMap/currentPosition/speed/lockStatus/battery`，订单详情含
`orderState/orderId/endStationNo/missions[].mapId/missions[].destination`。

假 RIoT 自己也要有一个 loopback 控制面，形状照抄模拟器（`runId`/`commandId`/幂等/稳定
`reasonCode`），能驱动：车辆位置、`procState`、速度、急停与控制状态、电量、订单状态推进。
**车辆运动状态可控是关键**——三个缺陷里有两个都需要"车动起来再停下"。

放在 `8005-agv-control-server/tools/ControlServer.FakeRiot/`，与既有两个工具并列。

落地时的两点补充：

1. **非 loopback 监听默认拒绝启动。**原需求只说了控制面照抄模拟器，没说监听边界。一个会回答
   「车在哪、订单到没到」的东西如果厂区网能访问到，那边某个程序就可能把它的回答当成 RIoT 的。
2. **控制面不提供任何「让车动」「把订单标记完成」的业务指令**，只能说明 RIoT *观测到* 什么。
   派车仍然只能由 ControlServer 通过 `POST /api/order/v1/add/byDefaultMissions` 发起。这与模拟器
   那条「HTTP 不提供开锁」是同一条边界。

还有一个坑值得后来者知道：这个项目原来带 `appsettings.json`，而 Web SDK 会把它作为 `Content`
复制到**每一个引用方**的输出目录——于是它盖掉了 `ControlServer.Host` 的同名文件，两条读
appsettings 的断言当场挂掉。种子值现在只写在 `FakeRiotSeed` 的默认值里，配置走命令行开关。

### 缺口 2：车载端没有自动化入口 —— 两条路并行，外加一条当时没想到的

**先落地的是第三条：合成协议对端。**`tools/ControlServer.FakeOnboard` 原本只做「握手完就退出」，
现在是长连接可编排对端——五步握手、两秒心跳、按 `Auto`/`Manual`/`Silent` 策略应答 sublot、装卸
结果与出发前安全检查。它没有 IO、没有 journal、没有操作员，**换不掉真车载端**；但它让编排器和
所有服务端侧场景今天就能跑，不必等 UIA。下面两条路仍然要走。


**短期（我方可做）：UI Automation 驱动。** 用 `System.Windows.Automation` 或
FlaUI 找到 `ScanTextBox`，设值，发 Enter 或点「手动提交」。控件有具名且命令绑定明确，可行性
不低。缺点诚实说：依赖控件树和窗口焦点，分辨率或布局一变就可能失效，属于「能用但脆」。

**长期（提给 Kun Wang）：车载端加一个测试控制面。** 形状完全照抄模拟器那套——loopback
HTTP、非生产环境才启用、只驱动 UI 意图不绕过业务逻辑、`runId`/`commandId` 幂等。至少需要：

- 提交 sublot（等价于扫码）
- 读当前 HMI 状态（`OnboardState`、`CanSubmit`、当前提示文案）
- 读当前会话与 journal 摘要

这个请求是有先例的：模拟器就是这么做的，同一套设计语言，对方接受成本低。**以 issue 形式提
出，附本方案链接和场景清单**，让对方判断优先级。若对方希望我方出 PR，按新政策（2026-09-03，
根 `CLAUDE.md`）可以提，但代码内容仍归对方决定。

### 缺口 3：两个 WPF 需要交互式桌面会话

计划任务（登录触发、交互式）按序拉起：先模拟器（等 `1502` 监听）再车载端。工作区已有先例——
`win11-01` 上的 `golden-renderer` runner 就是这么起的，见根 `CLAUDE.md` 的 CI 一节。

同时顺手解决另一个坑：**部署脚本写的 Machine 级环境变量对已登录会话不生效**。2026-09-03 车载端
启动失败卡了很久，就是因为桌面会话是环境变量写入之前建立的。计划任务重启会话即可覆盖；写进
部署文档的检查清单。

### 缺口 4：没有场景编排器 —— ~~本方案的交付物~~ **已建**（`8005-agv-control-server@8fcbdbc`）

`scripts/l2/`，用法见该目录的 `README.md`。一条命令，约 14 秒，无人值守：

```powershell
pwsh .\scripts\l2\Invoke-L2Scenario.ps1 -Scenario normal-load -EvidenceRoot <新目录>
```

下面是当初的职责清单，五条全部落地。

1. 起环境（假 RIoT → ControlServer → 模拟器 → 车载端），每一步等就绪判据而不是 sleep
2. 按场景脚本驱动三个控制面（假 RIoT / 模拟器 / 车载端 UIA）
3. 轮询断言（服务端数据库 + 各控制面 snapshot）
4. 产出证据（JSONL 时间线 + 结论 JSON + `SUMMARY.md`）
5. 拆环境，保证下一轮从干净状态开始

时间线的形状可以直接复用 `remote-ops/status/Get-WireToGateStatus.ps1` 的 journal：一行一次观测、
只追加、记录判据翻转。那个脚本今天在定位缺陷时就是靠这个把"12:56:49 STOPPED → 12:57:15
UNKNOWN"精确卡出来的。

---

## 4. 场景清单

按业务阶段 × 故障类型展开。标 ★ 的是 2026-09-03 实际踩到的，优先实现。

### 会话与握手

| 场景 | 注入手段 | 期望 |
| --- | --- | --- |
| ★ 车载端时钟慢于服务端 100 ms | 调车载机时钟 | 当前会**卡死**在 `DEPARTURE_SAFETY_NOT_READY`；修复后应容忍。**L2 这一层做不了**，见下 |
| 车载端时钟快于服务端 | 同上 | 正常进 `Ready` |
| 会话断开重连 | 停止/恢复 ControlServer | `sessionGeneration` 递增，journal 增长而非重建 |
| ★ 车辆运动中建立会话，随后停稳 | 假 RIoT 报 MOVING → STOPPED | ~~当前引擎读到陈旧快照**永久卡住**~~ 已在 L1 修复并回归（`4ad840b`）；L2 这条改为验证真实两端时序。**已实现**：`session-established-while-moving` |
| 车辆 `UNKNOWN`（急停/失控） | 假 RIoT 注入 `RIOT_EMERGENCY_NOT_OK` | 闸门 fail-closed，恢复后自愈 |

### 到站

| 场景 | 注入手段 | 期望 |
| --- | --- | --- |
| 正常到站 | 假 RIoT 推进订单到 `orderState=5` | 进 `AwaitingSublot`，下发 `SublotEntryRequested` |
| 车停在错误站点 | 假 RIoT 报错误 `currentPosition` | 不进入装载 |
| 订单未到终态 | `orderState` 停在中间态 | 不进入装载 |
| 车到站但仍在动 | `speed != 0` | 不进入装载 |
| 电量低于阈值 | `battery < MinimumBatteryPercent`(30) | 需求不受理 |

### 装载

| 场景 | 注入手段 | 期望 |
| --- | --- | --- |
| 正常装载 | 模拟器放货 + 关门 | 逐仓 `Committed`，进出发前安全检查 |
| ★ 超时不放货 | 车载端跑掉自己的操作员超时，上报一份 `completed=false` 的 `OperationResult` | `LOAD_RESULT_REQUIRES_RECOVERY` 且整台车停摆，且**这是对的**——出口在车载端的五步恢复握手（`8005-agv-onboard-hmi#4`）。**已实现到 Blocked 为止**：`load-result-requires-recovery` |
| 装载指令根本不被应答 | 车载端 `Silent` 策略 | 与上一条**不是同一件事**：`StationOperations` 停在 `Prepared`，`AdvanceAsync` 的 `AwaitingLoadResult` 分支走 `else { return; }`，旅程停在 `AwaitingLoadResult` 而**不进 `Blocked`**。尚未实现 |
| 放货后又取走 | `cargo` `OCCUPIED`→`EMPTY` | 结果与物理事实一致 |
| 锁不上 | `lock-feedback-override FIXED_0` | `LOCK_NOT_CLOSED`，不放行出发 |
| 假装锁上 | `FIXED_1` 而门实际开着 | 不能被骗过 |
| 光幕假装空 | `light-curtain-override FIXED_1` | 装载不被误判完成 |
| 光幕假装有货 | `FIXED_0` 而实际没放 | 不能被骗过 |
| 放错仓位 | 给非目标仓放货 | 目标仓未完成，非目标仓不计入 |
| IO 断链 | `faults/modbus DISCONNECT` | 车载端 fail-closed，恢复后能续 |
| IO 变慢 | `DELAY 500ms` | 在 `ioSnapshotMaxAgeMs`(1000) 内仍可用；超出则判 unknown |
| IO 无响应 | `NO_RESPONSE` | 同断链，且不得误报成功 |

### 出发与关卡

| 场景 | 注入手段 | 期望 |
| --- | --- | --- |
| 正常出发到关卡 | 假 RIoT 推进第二段订单 | 进卸载阶段 |
| 出发前车辆变为运动 | 假 RIoT 报 MOVING | 出发前安全检查拒绝 |
| 出发前锁被打开 | `lock-feedback-override FIXED_0` | 同上 |
| 关卡卸载后结单 | 取货（`cargo EMPTY`） | journey `Completed`，需求终态 |

### 恢复

| 场景 | 注入手段 | 期望 |
| --- | --- | --- |
| 装载中途车载端重启 | 杀进程重启 | 按 ADR 0006 可唯一解释恢复，不重复开门 |
| 装载中途服务端重启 | 重启服务 | 结果不丢，重连后续上 |
| 未确认结果的重放 | 断开确认链路 | 同一 `slotOperationAttemptId` 不重复执行 |

### 为什么「车载端时钟慢 100 ms」这一条现在做不了

缺陷在车载端的 `VehicleSafetySignal.IsFresh`
（[`8005-agv-onboard-hmi#1`](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/1)），
**合成对端里根本没有那段逻辑**——它不做新鲜度判定，也没有一个会因为时钟偏差而拒绝自己观测值的
本地时钟。用合成对端「复现」出来的只会是自己写进脚本的假象：绿了不说明车载端修好了，红了也不说明
车载端坏了。

这一条要等落地顺序第 5 步（车载端 UIA 驱动）和第 7 步（交互式桌面会话）。**凑齐三条不如说清哪一条
做不了。**

---

## 5. 断言与证据

断言来源三处，都已验证可读：

1. **ControlServer 数据库**（`C:\ProgramData\8005\ControlServer\data\controlserver.db`）——
   `SessionRecoveries`、`JourneyRuntimes`、`AcceptedDemands`、`JourneyBacklog`、`OrderIntents`、
   `StationOperations`、`ProtocolInbox`/`ProtocolOutbox`。读法：借 ControlServer 自带的
   `Microsoft.Data.Sqlite` + `SQLitePCLRaw`，`Mode=ReadOnly`。
2. **模拟器 `GET /snapshot`** —— 八仓物理与 DI/DO 原始值。
3. **HTTP 端点** —— `/health/ready`、`/api/runtime/sessions`、`/version`。

`JourneyBacklog.ReasonCode` 特别有价值：它记录了每条需求被筛掉的原因
（`OUT_OF_SCOPE_WORK_TYPE`/`OUT_OF_SCOPE_AREA`/`ONBOARD_FACTS_NOT_READY`/
`AREA_STATION_NOT_FOUND`/`PACKAGE_CAPACITY_NOT_UNIQUE`），是断言准入逻辑的现成钩子。

证据格式沿用现有 G3 的形状：`assertions.json` + `SUMMARY.md` + 时间线 JSONL，放进
`8005-agv-control-server/evidence/`。这样 L2 的产出可以直接进门禁体系，而不是另起一套。

---

## 6. 落地顺序

1. ~~**修 ControlServer 的两个缺陷**~~ **已完成**（`8005-agv-control-server@4ad840b`，
   复盘见该仓 `docs/defects/20260903-onboard-safety-facts-frozen-at-session-start.md`）
   - `ReadOnboardFactsAsync` 改为从「携带会话当前 `safetyStateVersion` 的那条消息」读安全摘要，
     `SafetyStateSnapshot` 与 `SafetyStateChanged` 一并纳入。仓位可用性刻意仍取自快照的
     `slotStates`——`SafetyStateChanged` 只给 `affectedSlots` 不给新状态，当作可用性丢失会让
     第一趟用过的仓位在会话余下时间里全部搁浅。
   - `Blocked` **没有**加出口，也**没有**改成不算 active。查证后结论不同于原判断：服务端的
     出口本来就是完整且有测试的，断点在车载端从不发起五步恢复握手，已开
     [`8005-agv-onboard-hmi#4`](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/4)。
     让 `Blocked` 不算 active 是不安全的——`ExecuteOnceAsync` 会转而走 `DiscoverAndAcceptAsync`，
     在仓位物理状态未证实、dispatch lease 仍被持有时把车派去跑别的需求。已加回归测试钉住。
     实际修掉的是另一处：`Blocked` 的 `BlockReasonCode` 被 `ONBOARD_SESSION_NOT_READY` 覆盖，
     车载端一关机，「在等哪一种恢复」这个唯一诊断就没了。
2. ~~**建假 RIoT**~~ **已完成**（`8005-agv-control-server@9ec81fa`）。六个 RIoT 端点 + loopback
   控制面，12 条黑盒测试起真实 Kestrel、用生产的 `HttpRiotMovementGateway` 去读。全仓
   255 → 267 通过
3. ~~**建场景编排器**~~ **已完成**（`8005-agv-control-server@8fcbdbc`）。`scripts/l2/` 加
   `tools/ControlServer.FakeMesIngest` 与升级后的 `ControlServer.FakeOnboard`；「正常装载」
   全链路连续三次 PASS，每次约 14 秒，干净 checkout 复跑一致
4. ~~**补 ★ 三个场景**~~ **三条里做完两条，第三条如实记为做不了**（`8005-agv-control-server@6a6d6dc`）
   - `session-established-while-moving`：会话带着 `vehicleStopped=false` 建立 → 需求判
     `ONBOARD_DEPARTURE_UNSAFE`；车停稳发 `SafetyStateChanged` → 受理并派车；车再动起来时
     RIoT 摆出一个完整到站 → **不采信**；车停稳 → 采信，进 `AwaitingSublot`。两个方向都走到了
   - `load-result-requires-recovery`：`Manual` 策略 + 一次 `completed=false` 的 `OperationResult`
     → `Blocked / LOAD_RESULT_REQUIRES_RECOVERY`；会话离开 `Ready` 后原因不被
     `ONBOARD_SESSION_NOT_READY` 覆盖；车载端关机后仍在；Blocked 期间新需求连候选评估都不进。
     **止于 Blocked**，出口要等 `8005-agv-onboard-hmi#4`
   - **时钟慢 100 ms 这一条没做**，理由见第 4 节末尾。合成对端造不出它，硬造出来的是假象
   - 为此给替身加了两个入口：假 RIoT 的 `mapStationReads`（否定判据不必 sleep）、假车载端的
     `FakeOnboard:Seed:*`（会话可以在车还在动的状态下建立）
5. **车载端 UIA 驱动**，让条码输入进入自动化 ← **下一步**
6. **给 Kun Wang 提测试控制面 issue**，附本文档与场景清单
7. **计划任务自启动**，把 L2 挂到 CI（`win11-01` 的 `golden-renderer` 交互式 runner）
8. 逐步补齐第 4 节其余场景

第 1、2、3 步之后，L2 就能跑第一条自动化链路；第 4 步之后，2026-09-03 那一下午的排查里能自动化的
部分是三条命令、一分钟。剩下的那部分要等车载端可驱动。

---

## 7. 已提出的跨仓库反馈

| 编号 | 内容 | 类型 |
| --- | --- | --- |
| [`8005-agv-onboard-hmi#1`](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/1) | `VehicleSafetySignal.IsFresh` 对时钟偏差零容差 | 缺陷 |
| [`8005-agv-onboard-hmi#2`](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/2) | 安全快照每会话只发一次，车辆停稳后不重报 | 缺陷（附带一个协议语义问题待对方定夺） |
| [`8005-agv-onboard-hmi#3`](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/3) | 车载端 loopback 测试控制面 | feature request |
| [`8005-agv-onboard-hmi#4`](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/issues/4) | 车载端从不发起五步恢复握手，装载失败后 journey 无出口 | 缺陷 |

`#2` 里我方承诺的服务端修复（`ReadOnboardFactsAsync` 纳入 `SafetyStateChanged`）已于
`8005-agv-control-server@4ad840b` 落地，未等对方排期。`#3` 在对方答复前走 UIA 临时方案。
`#4` 挡住的是 `CV-EXCEPTION-RESUME`、`CV-EXCEPTION-COMPENSATE`、
`CV-LOAD-CANCELLATION-ALL-EMPTY`、`CV-FAULT-CARGO-HANDOFF` 四条向量的 `ONBOARD_HMI_G2`，
即 `W2G-IS-02` 与 `W2G-IS-07`。

按根 `CLAUDE.md`（2026-09-03 变更）：那两个仓库**内容只读**，但 issue / PR / comment 是正当渠道。
诊断要带可复现证据，修复留给 owner。
