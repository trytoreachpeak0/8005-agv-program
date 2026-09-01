# 最终批准 REQ-0247–REQ-0249：决定安全联锁失败升级与紧急停止边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-067
Approval payload SHA-256: 1cbcc9b99ca275a311dcea844a426a874f3a6ed8dae3dce9975f886919fa8013
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-067` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0247 — 停稳必须依靠正面组合证据。 订单 HELD、急停状态或单次查询均不能单独构成停稳证明；必须同时取得新鲜且明确…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0247`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 停稳必须依靠正面组合证据。 订单 HELD、急停状态或单次查询均不能单独构成停稳证明；必须同时取得新鲜且明确为非移动的 movementState、连续多次位置不变，并确认期间没有新的移动迹象。任一必要事实未知时不得宣称已停稳；连续次数与时间窗口由决定监控新鲜度、告警升级、重试与日志留存规则统一确定。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)；`决定安全联锁失败升级与紧急停止边界 > Answer; line 69`；来源 SHA-256 `720c37d651f334847c8e9c456c84043301bd6e75e7f07d87351aae6b2e132c9b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **决定／旧候选指针：** issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md；R01-A1901 ／ R03-A2943 ／ R03-A2947 ／ R03-A2951 ／ R03-A2955。
- **规范文本 SHA-256：** `d07c69363eb3b3edd22a31b9e8257cd5a34e8f8c74b53892daf34a6b436265d1`。

### REQ-0248 — 急停调用按状态重试并保留现场兜底。 急停状态未确认前按受控退避持续重试 triggerEmergency 并…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0248`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 急停调用按状态重试并保留现场兜底。 急停状态未确认前按受控退避持续重试 triggerEmergency 并回查；确认 CAN_RECOVER 或 CAN_NOT_RECOVER 后停止重复触发，只监控停稳证明；原因消除前状态意外恢复 OK 时立即重触发并告警。远程调用失败、超时或结果未知且仍无停稳证明时，维持最高优先级告警并要求现场立即确认车辆和隔离危险区域；任何现场人员可操作已有物理急停且无需系统登录或审批，断电、抱闸等专业隔离只由具备相应作业资质者执行。物理隔离可控制现场风险，但不自动构成电子停稳证明或恢复资格。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)；`决定安全联锁失败升级与紧急停止边界 > Answer; line 70`；来源 SHA-256 `720c37d651f334847c8e9c456c84043301bd6e75e7f07d87351aae6b2e132c9b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **决定／旧候选指针：** issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md；R01-A1901 ／ R03-A2943 ／ R03-A2947 ／ R03-A2951 ／ R03-A2955。
- **规范文本 SHA-256：** `127fdaf0140e84b15df2abda1383a0535f1a8985f340874a4296982fb3e24993`。

### REQ-0249 — 发起急停遵循“停车宽、恢复严”。 系统满足条件时自动触发，不需要人工授权；现场人员可从车载端无需登录地为本车…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0249`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 发起急停遵循“停车宽、恢复严”。 系统满足条件时自动触发，不需要人工授权；现场人员可从车载端无需登录地为本车请求；服务端已登录且具有车辆查看权限的人员可对明确选中的车辆请求，不要求二次认证或审批。所有请求记录来源、身份（若有）、车辆、原因和结果；具体服务端角色由决定人员登录、维护操作与高风险权限边界统一确定。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)；`决定安全联锁失败升级与紧急停止边界 > Answer; line 71`；来源 SHA-256 `720c37d651f334847c8e9c456c84043301bd6e75e7f07d87351aae6b2e132c9b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **决定／旧候选指针：** issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md；R01-A1901 ／ R03-A2943 ／ R03-A2947 ／ R03-A2951 ／ R03-A2955。
- **规范文本 SHA-256：** `5315542378912aa4ca92a926f1de6059aeb1020d70d72c59f6dc47444a5c535f`。

## Required HITL resolution

- [ ] `REQ-0247`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0248`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0249`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0247`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0248`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0249`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-067`、Approval payload SHA-256 `1cbcc9b99ca275a311dcea844a426a874f3a6ed8dae3dce9975f886919fa8013`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
