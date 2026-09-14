# 16 —— `vectorId` ↔ 具名测试绑定架构测试（完成说明）

**日期：** 2026-09-08
**仓库：** `8005-agv-control-server`，分支 `fp/v2-impl`
**结果：** 五条验收全绿，L1 `569 passed / 0 failed / 0 skipped`（原基线 561 ＋ 8 条新守卫）

---

## 一句话

协议冻结的 31 条 `vectorId` 现在由一条架构测试机器守卫：**20 条绑定到具名测试，11 条按规格
7.2 钉住（其切片属批次 3～8，服务端实测零实现）**，两个方向都关死——掉一条绑定会红，钉住集
里多一条或少一条也会红。

**「31 个向量都被测了」这句话本票没有兑现，也不可能兑现**（见第四节）。本票兑现的是：这句话
从此不靠人数数，缺口的形状与理由写在代码里，只能被显式放开。

---

## 二、开工前又查出的三条事实

票据（`fe49efbf`）已经写了两条：两端一个 `vectorId` 标注都没有、控制端没有 vendor 协议仓。
两条都复核属实。下面三条是在它们之外查出来的，第 1 条**更正了票据自己的措辞**。

| # | 事实 | 怎么查的 |
| --- | --- | --- |
| 1 | 那 187 处 `IntegrationSlice` trait **全在控制端，车载端一处都没有** | 票据写「现有的只有 187 处 `[Trait("IntegrationSlice", …)]`」，没说在哪。实测 `grep -rn 'IntegrationSlice' tests/`：控制端 187，车载端 **0**。**票 15 那条「车载端侧 trait 重打为 `FP-IS-NN`」的前提因此不成立**——那是票 15 要面对的，本票未动 |
| 2 | 控制端这个工程走 **VSTest 而非 MTP** | `.github/workflows/test.yml` 用 `--logger 'trx;…'`，且 `Directory.Build.props` 无 `TestingPlatformDotnetTestSupport`。所以 trait 过滤是 `--filter "ProtocolVector=…"`，**不是** `--filter-trait` |
| 3 | `Xunit.TraitAttribute` 是 `sealed`，有公开 `Name`/`Value`，实现 `Xunit.v3.ITraitAttribute` | 用 `System.Reflection.Metadata` 直接读 `xunit.v3.core.dll` 的类型定义。`sealed` 这条决定了不能派生一个具名 `[ProtocolVector]` attribute |

规格 7.2 家族全表的「批次」列是本票的另一条关键依据（它不在票据里，也刻意不进
`index.json`）：`FP-IS-00`～`07` 属批次 2 轨 A，`FP-IS-08`～`15` 分属批次 3～8。

---

## 三、两个设计决定

### ① 测试怎么读到协议仓的 `index.json`

照 `RiotCallAllowlistArchitectureTests` 的形态，vendor 副本 ＋ 钉字节：

| 项 | 值 |
| --- | --- |
| 副本路径 | `vendor/8005-agv-protocol/integration-slices/index.json` |
| 来源 | `8005-agv-protocol` 提交 `f6ee75defe6e2d18f63f4082bee445dbb678ab1b`（`fp/v2-candidate`） |
| SHA-256 | `71e0a63d49d1973653e1f70addc19c334faff5e53e8597733c1423a7307bd82f`（19766 字节，LF） |
| 钉在哪 | `ProtocolVectorTestBindingArchitectureTests.ApprovedIndexSha256`，一处 |
| 行尾 | `.gitattributes` 加 `vendor/8005-agv-protocol/** -text`（原有 `*.json text eol=lf` 会做转换，哈希是按字节绑的） |
| 刷新流程 | `vendor/8005-agv-protocol/README.md`，四步，与 `vendor/8005-agv-program/README.md` 同构 |

**为什么不能读兄弟目录**：CI 的 `actions/checkout` 只取一个仓库，两个仓库是各自独立的克隆，
没有 submodule 也没有包。副本是清单能到达测试的唯一途径，哈希是它不退化成「第二份手抄清单」
的保障——手抄清单会悄悄漂移，按字节绑定的副本不会。

### ② 31 条绑定怎么建

**载体是 `[Trait("ProtocolVector", "CV-…")]`**，与既有 `IntegrationSlice` trait 并存、正交。

- **与票 14 零冲突**：票 14 只改 `IntegrationSlice` 的**值**（`W2G-IS-NN` → `FP-IS-NN`），
  不碰 trait 名，也不碰本票新增的这一族。
- **不做具名 attribute 的硬理由**：`TraitAttribute` 是 `sealed`（实测），自定义就得重新实现
  `ITraitAttribute`，白增一层扩展面。
- **trait 换来一件 attribute 换不来的事**：`dotnet test --filter "ProtocolVector=CV-SESSION-RECOVERY-HAPPY"`
  实跑，输出 `Passed: 2`——正是绑定在那条向量上的两条测试。

落地规模：**47 处 trait，跨 7 个测试文件，覆盖 20 条向量**（一条测试可以同时证明多条向量，
一条向量也可以由多条测试证明）。

---

## 四、20 绑 / 11 钉的切分，与它的代价

`index.json` 实测 16 切片 / 34 条目 / **31 去重**，`vectors/` 31 个目录，双向无遗漏。按规格
7.2 的批次列切分：

- **20 条**只要出现在 `FP-IS-00`～`07`（批次 2 轨 A，票 17 要重证的那八个切片）→ **现在真绑**
- **11 条**只出现在 `FP-IS-08`～`15` → **钉在 `VectorsAwaitingTheirSlice`**，每条写明切片与批次

这 11 条**不是偷懒，是实测零实现**。它们的切片赖以定义的线上消息在服务端 `src/` 与 `tests/`
上 `grep -rl` 全为 0：

```
DemandSelectionRequested                      src=0  tests=0     (FP-IS-09)
DemandSelectionResult                         src=0  tests=0     (FP-IS-09)
SlotConfigurationActivationCommand            src=0  tests=0     (FP-IS-14)
OnboardAlarmSnapshot                          src=0  tests=0     (FP-IS-15)
UnableToChargeFieldConfirmationRequested      src=0  tests=0     (FP-IS-13)
ManualStationClearanceConfirmationRequested   src=0  tests=0     (FP-IS-13)
```

钉住集全表：

| `vectorId` | 切片 | 批次 |
| --- | --- | --- |
| `CV-SLOT-CONFIGURATION-ACTIVATION` | `FP-IS-14` | 3 |
| `CV-ONBOARD-ALARM-SNAPSHOT` | `FP-IS-15` | 3 |
| `CV-TASK-TYPE-ADMISSION-FAIL-CLOSED` | `FP-IS-10` | 4 |
| `CV-REVERSED-DIRECTION-JOURNEY` | `FP-IS-11` | 4（第二阶段） |
| `CV-WAITING-POINT-IDLE-RETURN` | `FP-IS-12` | 5 |
| `CV-MULTI-STOP-PLAN-NINE-LEGS` | `FP-IS-08` | 6 |
| `CV-WORKLIST-SELECTION-ACCEPTED` | `FP-IS-09` | 7 |
| `CV-WORKLIST-SELECTION-STALE-REVISION` | `FP-IS-09` | 7 |
| `CV-AUTOMATIC-CHARGING-CYCLE` | `FP-IS-13` | 8 |
| `CV-UNABLE-TO-CHARGE-FIELD-CONFIRMATION` | `FP-IS-13` | 8 |
| `CV-MANUAL-STATION-CLEARANCE` | `FP-IS-13` | 8 |

**钉住不是放行。**三条机制让它没法变成红的垃圾桶：

1. 比对是**精确相等**——绑上了却没删钉住集那行，红；掉了绑定又没进钉住集，红；钉住一个协议
   根本没冻结的 id，也红（那个 id 永远不会出现在「缺具名测试的冻结向量」里）。
2. `EveryPinnedVectorBelongsOnlyToSlicesThisBatchDoesNotImplement` 拒绝任何属于
   `FP-IS-00`～`07` 的向量被钉住。属本批次的向量缺测试是**缺口**，不是排期。
3. 每行都写着切片与批次，删它的人是哪个批次一目了然。

形态取自 `ProtocolReasonCodeArchitectureTests` 的 `PinnedDeviations`——它落地时也是 11 个，
今天是空集。**空集本身是断言，清零后保留字段，不要删。**

---

## 五、五条验收逐条

| 验收 | 状态 | 兑现方式 |
| --- | --- | --- |
| 一条架构测试断言每个 `vectorId` 有具名测试对应，删掉一条测试能让它变红 | ✅ | `EveryFrozenVectorIsBoundToANamedTestOrPinnedToASliceNobodyHasBuiltYet`。自证见第六节的自证一（只删一条测试，单步变红） |
| 同一条测试断言不存在指向不存在 `vectorId` 的测试标注，改错一个 id 能让它变红 | ✅（形态有一处偏离，见下） | `NoTestClaimsAVectorIdTheProtocolNeverFroze`。自证见第六节自证二 |
| 断言的向量清单从协议仓的 `index.json` 读取，测试里不出现手抄的第二份清单 | ✅ | 运行时 `JsonDocument.Parse` 读 vendor 副本，SHA-256 钉字节。**测试里没有任何手抄的向量 id 清单**——见下面的说明 |
| 测试在 headless runner 上跑，不需要桌面 | ✅ | 只做文件读取与 `System.Reflection`，无 UI、无进程、无网络。CI 的 `test` job 跑在 `[self-hosted, headless]` 上 |
| 测试不挂任何 `IntegrationSlice` trait | ✅ | 全类 8 条 `[Fact]`，零 `IntegrationSlice` trait |

**第二条验收的形态偏离，明说：**票据写的是「**同一条测试**断言……」，落地是同一个测试**类**里的
两个 `[Fact]`（正向查缺、反向查伪）。拆开是为了报错能各说各的——合成一条的话，一次拼写错误
只会给出一条混在一起的失败。**如果「同一条测试」按字面理解为一个方法，这条是偏离，需要你裁定；**
按「一条架构测试 = 这个类」理解则不是。守卫的能力不受影响：拼错一个 id 会**同时**触发两条红
（见自证二）。

**2026-09-14 用户裁定：认可现状。**「同一条测试」按「一条架构测试 = 这个类」理解，两个 `[Fact]` 不算偏离；
车载端票 20 的同形落法与票 22 那条两个方向合成一条的断言一并按此了结，两端代码都不动。

**第三条验收，三处曾被怀疑是「第二份清单」的东西，逐个交代：**

| 候选 | 判定 |
| --- | --- |
| 11 条钉住集 | **不是向量清单，是缺口登记。**它是从运行时读出的清单里**减去**的东西，且钉一个不存在的 id 会红 |
| `LastSliceSequenceThisBatchImplements = 7` | **一个整数，不是清单。**切片→批次映射按规格 7.2 刻意不进 `index.json`，边界只能写在这一侧 |
| ~~3 条共享向量 id~~ | **本来是手抄的，复审指出后已改掉。**现在只断言「重复出现的条目恰好 3 个」，不列 id——去重仍被证明（34 条目 / 31 去重 / 3 重复），零手抄 |

守卫共 8 条测试：

```
TheVendoredIndexIsTheProtocolIndexByteForByte
TheIndexParsesIntoSixteenSlicesAndThirtyOneDistinctVectors
EveryFrozenVectorIsBoundToANamedTestOrPinnedToASliceNobodyHasBuiltYet
NoTestClaimsAVectorIdTheProtocolNeverFroze
EveryPinnedVectorBelongsOnlyToSlicesThisBatchDoesNotImplement
TheBindingCheckCatchesAVectorThatLostItsLastNamedTest
TheBindingCheckCatchesAPinnedVectorThatSomethingNowBinds
TheBindingCheckCatchesATestThatNamesAVectorNobodyFroze
```

---

## 六、四条自证：真做过，不是「应该会红」

自证方式是**真改工作树、真编译、真跑、看红、再还原**。下面是原样的测试输出。

### 自证一 —— 只删一条测试（票据 AC1 的字面证据）

删掉 `RecoveryStateMachineG2Tests.FormalCorrectionAndFaultCommandsUseDurableOutboxReplayAndExactAck`
**整个方法**（67 行）。`git diff --numstat` 确认**只有这一个文件被删了行，其余六个测试文件零改动**：

```
  Failed ControlServer.Tests.ProtocolVectorTestBindingArchitectureTests.EveryFrozenVectorIsBoundToANamedTestOrPinnedToASliceNobodyHasBuiltYet
  Error Message:
   These frozen vectors have no named test and are not pinned to an unbuilt slice. Either a test proving them was deleted, or its ProtocolVector trait was: CV-FAULT-CARGO-HANDOFF, CV-LOAD-CORRECTION
```

**选这条测试是因为它是那两条向量唯一的绑定。**这一点要说清楚（见第八节第 3 条）：守卫的粒度
是「向量失去**最后一条**具名测试」。20 条里 17 条有 ≥2 条绑定，删掉其中一条守卫仍绿——那不是
漏洞，是覆盖冗余，但票据 AC1 的字面（「删掉一条测试能让它变红」）**只在 3 条单绑向量上单步成立**：
`CV-LOAD-CORRECTION`、`CV-FAULT-CARGO-HANDOFF`、`CV-LOAD-CANCELLATION-ALL-EMPTY`。

### 自证二 —— 改错一个 `vectorId`

把 `OnboardMessageProcessorTests` 里一处 `CV-MANUAL-CHARGING-RETURN` 拼成 `…RETRUN`：

```
  Failed ControlServer.Tests.ProtocolVectorTestBindingArchitectureTests.NoTestClaimsAVectorIdTheProtocolNeverFroze
  Error Message:
   Tests carry a ProtocolVector trait naming vectors the protocol did not freeze: OnboardMessageProcessorTests.ManualChargingReturnToServiceIsAnsweredAndDecidedOncePerRequestId claims CV-MANUAL-CHARGING-RETRUN
```

报错点名**是哪条测试标错了哪个 id**（这是复审提出后加的，原先只报 id）。

拼错某条向量**仅有的**绑定时会同时触发两条红：错的 id 被这条报出来，被它抛下的那条真向量被
上一条报出来。早先一次自证（删 `WireToGateStoreTests.FiveStepRecovery…` ＋ 把
`CandidateHandshake…` 的 trait 拼错）实测就是这个结果，报的是 `CV-SESSION-RECOVERY-HAPPY`。

### 自证三 —— 篡改 vendored 副本

把副本里的 `CV-ONBOARD-ALARM-SNAPSHOT` 改成 `…SNAPSHOTS`：

```
  Failed ControlServer.Tests.ProtocolVectorTestBindingArchitectureTests.TheVendoredIndexIsTheProtocolIndexByteForByte
  Error Message:
   Assert.Equal() Failure: Strings differ

  Failed ControlServer.Tests.ProtocolVectorTestBindingArchitectureTests.EveryFrozenVectorIsBoundToANamedTestOrPinnedToASliceNobodyHasBuiltYet
  Error Message:
   These frozen vectors have no named test and are not pinned to an unbuilt slice. …: CV-ONBOARD-ALARM-SNAPSHOTS
```

副本漂移一个字符就被抓住。这是第三条验收（不许有第二份手抄清单）真正的保障。

### 自证四 —— 用过滤器把某条向量的具名测试单独跑出来

```
dotnet test … --filter "ProtocolVector=CV-SESSION-RECOVERY-HAPPY"
→ Passed!  - Failed: 0, Passed: 2, Skipped: 0, Total: 2
```

正是绑在那条向量上的两条测试。这证明绑定不只是给守卫看的元数据，它是可操作的。

**每次自证后工作树均已还原**，副本哈希复核为 `71e0a63d…`，`git diff --numstat` 各文件均为
「只增不删」，全量 `569 passed / 0 failed / 0 skipped`。

---

## 七、双轴复审（`mattpocock-skills:code-review`）与处置

跑了 Standards ＋ Spec 双轴。**六条被采纳并改掉，三条记录不改**。

### 采纳并已改

| 轴 | 发现 | 处置 |
| --- | --- | --- |
| Spec | 3 条共享向量 id 是手抄的，是 AC3 字面唯一被蹭到的地方 | 改成断言「重复条目数 == 3」，不列 id |
| Spec | `PinnedButBound` 的失败文案误诊——钉住一个协议没冻结的 id 时，报的却是「有测试绑上了，删掉那行」 | 改名 `PinnedInVain`，文案分两种成因各说一遍 |
| Spec | AC1 只在单绑向量上单步成立，原自证是「删测试 ＋ 破坏第二个 trait」两步 | 补了自证一（单绑向量，只删一条测试），并在第六节如实写明粒度 |
| Standards | `VectorBinding.TestName` 从未被读 —— Speculative Generality | 用起来：拼错 id 的报错现在点名是哪条测试 |
| Standards | `LastSliceThisBatchImplements` 名字承诺切片边界，代码比的是 `sequence` —— Mysterious Name | 改名 `LastSliceSequenceThisBatchImplements`，并把形状断言加强成「id 与 sequence 逐行配对」，让这个名字兑现 |
| Standards | `Assert.SkipWhen` 是全套件唯一的 skip，与 `CLAUDE.md` 的 `0 skipped` 基线冲突 | 把钉住集改成两个纯函数的**参数**，自证用合成集合。skip 去掉了，且两条自证在钉住集清零后依然有效 |
| Standards | `NewlyUnbound`/`PinnedButBound` 在 `Assert.True` 里各求值两次（message 参数是 eager 的） | 先存变量 |

### 记录不改

1. **AC2「同一条测试」拆成了两个 `[Fact]`**（Spec 轴）。理由与裁定请求见第五节。
2. **`CLAUDE.md:67-68` 与 `README.md:45` 仍写着 `W2G-IS-00`～`07` 与 `protocol-v0.1.1`**
   （Standards 轴，标为 hard）。核实属实。**但那是票 14 的范围**（服务端切 v2 身份三元组），
   本票的冲突边界写着「不碰产品代码」，改仓库怎么描述自己更不在内。
   **提请票 14 一并处理**：`CLAUDE.md` 的 `Collaboration workflow` 第一条、`Tests and gates`
   的 `243–249 passed` 基线（现为 569），以及 `README.md` 的 `protocol-v0.1.1` 段。
3. **`RepositoryRoot()` 是第六份逐字拷贝**（Standards 轴，弱 Duplicated Code）。前五份都这么
   写，抽公共 helper 会在架构测试之间引入耦合。先例治之。

---

## 八、改了哪些文件

```
新增  tests/ControlServer.Tests/ProtocolVectorTestBindingArchitectureTests.cs
新增  vendor/8005-agv-protocol/integration-slices/index.json      （整份 cp，未手工编辑）
新增  vendor/8005-agv-protocol/README.md
改    .gitattributes                                              +4（vendor 目录 -text）
改    tests/ControlServer.Tests/WireToGateStoreTests.cs           +11 trait
改    tests/ControlServer.Tests/RecoveryStateMachineG2Tests.cs     +13 trait
改    tests/ControlServer.Tests/OnboardMessageProcessorTests.cs     +9 trait
改    tests/ControlServer.Tests/JourneyRuntimeWorkerTests.cs        +6 trait
改    tests/ControlServer.Tests/OnboardJourneyPublisherTests.cs     +6 trait
改    tests/ControlServer.Tests/ApplicationOrchestrationTests.cs    +1 trait
改    tests/ControlServer.Tests/DemandAcceptanceAtomicityTests.cs   +1 trait
```

**零产品代码改动**（`src/` 未动），与票据的冲突边界一致。既有测试文件里只有 trait 行的插入，
`git diff --numstat` 每个文件删除列均为 0。

---

## 九、明账：本票没做什么

1. **车载端未做。**用户 2026-09-08 定：本票只做控制端，车载端另开票。理由是该仓零 trait 基建、
   交付要走 `w2g/*` 分支 PR 且合并权不在我方，而票 15 正在同一个仓改 v2——挤进去会撞车。
   **后果要说清楚：守卫只看得见控制端测试程序集**，车载端那一侧的向量覆盖至今没有机器守卫。

2. **31 条里 11 条没有具名测试。**见第四节。它们的归宿是批次 3～8，届时各自清掉钉住集里
   自己那几行。批次 3 要清 2 条（`FP-IS-14`/`15`）。

3. **守卫的粒度是「最后一条绑定」，不是「任意一条」。**20 条绑定向量里 17 条有 ≥2 条绑定，
   删掉其中一条守卫仍绿。这是覆盖冗余的正常结果，但要知道守卫**不能**替代 code review 去
   发现「某条向量的证明变弱了」。

4. **绑定的强度逐条不等。**守卫断言的是「这条向量有具名测试」，不是「测试穷尽了向量」。
   最薄的一条是 `CV-LOAD-CANCELLATION-ALL-EMPTY`——服务端的取消面
   （`OnboardRecoveryCoordinator.AuthorizeLoadCancellationAsync`）只有
   `FailedCompensationResultIsDurableReplayableAndNeverReleasesDemandOrVehicle` 一条测试覆盖，
   且走的是 `REJECTED` 分支，证的是 `AUTHORIZE_CANCELLATION_EXPLICITLY` 那一半；
   `RECONCILE_EMPTY_FINAL_STATE` 那一半在实现里（同文件 `safeEmpty` 判据）但没有独立测试。
   **票 17 的 `FP-IS-02` 重证应当补上这条。**

5. **没跑 CI。**改动只在本机验证（Debug 配置；CI 跑 Release）。要跑用
   `gh workflow run test.yml --ref fp/v2-impl`（`fp/v2-impl` 不在 workflow 的 push 分支表里）。

---

## 十、给下一个人的三条

- **清钉住集时不要删字段。**清零后 `VectorsAwaitingTheirSlice` 留着，空集是断言本身。两条自证
  都不依赖它非空，清零后照常有效。
- **协议仓的 `index.json` 一动，先跑 `vendor/8005-agv-protocol/README.md` 的四步**，
  再看守卫报什么。它报缺／报多通常是对的：新向量还没测试，或某条测试标着已删除的 id。
- **`LastSliceSequenceThisBatchImplements = 7` 是本批次的边界，不是常量真理。**批次 3 落地
  `FP-IS-14`/`15` 后，这个数不该跟着涨——它守的是「属本批次的向量不许被钉住」，
  而 `FP-IS-14`/`15` 是靠删钉住集那两行来兑现的，不是靠抬高这个数。抬高它等于给
  `FP-IS-08`～`13` 开后门。
