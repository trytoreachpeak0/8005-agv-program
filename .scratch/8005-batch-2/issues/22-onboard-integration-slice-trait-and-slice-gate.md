# 22 — 车载端 `IntegrationSlice` trait 与 `run-w2g-g2.ps1 -Slice`（`w2g/*` 长期分支）

**做什么：** 让 `ONBOARD_HMI_G2` 能按切片出证。两件事：给车载端的测试挂
`IntegrationSlice` trait，给 `run-w2g-g2.ps1` 加 `-Slice`。

**为什么现在做：** 它是**票 17 的输入**，也是交接文档里的「障碍 2」。票 17 要给
`FP-IS-00`～`07` 八个切片各出一份 `ONBOARD_HMI_G2` 的 `gate-result.json`，而
`run-w2g-g2.ps1` 跑的是整个解决方案、不按切片过滤——`summary.json` 里 `FP-IS-00` 与
`FP-IS-01` 共享同一个 `onboardHmiG2` 结论，其余六片根本不出现。按切片过滤又需要车载端先有
`IntegrationSlice` trait，而那是 0 处。

用户 2026-09-09 定：单开一张票，不并进票 17。

## 一、缺口是单边的，控制端那一半早就有

| | `IntegrationSlice` trait | `ProtocolVector` trait |
| --- | --- | --- |
| 控制端 `ControlServer.Tests` | **196 处**，`FP-IS-00`～`07` 每片都有（35／56／17／19／10／12／28／19） | 有 |
| 车载端两个测试工程 | **0 处** | **58 处，9 个文件** |

**关键实测：车载端的 58 处 `ProtocolVector` 已经覆盖 `FP-IS-00`～`07` 的全部 20 条向量，
一条不缺。** 所以本票不是「补测试」，是**把已经存在的向量绑定按协议自己的切片索引投影成切片
trait**——机械推导，不是重新设计绑定。八片各会被多少个测试覆盖（按属性块计，已排除
`FP-IS-13`）：

| 片 | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 测试数 | 11 | 5 | 5 | 9 | 2 | 5 | 8 | 19 |

**八片都非零**，所以票 14 那条「选中 0 条即拒绝」的闸不会在本批次误伤任何一片。

## 二、⚠️ `FP-IS-13` 是本票唯一一个真正要判断的地方

`CV-MANUAL-CHARGING-RETURN` **同时属于 `FP-IS-07` 与 `FP-IS-13`**（协议
`integration-slices/index.json`，`f6ee75d`）。车载端有 4 处测试挂着它。

**不挂 `FP-IS-13`。** 依据是控制端的既有做法，不是本票的发明：

```
OnboardMessageProcessorTests.cs:829  [Trait("IntegrationSlice", "FP-IS-07")]
OnboardMessageProcessorTests.cs:830  [Trait("IntegrationSlice", "FP-IS-06")]
OnboardMessageProcessorTests.cs:831  [Trait("ProtocolVector", "CV-MANUAL-CHARGING-RETURN")]
```

控制端三处 `CV-MANUAL-CHARGING-RETURN` 测试全挂 `FP-IS-07`，**一处 `FP-IS-13` 都没有**。
理由与票 14 修掉的那个缺陷同形：`FP-IS-13` 的四条向量里只有这一条有测试
（另三条 `CV-AUTOMATIC-CHARGING-CYCLE`、`CV-UNABLE-TO-CHARGE-FIELD-CONFIRMATION`、
`CV-MANUAL-STATION-CLEARANCE` 在两端都无实现），挂上去会让
`-Slice FP-IS-13` **选中 4 条测试并写出 `"status": "PASS"`**——一个只建了四分之一的切片拿到
一份绿证据。票 14 用「选中 0 条即拒绝」堵住了零实现的情形，堵不住这种部分实现的情形。

所以本票的投影规则带一个上界：**只投影到本批次实现的片**（`sequence ≤ 7`）。
`LastSliceSequenceThisBatchImplements` 这个常量票 20 已经定在
`ProtocolVectorTestBindingArchitectureTests` 里，**复用它，不要再抄一个 7 出来**。

## 三、投影规则（守卫要钉的就是这一条）

> 一个测试挂 `IntegrationSlice=S`，**当且仅当** S 是本批次实现的片（`sequence ≤ 7`），
> 且 S 的 `vectorIds` 里有该测试用 `ProtocolVector` 声明过的向量。

**这是双向的，比控制端那条严。** 控制端的
`EveryClaimedVectorIsCoveredByASliceItsOwnTestCarries` 是单向的（允许测试挂超出其向量的片，
上面那条 `FP-IS-06` 就是），它必须单向，因为它有 300 个不属于任何切片的测试要靠一张台账兜。
车载端不同：58 处向量 trait 就是全部切片面，切片 trait 完全由它推出，**双向等式成立且更容易
保持真**。将来真要给某个测试挂一个它向量之外的片，守卫会红，那时再开台账——红一次比默默漂
一年好。

## 四、要复用的机件（别重造）

- **票 20 的源码扫描器**（`ProtocolVectorTestBindingArchitectureTests` 里的 `ScanText`
  一族）。它已经处理了本票同样要面对的四件麻烦事：块注释里的 trait 不算数、
  `[Fact(Skip=…)]` 不算数、类级 trait 报红而不是静默漏计、多行与合并属性列表。
  **扫描器要提取成两个守卫共用的内部类**，按 trait 名参数化，并且改成每个测试方法收一组
  trait（现在只收 `(向量, 测试名)` 二元组，本票需要「同一个测试上的向量集合与切片集合」）。
  ⚠️ **提取之后 `ProtocolVectorTestBindingArchitectureTests` 的断言与自证一条都不许改**，
  它那 10 条自证就是提取有没有改变行为的判据。
- **为什么不能用反射**：一半向量由 `SQCD.Agv.WireToGateG2Tests`（`net8.0-windows`）证，守卫
  住在 `SQCD.Agv.UnitTests`（`net8.0`），`net8.0` 引不了 `net8.0-windows`。票 20 的类注释里
  写着这条，控制端那个守卫用反射是因为它只有一个测试工程。
- **切片索引**用 vendor 那份（`vendor/8005-agv-protocol/integration-slices/index.json`），
  它由 `manifest/release.json` 的 `files` 表钉住，票 20 的
  `TheVendoredIndexIsPinnedByTheManifestFileTable` 已经在查这条链。
- **`run-w2g-g2.ps1` 的切片清单读 `$ProtocolRoot` 那份索引**（脚本现在就是这么读的，
  且它前面已经比对过 `manifestSha256` 与 G1），不要改成读 vendor。

## 五、`run-w2g-g2.ps1` 要改成什么样

| | 不带 `-Slice`（现状，保留） | 带 `-Slice FP-IS-NN` |
| --- | --- | --- |
| `dotnet test` | 整个解决方案 | `--filter "IntegrationSlice=FP-IS-NN"` |
| 选中 0 条 | 不适用 | **建目录前就拒绝**，并报出该片的向量清单 |
| 证据目录 | `$EvidenceRoot\$Tag\<runId>-<commit>` | `$EvidenceRoot\$Tag\FP-IS-NN\<runId>-<commit>` |
| `summary.json` 的 `slices` | 硬编码 `FP-IS-00` ＋ `FP-IS-01` 两条 | 就该片一条，向量清单读自索引 |
| `gate-result.json` | 不出 | **出**，与控制端 `schemaVersion 1.1.0` 同形 |

三点说明：

1. **`gate-result.json` 是本票有意扩出去的一步。** 票 17 的验收第二条写的是「八份
   `gate-result.json` 全 PASS」，而车载端脚本至今只写 `summary.json`。不出这个文件，票 17 那
   条验收勾不上。形状对齐控制端 `test-wire-to-gate.ps1` 的 `1.1.0`，让两端证据能被同一个读法
   读，`gate` 字段写 `ONBOARD_HMI_G2`。
2. **`dotnet build` 与 `dotnet format` 不按切片缩。** 它们是全仓的，八片各跑一遍是重复但正确；
   缩了反而让每片的证据只覆盖自己那几个文件。
3. **`-Slice` 与 `-SkipProtocolG1` 必须能一起用。** 票 17 要连跑八片，G1 跑一遍就够，
   其余七片跳过。现在这两个参数没有耦合，改完仍不许耦合。

## 六、边界

- **只改 `8005-agv-onboard-hmi`，只在 `w2g/fp-v2-impl` 上。** 不动控制端、协议仓、
  `8005-agv-program` 的代码（本票的 `22-answer.md` 与本文件除外）。
- **不动 `vendor/`，不动 `src/`。** 本票不改任何产品代码：它只加 trait、加守卫、改门禁脚本。
- **不加、不删、不改任何一条既有测试的断言。** 只往属性列表里加 trait 行。
- **不碰 `LastSliceSequenceThisBatchImplements` 的值**，也不碰票 20 的两个钉住集。
- **不进门禁、不推送。** 票 17 才进门禁；推送与否由用户定（用户 2026-09-09 定：暂不推）。

## 七、开工前必须知道的两件事

1. **行尾问题已经没有了。** 2026-09-09 的 `d9dd631` 把 `* text=auto eol=lf` 搬进
   `.gitattributes`，全仓 206 个文本文件现在一律 `i/lf w/lf`，`dotnet format
   --verify-no-changes` `exit=0`。票 20／21 交接里那条「改既有文件前先探测该文件自己的行尾」
   可以退休了。
2. **守卫是源码扫描型，它扫 `tests/`。** 所以本票自己的自证如果要合成一段源码，
   **不能写成 raw string literal**（票 20 交接第六节第 4 条），否则扫描器会把自证里的假 trait
   当成真的。票 20 的 `TheScannerReadsMethodTraitsAndReportsTypeTraits` 是照抄的范例。

## 八、验收

**状态：** done —— 2026-09-09 完成，见 [22-answer.md](22-answer.md)。
车载端 `w2g/fp-v2-impl` = `b4f3530`（另有 `d9dd631`，是票 17 转交的行尾搬运，见 22-answer.md
第一节），`164 + 42 passed`，Debug 与 Release 都跑过，未推送、未进门禁。

- [x] 车载端每个带 `ProtocolVector` 的测试都挂上了对应的 `IntegrationSlice`，且只挂
      `sequence ≤ 7` 的片（新增 64 行，9 个文件）
- [x] `CV-MANUAL-CHARGING-RETURN` 那 4 处只挂 `FP-IS-07`，**没有任何一处挂 `FP-IS-13`**
- [x] 新守卫钉住第三节那条双向投影规则，两个方向各有一条断言
- [x] 新守卫钉住「每个切片 trait 值都是协议冻结的十六个之一」
- [x] 扫描器提取后，`ProtocolVectorTestBindingArchitectureTests` 的断言与自证**一条未改**，
      提取前后都是 `19 passed`
- [x] `run-w2g-g2.ps1 -Slice FP-IS-NN` 八片各跑通，`selectedTestCount` 与守卫算出的分布逐片
      相等（11／5／5／9／2／5／8／19）
- [x] `-Slice` 选中 0 条时**在建目录之前**拒绝，并报出该片的向量清单（`FP-IS-13` 实测）
- [x] `-Slice` 的运行产出 `gate-result.json`，`schemaVersion` `1.1.0`，`gate` 为
      `ONBOARD_HMI_G2`
- [x] `-Slice` 与 `-SkipProtocolG1` 可以同时使用（八次冒烟都是这么跑的）
- [x] 不带 `-Slice` 的既有调用形态行为不变
- [x] `dotnet test` 两个工程 Debug 与 Release 全绿，0 failed 0 skipped
- [x] 自证：三条，真改工作树、看红、原样记录、从副本还原并核 SHA-256

**冒烟另外查出两个真 bug**（都已修，见 22-answer.md 第五节）：`selectedTestCount` 把 MSBuild
的构建输出行一并算了进去（11 vs 真值 2，且已写进过一份 `gate-result.json`）；两个测试工程写
同一个 trx 文件名，后写的覆盖先写的（选中 5 条、落盘 3 条，`status` 仍是 PASS）。
