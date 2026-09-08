# 票 04 决议：`CP-0001` 已批准，需求基线切到 `v1.1.0`

Resolved: 2026-09-07
Resolves: `04-approve-cp-0001.md`

## 结论一句话

**用户 2026-09-07 批准 `CP-0001` 的两条修订**（`REQ-0298` 重写、`REQ-0146` 增列五个 `imap`
只读端点），需求基线由 `v1.0.0` 递增为 `v1.1.0`，**票 07 与票 12 的阻塞就此解除**，两张票
从此可以据修订文开工，不再需要按规格 8.8 第 3 条记录偏离。

## 批准记录

| 项 | 值 |
| --- | --- |
| 批准人 | 用户本人（Zhengyu Shao），本会话内明示 |
| 批准日期 | `2026-09-07` |
| 批准范围 | 两条修订**全批**，无保留 |
| 提出时基线 | `v1.0.0`，SHA-256 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba` |
| 新基线 | `v1.1.0`，SHA-256 `5fe4b701a46b5d16818bcbfdd65748a8dcc774efab0583673daa53e08236fb53` |
| content commit | `f2691893f7835a3d8035ba7dba6070e8dbc85b14` |
| 新 tag | `requirements-baseline-v1.1.0`（annotated，指向 content commit） |
| 归档件 | `requirements/change-proposals/CP-0001.md` |

批准前我逐字核对了两条的基线原文，与规格 9.1／9.2 的引用一致：`REQ-0298` 在
`current-requirements-v1.0.0.md:17257`，`REQ-0146` 在 `:8441`。

## 落地位置：`8005-fp` 下新开的 worktree

用户划的禁区里 `repos/8005-agv-program/` 只读。**用户批准了替代路径**：在
`C:\Users\szy\Desktop\8005-fp\8005-agv-program`（分支 `fp/batch-2`）新开该仓的 worktree，
与其余五个 worktree 同构，完全不动 `repos/` 下的工作树。基线更新、提案归档、tag 全在那里
完成，tag 与历史与 `repos/` 下的克隆共享。

**本票据答案是唯一写进 `repos/8005-agv-program/` 的文件**，落在 `.scratch/8005-batch-2/`
下，符合禁区。

## 规格 10.4 六步逐条落地

| 步 | 要求 | 实际 |
| --- | --- | --- |
| 1 | 头部 `Modified` 下逐条列出被修订条目 | ✅ 两行，各注明由 `CP-0001` 哪一修订项承载 |
| 2 | 改三个字段 | ✅ `Current Requirement` 换修订文、`Last Meaning Change In` → `v1.1.0`、`Change Proposal` → `CP-0001`。脚本复核：两条各命中一次，全文恰好 2 处 |
| 3 | 版本号按语义递增 | ✅ 两条都改文义 → minor，`v1.0.0` → `v1.1.0` |
| 4 | 重算 SHA-256，头部保留版本→哈希对照表，旧值不删 | ✅ 对照表在 `requirements/current-baseline.md`（定案 1） |
| 5 | 打新 annotated tag，旧 tag 不动 | ✅ 新 tag 指向 `f2691893`；实测旧 tag 仍指 `b9f32122`，未移动 |
| 6 | 提案归档，状态改已批准并记批准人日期 | ✅ `requirements/change-proposals/CP-0001.md`（该目录本次新建） |

提交拆成两个 commit，与 v1.0.0 当年的形态一致（`b9f32122` freeze content ＋ `130e2fb3`
publish 指针）：

- `f2691893` — 冻结 v1.1.0 内容，归档 `CP-0001`。**tag 指向它。**
- `05ae7a58` — 发布指针，填入 content commit 与对照表。

拆开的理由不是洁癖：指针文件里要写 content commit 的哈希，写在同一个 commit 里就是自指。

## 差异复核：除两条外一字未改

`diff` 全文比对 v1.0.0 blob 与 v1.1.0，**变更 37 行**，全部落在三处：头部版本元数据段、
`REQ-0146` 条目、`REQ-0298` 条目。条目总数复核 **348 条不变**。

`REQ-0298` 的标题行随首句改写（基线的标题规则实测是首 54 字符 ＋ `…`，320 条截断条目全部
符合，28 条短标题不截断）。`REQ-0146` 首句未变，标题行不动。

**两条的 `Verbatim Extract`（来源票据原文）一字未动**——那是来源的历史事实，不随基线修订
改写。所以 `REQ-0146` 条目里现在同时存在 `queryNearestStart、POST …`（修订后的
`Current Requirement`）与 `queryNearestStart 和 POST …`（原始 Verbatim Extract），这是对的，
不是漏改。

## 三处汇编时的自行定案

规格 10.4 没规定这三件事，按「设计细节自行定案」处理，同样记在 `CP-0001.md` 里：

1. **版本→哈希对照表放在 `current-baseline.md`，不放基线文件自身头部。**规格 10.4 第 4 条
   写的是「写进基线头部」，但基线文件的 SHA-256 是它自己的内容哈希，写进自身必然自指。
   `current-baseline.md` 本来就是记 `Baseline SHA-256` 的地方。基线头部改为一行指针。
2. **`Candidate Ledger SHA-256` 与 `Approval Manifest SHA-256` 在 v1.1.0 里记为 `none`。**
   这两个哈希是 v1.0.0 那次逐条批准工件的身份；v1.1.0 走的是变更提案流程，没有对应账本。
   照抄旧值会让人误以为存在一份对应 v1.1.0 的账本。头部另加
   `Change Proposals Applied: CP-0001`，`Version Approval Evidence` 指向 `CP-0001.md`。
3. **`REQ-0146` 的增列插在具名清单尾部**，即 `POST /api/task/v1/order/route/{vehicleKey}`
   之后、「使用 POST 的查询仍按无副作用语义管理」之前，并把原来的「A 和 B」改写为
   「A、B、…… 和 E」以保持中文列举格式。基线正文不使用反引号与加粗（v1.0.0 全文如此），
   规格 9.1／9.2 里的 markdown 强调标记因此在落地时去掉。

## 一个会咬人的实测坑：哈希口径是 git blob，不是工作树文件

**第一次算哈希就对不上。**`sha256sum requirements/baselines/current-requirements-v1.0.0.md`
得到 `ad521d5ba29983861a99f55be4103cad2b624e74e958722136d6283a502cc122`，而基线记录的权威值
是 `5e409953…`。

原因：该仓 `core.autocrlf=true`，而基线文件在 `.gitattributes` 里**没有** `-text` 保护
（有保护的只有 `.scratch/8005-full-product/` 下的证据 TSV 与最终规格，它们正是因为按字节
绑定 SHA-256 才加的）。所以工作树是 CRLF，blob 是 LF，**权威哈希绑定的是 blob**。

```bash
git cat-file blob <tag>:requirements/baselines/current-requirements-<版本>.md | sha256sum
```

v1.1.0 沿用同一口径：生成时从 `git show HEAD:…` 读 LF 内容、按 LF 算哈希、写出时转回工作树
的 CRLF。`git add` 之后从 index 复核 blob 哈希，与记录值一致；打完 tag 再从 tag 复核一次，
两版都对。**这个口径已写进 `current-baseline.md` 的对照表下方**，因为下一个人一定会踩。

这与 workspace `CLAUDE.md` 记的那个教训是同类：`.gitattributes` 的字节规则丢失导致查询文件
摘要对不上。

## 验收清单

- [x] 提案文本按规格 9.1／9.2 的建议修订文归档到 `requirements/change-proposals/`
- [x] 用户批准并留痕，批准记录含批准人与日期
- [x] 基线 `REQ-0298` 与 `REQ-0146` 按批准文本更新，版本号按「改文义 → minor」处置
- [x] 基线头部的版本→哈希对照表更新，旧 tag 不动（实测旧 tag 仍指 `b9f32122`）
- [x] 剖面 TSV 里这两条的 `FullProductCluster` 与 `Batch` 不变——实测两条仍是
      `FP-B0 批次 0 候选（MVP 已覆盖）`／`BATCH-0`，TSV 文件本身零改动
- [x] 批准结果通知到票 07 与票 12，两张票的阻塞解除（见下）

## 对票 07 与票 12 的解除通知

**规格 9.4 的开工禁令解除。**两张票现在可以据 `v1.1.0` 的修订文开工：

- **票 07（RIoT SDK `imap` Facade）**——五个 `imap` 只读端点已进 `REQ-0146` 的具名清单，
  新增 Facade 有需求依据。注意增列的是**五个**，`removedEdgeDetail` 不在其中，不要顺手加。
- **票 12（`RouteGraphSnapshot` 引擎）**——`REQ-0298` 已重写，引擎有需求依据。

**表述随之改变**：批准前的正确写法是「与基线 `REQ-0298` 原文存在一条已知且已记录的偏离，
处置见 `CP-0001`」；**批准后应直接写「符合 `REQ-0298`（v1.1.0）」**，并在引用基线时带上版本
号或哈希，因为同一条 ID 在两个版本里文义不同。

另外提醒票 02（白名单文档）：它要「预留 `CP-0001` 批准后增列五个 `imap` 端点的位置」，现在
批准已完成，但**增列动作仍归票 07**，票 02 只留位置——这一点不因批准而改变。

## 遗留

**规格文档自身没改。**`full-product-scope-and-sequence-specification.md` 第 9 节仍写着
`CP-0001` 状态「待用户批准」，第 1.1 节仍绑定 `v1.0.0` 的哈希。规格是用户 2026-09-04 批准
且按字节绑定 SHA-256（`7690592e…`）的文件，改它就作废那个绑定，属于另一次批准动作，不在
本票范围内。批准的权威记录是 `requirements/change-proposals/CP-0001.md` 与本答案。
