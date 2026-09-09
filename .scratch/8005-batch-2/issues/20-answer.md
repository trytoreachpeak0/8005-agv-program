# 20-answer —— 车载端 `vectorId` ↔ 具名测试绑定守卫

**状态：done（2026-09-09）。** 交付分支 `w2g/fp-v2-impl`，仓库 `8005-agv-onboard-hmi`。
`OnboardHmi_MVP` 零推送，`src/`、`docs/`、根 `README.md` 零改动（**该仓没有 `CLAUDE.md`**，
票 15 已实测，本次复审再次确认）。

本文只写票据没有、或与票据不一致的东西。能在票据里读到的不重复。

---

## 一、一句话结论

守卫落地了，但**车载端不是控制端的镜像**：31 个冻结向量里，本批次范围（`FP-IS-00`～`07`）的
20 个中只有 **18 个**能绑上真实的具名测试。剩下两个都属 `FP-IS-07`，都是真缺口，**不是排期**。
所以钉住集是两个而不是一个，票据验收第五条按字面写不成立——见第四节。

---

## 二、四处裁定

### 1. 守卫读源码，不用反射。控制端那份照抄不过来

控制端的 `ProtocolVectorTestBindingArchitectureTests` 用
`typeof(...).Assembly.GetTypes()` 反射自己这个程序集拿 trait。**车载端做不到**：

| 工程 | TFM | 依赖 |
| --- | --- | --- |
| `tests/SQCD.Agv.UnitTests` | `net8.0` | Core / Application / Infrastructure / AutomationHost |
| `tests/SQCD.Agv.WireToGateG2Tests` | `net8.0-windows` | ＋`src/SQCD.Agv.Wpf`（`WireToGateBusinessService` 在这里） |

31 个向量里有一半只由 G2 那个工程证明，而 `net8.0` 工程**不能引用 `net8.0-windows` 工程**。
票据验收第四条要求守卫落在 `SQCD.Agv.UnitTests` 且不需要桌面——两条约束合起来，反射方案会把
每一个只由 G2 证明的向量都报成"没有具名测试"，也就是**守卫只看得见半个仓库**，和票 16 留下的
那个洞同形。

所以改成**源码级扫描**：读 `tests/` 下两个工程的 `.cs`，认 `[Trait("ProtocolVector", "…")]`
attribute 块，归到它下面那行声明上。这不是新发明——本仓 `ReasonCodeRegistryArchitectureTests`
已经是全局源码扫描（扫 `src/`），本票沿用它的形态与 `FindRepositoryRoot()`。

**源码扫描比反射弱在两处，两处都补上了，且补法是"报红"而不是"忽略"：**

| 反射能做而文本不能 | 本票的处理 |
| --- | --- |
| 知道 `[Fact(Skip = …)]` 不跑 | 复现了。`RunsAsATest()` 读 `[Fact]/[Theory]` 的实参，含 `Skip` 就不算绑定，并进 `ClaimsOnTestsThatDoNotRun`，由 `NoProtocolVectorTraitSitsOnATestThatDoesNotRun` 报红 |
| 把类级 trait 应用到类内每个方法 | **不复现，改成禁止。** 文本解析类作用域是那种会静默出错的半吊子解析。`NoProtocolVectorTraitSitsOnATypeDeclaration` 直接对类级 `ProtocolVector` trait 报红，让盲点变成红而不是悄悄少算 |

另加一条 `TheScanCoversBothTestProjects`：分别扫两个工程目录，各自断言 `NotEmpty`。**这条是让
源码扫描诚实的那一条**——万一目录改名、排除规则吃多了，扫不到 G2 了，只由 G2 证明的向量会集体
需要钉住，而那个钉看起来像"缺口"而不像"扫描器坏了"。

### 2. 扫描器扫 `tests/`，而这个守卫自己就在 `tests/` 里

两条自证用的合成源码**不能写成 raw string literal**。写成字面量的话，它内部那几行
`[Fact(Skip = …)]` / `[Trait("ProtocolVector", …)]` 在本文件里就是货真价实的 attribute 行，
扫描器扫到自己，两条探针会把自己报成 offence。所以改成 `string.Join('\n', "…", "…")`——
每行都以引号开头，本文件任何一行都不会被当成 attribute。

**这是自指陷阱，不是风格问题。**控制端不会遇到（它用反射），下一个照抄的人会踩。

### 3. 不引入新的批准哈希常量

票 15 转交第 1 条说得对：`integration-slices/index.json` 进 vendor 之后由
`manifest/release.json` 的 `files` 表接管，不需要新常量。实测该表里有

```
{"path": "integration-slices/index.json", "role": "integration-slices",
 "bytes": 19766, "sha256": "71e0a63d49d1973653e1f70addc19c334faff5e53e8597733c1423a7307bd82f"}
```

与 `8005-agv-protocol` HEAD `f6ee75d` 的那个文件逐字节一致。
`ProtocolIdentityArchitectureTests.EveryOtherVendoredFileIsPinnedByTheManifestFileTable` 的
`Assert.Equal(70, …)` 已按转交事项改成 `71`（类文档里"pins all seventy-one"同步改成
seventy-two——那句算的是含 manifest 自己的总数）。

**但本票另外在守卫自己这里再核一遍**（`TheVendoredIndexIsPinnedByTheManifestFileTable`）：
下面每一条断言都把那个文件当协议本身来读，是这个类的前置条件。前置条件由远处一个类负责，
等于把"有人把那个 sweep 改窄了"这件事交给别人报——照
`ReasonCodeRegistryArchitectureTests` 对注册表文件的做法，在本地再核一次。

### 4. 钉住集是两个，不是一个

见第四节。

---

## 三、绑定实测结果：18 个向量 / 53 条 trait

**票据开工说明第 4 条"钉住集与控制端逐条相同"再一次被证伪**——票 15 已经在消息面那侧证伪过
一次，向量这侧同样不成立。控制端 20 绑 11 钉，车载端 **18 绑 13 钉**。

| 向量 | 条数 | 具名测试 |
| --- | --- | --- |
| `CV-SESSION-RECOVERY-HAPPY` | 4 | `HappyPathCompletesFullSequenceAndBecomesReady`、`BusinessBootstrapsRecoveryRequestBeforeServerSnapshot`、`ReadyWireToGateSessionDoesNotRemainInLegacyConnectingState`、`RecoveryRequiredIsVisibleWithTheServerReason` |
| `CV-SESSION-RECONNECT-DURING-RECOVERY` | 2 | `ReconnectDuringRecoveryRebindsDurableReportWithoutUnlockSideEffects`、`SameJourneyRevisionsWithStablePayloadAreAcceptedAcrossSessionGenerations` |
| `CV-SNAPSHOT-REPLACE-AND-ACK` | 2 | `SnapshotReplaceAndAckAcceptsHigherRevisionOnNewConnection`、`JourneySnapshotsAreProjectedAndHeartbeatDoesNotStealAsyncMessages` |
| `CV-SNAPSHOT-SAME-REVISION-CONFLICT` | 3 | `SameRevisionDifferentContentFailsClosedWithProtocolProblemReasonCode`、`SameJourneyRevisionWithDifferentContentFailsClosed`、`AppliedJourneyJournalUsesCanonicalPayloadForSameRevisionIdentity` |
| `CV-DEMAND-ACCEPT-TO-PICKUP` | 5 | `DemandAcceptanceSnapshotsArePersistedBeforeAcknowledgement`、`PersistedDemandProjectionIsRestoredWhenServerDoesNotResendIt`、`DropoffStopSnapshotsAreProjectedRatherThanRefused`、`APlanWhoseLegsAllNameTheWorklistDemandIsConsistent`、`APlanNamingADifferentDemandThanTheWorklistIsNotConsistent` |
| `CV-PICKUP-SUBLOT-LOAD` | 3 | `LoadUsesOnlyServerFrozenSlotsAndJournalsBeforePulses`、`AuthoritativeJourneyMustContainMatchingSublotBeforeScan`、`FormalSlotOperationCommandIsValidatedAndRaisedWithoutPhysicalSideEffect` |
| `CV-LOAD-CORRECTION` | 1 | `CorrectionRequiresEmptyThenOccupiedSequence` |
| `CV-LOAD-CANCELLATION-ALL-EMPTY` | 1 | `ClearSkipsEmptySlotsAndUnlocksOnlyOccupiedSlots` |
| `CV-PREDEPARTURE-SAFETY-EXPIRES` | 4 | `ExpiredEvidenceIsUnknownAndDoesNotPreserveStopped`、`StaleSnapshotIsRejectedBeforeUnlockAndDeparture`、`DelayedStoppedSafetyRevisionRecoversSessionToReadyWithoutIoSideEffects`、`FailedThenStoppedProviderRefreshFlowsThroughBusinessServiceToReady` |
| `CV-OPERATION-RESULT-UNKNOWN-RECONCILE` | 5 | 两个 `UnknownSnapshotFailsClosedWithoutUnlock`、`ActiveUnlockCheckpointIsNotPulsedAgainAfterUncertainFailure`、`AllUnknownIoStatesAreReportedWithoutImplyingSingleSlotFault`、`SingleUnknownIoStateIdentifiesAffectedPhysicalSlot` |
| `CV-DESTINATION-UNLOAD-ALL-EMPTY` | 2 | `UnloadAllTargetSlotsRequiresEverySlotToReachEmpty`、`UnloadFlowRequiresCargoAndReportsEmptySlot` |
| `CV-CONNECTION-LOSS-SAFE-FINISH` | 3 | `LoadUsesOnlyServerFrozenSlotsAndJournalsBeforePulses`、`SuccessfulResultIsRetriedWithSameMessageAfterConnectionRecovers`、`BusinessSafetySendFailureDisconnectsAndReplaysPendingRevision` |
| `CV-RELIABLE-RETRY-SAME-CONTENT` | 4 | `DurableOutboxIsAcknowledgedAfterServerDurableAck`、`BusinessProgressUsesStableDurableMessageAndDoesNotDuplicateAfterAck`、`LostSafetyStateChangedAckReplaysSameIdentityAndBusinessContentFromJournal`、`SuccessfulResultIsRetriedWithSameMessageAfterConnectionRecovers` |
| `CV-RELIABLE-RETRY-DIFFERENT-CONTENT` | 1 | `DurableOutboxRejectsDifferentContentForSameDeduplicationKey` |
| `CV-REQUEST-FIRST-RESULT-REPLAY` | 3 | `ReplayingACompletedVectorKeepsTheSameObservedAtAndDoesNotPulse`、`DuplicateOperationIdDoesNotUnlockAgain`、`MissingManualChargingReturnToServiceResultTimesOutExplicitly` |
| `CV-EXCEPTION-RESUME` | 5 | 三个 `Resume*`（`WireToGateSlotOperationExecutorTests`）、`ResumeAuthorizationRequiresExactPersistedAttemptAndCheckpoint`、`RecoverySessionAndActionResponsesAreCorrelatedWithoutPhysicalIo` |
| `CV-EXCEPTION-COMPENSATE` | 1 | `ActiveUnlockCheckpointIsNotPulsedAgainAfterUncertainFailure` |
| `CV-MANUAL-CHARGING-RETURN` | 4 | 四个 `ManualChargingReturnToService*` |

绑定依据是各向量 `expected.json` 的 `productAssertions.onboardHmi`（那是协议对**车载端**这一侧
的要求，与 `controlServer` 那一侧是两回事），不是消息名匹配。

---

## 四、票据验收第五条：按字面写不成立，改成两个钉住集

票据原文：

> - [ ] 钉住集里每条都写明切片与批次，且拒绝任何属于 `FP-IS-00`～`07` 的向量被钉住

**这一条建立在"车载端与控制端同形"的假设上，而假设不成立。**车载端有两个属于 `FP-IS-07`
的向量没有具名测试：

| 向量 | 性质 | 实测 |
| --- | --- | --- |
| `CV-FAULT-CARGO-HANDOFF` | **实现全有，测试全无** | 接收环解析 `FaultCargoRecoveryCommand`，`WireToGateBusinessService.HandleFaultCargoRecoveryCommandAsync` 走共用的 recovery-vector 路径执行并回 `FaultCargoRecoveryResult`。全仓唯一碰这条消息的测试是 `ProtocolPayloadShapeArchitectureTests`，它证的是 **payload 形状**不是**交接行为**——给它挂 trait 就是这个守卫存在的意义所要防的那种假绿 |
| `CV-FORCED-MECHANICAL-RECOVERY` | **实现缺一半，测试无从写起** | `ForcedMechanicalRecoveryResult` 在 `src/` 里没有实现，是票 15 已经钉在 `ProtocolMessageSurfaceArchitectureTests.MessagesWithoutAnImplementation` 里的两条发现之一。`REPORT_FORCED_RECOVERY_OUTCOME` 在产品代码改动之前没有东西可断言 |

三条路，选了第三条：

1. **并进 `VectorsAwaitingTheirSlice`** ——把缺陷说成排期。否决。
2. **让守卫落地即红** ——违反验收第四条（`dotnet test` 绿），而且红没有说明。否决。
3. **第二个钉住集 `VectorsThisBatchOwesANamedTest`**，每条写明切片、批次与**发现内容**。

**第三条保住了验收第五条真正想要的那个性质**——钉住集不能变成停车场。两条互为镜像的规则：

- `EveryScheduledPinBelongsOnlyToSlicesThisBatchDoesNotImplement`：排期集里不许有
  `FP-IS-00`～`07` 的向量（原验收那一条，原样保留）。
- `EveryOwedNamedTestPinBelongsToASliceThisBatchImplements`：欠账集里**只许**有
  `FP-IS-00`～`07` 的向量，外加两集交集为空。

有了镜像那条，一个批次 6 的向量不能被悄悄改标成"本批次欠账"，反过来也不行。**两个集合谁也
吸收不了谁的条目。**

`CV-FAULT-CARGO-HANDOFF` 那条**本可以由一条新测试关掉**——票据边界写的是"不改产品代码，
只加测试与 vendor 副本"，加测试在范围内。没做，理由是：全仓没有任何 G2 测试驱动过
`HandleRecoveryVectorCommandAsync`，要建的是一整套新夹具（异常恢复会话状态、
`ForcedRecoveryGeneration`、日志与 IO），那是一张票的量，而**它正好是票 17
（`FP-IS-00`～`07` 重证）的份内事**。守卫的职责是把缺口报出来，不是替下一张票把缺口补上。
**这两条就是票 17 要处置的输入。**

---

## 五、两条自证（真做过，原样输出）

自证纪律：先把文件复制到临时目录，改完从副本还原并核 SHA-256，不用 `git checkout --`。

### 自证一：删掉某向量唯一的具名测试 → 变红

删除 `tests/SQCD.Agv.UnitTests/WireToGateRecoveryVectorExecutorTests.cs` 里
`CorrectionRequiresEmptyThenOccupiedSequence` 整个方法（`CV-LOAD-CORRECTION` 唯一的绑定），
第 63～86 行连同其后的空行。

```
[xUnit.net 00:00:01.16]     SQCD.Agv.UnitTests.ProtocolVectorTestBindingArchitectureTests.EveryFrozenVectorIsBoundToANamedTestOrPinned [FAIL]
  Failed SQCD.Agv.UnitTests.ProtocolVectorTestBindingArchitectureTests.EveryFrozenVectorIsBoundToANamedTestOrPinned [18 ms]
  Error Message:
   These frozen vectors have no named test and are not pinned. Either a test proving them was deleted, or its ProtocolVector trait was: CV-LOAD-CORRECTION

Failed!  - Failed:     1, Passed:    18, Skipped:     0, Total:    19, Duration: 288 ms - SQCD.Agv.UnitTests.dll (net8.0)
```

还原后 SHA-256 回到 `a72f21ed2578032587c343a1aaf9e414cb7b7b36645ebbce44a4f8dbf0b2acff`。

### 自证二：把一个 `vectorId` 拼错 → 两条腿一起变红

在 **`net8.0-windows` 那个工程**（`tests/SQCD.Agv.WireToGateG2Tests/WireToGateG2Tests.cs`）
把 `CV-RELIABLE-RETRY-DIFFERENT-CONTENT` 改成 `CV-RELIABLE-RETRY-DIFFERENT-CONTNET`。
选这一条是因为它同时验证**跨工程扫描真的成立**——守卫跑在 `net8.0` 的
`SQCD.Agv.UnitTests` 里，而这次连 G2 工程都没有重新编译。

```
[xUnit.net 00:00:00.98]     SQCD.Agv.UnitTests.ProtocolVectorTestBindingArchitectureTests.NoTestClaimsAVectorIdTheProtocolNeverFroze [FAIL]
  Failed SQCD.Agv.UnitTests.ProtocolVectorTestBindingArchitectureTests.NoTestClaimsAVectorIdTheProtocolNeverFroze [22 ms]
  Error Message:
   Tests carry a ProtocolVector trait naming vectors the protocol did not freeze: DurableOutboxRejectsDifferentContentForSameDeduplicationKey (tests/SQCD.Agv.WireToGateG2Tests/WireToGateG2Tests.cs:1137) claims CV-RELIABLE-RETRY-DIFFERENT-CONTNET

[xUnit.net 00:00:01.08]     SQCD.Agv.UnitTests.ProtocolVectorTestBindingArchitectureTests.EveryFrozenVectorIsBoundToANamedTestOrPinned [FAIL]
  Failed SQCD.Agv.UnitTests.ProtocolVectorTestBindingArchitectureTests.EveryFrozenVectorIsBoundToANamedTestOrPinned [20 ms]
  Error Message:
   These frozen vectors have no named test and are not pinned. Either a test proving them was deleted, or its ProtocolVector trait was: CV-RELIABLE-RETRY-DIFFERENT-CONTENT

Failed!  - Failed:     2, Passed:    17, Skipped:     0, Total:    19, Duration: 320 ms - SQCD.Agv.UnitTests.dll (net8.0)
```

还原后 SHA-256 回到 `fc2b080eab10096396256b1e1ed9b3edd37f192c6c08d1c52b5f733916b12dcd`。

**两条自证都是对第七节复审加固之后的扫描器重跑的**，不是对早先那一版。

另有六条不需要动工作树的探针作为常驻测试：`TheScannerRefusesToCountASkippedTest`、
`TheScannerReadsMethodTraitsAndReportsTypeTraits`、`TheScannerIgnoresATraitInsideABlockComment`、
`TheScannerReadsMultiLineAndCombinedAttributeLists`、`TheScannerDoesNotReadADisplayNameAsASkip`、
`TheScannerReportsAClaimItCannotAttribute`。

---

## 六、测试与门禁

```
Debug   SQCD.Agv.UnitTests          Passed! - Failed: 0, Passed: 154, Skipped: 0, Total: 154
Debug   SQCD.Agv.WireToGateG2Tests  Passed! - Failed: 0, Passed:  37, Skipped: 0, Total:  37
Release SQCD.Agv.UnitTests          Passed! - Failed: 0, Passed: 154, Skipped: 0, Total: 154
Release SQCD.Agv.WireToGateG2Tests  Passed! - Failed: 0, Passed:  37, Skipped: 0, Total:  37
```

本票新增 19 条测试，全在守卫这一个类里（135 ＋ 19 = 154；票 15 的 172 = 135 ＋ 37）。**守卫全部落在
`SQCD.Agv.UnitTests`（`net8.0`，不引用 `SQCD.Agv.Wpf`），不需要桌面。**

trait 过滤实测可用（VSTest 表达式，不是 `--filter-trait`）：

```
dotnet test tests/SQCD.Agv.UnitTests --filter "ProtocolVector=CV-EXCEPTION-RESUME"
  → Passed: 4
dotnet test tests/SQCD.Agv.WireToGateG2Tests --filter "ProtocolVector=CV-MANUAL-CHARGING-RETURN"
  → Passed: 4
```

**没有进任何门禁**（`run-w2g-g2.ps1` 一次没跑）。

### ⚠️ 本机 SDK 与 `global.json` 已经对不上

`global.json` 钉 `8.0.424` 且 `rollForward: disable`。**本机 2026-09-09 04:19 把 .NET 8 SDK
升到了 `8.0.425`，`8.0.424` 已不在**（`C:\Program Files\dotnet\sdk` 只剩 `8.0.425` 与
`10.0.302`）。所以在仓库目录里跑任何 `dotnet` 命令都直接失败：

```
Requested SDK version: 8.0.424
global.json file: C:\Users\szy\Desktop\8005-fp\8005-agv-onboard-hmi\global.json
Installed SDKs:
8.0.425 [C:\Program Files\dotnet\sdk]
10.0.302 [C:\Program Files\dotnet\sdk]
```

上面所有编译与测试是**在仓库外一个只放了 `global.json`（钉 `8.0.425`）的临时目录里**、用绝对
路径指向 `.csproj` 跑的——同一个 feature band，仓库文件一个没动。

**顺带一条实测证据：SDK 10.0.302 编不过这个仓库。**它的分析器在票 15 留下的
`ReasonCodeRegistryArchitectureTests.cs:576` 上报 `CA1859`，而 `TreatWarningsAsErrors=true`。
所以"随便找个装着的 SDK 顶上"不成立。

### 这件事已经有裁定了，只是还没到本线上

远端分支 `w2g/dotnet-sdk-8.0.425` 的 HEAD `7a4e509`
**`chore(toolchain)!: .NET SDK 基线由 8.0.424 抬到 8.0.425`**（Zhengyu Shao，2026-09-09 10:24）
就是这件事的决议：`global.json` 一行改动 `8.0.424` → `8.0.425`。提交正文写明起因是
Windows Update 的 `KB5126052`／`KB5124008` 替换了同一 feature band 内的旧版本，
`8.0.424` 目录不复存在，**四个可写 .NET 仓在那台机器上全部 `dotnet build` 失败**，
并说明这是 ADR-cross-0056 第一层机制的预期表现而非故障。

所以这条**不是待裁定项，是待搬运项**：

- 那个分支在 **MVP 线**（`protocol-v0.3.0`）上，不在本线。`w2g/fp-v2-impl` 从更早的点分出，
  `global.json` 仍是 `8.0.424`。
- `8005-agv-control-server` 的 `global.json` 同样还是 `8.0.424`。
- **本票没有把那一行搬过来**——改工具链基线不在票 20 的边界内（"不改产品代码，只加测试与
  vendor 副本"），而且它是那位所有者自己带 ADR 引用的决定。要不要 cherry-pick 到
  `w2g/fp-v2-impl` 与控制端，请用户定。

⚠️ **那条提交自己还留了一句**：「**CI runner（`win11-01`）仍是 8.0.424**……在它升到 8.0.425
之前，它会是唯一落后的那台——而门禁证据与发布包都在它上面产出。」**票 17 要在那台机器上出证，
这句直接相关。**

---

## 七、双轴复审（`mattpocock-skills:code-review`）查出一条假绿

按交接文档第七节跑了 Standards ＋ Spec 双轴，prompt 里写明了"vendor 那两万行是逐字节副本，
不要复审"。

### Spec 轴：无 scope creep，无实现错误，抽样绑定无假绿

复审独立核过 vendor 副本（逐字节、19766 字节、`sha256` 与 manifest 表一致）、53 条 trait、
以及两条缺口是否真实（`FaultCargoRecoveryCommand`/`Result` 确实实现在
`WireToGateSessionClient.cs:1842,340` 与 `WireToGateBusinessService.RecoveryVectors.cs:660,1095`，
唯一碰它的测试是 `ProtocolPayloadShapeArchitectureTests.cs:427` 的形状断言；
`ForcedMechanicalRecoveryResult` 无实现，已被 `ProtocolMessageSurfaceArchitectureTests.cs:87`
钉住）。抽查了 `CV-LOAD-CANCELLATION-ALL-EMPTY`、`CV-EXCEPTION-COMPENSATE`、
`CV-DEMAND-ACCEPT-TO-PICKUP`、`CV-RELIABLE-RETRY-DIFFERENT-CONTENT` 四条绑定，**未发现假绿**。

对第四节那个两钉住集的设计，Spec 轴的结论是：**实质上站得住，字面上不成立**——两条镜像规则
让它不是停车场，两条缺口也都是真的，但守卫确实没有对两个本批次向量报红，**这需要用户裁定，
不是一段类注释能替代的**。同意，见第四节。

### Standards 轴：一条真的假绿路径 —— 块注释里的 trait

**这是本次复审最实质的一条，我自己没发现。**加固前的扫描器把"trimmed 以 `[` 开头且以 `]`
结尾"的行当 attribute 行，**不剥注释**。于是这段源码：

```
/*
[Fact]
[Trait("ProtocolVector", "CV-LOAD-CORRECTION")]
public void CommentedOut()
{
}
*/
```

会被读成一个真 attribute 块 ＋ 声明行 `public void CommentedOut()`，**整个被注释掉的测试
仍然绑定它的向量**。跑脚本实测复现了：`claimed ['CV-LOAD-CORRECTION'] -> declaration:
'public void CommentedOut()'`。

这正是本类存在的意义所要防的那一类事（"向量被一个没人跑的测试标成已证"），而且方向是**假绿**，
不是假红。已修：`BlankOutComments()` 先把 `//` 与 `/* */` 全部置空（保留换行，行号不漂），
再做分块。`TheScannerIgnoresATraitInsideABlockComment` 是它的常驻证明。

### Standards 轴其余几条，都改了

| 复审意见 | 处置 |
| --- | --- |
| `VectorTraitRegex` 把 `"ProtocolVector"` 又硬写了一遍，与 `VectorTrait` 常量成了第二份不比对的副本，改名即失明 | 改成把常量拼进 pattern。这条批评用的正是本文件自己的论点 |
| 多行 attribute 读不到 → 静默少算 | 分块改成**括号配平**累加（`BracketDelta`，跳过字符串字面量），多行 attribute 整块读进来 |
| `[Fact, Trait(...)]` 合并列表两个正则都不匹配 | `VectorTraitRegex` 去掉前导 `[` 锚点；`RunnableTestAttributeRegex` 改成 `(?<=[\[,])` 后顾 |
| `[Fact(DisplayName = "Skips…")]` 被当成 skip | `RunsAsATest` 从子串 `Skip` 改成 `SkipArgumentRegex`（`Skip\s*=`） |
| Data Clumps：三个 list 永远一起传 | 收成 `ClaimAccumulator` |
| Duplicated Code：两条镜像规则里同一个 `slices.Any(...)` 谓词写了两遍，只差一个 `!` | 抽成 `BelongsToASliceThisBatchImplements()` |
| Mysterious Name：`NewlyUnbound` 并没有跟任何"之前的状态"比 | 改名 `UnboundAndUnpinned` |
| Primitive Obsession：钉住集的值 `"FP-IS-13, batch 8"` 把切片 id 与批次塞进一个字符串，切片 id 从不被机器核对 | **不改。**复审自己也标了"repo-endorsed"——`ProtocolMessageSurfaceArchitectureTests` 就是这个形状，本票不单方面改族内约定 |

加固过程中**自己又发现一条**：`//` 注释置空之后会在 attribute 与声明之间留下一行空白，
声明就找不到了（`TheScannerIgnoresATraitInsideABlockComment` 第一次跑就是红在这）。已改成
按 C# 规则跳过空白行找声明。

另加一条守卫 `NoProtocolVectorTraitIsLeftUnattributed`：**扫描器读不懂的形状一律报红，不许
静默当成绑定。**这是对"文本解析总有读不懂的东西"这件事的正面回答——读不懂就说读不懂。

### 复审的一条误判

Spec 轴说验收第六条（两条自证）"not delivered，没有 `20-answer.md`"。复审跑的时候本文件
确实还没写。两条自证真做过，原样输出在第五节，且**已对加固后的扫描器重跑一遍**。

---

## 八、转交票 17 的三件事

### 1. ⚠️ 交接文档说"票 20 提供 `IntegrationSlice` trait"——不对，本票没有

`8005-batch-2-handoff-20260909-i.md` 第四节写着：

> 票 17 的第二条障碍是 `run-w2g-g2.ps1` 没有 `-Slice` 参数、不按切片过滤，要按切片出证就得先有
> `IntegrationSlice` trait——**而那正是票 20 的内容**。

**票 20 的十条验收从头到尾只说 `vectorId`，一条都没提 `IntegrationSlice`。**本票按票据执行，
落地后实测：

```
$ grep -c "IntegrationSlice" -r tests/ --include=*.cs   # 命中 0 个文件
$ grep -n "param(" -A5 scripts/run-w2g-g2.ps1
param(
    [string]$ProtocolRoot = '',
    [string]$EvidenceRoot = '',
    [switch]$SkipProtocolG1
)
```

`IntegrationSlice` trait 仍是 0 处，`run-w2g-g2.ps1` 仍无 `-Slice`。**票 17 的第二条障碍原封
不动。**要不要把它单开一张票、还是并进票 17，请用户定。

（顺带：向量 trait 与切片 trait 是正交的两族。本票**故意没有**顺手加切片 trait——一族没有守卫
的 trait 正是这个批次要消灭的那种手工声明，加了就得再配一条守卫，那是另一张票的量。）

### 2. `FP-IS-07` 有两条向量在车载端没有具名测试

见第四节。`VectorsThisBatchOwesANamedTest` 就是这份清单，票 17 要么补测试（`CV-FAULT-CARGO-HANDOFF`
可以，要建 recovery-vector 的 G2 夹具）、要么改产品代码（`CV-FORCED-MECHANICAL-RECOVERY`
必须先实现 `ForcedMechanicalRecoveryResult`）、要么由用户裁定降级。**不处置就不能声称
`FP-IS-07` 重证通过。**

### 3. SDK 版本挡着出证，但决议已存在，只差搬运

见第六节末。修法已经由 `w2g/dotnet-sdk-8.0.425` 的 `7a4e509` 定下（`global.json` 一行），
只是还没到 `w2g/fp-v2-impl` 与控制端上；而且那条提交自己指出 CI runner `win11-01` 仍是
`8.0.424`。这与交接文档第六节第 6 条（`dotnet format` 的 CRLF 冲突）是**两件不同的事**，
两件都挡着票 17。

---

## 九、票据两个未定项，本票没有替用户决定

1. **归哪个批次** —— 未定。产物放在 `w2g/fp-v2-impl`，与票 15 同一条线。
2. **是否阻塞票 17** —— 未定。但第八节第 2 条说明：**不阻塞的代价现在是具体的**——
   `FP-IS-07` 的两个向量在车载端无机器守卫，而票 17 恰好要给 `FP-IS-07` 出证。

另外，交接文档第六节第 7 条那条授权冲突**仍然没解**：`8005-agv-program/CLAUDE.md` 的
「Repository write authority」写着 `8005-agv-onboard-hmi` 对 agent 只读，而票 15／20 明确授权
「只在 `w2g/*` 分支上工作」。**本票与票 15 一样按票据执行**（只改 `tests/` 与 `vendor/`，
`OnboardHmi_MVP` 零推送）。哪句是权威，仍请用户定。

---

## 十、改动清单

| 文件 | 改动 |
| --- | --- |
| `tests/SQCD.Agv.UnitTests/ProtocolVectorTestBindingArchitectureTests.cs` | 新增，19 条测试 |
| `vendor/8005-agv-protocol/integration-slices/index.json` | 新增，逐字节副本，19766 字节 |
| `vendor/8005-agv-protocol/README.md` | 三份→四份、70→71、刷新步骤加一条 `cp`、失败点加一条 |
| `.gitattributes` | 注释里的 70 改 71（只有注释，`-text` 那行没动） |
| `tests/SQCD.Agv.UnitTests/ProtocolIdentityArchitectureTests.cs` | `Assert.Equal(70→71, vendored.Length)`，类文档 seventy-one→seventy-two |
| 另 8 个测试文件 | 只加 `[Trait("ProtocolVector", …)]` 行，53 条，无其他改动 |

`src/` 与 `docs/` 零改动（`git diff HEAD --name-only -- src docs` 为空；该仓无 `CLAUDE.md`）。
