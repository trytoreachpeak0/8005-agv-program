# 最终批准 REQ-0265–REQ-0267：决定仓位模型与 IO 映射配置、验证和启用门禁

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-072
Approval payload SHA-256: e4d24b898bb1ac23e2285a8ebcad26c7458ca585877ba685af6d5956b841a14b
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-072` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0265 — 一次激活动作包含重新投运意图。 系统管理员点击激活时无需再进行第二次人工审批；车载端原子激活后，服务端只有在…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0265`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 一次激活动作包含重新投运意图。 系统管理员点击激活时无需再进行第二次人工审批；车载端原子激活后，服务端只有在实际版本与指纹、完整能力和安全状态全部一致时才自动退出配置维护态。任一项失败、冲突或未知都继续隔离。维护管理员完成核验与系统管理员完成激活可以由不同个人账号执行，也可以由具备全部权限的系统管理员独立完成，不新增双人审批链；全部操作继续遵守票据 71 的个人账号和不可改写审计规则。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 27`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `bf78691d35f10ae42bb6f9e6ea69a768611d0287a2fe65ab2ddf7e2cf82df7b9`。

### REQ-0266 — 配置审计必须可还原全过程。 在票据 71 已批准的管理员审计字段之外，仓位配置记录还必须绑定模板、模型和 I…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0266`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 配置审计必须可还原全过程。 在票据 71 已批准的管理员审计字段之外，仓位配置记录还必须绑定模板、模型和 IO 候选/生效版本及指纹、目标车辆、变更理由、变更前后内容、静态校验结果、逐仓整车核验结果、激活请求、车载实际结果和最终对账结论；失败、超时与结果未知和成功同等保留。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 29`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `1130dfa45c118032468c8d9fc6016aec234286403deadccbc878e435a0629040`。

### REQ-0267 — 8005 已批准硬件事实保持版本化不可改写。 当前 8005 全部 AGV 的八仓配置继续以 DO1～DO8…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0267`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 8005 已批准硬件事实保持版本化不可改写。 当前 8005 全部 AGV 的八仓配置继续以 DO1～DO8 对应 1～8 号物理仓位开锁、DI1～DI8 对应锁反馈、DI9～DI16 对应仓内光幕，500 ms 脉冲复位及票据 35 已批准的信号极性和机构事实为准。配置系统必须把它们表示为受控版本，而不能把普通模板资料修改变成对这些事实的静默改写；未来现场配置确有变化时只能形成新版本并保留旧版本、证据与生效历史，需求基线的变化仍遵守既有版本化治理。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 30`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `fe5ef1bf2d849d17b0f19b72d90de4c2ec6d329bb81998af364144122fadcd77`。

## Required HITL resolution

- [ ] `REQ-0265`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0266`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0267`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0265`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0266`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0267`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-072`、Approval payload SHA-256 `e4d24b898bb1ac23e2285a8ebcad26c7458ca585877ba685af6d5956b841a14b`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
