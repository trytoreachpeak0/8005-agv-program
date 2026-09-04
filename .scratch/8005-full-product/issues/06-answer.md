# 票 06 决议：一次冻结协议 v2 消息面、错误码与向量范围

Status: closed
Resolved: 2026-09-04
Blocked by: 03（闭）、04（闭）、05（闭）、12（闭）、13（闭）

**本票产出「v2 设计面已冻结、可据以实施」，不产出「v2 已可发布」。**不写 Schema、样例或
向量文件，不改 `8005-agv-protocol` 仓库内容，不打 tag，不切 release。

v2 身份：**`ProtocolVersion` 2、`profileId` `AGV_FULL_PRODUCT`、release `1.0.0`**。

---

## 一、事实基础

本票开工前的自查结果。其中 1.4、1.7、1.8、1.9 四条**推翻或修正了票据正文的预设**。

### 1.1 冻结的单位是每条消息的 11 个 facet，不是「一条消息」

`manifest/release.json` 的 `messages` 对每条消息声明 11 项：`sender`、`receiver`、
`direction`、`deliveryClass`、`correlationRule`、`transportDedupKey`、`businessDedupKeys`、
`durableBeforeSend`、`durableBeforeAck`、`recoveryRole`、`schema`。54 条无一例外。

v1 现状分布：`deliveryClass` 为 RESPONSE 18、RELIABLE 16、REQUEST 12、SNAPSHOT 6、
LIVENESS 1、TELEMETRY 1；`direction` 为 C_TO_O 28、O_TO_C 23、BIDIRECTIONAL 3；
`correlationRule` 为 `MUST_BE_NULL` 35、`REQUIRED_ORIGINAL_MESSAGE_ID` 18、
`LOAD_REQUIRES_SUBLOT_CORRELATION_UNLOAD_NULL` 1；`recoveryRole` 有 19 个不同取值，
其中 `NONE` 25 条。`transportDedupKey` 恒为 `messageId`。

**少定一个 facet，实施图就要替本票做一次业务判断**——这决定了第 5 问交付物的粒度。

### 1.2 错误码注册表是封闭 enum，而且不只用于报错

`errors/error-codes.json` 43 条，`appendOnly: true`，全部 `introducedInRelease: 0.1.0`。
`schemas/common/types.schema.json#/$defs/ErrorCode` 把这 43 条写成**封闭 `enum`**。

关键是它的三个消费点：`Problem.reasonCode`（`ProtocolProblem`、`SessionRejected` 及
全部 `*Rejected`／`*Result` 用它）、**`BlockingFact.reasonCode`**（`VehicleBusinessStateSnapshot`
用它说「为什么被挡」）、**`SlotState.reasonCodes`**（`CapabilitySnapshot` 与
`SafetyStateSnapshot` 用它说「这个仓什么毛病」）。**注册表是快照的词汇表，不只是报错词汇表。**

### 1.3 两端都不做运行期 schema 校验，一致性工程只有 55 行

`8005-agv-onboard-hmi` 的 8 个 `PackageReference` 与 `8005-agv-control-server` 的 10 个
`PackageVersion` 里**没有任何 JSON Schema 校验库**。`Corvus.Json.Validator 4.6.7` 钉在
`compatibility/implementation-version-matrix.json` 里，consumers 写着「isolated .NET
conformance process」——**那个进程不存在**。

`8005-agv-control-server/tools/ControlServer.Conformance/Program.cs` 共 55 行，做的全部事情
是：校验 `--slice` 匹配 `^W2G-IS-0[0-7]$`、算 `--manifest` 文件的 SHA-256、与
`ProtocolCandidateIdentity.ManifestSha256` 比对、打印 `PREFLIGHT_PASS`。**它不跑任何向量，
不校验任何 schema。**G2 证据（`artifacts/g2/*/gate-result.json`）记着 `vectorIds` 数组与
`testExitCode: 0`——那个 exit code 来自本仓自己的 xunit 套件，**向量的 `input.ndjson` 与
`expected.json` 从未被机械执行过**，绑定靠人的断言。

### 1.4 控制服务端发出三个不在注册表里的码——而车载端 43 条全部命中

控制服务端 `src/` 全部 reasonCode 字面量只有 5 个，其中 **3 个不在那个封闭 enum 里**：

| 实际发出 | 位置 | 注册表里的对应 |
| --- | --- | --- |
| `PROTOCOL_RELEASE_MISMATCH` | `OnboardMessageProcessor.cs:82`，进 `SessionRejected` | `PROTOCOL_RELEASE_IDENTITY_MISMATCH` |
| `RECOVERY_AUTHENTICATION_REQUIRED` | `OnboardRecoveryCoordinator.cs:257`，进 `ExceptionRecoverySessionRejected` | `RECOVERY_AUTHENTICATION_FAILED` |
| `RECOVERY_SESSION_ALREADY_OPEN` | 同文件 `:278`，进 `ExceptionRecoverySessionRejected` | 无对应 |

另两个在表内：`ACTION_NOT_ALLOWED_IN_STATE`、`RECOVERY_SCOPE_MISMATCH`。

**反过来，`8005-agv-onboard-hmi` 对 43 条全部命中。**这是本图方法论第二条「零实现要分两种：
能力不存在，和能力在错误的一侧」的又一个实例，而且**这次两侧不是服务端与车载端的功能分工，
是同一个契约的遵守程度**：注册表是真的、车载端当真了，控制服务端没有。1.3 解释了它为什么
一直没被抓到——那三条消息在线上根本没人按 schema 验过。

### 1.5 43 条码里只有 10 条被任何协议资产覆盖过

1341 个 invalid 样例里 1273 个 `expected.code` 是 `PROTOCOL_SCHEMA_INVALID`（机械删必填字段
生成），其余为 `CORRELATION_INVALID` 53、`PROFILE_MESSAGE_NOT_ALLOWED` 11，加三条各 1 条，
**共覆盖 7 个码**。20 个向量里只有 3 个设了 `stableErrorCode`
（`PREDEPARTURE_CHECK_EXPIRED`、`MESSAGE_ID_CONTENT_CONFLICT`、
`SNAPSHOT_REVISION_CONTENT_CONFLICT`）。合计 **10 / 43**，其余 33 条全是业务与安全码。

### 1.6 `profileId` 改名的影响面是 1403 个文件、1509 处，不是票据写的 56／58

| 目录 | 含 `WIRE_TO_GATE_MVP` 的文件 | 出现处 |
| --- | --- | --- |
| `schemas/` | 56 | 58 |
| `examples/` | **1345** | **1450** |
| `manifest/`、`compatibility/`、`tools/` | 各 1 | 各 1 |

票据引的 56／58 只是 `schemas/`。`examples/` 共 1395 个 JSON：**valid 每消息恰好 1 个**
（`V-<Message>-MIN-001.json`），**invalid 1341 个是机械派生的**——按 `expected.rule` 分：
`required` 887、`type` 293、`semantic-correlation` 53、`enum-or-const` 41、`uniqueItems` 33、
`x-sorted` 19、`profile-denylist` 11，加四条语义各 1。

**但仓库里没有生成器。**`tools/` 只有 `finalize-manifest.mjs` 与 `g1-validate.mjs`。
这是第 5 问「实施图还欠什么」里最大的单项。

### 1.7 `g1-validate.mjs` 硬编码了 v1 的形状，票 03 的改动会直接把 G1 打红

| 行 | 硬编码内容 |
| --- | --- |
| 16 | `manifest.status==="CONTENT_SNAPSHOT"` |
| 19 | denylist 11 个名字，且每个必须有一个 invalid 样例 |
| 20 | **`requiredVectors` 20 个 id 全表** |
| 21 | **`check(index.slices.length===8)` ＋ 切片 id 全表 `W2G-IS-00..07`** |
| 22–24 | W2G-IS-01 专属断言：`vectorIds`、`requiredOutcomes`、`demandRepresentation`、`ownerResponsibilities`、adapter 轨迹 |
| 25 | **`check(worklistItems?.maxItems===1)`**、`worklistItem.required` 六字段精确数组、**顶层 `demandId` 必须支持 null** |

第 25 行那两条与票 03 的定案（`items.maxItems` 1→8）和本票的定案（顶层 `demandId` 去掉）
**直接冲突**——不同步改校验器，实施图第一次跑 `pnpm g1` 就会红在一个与它无关的地方。
`runner/runner-contract.schema.json` 的 `integrationSliceId` pattern `^W2G-IS-0[0-7]$`
与 `ControlServer.Conformance/Program.cs:11` 是同一个 regex 的两处副本。

### 1.8 版本错配是一条完整的说明性错误，不是「连接被拒而无解释」

票据正文第 4 问写「版本错配的表现是连接被拒而不是一条说明原因的错误」。**实测不成立。**
`OnboardMessageProcessor.cs:73-91` 在 `SessionHello` 分支 catch `ProtocolIdentityMismatchException`，
回 `SessionRejected`，payload 带 `problem`（reasonCode ＋ fieldPath ＋ displayMessage）、
`expectedProtocolVersion` 与完整 `expectedProtocolReleaseIdentity`。握手恒为第一条消息，
所以旧版车撞新版服务端拿到的是**完整的期望身份**。

`ValidateEnvelopeIdentity` 比对四项：`protocolVersion`、`profileId`、
`protocolReleaseManifestSha256`、`protocolReleaseVersion`。握手后的其余消息若身份不符，
异常不在该处 catch，会拆掉传输——但那条路走不到，因为握手已经拦住了。

### 1.9 `REQ-0264` 与 `REQ-0266` 本期就要指纹——票 05 交来的输入框窄了

票 05 把指纹这一项框成「`REQ-0316` 已判延后，但协议一次冻结不接受分批，现在不加将来要再发
一次 breaking」。查基线原文，**两条本期需求直接要它**：

- `REQ-0264`（票 05 已改判进 `FP-C7`，本期）：「断线、重启或结果未知时保持配置维护态，
  **必须依据车载端上报的实际版本、指纹和能力对账**，不能猜测成功。」
- `REQ-0266`（同为 `FP-C7`，本期）：「仓位配置记录还必须绑定模板、模型和 IO 候选/生效版本
  **及指纹**、目标车辆、变更理由……」

`REQ-0316`（已延后）是归档恢复那一路。所以指纹**不是为延后能力预留，是本期需求的实施前提**
——不加则 `REQ-0264` 的对账无法实施，`FP-C7` 本期做不完。这不再是权衡。
全部 54 个 schema 里 `fingerprint` 零命中。

### 1.10 `WireToGateMvpProtocolProfile` 词条的两个限定词都被完整产品推翻

`CONTEXT.md:251-253`：「**ProtocolVersion 1 中**为 WIRE_TO_GATE **单 Demand、双移动段**旅程
明确列出的必需且允许消息集合；它复用同一协议外壳和既有语义，不是新的 ProtocolVersion，
剖面外消息在该 release 中必须稳定拒绝。」完整产品是 ProtocolVersion 2、多 Demand、多停靠。
**两个限定词全不成立。**而 `ProtocolRelease` 词条正文（`:224`）里直接写着「同一
WireToGateMvpProtocolProfile 的 Schema、manifest……」，要一起改。

这与票 04、票 05 连续两次的结论一致——词条基线制定期就建齐了，**但这次是第一次发现一条
既有词条的定义被完整产品推翻，而不是缺词条**。

### 1.11 治理文档相对已打的 tag 已陈旧

`git tag` 显示 `protocol-v0.1.0` 与 `protocol-v0.1.1` **都存在**，`protocol-v0.1.1` 指向
commit `1531489e`，annotated tag message 里记着 content manifest、approval attestation、
schema bundle、vectors 四个 SHA-256。而：

- `docs/candidate-limitations.md` 仍写「其 attestation 仍为 `PENDING`；两名产品负责人必须
  批准新的精确 commit……**之后 `protocol-v0.1.1` 才能被创建**」——已经创建了。
- `manifest/release.json` 的 `status` 是 `CONTENT_SNAPSHOT`（这是 G1 第 16 行强制的，正确），
  但 `compatibility/report.json` 的 `status` 是 `SUPERSEDING_CANDIDATE`，而
  `ControlServer.Domain/ProtocolCandidateIdentity.cs` 的 `ApprovalStatus` 是
  `APPROVED_RELEASE`。三处说法不一致。

发布身份本身是健全的：tag 在、commit 在、schema bundle 与 vectors 哈希与 manifest 对得上。
陈旧的只是叙述性文档。**与票 01 查出的 `requirements-baseline-v1.0.0` tag 不存在不是同类问题**
——那是身份缺失，这是文档滞后。

---

## 二、六问定案

### 第 1 问 — 消息面：54 条沿用、5 条改、9 条新增，denylist 11 条不动

v2 的完整 allowlist = **v1 的 54 条全部沿用 ＋ 9 条新增 = 63 条**。无一条废弃。
`denylistedMessageTypes` 11 条原样沿用。

**全 63 条共同的三处身份变更**（因此每条 schema 都要改，共 56 个文件、58 处 ＋ 新增的）：
`protocolVersion` const 1 → **2**；`profileId` const `WIRE_TO_GATE_MVP` → **`AGV_FULL_PRODUCT`**；
`$id` 与全部 `$ref` 的 URI 段 `wire-to-gate/v1` → **`agv-full-product/v2`**。
`ProtocolProblem` 与 `SessionRejected` 的 `expectedProtocolVersion`／`expectedProfileId`
两个 const 同改。

**五条既有消息的 payload 变更**，逐条见第三节 3.2。

**九条新增消息**，全部取「单条 `Result` 带 `outcome` enum ＋ 可空 `problem`」范式，
不取「Accepted／Rejected 拆两条」范式，见 3.2。

**为什么 denylist 不动**：那 11 个名字记录的是「曾经设计过但明确不做」的形状，v2 的九条新增
业务能力没有一条需要它们；`OnboardCapabilitySnapshot` 虽与 `REQ-0316` 同名，但那是需求里的
概念名，不是这条被禁的消息形状。沿用还能省 11 个 invalid 样例（G1 第 19 行要求每个 denylist
名字有一个）。

**票 04 与票 12 之间有一处互相推诿，本票判给票 12。**票 04 给本票的输入第二条要求
`legType` 增 `TO_CHARGING_STATION`；票 12 的输入则说充电桩由它新加的第三维度
`StopPurposeCategory` 的 `CHARGER` 值承载、「票 04 不再向本票提第四个值」。两份输入不一致。
**判：不加 `TO_CHARGING_STATION`。**理由是票 12 的三维正交模型更晚也更结构化——
`legType`（取货/卸货）与 `publicStationFunction`（站点功能）**只在 `stopPurposeCategory`
为 `BUSINESS` 时有意义**，充电桩与等待点两者皆为 null。把充电塞回 `legType` 等于让枚举退化成
端点组合的笛卡尔积，正是票 13 拆 `stopRole` 时判定要避免的那个错误。

### 第 2 问 — 错误码与交付类别：注册表 +2 条，交付类别体系不扩

**交付类别体系一字不改。**v1 的六个 `deliveryClass`（REQUEST／RESPONSE／RELIABLE／SNAPSHOT／
LIVENESS／TELEMETRY）＋ 通用 `DurableAck` ＋ `SnapshotAppliedAck` ＋ 业务幂等 `businessDedupKeys`
＋ 五步 `RecoveryHandshake` 足以承载九条新增。新增的只有**一个 `recoveryRole` 取值**
`SLOT_CONFIGURATION`（见 3.2 第 7 条）。

**注册表增 2 条，不为控制端那 3 个表外码开口：**

| 新增码 | category | retryDisposition | allowedMessageTypes | 理由 |
| --- | --- | --- | --- | --- |
| `SLOT_CONFIGURATION_VERIFICATION_FAILED` | BUSINESS | AFTER_STATE_CHANGE | `*` | `REQ-0264` 的逐仓整车核验未过；修正后可重试 |
| `SLOT_CONFIGURATION_FINGERPRINT_MISMATCH` | BUSINESS | MANUAL_REVIEW | `*` | `REQ-0264`／`REQ-0316` 的指纹对账不符；指纹不符意味着硬件或配置被改过，必须人查 |

两条 `introducedInRelease` 均为 `1.0.0`。注册表 43 → **45**，`appendOnly` 不破。

**控制端那 3 个表外码判为实现缺陷，不是协议缺口。**`appendOnly` 允许追加，但追加等于把
实现的笔误固化成契约。处置交实施图：`PROTOCOL_RELEASE_MISMATCH` → `PROTOCOL_RELEASE_IDENTITY_MISMATCH`
（纯笔误）；`RECOVERY_AUTHENTICATION_REQUIRED` → `RECOVERY_AUTHENTICATION_FAILED`；
`RECOVERY_SESSION_ALREADY_OPEN` → `ACTION_NOT_ALLOWED_IN_STATE`（注册表无「已开」的对应码，
而「当前状态不允许该动作」正是它的含义）。

**覆盖标准按实现定，不按注册表定。**不要求 45 条各有向量——那会为 33 条没人实现的码造 33 个
向量，成本落在最没价值的地方。改为要求：**实现能发出的每个码至少有一个资产**（invalid 样例
或向量的 `stableErrorCode`）。

**并要求实施图在两端各加一条架构测试**：源码里所有 reasonCode 字面量必须属于注册表 enum。
这是本票性价比最高的一项——1.3 与 1.4 合起来说明，「协议仓的 enum」和「实现真正发出的字节」
之间目前**一条校验都没有**，而这条测试极便宜且正好抓住那三个缺陷。

### 第 3 问 — 测试向量：命名规则沿用，20 → 31 条，`productAssertions` 全量必填

**`vectorId` 命名沿用 `CV-<场景名>`（SCREAMING-KEBAB），不引入数字编号。**编号会制造「编号即
顺序」的错觉，而向量本来就跨切片共享——v1 已有三例（`CV-OPERATION-RESULT-UNKNOWN-RECONCILE`
同属 IS-03／06／07，`CV-SESSION-RECONNECT-DURING-RECOVERY` 同属 IS-00／05）。

**新增判据：每个新增业务闭环一条向量；enum 扩值、字段增删、上限放大不单独立向量。**
据此新增 11 条，20 → **31**：

| 新向量 | 覆盖 | 来源票据 |
| --- | --- | --- |
| `CV-MULTI-DEMAND-PLAN-AND-SELECT` | 多 Demand 计划 ＋ 车载选任务 ＋ 服务端裁决 | 03（B5） |
| `CV-MULTI-STOP-PICKUP-SEQUENCE` | 多停靠取货序列跑满 9 leg／8 item 上限 | 03（B3） |
| `CV-REVERSED-DIRECTION-JOURNEY` | `STAGING_TO_WIRE` 方向反转的停靠角色序列 | 13 |
| `CV-TASK-TYPE-ADMISSION-FAIL-CLOSED` | 六类任务的现场绑定缺失 → fail-closed | 13 |
| `CV-CHARGING-CYCLE-HAPPY` | 分配桩 → 前往 → 充电 → 离桩 | 04 |
| `CV-CHARGING-UNABLE-FIELD-CONFIRM` | 充不上 ＋ 现场确认闭环 | 04 |
| `CV-CHARGING-STATION-MANUAL-CLEARANCE` | 人工清桩确认闭环 | 04 |
| `CV-WAITING-POINT-IDLE-RETURN` | 空闲返回等待点，计划里出现无 Demand 的停靠 | 12 |
| `CV-SLOT-CONFIGURATION-ACTIVATION` | 配置原子激活 ＋ 指纹对账成功 | 05 |
| `CV-SLOT-CONFIGURATION-ACTIVATION-UNKNOWN` | 激活结果未知 → 保持配置维护态、不猜成功 | 05（`REQ-0264` 的核心分支） |
| `CV-ONBOARD-ALARM-SNAPSHOT` | 告警快照采用与清除 | 05 |

**绑定方式沿用 `integration-slices/index.json` 的 `vectorIds` 数组，允许跨切片共享。**
具体哪条向量属哪个切片由票 07 定，本票只定规则。

**`productAssertions` 由 W2G-IS-01 的特例推广为全部向量必填。**这是本轮唯一的实质增强：
它是**唯一**把「这条向量」和「两端各自该证明什么」接起来的字段，而 20 个里只有 1 个有
（`CV-DEMAND-ACCEPT-TO-PICKUP`，且 G1 第 23 行专门校验它与切片 `ownerResponsibilities` 一致）。
1.3 说明 G2 证据能记着 `vectorId` 却实际只跑自己的测试套——`productAssertions` 缺失正是这个
结构性缺口的一半。全量必填之后，「某条向量在某端算通过」才有可机械检查的定义。

**合法与非法样例的覆盖标准沿用 v1 的机械口径**：每条消息 1 个 valid（`V-<Message>-MIN-001`）；
invalid 按 `required`／`type`／`enum-or-const`／`uniqueItems`／`x-sorted` 逐字段派生，加
语义类（`semantic-correlation`、`profile-denylist`、`semantic-protocol-version`、
`semantic-release-identity`、`semantic-session-generation`、`unknown-message-type`）。
63 条消息预计 valid 63 个、invalid 约 1500 个。

### 第 4 问 — v1 与 v2 的版本关系：精确匹配、无协商、两端同窗口替换

**`ProtocolVersion` 2 ＋ release major `1.0.0` 不是选择，是治理强制的。**
`docs/release-governance.md` 第 9 条：「Required/type/enum/meaning/direction/delivery/dedup/
persistence/recovery/error/side-effect changes are breaking and require a ProtocolVersion and
release-major increase.」本票的变更命中其中至少七类。

**不引入版本协商，沿用「精确 ProtocolVersion ＋ 精确 ProtocolReleaseIdentity」。**
三条理由：其一，1.8 已证拒绝本身带完整期望身份，诊断信息不缺；其二，协商是 fail-open 方向的
能力，与票 05 定的「界面上只允许 fail-safe 方向动作」同源，协议面上更该守；其三，三台车，
同窗口替换的运维代价近乎为零，而协商能力自己要设计、要向量、要两端实现。

**切换规则**（写进规格，实施图照此执行）：

1. v2 的服务端与车载端**打进同一个 CD 包**——`remote-ops/factory-server/docs/wire-to-gate-cd.md`
   的现有约束在 v2 下继续成立，理由不变（两端无协商无降级，版本错配的表现是连接被拒）。
2. 服务端先停，两端同窗口替换，车逐台人工启动（车载端「搬完就停、不启动」的现有约束不变）。
3. 替换窗口内旧版车一律被 `SessionRejected` 拒绝并带期望身份。**这是可接受的**——它是显式的、
   带诊断的、fail-closed 的。
4. `ControlServer.Domain/ProtocolCandidateIdentity.cs` 的 9 个常量全部换成 v2 的值；
   车载端对应处同理。

### 第 5 问 — 冻结强度：设计面已冻结、可据以实施；交付物边界如下

本票交付**第三节**，即：v2 身份三元组、逐消息 11 facet 的变更与新增全表、类型层变更、
错误码增量、向量清单与规则、**必须同步修改的门禁硬编码清单**、以及实施图还欠什么。

**硬编码清单必须进交付物**——1.7 说明不给它，实施图第一次跑 G1 就会红在一个与它无关的地方。

**实施图拿到本票产出后还欠七件事才能切一个 `ProtocolRelease`**，见第三节 3.7。其中最大的
单项是 examples 树：约 1500 个 invalid 样例是机械派生的但**仓库里没有生成器**（1.6）。

### 第 6 问 — 发布与通知：本票不改治理规则，双人签名的「第二人」交票 08

**本图不产生 release。**本票的结论推送后，按 notify-after-change 规则在 `8005-agv-protocol`
开 issue @`SocialKKKK`，说明三件事：改了什么（v2 设计面已冻结，尚未落地为文件）、触及哪些
`W2G-IS-*` 切片（**全部八个**——身份三元组变更命中每条消息）、他的 `ONBOARD_HMI_G2` 证据
是否作废（**v2 落地并打 tag 之后全部作废；本票本身不作废任何证据**，因为它不改仓库内容）。

**双人签名规则一字不改。**`docs/release-governance.md` 要两名不同产品负责人签 attestation，
G1 第 27 行实打实校验 `new Set(approvals.map(a=>a.ownerId)).size===2`，AI 与 CI 不能批准。

**用户 2026-09-04 告知：`8005-agv-onboard-hmi` 与 `slots-simulator` 今后由我方负责开发。**
本票的处置：

1. **这是将来的开发归属变更，不是现在的写权限变更。**工作区 `CLAUDE.md` 的写权限表在用户明确
   改它之前照旧，那两个仓对 agent 仍然只读。
2. **交接的是那两个仓的开发，不是 `8005-agv-protocol` 的所有权。**Kun Wang 仍是协议共同维护者，
   在交接完成前他就是那第二名产品负责人。
3. **v2 打 tag 前必须确定第二名产品负责人是谁——交票 08。**两端都归一边写之后，双人签名的价值
   **变大而不是变小**：它从此是唯一一个外部评审点。
4. 不改 `release-governance.md`。改它等于自我豁免 map Notes 里「不代签任何 protocol release」
   「不以 AI／CI 充当两名产品负责人之一」两条。

**1.11 的文档陈旧一并列进 v2 冻结的处置清单**：`docs/candidate-limitations.md` 关于
「`protocol-v0.1.1` 尚不能创建」的整段作废重写；`compatibility/report.json` 的 `status`
与 `ProtocolCandidateIdentity.ApprovalStatus` 的口径统一。

---

## 三、v2 冻结面（交付物本体）

### 3.1 身份三元组与 URI

| 项 | v1 | v2 |
| --- | --- | --- |
| `protocolVersion` | 1 | **2** |
| `profileId` | `WIRE_TO_GATE_MVP` | **`AGV_FULL_PRODUCT`** |
| `releaseVersion` | `0.1.1` | **`1.0.0`** |
| schema `$id`／`$ref` URI 段 | `wire-to-gate/v1` | **`agv-full-product/v2`** |
| tag | `protocol-v0.1.1` | `protocol-v1.0.0` |

`AGV_FULL_PRODUCT` 与 `WIRE_TO_GATE_MVP` 同构——**阶段名，不带版本号**，版本活在
`protocolVersion` 与 `protocolReleaseVersion` 里。URI 段一并改是因为留着 `wire-to-gate`
会重新制造名实不符，而它只在 60 个 schema 文件里出现、examples 不含 `$id`，改起来便宜。

### 3.2 消息面全表

**A. 沿用且 payload 一字不改：49 条。**除下面 B 段列出的 5 条外的全部 v1 消息，只随 3.1 改
身份三元组与 URI。其中 `ManualChargingReturnToServiceRequested`／`Result` **保留在 allowlist
并要求实现**（票 04 定案；当前两端 `src/` 与 `tests/` 均零命中，属实施缺口不属协议缺口）。

**B. payload 变更：5 条。**

**B1 `UpcomingStopPlanSnapshot`**（C_TO_O／SNAPSHOT）

| 变更 | v1 | v2 |
| --- | --- | --- |
| 顶层 `demandId` | `Id \| null`，必填 | **去掉** |
| `legs.maxItems` | 2 | **9** |
| `legs[].sequence.maximum` | 2 | **9** |
| `legs[].legType` | enum `["TO_PICKUP","TO_GATE"]`，必填 | **`["TO_PICKUP","TO_DROPOFF"] \| null`**，仅 `BUSINESS` 下非空 |
| `legs[]` 新增 `stopPurposeCategory` | — | enum **`["BUSINESS","WAITING_POINT","CHARGER"]`**，必填 |
| `legs[]` 新增 `demandId` | — | **`Id \| null`**，必填；null = 该停靠不由 Demand 引起 |
| `legs[]` 新增 `publicStationFunction` | — | 五值 enum ＋ null，仅 `BUSINESS` 下非空 |
| `businessDedupKeys` | `["demandId"]` | **`["planRevision"]`** |

`legs[].movementLegId`／`stationId`／`mapId`／`state` 不变，`x-sortedBy: sequence` 与
`uniqueItems` 不变。**逐 leg 的可空 `demandId` 是票 12 那句「计划里可以有不由
`TransportDemand` 引起的停靠」在 schema 上的表达**，也是 B1 不变量在协议面上的实质落点。

**dedup 键改用 `planRevision` 的理由**：`SNAPSHOT_REVISION_CONTENT_CONFLICT` 这个码存在的
意义就是「同一 revision 必须同一内容」，快照用 revision 作业务幂等键才与它自洽；而多 Demand
之后「这份计划属于哪个 Demand」没有答案。

**B2 `CurrentStopWorklistSnapshot`**（C_TO_O／SNAPSHOT）

| 变更 | v1 | v2 |
| --- | --- | --- |
| `items.maxItems` | 1 | **8** |
| 顶层 `operationSessionId` | `Id \| null`，必填 | **下移到 `items[]`**，顶层去掉 |
| `items[].workType` | const `"WIRE_TO_GATE"` | **六值 enum，MES 原始字面值** |
| `items[].stopRole` | enum `["PICKUP","GATE"]` | **`["PICKUP","DROPOFF"]`** |
| `items[]` 新增 `publicStationFunction` | — | **五值 enum**（`REQ-0324`），必填 |
| `businessDedupKeys` | `["items[].demandId","items[].transportDemandKey"]` | **`["worklistRevision"]`** |

六值 enum 取值：`DIE_TO_WIRE_STAGING`、`DIE_TO_OVEN`、`WIRE_TO_GATE`、`WIRE_TO_OPTICAL`、
`STAGING_TO_WIRE`、`WIRE_TO_NITROGEN`（票 13：`REQ-0003` 定正式 SQL 是唯一查询原稿，
自造映射就要同步维护）。

`items` **不加 `minItems`**——v1 本来就没有，空数组合法，多 Demand 化不需要为「空清单」另做
处理（票据正文已核实）。`items[].expectedBasketCount` 的 `maximum: 8` 不变。

**dedup 键改用 `worklistRevision` 的理由（本票发现，票 03 未提）**：`items[].demandId` 这种
数组内寻址的键在 `maxItems: 1` 下是单值的，1→8 之后变成多值键，**dedup 语义无定义**。
与 B1 统一为 revision。

**B3 `CapabilitySnapshot`**（O_TO_C／SNAPSHOT）

| 变更 | v2 |
| --- | --- |
| 新增 `activeSlotConfigurationFingerprint` | `Sha256`，必填 |
| `slotStates` | **`minItems: 8, maxItems: 8` 不变** |

一个指纹字段覆盖 `REQ-0264`／`REQ-0266`／`REQ-0316` 三条的需要——它是**已生效整车配置的
指纹**，与既有的 `activeSlotConfigurationVersion` 配对，命名同源。不为 `slotModelVersion`
另加指纹：模型版本是已发布标识，配置才是需要防静默改写的那一层（`REQ-0267`）。

**B4 `SafetyStateSnapshot`**（O_TO_C／SNAPSHOT）：payload 不改。列在此处只为记录
**`slotStates` 的定长 8 出现在两条消息里**，Q6 的定案同时覆盖两处。

**B5 `VehicleBusinessStateSnapshot`**（C_TO_O／SNAPSHOT）

| 变更 | v1 | v2 |
| --- | --- | --- |
| `batteryState` | `["SUFFICIENT","LOW","UNKNOWN"]` | **增 `MANDATORY_CHARGE`**，四值 |
| 新增 `chargingCycleState` | — | enum `["NOT_CHARGING","ALLOCATED","EN_ROUTE","CHARGING","COMPLETE","UNABLE_TO_CHARGE","UNKNOWN"]`，必填 |
| `manualChargingHold` | boolean | **一字不动，含义不变** |

`batteryState` 只表达「电量档位」一个概念，`chargingCycleState` 表达「充电周期到哪一步」，
两者正交。合并会重犯票 13 拆 `stopRole` 时判定要避免的笛卡尔积错误。`MANDATORY_CHARGE` 对应
`REQ-0281` 的强制充电阈值。**`manualChargingHold` 保留原义作为「充电桩名册为空」那一态的载体**
（票 04 的 Q3）——含义变更在字段名不变时两端都静默编译，是最坏的一种 breaking。

**C. 新增 9 条。**全部取「单条 `Result` 带 `outcome` enum ＋ 可空 `problem`」范式
（范式来自 `ManualChargingReturnToServiceResult`），不取「Accepted／Rejected 拆两条」范式
——后者要多 4 条 schema、4 个 valid 样例、约 100 个 invalid 样例，而 v1 已证单条形态装得下。

| # | 消息 | dir | deliveryClass | correlationRule | recoveryRole | businessDedupKeys | durableBeforeSend / BeforeAck |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `DemandSelectionRequested` | O_TO_C | REQUEST | `MUST_BE_NULL` | NONE | `requestId`,`demandId` | false / false |
| 2 | `DemandSelectionResult` | C_TO_O | RESPONSE | `REQUIRED_ORIGINAL_MESSAGE_ID` | NONE | `requestId` | false / false |
| 3 | `UnableToChargeFieldConfirmationRequested` | O_TO_C | REQUEST | `MUST_BE_NULL` | NONE | `requestId` | false / false |
| 4 | `UnableToChargeFieldConfirmationResult` | C_TO_O | RESPONSE | `REQUIRED_ORIGINAL_MESSAGE_ID` | NONE | `requestId` | false / false |
| 5 | `ManualStationClearanceConfirmationRequested` | O_TO_C | REQUEST | `MUST_BE_NULL` | NONE | `requestId` | false / false |
| 6 | `ManualStationClearanceConfirmationResult` | C_TO_O | RESPONSE | `REQUIRED_ORIGINAL_MESSAGE_ID` | NONE | `requestId` | false / false |
| 7 | `SlotConfigurationActivationCommand` | C_TO_O | **RELIABLE** | `MUST_BE_NULL` | **`SLOT_CONFIGURATION`** | `activationId` | **true / true** |
| 8 | `SlotConfigurationActivationResult` | O_TO_C | **RELIABLE** | `MUST_BE_NULL` | **`PENDING_RESULT_REPLAY`** | `activationId` | **true / true** |
| 9 | `OnboardAlarmSnapshot` | O_TO_C | **SNAPSHOT** | `MUST_BE_NULL` | NONE | `alarmStateRevision` | false / false |

`transportDedupKey` 九条均为 `messageId`（与 v1 全表一致）。

**1／2 的 payload 要点**：`DemandSelectionRequested` 载 `requestId` ＋ `demandId` ＋
`worklistRevision` ＋ **五字段回显**（完整 SUBLOT、`workType`、起点、终点、`ExpectedBasketCount`）
（票 03）。`DemandSelectionResult` 的 `outcome` 取 `["ACCEPTED","REJECTED"]`，
拒绝原因用既有码 `WORKLIST_REVISION_STALE`／`DEMAND_NOT_CURRENT`／`VEHICLE_NOT_READY`／
`ACTION_NOT_ALLOWED_IN_STATE`，**不新增码**。

**3～6 的 payload 要点**：形状照抄 `ManualChargingReturnToServiceRequested`——`requestId`
（幂等）＋ `administrator`（`OperatorContext`）＋ `administratorRole`（enum
`MAINTENANCE_ADMINISTRATOR`／`SYSTEM_ADMINISTRATOR`，**保持原义不动**）＋ `reason`，
另加 `chargingStationId`。`Result` 的 `outcome` 取 `["CONFIRMED","REJECTED"]`。
**这四条落在车载端是因为票 04 的分端判据「动作的对象里有没有车」**——有车说明人在车旁。
只有桩的两个动作（`ChargingStationAllocationHold`、`ChargingStationRecoveryConfirmation`）
留在 ControlServer 侧，**不进协议**。

**7／8 的 payload 要点**：`SlotConfigurationActivationCommand` 载 `activationId` ＋
`slotModelVersion` ＋ `activeSlotConfigurationVersion` ＋ **`activeSlotConfigurationFingerprint`** ＋
完整 `SlotIoBinding` 集合。`Result` 载 `activationId` ＋ `outcome`
（`["ACTIVATED","VERIFICATION_FAILED","REJECTED"]`）＋ 可空 `problem` ＋
**车载实际生效的 `activeSlotConfigurationVersion` 与 `activeSlotConfigurationFingerprint`** ＋
`capabilityVersion`。

**为什么 7／8 必须是 RELIABLE 而不是 REQUEST／RESPONSE**：`REQ-0264` 写「断线、重启或结果未知
时保持配置维护态，必须依据车载端上报的实际版本、指纹和能力对账，不能猜测成功」——这正是
`PENDING_RESULT_REPLAY` 与 `durableBeforeSend`／`durableBeforeAck` 存在的理由。用 RESPONSE
就没有补报语义，断线即丢，`REQ-0264` 无法实施。`SLOT_CONFIGURATION` 是新增的 `recoveryRole`
取值，**它进 `RecoveryHandshake` 的第三步**（上报未结操作与恢复检查点）——未结的配置激活
与未结的仓位操作同类。

**9 的 payload 要点**：`alarmStateRevision`（`Revision`）＋ `observedAt` ＋ `alarms` 数组。
每个告警条目：`alarmCode`（**开放字符串，不用 `ErrorCode`**）＋ `category`（enum）＋
`severity`（enum）＋ `subjectType` ＋ 可空 `subjectId` ＋ `raisedAt`。走通用
`SnapshotAppliedAck`。

**为什么告警走快照而不是事件流**：`REQ-0269` 写「不可取得当前事实时直接表达原因，**不引入
『已过期』展示状态**……主看板不得继续把最后一次成功值呈现为当前值」。**快照 ＋ revision 天然
满足，事件流不满足**——事件流断线重连后必须靠补发对账才知道当前哪些告警未清，中间那段正是
「最后一次成功值」。协议里已有三处成熟的快照范式（能力、安全、车辆业务态），
`SNAPSHOT_REVISION_REGRESSION` 与 `SNAPSHOT_REVISION_CONTENT_CONFLICT` 两个码也已在表内。

**为什么不扩 `SafetyStateSnapshot`**：安全态有门禁后果，普通告警没有；混在一起会让
`safetyStateVersion` 因一条无关告警而跳版本，而 `SAFETY_STATE_VERSION_GAP` 是要触发对账的。

**为什么告警 code 不复用 `ErrorCode`**：告警是开放集合（硬件故障码由车厂定），塞进封闭 enum
等于每加一个故障码就发一次 breaking release，而一次 breaking release 作废两端全部 G1/G2/G3
证据。这是本票唯一一处**故意不复用既有词汇表**的地方。

### 3.3 类型层变更（`schemas/common/types.schema.json`）

| `$defs` | 变更 |
| --- | --- |
| `ErrorCode` | enum 43 → **45**（见 3.4） |
| `SlotNo` | `maximum: 8` **不变** |
| `SlotState` | 不变（`reasonCodes` 仍用 `ErrorCode`） |
| `BlockingFact` | 不变（`reasonCode` 仍用 `ErrorCode`） |
| `OperatorContext` | 不变。`verificationMethod` 的 `["BADGE","SESSION"]` 保留字段位，票 05 已定甲档下值填部署标识 |
| 新增 `StopPurposeCategory` | enum `["BUSINESS","WAITING_POINT","CHARGER"]` |
| 新增 `PublicStationFunction` | 五值 enum（`REQ-0324`：派工待送、烘箱、关卡、三光、氮气柜） |
| 新增 `TransportTaskType` | 六值 enum，MES 原始字面值 |
| 新增 `AlarmEntry` | 见 3.2 第 9 条 |

新增四个 `$defs` 而不是在消息 schema 里内联，是因为 `StopPurposeCategory` 与
`PublicStationFunction` 各自要出现在两条消息里（计划快照与工作清单快照），内联会制造第二份
真相——这正是 54 份内联信封副本已经造成的问题。

### 3.4 错误码增量

注册表 43 → **45**，两条新增见第 2 问。**不为控制端那 3 个表外码开口**，判为实现缺陷。
**新增一条门禁要求交实施图**：两端各加一条架构测试，断言源码里所有 reasonCode 字面量属于
注册表 enum。

### 3.5 向量清单与规则

见第 3 问。20 → **31**，命名规则不变，`productAssertions` 全量必填，切片绑定由票 07 定。

### 3.6 必须同步修改的门禁硬编码清单

**不改这些，实施图第一次跑 G1 就会失败在与它无关的地方。**

| # | 位置 | 现状 | v2 要求 |
| --- | --- | --- | --- |
| 1 | `tools/g1-validate.mjs:16` | `manifest.status==="CONTENT_SNAPSHOT"` | 保留不动 |
| 2 | `tools/g1-validate.mjs:19` | denylist 11 名 | 保留不动 |
| 3 | `tools/g1-validate.mjs:20` | `requiredVectors` 20 个 id | 改为 **31 个** |
| 4 | `tools/g1-validate.mjs:21` | `slices.length===8` ＋ 切片 id 全表 | **待票 07 定** |
| 5 | `tools/g1-validate.mjs:22-24` | W2G-IS-01 专属断言五处 | 随票 07 的切片家族重写 |
| 6 | `tools/g1-validate.mjs:25` | **`worklistItems?.maxItems===1`**、`worklistItem.required` 六字段、**顶层 `demandId` 支持 null** | **必改**，与 B1／B2 直接冲突 |
| 7 | `runner/runner-contract.schema.json` | `integrationSliceId` pattern `^W2G-IS-0[0-7]$` | **待票 07 定** |
| 8 | `8005-agv-control-server/tools/ControlServer.Conformance/Program.cs:11` | 同一 regex 的第二份副本 | 同 7；**两处必须一起改** |
| 9 | `8005-agv-control-server/src/ControlServer.Domain/ProtocolCandidateIdentity.cs` | 9 个 v0.1.1 常量 | 全换 v2 值 |
| 10 | `8005-agv-control-server/appsettings.json:9` | `ProtocolCandidate.profileId`，`src/` 内查不到任何读取 | **删除该配置项**，不是绑定它 |

第 10 条的判定理由：`ProtocolCandidateIdentity` 用编译期常量**正是对的设计**——协议身份必须
与构建绑定，不能靠部署配置漂移。那个 `appsettings.json` 键是一个会静默漂移的第二份真相，
删掉即可。票 13 交来「本票或实施图择一处置」，**本票判：删，交实施图执行**。

### 3.7 实施图还欠什么才能切一个 `ProtocolRelease`

1. 写 schema：54 条改身份三元组 ＋ 5 条改 payload ＋ 9 条新增 ＋ 类型层 4 个新 `$defs`，
   约 63 个消息文件 ＋ `envelope`／`types`／`bundle`。
2. **重生成 examples 树：63 个 valid ＋ 约 1500 个 invalid。**invalid 是机械派生的但
   **仓库里没有生成器**（1.6）——要么重建生成器，要么手写。**这是最大的单项。**
3. 写 31 个向量的 `input.ndjson` ＋ `expected.json`，全部带 `productAssertions`。
4. 改 3.6 的十处硬编码。
5. `pnpm manifest:finalize` ＋ `pnpm g1` 跑绿。
6. **两名产品负责人的外部 attestation ＋ annotated tag `protocol-v1.0.0`**（第 6 问）。
7. 两端实现 ＋ `CONTROL_SERVER_G2` ＋ `ONBOARD_HMI_G2` ＋ `G3`。

第 2 项与第 7 项是真实提前量，票 09 排批次时不得漏。

---

## 四、对其他票据的影响

### 票 07（切片家族编号与 W2G-IS-00～07 的关系）——现在解锁，且带三条硬约束

1. **`^W2G-IS-0[0-7]$` 这个 pattern 有两份副本**（`runner/runner-contract.schema.json` 与
   `ControlServer.Conformance/Program.cs:11`），票 07 定新编号后**两处必须一起改**，
   而它们分属两个仓库。
2. **`g1-validate.mjs:21` 硬编码 `slices.length===8`**，第 22–24 行还有 W2G-IS-01 的专属断言
   五处。切片家族一动，这六处一起动。
3. 31 条向量与切片的绑定由票 07 定；**向量可跨切片共享**（v1 已有三例），编号体系不要假定
   一对一。

### 票 08（验收边界与两人分工）——前提被交接改写

1. **`8005-agv-onboard-hmi` 与 `slots-simulator` 今后由我方开发**（用户 2026-09-04）。
   票 08 原本的「两人分工」前提要重写。
2. **v2 打 tag 需要两名不同产品负责人签 attestation，AI／CI 不能批准，G1 实打实校验
   `size===2`。**两端都归一边写之后「第二人是谁」成了硬前提——**这是票 08 必须回答的**。
   本票的判断：交接完成前 Kun Wang 就是那个人（交接的是那两个仓的开发，不是协议的所有权）。
3. **G2 证据的可信度问题**：1.3 查实 G2 记着 `vectorId` 却实际只跑本仓 xunit 套件，向量从未被
   机械执行。`productAssertions` 全量必填（第 3 问）把这个缺口补了一半，另一半——**谁来跑
   向量**——是票 08 的验收出口要回答的。

### 票 09（批次划分与 348 行定稿）

1. **协议 v2 是一个横切大件，跨全部簇**，与票 14 的 `RouteGraphSnapshot` 引擎并列。真实提前量
   在 3.7 的第 2 项（约 1500 个样例、无生成器）与第 7 项（两端实现 ＋ 三道门禁）。
2. **v2 必须先于任何跨端能力上线**，但它内部可与服务端侧的单端工作并行。
3. **三条实现缺陷交票 09 排期**：控制端 3 个表外错误码（第 2 问）、
   `ManualChargingReturnToServiceRequested`／`Result` 两端零实现（票 04 已定要求实现）、
   `appsettings.json:9` 的死配置（3.6 第 10 条）。
4. **两条新的架构测试**：reasonCode ∈ 注册表（两端各一条）。

### 票 10（规格汇编）

1. v2 的身份三元组、63 条消息面、45 条错误码、31 条向量进最终规格。
2. **1.11 的治理文档陈旧**（`candidate-limitations.md`、`compatibility/report.json` 的
   `status`、`ProtocolCandidateIdentity.ApprovalStatus` 三处口径不一）与票 01／12 查出的
   「需求文本引用位置不稳的外部身份」同属汇编前须有结论的一类，但**不同源**——那三条是身份
   缺失，这一条是文档滞后于已发生的事实。
3. 最终规格须如实记录：**车载端开发同事未评审、未批准 v2 设计面**；notify-after-change 的
   issue 是通知不是批准。

### 票 15（`REQ-0298` 与 `RouteGraphSnapshot` 冲突）——本票给它添了一个反向数据点

票 15 的第 3 问要判「要不要对 348 条做一次专门的冲突复核」，而那块迷雾分两个检出面：
「剖面判定错误」（票 09 逐条复核 ＋ 影响串分组，两层覆盖）与「需求文本含禁止性设计约束」
（无任何票据系统性覆盖）。

**本票给后一面添了第一个反向数据点**：1.9 查出 `REQ-0264`／`REQ-0266` 的原文里各有一个
名词（「指纹」）**要求了一个协议上不存在的字段**——这不是禁止性约束，是**遗漏性约束**，
方向与 `REQ-0298` 相反但检出手段相同（逐条读基线文本）。这说明那一面的复核收益比票 15 目前
估计的更高：它不只能查出「需求禁止了我们要做的事」，还能查出「需求要求了我们没有的东西」。
本票的手段是**读需求原文里的具体名词与动词**，与票 05 方法论第三条同源。

---

## 五、写回 `CONTEXT.md` 的领域词

**新增一条**，因为 1.10 查实既有词条的定义被完整产品推翻：

**AgvFullProductProtocolProfile（完整产品协议剖面）**：ProtocolVersion 2 中为 8005 完整产品
明确列出的必需且允许消息集合，覆盖六类运输任务、多车、多 Demand 多停靠、自动充电、等待点、
仓位配置激活与告警上报；它复用同一协议外壳和既有语义，剖面外消息在该 release 中必须稳定拒绝。
_Avoid_：WireToGateMvpProtocolProfile、另建第三个协议版本、未声明消息也尽量接受。

**改两条既有词条**：

1. `WireToGateMvpProtocolProfile`（`:251-253`）加一句 `_Note_`：它是 ProtocolVersion 1 的剖面，
   完整产品由 `AgvFullProductProtocolProfile` 承载，两者不是同一个剖面的两个版本。
2. `ProtocolRelease`（`:223-225`）正文「包含同一 WireToGateMvpProtocolProfile 的 Schema……」
   改为「包含同一协议剖面的 Schema……」——原文把一个具体剖面名写进了通用词条的定义里。

**不新增其他词条。**`StopPurposeCategory`、`PublicStationFunction`、`TransportTaskType`
三个 schema 类型的概念在 `CONTEXT.md` 中已有对应词条（票 12、票 13 已处置），本票只把它们
落到协议类型层，不重复立词。

---

## 六、未证明项与悬着的事

1. **`protocol-v0.1.1` 的 attestation 是外部 GitHub Release Asset，本会话未核验其内容。**
   tag message 里记着它的 SHA-256（`89f67c82…`），结构上流程走过了，但**两名批准人是谁、
   签名是否真实存在，本票未证**。v2 打 tag 前应核验一次 v0.1.1 的资产还在。
2. **约 1500 个 invalid 样例的生成器不在仓库里。**v1 是怎么生成它们的，无从得知；重建生成器
   的工作量本票未估。
3. **`OnboardAlarmSnapshot` 的告警条目字段是本票设计的，没有需求逐字对应。**`REQ-0270` 只说
   「全部 8005 告警集中显示在 ControlServer」，没规定告警的结构。`category` 与 `severity`
   两个 enum 的具体取值本票未定，交实施图——**但它们是 enum，定错要发 breaking release**，
   实施图落地前应回头确认一次。
4. **车载端告警的来源面本票未查。**只查了协议 schema 里 `Alarm`／`Alert` 零命中（票 05 的
   结论），**没查车载端 `src/` 里现有的故障码采集面**。那两个 enum 的取值应当从车载端已有的
   采集面推导，而不是凭空定。这是 map Notes 第 23 条的又一个适用点。
5. **`chargingCycleState` 的七个取值是本票定的**，票 04 定了充电全链路但没有逐状态列举。
   同上，enum 定错要发 breaking release。
6. **两端的架构测试（reasonCode ∈ 注册表）本票未写也未验证可行性。**控制端读注册表 JSON
   需要一份副本或一条构建期拷贝，机制本票未定。
7. **交接后「第二名产品负责人」是谁，未定**——交票 08，是 v2 打 tag 的硬前提。

---

## 七、决策归属

按用户 2026-09-04 的要求（「不想关心设计细节」），本票的决策分两类，如实记录：

**用户定案的六条**（范围、代价与不可逆方向）：冻结强度取设计面（第 5 问）；不引入版本协商、
两端同窗口替换（第 4 问）；`profileId` 改名并新立词条（3.1、第五节）；`CapabilitySnapshot`
加指纹（B3）；错误码取「不为表外码开口 ＋ 覆盖按实现定 ＋ 加架构测试」（第 2 问）；
`slotStates` 保持定长 8（B4）。

**本票自行定案、未经用户逐条确认的**：九条新增消息的命名与配对范式（3.2 C）；告警走快照而非
事件流、告警 code 不复用 `ErrorCode`（3.2 第 9 条）；`batteryState` 增 `MANDATORY_CHARGE` 与
`chargingCycleState` 单列（B5）；`UpcomingStopPlanSnapshot` 顶层 `demandId` 去掉、逐 leg 可空、
dedup 改 `planRevision`（B1）；`CurrentStopWorklistSnapshot` dedup 改 `worklistRevision`（B2）；
向量命名规则与 31 条清单、`productAssertions` 全量必填（第 3 问）；不改 `release-governance.md`
（第 6 问）；票 04 与票 12 的 `legType` 推诿判给票 12（第 1 问）；`appsettings.json:9` 判删
（3.6 第 10 条）；类型层新增四个 `$defs`（3.3）。

第六节的 3、4、5 三条是这一类里**风险最高的**——它们是 enum，定错要发一次 breaking release，
而一次 breaking release 作废两端全部门禁证据。实施图落地前应回头确认。
