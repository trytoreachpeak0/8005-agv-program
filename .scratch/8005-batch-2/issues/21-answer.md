# 票 21 答复 —— 车载端 `FP-IS-07` 两个向量缺口的关闭

**状态：done（已提交，未推送）。**
`8005-agv-onboard-hmi` `w2g/fp-v2-impl` = `ea3c75e`（`581e902` 落地 ＋ `ea3c75e` 复审修正）。

---

## 一、开工前先证伪了交接文档的两条

上一份交接（`…-20260909-j.md`）把票 17 的三条障碍列为「其中两条待用户裁定」。开工前逐条实测，
**两条已经不是待裁定项了**，理由都是同一条纪律：`git ls-remote --heads origin`。

| 交接里的说法 | 实测 |
| --- | --- |
| 第七节第 6 条：`dotnet format` 那道坎「怎么解」待裁定，「属于对方仓库的决定」 | **对方已经决定了。** 远端 `w2g/normalize-line-endings` HEAD `9ee7e4d`「chore(format): 加 `.gitattributes`，把工作区行尾钉成 LF」，Zhengyu Shao，2026-09-09 11:04——比这份交接（10:47）还晚 17 分钟。提交信息里直接写着「这正是 `ONBOARD_HMI_G2` 从未绿过的原因」，实测 22800 条 `ENDOFLINE`。**是待搬运项，不是待裁定项。** |
| 第五节第 3 条：SDK 那条修法在 `w2g/dotnet-sdk-8.0.425`（车载端） | 属实，且**控制端的对应修法在 `ControlServer_MVP` 的 `60b4fc9`**，不在任何 `w2g/*` 分支上。交接只提了车载端那一条。 |

搬运时还实测出一处交接没提的不对称：

- **控制端本线 `fp/v2-impl` 早就有 `* text=auto eol=lf`**（`.gitattributes` 第一行）。
  障碍 1 **只存在于车载端**。
- 车载端本线的 `.gitattributes` 只有票 15 加的 `vendor/8005-agv-protocol/** -text` 一条，
  缺全局那条；而 `9ee7e4d` 那份只有全局那条、没有 vendor 那条（它从 MVP 线出，那条线没有
  vendor 目录）。**两边要合并，且顺序有意义**——vendor 那条必须在全局那条之后，否则
  71 个文件的 SHA-256 会全部漂移。这条留给票 17。

---

## 二、SDK 基线已搬（用户 2026-09-09 定）

两条都是 cherry-pick，保住出处，各只改 `global.json` 一行：

| 仓 | 来源 | 落地 |
| --- | --- | --- |
| `8005-agv-onboard-hmi` `w2g/fp-v2-impl` | `7a4e509`（`w2g/dotnet-sdk-8.0.425`） | `3f26a32` |
| `8005-agv-control-server` `fp/v2-impl` | `60b4fc9`（`ControlServer_MVP`） | `a143c9c` |

效果实测：两个仓库目录内 `dotnet --version` 都返回 `8.0.425`。
**交接第六节第 1 条那个「仓库外临时目录钉 global.json ＋ 绝对路径指 .csproj」的绕法作废**，
本线之后直接在仓库里跑就行。

⚠️ **代价原样结转：**`7a4e509` 自己留的那句话仍然成立——**CI runner（`win11-01`）仍是
8.0.424**，而门禁证据与发布包都在它上面产出。搬运之后，那台机器现在会 `dotnet` 失败。
**这是票 17 出证前必须先解决的事**，见第七节。

---

## 三、`CV-FAULT-CARGO-HANDOFF` 的缺口比票据写的更深一层——但本票没有补它

票 20 的结论是「实现全有、测试全无，补一套 G2 夹具即可」。**实现确实全有，但它有一处
`HANDOFF_ONLY_ON_AUTHORIZED_COMMAND` 兑现不了的地方**，是建夹具时撞出来的：

> **命令自带的 `commandContentSha256` 从未被比对过。**

`WireToGateSessionClient` 对它做了 `RequireSha256` 形状校验，然后
`HandleFaultCargoRecoveryCommandAsync` 根本没把它传下去。`BindRecoveryVectorCommandAsync` 里
那个 `RECOVERY_COMMAND_HASH_MISMATCH` 比的是 `context.CommandContentSha256`——**本端自己算的
那份**，首次绑定时盖上去，之后只跟自己比。也就是说：

- 它能在本端状态漂移时触发（比如 `slotOperationAttemptId` 变了）；
- 它**永远不会**因为「服务端授权的内容与本端认为的不同」而触发。

而服务端发这个字段的**唯一目的**就是后者。对照组就在同一个仓里：resume 路径
`WireToGateSlotOperationExecutor` 一直在比对它的对应字段
（`context.CommandContentSha256` vs `resume.CommandContentSha256`）。

### 一度补上，复审之后撤回

`581e902` 顺手把比对启用了。复审（第七节）指出两件事，两件都成立：

1. **超出票据边界。**票据第一节对 `CV-FAULT-CARGO-HANDOFF` 写的是「**只加测试**」。
2. **代价是具体的，不是理论上的。**该字段对 `FaultCargoRecoveryCommand` 的哈希含
   `forcedRecoveryGeneration` 一项，车端取 `state.ForcedRecoveryGeneration`、服务端取
   `workflow.ForcedRecoveryGeneration`。两端**只在收到过同一条强制恢复命令之后才收敛**——
   服务端抬了代际而那条命令没送达车端（操作员取消、连接中断），此后每一条故障货命令都会卡
   在这道新门上。**把三条已发布向量押在一个跨仓、无守卫的前像约定上，不是这张票该做的事。**

`ea3c75e` 撤回。**缺口本身如实留在这里，留给单独一张票。**

### 撤回前核过的事实，留着给那张票用

两端的哈希函数逐一对齐过，**启用比对本身在算法上是安全的**：

| 消息 | 控制端 | 车载端 | 一致 |
| --- | --- | --- | --- |
| `LoadCompensationCommand` | `Compute(actionId, demandId, attemptId, slotsJson)` | `ForLoadCompensation(...)` 同 4 段 | ✅ |
| `LoadCorrectionCommand` | `Compute(correctionId, demandId, attemptId, Serialize(slots))` | `ForLoadCorrection(...)` 同 4 段 | ✅ |
| `FaultCargoRecoveryCommand` | `ForRecoveryAction(workflowId, demandId, attemptId, slotsJson, generation)` | `ForRecoveryAction(...)` 同 5 段 | ✅ |
| `ForcedMechanicalRecoveryCommand` | 同上 | 同上 | ✅ |

两端的 `Compute` 都是 `SHA256(string.Join('|', parts))` 转小写十六进制，逐字节同构；
`workflow.WorkflowId = actionId`（`OnboardRecoveryCoordinator.cs:366`）；
`SlotsJson = JsonSerializer.Serialize(slots)` 与车载端产出同一个字符串。
**风险不在算法，在两端代际的收敛时机。**那张票要先解决这个，才谈得上启用。

### 本票怎么覆盖 `HANDOFF_ONLY_ON_AUTHORIZED_COMMAND`

改由**作用域**证明：命令指向另一个 `handoffId`，其余字段全部匹配，
`BindRecoveryVectorCommandAsync` 判 `RECOVERY_SCOPE_MISMATCH`。
这是这条断言本来就有的那一半，且是既有机制，不新增风险。自证 C 证过它不是空跑。

---

## 四、`CV-FORCED-MECHANICAL-RECOVERY`：补了什么

`ForcedMechanicalRecoveryCommand` 此前落进 `WireToGateSessionClient.cs` 那个
`WireToGateRecoveryCommand` raw-JSON 兜底桶，被 `WireToGateRecoverySafetyPolicy` 对着
`WireToGateRecoverySafetyFacts.Unknown` 判一下、记条日志就完了。补齐的清单在提交信息里，
这里只记**三处不能照抄既有向量**的地方：

### 1. 结果 payload 不同形

`ForcedMechanicalRecoveryResult` 与其余四条向量的 result 有三处结构差异，
照抄 `SendRecoveryVectorResultAsync` 的现有分支会写错：

| 差异 | 为什么 |
| --- | --- |
| **没有 `demandId`** | 命令那一半的 `demandId` 是 `nullable`，结果里根本没这个字段 |
| **没有 `slotResults`** | 其余四条都带逐仓结果数组，这一条只带裸 `slots`。强制机械恢复是人手撬门，**车端没有可信的逐仓电子读数可报** |
| **`electronicEmptyProven` / `vehicleReadyProven` 是 `const: false`** | schema 层面禁止这条消息声称证明了电子空载或车辆就绪。这是这条向量的语义核心，也是 `forbiddenSideEffects` 里 `ready-before-reconciliation` 与 `unknown-as-success` 的落点 |

两个 proof 字段在发送点**硬编码 `false`**，`ValidateForcedMechanicalRecoveryResult` 里再挡一道
（传 `true` 直接 `PROTOCOL_SCHEMA_INVALID`）。写成两道不是冗余：schema 用 `const` 钉住，
说明协议作者认为「有人会算出 `true`」是个真实风险；把它挡在本端，日志里就不会留下一条
车辆支持不了的声称。

### 2. 栅栏的两半在**不同**位置，这是 `581e902` 里写错、`ea3c75e` 改对的地方

`REFUSE_STALE_FORCED_RECOVERY_GENERATION` 有两半，一开始被当成一件事写在了一起：

| | 位置 | 为什么 |
| --- | --- | --- |
| **拒绝** | `HandleRecoveryVectorCommandAsync`，读状态之后、重放短路之前 | 陈旧命令既不进日志也不碰仓门 IO，`return` 前只发一条 `RECOVERY_BLOCKED` |
| **抬升** | `BindRecoveryVectorCommandAsync` 的写回处，**所有作用域比对都过之后** | 这个代际得先被证明真的授权了这条向量 |

**`581e902` 把抬升也放在了拒绝旁边，那是一个真 bug**（复审查出，见第七节）：

> 一条携带 `forcedRecoveryGeneration: 999` 的命令，**即使随后因作用域不符被拒**，也已经把
> 车端的栅栏永久抬到 999。此后服务端按自己的代际继续发命令，车端一律判为陈旧拒掉，而
> **没有任何路径会把栅栏降下来**——恢复通道从此关闭，起因只是一条车端已经决定不服从的消息。

fail-closed、不可恢复、由未经校验的输入触发。`ea3c75e` 把抬升挪进绑定，与上下文盖章同一次
写入（一个没有对应上下文的代际，会把车辆挡在没有任何记录的工作之外）。
`ForcedRecoveryGenerationIsNotRaisedByACommandRefusedOnScope` 守住它，自证 B 证过。

判据是 `generation < state.ForcedRecoveryGeneration` 才算陈旧；**相等是正常重传，不是陈旧**。

### 3. 栅栏参数做成必填，不是可选

`HandleRecoveryVectorCommandAsync` 已经有 12 个参数，加第 13 个的自然做法是给个
`long? forcedRecoveryGeneration = null` 的默认值，只有新调用点传。**没这么做。**

可选参数默认「不设栅栏」是一种 fail-open 形状：第六条向量接进来时，什么都不写就自动继承
「不设防」。改成必填之后，四个既有调用点各写一行 `forcedRecoveryGeneration: null`——
**那四个 `null` 从此是记录在案的决定，不是遗漏。**（票 15 的复审查出过一条自己引入的
fail-open，这条纪律是从那里来的。）

---

## 五、票据验收第五条那条「不执行任何仓门 IO」怎么做到**可断言**

`581e902` 在这里推理反了，值得原样记下来。

当时八个仓位初始都是「已锁、输出复位、**无货**」。`WireToGateRecoveryVectorExecutor`
`ExecuteClearAsync` 有一条短路——目标仓位本来就没货时直接标 `COMPLETED`，不调
`PulseUnlockAsync` 也不调 `WaitForLockerAsync`。于是**成功用例的 `UnlockCount` 也是 0**。

当时的论证是：「两种路径的 `UnlockCount` 都是 0，这条断言只能靠结果消息来区分，那正是要证的
东西。」——**这句话自己就承认了 `Assert.Equal(0, UnlockCount)` 在拒绝用例里什么也没证。**
一条对成功路径同样成立的断言，不是断言。

`ea3c75e` 改成：**拒绝用例给目标仓位放货**（`io.SetCargoPresent`）。命令若被接受，执行器会先
`PulseUnlockAsync`（计数变 1）再因别的原因失败，所以 `UnlockCount == 0` 只在真被拒时成立。
成功用例保持无货，走短路，仍然 0。

第二处同形的问题：`WaitForInboundAsync` 匹配的是 `Server.SentEnvelopes`，**服务端一写出命令
就返回**，不证明车端读过它——拒绝用例的每一条「什么都没发生」都可能因为「还没发生」而成立。
改成等守卫自己发布的 `RECOVERY_BLOCKED` 操作员事件，订阅建立在 `business.Start()` 之前，
不留缝隙。

（顺带：`FakeIoModuleClient.WaitForLockerAsync` 至今 `throw new NotSupportedException("G2会话
测试不执行仓位操作。")`。本票没有解除它——四条测试都不需要走到那一步。真正驱动物理解锁的
G2 夹具仍然不存在，**这是票 17 要面对的下一层**。）

---

## 六、三条自证（真做过，原样输出）

基线：`154 passed`（`SQCD.Agv.UnitTests`）＋ `37 passed`（`SQCD.Agv.WireToGateG2Tests`）。
落地后：`154 passed` ＋ `42 passed`，Debug 与 Release 都跑过，0 failed 0 skipped。

**复审改动了守卫，所以三条自证都是对 `ea3c75e` 的版本重跑的。**
自证前把 `WireToGateBusinessService.RecoveryVectors.cs` 复制到临时目录，
SHA-256 = `f05b6e646012578a25dce605c3a94d93f466b21507c7180dad46cd1ddba016bf`。

### 自证 A：删掉代际栅栏的拒绝分支

```
  Failed SQCD.Agv.WireToGateG2Tests.RecoveryVectorG2Tests.StaleForcedRecoveryGenerationIsRefusedWithoutSlotIoOrResult [5 s]
  Error Message:
   Timed out after 5s waiting for: a guard to publish a RECOVERY_BLOCKED operator event
```

陈旧命令没有被拒绝，守卫从未发布拒绝事件。**测试不是空跑。**

> 第一次跑这条时失败信息是无信息的 `A task was canceled`。**这本身是一条发现**：拒绝用例的
> 超时是一个真实结论，值得读起来像结论。`WaitUntilAsync` 因此改成超时即 `Assert.Fail` 并说明
> 在等什么，上面那行是改完之后的输出。

### 自证 B：把代际抬升挪回绑定之前（即 `581e902` 的那个 bug）

```
  Failed SQCD.Agv.WireToGateG2Tests.RecoveryVectorG2Tests.ForcedRecoveryGenerationIsNotRaisedByACommandRefusedOnScope [497 ms]
  Error Message:
   Assert.Equal() Failure: Values differ
Expected: 0
Actual:   9
```

作用域不符被拒的命令，把栅栏从 0 抬到了 9。**这正是复审描述的那条路径，现在有守卫了。**

### 自证 C：删掉 `handoffId` 的作用域比对

```
  Failed SQCD.Agv.WireToGateG2Tests.RecoveryVectorG2Tests.FaultCargoCommandNamingADifferentHandoffIsRefusedWithoutSlotIo [5 s]
  Error Message:
   Timed out after 5s waiting for: a guard to publish a RECOVERY_BLOCKED operator event
```

指向另一个 handoff 的命令被照单执行。**`HANDOFF_ONLY_ON_AUTHORIZED_COMMAND` 的覆盖是实的。**

三次都从副本还原，还原后 SHA-256 复核一致（`f05b6e64…`），行尾与编码未变
（`Unicode text, UTF-8 text, with CRLF line terminators`，无 BOM）。

---

## 七、双轴复审的处置

按交接第八节跑了 `mattpocock-skills:code-review`（Standards ＋ Spec 两个子 agent）。
**这是它第四次在当票查出最实质的缺口**——票 14 查出 7 处 v1 形状的报文，票 15 查出一条自己
引入的 fail-open，票 20 查出一条真的假绿，本票查出一个 fail-closed 的真 bug。

### 采纳并已修（`ea3c75e`）

| # | 轴 | findings | 处置 |
| --- | --- | --- | --- |
| 1 | Spec | **代际抬升发生在授权校验之前**，一条被拒的命令能永久抬高栅栏，fail-closed 不可恢复 | 抬升移进 `BindRecoveryVectorCommandAsync`，新增回归测试 ＋ 自证 B。见第四节第 2 条 |
| 2 | Spec | **`commandContentSha256` 比对是范围外改动**，且把三条已发布向量押在两端代际的收敛时机上 | 撤回，缺口如实留在第三节，另开一张票 |
| 3 | Spec | **`Assert.Equal(0, UnlockCount)` 对成功路径同样成立**，在拒绝用例里什么也没证 | 拒绝用例改成目标仓位放货。见第五节 |
| 4 | Spec | **`WaitForInboundAsync` 匹配 `SentEnvelopes`**，服务端一写出就返回，不证明车端读过 | 改等守卫自己发布的 `RECOVERY_BLOCKED`。见第五节 |
| 5 | Standards | **日志缺关联信息**（`docs/ARCHITECTURE.md` §6 要 `operationId`、仓位、错误码） | 两条新日志补齐，错误码用协议注册表里**已注册**的 `FORCED_RECOVERY_GENERATION_STALE` |
| 6 | Standards | **`authoris*` 是英式拼写**，仓库既有一律 `authoriz*` | 本次引入的全部改掉（实测：仓里所有 `authoris*` 都是本票引入的） |
| 7 | Standards | **`NullLogger` 与 `WireToGateG2Tests` 里那份重复**，且那份是 `private` 无法复用 | 提成程序集内共享的 `RecordingLogger` |

第 5 条值得单独说一句：**跟着那条编码规范走，找到了一个已注册的错误码**
（`vendor/8005-agv-protocol/errors/error-codes.json` 有 `FORCED_RECOVERY_GENERATION_STALE`，
控制端 `ServerReasonCodes.ForcedRecoveryGenerationStale` 在用，车载端
`WireToGateSessionClient.cs:2367` 的已知集合里也有它）。原来那条日志是自己编的文本。

### 核过但不采纳

| # | 轴 | findings | 为什么不改 |
| --- | --- | --- | --- |
| 8 | Standards | **Shotgun Surgery ＋ Repeated Switches**：第五条向量牵动 8 处（`IsKnown`、journal 两处守卫、派发 switch、bind 的豁免、result switch、`RecoveryActionId` 三元、假服务端），没有任何地方收敛「一条向量是什么」 | **属实。**收敛成 per-vector 描述子会改到既有四条向量的行为路径，超出本票边界。**记在这里，值得单开一张票**——它与第九节第 2 条是同一类问题 |
| 9 | Standards | **`HandleRecoveryVectorCommandAsync` 13 个参数**，一族参数总是同行同现，是一个 `RecoveryVectorCommandScope` 想出生 | 同上。顺带：复审说「把 `forcedRecoveryGeneration` 论证成必填是在争另一条轴」——**这条不接受**，必填与提取参数对象正交，提取之后那个字段在描述子里仍然不能有默认值 |
| 10 | Spec | **null-`demandId` 拒绝**丢掉了 schema 声明合法的命令（`anyOf [Id, null]`） | **行为上没有区别**：`WireToGateRecoveryVectorContext.DemandId` 非空，null 的 demandId 在 `BindRecoveryVectorCommandAsync` 里一样会判作用域不符。前置判定只是把它变成一条说得清的 `RECOVERY_BLOCKED`，而不是落到派发处的兜底 catch。保留 |

### 复审自己也有一处不准

Spec 轴第 6 条说「服务端那一半哈希的是字面量 `0`」——**那说的是本票的测试替身**
（`FakeControlServerIdentifiers.RecoveryActionContentSha256(..., 0)` 的故障货分支），不是真实
控制端。真实控制端用 `workflow.ForcedRecoveryGeneration`。**结论仍然成立**（两端代际的收敛
时机才是风险），但成立的理由不是它写的那个。

---

## 八、转交票 17 的四件事

1. **🔴 CI runner 现在会 `dotnet` 失败。** 第二节搬运的直接后果：两个仓的 `global.json` 已经
   要求 8.0.425，而 `win11-01` 是 8.0.424（`7a4e509` 提交信息里记着，2026-09-08T17:15 那次
   出包的 `dotnet --info` 可证）。**门禁证据与发布包都在它上面产出。** 出证前必须先让它升级，
   或由用户决定别的处置。这是搬运的已知代价，用户 2026-09-09 已经在知情下选了「现在就搬」。

2. **障碍 1 的修法已存在，是搬运不是裁定。** `9ee7e4d` 那份 `.gitattributes` 要与本线现有的
   vendor 那条**合并**，且 vendor 那条必须在后（见第一节）。搬完记得整棵工作树会重新展开为
   LF——交接第六节第 2 条那条「先探测再写回」的纪律届时可以退休。

3. **障碍 2 原封不动。** `IntegrationSlice` trait 在车载端仍是 0 处，`run-w2g-g2.ps1` 仍然没有
   `-Slice`。本票**故意没做**（票据第五节边界写明）。顺带实测：**控制端有这一族**——
   `RecoveryStateMachineG2Tests.cs:457` 那条测试同时挂着 `[Trait("IntegrationSlice", "FP-IS-05")]`
   与 `[Trait("IntegrationSlice", "FP-IS-07")]`。所以这不是「两端都缺」，是单边缺口，
   与票 20 的向量缺口同形。

4. **真正驱动物理解锁的 G2 夹具仍然不存在**，见第五节末。`FP-IS-07` 的向量绑定已经补齐，
   但「解锁—等待反馈—复位」那条路径在车载端至今没有测试驱动过。

---

## 九、本票没碰的两处，记下来免得下次重新发现

1. **`FakeControlServer.SendResumeCommandAfterRecoveryAction` 是死代码。**
   声明在 `FakeControlServer.cs:101`，全仓零引用（`grep` 实测，只有它自己那一行与编译产物）。
   不在本票边界内，没删。

2. **`handoffId` 与 `commandContentSha256` 是两端各算一遍、互不比对的派生。**
   控制端 `StableGuid(identity, purpose)` = `SHA256($"{identity}|{purpose}")` 取前 16 字节整成
   UUIDv5 形；车载端 `StableUuid($"{actionId}|fault-cargo-handoff")` 逐字节同构。
   `RecoveryActionSubmitted` 的 payload 里**没有** `handoffId` 字段，两端谁也不告诉谁自己算的
   是什么——**它们一致纯粹因为两边碰巧写法相同**，而 `BindRecoveryVectorCommandAsync` 会拿它
   当作用域判据。开工时一度以为这是互操作缺陷，逐字节核过才确认不是。

   **没有任何东西把这两份实现钉在一起。**本票的 `FakeControlServerIdentifiers` 里因此有第三份
   副本（测试替身必须扮演服务端那一半），已在该类的注释里写明这层依赖。
   **这值得单开一张票**——形态与票 16／20 完全一致：一个双端约定，没有机器守卫。

---

## 十、票据验收对照

| 验收 | 结果 |
| --- | --- |
| `CV-FAULT-CARGO-HANDOFF` 有具名测试，覆盖两条断言且不只证 payload 形状 | ✅ `AuthorizedFaultCargoCommandIsExecutedAndItsOutcomeIsReported`（`REPORT_HANDOFF_OUTCOME`）＋ `FaultCargoCommandNamingADifferentHandoffIsRefusedWithoutSlotIo`（`HANDOFF_ONLY_ON_AUTHORIZED_COMMAND`，自证 C） |
| `ForcedMechanicalRecoveryCommand` 有 typed payload 与 handler，不再落兜底桶 | ✅ |
| `ForcedMechanicalRecoveryResult` 有发送路径，逐字段合 schema，两个 proof 硬编码 `false` | ✅ 由 `ProtocolPayloadShapeArchitectureTests` 拿**冻结 schema** 实证，不是自己写的期望 |
| `CV-FORCED-MECHANICAL-RECOVERY` 有具名测试，覆盖两条断言 | ✅ `ForcedMechanicalRecoveryOutcomeIsReportedWithNeitherProofClaimed`（`REPORT_FORCED_RECOVERY_OUTCOME`）＋ `StaleForcedRecoveryGenerationIsRefusedWithoutSlotIoOrResult`（`REFUSE_STALE_FORCED_RECOVERY_GENERATION`，自证 A） |
| 陈旧代际被拒时不执行仓门 IO、不产生结果 | ✅ 目标仓位放货使 `UnlockCount == 0` 真正有区分力；另有 `ForcedRecoveryGenerationIsNotRaisedByACommandRefusedOnScope` 守住栅栏不被未授权命令抬升（自证 B） |
| `VectorsThisBatchOwesANamedTest` 清空；两条镜像规则仍绿 | ✅ 字段保留，空集本身是断言 |
| `MessagesWithoutAnImplementation` 里那条钉子移除 | ✅ |
| 两个工程 Debug 与 Release 全绿 | ✅ `154 + 42`，0 failed 0 skipped |
| 自证真做过 | ✅ 第六节，三条，且都对复审后的版本重跑过 |
