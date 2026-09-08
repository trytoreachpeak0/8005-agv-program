# 15 —— 车载端实现协议 v2（完成说明）

**日期：** 2026-09-09
**仓库：** `8005-agv-onboard-hmi`，分支 `w2g/fp-v2-impl`
**结果：** `168 passed / 0 failed / 0 skipped`（原基线 151 ＋ 17 条新守卫），提交 `f0b4e0d`，已推送
**四处裁定由用户 2026-09-09 逐条定**：三处开工时定（第二节），一处收尾时定（第十三节）。

---

## 一句话

车载 HMI 现在说 v2：三份身份副本全部切到 `AGV_FULL_PRODUCT` ＋ `protocolVersion 2` ＋
`protocol-v1.0.0` 候选，**四类 payload 形状按 v2 schema 改对**，错误码 43 → 54，并新增三个架构
测试把身份、消息面与 payload 形状各自钉死。

**「63 条消息车载端都实现了」这句话本票没有兑现，也不该在批次 2 兑现**（11 条缺口，见第五节）。
本票兑现的是：这句话从此不靠人数数。

**本票查出一条会当场打断联调的缺陷**：车载端的入站校验只认 v1 的 `GATE` ／ `TO_GATE`，而控制端
`978a9e4` 发的是 v2 的 `DROPOFF` ／ `TO_DROPOFF`——**票 17 一开跑就会撞上**。见第四节。

---

## 二、三处裁定（用户 2026-09-09）

| # | 问题 | 裁定 | 落地 |
| --- | --- | --- | --- |
| 1 | 验收第三条「车载端侧 `IntegrationSlice` trait 重打为 `FP-IS-NN`」，而车载端零处 trait | **改写为空真，从零建归票 20** | 票据该行已划掉并注明；本票只改两个门禁脚本里的 `W2G-IS-NN` 字面量 |
| 2 | `CapabilitySnapshot` 新增的必填 `activeSlotConfigurationFingerprint` 发什么值 | **对配置身份取 SHA-256** | `WireToGateSessionClient.ActiveSlotConfigurationFingerprint`，见第六节 |
| 3 | 三处比 v2 schema 更严的入站校验（legs≤2、items≤1、workType 只收 `WIRE_TO_GATE`） | **本票不改，逐条记为发现** | 代码里两条 `<remarks>` 写明它们是业务收窄而非 schema 合规；见第九节 |

### 裁定 1 的一处补充事实

票 20 的开工说明写着「20 绑 / 11 钉的切分对车载端同样成立，钉住集与控制端逐条相同——**但要
自己重测一遍再照抄，别假定**」。**重测的结果是不成立**：控制端钉住的
`CapabilitySnapshotRequested`／`SafetyStateSnapshotRequested`／`SublotRejected` 三条，车载端
**全部具名**，`SublotRejected` 还有完整的解析与校验。切片要两端才证得了，消息实现不用。

---

## 三、身份切换：三份副本，不是一份

票据写「车载端三项身份全部切到 v2」。**实测是三份副本**，`grep -rln "protocol-v0.1.1|WIRE_TO_GATE_MVP|1531489e…"` 查出来的：

| 副本 | 原值 | 现值 | 谁保证它不漂 |
| --- | --- | --- | --- |
| `src/SQCD.Agv.Contracts/WireToGateProtocol.cs` 的 `WireToGateRelease` | 九个 v1 常量 | 九个 v2 常量 ＋ 新增 `ApprovalStatus` | `ProtocolIdentityArchitectureTests` 拿 vendored manifest 逐字段核 |
| `scripts/run-w2g-g2.ps1` 的 `$expected` 表 | 同上 | 同上 | `TheGateScriptExpectsTheSameIdentityAsTheAssembly` 逐字段核 |
| `tests/…/ReasonCodeRegistryArchitectureTests.cs` 的 vendor 路径 | `vendor/…/protocol-v0.1.1/errors/` | `vendor/…/errors/` | 路径里的版本段去掉了——版本是 manifest 里的字段，写进目录名就是第四处要人手同步的地方 |

九个值全部取自协议仓 `f6ee75defe6e2d18f63f4082bee445dbb678ab1b`，与控制端
`ProtocolCandidateIdentity` **逐字节相同**。两端不互相抄，各自读候选；握手比对
`commit`／`manifestSha256`／`profileId`／`protocolVersion` 四项，任一处不同即拒会话。

`ApprovalStatus` 是新加的第十个常量，**故意不进 `Identity`**：v2 的
`$defs/ProtocolReleaseIdentity` 是 `additionalProperties: false` 的九个名字，approval status
不在其中。它是关于这个构建的事实，不是线上身份的字段。
`TheWireIdentityCarriesExactlyTheNineFrozenNames` 把这条钉住了——它序列化真实的
`SessionHello` payload，比对属性名集合与 schema 的 `required`，并断言 `approvalStatus` 不在里面。

### schema URI 段那半条：车载端同样不带

验收第一条提到「schema `$id`／`$ref` URI 段」。`grep -rn "wire-to-gate/v" src tests scripts`
**零命中**——车载端不读 schema 的 `$id`。这半条在车载端侧**空真**，如实记录。

### `run-w2g-g2.ps1` 的 tag 断言：从绑 tag 改成绑 commit

原脚本有一句 `git rev-list -n 1 protocol-v0.1.1^{commit}` 并断言它等于 `$expected.Commit`。
**`protocol-v1.0.0` 这个 tag 不存在**（协议仓 `git tag --list` 实测：`protocol-v0.1.0`、
`v0.1.1`、`v0.2.0`、`v0.3.0`），照搬会让脚本直接失败。改成两条：

- **tag 存在则必须指向候选 commit**（打错地方比没打更危险），不存在不报错；
- **协议仓 HEAD 必须是候选 commit 的后继**，这条取代原来的「tag 是 HEAD 的祖先」。

`summary.json` 的 `protocol` 节相应多了 `tagExists`、`candidateCommit`、
`candidateIsAncestorOfHead`、`approvalStatus` 四个字段，并新增一条 `knownLimitations`
说明本证据绑的是未批准的候选。

---

## 四、四类 payload 形状缺陷，与那条会当场打断联调的

**这一节是本票最实质的部分。**票 14 转交的第 4 条说「身份切了不等于报文切了」，车载端这边
一共四类，**其中两类是接收侧，会让车载端拒收控制端 v2 发出的每一条快照**。

| # | 位置 | 破法 | v2 schema |
| --- | --- | --- | --- |
| 1 | `ValidateCurrentStopWorklist` | `item.StopRole is not ("PICKUP" or "GATE")` | `stopRole` 是 `["PICKUP","DROPOFF"]` |
| 2 | `ValidateUpcomingStopPlan` | `leg.LegType is not ("TO_PICKUP" or "TO_GATE")` | `legType` 是 `["TO_PICKUP","TO_DROPOFF"] \| null` |
| 3 | `VehicleBusinessStateSnapshotPayload` | 没有 `ActivePurpose` | 必填，可空，四值 |
| 4 | `UpcomingStopPlanSnapshotPayload` ／ `WireToGateMovementLeg` | 顶层多 `DemandId`；leg 缺 `StopPurposeCategory`／`DemandId`／`PublicStationFunction` | 顶层 `required: [planRevision, legs]`；leg 九个字段全必填 |
| 5 | `CapabilitySnapshotPayload` | 缺 `ActiveSlotConfigurationFingerprint` | 必填 `Sha256` |

### 为什么 1 与 2 是「当场打断」而不是「潜在」

控制端票 14 已经把这两个值改到 v2（`stopRole GATE → DROPOFF`、`legType TO_GATE → TO_DROPOFF`，
见 `14-answer.md` 第七节）。**所以只要票 17 让两端连起来，车载端收到的每一条卸货工作单与
计划快照都会被判成 `PROTOCOL_SCHEMA_INVALID`。**这不是形状不好看，是会话直接断。

### 3 与 4 的破法是「反序列化直接抛」，不是「字段漏发」

信封反序列化用 `JsonUnmappedMemberHandling.Disallow`（这是该仓一条有意的纪律，注释写着
「悄悄忽略新增或拼错的字段会让两端看起来兼容而做出不同的安全判断」）。所以 payload 里多一个
C# record 没有的字段，**当场抛 `InvalidDataException`**。v2 控制端发的
`VehicleBusinessStateSnapshot` 带 `activePurpose`、`UpcomingStopPlanSnapshot` 的 leg 带三个新
字段——三条快照一条都收不下。

### 5 是发送侧，且没有任何门禁会报

控制端 `978a9e4` 根本不读 `activeSlotConfigurationFingerprint`（`grep -rn` 实测零命中），两端
也都不做运行期 schema 校验。**少发一个必填字段不会有任何东西报错**——正是票 14 那七处缺陷的
同一形状。

### 一个跟着改的投影决定

v2 把 `demandId` 从快照顶层移进 leg（因为 `legs.maxItems` 2 → 9，一条九腿计划配一个需求号
语义无定义）。车载端的 `WireToGateJourneySnapshot.HasConsistentDemand` 读的正是那个顶层字段。
处置：`WireToGateUpcomingStopPlan.DemandId` 改成**由 legs 派生**——非空 `demandId` 去重后恰好
一个就返回它，零个或多个返回 `null`。今天两条腿带同一个需求号，行为不变；将来充电腿／等待点
腿不带需求号时返回 `null` 也是如实的，而不是猜一个。

**不用 `SingleOrDefault`**：它在多于一个时抛异常，而「legs 意见不一」是这个投影必须能活下来
的真实形状。

---

## 五、消息面 63：52 具名 / 11 钉住

`ProtocolMessageSurfaceArchitectureTests` 把 `manifest/release.json` 整份 vendor 进来，逐条比对
63 个 messageType 在 `src/**/*.cs` 里是否作为**带引号的字符串字面量**出现。denylist 的 11 个
类型零命中。

### 11 条缺口，两种性质

| 消息 | 归属 | 理由（逐条实查） |
| --- | --- | --- |
| `DemandSelectionRequested`／`Result` | FP-IS-09，批次 7 | v2 新增 |
| `SlotConfigurationActivationCommand`／`Result` | FP-IS-14，批次 3 | v2 新增 |
| `OnboardAlarmSnapshot` | FP-IS-15，批次 3 | v2 新增 |
| `UnableToChargeFieldConfirmationRequested`／`Result` | FP-IS-13，批次 8 | v2 新增 |
| `ManualStationClearanceConfirmationRequested`／`Result` | FP-IS-13，批次 8 | v2 新增 |
| `ForcedMechanicalRecoveryResult` | **v1 就没实现** | `ForcedMechanicalRecoveryCommand` 走 `WireToGateBusinessService` 的通用分支，被 `WireToGateRecoverySafetyPolicy` 按 `Unknown` 事实阻断并只记日志——**没有任何路径执行它，也就没有路径报结果** |
| `HardwareRecoveryRecordResult` | **v1 就没实现** | `HardwareRecoveryRecordSubmitted` 是 `O_TO_C`，却只作为**入站 case 标签**出现，车载端从不提交记录，自然没有结果要读 |

### 「具名」看不见方向，所以另加一条守卫

「在 `src/` 里带引号出现」这个判据说不出名字在线的哪一侧。实测有 **9 个 `O_TO_C` 消息类型
出现在车载端的入站 `case` 列表里**：

```
ExceptionRecoverySessionRequested   HardwareRecoveryRecordSubmitted
LoadCancellationStartRequested      LoadCompensationRequested
LoadCorrectionRequested             ManualChargingReturnToServiceRequested
RecoveryActionSubmitted             SafetyStateChanged
SlotOperationCommandRejected
```

其中 7 条是车载端自己也在发的消息（标签等于自己的消息回来了），另外两条
`HardwareRecoveryRecordSubmitted` 与 `SlotOperationCommandRejected` 是车载端**本该发起却只会
解析**的消息。

**这 9 条一条都不是 v2 造成的**：拿 `protocol-v0.1.1` 的 manifest 逐条比过，v1 → v2 之间
**没有任何消息改过方向**。它们是 v1 的缺陷被 v2 切换照出来的，不是切换制造的。所以落成
`NoOnboardToServerMessageTypeIsDispatchedByTheReceiveLoopUnlessPinned`，集合精确比较（加第十条
会红），**不在本票里删**——删一个标签会改变车载端对一条走错方向的消息的应答（从「当恢复命令
记日志并阻断」变成 `UNKNOWN_MESSAGE_TYPE`），那是行为变更，要单独的票。

---

## 六、`activeSlotConfigurationFingerprint` 取什么值

裁定 2 的落地。指纹 = SHA-256 over

```
slotModelVersion=<配置值>\n
activeSlotConfigurationVersion=<配置值>\n
slotNos=1,2,3,4,5,6,7,8\n
```

三项就是这个构建上「活动仓位配置」的全部内容：仓位遵循的模型、为它们选定的配置、以及有哪些
仓位。任一项变则指纹变；都不变则跨重启稳定——**稳定是它能当身份用而不是当 nonce 用的前提**。

**它明确不是一个验证结果。** `FP-C7`（配置生效治理）排在批次 3，切片 `FP-IS-14`；在它落地
之前，车载端没有任何东西验证物理仓位与它声称的配置相符，
`SlotConfigurationActivationCommand`／`Result` 也都还没实现（已钉住）。那一片落地时要重新审
这个指纹的输入，值会变。

**为什么不发一个恒定值。** 字段必填、类型 `Sha256`，发六十四个零是 schema 合法的，也是完全
没有意义的——那正是「身份切了报文没切」的形状。控制端今天不读这个字段，所以本仓之外没有任何
东西会察觉。

---

## 七、vendor：三份副本，零个新哈希常量

车载端原先只 vendor 了 `protocol-v0.1.1/errors/error-codes.json`，**而且没有钉字节**（票 20
的开工说明实测过这一点）。本票换成：

```
vendor/8005-agv-protocol/manifest/release.json          （消息面 63 ＋ denylist 11 ＋ 1758 条文件表）
vendor/8005-agv-protocol/errors/error-codes.json        （54 个码）
vendor/8005-agv-protocol/schemas/                       （69 个文件）
```

### 钉法比控制端更省一个常量

控制端给 schema 树另发明了一个 `ApprovedSchemaTreeSha256`。**车载端不需要**，因为链条是现成的：

1. `manifest/release.json` 的 SHA-256 **按定义**就是 `WireToGateRelease.ManifestSha256`，
   车载端每条报文的信封都带着它。`TheVendoredManifestIsTheProtocolManifestByteForByte`
   直接拿那个常量去核副本。
2. **其余 70 个文件逐个出现在那份 manifest 自己的 `files` 表里**，`sha256` 是原始字节摘要。
   `EveryOtherVendoredFileIsPinnedByTheManifestFileTable` 遍历 vendor 目录逐个比对，
   **并断言没有一个文件游离在表外**（反方向那一半才是承重的）。

于是整棵副本的可信度追溯到线上那一个值，链条上**没有任何一处是人手抄进测试的**。

manifest 里的 `errorRegistrySha256`（`ea538d59…`）不是这里用的那个：它由协议仓自己的 JCS
规范化算法算出，与原始字节摘要（`6692bfd2…`）不同。本仓不复现那个算法——复现它就变成了重新
实现一个算法，而不是核对一份副本。

仓库根新增 `.gitattributes` 一行 `vendor/8005-agv-protocol/** -text`（该仓原先没有
`.gitattributes`；只加这一行，不碰其他文件的行尾处理）。刷新步骤写在
`vendor/8005-agv-protocol/README.md`。

### 错误码 43 → 54

纯 append，v1 的 43 个一个没删。`IsProtocolErrorCode` 那份内联清单补了 11 个新码。
`ReasonCodeRegistryArchitectureTests.InlineProtocolErrorCodeSetMatchesVendoredRegistry`
本来就要求两个集合**双向相等**，所以换注册表当场就红了——这条守卫是票 09 留下的，本票只是
把它喂了新数据。

---

## 八、四条新守卫（17 条测试）

| 守卫 | 落在哪 | 条数 | 管什么 |
| --- | --- | --- | --- |
| `ProtocolIdentityArchitectureTests` | `SQCD.Agv.UnitTests`（headless） | 7 | 九个常量 ＝ 候选；vendor ＝ 协议按字节；线上身份恰好九个名字；tag 合法且 approvalStatus 说它是候选；脚本副本不漂 |
| `ProtocolMessageSurfaceArchitectureTests` | 同上 | 5 | 63 条消息具名或钉住（双向）；denylist 零命中；`O_TO_C` 不出现在入站 dispatch（除已钉的 9 条） |
| `ProtocolPayloadShapeArchitectureTests` | `SQCD.Agv.WireToGateG2Tests` | 4 | 驱动真实会话，逐条按 schema 核对车载端发出的原始字节；**fake 服务端发的 C_TO_O 也一起核** |
| `DropoffStopSnapshotsAreProjectedRatherThanRefused` | 同上 | 1 | 第四节那条「当场打断」的回归测试 |

### payload 形状守卫为什么落在 G2 工程

它要驱动**真实的** `WireToGateSessionClient` 走一遍握手与业务面，而 `FakeControlServer` 在 G2
工程里。照抄控制端那句：**手搓的 fixture 只能证明 fixture 自己合规**。一次会话跑出 15 个
`O_TO_C` 消息类型的真实字节，`TheSessionDrivesEveryImplementedOnboardToServerMessageType`
断言覆盖集合恰好等于「已实现 ∖ 已钉住」——**某条发送路径不再被驱动会红**，而不是悄悄少查一条。

5 条钉住的发送路径，两种性质：

- **测试台限制**（2 条）：`LoadCancellationStartRequested` 要等一个 fake 不会合成的
  `LoadCancellationAuthorization`；`ProtocolProblem` 只在拒收时发出，会结束这条会话。
- **根本没有发送路径**（3 条，是发现不是限制）：`DurableAck` 在 manifest 里是
  `BIDIRECTIONAL` 但这一端只收不发；`HardwareRecoveryRecordSubmitted` 与
  `SlotOperationCommandRejected` 见第五节。

### 顺带把测试台也钉住了

`EveryMessageTheFakeServerSendsMatchesItsFrozenSchema` 把 `FakeControlServer` 发的三条 C_TO_O
快照也按 schema 核了一遍。理由：客户端用 `Disallow` 解析入站报文，所以它的 record 与测试台的
字面量**必须**一致——但两者可以一致在一个真实服务端永远不会发的形状上，那时整套 G2 是对着
一个虚构绿的。

---

## 九、本票不改、逐条记为发现的三处（裁定 3）

三处入站校验比 v2 schema 严，会把**合法的 v2 报文**判成 `PROTOCOL_SCHEMA_INVALID`：

| 校验 | 车载端 | v2 schema | 为什么这次不放开 |
| --- | --- | --- | --- |
| `payload.Items.Count > 1` | 最多 1 条 | `items.maxItems: 8` | 上层投影假定单需求：`WireToGateJourneySnapshot.CanAcceptSublot` 要求恰好 1 条，`HasConsistentDemand` 原先用 `SingleOrDefault`——放开校验不放开投影，就是引入一条崩溃路径 |
| `item.WorkType != "WIRE_TO_GATE"` | 只收一个值 | `TransportTaskType` 六个 MES 原始字面值 | 六值是批次 3 以后的业务面 |
| `payload.Legs.Count > 2` | 最多 2 条 | `legs.maxItems: 9` | 第三条腿随等待点（`FP-C4`，批次 5）与充电（`FP-C1`，批次 8）到来 |

**三处今天都打不到**：控制端最多发 2 条腿、1 条 item、只发 `WIRE_TO_GATE`。它们是潜在缺陷不是
现行故障。代码里两条 `<remarks>` 写明了它们是业务收窄而非 schema 合规，以及放开时要连带改
什么。

---

## 十、八条自证：真改、真跑、看红、还原

`14-answer.md` 第十节的样板。每条都是真改工作树、真编译、真跑，下面是原样输出（只截关键行）。

**自证 1 —— `CapabilitySnapshot` 少发指纹**（删掉实参与 record 字段）

```
The onboard sends payloads its own frozen schemas reject:
CapabilitySnapshot.payload omits required activeSlotConfigurationFingerprint
Failed!  - Failed: 1, Passed: 3, Skipped: 0, Total: 4
```

**自证 2 —— schema 守卫抓到手写校验器漏掉的东西**（两处改动：让 `ValidateUpcomingStopPlan`
不再查 `stopPurposeCategory`，同时让 fake 发一个表外取值。这条是双改动，因为要证明的正是
「手写校验器是漂移发生的地方，schema 派生的守卫是抓住它的东西」）

```
The fake control server sends payloads the frozen schemas reject, so the client is being
parsed against a fiction: UpcomingStopPlanSnapshot.payload.legs[0].stopPurposeCategory is
"CHARGING_STOP", outside the frozen enumeration BUSINESS/WAITING_POINT/CHARGER
Failed!  - Failed: 1, Passed: 3, Skipped: 0, Total: 4
```

**自证 3 —— 把两个枚举改回 v1 拼写**（`GATE`／`TO_GATE`）

```
Failed SQCD.Agv.WireToGateG2Tests.WireToGateG2Tests.DropoffStopSnapshotsAreProjectedRatherThanRefused [2 s]
  Error Message:
   System.Threading.Tasks.TaskCanceledException : A task was canceled.
Failed!  - Failed: 1, Passed: 0, Skipped: 0, Total: 1
```

**如实说明**：这条红成超时而不是断言失败——车载端拒收快照，投影永远不出现，`WaitUntilAsync`
一直等到测试 token 取消。红得不好看，但红的原因正是要证的那一条。

**自证 4 —— 把 `ProfileId` 改回 `WIRE_TO_GATE_MVP`**

```
Failed ProtocolIdentityArchitectureTests.TheGateScriptExpectsTheSameIdentityAsTheAssembly
Failed ProtocolIdentityArchitectureTests.TheIdentityConstantsAreTheCandidatesOwnValues
   Assert.Equal() Failure: Strings differ
   Expected: "WIRE_TO_GATE_MVP"   Actual: "AGV_FULL_PRODUCT"
Failed!  - Failed: 2, Passed: 5, Skipped: 0, Total: 7
```

**自证 5 —— 往一个 vendored schema 末尾追加一个空格**

```
The vendored protocol copy is not the protocol: schemas/messages/CapabilitySnapshot.schema.json
is c429796ba64dc370c48788c83053f5ba1377c9d414dd53b62e1a5a01434afcb2,
the manifest says 86e6a53ee79cd49b3169c2cda55859c6ed7ce662fea96b5787a4499fb7c1eb5b
Failed!  - Failed: 1, Passed: 0, Skipped: 0, Total: 1
```

**自证 6 —— 只改门禁脚本里的 `ProfileId`，不改程序集**

```
Failed ProtocolIdentityArchitectureTests.TheGateScriptExpectsTheSameIdentityAsTheAssembly
   Expected: "AGV_FULL_PRODUCT"   Actual: "WIRE_TO_GATE_MVP"
Failed!  - Failed: 1, Passed: 11, Skipped: 0, Total: 12
```

**自证 7 —— 让 `SublotSubmitted` 丢掉在 `src/` 里的最后一处引用**

```
These frozen message types are named nowhere in src/ and are not pinned. Either the
implementation was deleted, or the surface grew and nobody followed it: SublotSubmitted
Failed!  - Failed: 1, Passed: 4, Skipped: 0, Total: 5
```

**自证 8 —— 从 `IsProtocolErrorCode` 删掉一个 v2 新码**

```
'IsProtocolErrorCode' is a second copy of the error-code registry and has drifted.
In the registry but not listed inline: SLOT_CONFIGURATION_FINGERPRINT_MISMATCH
Failed!  - Failed: 1, Passed: 4, Skipped: 0, Total: 5
```

### 一次操作事故，记账

做自证 1 时用了 `git checkout -- src/SQCD.Agv.Infrastructure/WireToGateSessionClient.cs` 还原，
**而那个文件的本票改动全部未暂存，于是被一起抹掉了**。改动是靠重放当时的编辑脚本恢复的，
恢复后 `168 passed` 与恢复前一致。此后的自证一律改成「先复制到临时目录，再从副本还原」。

---

## 十一、`dotnet format --verify-no-changes` 在本机过不了，与本票无关

门禁脚本的第三条命令是 `dotnet format --verify-no-changes`。本机实测 `exit=2`，
**21494 条 `ENDOFLINE` ＋ 16 条 `WHITESPACE`，涉及 71 个 `.cs` 文件——包括本票一个字都没碰的
`App.xaml.cs`。16 条 `WHITESPACE` 全部集中在 `src/SQCD.Agv.Core/DomainModels.cs`，同样没碰过。**

原因是环境的：该 checkout 的 `core.autocrlf=true`，git 把仓库里存的 LF 换成 CRLF 落盘，而
`.editorconfig` 写着 `end_of_line = lf`。实测同一个文件：

```
worktree: 75 73 69 6e 67 ... 0d 0a      （CRLF）
git blob: 75 73 69 6e 67 ... 0a         （LF）
```

**这是票 17 要知道的一件事**：`ONBOARD_HMI_G2` 要在八个切片上各出一份证据，而
`run-w2g-g2.ps1` 把 format 的非零退出码计入 `hmiStatus`。跑门禁的机器要么
`core.autocrlf=false`／`input`，要么给该仓加 `* text=auto eol=lf`——后者会重写全仓文件的行尾，
**属于对方仓库的决定，本票不做**。

---

## 十二、留给票 17 与票 20 的

**给票 17：**

1. **两端现在能对上了。** 车载端 v2 的四类形状缺陷已修，第四节那两条「当场打断」有回归测试
   （`DropoffStopSnapshotsAreProjectedRatherThanRefused`）。
2. **`dotnet format` 那道坎**，见第十一节。**先解决它再排八片的窗口**，否则八份证据全是 FAIL。
3. **`run-w2g-g2.ps1` 没有 `-Slice` 参数**，它跑整个解决方案的测试、不按切片过滤，
   `summary.json` 里 `FP-IS-00` 与 `FP-IS-01` 共享同一个 `onboardHmiG2` 结论。**票 17 要按切片
   分别出证，这个脚本要先改造**——而按切片过滤需要车载端先有 `IntegrationSlice` trait，那是
   票 20。已在脚本的 `knownLimitations` 里写明。
4. **`run-staged-g3-recovery-ack-drop.ps1` 的 `startedScope`** 已改成 `FP-IS-00`／`FP-IS-06`。
   该脚本的 peer commit 绑定本票没动。

**给票 20：**

1. **vendor 目录已经建好并钉住了**，`integration-slices/index.json` 还没 vendor——票 20 要加
   那一份。**加进去之后不需要新哈希常量**：它同样在 manifest 的 `files` 表里，
   `EveryOtherVendoredFileIsPinnedByTheManifestFileTable` 会自动接管它，那条断言的
   `Assert.Equal(70, vendored.Length)` 要跟着改成 71。
2. **`.gitattributes` 的 `-text` 已经挂上**，不用再加。
3. **钉住集不要照抄控制端**，见第二节。
4. `ReasonCodeRegistryArchitectureTests` 读的 vendor 路径已经不带版本段了。

---

## 十三、交付形态：票据那句话在收尾时失效了

**这一节是收尾才出现的，不是开工时能知道的。**准备开 PR 时 `git fetch` 查出的。

### 事实

| 什么 | 交接时（2026-09-08） | 收尾时（2026-09-09） |
| --- | --- | --- |
| `origin/OnboardHmi_MVP` | `641292e`，与本分支零差异 | **`2f14029`，前进了 12 个提交** |
| 车载端钉的协议 | `protocol-v0.1.1` | **`protocol-v0.3.0`**（`ProtocolVersion 3`／`WIRE_TO_GATE_MVP`，PR #19 合并） |
| 控制端 MVP 线 | —— | `ControlServer_MVP` = `b1cb0f3`，**同样已 pin 到 `protocol-v0.3.0`** |

`1ba8d35`（那条 pin 的提交）自己写着：

> 服务端已在 `8005-agv-control-server` 侧升到 0.3.0。明文期两端没有协商也没有降级，版本错配
> 的表现是连接被拒，所以这一半不跟上，现场就是连不上——两端必须同版本才能出包。

`protocol-v0.3.0` 是**已发布**的：2026-09-08 由 product owner 单人签名，commit `345c53c5…`，
release G1 PASS。本票钉的 v2 候选是**未发布**的（`ApprovalStatus = SUPERSEDING_CANDIDATE`，
`protocol-v1.0.0` 这个 tag 至今没打）。

**所以把本分支 PR 进 `OnboardHmi_MVP`，就是把一份已签的发布换成一份未批准的候选。**

### 两条线，本来就是两条

查清楚之后这件事其实是自洽的，只是票据写在它发生之前：

| 线 | 控制端 | 车载端 | 钉的协议 |
| --- | --- | --- | --- |
| **WIRE_TO_GATE MVP**（出货的那条） | `ControlServer_MVP` | `OnboardHmi_MVP` | 已发布 `protocol-v0.3.0` |
| **全产品（本线，批次 2）** | `origin/fp/v2-impl` | `origin/w2g/fp-v2-impl` | 未发布的 v2 候选 |

**控制端这一侧从来没有把 `fp/v2-impl` PR 进 `ControlServer_MVP`。**票 14 落地时也是推长期分支
了事。车载端这一票的票据写「PR 交给 `OnboardHmi_MVP`」，是因为它写在 2026-09-04，那时 MVP 线
还停在 `protocol-v0.1.1`，两条线还没分叉。

### 用户 2026-09-09 裁定

**只推长期分支，不开 PR。**分支名沿用 `w2g/fp-v2-impl`。

推送结果：`641292e..f0b4e0d`，**fast-forward，未 force-push**。远端该分支本来就在（停在
`641292e`，即 PR #13 合并的那条 reasonCode 提交），本次只是把它推进一格。

### 一条协议侧的发现

**`OPERATOR_TIMEOUT` 在已发布的 `protocol-v0.3.0` 注册表里有（44 个码），在 v2 候选里没有
（54 个码）。**两条线在协议仓自己那里已经分叉，不只是两个实现仓分叉。v2 候选的 54 个码是
v1 的 43 个 ＋ 11 个新的，`OPERATOR_TIMEOUT` 是 v0.3.0 在另一条线上加的第 44 个。

**这意味着 v2 候选将来要变成 `protocol-v1.0.0` 时，`OPERATOR_TIMEOUT` 需要有人决定收不收。**
不收就是 v1.0.0 丢掉一个已发布的码（`appendOnly` 破了）；收就要重算 manifest 与三个哈希，
两个实现仓的身份常量跟着全动。**这条不在本票范围内，也不在批次 2 的任何一张票里。**

---

## 十四、待用户裁定，不要替他决定

前四条从上一份交接原样结转，**至今未定**（票 16 的形态偏离、票 20 归哪个批次、票 20 是否阻塞
票 17、`8005-agv-program` 要不要开 PR）。本票新增两条：

1. **第五节那 9 个走错方向的 `case` 标签要不要单开一张票。** 它们都是 v1 缺陷，删掉会改变车载
   端对一条走错方向的消息的应答。已钉住，不会再长。
2. **第九节那三处业务收窄要不要单开一张票。** 今天打不到，但都会在批次 3～8 变成现行故障。
3. **`OPERATOR_TIMEOUT` 怎么并进 v2 候选**，见第十三节末。它已经不是实现仓的问题，是协议仓的
   问题，而批次 2 的票里没有一张覆盖它。
4. **`8005-agv-program/CLAUDE.md` 第 19 行与票 15／20 的授权不一致。** 那里写着
   `8005-agv-onboard-hmi` and `slots-simulator` are **read-only for agents**；票 15／20 则明确
   授权「只在 `w2g/*` 分支上工作」，且 PR #5／#13／#15～#19 都是这么落的。本票按票据执行了。
   **两句话哪句是权威，请你定**——是 `CLAUDE.md` 那行该改成「`w2g/*` 分支可写，其余只读」，
   还是票据的授权本来就该收回。本票没有改 `CLAUDE.md`，那是治理声明，不该我顺手改。
