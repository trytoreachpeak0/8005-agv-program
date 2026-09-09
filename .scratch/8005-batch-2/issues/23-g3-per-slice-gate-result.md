# 23 — G3 的按片出证与分级状态（控制端 `scripts/`）

**做什么：** 让 G3 能按切片出 `gate-result.json`，并把「跑了什么」与「算不算通过」拆成两个
字段。三件事：给三个 G3 runner 加 `-Slice`、按片发 `gate-result.json`、把
`classification` 里那组字面常量改成算出来的。

**为什么现在做：** 它是**票 17 第三条验收的唯一出路**。票 17 要给 `FP-IS-00`～`07` 八个切片各
出一份 G3 的 `gate-result.json`，而三个 runner 把切片结论写成字面常量、且都只发
`run-result.json`——**全仓只有 `test-wire-to-gate.ps1` 发 `gate-result.json`，而它第 4 行是
`[ValidateSet('G2')]`**，在参数层面就拒绝被要求跑 G3。这不是配置问题，是那三个 runner 的既定
立场，详见 [17-answer.md](17-answer.md) 第六节。

用户 2026-09-09 定：**单开一张票**，并**引入分级状态**（不是把 staged G3 直接认成通过，也不是
维持现状）。

## 一、⚠️ 本票最重要的事实：四个 runner 只命名了四片

`FP-IS-NN` 在全部四个 G3 runner 里的出现情况（2026-09-09 实测）：

| runner | 仓 | 命名的片 |
| --- | --- | --- |
| `run-staged-g3.ps1` | 控制端 | `FP-IS-00`、`FP-IS-06` |
| `run-staged-g3-restart.ps1` | 控制端 | `FP-IS-00`、`FP-IS-06` |
| `run-demand-bearing-g3-vectors.ps1` | 控制端 | `FP-IS-04`、`FP-IS-05` |
| `run-staged-g3-recovery-ack-drop.ps1` | 车载端 | `FP-IS-00`、`FP-IS-06` |

**`FP-IS-01`、`FP-IS-02`、`FP-IS-03`、`FP-IS-07` 在任何 G3 runner 里一次都不出现。**

所以「八片各一份 G3 `gate-result.json`」不是一件事，是两件：

- **甲（机械）**：`00`／`04`／`05`／`06` 四片已有断言支撑，把常量换成算出来的即可；
- **乙（需要判断）**：`01`／`02`／`03`／`07` 四片**没有任何 runner 声称覆盖它们**。
  是补新场景，还是如实记「本批次这四片没有 G3 面」，本票要给出结论并写进证据，
  **不许靠把它们塞进某个 runner 的 `officialSlices` 数组来凑齐八份**。

⚠️ **甲那四片的「断言支撑」是读出来的，不是代码里写着的。** 三个 runner 共 19／20／20 条具名
断言，**没有一条挂着切片标识**；切片归属整个存在于 `officialSlices` 那个字面常量里。所以甲的
第一步不是改代码，是**把「哪条断言构成哪一片的 G3 证据」写下来**——它现在只存在于当初写常量
那个人的脑子里。写下来之后守卫才有东西可钉。

## 二、分级状态：拆成两个字段

用户裁定引入分级，**不是给 staged G3 发一个和 G2 一样的 `PASS`**。落法是把现在混在一起的两
件事拆开：

| 字段 | 回答什么 | 取值 |
| --- | --- | --- |
| `status` | 这一片的断言在这次运行里过了没有 | `PASS` / `FAIL` / `INCONCLUSIVE` |
| `assuranceLevel` | 这次运行**实际动了什么** | 见下表 |

`assuranceLevel` 的取值与含义（**这张表是本票要立的东西，逐条写进脚本注释**）：

| 值 | 含义 | 谁产出 |
| --- | --- | --- |
| `STAGED_REBUILD` | 绑 commit，从 exact clone 重新 build/publish，合成对端，**不碰任何候选产物** | `run-staged-g3.ps1`、`run-staged-g3-restart.ps1` |
| `DEMAND_BEARING_RESTORE` | 同上，外加恢复一份已授权现场运行的库 | `run-demand-bearing-g3-vectors.ps1` |
| `CANDIDATE_ARTEFACT` | 跑的是候选发布产物本身 | **今天没有任何 runner 产出它**，留位 |

`formalSlicePass` **不再是字面 `$false`**，改成算出来的：

```
formalSlicePass = ($status -eq 'PASS') -and ($assuranceLevel -in $LevelsThatCountAsSlicePass)
```

`$LevelsThatCountAsSlicePass` 是一个具名常量，**它旁边必须写清用户 2026-09-09 的裁定原文**，
让下一个人看到的是一条决议而不是一个魔数。按本票的裁定，它含 `STAGED_REBUILD` 与
`DEMAND_BEARING_RESTORE`。

⚠️ **2026-09-04 那份 `SUMMARY.md` 里「不构成切片通过」的措辞随之作废，但那份证据不许改**
（证据目录只增不改）。作废的说明写在本票的 `23-answer.md` 与新一轮 G3 的 `SUMMARY.md` 里。

## 三、`gate-result.json` 的形状

对齐控制端 `test-wire-to-gate.ps1` 与车载端 `run-w2g-g2.ps1` 已有的 `1.1.0`，**升到 `1.2.0`**
（加了 `assuranceLevel`、`runKind`、`assertionIds`，纯增量，`1.1.0` 的读者仍能解析）：

- `gate` = `'G3'`（**不是** `G3_STAGED` 这类——runner 的区分放 `runKind`）
- `runKind` = 沿用 `run-result.json` 现有的那个值（如
  `STAGED_G3_REAL_PEERS_DETERMINISTIC_PLAINTEXT`），不新造
- `integrationSliceId`、`vectorIds`（读索引，**不手抄**）、`integrationSliceIndexSha256`
- `status`、`assuranceLevel`、`formalSlicePass`
- `assertionIds` = **这一片认领的那几条具名断言的名字**，以及各自的结果。
  这是第一节末那条「把归属写下来」的落点。
- 与 `run-result.json` 同一套 commit 绑定与协议身份字段

**一次运行发多份 `gate-result.json`**（它认领几片就发几份），不是一份里塞一个数组——票 17 的
验收数的是文件数，且两端 G2 已经是一片一份。目录按
`$EvidenceRoot\<runKind>\FP-IS-NN\gate-result.json` 分，`run-result.json` 仍在
`$EvidenceRoot` 根上，一次运行一份。

## 四、`-Slice` 的语义（与 G2 那两个脚本**不同**，别照抄）

G2 的 `-Slice` 是**过滤器**：改 `dotnet test --filter`，只跑那一片的测试。
**G3 没有可过滤的东西**——它跑的是一个完整的对端联调场景，不是一组可筛选的测试。

所以 G3 的 `-Slice` 是**选择出证范围**，不是选择跑什么：

| | 不带 `-Slice`（现状，保留） | 带 `-Slice FP-IS-NN` |
| --- | --- | --- |
| 实际跑的 | 整个场景 | **完全一样，一个字都不少跑** |
| `run-result.json` | 照发 | 照发 |
| `gate-result.json` | 该 runner 认领的每片各一份 | 只发该片那一份 |
| 该 runner 不认领 `NN` | 不适用 | **建目录前就拒绝**，并报出它认领哪几片 |

⚠️ **不许为了让 `-Slice FP-IS-02` 有输出，就让 runner 少跑一段或多认领一片。**
拒绝是正确行为，票 14 在 G2 那边立的先例（选中 0 条即拒绝，不写 INCONCLUSIVE 证据）同理：
**没有的东西，正确的产物是没有产物。**

## 五、要复用的机件（别重造）

- **`test-wire-to-gate.ps1` 的 `gate-result.json` 写法**：`ConvertTo-Json` ＋
  `Set-Content -Encoding utf8NoBOM`，字段顺序用 `[ordered]@{}`。三个 runner 共用一个函数，
  不要各写一份。
- **`run-staged-g3.ps1` 已有的身份读法**：从 `src/ControlServer.Host/appsettings.json` 的
  `ProtocolCandidate` 读，不硬编码。`$expectedProtocol` 已经在脚本里。
- **切片索引**读克隆出来的协议仓那份（三个 runner 都已经克隆协议仓并比过
  `manifestSha256`），**不是** vendor 那份——vendor 那份是给测试进程用的。
- **`run-demand-bearing-g3-vectors.ps1` 的 `SharedRunnerSource` 机制**：它已经从
  `run-staged-g3.ps1` 读回对端绑定与合成对端夹具，新的共用函数照这条路走，
  不要变成三份互相漂移的副本。

## 六、边界

- **只改 `8005-agv-control-server` 的 `scripts/`，只在 `fp/v2-impl` 上。**
  车载端的 `run-staged-g3-recovery-ack-drop.ps1` 是否同改，**本票不做**，见第八节第 2 条。
- **不动 `src/`、`tests/`、`vendor/`。** 本票不改任何产品代码，也不改任何一条断言。
- **不改三个 runner 现有的任何一条具名断言的判据**——本票只增加「这条断言归哪一片」的
  元信息与出证路径。`run-demand-bearing-g3-vectors.ps1` 那条关于现场库历史的断言照旧失败，
  怎么办是 [17-answer.md](17-answer.md) 第七节第 2 条，**不在本票内**。
- **证据目录只增不改**，`-EvidenceRoot` 必须是不存在的目录，失败的证据也留。
- **不进门禁、不推送。** 本票的自证跑在临时证据目录里；票 17 的正式 G3 重跑要另外点头。
- 新脚本／新函数 PowerShell 7，`#Requires -Version 7`。

## 七、开工前必须知道的三件事

1. **🔴 `$OnboardCommit` 绑 `153b705`，而车载端本地是 `7c4dfe9`（ahead 1，未推）。**
   `run-staged-g3.ps1` 的 `-RemoteRef 'origin/w2g/fp-v2-impl'` 断言远端 tip 等于绑定值。
   **推了 `7c4dfe9` 而不同时改 `$OnboardCommit`，下次跑 G3 会在克隆阶段抛
   `onboard-hmi remote ref mismatch`。要推就两件一起做。**

2. **`run-staged-g3.ps1` 从 GitHub 克隆车载端，但从本地路径克隆控制端。**
   所以本票改控制端脚本不需要推送就能自证；车载端那一侧不是。

3. **`\a` 会被写文件的工具吃成 BEL 字节。** `run-staged-g3.ps1:71` 曾因
   `'src\ControlServer.Host\appsettings.json'` 落盘成 `...Host<0x07>ppsettings.json` 而起手就抛
   （票 14 引入，四天没人发现）。改完用
   `grep -P '[\x00-\x08\x0b\x0c\x0e-\x1f]' scripts/*.ps1` 扫一遍，很便宜。

## 八、验收

**状态：** open —— 2026-09-09 由用户裁定单开，尚未开工。

- [ ] 第二节那两个字段落地：`status` 与 `assuranceLevel` 分开，`assuranceLevel` 的三个取值
      各有注释说明它实际动了什么
- [ ] `formalSlicePass` 由 `$LevelsThatCountAsSlicePass` 算出，该常量旁写明用户
      2026-09-09 的裁定原文
- [ ] `officialSlices` 不再是字面常量，由该 runner 认领的片算出
- [ ] **第一节乙那四片（`01`／`02`／`03`／`07`）有明确结论并写进 `23-answer.md`**——
      补场景，或如实记「本批次无 G3 面」。**没有靠扩 `officialSlices` 数组凑数**
- [ ] 每条具名断言的切片归属写下来了（`assertionIds`），且三个 runner 各自的归属表能被
      一条守卫或一次自证核住
- [ ] 三个 runner 都有 `-Slice`，语义是第四节那张表（**不改变实际跑什么**）
- [ ] `-Slice` 指到该 runner 不认领的片时，**在建目录之前**拒绝并报出它认领哪几片
- [ ] `gate-result.json` `schemaVersion` `1.2.0`，`gate` 为 `G3`，一片一份
- [ ] 不带 `-Slice` 的既有调用形态行为不变（`run-result.json` 逐字段同形）
- [ ] `grep -P '[\x00-\x08\x0b\x0c\x0e-\x1f]' scripts/*.ps1` 无命中
- [ ] `dotnet test` Debug 与 Release 全绿，0 failed 0 skipped（本票不改产品代码，
      这一条是回归）
- [ ] 自证：真改工作树、真跑、看红、从副本还原并核 SHA-256、**还原后刷时间戳**再跑

## 九、本票不决定的（留给票 17 或用户）

1. **G2 的 `gate-result.json` 要不要也补 `assuranceLevel`。** 两端 G2 现在是 `1.1.0`、
   没有这个字段。补了两端才同形，但那要动 `test-wire-to-gate.ps1` 与
   `run-w2g-g2.ps1`（跨两个仓），本票不做。
2. **车载端 `run-staged-g3-recovery-ack-drop.ps1` 同改。** 它也命名 `FP-IS-00`／`FP-IS-06`，
   同病。跨仓且要另开授权，本票不做。
3. **票 17 第三条验收最终认到哪一级。** 本票只提供 `assuranceLevel` 这把尺，
   票 17 写清它认 `STAGED_REBUILD` 还是只认 `CANDIDATE_ARTEFACT`。
