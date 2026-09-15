# 生成器分叉台账

`tools/generate-protocol-candidate.mjs` 是协议仓整棵树的唯一机械来源，但它与
`8005-agv-protocol` 的实际内容已经分叉。**直接重跑生成器会静默回退协议仓里的手工修复。**
这份台账把每一处差异归类，让重跑变成一件可以安全做的事。

归类只有三类，没有第四类：

- **回灌** —— 协议仓的内容是对的，生成器要学会写出它。指派到具体票据。
- **覆盖** —— 生成器写出的是权威，协议仓的现状被覆盖即可。
- **手工步骤** —— 不该由生成器产出，生成之后另有动作。逐条列出，见第 4 节。

---

## 1. 比对方法（可复现）

控制端没有 Node，生成在 `vm01` 上跑：

```bash
# 生成器与 tools/templates/ 送到 vm01，跑一次，取回输出
ssh vm01 'pwsh -NoProfile -Command "Set-Location C:\fp-gen\base; node tools\generate-protocol-candidate.mjs out"'
# 协议仓 HEAD 展开成干净树
git archive HEAD | tar -x -C <repo-tree>
diff -rq <repo-tree> <generator-out>
```

| 项 | 值 |
| --- | --- |
| 比对日期 | 2026-09-04 |
| 生成器输出 | **1504** 个文件 |
| 协议仓 `fp/v2-candidate` HEAD（`e54e988`） | **1517** 个文件 |
| 逐字节相同 | **1493** 个 |
| 差异条目 | **22** 条（下表逐条归类，无遗漏） |

1504 与 1493 两个数字与票 09 在 `vm01` 上的实测一致。协议仓从 1516 变成 1517 是
`7b41f75` 同时新增了 `.github/workflows/g1.yml`。

---

## 2. 只在协议仓、生成器不产（14 个文件）

| # | 路径 | 归类 | 理由与去向 |
| --- | --- | --- | --- |
| 1 | `.gitattributes` | 手工步骤 | 仓库元文件。`* text=auto eol=lf` 决定每个协议文件的字节形态，因此**进** content manifest，但它不是协议内容，生成器不该产 |
| 2 | `.gitignore` | 手工步骤 | 同上 |
| 3 | `README.md` | 手工步骤 | 仓库门面，与 `docs/README.md` 是两份东西，后者才是生成物 |
| 4 | `THIRD-PARTY-NOTICES.md` | 手工步骤 | 依赖许可声明，随 `pnpm` 依赖变化而非随协议变化 |
| 5 | `CLAUDE.md` | 手工步骤 | agent 指令文件。**进** content manifest（见第 5 节 `b9dc224`） |
| 6 | `.github/workflows/g1.yml` | 手工步骤 | CI 配置，不随协议发布分发，**不进** content manifest（见第 5 节 `7b41f75`） |
| 7 | `pnpm-lock.yaml` | 手工步骤 | `pnpm install` 产物 |
| 8 | `evidence/g1-result.json` | 手工步骤 | `pnpm g1` 产物，manifest 排除 |
| 9 | `attestations/release-approval.template.json` | **回灌 → #6** | 治理面。它是 `approvals/release-approval.json` 的替代物，生成器要写出这个空模板并停止写出旧的那个 |
| 10 | `schemas/governance/content-manifest.schema.json` | **回灌 → #6** | 票 #6 明写 |
| 11 | `schemas/governance/integration-slice-index.schema.json` | **回灌 → #6** | 票 #6 明写 |
| 12 | `schemas/governance/release-approval-attestation.schema.json` | **回灌 → #6** | 票 #6 明写 |
| 13 | `vectors/CV-DEMAND-ACCEPT-TO-PICKUP/input.ndjson` | **回灌 → #6** | 票 #6 明写；向量集合本身由 #9 扩到 31 条 |
| 14 | `vectors/CV-DEMAND-ACCEPT-TO-PICKUP/expected.json` | **回灌 → #6** | 同上 |

第 9～14 项正是票 09 实测「1504 vs 1516」那 12 个文件差额的来源（另两个是本节第 5、6 项）。
**不补的话，重跑生成器会把它们抹掉。**

---

## 3. 只在生成器输出（1 个文件）

| # | 路径 | 归类 | 理由与去向 |
| --- | --- | --- | --- |
| 15 | `approvals/release-approval.json` | **回灌 → #6** | 「停止写出」这件事本身要回灌。候选不该自带空批准记录——批准是外部 attestation，由两名产品负责人在 GitHub Release Asset 上做。门禁里读它的那条检查同时删 |

---

## 4. 两边都有、内容不同（8 个文件 ＋ 2 个模板）

| # | 路径 | 归类 | 差异与去向 |
| --- | --- | --- | --- |
| 16 | `package.json` | **覆盖** | `version` 0.1.0 vs 0.1.1。生成器已改为引用 `candidateVersion`，#4 把常量升到 `1.0.0` 后自然正确；中间的 0.1.1 不需要保留 |
| 17 | `compatibility/report.json` | **回灌 → #4** | 协议仓多出 `baseRelease`／`wireCompatibility`／`changeSummary` 三个字段，`status` 与 `classification` 也改过。字段结构要回灌，取值由 #4 按 v2 重定（v2 是新 major，`INITIAL_CANDIDATE_NO_BASE_RELEASE` 不再成立） |
| 18 | `compatibility/implementation-version-matrix.json` | **回灌 → #4** | 协议仓 `pinnedPackages` 多一条 `xunit.runner.visualstudio 3.1.5`。与工具链基线 ADR 一致，生成器漏了 |
| 19 | `docs/README.md` | **回灌 → #6** | 协议仓改写为「approval-neutral content snapshot」，并把 `pnpm manifest:finalize` 写进步骤 |
| 20 | `docs/release-governance.md` | **回灌 → #6** | 协议仓多出六条：content snapshot 定义、attestation 外置、G1 双产物校验、attestation 不含自身哈希、发布顺序、补丁发布的适用条件 |
| 21 | `docs/candidate-limitations.md` | **回灌 → #6** | 协议仓已把「manifest／approval 循环依赖」从未解决改写为已解决 |
| 22 | `integration-slices/index.json` | **回灌 → #9** | `schemaVersion` 1.0.0 vs 1.1.0；`W2G-IS-01` 的 `vectorIds` 改为单条 `CV-DEMAND-ACCEPT-TO-PICKUP`；新增 `definition` 块。#9 把家族整体换成 `FP-IS-00`～`15` 并让 `definition` 全部必填，这一处一并落地 |
| 23 | `manifest/release.json` | 手工步骤 | 生成器写的是种子（`CANDIDATE_UNFINALIZED`，只有 `messages` 与 `denylistedMessageTypes`），协议仓里的是 `pnpm manifest:finalize` 跑完的结果（`CONTENT_SNAPSHOT` ＋ 六个哈希 ＋ `files` 表）。**这是设计如此**，不是分叉 |
| 24 | `tools/finalize-manifest.mjs` | **回灌 → #6** | 见 4.1 |
| 25 | `tools/g1-validate.mjs` | **回灌 → #6 与 #7** | 见 4.2 |

### 4.1 `tools/finalize-manifest.mjs` 的四处增量

| 增量 | 去向 |
| --- | --- |
| 排除列表新增 `attestations/` 与 `.github/` | **#6**（`.github/` 那半来自 `7b41f75`，见第 5 节） |
| `status` `CANDIDATE_UNAPPROVED` → `CONTENT_SNAPSHOT` | **#6** |
| 删掉 `approvalStatus:"PENDING"` 字段 | **#6** |
| `releaseVersion` 与 `generatedAt` 的取值 | **#4**（`releaseVersion` 现已是 `__CANDIDATE_VERSION__` 占位符） |

### 4.2 `tools/g1-validate.mjs` 的十一处增量

协议仓版本 29 行，生成器写出 25 行。差的不是四行，是十一处检查：

| # | 增量 | 去向 |
| --- | --- | --- |
| 1 | invalid 样例按目录名取 validator，新增 `x-sorted` 语义规则处理 | #6 |
| 2 | manifest 断言改 `CONTENT_SNAPSHOT`、要求 `approvalStatus` 不存在、消息名严格相等 | #6 |
| 3 | 新增 governance `content-manifest` schema 校验 | #6 |
| 4 | 新增 manifest／`package.json` 版本一致断言 | #6 |
| 5 | 排除列表新增 `attestations/` 与 `.github/` | #6（`7b41f75`） |
| 6 | `requiredVectors` 新增 `CV-DEMAND-ACCEPT-TO-PICKUP`；新增 vectorId 一致、步骤连续、消息序列一致三项 | #6，向量集合本身由 #9 扩到 31 |
| 7 | 新增 governance `integration-slice-index` schema 校验 | #6 |
| 8 | `W2G-IS-01` 专项断言（`vectorIds`、`requiredOutcomes`、`demandRepresentation` 四项） | 回灌 #6，修改 #9（`definition` 改 `authorityModel` 后这一段要重写） |
| 9 | `CV-DEMAND-ACCEPT-TO-PICKUP` 的 `productAssertions` 与 adapter 轨迹断言 | 回灌 #6，修改 #9（`productAssertions` 由特例推广为全量必填） |
| 10 | **`worklistItems.maxItems === 1` 与 `UpcomingStopPlanSnapshot.demandId` 必须支持 null** | 回灌 #6，修改 **#7**（票 #7 明写要改的两处 v1 形状硬编码） |
| 11 | 批准检查从 `approvals/release-approval.json` 空批准，改为 `attestations/` 模板 ＋ `PROTOCOL_APPROVAL_ATTESTATION` 环境变量 ＋ attestation schema ＋ 两名不同 owner；结果里多三个 `approvalAttestation*` 字段 | #6 |

**回灌与修改是两件事，都在这张表里。**#6 把模板整体对齐到协议仓 HEAD——十一处全部回灌，
包括 #7 与 #9 后续要改的那几处；#7 与 #9 再在真实文件上做行级修改。**顺序约束因此是硬的：
#6 必须在 #7 之前。**第 10 项那两处断言只存在于协议仓版本里，回灌之前 #7 无处可改。批次 1
的既定顺序（#3 → #4／#5／#6 → #7／#8 → #9）已经满足这一条。

---

## 5. 两个 G1 修复的处置

票据要求这两个不得默认丢弃。逐条：

### `b9dc224`「manifest 收录 `CLAUDE.md`」→ 登记为手工步骤

`CLAUDE.md` 是仓库元文件，生成器不该产它（本台账第 5 项）。修复的实质是「`CLAUDE.md`
在树里，因此 content manifest 要收录它」，而 manifest 由 `pnpm manifest:finalize` 在生成之后
扫真实文件树重算。**只要放回仓库元文件之后再跑 finalize，这个修复自动成立**，不需要写进
生成器。第 6 节的手工步骤顺序保证了这一点。

### `7b41f75`「G1 与 manifest 一致排除 `.github/`」→ 回灌，指派 #6

这是两份排除列表的代码改动，生成器不知道，重跑必然回退。回灌到
`tools/templates/g1-validate.mjs` 与 `tools/templates/finalize-manifest.mjs`。

**那个 commit 留下的约束一并抄在这里**：两份排除列表是逐字相同的复制品，
**改一个必须同时改另一个**。只改 `g1-validate` 的结果是 finalize 生成 N+1 条、g1 按 N 条
校验，门禁直接红。模板外提之后这两份列表是可读的行级文本，但它们仍然是两份。

---

## 6. 生成后的手工步骤（逐条，不留「暂未分类」）

重跑生成器之后，按顺序补齐这些，缺一项 G1 就红：

1. **放回七个仓库元文件**：`.gitattributes`、`.gitignore`、`README.md`、
   `THIRD-PARTY-NOTICES.md`、`CLAUDE.md`、`.github/workflows/g1.yml`、`pnpm-lock.yaml`。
   生成器只写它产出的那棵树，不删也不碰这些。
2. **`pnpm install --frozen-lockfile`** —— `pnpm-lock.yaml` 已在上一步就位。
3. **`pnpm manifest:finalize`** —— 把种子 manifest 换成 content snapshot。必须在第 1 步之后，
   否则文件表少七条。
4. **`pnpm g1`** —— 产出 `evidence/g1-result.json`。

第 1 步的七个文件里，六个进 content manifest，只有 `.github/workflows/g1.yml` 不进——
这正是 `7b41f75` 定的边界。

---

## 7. 消化进度

| 票 | 消化的条目 | 状态 |
| --- | --- | --- |
| #3 基座 | 无（**不做任何回灌**：改造前后输出逐字节相同，1504 个文件全等） | 完成 |
| #4 身份 | 16、17、18 | 完成 |
| #5 类型层 | 无（不碰本表任何条目） | 完成 |
| #6 治理面 | 9～15、19～21、24、25 | 完成 |
| #7 payload | 25 的第 10 项（在 #6 回灌后的真实文件上改） | 完成 |
| #8 新增消息 | 无（只在消息定义区末尾追加） | 完成 |
| #9 向量与切片 | 22、25 的第 8／9 项 | 完成 |
| 手工步骤 | 1～8、23 | 每次重跑生成器后执行第 6 节 |

**表里没有剩余的未指派条目，批次 1 的七张票已全部消化完它们各自的份额。**

批次 1 做完后的实测：生成器产出 **1754** 个文件，63 条消息、45 条错误码、31 条向量、
16 个切片。门禁不再自带向量清单、切片数与 id 前缀——三者由生成器注入，那是本表里
「回灌」之外顺带消掉的三处重复真相。

#6 之后的实测：生成器产出 **1507** 个文件（1504 − 3 ＋ 6），`runner/` 与 `approvals/` 不再
产出，`schemas/governance/` 三个、`attestations/release-approval.template.json` 与
`vectors/CV-DEMAND-ACCEPT-TO-PICKUP/` 两个已由生成器机械产出。三个 governance schema 与
协议仓 HEAD 做过结构化深比较：两个语义完全相同（只有排版差异，生成器统一用
`JSON.stringify(value, null, 2)`），`content-manifest.schema.json` 的唯一差异是**有意删掉的**
`runnerContractsSha256`（`properties` 与 `required` 各一处）。attestation 模板与那个向量的两个
文件与 HEAD **逐字节相同**。

---

## 8. 批次 5 起点复核与跨线差异

批次 5 的协议侧生成器票（program#89～#95）都默认「生成器就是 `protocol-v1.0.0` 的机械来源」。
第 7 节之后生成器又和协议候选同步过两次——`a9d7a405`（对齐协议仓 `16e2567`，单人签名）与
`8a5dfd7d`（对齐 `9f22db8`，AI 可经授权批准）——两次提交各自在正文里声明了「1762 个文件逐字节
相同」，但本台账没有记。本节把那句声明换成实测，并把协议仓两条线之间的账算清。

### 8.1 起点复核（program#89）

| 项 | 值 |
| --- | --- |
| 复核日期 | 2026-09-15 |
| 机器 | 控制端 `LAB-WIN-01`，Windows 11 Pro 10.0.26200，node v24.20.0，pnpm 11.25.0 |
| 生成器 | `fp/b5-protocol` 的分出点 `c5eda22f`（创建该分支时的 `origin/main`）。生成器 blob `8b976a33`，`templates/g1-validate.mjs` `7b5502ea`，`templates/finalize-manifest.mjs` `4eaef0e4`；自 `8a5dfd7d` 起未改 |
| 对照 | 协议仓 `9f22db8`（`protocol-v1.0.0`，注释 tag `05b267f`；`origin/fp/v2-candidate` 顶端，之后无未发布提交），1762 个跟踪文件 |
| 生成器输出 | **1754** 个文件 |
| 放回七个元文件、finalize、G1 之后 | **1762** 个文件（`node_modules/` 不计） |
| 逐字节相同／不同／缺失／多余 | **1762／0／0／0** |
| `pnpm g1` | **PASS**，failures 为空；manifest `a0e1deedb50419057dbe6aa7a7e8df983fb9ea901bbc452f97020ebf4743ef23`，与 `9f22db8` 的 `manifest/release.json` 相同 |
| `--verify-determinism` | 1754 个文件，**0 divergent** |

**结论：没有差异需要归类，前提成立。**program#96（批次5-21）落地前不需要先处理任何复核差异。

做法与第 6 节相同，只多了比对与留证：

1. 生成器写到空临时目录，这一份原样保留，作为「finalize 之前的输出」。
2. 复制一份，`git archive 9f22db8 -- <七个元文件>` 展开进去，展开后逐个核对 blob id 与 `9f22db8` 一致。
3. `pnpm install --frozen-lockfile`、`pnpm manifest:finalize`、`pnpm g1`。
4. 候选树每个文件（`node_modules/` 除外）算 git blob id，与 `git ls-tree -r 9f22db8` 逐条比对。这与和
   `git archive 9f22db8` 展开的树逐字节比对等价，且不受控制端 `core.autocrlf=true` 影响。
5. `node generate-protocol-candidate.mjs --verify-determinism`。

两个坑，重跑时别再踩：

- **`git hash-object` 打不开临时目录里的长路径负例**（`Filename too long`，超过 MAX_PATH），blob id
  要在进程内按 `sha1("blob <字节数>\0" + 内容)` 自己算。
- **program 仓的生成器 `.mjs` 没有 `eol=lf` 属性**（只有 `tools/templates/*.mjs` 有），控制端检出是 CRLF。
  这不影响输出——生成器读模板、写文本时都把 `\r\n` 换成 `\n`——但记录生成器身份时要取经过 clean
  filter 的 blob id（`git hash-object <文件>`，不带 `--no-filters`），否则记下的是 CRLF 字节的哈希。

### 8.2 跨线差异：协议仓 `main` 独有的 8 个提交

协议仓 `main`（MVP 线）与 v2 线的 merge-base 是 `e54e988`，`protocol-v0.3.0` 与 `protocol-v1.0.0`
互不为祖先。`main` 独有的 8 个提交从未进入生成器。逐条对照提交内容与 `9f22db8` 实读：

| `main` 独有提交 | 内容 | `9f22db8` 现状 | 处置 |
| --- | --- | --- | --- |
| `db064d2` | `CV-LOAD-CANCELLATION-BEFORE-LOAD`，两步：`LoadCancellationStartRequested` → `LoadCancellationAuthorization`，授权即终结 | 31 条向量里没有 | program#93（批次5-05）按 ADR-cross-0046 以四步形态重做：取消请求 → 授权 → 空 `slotResults` 的 `ALL_EMPTY` 结果 → `DurableAck`（规格第 19.4 节）。**不照搬** |
| `952b49c` | 0.2.0 解除单单收窄：`items` 上限 8、`legs` 上限 10、`legType` 加 `TO_CHARGER`、`expectedSublots` 数组、`slotResults` `minItems: 0` | `CurrentStopWorklistSnapshot.items` `maxItems: 8`；`legs` `maxItems: 9`、`sequence` 上限 9；充电停靠由腿上的 `stopPurposeCategory`（`BUSINESS`／`WAITING_POINT`／`CHARGER`）表达；`SublotEntryRequested.expectedSublot` 仍是单值；`LoadCancellationResult.slotResults` 仍是 `minItems: 1` | 上限与充电停靠：v1.0.0 已以 v2 形态具备，不移植。`expectedSublots` 归 program#92（批次5-04）；`slotResults` `minItems: 0` 归 program#93（批次5-05）。同一提交里 `CLAUDE.md`、`README.md` 的改动是元文件；`compatibility/report.json`、`docs/candidate-limitations.md` 是 MVP 线 0.2.0 的叙述，v2 的对应内容由生成器写出，归 program#90（批次5-02） |
| `dff1686` | 发布批准改为单人签名 | attestation schema 在 APPROVED 时 `approvals` `minItems`／`maxItems` 为 1；G1 为 `size===1` | 已由协议仓 `16e2567` 与生成器 `a9d7a405` 移植（`8a5dfd7d` 另加 `approverKind`／`authorizedBy`） |
| `b31a47a` | 取消推送后的通知义务（`CLAUDE.md`） | `9f22db8:CLAUDE.md` 仍写着每次推送后开 issue @`SocialKKKK` | 元文件，生成器不产（第 2 节第 5 项）。由 program#96（批次5-21）放回元文件时改写 |
| `dbae7b9` | 三条恢复消息加 `slotOperationAttemptId`；注册表加 `OPERATOR_TIMEOUT`；G1 新增「注册表 `codes` 顺序与 `ErrorCode` enum 一致」检查 | 三条消息都没有该字段；注册表 54 条，没有 `OPERATOR_TIMEOUT` | 字段归 program#95（批次5-07）；码归 program#91（批次5-03）。**一致性检查不移植**：生成器里 `errorCodeNames = errorCodes.map((item) => item.code)`，`errors/error-codes.json` 的 `codes` 与 `ErrorCode` enum 由同一个 `requiredErrorCodes` 列表派生，结构上不会分叉。MVP 线需要这条检查，是因为那边两处靠手工同步 |
| `345c53c` | `CurrentStopWorklistSnapshot.stationDepartureDeadlineAt` | payload 只有 `stationId`、`worklistRevision`、`operationSessionId`、`items` | program#91（批次5-03） |
| `fbdc94d` | 仓内候选 G1 记录跟上 0.3.0 | — | 不移植：`evidence/` 在 finalize 与 G1 的排除列表里，不进 manifest；v2 的 `evidence/g1-result.json` 由 `pnpm g1` 重新产出 |
| `850ca4c` | SDK 矩阵 8.0.425／8.0.31，G1 不再硬编码 | 矩阵仍是 8.0.424／8.0.30，G1 断言同一对字面量 | **本票移植**，见 8.3 |

八行里没有「暂未分类」：六行指派到票或已移植，两行（`fbdc94d` 与 `dbae7b9` 的一致性检查）写明不移植的理由。

### 8.3 移植 `850ca4c`

`850ca4c` 修的是「两份基线一起过期、一起绿」：ADR-cross-0056 在 2026-09-09 把 SDK 基线抬到 8.0.425，
矩阵还停在 8.0.424／8.0.30，而 G1 断言的正是脚本里硬编码的同一对值。生成器与 G1 模板带着同一个毛病，
这里照 `850ca4c` 改两处，取值以 `850ca4c` 为准：

- 生成器写 `compatibility/implementation-version-matrix.json` 的那段：`dotnetSdk` 8.0.425、`dotnetRuntime`
  8.0.31、`requiredAction` 同步。`pinnedPackages` 里 EF Core Sqlite 的 8.0.30 是包版本，不动。
- `tools/templates/g1-validate.mjs`：矩阵检查换成 `850ca4c` 的原句，只要求两者是精确版本号。与真实
  工具链的比对归工作区根的 `check-toolchain.ps1`。

两处必须一起改。分两步做时实测如下（每列都是一次完整的生成、放回元文件、finalize、G1）：

| 检查 | 移植前 `c5eda22f` | 只改矩阵 | 两处都改 |
| --- | --- | --- | --- |
| 生成的矩阵三项等于 `850ca4c` | ✗ | ✓ | ✓ |
| G1 的矩阵检查语句等于 `850ca4c` | ✗ | ✗ | ✓ |
| `pnpm g1` PASS | ✓（两份一起过期） | ✗ `version matrix mismatch` | ✓ |
| 把 `dotnetRuntime` 改成 `8.0` 时 G1 以 `850ca4c` 的报错拒绝 | ✗ | ✗ | ✓ |

两处都改之后：

| 项 | 值 |
| --- | --- |
| finalize 之前的生成输出，移植前后比 | 1754 个文件，1752 相同；**只有 `compatibility/implementation-version-matrix.json` 与 `tools/g1-validate.mjs` 不同**，无增删 |
| 生成的矩阵 | blob `4598e66`，与协议仓 `850ca4c` 的同名文件逐字节相同 |
| `tools/g1-validate.mjs` 相对 `9f22db8` | 只改矩阵检查所在的一行 |
| `pnpm g1` | **PASS**，failures 为空；manifest `4a0625e803ef39e2279279d3a0d5695fb6fc10c80b0b124b116e53a0f9982ba7` |
| 与 `9f22db8` 比 | 1758 相同、4 不同、0 缺失、0 多余。不同的是上面两个文件，以及随之变化的 `manifest/release.json`、`evidence/g1-result.json` |
| manifest 分哈希 | 只有 `fileTableSha256` 变（文件表恰两条变化）；`schemaBundleSha256`、`examplesSha256`、`vectorsSha256`、`errorRegistrySha256` 不变 |
| `--verify-determinism` | 1754 个文件，**0 divergent** |

没有写协议仓，没有改任何 schema、向量、错误码、切片或身份常量。协议仓的这两处变化由 program#96
（批次5-21）随 v2.0.0 候选包一并落地。
