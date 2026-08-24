# 最终批准 REQ-0318–REQ-0320：决定归档 AGV 的恢复与身份连续性

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-087
Approval payload SHA-256: 3ac3fd43716355b5edf9824b2b54fccf687aa81736b72f6538a6305a9b98f145
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-087` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0318 — 车辆离线时可以先恢复档案。 完成恢复只要求操作者为 SystemAdministrator、原 agvId …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0318`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 车辆离线时可以先恢复档案。 完成恢复只要求操作者为 SystemAdministrator、原 agvId 已归档、没有重复活动档案、目标 deviceKey 存在于正确 RIoT 环境且未绑定另一活动 AGV、新 VehicleCredential 已创建，以及新生命周期和候选绑定能够原子建立。车辆在线、凭证实际握手、配置一致性和实时安全/业务对账属于后续启用门禁；未完成或失败时车辆继续 Disabled、业务未就绪，但不重新归档。恢复事务任一步失败时原档案保持归档，候选凭证和候选绑定不得部分生效。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 28`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `81f83f9511589e15a3912ba20e4343132d1237ada635acc59cb2d9a322d8656e`。

### REQ-0319 — 业务就绪要求完整、正面的新代次证据。 启用前必须验证新 VehicleCredential 并建立新代次 V…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0319`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 业务就绪要求完整、正面的新代次证据。 启用前必须验证新 VehicleCredential 并建立新代次 VehicleConnectionSession，确认心跳和能力快照新鲜、协议版本匹配且无旧代次消息混入；确认当前 deviceKey 仍唯一绑定该 agvId、RIoT 车辆存在且在线、无未终结或结果未知的旧订单、车辆停止且位置和地图上下文可确认；确认急停状态允许运行、全部仓门锁闭、开锁输出复位、每个仓位占用均明确为 EMPTY；确认原配置一致或新配置已完成整车核验和原子激活；并确认服务端无未结任务、仓位操作、预留、调度绑定或结果未知调用。任一事实未知、冲突或发现货物时均阻断；发现货物或安全异常须进入既有异常处置，不能人工强制授予 VehicleBusinessReadiness。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 29`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `68659f5a919cd9a2e306c58432196cf114d8707a961614ebba86340a977bbb21`。

### REQ-0320 — 每次恢复尝试形成不可改写审计。 成功、失败、超时和结果未知均记录恢复尝试 ID、目标 agvId、归档原因和…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0320`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 每次恢复尝试形成不可改写审计。 成功、失败、超时和结果未知均记录恢复尝试 ID、目标 agvId、归档原因和时间、SystemAdministrator 个人账号/会话/终端/来源地址及恢复理由、原/新生命周期代次、原/新 deviceKey 和绑定检查、新 VehicleCredential 指纹与生效结果、配置候选版本和一致性判断、重复档案与 RIoT 环境检查、逐项门禁结果、请求/提交时间、失败原因和最终状态。任何秘密原值不得进入审计，任何管理员都不能修改或删除记录。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 31`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `095a8fdf49dec4524cfc24ec88ae83853da4f7babbb764eef5d1078e12c4c647`。

## Required HITL resolution

- [ ] `REQ-0318`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0319`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0320`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0318`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0319`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0320`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-087`、Approval payload SHA-256 `3ac3fd43716355b5edf9824b2b54fccf687aa81736b72f6538a6305a9b98f145`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
