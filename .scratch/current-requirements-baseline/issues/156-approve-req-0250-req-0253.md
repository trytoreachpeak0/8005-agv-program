# 最终批准 REQ-0250–REQ-0253：决定人员登录、维护操作与高风险权限边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-068
Approval payload SHA-256: d337129ca98c4ada89a7b839263af6ffd1dfbea5df815c642956e7735c0a9f7a
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-068` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0250 — 当前只有三种人员访问身份。 操作员通过手工输入工号形成本站操作者声明；维护管理员和系统管理员通过个人账号密码…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0250`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 当前只有三种人员访问身份。 操作员通过手工输入工号形成本站操作者声明；维护管理员和系统管理员通过个人账号密码登录。R-01～R-15 只可保留为人员岗位或审计属性，不再作为系统授权角色。当前不设置独立只读账号；没有维护职责的厂内 IT 或生产管理人员不登录 8005，不得为了只读查看而取得维护管理员权限。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)；`决定人员登录、维护操作与高风险权限边界 > Answer; line 19`；来源 SHA-256 `d2209c67f543e6d27fdcc80b6cdd304fa6c63580e243e9757f19721888b2ae38`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **决定／旧候选指针：** issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md；R01-A1905 ／ R01-A1907 ／ R02-A0222 ／ R03-A0670 ／ R03-A0742 ／ R03-A0796 ／ R03-A0892 ／ R03-A0958。
- **规范文本 SHA-256：** `509a034bbbb2b09ca09997d8bd7b7b78e7dc1260d270021887641d837b84def8`。

### REQ-0251 — 系统管理员是软件维护人员的最高权限角色。 SystemAdministrator 拥有全部 8005 系统权…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0251`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 系统管理员是软件维护人员的最高权限角色。 SystemAdministrator 拥有全部 8005 系统权限，包括维护管理员能力、账号与角色管理、IO 映射修改和激活、系统级参数、外部接口配置、凭证及软件版本维护。全部权限仍不能覆盖车辆停稳、仓门安全、状态未知阻断、结果未知对账或其它物理与业务安全门禁。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)；`决定人员登录、维护操作与高风险权限边界 > Answer; line 22`；来源 SHA-256 `d2209c67f543e6d27fdcc80b6cdd304fa6c63580e243e9757f19721888b2ae38`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **决定／旧候选指针：** issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md；R01-A1905 ／ R01-A1907 ／ R02-A0222 ／ R03-A0670 ／ R03-A0742 ／ R03-A0796 ／ R03-A0892 ／ R03-A0958。
- **规范文本 SHA-256：** `356928dc8606592a5ba3ed4f7e3d41af310b922c42ca9597d682d89c3524c567`。

### REQ-0252 — 管理员必须一人一号且单会话。 每个管理员账号唯一绑定一名自然人，只授予维护管理员或系统管理员之一；禁止多人共…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0252`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 管理员必须一人一号且单会话。 每个管理员账号唯一绑定一名自然人，只授予维护管理员或系统管理员之一；禁止多人共用账号。每个账号只允许一个活动登录会话，新登录终止并审计旧会话；不同人员需要分别建立账号。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)；`决定人员登录、维护操作与高风险权限边界 > Answer; line 23`；来源 SHA-256 `d2209c67f543e6d27fdcc80b6cdd304fa6c63580e243e9757f19721888b2ae38`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **决定／旧候选指针：** issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md；R01-A1905 ／ R01-A1907 ／ R02-A0222 ／ R03-A0670 ／ R03-A0742 ／ R03-A0796 ／ R03-A0892 ／ R03-A0958。
- **规范文本 SHA-256：** `2e70b796ccd0597db7f921484c87ae1c2cb9d9cdc0e39791e61e144212a5ac7b`。

### REQ-0253 — 统一异常处置权限随两个管理员角色授予。 ExceptionRecoveryPermission 不再按 R-…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0253`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 统一异常处置权限随两个管理员角色授予。 ExceptionRecoveryPermission 不再按 R-09、R-11、R-13 岗位或额外的逐人附加权限分别配置，维护管理员和系统管理员均自动具备，操作员不具备。任一管理员验证个人账号后均可独立完成票据 69 的单一 ExceptionRecoverySession，不重新引入双角色批准、审批链或逐动作二次认证；断电、抱闸和强制机械开锁等现场动作仍须由具备相应作业资质的实际人员执行并记录。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md](../../../.scratch/current-requirements-baseline/issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)；`决定人员登录、维护操作与高风险权限边界 > Answer; line 24`；来源 SHA-256 `d2209c67f543e6d27fdcc80b6cdd304fa6c63580e243e9757f19721888b2ae38`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md。
- **决定／旧候选指针：** issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md；R01-A1905 ／ R01-A1907 ／ R02-A0222 ／ R03-A0670 ／ R03-A0742 ／ R03-A0796 ／ R03-A0892 ／ R03-A0958。
- **规范文本 SHA-256：** `6c24a30dc88b323bfc3b487badf9665401c1281a6a3f19c4c64075af0c0d3d51`。

## Required HITL resolution

- [ ] `REQ-0250`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0251`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0252`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0253`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0250`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0251`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0252`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0253`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-068`、Approval payload SHA-256 `d337129ca98c4ada89a7b839263af6ffd1dfbea5df815c642956e7735c0a9f7a`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
