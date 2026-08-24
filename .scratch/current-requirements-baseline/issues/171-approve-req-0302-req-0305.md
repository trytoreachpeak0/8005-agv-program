# 最终批准 REQ-0302–REQ-0305：决定地图拓扑同步与历史快照产品边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-083
Approval payload SHA-256: acb0effb5bc88d9812aea9c98fc4b1a42acd6021dc4f3ee2cc96406ab4db606f
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-083` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0302 — 新鲜度按最近完整确认计算。 同步周期和最大允许未确认时长必须在投运前分别批准，且最大未确认时长须大于正常同步…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0302`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 新鲜度按最近完整确认计算。 同步周期和最大允许未确认时长必须在投运前分别批准，且最大未确认时长须大于正常同步周期；没有批准值时不得启用依赖 Map/Station 的业务。暂时刷新失败但仍处于允许时长内时，可以明确标记使用最后已知有效快照，并继续由实时 RouteCost 完成建单前可达性校验；不得把失败描述为已经取得最新 RIoT 目录。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 46`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `aa54818e945400b45636cb4d6a3ecc0798cd7e1ea91aad4b913803b26f0ef7a2`。

### REQ-0303 — 无快照或超过新鲜度边界时 fail-closed。 系统仍可启动并展示、诊断和重试同步，也可继续观察已经存在…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0303`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 无快照或超过新鲜度边界时 fail-closed。 系统仍可启动并展示、诊断和重试同步，也可继续观察已经存在的 RIoT 订单，但不得激活 Map/Station 相关配置、为新 TransportDemand 解析执行站点、为尚未建单的任务创建新的 RIoT move 订单。错误环境、未批准 build 或接口契约不兼容产生同一业务门禁；保留的旧快照只有在仍处于批准的新鲜度范围内才能继续支持新动作。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 47`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `9a3d9bfeb1d701e611acde561f7f92f97e9e4a4c12ed80faec10016f651eb927`。

### REQ-0304 — 新目录自动成为当前事实，但不自动改写业务配置。 完整候选发布后，新增、删除、激活状态变化、Map/Stati…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0304`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 新目录自动成为当前事实，但不自动改写业务配置。 完整候选发布后，新增、删除、激活状态变化、Map/Station 改名或身份变化都进入新的不可变修订，并重新评估 AREA 命名解析与依赖站点的配置有效性。系统不得因此编辑 RIoT 地图、自动猜测公共站点功能、替换 FixedTaskStation 绑定或把一个失效站点静默映射到另一个站点；公共业务点绑定的具体失效、复核与重新激活由决定公共业务点绑定的维护与生效治理继续收敛。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 48`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `37c276132d58ab9113273402f8e1c2c1397e1338b4d988a99724fb734500ba3a`。

### REQ-0305 — TransportDemand 冻结已解析站点且不被后续目录重写。 新任务只可从当时新鲜的当前快照取得并冻结…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0305`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** TransportDemand 冻结已解析站点且不被后续目录重写。 新任务只可从当时新鲜的当前快照取得并冻结 mapId + stationId、当时名称和目录修订；后续改名不改变既有 Station 身份，也不重新解析任务。每次尚未创建的新 RIoT move 订单仍须确认冻结的 mapId + stationId 存在于当前新鲜快照并通过 RouteCost；Map 失效、Station 身份消失或目录不可用时阻断该新动作并记录精确原因，禁止自动换站、换图或用相似名称重映射。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 49`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `150e4ea3dfbfb7b01d7e21695b972190fc7ffd814c7645235fc332477cbe831a`。

## Required HITL resolution

- [ ] `REQ-0302`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0303`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0304`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0305`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0302`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0303`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0304`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0305`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-083`、Approval payload SHA-256 `acb0effb5bc88d9812aea9c98fc4b1a42acd6021dc4f3ee2cc96406ab4db606f`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
