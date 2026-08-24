# 最终批准 REQ-0289–REQ-0292：决定空闲返回、停靠点资格与调度竞争边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-079
Approval payload SHA-256: e4f3d133645cb65185265056b8f6108400ebed24e9fcdda9f7c4c146ac199fca
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-079` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0289 — 首版只允许专用等待点。 等待点必须以明确的 RIoT 地图 + 站点登记，不得同时承担业务或充电角色，也不得…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0289`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 首版只允许专用等待点。 等待点必须以明确的 RIoT 地图 + 站点登记，不得同时承担业务或充电角色，也不得与业务站或充电站共享物理坐标。不同站点身份即使坐标相同也不获准使用，因为已取消的实测没有证明单值 currentPosition 能稳定区分其角色。等待点继续使用既有 WaitingPointVehicleScope：默认对同图全部车辆开放，配置白名单时仅白名单车辆合格。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 19`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `d58ed0939e58004870c73d20c3a307588f427117c1480431d4ac66d8f5d478ca`。

### REQ-0290 — 所有用途通过唯一 VehiclePurposeClaim 原子争用车辆。 已开始或结果未知的搬运、充电、清桩…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0290`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 所有用途通过唯一 VehiclePurposeClaim 原子争用车辆。 已开始或结果未知的搬运、充电、清桩/维护和空闲返回保持现有占有，不允许新用途抢占。没有现有用途时，达到 MandatoryChargeEntryThreshold 的车辆先进入强制充电且不得接普通搬运或空闲返回；电量允许时先执行 TaskFirstDispatchSelection，只有没有合法搬运用途时才评估空闲返回。空闲返回不预留未来车辆，也不压过尚未形成承诺的搬运或强制充电。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 20`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `91314d94f1e5a6d18107f749f2af11dcae601b5ef629142d218d4fbf99eefa69`。

### REQ-0291 — IdleReturnEligibility 是严格兜底资格。 车辆须已结束当前用途、没有下一业务目标、活动或…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0291`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** IdleReturnEligibility 是严格兜底资格。 车辆须已结束当前用途、没有下一业务目标、活动或结果未知的 RIoT 订单、充电/清桩/维护门禁，电量高于强制充电入口阈值，并且本轮任务优先派车没有选中该车。启用空闲返回或激活新版等待点配置时，立即重评所有当前满足这些条件的车辆；忙碌或受阻车辆不改变当前状态，只在以后首次满足资格时评估。停用功能只阻止新承诺，不取消或改写既有返回订单。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 21`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `24792f48e1049bd9f558b6b820eb5aadfa2b65a1054dd415454fc20638e32fc6`。

### REQ-0292 — 车辆与等待点必须原子取得后才形成 IdleReturnCommit。 服务端基于同一份新鲜快照同时取得该车的…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0292`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 车辆与等待点必须原子取得后才形成 IdleReturnCommit。 服务端基于同一份新鲜快照同时取得该车的 IDLE_RETURN VehiclePurposeClaim 和具体等待点的 WaitingPointExclusiveClaim；任一取得失败都不形成承诺。形成承诺后，返回成为车辆当前已承诺下一站，沿用 PlannedStopMutationBoundary，不得因后来出现搬运任务或其它车辆优先级变化而取消、换点或抢占；新任务等待本次返回到点收敛后重新派车。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md](../../../.scratch/current-requirements-baseline/issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md)；`决定空闲返回、停靠点资格与调度竞争边界 > Answer; line 22`；来源 SHA-256 `a43a667ea1299d62cd617adbd2a48d846dc8ac50724675d83753fe82d419fc11`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md。
- **决定／旧候选指针：** issues/76-decide-idle-return-parking-point-eligibility-and-arbitration.md；R03-A2993 ／ R03-A3030 ／ R03-A3049 ／ R03-A3072。
- **规范文本 SHA-256：** `6691686397e7fb56cf9327087e07f1d8e7e69b89ff013e7fcee86fec5ea2f23e`。

## Required HITL resolution

- [ ] `REQ-0289`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0290`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0291`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0292`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0289`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0290`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0291`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0292`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-079`、Approval payload SHA-256 `e4f3d133645cb65185265056b8f6108400ebed24e9fcdda9f7c4c146ac199fca`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
