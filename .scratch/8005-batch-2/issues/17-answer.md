# 票 17 决议（进行中）—— `FP-IS-00`～`07` 在 v2 下重证

**日期：** 2026-09-09（第二轮）
**状态：四道门禁跑了三道半。** 用户 2026-09-09 第二次裁定「先跑一轮 v2 身份的 G3，验收另议」。
**八个切片仍未通过**——而现在知道了原因：**用现有 G3 runner 做不出「八片各一份 `gate-result.json`」，
且这是那三个 runner 的既定立场，不是本轮的疏漏。**详见第六节。

| 门禁 | 结果 | 绑定 |
| --- | --- | --- |
| `G1` | ✅ `PASS`，`failures: []` | 协议仓已提交的 `evidence/g1-result.json`@`f6ee75d`，本轮独立复现逐字段相同 |
| `CONTROL_SERVER_G2` × 8 | ✅ 八份 `gate-result.json` 全 PASS | `fp/v2-impl` = `a143c9c`；`FP-IS-02` 另有一份 `3f62647` 的重出 |
| `ONBOARD_HMI_G2` × 8 | ✅ 八份 `gate-result.json` 全 PASS | `w2g/fp-v2-impl` = `360a405`，**本轮已提交入库** |
| `G3` | ⚠️ 三个 runner 两过一败，**且按片验收结构上做不出来** | `e3ea250` ＋ `153b705` ＋ `fb5f7c5` ＋ `f6ee75d` |

所有证据都绑 `protocol-v1.0.0@f6ee75defe6e2d18f63f4082bee445dbb678ab1b`，
`approvalStatus` = `SUPERSEDING_CANDIDATE`，`tagExists` = `false`（tag 至今没打）。

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

`b835a40` 因此在 `Invoke-ProtocolG1` 里前置认出这个形状并如实说明，而不是报成 FAIL 诬告候选。
指向一份普通克隆时实测 `Status: PASS`、`protocol.g1Status = PASS`。

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
- 三个都只发 `run-result.json`，**全仓只有 `test-wire-to-gate.ps1` 发 `gate-result.json`**。

而这是**刻意的立场**，2026-09-04 那份 G3 证据的 `SUMMARY.md` 写得明白：staged G3 绑 commit、
从 exact clone 重新 publish、**不碰任何候选产物，因此不构成切片通过**。

所以票据里那条「八个切片各跑一遍 `G3`，全 PASS，八份 `gate-result.json`」**不是「差几件用户点头
的事」，是缺一次 G3 runner 的按片改造**——与票 22 给车载端 `run-w2g-g2.ps1` 做的同形，
外加一件票 22 不需要做的前置：**先定清「staged G3 下一片算不算通过」**。
那已经越出「跑一轮 v2 身份的 G3」这个授权，见第七节第 1 条。

## 七、待用户裁定

1. **🔴 G3 按片改造要不要单开一张票。**见第六节。改造范围：给三个 runner 加 `-Slice`、
   按片发 `gate-result.json`、把 `officialSlices` 由常量改成算出来的，并先裁定「staged G3
   下一片算不算通过」——后者是判断问题不是工程问题，`formalSlicePass = $false` 是有意为之。
   在它落地之前，**票 17 的第三条验收无法勾上**。

2. **`run-demand-bearing-g3-vectors.ps1` 那条断言怎么办。**两条路：
   ① 保持现状，承认这个 runner 在 v2 下不可能过，直到重采一次 v2 现场运行；
   ② 把它拆开——运行中服务端的身份仍然断言，恢复的现场库那份改成如实记录
   （`fieldStoreProtocolCommit`）而不是断言相等。
   **②属于改门禁断言，不在本轮授权内。**

3. **八份 `ONBOARD_HMI_G2` 要不要在 G1 修好之后重出。**用户本轮定「先不重出」。
   重出的话八份 `g1Status` 会从 `SKIPPED` 变 `PASS`，但要 `-ProtocolRoot` 指一份普通克隆
   （见第二节），且要再占一次机器与门禁授权。

4. **控制端 `dotnet format --verify-no-changes` 在 `fp/v2-impl` 上是 `exit=2`。**
   8 条 `WHITESPACE`，散在 `OnboardJourneyPublisher.cs`、`OnboardPeerSession.cs`、
   `ExperimentalRiotCreateGateTests.cs`、`JourneyRuntimeWorkerTests.cs`——**四个文件工作树都没改动，
   是分支上既有的**，与本轮无关。`test-wire-to-gate.ps1` 不跑 format，所以
   `CONTROL_SERVER_G2` 不受影响；车载端的 `run-w2g-g2.ps1` 跑，而车载端 `formatExitCode` 是 0。
   补不补请用户定。

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
