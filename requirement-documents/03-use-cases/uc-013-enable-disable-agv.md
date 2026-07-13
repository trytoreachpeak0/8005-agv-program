---
id: UC-013
type: use-case
title: "Enable/Disable AGV 启用/禁用 AGV"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-09
updated: 2026-07-09
primary_actor: "AGV Operations / Dispatch Administrator AGV 运维/调度管理员（R-13，暂定，见 Notes），见 [[stakeholders-and-user-classes|干系人与用户角色清单]]"
secondary_actor: "None 无（本 UC 只操作本地数据库中的 AGV 调度开关状态，不调用 RIOT 接口做设备级禁用/暂停，见 Assumption）"
frequency: "TBD 待定，预期为低频的人工维护类操作（如设备保养、临时停用故障车辆），与 UC-012 同量级或更低"
related_uc: ["UC-008", "UC-012"]
related_br: []
aliases: ["UC-013"]
---

# UC-013 Enable/Disable AGV 启用/禁用 AGV

## Description 描述

AGV 运维/调度管理员在系统内选中某台多仓位 AGV，点击"禁用"或"启用"按钮，控制该 AGV 是否可以被系统继续派发新任务。禁用操作不会打断该 AGV 当前正在执行的移动任务（无论是 [[uc-008-dispatch-move-order-to-riot|UC-008]] 派发的搬运任务，还是 [[uc-012-manually-dispatch-agv-to-charge|UC-012]] 派发的充电任务）：若点击"禁用"时该 AGV 当前 RIOT 任务队列为空，立即变为"已禁用"；若队列不为空（有任务正在执行），先变为"禁用待生效"，待当前任务执行完成/取消后，系统自动将其转为"已禁用"。一旦处于"已禁用"（或"禁用待生效"）状态，该 AGV 便不会再被 UC-008 派发新的搬运任务，也不会被 UC-012 派发新的充电任务。"启用"则是相反操作，将该 AGV 恢复为正常可派车/可充电状态。

> 本 UC 与 [[uc-008-dispatch-move-order-to-riot|UC-008]]、[[uc-012-manually-dispatch-agv-to-charge|UC-012]] 的分工边界：本 UC 只负责维护"该 AGV 当前是否允许被派发新任务"这一开关状态本身，不负责具体派发搬运任务或充电任务的逻辑——那两者仍分别由 UC-008、UC-012 各自的 Precondition 去核验本 UC 维护的开关状态。

## Trigger 触发条件

AGV 运维/调度管理员在 AGV 列表中选中目标 AGV，点击"禁用"或"启用"按钮。 The AGV operations/dispatch administrator selects a target AGV in the AGV list and clicks "Disable" or "Enable".

## Precondition 前置条件

**System & Interface 系统与接口**

1. 本地服务器可读取该 AGV 当前 RIOT 任务队列是否为空（具体是读取本地缓存记录，还是即时查询 RIOT 接口，TBD 待补充）。The local server can read whether the AGV's current RIOT task queue is empty (whether via a local cached record or a live RIOT query is TBD).

**Personnel & Authorization 人员与权限**

2. AGV 运维/调度管理员具备禁用/启用 AGV 的操作权限。The AGV operations/dispatch administrator has permission to disable/enable an AGV.

## Postcondition 后置条件

**Task & Data 任务与数据**

1. 点击"禁用"且该 AGV 当前 RIOT 任务队列为空：该 AGV 状态立即变为"已禁用（Disabled）"。When "Disable" is clicked and the AGV's RIOT task queue is currently empty, the AGV's status immediately becomes "Disabled".
2. 点击"禁用"且该 AGV 当前 RIOT 任务队列不为空：该 AGV 状态先变为"禁用待生效（Disable Pending）"，当前正在执行的任务不受影响、继续执行至完成或取消；完成/取消后，系统自动将该 AGV 状态转为"已禁用"。When "Disable" is clicked while the AGV's RIOT task queue is not empty, the AGV's status first becomes "Disable Pending"; the currently executing task is unaffected and continues to completion or cancellation, after which the system automatically transitions the AGV to "Disabled".
3. 点击"启用"：该 AGV 状态从"已禁用"或"禁用待生效"恢复为其原本应有的正常状态，清除禁用相关标记，重新可被 [[uc-008-dispatch-move-order-to-riot|UC-008]] 派发搬运任务、可被 [[uc-012-manually-dispatch-agv-to-charge|UC-012]] 派发充电任务。When "Enable" is clicked, the AGV's status is restored from "Disabled" or "Disable Pending" back to its normal state, clearing the disable-related flag, and the AGV again becomes eligible for dispatch via UC-008 and for manual charging via UC-012.
4. 本次操作（操作人、AGV、操作类型：禁用/启用、时间戳）被记录到本地数据库，用于追溯。This operation (operator, AGV, operation type: disable/enable, timestamp) is logged in the local database for traceability.

## Assumption 假设

1. 本 UC 的"禁用"是纯本地系统层面的调度开关，只影响本地服务器是否会继续为该 AGV 调用 RIOT 接口下发新任务，不涉及调用 RIOT 接口对该 AGV 做设备级的禁用/暂停/断电；若后续业务上需要联动 RIOT 侧做设备级禁用，TBD 待补充，不在本 UC 范围内。This UC's "disable" is a purely local scheduling switch that only affects whether the local server continues dispatching new RIOT move orders to the AGV; it does not call any RIOT interface to disable/pause/power off the AGV at the device level. If device-level disabling via RIOT is needed later, this is TBD and out of scope for this UC.
2. "已禁用"/"禁用待生效"状态不影响该 AGV 已有的历史搬运任务记录或仓位占用情况（如仓位中仍有在运产品）；本 UC 只影响"该 AGV 是否可被派发新任务"，不影响已有数据。The "Disabled"/"Disable Pending" status does not affect the AGV's existing transport task records or slot occupancy (e.g. in-transit products still in its slots); this UC only affects whether the AGV is eligible for new task dispatch, not existing data.

## Normal Flow 正常流程

### 13.0 Enable/Disable AGV

1. AGV 运维/调度管理员在 AGV 列表中选中目标 AGV
2. AGV 运维/调度管理员点击"禁用"或"启用"按钮
3. 若点击"禁用"：
   3.1 系统核验该 AGV 当前是否已处于"已禁用"或"禁用待生效"状态（见 Exception Flow E3.1）
   3.2 系统核验该 AGV 当前 RIOT 任务队列是否为空：为空则立即将该 AGV 状态置为"已禁用"；不为空则置为"禁用待生效"，待该任务执行完成/取消、队列重新变空后，系统自动将其转为"已禁用"
4. 若点击"启用"：
   4.1 系统核验该 AGV 当前是否确实处于"已禁用"或"禁用待生效"状态（见 Exception Flow E4.1）
   4.2 系统将该 AGV 状态恢复为其原本应有的正常状态，清除禁用相关标记
5. 系统记录本次操作（操作人、AGV、操作类型：禁用/启用、时间戳）

## Alternative Flow 备选流程

不存在需要区分的备选流程："禁用"与"启用"两个方向已在 Normal Flow 第 3、4 步以分支方式表达（写法参照 [[uc-004-slot-door-safety-interlock|UC-004]] 用分支步骤表达"暂停待恢复"与"直接取消"两条路径的方式），不构成独立的触发方式或流程分支。 No alternative flow is needed: the "disable" and "enable" directions are already expressed as branches within steps 3 and 4 of the Normal Flow, following the same branching style used in UC-004 for its "pause-then-resume" vs. "cancel" paths.

## Exception Flow 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤一一对应：

* E3.1 该 AGV 已处于"已禁用"/"禁用待生效"状态，重复点击"禁用"
* E4.1 该 AGV 当前并非"已禁用"/"禁用待生效"状态，点击"启用"

### E3.1 该 AGV 已处于"已禁用"/"禁用待生效"状态，重复点击"禁用"

1. AGV 运维/调度管理员对某台已处于"已禁用"或"禁用待生效"状态的 AGV 再次点击"禁用"按钮
2. 系统按第 3.1 步核验，发现该 AGV 当前已处于"已禁用"或"禁用待生效"状态
3. 系统提示"该 AGV 当前已处于禁用（或禁用待生效）状态"，忽略本次重复操作，不重复记录
4. AGV 运维/调度管理员核对该 AGV 当前状态，确认是否还需要其他操作

### E4.1 该 AGV 当前并非"已禁用"/"禁用待生效"状态，点击"启用"

1. AGV 运维/调度管理员对某台当前处于正常（非禁用）状态的 AGV 点击"启用"按钮
2. 系统按第 4.1 步核验，发现该 AGV 当前并非"已禁用"或"禁用待生效"状态
3. 系统提示"该 AGV 当前无需启用"，忽略本次操作，不重复记录
4. AGV 运维/调度管理员核对该 AGV 当前状态，确认是否操作了正确的目标 AGV

## Notes 备注

* 本 UC 是用户提出的新场景："用户可以禁用和启用车子，这个禁用和启用是用户在本系统里面禁用和启用的，禁用和启用之后，车子无法执行任务，包括充电任务"。经与用户确认后独立成 UC，并要求 [[uc-008-dispatch-move-order-to-riot|UC-008]]、[[uc-012-manually-dispatch-agv-to-charge|UC-012]] 的 Precondition 中补充核验本 UC 维护的禁用状态。
* 经与用户确认：禁用操作不会打断该 AGV 当前正在执行的任务（无论是搬运任务还是充电任务），只阻止之后的新派发；若该 AGV 当前有任务正在执行，禁用先进入"禁用待生效"这一过渡状态，等当前任务执行完成/取消后，系统自动将其转为"已禁用"，不需要人工二次确认。
* Actor 暂定为 AGV 运维/调度管理员（R-13），与 [[uc-012-manually-dispatch-agv-to-charge|UC-012]] 保持一致；用户对此暂未最终确认，后续可能需要进一步讨论是否也允许班组长/生产管理者（R-09/R-10）操作，TBD。
* 待补充（TBD）事项：
  1. Actor 范围是否需要扩展到 R-09/R-10，待后续与用户确认。
  2. "禁用"是否需要联动调用 RIOT 接口做设备级禁用/暂停，本次先按纯本地调度开关处理（见 Assumption 第 1 条）。
  3. 本地服务器判断"该 AGV 当前 RIOT 任务队列是否为空"具体走本地缓存记录还是即时查询 RIOT 接口。
  4. 是否需要在 [[uc-011-view-slot-monitoring-dashboard|UC-011]] 监控看板中展示 AGV 的"已禁用"/"禁用待生效"状态，本 UC 暂不展开，留待后续协调确认。

## Related Use Cases 关联用例

* [[uc-008-dispatch-move-order-to-riot|UC-008]]：本 UC 维护的"已禁用"/"禁用待生效"状态，是该 UC Precondition 中新增的核验项之一——处于该状态的 AGV 不会被该 UC 自动派发新的搬运任务。
* [[uc-012-manually-dispatch-agv-to-charge|UC-012]]：本 UC 维护的"已禁用"/"禁用待生效"状态，同样是该 UC Precondition 中新增的核验项之一——处于该状态的 AGV 无法被该 UC 手动派发充电任务。

## Other Information 其他信息

