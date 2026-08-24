# 最终批准 REQ-0236–REQ-0239：决定故障车辆隔离、货物处置与人工越权边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-064
Approval payload SHA-256: 1216f885fea36d02f4f1c866ed34d14cbe1f001f16c191c12014a566621c9787
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-064` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0236 — 异常处置权限按个人授予。 初始授予 R-09 班组长、R-11 设备/电气维护人员和 R-13 AGV 运维…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0236`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 异常处置权限按个人授予。 初始授予 R-09 班组长、R-11 设备/电气维护人员和 R-13 AGV 运维/调度管理员，也可显式授予经过现场培训的生产人员而不改变岗位角色。任何持权人验证个人身份后均可独立完成系统内整套异常处置；无权限人员可以报告、协助或接管货物但不能操作异常处置界面。断电、抱闸和强制机械开锁仍由具备相应现场作业资质者实际执行并记录，作业资质不是系统审批步骤。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 50`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `edb9cf3105dea681c7c6a0df36ce55d0737b2e258c2314e7a22d3ae2190d9b08`。

### REQ-0237 — 普通放错只在离站前纠正。 8005 是一对一输送；车辆离开起点前保留既有 LoadCorrection 调整…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0237`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 普通放错只在离站前纠正。 8005 是一对一输送；车辆离开起点前保留既有 LoadCorrection 调整机会，离站后将错就错完成输送，不再换仓、重绑、重开任务、生成补运或修改 MES，最多记录差错事实。ExceptionRecoverySession 不处理普通存放错误，只处理仓内传感器/锁故障、车辆本体故障及实际被困货物。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 51`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `3a89c9f4aae5e19c963841556349f7ea351177426773a4532ddc65d292ffd9c5`。

### REQ-0238 — 已装货任务保持原绑定并采用双路径。 已有装货事实或货物状态未知时进入 FaultedVehicleCargo…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0238`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 已装货任务保持原绑定并采用双路径。 已有装货事实或货物状态未知时进入 FaultedVehicleCargoHold，保留原车辆、DemandId、仓位、产品和订单绑定，只允许修复后由原车继续，或在异常处置会话中取出、交接并终止；超时只告警，不自动选择路径或取消。路径选择不是审批：货物仍完整保留于原仓位并重新安全闭环时可改走修复续行；一旦产品已经从原绑定中取出并交接，对应 DemandId 必须完成取货终止闭环。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 53`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `b23a13341843fda061781601246b0cbb5ac3718b42262dc3ce7d265fc4f8f10a`。

### REQ-0239 — 修复续行保持同一业务任务与载货车辆。 原 RIoT 订单仍确认为 HELD 且身份、目标和货物绑定一致时走既…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0239`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 修复续行保持同一业务任务与载货车辆。 原 RIoT 订单仍确认为 HELD 且身份、目标和货物绑定一致时走既有 OrderContinue 授权及回查；原订单已明确终结、相关阻断收敛且 8005 任务未终止时，可重新通过正常派车和安全门禁后为同一 DemandId 建立关联旧订单的新 RIoT 移动单。订单结果未知、身份/位置/路线冲突时继续载货保全，不得换号绕过或改派；已经形成补救终止记录的任务不得复活。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md](../../../.scratch/current-requirements-baseline/issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)；`决定故障车辆隔离、货物处置与人工越权边界 > Answer; line 54`；来源 SHA-256 `8c50b5fe0c935a9f71a114f6255f06ec1f531e7550429e4e7dfa57c683ef511f`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md。
- **决定／旧候选指针：** issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md；R01-A1899 ／ R03-A1587 ／ R03-A1595 ／ R03-A1597 ／ R03-A1601 ／ R03-A1616 ／ R03-A1618 ／ R03-A1628。
- **规范文本 SHA-256：** `2b883854645d47b09c5faeab2f6cceb120a08f90dfb8284a7a9d54d060100753`。

## Required HITL resolution

- [ ] `REQ-0236`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0237`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0238`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0239`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0236`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0237`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0238`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0239`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-064`、Approval payload SHA-256 `1216f885fea36d02f4f1c866ed34d14cbe1f001f16c191c12014a566621c9787`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
