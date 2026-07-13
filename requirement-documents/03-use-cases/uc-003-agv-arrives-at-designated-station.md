---
id: UC-003
type: use-case
title: "AGV Arrives at Designated Station AGV 到达指定站点"
status: draft
priority: high
created_by: "邵正宇"
updated_by: "邵正宇"
created: 2026-07-09
updated: 2026-07-09
primary_actor: "多仓位 AGV 系统"
secondary_actor: "None 无（本 UC 不直接与 RIOT 交互，依赖 [[uc-009-monitor-move-order-until-arrival|UC-009]] 确认到站事件后触发）"
frequency: "TBD 待定"
related_uc: ["UC-001", "UC-006", "UC-008", "UC-009", "UC-010"]
related_br: ["BR-001"]
aliases: ["UC-003"]
---

# UC-003 AGV Arrives at Designated Station AGV 到达指定站点

## Description 描述

[[uc-009-monitor-move-order-until-arrival|UC-009]] 持续轮询 RIOT 确认该多仓位 AGV 已到达目标站点后，将到站事件传递给本 UC：本地系统将记录的 AGV 状态更新为"已到站"，并触发操作面板界面自动跳转到对应站点的装卸操作界面。本 UC 只覆盖"到站事件确认之后，本地系统如何更新状态、呈现界面"这一过程本身，不包含 RIOT 下发移动任务（见 [[uc-008-dispatch-move-order-to-riot|UC-008]]）、下发之后持续轮询等待到站（见 [[uc-009-monitor-move-order-until-arrival|UC-009]]）、AGV 导航移动的过程——这些均不在本 UC 范围内（见 Assumption）。[[uc-001-load-completed-lot-into-slot|UC-001]]（放入完工产品）等业务 UC 的 Trigger 依赖本 UC 完成后触发。

> 本 UC 不涉及人工 Actor 驱动的操作步骤：操作员在本 UC 中唯一能感知到的，是到站后界面自动跳转这一结果（见 Postcondition），并不需要在本 UC 过程中做出任何操作或决策。
>
> "一次派车具体包含哪些站点/任务"的分配与生成规则（即"本次派车任务范围"）不在本 UC 范围内定义，见 [[br-001-dispatch-task-range|BR-001]]；本 UC 只描述到站事件确认后，本地系统如何感知并呈现该状态。

## Trigger 触发条件

[[uc-009-monitor-move-order-until-arrival|UC-009]] 确认该 AGV 已到达目标站点，并将到站事件传递给本 UC。

## Precondition 前置条件

**Task & Data 任务与数据**

1. [[uc-009-monitor-move-order-until-arrival|UC-009]] 已完成到站确认，本 UC 收到其传递的到站事件。UC-009 has confirmed the arrival and handed off the arrival event to this UC.

> 经与用户确认：AGV 电量是否充足、目标站点是否可用、仓门开启期间的移动安全联锁等，均不作为本 UC 的 Precondition——这些属于派车下发、AGV 导航移动阶段需要关注的问题，而本 UC 的起点已经是"到站事件已被确认"这一事实，不涉及派车/导航/轮询过程本身。

## Postcondition 后置条件

1. AGV 到达目标站点并停稳。
2. 本地系统将该 AGV 状态由"移动中"更新为"已到站"。
3. 操作面板界面自动跳转到该站点对应的装卸操作界面（这是本 UC 对操作员唯一直接可见的输出，对应 [[uc-001-load-completed-lot-into-slot|UC-001]] 的 Trigger 来源）。

## Assumption 假设

1. AGV 到站/停稳的判定由 AGV 本体自主完成、RIOT 可读取该状态，本 UC 不核验该判定算法本身是否准确。

## Normal Flow 正常流程

### 3.0 AGV Arrives at Designated Station

1. 系统接收到 [[uc-009-monitor-move-order-until-arrival|UC-009]] 传递的到站事件确认
2. 本地系统将该 AGV 状态由"移动中"更新为"已到站"
3. 系统触发操作面板界面自动跳转到该站点对应的装卸操作界面

## Alternative Flow 备选流程

TBD 待补充（如：是否存在无需操作员介入的"过站不停"场景等）

## Exception Flow 异常流程

本 UC 起点已经是"到站事件已被 UC-009 确认"这一事实，轮询/通信相关的异常已移至 [[uc-009-monitor-move-order-until-arrival|UC-009]] 处理（见该 UC 的 Exception Flow E1.1）；本 UC 本身目前暂无需要单独定义的异常流程，TBD 待补充（如状态更新失败、界面跳转失败等本地异常场景）。

## Notes 备注

* 本 UC 从 UC-001「放入完工产品」拆分而来：UC-001 只覆盖"AGV 已到站后，操作员装料"的部分，AGV 如何到达站点属于本 UC 的范围。
* 经与用户确认：本 UC 的 Actor 是系统（多仓位 AGV 系统），不是人工角色；操作员在本 UC 中只是"界面跳转"这一结果的接收方，不驱动流程。
* 经与用户确认：原本计划放入本 UC 的"本次派车任务范围如何生成"这部分内容，因其本质是调度策略规则（供多个 UC 复用判定，而非本 UC 独有的一段流程），已拆分为独立的业务规则 [[br-001-dispatch-task-range|BR-001]]，不再作为本 UC 的 TBD 事项。
* 经与用户进一步确认：本 UC 的起点已经是"AGV 已到站"这一事实，不包含 RIOT 下发移动任务、AGV 导航移动的过程——RIOT 接收任务后会根据任务内容逐一下发移动指令，AGV 到站/停稳由其自身判断、RIOT 可读取该状态，本地服务器再通过轮询 RIOT 获知；这一整条链路里，只有"本地服务器轮询获知到站状态 → 更新本地记录 → 触发界面跳转"这一段属于本 UC，之前版本中的"下发任务""导航移动""堵路避障""定位精度判定"等步骤均已移出本 UC（相应地，原 Precondition 中的电量/站点可用/移动安全联锁核验，以及原 Exception Flow 中的任务下发失败/堵路避障超时/定位精度不足，也一并移除）。
* 经与用户进一步确认：本 UC 原先直接包含的"本地服务器轮询 RIOT，读取到该 AGV 状态已变为已到达指定站点"这一段轮询/等待过程，连同其对应的 Precondition（RIOT 与本地服务器通讯正常）、Exception Flow（E2.1 轮询/通信异常）、Assumption（AGV 导航路径规划的正确性由 RIOT 保证），已拆分为独立的 [[uc-009-monitor-move-order-until-arrival|UC-009]]；本 UC 精简为只保留"到站事件已被确认之后，本地系统如何更新状态、触发界面跳转"这一段，Trigger 相应改为"UC-009 确认到站并传递事件"。

## Related Use Cases 关联用例

* [[uc-001-load-completed-lot-into-slot|UC-001]]：本 UC 的 Postcondition（到站、界面跳转）是 UC-001 的 Trigger 来源。
* [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：本 UC 的 Postcondition（到站、界面跳转）同样是 UC-006 的 Trigger 来源——操作员到站后可先在待处理任务列表中取消不再需要的任务，再执行 UC-001 装载其余任务。
* [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：本 UC 的 Postcondition（到站、界面跳转）同样是 UC-010 的 Trigger 来源之一——AGV 到站后，系统据此自动识别并打开该站点待取料的仓位，供终点站操作员取出存料；与 [[uc-001-load-completed-lot-into-slot|UC-001]] 不同，UC-010 不依赖界面跳转本身发起操作（系统自动开仓），但仍需以本 UC 的到站确认为前提。
* [[uc-009-monitor-move-order-until-arrival|UC-009]]：本 UC 的 Trigger 直接依赖该 UC 完成到站确认并传递到站事件；本 UC 是从该 UC 中拆分出来的下游处理阶段，两者是直接的前后衔接关系。
* [[uc-008-dispatch-move-order-to-riot|UC-008]]：本 UC 与该 UC 是间接关系——UC-008 向 RIOT 下发移动任务后，需经 [[uc-009-monitor-move-order-until-arrival|UC-009]] 持续轮询确认到站，才会触发本 UC，本 UC 不直接依赖 UC-008。

## Other Information 其他信息

