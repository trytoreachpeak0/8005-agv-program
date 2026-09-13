# 票 23 决议（进行中）—— G3 的按片出证与分级状态

控制端 `fp/v2-impl` = `e4a8f0f`（新增 `scripts/g3-slice-evidence.ps1`，改三个 runner），未推送。

本文只记**票据与提交信息里没有的东西**：开工时被证伪的两条自述、分级怎么落的、
断言归属表是怎么来的、以及它的可信度到哪为止。逐条代码细节在 `e4a8f0f` 的提交信息里。

## 一、⚠️ 开工头一小时证伪了我自己写在票据里的两条

票 23 是本轮开的，**它第五节和第六节各有一条是我写票时想当然的**，开工核范围时当场证伪。
记在这里而不是悄悄改掉，因为这正是交接文档反复说的那条纪律的又一次命中：
**票据里的因果断言，开工前要自己跑一遍再信——包括自己一小时前写的那张票。**

| 票据初稿原文 | 实测 |
| --- | --- |
| 第五节：「切片索引读克隆出来的协议仓那份（**三个 runner 都已经克隆协议仓**并比过 `manifestSha256`）」 | **错。只有 `run-staged-g3.ps1` 克隆协议仓**（`$protocolSource`，`New-ExactClone -Name 'protocol'`）。`run-staged-g3-restart.ps1` 与 `run-demand-bearing-g3-vectors.ps1` 一次都不克隆它，它们的协议身份是从**运行中服务端的 version 端点**读回来的（`$version.protocolCommit`）。所以索引只能统一走 vendor 那份 |
| 第六节：「三个 runner 的 `-Slice` 与票 22 给车载端做的同形」 | **半错。** 形状同，语义反：G2 的 `-Slice` 是过滤器（改 `dotnet test --filter`，少跑测试），**G3 没有可过滤的东西**。已在票据第四节写清，落地时 `-Slice` 只选出证范围，一个字都不少跑 |

第一条带出一个正面结果：既然只有 staged 克隆协议仓，那就**让它顺手断言 vendor 那份与克隆那份
逐字节相同**。三个 runner 的 `gate-result.json` 都写 `integrationSliceIndexSha256`，
而这条断言把「vendor 那份就是协议自己那份」从「靠 manifest 文件表推」变成「这次运行真比过」。

## 二、分级落成了两个字段，不是一个新枚举值

用户裁定「引入分级状态」。**落法不是给 `status` 加一个 `STAGED_PASS` 取值**，而是把原来混在
一个词里的两件事拆开：

| 字段 | 回答 | 取值 |
| --- | --- | --- |
| `status` | 这一片的断言在这次运行里过了没有 | `PASS` / `FAIL` / `INCONCLUSIVE` |
| `assuranceLevel` | 这次运行**实际动了什么** | `STAGED_REBUILD` / `DEMAND_BEARING_RESTORE` / `CANDIDATE_ARTEFACT` |

**为什么不是加枚举值。** 加一个 `STAGED_PASS` 会让读的人必须知道「STAGED_PASS 比 PASS 弱」
这条约定才能读懂结果，而这条约定没有地方写。拆成两个字段之后，弱在哪里是**字面写着的**：
`assuranceLevel` 自带一句话说明它动了什么、没动什么。

`formalSlicePass` 由二者算出：

```
formalSlicePass = ($status -eq 'PASS') -and ($assuranceLevel -in $LevelsThatCountAsSlicePass)
```

`Get-G3AssuranceLevelsThatCountAsSlicePass` 返回 `STAGED_REBUILD` 与 `DEMAND_BEARING_RESTORE`，
**函数注释里逐字写着用户 2026-09-09 的裁定**——下一个人看到的是一条决议，不是一个魔数。

`CANDIDATE_ARTEFACT` **既不在计入表里，也没有任何 runner 产出它**。留着它是为了让这把尺
露出自己的顶端，而不是停在「刚好造出来的最高一级」——否则半年后没人记得还有一级没做。

⚠️ **2026-09-04 那份 `SUMMARY.md` 里「不构成切片通过」的措辞随本票作废**，但那份证据
一个字节都没动（证据目录只增不改）。

## 三、🔴 断言归属表是我写的，不是我抄的——它的可信度到此为止

这是本票最需要读的一节。

`scripts/g3-slice-evidence.ps1` 的 `Get-G3RunnerClaim` 那张表，把三个 runner 的
**19／20／20 条具名断言**逐条分给 `FP-IS-00`／`04`／`05`／`06` 四片，外加一组
`runWide`（前置与全局安全检查，每片都算）。

**它在本票之前不存在于任何地方。** 三个 runner 的 `assertions` 块里没有一条挂着切片标识；
切片归属整个存在于 `officialSlices` 那个字面常量里，从 `b4afdb3` 起就是如此。
所以这张表是**一次首次书面陈述**，依据是断言名与各片在协议冻结索引里的 `vectorIds`，
**不是对既有记录的转录**。它值得由切片家族的负责人复核一遍。

在复核之前它凭什么能用——凭 `Assert-G3ClaimCoversReport`，它**双向抛**：

- 运行报了一条表里没有的断言 → 抛。否则那条断言不计入任何一片，证据会悄悄变松。
- 表里点名了一条运行没报的断言 → 抛。否则某片会凭一条根本没产出的证据算通过。

这条守卫在每次 `Write-G3GateResults` 的第一行跑。**开工时它就当场立功了一次**：
离线自证的提取器把 staged 的断言名按 4 空格缩进找，而 staged 的 `assertions` 嵌在 `$result`
里、键是 8 空格，于是提取到 0 条——守卫立刻把 19 条「表里点名但运行没报」全列了出来。
是提取器的 bug 不是表的 bug，但**它证明了这条守卫在真出错时会说人话**。

## 四、`-Slice` 的语义与 G2 那两个脚本相反

| | G2（`test-wire-to-gate.ps1`、`run-w2g-g2.ps1`） | G3（本票三个 runner） |
| --- | --- | --- |
| `-Slice` 是什么 | **过滤器**：`dotnet test --filter "IntegrationSlice=…"`，少跑测试 | **出证范围选择器**：场景照跑不误，一个字都不少 |
| 少跑了吗 | 是 | **否** |
| 选中/认领 0 条 | 建目录前拒绝（票 14） | 建目录前拒绝（本票） |

**为什么 G3 不能是过滤器**：G3 跑的是一个完整的对端联调场景（克隆、build、publish、起真对端、
重启、注错），不是一组可筛选的测试。按片截断它会改变证据的含义——剩下那半段证明不了整条链路。

四条拒绝路径都真跑过（见第六节），**四次都在 `StageRoot` 与 `EvidenceRoot` 被创建之前抛出**。

## 五、四片如实记「本批次无 G3 面」

`FP-IS-01`／`02`／`03`／`07` 在四个 G3 runner 里一次都不出现（控制端三个 ＋ 车载端
`run-staged-g3-recovery-ack-drop.ps1`）。用户 2026-09-09 裁定：**本批次记录这个缺口，
不补四个新的跨仓场景**。

落法是 `Get-G3SlicesWithoutSurfaceThisBatch`，一片一句理由。这四片：

- **不发 `gate-result.json`**——是「没有产物」，不是「产物写着 INCONCLUSIVE」。
  依据是票 14 在 G2 那边立的先例：选中 0 条测试时拒绝出证，而不是写一份绿的。
- `-Slice FP-IS-02` 这类调用被拒绝时，报的是「这一片本批次没有 G3 面」＋该片的向量清单
  ＋裁定日期，**不是**一句泛泛的「本 runner 不认领」。这个区别是有意的：
  前者告诉你没人能证它，后者只告诉你找错了 runner。

`classification` 里另加一个 `slicesWithoutSurfaceThisBatch` 字段，让每一份 `run-result.json`
自己就说得清「八片里有四片本轮没有 G3 面」，不用去翻票据。

## 六、自证（**未完，下一个 session 接**）

**离线（20 条，全绿）**：`Get-G3RunnerClaim` 那张表对着三个 runner 源码里的真实断言名双向核过
（19／20／20，两个方向都不多不少）；一条只属某片的断言失败只让那片 FAIL、另一片仍 PASS；
一条 `runWide` 失败让每片都 FAIL；runner 自身出错时每片记 `INCONCLUSIVE` 而不是 `FAIL`；
两条拒绝路径的措辞；`gate-result.json` 一片一份且 `-Slice` 只出那一份；
身份字段为空时抛且不写文件。脚本在
`%TEMP%\claude\<本 session 目录>\scratchpad/verify-g3-slice-evidence.ps1`。

**`-Slice` 拒绝路径（真跑，4/4）**：`run-staged-g3.ps1 -Slice FP-IS-02`（无 G3 面）、
同脚本 `-Slice FP-IS-04`（别的 runner 认领）、`run-staged-g3-restart.ps1 -Slice FP-IS-02`、
`run-demand-bearing-g3-vectors.ps1 -Slice FP-IS-00`。
**四次都在 `StageRoot` 与 `EvidenceRoot` 被创建之前抛出**，实测两个目录事后都不存在。

**门禁运行（临时证据目录，用户 2026-09-09 授权，不入库）**：

| runner | 结果 |
| --- | --- |
| `run-staged-g3.ps1` | ✅ `STAGED_G3_RECOVERY_REPLAY_PASS`；`FP-IS-00`／`FP-IS-06` 各一份 `gate-result.json`，都是 `status=PASS` ＋ `assuranceLevel=STAGED_REBUILD` ＋ `formalSlicePass=true`；断言归属 12／10 条 |
| `run-staged-g3-restart.ps1` | ✅ `STAGED_G3_PROCESS_RESTART_PASS`；同上两片，`protocolReleaseVersion` 修好后为 `'1.0.0'`，九个身份字段无一为空 |
| `run-demand-bearing-g3-vectors.ps1` | ❌ `DEMAND_BEARING_SLICE_FAIL`（**预期内**，见下）；`FP-IS-04`／`FP-IS-05` 各一份 `gate-result.json`，都是 `status=FAIL` ＋ `assuranceLevel=DEMAND_BEARING_RESTORE` ＋ `formalSlicePass=false` |

三个 runner 共出 **6 份 `gate-result.json`**，覆盖 `FP-IS-00`／`04`／`05`／`06`
（`00` 与 `06` 各两份，staged 与 restart 一人一份）。

**demand-bearing 那次失败正好把 FAIL 路径验成了。** 它唯一失败的断言是
`protocolAndBuildIdentityBoundToTheSharedBinding`，失败的原因是恢复的现场库里记的
`protocolCommit` 是 2026-08-29 `protocol-v0.1.1` 的历史，**任何 v2 身份的运行对它都过不了**
（[17-answer.md](17-answer.md) 第七节第 2 条）。

它是 `runWide`，
所以两片都该 FAIL——实测两片 `status` 都是 `FAIL`、`formalSlicePass` 都是 `false`，
**不是 `INCONCLUSIVE`**（那个留给 runner 自身出错），而且两份证据照样写了出来。
这正是设计要的区别：**「问了，答案是不对」与「没问成」在证据里必须长得不一样。**

⚠️ **2026-09-09 第四轮就地更正：上面那句「它唯一失败的断言是 …」写得不准。**
那条断言是**七项合取**（`run-demand-bearing-g3-vectors.ps1:626-632`），
现场库历史只是**第 7 项**；前六项问的是运行中服务端与被测构建的身份，
而当时的证据把七项揉成一个布尔值，**分辨不出是哪一项 `false`**。
[票 24](24-demand-bearing-field-store-assertion-split.md) 已把第 7 项拆成如实记录，
2026-09-09 重跑实测：前六项作为断言全过、`status` 转 `PASS`，
新记录字段 `fieldStoreProvenance.matchesBoundProtocolCommit` 为 `false`——
**当初「挂的只是现场库那一项」的推断，到这一轮才成为实测结论。**

### 第一轮 restart 查出的一个真缺口（已修，`a46101e`）

两个不克隆协议仓的 runner 从运行中服务端读身份，我读的是 `$version.releaseVersion`，
**而服务端把它叫 `protocolReleaseVersion`**。于是一份 `gate-result.json` 带着
`protocolReleaseVersion: null` 出去了，旁边八个身份字段逐条正确。

**教训**：从一个 JSON 对象上读字段，PowerShell 对不存在的字段返回 `$null` 而不报错，
所以「拼错字段名」和「这一项确实没有」在证据里长得一模一样。
已加守卫：九个身份字段任一为空就抛，**并且不写这份证据**。

## 七、待用户裁定 / 本票不决定的

1. **断言归属表需要切片家族负责人复核**（第三节）。守卫挡得住漂移，挡不住第一次就分错。
2. **G2 的 `gate-result.json` 要不要也补 `assuranceLevel`。** 两端 G2 现在是 `1.1.0`、没有
   这个字段；补了两端才同形，但要跨两个仓改 `test-wire-to-gate.ps1` 与 `run-w2g-g2.ps1`。
3. **车载端 `run-staged-g3-recovery-ack-drop.ps1` 同改。** 它也命名 `FP-IS-00`／`FP-IS-06`，
   同病，跨仓且要另开授权。
4. **票 17 第三条验收最终认到哪一级。** 本票只提供尺子。按现在的常量，
   `STAGED_REBUILD` 与 `DEMAND_BEARING_RESTORE` 计入，所以票 17 预计认这两级 ＋ 四片记在案。
