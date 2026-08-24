# 最终批准 REQ-0232–REQ-0235：决定故障车辆隔离、货物处置与人工越权边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-063
Approval payload SHA-256: 602f661a024452178960d8751f7f51e5b91ad503434a57561f959739f9615dd5
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-063` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0232 — 故障采用“疑似阻断—确认隔离”两级事实模型。 离线、通信中断、导航失败、单个订单 FAILED 和持续时间均…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0232`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 故障采用“疑似阻断—确认隔离”两级事实模型。 离线、通信中断、导航失败、单个订单 FAILED 和持续时间均不足以证明单车故障，只形成 SuspectedVehicleFaultBlock，立即阻止新派车并告警。时间只提高告警和响应紧迫度，永远不能单独升级故障事实。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 45`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `8f4acc136519e5819709bb6049b5ecc7239ff303bccdc748e79750d70501429d`。

### REQ-0233 — 自动确认故障使用严格硬证据白名单。 当前唯一可自动进入 VehicleFaultIsolation 的事实是…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0233`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 自动确认故障使用严格硬证据白名单。 当前唯一可自动进入 VehicleFaultIsolation 的事实是新鲜的 emergencyState=CAN_NOT_RECOVER。sysState、lastErrorCode、hardwareErrorCode、faultCodesList 及其它候选须先绑定环境、build、车型/固件、语义、严重度和清除条件并再次批准。具备 ExceptionRecoveryPermission 的人员也可在异常处置会话中依据具体现场事实确认隔离；软件或网络异常本身仍不能证明单车故障。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 46`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `e78ad687d16dcb3e301e5bce9d21b4167c2cb29cc396c01d78a653e2d2ebc677`。

### REQ-0234 — 进入阻断先保护当前订单。 进入疑似阻断或正式隔离时立即禁止新派车，并对本项目当前执行订单自动调用 Order…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0234`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 进入阻断先保护当前订单。 进入疑似阻断或正式隔离时立即禁止新派车，并对本项目当前执行订单自动调用 OrderHold、回查 HELD；不得以 Cancel 代替停车。OrderHold 不可用、结果未知或车辆未及时停下时保持全部阻断并形成高优先级事件，具体 EmergencyStop 升级交由决定安全联锁失败升级与紧急停止边界统一决定；实际停车得到证明前不得显示为已安全停稳。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 48`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `885eda8e01883e19633504e7d35893362fd201f8139c4279590d400bf9688a5a`。

### REQ-0235 — 所有故障与被困货物处理统一为一次身份验证的异常处置会话。 ExceptionRecoverySession …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0235`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 所有故障与被困货物处理统一为一次身份验证的异常处置会话。 ExceptionRecoverySession 绑定一个处置人员、一个事件、一台车辆及固定任务/仓位范围；会话内可以连续选择修复续行、受控取货、强制机械取出、实物交接和车辆恢复，不使用审批工单、双人复核或逐动作二次认证。人员交接、切换车辆、扩大仓位范围、主动退出或事件关闭时会话结束；短暂断线后仅在同一人员、同一事件且会话仍有效时完成最新对账后继续，断线期间不得扩围。空闲超时由统一登录权限规则配置。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 49`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `46e7f13bab427e09afd265bf88dc40914fc78b4a12c2494875ca353ecbdffa1b`。

## Required HITL resolution

- [ ] `REQ-0232`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0233`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0234`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0235`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0232`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0233`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0234`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0235`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-063`、Approval payload SHA-256 `602f661a024452178960d8751f7f51e5b91ad503434a57561f959739f9615dd5`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
