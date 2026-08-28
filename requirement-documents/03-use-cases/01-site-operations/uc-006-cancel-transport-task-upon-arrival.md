---
id: UC-006
type: use-case
title: "离站前清空并取消装货任务"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-09
updated: 2026-07-30
primary_actor: "生产操作员"
secondary_actor: "ControlServer"
frequency: "待定，预期低于 UC-001 的装载频率"
related_uc: ["UC-001", "UC-002", "UC-003", "UC-005", "UC-008", "UC-011", "UC-042", "UC-043"]
related_br: []
aliases: ["UC-006"]
---

# UC-006 离站前清空并取消装货任务

## 描述

StopClosureCommit 前，生产操作员可以从 CurrentStopWorklist 中选择任意可取消的装货 DemandId，执行一次统一的“清空并取消”流程。该任务可以尚未装货、只装了一部分，或已经自动提交。

没有物理装载时直接报告 ALL_EMPTY。已经装载时，车载端只把所选 DemandId 中实时确认为 OCCUPIED 的目标仓位组成 BatchUnlock 集合并一次性打开；完整目标范围全部达到 `EMPTY + 锁闭 + 开锁输出已复位` 后，服务端才完成取消。车上其它 SUBLOT 的仓位、任务和确认记录保持不变。

## 触发条件

操作员判断 CurrentStopWorklist 中某个装货任务不再需要执行，选择该 DemandId 并确认“清空并取消”。

## 前置条件

1. AGV 尚未离开当前站点。
2. 目标 DemandId 未取消，且未处于另一个不可取消终态。
3. 同车没有另一 SUBLOT 正在执行装货、纠错、补偿或取消等物理仓位操作。
4. 生产操作员已取得项目策略要求的有效工号；不需要班组长审批。
5. 系统不要求操作员选择或填写取消原因。
6. 目标 LoadBatch 未因关键硬件故障处于 VehicleRecoveryRequired；该状态下不得用本用例绕过生产决策权限，必须先按 UC-001 E2.1 由 R-09 或等效生产管理权限作出 LoadCompensationDecision，再进入专用装货补偿恢复。

## 后置条件

1. 所选 DemandId 的完整目标仓位范围全部为 EMPTY、锁闭且开锁输出已复位。
2. 服务端将该 DemandId 终结为 `CANCELLED_BY_OPERATOR`，释放其 SublotReservation 与仓位占用，并持久化取消抑制记录。
3. 服务端终结当前 DemandId，并在调度侧永久抑制其 TransportDemandKey（任务类型 + SUBLOT）；MES 在人工扫码过站前继续返回同键候选时，MesIngest 仍照常投影，调度不得创建或恢复业务任务。同一 SUBLOT 以后命中其它任务类型时属于不同业务键，不受本次取消影响。
4. 同车其它 SUBLOT 不受影响。
5. 已正式提交任务的原 LoadBatch 提交事实保留，取消以追加补偿记录表达。
6. 服务端发布更高 revision 的 CurrentStopWorklistSnapshot，并重新计算 UpcomingStopPlan。新版快照到达后，释放仓位可以装入新的 SUBLOT。

## 正常流程

### 6.0

1. 操作员从 CurrentStopWorklist 选择一个可取消的装货 DemandId，确认“清空并取消”。
2. 车载端发送 LoadCancellationStartRequested。
3. 服务端核验前置条件，返回 LoadCancellationAuthorization(AUTHORIZED)，携带所选 DemandId 和完整目标仓位范围，并进入 LoadCancelPending。
4. 车载端根据执行日志与实时 IO 核对授权范围：
   - 已经 EMPTY 的目标仓位不打开；
   - OCCUPIED 的目标仓位组成 BatchUnlock 集合，一次性打开；
   - 其它 SUBLOT 的仓位不得加入集合。
5. 操作员取出所选任务的全部产品并按任意顺序关门。
6. 每个仓位在锁闭反馈到达后立即核对稳定 SlotOccupancyState：
   - EMPTY：记录该仓位清空证据；
   - OCCUPIED：自动再次弹开该仓门，要求继续取出；
   - UNKNOWN：暂停并进入恢复。
7. 完整目标范围全部达到 `EMPTY + 锁闭 + 开锁输出已复位` 后，车载端可靠上报 LoadCancellationResult(ALL_EMPTY)。
8. 服务端持久化接受结果后完成取消，释放预留和仓位，发布新版 CurrentStopWorklistSnapshot 与 UpcomingStopPlan。

## 备选流程

### A1 尚未产生物理装载

服务端授权空目标范围；车载端立即报告 ALL_EMPTY，随后按 Normal Flow 第 8 步完成取消。

### A2 授权到达时当前装货仓门已经打开

操作员可以直接取出或不再放入花篮，使当前仓位以 EMPTY 安全收尾并计入取消清空，不要求先完成 OCCUPIED 装货再重新开门。

### A3 车上保留其它 SUBLOT

例如 A 占仓位 1、2，B 占仓位 3、4。取消 A 时只批量打开仓位 1、2；B 的仓位 3、4、任务、确认记录和业务占用保持不变。取消完成并收到新版快照后，仓位 1、2 可以用于新的 SUBLOT-C。

## 异常流程

### E1 请求被拒绝

车辆已离站、任务已经取消、状态不允许取消或另一 SUBLOT 正在执行物理仓位操作时，服务端返回 REJECTED 与稳定原因码。车载端不开始新的开锁动作。

### E2 清空未完成

任一授权仓位仍为 OCCUPIED 时，系统自动再次弹开该仓门，不设可强制放行的重试次数上限；任务保持 LoadCancelPending。

### E3 状态未知或机构故障

SlotOccupancyState 为 UNKNOWN、授权范围与执行日志不一致、锁闭反馈无效或开锁输出无法确认复位时，暂停并进入恢复；车辆不得离站。

### E4 断线

只完成已经开始的当前开锁集合安全收尾。重连后完成 RecoveryHandshake、对账并重新取得服务端授权，才能继续剩余清空。

## 备注

- “全有或全无”以单个 SUBLOT/LoadBatch 为边界，不是整车边界。
- 不要求先执行 UC-005 再回来取消；“清空并取消”从一开始就记录取消意图。
- 初次批量开锁后，每个未达到 EMPTY 的仓位在关门核验时独立自动弹开；已经 EMPTY 且安全锁闭的仓位不因其它仓位失败而重开。
- 取消记录包含 DemandId、SUBLOT、AGV、站点、OperationSession、操作员、时间和逐仓清空证据，不要求原因字段。
- 车载端在新版 CurrentStopWorklistSnapshot 到达前不得只凭本地 EMPTY 提前复用仓位。

## 关联用例

- [[uc-001-load-completed-lot-into-slot|UC-001]]：装货任一阶段均可申请取消；另一 SUBLOT 正在装货时不得穿插。
- [[uc-002-confirm-task-completion|UC-002]]：StopClosureCommit 前仍可补偿取消；本站一旦结束便不再开放普通取消。
- [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]：仍需运输时用单仓纠错；不再运输时直接使用本 UC。
- [[uc-008-dispatch-move-order-to-riot|UC-008]]：取消完成后依据剩余任务重新计算移动计划。
- [[uc-043-verify-identity-and-manage-operation-session|UC-043]]：取消不清除当前工号或结束到站操作会话。
