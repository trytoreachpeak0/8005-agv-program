---
id: FR-007
type: functional-requirement
title: "Pre-Departure Load Clear-and-Cancel 离站前装货清空并取消"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-006"]
related_br: []
related_fr: ["FR-006"]
related_nfr: ["NFR-002"]
related_tc: ["TC-015", "TC-016", "TC-017", "TC-098", "TC-099", "TC-100", "TC-101", "TC-102", "TC-119"]
aliases: ["FR-007"]
---

# FR-007 Pre-Departure Load Clear-and-Cancel 离站前装货清空并取消

## Description 需求描述

系统应允许已核验操作员在 StopClosureCommit 前，从 CurrentStopWorklist 选择一个未处于关键硬件故障恢复的装货 DemandId 执行“清空并取消”，不论其尚未装货、部分装货或已经自动提交。服务端授权所选 DemandId 的完整目标仓位范围；车载端将其中实时 OCCUPIED 的仓位批量打开，完整范围全部证明 EMPTY 且机构安全后才报告 ALL_EMPTY，服务端随后完成取消。

取消只作用于所选 DemandId/LoadBatch，同车其它 SUBLOT 不受影响。不同 SUBLOT 的物理仓位操作必须串行。正式提交后的取消保留原确认与提交历史。取消不要求原因；取消抑制当前 DemandId，不永久拉黑 SUBLOT。

## Acceptance Criteria 验收标准

- **AC-1（未装货任务直接取消）**
  - **Given** 目标 DemandId 尚无物理装载且车辆未离站
  - **When** 操作员确认“清空并取消”
  - **Then** 服务端授权空范围，车载端报告 ALL_EMPTY，服务端完成取消并记录操作

- **AC-2（已装货任务批量清空）**
  - **Given** 所选 DemandId 已部分或全部装货且车辆未离站
  - **When** 服务端授权取消
  - **Then** 只把该 DemandId 中实时 OCCUPIED 的目标仓位组成 BatchUnlock 集合一次性打开；EMPTY 仓位跳过，其它 SUBLOT 仓位不得加入

- **AC-3（全部为空后才完成取消）**
  - **Given** 取消清空正在执行
  - **When** 所选 DemandId 的完整目标范围全部达到 `EMPTY + 锁闭 + 开锁输出已复位`
  - **Then** 车载端可靠报告 ALL_EMPTY；服务端终结为 `CANCELLED_BY_OPERATOR`，释放预留与仓位并发布新版作业清单

- **AC-4（目标态不符自动重开）**
  - **Given** 某取消仓位锁闭后仍为 OCCUPIED
  - **When** 车载端取得稳定有效占用状态
  - **Then** 自动再次弹开该仓门，不设强制放行次数上限；UNKNOWN 或机构状态无效时暂停恢复

- **AC-5（正式提交后的补偿审计）**
  - **Given** LoadBatch 已自动提交但 StopClosureCommit 尚未发生
  - **When** 操作员完成清空并取消
  - **Then** 最终有效状态为 CANCELLED_BY_OPERATOR，同时保留原装货操作员、原提交事实、取消操作和逐仓清空证据

- **AC-6（多 SUBLOT 隔离）**
  - **Given** A 与 B 均已装好并占用不同仓位
  - **When** 操作员取消 A
  - **Then** 只清空 A 的完整目标仓位；B 的仓位、任务、确认记录和业务占用保持不变

- **AC-7（不同 SUBLOT 物理操作串行）**
  - **Given** B 尚在装货、纠错、补偿或取消
  - **When** 操作员请求取消 A
  - **Then** 服务端以稳定忙碌原因拒绝授权；B 到达稳定边界后可重新发起

- **AC-8（取消范围与后续复用）**
  - **Given** A 已取消并收到包含取消终态和释放仓位的新版 CurrentStopWorklistSnapshot
  - **When** 操作员提交新的合法 SUBLOT-C
  - **Then** A 释放的仓位可用于 C；A 的 DemandId 终态与 TransportDemandKey 永久抑制保持，同一 SUBLOT 以后命中其它任务类型时不受永久阻断

- **AC-9（已离站或业务状态不合法时拒绝）**
  - **Given** 车辆已经离站，或目标 DemandId 已取消、已进入其它不可取消终态
  - **When** 操作员请求清空并取消
  - **Then** 服务端返回 REJECTED 与稳定原因码，不下发任何开锁指令

- **AC-10（关键硬件故障不能走普通取消）**
  - **Given** 目标 LoadBatch 因锁 DI 等关键硬件故障处于 VehicleRecoveryRequired
  - **When** 普通生产操作员通过本 FR 请求清空并取消
  - **Then** 服务端拒绝普通取消且不下发开锁；必须先由 R-09 或等效生产管理权限作出 LoadCompensationDecision，再按 FR-002 的专用补偿恢复边界处理

## Related 关联

- **Use Cases：** [[uc-006-cancel-transport-task-upon-arrival|UC-006]]
- **Functional Requirements：** LoadCorrectionPending 可由 [[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] 转入本 FR
- **Non-Functional Requirements：** 授权、拒绝、逐仓清空、取消终态和历史补偿均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-015|TC-015]]：未装货任务直接取消
- [[TC-016|TC-016]]：已离站或不合法状态拒绝
- [[TC-017|TC-017]]：已装货任务批量清空后取消
- [[TC-098|TC-098]]：占用不符自动重开
- [[TC-099|TC-099]]：正式提交后取消保留历史
- [[TC-100|TC-100]]：取消 A 保留 B
- [[TC-101|TC-101]]：另一 SUBLOT 活动时拒绝穿插
- [[TC-102|TC-102]]：取消释放仓位供新 SUBLOT 复用
- [[TC-119|TC-119]]：关键硬件故障不能用普通取消绕过生产决策权限

## Notes 备注

- 正常离站前清空并取消不要求班组长审批或填写取消原因；关键硬件故障后的整批清空不属于本规则，必须先取得 LoadCompensationDecision。
- 车辆离站后不适用本 FR，必须转异常卸出。
- 车载端在新版 CurrentStopWorklistSnapshot 到达前不得仅凭本地 EMPTY 提前复用仓位。
