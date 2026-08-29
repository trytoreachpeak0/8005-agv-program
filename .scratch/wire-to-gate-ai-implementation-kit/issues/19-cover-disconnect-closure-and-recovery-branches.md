# 覆盖断联安全收尾与恢复分支向量

Type: task
Mode: AFK
Status: open
Blocked by: 18

## Question

在票据 18 交付的泛化故障注入之上，如何取得票据 10 要求的「断联安全收尾」与「恢复分支」两类向量
在当前双端 commit（`ControlServer 3d8b00c` + `OnboardHmi 304e6ad`）下的机器可读证据？

### 为什么排在 18 之后

两类向量都需要在业务消息中途制造断联，而这正是票据 18 交付的注入能力。在 18 落地前，
`PumpAsync` 只能对 `RecoveryStateReport` 的 `DurableAck` 丢一次包，无法在装货或发车安全检查
中途断开。两票改同一处，串行避免反复冲突。

### 票据 18 交付后已确立的事实（**不要重新摸一遍**）

1. 注入能力已就位：`PumpAsync` 的规则表支持 `drop-and-close`／`drop`／`delay`／`hold-until-next`，
   按 `direction` + `messageType` + `acceptedMessageType` 匹配，一次性触发，由
   `[StagedG3TlsHarness]::AddFault(...)` 在运行时装配。
2. **服务端 accept 循环串行**：`OnboardTcpServer.ExecuteAsync` 在循环体内 `await
   HandleClientAsync`，同一时刻只服务一个车载连接。合成对端不能与真实车载端并存——必须先停车载端
   再驱动业务面。runner 已按此排序。
3. **本票范围里有一半在 staged 运行中不可达**，与 18 同源：
   - 「在仓位操作进行中断开」需要一行 `StationOperations`，它只由 `PrepareSlotOperationAsync`
     写入，需来自 MesIngest 与 RIoT 的已受理 demand。
   - `OperationResult` 同理不可达（`SingleAsync` 在 `StationOperations` 上解析 forced recovery
     generation，捏造 attempt 会在确认前抛出）。
   - 恢复动作族（`LoadCancellationStartRequested` 等）走
     `OnboardRecoveryCoordinator.ProcessRequestAsync`，先确认它需要多少既有 workflow 状态，
     再决定哪些分支能在无 demand 的 staged 运行中取证。

   **先做这一步分类**：把本票范围切成「staged 可达」与「需带 demand 运行」两半，可达的先取证，
   不可达的具名写进 `coverageLimits`，不要为了凑覆盖率捏造 `StationOperations` 行——那会同时
   破坏 `noMovementOrExternalSideEffects` 断言的含义。

### 范围

- **断联安全收尾**：在仓位操作进行中断开连接，断言服务端把操作与 Demand 转入
  `RecoveryRequired` 而非误报完成，物理事实不被提交，车辆租约不释放。
- **恢复分支**：驱动 `protocol-v0.1.1` 的恢复动作、resume、cancellation、compensation、
  correction、fault-cargo 与 forced-mechanical 命令族，断言 `ForcedRecoveryGeneration` 单调推进、
  旧代迟到结果只进历史证据、不重复建单／不重复仓门副作用／不重复完成。
- 同时把「RIoT UNKNOWN 对账」作为正式 G3 向量记录——该行为已在
  `evidence/g3/20260829-authorized-single-real-create/` 的审计链中出现，但从未作为向量断言。

### 完成判据

新增断言全部 PASS 且绑定 `3d8b00c` + `304e6ad`；18 与更早的断言不回归；证据归档于 ControlServer
仓 `evidence/g3/`，票据只留路由指针。

### 注意

同票据 18 的注意事项：不动车、不建单、不使用现场凭据，`StageRoot` 用短路径，
`-InstallTemporaryCurrentUserRoot` 逐次授权并复核无残留。
