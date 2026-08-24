# 最终批准 REQ-0277–REQ-0280：决定账户恢复与密码增强策略

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-076
Approval payload SHA-256: 521d0c8a056c7bca40fbcb93852fbea8378463cd4f3b3c38cc9230ae99990a18
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-076` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0277 — 设置新密码不联动当前会话。 系统管理员为已有账号设置新密码后，新密码从该账号下一次登录开始使用；该账号已经建…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0277`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 设置新密码不联动当前会话。 系统管理员为已有账号设置新密码后，新密码从该账号下一次登录开始使用；该账号已经建立的登录会话和 ExceptionRecoverySession 不因此终止。需要立即停止账号使用时，系统管理员必须使用票据 71 已批准的账号停用或角色降低能力，而不能把设置密码当作撤权动作。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 23`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `25cda5ff096696c4e1910e053e9c7859a7f619d08f863705420a07bba42b3f81`。

### REQ-0278 — 管理员登录会话不自动超时。 MaintenanceAdministrator 与 SystemAdminis…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0278`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 管理员登录会话不自动超时。 MaintenanceAdministrator 与 SystemAdministrator 的当前登录会话均不设置空闲超时或最长总有效期；只在主动注销、同账号新登录替换旧会话、账号停用或角色降低等既有明确边界结束。空闲与绝对超时能力留待未来版本。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 24`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `849c1a1e7ef34cc3db13fbf0cba43785fa8764ac36970fa1b4bae36773d6285a`。

### REQ-0279 — 异常处置会话也不设置空闲超时。 ExceptionRecoverySession 只在人员交接、切换车辆、扩…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0279`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 异常处置会话也不设置空闲超时。 ExceptionRecoverySession 只在人员交接、切换车辆、扩大目标仓位范围、主动退出、事件关闭、父登录会话主动注销或被新登录替换、账号停用或角色降低时结束。短暂断线仍只允许同一人员、同一事件在完成最新状态对账后继续；会话结束后不得发起新处置动作，已发出但结果未知的动作继续对账，车辆、仓位和任务继续保持既有安全阻断直至事实闭环。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 25`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `29a21873b30e43801f1932bea163c07e12c25945be9c51ccf3acb60360c3fc59`。

### REQ-0280 — 密码设置沿用不可改写审计。 每次密码设置记录执行系统管理员的个人账号、当时角色和登录会话、目标账号、时间、终…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0280`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 密码设置沿用不可改写审计。 每次密码设置记录执行系统管理员的个人账号、当时角色和登录会话、目标账号、时间、终端与来源、结果以及失败分类；任何页面、日志或审计记录均不得记录或展示明文密码。审计本身继续遵守票据 71 的不可修改、不可删除规则。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md](../../../.scratch/current-requirements-baseline/issues/74-decide-account-recovery-and-password-hardening-policy.md)；`决定账户恢复与密码增强策略 > Answer; line 26`；来源 SHA-256 `ef2f4f34a60abfaaeb4acd6e3677c022074e33e26563278c3f6da5310c71f90e`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/74-decide-account-recovery-and-password-hardening-policy.md。
- **决定／旧候选指针：** issues/74-decide-account-recovery-and-password-hardening-policy.md；R02-A0773 ／ R02-A0808。
- **规范文本 SHA-256：** `25da64fc67cfe88d483721a389a388f9392af99b21d3fb0604fd7df277803ebf`。

## Required HITL resolution

- [ ] `REQ-0277`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0278`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0279`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0280`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0277`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0278`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0279`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0280`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-076`、Approval payload SHA-256 `521d0c8a056c7bca40fbcb93852fbea8378463cd4f3b3c38cc9230ae99990a18`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
