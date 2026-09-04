# 决定全量切片家族编号与 W2G-IS-00～07 的关系

Type: grilling
Status: closed
Blocked by: 06
Blocks: 08, 09

## Question

`W2G-IS-00`～`W2G-IS-07` 是 WIRE_TO_GATE MVP 的八个 integration slice，记录在 `8005-agv-protocol/integration-slices/index.json`，每个切片的 `gates` 就是两人的分工，跨仓库反馈必须带可复现的门禁证据。完整产品需要新的编号体系。

须回答：

1. **新旧关系**：新家族对既有八个切片是沿用、替换还是并存？三种各有代价——沿用会让 MVP 的门禁证据与完整产品的门禁证据混在同一编号下难以区分；替换会作废既有证据链；并存要求两套编号在同一 `index.json` 内共存且不冲突。选定一种并说明既有 MVP 证据在新体系下如何被引用。
2. **编号体系**：新切片的 ID 前缀与编号规则。`W2G-IS-*` 是 WIRE_TO_GATE 场景专用的；完整产品覆盖六类 MES 任务中的哪些、以及非搬运的充电与治理面，前缀是否仍用 `W2G`。命名必须让人一眼看出切片属哪个批次、哪个业务面。
3. **切片粒度**：一个切片对应一个批次、一个业务能力，还是一次双端联调？MVP 的粒度是「一次可独立联调并产出门禁证据的双端能力」，完整产品是否沿用同一粒度标准。
4. **门禁模型**：MVP 用 G0～G3 四道门禁绑定两端精确构建与不可改写联合证据。完整产品的门禁是沿用 G0～G3 还是需要增减？特别是：现场验收（第二台 AGV 与充电桩都已具备）在门禁模型里是新增一道，还是仍归票 08 的验收边界处理。
5. **与协议 v2 的绑定**：每个新切片绑定的 `ProtocolReleaseIdentity`、向量集合与双端 Fake 版本的表达方式。票 06 已冻结向量范围与 `vectorId` 规则，本票定切片如何引用它们。
6. **`index.json` 的变更方式**：新家族写进既有 `index.json` 还是另立文件；无论哪种，改动 `8005-agv-protocol` 都须按 notify-after-change 规则开 issue @`SocialKKKK`。本票只决定形态，不执行改动。

### 票 03 定下的 `W2G-IS-01` 改动面（本票的输入）

[票 03 决议](03-answer.md)把 B5 定为**幅度 1：只推翻 select，保留「不发现、不绑定」**。
后果落在 `W2G-IS-01` 上，且**四处联动、改一个字符 G1 就红**：

| 位置 | 内容 |
| --- | --- |
| `integration-slices/index.json:65` | `ownerResponsibilities.onboardHmi` 里的 `NEVER_DISCOVER_SELECT_OR_BIND_DEMAND` |
| `vectors/CV-DEMAND-ACCEPT-TO-PICKUP/expected.json:36` | 同名 token 出现在 `productAssertions.onboardHmi` |
| `tools/g1-validate.mjs:22-23` | 逐字断言上述两处**完全相等** |
| `vectors/CV-DEMAND-ACCEPT-TO-PICKUP/expected.json:17-25` | `forbiddenSideEffects` 里的 `onboard-demand-selection`、`onboard-demand-binding` |

**`onboardMode` 的 `READ_ONLY_COMMITTED_PROJECTION` 语义仍成立，token 可不改**：投影依然
只读，新增的是一条车载到服务端的请求，与既有 `SublotSubmitted` 结构同构。但注意它被
`schemas/governance/integration-slice-index.schema.json:108` 用 `const` 锁死为唯一合法取值，
若最终决定改它，schema 也要一起动。

还须知道：`W2G-IS-01` 是 8 个切片中**唯一带 `definition` 块**的，其余 7 个只有
id、sequence、prerequisites、vectorIds、gates、`forbidUnclosedFailOrInconclusive`。
`definition` 的 `required` 被 schema 锁为四项且 `additionalProperties: false`
（`integration-slice-index.schema.json:79-85`），**里面不可能再加别的字段**。
slice 级没有 forbidden side effects 字段，那是**向量级**的
（`runner/runner-contract.schema.json:89-95`）。

### 已知边界

- 本票不产出逐切片的验收证据清单。那是实施图的事，地图 Notes 已把顺序粒度限定在批次与切片编号层。
- 本票不改 `8005-agv-protocol` 仓库内容，不写 `index.json`。
- 本票不决定批次划分本身，那是票 09；本票定的是批次将要绑定的切片体系。
- 本票不代 Kun Wang 分配工作量。分工与排期是票 08。

## 来自票 06 的输入（2026-09-04）

**票 06 已冻结 v2 设计面，本票现在解锁。**三条硬约束，全部是本票定编号时会撞上的。

**一、`^W2G-IS-0[0-7]$` 这个 pattern 有两份副本，分属两个仓库。**
`8005-agv-protocol/runner/runner-contract.schema.json` 的 `integrationSliceId` 与
`8005-agv-control-server/tools/ControlServer.Conformance/Program.cs:11` 各写了一遍。
**本票定新编号后两处必须一起改**，漏一处的表现是一致性 runner 拒绝新切片 id。

**二、`g1-validate.mjs` 里还有六处与切片强耦合的硬编码。**第 21 行
`check(index.slices.length===8)` 加切片 id 全表 `W2G-IS-00..07`；第 22–24 行是
**W2G-IS-01 的专属断言五处**（`vectorIds` 必须恰为 `["CV-DEMAND-ACCEPT-TO-PICKUP"]`、
`requiredOutcomes` 五项精确数组、`demandRepresentation` 三字段、
`ownerResponsibilities.onboardHmi` 与向量 `productAssertions` 必须逐字相等、
adapter 轨迹三步精确数组）。切片家族一动，这六处一起动。

**注意 `ownerResponsibilities.onboardHmi` 里的 `NEVER_DISCOVER_SELECT_OR_BIND_DEMAND` 字面
必须改**（票 03 已提），而 G1 第 23 行要求它与 `CV-DEMAND-ACCEPT-TO-PICKUP` 的
`productAssertions.onboardHmi` **逐字相等**——两处一起改，否则 G1 红。

**三、向量可跨切片共享，编号体系不要假定一对一。**v1 已有三例：
`CV-OPERATION-RESULT-UNKNOWN-RECONCILE` 同属 IS-03／06／07，
`CV-SESSION-RECONNECT-DURING-RECOVERY` 同属 IS-00／05。票 06 定的 31 条向量与切片的绑定
**由本票决定**，票 06 只定了命名规则（`CV-<场景名>`，不带编号）与新增判据
（每个新增业务闭环一条，enum 扩值不单独立向量）。

**另注一处结构性事实**：`integration-slices/index.json` 里**只有 W2G-IS-01 有 `definition`
块**，其余七个切片只有 `vectorIds` ＋ `gates`。那是 0.1.1 那次修正加的。本票要判新家族是否
全部切片都带 `definition`——票 06 已把 `productAssertions` 由 IS-01 的特例推广为全部向量必填，
`definition` 是否同理推广，由本票定。

详见 [票 06 决议](06-answer.md) 的 3.6 与第四节。

---

## 决议（2026-09-04）

见 [票 07 决议](07-answer.md)。

**替换**为 `FP-IS-NN` 家族（`^FP-IS-[0-9]{2}$`），**16 个切片**：`FP-IS-00`～`07` 与
`W2G-IS-00`～`07` 一一对应作为 v2 重证，`FP-IS-08`～`15` 是新能力；票 06 的 31 条向量
全部绑定、无一落空。门禁 `G1 / CONTROL_SERVER_G2 / ONBOARD_HMI_G2 / G3` 不增不减，
现场验收不进门禁模型；`definition` 推广为全部切片必填，`demandRepresentation` 重写为
`authorityModel`；**批次与业务簇都不进 id**。

四条推翻本票据预设的事实：pattern 副本是 **9 处 ＋ 161 个测试 trait**（票据与票 06 说两处）；
票据陈述的三种代价**两种不成立、一种结构上做不到**；「一眼看出属哪个批次」是**循环依赖**
（批次由票 09 定，票 09 被本票阻塞）；`definition` 的 `demandRepresentation` **三个字段全是
`const`**，推广必然连带重写。另查出 `runner/` 两个 schema 是**无生产者无消费者且与现实
不兼容的孤儿**，以及**票 06 判为「v2 落地最大单项」的样例生成器实际存在**——在本仓
`.scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.mjs`。
