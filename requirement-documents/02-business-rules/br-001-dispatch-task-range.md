---
id: BR-001
type: business-rule
title: "Dispatch Task Range Definition 派车任务范围定义"
status: draft
created: 2026-07-09
updated: 2026-07-13
related_uc: ["UC-001", "UC-003", "UC-007", "UC-008", "UC-023", "UC-024", "UC-027", "UC-028", "UC-029"]
related_br: ["BR-002", "BR-003", "BR-004", "BR-005", "BR-006"]
aliases: ["BR-001"]
---

# BR-001 Dispatch Task Range Definition 派车任务范围定义

## Rule Statement 规则内容

多仓位 AGV 每次由 RIOT/调度系统下发移动任务（即"一次派车"）时，会关联一个"本次派车任务范围"：该范围可能同时涵盖多个相邻站点各自的搬运任务（例如同一次派车里同时包含 A、B 两个相邻站点的任务），而不要求"任务范围"与"AGV 当前停靠的物理站点"严格一一对应。

判定某个搬运任务（子批号）是否"属于本次派车范围"的标准是：该任务是否已被分配进本次派车下发时关联的任务集合中，而不是该任务的目标站点与 AGV 当前物理位置之间的距离远近。距离较近但未被分配进本次派车范围的任务（不属于该集合），即使系统中确实存在该任务记录，也判定为不属于本次派车范围。

只有已按 [[br-003-area-station-mapping|BR-003]] 成功解析并冻结起终点的任务才能进入派车范围。AREA 为空、映射缺失/停用/异常或站点未冻结的任务必须保持位置异常，不得通过与其他正常任务合并而绕过校验。

本次派车任务范围由本系统生成，并交给 [[uc-023-allocate-transport-tasks-to-agv|UC-023]] 选择具体 AGV。范围生成时机、是否允许在 AGV 移动过程中调整、具体数据结构及相邻站点组合算法仍为 TBD。

本规则只决定“本次包含哪些任务”；[[br-002-agv-allocation-eligibility|BR-002]] 和 UC-023 决定“这些任务分给哪台 AGV”；[[uc-008-dispatch-move-order-to-riot|UC-008]] 负责向 RCS/RIOT 正式下发。

本规则可由 [[uc-027-execute-workflow-steps|UC-027]] 在预置任务范围/分配步骤中调用，但仍是不可绕过的硬约束。[[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]、任何模板版本、条件跳过、重试或人工异常处置均不得把范围外任务纳入本次派车，也不得允许站点未按 BR-003 解析并冻结的任务进入范围。

## Rationale 制定原因

由于相邻站点物理距离很近，一次派车可能同时涵盖多个相邻站点各自的搬运需求。允许操作员在车辆停靠 A 点时，提前装载本次派车任务范围内、属于相邻 B 点的产品，不需要等车辆真正到达 B 点，可以提升装载效率、减少 AGV 空跑/等待时间。

## Source 来源

TBD 待补充（如：客户现场访谈、AGV/RIOT 调度系统技术方案等）

## Related Use Cases 关联用例

* [[uc-001-load-completed-lot-into-slot|UC-001]]：Normal Flow 第 1.2 步、Exception Flow E1.2 依据本规则核验"子批号对应的任务是否属于本次派车范围"。
* [[uc-003-agv-arrives-at-designated-station|UC-003]]：本规则在本系统分配和下发前生成；UC-003 只处理到站后的感知和呈现。
* [[uc-007-sync-transport-task-from-mes|UC-007]]：本规则划分"派车任务范围"所依据的任务集合，来源于该 UC 从 MES 同步生成的本地任务记录；UC-007 关注任务的"生成"阶段，本规则关注生成之后、派车下发时的"分配"阶段，两者是上下游关系，不重叠。
* [[uc-023-allocate-transport-tasks-to-agv|UC-023]]：消费本规则生成的任务集合，并依据 BR-002 选择和绑定具体 AGV。
* [[uc-008-dispatch-move-order-to-riot|UC-008]]：消费已确定的任务集合和车辆绑定，只负责调用 RCS/RIOT 接口下发并更新本地任务状态。
* [[br-002-agv-allocation-eligibility|BR-002]]：定义可承接本规则任务集合的候选车辆条件和排序因素。
* [[br-003-area-station-mapping|BR-003]]、[[uc-024-maintain-area-station-mapping|UC-024]]：保证进入本规则的任务已具有有效、冻结的地图站点。
* [[uc-027-execute-workflow-steps|UC-027]]：在预置分配步骤中调用本规则，并将完成、失败或等待结果回传流程引擎。
* [[uc-028-handle-workflow-step-exception|UC-028]]：处理范围计算失败或输入不完整，不能通过跳过/人工处置覆盖本规则。
* [[uc-029-view-workflow-instance-progress|UC-029]]：只读展示任务范围步骤、输入、结果和审计。
* [[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]：约束模板匹配、快照和步骤执行，但均不能覆盖本规则的范围及站点硬约束。
