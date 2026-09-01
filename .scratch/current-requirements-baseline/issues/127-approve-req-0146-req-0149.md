# 最终批准 REQ-0146–REQ-0149：决定 RIoT 项目 API 白名单与调用安全边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-039
Approval payload SHA-256: 54e87924094ecb63c19c7a445320a16043c5122917ab79df9382cabad57d224e
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md](../../../.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-039` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0146 — 观察与计算：build 查询；地图和站点查询；可调度车辆和指定车辆状态查询；按 upperId/orderI…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0146`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 观察与计算：build 查询；地图和站点查询；可调度车辆和指定车辆状态查询；按 upperId/orderId 查询订单；以及所有已确认的无副作用路由读取，包括动态路由代价、代价单位、车辆到站 RouteCost、最近起点/终点、订单剩余路径代价和订单轨迹。具体包括当前 Facade 使用的地图/车辆/订单查询，以及 GET /api/version/v1/infos、GET /api/task/v1/task/getVehicleInfo/{deviceKey}、GET /api/task/v1/route/、GET /api/task/v1/route/curRemainCost/{orderKey}、GET /api/task/v1/route/getCostUnit、POST /api/task/v1/route/getRouteCostsBy、POST /api/task/v1/route/queryNearEnd、POST /api/task/v1/route/queryNearestStart 和 POST /api/task/v1/order/route/{vehicleKey}。使用 POST 的查询仍按无副作用语义管理；两个清除动态路由代价的 DELETE 不获批。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md](../../../.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md)；`决定 RIoT 项目 API 白名单与调用安全边界 > Answer > 当前获批调用; line 17`；来源 SHA-256 `205a1c4bd5760e3f5a50de3eec050d5d8e99eec4ab74a789e005c22bf4a9c664`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **决定／旧候选指针：** issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `54ec542499b95bf680ef0b547370c471e2866a0be6e83dcb7bd7cedb0ee13629`。

### REQ-0147 — 常规建单：只允许 POST /api/order/v1/add/byDefaultMissions 创建指定…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0147`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 常规建单：只允许 POST /api/order/v1/add/byDefaultMissions 创建指定车辆、地图和站点的单段 move；须使用稳定 upperId，并先验证车辆 ON_LINE、RouteCost 可达且该车未占用 RIoT 车辆订单名额。模板建单、订单组合、改单不获批。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md](../../../.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md)；`决定 RIoT 项目 API 白名单与调用安全边界 > Answer > 当前获批调用; line 18`；来源 SHA-256 `205a1c4bd5760e3f5a50de3eec050d5d8e99eec4ab74a789e005c22bf4a9c664`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **决定／旧候选指针：** issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `27ff023186ce5e7356470f8a35ce3ab10ccdd412d9ea4adbca7ebc3fc5e5199a`。

### REQ-0148 — 受控订单命令：只允许 POST /api/task/v1/order/command/{orderId} 的…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0148`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 受控订单命令：只允许 POST /api/task/v1/order/command/{orderId} 的 CMD_ORDER_CANCEL、CMD_ORDER_HELD、CMD_ORDER_CONTINUE_FROM_HELD 和 CMD_ORDER_CONTINUE_FROM_HANG。取消仅作用于 8005 自己创建并可关联 TransportDemand 的订单；OrderHold 可在已批准保护条件下自动触发；OrderContinue 只有在暂停原因消除、重连/未结操作对账完成、重新通过 PreDepartureSafetyCheck 且服务端生成本次明确授权后才能调用；HangContinue 只用于已批准原因白名单中的普通 HANG、受次数上限约束，未知原因和充电失败不使用。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md](../../../.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md)；`决定 RIoT 项目 API 白名单与调用安全边界 > Answer > 当前获批调用; line 19`；来源 SHA-256 `205a1c4bd5760e3f5a50de3eec050d5d8e99eec4ab74a789e005c22bf4a9c664`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **决定／旧候选指针：** issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `a2f4f88e81f505c4bfc90fd80ced8d4c0965478c3897a0bba3aeaabe1434974f`。

### REQ-0149 — 调度可用性：允许 POST /api/task/vehicles/updateVehicleIntegrat…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0149`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 调度可用性：允许 POST /api/task/vehicles/updateVehicleIntegrationLevel 的 serviceId=enable|disable。它只决定车辆是否承接后续调度：disable 不阻止建单进入 QUEUEING，也不暂停或终止当前 EXECUTING 订单；应用建单前必须独立确认 ON_LINE，并在调用后回查实际状态。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md](../../../.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md)；`决定 RIoT 项目 API 白名单与调用安全边界 > Answer > 当前获批调用; line 20`；来源 SHA-256 `205a1c4bd5760e3f5a50de3eec050d5d8e99eec4ab74a789e005c22bf4a9c664`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md。
- **决定／旧候选指针：** issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `4c3611493280ab56e85fc27611ffa3043e03e9555c7b8dec5ebbc8b7d52d7bb9`。

## Required HITL resolution

- [ ] `REQ-0146`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0147`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0148`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0149`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0146`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0147`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0148`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0149`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

机械修复说明：`REQ-0149` 已按候选总账恢复字面量 `serviceId=enable|disable`；规范文本语义、文本 SHA-256 与 Approval payload 均未改变，修正后的初始票据 SHA-256 为 `ed2ca2bb5cf19464f11e0fbe8e92d884817eac1bbfa02c2f2b44f953b9d9c2a6`。

本批准绑定批次 `V1-APP-039`、Approval payload SHA-256 `54e87924094ecb63c19c7a445320a16043c5122917ab79df9382cabad57d224e`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
