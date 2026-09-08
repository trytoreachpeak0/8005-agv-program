# 批次 1 出口核实（2026-09-08）

批次 2 轨 A 的票 14／15／16／17 都以「批次 1 完成」为前置，而批次 1 是**无条目载体**的工程
（规格 3.2），没有票据、没有决议文档，出口状态此前只能靠 commit message 转述。本文把规格
8.3 的四条出口逐条核实一遍，作为轨 A 开工的依据。

**放在 `.scratch/8005-batch-2/` 而不是新开 `.scratch/8005-batch-1/`**：它服务的是批次 2 轨 A
的开工判定，不是批次 1 自己的交付物。若需要独立的批次 1 收口档，本文可整体搬过去。

## 结论：四条出口全绿

> **更正（2026-09-08 下午）。**本文首版把出口 2 判为「未达成，记为缺口」，理由是「升级后的
> 生成器只在 `vm01`，从未回到任何仓库」。**那个判断是错的。**错因是只 `find` 了磁盘上的工作树，
> 没有查其它分支——生成器早在 2026-09-04 就提交在 `fp/generator-v2` 上并推送到 origin（八个
> 提交），分叉台账在同一条分支。真实缺口不是「没回来」，是「**没合进 `main`**」。已合并，
> 并补做了两条独立验证。

| # | 出口（规格 8.3） | 结论 |
| --- | --- | --- |
| 1 | G1 通过（候选态，用 tracked 空白模板） | ✅ **绿，CI 实证** |
| 2 | 生成器可重跑且输出确定（同输入两次逐字节相同） | ✅ **绿，vm01 实证**（本文首版误判为缺口，当天更正） |
| 3 | 两条 `reasonCode ∈ 注册表` 架构测试绿 | ✅ **绿，两端各自实跑** |
| 4 | `runner/` 两个 schema 已删且 manifest 哈希随之更新 | ✅ **绿** |

轨 A 的票 14／15／16 本来就不依赖生成器（它们读的是协议仓里已有的 v2 内容）。四条出口
现已全绿，**批次 1 完整收口**。

---

## 出口 1 —— G1 通过

**这是 G1 第一次在 `fp/v2-candidate` 上真正执行。**此前所有 g1 运行都在 `main`
（`g1.yml` 的 push 触发是 `branches: [main]`），这条分支上一次都没跑过；而仓内
`evidence/g1-result.json` 的 `checkedAt` 是 `tools/g1-validate.mjs` 里的**硬编码常量**
（`"2026-09-04T00:00:00Z"`），它证明不了执行发生过，只能证明内容自洽。

本机也无法验证：`g1.yml` 的注释逐字写着 *the control machine has no Node installed*，实测确认
本机没有 node／pnpm，协议仓也没有 `node_modules`。**`pnpm g1` 在这台机器上跑不了。**

**做法**：`gh workflow run g1.yml --ref fp/v2-candidate`（`g1.yml` 声明了 `workflow_dispatch`）。

run [34212719223](https://github.com/trytoreachpeak0/8005-agv-protocol/actions/runs/34212719223)，
node v24.20.0，2026-09-08T09:56:33Z：

```json
{
  "gate": "G1", "status": "PASS",
  "candidateManifestSha256": "84f984eabf17106e92666c415b63100d404e9ec69a9a710dfddf17683cc42788",
  "approvalAttestationStatus": "PENDING", "approvalAttestationSource": "TRACKED_TEMPLATE",
  "schemaCount": 69, "messageTypeCount": 63, "validExampleCount": 63,
  "invalidExampleCount": 1548, "trajectoryCount": 31, "integrationSliceCount": 16,
  "failures": []
}
```

**与仓内 `evidence/g1-result.json` 逐字段一致**，manifest 哈希也对上。所以那份提交的证据本来
就是准的，只是此前无从独立验证。

顺带记下：`main` 上 2026-09-08 09:20 那次 g1 是 failure，但原因是 runner 连不上 github.com
（`Failed to connect to github.com:443`，三次重试全挂），**不是门禁红**。这台 runner 到 github
的网络当天不稳，重跑前先看是不是这个。

## 出口 2 —— 生成器可重跑且输出确定：**绿**

### 载体在哪

`.scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.mjs`，**原位升级**，
正是规格 3.2 写的那个路径。1136 行（v0.1.1 那版 595 行），顶层常量已切到 v2：

```js
const BASE_ID          = "https://schemas.8005-agv.local/agv-full-product/v2";
const candidateVersion = "1.0.0";
const profileId        = "AGV_FULL_PRODUCT";
const protocolVersion  = 2;
```

同批还有 `tools/templates/{g1-validate,finalize-manifest}.mjs` 与
`evidence/generator-divergence-ledger.md`（**分叉台账**，185 行，第 6 节即生成后手工步骤）。

来自 `fp/generator-v2` 的八个提交，2026-09-04 已推送到 origin，本次合并进 `main`：

```
a389222b  生成器变成能安全重跑的工具
3ec8de21  候选身份从 v1 换到 v2
5e59a3f5  类型层四个新 $defs 与错误码 43 → 45
56562796  删 runner/ 与 approvals 写出，治理面纳入生成器
a0fe0803  五条消息的 payload 变更
67b496e2  九条新增消息，消息面 54 → 63
9cbd32b8  向量 20 → 31，切片家族 FP-IS-00～15
ab55d93b  错误码 45 → 54，控制端那九个区分进 v2 注册表
```

### 验证只能在 vm01 上做

控制端没有 node／pnpm（`g1.yml` 注释逐字写着 *the control machine has no Node installed*，
实测确认）。`vm01` = Hyper-V 客户机 `win11-01`／`DESKTOP-F9HC40O`，node v24.20.0，
也是两个仓库的 self-hosted runner 宿主。进法 `ssh vm01`（经 `factory01` 跳板）。
**跑之前先确认两个 runner 都 `busy=false`。**

### 证据一：确定性

```
node tools/generate-protocol-candidate.mjs --verify-determinism
{ "deterministic": true, "fileCount": 1754, "divergentFileCount": 0, "divergent": [] }
EXITCODE=0
```

该模式 **spawn 两个独立进程**再比对，不是同进程跑两遍——生成器带模块级计数器，同进程重跑
会继续计数而不是重来，报出的是假分歧。这一点值得记下，将来改生成器别把它改掉。

### 证据二：复现（比出口要求的更强）

用这份生成器新产一棵树，与 `fp/v2-candidate`（`f6ee75d`）逐文件 SHA-256 比对：

| | |
| --- | --- |
| 生成树文件数 | 1754 |
| **逐字节相同** | **1753** |
| 只在生成树有 | **0** |
| 只在仓库有 | 9 |
| 内容不同 | 1（`manifest/release.json`） |

**差异恰好等于分叉台账第 6 节列的生成后手工步骤，一项不多一项不少：**

| 差异 | 台账步骤 |
| --- | --- |
| 7 个元文件（`.gitattributes`／`.gitignore`／`README.md`／`THIRD-PARTY-NOTICES.md`／`CLAUDE.md`／`.github/workflows/g1.yml`／`pnpm-lock.yaml`） | 1「放回七个仓库元文件」 |
| `manifest/release.json` 内容不同 | 3 `pnpm manifest:finalize` |
| `evidence/g1-result.json` 只在仓库有 | 4 `pnpm g1` |
| `.git`（worktree 指针文件，非生成物） | — |

**独立复现与台账互证**：台账说要补哪几步，复现出的差异就正好是那几步。

仓库里那份生成器与 vm01 上跑的那份**归一化行尾后逐字节相同**
（`19570b5480291d10aadad7557cac4e6f1ff5d318d789cdcda65ea3f75379d443`；vm01 那份是 CRLF，
比仓库里的 LF 版多 1136 字节 = 行数）。

### 复现用的脚本与两个坑

比对脚本 `.scratch/8005-batch-2/tools/Emit-GeneratedDigest.ps1`——在 vm01 上生成一棵树并输出
「相对路径 TAB SHA-256」清单，拿回控制端与本地 checkout 比对。

**不要在 vm01 上 `git clone`**：非交互 SSH 会话没有 git 凭据
（`fatal: could not read Username for 'https://github.com'`）。
**也不要直接读 runner 的 work 目录**：它归 `NT AUTHORITY` 的 `NETWORK SERVICE`，
当前用户是 `agvops`，git 会报 `detected dubious ownership`。
把清单拿回控制端比对同时绕开了这两条。

## 出口 3 —— 两条 `reasonCode ∈ 注册表` 架构测试

| 端 | 文件 | 结论 |
| --- | --- | --- |
| control-server | `tests/ControlServer.Tests/ProtocolReasonCodeArchitectureTests.cs` | ✅ 在 CI 的 561 绿里（run [34212715811](https://github.com/trytoreachpeak0/8005-agv-control-server/actions/runs/34212715811)：`失败: 0，通过: 561`） |
| onboard-hmi | `tests/SQCD.Agv.UnitTests/ReasonCodeRegistryArchitectureTests.cs` | ✅ 本机实跑，5 条断言全过（`Failed: 0, Passed: 5`，390 ms） |

onboard-hmi 的跑法（SDK 8.0.424 ＋ xunit.v3 ＋ `Microsoft.NET.Test.Sdk`／
`xunit.runner.visualstudio`，即 VSTest 模式）：

```
dotnet test tests/SQCD.Agv.UnitTests --filter "FullyQualifiedName~ReasonCodeRegistryArchitectureTests"
```

## 出口 4 —— `runner/` 两个 schema 已删且 manifest 哈希随之更新

- `schemas/runner/` 不存在。
- `manifest/release.json` 的文件表 **1758 条，其中 0 条 runner**。
- `approvals/release-approval.json` 已删（由外置的 `attestations/release-approval.template.json`
  取代）。
- `schemas/governance/` 三个 schema 齐（`content-manifest`／`integration-slice-index`／
  `release-approval-attestation`）。
- **哈希确实随之更新**：G1 在 CI 上逐文件校验 SHA-256 与文件数并通过，这是比对照 manifest
  自身更强的证据。

---

## 附带更正：错误码不是 45，是 54

规格 3.2、票 09（第 263／337／460 行）、票 14／15 的验收逐字写着「错误码 43 → **45**」。
**实测是 43 → 54，54 才是对的。**

「45」写在票 06 冻结之时，那时只查出控制端 3 个表外码。控制服务端提交 `9eb2397` 的标题即
「**reasonCode ∈ 注册表 的架构测试，顺便发现表外码是 14 个不是 3 个**」：

- 3 个是笔误（`PROTOCOL_RELEASE_MISMATCH` 少了 `IDENTITY` 之类），改名解决；
- 另 11 个**不是笔误，是实现表达了协议没有的区分**——协议只有一个 `RECOVERY_SCOPE_MISMATCH`，
  服务端分了事件／需求／操作员三种；只有一个 `ACTION_NOT_ALLOWED_IN_STATE`，服务端分了
  「已选动作」「找不到操作」「没有已证检查点」。合并会丢掉车载端给操作员看的提示。
- **用户 2026-09-04 定：那 11 个钉住，归宿是协议 v2 的错误码面**，不在那张票里改名。

那 11 个里 9 个进了注册表，另 2 个不进：

| 内部码 | 归宿 |
| --- | --- |
| `RECOVERY_SESSION_CLOSED` | 在 `ToSessionReadinessReasonCode` 边界映射到注册表已有的 `RECOVERY_SESSION_NOT_OPEN` |
| `FORCED_RECOVERY_GENERATION_MISMATCH` | 同上，映射到 `FORCED_RECOVERY_GENERATION_STALE` |

**43 ＋ 2（票 06 冻结的 `SLOT_CONFIGURATION_VERIFICATION_FAILED`／`_FINGERPRINT_MISMATCH`）
＋ 9 ＝ 54**，与 `fp/v2-candidate` 的 `errors/error-codes.json` 实测一致，`appendOnly` 不破
（0 删除，全部 `introducedInRelease: 1.0.0`）。架构测试的 `PinnedDeviations` 现为**空集**，
14 个全部收口。

票 14／15 的验收数字已改为 54。**规格 3.2 与票 09 的 45 未改**——本图不回溯改旧票据，引用
那两处时必须带上这条更正。

## 附带发现：白名单与实现对 `triggerEmergency` 的触发条件描述不一致

`vendor/8005-agv-program/docs/riot-call-allowlist.md` 第 167 行写的获批触发条件是

> 车辆在仓门未安全锁闭时移动、无 RIoT 订单可供 `OrderHold`、且无其它获批 RIoT 停车动作时，
> 8005 自动 `triggerEmergency` 并进入持续保持

但实现里**发车安全只是发车前门禁**（`JourneyRuntimeStage.AwaitingDepartureSafety`），不是在途
撤销触发急停；急停的唯一运行时路径是订单终态 FAILED → 证不出停住 → 升级。详见票 19 的
开工前判定。**这是文档与实现的一处偏离，不属于批次 1，单独记下。**
