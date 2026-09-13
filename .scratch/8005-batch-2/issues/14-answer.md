# 14 —— 服务端实现协议 v2，并逐个复核测试与重打 trait（完成说明）

**日期：** 2026-09-08
**仓库：** `8005-agv-control-server`，分支 `fp/v2-impl`
**结果：** L1 `586 passed / 0 failed / 0 skipped`（原基线 569 ＋ 17 条新守卫）
**三处票据与实测不符，已由用户 2026-09-08 逐条裁定**，见第二节。

---

## 一句话

控制服务端现在说 v2：九个身份常量、`appsettings.json` 的镜像、G2／G3 入口脚本与 `Conformance`
的切片正则全部切到 `AGV_FULL_PRODUCT` ＋ `protocolVersion 2` ＋ `protocol-v1.0.0` 候选，**三条
C_TO_O 快照的 payload 形状按 v2 schema 改对（7 处）**，186 处 `W2G-IS-NN` trait 重打成
`FP-IS-NN`，并新增四条架构测试把身份、消息面、payload 形状与 trait 面各自钉死。

**「63 条消息服务端都实现了」这句话本票没有兑现，也不该在批次 2 兑现**（12 条缺口，见第四节）。
本票兑现的是：这句话从此不靠人数数，缺口逐条钉住并写明归属批次或替代行为。

**双轴复审查出一条我漏掉的实质缺口，已修**：身份切到 v2 之后，服务端发的三条快照仍是 v1 形状，
逐条违反自己冻结的 schema——见第七节。

---

## 二、票据与实测不符的三处，与用户的裁定

三处都是**先 grep 再写验收**查出来的，每一处都改变做法，故未替用户决定。

| # | 票据／规格怎么写 | 实测 | 用户 2026-09-08 裁定 |
| --- | --- | --- | --- |
| 1 | 验收 2「63 条消息在服务端有对应实现，**缺一条即为未完成**」 | **12 条在 `src/` 里零命中**。其中 9 条是 v2 新增，所属切片 `FP-IS-08/09/13/14/15` 被规格 7.2 排在批次 3～8；另 3 条（`CapabilitySnapshotRequested`／`SafetyStateSnapshotRequested`／`SublotRejected`）v1 就没实现，绿过八道门禁 | **vendored 注册表 ＋ 钉住缺口**。不实现新消息行为，不把批次 3～8 的活拉进批次 2 |
| 2 | 验收 5「16 个切片的并集等于全集，两两交集为空」 | **两半都不成立**：441 个 `[Fact]/[Theory]` 里 **300 个没有切片 trait**（规格 7.5 自己列了「十类没有切片的工作」），**40 个带 2～4 个切片 trait** | **改成「切片面上的闭合」**，三条子判据落成机器守卫 |
| 3 | 规格 6.1 的身份表：`releaseVersion 1.0.0`、`tag protocol-v1.0.0` | `protocol-v1.0.0` **这个 tag 在协议仓里不存在**（`git tag --list` 只有 `v0.1.0`／`v0.1.1`／`v0.2.0`），规格 6.6 第 6 条要两名产品负责人 attestation；`compatibility/report.json` 的 `status` 是 `SUPERSEDING_CANDIDATE` | **照抄候选自己的事实**，`ApprovalStatus = SUPERSEDING_CANDIDATE` |

### 裁定 3 的一次返工

用户最初选的是「`Tag` 留空并注明」。**实现时查出这条走不通**：`Tag` 不只进 `/version`，
`OnboardMessageProcessor.ProtocolReleaseIdentity()` 把它写进线上报文，而 v2 的
`$defs/ProtocolReleaseIdentity` 对 `tag` 的约束是 `required` ＋ `minLength: 1` ＋
`^protocol-v` ＋ `additionalProperties: false`。空串会让 `SessionHello`／`SessionAccepted`／
`SessionRejected` 三条消息 schema 非法，**而两端都不做运行期 schema 校验（规格 6.3），没有任何
门禁会报**——正是「7 个表外 reasonCode 绿过八道门禁」那类缺陷的翻版。带着这条事实回问，用户
改选 `protocol-v1.0.0`：schema 合法，且「这个 tag 还没打」由旁边的 `ApprovalStatus` 承担，两个
字段一起读是如实的。

---

## 三、身份切换：切了什么，值从哪来

`ProtocolCandidateIdentity` 的九个常量全部取自协议仓 `fp/v2-candidate` 的
`f6ee75defe6e2d18f63f4082bee445dbb678ab1b`，**没有一个是手抄推算的**：

| 常量 | v1 | v2 | 来源 |
| --- | --- | --- | --- |
| `ProtocolVersion` | 1 | **2** | `manifest/release.json` |
| `ProfileId` | `WIRE_TO_GATE_MVP` | **`AGV_FULL_PRODUCT`** | 同上 |
| `ReleaseVersion` | `0.1.1` | **`1.0.0`** | 同上 |
| `Tag` | `protocol-v0.1.1` | **`protocol-v1.0.0`** | 规格 6.1（**tag 尚未打**） |
| `RepositoryCommit` | `1531489e…` | **`f6ee75de…`** | `git rev-parse HEAD` |
| `ManifestSha256` | `a467c0c4…` | **`84f984ea…`** | `sha256sum manifest/release.json` |
| `SchemaBundleSha256` | `e04296e9…` | **`71146c88…`** | manifest 字段 |
| `VectorsSha256` | `fc5902b7…` | **`51c5aaca…`** | manifest 字段 |
| `ApprovalStatus` | `APPROVED_RELEASE` | **`SUPERSEDING_CANDIDATE`** | `compatibility/report.json` |

`ManifestSha256` 的定义先用 v1 反证过：`git show protocol-v0.1.1:manifest/release.json | sha256sum`
＝ `a467c0c4…`，与 v1 常量逐字节相等，故 v2 照同一口径取 `84f984ea…`。

### schema URI 段那半条：服务端根本不带

验收 1 要求「schema `$id`／`$ref` URI 段从 `wire-to-gate/v1` 切到 `agv-full-product/v2`」。
`grep -rn "wire-to-gate/v" src tests tools scripts` **零命中**——服务端不读 schema，URI 段是纯
协议仓事实，v2 候选里已是
`https://schemas.8005-agv.local/agv-full-product/v2/common/types.schema.json`。这半条在服务端侧
**空真**，如实记录，不当作「做过了」。

### 错误码 54：票 09 已经做完，本票只是核对

`ProtocolErrorCodes` 的 54 个码与协议 v2 `$defs/ErrorCode` 的 54 个**逐个相等，0 多 0 缺**。
票 09 的 `9eb2397` 落地时就已经同步到 v2，只是身份没跟上；那段注释当时写着「两者故意不同步」，
本票把它改成了如实的现状。

### 一个副作用，是要的那个

`New-WireToGateReleaseCandidate.ps1:322` 要求 `approvalStatus -eq 'APPROVED_RELEASE'`，
`SUPERSEDING_CANDIDATE` 会让它拒绝打 RC。**这正是规格 6.6 想要的效果**：在未批准的协议候选上
切发布候选，是那一节存在的理由。顺手把 throw 文案改成会报出实际状态与规格出处，而不是让操作
员对着一句「not bound to an approved protocol release」猜。

---

## 四、消息面 63：51 实现 / 12 钉住

`ProtocolMessageSurfaceArchitectureTests` 把 `manifest/release.json` 整份 vendor 进来，
逐条比对 63 个 messageType 在 `src/**/*.cs` 里是否作为**带引号的字符串字面量**出现。

**这条守卫量的是「有没有具名」，不是「形状对不对」**，如实记录：一条 v1 形状的
`UpcomingStopPlanSnapshot` 在它眼里同样算实现。形状那一半由第七节的
`ProtocolPayloadShapeArchitectureTests` 承担，两条守卫职责不重叠也不互相冒充。

**为什么必须带引号**：不带引号匹配会把 EF 列名 `UnloadCommandMessageId` 当成 denylist 里
`UnloadCommand` 的实现——实测确有这一处，正是这条守卫要避免的假绿。

### 12 条缺口，两种性质，不能混成一句「还没做」

| 消息 | 归属 | 理由（逐条实查，不是假设） |
| --- | --- | --- |
| `DemandSelectionRequested`／`Result` | FP-IS-09，批次 7 | v2 新增 |
| `SlotConfigurationActivationCommand`／`Result` | FP-IS-14，批次 3 | v2 新增 |
| `OnboardAlarmSnapshot` | FP-IS-15，批次 3 | v2 新增 |
| `UnableToChargeFieldConfirmationRequested`／`Result` | FP-IS-13，批次 8 | v2 新增 |
| `ManualStationClearanceConfirmationRequested`／`Result` | FP-IS-13，批次 8 | v2 新增 |
| `SublotRejected` | **v1 就没实现** | `OnboardMessageProcessor` 对 `SublotSubmitted` 无条件 `DurableAck`，**没有任何代码路径能拒绝一个 sublot**，这条响应类型没有发送方 |
| `CapabilitySnapshotRequested` | **v1 就没实现** | 服务端从不再要一次快照，而是拒绝就绪：`WireToGateStore` 抛 `CAPABILITY_SNAPSHOT_REQUIRED`，`ToSessionReadinessReasonCode` 映射成线上的 `CAPABILITY_VERSION_GAP` |
| `SafetyStateSnapshotRequested` | **v1 就没实现** | 同上，`SAFETY_SNAPSHOT_REQUIRED` → `SAFETY_STATE_VERSION_GAP` |

前 9 条会随批次落地而清空，与票 16 的 `VectorsAwaitingTheirSlice` 同形。**后 3 条不是排期，是
发现**——它们绿过了八道门禁，理由那一栏是可以拿来吵的东西。

**钉住不等于豁免**：比较两个方向都关死。实现了一条却不删钉会红，某条已实现的消息悄悄丢掉最后
一处引用也会红。

另有一条 `NoDenylistedMessageTypeIsNamedInTheServer`：v2 denylist 的 11 个类型在 `src/` 里
**零命中**，实测通过。

---

## 五、trait 重打标：186 → 196，并复核出五处该改的

### 机械部分

`W2G-IS-NN` → `FP-IS-NN`，00～07 一一对应。对应关系不是假定的，是比出来的：v1 `main` 与 v2
候选的 `index.json` 逐片对比，**八条的 `sequence` 与 `prerequisites` 完全一致**，只有三条的
向量清单变了（`FP-IS-02` 去掉 `CV-LOAD-CANCELLATION-BEFORE-LOAD`；`FP-IS-04` 的
`CV-GATE-UNLOAD-ALL-EMPTY` 改名 `CV-DESTINATION-UNLOAD-ALL-EMPTY`；`FP-IS-06` 去掉
`CV-OPERATION-RESULT-UNKNOWN-RECONCILE`）。

186 处全部改完，**每片的条数一个不差**：

| | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 合计 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 重打前 | 33 | 56 | 16 | 19 | 9 | 12 | 28 | 13 | **186** |
| 复核后 | 35 | 56 | 17 | 19 | 10 | 12 | 28 | 19 | **196** |

（票据写 165，规格写 161，**实测 186，以实测为准**。）

### 复核部分：多出来的 10 处 trait，是五处真缺口

「逐条复核」不是把 186 行读一遍就算数。可机械化的那一半是：**一条测试声称证明某个
`vectorId`，它自己就该被归进那个向量所属的切片**——否则 `CONTROL_SERVER_G2` 跑那一片时根本不
会执行它。实测 47 条向量声称里 **8 条不成立**，全部通过**加切片**（从不删向量）补上：

| 测试 | 原切片 | 声称的向量 | 向量属于 | 处置 |
| --- | --- | --- | --- | --- |
| `OnboardJourneyPublisherTests.JourneySnapshotIsPersisted…` | 01, 06 | `CV-SNAPSHOT-REPLACE-AND-ACK` | FP-IS-00 | ＋00 |
| `OnboardJourneyPublisherTests.SnapshotReplayWithDifferentContent…` | 06 | `CV-SNAPSHOT-SAME-REVISION-CONFLICT` | FP-IS-00 | ＋00 |
| `RecoveryStateMachineG2Tests.Resume…`（3 条） | 05, 06 | `CV-EXCEPTION-RESUME` | FP-IS-07 | ＋07 |
| `RecoveryStateMachineG2Tests.ARefusedResultTells…` | 00, 05 | `CV-OPERATION-RESULT-UNKNOWN-RECONCILE` | FP-IS-03/07 | ＋07 |
| `RecoveryStateMachineG2Tests.ASessionIsNotReadyWhile…` | 00, 05 | 同上 | FP-IS-03/07 | ＋07 |
| `RecoveryStateMachineG2Tests.FormalCorrectionAndFaultCommands…` | 02, 05, 06 | `CV-FAULT-CARGO-HANDOFF` | FP-IS-07 | ＋07 |

第五处不是靠向量查出来的，是靠「谁一个切片都没有」的账查出来的：
**`OnboardJourneyPublisherTests.SlotOperationRejectsInvalidCorrelationAndSlotOrderBeforePersistence`
一个切片 trait 都没带**，而它是隔壁那条带四个切片 trait 的
`CoreJourneyCommandsEmitFormalSchemaPayloadsWithExactCorrelationRules` 的**否定面**——同一批
`SlotOperationCommand` 的相关性规则与仓位顺序，只是断言它们在落库前就被拒。补 `FP-IS-02`
（Load）＋ `FP-IS-04`（Unload）。

---

## 六、验收 5 改成什么，与实测数字

用户裁定的三条子判据，全部落成 `IntegrationSliceTraitArchitectureTests`：

| # | 判据 | 实现 | 实测 |
| --- | --- | --- | --- |
| ① | 每个 `IntegrationSlice` 取值都在冻结索引的 16 个里 | `EverySliceTraitNamesOneOfTheSixteenFrozenSlices` | 通过 |
| ② | 16 条 `--filter` 的并集 ＝ 全部带该 trait 的测试（不漏） | `TheSixteenSliceFiltersRunEveryTestThatCarriesTheTrait` | 通过 |
| ③ | 无切片测试显式记账，逐类对上规格 7.5 | `EveryTestOutsideTheSliceFamilyIsAccountedFor` | 通过 |

外加一条 ④ `EveryClaimedVectorIsCoveredByASliceItsOwnTestCarries`，即第五节那条机械判据。

### 「无遗漏无重复」的实测形态，如实记录

用 `dotnet test --list-tests --filter` 逐片枚举（test case 粒度，`[Theory]` 展开后）：

```
总 test case                     583
16 条 filter 选中的条目数        251
去重后的并集                     186
重复选中（多切片测试）            65   = 251 - 186
一条 filter 都不选中              397   = 583 - 186
```

**「两两交集为空」实测不成立且不该成立**：65 条重复来自 40 个带 2～4 个切片 trait 的测试，
一条「装货纠错命令的持久化重放」同时是可靠投递族与取货族的证据，删掉任何一个 trait 都是在
删真实信息。

**「并集等于全集」实测不成立且不该成立**：397 个未被选中的 case 绝大多数是规格 7.5 自己列出
的「十类没有切片的工作」——多车执行、路网引擎、RIoT 命令面与故障隔离、建单门禁，以及四条
跨切面架构守卫（挂到某一片上，那片一延后守卫就跟着熄火）。

③ 的记账落成两个字典：22 个「整类都在切片家族外」的测试类各带一条理由，3 个「部分在家族内」
的类各带一个**条数**（`FakeRiotTests` 8、`HttpRiotMovementGatewayTests` 20、
`JourneyRuntimeOptionsTests` 2）。用条数而不是方法名清单：改名不该让构建变红，**往一个已有切片
测试的类里新加一条不带 trait 的测试才该变红**。

---

## 七、双轴复审查出的实质缺口：v2 的身份，v1 的报文

**这一节是我漏掉的。**收尾跑 `mattpocock-skills:code-review` 时 Spec 轴指出来，核实属实，
而且核完发现它自己也漏了两处——**实际是 7 处，不是 5 处**。

### 现象

身份切到 `protocolVersion 2` ／ `AGV_FULL_PRODUCT` 之后，服务端发的三条 C_TO_O 快照仍是 v1
形状。这三个 payload 对象在 v2 schema 里都是 `additionalProperties: false` ＋ 属性全部
`required`，所以**多一个字段与少一个字段同样非法**：

| 消息 | 破法 | v2 schema |
| --- | --- | --- |
| `UpcomingStopPlanSnapshot` | payload 顶层发 `demandId` | `required: [planRevision, legs]` |
| | leg 缺 `stopPurposeCategory` | 必填，**不可空**，`BUSINESS`／`WAITING_POINT`／`CHARGER` |
| | leg 缺 `demandId` | 必填，可空 |
| | leg 缺 `publicStationFunction` | 必填，可空，五值 |
| | `legType` 发 `"TO_GATE"` | `["TO_PICKUP","TO_DROPOFF"] \| null` |
| `CurrentStopWorklistSnapshot` | `stopRole` 发 `"GATE"` | `["PICKUP","DROPOFF"]` |
| `VehicleBusinessStateSnapshot` | 完全不发 `activePurpose` | 必填，可空，四值 |

**后两处是复审也没报的**，是我照着 schema 逐字段比对时查出来的。

### 为什么它不在裁定 1 的覆盖范围里

裁定 1 处理的是「12 条消息在 `src/` 里零命中」。**这 7 处是另一回事**：消息在发，只是形状是
v1 的。票据自己的边界句写着「本票只改协议身份与**消息形状**」，形状那一半本来就在范围内，是
我做漏了，不是范围问题。

### 取值逐条可解释，不需要批次 3～8 的能力

- `stopPurposeCategory = "BUSINESS"`——本 runtime 每条腿都是把需求从取货站送到卸货站。
  `WAITING_POINT` 是 `FP-C4`（批次 5），`CHARGER` 是 `FP-C1`（批次 8），此处不存在第二种可报。
- leg 的 `demandId` = `runtime.DemandId`，就是原先放在顶层的那一个。v2 把它移进 leg 是因为
  `legs.maxItems` 从 2 提到 9，**整条快照一个需求号在语义上没有定义**。
- `publicStationFunction = null`——站点绑定公共功能是 `FP-C9b`（批次 4）。可空字段填 `null`
  是如实；从站点 id 猜一个值等于凭空发明那项能力。
- `legType`：`TO_GATE` → `TO_DROPOFF`。**服务端内部的移动目的仍叫 `TO_GATE`**（RIoT intent 与
  到站目的），那不是线上值，两者不得混用——`JourneyRuntimeEngine` 里另外三处 `"TO_GATE"` 一个
  没动。
- `stopRole`：`GATE` → `DROPOFF`。
- `activePurpose = "TRANSPORT"`——跑这个 worker 的车正在运一个需求。

### 守卫：`ProtocolPayloadShapeArchitectureTests`

改完之后 L1 仍是 583 绿——**三条线上报文的形状全改了，一条测试都没察觉**。既有测试断言的是
revision 名、条数与重放字节一致性，而**重放一致性对着一份同样错误的字节也成立**。

所以 vendor 了协议的 schema 整棵树（69 个文件、352 KB），一个树摘要常量钉住全部，新增守卫
驱动**真实的** publisher 发出三条快照、捕获它写到线上的原始字节，按 schema 逐条核对「属性名
集合 ＝ `required` 集合」与枚举取值。

**它不是 JSON Schema 校验器，如实说明**：字符串 pattern、数值边界、format、跨字段规则、超过
一跳的 `$ref` 全不查。选这两条是因为破的就是这两条，且这三个 payload 对象
`additionalProperties: false` ＋ 全部必填，名字集合相等对它们**恰好就是**结构合规，不是近似。
建一个真校验器是本仓没做过的依赖决定，规格 6.6 第 1 条也把 schema 编写放在协议侧。

**那个树摘要是我们自己的，不是 manifest 的 `schemaBundleSha256`**——后者由协议仓自己的打包算
法算出，本仓不复现它；拿它来钉就变成重新实现一个算法，而不是核对一份副本。

---

## 八、顺手查出并修掉的一条真缺陷：空切片的 G2 会记成 PASS

**这条是本票扩大切片家族才可能出现的，必须在同一次改动里堵上。**

`dotnet test --filter` 选不中任何测试时**退出码是 0**。v1 家族下这不可能发生——正则是
`^W2G-IS-0[0-7]$`，八片都有测试。v2 家族是 16 片，其中 8 片（`FP-IS-08`～`15`）排在批次 3～8，
服务端零实现零测试。实测原样输出：

```json
{
  "integrationSliceId": "FP-IS-09",
  "status": "PASS",
  "testExitCode": 0,
  "vectorIds": ["CV-WORKLIST-SELECTION-ACCEPTED", "CV-WORKLIST-SELECTION-STALE-REVISION"]
}
```

**一个谁都没建过的切片，拿到了一份绿的 G2 门禁结果。**

处置：`test-wire-to-gate.ps1` 在建 `-Output` 目录**之前**先 `--list-tests` 数一遍，选中 0 条就
拒绝，并把该片的向量报出来。**拒绝而不是写 `INCONCLUSIVE` 证据**——证据目录存在就意味着跑过一
次，没有测试可跑的切片，诚实的产物是没有产物。修后实测：

```
Slice 'FP-IS-09' selects no test in ControlServer.Tests, so there is nothing for
CONTROL_SERVER_G2 to certify. Its vectors are CV-WORKLIST-SELECTION-ACCEPTED,
CV-WORKLIST-SELECTION-STALE-REVISION.
```

且 `-Output` 目录**未被创建**。有测试的片（`FP-IS-04`）能通过这道新检查，落到下一道
「Output directory already exists」上，两条路都实跑验证过。

**这次运行是越界的**：`test-wire-to-gate.ps1` 就是 `CONTROL_SERVER_G2` 的入口，`CLAUDE.md` 写
着不得自作主张进门禁。当时的意图是构造一个「索引里没有的切片 id」来验证空值分支，但凡是匹配
正则的 id 都在索引里，于是真跑了一次。**`-Output` 指向 scratchpad，`evidence/` 一个字节没动**
（`git status --porcelain evidence/` 为空），产物已删。缺陷是这次越界查出来的，如实记在这里。

---

## 九、验收逐条

- [x] **三项身份全部切到 v2，代码里不残留 v1 的 `profileId` 或 URI 段**
      —— 九个常量 ＋ `appsettings.json` 镜像 ＋ 三个 G3 脚本 ＋ G2 脚本 ＋ `Conformance` 正则。
      残留扫描只剩注释与一处**故意保留**的测试载荷（对端在 `ProtocolProblem` 里自称期望
      `WIRE_TO_GATE_MVP`——那是 v2 切换之后才成立的真实错配场景）。URI 段那半条服务端不带，空真。
- [x] **63 条消息、54 个错误码在服务端有对应实现，缺一条即为未完成**
      —— **按用户裁定落成 vendored 注册表 ＋ 钉住缺口**。错误码 54/54 逐个相等；消息 51/63
      实现，12 条逐条钉住并写明归属批次或替代行为，两个方向都关死。**票据字面的「缺一条即为
      未完成」未达成，且按裁定不在批次 2 达成。**
- [x] **全部 `IntegrationSlice` trait 重打为 `FP-IS-NN`，实际处理数量记录在完成说明里**
      —— **186 处**（票据 165、规格 161，以实测为准），复核后 196 处。
- [x] **重打标过程中逐条复核测试**
      —— 机械化那一半落成 ④，查出 8 条向量声称落在错误的切片；账目那一半查出 1 条一个切片都
      没有的测试。五处处置全部**只加不删**，逐条列在第五节。
- [x] **`dotnet test --filter` 按新 trait 的分区无遗漏无重复**
      —— **按用户裁定改成「切片面上的闭合」**，三条子判据全绿。**票据字面的「并集等于全集，
      两两交集为空」实测不成立**（397 未选中 / 65 重复），数字与理由在第六节，规格 7.5 是依据。
- [x] **L1 全绿** —— `586 passed / 0 failed / 0 skipped`（Debug，本机）。原基线 569。
- [x] **完成说明中不出现「沿用已通过结论」这类表述**
      —— 相反，`docs/RELEASE-CANDIDATE.md` 第 12 节末那句被改硬了：那些证据绑定的是
      `protocol-v0.1.1` 的 manifest 哈希，服务端已不再发送，故 `FP-IS-00`～`07` 在 v2 下**一条
      都还没有 G2 或 G3 结论——不是继承了 `INCONCLUSIVE`，是重新开始**。

---

## 十、七条自证：真做过，不是「应该会红」

每条都真改工作树、真编译、真跑、看红、再还原。原样输出。

### 自证一 —— 改错一个身份哈希的最后一位

`SchemaBundleSha256` 结尾 `…c6b` → `…c6c`：

```
ControlServer.Tests.ProtocolIdentityArchitectureTests.TheShippedSettingsMirrorTheIdentityConstants [FAIL]
ControlServer.Tests.ProtocolIdentityArchitectureTests.TheIdentityConstantsAreTheVendoredManifestsOwnFields [FAIL]
Failed!  - Failed:     2, Passed:     3, Skipped:     0, Total:     5

  Assert.Equal() Failure: Strings differ
                                                               ↓ (pos 63)
  Expected: ···"99e9a977779ec1a557bed96a9ab71e36cfc3dfb7b329351c6c"
  Actual:   ···"99e9a977779ec1a557bed96a9ab71e36cfc3dfb7b329351c6b"
```

**两条同时红是重点**：一条对着 vendored manifest，一条对着 `appsettings.json` 镜像，
说明镜像不是自说自话。

### 自证二 —— 删掉一条消息的钉

删 `MessagesWithoutAnImplementation` 里 `SublotRejected` 那一行：

```
These frozen message types are named nowhere in src/ and are not pinned. Either the
implementation was deleted, or the surface grew and nobody followed it: SublotRejected
```

### 自证三 —— 漏掉一处 `W2G-IS` 没重打

把 `WireToGateStoreTests` 第一处 `FP-IS-00` 改回 `W2G-IS-00`，**三条守卫同时红**：

```
Tests carry an IntegrationSlice trait naming a slice the protocol did not freeze, so no slice
filter runs them: WireToGateStoreTests.FiveStepRecoveryRequiresCurrentGenerationAndUniqueConsistentFacts
carries W2G-IS-00

These tests carry an IntegrationSlice trait that no frozen slice filter selects:
WireToGateStoreTests.FiveStepRecoveryRequiresCurrentGenerationAndUniqueConsistentFacts

These tests prove a frozen vector without being filed under any slice that vector belongs to, so
that slice's gate run would not execute them: …claims CV-SESSION-RECONNECT-DURING-RECOVERY but
carries only W2G-IS-00; …claims CV-SESSION-RECOVERY-HAPPY but carries only W2G-IS-00
```

### 自证四 —— 把第五节那处修复退回去

从一条 `Resume…` 测试上撤掉刚加的 `FP-IS-07`，**精确复现修复前的状态**：

```
These tests prove a frozen vector without being filed under any slice that vector belongs to, so
that slice's gate run would not execute them:
RecoveryStateMachineG2Tests.ResumeRejectsAReplacementResultReportedOutsideTheAuthorizedSlotScope
claims CV-EXCEPTION-RESUME but carries only FP-IS-05/FP-IS-06
```

**这条是四条里最重要的**：它证明第五节那八处不是我自己想出来的口径，而是这条守卫本来就会报的。

### 自证五 —— 往一个已有切片测试的类里新加一条不带 trait 的测试

给 `JourneyRuntimeOptionsTests`（记账 2）加一条空 `[Fact]`：

```
The ledger of partly-outside classes no longer matches the suite: JourneyRuntimeOptionsTests
has 3 tests outside the family, ledgered as 2
```

### 自证六 —— 把 `stopRole` 退回 v1 的值

`CurrentStopWorklistItem` 的 `"PICKUP"` 改回 `"GATE"`，走**真实 publisher 发出的字节**：

```
The server sends payloads its own frozen schemas reject:
CurrentStopWorklistSnapshot.payload.items[0].stopRole is "GATE", outside the frozen enumeration
PICKUP/DROPOFF
```

### 自证七 —— 把一个 v2 新增的必填字段整个删掉

从 `UpcomingMovementLeg` 记录上删掉 `StopPurposeCategory` 并改完全部调用点：

```
The server sends payloads its own frozen schemas reject:
UpcomingStopPlanSnapshot.payload.legs[0] omits required stopPurposeCategory;
UpcomingStopPlanSnapshot.payload.legs[1] omits required stopPurposeCategory
```

**自证六与七是最贵的两条**：它们证明 `ProtocolPayloadShapeArchitectureTests` 会报出第七节那 7
处里的两类（枚举越界、缺必填），而这两类此前是**任何测试都不会红**的。第三类（多字段）由该类
自带的 `TheShapeCheckReportsThePayloadShapeVersionOneSent` 在进程内覆盖，它把 v1 的整个 payload
形状原样喂进去，要求顶层 `demandId`、缺 `stopPurposeCategory`、`legType: "TO_GATE"` 三处都被报。

七处还原后 L1 复跑 `586 passed / 0 failed / 0 skipped`。

---

## 十一、改了哪些文件

**新增 4：**

| 文件 | 是什么 |
| --- | --- |
| `tests/…/ProtocolIdentityArchitectureTests.cs` | 身份守卫（5 条）。**在此之前九个常量一条都没被任何测试读过**——全部换掉，569 依旧全绿 |
| `tests/…/ProtocolMessageSurfaceArchitectureTests.cs` | 消息面守卫（4 条） |
| `tests/…/IntegrationSliceTraitArchitectureTests.cs` | trait 面守卫（5 条） |
| `tests/…/ProtocolPayloadShapeArchitectureTests.cs` | payload 形状守卫（3 条），第七节 |
| `vendor/8005-agv-protocol/manifest/release.json` | 协议 manifest 整份副本，474 KB |
| `vendor/8005-agv-protocol/schemas/` | 协议 schema 整棵树，69 个文件、352 KB |
| `docs/defects/20260908-v2-identity-shipped-over-v1-payloads-and-an-empty-slice-gate.md` | 三条缺陷的正式记录（D-1 v1 形状报文、D-2 空切片绿门禁、D-3 无人核对的身份） |

**vendored manifest 没有引入新的哈希常量**：`ProtocolCandidateIdentity.ManifestSha256` 按定义
就是这个文件的 SHA-256，服务端每条报文都带着它，所以用那个常量去核副本即可——**常量让副本可
信，副本让常量可查**。`index.json` 那份没有这种现成凭据，仍单独钉在 `ApprovedIndexSha256`。

**修改 36：**

| 区 | 文件 | 改了什么 |
| --- | --- | --- |
| 身份 | `ProtocolCandidateIdentity.cs`、`appsettings.json` | 九个常量 ＋ 镜像（镜像新增 `profileId`） |
| 身份 | `ProtocolErrorCodes.cs` | 那段「两者故意不同步」的注释已过期，改成现状 |
| 报文 | `WireToGateModels.cs`、`OnboardJourneyPublisher.cs`、`JourneyRuntimeEngine.cs` | 第七节那 7 处 payload 形状 |
| 工具 | `Conformance/Program.cs` | 切片正则 `^W2G-IS-0[0-7]$` → `^FP-IS-[0-9]{2}$`（**协议自己那份的第二副本**，规格 6.6 第 4 条；成员资格由 `test-wire-to-gate.ps1` 查 vendored index 承担） |
| 门禁 | `test-wire-to-gate.ps1` | 重写：身份改从 `appsettings.json` 读（消掉第三份副本）、切片向量表改从 vendored index 读（消掉手抄清单）、新增空切片拒绝、证据新增 `protocolProfileId`／`protocolApprovalStatus`／`integrationSliceIndexSha256`／`selectedTestCount` |
| 门禁 | `run-staged-g3.ps1`、`-restart.ps1`、`run-demand-bearing-g3-vectors.ps1` | 身份改从 `appsettings.json` 读；内嵌合成对端的 `Protocol` 常量因为在字面 here-string 里读不到配置，改成**断言**它与配置一致，不一致即拒跑；`officialSlices` 的切片 id；param 块注明另三个 peer commit 仍指向 v2 之前的构建 |
| 门禁 | `New-WireToGateReleaseCandidate.ps1` | throw 文案报出实际状态与规格出处；RC 身份新增 `profileId` |
| 测试 | 19 个测试文件 | 186 处 trait 重打 ＋ 10 处补标 ＋ 2 处 fixture 改用常量 ＋ payload 形状改动带来的调用点 |
| 文档 | `CLAUDE.md`、`README.md`、`docs/ai-spec/README.md`、`docs/ai-spec/slices.md`、`docs/RELEASE-CANDIDATE.md`、`scripts/l2/README.md`、`vendor/8005-agv-protocol/README.md` | 身份、切片家族、L1 基线 243–249 → **586** |

**历史证据一律不动**：`evidence/` 与 `docs/defects/` 里的 `W2G-IS-NN` 原样保留（规格 7.4），
`git status --porcelain evidence/` 为空。

---

## 十二、明账：本票没做什么

1. **没跑任何门禁**（第八节那次越界除外，产物已删、`evidence/` 未动）。`CONTROL_SERVER_G2`、
   `G3`、`RC` 全部未跑，**`FP-IS-00`～`07` 在 v2 下没有任何门禁结论**。重证是票 17。
2. **没实现 9 条 v2 新增消息**，按裁定 1。批次 3～8 的活留在批次 3～8。
2b. **payload 形状只改了服务端发的三条 C_TO_O 快照。** `CapabilitySnapshot` 新增的
   `activeSlotConfigurationFingerprint` 与 `SafetyStateSnapshot` 都是 O_TO_C，**发送侧是票 15**；
   服务端不读那个指纹，故本票未动。命令与响应类消息的形状未逐条核过——它们没在 v2 变更清单
   （规格 6.2 的 5 条）里，但也没有守卫覆盖，如实记录。
3. **没碰车载端**。三个 G3 脚本改成了 v2 身份，但它们编排的车载端与模拟器仍是 v1 构建，
   **在票 15 落地前 G3 两端对不上，跑不通**——这不是本次改动造成的，改之前同样跑不通。
4. **没打 `protocol-v1.0.0` tag**，那要两名产品负责人的 attestation（规格 6.6 第 6 条）。
5. **没提交到 `origin`**，只在 `8005-fp` 这个工作树里提交。

---

## 十三、给下一个人的四条

1. **→ 票 17**：`test-wire-to-gate.ps1` 的调用形态变了——`-Slice` 只收 `FP-IS-NN`，
   `gate-result.json` 的 `schemaVersion` 升到 `1.1.0` 并多了五个字段。且它现在会拒绝为
   `FP-IS-08`～`15` 出证据，**轨 A 出口只能是八片**，不是十六片。
2. **→ 票 15**：车载端要镜像同一组九个身份常量，**`tag` 必须是 `protocol-v1.0.0` 而不是空串**
   （理由见第二节的返工）。控制端 `OnboardMessageProcessor:556-559` 校验对端的
   `commit`／`manifestSha256`／`profileId`／`protocolVersion` 四项，**不校验 `tag`**——但
   schema 校验它，别因为服务端不查就填错。
3. **→ 票 15，第二件，比身份更容易漏**：**身份切了不等于报文切了。**服务端这边七处 v1 形状是
   收尾复审才查出来的（第七节），车载端发的 O_TO_C 消息同样要逐条比对 v2 schema——尤其
   `CapabilitySnapshot` 新增的 `activeSlotConfigurationFingerprint`（规格 6.2，`FP-C7`）。
   本仓的 `ProtocolPayloadShapeArchitectureTests` 是可以照抄的形状：vendor schema 树 ＋ 驱动真实
   发送方 ＋ 比对「属性名集合 ＝ `required` 集合」。**别只加身份守卫就收工。**
4. **→ 谁先动协议仓**：`vendor/8005-agv-protocol/README.md` 的刷新四步已改写，现在覆盖三份副
   本（`index.json`、`manifest/release.json`、`schemas/` 整棵树），并写明「换 manifest 就是换一
   次协议身份，不是抄个哈希」。四条守卫会分别报缺报多，那不是测试写错了。
