# 最终批准 REQ-0321–REQ-0324：决定 AREA 显式覆盖的维护与生效治理

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-088
Approval payload SHA-256: 4a3b9574b15bf5d34c56190415dacd1c7a758fc7eee0d8e8f7f305fad6a1a8e3
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-088` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0321 — 机台侧站点只按命名规则自动识别。 一张 Map 内，只有 stationName 由一个至三个合法 MES …

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0321`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 机台侧站点只按命名规则自动识别。 一张 Map 内，只有 stationName 由一个至三个合法 MES AREA 编码以下划线连接形成的 Station 才是 AreaNamedMachineStation；系统据此建立 AREA 到 Station 的反向解析关系，不提供人工覆盖或自动猜测旁路。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)；`决定 AREA 显式覆盖的维护与生效治理 > Answer; line 19`；来源 SHA-256 `d63b7aacda000b2dc1baa4a18f1036db4297055f4b15bf8cac4470b223914d14`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/79-decide-area-override-maintenance-and-effectivity-governance.md；R01-A1897。
- **规范文本 SHA-256：** `83e560b38589a47ec7a86e24d3c7e1ff648549e02fc59c4aa9ec0f03f446bb37`。

### REQ-0322 — AREA 必须唯一解析。 同一 AREA 没有匹配或同时命中多个 Station 时，相关新 Transpo…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0322`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** AREA 必须唯一解析。 同一 AREA 没有匹配或同时命中多个 Station 时，相关新 TransportDemand 阻断并形成精确告警；系统不得自动择一。地图维护人员只能通过修正地图站点名称消除问题，不能用本地覆盖掩盖地图事实。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)；`决定 AREA 显式覆盖的维护与生效治理 > Answer; line 20`；来源 SHA-256 `d63b7aacda000b2dc1baa4a18f1036db4297055f4b15bf8cac4470b223914d14`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/79-decide-area-override-maintenance-and-effectivity-governance.md；R01-A1897。
- **规范文本 SHA-256：** `646dad157e372d76b20271a2aaafc7c486af61e0908e30ba401d7f94c062b06c`。

### REQ-0323 — 非 AREA 命名站点不一律视为异常。 地图可以包含公共业务点、等待点、充电点及其它普通 Station；它…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0323`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 非 AREA 命名站点不一律视为异常。 地图可以包含公共业务点、等待点、充电点及其它普通 Station；它们不因名称无法解析为 AREA 而形成全图“解析失败”清单。只有具体 MES AREA 无法得到唯一机台站点时才形成任务相关的解析异常。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以故障注入/状态机测试覆盖安全门禁，并在适用时用受控现场记录核对；不得以模拟结果冒充现场通过
- **精确来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)；`决定 AREA 显式覆盖的维护与生效治理 > Answer; line 21`；来源 SHA-256 `d63b7aacda000b2dc1baa4a18f1036db4297055f4b15bf8cac4470b223914d14`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/79-decide-area-override-maintenance-and-effectivity-governance.md；R01-A1897。
- **规范文本 SHA-256：** `6eac036661df2548254f10c70b3a81c2eb6fb3720e77fbf5023081817a76819d`。

### REQ-0324 — 公共业务点走独立绑定。 派工待送、烘箱、关卡、三光和氮气柜等使用 PublicStationFunction…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0324`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 公共业务点走独立绑定。 派工待送、烘箱、关卡、三光和氮气柜等使用 PublicStationFunction；每张 Map 上的每种功能显式绑定一个 FixedTaskStation，TransportDemand 按任务类型使用对应功能，不把公共业务点伪装成 MES AREA 站点。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md](../../../.scratch/current-requirements-baseline/issues/79-decide-area-override-maintenance-and-effectivity-governance.md)；`决定 AREA 显式覆盖的维护与生效治理 > Answer; line 22`；来源 SHA-256 `d63b7aacda000b2dc1baa4a18f1036db4297055f4b15bf8cac4470b223914d14`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/79-decide-area-override-maintenance-and-effectivity-governance.md。
- **决定／旧候选指针：** issues/79-decide-area-override-maintenance-and-effectivity-governance.md；R01-A1897。
- **规范文本 SHA-256：** `ba8b5971ec42815a523a7ad2192a34bb706dbccfa48ed3bae6736ff9a8537be0`。

## Required HITL resolution

- [ ] `REQ-0321`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0322`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0323`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0324`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0321`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0322`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0323`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0324`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-088`、Approval payload SHA-256 `4a3b9574b15bf5d34c56190415dacd1c7a758fc7eee0d8e8f7f305fad6a1a8e3`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
