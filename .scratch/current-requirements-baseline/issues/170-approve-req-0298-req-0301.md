# 最终批准 REQ-0298–REQ-0301：决定地图拓扑同步与历史快照产品边界

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-082
Approval payload SHA-256: 69c523cec37c441ca0325b64226827d2935fd477282e18cbe05aacd5917872d7
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-082` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0298 — 当前产品只同步 Map/Station 目录，不同步本地路网。 MapStationCatalogSnaps…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0298`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 当前产品只同步 Map/Station 目录，不同步本地路网。 MapStationCatalogSnapshot 覆盖 RIOT-8005-RUNTIME 当前全部有效 Map 及每张 Map 的全部 Station，用于 AREA 命名机台站点解析、FixedTaskStation 绑定、配置校验和变化检测。Edge、几何路网、本地最短路与动态交通状态均不进入本产品事实；派车可达性和路径成本继续使用已批准的实时 RIoT RouteCost 证据边界。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以版本化 HTTP/OpenAPI 契约测试验证字段、边界、排序、分页、错误和鉴权，并与运行时响应核对
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 42`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `651b4893445272b28131deab85a547ce53a5f597f7ca0c467c90a6206d141985`。

### REQ-0299 — 启动、周期和人工刷新共同维持目录。 服务启动时必须尝试一次全量同步，运行期间按投运前批准的周期执行非重入刷新…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0299`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 启动、周期和人工刷新共同维持目录。 服务启动时必须尝试一次全量同步，运行期间按投运前批准的周期执行非重入刷新，维护管理员和系统管理员可以手动触发；人工刷新不能编辑 RIoT 事实、绕过校验或强制发布候选。同步周期不在需求基线中猜定默认分钟数，也不把每次创建或派发 TransportDemand 变成同步触发点。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 43`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `9327668bf95d32bffb966a53434218d952e12ad506f894176028fadfaee56602`。

### REQ-0300 — 新快照只允许全量原子发布。 只有 Map 清单和每张有效 Map 的完整 Station 清单全部读取成功，…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0300`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 新快照只允许全量原子发布。 只有 Map 清单和每张有效 Map 的完整 Station 清单全部读取成功，Map 身份和同图 Station 身份唯一、必需标识及名称完整，候选才可一次性成为当前快照。任一调用失败、返回残缺、重复、缺字段、跨环境或无法确认来源时，整次候选拒绝；不得逐 Map 发布、混用不同轮次或用部分结果覆盖上一份有效快照。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 44`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `594bfa25448f9b07f61d25f7638f26a761f5dc7e0240a680d9b8067a745a8e63`。

### REQ-0301 — 本地可追溯身份弥补 RIoT 原生版本缺口。 每个不同内容的有效快照记录来源环境/build、完整观测起止时…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0301`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 本地可追溯身份弥补 RIoT 原生版本缺口。 每个不同内容的有效快照记录来源环境/build、完整观测起止时间、Map/Station 数量、规范化内容指纹和本地单调修订身份；RIoT gmtUpdate 或未来出现的原生版本只能作为附加来源证据，不能单独代替完整性身份。一次全量成功但内容未变化的观测只更新“最近完整确认时间”和审计，不制造重复内容修订。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以脚本化轮次进入生产 Host/领域入口、真实 SQL Server 持久化及正式 API 读回验证；现场 Oracle 事实仅由受控探针证明
- **精确来源：** [.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md](../../../.scratch/current-requirements-baseline/issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md)；`决定地图拓扑同步与历史快照产品边界 > Answer; line 45`；来源 SHA-256 `cd3bc6c26f9a9b0e6a36182f077ba506b3161a71d9c99408e536300203ecf87c`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md。
- **决定／旧候选指针：** issues/77-decide-map-topology-sync-and-snapshot-product-boundary.md；R03-A1880 ／ R03-A1885 ／ R03-A1889 ／ R03-A1901。
- **规范文本 SHA-256：** `49a81dc181ce11f02f0ec91fe8d2b114a54a351a7c7fc79c91beb45add1e749b`。

## Required HITL resolution

- [ ] `REQ-0298`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0299`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0300`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0301`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0298`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0299`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0300`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0301`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-082`、Approval payload SHA-256 `69c523cec37c441ca0325b64226827d2935fd477282e18cbe05aacd5917872d7`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
