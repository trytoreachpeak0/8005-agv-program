---
id: UC-012
type: use-case
title: "Manually Dispatch Idle AGV to Charge 空闲状态下手动派车充电"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-09
updated: 2026-07-09
primary_actor: "AGV Operations / Dispatch Administrator AGV 运维/调度管理员（R-13），见 [[stakeholders-and-user-classes|干系人与用户角色清单]]"
secondary_actor: RIOT
frequency: "TBD 待定，预期为低频的人工维护类操作，与 R-13 的日常调度巡检节奏相关，远低于 UC-001 等业务操作类 UC 的发生频率"
related_uc: ["UC-008", "UC-009", "UC-013"]
related_br: []
aliases: ["UC-012"]
---

# UC-012 Manually Dispatch Idle AGV to Charge 空闲状态下手动派车充电

## Description 描述

AGV 运维/调度管理员（R-13）在界面上查看到某台多仓位 AGV 当前处于"空闲"状态（即该 AGV 在 RIOT 侧没有正在执行的移动任务），可以主动选中该 AGV 并点击"手动充电"按钮。系统在核验该 AGV 确实空闲后，调用 RIOT 接口为其创建一个"充电"类型的移动任务，AGV 随即前往充电桩开始充电。充电达到预设电量阈值后，系统自动结束本次充电，该 AGV 的 RIOT 任务队列重新变为空，自然满足 [[uc-008-dispatch-move-order-to-riot|UC-008]] 的下发条件，可被重新纳入正常派车候选，不需要 R-13 额外手动"停止充电"。

> 本 UC 与 [[uc-008-dispatch-move-order-to-riot|UC-008]] 是对"该 AGV 当前 RIOT 任务队列变为空"这一同一触发窗口的两个竞争消费者：AGV 一旦空闲，UC-008 会尝试自动派发本地待处理的搬运任务，本 UC 则由 R-13 主动争取该窗口去派发充电任务；两者不做互相抢占的设计，谁先执行谁获胜（详见 Exception Flow E2.1、Related Use Cases）。

## Trigger 触发条件

AGV 运维/调度管理员在界面上选中一台当前空闲（RIOT 任务队列为空）的多仓位 AGV，点击"手动充电"按钮。 The AGV operations/dispatch administrator selects a currently idle multi-slot AGV (empty RIOT task queue) in the UI and clicks "Charge Manually".

## Precondition 前置条件

**System & Interface 系统与接口**

1. RIOT 接口在线可用。RIOT interface is online and reachable.
2. RIOT 提供可下发"充电"类型移动任务的接口，支持指定或自动选择可用充电桩（TBD 待与 RIOT 技术对接确认，具体接口能力尚未最终验证）。RIOT provides an interface to dispatch a "charge" type move order, supporting either a specified or an automatically selected available charging station (TBD, pending confirmation with the RIOT integration side).

**Task & Data 任务与数据**

3. 该 AGV 当前在 RIOT 任务队列中的任务数量确实为 0（无正在执行的移动任务）。The AGV's RIOT task queue is confirmed to be empty (0 tasks), i.e. no move order currently executing.
4. 该 AGV 当前未处于"已禁用"或"禁用待生效"状态（见 [[uc-013-enable-disable-agv|UC-013]]）。The AGV is not currently in "Disabled" or "Disable Pending" status (see [[uc-013-enable-disable-agv|UC-013]]).

**Personnel & Authorization 人员与权限**

5. AGV 运维/调度管理员具备手动发起充电的操作权限。The AGV operations/dispatch administrator has permission to manually dispatch a charging move order.

> 本 UC 不要求该 AGV 全部仓位均为"空闲"——即使仓位中仍存有在运产品（尚未取出/尚未确认完成），只要该 AGV 当前没有正在执行的移动任务，也允许发起充电，因为仓位占用状态与"是否需要充电"是两个独立维度，不做强制关联。

## Postcondition 后置条件

**System & Interface 系统与接口**

1. 该 AGV 在 RIOT 侧新增一个"充电"类型移动任务，其 RIOT 任务队列数量由 0 变为 1；AGV 随即按 RIOT 规划路径移动至充电桩并开始充电。A new "charge" move order is created for the AGV on the RIOT side; its RIOT task queue count changes from 0 to 1, and the AGV navigates to the charging station and begins charging.

**Task & Data 任务与数据**

2. 本次手动充电下发记录（操作人、AGV、充电桩、时间戳）被记录到本地数据库，用于追溯。This manual charge dispatch (operator, AGV, charging station, timestamp) is logged in the local database for traceability.
3. 充电达到预设电量阈值后（具体阈值 TBD），系统自动结束该充电任务，该 AGV 的 RIOT 任务队列重新变为 0，自然满足 [[uc-008-dispatch-move-order-to-riot|UC-008]] 的 Trigger 条件，可被重新纳入正常派车候选，不需要人工点击"停止充电"。Once the AGV's battery reaches a preset threshold (TBD), the system automatically ends the charging move order; the AGV's RIOT task queue returns to 0, naturally satisfying the Trigger condition of [[uc-008-dispatch-move-order-to-riot|UC-008]] so the AGV becomes eligible for normal dispatch again, without the operator needing to click "stop charging".

## Assumption 假设

1. 电量阈值、"何时判定为已充满可重新派车"的具体数值尚未确定，TBD 待补充。The specific battery threshold used to determine "sufficiently charged, eligible for redispatch" has not yet been finalized (TBD).
2. 充电桩的具体选择（如存在多个充电桩时如何分配）由 RIOT 自主规划，本 UC 不关心具体选桩算法本身。The specific selection of which charging station to use (e.g. when multiple stations are available) is planned autonomously by RIOT; this UC does not concern itself with the station-selection algorithm itself.
3. 本 UC 与 `vision-and-scope.md` 中提到的"低电量自动回充"是两个不同场景：本 UC 是 R-13 在 AGV 空闲时主动手动触发；"低电量自动回充"是系统检测到电量不足时自动触发，触发方式不同。后者不在本 UC 范围内，留待后续需要时单独建 UC 覆盖。This UC is distinct from the "automatic low-battery return-to-charge" scenario mentioned in `vision-and-scope.md`: this UC is manually triggered by R-13 while the AGV is idle, whereas the automatic scenario is system-triggered upon detecting low battery. The latter is out of scope for this UC and would require a separate UC if needed later.
4. R-13 在点击"手动充电"之前，会自行判断该 AGV 当前确实适合被派去充电（如电量确实有必要补充、或作为例行维护安排），系统不核验发起充电请求本身的合理性/必要性。Before clicking "Charge Manually", R-13 is assumed to have already judged that dispatching this AGV to charge is appropriate (e.g. genuinely needs a battery top-up, or as routine maintenance scheduling); the system does not verify the necessity/reasonableness of the request itself.

## Normal Flow 正常流程

### 12.0 Manually Dispatch Idle AGV to Charge

1. AGV 运维/调度管理员查看 AGV 列表，确认某台多仓位 AGV 当前状态为"空闲"（RIOT 任务队列为空）
2. AGV 运维/调度管理员选中该 AGV，点击"手动充电"按钮
   2.1 系统核验该 AGV 当前 RIOT 任务队列是否确实为空（见 Exception Flow E2.1）
   2.2 系统核验 RIOT 接口是否在线可用（见 Exception Flow E2.2）
   2.3 系统核验该 AGV 当前是否处于"已禁用"或"禁用待生效"状态（见 Exception Flow E2.3）
3. 系统调用 RIOT 接口，为该 AGV 创建一个"充电"类型的移动任务
   3.1 系统核验 RIOT 是否正常接收本次下发请求（见 Exception Flow E3.1）
4. 系统记录本次手动充电下发日志（操作人、AGV、充电桩、时间戳）
5. AGV 按 RIOT 规划路径移动至充电桩并开始充电（导航与充电过程本身由 RIOT 自主管理，不在本 UC 范围内展开）
6. 系统监测该 AGV 电量，达到预设阈值后，充电任务在 RIOT 侧执行完成，该 AGV 的 RIOT 任务队列重新变为 0

## Alternative Flow 备选流程

不存在需要区分的备选流程：无论该 AGV 当前仓位是否仍有在运产品，本 UC 均按 Normal Flow 相同的核验、下发、记录步骤处理，不存在触发方式或步骤不同的分支路径。 No alternative flow is needed: regardless of whether the AGV's slots currently hold in-transit products, this UC follows the same verify/dispatch/log steps described in the Normal Flow; there is no distinct trigger or branching path.

## Exception Flow 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤（或子步骤）一一对应：

* E2.1 请求时该 AGV 已不再空闲（已被 UC-008 抢先派发新任务）
* E2.2 RIOT 接口通信异常
* E2.3 该 AGV 当前已被禁用，无法发起充电
* E3.1 充电指令下发失败/超时

### E2.1 请求时该 AGV 已不再空闲

1. AGV 运维/调度管理员选中某台此前空闲的 AGV，点击"手动充电"按钮
2. 系统按第 2.1 步核验该 AGV 当前 RIOT 任务队列，发现其数量已不为 0（例如 [[uc-008-dispatch-move-order-to-riot|UC-008]] 已抢先为其派发了新的搬运任务）
3. 系统提示"该 AGV 当前已不空闲，无法发起充电"，拒绝本次充电请求
4. AGV 运维/调度管理员可等待该 AGV 再次空闲后重新发起充电请求，不做抢占或排队等待处理

### E2.2 RIOT 接口通信异常

1. 系统按第 2.2 步核验 RIOT 接口是否在线可用
2. 系统发现本地服务器与 RIOT 之间通信异常或超时
3. 系统提示"RIOT 接口异常，无法发起充电"，拒绝本次充电请求，并提示上报 IT/软件维护人员（R-12）或 AGV 运维/调度管理员（R-13）自行排查
4. IT/软件维护人员排查并修复 RIOT 接口/网络异常后，AGV 运维/调度管理员可重新发起充电请求

### E2.3 该 AGV 当前已被禁用，无法发起充电

1. AGV 运维/调度管理员选中某台 AGV，点击"手动充电"按钮
2. 系统按第 2.3 步核验，发现该 AGV 当前处于"已禁用"或"禁用待生效"状态（见 [[uc-013-enable-disable-agv|UC-013]]）
3. 系统提示"该 AGV 当前已被禁用，无法发起充电"，拒绝本次充电请求
4. AGV 运维/调度管理员若确认该 AGV 确实需要充电，需先通过 [[uc-013-enable-disable-agv|UC-013]] 将其启用后，再重新发起充电请求

### E3.1 充电指令下发失败/超时

1. 系统按第 3 步向 RIOT 发起创建"充电"移动任务的请求
2. 系统按第 3.1 步核验，发现本次请求通信异常、超时，或 RIOT 返回下发失败
3. 系统自动重试（具体重试次数/间隔 TBD）
4. 若重试仍失败且达到预设阈值（次数/时长，具体数值 TBD），系统触发告警提示（如界面告警、上报 IT/软件维护人员 R-12 或 AGV 运维/调度管理员 R-13），本次充电下发暂停，该 AGV 保持原空闲状态，可被后续重新尝试或被 [[uc-008-dispatch-move-order-to-riot|UC-008]] 正常派车
5. IT/软件维护人员或 AGV 运维/调度管理员排查并修复 RIOT 接口/网络异常后，可重新尝试发起充电请求

> TBD 待补充：充电过程中途发生异常（如长时间电量不上升、充电桩故障、AGV 充电中失联）应如何处理，暂不在本 UC 中深入展开。

## Notes 备注

* 本 UC 是用户提出的新场景："车子在空闲状态下，用户能主动让车子去充电"，经与用户确认后拆分为独立 UC，而不是并入 [[uc-008-dispatch-move-order-to-riot|UC-008]]：两者虽然都表现为"AGV 空闲后调用 RIOT 接口下发一个移动任务"，但触发来源不同——UC-008 由系统自动从本地待处理任务中选取下发，本 UC 由 R-13 人工主动发起，且下发的任务类型（充电 vs 搬运）不同，因此独立成文，但在 Related Use Cases 中明确两者对"AGV 空闲"这一同一触发窗口的竞争关系。
* 经与用户确认："空闲"的判定只要求该 AGV 当前 RIOT 任务队列为空（无正在执行的移动任务），不要求其仓位也全部空闲；即使仓位中仍有在运产品，也允许发起充电。
* 经与用户确认：本 UC 与 UC-008 之间**不做抢占设计**——若 R-13 发起充电请求时，该 AGV 已经被 UC-008 抢先派发了新的搬运任务（即两者竞争同一个"空闲触发窗口"、UC-008 先完成），本次充电请求直接被拒绝（见 Exception Flow E2.1），提示 R-13 等待该 AGV 再次空闲后重试，不引入额外的排队/抢占机制。
* 经与用户确认：充电结束的处理方式为"自动阈值"——AGV 电量达到预设阈值后，系统自动结束充电，AGV 自动重新变为可派车状态，不需要 R-13 额外手动点击"停止充电"。
* 本 UC 与 `vision-and-scope.md` 主要特性清单中提到的"低电量回充"是两个不同场景（见 Assumption 第 3 条）：本 UC 覆盖的是人工在 AGV 空闲时主动触发的充电，"低电量自动回充"这一系统自动触发的场景暂不在本 UC 范围内，留待后续需要时单独建 UC 补充。
* 待补充（TBD）事项：
  1. RIOT 是否真的提供"下发充电类型移动任务"的接口（区别于普通站点移动任务），需要后续与 RIOT 技术对接确认。
  2. 电量阈值、"何时视为已充满可重新派车"的具体数值。
  3. 充电过程中途异常（电量不上升、充电桩故障、AGV 失联等）的具体处理机制。
  4. 是否需要在 [[uc-011-view-slot-monitoring-dashboard|UC-011]] 监控看板中展示 AGV 的"充电中"状态，本 UC 暂不扩展 UC-011 的范围，留待后续协调确认。

## Related Use Cases 关联用例

* [[uc-008-dispatch-move-order-to-riot|UC-008]]：本 UC 与该 UC 是对"该 AGV 当前 RIOT 任务队列变为空"这一同一触发窗口的两个竞争消费者——AGV 空闲后，UC-008 会尝试自动派发本地待处理搬运任务，本 UC 则由 R-13 主动争取该窗口派发充电任务；两者不做互相抢占，谁先执行谁获胜，若本 UC 请求时窗口已被 UC-008 消费，则本次充电请求被拒绝（见 Exception Flow E2.1）。
* [[uc-009-monitor-move-order-until-arrival|UC-009]]：本 UC 下发充电任务后，AGV 移动至充电桩的导航过程是否需要复用该 UC 的轮询监听逻辑，TBD 待补充，本 UC 暂不展开该过程本身。
* [[uc-011-view-slot-monitoring-dashboard|UC-011]]：该看板当前只展示仓位相关状态，是否需要扩展展示 AGV 的"充电中"状态，TBD 待补充，见 Notes。
* [[uc-013-enable-disable-agv|UC-013]]：本 UC 新增的 Precondition 第 4 条依赖该 UC 维护的"已禁用"/"禁用待生效"状态——处于该状态的 AGV 无法被本 UC 手动派发充电任务（见 Exception Flow E2.3）；若需要为已禁用的 AGV 发起充电，需先通过该 UC 将其启用。

## Other Information 其他信息

