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
