# 最终批准 REQ-0268–REQ-0271：决定监控新鲜度、告警升级、重试与日志留存规则

Type: grilling
Status: resolved
Blocked by: 88
Batch: V1-APP-073
Approval payload SHA-256: b8556b1a60034e91d02a7fb999ca2ab784d9bdb93356aa9ce666cd9c67336787
Candidate ledger SHA-256: 9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646

## Question

用户是否逐条批准本批 4 个候选的精确规范文本、适用范围与验证方法进入首个当前需求基线 `v1.0.0`？

本批按同一规范来源和责任边界组织，每条仍须独立判断。使用 `grilling` 与 `domain-modeling`；不得由代理替用户关闭批准票。

## Batch boundary

- **来源：** [.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md](../../../.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md)
- **责任角色：** 该既有产品／领域决定的责任人与最终批准人
- **分批规则：** 同一来源内按 `REQ` 顺序分组，每批至多 4 条；分组只降低审阅负担，不合并需求或共享批准状态。
- **批次身份：** `V1-APP-073` + 本票 `Approval payload SHA-256` + 候选总账 SHA-256；任一绑定字段变化都必须重新生成并重新批准。

## Recommendation

默认建议逐条“批准”：这些候选已经完成来源层叠、冲突处置和当前规范化。这个建议不扩大证据权威；规格来源仅证明精确候选来源身份，既有 HITL 决定仅证明其决定内容，均不能替代用户对本条精确文本、范围、验证方法及批次身份的最终批准。

## Candidates

### REQ-0268 — 车队与仓位看板采用统一的 2 秒刷新节奏。 看板每 2 秒从 ControlServer 获取一次最新状态并…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0268`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 车队与仓位看板采用统一的 2 秒刷新节奏。 看板每 2 秒从 ControlServer 获取一次最新状态并支持人工刷新；2 秒是界面更新节奏，不是设备读取周期或读取超时。设备读取尚未结束时不得因为经过一个刷新周期就判定失败，也不得启动重叠读取。该规则不适用于 MesIngestWatch 页面。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md](../../../.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md)；`决定监控新鲜度、告警升级、重试与日志留存规则 > Answer; line 26`；来源 SHA-256 `42b04eba561fdd6ff55451124ba8e902d5c6039b7d3bb584d493f7e727041dd9`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **决定／旧候选指针：** issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md；R01-A0119 ／ R01-A1913 ／ R01-A1915 ／ R01-A1923 ／ R01-A1928 ／ R01-A2951 ／ R01-A3047 ／ R03-A0121 ／ R03-A0677 ／ R03-A1505 ／ R03-A1561 ／ R03-A3078 ／ R03-A3080。
- **规范文本 SHA-256：** `d974c45b697b814add1ab3f6b050cf02156b804c895f3f6ad5bf202637755d65`。

### REQ-0269 — 不可取得当前事实时直接表达原因，不引入“已过期”展示状态。 对应设备连接失败时显示“设备连接失败”，连接正常…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0269`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 不可取得当前事实时直接表达原因，不引入“已过期”展示状态。 对应设备连接失败时显示“设备连接失败”，连接正常但当前信息无法取得时显示“信息读取失败”；主看板不得继续把最后一次成功值呈现为当前值。最后一次成功值只可在排障详情中连同采集时间查看。TCP 明确断开仍立即按既有连接存活策略判定失联；其它连接失效继续沿用已批准的合法消息存活边界。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md](../../../.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md)；`决定监控新鲜度、告警升级、重试与日志留存规则 > Answer; line 27`；来源 SHA-256 `42b04eba561fdd6ff55451124ba8e902d5c6039b7d3bb584d493f7e727041dd9`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **决定／旧候选指针：** issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md；R01-A0119 ／ R01-A1913 ／ R01-A1915 ／ R01-A1923 ／ R01-A1928 ／ R01-A2951 ／ R01-A3047 ／ R03-A0121 ／ R03-A0677 ／ R03-A1505 ／ R03-A1561 ／ R03-A3078 ／ R03-A3080。
- **规范文本 SHA-256：** `88b8f732a63f3b6fcbeb120c0440cb2dd2db90bcd50c9777a636eac26c3c0846`。

### REQ-0270 — 告警可见对象按当前访问模型收敛。 与当前 AGV、当前停靠或当前操作直接相关的告警显示在对应 Onboard…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0270`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 告警可见对象按当前访问模型收敛。 与当前 AGV、当前停靠或当前操作直接相关的告警显示在对应 OnboardHmi；全部 8005 告警集中显示在 ControlServer，维护管理员和系统管理员均可查看。查看告警不扩大其处置权限；第一版不发送短信、邮件或企业微信，也不恢复 R-12/R-13 为系统授权角色。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 以公开 WPF/会话 seam 验证可观察行为；涉及视觉、DPI 或控件布局时另按 Golden WPF 流程取得用户预览批准
- **精确来源：** [.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md](../../../.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md)；`决定监控新鲜度、告警升级、重试与日志留存规则 > Answer; line 28`；来源 SHA-256 `42b04eba561fdd6ff55451124ba8e902d5c6039b7d3bb584d493f7e727041dd9`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **决定／旧候选指针：** issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md；R01-A0119 ／ R01-A1913 ／ R01-A1915 ／ R01-A1923 ／ R01-A1928 ／ R01-A2951 ／ R01-A3047 ／ R03-A0121 ／ R03-A0677 ／ R03-A1505 ／ R03-A1561 ／ R03-A3078 ／ R03-A3080。
- **规范文本 SHA-256：** `414c8b5b8a8bc236906bba06dcca5441ae64e9bc8066fb599f79106dbe80740e`。

### REQ-0271 — 服务端业务与管理员审计至少在线保留 180 天。 BusinessAuditRecord 与 Adminis…

- **推荐结论：** 批准按下列精确文本、范围与验证方法纳入 `v1.0.0`。这只是推荐；必须由用户对本条明确批准、拒绝或要求修订。
- **取舍：** 批准会把该文本和范围锁为首版规范输入，并接受所列验证边界；拒绝会在首版留下明确缺口；修订会产生新的精确候选并重新核对冲突、来源与影响。
- **候选永久需求身份：** `REQ-0271`；批准后生效，拒绝时编号仍不回收复用。
- **规范文本：** 服务端业务与管理员审计至少在线保留 180 天。 BusinessAuditRecord 与 AdministratorActionAuditRecord 在期限内必须可查询、导出，容量限制不得导致提前删除。超过 180 天后的继续保留、归档或清理由系统管理员配置，变更本身必须形成管理员操作审计记录。
- **适用范围：** 8005 多仓位 AGV 项目；更窄边界以本条文本及来源票据为准
- **验证方法：** 按来源决定的可观察状态、审计记录与边界案例形成验收；最终批准批次需补充或确认逐项 Given/When/Then
- **精确来源：** [.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md](../../../.scratch/current-requirements-baseline/issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md)；`决定监控新鲜度、告警升级、重试与日志留存规则 > Answer; line 29`；来源 SHA-256 `42b04eba561fdd6ff55451124ba8e902d5c6039b7d3bb584d493f7e727041dd9`。
- **来源批准边界：** 用户本人作为默认且唯一最终批准人；决定内容记录于来源票据；issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **形成与 AI 边界：** `verbatim-list-item`；AI 参与 `none`；来源层差异：该决定消解旧候选的冲突、未决或适用范围；旧声明原文保留在 R01–R13 来源去留账。
- **首版前替代与冲突处置：** resolved-decision-over-unapproved-source-claims; no deprecated REQ fabricated；resolved real conflict or ambiguity by issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md。
- **决定／旧候选指针：** issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md；R01-A0119 ／ R01-A1913 ／ R01-A1915 ／ R01-A1923 ／ R01-A1928 ／ R01-A2951 ／ R01-A3047 ／ R03-A0121 ／ R03-A0677 ／ R03-A1505 ／ R03-A1561 ／ R03-A3078 ／ R03-A3080。
- **规范文本 SHA-256：** `2c85c4c45ef9900a66706113853209690f662a11e72e7472c59d5c9ca490c4cf`。

## Required HITL resolution

- [ ] `REQ-0268`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0269`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0270`：批准／拒绝／修订（写明精确选择）
- [ ] `REQ-0271`：批准／拒绝／修订（写明精确选择）

只有用户对每一项作出明确选择，且所有修订项形成新的可核查精确文本后，本票才能记录 `## Answer` 并设为 `resolved`。批量回复“采用推荐值”仅在本票完整展示上述绑定内容且没有例外时，解释为逐条批准本批全部推荐项。

## Answer

用户本人作为本地图默认且唯一最终批准人，于 $approvedAt 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

- `REQ-0268`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0269`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0270`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。
- `REQ-0271`：批准本票所列精确规范文本、适用范围与验证方法进入 `v1.0.0`。

本批准绑定批次 `V1-APP-073`、Approval payload SHA-256 `b8556b1a60034e91d02a7fb999ca2ab784d9bdb93356aa9ce666cd9c67336787`、候选总账 SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`、当前 95 批 manifest SHA-256 `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md](../evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 `Superseded Answer` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
