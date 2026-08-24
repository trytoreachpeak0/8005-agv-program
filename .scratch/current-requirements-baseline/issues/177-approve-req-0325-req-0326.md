# 最终批准 REQ-0325–REQ-0326：决定 AREA 显式覆盖的维护与生效治理

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-089
Approval payload SHA-256: 5f6e22b3288dd446e0b4109bdba36893828ffa8d75d74035b0b83fa5e7de7ade
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 2 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-089` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0325 — 既有任务不被地图变化重写。 新任务只能使用当时唯一有效的 AREA 解析结果并冻结其 Station；后续改…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0325`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 既有任务不被地图变化重写。 新任务只能使用当时唯一有效的 AREA 解析结果并冻结其 Station；后续改名、删除或冲突不静默改写已创建任务。具体地图同步、快照与已冻结任务失效处置仍由《决定地图拓扑同步与历史快照产品边界》承接。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)；`决定 AREA 显式覆盖的维护与生效治理 > Answer; line 23`；来源 SHA-256 `d63b7aacda000b2dc1baa4a18f1036db4297055f4b15bf8cac4470b223914d14`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/79-decide-area-override-maintenance-and-effectivity-governance.md；R01-A1897。
- **规范文本 SHA-256：** `ab81dfe6aba05f77f4db299fae1597769a1748ee5dd3beba8f8f6e02c83c1cb2`。

### REQ-0326 — 覆盖治理问题随能力一并消失。 覆盖的发现、录入、复核、批准、二次认证、版本、生效、回滚和审计均不属于当前需求…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0326`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 覆盖治理问题随能力一并消失。 覆盖的发现、录入、复核、批准、二次认证、版本、生效、回滚和审计均不属于当前需求；旧材料中“少量显式覆盖优先于自动解析”的表述只保留为被本决定废止的历史方案，不能进入首个当前基线。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)；`决定 AREA 显式覆盖的维护与生效治理 > Answer; line 24`；来源 SHA-256 `d63b7aacda000b2dc1baa4a18f1036db4297055f4b15bf8cac4470b223914d14`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/79-decide-area-override-maintenance-and-effectivity-governance.md；R01-A1897。
- **规范文本 SHA-256：** `3bfaeaffe8a80ed3ca3eff73d2f79da4cea36153ef925a179fdf1471cf405879`。

## Required HITL resolution

- [ ] `REQ-0325`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0326`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0325`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0326`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-089`、Approval payload SHA-256 `5f6e22b3288dd446e0b4109bdba36893828ffa8d75d74035b0b83fa5e7de7ade`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
