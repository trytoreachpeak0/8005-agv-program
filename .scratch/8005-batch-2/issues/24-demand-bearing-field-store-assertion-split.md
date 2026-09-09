# 24 — 把 demand-bearing G3 那条身份断言里的现场库历史项拆出来

**做什么：** `run-demand-bearing-g3-vectors.ps1` 的 `protocolAndBuildIdentityBoundToTheSharedBinding`
是**七项合取**，其中最后一项问的是被恢复的现场库里记的历史 `protocolCommit`。
用户 2026-09-09 已裁定那一项为**已知豁免**（票 17 第三条的收口路①）。本票把它从合取里拆出来：
**前六项仍然是断言，第七项改成如实记录**，写进 `gate-result.json` 与 `run-result.json`。

**为什么必须拆，而不是笼统豁免整条断言：** 七项里只有第七项与现场库历史有关，
前六项问的是运行中服务端与被测构建的身份——那正是门禁该守的东西。
按名字豁免整条，等于把六项真正的身份检查一起吞掉：将来服务端身份配错、被测构建 commit 对不上，
这条照样 `FAIL`，而豁免会让它看起来仍是「那个已知的现场库问题」。
**豁免要成立，必须先让证据能分辨是哪一项挂了。**

**授权：** 用户 2026-09-09 第四轮明确「先拆再跑」——**改门禁断言 ＋ 随后跑一轮 G3 出证入库**，
两件都在授权内。这是本线第一次获准改门禁断言。

**前置：** ~~票 23（G3 按片出证与分级状态）~~✅。本票是[票 17](17-fp-is-00-07-recertification.md)
第三条验收的收口路径，与票 23 同形：票 23 提供尺子，本票修正尺子上一处量错的刻度。

## 一、⚠️ 开工前先纠正一处指称错误

**上一轮（2026-09-09 第四轮）落地豁免时，把这条断言写成了「六项合取」，并说豁免第六项。
两处都错，源码是七项：**

```powershell
# scripts/run-demand-bearing-g3-vectors.ps1:626-632
$protocolBindingPass = $null -ne $version -and                                              # 1
    $version.protocolCommit -eq $ProtocolCommit -and                                        # 2
    $version.protocolTag -eq 'protocol-v1.0.0' -and                                         # 3
    $null -ne $probeResult -and                                                             # 4
    [string]$probeResult.serverBuildCommit -eq $ControlServerCommit -and                    # 5
    $null -ne $baseline -and                                                                # 6
    [string]$baseline.sessionRecoveryRows[0]['protocolCommit'] -eq $ProtocolCommit          # 7
```

漏掉的是第 6 项 `$null -ne $baseline`——一个非空守卫。写文档时贴的代码块少了这一行，
于是「最后一项」被数成了第六项。**豁免的对象是第 7 项，不是第 6 项。**
第 6 项必须留在断言里：现场库根本没读到，与「读到了、历史对不上」是两回事。

已在票 17、`17-answer.md`、`23-answer.md` 三处更正。**这是本线第七次证实同一条纪律：
文档里的因果断言（包括自己一小时前写的）开工前要回源码核。**

## 二、拆成什么形状

**断言侧**（`$protocolBindingPass`，保留断言名不变）：只留第 1～6 项。
名字 `protocolAndBuildIdentityBoundToTheSharedBinding` 仍然贴切——它现在恰好只说
「运行中服务端与被测构建的身份绑到了共享绑定」。

**记录侧**（新增，**不是断言、不参与 `status` 判定**）：

| 字段 | 内容 |
| --- | --- |
| `fieldStoreProvenance.protocolCommit` | `baseline.sessionRecoveryRows[0]['protocolCommit']`，如实记录 |
| `fieldStoreProvenance.matchesBoundProtocolCommit` | 它与 `$ProtocolCommit` 是否相等，如实记录**布尔值**，不据此判定通过 |
| `fieldStoreProvenance.exemption` | 指向票 17 那条裁定的常量，让读证据的人一眼知道这项为什么不判定 |
| `fieldStoreProvenance.note` | 一句话说清它为什么恒不相等 |

**`matchesBoundProtocolCommit` 必须照实写 `false`，不许省略、不许改名成看起来中性的东西。**
豁免的意思是「不拿它当通过条件」，不是「不说」。

## 三、断言名不增不减，所以归属表不动

拆分只把一个合取项移出 `$protocolBindingPass`，**`$assertions` 里一个名字都没增删**，
所以 `scripts/g3-slice-evidence.ps1` 的 `Get-G3RunnerClaim` 不改，
`Assert-G3ClaimCoversReport` 双向守卫也不会抛。**这是刻意选的最小改动面**：
改门禁断言本身已经够重，不要顺手动那张手写归属表。

## 四、`gate-result.json` 的 schemaVersion 要升

票 23 定在 `1.2.0`。新增一个可选节是 additive，升 `1.3.0`：
`1.2.0` 的读者仍能解析，而能分辨形状的读者知道这一份带着现场库出处。
**只有 demand-bearing runner 传这个节**，另外两个 runner 不碰现场库，它们的 `gate-result.json`
不该凭空长出一个恒为空的字段。

## 五、非空守卫

`Write-G3GateResult` 已有一张「九个身份字段不许为空」的表（票 23 加的，起因是
`protocolReleaseVersion` 拼错字段名带着 `null` 出证）。**新字段照同一条纪律办**：
Context 里给了 `fieldStoreProvenance`，就要求 `protocolCommit` 非空——
空的意思是现场库没读出来，那本身是运行问题，不该写成一份看着完整的证据。

## 六、边界

- **不改另外两个 runner。** 它们不恢复现场库，这条断言与它们无关。
- **不改断言归属表**（见第三节）。
- **不动已入库的证据。**「证据目录只增不改」照旧；`evidence/g3/20260909-v2-identity/`
  是改造前旧形态跑的，留着不动。
- **不重采现场运行。** 重采一次 v2 身份的现场运行才是这条断言真正的解，
  但那要真车真现场，不在本批次。
- **不碰协议仓与车载端。**

## 七、验收

**状态：** in-progress —— 2026-09-09 开票。

- [ ] `$protocolBindingPass` 只含第 1～6 项，第 7 项不再参与它
- [ ] `fieldStoreProvenance` 四个字段写进 `gate-result.json`，`matchesBoundProtocolCommit`
      如实为 `false`
- [ ] `$assertions` 的名字集合与改动前逐字相同（归属表守卫不抛可作旁证）
- [ ] `schemaVersion` = `1.3.0`，且另外两个 runner 出的 `gate-result.json` 里没有该节
- [ ] 非空守卫覆盖新字段，且真验过它会抛
- [ ] 真跑一轮三个 runner 的 G3，证据入库（用户已授权）
- [ ] `FP-IS-04`／`FP-IS-05` 的 `status` 从 `FAIL` 变 `PASS`，
      且 `formalSlicePass=true`、`assuranceLevel=DEMAND_BEARING_RESTORE`
- [ ] 证据 `SUMMARY.md` 里逐字写清豁免范围（豁免第 7 项，不豁免前六项）
- [ ] 自证：真改、真跑、看红、还原，记原样输出

## 八、本票不决定的（留给票 17 或用户）

- **票 17 第三条验收勾不勾。** 本票只让那两片有资格 `PASS`；
  勾上还要看四片无 G3 面那件事，那是票 17 的事。
- **`FP-IS-01`／`02`／`03`／`07` 的 G3 面。** 用户已裁定本批次如实记录、不补场景。
- **重采 v2 现场运行。** 见第六节。
- **推不推四个仓。** 全线未推，由用户定。
