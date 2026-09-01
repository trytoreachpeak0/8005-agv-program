# 最终批准 REQ-0331–REQ-0333：决定 RIoT 建单未确认时任务绑定、重试与释放边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-091
Approval payload SHA-256: 4dd30c49c45a026aa83b27089405125b1389a013a52cee59f5e9693655edb965
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md](../../../.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-091` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0331 — 查到多单、字段不一致或无法完整核验时，继续阻断，不得接管、释放或重派。

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0331`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 查到多单、字段不一致或无法完整核验时，继续阻断，不得接管、释放或重派。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md](../../../.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md)；`决定 RIoT 建单未确认时任务绑定、重试与释放边界 > Answer > 超时、结果未知与对账; line 32`；来源 SHA-256 `11ebbf6172e620701e26edf448a624e553b3e26fd85c14783bc449c94645d42d`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md。
- **决定／旧候选指针：** issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md；R03-A1571。
- **规范文本 SHA-256：** `78be61cae01cbc2ca1ab1d390788b5a9ac503a478b1047667e2f434453e8d48c`。

### REQ-0332 — 可靠确认订单不存在时，在原前提仍成立的范围内保留绑定，以原 upperId 有限重试；次数和退避时长仍留给正…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0332`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 可靠确认订单不存在时，在原前提仍成立的范围内保留绑定，以原 upperId 有限重试；次数和退避时长仍留给正式 spec 配置。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md](../../../.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md)；`决定 RIoT 建单未确认时任务绑定、重试与释放边界 > Answer > 超时、结果未知与对账; line 33`；来源 SHA-256 `11ebbf6172e620701e26edf448a624e553b3e26fd85c14783bc449c94645d42d`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md。
- **决定／旧候选指针：** issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md；R03-A1571。
- **规范文本 SHA-256：** `4827b249509539b0d204c20367f98be0c31534c5656f17040ccb538ccd9216f4`。

### REQ-0333 — 建单调用和对账结果同时未知时，进入“建单结果双重未知”：继续保留全部绑定并升级告警，不因时间、重试次数或任何…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0333`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 建单调用和对账结果同时未知时，进入“建单结果双重未知”：继续保留全部绑定并升级告警，不因时间、重试次数或任何管理员操作强制释放。维护管理员或系统管理员只能查看审计、重新对账、暂停后续调用，或登记经独立核验的 RIoT 结果，不能把未知强制视为不存在。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md](../../../.scratch/current-requirements-baseline/issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md)；`决定 RIoT 建单未确认时任务绑定、重试与释放边界 > Answer > 超时、结果未知与对账; line 34`；来源 SHA-256 `11ebbf6172e620701e26edf448a624e553b3e26fd85c14783bc449c94645d42d`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md。
- **决定／旧候选指针：** issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md；R03-A1571。
- **规范文本 SHA-256：** `8de7e8da2754bad791a9b50f5c7a4daebd17e102ee7b863280b1165dc3708cae`。

## Required HITL resolution

- [ ] `REQ-0331`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0332`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0333`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0331`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0332`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0333`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-091`、Approval payload SHA-256 `4dd30c49c45a026aa83b27089405125b1389a013a52cee59f5e9693655edb965`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
