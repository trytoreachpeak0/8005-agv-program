# 最终批准 REQ-0174–REQ-0177：决定无联网充电桩的充电失败确认与暂停触发边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-047
Approval payload SHA-256: 5c904f0e27fdfde9dd0b6d1d6ae95e1d2a68fb206f3b5e33a54e05b1a809ea93
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-047` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0174 — “已确认充不上”可由严格系统事实自动形成。 车辆、订单、预占和目标充电桩身份必须一致；车辆已到精确的 RIo…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0174`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** “已确认充不上”可由严格系统事实自动形成。 车辆、订单、预占和目标充电桩身份必须一致；车辆已到精确的 RIoT 地图 + 站点并执行开始充电；RIoT 完成内部重试后返回已经目标 build/契约验证的失败码（当前证据为 407802）且订单最终进入 HANG；全程无 batteryState=CHARGING 或成功结果，所有事实新鲜、连续且无冲突。该事实不对车辆或充电桩归责。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)；`决定无联网充电桩的充电失败确认与暂停触发边界 > Answer; line 32`；来源 SHA-256 `3cc41b2331675a2c3ed12295668b2e67b50691932a18aceafa8d9df079b8db9e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **决定／旧候选指针：** issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `884c5af99269517c20877b421daad89d01ed566903f768126b88294991b47678`。

### REQ-0175 — 一般充电类异常不得误触发暂停。 单独 HANG、超时、未到桩、导航不可达、车辆不可执行、自由文本失败提示、订…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0175`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 一般充电类异常不得误触发暂停。 单独 HANG、超时、未到桩、导航不可达、车辆不可执行、自由文本失败提示、订单异常或结果未知都不足以确认充不上，必须保持原事实并进入对应异常分支。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)；`决定无联网充电桩的充电失败确认与暂停触发边界 > Answer; line 33`；来源 SHA-256 `3cc41b2331675a2c3ed12295668b2e67b50691932a18aceafa8d9df079b8db9e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **决定／旧候选指针：** issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `3645ed3cdd5656b5fe75ece0447d8f360318eefe29b5ae9c5ff58a75f75248d5`。

### REQ-0176 — 系统事实不完整时，只有 R-11 可补充现场确认。 R-11 或等效维护权限人员可以个人身份确认具体车辆已在…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0176`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 系统事实不完整时，只有 R-11 可补充现场确认。 R-11 或等效维护权限人员可以个人身份确认具体车辆已在具体充电桩实际尝试开始充电但充电未建立；普通生产操作员只能报告或申请检查，人工不能覆盖身份冲突。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)；`决定无联网充电桩的充电失败确认与暂停触发边界 > Answer; line 34`；来源 SHA-256 `3cc41b2331675a2c3ed12295668b2e67b50691932a18aceafa8d9df079b8db9e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **决定／旧候选指针：** issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `73713fe55ecf56766ab61e1bea6756e200c6186b0c735b1bce1e21bb4915c518`。

### REQ-0177 — 确认后立即以不可变、幂等事件暂停该桩的全部 8005 分配。 事件记录唯一 ID 和触发来源，充电桩 RIo…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0177`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 确认后立即以不可变、幂等事件暂停该桩的全部 8005 分配。 事件记录唯一 ID 和触发来源，充电桩 RIoT 地图 + 站点、名册记录与版本，AGV、预占和订单身份，到桩/开始充电/失败/最终 HANG/确认/暂停时间，原始位置、订单、动作结果和电池状态及证据引用，RIoT build/契约版本，以及人工确认的个人身份、角色、认证时间和现场处置。理由固定为已确认充不上，根因保持 UNKNOWN。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md](../../../.scratch/current-requirements-baseline/issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md)；`决定无联网充电桩的充电失败确认与暂停触发边界 > Answer; line 35`；来源 SHA-256 `3cc41b2331675a2c3ed12295668b2e67b50691932a18aceafa8d9df079b8db9e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md。
- **决定／旧候选指针：** issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `4902fd1b7515d9e58bb5cfcac704a504232b4aad8e8029d3fbf398146aef6d42`。

## Required HITL resolution

- [ ] `REQ-0174`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0175`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0176`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0177`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0174`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0175`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0176`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0177`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-047`、Approval payload SHA-256 `5c904f0e27fdfde9dd0b6d1d6ae95e1d2a68fb206f3b5e33a54e05b1a809ea93`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
