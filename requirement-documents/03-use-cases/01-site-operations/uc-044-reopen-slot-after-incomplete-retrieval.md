---
id: UC-044
type: use-case
title: "取料关门后检测到残留产品时重新打开仓位 Reopen Slot After Incomplete Retrieval"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
primary_actor: "终点站操作员（按场景引用 R-02/R-03/R-04/R-06/R-07/R-08，见 [[stakeholders-and-user-classes|干系人与用户角色清单]]）"
secondary_actor: "无（本操作只涉及本地数据库与仓位/光幕状态，不需要 MES 参与）"
frequency: "待定，预期远低于 UC-010 的正常取料频率"
related_uc: ["UC-002", "UC-004", "UC-010", "UC-043"]
related_br: []
aliases: ["UC-044"]
---

# UC-044 取料关门后检测到残留产品时重新打开仓位

## 描述

在 [[uc-010-unload-completed-lot-at-destination-station|UC-010]] 的取料流程中，操作员关闭仓位仓门后，若光幕检测到该仓位内仍有产品残留（说明取料不彻底，或误关门时仓内产品尚未取出），系统判定本次关闭未完成，自动再次弹开该仓门，供操作员取出残留产品后再次关闭，直至光幕确认该仓位内已清空为止。

本 UC 从 UC-010 原 Exception Flow E4.1 拆分而来，写法上参照 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 相对 [[uc-001-load-completed-lot-into-slot|UC-001]] 的拆分方式：触发方式是系统通过光幕自动检测，不额外提供操作员主动发起"重新打开"的独立入口。

## 触发条件

[[uc-010-unload-completed-lot-at-destination-station|UC-010]] Normal Flow 中，操作员关闭某仓位仓门后，系统通过光幕检测到该仓位内仍有产品残留，与系统预期的"已清空"状态不一致。

## 前置条件

**设备与硬件**

1. 目标仓位当前处于"仓门已关闭，但光幕检测到残留产品"的异常状态。
2. IO 模块通信正常，可正常对该仓位执行开锁及门状态/光幕读取操作。

**任务与数据**

3. 该仓位关联的卸货尚未达到 `EMPTY + 锁闭 + 开锁输出已复位` 的物理闭环。

**人员与权限**

4. 若项目级卸货身份核验策略开启，则沿用当前已核验工号；8005 项目该策略关闭，不要求输入工号。

## 后置条件

**设备与硬件**

1. 目标仓位电子锁在重新关闭后恢复锁闭状态。
2. 光幕检测确认该仓位内确已清空，与系统记录一致。

**任务与数据**

3. 目标仓位状态恢复为 UC-010 预期的"空闲"，与 UC-010 后续流程衔接一致。
4. 本次重新打开、取出残留产品及重新核验的操作（操作员、仓位号、时间戳）被记录到本地数据库，用于追溯。

## 假设

1. 操作员能够在重新打开仓位后正确识别并取出全部残留产品，不会遗漏。

## 正常流程

### 44.0

1. 系统通过光幕检测到操作员刚关闭的仓位内仍有产品残留
2. 系统提示该仓位“取出未完成”，准备自动再次弹开仓门
3. 系统按 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A 核验该 AGV 当前是否处于移动状态，只有核验通过（未在移动）才允许下发开锁指令，否则拒绝本次开门（见该 UC Exception Flow EA1.1）
4. 系统自动输出开锁脉冲，重新弹开该仓位仓门
5. 操作员取出残留产品
6. 操作员重新关闭该仓位仓门
   6.1 系统通过光幕检测确认该仓位内确已清空（见 Exception Flow E6.1）
7. 核验通过后，系统将该仓位状态恢复为 UC-010 预期的"空闲"，记录本次处理过程，流程返回 [[uc-010-unload-completed-lot-at-destination-station|UC-010]] 继续

## 备选流程

不存在需要区分的备选流程：无论该仓位是首次还是多次重新打开后仍检测到残留，均按 Normal Flow 重复第 4～6 步，直至光幕确认清空。

## 异常流程

以下异常与 Normal Flow 中的对应步骤关联：

- E6.1 重新关闭后光幕仍检测到残留

### E6.1 重新关闭后光幕仍检测到残留

1. 操作员重新关闭仓位仓门
2. 系统按第 6.1 步通过光幕检测，发现该仓位内仍检测到产品残留
3. 系统提示该仓位取出仍未完成，并自动再次输出开锁脉冲
4. 系统重新执行第 4～6 步，直至该仓位光幕确认已清空，不设可强制放行的重试次数上限；操作员可暂停并上报班组长或设备/电气维护人员（R-11），但任务与 StationOperationGuard 保持

## 备注

- 本 UC 从 [[uc-010-unload-completed-lot-at-destination-station|UC-010]] 原 Exception Flow E4.1 拆分而来，独立成文，便于单独维护和引用；UC-010 自身的 Normal Flow 与 Exception Flow 相应改为指向本 UC，不再重复描述具体的重新打开流程。
- 本 UC 触发方式仅为系统光幕自动检测，不提供操作员主动发起"重新打开"的独立入口；若操作员在关门、光幕核验通过之后才发现问题（如产品已经离开仓位现场），不在本 UC 范围内，需另行处理。
- 本 UC 的重新打开动作属于当前 Sublot 的仓位操作，继续沿用该 Sublot 已绑定的操作员，不需要重复验证身份，也不允许在该 Sublot 完成前更换操作员。
- [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 中也存在类似的"关闭仓门后光幕检测到残留"场景（其 Exception Flow E5.1），与本 UC 处理逻辑相似但服务的是装载/纠错方向；两者是否需要进一步合并为统一的底层能力，留待后续讨论，本 UC 暂不改动 UC-005。

## 关联用例

- [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：本 UC 从其 Exception Flow E4.1 拆分而来，处理完毕后流程返回该 UC 继续；该 UC 的 Normal Flow 第 4.1 步及 Exception Flow E4.1 改为指向本 UC。
- [[uc-004-slot-door-safety-interlock|UC-004]]：本 UC 重新打开仓门前，需先经过该 UC Flow A 核验 AGV 当前是否移动（移动中则拒绝开门）。
- [[uc-002-confirm-task-completion|UC-002]]：不参与卸货任务提交；本 UC 处理完毕后由 UC-010 按逐仓卸货闭环更新业务状态。
- [[uc-043-verify-identity-and-manage-operation-session|UC-043]]：本 UC 复用当前到站会话和当前 Sublot 已绑定的操作员，不需要重复验证身份。

## 其他信息
