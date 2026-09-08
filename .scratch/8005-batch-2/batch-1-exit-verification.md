# 批次 1 出口核实（2026-09-08）

批次 2 轨 A 的票 14／15／16／17 都以「批次 1 完成」为前置，而批次 1 是**无条目载体**的工程
（规格 3.2），没有票据、没有决议文档，出口状态此前只能靠 commit message 转述。本文把规格
8.3 的四条出口逐条核实一遍，作为轨 A 开工的依据。

**放在 `.scratch/8005-batch-2/` 而不是新开 `.scratch/8005-batch-1/`**：它服务的是批次 2 轨 A
的开工判定，不是批次 1 自己的交付物。若需要独立的批次 1 收口档，本文可整体搬过去。

## 结论：四条出口，三条绿，一条记为缺口

| # | 出口（规格 8.3） | 结论 |
| --- | --- | --- |
| 1 | G1 通过（候选态，用 tracked 空白模板） | ✅ **绿，CI 实证** |
| 2 | 生成器可重跑且输出确定（同输入两次逐字节相同） | ❌ **未达成，记为缺口** |
| 3 | 两条 `reasonCode ∈ 注册表` 架构测试绿 | ✅ **绿，两端各自实跑** |
| 4 | `runner/` 两个 schema 已删且 manifest 哈希随之更新 | ✅ **绿** |

**缺口不阻塞轨 A。**票 14／15／16 依赖的是协议仓里**已有的** v2 内容，不依赖生成器本身。

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

## 出口 2 —— 生成器可重跑且输出确定：**未达成**

**升级后的生成器只存在于 `vm01`，从未回到任何仓库。**

提交 `f6ee75d`（协议 v2 候选）正文自己写着「生成在 `vm01` 上跑（控制端没有 node/pnpm）」，
并引用一份「分叉台账第 6 节」的生成后手工步骤。**那份台账在本机不存在**（全盘 grep 无果）。

本机三份 `generate-protocol-candidate.mjs` 副本**字节完全相同**（SHA-256 前 16 位
`7b037dc9a518ea9c`），且都是 v0.1.1 MVP 版：

```
8005-fp/8005-agv-program/.scratch/wire-to-gate-ai-implementation-kit/tools/
8005-workspace/repos/8005-agv-program/.scratch/wire-to-gate-ai-implementation-kit/tools/
8005-workspace/repos/8005-agv-program/.claude/worktrees/full-product-map/.scratch/…/tools/
```

```js
const BASE_ID          = "https://schemas.8005-agv.local/wire-to-gate/v1";
const candidateVersion = "0.1.0";
const profileId        = "WIRE_TO_GATE_MVP";
const protocolVersion  = 1;
```

它写出的 `tools/g1-validate.mjs` 仍是 v0.1.1 契约：`index.slices.length===8`（v2 是 16）、
校验 `runner/` 两个 schema（规格要求删）、读 `approvals/release-approval.json`（规格要求不再
写出）、`manifest.status==="CANDIDATE_UNAPPROVED"`（实际是 `CONTENT_SNAPSHOT"`）。协议仓里
**真正提交的**那份则是 v2 的（16 切片、`schemas/governance/` 三个、无 runner）。

提交正文提到的 `--verify-determinism` 开关，本机三份里都没有。

**规格 3.2 的 11 项输出点是批次 1 唯一真正的工作量，而它现在不在版本控制里。**同输入重跑本机
根本跑不了；就算装上 node，跑的也是 v0.1.1 那份，产不出 v2。

**用户 2026-09-08 定：记为缺口，不阻塞轨 A 开工。**要真正关上它，只有两条路——从 `vm01` 取回
那份升级后的 `.mjs` 与分叉台账并提交进仓，或照规格 3.2 的 11 项输出点在本机重建一份直到它能
产出与 `fp/v2-candidate` 逐字节相同的树。

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
