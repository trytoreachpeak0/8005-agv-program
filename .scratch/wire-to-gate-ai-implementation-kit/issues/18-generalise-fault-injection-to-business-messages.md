# 把故障注入泛化到业务消息面

Type: task
Mode: AFK
Status: open
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
