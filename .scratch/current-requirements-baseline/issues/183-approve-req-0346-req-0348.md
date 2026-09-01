# 最终批准 REQ-0346–REQ-0348：决定公共业务点绑定的维护与生效治理

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-095
Approval payload SHA-256: 60c23ed7b32ebff493041565bdc86c3fc13ca32997fe0f1cdc8327e79f73c2c3
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-095` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0346 — 回滚是受控的新激活，不是历史覆盖。 SystemAdministrator 只可选择旧不可变版本的内容，在当…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0346`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 回滚是受控的新激活，不是历史覆盖。 SystemAdministrator 只可选择旧不可变版本的内容，在当前新鲜目录、当前任务类型功能规则和完整现场核对下重新校验，并作为一次新的激活记录生效。回滚仍只影响之后创建的 TransportDemand，不回写已有任务。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 47`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `496ab87b684e0188a76988f23ea9587b53369a28817a2589288b563187ef04c6`。

### REQ-0347 — 激活结果未知时不猜测生效版本。 激活、恢复或回滚超时、断联或返回矛盾结果时，相关 Map 暂停新的公共站点使…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0347`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 激活结果未知时不猜测生效版本。 激活、恢复或回滚超时、断联或返回矛盾结果时，相关 Map 暂停新的公共站点使用；系统必须读取实际生效版本、版本身份和完整内容完成对账，禁止以请求成功、本地预期或部分功能状态表示整图已生效。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 48`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `8e5da76abcdbe98786b0e919833d1b07e71dcb7b21c6d8ec60e619cb1e468680`。

### REQ-0348 — 全部操作和变化证据必须不可改写地审计。 在票据 71 已批准字段之外，记录 Map、PublicStatio…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0348`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 全部操作和变化证据必须不可改写地审计。 在票据 71 已批准字段之外，记录 Map、PublicStationFunction、变更前后 Station 身份与名称、目录修订、新旧规则与绑定版本、影响预览、变更理由、现场核对证据、活动任务影响数量、校验结果、激活/暂停/恢复/回滚请求及最终对账结论；成功、失败、超时和结果未知同等保留。记录至少在线保留 180 天，仍被配置版本、TransportDemand、审计或未关闭异常引用时不得删除。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md)；`决定公共业务点绑定的维护与生效治理 > Answer; line 49`；来源 SHA-256 `6f979bfffefacb1b2486ae13e7e64fe159920c9191d8b548e1900771d199a656`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/83-decide-public-station-binding-maintenance-and-effectivity-governance.md；none-explicitly-linked; preserved in v1-legacy-source-disposition.tsv。
- **规范文本 SHA-256：** `9effd29ca2e1f094d07070b6cdd4b73087372a3244c5831841cb2a9dc370afc4`。

## Required HITL resolution

- [ ] `REQ-0346`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0347`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0348`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0346`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0347`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0348`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-095`、Approval payload SHA-256 `60c23ed7b32ebff493041565bdc86c3fc13ca32997fe0f1cdc8327e79f73c2c3`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
