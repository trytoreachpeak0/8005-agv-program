# 票 19 开工前判定：演练按不按得下去（2026-09-08）

**这不是决议。**W1 窗口未开，演练未做，票 19 仍是 `ready-for-agent`。本文只回答交接文档要求
先想清楚的那一件事：**进了现场，急停按得下去吗？**

## 结论：按不下去——除非现场有人能在 RIoT 侧把一张在途单置为 FAILED

**卡在两处，一处是已知的（没有人发起入口），一处是此前没人记下的（唯一那条路径的入口在
对端手上）。**批次 2 的完成不因它挂起——票 19 逐字写着「不要因为这张票而把整个批次 2 的完成
挂起」，且 W1 的门槛是批次 3 代码就绪，与批次 2 无关。

## 一、8005 侧没有「人发起急停」的入口

`EmergencyStopSupervisor.RequestStopAsync` 在**生产代码里只有一个调用方**：

```
src/ControlServer.Host/Runtime/Faults/VehicleFaultCoordinator.cs:679   （EscalateAsync 内）
```

其余全部引用都在 `tests/ControlServer.Tests/EmergencyStopSupervisorTests.cs`。没有 API、没有
命令、没有恢复会话动作能直接发起急停。票 10 决议的缺口三记的「人发起的两条来源只有策略没有
传输」仍然成立，票 18 没有触碰它。

## 二、唯一那条运行时路径，两个条件必须同时成立

### 条件 1 —— RIoT 把该车的在途单报成终态 FAILED

唯一入口在 `JourneyRuntimeEngine.cs:833`：

```csharp
if (arrival.Order.Kind != RiotOrderObservationKind.Terminal ||
    arrival.Order.OrderState != RiotOrderState.Failed ||
    arrival.Intent.OrderId is not string orderId)
{
    return false;
}
…
await faults.ObserveAsync(…, VehicleFaultEvidence.OrderFailed, …);
```

`VehicleFaultCoordinator` 的三个公开入口里，只有 `ObserveAsync` 通向升级，而 `ObserveAsync`
**在整个 `src/` 里只有这一个调用方**。`ConfirmIsolationAsync`（人确认隔离）与 `ResumeAsync`
都不发急停。

### 条件 2 —— 该车证不出停住

`VehicleFaultCoordinator.RequiresEscalation`：

```csharp
if (holdConfirmed && proof.Proven) { return false; }

return latest.Reading != VehicleMotionReading.NotMoving   // 读数不是「确证未移动」，Unknown 也算
    || !latest.HasKnownPosition                            // 位置未知
    || proof.MissingFacts.Contains(StopProof.PositionChanged)
    || proof.MissingFacts.Contains(StopProof.EvidenceStale);
```

**一台老老实实停在站上、位置已知、读数新鲜的车永远不会升级。**`STOP_PROOF_TOO_FEW_SAMPLES`／
`SAMPLES_TOO_CLOSE`／`OBSERVATION_GAP` 单独都不触发——这正是票 18 的 `L2-CS-12` 断言的东西。

> **所以演练要造的是「车读不出停住」，不是「单失败了」。**单失败只是入口，`REQ-0247` 的组合
> 证据判定会把一台停稳的车挡在急停之外。

## 三、条件 2 有解，条件 1 没有

**条件 2 好办**：**空载不等于静止**——票 19 只要求「车上无货且无产品在仓」，没要求车不动。
让空载车在途行驶，`latest.Reading == Moving` 直接满足，不需要动任何传感器。这比「把遥测掐断
让读数变 Unknown」干净得多，后者是在造传感器故障，不是受控演练。

**条件 1 是真门槛**：需要 RIoT 侧把一张在途单置为 FAILED，而**8005 的 RIoT 调用白名单里没有
任何一个调用能做到**。看 `vendor/8005-agv-program/docs/riot-call-allowlist.md`：建单只批
`POST /api/order/v1/add/byDefaultMissions`；订单命令面只有 `CancelOrderAsync`／
`OrderHoldAsync`／`OrderContinueAsync`／`HangContinueAsync`（都经私有
`PostOrderCommandAsync`），**都改不成 FAILED**。

**这必须由 RIoT 侧的人操作。**这件事票 19 里没写，是演练脚本作者一定会撞上的第一堵墙。

## 四、白名单描述的那条触发条件没有实现

白名单第 167 行写着获批的 `triggerEmergency` 触发条件是

> 车辆在仓门未安全锁闭时移动、无 RIoT 订单可供 `OrderHold`、且无其它获批 RIoT 停车动作时，
> 8005 自动 `triggerEmergency` 并进入持续保持

**实现里不是这样。**`DepartureSafety` 只出现在发车前门禁（`JourneyRuntimeStage.AwaitingDepartureSafety`
→ `AuthorizeMovementAsync`，由一份有新鲜度上限的 `PreDepartureSafetyCheckResult` 授权），
**没有任何在途撤销路径通向急停**。`REQ-0246` 在代码里落成的是「证不出停住就立刻升级」这条
规则本身（`VehicleFaultCoordinator.cs:421` 与 `Ports.cs:498` 的注释都这么写），不是白名单描述
的那个场景。

`LOCK_NOT_CLOSED`／`UNLOCK_OUTPUT_NOT_RESET` 在实现里只出现在
`WireToGateStore.OperationInducedUnsafety`——用于放宽会话就绪判定，**只读不发**，与急停无关。

**这条偏离不属于票 19，但演练脚本若照白名单写就会落空，必须记下。**

## 五、进现场之前要落实的三件事

1. **RIoT 侧谁能把一张在途单置为 FAILED？**没有这个人，演练开不了。这是对端（RIoT 运维）的
   动作，不在 8005 的白名单里。
2. **备选：把「人发起急停」的入口做出来。**那属于 `REQ-0253` 权限模型那条线（票 10 决议缺口三、
   票 11 决议、票 18 决议缺口二都指向它），**不属于票 19**。若用户选这条，要另开票。
3. **W1 窗口本身。**门槛是批次 3 代码就绪，窗口内主体是三台车逐台逐仓 IO 核对。**顺序不得
   倒置：先核对，后启用门禁**（规格 3.5）。

## 六、出口判据的数法，与 L2 同源

W1 出口「8005 侧只发一次调用」——**数 `RiotOrderCommandAudit` 的 attempt 行数，不数 RIoT 侧的
请求数**。后者分不清「重试」与「重复发令」。票 18 的 `L2-CS-09/10/11` 已在 L2 上按这个数法证过
一次，现场是同一套判定。

证据落 `evidence/field/<日期>-W1-<描述>/`，形状同 L2 ＋ 现场记录与照片指针。**该目录尚不存在，
票 19 是第一个用它的**；不要复用 `evidence/g3/`——G3 是门禁，现场窗口不是门禁。

## 状态

**票 19 仍为 `ready-for-agent`，卡在：W1 窗口未开 ＋ 条件 1 缺现场执行人。**
**批次 2 的完成不因它挂起。**
