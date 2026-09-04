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
| 8 | `W2G-IS-01` 专项断言（`vectorIds`、`requiredOutcomes`、`demandRepresentation` 四项） | #9（`definition` 改 `authorityModel` 后这一段要重写） |
| 9 | `CV-DEMAND-ACCEPT-TO-PICKUP` 的 `productAssertions` 与 adapter 轨迹断言 | #9（`productAssertions` 由特例推广为全量必填） |
| 10 | **`worklistItems.maxItems === 1` 与 `UpcomingStopPlanSnapshot.demandId` 必须支持 null** | **#7**（票 #7 明写要改的两处 v1 形状硬编码） |
| 11 | 批准检查从 `approvals/release-approval.json` 空批准，改为 `attestations/` 模板 ＋ `PROTOCOL_APPROVAL_ATTESTATION` 环境变量 ＋ attestation schema ＋ 两名不同 owner；结果里多三个 `approvalAttestation*` 字段 | #6 |

**这里有一条顺序约束，不是建议：#6 必须在 #7 之前完成。**第 10 项那两处断言只存在于协议仓
版本里，生成器当前写出的版本没有它们——#6 回灌之前，#7 无处可改。批次 1 的既定顺序
（#3 → #4／#5／#6 → #7／#8 → #9）已经满足这一条。

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

## 7. 本次基座改造对本台账的影响

票 #3 只做基座，**不做任何回灌**：改造前后生成器输出逐字节相同（1504 个文件全等），
`--verify-determinism` 双跑 0 差异。所以上表第 9～14、15、17～22、24、25 项在票 #3 完成时
仍然全部有效，由指派到的票据逐张消化。
