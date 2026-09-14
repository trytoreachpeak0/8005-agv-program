# 票 17 决议（进行中）—— `FP-IS-00`～`07` 在 v2 下重证

**日期：** 2026-09-09（第二轮）
**状态：四道门禁跑了三道半。** 用户 2026-09-09 第二次裁定「先跑一轮 v2 身份的 G3，验收另议」。
**八个切片仍未通过**——而现在知道了原因：**用现有 G3 runner 做不出「八片各一份 `gate-result.json`」，
且这是那三个 runner 的既定立场，不是本轮的疏漏。**详见第六节。

**2026-09-09 第四轮更新：那个「做不出来」已由[票 23](23-g3-per-slice-gate-result.md) 解掉**
（三个 runner 都真跑过，六份 `gate-result.json`），**但第三条验收仍不勾——卡点换成了口径**：
`FP-IS-00`／`06` 通过，`FP-IS-04`／`05` 失败在一条关于现场库历史的已知断言上，
`FP-IS-01`／`02`／`03`／`07` 本批次无 G3 面。该条已按分级口径如实改写、保持未勾，
收口条件见票 17 第三条末尾与本文第七节第 1 条。

| 门禁 | 结果 | 绑定 |
| --- | --- | --- |
| `G1` | ✅ `PASS`，`failures: []` | 协议仓已提交的 `evidence/g1-result.json`@`f6ee75d`，本轮独立复现逐字段相同 |
| `CONTROL_SERVER_G2` × 8 | ✅ 八份 `gate-result.json` 全 PASS | `fp/v2-impl` = `a143c9c`；`FP-IS-02` 另有一份 `3f62647` 的重出 |
| `ONBOARD_HMI_G2` × 8 | ✅ 八份 `gate-result.json` 全 PASS | `w2g/fp-v2-impl` = `360a405`，**本轮已提交入库** |
| `G3` | ⚠️ 三个 runner 两过一败；~~按片验收结构上做不出来~~ **票 23 已解，现卡在口径（第七节第 1 条）** | `e3ea250` ＋ `153b705` ＋ `fb5f7c5` ＋ `f6ee75d` |

所有证据都绑 `protocol-v1.0.0@f6ee75defe6e2d18f63f4082bee445dbb678ab1b`，
`approvalStatus` = `SUPERSEDING_CANDIDATE`。

⚠️ **`tagExists` 这个字段不在 `gate-result.json` 里**（复审查出来的一处措辞不准）。
它在车载端的 `summary.json` 与本轮 G3 的 `run-result.json` 里，两处都记 `false`。
`gate-result.json` 记的是 `protocolTag`／`protocolApprovalStatus` 那一组。

---

## 一、⚠️ 上一版 `17-answer.md` 第四节是错的

**原文：**「协议 G1 在本机跑不了……给 `run-w2g-g2.ps1` 补 pnpm 后备是没用的，补了也过不了 `ajv`
那关。真正缺的是『这台机器能装协议仓的依赖』。」

**实测证伪：**

- `pnpm install --frozen-lockfile` 在本机 **1.2 秒跑通**，六个包全在本地 pnpm
  content-addressable store（`C:\Users\szy\AppData\Local\pnpm\store\v11`）里，`downloaded 0`，
  **连网都不用**。
- 真正缺的是三件，隔壁 `run-staged-g3.ps1` 第 33-61 行与第 2189-2194 行早就做了：
  ① node 目录**前置到 PATH**；② pnpm 回落到随 node 一起装的 `pnpm.cjs`；③ 跑 g1 之前先 install。
  少了①时 pnpm 自己起得来，但它派生的 `node tools/g1-validate.mjs` 报
  `'node' is not recognized as an internal or external command`——**这就是当初被误读成「缺 ajv」的那一步。**
- 三件齐全后 G1 返回 `"status": "PASS"`、`failures: []`、
  `candidateManifestSha256` = `84f984ea…`，与协议仓已提交的 `evidence/g1-result.json` 逐字段相同。

已修：车载端 `b835a40`。**这是第三轮证实同一条纪律：交接与答复文档里的因果断言，开工前要自己跑一遍再信。**

## 二、G1 还有第二个形状，与 pnpm 无关

修完 pnpm 那三件之后，`run-w2g-g2.ps1` 的 G1 在**这个工作区**仍然 FAIL：

```
"failures": ["manifest file count", "manifest missing .git"]
```

`g1-validate.mjs:17` 的排除规则写作 `p.startsWith(".git/")`——**带斜杠，假定 `.git` 是目录**。
`8005-fp/8005-agv-protocol` 是一个 **linked worktree**，它的 `.git` 是一个 101 字节的文件
（内容 `gitdir: C:/Users/szy/Desktop/8005-workspace/repos/8005-agv-protocol/.git/worktrees/…`），
`p === ".git"` 匹配不上那条规则，于是文件清单**恰好多一条**：实测 manifest 1758 条、walk 1759 条，
差集只有 `.git` 一项（`node_modules` 被正确排除）。

**这不是协议内容的问题。协议仓也不能为此修改**——`g1-validate.mjs` 在 manifest 的清单里，
改它就改掉 `manifestSha256`，两端所有身份绑定全废。

`b835a40` 因此在 `Invoke-ProtocolG1` 里前置认出这个形状并如实说明。
指向一份普通克隆时实测 `Status: PASS`、`protocol.g1Status = PASS`。

⚠️ **本节初稿写的「而不是报成 FAIL 诬告候选」是错的，复审查出来的。**
前置判定走的是 `Add-Failure`（`run-w2g-g2.ps1:266`），而 `$failures` 非空即
`status = 'FAIL'`（同文件 `:524`），最后仍然 `throw`。**只有措辞变了，运行结论没变。**
真正的收益是下一个人不必再花一轮去查「为什么 manifest file count 对不上」——
不是「把 FAIL 变成了别的」。

**`run-staged-g3.ps1` 不受影响**：它用 `git clone` 取协议仓，那种 `.git` 是目录——本轮三次 G3
运行的 `logs/protocol-g1.log` 都是 `PASS`。

### 顺带发现的一个真隐患

`g1-validate.mjs` **会写** `evidence/g1-result.json`。本轮第一次冒烟（前置判定还没加）跑在协议
工作树上，把那个已提交的文件覆写成了 FAIL 结果。已 `git checkout --` 还原并核过 SHA-256
（`82a20ee2…`），顺带删掉了那次装出来的 `node_modules`，协议工作树现在与开工时逐字节一致。
**加了前置判定之后这条路走不通了**，但换一份普通克隆跑 G1 仍会写它自己那份——这一点值得记住。

## 三、`CONTROL_SERVER_G2`：八片全 PASS，`FP-IS-02` 另有一份重出

原八份：`evidence/g2/20260909-fp-is-00-07-v2-recertification/`，提交 `5915cf7`，绑 `a143c9c`。

**票 16 转交的那条测试本轮补上了**（用户 2026-09-09 裁定「补测试 + 重出证据」）：

`CV-LOAD-CANCELLATION-ALL-EMPTY` 对服务端要 `AUTHORIZE_CANCELLATION_EXPLICITLY` 与
`RECONCILE_EMPTY_FINAL_STATE` 两件，此前只有前者被
`FailedCompensationResultIsDurableReplayableAndNeverReleasesDemandOrVehicle` 的 `REJECTED`
分支覆盖。`3f62647` 加了
`AuthorizedLoadCancellationReconcilesOnlyWhenEverySlotIsProvenEmpty`——**一条测试、两段**：
同一次 `AUTHORIZED` 授权之下，只有每个仓位都证到 `EMPTY` 才收敛需求、释放租约、收尾旅程；
把其中一个仓位的 `finalPhysicalState` 换成 `OCCUPIED`，收敛就不发生，而报文照样落库并被确认。
第二段因此同时是第一段的 vacuity proof。

**做成一条 `[Fact]` 而不是两条，是刻意的**——票据原文写「补一条独立测试」，而「一条测试落地成两个
`[Fact]`」正是待裁定第 1 条那个形态偏离。不再增加第五例。

三条自证（改产品代码、看红、从副本还原并核 SHA-256）：

| 改动 | 红在哪 |
| --- | --- |
| 去掉 `&& safeEmpty` | `Expected: RecoveryRequired, Actual: Reconciled`（OCCUPIED 那段） |
| 期望态 `"EMPTY"` 改 `"OCCUPIED"` | `Expected: Reconciled, Actual: RecoveryRequired`（EMPTY 那段） |
| 授权判据 `Accepted` 改 `RecoveryRequired` | `Expected: "AUTHORIZED", Actual: "REJECTED"` |

重出的证据：`evidence/g2/20260909-fp-is-02-reconcile-empty-final-state/`，提交 `e3ea250`，
绑 `3f62647`。`selectedTestCount` 17 → **18**，trx 里 `<UnitTestResult` 逐条数出 18 条全 `Passed`，
与 `selectedTestCount` 相等。除 `implementationCommit` 外十二个身份字段与上一轮逐字段相同。
**旧那八份保留不动。** `ONBOARD_HMI_G2` 未重跑——车载端一个字节都没动。

## 四、`ONBOARD_HMI_G2`：八片全 PASS，本轮已提交入库

用户 2026-09-09 裁定「`git add -f` 提交，两端对齐」。提交 `153b705`，73 个文件。

破的是该仓 `.gitignore` 第 9 行的 `evidence/`。先例是 `a1e32dd`（2026-08-26，为一份缺陷说明强制
加过一份 G3 证据），本次是第二次破例。理由：控制端同一轮那八份已提交（那个仓没有这条 ignore），
两端证据一个在库里一个只在盘上是不对称的。

逐片对账（`selectedTestCount` = `recordedTestCount` = trx 里 `<UnitTestResult` 行数，0 条非 `Passed`）：

| 片 | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 条数 | 11 | 5 | 5 | 9 | 2 | 5 | 8 | 19 |

⚠️ **八份的 `g1Status` 都是 `SKIPPED`**，出证时用了 `-SkipProtocolG1`。此后 `b835a40` 把 G1 修好，
**重出与否用户裁定为「先不重出」**，这八份如实保留当时的记录。

两端的 `integrationSliceIndexSha256` 都是 `71e0a63d…`，逐字节相同。

## 五、`G3`：三个 runner 两过一败

证据 `8005-agv-control-server/evidence/g3/20260909-v2-identity/`，提交 `0d26bc9`。
逐条数字与失败原因在那个目录的 `SUMMARY.md`，这里只记要点。

| runner | 结果 | 断言 |
| --- | --- | --- |
| `run-staged-g3.ps1` | `STAGED_G3_RECOVERY_REPLAY_PASS` | 19 / 19 |
| `run-staged-g3-restart.ps1` | `STAGED_G3_PROCESS_RESTART_PASS` | 20 / 20 |
| `run-demand-bearing-g3-vectors.ps1` | **`DEMAND_BEARING_SLICE_FAIL`** | **19 / 20** |

### 开跑前撞上两处此前没人记下的障碍

1. **`run-staged-g3.ps1:71` 的路径里混进了一个 BEL 字节（0x07）。**
   字面量是 `'src\ControlServer.Host<0x07>ppsettings.json'`——写这行的工具把 `\a` 当成了 alert
   转义。PowerShell 单引号串里它是普通字符，于是路径解析成 `src\ControlServer.Hostppsettings.json`，
   脚本**起手第一件事**就抛 `Cannot find path`。由票 14 的 `978a9e4` 引入（那次把身份改成读
   appsettings 镜像），此后没跑过 G3 所以从未触发。已修：`c6cc965`。
   全仓 `scripts/` 的控制字符扫描只有这一处，车载端 `scripts/` 干净。

2. **`run-staged-g3.ps1` 断言 `refs/tags/protocol-v1.0.0^{}` 解析得到候选 commit。**
   那个 tag 至今没打，这条断言在 v2 线上必然开跑即抛。票 15 已在车载端做过同一处改动
   （`run-w2g-g2.ps1:370`），控制端本轮补上：改为绑候选 commit，tag 不存在则记
   `tagExists: false`，**tag 若存在却指向别处仍然抛**。已修：`1987b73`。

**这两条都不在票据、`17-answer.md` 第五节或交接文档列的「四件前提」里。**
那四件（推车载端、改四条 commit 绑定与 `-RemoteRef`、占交互桌面、`-FieldRunRoot`）本轮全部落实：

- 车载端 `w2g/fp-v2-impl` 已推，远端 tip = `153b705`，`-RemoteRef 'origin/w2g/fp-v2-impl'` 的断言通过；
- 四条 commit 绑定与两个 runner 的 `-RemoteRef` 已移到 v2 线（`1987b73`）；
- 交互桌面锁没有排队，三次运行合计约 5 分钟；
- **`-FieldRunRoot` 不是障碍**：`C:\Users\szy\w2g-stage\run\fullloop-20260829T131549Z\controlserver.db`
  在盘上，2026-09-04 那轮用的就是它。

### 那条失败：问的是现场库的历史，不是被测构建

唯一失败的断言是 `protocolAndBuildIdentityBoundToTheSharedBinding`
（`run-demand-bearing-g3-vectors.ps1:614`），六个合取项里五个通过，失败的是

```
[string]$baseline.sessionRecoveryRows[0]['protocolCommit'] -eq $ProtocolCommit
```

恢复的现场库里那一行是 `1531489e42e328f28bfe0c51ed3f8c56e5ce0279`——**`protocol-v0.1.1` 的 commit**，
是 2026-08-29 那次已授权现场运行在**当时的协议**下写进去的。现场库是 v0.1.1 时代的冻结产物，
**任何 v2 身份的运行对它都过不了这一条**，除非重新采一次 v2 下的已授权现场运行。

**决定性佐证（收尾复审补的）：2026-09-04 那一轮之所以通过这条断言，正是因为当时
`$ProtocolCommit` 本身就是 `1531489e`。** 换句话说，这条断言从来没有独立地证过什么——
它只在「现场库与候选是同一个协议」时成立，而那恰好是协议不变时的默认情形。

顺带一处更正：该断言是**七个**合取项不是六个（三个存在性检查 ＋ 四个实质比较），
`SUMMARY.md` 里的表已改。

该 runner 真正要证的 19 条全部通过（RIoT `UNKNOWN` 对账逐腿恰好建一次单、结果重放与三类拒绝、
卸货原子收尾、宿主重启后需求与租约存活、无移动无外部副作用、密钥扫描）。
**失败证据按纪律保留，不重跑覆盖。**

## 六、🔴 票 17 的按片验收，用现有 runner 结构上做不出来

**这是本轮最重要的发现，不是本轮的疏漏。**

三个 G3 runner 都把切片结论写成**字面常量**：

```
run-staged-g3.ps1:2899-2904          formalSlicePass = $false
                                     officialSlices = FP-IS-00 / FP-IS-06，都是 INCONCLUSIVE
                                     fullG3 = 'INCONCLUSIVE'
run-staged-g3-restart.ps1:892-897    同上
run-demand-bearing-g3-vectors.ps1:728-733  同上（只名 FP-IS-04 / FP-IS-05）
```

- 三个加起来只提到**四片**（`00`／`04`／`05`／`06`），`FP-IS-01`／`02`／`03`／`07`
  在任何 G3 runner 里都不出现；
- 三个都只发 `run-result.json`，**全仓只有 `test-wire-to-gate.ps1` 发 `gate-result.json`**；
- **而 `test-wire-to-gate.ps1:4` 是 `[ValidateSet('G2')][string]$Gate = 'G2'`**——
  唯一那个会发 `gate-result.json` 的脚本，**在参数层面就拒绝被要求跑 G3**。
  （这条是收尾复审补的，比初稿的判断更硬。）
- 三个 runner 都没有 `-Slice` 参数；`Slice` 这个词在它们里面只出现在那几个 classification
  常量中间。

这些常量**早于本轮**：由 `b4afdb3`（staged G3 runner 建立时）写下，票 14 的 `978a9e4`
只是把 `W2G-IS-NN` 重打标成 `FP-IS-NN`。所以「既定立场」不是事后追认。

而这是**刻意的立场**，2026-09-04 那份 G3 证据的 `SUMMARY.md` 写得明白：staged G3 绑 commit、
从 exact clone 重新 publish、**不碰任何候选产物，因此不构成切片通过**。

所以票据里那条「八个切片各跑一遍 `G3`，全 PASS，八份 `gate-result.json`」**不是「差几件用户点头
的事」，是缺一次 G3 runner 的按片改造**——与票 22 给车载端 `run-w2g-g2.ps1` 做的同形，
外加一件票 22 不需要做的前置：**先定清「staged G3 下一片算不算通过」**。
那已经越出「跑一轮 v2 身份的 G3」这个授权，见第七节第 1 条。

### 🔴 2026-09-09 第三轮补：缺口比上面写的大，四片根本没有 G3 面

开票 23 前把范围又核了一遍，查出上面那段漏说的一半。把**车载端**的
`run-staged-g3-recovery-ack-drop.ps1` 也算进来，四个 G3 runner 命名的片是：

| runner | 仓 | 命名的片 |
| --- | --- | --- |
| `run-staged-g3.ps1` | 控制端 | `FP-IS-00`、`FP-IS-06` |
| `run-staged-g3-restart.ps1` | 控制端 | `FP-IS-00`、`FP-IS-06` |
| `run-demand-bearing-g3-vectors.ps1` | 控制端 | `FP-IS-04`、`FP-IS-05` |
| `run-staged-g3-recovery-ack-drop.ps1` | 车载端 | `FP-IS-00`、`FP-IS-06` |

**`FP-IS-01`／`02`／`03`／`07` 在四个 runner 里一次都不出现。**
所以「八份 `gate-result.json`」不是一件事是两件：`00`／`04`／`05`／`06` 是把常量换成算出来的
（机械），另四片**没有任何 runner 声称覆盖**，要补场景或如实记「本批次无 G3 面」。

**还有一条更靠里的**：三个 runner 共 19／20／20 条具名断言（`assertions` 那个 `[ordered]@{}`），
**没有一条挂着切片标识**。切片归属整个存在于 `officialSlices` 那个字面常量里，也就是说
「哪条断言构成哪一片的 G3 证据」这件事**今天在代码里没有任何记录**。按片改造的第一步不是改
代码，是把这张归属表写下来——写下来守卫才有东西可钉。已写进票 23 第一节与第三节的
`assertionIds`。

顺带纠一句上面写过的措辞：`test-wire-to-gate.ps1` **已经有** `-Slice` 参数（第 5 行，
`^FP-IS-(0[0-9]|1[0-5])$`），挡路的只有第 4 行 `$Gate` 的 `[ValidateSet('G2')]`；
但它的主体是对本地工作树跑 `dotnet test --filter`，**本质是 G2 夹具**，
放宽 ValidateSet 扩不到 G3。

## 七、待用户裁定

1. ~~**🔴 G3 按片改造要不要单开一张票。**~~
   **✅ 2026-09-09 用户裁定，两问都已定：**

   - 判断题「staged G3 下一片算不算通过」→ **引入分级状态**。不维持现状，也不直接认成通过。
     落法是把 `status`（断言过没过）与 `assuranceLevel`（实际动了什么）拆成两个字段，
     `formalSlicePass` 由 `$LevelsThatCountAsSlicePass` 算出而不再是字面 `$false`；
     `STAGED_REBUILD` 与 `DEMAND_BEARING_RESTORE` 计入，`CANDIDATE_ARTEFACT` 留位。
   - 改造 → **单开票 23**，见
     [23-g3-per-slice-gate-result.md](23-g3-per-slice-gate-result.md)。

   ⚠️ **随之作废的是 2026-09-04 那份 `SUMMARY.md` 里「不构成切片通过」的措辞，
   但那份证据不许改**（证据目录只增不改），作废说明写在票 23 的答复与新一轮 G3 的
   `SUMMARY.md` 里。

   **✅ 票 23 当轮也做完了**（控制端 `a46101e`，见
   [23-answer.md](23-answer.md)）。三个 runner 真跑过，共六份 `gate-result.json`。
   **但本票第三条验收仍勾不上，卡点换成了口径**：`FP-IS-00`／`06` 通过，
   `FP-IS-04`／`05` 失败在下面第 2 条那条现场库历史断言上，`01`／`02`／`03`／`07` 无 G3 面。
   🔴 **要用户定的是本票第三条验收改写成什么**，两条路：

   - ① 认 `STAGED_REBUILD` ＋ `DEMAND_BEARING_RESTORE` 两级，把出口改写成
     「四片有 G3 面：两片通过、两片失败在一条关于现场库历史的已知断言上；四片无 G3 面，记在案」；
   - ② 先按下面第 2 条把那条断言处理掉（本轮裁定不动），再回来谈八片。

   **✅ 2026-09-09 第四轮定了。** 用户看过上面两条路后把选择交给 agent（原话「我也不知道做哪个，
   你选一个最佳的吧」）。选定的是 ①**的一半**：**按分级口径如实改写第三条验收，但不勾，
   本票保持 `in-progress`。** 三条理由：

   1. **改写是必做的，勾不勾是另一件事。** 验收原文「八个切片各跑一遍 `G3`，全 PASS」现在
      与实测对不上——它预设八片都有 G3 面，而 `FP-IS-01`／`02`／`03`／`07` 在四个 runner 里
      一次都不出现。留着这句话，票据本身就是一处失真。改写消除失真，与「出口达没达成」无关。
   2. **勾上等于宣告批次 2 轨 A 出口达成，那是发布层判断，不是文档编辑。** 它的实际内容是
      「接受两片 FAIL 的豁免 ＋ 接受四片无 G3 面」，后果落在 release attestation 那一侧，
      本线的既有纪律是「证据与说明中不得暗示存在可沿用的通过结论」。agent 代签这一步越界。
   3. **不勾是可逆的，勾了不可逆。** 从现在这个状态勾上只要改一行加一段豁免说明；反过来，
      一旦勾上并把豁免理由写进证据 `SUMMARY.md`，撤销要动已入库的证据，而证据目录只增不改。
      两个方向成本不对称时选便宜的那边。

   落地：票 17 第三条验收已改写成分级口径，并在该条末尾写明**勾上它需要的两个收口条件**
   （已知豁免裁定，或先按第 2 条拆断言再重跑），两条都注明要用户裁定。
   **路②仍未动**——它属于改门禁断言，不在任何已有授权内。

   **✅ 同一轮用户随后选了①**：`FP-IS-04`／`05` 那条断言裁定为已知豁免，
   并接受「四片本批次无 G3 面」作为如实出口。**豁免范围写窄到第 7 项合取**，理由与它当前
   不可验证这一点见下面第 2 条。**第三条验收仍未勾**，因为口径解决后还剩一件实事：
   **要跑一轮改造后的 G3 并把六份 `gate-result.json` 入库**——票 23 那六份是临时目录的自证、
   已随 session 消失，库里现有的 `evidence/g3/20260909-v2-identity/` 是分级改造之前的旧形态。
   **跑门禁需要用户单独授权，本轮没跑。**

2. **`run-demand-bearing-g3-vectors.ps1` 那条断言怎么办。**
   ~~**2026-09-09 用户裁定：本轮先不动。**~~
   **✅ 2026-09-09 第四轮改判：裁定为已知豁免**（用户选路①）。两条路原文：
   ① 保持现状，承认这个 runner 在 v2 下不可能过，直到重采一次 v2 现场运行；
   ② 把它拆开——运行中服务端的身份仍然断言，恢复的现场库那份改成如实记录
   （`fieldStoreProtocolCommit`）而不是断言相等。
   **②属于改门禁断言，不在本轮授权内。**

   ### 🔴 落地豁免时查出来的事：这不是「一条断言」，是七项合取

   写豁免范围时回源码核了一遍，`run-demand-bearing-g3-vectors.ps1:626-632`：

   ```powershell
   $protocolBindingPass = $null -ne $version -and                                           # 1
       $version.protocolCommit -eq $ProtocolCommit -and                                     # 2
       $version.protocolTag -eq 'protocol-v1.0.0' -and                                      # 3
       $null -ne $probeResult -and                                                          # 4
       [string]$probeResult.serverBuildCommit -eq $ControlServerCommit -and                 # 5
       $null -ne $baseline -and                                                             # 6
       [string]$baseline.sessionRecoveryRows[0]['protocolCommit'] -eq $ProtocolCommit       # 7
   ```

   ⚠️ **本节初稿把它写成「六项」并说豁免第六项，两处都错**：贴代码时漏掉了第 6 项
   `$null -ne $baseline`，于是最后一项被数成了第六。**豁免的是第 7 项。**
   第 6 项必须留在断言里——「现场库根本没读到」与「读到了、历史对不上」是两回事。

   🔴 **更该记的是这个错误怎么来的：本文第五节末尾早就写过「该断言是七个合取项不是六个
   （三个存在性检查 ＋ 四个实质比较）」，是上一轮就做过的更正。** 第四轮写本节时没有回读
   同一份文档的第五节，凭对交接文档那句「一条关于现场库历史的断言」的印象重述，
   又把六项写了回去。**回源码核救回来了这一次**——但纪律要补一条：
   动一条断言之前，先 grep 本文件里它自己的名字，看这份文档对它已经说过什么。

   **只有第 7 项与现场库历史有关**，前六项问的全是运行中服务端与被测构建的身份。
   所以 `23-answer.md` 第四节那句「那条问的是恢复的现场库里记的 `protocolCommit`」
   **描述的是第 7 项，不是整条断言**——已在该文件就地更正。

   **这决定了豁免必须写窄：豁免的是第 7 项合取，不是 `protocolAndBuildIdentityBoundToTheSharedBinding`
   这个名字。** 笼统豁免整条，等于把六项真正该守的身份检查一起吞掉——将来服务端身份配错、
   被测构建 commit 对不上，这条照样 `FAIL`，而豁免会让它看起来仍是「那个已知的现场库问题」。

   ⚠️ **而以脚本当前的形态，这个窄豁免在证据层面不可验证**：六项揉成一个布尔值写进
   `gate-result.json`，看不出是哪一项 `false`。目前「false 的只可能是第 7 项」是**推断**，
   靠两条旁证：

   - 同脚本 `restartedHostServesTheSameStorePass`（626 行上方）里
     `$versionAfterRestart.protocolCommit -eq $ProtocolCommit` 与
     `$handshakeResult.serverBuildCommit -eq $ControlServerCommit` **都通过了**，
     与第 2／5 项同源；
   - `/version` 端点的字段名实核过（`Program.cs:167-169` 发 `protocolReleaseVersion`／
     `protocolTag`／`protocolCommit`），`appsettings.json` 的 `ProtocolCandidate.tag`
     就是 `protocol-v1.0.0`，所以第 3 项成立——**这一项没有独立佐证，是靠读配置推的**。

   **要让豁免可验证，就得做路②的前半段**：把第 7 项从合取里拆出来单独出字段。
   这仍然属于改门禁断言，**未获授权，本轮没做**。

3. **八份 `ONBOARD_HMI_G2` 要不要在 G1 修好之后重出。**用户本轮定「先不重出」。
   重出的话八份 `g1Status` 会从 `SKIPPED` 变 `PASS`，但要 `-ProtocolRoot` 指一份普通克隆
   （见第二节），且要再占一次机器与门禁授权。

4. **控制端 `dotnet format --verify-no-changes` 在 `fp/v2-impl` 上是 `exit=2`。**
   **2026-09-09 用户裁定：本轮先不动。**
   8 条 `WHITESPACE`，散在 `OnboardJourneyPublisher.cs`、`OnboardPeerSession.cs`、
   `ExperimentalRiotCreateGateTests.cs`、`JourneyRuntimeWorkerTests.cs`——**四个文件工作树都没改动，
   是分支上既有的**，与本轮无关。`test-wire-to-gate.ps1` 不跑 format，所以
   `CONTROL_SERVER_G2` 不受影响；车载端的 `run-w2g-g2.ps1` 跑，而车载端 `formatExitCode` 是 0。
   补不补请用户定。
   **→ 2026-09-14 转出 `8005-agv-control-server#59`。**当日在 `fp/v2-impl`（`2b2aa51c`）实测已涨到
   11 个文件 37 处 `WHITESPACE`。

5. 上一版第七节那两件本轮都做完了（车载端证据已提交、`FP-IS-02` 测试已补并重出证据）。

## 八、两条顺带记下的观察

1. **`8005-agv-control-server/CLAUDE.md` 第 121 行还写着 `global.json` 是 `8.0.424`**，
   `a143c9c` 之后已经是 `8.0.425`。本轮仍没改（不在授权范围内）。

2. **🔴 交接第七节第 11 条的判断要改：那条已经是 bug，不是「将来才会变成 bug」。**

   原文说「目前没有任何机制对证据文件取哈希，所以不构成问题」。**有的**——
   `run-result.json` 自己带一张 `evidenceFiles` 的 SHA-256 表，三个 G3 runner 都发。
   那张表是在落库前对盘上的 CRLF 版本算的，而 `.gitattributes` 的 `* text=auto eol=lf`
   在落库时把它们规范成 LF，**于是库里的字节与表里的摘要对不上**。

   本轮实测（`evidence/g3/20260909-v2-identity/staged/`）：

   | 文件 | `evidenceFiles` 记的 | 库里 blob 实际 |
   | --- | --- | --- |
   | `configuration.json` | `f4ba9086…` | `86f4d427…` |
   | `logs/protocol-g1.log` | `bcf40949…` | `e4debd31…` |

   表里那两个值与**盘上**的文件逐位相同，所以表本身没算错，是落库改了字节。

   **而且这不是本轮引入的。**上一轮已提交的 `evidence/g3/20260904-after-journey-fix/`
   同病：`staged` 前 40 条里 17 条对不上，`process-restart` 前 40 条里 15 条对不上
   （对得上的是本来就只有 LF 或不含换行的那些）。

   目前没有任何东西去**校验**这张表，所以它还没让谁做出错误判断；但它是一张**已经错了**的
   摘要表，任何将来写来核对证据完整性的工具都会一上来就报全红。要不要修、怎么修
   （给 `evidence/**` 加 `-text`？还是让 runner 写 LF？）请用户定。
   **2026-09-09 用户裁定：本轮先不动，缺口保持记录在案。**
