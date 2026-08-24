# 最终批准 REQ-0342–REQ-0345：决定公共业务点绑定的维护与生效治理

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-094
Approval payload SHA-256: 98292014a93e96d66af354cf1652b62be0a0eac44a98ebe7b3545ec3d1a4bed2
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-094` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0342 — 变化影响以必要范围收敛。 单一站点变化只阻断依赖受影响 PublicStationFunction 的新使用…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0342`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 变化影响以必要范围收敛。 单一站点变化只阻断依赖受影响 PublicStationFunction 的新使用，其余已验证功能继续运行；Map 身份或名称变化则按上述边界处理全图。系统无法自动发现“Map/Station 身份和名称均未变但物理用途已改变”；现场发现此情况时必须立即暂停相关绑定。首次投运、上述目录变化、任务类型规则变化、现场用途变化报告或人工暂停均触发复核；不设置无证据支持的定期重复审批。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 43`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `fc67562d23b0df7de4b96886714613c0266d6600d7bb4b42c38b0a8e9e21ad95`。

### REQ-0343 — 任务类型—功能关系本身也必须版本化。 TaskTypePublicStationRuleVersion 固定…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0343`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 任务类型—功能关系本身也必须版本化。 TaskTypePublicStationRuleVersion 固定每个受支持 TASK_TYPE 使用的 PublicStationFunction 及其在运输中是起点还是终点。新任务类型或关系变更只有在相关 Map 的绑定版本已满足新功能需求时才可激活；规则与绑定在同一发布门禁内校验，不允许先放行缺失固定站点的 TASK_TYPE。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 44`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `76b76e5a0ba0458966d5d09623c7af40ca40a3f708292f5851b0ee7eea87f4a3`。

### REQ-0344 — TransportDemand 冻结规则、站点和所依赖版本。 新建 TransportDemand 记录其 …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0344`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** TransportDemand 冻结规则、站点和所依赖版本。 新建 TransportDemand 记录其 TaskTypePublicStationRuleVersion、PublicStationBindingSetVersion 与 ResolvedTransportStation；后续规则、绑定或名称变化不重写、迁移或重新解析既有任务。旧站身份仍存在、目录新鲜且未被暂停时，既有任务可继续使用冻结站点；冻结站点失效或被暂停时，尚未创建的新 RIoT move 必须阻断并记录精确原因。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 45`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `f3fe0dfee21234c5eabae81efe1957d953adf3eaeb652fb925e1d2eb9d7c3b37`。

### REQ-0345 — 已存在的 RIoT 订单不被配置变化自动取消。 已建单或正在执行的移动继续按 OrderRef 观察、对账和…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0345`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 已存在的 RIoT 订单不被配置变化自动取消。 已建单或正在执行的移动继续按 OrderRef 观察、对账和收敛；目录、绑定、规则或暂停变化不自动改单、换站、换图或取消。后续尚未建单的停靠继续遵守当前新鲜目录、绑定暂停与 RouteCost 门禁。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 46`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `4d90f127a310ec0c10820929ba24610a70e7610804e563d486c65b2963ca31aa`。

## Required HITL resolution

- [ ] `REQ-0342`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0343`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0344`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0345`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0342`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0343`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0344`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0345`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-094`、Approval payload SHA-256 `98292014a93e96d66af354cf1652b62be0a0eac44a98ebe7b3545ec3d1a4bed2`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
