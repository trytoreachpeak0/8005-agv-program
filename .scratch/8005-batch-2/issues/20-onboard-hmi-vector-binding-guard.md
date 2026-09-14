# 20 — 车载端的 `vectorId` ↔ 具名测试绑定守卫（`w2g/*` 分支 → PR）

**做什么：** 把票 16 在控制端落成的那条守卫，在车载端也建一份。协议冻结的每个 `vectorId`
都有一条车载端具名测试对应，反过来每条声称对应向量的标注都指向真实存在的 `vectorId`。

**为什么单开一张票，而不是并进票 16。** 用户 2026-09-08 定。三条理由，都是当时实测出来的：

1. **车载端零 trait 基建。**该仓 `tests/` 有 **0 处** `[Trait("IntegrationSlice", …)]`
   （票 16 实测；控制端那 187 处全在控制端）。控制端是在既有 trait 之上加一族正交 trait，
   车载端要从零建。
2. **交付形态是 PR，合并权不在我方。**只能在 `w2g/*` 分支上工作，改动交给
   `OnboardHmi_MVP`，我们不合并。
3. **票 15 正在同一个仓改 v2。**票 16 挤进去会撞车。

**代价要写在明处：**票 16 落地后，**守卫只看得见控制端测试程序集**——车载端那一侧的向量
覆盖至今没有任何机器守卫。这张票就是补这个洞。

## 开工前必须知道的五件事（2026-09-08 实测）

### 1. 该仓没有 CI

`.github/workflows/` 在 `HEAD`、`origin/OnboardHmi_MVP` 上**都不存在**（`git ls-tree` 实测，
该仓只有 `origin/OnboardHmi_MVP` 一个远程分支）。

**所以规格 14.5「CI 上一条测试绿」这个说法在这个仓套不上。**守卫的运行路径是本地
`dotnet test`、我方的 L2 发布流程，以及 Kun Wang 自己跑的那套。**验收不要写「CI 绿」，
写「`dotnet test` 绿且不需要桌面」。**

### 2. 守卫要落在 `SQCD.Agv.UnitTests`，不是 `SQCD.Agv.WireToGateG2Tests`

| 工程 | TFM | 能否 headless |
| --- | --- | --- |
| `tests/SQCD.Agv.UnitTests` | `net8.0`（继承 `Directory.Build.props`） | ✅ |
| `tests/SQCD.Agv.WireToGateG2Tests` | `net8.0-windows` | ❌ 桌面相关 |

两个都是 xunit.v3 ＋ `xunit.runner.visualstudio`（即 **VSTest 模式**，与控制端一致，
trait 过滤写 `--filter "ProtocolVector=…"`，**不是** `--filter-trait`）。

### 3. 该仓已有 vendor 协议仓的先例，但**它没有钉哈希**

`vendor/8005-agv-protocol/protocol-v0.1.1/errors/error-codes.json` 由
`tests/SQCD.Agv.UnitTests/ReasonCodeRegistryArchitectureTests.cs` 运行时读取，
`FindRepositoryRoot()` 定位仓库根。形态可以照抄。

**但那份副本没有 SHA-256 钉字节**——测试与 `vendor/.../README.md` 里 `grep -ci sha256` 都是 0。
票 16 的验收第三条（不许有第二份手抄清单）恰恰是靠钉字节兑现的。

> **本票要钉。**样板是控制端的
> `tests/ControlServer.Tests/ProtocolVectorTestBindingArchitectureTests.cs` ＋
> `vendor/8005-agv-protocol/README.md` ＋ `.gitattributes` 的 `-text` 行。
> 给既有的 `error-codes.json` 补钉哈希**不在本票范围**，但值得单独提一句。

### 4. 车载端的实现缺口与控制端**一样**

新切片（`FP-IS-08`～`15`）赖以定义的消息在车载端 `src/` 里同样 `grep -rl` 全为 0：
`DemandSelectionRequested`、`SlotConfigurationActivation*`、`OnboardAlarmSnapshot`、
`UnableToCharge*`、`ManualStationClearance*`。

所以 **20 绑 / 11 钉的切分对车载端同样成立**，钉住集与控制端逐条相同。这不是巧合——切片是
双端的，一端没实现另一端也无从证明。**但要自己重测一遍再照抄，别假定。**

### 5. 数字：16 切片 / 34 条目 / **31 去重**

`vectorIds` 条目合计 34，去重 31，与 `vectors/` 的 31 个目录双向无遗漏。三条向量跨切片共享。
**断言按 31 数，不是 34。**协议仓 `fp/v2-candidate` HEAD `f6ee75d`，`index.json` 的
SHA-256 是 `71e0a63d49d1973653e1f70addc19c334faff5e53e8597733c1423a7307bd82f`（19766 字节，LF）。

## 可以照抄的东西

票 16 的成果在 `8005-agv-control-server` 提交 `562544e`（分支 `fp/v2-impl`，CI run
[34227325616](https://github.com/trytoreachpeak0/8005-agv-control-server/actions/runs/34227325616)
绿）。决议与四条自证的原样输出见 [`16-answer.md`](16-answer.md)。

**别照抄的一处**：控制端的守卫是 8 条 `[Fact]`，其中验收第二条「同一条测试」被拆成了两个
方法——那处形态偏离待用户裁定，裁定结果出来之前车载端照做即可，之后两边一起改。
（**2026-09-14 用户裁定认可现状，两边都不改。**）

## 冲突边界

- **只在 `w2g/*` 分支上工作，改动以 PR 交给 `OnboardHmi_MVP`，我们不合并。**
  绝不推 `OnboardHmi_MVP`，绝不 force-push，绝不动不是我们的分支或 tag。
- **不碰该仓的 `CLAUDE.md` 与 `docs/`**——那仍是他们的文档。
- **该仓工作树脏会中断 L2**（`Get-L2PeerPublish` 拒绝脏源），跑 L2 前先提交到 `w2g/*`。
- 不改产品代码，只加测试与 vendor 副本。

**前置：** ~~票 15（车载端 v2）~~✅ **于 2026-09-09 完成，前置解除**（见
[15-answer.md](15-answer.md)）。分支 `w2g/fp-v2-impl` = `9ec5b29`，已推送，`172 passed`。

票 15 转交本票五件事：

1. **vendor 目录已经建好并按字节钉住了**，但 vendor 的是 `manifest/release.json`、
   `errors/error-codes.json` 与 `schemas/` 整棵树，**`integration-slices/index.json` 还没有**
   ——本票要加那一份。**加进去之后不需要新的哈希常量**：它同样在 manifest 的 `files` 表里，
   `ProtocolIdentityArchitectureTests.EveryOtherVendoredFileIsPinnedByTheManifestFileTable`
   会自动接管它。**那条断言的 `Assert.Equal(70, vendored.Length)` 要跟着改成 71。**
   本票开工说明第 3 条写的「给既有的 `error-codes.json` 补钉哈希不在本票范围」已经由票 15 做掉了。
2. **`.gitattributes` 的 `vendor/8005-agv-protocol/** -text` 已经挂上**（该仓原先没有
   `.gitattributes`，票 15 只加了这一行），不用再加。
3. **钉住集不要照抄控制端。**本票开工说明第 4 条写「20 绑 / 11 钉的切分对车载端同样成立，钉住集
   与控制端逐条相同——但要自己重测一遍再照抄」。**票 15 重测的结果是不成立**：控制端钉住的
   `CapabilitySnapshotRequested`／`SafetyStateSnapshotRequested`／`SublotRejected` 三条，车载端
   **全部具名**，`SublotRejected` 还有完整的解析与校验。车载端的 11 条缺口是另一组，见
   15-answer.md 第五节。**向量那一侧要自己再测一遍，同样别假定。**
4. **`ReasonCodeRegistryArchitectureTests` 读的 vendor 路径已经不带版本段了**
   （`vendor/8005-agv-protocol/errors/error-codes.json`），注册表也已换成 v2 的 54 个码。
5. **交付形态改了：只推长期分支，不开 PR。** 用户 2026-09-09 定。`OnboardHmi_MVP` 已钉到
   **已发布的** `protocol-v0.3.0`，PR 进去等于覆盖已签发布。做法对齐控制端的
   `origin/fp/v2-impl`。**本票下面那两条关于 PR 的验收要跟着改写。**

## 两个未定项，等用户裁定

1. **归哪个批次。**本票不在规格第 8 节冻结的批次 2 范围里——它是票 16 拆分出来的另一半，
   2026-09-08 才存在。放在 `8005-batch-2/issues/` 只是因为它的前置（票 15）在这里。
2. **是否阻塞票 17（轨 A 出口）。**票 17 原本把票 16 列为前置。票 16 拆分后，车载端这一半
   要不要同样卡住出口，是排期决定：卡住则轨 A 出口要多等本票一轮，不卡住则轨 A 出口达成时
   车载端的向量覆盖仍无机器守卫。**票 17 的前置行目前未把本票列入。**
   （原文写的代价是「多等一个 PR 的评审周期」，那是交付形态改为只推分支之前的算法，
   见上第 5 条。）

**状态：** done（2026-09-09）。决议见 [`20-answer.md`](20-answer.md)。

- [x] 一条架构测试断言每个 `vectorId` 有车载端具名测试对应，删掉一条测试能让它变红
      —— `EveryFrozenVectorIsBoundToANamedTestOrPinned`；自证一见 20-answer 第五节
- [x] 同一条测试断言不存在指向不存在 `vectorId` 的标注，改错一个 id 能让它变红
      —— `NoTestClaimsAVectorIdTheProtocolNeverFroze`。**与控制端一样落成两个 `[Fact]` 而不是
      「同一条测试」**，形态偏离与票 16 同源，仍待用户裁定；裁定后两端一起改
      —— **2026-09-14 用户裁定认可现状**：「同一条测试」按同一个架构测试类理解，不是偏离，两端代码都不动
- [x] 向量清单从 vendor 的 `index.json` 读取并**钉住 SHA-256**，测试里不出现手抄的第二份清单
      —— 由 manifest `files` 表钉住，未引入新哈希常量（票 15 转交第 1 条）；本地再核一遍见
      `TheVendoredIndexIsPinnedByTheManifestFileTable`
- [x] 守卫落在 `SQCD.Agv.UnitTests`，`dotnet test` 绿且**不需要桌面**（不写「CI 绿」，该仓无 CI）
      —— 为此守卫改成**源码级扫描**：`net8.0` 工程不能引用 `net8.0-windows` 的 G2 工程，
      反射方案只看得见半个仓库。理由见 20-answer 第二节第 1 条
- [x] ⚠️ 钉住集里每条都写明切片与批次，且拒绝任何属于 `FP-IS-00`～`07` 的向量被钉住
      —— **按字面不成立，需用户裁定。**车载端有两个 `FP-IS-07` 向量没有具名测试：
      `CV-FAULT-CARGO-HANDOFF`（实现全有、测试全无）与 `CV-FORCED-MECHANICAL-RECOVERY`
      （`ForcedMechanicalRecoveryResult` 根本没实现）。落地为两个互为镜像、谁也吸收不了谁的
      钉住集，每条写明切片、批次与发现内容。详见 20-answer 第四节
      —— **2026-09-14 勾上**：两个向量已由票 21 关闭，`w2g/b3-on-v2@b960108` 上欠账集
      `VectorsThisBatchOwesANamedTest` 为空；「本批次向量不许被钉住」的镜像规则仍在，
      这一条想要的性质按两个钉住集的形态成立
- [x] 两条自证真做过并如实记下原样输出，不是「应该会红」
      —— 20-answer 第五节，且已对复审加固后的扫描器重跑一遍
- [x] 全部工作在 `w2g/*` 分支上，`OnboardHmi_MVP` 零推送
- [x] ~~PR 已开，标题与正文用中文~~ —— **改写：不开 PR，见上第 5 条**
- [x] 该仓 `docs/` 与 `README.md` 未被本票改动（**该仓没有 `CLAUDE.md`**，票 15 实测）
      —— `src/` 也零改动
- [x] 工作树干净，`w2g/*` 分支已推送，L2 可从它发布车载端 —— 已提交、工作树干净，
      **推送待用户确认**（`8005-agv-program/CLAUDE.md` 说该仓对 agent 只读，与本票授权冲突，
      交接文档第六节第 7 条列为待裁定）
      —— **2026-09-14 勾上**：`w2g/*` 长期分支已推送（用户 2026-09-09 定「只推长期分支」），
      批次 2 收尾的 G3 从远端 `w2g/b3-on-v2` 发布车载端；`CLAUDE.md` 第 19 行现已写明该仓在
      `w2g/*` 分支可写，冲突不再存在

**⚠️ 本票不解决票 17 的第二条障碍。**交接文档 `…-20260909-i.md` 第四节说「要按切片出证就得先有
`IntegrationSlice` trait——而那正是票 20 的内容」，但本票十条验收从头到尾只说 `vectorId`。
落地后实测：该仓 `IntegrationSlice` trait 仍为 **0 处**，`run-w2g-g2.ps1` 仍无 `-Slice` 参数。
详见 20-answer 第八节第 1 条。
