---
id: BR-003
type: business-rule
title: "AREA-to-Station Mapping AREA—地图站点映射规则"
status: draft
created: 2026-07-13
updated: 2026-07-13
related_uc: ["UC-007", "UC-008", "UC-023", "UC-024", "UC-026", "UC-027", "UC-028", "UC-029"]
related_br: ["BR-001", "BR-002", "BR-004", "BR-005", "BR-006"]
aliases: ["BR-003"]
---

# BR-003 AREA-to-Station Mapping AREA—地图站点映射规则

## Rule Statement 规则内容

### 1. 映射基数

1. 一个非空 MES AREA 在同一时间只能存在一个有效的 RCS/RIOT 地图站点映射。
2. 多个 AREA 可以映射到同一个地图站点，用于多个相邻机台共用停车或接驳点。
3. 系统不得根据 AREA 名称猜测站点，也不得在多个候选站点中自动任选一个。

### 2. 站点来源与有效性

1. 可选站点必须来自 RCS/RIOT 当前地图站点列表。
2. 管理员不能手工录入一个未被 RCS/RIOT 确认存在的站点编号。
3. 站点列表同步失败、结果不完整或站点状态无法确认时，采用 fail-closed：允许只读查看，禁止新增、修改或重新启用映射。
4. 已启用映射的目标站点后续从 RCS/RIOT 消失或失效时，系统应将映射标记为异常；依赖该映射的新任务不得进入分配和下发。

### 3. 版本与停用

1. 映射不物理删除。修改时关闭原有效版本并创建新版本；不再使用时将当前版本停用。
2. 每个版本至少记录 AREA、目标站点、状态、生效时间、失效时间、操作人、原因和审计信息。
3. 新版本或停用只影响生效后创建的新任务。
4. 已创建任务继续使用创建时冻结的 AREA、EQP、起点和终点快照，不因映射变化自动更新。

### 4. 任务使用规则

1. [[uc-007-sync-transport-task-from-mes|UC-007]] 创建任务时，必须按任务创建时刻读取有效映射并冻结站点快照。
2. AREA 为空、映射缺失、映射已停用、映射异常或目标站点无效时，任务进入“位置异常（LOCATION_ERROR）”，不得下发。
3. 起终点未成功解析并冻结的任务，不得进入 [[br-001-dispatch-task-range|BR-001]] 的派车任务范围，也不得进入 [[uc-023-allocate-transport-tasks-to-agv|UC-023]] 的车辆分配。
4. [[uc-008-dispatch-move-order-to-riot|UC-008]] 使用任务已冻结的站点下发 RCS/RIOT，不在下发时重新解析 AREA。

### 5. 流程步骤使用边界

1. 本规则的映射校验/查询能力可由 [[uc-026-select-template-and-create-workflow-instance|UC-026]] 和 [[uc-027-execute-workflow-steps|UC-027]] 作为预置能力调用，但流程只能读取、校验并冻结已由 UC-024 人工维护且发布生效的映射版本。
2. [[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]、任何模板、条件跳过、重试或人工异常处置均不得修改映射、猜测/替换站点、覆盖历史任务快照或绕过本规则的 fail-closed 条件。
3. 映射异常步骤只能失败或等待有权限人员通过 UC-024 修复；流程实例状态不得替代任务的“位置异常”业务语义。

## Rationale 制定原因

MES AREA 是生产位置编码，RCS/RIOT 地图站点是 AGV 可导航目标，两者语义不同。通过显式、版本化映射，可以避免机台移位或地图调整后把历史任务改派到错误位置，并确保站点配置变更可审计、可追溯。

## Source 来源

2026-07-13 需求确认：

- R-12 和 R-13 均可维护映射。
- 地图站点必须从 RCS/RIOT 同步，不允许任意手工录入。
- 映射修改只影响新任务。
- 不再使用的映射采用停用并保留历史，不物理删除。

## Related Use Cases 关联用例

- [[uc-024-maintain-area-station-mapping|UC-024]]：执行本规则规定的新增、修改、停用、同步和审计。
- [[uc-007-sync-transport-task-from-mes|UC-007]]：任务创建时解析并冻结站点。
- [[uc-023-allocate-transport-tasks-to-agv|UC-023]]：排除位置异常或站点未冻结的任务。
- [[uc-008-dispatch-move-order-to-riot|UC-008]]：使用冻结站点正式下发。
- [[uc-026-select-template-and-create-workflow-instance|UC-026]]：消费并冻结本规则提供的站点解析结果，不能修改映射。
- [[uc-027-execute-workflow-steps|UC-027]]：通过预置步骤调用映射校验/查询，并接收完成、失败或等待修复结果。
- [[uc-028-handle-workflow-step-exception|UC-028]]：映射异常时保持阻断，不能跳过或人工覆盖本规则。
- [[uc-029-view-workflow-instance-progress|UC-029]]：只读展示映射版本、位置异常、等待原因和步骤审计。
- [[br-001-dispatch-task-range|BR-001]]、[[br-002-agv-allocation-eligibility|BR-002]]：分别依赖有效冻结站点确定任务范围和车辆覆盖资格。
- [[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]：约束模板和流程执行，但均不能覆盖本规则的映射硬约束。
