# 最终批准 REQ-0257–REQ-0260：决定仓位模型与 IO 映射配置、验证和启用门禁

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-070
Approval payload SHA-256: 7b4818f9b629a96c73eb30c3619c6fdb36fc13920f5f341257ed0c03c58d97b5
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-070` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0257 — 单仓与整车采用两层模板。 SlotTemplate 是可供多个仓位共同引用的受控业务规格，只定义长、宽、高和…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0257`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 单仓与整车采用两层模板。 SlotTemplate 是可供多个仓位共同引用的受控业务规格，只定义长、宽、高和兼容花篮类型，不记录载重。“所属面”不再是独立字段，而并入规范的 SlotPosition。VehicleSlotTemplate 定义整车物理仓位集合、编号，以及每仓的 SlotPosition 和 SlotTemplate 引用，不包含 IO 映射；多个同构 AGV 可以复用同一模板。单车不得直接覆盖整车布局，确有差异时必须建立新模板或新拓扑版本。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 19`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `b5ad350ad852696727deaaf8b89223d62830bcf7a68c86a38f270bac23c7fb47`。

### REQ-0258 — 服务端是唯一权威维护入口。 ControlServer 保存并发布 SlotTemplate、Vehicle…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0258`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 服务端是唯一权威维护入口。 ControlServer 保存并发布 SlotTemplate、VehicleSlotTemplate、不可变的 SlotModelVersion 和 IoConfigDraft。查看、编辑、多选、复制、审计、提交及激活都通过服务端 ConfigurationMaintenanceConsole 完成；车载端不提供平行编辑界面，也不允许直接修改本地文件形成受支持配置。系统管理员可以维护仓位模板、模型和 IO 映射并激活候选版本；维护管理员可以查看、核对和执行实际硬件测试，但不能修改或激活配置。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 20`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `0bd176da3f5f67fe2882a4acc97e911a61854cb7ae7827ca8c9d4e864a8babaf`。

### REQ-0259 — 新 AGV 可以先登记，但不能带着缺口投运。 不要求接入当天完成 IO 录入；然而已发布模型中的全部仓位必须…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0259`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 新 AGV 可以先登记，但不能带着缺口投运。 不要求接入当天完成 IO 录入；然而已发布模型中的全部仓位必须具有完整并经实际核对的 SlotIoBinding，整车才达到 SlotConfigurationReadiness。在此之前整车不得取得业务就绪，任何未配置或未验证仓位不得被业务分配，管理员也不能强制放行。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 21`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `b5af1c0d3efdf73a13b3c030d425ca7fc02378279b6fba4c6ab2ce675e0a757c`。

### REQ-0260 — 模板资料变更与硬件配置变更分开治理。 只修改 SlotTemplate 长、宽、高或花篮兼容性的 SlotM…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0260`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 模板资料变更与硬件配置变更分开治理。 只修改 SlotTemplate 长、宽、高或花篮兼容性的 SlotMetadataChange 在服务端一次发布，全部引用车辆的新任务直接使用新修订，不进入车辆配置维护态，也不重新执行 IO 测试。已开始或已预留的任务保留分配时的 SlotAssignmentTemplateSnapshot 直至结束，不因发布中途失效。若变更源于即时安全风险，必须先禁用受影响仓位或车辆并走异常处置，不能用普通资料发布静默中断在途任务。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md](../../../.scratch/current-requirements-baseline/issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md)；`决定仓位模型与 IO 映射配置、验证和启用门禁 > Answer; line 22`；来源 SHA-256 `c5b51492022b1322e52bfd255fa06c574013592e2cf01e616333a06b1b80a0e7`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md。
- **决定／旧候选指针：** issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md；R01-A1893 ／ R01-A1925 ／ R03-A0948 ／ R03-A0961 ／ R03-A0977。
- **规范文本 SHA-256：** `472a46d2324ad4e712650a8d0eeb92ed3f4921e5506d911239bcacf13b87721a`。

## Required HITL resolution

- [ ] `REQ-0257`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0258`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0259`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0260`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0257`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0258`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0259`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0260`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-070`、Approval payload SHA-256 `7b4818f9b629a96c73eb30c3619c6fdb36fc13920f5f341257ed0c03c58d97b5`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
