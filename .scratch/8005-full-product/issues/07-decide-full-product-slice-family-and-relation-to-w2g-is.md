# 决定全量切片家族编号与 W2G-IS-00～07 的关系

Type: grilling
Status: open
Blocked by: 06

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
