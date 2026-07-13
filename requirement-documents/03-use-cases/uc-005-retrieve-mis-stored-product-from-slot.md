---
id: UC-005
type: use-case
title: "Retrieve Mis-stored Product from Slot 取出仓位中存错的产品"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-08
updated: 2026-07-09
primary_actor: "Production Operator 生产操作员"
secondary_actor: "None 无（本操作只涉及本地数据库回滚，不需要 MES 参与）"
frequency: "TBD 待定，预期远低于 UC-001 的装载频率"
related_uc: ["UC-001", "UC-002", "UC-004", "UC-006", "UC-011"]
related_br: []
aliases: ["UC-005"]
---

# UC-005 Retrieve Mis-stored Product from Slot 取出仓位中存错的产品

## Description 描述

After a slot door is closed during [[uc-001-load-completed-lot-into-slot|UC-001]], and before the corresponding task is confirmed complete via [[uc-002-confirm-task-completion|UC-002]], the production operator may discover that the wrong product was stored (wrong sublot, wrong quantity, or a damaged item). This use case allows the operator to select the affected sublot; the system reopens all slot(s) associated with that sublot together (a sublot may occupy one or more slots, and partial retrieval of only some of its slots is not supported), so the operator can remove all the products and roll the slot(s) and task data back to the state before the mistaken load, allowing a correct load (or no load) to proceed. 在 [[uc-001-load-completed-lot-into-slot|UC-001]] 完成装载、仓门关闭之后，且对应任务尚未通过 [[uc-002-confirm-task-completion|UC-002]] 确认完成之前，若生产操作员发现某子批号存放的产品有误（子批号错误、数量错误、产品损坏等），可通过本 UC 选择该子批号，系统会将该子批号关联的全部仓位（一个子批号可能对应一个或多个仓位）一起重新打开，不支持只取出其中部分仓位，操作员取出全部产品后，将这些仓位与任务数据回滚到误装载之前的状态，以便后续重新正确装载或保持空闲。

## Trigger 触发条件

The production operator discovers that a sublot was mis-stored and needs to retrieve all of its associated slot(s) before the task is confirmed as completed. 生产操作员发现某子批号存放的产品有误，需要在任务被确认完成之前取出该子批号对应的全部产品

## Precondition 前置条件

**Equipment & Hardware 设备与硬件**

1. The IO module is communicating normally, so the lock(s) of the target sublot's slot(s) can be released and door status read. IO 模块通信正常，可正常对该子批号关联的仓位执行开锁及门状态读取操作

**Task & Data 任务与数据**

2. All slot(s) associated with the target sublot are currently "Occupied", and the corresponding task has not yet been confirmed as completed via [[uc-002-confirm-task-completion|UC-002]]. 目标子批号关联的全部仓位当前状态均为"已占用"，且其关联任务尚未通过 UC-002 确认完成

**Personnel & Authorization 人员与权限**

3. The production operator has permission to reopen occupied slot(s) for correction. 生产操作员具备"开仓纠错取出"操作权限

> 经与用户确认：本操作不需要班组长（R-09）审批，生产操作员具备该权限后可自行发起并完成取出，不需要额外的二次确认流程。

## Postcondition 后置条件

**Equipment & Hardware 设备与硬件**

1. The electronic locks of all the target sublot's slot(s) return to the locked state after the doors are closed. 目标子批号关联的全部仓位电子锁在仓门关闭后均恢复锁闭状态
2. The light curtains confirm all the doors are closed and all the slots are actually empty, consistent with the system record. 光幕检测确认全部仓门已关闭且仓位内确实无产品，与系统记录一致

**Task & Data 任务与数据**

3. All the target sublot's slot statuses change back from "Occupied" to "Idle", and the previously recorded slot–sublot mappings are rolled back/cleared. 目标子批号关联的全部仓位状态由"已占用"回滚为"空闲"，原先记录的仓位-子批号映射关系被回滚/清除
4. The retrieval operation (operator, original sublot, slot number(s), timestamp) is logged in the local database for traceability. 本次取出操作（操作员、原子批号、仓位号、时间戳）被记录到本地数据库，用于追溯
5. The associated transport task remains "Executing" status, awaiting a correct load. 相关搬运任务状态保持"进行中"，等待重新正确装载

## Assumption 假设

TBD 待补充

## Normal Flow 正常流程

### 5.0 Retrieve Mis-stored Product from Slot
1. 生产操作员发现某子批号存放的产品有误
2. 生产操作员选择该子批号，发起"取出"请求
   2.1 系统核验该子批号关联的全部仓位是否均为"已占用"状态，且对应任务尚未被 [[uc-002-confirm-task-completion|UC-002]] 确认完成（见 Exception Flow E2.1）
3. 系统一次性打开该子批号关联的全部仓位仓门（不支持只打开/取出其中部分仓位）
   3.1 系统核验各仓位仓门是否均已正常打开（见 Exception Flow E3.1）
   3.2 生产操作员核验各仓位内是否确实存放有产品，与系统记录一致（见 Exception Flow E3.2）
4. 生产操作员从全部仓位中取出产品
5. 生产操作员关闭全部仓位
   5.1 系统通过光幕检测确认各仓位内确实已无产品残留（见 Exception Flow E5.1）
6. 系统将该子批号关联的全部仓位状态回滚为"空闲"，清除仓位-子批号映射关系

## Alternative Flow 备选流程

TBD 待补充

## Exception Flow 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤（或子步骤）一一对应：

* E2.1 该子批号关联仓位状态不满足核验条件（未占用 / 对应任务已被确认完成）
* E3.1 仓门开锁失败（电子锁/机械故障）
* E3.2 打开仓门后发现某仓位实际为空，无产品可取
* E5.1 关闭仓门后光幕检测仓位内仍有产品残留

### E2.1 该子批号关联仓位状态不满足核验条件
1. 生产操作员选择子批号，发起取出请求
2. 系统按第 2.1 步核验，出现以下任一情况：
   2.1 该子批号关联的仓位中存在并非"已占用"状态的仓位
   2.2 该子批号对应的任务已经通过 [[uc-002-confirm-task-completion|UC-002]] 确认完成
3. 系统拒绝本次取出请求，提示"当前不可取出"
4. 生产操作员核对子批号及现场情况；若确认是因为任务已被确认完成才发现存错，需走退料/异常处理流程（超出本 UC 范围，见 Notes），否则联系班组长协助核实

### E3.1 仓门开锁失败
1. 系统按第 3 步向该子批号关联的全部仓位下发开锁指令
2. 系统核验发现其中某仓位仓门未能在规定时间内正常打开
3. 系统将该仓位标记为"异常锁定"，暂停对该仓位的后续操作；该子批号关联的其他仓位不受影响，仍按计划打开
4. 生产操作员联系设备/电气维护人员（R-11）处理
5. 设备/电气维护人员排查并修复电子锁/机械故障后，解除该仓位的"异常锁定"，操作员重新发起取出请求

### E3.2 打开仓门后发现某仓位实际为空
1. 系统按第 3 步打开该子批号关联的全部仓位
2. 生产操作员按第 3.2 步核验，发现其中某仓位内实际没有产品，与系统记录不一致
3. 生产操作员上报该仓位状态异常
4. 系统将该仓位标记为"异常锁定"，暂停分配该仓位，等待核实原因（如历史记录未正确关闭、人工误操作等）；该子批号关联的其他仓位不受影响，可正常继续取出流程
5. 核实并处理完毕（清空仓位或更正系统记录）后，方可解除该仓位的"异常锁定"，恢复正常使用

### E5.1 关闭仓门后光幕检测仓位内仍有产品残留
1. 生产操作员关闭全部仓位仓门
2. 系统按第 5.1 步通过光幕检测，发现其中某仓位内仍检测到产品残留
3. 系统提示该仓位取出未完成，要求生产操作员重新打开该仓位确认
4. 生产操作员重新打开该仓位，取出残留产品后再次关闭
5. 系统重新执行"关门→光幕核验"检查（即重新执行第 5.1 步），直至该仓位光幕确认无残留

## Notes 备注

* 本 UC 从 [[uc-001-load-completed-lot-into-slot|UC-001]] 的 Postcondition 拆分而来：用户提出"操作员可能存错东西，需要取出"的场景，与 UC-001 的正向装载流程、UC-002 的确认完成流程都不同，独立为本 UC。
* 若任务已通过 [[uc-002-confirm-task-completion|UC-002]] 确认完成后才发现存错，如何处理不在本 UC 范围内，需要额外的退料/异常处理流程，待后续补充。
* 经与用户确认：本操作以"子批号"为最小操作单位——操作员选择一个子批号后，系统会将该子批号关联的全部仓位（一个子批号可能对应一个或多个仓位）一起打开，要求整批一起取出，不支持只取出其中部分仓位。
* 经与用户确认：本操作不需要班组长审批，生产操作员可自行发起并完成整个取出流程。
* 经与用户确认：取出记录不需要录入"取出原因"，本地数据库中只记录操作员、原子批号、仓位号、时间戳，不单独记录原因字段。
* 经与用户确认：本 UC 支持反复纠错——同一仓位/子批号取出后若重新装载又发现有误，可再次执行本 UC，不限制纠错次数。
* 经与用户确认：`priority` 定为 `medium`，原因是本 UC 属于异常/纠错场景，预期发生频率低于正常装载（[[uc-001-load-completed-lot-into-slot|UC-001]]）。

## Related Use Cases 关联用例

* [[uc-001-load-completed-lot-into-slot|UC-001]]：本 UC 处理的是 UC-001 装载完成后、任务被确认完成前的纠错场景。
* [[uc-002-confirm-task-completion|UC-002]]：任务一旦通过该 UC 确认完成，本 UC 便不再适用。
* [[uc-004-slot-door-safety-interlock|UC-004]]：本 UC 打开仓门期间的 AGV 移动安全联锁检查，由该 UC 统一处理，不在本 UC 的 Precondition 中重复定义。
* [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：本 UC 取出产品、使仓位恢复"空闲"后，若确认该任务确实不再需要运送，可转该 UC 取消任务；UC-006 要求目标任务尚未装载任何仓位，因此已装载的任务需先经本 UC 处理完毕才能被取消。
* [[uc-011-view-slot-monitoring-dashboard|UC-011]]：本 UC 取出纠错、仓位回滚为"空闲"的过程，以及 Exception Flow（E3.1/E3.2）产生的"异常锁定"状态，均会实时体现在该 UC 提供的仓位监控看板中；该 UC 为纯只读展示，不影响本 UC 的流程本身。

## Other Information 其他信息

