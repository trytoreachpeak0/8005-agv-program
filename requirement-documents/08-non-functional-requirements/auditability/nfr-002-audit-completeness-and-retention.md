---
id: NFR-002
type: non-functional-requirement
title: "Audit Completeness and Retention 关键操作审计完整性与留存"
status: draft
priority: high
category: auditability
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-001", "UC-002", "UC-005", "UC-006", "UC-010", "UC-034", "UC-043", "UC-044", "UC-014", "UC-015", "UC-016", "UC-017", "UC-018", "UC-039", "UC-013", "UC-019", "UC-020", "UC-038"]
related_fr: ["FR-001", "FR-002", "FR-003", "FR-004", "FR-005", "FR-006", "FR-007", "FR-008", "FR-009", "FR-011", "FR-012", "FR-013", "FR-014", "FR-016", "FR-017", "FR-018", "FR-019", "FR-020", "FR-021", "FR-022", "FR-023", "FR-024", "FR-025", "FR-026", "FR-027", "FR-028"]
related_tc: []
aliases: ["NFR-002"]
---

# NFR-002 Audit Completeness and Retention 关键操作审计完整性与留存

## Description 需求描述

对影响任务、仓位状态、开锁/装载结果及安全相关拒绝的关键操作，系统应完整记录可追溯审计信息，并在约定留存期内可查询与导出，以满足搬运过程可追溯与事后审计需要。

## Category 质量属性类别

`auditability`

## Context / Stimulus 工况与刺激

- 适用：生产与试运行期间发生的关键业务写操作与关键拒绝（如任务范围核验失败、开锁失败、占位落库、异常锁定等）。
- 刺激：质量/班组追溯某次错装或拒绝开锁；审计人员按时间范围导出操作记录（见 [[uc-034-query-and-export-audit-logs|UC-034]]）。
- 不包括：调试级超详细追踪日志的永久留存策略（可由运维日志另定）；外部系统（MES/RCS）侧日志不在本 NFR 范围。

## Metric / Scale 度量指标

1. **完整性**：关键操作成功或失败后，是否存在对应审计记录；记录是否包含最低字段集。
2. **留存期**：审计记录自写入起可查询/导出的最短保留天数。
3. **时效性（可选草稿）**：记录对查询可见的延迟上限。

**最低字段集（初稿）：** 操作时间、操作者（或系统主体）、操作类型、关联对象标识（如任务 ID / 子批号 / 仓位号 / AGV ID，视事件而定）、结果（成功/失败及原因摘要）、关联会话或请求标识（如有）。

## Target / Fit Criterion 目标与适合标准

> 留存天数待与客户质量/IT 确认；以下为可评审草稿。

- **FC-1（完整性）**
  - **Given** 发生一次属于“关键操作”目录的事件（含拒绝类，例如 FR-001 范围外拒绝、FR-002 开锁失败或占位落库）
  - **When** 事件处理结束
  - **Then** 系统中存在对应审计记录，且包含最低字段集；不得出现“业务已变更但无审计记录”的静默成功/失败

- **FC-2（留存）**
  - **Given** 一条已写入的关键操作审计记录
  - **When** 在写入后的留存期内通过查询/导出接口访问
  - **Then** 记录仍可被查询与导出；留存期 ≥ **180 天**（TBD：最终天数以客户确认准）

- **FC-3（查询可见延迟）**
  - **Given** 一条关键操作审计记录刚写入
  - **When** 授权用户按 [[uc-034-query-and-export-audit-logs|UC-034]] 查询
  - **Then** 在 **≤ 5 分钟**内可见（TBD；若实现为同步写入则可更严）

## Measurement Method 测量方法

1. 维护“关键操作”事件目录（与 FR/UC 对齐，评审冻结）。
2. 对目录内事件做抽样或自动化断言：业务结果与审计记录 1:1（或约定的聚合规则）对应，字段齐全。
3. 用带时间戳的样例数据验证留存与过期策略（或配置项 + 集成测试）。
4. 验收时由质量/班组按 UC-034 实际查询/导出抽查。

## Origin / Rationale 来源与制定原因

- [[vision-and-scope|愿景与范围]]：业务目标与成功指标要求搬运过程可追溯；质量约束要求数据可追溯性。
- [[uc-034-query-and-export-audit-logs|UC-034]]：提供查询与导出能力，本 NFR 约束其数据完整性与留存。
- 限制条款：流程模板不得绕过审计要求。

## Related 关联

- **Functional Requirements：** 约束 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]]、[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]]（UC-001 装载）、[[fr-003-confirm-completion-eligibility-check|FR-003]]、[[fr-004-batch-task-completion-session-closure-and-non-reversibility|FR-004]]（UC-002 确认完成）、[[fr-005-mis-stored-retrieval-eligibility-check|FR-005]]、[[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]]（UC-005 存错取出）、[[fr-007-task-cancellation-eligibility-check-and-state-rollback|FR-007]]（UC-006 取消运送）、[[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]]、[[fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation|FR-009]]（UC-010 终点取出）、[[fr-011-identity-and-role-verification-via-mes|FR-011]]、[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]]、[[fr-013-session-termination-rules|FR-013]]（UC-043 身份核验与操作会话）、[[fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration|FR-014]]（UC-044 残留仓位重新打开）、[[fr-016-slot-enable-disable-batch-eligibility-and-state-update|FR-016]]（UC-014 仓位启用/禁用）、[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]]、[[fr-018-slot-light-curtain-function-test|FR-018]]、[[fr-019-slot-door-state-detection-test|FR-019]]（UC-015/016/017 硬件功能测试）、[[fr-020-bidirectional-io-point-mapping-verification|FR-020]]、[[fr-021-slot-to-io-point-mapping-create-modify-validation|FR-021]]（UC-018/039 IO 点位映射核对与配置）、[[fr-022-slot-model-draft-field-and-layout-validation|FR-022]]、[[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]]、[[fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation|FR-024]]（UC-038 多仓位AGV模型草稿/发布/停用）、[[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]]、[[fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging|FR-026]]（UC-019 从 RCS 接入 AGV）、[[fr-027-agv-enable-disable-state-transition-and-pending-effect-handling|FR-027]]（UC-013 AGV 启用/禁用）、[[fr-028-agv-dispatch-profile-update-eligibility-and-persistence|FR-028]]（UC-020 AGV 调度配置维护）等产生关键写/拒绝的能力必须可审计；后续权限变更等 FR 同样适用。不含 [[fr-010-arrival-status-update-and-operation-panel-navigation|FR-010]]、[[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]]、[[fr-029-agv-archive-eligibility-check-and-state-transition|FR-029]]、[[fr-030-agv-fleet-dashboard-display-and-eligibility-reasoning|FR-030]]——对应 UC 均为纯只读展示，或 Postcondition 未显式要求记录审计，见各自 FR 的 Notes 说明。
- **Use Cases：** [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-002-confirm-task-completion|UC-002]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-006-cancel-transport-task-upon-arrival|UC-006]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]]（装载/确认/纠错/取消/取出场景产生审计）、[[uc-043-verify-identity-and-manage-operation-session|UC-043]]（身份核验成功/失败、会话开始、阶段切换及结束均记录审计）、[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]]（残留仓位重新打开、清空核验过程记录审计）、[[uc-014-enable-disable-slot|UC-014]]（仓位启用/禁用批量操作记录审计）、[[uc-015-slot-door-unlock-open-test|UC-015]]、[[uc-016-slot-light-curtain-function-test|UC-016]]、[[uc-017-slot-door-state-detection-test|UC-017]]（硬件功能测试结果记录审计）、[[uc-018-io-point-mapping-verification-test|UC-018]]、[[uc-039-maintain-slot-io-point-mapping|UC-039]]（IO 点位映射核对结果与配置变更记录审计）、[[uc-038-maintain-agv-slot-model|UC-038]]（型号草稿变更、发布、停用记录审计）、[[uc-019-register-agv-from-rcs|UC-019]]（接入操作及配置内容记录审计）、[[uc-013-enable-disable-agv|UC-013]]（启用/禁用操作记录审计）、[[uc-020-maintain-agv-dispatch-profile|UC-020]]（调度配置变更记录审计）、[[uc-034-query-and-export-audit-logs|UC-034]]（消费审计数据）。

## Verification 验证方式

对应 Test Case / 审计专项验收待建。建议：关键成功与拒绝路径各至少一条端到端“操作 → 记录 → 查询/导出”；留存策略用配置或时钟模拟验证。

## Notes 备注

- **180 天 / 5 分钟**为草稿目标，确认前不得当作已承诺合规指标。
- “关键操作”目录需在首批 FR 评审时冻结一版，避免 NFR 无法判定。
- 本 NFR 不替代 UC-034 的交互流程；也不替代具体“写审计”的功能需求——若后续将“审计写入服务”拆成独立 FR，本 NFR 仍作为完整性与留存的质量约束。
- 2026-07-14：01-site-operations 域第二批（UC-002/005/006/010）拆出的 FR-003~FR-009 已按同一规则纳入 `related_fr`——包括核验类 FR（如 FR-005、FR-007）在内，因为其拒绝路径同样属于 Context/Stimulus 中定义的"关键拒绝"，需要审计记录。
- 2026-07-14：01-site-operations 域第三批（UC-003/043/044）拆出的 FR-010~FR-014 中，[[fr-011-identity-and-role-verification-via-mes|FR-011]]、[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]]、[[fr-013-session-termination-rules|FR-013]]、[[fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration|FR-014]] 已纳入 `related_fr`；[[fr-010-arrival-status-update-and-operation-panel-navigation|FR-010]]（UC-003 到站状态更新）不纳入，因其对应的 UC-003 Postcondition 未显式要求记录审计，与其余 8 条已登记 FR 所在 UC 的写法不同，保持"不是每条 FR 都需要 NFR"的既定原则。至此 `01-site-operations` 域 8 个 UC（UC-001/002/003/005/006/010/043/044）已全部有对应 FR 覆盖。
- 2026-07-14：`02-slot-and-hardware` 域三批（UC-011/014/015/016/017/018/039）拆出的 FR-015~FR-021 中，[[fr-016-slot-enable-disable-batch-eligibility-and-state-update|FR-016]]、[[fr-017-slot-door-unlock-open-test-and-result-recording|FR-017]]、[[fr-018-slot-light-curtain-function-test|FR-018]]、[[fr-019-slot-door-state-detection-test|FR-019]]、[[fr-020-bidirectional-io-point-mapping-verification|FR-020]]、[[fr-021-slot-to-io-point-mapping-create-modify-validation|FR-021]] 已纳入 `related_fr`；[[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]]（UC-011 仓位监控看板）不纳入，因其对应的 UC-011 是纯只读查询，不改变任何数据、Postcondition 未要求记录审计，与 FR-010 的既定处理方式一致。
- 2026-07-14：`03-agv-fleet-management` 域三批（UC-013/019/020/021/022/038）拆出的 FR-022~FR-030 中，[[fr-022-slot-model-draft-field-and-layout-validation|FR-022]]、[[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]]、[[fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation|FR-024]]（UC-038，BR-008 第 5 条要求发布/停用二次认证并审计）、[[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]]、[[fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging|FR-026]]（UC-019 Postcondition 5 明确"接入操作及配置内容被记录到审计日志"）、[[fr-027-agv-enable-disable-state-transition-and-pending-effect-handling|FR-027]]（UC-013 Postcondition 4）、[[fr-028-agv-dispatch-profile-update-eligibility-and-persistence|FR-028]]（UC-020 Postcondition 3）已纳入 `related_fr`；[[fr-029-agv-archive-eligibility-check-and-state-transition|FR-029]]（UC-021 归档）与 [[fr-030-agv-fleet-dashboard-display-and-eligibility-reasoning|FR-030]]（UC-022 车队看板，纯只读）不纳入——UC-021 Postcondition 未显式要求记录审计（Normal Flow 第 7 步"记录操作人、时间和原因"是否等同于本 NFR 定义的完整审计记录仍存歧义，按从严规则暂不纳入，与 FR-010/FR-015 的既定处理方式一致），UC-022 是纯只读查询同样不纳入。
