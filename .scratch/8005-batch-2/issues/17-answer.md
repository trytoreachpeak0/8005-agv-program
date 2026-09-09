# 票 17 决议（进行中）—— `FP-IS-00`～`07` 在 v2 下重证

**日期：** 2026-09-09
**状态：三道门禁跑了两道。** 用户 2026-09-09 裁定「先跑两道 G2，G3 等推送定下来」。
**八个切片因此尚未通过**——一片要四道门禁齐全才算过。

| 门禁 | 结果 | 绑定 |
| --- | --- | --- |
| `CONTROL_SERVER_G2` × 8 | ✅ 八份 `gate-result.json` 全 PASS | `fp/v2-impl` = `a143c9c` |
| `ONBOARD_HMI_G2` × 8 | ✅ 八份 `gate-result.json` 全 PASS | `w2g/fp-v2-impl` = `360a405` |
| `G3` × 8 | ⬜ 未运行 | 需先推车载端，见第五节 |

两份证据都绑 `protocol-v1.0.0@f6ee75defe6e2d18f63f4082bee445dbb678ab1b`，
`approvalStatus` = `SUPERSEDING_CANDIDATE`。

---

## 一、开工前先清掉的两条硬障碍

票据里列的两条硬障碍在本轮开工前已经不存在，过程不在本票里：

1. **`dotnet format`** —— 2026-09-09 `d9dd631` 搬入 `.gitattributes` 的全局 LF 规则。
   `exit=2`／22093 条 `ENDOFLINE` → `exit=0`／零诊断。
2. **`-Slice`／`IntegrationSlice`** —— 票 22（`b4f3530` ＋ `360a405`）。
   见 [22-answer.md](22-answer.md)。

第三条「`win11-01` 的 SDK」经实测证伪：历史 `CONTROL_SERVER_G2` 证据的 `.trx` 里写的是
`computerName="LAB-WIN-01"`，G3 证据里的路径也是本机。**用户 2026-09-09 裁定不算本票前提。**
本轮两道 G2 确实都在 `LAB-WIN-01` 上产出，`.NET SDK 8.0.425`。

---

## 二、`CONTROL_SERVER_G2`：八片全 PASS

证据：`8005-agv-control-server/evidence/g2/20260909-fp-is-00-07-v2-recertification/`，
提交 `5915cf7`。出证前跑过全量套件：`586 passed / 0 failed / 0 skipped`（Release）。

| 片 | `selectedTestCount` | `testExitCode` |
| --- | --- | --- |
| `FP-IS-00` | 59 | 0 |
| `FP-IS-01` | 69 | 0 |
| `FP-IS-02` | 17 | 0 |
| `FP-IS-03` | 27 | 0 |
| `FP-IS-04` | 10 | 0 |
| `FP-IS-05` | 12 | 0 |
| `FP-IS-06` | 38 | 0 |
| `FP-IS-07` | 19 | 0 |

十二个身份字段八份逐字段一致。

---

## 三、`ONBOARD_HMI_G2`：八片全 PASS

证据：`8005-agv-onboard-hmi/evidence/g2/20260909-fp-is-00-07-v2-recertification/`。
**未提交**——该仓 `.gitignore` 第 9 行把 `evidence/` 与 `bin/`、`obj/`、`logs/`、`artifacts/`
归在一起，全仓只有一份 G3 证据当年被强制加进去过（`a1e32dd`，为了一份缺陷说明）。
**要不要破例把这八份也提交，请用户定**（见第六节第 1 条）。

| 片 | selected | recorded | build/test/format |
| --- | --- | --- | --- |
| `FP-IS-00` | 11 | 11 | 0/0/0 |
| `FP-IS-01` | 5 | 5 | 0/0/0 |
| `FP-IS-02` | 5 | 5 | 0/0/0 |
| `FP-IS-03` | 9 | 9 | 0/0/0 |
| `FP-IS-04` | 2 | 2 | 0/0/0 |
| `FP-IS-05` | 5 | 5 | 0/0/0 |
| `FP-IS-06` | 8 | 8 | 0/0/0 |
| `FP-IS-07` | 19 | 19 | 0/0/0 |

八次运行时工作树都是干净的（`hmi.workingTreeStatus` 均为空数组）。构建与
`dotnet format` 是全仓的，八次各跑一遍，不按切片收窄。

### 两端读的是同一张切片表

两份证据的 `integrationSliceIndexSha256` 都是
`71e0a63d49d1973653e1f70addc19c334faff5e53e8597733c1423a7307bd82f`，**逐字节相同**。
控制端读 `vendor/8005-agv-protocol/integration-slices/index.json`，车载端的脚本读
`$ProtocolRoot` 那份——两条路径落到同一份内容，不是各自一份手抄表。

---

## 四、⚠️ 协议 G1 在本机跑不了，八份 `ONBOARD_HMI_G2` 都是 `g1Status: SKIPPED`

**先试过，没绕过去，如实记在证据里。**

`run-w2g-g2.ps1` 的 `Invoke-ProtocolG1` 调 `& pnpm g1`。这台机器：

- `pnpm` 不在 PATH 上（`run-staged-g3.ps1` 有一条指向 codex runtime 里 `pnpm.cjs` 的后备，
  `run-w2g-g2.ps1` 没有）；
- 那份 `pnpm.cjs` 自己会先做依赖状态检查、去调 `pnpm install`，同样因为 `pnpm` 不在 PATH 而失败；
- 绕过 pnpm 直接 `node tools/g1-validate.mjs` 也不行：协议仓没有 `node_modules`，
  起手就是 `Cannot find package 'ajv'`。

**所以给 `run-w2g-g2.ps1` 补 pnpm 后备是没用的**——补了也过不了 `ajv` 那关。真正缺的是
「这台机器能装协议仓的依赖」。**本票没有去装**：那要网络，且要写进一个本线只读的仓。

06:05 那次带 G1 的尝试因此中止，**没有产出任何文件**（运行 id
`20260909T060552149Z-360a4059c9da`，目录为空，已删除；这条记在车载端证据的 `SUMMARY.md` 里）。

**G1 不是本票要的三道门禁之一**（票据原文：`CONTROL_SERVER_G2`、`ONBOARD_HMI_G2`、`G3`），
而协议身份的九个哈希字段仍由脚本自己逐项比对过、八份一致。

---

## 五、`G3` 没跑的原因，以及跑它需要什么

`run-staged-g3.ps1` **从 GitHub 克隆车载端**（`$OnboardRepository` 默认是仓库 URL），
且 `New-ExactClone -RemoteRef 'origin/OnboardHmi_MVP'` 会断言远端 tip 等于 `$OnboardCommit`。
车载端本线的提交按用户 2026-09-09 的裁定尚未推送——远端停在 `9ec5b29`，本地 `360a405`。

跑 G3 需要四件事，**每一件都要用户点头**：

1. **推 `w2g/fp-v2-impl` 到 origin。**
2. **改 `run-staged-g3.ps1` 的四条 commit 绑定与 `-RemoteRef`**：`OnboardHmi_MVP` → `w2g/fp-v2-impl`，
   `$ControlServerCommit`／`$OnboardCommit` 移到本线的 commit。
   （`$SimulatorCommit` 不用动：`slots-simulator` 在 `fb5f7c5`，与脚本默认值一致，且全仓不引用
   任何协议身份。）
3. **占用交互桌面**：两个 WPF 窗口会抢焦点，机器级互斥锁
   `Global\W2G-InteractiveDesktop` 可能排队最长 30 分钟。
4. **`run-demand-bearing-g3-vectors.ps1` 还要 `-FieldRunRoot`**，指向一次已授权的现场运行的根目录。

---

## 六、待用户裁定的两件新事

1. **车载端那八份 `ONBOARD_HMI_G2` 证据要不要提交？** 该仓 `.gitignore` 把 `evidence/` 当构建
   产物排除，只有一份 G3 证据被强制加过。控制端那八份已提交（那个仓没有这条 ignore）。
   **两端证据一个在库里一个只在盘上，是本轮的不对称处。**
2. **票 16 转交的那条本轮没做**：`FP-IS-02` 重证时应当给控制端的
   `RECONCILE_EMPTY_FINAL_STATE` 补一条独立测试（现在只有 `REJECTED` 分支被
   `FailedCompensationResultIsDurableReplayableAndNeverReleasesDemandOrVehicle` 覆盖）。
   那是改控制端产品测试，不是纯出证，**已经越出「跑两道 G2」这个授权**。
   补完之后 `FP-IS-02` 的 `CONTROL_SERVER_G2` 要重出一份新证据。

---

## 七、两条顺带记下的观察

1. **`8005-agv-control-server/CLAUDE.md` 第 121 行还写着 `global.json` 是 `8.0.424`**，
   `a143c9c` 之后已经是 `8.0.425`。本轮没改（不在授权范围内）。
2. **提交控制端证据时 git 报了 16 条 `CRLF will be replaced by LF`。** 这正是
   [22-answer.md](22-answer.md) 第九节第 2 条记下的那件事：脚本用 `Set-Content` 写出 CRLF，
   而两个仓的 `.gitattributes` 都说 `* text=auto eol=lf`，落库即被规范化。
   **目前没有任何机制对证据文件取哈希，所以不构成问题**；将来若给证据加摘要绑定，这一条会
   立刻变成 bug。
