# 把故障注入泛化到业务消息面

Type: task
Mode: AFK
Status: resolved
Blocked by: none

## Question

如何把 `scripts/run-staged-g3.ps1` 的故障注入从单一 `RecoveryStateReport` 泛化到 WIRE_TO_GATE
的业务消息面，使票据 10 要求的「结果重放」与「重复／乱序／延迟」三类向量能在当前双端 commit
（`ControlServer 3d8b00c` + `OnboardHmi 304e6ad`）下取得机器可读证据？

### 已知的起点

drop 判定集中在 harness 的 `PumpAsync`，只有三行，消息类型是硬编码字符串：

```csharp
bool drop = injectDrop &&
    Equals(metadata.GetValueOrDefault("messageType"), "DurableAck") &&
    Equals(metadata.GetValueOrDefault("acceptedMessageType"), "RecoveryStateReport") &&
    Interlocked.CompareExchange(ref _droppedRecoveryAck, 1, 0) == 0;
```

`RunProbeAsync` 已有 `Envelope`、`Hello`、`Heartbeat`、`StableGuid`、`Sha256` 等构造器，可手工
构造业务消息，**不需要驱动真实旅程**——staged 运行的 `journeyRuntimeEnabled = false`，服务端本来
就不会自行下发 `SlotOperationCommand`。

### 范围

- drop 的目标消息类型参数化，覆盖 `OperationResult`、`SlotOperationCommand`、
  `PreDepartureSafetyCheck`，保留现有 `RecoveryStateReport` 断言不回归。
- 在 `PumpAsync` 同一层加入 delay 与 reorder 两种注入。
- 为上述每种消息补重复（同 ID 同内容字节级重放）与冲突（同 ID 异内容稳定拒绝）断言，写入
  `run-result.json` 的 `assertions`。

### 完成判据

`run-result.json` 中新增断言全部 PASS 且绑定 `3d8b00c` + `304e6ad`；既有七条断言不回归；
`noMovementOrExternalSideEffects` 与 `secretScan` 保持 PASS；证据归档于 ControlServer 仓
`evidence/g3/`，票据只留路由指针。

### 注意

- 不动车、不建单、不使用现场凭据。
- `StageRoot` 必须是短路径，否则克隆 protocol 仓时撞 Windows MAX_PATH。
- 运行需 `-InstallTemporaryCurrentUserRoot`，要用户逐次授权，且运行后必须复核根证书、端口、
  进程无残留。

## Answer

把 `PumpAsync` 里三行硬编码的 drop 判定换成运行时装配的规则表，四种动作
（`drop-and-close`／`drop`／`delay`／`hold-until-next`），并由一个合成对端手工构造业务消息通过
第二条故障代理驱动，不驱动真实旅程。十二条断言全部 PASS，绑定 `3d8b00c` + `304e6ad`，
原七条不回归。

覆盖四种消息：`SublotSubmitted`、`OperationProgress`、`PreDepartureSafetyCheckResult`、
`SlotOperationCommandRejected`——它们的服务端处理是一条 `DurableAck`，无需 demand 与 station
operation。结果重放的判据取自代理记录中被吞掉那一行的哈希（探针看不见它），与同会话代重发拿到
的响应逐字节相等；`DurableAck` 内含 `durablyAcceptedAt`，重算必变，故相等即证明是存储重放。

### 两条不可达，已在运行结果中具名而非默认覆盖

`OperationResult` 与 `SlotOperationCommand` 在 staged 运行中不可达，写入
`run-result.json` 的 `businessProbe.coverageLimits`：

- `OperationResult`：`OnboardMessageProcessor` 用 `SingleAsync` 在 `StationOperations` 上解析
  forced recovery generation，指向捏造 attempt 的消息在任何确认之前就抛出。`StationOperations`
  只由 `PrepareSlotOperationAsync` 写入，需来自 MesIngest 与 RIoT 的已受理 demand。
- `SlotOperationCommand`：只由 `JourneyRuntimeEngine`（本运行关闭）发布，或由
  `OnboardRecoveryCoordinator` 从同一条带 demand 路径创建的 outbox 行重放。

因此票 10 的「结果重放」一类中，`RecoveryStateReport` 与业务面已 PASS，`OperationResult`
仍缺，且**不是本 runner 能补的**——需要一次带 demand 的运行。未捏造任何状态：
`orderIntentCount`／`acceptedDemandCount`／`stationOperationCount` 三项仍为 0。

### 首次运行红，根因已单独证出

`OnboardTcpServer.ExecuteAsync` 的 accept 循环串行（循环体内 `await HandleClientAsync`），
服务端同一时刻只服务一个车载连接。判据不涉及协议：持有一条已完成握手、一个字节不发的 TLS 连接，
第二个客户端握手始终不完成；第一条一关，第二条立即通过。修法是排序——先停车载端与其代理，
再把服务端交给业务面。

同时修掉一个我自己引入的自指字段：`harnessWorktreeClean` 在运行结束时采集，而仓内的 EvidenceRoot
此时已是未跟踪内容，导致该字段恒为假。改为运行开始、任何证据落盘前采集。

### 路由指针

Owning repository: https://github.com/trytoreachpeak0/8005-agv-control-server
Published branch/commit: `ControlServer_MVP@6a678a1`（已推送，回读一致）
Owner artifact: `evidence/g3/20260830-business-message-fault-injection/`（绿），
`evidence/g3/20260829-business-message-fault-injection/`（红证据，保留判据）
Impact on this ticket: 已解决；`OperationResult` 与 `SlotOperationCommand` 转入票 19 的前置事实。
