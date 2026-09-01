# 最终批准 REQ-0310–REQ-0313：决定归档 AGV 的恢复与身份连续性

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-085
Approval payload SHA-256: bbc6ab0db7181819bd22b641ed3ca1c02f6d6d3aa8f7889c83219e92ae0c1dd5
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-085` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0310 — 允许恢复，但只能恢复原车辆档案。 已归档 AGV 可以恢复；恢复必须沿用原本地 agvId，不得为同一实体车…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0310`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 允许恢复，但只能恢复原车辆档案。 已归档 AGV 可以恢复；恢复必须沿用原本地 agvId，不得为同一实体车辆创建替代档案、复制档案或以新登记绕过历史。历史任务、仓位记录、配置版本、RIoT 映射和审计继续关联同一 agvId。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 19`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `3133e8f9f8f1f3b311c47c4a76c0409db9a545d4a6cb5a496d3d3274a4e61e3c`。

### REQ-0311 — 恢复权限只属于系统管理员。 仅 SystemAdministrator 可以用个人账号发起并确认恢复，不设双…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0311`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 恢复权限只属于系统管理员。 仅 SystemAdministrator 可以用个人账号发起并确认恢复，不设双人审批或第二角色复核。MaintenanceAdministrator 与恢复流程无关，没有查看专门恢复入口、请求、核验、确认或执行恢复的权限；系统管理员权限仍不能绕过身份冲突、状态未知或安全事实门禁。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 20`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `7a3934bb6f9be34c19f6874f2f1453acc4a250c689fad69dd985f36ea10fe28c`。

### REQ-0312 — 本地 agvId 是唯一车辆身份。 AgvIdentity 由 ControlServer 首次接入时创建并…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0312`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 本地 agvId 是唯一车辆身份。 AgvIdentity 由 ControlServer 首次接入时创建并永久不变。RIoT 删除车辆后重新加入会生成新的 deviceKey，这不表示实体车辆改变，也不创建新的 agvId；车辆名称、IP、在线状态和 deviceKey 均不参与车辆身份判定。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 21`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `dc7d38e073ce00b611ad7d2174c1cda783b97215beee588c07ef2f860ed01c4e`。

### REQ-0313 — deviceKey 只形成当前 RIoT 绑定。 RiotVehicleBinding 表达一个生命周期内 …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0313`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** deviceKey 只形成当前 RIoT 绑定。 RiotVehicleBinding 表达一个生命周期内 agvId 与当前 deviceKey 的唯一映射；恢复时允许绑定新的 deviceKey，全部旧映射保留生效区间用于审计而不得覆盖。目标 deviceKey 当前已绑定另一未归档 AGV 时，恢复失败，必须先完成独立冲突处置。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md](../../../.scratch/current-requirements-baseline/issues/78-decide-archived-agv-restoration-and-identity-continuity.md)；`决定归档 AGV 的恢复与身份连续性 > Answer; line 22`；来源 SHA-256 `6a928bb715c4ab0d4e88f9cee49476b6a640e61b3345cf9d5dd1a9761befda66`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/78-decide-archived-agv-restoration-and-identity-continuity.md。
- **决定／旧候选指针：** issues/78-decide-archived-agv-restoration-and-identity-continuity.md；R03-A1102 ／ R03-A1186。
- **规范文本 SHA-256：** `5a81998a9a7d62b08fa0aad3d6f611a0217a4522105a76bdf43fa0819d1fc6c1`。

## Required HITL resolution

- [ ] `REQ-0310`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0311`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0312`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0313`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0310`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0311`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0312`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0313`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-085`、Approval payload SHA-256 `bbc6ab0db7181819bd22b641ed3ca1c02f6d6d3aa8f7889c83219e92ae0c1dd5`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
