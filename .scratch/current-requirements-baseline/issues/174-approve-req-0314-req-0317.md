# 最终批准 REQ-0314–REQ-0317：决定归档 AGV 的恢复与身份连续性

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-086
Approval payload SHA-256: a9d831e008d0b6583e4d9bbe19934b07847485877209b23701b130ea3cf05cab
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-086` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0314 — 每次恢复开始新的生命周期代次。 同一 agvId 每次从归档恢复时递增 AgvLifecycleGenera…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0314`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 每次恢复开始新的生命周期代次。 同一 agvId 每次从归档恢复时递增 AgvLifecycleGeneration。当前任务和 RIoT 订单绑定、VehicleConnectionSession、消息序列、待处理指令、调度占用、结果未知调用，以及缓存的在线、位置、电量等运行态全部重置；归档前连接、订单、消息和迟到结果只能保留为旧代次历史，不能更新新代次当前状态或重新打开历史任务。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 23`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `37fa49a5066bcb54192e9549c23b29a5c3be43868e68f76eb391c171be712a44`。

### REQ-0315 — 运行态重置不清除历史，也不猜测物理事实。 任务、仓位历史、配置版本、审计和 deviceKey 映射历史不复…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0315`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 运行态重置不清除历史，也不猜测物理事实。 任务、仓位历史、配置版本、审计和 deviceKey 映射历史不复制、不迁移、不删除。仓门、占用、急停、位置等实时事实恢复后先为未知，必须重新读取；“清零”不能把未知占用推定为 EMPTY，也不能把历史结束任务改回活动状态。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 24`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `986352d82e39eb520719a52b83d9f6e958198e2e3224a595d5152deed6356992`。

### REQ-0316 — 归档前配置可以作为恢复候选。 原 ActiveSlotConfiguration 保留为候选；车载重新连接后…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0316`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 归档前配置可以作为恢复候选。 原 ActiveSlotConfiguration 保留为候选；车载重新连接后上报的 SlotModelVersion、IO 配置版本与指纹及完整 OnboardCapabilitySnapshot 与归档前记录完全一致，且没有硬件改动证据时，可继续使用原配置而不重复整车 IO 实测。版本、指纹、仓位集合或能力有任何差异、缺失或未知时，车辆保持业务未就绪，按既有 VehicleConfigurationMaintenance 完成整车 SlotConfigurationVerification 和原子激活；改变模型或硬件配置不得通过新建 agvId 绕过该流程。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 25`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `690ef368e2201fcb9f2456ab89f2a6e0e62d6089e9b3f985b88428e63c6a0790`。

### REQ-0317 — 恢复与投运严格分离。 恢复事务成功只把车辆置为未归档的新生命周期，并原子建立候选 RiotVehicleBi…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0317`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 恢复与投运严格分离。 恢复事务成功只把车辆置为未归档的新生命周期，并原子建立候选 RiotVehicleBinding 和新 VehicleCredential；最终状态固定为 Disabled 且 VehicleBusinessReadiness = false，不得接单、移动或执行仓位操作。恢复不会自动启用，检查通过也不会自动启用；后续仍须通过独立的正常启用操作明确投运。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 27`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `6c71cfa4365267707e38c03764b01e1bbf50316ad652cb8f5440a250f6b05639`。

## Required HITL resolution

- [ ] `REQ-0314`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0315`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0316`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0317`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0314`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0315`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0316`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0317`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-086`、Approval payload SHA-256 `a9d831e008d0b6583e4d9bbe19934b07847485877209b23701b130ea3cf05cab`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
