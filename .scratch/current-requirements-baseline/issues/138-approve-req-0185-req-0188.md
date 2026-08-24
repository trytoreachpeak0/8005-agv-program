# 最终批准 REQ-0185–REQ-0188：决定 MES 运输候选的业务纳入与排除边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-050
Approval payload SHA-256: ad0f52567bbd04d766aef447924c0b9401ce881e114aeed05c956bdc448c340b
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md](../../../.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-050` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0185 — 共晶与低温共晶在选任务阶段排除。 项目维护 TransportExecutionExcludedArea 列…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0185`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 共晶与低温共晶在选任务阶段排除。 项目维护 TransportExecutionExcludedArea 列表；MES AREA 机台端点命中时仍保留 TransportDemand，但不得派车或装货。该判断不在 MesIngest 执行。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md](../../../.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md)；`决定 MES 运输候选的业务纳入与排除边界 > Answer; line 24`；来源 SHA-256 `364954262dc136c5e4def75e10e2476f2d532ddd0ebf4bef2487827aa1c0a4a2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **决定／旧候选指针：** issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md；R01-A0045 ／ R01-A0047 ／ R01-A0048 ／ R01-A0051。
- **规范文本 SHA-256：** `dda6c3ce8f93de4984c0d429ca97ffd3ca99f6f016848d34e47cb8a74eb5bc2b`。

### REQ-0186 — PACKAGE 缺值与容量未覆盖分层处理。 PACKAGE 空值属于字段完整性失败，由 MesIngest …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0186`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** PACKAGE 缺值与容量未覆盖分层处理。 PACKAGE 空值属于字段完整性失败，由 MesIngest 单行报警并隔离；PACKAGE 有值但没有匹配到已批准容量规则时，TransportDemand 继续保留，由 8005 任务/装货准备模块形成 LoadPreparationAlert，在仓位分配和开锁前阻断。该模块逐 DemandId 保存 PACKAGE、TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、首次发现、最后发现、当前是否仍未覆盖，并按 PACKAGE 汇总当前/累计受影响需求数、首次/最后发现时间及 TASK_TYPE 分布；相同需求按轮次更新而不重复插入，规则补齐后关闭告警但永久保留历史。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md](../../../.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md)；`决定 MES 运输候选的业务纳入与排除边界 > Answer; line 25`；来源 SHA-256 `364954262dc136c5e4def75e10e2476f2d532ddd0ebf4bef2487827aa1c0a4a2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **决定／旧候选指针：** issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md；R01-A0045 ／ R01-A0047 ／ R01-A0048 ／ R01-A0051。
- **规范文本 SHA-256：** `857f27a312f4a2e3f9dcb57fb039704003862a1d251d1259e70310b88a515b91`。

### REQ-0187 — AREA→EQP 唯一性是选任务门禁。 当前客户数据允许一个 AREA 对应多台机，客户后续将调整为 ARE…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0187`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** AREA→EQP 唯一性是选任务门禁。 当前客户数据允许一个 AREA 对应多台机，客户后续将调整为 AREA 与机台一一对应。8005 需要独立的 AreaEqpUniquenessMonitor，针对老厂 AREA 名册直接查询设备主数据，不按工序过滤；每个 AREA 必须恰好返回一个 EQP。结果为零、多台、查询失败或超过新鲜度期限时，保留 TransportDemand，产生选任务告警并暂停新的相关选任务，已在执行中的任务不受影响；服务启动、名册变更时立即检查，并按可配置周期重复检查。EQP→AREA 的反向唯一性由客户 MES 自身卡控，8005 不重复验证。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md](../../../.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md)；`决定 MES 运输候选的业务纳入与排除边界 > Answer; line 26`；来源 SHA-256 `364954262dc136c5e4def75e10e2476f2d532ddd0ebf4bef2487827aa1c0a4a2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **决定／旧候选指针：** issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md；R01-A0045 ／ R01-A0047 ／ R01-A0048 ／ R01-A0051。
- **规范文本 SHA-256：** `8464c1a3c145552c30b77342abb2ac91c8bf5c3882215210b91a7976ed5d02b5`。

### REQ-0188 — 旧 SQL 只提供查询原型。 GetEqpnoByArea.sql 的 SHA-256 为 4eaee079…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0188`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 旧 SQL 只提供查询原型。 GetEqpnoByArea.sql 的 SHA-256 为 4eaee07989a0e2e9d3b7c296c8148c16a807cd52eae2dc100a0784c5787f78b0，证明可从 fw_eqpres_eqpinformation 按 AREA 查询 EQP；其中 step = '装片' 不属于新监控器的唯一性条件，旧程序 ExecuteScalar 只取首行的行为也不得复用，因为它会掩盖多 EQP 冲突。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md](../../../.scratch/current-requirements-baseline/issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md)；`决定 MES 运输候选的业务纳入与排除边界 > Answer; line 27`；来源 SHA-256 `364954262dc136c5e4def75e10e2476f2d532ddd0ebf4bef2487827aa1c0a4a2`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md。
- **决定／旧候选指针：** issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md；R01-A0045 ／ R01-A0047 ／ R01-A0048 ／ R01-A0051。
- **规范文本 SHA-256：** `492c84f4cf2e781d5910c2f9321bf37dca6dfefbe113d315319e80c6718e42da`。

## Required HITL resolution

- [ ] `REQ-0185`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0186`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0187`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0188`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0185`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0186`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0187`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0188`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-050`、Approval payload SHA-256 `ad0f52567bbd04d766aef447924c0b9401ce881e114aeed05c956bdc448c340b`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
