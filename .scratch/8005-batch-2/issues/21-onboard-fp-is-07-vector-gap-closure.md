# 21 — 车载端 `FP-IS-07` 两个向量缺口的关闭（`w2g/*` 长期分支）

**做什么：** 把票 20 的守卫报出来的两个 `FP-IS-07` 向量缺口关掉，让
`VectorsThisBatchOwesANamedTest` 这个欠账集清空。

**为什么现在做：** 它是**票 17 的输入**。票 17 要给 `FP-IS-00`～`07` 八个切片各出一份 G2
证据，而 `FP-IS-07` 的六条向量里有两条在车载端**没有任何具名测试**——其中一条连产品代码都
没有。不关掉就不能声称 `FP-IS-07` 重证通过，票 17 的出口是假的。

用户 2026-09-09 定：单开一张票，且**补产品代码**（不是只补能补的那一条）。

## 一、两个缺口的性质完全不同

| 向量 | 车载端现状（2026-09-09 实测） | 本票要做的 |
| --- | --- | --- |
| `CV-FAULT-CARGO-HANDOFF` | **实现端到端全有**：`FaultCargoRecoveryCommandPayload` / `FaultCargoRecoveryResultPayload`（`WireToGateBusinessProtocol.cs:249,257`）、`WireToGateFaultCargoRecoveryCommand`（`WireToGateBusiness.cs:106`）、反序列化（`WireToGateSessionClient.cs:1842`）、`HandleFaultCargoRecoveryCommandAsync`（`WireToGateBusinessService.RecoveryVectors.cs:660`）、`SendFaultCargoRecoveryResultAsync`（`WireToGateSessionClient.cs:340`）全在 | **只加测试**。全仓没有任何测试驱动过 `HandleRecoveryVectorCommandAsync`，要建一整套 G2 夹具 |
| `CV-FORCED-MECHANICAL-RECOVERY` | **只有一个兜底分支**。`ForcedMechanicalRecoveryCommand` 在 `WireToGateSessionClient.cs:1878` 落进 `WireToGateRecoveryCommand` 那个 raw-JSON 泛型桶，无 typed payload、无 handler、无发送方法。`ForcedMechanicalRecoveryResult` 在 `src/` 里 **0 处**——它是票 15 钉在 `ProtocolMessageSurfaceArchitectureTests.MessagesWithoutAnImplementation` 里的两条发现之一 | **补产品代码 ＋ 测试** |

**缺口是单边的。**控制端两条向量都有实现也都有测试
（`RecoveryStateMachineG2Tests.cs:459/694/734`、`WireToGateStoreTests.cs:332`，
`ForcedMechanicalRecoveryResult` 在 `OnboardRecoveryCoordinator.cs` 与
`OnboardMessageProcessor.cs`）。协议冻结的 `ForcedMechanicalRecoveryResult` 方向是
**`O_TO_C`**——本来就该车载端发，缺的是车载端这一半。

## 二、四条产品断言（来自协议仓向量，不是本票发明的）

`8005-agv-protocol@f6ee75d` 的 `vectors/<向量>/expected.json` 里 `productAssertions.onboardHmi`：

| 向量 | 断言 | 含义 |
| --- | --- | --- |
| `CV-FAULT-CARGO-HANDOFF` | `HANDOFF_ONLY_ON_AUTHORIZED_COMMAND` | 只在服务端授权的命令上做交接；作用域不符必须拒 |
| | `REPORT_HANDOFF_OUTCOME` | 交接结果必须上报，且可重放 |
| `CV-FORCED-MECHANICAL-RECOVERY` | `REFUSE_STALE_FORCED_RECOVERY_GENERATION` | 陈旧 `forcedRecoveryGeneration` 的命令必须拒 |
| | `REPORT_FORCED_RECOVERY_OUTCOME` | 强制恢复结果必须上报 |

两条向量的 `forbiddenSideEffects` 都含 `unknown-as-success` 与 `duplicate-slot-unlock`，
`finalState.physical` 都是 `NO_UNPROVEN_STATE`。

## 三、`ForcedMechanicalRecoveryResult` 的 payload 与其余四条向量**不同形**

`schemas/messages/ForcedMechanicalRecoveryResult.schema.json`：

```
exceptionRecoverySessionId, recoveryActionId, forcedRecoveryGeneration,
outcome ∈ {MECHANICALLY_ISOLATED, FAILED, UNKNOWN},
slots, operator, observedAt,
electronicEmptyProven: {"type":"boolean","const":false},
vehicleReadyProven:    {"type":"boolean","const":false}
```

三处与既有四条向量（`LoadCancellation`／`LoadCompensation`／`LoadCorrection`／
`FaultCargoHandoff`）的 result 不一样，**照抄 `SendRecoveryVectorResultAsync` 现有分支会写错**：

1. **没有 `demandId`**。命令那一半的 `demandId` 是 `nullable`，结果里根本没有这个字段。
2. **没有逐仓结果数组**。其余四条都带 `slotResults`（`WireToGateSlotResultPayload[]`），
   这一条只带 `slots`（裸 `int[]`）。强制机械恢复是人手介入，**车端没有可信的逐仓电子读数
   可报**——这正是下一条的原因。
3. **`electronicEmptyProven` 与 `vehicleReadyProven` 是 `const: false`。**
   schema 层面禁止这条消息声称证明了电子空载或车辆就绪。**这是这条向量的语义核心**，
   也是 `forbiddenSideEffects` 里 `ready-before-reconciliation` 与 `unknown-as-success`
   的落点。实现里这两个字段必须是硬编码的 `false`，不是从状态算出来的值。

## 四、可以复用的既有机件（别重造）

- `WireToGateRecoveryCommandHash.ForRecoveryAction(...)`（`WireToGateRecovery.cs:105`）
  **已经收 `forcedRecoveryGeneration` 参数**，`HandleFaultCargoRecoveryCommandAsync` 就在用它。
  强制恢复这条直接复用，不要新增哈希函数。
- `WireToGateRecoveryState.ForcedRecoveryGeneration`（`WireToGateRecovery.cs:173`，`long`）
  已存在，且已在 `RecoveryStateReport` 里上报给服务端（`WireToGateSessionClient.cs:1007`）。
  服务端的 `FENCE_FORCED_RECOVERY_BY_GENERATION` 就是拿它对账的。**车端的
  `REFUSE_STALE_FORCED_RECOVERY_GENERATION` 是同一个数的另一侧**。
- `HandleRecoveryVectorCommandAsync` 的重放短路（读 `resultKey` 的既有 outgoing）与
  `TryClaimOperation` 幂等闸，四条向量共用，第五条照接。

## 五、边界

- **只改 `8005-agv-onboard-hmi`，只在 `w2g/fp-v2-impl` 上。** 不动控制端、协议仓、
  `8005-agv-program` 的代码（本票的 `<NN>-answer.md` 除外）。
- **不动 `vendor/`。** 本票不需要重新 vendor，协议副本已是 `f6ee75d` 那一份。
- **不建 `IntegrationSlice` trait 族、不改 `run-w2g-g2.ps1`。** 那是障碍 2，另一张票。
  本票只挂 `[Trait("ProtocolVector", …)]`。
- **不进门禁、不推送。** 推送与否由用户定。

## 六、开工前必须知道的三件事

### 1. 守卫会自己检查本票的成果

`ProtocolVectorTestBindingArchitectureTests.VectorsThisBatchOwesANamedTest` 里钉着这两条。
**加完测试必须把对应条目从钉住集删掉**，否则
`EveryOwedNamedTestPinBelongsToASliceThisBatchImplements` 的镜像规则会报「钉了但已经有测试」。
守卫是源码扫描型，它扫 `tests/`——**合成源码不能写 raw string literal**（票 20 交接第六节
第 4 条），本票如果要加自证，同样适用。

### 2. 测试落哪个工程

`SQCD.Agv.UnitTests` 是 `net8.0` headless，`SQCD.Agv.WireToGateG2Tests` 是 `net8.0-windows`
要桌面。`HandleRecoveryVectorCommandAsync` 在 `SQCD.Agv.Wpf` 程序集里，
**所以这套 G2 夹具只能落在 `SQCD.Agv.WireToGateG2Tests`**。两个工程都是 VSTest 模式，
trait 过滤写 `--filter "ProtocolVector=…"`。

### 3. 行尾

该仓工作树行尾是混的：checkout 出来的老文件是 CRLF，票 15 之后新写的是 LF。
**改既有文件前先探测该文件自己的行尾**。（远端 `w2g/normalize-line-endings@9ee7e4d` 是这个
问题的上游修法，但它归票 17，本票不搬。）

## 七、验收

**状态：** done —— 2026-09-09 完成，见 [21-answer.md](21-answer.md)。
车载端 `w2g/fp-v2-impl` = `ea3c75e`（落地 `581e902` ＋ 复审修正 `ea3c75e`），
`154 + 42 passed`，Debug 与 Release 都跑过，未推送。

- [x] `CV-FAULT-CARGO-HANDOFF` 有具名测试，覆盖 `HANDOFF_ONLY_ON_AUTHORIZED_COMMAND`
      与 `REPORT_HANDOFF_OUTCOME` 两条断言，且**不是**只证 payload 形状
- [x] `ForcedMechanicalRecoveryCommand` 有 typed payload 与 handler，不再落进
      `WireToGateRecoveryCommand` 那个 raw-JSON 兜底桶
- [x] `ForcedMechanicalRecoveryResult` 有发送路径，payload 逐字段符合 schema；
      `electronicEmptyProven` 与 `vehicleReadyProven` 硬编码 `false`
- [x] `CV-FORCED-MECHANICAL-RECOVERY` 有具名测试，覆盖
      `REFUSE_STALE_FORCED_RECOVERY_GENERATION` 与 `REPORT_FORCED_RECOVERY_OUTCOME`
- [x] 陈旧 generation 的命令被拒时**不执行任何仓门 IO**，且不产生结果消息
- [x] `VectorsThisBatchOwesANamedTest` 清空；两条镜像规则仍绿
- [x] `ProtocolMessageSurfaceArchitectureTests.MessagesWithoutAnImplementation` 里
      `ForcedMechanicalRecoveryResult` 那条钉子相应移除
- [x] `dotnet test` 两个工程 Debug 与 Release 全绿，0 failed 0 skipped，不需要桌面以外的前提
- [x] 自证：真改工作树使守卫红、看红、原样记录、再从副本还原并核 SHA-256
