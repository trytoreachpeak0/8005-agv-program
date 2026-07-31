---
id: UC-009
type: use-case
title: "持续监听移动任务直到AGV到站"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-09
updated: 2026-07-30
primary_actor: "本地服务器（系统内部过程，非人工角色）"
secondary_actor: RIOT
frequency: "与 UC-008 下发频率一致：每次 UC-008 完成一次下发，都会触发本 UC 开始一轮持续轮询，直到检测到该 AGV 到站或轮询异常需人工介入"
related_uc: ["UC-003", "UC-008"]
related_br: ["BR-001"]
aliases: ["UC-009"]
---

# UC-009 持续监听移动任务直到AGV到站

## 描述

[[uc-008-dispatch-move-order-to-riot|UC-008]] 完成向 RIOT 下发移动任务后，本地服务器持续轮询 RIOT 获取该 AGV 的移动任务执行状态，车载车辆概览显示“正在前往”并突出后续停靠计划中的下一站；检测到该 AGV 已到达目标站点后，将到站事件交由 [[uc-003-agv-arrives-at-designated-station|UC-003]] 处理当前站切换、作业清单刷新与界面跳转。

> 本 UC 只覆盖"移动任务下发之后，本地服务器如何持续监听、等待到站"这一段轮询/等待过程本身，不包含到站之后如何更新本地状态、触发界面跳转（后者见 [[uc-003-agv-arrives-at-designated-station|UC-003]]），也不包含如何确定/下发移动任务内容（见 [[uc-008-dispatch-move-order-to-riot|UC-008]]）。

## 触发条件

[[uc-008-dispatch-move-order-to-riot|UC-008]] 完成向 RIOT 下发该 AGV 的移动任务。

## 前置条件

**系统与接口**

1. RIOT 接口在线可用。
2. 该 AGV 存在一个刚由 [[uc-008-dispatch-move-order-to-riot|UC-008]] 下发、正在 RIOT 侧执行中的移动任务。

## 后置条件

**系统与接口**

1. 系统确认该 AGV 已到达目标站点，并将该到站事件传递给 [[uc-003-agv-arrives-at-designated-station|UC-003]]，交由其处理后续的状态更新与界面跳转。
2. 若轮询过程中发生异常（如通信中断），系统触发告警，等待人工介入；在异常解除前，不视为该 AGV 已到站。

## 假设

1. AGV 到站/停稳的判定由 AGV 本体自主完成、RIOT 可读取该状态，本 UC 不核验该判定算法本身是否准确。
2. AGV 导航路径规划的正确性由 RIOT 保证，本 UC 不核验路径本身是否最优。

## 正常流程

### 9.0

1. [[uc-008-dispatch-move-order-to-riot|UC-008]] 完成下发后，系统开始持续轮询 RIOT 获取该 AGV 移动任务的执行状态
   1.1 系统核验本次轮询/通信是否正常（见 Exception Flow E1.1）
2. 系统将车载车辆概览的运行维度显示为“正在前往”，并在 UpcomingStopPlan 中突出当前下一站；后面的未执行停靠按服务端最新计划只读展示
3. 系统持续轮询，直到读取到该 AGV 状态变为"已到达目标站点"
4. 系统将到站事件传递给 [[uc-003-agv-arrives-at-designated-station|UC-003]]，交由其处理当前站切换、CurrentStopWorklist 刷新和界面跳转

## 备选流程

不存在需要区分的备选流程：无论本次移动任务涵盖一个还是多个相邻站点（见 [[br-001-dispatch-task-range|BR-001]]），系统均按Normal Flow持续轮询、等待到站，不存在触发方式或步骤不同的分支路径。

## 异常流程

以下异常以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤一一对应：

* E1.1 轮询/通信异常导致本地服务器未能及时获知到站状态

### E1.1 轮询/通信异常导致本地服务器未能及时获知到站状态

1. 系统按第1步开始轮询 RIOT
2. 系统按第1.1步核验，发现本地服务器与 RIOT 之间通信异常或超时，未能在预期周期内获取到该 AGV 的最新移动任务状态
3. 系统触发告警提示（如界面告警、上报 IT/软件维护人员 R-12 或 AGV 运维/调度管理员 R-13），并持续尝试重新建立轮询（具体重试次数/间隔 TBD）
4. IT/软件维护人员或 AGV 运维/调度管理员排查并修复 RIOT 接口/网络异常后，轮询恢复正常，继续等待该 AGV 到站
5. 在通信恢复、确认到站之前，该 AGV 的本地状态保持"移动中"，不会被误更新为"已到站"

## 备注

* 本 UC 是从 [[uc-003-agv-arrives-at-designated-station|UC-003]] 中拆分出来的：UC-003 原先的 Trigger（"本地服务器轮询 RIOT，读取到该 AGV 的状态已变为已到达目标站点"）以及 Normal Flow 前两步、Exception Flow E2.1（轮询/通信异常）实际描述的正是"下发之后持续监听、等待到站"这一段过程，与 UC-003 关注的"到站事件确认之后如何更新状态、触发界面跳转"是两个不同阶段，因此拆分为独立的 UC-009，UC-003 相应精简，只保留到站事件确认之后的处理。
* 经与用户确认：本 UC 与 UC-003 的分界点是"到站事件是否已确认"——本 UC 负责"持续轮询直到确认到站"，UC-003 负责"确认到站之后做什么"，两者是前后衔接关系，不重叠。
* 本 UC 的 Trigger 直接衔接 [[uc-008-dispatch-move-order-to-riot|UC-008]] 的 Postcondition（该 AGV 在 RIOT 侧新增一个移动任务），构成"UC-007 生成任务 → UC-008 下发移动任务 → UC-009 持续监听 → UC-003 到站处理 → UC-001 装载"的完整链路。
* UpcomingStopPlan 只表达服务端排定的业务停靠，不包含 RIOT 的路径节点；车载端不得根据该计划自行控制导航。

## 关联用例

* [[uc-008-dispatch-move-order-to-riot|UC-008]]：本 UC 的 Trigger 依赖该 UC 完成向 RIOT 下发移动任务；本 UC 是该 UC 下发之后的直接下一步。
* [[uc-003-agv-arrives-at-designated-station|UC-003]]：本 UC 确认到站后，将到站事件传递给该 UC 处理后续的状态更新与界面跳转；本 UC 是从该 UC 中拆分出来的前置监听阶段。

## 其他信息

