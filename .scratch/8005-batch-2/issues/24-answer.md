# 票 24 决议 —— 把现场库历史那一项从身份断言里拆出来

**日期：** 2026-09-09（第四轮）
**状态：** done —— 拆分已落地（控制端 `b46b072`），三个 G3 runner 真跑并入库（`1f25f6e`）。

| | 改动前 | 改动后 |
| --- | --- | --- |
| `protocolAndBuildIdentityBoundToTheSharedBinding` | 七项合取，含现场库历史 | 六项合取，只问运行中服务端与被测构建 |
| 现场库记的 `protocolCommit` | 第 7 项断言，恒 `false` | `fieldStoreProvenance` 记录节，不参与判定 |
| `run-demand-bearing-g3-vectors.ps1` | `DEMAND_BEARING_SLICE_FAIL`，19／20 | `DEMAND_BEARING_G3_VECTORS_PASS`，**20／20** |
| `FP-IS-04`／`05` | `status=FAIL`，`formalSlicePass=false` | `status=PASS`，`formalSlicePass=true` |

---

## 一、⚠️ 开工第一件事就证伪了本票初稿的一个数

本票初稿（连同 `17-answer.md` 第七节第 2 条、票 17 第三条、README）都把那条断言写成
**六项合取**并说豁免第六项。**回源码核，是七项**——漏掉的是 `$null -ne $baseline`。

**更该记的是这个错误怎么来的。** `17-answer.md` **第五节末尾上一轮就写过**
「该断言是七个合取项不是六个（三个存在性检查 ＋ 四个实质比较）」。
第四轮写第七节时没有回读同一份文档的第五节，凭对交接文档那句「一条关于现场库历史的断言」的
印象重述，把六项写了回去。

**新纪律：动一条断言之前，先 grep 本答复文件里它自己的名字，看这份文档对它已经说过什么。**
「回源码核」这一条本轮是奏效的（正是它救回来的），但它救的是一个**本可以不犯**的错。

顺带，第五节还留了一条本票该引的论据：

> 2026-09-04 那一轮之所以通过这条断言，正是因为当时 `$ProtocolCommit` 本身就是 `1531489e`。
> 换句话说，这条断言从来没有独立地证过什么——它只在「现场库与候选是同一个协议」时成立。

**这是拆分正确性的最强论据**：被拆掉的那一项在协议不变时恒真、在协议变化时恒假，
两种情形下都不携带关于被测构建的信息。

## 二、拆成了什么

`run-demand-bearing-g3-vectors.ps1:626-632`（改动前）→ 断言只留前六项：
`$null -ne $version`、`$version.protocolCommit -eq $ProtocolCommit`、
`$version.protocolTag -eq 'protocol-v1.0.0'`、`$null -ne $probeResult`、
`$probeResult.serverBuildCommit -eq $ControlServerCommit`、`$null -ne $baseline`。

**断言名一个字没改**，所以 `Get-G3RunnerClaim` 那张手写归属表不动，
`Assert-G3ClaimCoversReport` 双向守卫也不会抛——这是刻意选的最小改动面。

第 7 项变成记录节，写进两份 demand-bearing `gate-result.json` 与该 runner 的 `run-result.json`：

```json
"fieldStoreProvenance": {
  "protocolCommit": "1531489e42e328f28bfe0c51ed3f8c56e5ce0279",
  "matchesBoundProtocolCommit": false,
  "exemption": "TICKET_17_KNOWN_EXEMPTION_FIELD_STORE_HISTORY",
  "note": "..."
}
```

`matchesBoundProtocolCommit` **照实写 `false`**。豁免的意思是这条事实不判定切片，
不是证据不再陈述它。`gate-result.json` 升 `schemaVersion 1.3.0`（additive）；
**只有 demand-bearing 传这个节**，另外两个 runner 不碰现场库，它们的证据里不该长出一个恒空的字段
——实测三份 staged／restart 的 `gate-result.json` 里 `fieldStoreProvenance` 确实不出现。

非空守卫按票 23 的先例加在 `Write-G3GateResult` 里：给了这个节就要求 `protocolCommit` 非空。

## 三、自证：八条检查，真看红，真还原

自证脚本从**被测源码**里读事实，不在测试里重抄断言（票 23 那条纪律）：用 AST 找
`$protocolBindingPass` 与 `$fieldStoreProtocolCommit` 的赋值表达式，比对里面有没有
`sessionRecoveryRows`；断言名集合也是从 `$assertions` 字面量里提出来，与归属表对账。

```
PASS  the identity assertion no longer reads the restored store history
PASS  the identity assertion still checks the six things it should
PASS  the restored store history is what got recorded instead
PASS  the runner still reports exactly the assertions the claim table attributes
PASS  protocolAndBuildIdentityBoundToTheSharedBinding is still a reported assertion
PASS  a gate result with provenance carries it, at schemaVersion 1.3.0, and still PASSes
PASS  a gate result without provenance does not grow the section
PASS  an empty provenance protocolCommit is refused (red path)
```

**看红**：把第 7 项临时放回断言，重跑——**只有第一条转红**，其余七条不变，
并且它把整个表达式原样贴了出来（`$protocolBindingPass still reads sessionRecoveryRows: ...`）。
这证明提取器不是恒绿，也证明它出错时说人话。还原后八条复绿。

## 四、真跑：三个 runner 全过

证据 `8005-agv-control-server/evidence/g3/20260909-graded-per-slice/`，提交 `1f25f6e`，79 个文件。

| runner | 运行 ID | 结果 | 断言 |
| --- | --- | --- | --- |
| `run-staged-g3.ps1` | `20260909T101735630Z` | `STAGED_G3_RECOVERY_REPLAY_PASS` | 19 / 19 |
| `run-staged-g3-restart.ps1` | `20260909T102015738Z` | `STAGED_G3_PROCESS_RESTART_PASS` | 20 / 20 |
| `run-demand-bearing-g3-vectors.ps1` | `20260909T101613312Z` | `DEMAND_BEARING_G3_VECTORS_PASS` | 20 / 20 |

六份 `gate-result.json` 全部 `status=PASS` ＋ `formalSlicePass=true`：
`FP-IS-00`／`06` 各两份（staged 与 restart），`FP-IS-04`／`05` 各一份。

**🔴 最要紧的一条：推断变成了实测。** 上一轮说「挂的只可能是现场库那一项」是靠旁证推的
（同脚本别的断言过了、字段名核过）。本轮把第 7 项移出断言之后，
**前六项作为断言全部通过，同时第七项被量出来仍是 `false`**——两件事同时成立，
才真正证明当初挂的就是它。**这不是把 FAIL 改绿，是把一个混在一起的结论拆开各自报数。**

开跑前四条 commit 绑定都核过：车载端 `153b705` = `origin/w2g/fp-v2-impl`、
simulator `fb5f7c5` = `origin/main`、协议 `f6ee75d` = `origin/fp/v2-candidate`；
控制端绑定从 `e3ea250` 移到 `b46b072`（`947b07a`，CLAUDE.md 要求开跑前移绑定），
两者之间 `src/`／`tools/`／`Directory.Packages.props`／`global.json` 逐字节相同。

⚠️ **写绑定时我编了一个 SHA。** 由短 hash `b46b072` 补全后半段写成
`b46b0724a1bd05b41ff5f56dd0debf2f2ee0eb0f`，真实值是 `b46b0727de5aad74e9ffd56709219dd76e75e0b2`。
`git cat-file -t` 当场查出来。**从短 hash 手写完整 SHA 这件事本身就不该做**——
写完必须 `git cat-file` 或 `git rev-parse` 核一遍。runner 会在 checkout 时报错，
但那要到跑了十几分钟以后。

## 五、顺带查出的两件（都不在本票范围，如实记录）

1. **`harnessWorktreeCleanAtStart` 在后两次运行里是 `false`，原因不是代码。**
   三个 runner 连着跑，而它们把证据写进工作树；第一个跑完之后，
   `git status --porcelain` 就报 `?? evidence/g3/20260909-graded-per-slice/`。
   **runner 记录的「工作树干净否」把自己的产物算了进去**，所以连跑时从第二个起必然 `false`。
   三次运行期间没有任何未提交的代码改动。已写进证据 `SUMMARY.md`，脚本本轮不改。

2. **`evidenceFiles` 的 SHA-256 与库里的 blob 对不上，这批也一样。**
   已知问题（`17-answer.md` 第八节第 2 条，用户裁定不动）：表对盘上的 CRLF 字节算，
   `.gitattributes` 落库时规范成 LF。**如实带着这个问题入库**，并在 `SUMMARY.md` 里
   写明「要核摘要请对签出的文件核，不要对 blob 核」。

## 六、本票没做的

- **没改另外两个 runner**，它们不恢复现场库。
- **没动那张断言归属表**（断言名没有增删改）。
- **没重采 v2 现场运行**——那才是这条断言真正的解，要真车真现场，不在本批次。
- **没动已入库的旧证据**，包括上一轮那次 `DEMAND_BEARING_SLICE_FAIL`。
- **没碰协议仓与车载端**，一个字节都没动。
- **四个仓全部未推。**

## 七、对票 17 的影响

票 17 第三条验收的两个收口条件本轮都满足了：豁免由用户裁定（路①），
正式证据由本轮三次运行产出并入库。该条已勾上，**票 17 全部验收随之勾满**。

**但要清楚它勾的是什么**，这些都写在票 17 那一条与证据 `SUMMARY.md` 里：

- 四片有 G3 面且 `formalSlicePass=true`；**四片本批次没有 G3 面**，记在
  `slicesWithoutSurfaceThisBatch`，不发证据；
- `FP-IS-04`／`05` 通过的前提是那条现场库历史被裁定豁免；
- `assuranceLevel` 到 `DEMAND_BEARING_RESTORE` 为止，**`CANDIDATE_ARTEFACT` 至今无人占据**；
- 八份 `ONBOARD_HMI_G2` 的 `g1Status` 仍是 `SKIPPED`（用户裁定不重出）；
- `fullG3` 与 `releaseCandidate` 在三份 `run-result.json` 里都仍是 `INCONCLUSIVE`。
