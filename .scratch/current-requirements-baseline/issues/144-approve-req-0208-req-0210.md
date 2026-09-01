# 最终批准 REQ-0208–REQ-0210：决定派车评分、路网成本与无车响应升级规则

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-056
Approval payload SHA-256: c1fabbe5fe5540110ef05552502dafe4522e247015abf8294f750d541ed914b7
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 3 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-056` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0208 — 电量和仓位首先是硬资格。 车辆预计完成任务后无法保留经批准的最低电量余量，或电量未知时，直接退出候选；通过后…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0208`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 电量和仓位首先是硬资格。 车辆预计完成任务后无法保留经批准的最低电量余量，或电量未知时，直接退出候选；通过后电量只作其它选车层全部相同时的末级裁决，具体阈值由后续充电阈值票据治理。可用仓位数量、规格、载重及当前已载任务兼容性不足时同样退出候选；通过后不因剩余空仓更多而取得排序优势。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 27`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `06970736bafc92804bbb65c144ecdc25340c8f6ae616b8281c180cf8dd1c06b5`。

### REQ-0209 — 最终并列必须确定且可审计。 任务所有业务层相同时按本地创建时间、再按 DemandId 稳定排序；车辆所有业…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0209`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 最终并列必须确定且可审计。 任务所有业务层相同时按本地创建时间、再按 DemandId 稳定排序；车辆所有业务层相同时优先从未成功接单者、再按上次成功接单时间从早到晚、最后按 agvId 稳定排序。不得使用随机选择或依赖未声明的数据库顺序。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 28`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `2b9bbafb8c3745a2269fbf20448770ecd22b3fc24351af93316aa09046b80736`。

### REQ-0210 — 正常积压与结构性无解分别升级。 所有车辆只是忙碌、容量暂满或单车位站点暂被占用时，任务保持正常积压并展示等待…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0210`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 正常积压与结构性无解分别升级。 所有车辆只是忙碌、容量暂满或单车位站点暂被占用时，任务保持正常积压并展示等待状态，达到该分区批准的防饥饿阈值后再升级告警。地图不一致、站点缺失、全部路线不可达或必要准入配置缺失等导致任务没有任何潜在合法车辆时，立即形成按任务与原因去重的 StructuralDispatchBlock 告警；同一原因持续存在只更新既有告警，不按每轮调度重复新建。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md](../../../.scratch/current-requirements-baseline/issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)；`决定派车评分、路网成本与无车响应升级规则 > Answer; line 29`；来源 SHA-256 `ef0b1934343111a56282b570fe8c31695719b36f03a5470fa1c9c4a8b6199129`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md。
- **决定／旧候选指针：** issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md；R01-A0095 ／ R01-A0294 ／ R01-A0295 ／ R01-A0729 ／ R01-A0732 ／ R01-A1887 ／ R01-A1889 ／ R02-A0304 ／ R02-A0988 ／ R02-A0990 ／ R02-A1007 ／ R02-A1009 ／ R03-A1541。
- **规范文本 SHA-256：** `f85040d72a56a0c3742a22ff59f0b331f8508257c529f8eb2ac851cc223b2b9f`。

## Required HITL resolution

- [ ] `REQ-0208`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0209`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0210`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0208`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0209`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0210`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-056`、Approval payload SHA-256 `c1fabbe5fe5540110ef05552502dafe4522e247015abf8294f750d541ed914b7`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
