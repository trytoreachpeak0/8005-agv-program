# 票 10 决议：六个命令接上了，对账要回读终态，急停停车宽恢复严

Resolved: 2026-09-08
Resolves: `10-fp-c11-riot-order-command-surface.md`

## 结论一句话

服务端现在能对 RIoT 侧的订单发命令，**而且每一次都要回读终态才算数**。急停按 `REQ-0248` 的
受控退避一直重试到闩锁确认，按 `REQ-0167` 的四条硬事实才自动解除，缺哪条报哪条。

control-server `fp/v2-impl`，commit `9f53870` ＋ `96d1390`。

| 项 | 值 |
| --- | --- |
| 端口 | `src/ControlServer.Application/RiotOrderCommandPorts.cs` |
| 适配器 | `src/ControlServer.Infrastructure/Adapters/HttpRiotOrderCommandGateway.cs` |
| 对账 | `src/ControlServer.Host/Runtime/Commands/RiotOrderCommandService.cs` |
| 急停 | `src/ControlServer.Host/Runtime/Commands/EmergencyStopSupervisor.cs` |
| 退避参数 | `src/ControlServer.Host/Runtime/Commands/RiotCommandOptions.cs`，配置节 `RiotCommands` |
| 现场兜底文档 | `docs/emergency-stop-field-fallback.md`（中文，给现场人员看） |
| 新增测试 | **56 条**（命令面 26 ＋ 急停 30） |
| 全量套件 | **451 passed / 0 failed / 0 skipped**（票 08 基准 395 ＋ 56） |
| L2 | `normal-load` PASS |
| 新增 migration | **零** |
| `Ports.cs` 改动 | **零** |
| 证据 | `evidence/fp-c11/20260908-ticket10/`、`evidence/l2/20260908-ticket10-normal-load-001/` |

## 票 08 的守卫在本票上真的挡了一次

票 08 决议预告过：急停的两个 Facade 挂在 `DeviceClient` 上，`get_Device` 不在放行清单里，
第一次用会红。**实际发生的就是这个**：

```
EveryRiotCallProductCodeMakesIsOnTheAllowlist [FAIL]
  Product code calls RIoT Facade methods that section 1 of the allowlist does not approve: get_Device
```

**六个命令方法本身一条都没红**——它们都在白名单 1.3 与 1.5 里。红的只有「产品代码第一次伸手到
`DeviceClient` 这个客户端」这件事本身。确认是有意为之后加一行，并在测试注释里记下这一行的来历。

默认拒绝的清单按设计工作了一次，代价是一行。**这条经验值得留给票 16 的 `vectorId` 守卫。**

## 三处自行定案

### 一、命令网关是两个方法，不是六个

票据按「六个端点」写，票 03 已经发现**实际只有两条路由**。端口因此是
`IssueOrderCommandAsync(kind, orderId, reason)` 与 `IssueEmergencyCommandAsync(kind, deviceKey)`。

按路由拆的好处不只是少四个方法：**两个目标各自非空且不可互换**。订单命令打的是 RIoT 的
`orderId`，急停打的是 `deviceKey`，一个把两者塞进同一个可空字段的接口迟早会有人传错。

**网关不为 RIoT 失败抛异常。**调用方必须能分「被拒了」和「根本没到」，而异常把这两件事压成
一件——压完之后，一条可能已经生效的命令重发一次看起来就是安全的。所以有三态
`Accepted`／`Failed`／`Unknown`，它描述**调用**，不描述**结果**。

### 二、对账读的是订单状态，状态码取自行为实验室

`experiments/catalog.md:70` 给了封闭映射：1 QUEUEING、2 CANCELLED、3 EXECUTING、4 FAILED、
5 SUCCESS、6 DELETED、7 PAUSED、8 SUSPENDED、9 HANG、10 队列优先。Round 10／14／27 实测过其中三条
（HELD → 7、CONTINUE_FROM_HELD → 3、CANCEL → 2、HANG 门槛是 9）。

| 命令 | 目标态 | 落到别的终态 | 还没到 |
| --- | --- | --- | --- |
| `CANCEL` | 2 | Failed | Pending |
| `OrderHold` | 7 | Failed | Pending |
| `OrderContinue` | 3 或 5 | Failed | Pending |
| `HangContinue` | 3 或 5 | Failed | Pending |

**两个 continue 接受 5 SUCCESS**：一张恢复后已经跑完的订单确实恢复了，只认 3 会把一条真的
生效了的命令报成没生效，纯粹因为回读晚了几秒。

**观察胜过调用。**超时但订单已经 HELD 的那次命令是 `Confirmed`——这正是回查而不是重试的意义。
反过来，读不到订单一律 `Unknown`，无论调用说了什么；**`NotFound` 也是 `Unknown`**，刚发过命令的
`upperId` 查不到是矛盾，不是确认。

`RiotOrderState` 这十个常量放在 Application 层，只此一处按含义读状态码——服务端别处要么原样带着，
要么收进 `RiotOrderObservationKind`，那才是对的默认：**状态码是 RIoT 的词汇，不是 8005 的**。

### 三、急停按 episode supervise，退避是到期时间不是 sleep

`REQ-0248` 要求重试持续到状态确认，而那可能跨越进程重启。**在内存里持一个 delay 循环，重启后
计划就从头开始，而且不拨真实时钟就没法测。**改成每次评估问一句「距上一次 attempt 够不够久」，
从审计流算出来：计划扛得住崩溃，测试拨时钟就能穷举。

Episode 也从审计流读：最近一次 `triggerEmergency` 之后，没有被**已确认**的 `cancelEmergency`
关掉，就是开着的。**发出去但没确认的解除不关闭任何东西**——那正是车可能仍然闩着的情形，把它
当成关闭就是一次被遗忘的急停。

退避没有次数上限。`REQ-0248` 没有，代码里也不该有：一台没能证明停住的车，过一小时仍然是一台
没能证明停住的车。

## 停稳判定不在本票，这是有意的

`REQ-0247` 的组合证据规则归票 11（那张票自己这么写的）。本票**读**故障事实上的 `StopProven`，
不重新推导。

理由不只是分工。**显然的那条第二规则是循环的**：`IRiotVehicleSafetyFacts` 对每台闩锁生效的车都会
报 `RIOT_EMERGENCY_NOT_OK`，所以「安全事实全部通过」这个条件，被本类按住的车永远满足不了。
在这里再推一遍只会让同一个问题有两条规则，而其中一条恒假。

## 两处自审改出来的东西

### 解除失败原本会每个评估周期重发一次

`cancelEmergency` 被接受但闩锁没开时，episode 仍然开着，下一次评估直接再发一次——**没有退避、
没有上限**。已改为与触发共用同一套退避。「恢复严」不该表现为对 RIoT 的猛敲，而一次瞬时失败就
永久放弃又会把车困死。

### 解除未确认原本复用了「停车未确认」的告警码

两者要人跑的方向正好相反：`EMERGENCY_STOP_UNCONFIRMED` 是「车可能还在动，立刻去现场隔离」，
解除失败是「车肯定停着，只是回不了岗」。**用同一个码会让人白跑一趟。**已拆成
`EMERGENCY_RELEASE_UNCONFIRMED`，两条都进了现场兜底文档的告警表。

## 三处如实登记的缺口

### 一、`REQ-0167` 的另外半条在本批次没有对象

`REQ-0167` 是两半：自动恢复 8005 自己造成的临时 **RIoT 侧 `DispatchDisable`**，以及自动解除
8005 自己触发的软件急停。**后一半本票完整落地，前一半没有对象。**

证据是硬的：票 08 的 IL 扫描列出了 `src/` 实际调用的 13 个 Facade 方法，
**`DispatchEnableAsync`／`DispatchDisableAsync`／`UpdateIntegrationLevelAsync` 一个都不在里面**。
8005 从不动 RIoT 的车辆调度使能，所以不存在「由 8005 造成的临时禁用」可供恢复。

**不为此加一条「恢复一个我们从不发出的禁用」的路径**——那是纯粹的臆测代码。真要禁用车辆是票 11
（故障隔离处置）的判断；到那时这半条才有对象。已写进现场兜底文档末节。

### 二、命令审计表没有 `REQ-0249` 要的三个字段

`REQ-0249` 要求每次请求记下**来源、身份（若有）、车辆、原因、结果**五项。表里有车辆（`AgvId`）
和结果（`Outcome`），**没有来源、身份、原因的一等列**，而加列是 migration，本批次不做
（票 06 的并行约定）。

现在的处置是两层：

- **`ReceiptJson`** 落一份完整的请求上下文（含五项）；
- **每一次请求都写一条日志**，包括那两种不发出任何调用的请求（被拒的，以及车已闩锁的）。

残留的缺口很小但真实：**arm 与 record 之间那个窗口里，请求上下文只活在语义哈希里**——哈希能让
「换了个理由的重复请求」可见，但不能让它可读。要补，是三个列加一次 migration，建议并进下一次
真的要改那张表的动作里。

**另外注意：不发出调用的请求不写 attempt 行，这是有意的。**那张表数的是调用次数，票 06 的决议
把「调了一次还是三次可判定」定为它存在的理由；把一次没发生的调用写进去会破坏这条性质。

### 三、人发起急停的两条入口只有策略，没有传输

`REQ-0249` 的三条来源在 `EmergencyStopRequestSource` 里齐了，授权规则也实现并测了
（自动与车载端**零门槛**，服务端操作员**只要求有身份**，都不要求二次认证或审批）。

但**车载端与服务端的实际入口没有建**——那需要 v2 协议消息或 HTTP 端点，属于票 14／15 与票 11
的流程。本票交付的是策略与记录，不是传输面。今天唯一有调用方的来源是 `Automatic`。

## 验收对账

| 票据条目 | 结果 |
| --- | --- |
| 六个命令经具名 Facade 发出，`src/` 下 `.Raw` 仍零命中 | ✅ 由票 08 的架构测试对编译产物逐条证明 |
| 每次命令有对账：确认终态之前不认为命令成功 | ✅ `Reconcile` 纯函数逐格穷举；「接受但订单没动」明确是 `Pending`、`Succeeded` 为假 |
| `triggerEmergency` 按受控退避重试，退避参数可配置 | ✅ 从审计流算到期时间；`RiotCommands` 三个键有绑定测试与校验器 |
| 现场兜底路径保留并有文档说明 | ✅ `docs/emergency-stop-field-fallback.md` |
| 自动触发不需人工授权；恢复走严格判据 | ✅ 策略与记录齐备；**人发起的两条入口只有策略没有传输**，见缺口三 |
| `REQ-0167` 的自动恢复 | ✅ 急停那一半完整；⚠ **`DispatchDisable` 那一半在本批次没有对象**，见缺口一 |
| 不把 `CreateDispatchDisabled` 与 RIoT 侧 `DispatchDisable` 混为一谈 | ✅ 新增文件里两个名字**零命中**，实测过 |
| L1 新增覆盖：每个命令的成功、失败、重试与对账各有测试 | ✅ 56 条 |
| 无新增 migration | ✅ `Persistence/Migrations/` 与 `ControlServerDbContext` 一行未动 |

一处偏离（`REQ-0167` 的 DispatchDisable 半条），理由是它在本批次没有对象，不是少做。

## 顺带做的一件事

把 `HttpRiotMovementGateway` 的异常分类抽成
`src/ControlServer.Infrastructure/Adapters/RiotCallFailureClassification.cs`，两个够到 RIoT 的
适配器共用。它划的那条线——**一次拒绝，与一次可能根本没到达的调用**——决定重试安不安全，
两处不该能各自漂移。`HttpRiotMovementGatewayTests` 直接覆盖，L2 `normal-load` 再端到端确认一次。

`order-ref-missing` 那个 create 专属的特例留在原处，没有做成共用件里的一个洞。

## 给下游票的指针

**票 11（故障隔离）现在可以开工，前置已解除。**它是本票两个组件的调用方，两个都是**被驱动的**
——没有 hosted service，因为同一批 episode 有两个调度器就是两个组件开始互相不认账的方式。

1. **`OrderHold`（`REQ-0234`）走 `RiotOrderCommandService.IssueAsync`**，不要直接调 Facade。
   目标是 `RiotOrderCommandTarget(agvId, upperId, orderId)`——**三个身份都要**，`upperId` 是审计
   的键，`orderId` 是端点的地址，两者不可互换。
2. **停稳判定是你的。**把结论写进 `IVehicleFaultStore.RecordStopProofAsync`，急停监督器读它。
   **别在监督器里再推一遍**，理由见上文。
3. **要让车自动恢复，故障事实必须真的被 `ClearAsync` 清掉**（`Level=None` 且 `ClearedAt` 有值）。
   只把 `Level` 降回去不算，`ClearedAt` 是判据的一部分。
4. **驱动节奏由你定。**`EvaluateAsync(subject, ct)` 每次调用只做一件该做的事：该重试就重试、
   该确认就确认、该拒绝解除就报原因码。多调几次没有副作用，退避自己会挡住。
5. **`EmergencyStopSubject` 要 `agvId` 与 `deviceKey` 两个**，它们不是同一个串
   （`remote-ops/fleet.md` 是唯一的对照表）。
6. **`PriorityExecAsync` 仍然不能用**——票 08 的守卫会当场变红，实测过。

**票 16（`vectorId` 测试绑定架构测试）**：本票是票 08 那套守卫第一次真的挡住人的记录，
「默认拒绝 ＋ 红一次加一行」这个循环成立且代价很小，可以照搬。
