# 最终批准 REQ-0243–REQ-0246：决定安全联锁失败升级与紧急停止边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-066
Approval payload SHA-256: 7a0d1296d1c66fc6172f563f9ca15210583a2684d8d68cbe9e02e49c77c31ec6
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-066` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0243 — 仓内光幕不属于安全联锁。 8005 的仓内光幕只形成 SlotOccupancyState，用于判断有物、无…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0243`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 仓内光幕不属于安全联锁。 8005 的仓内光幕只形成 SlotOccupancyState，用于判断有物、无物或未知；它不是人员安全光幕，也不参与车辆移动安全联锁。光幕异常按占用事实未知和相应业务阻断处理，不因其自身触发车辆急停。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)；`决定安全联锁失败升级与紧急停止边界 > Answer; line 65`；来源 SHA-256 `720c37d651f334847c8e9c456c84043301bd6e75e7f07d87351aae6b2e132c9b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **决定／旧候选指针：** issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md；R01-A1901 ／ R03-A2943 ／ R03-A2947 ／ R03-A2951 ／ R03-A2955。
- **规范文本 SHA-256：** `40c6a289bd90e80702bb75cacb6be7bad21069f5b5acb60e08a911dae0465196`。

### REQ-0244 — 仓门安全以“明确证明锁闭”为准。 8005 没有独立门磁，不能直接观测仓门打开或关闭；只有有效锁反馈明确证明…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0244`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 仓门安全以“明确证明锁闭”为准。 8005 没有独立门磁，不能直接观测仓门打开或关闭；只有有效锁反馈明确证明锁闭才满足安全条件，明确未锁闭、反馈无效或未知均属于“仓门未能证明安全锁闭”，按不安全处理。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)；`决定安全联锁失败升级与紧急停止边界 > Answer; line 66`；来源 SHA-256 `720c37d651f334847c8e9c456c84043301bd6e75e7f07d87351aae6b2e132c9b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **决定／旧候选指针：** issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md；R01-A1901 ／ R03-A2943 ／ R03-A2947 ／ R03-A2951 ／ R03-A2955。
- **规范文本 SHA-256：** `963f1ca60256ebe458a2ff9eb01b8efbbaea82ca4276adc733e4f0f13f70afb8`。

### REQ-0245 — 仓门未锁闭采用三层处置。 已授权正常装卸开仓只维持 StationOperationGuard，不告警、不急…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0245`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 仓门未锁闭采用三层处置。 已授权正常装卸开仓只维持 StationOperationGuard，不告警、不急停；车辆已有停稳证明、但仓门在授权操作之外未锁闭或状态未知时，阻断移动并发出高优先级告警；车辆出现移动或停稳证明失效时立即升级软件急停。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)；`决定安全联锁失败升级与紧急停止边界 > Answer; line 67`；来源 SHA-256 `720c37d651f334847c8e9c456c84043301bd6e75e7f07d87351aae6b2e132c9b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **决定／旧候选指针：** issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md；R01-A1901 ／ R03-A2943 ／ R03-A2947 ／ R03-A2951 ／ R03-A2955。
- **规范文本 SHA-256：** `06a4f33ed01744a0830afc9291ff745c9562ec4f2d6d1f2cf96f92b458a61781`。

### REQ-0246 — 无法证明停车时立即升级，不等待固定超时。 当仓门未能证明安全锁闭，或疑似车辆故障阻断/车辆故障隔离已经要求停…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0246`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 无法证明停车时立即升级，不等待固定超时。 当仓门未能证明安全锁闭，或疑似车辆故障阻断/车辆故障隔离已经要求停车，而 OrderHold 后无法同时证明订单已 HELD 和车辆已停稳，且车辆仍在移动或因监控失败无法排除继续移动时，8005 自动调用 triggerEmergency。不得以 Cancel 代替停车。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md](../../../.scratch/current-requirements-baseline/issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)；`决定安全联锁失败升级与紧急停止边界 > Answer; line 68`；来源 SHA-256 `720c37d651f334847c8e9c456c84043301bd6e75e7f07d87351aae6b2e132c9b`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md。
- **决定／旧候选指针：** issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md；R01-A1901 ／ R03-A2943 ／ R03-A2947 ／ R03-A2951 ／ R03-A2955。
- **规范文本 SHA-256：** `52f37d76d4ec58c5aaeda610fb570d63a8d03ae6bb3225ea8b02ebc19255cdaf`。

## Required HITL resolution

- [ ] `REQ-0243`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0244`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0245`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0246`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0243`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0244`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0245`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0246`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-066`、Approval payload SHA-256 `7a0d1296d1c66fc6172f563f9ca15210583a2684d8d68cbe9e02e49c77c31ec6`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
