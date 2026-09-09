# 票 22 决议 —— 车载端 `IntegrationSlice` trait 与 `run-w2g-g2.ps1 -Slice`

**日期：** 2026-09-09
**落地：** `8005-agv-onboard-hmi` `w2g/fp-v2-impl` = `360a405`。三个提交：`d9dd631`（行尾搬运，
属票 17 的转交事项，见第一节）、`b4f3530`（本票落地）、`360a405`（复审修正，见第七节）。
**三个提交都未推送**，用户 2026-09-09 定「现在不推」。**未进任何门禁。**

---

## 一、先说不属于本票的那一个提交：`d9dd631`

票 17 的「票 21 转交本票四件事」第 2 条——`dotnet format` 那道坎的修法搬运。本票开工前先做掉
它，否则 `run-w2g-g2.ps1` 的每一次运行（包括本票的八次冒烟）都必然 FAIL。

在 `ea3c75e` 的树上前后实测：

| | `dotnet format ./SQCD_8005AGV.sln --verify-no-changes --no-restore` |
| --- | --- |
| 搬运前 | `exit=2`，22093 条 `ENDOFLINE` ＋ 16 条 `WHITESPACE`，62 个 `.cs` 文件 |
| 搬运后 | `exit=0`，零诊断 |

**不是 cherry-pick。** 远端 `w2g/normalize-line-endings@9ee7e4d` 只有全局那一行（它从 MVP 线出，
那条线没有 vendor 目录），本线还要留票 15 加的 `vendor/8005-agv-protocol/** -text`。

工作树 123 个文件由 `i/lf w/crlf` 重新展开成 `i/lf w/lf`，全仓 206 个文本文件现在一律 LF。
**vendor 下 73 个文件字节未动**：`manifest/release.json` 仍是
`84f984eabf17106e92666c415b63100d404e9ec69a9a710dfddf17683cc42788`，73 个文件的汇总摘要仍是
`590edd3c15a841b3ad4e6f91eb38e7d884fcf3c1bf0a93474a5c88c311d35714`。

### ⚠️ 顺序那条注释我第一版写错了，是自证纠正的

第一版注释写着「vendor 那条排在前面就会让摘要漂移」。**不成立。** 四种组合各真跑一遍
（删掉 `manifest/release.json` 再 `git checkout`，核 SHA-256）：

| 全局那条 | vendor 这条的位置 | vendor 的 `text` | manifest 摘要 |
| --- | --- | --- | --- |
| `text=auto eol=lf` | 之后（落地形态） | unset | `84f984ea…` 不变 |
| `text=auto eol=lf` | 之前 | auto | `84f984ea…` **不变** |
| `text=auto` | 之后 | unset | `84f984ea…` 不变 |
| `text=auto` | 之前 | auto | `a0501d80…` **漂移** |

真相是：**只要全局那条带着 `eol=lf`，顺序不影响字节**；顺序只在有人把 `eol=lf` 删掉、退回让
`core.autocrlf` 决定时才成为分界。`-text` 让 vendor 的字节与 `eol` 属性无关，顺序让它在那种
情况下仍然生效——两件都要留，但理由不是我原先写的那个。注释已按实测改写，表进了文件。

**教训：写进产物的因果断言要跑一遍再写。**这条与纪律里「写任何验收之前先 grep 确认符号真的
存在」同形，只是从「存在性」挪到了「因果性」。

---

## 二、本票的核心判断：投影，不是新绑定

开工前实测：车载端 `IntegrationSlice` 0 处，`ProtocolVector` 58 处、9 个文件，
**已覆盖 `FP-IS-00`～`07` 的全部 20 条向量，一条不缺**。

所以规则是一条等式，不是一张新的绑定表：

> 一个测试挂 `IntegrationSlice=S`，**当且仅当** S 的 `sequence ≤ 7`，且 S 的 `vectorIds` 里有
> 该测试用 `ProtocolVector` 声明过的向量。

**比控制端那条严，而且是有意的。** 控制端的
`EveryClaimedVectorIsCoveredByASliceItsOwnTestCarries` 是单向覆盖（允许测试挂超出其向量的片，
`OnboardMessageProcessorTests.cs:830` 那条 `FP-IS-06` 就是），它必须单向：那边 441 个测试里
300 个不属于任何切片，要靠 `ClassesOutsideTheSliceFamily` 一张手写台账兜住。车载端没有那个
人口——向量 trait 就是全部切片面，切片 trait 完全由它推出，双向等式既可查又更容易保持真。
将来真要给某个测试挂一个它向量之外的片，守卫会红，那时再开台账。

落地：新增 **64 行** trait，涉及 9 个文件。`LastSliceSequenceThisBatchImplements` 复用票 20 定在
`ProtocolVectorTestBindingArchitectureTests` 里的那个常量，没有第二个 7。

---

## 三、⚠️ `FP-IS-13`：本票唯一真正要判断的地方

`CV-MANUAL-CHARGING-RETURN` **同时属于 `FP-IS-07` 与 `FP-IS-13`**，车载端有 4 处测试挂它。

**不投影到 `FP-IS-13`。** 依据是控制端的既有做法，不是本票的发明——控制端三处
`CV-MANUAL-CHARGING-RETURN` 测试全挂 `FP-IS-07`（`OnboardMessageProcessorTests.cs:829/920/989`，
其中一处另挂 `FP-IS-06`），**一处 `FP-IS-13` 都没有**。

理由：`FP-IS-13` 的四条向量里只有这一条有测试，另三条
（`CV-AUTOMATIC-CHARGING-CYCLE`、`CV-UNABLE-TO-CHARGE-FIELD-CONFIRMATION`、
`CV-MANUAL-STATION-CLEARANCE`）在两端都无实现。挂上去会让 `-Slice FP-IS-13` **选中 4 条测试并
写出 `"status": "PASS"`**——一个只建了四分之一的切片拿到绿证据。

票 14 用「选中 0 条即拒绝」堵住了**零实现**的情形，**堵不住部分实现的情形**。所以这条堵在
trait 这一层，且 `NoTestCarriesASliceThisBatchDoesNotImplement` 单独说了一遍，不让它只作为
`sequence ≤ 7` 这个上界的算术副作用存在——**它是一个决定，不是一条算术结论**。

---

## 四、扫描器提取

票 20 的源码扫描器搬进 `TestSourceTraitScanner`，按 trait 名参数化，并从「一条 `(向量, 测试名)`
二元组」改成「一个测试方法收一组 trait」——本票问的是「同一个测试上的向量集合与切片集合」，
两张平表答不了。切片索引的读法一并收进 `VendoredSliceIndex`，两个守卫共用一份解析。

**为什么不能用反射**：一半向量由 `SQCD.Agv.WireToGateG2Tests`（`net8.0-windows`）证，守卫住在
`SQCD.Agv.UnitTests`（`net8.0`），`net8.0` 引不了 `net8.0-windows`。控制端那个守卫用反射，
是因为它只有一个测试工程。

**`ProtocolVectorTestBindingArchitectureTests` 的 19 条断言与自证一行未改**，只留了一个
`Adapt` 适配器把新形状压回旧形状。提取前后都是 `19 passed`——那 10 条驱动 `ScanText` 的自证
就是「提取有没有改变行为」的判据。

---

## 五、`-Slice` 与两个被冒烟跑出来的真 bug

`-Slice FP-IS-NN` 按 `IntegrationSlice` 过滤测试，证据目录多一层切片名，另写一份
`gate-result.json`（`schemaVersion 1.1.0`，与控制端 `test-wire-to-gate.ps1` 对齐，`gate` 为
`ONBOARD_HMI_G2`；**是超集不是同一份字段表**，多出的四个字段见第七节第 4 条）。构建与 `dotnet format` **仍是全仓的**——它们是这棵树的属性，不是这一片的
属性，按片收窄会让每份证据只覆盖那片碰巧改到的文件。

选不中任何测试的切片在**建目录之前**被拒。实测 `-Slice FP-IS-13` 的 `dotnet test` 退出码是
**0**——与票 14 在控制端实测到的完全一样，不拒就是一份绿证据。

### bug 一：`selectedTestCount` 数成 11，真值是 2

preflight 的 `dotnet test --list-tests` 会连带构建，MSBuild 每个工程打一行
`  SQCD.Agv.Core -> ...\*.dll`，被 `^\s+SQCD\.Agv\.\S` 一并算了进去：9 个工程 ＋ 2 条测试 = 11。
**这个 11 已经被写进了第一次冒烟的 `gate-result.json`**——一份说谎的证据。

修法是要求第二个点：`^\s*SQCD\.Agv\.\S+\.\S`（`\s*` 是复审那轮改的，见第七节第 3 条）。
测试全名 `SQCD.Agv.UnitTests.Xxx.Yyy` 有那个点，构建行 `SQCD.Agv.Core -> ...` 那个位置是空格。
控制端的 `^\s+ControlServer\.Tests\.\S` 天然带这个点，本端抄形不抄意就踩了。

### bug 二：两个测试工程写同一个 trx，后写的覆盖先写的

`--logger "trx;LogFileName=onboard-$Slice.trx"` 在单工程的控制端没问题，本端有两个测试工程。
实测 `-Slice FP-IS-01` 选中 5 条，落盘的唯一一个 trx 里只有 3 条——**证据丢了 2 条测试结果，
而 `status` 仍是 PASS**。

改用 `LogFilePrefix`（VSTest 会追加框架与时间戳，每个工程各留一份）。**但不信它**：它的时间戳
只到秒，两个工程在同一秒收尾仍会撞。所以跑完数 trx 里的 `<UnitTestResult`，与选中条数不等就
`Add-Failure`——把一次静默少报变成一次 FAIL。`recordedTestCount` 进 `summary.json` 与
`gate-result.json`。

---

## 六、验证

### 八片各跑一遍脚本

`-SkipProtocolG1`，`-EvidenceRoot` 指向临时目录，**证据未进 `evidence/`，未进门禁**：

| 片 | status | selected | recorded | 向量数 |
| --- | --- | --- | --- | --- |
| `FP-IS-00` | PASS | 11 | 11 | 4 |
| `FP-IS-01` | PASS | 5 | 5 | 1 |
| `FP-IS-02` | PASS | 5 | 5 | 3 |
| `FP-IS-03` | PASS | 9 | 9 | 2 |
| `FP-IS-04` | PASS | 2 | 2 | 1 |
| `FP-IS-05` | PASS | 5 | 5 | 2 |
| `FP-IS-06` | PASS | 8 | 8 | 3 |
| `FP-IS-07` | PASS | 19 | 19 | 6 |

八片的 `selectedTestCount` 与守卫按索引算出的分布逐片相等。`FP-IS-13` 被拒，退出码 1，
**证据目录没有被创建**。

不带 `-Slice` 的既有形态：目录层级不变，两条切片行与 `FP-IS-01` 的三个附加字段
（`demandMode`／`demandSource`／`controlServerOutcomes`）都在，不出 `gate-result.json`。

### 测试与门禁前置

`164 passed`（`SQCD.Agv.UnitTests`，比票 21 的 154 多的 10 条就是新守卫）＋ `42 passed`
（`SQCD.Agv.WireToGateG2Tests`），**Debug 与 Release 都跑过，0 failed 0 skipped**。
Release 构建 0 warning / 0 error。`dotnet format --verify-no-changes` `exit=0`。

### 三条自证（真改工作树、看红、从副本还原并核 SHA-256）

1. 删掉 `tests/SQCD.Agv.UnitTests/SafetyRulesTests.cs:9` 那条 `FP-IS-07`：

       These tests are not filed under exactly the slices their own ProtocolVector traits project
       onto, so a slice gate would run the wrong set: ResumeAuthorizationRequiresExactPersisted
       AttemptAndCheckpoint (tests/SQCD.Agv.UnitTests/SafetyRulesTests.cs:8) is missing FP-IS-07

   还原后 SHA-256 `fe5df933e8cf6c57be4beb4cfc36be69d9fdd44f59f6d77b8b8a3d2ccb78ea3b`，一致。

2. 给 `tests/SQCD.Agv.WireToGateG2Tests/WireToGateG2Tests.cs:296` 那条
   `CV-MANUAL-CHARGING-RETURN` 加上 `FP-IS-13`：

       These tests are filed under a slice scheduled into a later batch. A slice gate for it would
       select them and write a PASS over a slice nobody has finished building:
       ManualChargingReturnToServiceAcceptedResultIsCorrelatedToRequestedMessage
       (tests/SQCD.Agv.WireToGateG2Tests/WireToGateG2Tests.cs:296) carries FP-IS-13

   `NoTestCarriesASliceThisBatchDoesNotImplement` 与投影那条各报一次，两条互不依赖。
   还原后 SHA-256 `3a479fef36d10f62139753a67641805ae3ad8c506b182773582fa8a39e80b728`，一致。

3. 把 `LogFilePrefix` 改回 `LogFileName` 再跑 `-Slice FP-IS-01`：`status` 变 FAIL，
   `selectedTestCount = 5`、`recordedTestCount = 3`，`failures` 里记着「trx 里 3 条，选中 5 条」。
   还原后 SHA-256 `915521a4a9a7f65b3e4d36bffba88ea68548abcb13d921fc628b9b020a854e88`，一致。

---

## 七、双轴复审（`mattpocock-skills:code-review`）

按交接文档跑了 Standards ＋ Spec 双轴，prompt 里写明了「vendor 那两万行是逐字节副本，不要复审」。
**两轴各查出一条我自己不会发现的东西。逐条核过，一条不同意。** 修正在 `360a405`。

### 两条真问题（已修）

1. **preflight 不查 `$LASTEXITCODE`（Standards ＋ Spec 两轴都点了）。**
   `dotnet test --list-tests` 会连带构建，编译失败同样产出零条匹配行，于是脚本 throw 的是
   「切片选不中任何测试」——把树坏了说成切片没建。**自证四**：往 `SafetyRulesTests.cs` 末尾塞
   一行非 C#，改前报「选不中任何测试」，改后报「列举切片 'FP-IS-04' 的测试失败（exit=1）。
   这通常是构建坏了，不是这一片没有测试」，两次都没建证据目录。还原后 SHA-256
   `fe5df933…`，一致。

2. **守卫靠在渲染后的句子里搜 trait 名分辨问题归属（Standards，Primitive Obsession）。**
   扫描器手里本来就有 `TraitClaim(TraitName, Value)`，却拍平成一句话让守卫用
   `claim.Contains(" IntegrationSlice ")` 解析回去。一个含该子串的路径或 trait 值会让它答错。
   改成 `ProblemClaim(Site, TraitName, Value, Reason)`，两个守卫按字段过滤。

### 三条措辞与去重（已修）

3. **注释与代码矛盾（Standards，硬）。** 注释写「不靠 VSTest 的缩进」，正则却是 `^\s+`。
   改成 `^\s*`，注释改成说清真正吃劲的是第二个点。**这条我写第一遍时就该发现**——它正是
   bug 一那条修法自己的注释。
4. **`gate-result.json` 说「同形」实为超集（Spec）。** 本端多 `implementationBranch`、
   `recordedTestCount`、`buildExitCode`、`formatExitCode`。注释与 `LOCAL_G2_EVIDENCE.md` 改成
   「对齐但是超集」，逐个说明为什么多。
5. **六处 `IsNullOrWhiteSpace($Slice)` → `$isSliceRun`；`$runDirectory` 不再赋值后立刻被覆盖
   （Standards，Duplicated Code）。** 顺带把 `$sliceEntry` 用 `@()` 包起来并断言恰好 1 条——
   索引里真出现重复 id 时 `$null -eq` 拦不住，数组会把 `vectorIds` 摊平进证据。

### 一条不同意

**Standards 说 `LastSliceSequenceThisBatchImplements` 提成 `internal` 是 Feature Envy，应当移进
`VendoredSliceIndex`。不移。** `VendoredSliceIndex` 是「协议冻结了什么」，那个 7 是「本批次实现
到哪」——票 20 的类注释明确写着切片到批次的映射**故意不放进协议仓**（规格 7.2：重排批次不该变成
一次让两端证据全部作废的协议变更），所以它必须在本侧声明。把它搬进那个类，等于把一个我方的排期
事实混进一个只描述协议文件的类里。留在票 20 那个把它解释清楚的守卫里，跨类引用一次，是更诚实的
形态。

### 三条我核过、认为是措辞问题而不是缺陷

- **Spec：验收第 3 条字面写「两个方向各有一条断言」，落地是一条合并断言。**属实，是形态偏离。
  合并的理由写在方法注释里，且两个方向各有一条独立的 vacuity proof（第六节自证一、二分别打的
  就是这两个方向）。**这与第 1 条待裁定（票 16 那个「同一条测试」vs 两个 `[Fact]`）同类，
  一并等裁定。**
- **Spec：「`--filter` 选中数与守卫算出的数一致」没有机器检查。**属实。机器能查的是
  `selected == recorded`（已做）；「与守卫算出的数一致」跨进程，要做只能在守卫里写死一张每片
  条数表——那正是票 20 明确反对的第三份手抄清单。本轮是人工逐片核对（第六节表）。
- **Spec：`summary.json` 的 `schemaVersion` 两条路径都升到 `1.1.0`，与「不带 -Slice 行为不变」
  有出入。**属实，但**现状是对的**：不带 `-Slice` 时那四个字段确实存在（值为 `null`），
  版本号停在 `1.0.0` 才是说谎。票据那句「行为不变」说的是结论不变，措辞不够精确。

### Spec 轴确认干净的四项

`FP-IS-13` 全仓零处；投影规则没有逃逸口（类级 trait、`Skip=`、无法归属、`bin`/`obj` 四条路都
通向红，无 trait 的测试投影到空集是正确的，`tests/` 之外没有 `[Fact]`）；票据边界第六节逐条守住
（无 `vendor/`、无 `src/`、无既有断言改动、`LastSliceSequenceThisBatchImplements` 值仍是 7、
票 20 两个钉住集未动）；`d9dd631` 确实是合并不是 cherry-pick。

Standards 轴独立用真 `git check-attr -a` 在一个临时仓里复现了 `.gitattributes` 那张四行表，
**逐行一致**。

⚠️ **两轴各有一条断言我核出是「结论对、理由不完全对」**：Spec 说 `NoTestCarriesASliceThisBatch
DoesNotImplement` 在零个切片 trait 时会空过——对，但它前面的 `Assert.Equal(8, implemented.Count)`
是对索引的断言不是对测试的，真正兜住那种退化的是投影那条，它自己也这么说了。

## 八、两处有意越出票据字面的改动

**都不是悄悄做的，列在这里等裁定。**

1. **`gate-result.json` 是本票新加的产物。** 票 22 第五节写明了，理由是票 17 的验收第二条是
   「八份 `gate-result.json` 全 PASS」，而车载端脚本至今只写 `summary.json`——不出这个文件，
   票 17 那条勾不上。`summary.json` 保留：transcript、G1 结果与身份校验三样 gate-result 放不下。

2. **`docs/LOCAL_G2_EVIDENCE.md` 顺手修了两个过期常量。** 它还写着 `protocol-v0.1.1` 与
   `1531489e42e328f28bfe0c51ed3f8c56e5ce0279`，是票 15 切 v2 身份时漏掉的；脚本的 `$expected`
   是权威。本票要在这份文档里补 `-Slice` 的说明，把它旁边两个错的常量留着不合适。

---

## 九、本票没做、记下来的四件事

1. **`run-w2g-g2.ps1` 没有 `#Requires -Version 7`。** 全局偏好要求的是**新** `.ps1`，它不是新
   文件，本票没加。控制端的 `test-wire-to-gate.ps1` 有。要不要补齐，请用户定。

2. **证据 JSON 是 CRLF 的。** `Set-Content` 在 Windows 上默认 CRLF，而 `d9dd631` 之后
   `.gitattributes` 说 `* text=auto eol=lf`——一旦这些证据被 `git add`，索引里会是 LF，与脚本
   写出的字节不同。目前没有任何机制对证据文件取哈希（与 vendor 不同），且仓库里既有的证据在
   索引中本来就是 LF，所以不构成问题。**但如果将来给证据加摘要绑定，这一条会变成 bug。**

3. **`-Slice` 的八次运行会跑八遍 `dotnet format` 与八遍全仓构建。** 这是有意的（第五节），
   代价是票 17 连跑八片时每片多约 40 秒。真嫌慢的话该改的是票 17 的跑法（比如先跑一次 format
   再八次带开关跳过），不是把 format 按片收窄。

4. **带 `-Slice` 时 `logs/dotnet-build-release.log` 记的是一次增量空转。** preflight 的
   `--list-tests` 已经把该构建的都构建了，脚本自己那次 `dotnet build` 落到日志里只剩「全是最新」。
   构建的真实结果仍由 `buildExitCode` 与 preflight 的退出码共同兜住，但**日志本身信息量比不带
   `-Slice` 时低**。要修就得让 preflight 走 `Invoke-LoggedCommand`，而它跑在证据目录存在之前——
   这个先后顺序是票据第五节写死的，本票没动。

---

## 十、转交票 17 的三件事

1. **障碍 2 已解除。** `run-w2g-g2.ps1 -Slice FP-IS-NN` 八片都能出 `gate-result.json`，
   `CONTROL_SERVER_G2` 那边八片本来就有 trait（35／56／17／19／10／12／28／19 处）。
   **票 17 的两条硬障碍现在都不在了**（另一条见下）。

2. **🔴 交接文档说的「`win11-01` 是票 17 的硬前提」这条，实测站不住。** 该说法出自
   `7a4e509` 提交信息里的「门禁证据与发布包都在它上面产出」。但历史 `CONTROL_SERVER_G2` 证据的
   `.trx` 里写的是 `computerName="LAB-WIN-01"`（`evidence/g2/20260830-issue26-264615a/*/`），
   G3 证据里的路径也是 `C:\Users\szy`——**都是本机，不是 `win11-01`**。本机已是 8.0.425。
   `win11-01` 上跑的是 GitHub Actions（`test.yml`／`l2.yml`，触发条件是推 `main`／
   `ControlServer_MVP` 或开 PR）与 `release.yml` 出包，而票 17 的出口明写「不含 RC」。
   **用户 2026-09-09 裁定：不算票 17 的前提，门禁在本机出证**，`win11-01` 的升级另作运维事项。

3. **G3 有一条交接没写的前提：车载端必须先推。** `run-staged-g3.ps1` 是**从 GitHub 克隆**车载端
   的（`$OnboardRepository` 默认是仓库 URL），且 `New-ExactClone -RemoteRef 'origin/OnboardHmi_MVP'`
   会断言远端 tip 等于 `$OnboardCommit`。本线要改成 `origin/w2g/fp-v2-impl`，而远端停在
   `9ec5b29`，本地已到 `b4f3530`（领先 6）。四条 commit 绑定也都还指着 v2 之前的构建。
   **用户 2026-09-09 裁定：现在不推，等到真要跑 G3 时再说。**
   （`slots-simulator` 那条不用动：它在 `fb5f7c5`，与脚本默认值一致，且全仓不引用任何协议身份。）
