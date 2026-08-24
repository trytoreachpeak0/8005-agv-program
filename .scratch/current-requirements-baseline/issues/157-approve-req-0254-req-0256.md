# 最终批准 REQ-0254–REQ-0256：决定人员登录、维护操作与高风险权限边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-069
Approval payload SHA-256: 7fb56f4692f04d72db840dc7b41b7f9370ff59ecadf84776f1a9f154f916a4dd
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-069` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0254 — 票据 62 的专门权限并入管理员角色。 系统事实不足时的“充不上现场确认”、人工清桩确认和充电桩恢复确认均可…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0254`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 票据 62 的专门权限并入管理员角色。 系统事实不足时的“充不上现场确认”、人工清桩确认和充电桩恢复确认均可由维护管理员或系统管理员以个人账号独立提交，普通操作员不可提交；这些能力不再引用 R-11/R-13 系统角色，也不另建可独立分配的权限。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)；`决定人员登录、维护操作与高风险权限边界 > Answer; line 25`；来源 SHA-256 `d2209c67f543e6d27fdcc80b6cdd304fa6c63580e243e9757f19721888b2ae38`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **决定／旧候选指针：** issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md；R01-A1905 ／ R01-A1907 ／ R02-A0222 ／ R03-A0670 ／ R03-A0742 ／ R03-A0796 ／ R03-A0892 ／ R03-A0958。
- **规范文本 SHA-256：** `073a2800aa062c5d9890f435c35513ce6ec760778893166e221d0986e33c1980`。

### REQ-0255 — 所有管理员操作形成不可改写审计。 每次查看或变更记录个人账号、当时角色与登录会话、时间、终端及来源地址、操作…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0255`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 所有管理员操作形成不可改写审计。 每次查看或变更记录个人账号、当时角色与登录会话、时间、终端及来源地址、操作对象、原因、前后状态，以及请求、执行和最终核验结果；失败、超时与结果未知和成功操作同等保留。管理员可查看和导出，但任何管理员都不能修改或删除记录；具体保留期由决定监控新鲜度、告警升级、重试与日志留存规则确定。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)；`决定人员登录、维护操作与高风险权限边界 > Answer; line 27`；来源 SHA-256 `d2209c67f543e6d27fdcc80b6cdd304fa6c63580e243e9757f19721888b2ae38`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **决定／旧候选指针：** issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md；R01-A1905 ／ R01-A1907 ／ R02-A0222 ／ R03-A0670 ／ R03-A0742 ／ R03-A0796 ／ R03-A0892 ／ R03-A0958。
- **规范文本 SHA-256：** `031a44bc3ea01c4000cd69980d0443b94adb326947699c998d884da5ff254474`。

### REQ-0256 — 系统管理员可以立即撤权。 创建账号、调整角色和停用账号只属于系统管理员；停用账号或降低角色后，该账号的活动登…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0256`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 系统管理员可以立即撤权。 创建账号、调整角色和停用账号只属于系统管理员；停用账号或降低角色后，该账号的活动登录与异常处置权限立即失效。已经发出但结果未知的动作不能因撤权被视为取消，系统继续对账并保留审计；后续处置须由另一个具备权限的个人账号重新登录接手。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)；`决定人员登录、维护操作与高风险权限边界 > Answer; line 28`；来源 SHA-256 `d2209c67f543e6d27fdcc80b6cdd304fa6c63580e243e9757f19721888b2ae38`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **决定／旧候选指针：** issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md；R01-A1905 ／ R01-A1907 ／ R02-A0222 ／ R03-A0670 ／ R03-A0742 ／ R03-A0796 ／ R03-A0892 ／ R03-A0958。
- **规范文本 SHA-256：** `e065c879e707cb6c326881a405997109f17dbfb8eb07b01884846e197af5c000`。

## Required HITL resolution

- [ ] `REQ-0254`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0255`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0256`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0254`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0255`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0256`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-069`、Approval payload SHA-256 `7fb56f4692f04d72db840dc7b41b7f9370ff59ecadf84776f1a9f154f916a4dd`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
