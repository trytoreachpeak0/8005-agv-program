# 覆盖断联安全收尾与恢复分支向量

Type: task
Mode: AFK
Status: resolved
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

## Answer

新增合成恢复对端 `RunRecoveryProbeAsync`（`ControlServer_MVP@e0d4da3`），十九条断言全 PASS
并绑定 `3d8b00c` + `304e6ad`；证据归档于 ControlServer 仓
[`evidence/g3/20260830-recovery-and-disconnect-vectors/SUMMARY.md`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/9a94c3b99cbe8449140c72c630bd541e87bfa259/evidence/g3/20260830-recovery-and-disconnect-vectors/SUMMARY.md)，
提交 `ControlServer_MVP@9a94c3b`，已推送并回读一致。18 与更早的十二条断言不回归。

### 先做的分类：哪一半可达

按票据要求先读了 `OnboardRecoveryCoordinator`，得到的判据是**是否需要一行
`StationOperations`**，而不是消息类型：

| 恢复动作 | 接受路径可达？ | 判据 |
| --- | --- | --- |
| `FORCED_MECHANICAL_RECOVERY` | **可达** | `ValidateActionPreconditions` 对它直接返回 `null`；`QueueForcedMechanicalRecoveryCommandAsync` 的 `DemandId` 可为 null |
| `RESUME_AFTER_REPAIR` | 否 | 需 `operation.Status == RecoveryRequired`，另需会话上的 `ProvenRecoveryCheckpoint` |
| `COMPENSATE_LOAD_ALL_EMPTY` | 否 | 需 `operation.OperationType == Load` |
| `FAULT_CARGO_HANDOFF` | 否 | `session.DemandId is null` 即拒绝 |
| `LOAD_CANCELLATION` / `LOAD_CORRECTION` | 否 | 需已受理 demand／已 `Committed` 的操作 |

会话本身则**可以无 demand 开启**：`ValidateSessionScopeAsync` 在 `demandId is null` 时直接返回
`null`，只需一行 `SessionRecoveries`（握手即产生）与环境变量里的管理员凭证。

因此范围切成两半：`FORCED_MECHANICAL_RECOVERY` 承载所有需要真实 workflow 的向量，其余七种
只在**授权边界**取证。这不是凑数的负向用例——「服务端拒绝为自己从未受理过的 demand 授权任何
恢复动作」本身就是安全属性，同时把不可达的一半在证据里划出明确边界。

### 断联安全收尾

票据原文要求「在仓位操作进行中断开」，该形态不可达。改为对服务端出向的
`ForcedMechanicalRecoveryCommand` 注入 `drop-and-close`——它是唯一无需 demand 的已授权恢复命令，
且同样是「服务端已提交决定、车载尚未收到」的中途断联。

```
droppedCommandMessageId          6d8081bc-4033-5858-aecc-be278dd920f5
droppedCommandSessionGeneration  3
replayedCommandSessionGeneration 4
```

合成对端收到 `RecoveryActionAccepted` 后连接即断，命令一个字节未达。重连并发
`RecoveryStateReport` 后，`ReplayPendingCommandsAsync` 从**同一条 outbox 行**重发了同一 messageId
的命令，`recoveryActionId` 与 `forcedRecoveryGeneration` 均未变。

线上字节不相等是预期行为：`ReplayPendingForSessionAsync` 只重写 `sessionGeneration`，`sentAt` 仍
冻结在 `row.CreatedAt`。判据因此取自身份而非字节——`ProtocolOutbox` 中该消息类型仅两行（两次
动作各一行），`rowCount` 均为 1，断联没有制造第二条命令。

### 恢复分支与代际

两次 `FORCED_MECHANICAL_RECOVERY` 之间必须插入一次报告新代的 `RecoveryStateReport`，否则
`ReportedForcedRecoveryGeneration != ForcedRecoveryGeneration` 会直接拒绝——这条串接关系是本轮
新确立的事实。`VehicleRecoveryGenerations` 从 1 单调推进到 2 后：

| 结果消息 | 代 | workflow 终态 | 证据行 |
| --- | --- | --- | --- |
| 指向第一次动作 | 1（已被取代）| `HistoricalOnly` | `historicalOnly = true` |
| 指向第二次动作 | 2（当前）| `RecoveryRequired` | `historicalOnly = false` |

第二条走的是成功分支，**服务端仍置为 `RecoveryRequired` 而非 `Reconciled`**——强制机械恢复是
隔离不是完成。会话保持 `EXECUTING`，`CLOSED` 会话数 0，`Reconciled` workflow 数 0，
`OrderIntents`／`AcceptedDemands`／`StationOperations` 全为 0。

### RIoT UNKNOWN 对账：不可达，已具名并路由

RIoT 指向死端口且不存在 demand，不会发生任何建单尝试，也就无从产生 UNKNOWN。已写入
`recoveryProbe.coverageLimits` 并指向既有审计链 `evidence/g3/20260829-authorized-single-real-create/`。
它需要一次对接真实 RIoT 的带 demand 运行，属于票据 10 的范围，已在票据 10 追加指针。

### 两条方法论的执行

- **判据先单独证出来**：正式运行前用两个秒级回路把 harness 与 PowerShell 断言分别证过——
  `Check-RecoveryProbe.ps1` 在本机发布的 ControlServer 上跑完整探针（不写证书存储、不弹框），
  `Check-RecoveryAssertions.ps1` 把 runner 的数据库观测段与断言段**原样抽出**喂给真实产物，
  再逐条施加单点变异：车辆代际停在 1、旧代结果被当作当前代、会话报 `CLOSED`、出现
  `Reconciled` workflow、命令从未被丢弃、命令在同代重放、重复的命令 outbox 行、多出一条硬件
  恢复记录——**八条全部被检出**，还原后全绿。正式运行因此一次通过。
- **身份字段必须为真**：同一份 harness 曾以未提交状态先跑过一次并全绿，但那次
  `commits.harness` 只能报出 `6a678a1`——一个并不含本次探针的身份，`harnessWorktreeCleanAtStart`
  随之为 `false`。该次证据已作废删除，提交 `e0d4da3` 后重跑，本目录身份可直接采信。

### 顺带确立的三条事实（后续票据可直接用）

1. **管理员凭证**：`CONTROL_SERVER_RECOVERY_AUTHENTICATION_PROOF` 由 runner 每次运行现生成注入
   服务端环境，`RedactRecoveryAuthenticationProof` 保证不落库，并已加入证据 secret scan。
2. **恢复请求不受 readiness 门禁**：`OnboardMessageProcessor` 对恢复消息只做 `RequireCurrentSession`，
   不要求会话 `READY`，因此合成对端不必先补 Capability／Safety 快照。
3. **`AdvanceForcedRecoveryGenerationAsync` 会栅栏该车所有未确认 outbox 行**，但发生在命令入队
   之前，所以新命令不会被自己这一步栅栏掉。

### 运行后独立复核

不采信 `temporaryTrustCleanupVerified` 自报：`CurrentUser\Root` 中 `CN=8005 staged G3*` 计数为 0；
58205／58207／58215／58216／1502／58006 均无 LISTEN；无 `SQCD*` 残留进程（`ControlServer.Host`
PID 32544 是已安装服务）。本轮只改 `scripts/` 下的验证脚本，未触产品代码或测试项目，未跑 tier 1。

`formalSlicePass = false`，`W2G-IS-00`／`W2G-IS-06`、完整 G3 与 RC 仍为 `INCONCLUSIVE`。
