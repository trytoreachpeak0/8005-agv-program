# 最终批准 REQ-0306–REQ-0309：决定地图拓扑同步与历史快照产品边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-084
Approval payload SHA-256: 935ce29e076f740ef68d888796b3db8b6652152341dd9552a8f825352039ecf3
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-084` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0306 — 已经存在的 RIoT 订单不因目录变化被自动取消。 已建单或正在执行的移动继续按其 RIoT OrderRe…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0306`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 已经存在的 RIoT 订单不因目录变化被自动取消。 已建单或正在执行的移动继续按其 RIoT OrderRef 观察、对账和收敛，目录变化不重写订单或已完成历史；若后续尚未建单的停靠失效，则在该次新 move 前阻断。已经载货而无法继续时进入既有异常处置与货物闭环，不以目录同步自行选择新目的地。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 50`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `671e46d25e2b97aece7b805919c3814fc234c2e0e576dcdd96f7b00bb1e8edf7`。

### REQ-0307 — 历史快照按引用和审计期限共同留存。 任何仍被活动或保留期内 TransportDemand、配置版本、审计记…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0307`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 历史快照按引用和审计期限共同留存。 任何仍被活动或保留期内 TransportDemand、配置版本、审计记录或未关闭异常事件引用的目录修订不得删除；历史修订只供解释和审计，不能重新成为新业务的当前目录。无引用的已替代修订、成功/失败同步尝试及人工刷新审计至少在线保留 180 天，之后才可按 BusinessAuditRetentionPolicy 由系统管理员配置归档或清理并记录管理员操作审计。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 51`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `8e55ccc9f6f5d875ea8de45fc4c8bd03d35f9d26f66f29a49f31dc890bb73fa5`。

### REQ-0308 — 同步异常形成目录级状态，真实缺站形成任务级阻断。 刷新失败、候选无效、超过新鲜度或 build/环境不兼容形…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0308`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 同步异常形成目录级状态，真实缺站形成任务级阻断。 刷新失败、候选无效、超过新鲜度或 build/环境不兼容形成按原因去重并持续更新的 Map/Station 目录不可用状态，在 ControlServer 向维护管理员和系统管理员展示；不得为每轮轮询或每个等待任务重复制造告警。当前有效快照已经证明具体 Map/Station 缺失时，受影响任务形成精确的 StructuralDispatchBlock；恢复完整快照或修复真实目录后重新评估，但不绕过其它门禁。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 52`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `cc0678a664944e401868a33f52e73762affbb12da90ddddb0e91701b9c4db4ff`。

### REQ-0309 — 具体 API 与数据结构继续留给证据验证和正式设计。 实现只能经已批准的 RIoT Map/Station …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0309`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 具体 API 与数据结构继续留给证据验证和正式设计。 实现只能经已批准的 RIoT Map/Station 只读调用面和具名 Facade 获取目录；目标环境权限、全量语义、分页/数量一致性和必需字段必须在激活前验证，缺失能力不得以手工录入、Edge 数据或未授权接口补洞。具体 endpoint 组合、分页协议、超时与重试参数、事务和表结构、内容指纹算法、DTO、界面及部署方式均属于后续正式 spec、系统设计与实施验收，不进入本次需求基线。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 53`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `16088f65ca990409cb90bfb894d206ff474c73a2e88ae0734e9b025aad457734`。

## Required HITL resolution

- [ ] `REQ-0306`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0307`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0308`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0309`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0306`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0307`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0308`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0309`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-084`、Approval payload SHA-256 `935ce29e076f740ef68d888796b3db8b6652152341dd9552a8f825352039ecf3`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
