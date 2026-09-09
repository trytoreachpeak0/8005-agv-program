# 17 — `FP-IS-00`～`07` 在 v2 下重证

**做什么：** 把八个批次 0 切片在协议 v2 下重新证一遍，三道门禁全 PASS：
`CONTROL_SERVER_G2`、`ONBOARD_HMI_G2`、`G3`。这是**批次 2 轨 A 的出口**。

八个切片与 `W2G-IS-00`～`07` 一一对应，关系是「**v2 下的重证**」而不是「可以沿用的通过
结论」——`ConformanceRunIdentity` 已规定任一绑定分量变化都必须建立新运行。

**而且根本没有通过结论可以沿用**：`RELEASE-CANDIDATE.md` 第 12 节末原文写着
`W2G-IS-00`～`07` 与 RC 目前仍为 `INCONCLUSIVE`，八类 G3 向量各有证据不等于八个切片通过。
**证据与说明里都不得暗示存在可沿用的通过结论。**

`ONBOARD_HMI_G2` 自 2026-09-04 起由我方跑、我方填那一列，不再等 Kun Wang。**但这不改变
谁签发布**——release attestation 仍要两名不同产品负责人。

**排期提示（不是硬依赖）**：G2 与 G3 证据绑定精确 commit。轨 B 的能力票会持续改服务端，
建议把这八个切片的重证放在一个**连续窗口**内跑完，窗口内轨 B 暂缓合并；或等轨 B 的票
09～13 合完再跑。两种都行，别边跑边合。

**前置：** ~~票 14（服务端 v2）~~✅、~~票 15（车载端 v2）~~✅、~~票 16（`vectorId` 绑定守卫）~~✅、
~~票 21（`FP-IS-07` 两个向量缺口）~~✅、~~票 22（`IntegrationSlice` trait ＋ `-Slice`）~~✅。
**2026-09-09：两条硬障碍都已不在**——`dotnet format` 那条已搬运（`d9dd631`），
`-Slice`／`IntegrationSlice` 那条由票 22 关闭（`b4f3530`），`win11-01` 那条经实测与用户裁定
不是本票前提。**本票现在真的可开工，且开工的第一步是进门禁，需用户点头。**

**票 16 于 2026-09-08 完成，这一条前置解除**（见 [16-answer.md](16-answer.md)）。守卫落在
控制端 `562544e`，CI 绿（run
[34227325616](https://github.com/trytoreachpeak0/8005-agv-control-server/actions/runs/34227325616)，
`569 passed / 0 failed / 0 skipped`）。

**票 14 于 2026-09-08 完成，这一条前置也解除**（见 [14-answer.md](14-answer.md)）。服务端已说
v2，三条 C_TO_O 快照的 payload 形状按 v2 schema 改对，186 处 trait 重打为 `FP-IS-NN`，
L1 `586 passed / 0 failed / 0 skipped`。
**票 15 于 2026-09-09 完成，最后一条前置解除**（见 [15-answer.md](15-answer.md)）。车载端
`w2g/fp-v2-impl` = `9ec5b29`（已推送），`172 passed / 0 failed / 0 skipped`。

票 15 转交本票四件事，**其中前两件会挡住出证，开工先看**：

1. **`dotnet format --verify-no-changes` 在 `core.autocrlf=true` 的 checkout 上必然失败。**
   实测 `exit=2`、21494 条 `ENDOFLINE` ＋ 16 条 `WHITESPACE`，涉及 71 个 `.cs` 文件，**包括票 15
   一个字都没碰的 `App.xaml.cs` 与 `DomainModels.cs`**。原因是仓库存 LF、`.editorconfig` 要 LF、
   而 git 落盘成 CRLF。`run-w2g-g2.ps1` 把 format 的退出码计入 `hmiStatus`，所以**不先解决它，
   八份证据全是 FAIL**。两条路：跑门禁的机器设 `core.autocrlf=false`／`input`，或给该仓加
   `* text=auto eol=lf`（会重写全仓行尾，**属于对方仓库的决定**）。详见 15-answer.md 第十一节。
2. **`run-w2g-g2.ps1` 没有 `-Slice` 参数。** 它跑整个解决方案的测试、不按切片过滤，
   `summary.json` 里 `FP-IS-00` 与 `FP-IS-01` 共享同一个 `onboardHmiG2` 结论，其余六片根本不
   出现。**本票要按切片各出一份证据，这个脚本要先改造**——而按切片过滤需要车载端先有
   `IntegrationSlice` trait，那是票 20。已在脚本的 `knownLimitations` 里写明。
3. **车载端的门禁脚本身份已切到 v2 候选**，`$expected` 表十个值与
   `WireToGateProtocol.cs` 由 `ProtocolIdentityArchitectureTests` 逐字段钉住。tag 断言从「绑
   tag」改成「绑候选 commit」——`protocol-v1.0.0` 至今没打。`summary.json` 的 `protocol` 节多了
   `tagExists`／`candidateCommit`／`candidateIsAncestorOfHead`／`approvalStatus` 四个字段。
   `run-staged-g3-recovery-ack-drop.ps1` 的 `startedScope` 已改成 `FP-IS-00`／`FP-IS-06`。
4. **车载端的门禁跑在 `w2g/fp-v2-impl` 上，不是 `OnboardHmi_MVP`。**
   `OnboardHmi_MVP` 已钉到已发布的 `protocol-v0.3.0`（`ProtocolVersion 3`／`WIRE_TO_GATE_MVP`），
   与本线不是同一条协议。**证据里的 commit 绑定要写 `w2g/fp-v2-impl` 的 commit。**

票 14 转交本票三件事：

1. **`test-wire-to-gate.ps1` 的调用形态变了。** `-Slice` 只收 `FP-IS-NN`（正则
   `^FP-IS-(0[0-9]|1[0-5])$`）；身份不再硬编码在脚本里，改从
   `src/ControlServer.Host/appsettings.json` 的 `ProtocolCandidate` 读；切片的向量清单改从
   `vendor/8005-agv-protocol/integration-slices/index.json` 读，不再是脚本里那份手抄表。
   `gate-result.json` 的 `schemaVersion` 升到 `1.1.0`，新增 `protocolProfileId`、
   `protocolVersion`、`protocolApprovalStatus`、`integrationSliceIndexSha256`、
   `selectedTestCount` 五个字段。
2. **`FP-IS-08`～`15` 出不了 G2 证据，本票的出口只能是八片。** 票 14 实测发现
   `dotnet test --filter` 选不中任何测试时退出码是 0，脚本会把它写成 `"status": "PASS"`——
   一个零实现的切片拿到过一份绿的 G2 结果。已改成建目录前先数、选中 0 条即拒绝并报出该片向量。
3. **`ApprovalStatus` 是 `SUPERSEDING_CANDIDATE`，不是 `APPROVED_RELEASE`。**
   `New-WireToGateReleaseCandidate.ps1` 因此拒绝打 RC，这是规格 6.6 要的效果，不是要绕过的
   障碍。本票的出口是三道门禁全 PASS，**不含 RC**。

## 票 21 转交本票四件事（2026-09-09，见 [21-answer.md](21-answer.md)）

**票 21 已把 `FP-IS-07` 的两个向量缺口关掉**，`VectorsThisBatchOwesANamedTest` 已清空。
车载端 `w2g/fp-v2-impl` = `ea3c75e`，`154 + 42 passed`，未推送。本票不再有向量欠账。
但票 21 换来了四件新的开工须知：

1. ~~**🔴 CI runner（`win11-01`）现在会 `dotnet` 失败。**~~ **这条不是本票的前提，2026-09-09
   实测证伪 ＋ 用户裁定。** SDK 基线 8.0.425 确实已搬到 `w2g/fp-v2-impl`（`3f26a32`）与控制端
   `fp/v2-impl`（`a143c9c`），`win11-01` 确实还是 8.0.424；错的是「门禁证据与发布包都在它上面
   产出」这半句——它出自 `7a4e509` 的提交信息，但历史 `CONTROL_SERVER_G2` 证据的 `.trx` 里写的
   是 `computerName="LAB-WIN-01"`（见 `evidence/g2/20260830-issue26-264615a/*/`），G3 证据里的
   路径也是 `C:\Users\szy`，**都是本机**。本机已是 8.0.425。`win11-01` 上跑的是 GitHub Actions
   （`test.yml`／`l2.yml`，触发条件是推 `main`／`ControlServer_MVP` 或开 PR）与 `release.yml`
   出包，而本票的出口明写「不含 RC」。
   **用户 2026-09-09 裁定：不算本票前提，门禁在本机出证**，`win11-01` 的升级另作运维事项跟踪。

   好处仍然成立：本机现在可以直接在仓库目录内跑 `dotnet`，旧交接里那个「仓库外临时目录钉
   `global.json`」的绕法作废。

2. **上面第 1 条障碍（`dotnet format`）的修法已经存在，是搬运不是裁定。**
   远端 `w2g/normalize-line-endings` HEAD `9ee7e4d`（Zhengyu Shao，2026-09-09 11:04）给该仓加
   `.gitattributes` 的 `* text=auto eol=lf`，提交信息里直接写着「这正是 `ONBOARD_HMI_G2`
   从未绿过的原因」，实测 22800 条 `ENDOFLINE`。

   ⚠️ **不能直接 cherry-pick。** 那份只有全局那条（它从 MVP 线出，那条线没有 vendor 目录），
   本线现有的 `.gitattributes` 只有票 15 加的 `vendor/8005-agv-protocol/** -text`。
   **两条都要有。**

   另：**控制端本线早就有 `* text=auto eol=lf`**，这条障碍只存在于车载端。

   ✅ **2026-09-09 已搬运，见 `d9dd631`。** 前后实测：`exit=2`／22093 条 `ENDOFLINE` ＋ 16 条
   `WHITESPACE`／62 个 `.cs` → `exit=0`／零诊断。全仓 206 个文本文件现在一律 `i/lf w/lf`，
   vendor 73 个文件字节未动（`manifest/release.json` 仍是 `84f984ea…`）。

   ⚠️ **上面「否则 71 个文件的 SHA-256 会全部漂移」那句是错的**，搬运时把四种规则顺序各真跑一遍
   证伪了它：只要全局那条带着 `eol=lf`，vendor 那条在前在后摘要都不漂；顺序只在有人把 `eol=lf`
   删掉、退回让 `core.autocrlf` 决定时才成为分界。四行表在 `.gitattributes` 的注释里，推导在
   [22-answer.md](22-answer.md) 第一节。

3. ~~**上面第 2 条障碍（`-Slice`／`IntegrationSlice`）原封不动。**~~
   **✅ 2026-09-09 由票 22 关闭**（用户裁定单开一张票），见
   [22-onboard-integration-slice-trait-and-slice-gate.md](22-onboard-integration-slice-trait-and-slice-gate.md)
   与 [22-answer.md](22-answer.md)。车载端 `b4f3530`：新增 64 行 `IntegrationSlice` trait
   （由既有 58 处 `ProtocolVector` 按切片索引投影，只投到 `sequence ≤ 7` 的八片），
   `run-w2g-g2.ps1` 有了 `-Slice`，带 `-Slice` 的运行另出一份 `gate-result.json`
   （`schemaVersion 1.1.0`，与控制端同形）。
   ⚠️ `CV-MANUAL-CHARGING-RETURN` **不挂 `FP-IS-13`**，理由见 22-answer.md 第三节。

   八片实测选中数：`FP-IS-00` 11、`01` 5、`02` 5、`03` 9、`04` 2、`05` 5、`06` 8、`07` 19，
   八片全 PASS。**这些冒烟跑在临时证据目录里，不是本票的门禁证据。**

4. **真正驱动物理解锁的 G2 夹具仍然不存在。** 票 21 的四条测试走的是「目标仓位本来就没货」
   那条短路，`PulseUnlockAsync` 与 `WaitForLockerAsync` 一次都没调用；
   `FakeIoModuleClient.WaitForLockerAsync` 至今 `throw new NotSupportedException`。
   `FP-IS-07` 的向量绑定补齐了，但「解锁—等待反馈—复位」在车载端仍无测试驱动。

票 16 转交本票一件事：`CV-LOAD-CANCELLATION-ALL-EMPTY` 是它 20 条绑定里最薄的一条——服务端
取消面（`OnboardRecoveryCoordinator.AuthorizeLoadCancellationAsync`）只有
`FailedCompensationResultIsDurableReplayableAndNeverReleasesDemandOrVehicle` 一条测试覆盖，
且走的是 `REJECTED` 分支，只证了 `AUTHORIZE_CANCELLATION_EXPLICITLY` 那一半；
`RECONCILE_EMPTY_FINAL_STATE` 那一半在实现里（同文件 `safeEmpty` 判据）但没有独立测试。
**`FP-IS-02` 重证时应当补上。**

**状态：** in-progress —— 2026-09-09 第二轮：两道 G2 已全绿并全部入库；**G1 本身实测通过**
（协议仓已提交的 `evidence/g1-result.json` 本轮独立复现，且三次 G3 运行的 G1 都 `PASS`），
但**已出证的那八份 `ONBOARD_HMI_G2` 仍记 `g1Status: SKIPPED`**——修好 G1 的 `b835a40`
晚于它们，用户裁定先不重出。G3 三个 runner 跑了两过一败。见 [17-answer.md](17-answer.md)。
**八个切片仍未通过，而上一轮查清了原因：第三条验收用现有 G3 runner 结构上做不出来**，
详见 17-answer.md 第六节。
**2026-09-09 第三轮：用户裁定「引入分级状态」＋「单开票 23」，
本票第三条验收自此显式阻塞在[票 23](23-g3-per-slice-gate-result.md)**，
其余三条待裁定（demand-bearing 断言、证据 SHA-256、控制端 format 8 条）用户定先不动。
**2026-09-09 第四轮：票 23 已 `done`，第三条验收的阻塞随之从工程问题变成口径问题。**
用户把「改写成什么」交给 agent 定，选定**按分级口径如实改写、但不勾**，
本票因此仍是 `in-progress`，且**唯一未完的就是第三条**。
**同一轮用户随后选了收口路①：`FP-IS-04`／`05` 那条断言裁定为已知豁免**（范围写窄到第 7 项合取，
见该条末尾）。**口径问题到此解决，第三条现在只差一件事：跑一轮改造后的 G3 并把证据入库，
而那需要用户单独授权门禁。**

- [x] 八个切片各跑一遍 `CONTROL_SERVER_G2`，八份 `gate-result.json` 全 PASS
      —— `fp/v2-impl` = `a143c9c`，证据已提交（`5915cf7`）；`FP-IS-02` 另有一份绑 `3f62647`
      的重出（`e3ea250`，`selectedTestCount` 17 → 18）
- [x] 八个切片各跑一遍 `ONBOARD_HMI_G2`，八份 `gate-result.json` 全 PASS
      —— `w2g/fp-v2-impl` = `360a405`，**证据已 `git add -f` 提交入库**（`153b705`，73 个文件，
      用户 2026-09-09 裁定两端对齐；先例 `a1e32dd`）
- [ ] `G3` 的按片出证与分级结论 —— **2026-09-09 第四轮按[票 23](23-g3-per-slice-gate-result.md)
      的分级口径改写，本条仍不勾**，收口条件写在本条末尾。
      **改写前的原文是「八个切片各跑一遍 `G3`，全 PASS」**：那个口径在本批次不可能成立，
      而且它预设的「八片都有 G3 面」本身与事实不符（见下表）。改写只是让本条与实测对齐，
      **不代表本条已达成**。下面这段解释它当初为什么做不出来，保留不删：
      三个 runner 把切片结论写成字面常量（`formalSlicePass = $false`、
      `officialSlices` 只名 `FP-IS-00`／`04`／`05`／`06` 且都是 `INCONCLUSIVE`），
      且都只发 `run-result.json`，全仓只有 `test-wire-to-gate.ps1` 发 `gate-result.json`
      而它第 4 行是 `[ValidateSet('G2')]`。**这是那三个 runner 的既定立场，不是配置问题**
      ——见 17-answer.md 第六节。上一轮已按现有形态跑完一轮 v2 身份的 G3，证据 `0d26bc9`。

      **✅ 票 23 于 2026-09-09 完成**（控制端 `a46101e`），三个 runner 都真跑过。
      但**本条仍勾不上，而且卡点已经从工程问题变成口径问题**——实测出来的是这样：

      | | 片 | 结果 |
      | --- | --- | --- |
      | 有 G3 面且通过 | `FP-IS-00`、`FP-IS-06` | `status=PASS`、`assuranceLevel=STAGED_REBUILD`、`formalSlicePass=true`（staged 与 restart 各出一份，共四份） |
      | 有 G3 面但失败 | `FP-IS-04`、`FP-IS-05` | `status=FAIL`，失败在 `protocolAndBuildIdentityBoundToTheSharedBinding`——**那条问的是恢复的现场库的历史，不是被测构建**（第七节第 2 条，用户裁定本轮不动） |
      | 无 G3 面 | `FP-IS-01`／`02`／`03`／`07` | 四个 G3 runner 里一次都不出现；用户裁定如实记录，不发证据 |

      **所以「八个切片全 PASS」在本批次不可能成立。**
      2026-09-09 第四轮用户把改写口径的选择交给 agent，选定的是**「按分级口径如实改写，但不勾」**
      （理由见 [17-answer.md](17-answer.md) 第七节第 1 条末尾）：改写消除票据与实测之间的失真，
      而「本批次轨 A 出口是否达成」属于发布层判断，不由 agent 代签。

      **✅ 2026-09-09 第四轮：用户选路①，`FP-IS-04`／`05` 那条断言裁定为已知豁免。**
      同时接受「四片本批次无 G3 面」作为如实出口。路②（拆断言）**未选、未做**。

      **豁免的范围是这个，不能写宽：**

      - 豁免的是 `protocolAndBuildIdentityBoundToTheSharedBinding` 的**第 7 项合取**——
        `baseline.sessionRecoveryRows[0].protocolCommit -eq $ProtocolCommit`，
        问的是被恢复的现场库的历史（2026-08-29 那次现场运行绑 `protocol-v0.1.1`），
        不是被测构建，任何 v2 身份的运行对它都过不了，除非重采一次 v2 现场运行。
      - **不豁免同一条断言的前六项**（运行中服务端的 `protocolCommit`／`protocolTag`、
        被测构建的 `serverBuildCommit`、两个非空守卫）。它们是真正该守的身份绑定。
      - ⚠️ **以脚本当前形态，这个窄豁免在证据层面不可验证**：六项揉成一个布尔值，
        `gate-result.json` 看不出是哪一项 `false`。「只有第 7 项挂了」当时是带旁证的推断。
        要让它可验证得做路②的前半段（把第 7 项单独出字段），**那仍需单独授权**。
        展开见 [17-answer.md](17-answer.md) 第七节第 2 条。

      **裁定完成后，勾上本条还差最后一步——而这一步没做：**

      ⚠️ **本票正式出证要另跑一轮 G3 并另外授权。** 票 23 那六份 `gate-result.json`
      是它自己的自证，落在临时目录、随 session 清理**已经消失**，**不是本票的门禁证据**。
      库里现有的 `evidence/g3/20260909-v2-identity/` 是**分级改造之前**按旧形态跑的，
      没有按片 `gate-result.json`。所以本条**在证据入库之前不能勾**——
      勾了就是「验收勾上、证据不在库」，正是本线一直在防的失真。
      出证那一轮的 `SUMMARY.md` 里要把上面这段豁免范围逐字写进去。
- [x] 每份 `gate-result.json` 绑定精确的 `ProtocolReleaseIdentity`（v2 三元组）
      —— 两端各八份逐字段一致，`approvalStatus` = `SUPERSEDING_CANDIDATE`，`tagExists` = `false`
- [x] 证据落在 `evidence/g2/<日期>-<描述>/`（车载端脚本另插一层 `protocol-v1.0.0`，是它既有的
      目录约定）；`evidence/g3/20260909-v2-identity/` 三个子目录一 runner 一份
- [x] `-EvidenceRoot`／`-Output` 都是不存在的目录；**在这两个仓里**本轮没有重跑覆盖任何既有证据，
      **包括那份失败的 `DEMAND_BEARING_SLICE_FAIL`**。
      ⚠️ 范围说明：协议仓的 `evidence/g1-result.json` **被覆写过一次**——`g1-validate.mjs` 会写它，
      本轮第一次冒烟跑在了协议工作树上。已还原并核过 SHA-256（`82a20ee2…`），
      详见 17-answer.md 第二节末
- [x] 证据目录只增不改
- [x] 车载端侧的门禁跑在我方 `w2g/*` 分支上，commit 绑定如实记录
      （`implementationBranch` = `w2g/fp-v2-impl`）
- [x] 证据与说明中不出现「沿用已通过结论」这类表述——三份 `SUMMARY.md` 都在开头明写

⚠️ **本轮做不到／没做的，写在这里而不是藏起来**：

1. ~~**G3 的按片验收做不出来**（上面第三条）。需单开一张改造票，并先裁定「staged G3 下一片
   算不算通过」。~~ **2026-09-09 两件都做完了**：分级状态由用户裁定引入，改造由
   [票 23](23-g3-per-slice-gate-result.md) 完成。**但上面第三条仍不勾**，
   现在缺的不是工具而是那两个收口裁定（见该条末尾）。
2. **`run-demand-bearing-g3-vectors.ps1` 失败一条断言**，失败在恢复的现场库那行记的
   `protocolCommit` 是 `protocol-v0.1.1` 的——那是 2026-08-29 现场运行的历史，
   任何 v2 身份的运行对它都过不了。该 runner 真正要证的 19 条全过。
3. **八份 `ONBOARD_HMI_G2` 的 `g1Status` 仍是 `SKIPPED`。** G1 本身实测通过
   （`b835a40` 修好了 `run-w2g-g2.ps1`），但用户裁定「先不重出证据」。

**上一版这里写的两件已经不成立**：「协议 G1 在本机跑不了」经实测证伪（见 17-answer.md
第一节）；`FP-IS-02` 那条测试**已补**（`3f62647`）并已重出证据（`e3ea250`）。
