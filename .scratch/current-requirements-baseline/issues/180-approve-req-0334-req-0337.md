# 最终批准 REQ-0334–REQ-0337：决定公共业务点绑定的维护与生效治理

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-092
Approval payload SHA-256: ed0b2656c7da73ec50a1931291aa821e71d3d420e340fd36f65fa0689f72568e
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-092` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0334 — 规范绑定键是 mapId + PublicStationFunction。 TASK_TYPE 只通过受控的…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0334`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 规范绑定键是 mapId + PublicStationFunction。 TASK_TYPE 只通过受控的任务类型—功能规则引用 PublicStationFunction，不按 TASK_TYPE 重复维护站点值。每张 Map 每种功能最多一个 FixedTaskStation，且同一 Station 不得同时承担多个 PublicStationFunction；未来确需复用时须以新的现场物理和作业证据重新批准，不可以普通配置放行。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 35`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `bfabdedadb1f8e1aa49c1ad086ba2cde10eeca1d5387adaa6e85118ca1918ec9`。

### REQ-0335 — Map 目录可见不等于公共站点就绪。 MapPublicStationRequirementSet 是该 M…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0335`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** Map 目录可见不等于公共站点就绪。 MapPublicStationRequirementSet 是该 Map 当前获准启用的任务类型所实际依赖的 PublicStationFunction 集合。相关任务类型只有在全部需求功能具有有效绑定后才可投运；不强迫每张 Map 配齐尚未启用的其余功能，也不允许为缺失功能填入默认站点。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 36`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `ff5b81012ff276c95d13d85f7a7493bc7fa737678b3727314ca704a180f54d33`。

### REQ-0336 — 现场核对与配置激活遵守现有两级管理员权限。 MaintenanceAdministrator 可识别公共功能…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0336`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 现场核对与配置激活遵守现有两级管理员权限。 MaintenanceAdministrator 可识别公共功能、核对实际物理用途与目录中的具体 Station，但不可编辑或激活绑定；SystemAdministrator 负责录入、修改、激活、恢复和回滚。SystemAdministrator 可独立完成核对与激活，不新增双人审批链，也不要求当前基线最终批准人逐个批准现场站点值。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 37`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `2bb88cc6a78c039aee3af29236499fc0cb71e9d9ed4bd5c2ff9865df1976c7c9`。

### REQ-0337 — 每张 Map 以完整不可变绑定集版本生效。 PublicStationBindingSetVersion 保…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0337`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 每张 Map 以完整不可变绑定集版本生效。 PublicStationBindingSetVersion 保留该 Map 完整的功能—Station 绑定、MapPublicStationRequirementSet、所依赖的任务类型规则版本和 MapStationCatalogSnapshot 修订。草稿、复制和校验不影响运行；候选只能整图原子激活，任一失败都不得部分发布、逐功能切换或混用新旧版本。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 38`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `c10304d394829cd49d4fdcfce30dba8842b68454723e485d8c0ace911f11a616`。

## Required HITL resolution

- [ ] `REQ-0334`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0335`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0336`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0337`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0334`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0335`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0336`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0337`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-092`、Approval payload SHA-256 `ed0b2656c7da73ec50a1931291aa821e71d3d420e340fd36f65fa0689f72568e`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
