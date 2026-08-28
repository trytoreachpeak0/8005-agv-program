---
id: UC-005
type: use-case
title: "装货时取出并重放放错产品"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-08
updated: 2026-07-30
primary_actor: "生产操作员"
secondary_actor: "ControlServer"
frequency: "待定，预期远低于 UC-001 的装载频率"
related_uc: ["UC-001", "UC-002", "UC-004", "UC-006", "UC-011", "UC-043"]
related_br: []
aliases: ["UC-005"]
---

# UC-005 装货时取出并重放放错产品

## 描述

StopClosureCommit 前，生产操作员若发现当前或先前仓位放错产品，可以在不取消该 SUBLOT 任务、不改变目标仓位集合、也不撤销已经形成的 LoadBatch 提交事实的前提下纠正。

- 当前仓门尚未锁闭：在当前仓位操作内直接取出错误产品、放入正确产品，不另建 LoadCorrection。
- 放错仓位已经锁闭：操作员选择该物理仓位，服务端在原 SlotOperationAttemptId 下授权 LoadCorrection；车载端只重新打开该仓位，正确产品必须放回原仓位。

纠错期间暂停后续仓位装货。一个 SUBLOT 要么全部目标仓位装入成功后整体提交，要么最终全部不装，不允许部分装入成为成功终态。

## 触发条件

操作员在 LoadBatch 正式提交前发现当前 SUBLOT 的某个仓位放错产品，并决定取出后继续完成同一 SUBLOT。

## 前置条件

1. AGV 尚未离开当前站点，StationOperationGuard 有效，IO 与安全状态允许仓位操作。
2. 当前停靠尚未 StopClosureCommit；LoadBatch 可以尚未提交或已经自动提交。
3. 若目标仓位已经锁闭，它必须属于当前 SUBLOT 的完整目标仓位集合，实时状态为 OCCUPIED，且没有另一 SUBLOT 正在执行物理仓位操作。
4. 生产操作员已通过 [[uc-043-verify-identity-and-manage-operation-session|UC-043]] 取得当前 SUBLOT 绑定的有效工号；同一 SUBLOT 内不得换人。
5. 本操作不需要班组长审批，也不要求填写纠错原因。

## 后置条件

### 纠错完成

1. 原仓位达到 `OCCUPIED + 锁闭 + 开锁输出已复位`。
2. 原任务、SUBLOT、DemandId、SlotOperationAttemptId、目标仓位集合、SublotReservation 和仓位—SUBLOT 映射均不改变。
3. 若还有未装目标仓位，恢复 UC-001；若已全部装完，保持原 LoadBatch 提交事实并重新进入 StationDepartureWaiting。
4. 纠错请求、授权、逐仓物理结果和操作员被记录。

### 等待重放

错误产品已经取出但正确产品暂时不可得时，进入 LoadCorrectionPending。原任务、预留和 StationOperationGuard 均保持，后续装货暂停；只能稍后在原仓位继续重放，或转 [[uc-006-cancel-transport-task-upon-arrival|UC-006]] 清空并取消。

## 正常流程

### 5.0 已锁闭仓位纠错

1. 操作员在当前 SUBLOT 的目标仓位图中选择一个放错且已经锁闭的物理仓位，发起“取出重放”。
2. 服务端核验前置条件，并在原 SlotOperationAttemptId 下返回可靠的 LoadCorrectionCommand；车载端暂停打开后续装货仓位。
3. 车载端只打开所选原仓位，不打开同一 SUBLOT 的其它仓位。
4. 操作员取出错误产品，再把正确产品放回原仓位。
5. 操作员关门；锁闭反馈有效后，车载端读取稳定的 SlotOccupancyState。
6. 若状态为 OCCUPIED、锁闭有效且开锁输出已复位，车载端可靠上报 LoadCorrectionResult，服务端恢复原 LoadBatch 的后续流程。

## 备选流程

### A1 当前仓门尚未锁闭

1. 操作员在当前开门仓位发现放错。
2. 操作员直接取出错误产品并放入正确产品。
3. 车载端继续当前仓位操作；达到 `OCCUPIED + 锁闭 + 开锁输出已复位` 后按 UC-001 正常完成。本分支不创建 LoadCorrection。

### A2 正确产品暂时不可得

1. 操作员已取出错误产品，但无法立即取得正确产品。
2. 允许先把原仓位安全锁闭为空仓，系统进入 LoadCorrectionPending，不把 EMPTY 记为纠错成功。
3. 后续只允许：
   - 再次打开原仓位并放入正确产品，返回 Normal Flow 第 4 步；
   - 转 UC-006，对当前 SUBLOT 执行“清空并取消”。

## 异常流程

### E1 关门后仍为 EMPTY

系统自动再次弹开原仓门并提示放入正确产品；不设可强制放行的重试次数上限。操作员可以暂停并呼叫维护，但任务、预留和 StationOperationGuard 保持。

### E2 状态为 UNKNOWN 或机构状态无效

系统不自动猜测或循环开锁，暂停当前操作并进入恢复；恢复完成前不得继续其它仓位或离站。

### E3 本站已经结束

StopClosureCommit 已发生时服务端拒绝普通 LoadCorrection；车辆未移动也不得重新开放本站。车辆已经离站时转独立异常卸出流程。

### E4 另一 SUBLOT 正在执行物理仓位操作

服务端拒绝穿插纠错。必须等待另一 SUBLOT 完成或取消到稳定边界后重新发起。

## 备注

- LoadCorrection 的最小单位是操作员选定的一个原仓位，不是整个 SUBLOT；同一时刻只纠正一个仓位。
- 花篮没有独立身份，系统无法自动识别产品是否放错；正确归属由已核验操作员承担，光幕只证明 OCCUPIED/EMPTY。
- 支持反复纠错，不限制次数，但每次都必须在原仓位完成 `OCCUPIED → EMPTY → OCCUPIED`。
- UC-005 不清除仓位—SUBLOT 映射，也不释放 SublotReservation。

## 关联用例

- [[uc-001-load-completed-lot-into-slot|UC-001]]：纠错可以在装货中途发生，完成后恢复剩余装货。
- [[uc-002-confirm-task-completion|UC-002]]：纠错安全闭环后重新进入离站等待；操作员可用该 UC 结束本站。
- [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：操作员决定不再存放时直接转“清空并取消”，不是先完成 UC-005 再重新取消。
- [[uc-043-verify-identity-and-manage-operation-session|UC-043]]：沿用当前 SUBLOT 绑定工号。
