# 最终批准 REQ-0170–REQ-0173：决定充电失败改派的备用桩筛选与排队关系

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-046
Approval payload SHA-256: 2c62f6d6ef64ee597a8dbe668b8b2d5004fd30064e02578e0c737f66908ae57b
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md](../../../.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-046` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0170 — ChargeHangReassign 与普通待充共用一条候选链。 先限定为该车允许集合中的 8005 项目独…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0170`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** ChargeHangReassign 与普通待充共用一条候选链。 先限定为该车允许集合中的 8005 项目独占充电桩，排除刚失败的站点和已暂停分配的站点，再保留 RIoT 当前地图中身份有效、占用/预占状态可确认且当前空闲的站点；任一资格或状态未知都 fail-closed。NearStationQuery 只对这个已过滤集合计算，不得从全图或失败站点中回填。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md](../../../.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md)；`决定充电失败改派的备用桩筛选与排队关系 > Answer; line 29`；来源 SHA-256 `417e9daa334340753ac2a606424da7017e672706da284715f114f9ecc1c287f6`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **决定／旧候选指针：** issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md；R09-A0034 ／ R09-A0035 ／ R09-A0036 ／ R09-A0037 ／ R09-A0038 ／ R09-A0039 ／ R09-A0040。
- **规范文本 SHA-256：** `ca1161eb48fad3606faae12e4daae6f30f10996b1a7977473984ba88794086dc`。

### REQ-0171 — 独占资格由受控名册授予。 项目级“8005 独占充电桩名册”以 RIoT 地图 + 站点标识固定身份并保留批…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0171`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 独占资格由受控名册授予。 项目级“8005 独占充电桩名册”以 RIoT 地图 + 站点标识固定身份并保留批准/变更记录；每辆 AGV 的候选集必须是名册的子集。共享桩、归属未知桩和仅因当前无车占位而被猜测为独占的桩不得进入自动充电或改派。普通候选配置不能自行授予独占资格。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md](../../../.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md)；`决定充电失败改派的备用桩筛选与排队关系 > Answer; line 30`；来源 SHA-256 `417e9daa334340753ac2a606424da7017e672706da284715f114f9ecc1c287f6`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **决定／旧候选指针：** issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md；R09-A0034 ／ R09-A0035 ／ R09-A0036 ／ R09-A0037 ／ R09-A0038 ／ R09-A0039 ／ R09-A0040。
- **规范文本 SHA-256：** `d9d71b81981d070275869a9e4facac1d173bb7fd9c54b92d113c86295aec45e4`。

### REQ-0172 — 充电失败车辆不取得独立优先级。 它与普通待充车辆进入同一排队集合，统一按当前电量排序；失败事实本身不允许插队…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0172`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 充电失败车辆不取得独立优先级。 它与普通待充车辆进入同一排队集合，统一按当前电量排序；失败事实本身不允许插队或越过其它车辆。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md](../../../.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md)；`决定充电失败改派的备用桩筛选与排队关系 > Answer; line 31`；来源 SHA-256 `417e9daa334340753ac2a606424da7017e672706da284715f114f9ecc1c287f6`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **决定／旧候选指针：** issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md；R09-A0034 ／ R09-A0035 ／ R09-A0036 ／ R09-A0037 ／ R09-A0038 ／ R09-A0039 ／ R09-A0040。
- **规范文本 SHA-256：** `a563335baa6496eaa73a78dc98a5815d52f3bd15353d4c1219b69574088a264f`。

### REQ-0173 — 成功预占后不可抢占。 候选计算不等于取得资源，只有原子预占成功的车辆才可下单；电量优先只在尚未取得预占的车辆…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0173`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 成功预占后不可抢占。 候选计算不等于取得资源，只有原子预占成功的车辆才可下单；电量优先只在尚未取得预占的车辆之间排序。一旦预占成功，在途期间也不得被后来的更低电量车辆取消、改写或窃取；新的低电量车辆等待下一个空闲桩。订单结果未知时原预占继续占用；只有充电停止/完成、原车离开且桩位恢复空闲均可确认后才释放。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md](../../../.scratch/current-requirements-baseline/issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md)；`决定充电失败改派的备用桩筛选与排队关系 > Answer; line 32`；来源 SHA-256 `417e9daa334340753ac2a606424da7017e672706da284715f114f9ecc1c287f6`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md。
- **决定／旧候选指针：** issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md；R09-A0034 ／ R09-A0035 ／ R09-A0036 ／ R09-A0037 ／ R09-A0038 ／ R09-A0039 ／ R09-A0040。
- **规范文本 SHA-256：** `743c5ad7dc809add137e2f74e7f9431e2f0f0cd9247f95ef21dcb63c9908d9db`。

## Required HITL resolution

- [ ] `REQ-0170`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0171`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0172`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0173`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0170`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0171`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0172`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0173`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-046`、Approval payload SHA-256 `2c62f6d6ef64ee597a8dbe668b8b2d5004fd30064e02578e0c737f66908ae57b`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
