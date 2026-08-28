---
id: BR-002
type: business-rule
title: "AGV Allocation Eligibility AGV 可分配条件"
status: draft
created: 2026-07-13
updated: 2026-07-14
related_uc: ["UC-004", "UC-008", "UC-013", "UC-019", "UC-020", "UC-021", "UC-022", "UC-023", "UC-027", "UC-028", "UC-029", "UC-038", "UC-045"]
related_br: ["BR-001", "BR-003", "BR-004", "BR-005", "BR-006", "BR-008", "BR-014", "BR-015"]
aliases: ["BR-002"]
---

# BR-002 AGV Allocation Eligibility AGV 可分配条件

## Rule Statement 规则内容

一台 AGV 只有同时满足以下全部硬性条件，才允许进入本系统的任务分配候选集合：

1. 已通过 [[uc-019-register-agv-from-rcs|UC-019]] 接入，且未归档。
2. 在本系统中已启用，不处于“已禁用”或“禁用待生效”。
3. RCS/RIOT 在线，且该车当前无正在执行的移动任务。
4. 本地不存在该车未完成的搬运、充电、等待装料、等待取料、站点操作或异常恢复作业。
5. 所有仓门均明确处于关闭状态。
6. 光幕、门锁、IO 通信及其他阻止移动的安全/设备状态均正常。
7. 当前电量不低于该车配置的最低接单电量阈值。
8. 车辆配置的服务区域/站点覆盖本次任务集合。
9. 可用仓位数量、仓位规格和载重满足本次任务集合的装载要求（该车的仓位数量/位置/规格来自其接入时绑定的多仓位 AGV 模型版本快照，见 [[uc-038-maintain-agv-slot-model|UC-038]]、[[br-008-agv-slot-model-versioning|BR-008]]）。

“RCS/RIOT 任务队列为空”只说明车辆没有移动任务，不代表本地业务已经完成。AGV 停在站点等待装料或取料时，即使 RCS/RIOT 显示空闲，仍不得参与新任务分配。

## Fail-closed 规则

以下任一关键状态读取失败、过期或无法确定时，车辆必须判定为“不可分配”，不得使用默认正常值继续派车：

- RCS/RIOT 在线、位置或任务队列状态。
- 本地未完成任务/作业状态。
- 任一仓门状态。
- 光幕、门锁或移动安全联锁状态。
- 电量、服务区域或仓位能力等本轮分配所需信息。

系统应记录并展示具体不可分配原因；达到告警条件时通知相关维护人员。状态恢复并重新满足全部条件后，车辆才可再次进入候选集合。

本规则可由 [[uc-027-execute-workflow-steps|UC-027]] 在预置选车或下发前复核步骤中调用，但上述资格与 fail-closed 条件均为不可绕过的硬约束。[[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]、任何模板版本、条件跳过、重试或人工异常处置均不得把不合格或关键状态未知的车辆判为可分配。

## Candidate Ordering 候选排序

通过全部硬性条件的车辆，按以下因素综合排序：

1. **任务类型优先级（已确认）**：[[br-014-transport-task-types-and-fixed-stations|BR-014]] 定义的第 5 类 `STAGING_TO_WIRE`（派工待送区 → 指定焊线/键合机台）优先级最高。
2. **无车辆响应升级（已确认原则，阈值可配置）**：任务持续处于可分配但无车辆响应状态达 1～3 分钟区间内的配置阈值时，应提升该任务优先级；具体默认分钟数仍可边开发边定，不得写死为不可配置常量。
3. 任务等待时长与 MES 事件时间（`DATES`）。
4. **路径成本 / 预计到达成本（已确认原则，算法与权重见 [[br-015-path-cost-and-dispatch-ranking|BR-015]]）**：基于 [[uc-045-sync-map-topology-from-riot|UC-045]] 同步的 RIOT 地图路网，估算车辆当前位置到本轮任务集合首站（默认取货/作业点）的最短路径成本，作为排序因子之一；与紧急度、等待时长等时间指标一并权衡。路径近不得压过已确认的硬优先（如第 5 类）。路网不可用时按 BR-015 降级：可继续分配，但不得伪装为已按路网最短路径计费。
5. 剩余电量及执行本次任务后的电量风险。
6. 可用仓位与本次任务集合的匹配程度。
7. 车辆配置的调度权重。

除上述已确认项外，具体评分公式、因素权重、并列规则和防止单车长期饥饿的公平性机制仍为 TBD。在这些规则确认前，实现不得将临时数值固化为不可配置的正式调度策略。顺路取货与复合停靠对行程的影响见 [[br-001-dispatch-task-range|BR-001]]，不改变本规则的硬性可分配条件；「任务是否属于本次派车范围」不看路径远近（BR-001），路径成本只影响本节能排序。

## Rationale 制定原因

RCS/RIOT 负责车辆导航和运动执行，但其“空闲”通常只表示没有正在运行的移动任务。车辆可能已经到站并等待用户装料/取料，此时仓门或本地作业仍未结束。若本系统只依赖 RCS/RIOT 空闲状态继续分配，会造成任务重叠、误发车或仓门打开时移动等安全风险。

## Source 来源

2026-07-13 需求确认：

- 本系统选择具体 AGV 并分配业务任务。
- 自动分配考虑启停/在线/空闲、仓位、电量、位置、服务区域及任务优先级。
- 本地无未完成作业且所有仓门关闭是可分配的必要条件。
- 仓门、光幕、安全状态或 RCS 状态未知时禁止分配。

2026-07-14：自 MES 任务模型确认第 5 类最高优先级与 1～3 分钟无响应升级原则（见 [[br-014-transport-task-types-and-fixed-stations|BR-014]]）。

2026-07-14：确认派车排序可使用基于 RIOT 路网的最短路径成本，细则见 [[br-015-path-cost-and-dispatch-ranking|BR-015]]、路网同步见 [[uc-045-sync-map-topology-from-riot|UC-045]]。

## Related Use Cases 关联用例

- [[uc-004-slot-door-safety-interlock|UC-004]]：本规则第 5/6 条"所有仓门关闭、移动安全联锁状态正常"是派发新任务前、AGV 维度的检查点；该 UC 的 Flow A（开门前核验）、Flow B（门已开期间监控）是更细粒度、"门-移动"这一对状态本身的检查，覆盖该 AGV 已有任务、正在跟车运行的场景，与本规则检查时机不同、互不重复。
- [[uc-022-view-agv-fleet-and-availability|UC-022]]：按本规则展示可分配结论和原因。
- [[uc-023-allocate-transport-tasks-to-agv|UC-023]]：按本规则过滤和排序候选车辆。
- [[uc-008-dispatch-move-order-to-riot|UC-008]]：正式下发前再次核验关键安全条件。
- [[uc-013-enable-disable-agv|UC-013]]：维护本规则所依赖的本地启停状态。
- [[uc-019-register-agv-from-rcs|UC-019]]、[[uc-020-maintain-agv-dispatch-profile|UC-020]]、[[uc-021-archive-agv|UC-021]]：维护本规则所需的车辆档案、配置和归档状态。
- [[uc-038-maintain-agv-slot-model|UC-038]]、[[br-008-agv-slot-model-versioning|BR-008]]：定义本规则第 9 条所依赖的仓位数量、位置、规格数据来源（模型版本快照）及其不可变、不可更换规则。
- [[uc-027-execute-workflow-steps|UC-027]]：在预置选车/复核步骤中调用本规则，并将完成、失败或等待状态恢复结果回传流程引擎。
- [[uc-028-handle-workflow-step-exception|UC-028]]：处理安全状态未知、资格不满足或重试耗尽，不能跳过本规则。
- [[uc-029-view-workflow-instance-progress|UC-029]]：只读展示资格核验输入、不可分配原因和步骤审计。
- [[br-001-dispatch-task-range|BR-001]]、[[br-003-area-station-mapping|BR-003]]：分别提供待承接任务集合及其有效冻结站点。
- [[br-015-path-cost-and-dispatch-ranking|BR-015]]、[[uc-045-sync-map-topology-from-riot|UC-045]]：细化候选排序中的路径成本因子及其路网数据来源。
- [[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]：约束模板和步骤执行，但均不能覆盖本规则的车辆安全资格。
