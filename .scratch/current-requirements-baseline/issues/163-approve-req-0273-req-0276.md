# 最终批准 REQ-0273–REQ-0276：决定账户恢复与密码增强策略

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-075
Approval payload SHA-256: 89e656424cdbcbbe787933a4ad29c7570783f6c3110bbfe7d24935f161a41fa5
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-075` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0273 — 不建立泄露、找回或强制重置流程。 当前版本不考虑密码疑似泄露后的专门处置，不提供账号找回或独立强制重置流程；…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0273`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 不建立泄露、找回或强制重置流程。 当前版本不考虑密码疑似泄露后的专门处置，不提供账号找回或独立强制重置流程；首次登录使用的“待强制改密”标记一旦清除便不能重新置位。相关增强留待未来版本，不属于当前基线。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 19`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `59be17fc9de4f7f170d1c85b2d6881a410b5f1302cea63668ca56c48850383b6`。

### REQ-0274 — 密码只能由系统管理员设置。 SystemAdministrator 可以设置自己的密码以及维护管理员、其他系…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0274`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 密码只能由系统管理员设置。 SystemAdministrator 可以设置自己的密码以及维护管理员、其他系统管理员的密码；MaintenanceAdministrator 不能修改自己的密码，也不存在普通管理员自助改密入口。设置已有账号的新密码是常规账号管理动作，不建立一次性重置凭据或再次强制改密阶段。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 20`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `1d1d7105bf5c1fe47cc5aba56b2c9630024c019578fe01ae11dc6a528c6cd568`。

### REQ-0275 — 首次改密仅用于部署初始化。 首次部署创建一个绑定具名自然人的系统管理员个人账号，并为其提供临时初始密码；该系…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0275`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 首次改密仅用于部署初始化。 首次部署创建一个绑定具名自然人的系统管理员个人账号，并为其提供临时初始密码；该系统管理员首次登录后必须先设置自己的正式密码，才可进入其它管理功能。成功后永久清除首次改密标记，不保留永久共享的 admin 账号作为兜底入口。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 21`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `1b4ee896c5ee7c64a312ab8ae0d74dc4a6ed02b5aa4365244711cf6776235ed4`。

### REQ-0276 — 基础密码格式固定且不做可配置增强。 密码长度为 6～20 个字符，至少包含一个英文字母和一个数字，不得等于或…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0276`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 基础密码格式固定且不做可配置增强。 密码长度为 6～20 个字符，至少包含一个英文字母和一个数字，不得等于或完整包含登录名，比较时忽略大小写；不强制特殊符号或大小写混合。当前版本不要求定期换密、不维护密码历史，也不提供部署方调整或增强密码策略的配置边界。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 22`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `37bb8a487a9a3852ce547e6011a74d63f685542443452071ca041dc488c54c4b`。

## Required HITL resolution

- [ ] `REQ-0273`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0274`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0275`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0276`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0273`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0274`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0275`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0276`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-075`、Approval payload SHA-256 `89e656424cdbcbbe787933a4ad29c7570783f6c3110bbfe7d24935f161a41fa5`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
