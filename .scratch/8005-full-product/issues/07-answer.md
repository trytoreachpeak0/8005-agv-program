# 票 07 决议：完整产品切片家族编号与 W2G-IS-00～07 的关系

日期：2026-09-04
票据：[07-decide-full-product-slice-family-and-relation-to-w2g-is.md](07-decide-full-product-slice-family-and-relation-to-w2g-is.md)
前置：[票 06 决议](06-answer.md)（协议 v2 冻结面）
用户决策：Q1 取 (a) 替换为 `FP-IS-NN` 家族；Q2 取 (a) 复活生成器，估算交票 09

**一句话**：完整产品切片家族**替换**旧家族，取 `FP-IS-NN`（`^FP-IS-[0-9]{2}$`），
**16 个切片**——前 8 个与 `W2G-IS-00～07` 一一对应作为 v2 重证，后 8 个是新能力；
31 条向量全部绑定，无一条落空；门禁模型 `G1 / CONTROL_SERVER_G2 / ONBOARD_HMI_G2 / G3`
**不增不减**；`definition` 块推广为全部切片必填，但 `demandRepresentation` 必须重写；
**批次与业务簇都不进 id**。

---

## 一、事实基础

### 1.1 `^W2G-IS-0[0-7]$` 不是两份副本，是 9 处，另有 161 个测试 trait

票 06 的 3.6 第 7、8 条只列了 `runner/runner-contract.schema.json` 与
`ControlServer.Conformance/Program.cs:11`。逐仓实读的完整结果：

| 仓 | 位置 | 内容 |
| --- | --- | --- |
| protocol | `schemas/governance/integration-slice-index.schema.json:30` | `integrationSliceId` 的 pattern |
| protocol | `schemas/governance/integration-slice-index.schema.json:41` | `prerequisites.items` 的 pattern |
| protocol | `runner/runner-contract.schema.json:14` | pattern |
| protocol | `runner/result.schema.json:13` | pattern |
| protocol | `runner/result.schema.json:71` | `supportedIntegrationSliceIds.items` 的 pattern |
| protocol | `tools/g1-validate.mjs:21` | `slices.length===8` ＋ 八个 id 的全表逐字比对 |
| control-server | `tools/ControlServer.Conformance/Program.cs:11` | `Regex.IsMatch` |
| control-server | `scripts/test-wire-to-gate.ps1:4` | `[ValidatePattern('^W2G-IS-0[0-7]$')]` |
| control-server | `scripts/run-staged-g3.ps1`、`run-staged-g3-restart.ps1`、`run-demand-bearing-g3-vectors.ps1` | 各 2 处字面量 |

**另有两处票 06 完全没有提到的结构性耦合**：

1. **`scripts/test-wire-to-gate.ps1:15-23` 是 `integration-slices/index.json` 的第二份副本。**
   一张 `$sliceVectors` 哈希表，把八个切片的向量集合原样又写了一遍。两份之间没有任何东西
   在校验一致性——协议仓改了 `index.json`，控制端这张表不会红，只会静默地跑一组别的向量。
2. **`[Trait("IntegrationSlice", "W2G-IS-0N")]` 在 `tests/ControlServer.Tests/` 出现 161 次**
   （IS-01 43、IS-00 28、IS-06 27、IS-03 19、IS-02 15、IS-05 11、IS-07 9、IS-04 9）。
   `test-wire-to-gate.ps1` 用 `dotnet test --filter "IntegrationSlice=$Slice"` 分片，
   **切片编号就是测试的分区键**。

车载端（只读）另有 `docs/ONBOARD_DEVELOPER_HANDOFF.md`、
`docs/WANG_KUN_FIRST_INTEGRATION_WORK_PACKAGE.md` 两份文档与
`evidence/g2/**/summary.json`、`evidence/g3/**/run-result.json`、`evidence/g3/**/runner.ps1`
携带旧编号；证据不可变，文档归 Kun Wang。

### 1.2 票据陈述的三种代价，两种不成立、一种是结构上做不到

票据正文把「沿用／替换／并存」的代价写成三句话。逐条核对：

**「替换会作废既有证据链」——不成立。证据本来就作废。**
`docs/release-governance.md:12`：「It still changes the manifest/vector identity and invalidates
affected G1/G2/G3 evidence.」票 06 第 6 问同样写明「v2 落地并打 tag 之后全部作废」。
**MVP 证据的失效由 `ProtocolReleaseIdentity` 换代引起，与切片编号无关。**改不改编号，
`protocol-v0.1.1` 下的那批 G2／G3 一样归零。这条代价在三个选项之间是**常量**，不是变量。

**「沿用会让两代证据混在同一编号下难以区分」——机械上分得开。**
实读 `8005-agv-control-server/artifacts/g2/protocol-v0.1.1-is01/gate-result.json`，
16 个字段里有 `protocolReleaseVersion`、`protocolTag`、`protocolRepositoryCommit`、
`protocolManifestSha256`、`protocolSchemaBundleSha256`、`protocolVectorsSha256` 六项发布身份。
**沿用的真实代价不在证据检索，在两处别的地方**：其一，`W2G` 是六类 MES 任务之一的名字
（票 13 查实六类真名，`WIRE_TO_GATE` 只占其一），完整产品还含充电、配置激活、告警，
前缀永久名实不符；其二，161 个测试 trait 里的 `W2G-IS-01` 会同时指 v1 与 v2 两代能力，
而 trait 是纯字符串，没有任何东西能把它绑到某个 release。

**「并存要求两套编号在同一 `index.json` 内共存」——结构上做不到。**
`integration-slice-index.schema.json:15-16` 把 `slices` 锁成 `"minItems": 8, "maxItems": 8`，
`sequence` 锁成 `maximum: 7`；且票 06 的 3.1 已把 schema `$id`／`$ref` 的 URI 段整体从
`wire-to-gate/v1` 改到 `agv-full-product/v2`，**v1 的 `index.json` 活在不可变 tag
`protocol-v0.1.1` 里**，一个仓库只有一个 `integration-slices/index.json` 路径。
并存不是「两套编号写进一个文件」，而是「同一路径下的文件被两个 release 分别冻结」——
**那正是替换，只是换了个说法**。

### 1.3 「一眼看出属哪个批次」是循环依赖

票据第 2 问要求「命名必须让人一眼看出切片属哪个批次、哪个业务面」。
依赖图是 `09 ← 07, 13, 14, 15`——**批次由票 09 划分，而票 09 被本票阻塞**。
本票开工时批次数、批次边界、每条需求归哪个批次全部未知。
**id 里不可能编码批次**，这不是取舍，是顺序约束。

### 1.4 `definition` 块无法原样推广：`demandRepresentation` 三个字段全是 `const`

`integration-slice-index.schema.json` 的 `$defs.definition.properties.demandRepresentation`：

```
controlServerFact: { "const": "AcceptedDemandSnapshot" }
wireMessages:      { "type": "array", "const": ["UpcomingStopPlanSnapshot", "CurrentStopWorklistSnapshot"] }
onboardMode:       { "const": "READ_ONLY_COMMITTED_PROJECTION" }
```

三个 `const` 加 `additionalProperties: false` 加 `required` 四项。
**充电切片、配置激活切片、告警切片一个字段都填不进去**——它们的服务端权威事实不是
`AcceptedDemandSnapshot`，线上消息不是那两条，车载端也不是只读投影。
「`definition` 是否推广」不是一个是非题：**推广必然连带重写这个子块**。

### 1.5 `runner/` 两个 schema 是无生产者无消费者的孤儿，而且与现实不兼容

这是本票最意外的一条，也是票 06 那条「G2 记着 `vectorId` 却只跑自家 xunit」的**上游原因**。

**`runner-contract.schema.json` 描述不了仓库里真实存在的向量。**契约要求顶层是一个对象，
带 `vectorId`／`integrationSliceId`／`virtualClockStart`／`steps`／`initialPersistentFacts`／
`forbiddenSideEffects` 六项必填；而 `vectors/CV-DEMAND-ACCEPT-TO-PICKUP/input.ndjson`
是**一串 step 对象的 NDJSON 流**，没有顶层对象，step 里带着契约 `additionalProperties: false`
禁止的 `adapter`／`result`／`virtualTimeOnly`，又缺契约要求必填的 `payloadRef`。
另外 `initialPersistentFacts` 被锁成 `"properties": {}, "required": [], "additionalProperties": false`
——**它只能是空对象**，任何需要前置状态的场景（低电量车、已登记的桩、已生效的绑定集）
在这个契约下无法表达。

**`result.schema.json` 同样对不上真实的门禁结果。**它 `required` 16 项，
而 `gate-result.json` 只提供其中 5 项（`integrationSliceId`、`protocolManifestSha256`、
`startedAt`、`finishedAt`、`vectorIds`），缺 11 项——**其中 `onboardHmiCommit`、
`fakePeerIdentities`、`firstDivergence`、`evidencePointers` 四项正是「双端联合证据」
的核心**，一个都没落地；同时 `gate-result.json` 自带 11 个契约里没有的字段。

**没有任何东西在校验这两件事。**`g1-validate.mjs` 对 `runner/` 只做两件事——
`ajv.validateSchema(s)` 与 `ajv.compile(s)`，即「它是不是一个合法且能编译的 schema」，
**从不用它校验任何文档**。

后果对本票是直接的：9 处 pattern 副本里有 **3 处**（`runner-contract:14`、`result:13`、
`result:71`）活在**没有生产者也没有消费者、且与现实不兼容**的文档里。

### 1.6 保形向量是单会话格式，多车并发在结构上证不了

`runner-contract.schema.json` 的 `steps[]` 只有 `step`／`atMs`／`action`／`messageType`／
`payloadRef` 五个字段，`action` 十一个取值里没有任何一个能指定「哪辆车」；
`integrationSliceId` 与 `vectorId` 都是单值；`input.ndjson` 是一条流。
**保形向量表达的是一个会话的一条时间线。**

这解释了票 06 为什么给 B2（多车并发）**一条向量都没有**——不是遗漏。多车并发的证明
只能落在服务端单端测试与现场验收上，**不能立切片**（见第 3 问）。

### 1.7 `CONTEXT.md:231` 的 `IntegrationSlice` 词条定义被完整产品推翻

原文：「以稳定 IntegrationSliceId 标识、能够由共享协议向量和确定性故障脚本独立复现的
一段 **WIRE_TO_GATE** 跨端能力」。完整产品的切片覆盖自动充电、仓位配置原子激活、
车载告警上报——**都不是 WIRE_TO_GATE 能力**。

**这是本图第二次「既有词条的定义被推翻，而不是缺词条」**，第一次是票 06 的
`WireToGateMvpProtocolProfile`。交接文档预告的检查点（「下一票仍先查 `CONTEXT.md`，
但要多查一步：现有词条的定义在完整产品下还成不成立」）在本票命中。

### 1.8 生成器存在，且它写的是整棵树——票 06 的「最大单项」估算前提是错的

票 06 的 1.6 与 3.7 第 2 项写「约 1500 个 invalid 样例是机械派生的但**仓库里没有生成器**
……**这是最大的单项**」。它查的是 `8005-agv-protocol`。生成器不在那里，在**本仓**：

`8005-agv-program/.scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.mjs`，
**595 行**，入口 `node generate-protocol-candidate.mjs <protocol-repository>`。
顶层四个常量决定全部身份：

```js
const BASE_ID = "https://schemas.8005-agv.local/wire-to-gate/v1";
const candidateVersion = "0.1.0";
const profileId = "WIRE_TO_GATE_MVP";
const protocolVersion = 1;
```

——**正是票 06 的 3.1 要改的那四项**。它写出的文件覆盖 `schemas/`（envelope、types、bundle、
逐消息）、`examples/valid` 与 `examples/invalid`（`required`／`type`／`enum-or-const`／
`uniqueItems`／`x-sorted`／`semantic-*` 逐条派生，正是票 06 第 3 问描述的机械口径）、
`vectors/`、`integration-slices/index.json`、`runner/` 两个 schema、`errors/error-codes.json`、
`manifest/release.json`、`compatibility/`、`docs/` 三篇，**连 `tools/g1-validate.mjs` 本身
都是它 `writeText` 出来的**。

**切片家族在它里面是一张 10 行的表**（第 480–490 行），`prerequisites` 由一行 `.map()`
推导，`gates` 与 `forbidUnclosedFailOrInconclusive` 是常量。

**它落后一个修订。**产出的是 `0.1.0`，`index.json` 的 `schemaVersion` 是 `"1.0.0"` 且
**不带 `definition` 块**；`schemas/governance/` 三个文件（`content-manifest`、
`integration-slice-index`、`release-approval-attestation`）**不在它的输出清单里**；
它写的 `g1-validate.mjs` 是旧版（`manifest.status==="CANDIDATE_UNAPPROVED"`、
读 `approvals/release-approval.json`、无 `x-sorted` 语义规则、无 attestation 外置逻辑）。
**这些都是 0.1.1 手工补上去的，要用生成器产 v2 就得先把它们补回生成器。**

用户 2026-09-04 已决定取「复活并升级生成器」。**工作量重估交票 09**——票 06 把
examples 树标成「最大单项」是在「生成器不存在」的前提下估的，前提错了估算必须重做。

---

## 二、六问定案

### 第 1 问 — 新旧关系：替换。旧家族随 `protocol-v0.1.1` 原地冻结

**完整产品建立全新切片家族，`W2G-IS-00～07` 不被任何 v2 资产引用。**

理由按 1.2 的三条核对结果重排：

1. 「替换代价高」的那个代价（证据作废）在三个选项之间是常量，**它不是选替换要付的价**。
2. 替换的真实增量代价是**一次机械重打标**：161 个 trait ＋ 9 处硬编码 ＋ 两份脚本。
   而这 161 个测试本来就要因为 v2 的消息面变更（54 沿用 ＋ 5 改 payload ＋ 9 新增）
   被逐个复核，**重打标搭在一次必然发生的遍历上**。
3. 沿用要付的是一个**永久**的名实不符：`W2G` 是六类 MES 任务里一类的名字。

**旧家族的证据在新体系下如何被引用**——靠 `ProtocolReleaseIdentity`，不靠编号：

> 批次 0 的跨端能力证据 = `protocol-v0.1.1` 下 `W2G-IS-00`～`W2G-IS-07` 的
> `CONTROL_SERVER_G2` / `ONBOARD_HMI_G2` / `G3` 结果，
> 由 `gate-result.json` 的 `protocolTag` ＋ `protocolRepositoryCommit` ＋ 三个哈希唯一定位。

规格中同时写明 **`FP-IS-00`～`FP-IS-07` 与 `W2G-IS-00`～`W2G-IS-07` 一一对应**，
关系是「v2 下的重证」而**不是「可以沿用的通过结论」**——
`ConformanceRunIdentity` 词条已经规定「任一绑定分量变化都必须建立新运行」。

### 第 2 问 — 编号体系：`FP-IS-NN`，批次与业务簇都不进 id

**前缀 `FP-IS`**（Full Product Integration Slice），与剖面 TSV 的 `FP-C*` 簇编号、
`FP-B0` 批次 0 标记同源，一眼可辨属于完整产品这一代。

**pattern `^FP-IS-[0-9]{2}$`**——两位数字，**不把切片数量编进正则**。
v1 的 `0[0-7]` 是一个具体教训：加一个切片要改 5 个文件里的正则。
数量约束改由 `g1-validate.mjs` 一处承担（见第 3 节 3.4）。

**批次不进 id**：1.3 的循环依赖，这是顺序约束不是取舍。

**业务簇也不进 id**，理由是稳定性：**本图已经把需求→簇的归属改判过五次**
（票 12 改 1 条、票 13 改 19 条、票 04 改 2 条、票 05 改 18 条，票 06 另改一处形态判定）。
簇编进 id 意味着每次改判都要给一个活在 161 个测试 trait 与不可变证据目录里的标识符改名。
**id 必须比它描述的分类更稳定。**

**「一眼看出业务面」由 `definition.scope` 承担**——它已经是 schema 里的必填
SCREAMING_SNAKE token（v1 只有 IS-01 有，本票推广为全部必填，见第 5 问），
例如 `AUTOMATIC_CHARGING_CYCLE_AND_CLEARANCE`。文档与证据目录写
`FP-IS-13 AUTOMATIC_CHARGING_CYCLE_AND_CLEARANCE`，id 稳定、面可见。

**票据第 2 问的两个要求本票只满足一个**：业务面满足，批次不满足且不可能满足。
批次→切片的映射归**最终规格**（票 10），不进协议仓——见第 6 问。

### 第 3 问 — 切片粒度：沿用 MVP 标准，并补一条把单端工作排除在外的边界

**沿用**「一次可独立联调并产出门禁证据的双端能力」，不改粒度标准。
同一业务闭环的失败分支与主干**同属一个切片**（v1 的 IS-02 就是取货 ＋ 修正 ＋ 全空取消
三条向量一个切片），本票的 `FP-IS-13`（充电三条向量）与 `FP-IS-14`（激活成功 ＋ 结果未知）
照此办理。

**补一条 v1 不需要而完整产品必须有的边界**：

> **切片只覆盖「控制服务端 ↔ 车载端」的双端能力。**
> 服务端↔RIoT、服务端↔MES、服务端↔人 的单端能力不立切片，
> 其验收归批次自身，由票 08 定证据形态。

完整产品比 MVP 多出成规模的单端工程，照 MVP 的粒度标准会无处安放：
票 14 的 `RouteGraphSnapshot` 路网成本引擎（服务端↔RIoT）、
`FP-C5` AGV 归档恢复（票 05 判恢复入口不在看板也不在车载端）、
`FP-C9b` 公共站点绑定运维治理（服务端内部配置治理）、
`FP-C8` 看板本体（服务端↔人）。

**多车并发（B2）也不立切片，但理由不同**：1.6 已证保形向量是单会话格式，
`steps[]` 没有任何字段能指定车辆，**多车并发在这个证据形态下结构上不可表达**。
它的证明落在服务端单端测试 ＋ 现场验收，交票 08。

### 第 4 问 — 门禁模型：`G1 / CONTROL_SERVER_G2 / ONBOARD_HMI_G2 / G3` 不增不减

**四道门禁一字不改**，`gates` 保持 `const` 数组。

**现场验收不进门禁模型**，仍归票 08 的验收边界。三条理由：

1. `gates` 是**每个切片必须相同的 `const`**。现场前置条件逐簇不同——票 04 查实
   三个充电桩物理上还没安装，票 12 查实等待点尚未测绘进 RIoT 地图——
   把现场验收做成每切片必过的第五道门，等于让 `FP-IS-00` 这种纯会话层切片
   去等充电桩安装。
2. 现场验收的粒度是**批次与场地**，不是切片。票 13 已经定「验收期只有 `WIRE_TO_GATE`
   能在现场真实触发」，那是一句关于**投运范围**的话，不是关于某个切片的话。
3. map Notes 已把「逐切片的验收证据清单」划给实施图，把「验收边界与证据要求」划给票 08。

**另记一条对票 08 有用的事实**：`CONTROL_SERVER_G2` 与 `ONBOARD_HMI_G2`
命名的是**哪一端**，不是**哪个人**。用户 2026-09-04 告知的两仓开发归属交接
**不需要改动门禁名称或切片的 `gates` 数组**，分工机制原样成立。

**但 G2 的内容有一个已知缺口，本票不补、明确交票 08**：票 06 的 1.3 查实 G2 证据记着
`vectorIds` 而实际跑的是本仓 xunit 套件，向量从未被机械执行；本票 1.5 进一步查实
**`runner/` 两个 schema 与真实向量、真实门禁结果都不兼容，且无人校验**。
「谁来跑向量、跑出来的结果按什么格式落证据」是票 08 的验收出口问题。
**`runner/` 两个文件在 v2 下是修还是删，由票 08 定**——本票只规定：若它们存活，
其 pattern 必须随本家族改为 `^FP-IS-[0-9]{2}$`。

### 第 5 问 — 与协议 v2 的绑定：`vectorIds` 数组不变，`definition` 推广为全部必填

**向量绑定形态沿用 `vectorIds` 数组，允许跨切片共享。**票 06 的 31 条向量
在本票的 16 个切片下全部有归属、无一条落空，共享 3 例（沿用 v1 的三例，见第 3 节 3.1）。

**`ProtocolReleaseIdentity` 的表达方式不变**：切片本身不携带发布身份，
身份由 `manifest/release.json` 与门禁结果携带。切片是**契约内容的分区**，
不是发布单位——把 release 身份写进每个切片会制造 16 份会漂移的副本。

**`definition` 推广为全部 16 个切片必填**，理由与票 06 把 `productAssertions` 全量必填
同源：v1 只有 IS-01 有 `definition`，于是 G1 只能给 IS-01 写专属断言，
其余七个切片除了「向量 id 在注册表里」之外**没有任何可机械检查的内容**。
16 个切片、其中 8 个是全新能力，这个缺口只会更大。

**代价是 `demandRepresentation` 必须重写**（1.4）。本票的处置见第 3 节 3.3。

### 第 6 问 — `index.json` 的变更方式：同一路径、随 v2 整体重生成，不另立文件

**写进既有 `integration-slices/index.json`，不另立文件。**
1.2 已证「并存」在结构上就是「替换」——一个仓库一个该路径，
v1 的那份被 `protocol-v0.1.1` 冻结，v2 的那份是新内容。
另立文件只会制造第二个真相源，而 1.1 已经有一个活生生的反例
（`test-wire-to-gate.ps1` 的 `$sliceVectors` 与 `index.json` 无人校验地并存）。

**产出方式取用户已定的 (a)：升级 1.8 的生成器，`slices` 表改完重跑。**
本票的家族改动在生成器里是**一张 10 行表的替换 ＋ 一处 pattern 常量**，
不是 9 处手改。生成器落后一个修订的补齐工作与整体工作量重估**交票 09**。

**本票不改 `8005-agv-protocol` 任何内容，不写 `index.json`。**
落地时按 notify-after-change 规则开 issue @`SocialKKKK`，说明三件事：
改了什么（切片家族整体替换为 `FP-IS-00～15`）、触及哪些 `W2G-IS-*`
（**全部八个，全部被 `FP-IS-00～07` 取代**）、他的 `ONBOARD_HMI_G2` 证据是否作废
（**v2 打 tag 后全部作废，与票 06 的结论一致，不因本票额外作废任何东西**）。
这条通知与票 06 的那条**应当合并为一次**——协议改动要攒批次，两票都只改设计面未落地。

---

## 三、完整产品切片家族（交付物本体）

### 3.1 家族全表：16 个切片，31 条向量

前 8 个是 `W2G-IS-00～07` 的 v2 重证（向量集合、`sequence`、`prerequisites` 全部沿用）；
后 8 个是新能力。`面` 列是剖面 TSV 的 `FullProductCluster`，**只写在本规格里，不进
`index.json`**（第 2 问）。

| id | seq | prereq | `definition.scope` | `vectorIds` | 面 | 来源 |
| --- | --- | --- | --- | --- | --- | --- |
| `FP-IS-00` | 0 | — | `SESSION_HANDSHAKE_RECOVERY_AND_SNAPSHOT` | `CV-SESSION-RECOVERY-HAPPY`、`CV-SESSION-RECONNECT-DURING-RECOVERY`、`CV-SNAPSHOT-REPLACE-AND-ACK`、`CV-SNAPSHOT-SAME-REVISION-CONFLICT` | FP-B0 | v1 IS-00 |
| `FP-IS-01` | 1 | 00 | `DEMAND_ACCEPTANCE_AND_TO_PICKUP` | `CV-DEMAND-ACCEPT-TO-PICKUP` | FP-B0 | v1 IS-01 |
| `FP-IS-02` | 2 | 01 | `STATION_PICKUP_AND_MULTI_SLOT_LOAD` | `CV-PICKUP-SUBLOT-LOAD`、`CV-LOAD-CORRECTION`、`CV-LOAD-CANCELLATION-ALL-EMPTY` | FP-B0 | v1 IS-02 |
| `FP-IS-03` | 3 | 02 | `PREDEPARTURE_SAFETY_AND_RESULT_RECONCILE` | `CV-PREDEPARTURE-SAFETY-EXPIRES`、`CV-OPERATION-RESULT-UNKNOWN-RECONCILE` | FP-B0 | v1 IS-03 |
| `FP-IS-04` | 4 | 03 | `DESTINATION_BATCH_UNLOAD` | `CV-GATE-UNLOAD-ALL-EMPTY` | FP-B0 | v1 IS-04 |
| `FP-IS-05` | 5 | 00 | `CONNECTION_LOSS_SAFE_FINISH` | `CV-CONNECTION-LOSS-SAFE-FINISH`、`CV-SESSION-RECONNECT-DURING-RECOVERY` | FP-B0 | v1 IS-05 |
| `FP-IS-06` | 6 | 00 | `RELIABLE_DELIVERY_AND_RESULT_REPLAY` | `CV-RELIABLE-RETRY-SAME-CONTENT`、`CV-RELIABLE-RETRY-DIFFERENT-CONTENT`、`CV-REQUEST-FIRST-RESULT-REPLAY`、`CV-OPERATION-RESULT-UNKNOWN-RECONCILE` | FP-B0 | v1 IS-06 |
| `FP-IS-07` | 7 | 00 | `EXCEPTION_RECOVERY_AND_MANUAL_RETURN` | `CV-OPERATION-RESULT-UNKNOWN-RECONCILE`、`CV-EXCEPTION-RESUME`、`CV-EXCEPTION-COMPENSATE`、`CV-FAULT-CARGO-HANDOFF`、`CV-FORCED-MECHANICAL-RECOVERY`、`CV-MANUAL-CHARGING-RETURN` | FP-B0 | v1 IS-07 |
| `FP-IS-08` | 8 | 04 | `MULTI_STOP_JOURNEY_PLAN` | `CV-MULTI-STOP-PICKUP-SEQUENCE` | FP-C2 | 票 03 B3 |
| `FP-IS-09` | 9 | 08 | `ONBOARD_WORKLIST_SELECTION` | `CV-MULTI-DEMAND-PLAN-AND-SELECT` | FP-C3 | 票 03 B5 |
| `FP-IS-10` | 10 | 01 | `TASK_TYPE_ADMISSION_FAIL_CLOSED` | `CV-TASK-TYPE-ADMISSION-FAIL-CLOSED` | FP-C9a | 票 13 |
| `FP-IS-11` | 11 | 10 | `REVERSED_DIRECTION_JOURNEY` | `CV-REVERSED-DIRECTION-JOURNEY` | FP-C9a | 票 13 |
| `FP-IS-12` | 12 | 04 | `WAITING_POINT_IDLE_RETURN` | `CV-WAITING-POINT-IDLE-RETURN` | FP-C4 | 票 12 |
| `FP-IS-13` | 13 | 12 | `AUTOMATIC_CHARGING_CYCLE_AND_CLEARANCE` | `CV-CHARGING-CYCLE-HAPPY`、`CV-CHARGING-UNABLE-FIELD-CONFIRM`、`CV-CHARGING-STATION-MANUAL-CLEARANCE` | FP-C1 | 票 04 |
| `FP-IS-14` | 14 | 00 | `SLOT_CONFIGURATION_ACTIVATION` | `CV-SLOT-CONFIGURATION-ACTIVATION`、`CV-SLOT-CONFIGURATION-ACTIVATION-UNKNOWN` | FP-C7 | 票 05 |
| `FP-IS-15` | 15 | 00 | `ONBOARD_ALARM_SNAPSHOT` | `CV-ONBOARD-ALARM-SNAPSHOT` | FP-C8 | 票 05 |

**核对**：`vectorIds` 条目合计 34，去重 31，与票 06 冻结的 31 条**恰好相等**，
无遗漏无多余。共享 3 例，全部沿用 v1：`CV-OPERATION-RESULT-UNKNOWN-RECONCILE`
属 03／06／07，`CV-SESSION-RECONNECT-DURING-RECOVERY` 属 00／05。
`sequence` 0～15 连续，`prerequisites` 一律指向更小的 `sequence`。

**三条非显然的依赖边，各有事实依据**：

- **`FP-IS-13` ← `FP-IS-12`（充电依赖等待点）**：票 02 已查实
  「充电依赖的是等待点而非多车调度」（`REQ-0178`）；`REQ-0179` 规定清桩的两种完成证明
  之一是「系统确认车辆已到地图等待点」。
- **`FP-IS-11` ← `FP-IS-10`（反向旅程排在准入之后且单列）**：票 13 明文要求
  `STAGING_TO_WIRE` 单列后一批，理由是 `BuildRouteEvidenceId` 起终点互换
  **编译期完全静默**却会让幂等重放失配。这是风险隔离，不是省事。
- **`FP-IS-09` ← `FP-IS-08`（选任务依赖多 Demand 计划）**：没有多 Demand 计划，
  「从最新 `CurrentStopWorklistSnapshot` 里选一个」无对象可选；票 06 已把
  `worklistItems.maxItems` 由 1 放到 8。

### 3.2 无切片的簇，及各自的理由

**这份清单是票 08 与票 09 的直接输入**——切片家族**不覆盖完整产品的全部工作**。

| 面 | 条数 | 无切片的理由 |
| --- | --- | --- |
| `FP-C2` 的多车并发（B2 那一半） | — | 保形向量是单会话格式，`steps[]` 无车辆维度，**结构上不可表达**（1.6）。证明落服务端单端测试 ＋ 现场验收，交票 08 |
| `FP-C5` AGV 归档恢复与身份连续性 | 6 | 单端。票 05 已判恢复入口不在看板、不在车载端，只在受控运维流程里 |
| `FP-C9b` 公共站点绑定运维治理 | 9 | 单端（服务端内部配置治理）。其唯一的线上后果是 fail-closed 准入，已由 `FP-IS-10` 覆盖 |
| `FP-C6` 账号权限与密码治理 | 8 | 票 05 判随 `FP-C10` 延后（`REQ-0254` 除外，判部分实施且协议 v1 已实装） |
| `FP-C10` 人员认证与账号 | 8 | 票 05 判整簇延后 |
| 票 14 的 `RouteGraphSnapshot` 引擎 | — | 单端（服务端↔RIoT）。票 14 已判它是「可与 B2 并行的旁路大件」 |
| `FP-C8` 看板本体（`REQ-0268`／`REQ-0269`） | 2 | 单端（服务端↔人）。仅告警的车载端来源那一半由 `FP-IS-15` 覆盖 |

### 3.3 `definition` 块的 v2 形态

**必填**（v1 是可选，只有 IS-01 有）。四个字段里三个沿用，一个重写。

| 字段 | v1 | v2 |
| --- | --- | --- |
| `scope` | `^[A-Z][A-Z0-9_]+$`，可选块内必填 | 不变，全部切片必填，取值见 3.1 |
| `requiredOutcomes` | `tokenArray` | 不变 |
| `ownerResponsibilities` | `{controlServer, onboardHmi}`，均 `tokenArray` | 不变 |
| `demandRepresentation` | 三个 `const`，只描述 Demand | **删除，换成 `authorityModel`** |

**`authorityModel`**（替换 `demandRepresentation`，`additionalProperties: false`，三项必填）：

| 字段 | 形态 | 说明 |
| --- | --- | --- |
| `controlServerFact` | `^[A-Z][A-Za-z0-9]+$`（PascalCase） | 本切片的权威落在服务端哪个持久事实上。v1 锁死 `AcceptedDemandSnapshot`，v2 放开为模式 |
| `wireMessages` | 消息类型名数组，`minItems: 1`，`uniqueItems` | 本切片的线上消息面。v1 锁死那两条，v2 放开 |
| `onboardModes` | enum 数组，`minItems: 1`，`uniqueItems` | **由单值改为数组**——v1 的单 `const` 只在 IS-01 恰好只有一种权威关系时成立 |

**`onboardModes` 四个取值**，各对应 `CONTEXT.md` 里已有的一条权威边界：

| 取值 | 含义 |
| --- | --- |
| `READ_ONLY_COMMITTED_PROJECTION` | 车载端只读展示服务端已承诺的投影，不发现、不选择、不绑定 |
| `REQUEST_SUBJECT_TO_SERVER_ADJUDICATION` | 车载端可发起请求，裁决权在服务端 |
| `LOCAL_PHYSICAL_EXECUTION_AUTHORITY` | 车载端持有物理执行与 IO 独占权威 |
| `ONBOARD_AUTHORED_FACT_REPORT` | 车载端是某类事实的作者，服务端只采纳与记录 |

**逐切片取值**（本票定的是分类判断，不是填表；`requiredOutcomes`／`ownerResponsibilities`／
`wireMessages` 的逐条内容归实施图）：

| 切片 | `onboardModes` |
| --- | --- |
| `FP-IS-00`、`01`、`08`、`10`、`11`、`12` | `[READ_ONLY_COMMITTED_PROJECTION]` |
| `FP-IS-02` | `[LOCAL_PHYSICAL_EXECUTION_AUTHORITY, REQUEST_SUBJECT_TO_SERVER_ADJUDICATION]` |
| `FP-IS-03`、`04`、`14` | `[LOCAL_PHYSICAL_EXECUTION_AUTHORITY]` |
| `FP-IS-05`、`15` | `[ONBOARD_AUTHORED_FACT_REPORT]` |
| `FP-IS-06` | `[READ_ONLY_COMMITTED_PROJECTION, ONBOARD_AUTHORED_FACT_REPORT]` |
| `FP-IS-07` | `[LOCAL_PHYSICAL_EXECUTION_AUTHORITY, ONBOARD_AUTHORED_FACT_REPORT]` |
| `FP-IS-09` | `[REQUEST_SUBJECT_TO_SERVER_ADJUDICATION]` |
| `FP-IS-13` | `[READ_ONLY_COMMITTED_PROJECTION, ONBOARD_AUTHORED_FACT_REPORT]` |

**`FP-IS-01` 的 `ownerResponsibilities.onboardHmi` 必须改**：v1 的
`NEVER_DISCOVER_SELECT_OR_BIND_DEMAND` 在 B5 幅度 1 之下不再成立（票 03）。
`onboardMode` 的 `READ_ONLY_COMMITTED_PROJECTION` **在 `FP-IS-01` 上仍然成立**
（那条投影依然只读，新增的是 `FP-IS-09` 的请求，与 `SublotSubmitted` 同构），
所以是 token 改而不是模式改。改动与向量 `productAssertions.onboardHmi` **同步**——见 3.4。

### 3.4 `g1-validate.mjs` 的切片校验重写

v1 第 21–24 行是「8 个切片数 ＋ id 全表 ＋ IS-01 专属五处断言」。
**IS-01 专属断言之所以是专属的，是因为只有它有 `definition`**；`definition` 全量必填
之后，那五处应当推广为家族级规则，且**全部与切片数量无关**。

**删除**：`slices.length===8`、八个 id 的全表逐字比对、IS-01 的五处专属断言。

**新增七条家族级规则**：

1. 每个 `integrationSliceId` 匹配 `^FP-IS-[0-9]{2}$` 且全表唯一。
2. `sequence` 从 0 起连续、无重复（**取代 `slices.length===8`**，且是更强的检查）。
3. 每个 `prerequisites` 元素存在于本表内，且其 `sequence` 严格小于本切片
   （**v1 没有这条检查，靠人写对**）。
4. 每个切片 `vectorIds` ⊆ `requiredVectors`（沿用 v1）；**且反向也成立**——
   31 条向量每一条至少被一个切片引用（**v1 没有这条，一条向量可以无人认领**）。
5. 每个切片 `definition` 存在（**由可选改必填**）。
6. 切片的 `definition.ownerResponsibilities.onboardHmi` **恰好等于**其全部向量
   `productAssertions.onboardHmi` 的**并集**；`controlServer` 同理。
   ——v1 是「IS-01 与其唯一向量逐字相等」，在多向量切片上无法成立；
   取并集是它的自然推广：**没有向量证明的责任不许声明，向量断言的东西必须在责任表里**。
7. `definition.requiredOutcomes` ⊇ 该切片全部向量 `productAssertions.controlServer` 的并集。

**第 6、7 条只在 v1 唯一的实例（IS-01）上验证过成立**：
`requiredOutcomes` 五项 ⊇ `productAssertions.controlServer` 四项，第五项
`COMMITTED_DEMAND_JOURNEY_PROJECTED` 是车载侧成果的 outcome 措辞。
其余 15 个切片的 token 尚不存在，**规则的可满足性由实施图在写 `definition` 时负责**。

### 3.5 必须同步修改的位置全表（接续票 06 的 3.6）

票 06 的 3.6 有十条，其中第 4、5、7、8 条「待票 07 定」。本票定案后的完整清单：

| # | 位置 | v2 要求 | 票 06 是否列出 |
| --- | --- | --- | --- |
| 1 | `schemas/governance/integration-slice-index.schema.json:8` `schemaVersion` | `"1.1.0"` → `"2.0.0"` | 否 |
| 2 | 同上 `:15-16` `minItems/maxItems: 8` | **删除**（改由 g1 的连续性规则承担） | 否 |
| 3 | 同上 `:30` `integrationSliceId` pattern | `^FP-IS-[0-9]{2}$` | 否 |
| 4 | 同上 `:35-37` `sequence` `maximum: 7` | **删除 `maximum`** | 否 |
| 5 | 同上 `:41` `prerequisites.items` pattern | `^FP-IS-[0-9]{2}$` | 否 |
| 6 | 同上 `$defs.definition` | `demandRepresentation` → `authorityModel`（3.3）；`definition` 由可选改必填 | 否 |
| 7 | 同上 `$id` | URI 段随票 06 的 3.1 改 `agv-full-product/v2` | 票 06 的 3.1 已含 |
| 8 | `integration-slices/index.json` | 8 条 → **16 条**，内容见 3.1 | 票 06 第 4 条「待票 07 定」 |
| 9 | `tools/g1-validate.mjs:21-24` | 按 3.4 重写为七条家族级规则 | 票 06 第 4、5 条 |
| 10 | `runner/runner-contract.schema.json:14` | pattern 改 `^FP-IS-[0-9]{2}$`——**若该文件在 v2 存活**（1.5、第 4 问） | 票 06 第 7 条 |
| 11 | `runner/result.schema.json:13` `:71` | 同上，两处 | 否（票 06 只提了 runner-contract） |
| 12 | `8005-agv-control-server/tools/ControlServer.Conformance/Program.cs:11` | regex 改 `^FP-IS-[0-9]{2}$` | 票 06 第 8 条 |
| 13 | `8005-agv-control-server/scripts/test-wire-to-gate.ps1:4` | `[ValidatePattern]` 同上 | **否** |
| 14 | `8005-agv-control-server/scripts/test-wire-to-gate.ps1:15-23` | `$sliceVectors` 表 8 → 16 条；**并加一条与 `index.json` 的一致性校验**（1.1） | **否** |
| 15 | `8005-agv-control-server/tests/**/*.cs` | `[Trait("IntegrationSlice", ...)]` **161 处**重打标 | **否** |
| 16 | `8005-agv-control-server/scripts/run-staged-g3.ps1`、`run-staged-g3-restart.ps1`、`run-demand-bearing-g3-vectors.ps1` | 各 2 处字面量 | **否** |
| 17 | `8005-agv-program/.scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.mjs:480-490` `:494` `:500` `:510` | `slices` 表 ＋ 3 处 pattern（1.8、第 6 问） | **否**（票 06 认为生成器不存在） |

**第 14 条不只是改数量，是补一条缺失的校验。**两份切片→向量映射无人对账
已经存在于 v1，家族翻倍之后风险同步翻倍。

### 3.6 向量命名的一处遗留债，本票不改

`CV-GATE-UNLOAD-ALL-EMPTY` 与 `CV-MANUAL-CHARGING-RETURN` 里的 `GATE`
是 `WIRE_TO_GATE` 的关卡，而完整产品的六类任务有五个不同终点。
票 06 已把 20 条 v1 向量定为**沿用、不改名**，本票不推翻它——
改名会连带 `g1-validate.mjs` 的 `requiredVectors` 表、目录名与两端的证据引用，
收益只是措辞。**记为遗留债**，若将来重生成整棵树时一并处理。
切片的 `scope` 用 `DESTINATION_BATCH_UNLOAD` 而不是 `GATE_*`，那一层不欠债。

---

## 四、对其他票据的影响

### 票 08（验收边界、证据要求与分工排期）——本票交去三件事

1. **切片家族不覆盖完整产品的全部工作**，3.2 是那份清单。
   `FP-C5`／`FP-C9b`／看板本体／`RouteGraphSnapshot` 引擎是单端工程，
   **多车并发（B2）是结构上不可用保形向量证明的**（1.6）。
   这四类的验收出口形态由票 08 定。
2. **`runner/` 两个 schema 在 v2 下是修还是删，是票 08 的决定。**1.5 查实它们既无
   生产者也无消费者，且与真实向量、真实门禁结果都不兼容，而 G1 只检查它们「能编译」。
   这是票 06 那条「G2 记着 `vectorId` 却只跑自家 xunit」的**上游原因**：
   门禁结果本来就没按契约产出，契约要求的 `onboardHmiCommit`／`fakePeerIdentities`／
   `firstDivergence`／`evidencePointers` 四项——**双端联合证据的核心**——一项都没落地。
   若票 08 定「要有真跑向量的 runner」，这两个文件要按真实格式重写；
   若定「不要」，应当删除而不是留作虚假文档。
3. **门禁名称不受两仓归属交接影响。**`CONTROL_SERVER_G2`／`ONBOARD_HMI_G2`
   命名的是哪一端不是哪个人，`gates` 数组一字不改（第 4 问）。
   票 08 要回答的仍是「v2 打 tag 的第二名产品负责人是谁」（票 06 已交）。

### 票 09（批次划分与 348 行定稿）——本票交去四件事

1. **票 06 的「最大单项」估算前提是错的。**生成器存在（1.8），595 行，写整棵树，
   四个顶层常量正是 v2 要改的四项，切片家族在里面是 10 行表。
   用户已定复活并升级它。**examples 树的工作量必须重估**，
   同时要把 0.1.1 手工补的东西（`schemas/governance/` 三个文件、attestation 外置逻辑、
   `x-sorted` 语义规则、`definition` 块、`productAssertions`）补回生成器——
   **那部分才是真实提前量**，不是 1500 个文件。
2. **切片是排期的可交付单位，但只覆盖双端能力。**16 个切片各要 2 个 G2 ＋ 1 个 G3；
   3.2 那七类工作没有切片，排期时不能靠切片计数覆盖。
3. **3.1 的 `prerequisites` 是硬顺序约束**，与票 02 的重构顺序 `B2 → (B1+B4) → B3 → B5`
   并存而不冲突：前者约束联调证据的先后，后者约束不变量推翻的先后。
   **两者的交叉点是 `FP-IS-08`（B3）与 `FP-IS-09`（B5）**——切片顺序 08→09
   与不变量顺序 B3→B5 方向一致，无矛盾。
4. **161 个测试 trait 的重打标是真实工作量**（3.5 第 15 条），且它必然与
   「v2 消息面变更后逐个复核测试」合并进行。别单列成两件事。

### 票 10（规格汇编）——批次→切片映射写在规格里，不写进协议仓

**批次与切片的对应关系是本规格的内容，不是协议契约的内容**（第 2 问）。
`index.json` 只记契约事实（id、顺序、前置、向量、门禁）；
「`FP-IS-13` 属批次 N」「`FP-IS-13` 覆盖 `FP-C1` 的 19 条」这两句话写在最终规格里。
理由：批次划分是本图的计划事实，写进协议仓意味着一次重新排期变成一次协议变更，
而协议变更要作废两端的门禁证据。

规格里另须原样保留两句：**旧家族证据的引用式**（第 1 问那段引文）与
**3.2 的无切片清单**。

### 票 15（`REQ-0298` 与 `RouteGraphSnapshot` 冲突）——不受本票影响

本票不触及 `REQ-0298`，也不改变票 15 的前提。唯一相关的一点：
票 14 的 `RouteGraphSnapshot` 引擎在本票里被判为**单端工程、无切片**（3.2），
所以票 15 的结论无论走向哪边，都不会改动切片家族。

---

## 五、写回 `CONTEXT.md` 的领域词

### 5.1 改写既有词条 `IntegrationSlice`

原文把切片限定为「一段 **WIRE_TO_GATE** 跨端能力」（1.7）。完整产品的切片覆盖
自动充电、仓位配置激活、告警上报，该限定词不成立。同时补上本票新定的两条边界：
**切片只覆盖控制服务端↔车载端的双端能力**，以及**编号家族随协议大版本整体换代**。

### 5.2 新增词条 `IntegrationSliceFamily（切片家族）`

本票产出的是一个**家族**而不是若干切片，而「家族随 release 整体换代、旧家族随 tag 冻结、
旧证据只能被引用不能被复用」这三件事目前没有任何词条承载——
`ProtocolReleaseIdentity` 说的是契约身份，`ConformanceRunIdentity` 说的是单次运行身份，
中间缺的正是「某个 release 下切片编号的完整集合」这一层。

---

## 六、未证明项与悬着的事

1. **`runner/` 两个 schema 的历史意图未查。**1.5 证明了它们与现实不兼容，
   但没查它们是「写早了还没实现」还是「实现过后来偏离了」。
   `git log` 未追。交票 08 决定修或删时可一并查。
2. **生成器能否重跑未实测。**1.8 是逐行读出来的结论，**没有实际执行过**
   `node generate-protocol-candidate.mjs`。Bash 工具里没有 `node`（票 06 已记），
   且它会往目标仓写整棵树，本票不做。**票 09 重估前应当先在一次性目录里试跑一次**。
3. **3.4 的第 6、7 条规则只在 IS-01 一个实例上验证。**其余 15 个切片的
   `requiredOutcomes`／`ownerResponsibilities` token 尚不存在，规则的可满足性
   要到实施图写 `definition` 时才知道。**若某个切片写不出满足并集关系的 token，
   要回头改的是规则不是切片。**
4. **`onboardModes` 四个取值的完备性未证。**它们各对应 `CONTEXT.md` 里一条已有的
   权威边界，16 个切片都填得进去，但**没有穷举协议 v2 的 63 条消息去验证
   不存在第五种权威关系**。这与票 06 交给实施图的 `OnboardAlarmSnapshot`
   两个 enum 属同类风险——**enum 定错要发 breaking release**。
5. **车载端两份文档的过时未处置。**`ONBOARD_DEVELOPER_HANDOFF.md` 与
   `WANG_KUN_FIRST_INTEGRATION_WORK_PACKAGE.md` 按 `W2G-IS-00～07` 组织，
   仓库对 agent 只读。归 Kun Wang，随第 6 问的通知一并告知即可，本图不动。
6. **`test-wire-to-gate.ps1` 的 `$sliceVectors` 与 `index.json` 无人对账**（1.1），
   这是 v1 就存在的缺陷，本票只在 3.5 第 14 条要求 v2 补上校验，**未给 v1 开缺陷单**。

---

## 七、决策归属

按 map Notes 2026-09-04 的常设偏好，本节逐条标明哪些经用户确认、哪些由本会话自定。

### 7.1 用户 2026-09-04 明确定案的（2 条）

| # | 决策 | 位置 |
| --- | --- | --- |
| 1 | 切片家族取**替换**，前缀 `FP-IS` | 第 1、2 问 |
| 2 | v2 协议仓内容取**复活并升级生成器**，估算交票 09 | 第 6 问、1.8 |

### 7.2 本票自行定案、未经用户逐条确认（11 条）

| # | 决策 | 理由 | 选错的代价 |
| --- | --- | --- | --- |
| 1 | pattern `^FP-IS-[0-9]{2}$`，不把数量编进正则 | v1 的 `0[0-7]` 使加一个切片要改 5 处正则 | 改一次 schema |
| 2 | 批次不进 id | 1.3 的循环依赖，**这是顺序约束不是取舍** | 无（不可行） |
| 3 | 业务簇不进 id，改由 `definition.scope` 承担 | 本图已改判簇归属 5 次；id 必须比它描述的分类稳定 | 一次重命名 |
| 4 | **16 个切片**及其 `sequence`／`prerequisites`／向量绑定（3.1） | 前 8 个 1:1 沿用已被真实联调验证过的分解；后 8 个按「一次可独立联调的双端能力」切，同闭环的失败分支不单列（沿用 v1 IS-02 的先例） | 一个切片拆合，重打一批 trait |
| 5 | 切片只覆盖双端能力，单端工程不立切片（第 3 问、3.2） | 完整产品比 MVP 多出成规模的单端工程，照 MVP 粒度会无处安放 | 票 08 的验收出口要重写一节 |
| 6 | 多车并发不立切片 | 1.6 的结构性事实，**不是判断** | 无（不可行） |
| 7 | 门禁模型不增不减，现场验收不进门禁（第 4 问） | `gates` 是每切片相同的 `const`，而现场前置逐簇不同 | 一次 schema 改动 ＋ 票 08 重排 |
| 8 | `definition` 推广为全部必填 | 与票 06 把 `productAssertions` 全量必填同源：不推广则 15 个切片无可机械检查的内容 | 15 个 `definition` 块白写 |
| 9 | `demandRepresentation` → `authorityModel`，`onboardMode` 单值改数组 `onboardModes`，四个取值（3.3） | 1.4 证明原块填不进新切片；单值只在 IS-01 恰好只有一种权威关系时成立 | **enum 定错要发 breaking release**，见第 6 节第 4 项 |
| 10 | `g1-validate.mjs` 的七条家族级规则（3.4），特别是**并集关系取代逐字相等** | 逐字相等在多向量切片上无法成立；并集是它的自然推广且更强 | 规则不可满足则回头改规则 |
| 11 | `CV-GATE-*` 向量命名遗留债不改（3.6） | 票 06 已定 20 条 v1 向量沿用不改名，收益只是措辞 | 措辞债延续 |

**第 2、6 条不是设计选择**，是本票查出来的结构性事实，列在此处只为让读者知道
它们没有被交给用户。**第 9 条是本节风险最高的一条**——它是 enum，定错要发 breaking release，
且完备性未证（第 6 节第 4 项）。
