---
id: FR-008
type: functional-requirement
title: "Destination Station Auto-Identify and Batch Unlock 终点站自动识别待取料仓位并批量开锁"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-010", "UC-004"]
related_br: ["BR-013", "BR-014"]
related_fr: ["FR-009"]
related_nfr: ["NFR-002"]
related_tc: ["TC-018", "TC-019", "TC-020", "TC-021", "TC-022"]
aliases: ["FR-008"]
---

# FR-008 Destination Station Auto-Identify and Batch Unlock 终点站自动识别待取料仓位并批量开锁

## Description 需求描述

系统应当在 AGV 到达某站点后，自动识别该 AGV 上所有“目标（交货）站点=当前站点”且状态为“已占用”的仓位，在界面上列出本次到站待取料清单；不要求输入 Sublot，8005 项目也不要求输入工号。通过移动安全联锁后，车载端须先持久化完整集合，再执行批量开锁：同一 IO 模块内优先使用 Modbus `0x0F` 写多个线圈，跨模块按模块分组并行发送，全部已计划分组发送后才统一检查反馈。开锁失败或状态未知不得影响已经成功打开仓位的正常处理。

## Rationale 制定原因

终点站场景下产品已在 AGV 上、任务归属已明确，不存在"扫错子批号"的问题，因此仓位识别可完全由系统自动完成；将 [[uc-010-unload-completed-lot-at-destination-station|UC-010]] Normal Flow 第 1、2 步（含系统核验点）落实为可单独验收的能力，为后续取出与占位回滚（见 [[fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation|FR-009]]）提供正确的待处理仓位集合。

## Origin 需求来源

- [[uc-010-unload-completed-lot-at-destination-station|UC-010]] Normal Flow 第 1、2、2.0、2.1、2.2 步及 Exception Flow E2.1、E2.2
- [[uc-004-slot-door-safety-interlock|UC-004]] Flow A（开锁前移动核验）
- [[br-013-multi-basket-loading|BR-013]]（花篮装载明细与开门语义）、[[br-014-transport-task-types-and-fixed-stations|BR-014]]（合法终点由任务冻结站点决定）

## Acceptance Criteria 验收标准

- **AC-1（自动识别待取料清单）**
  - **Given** AGV 已到达某站点，且该 AGV 上存在一个或多个"已占用"且关联任务目标站点等于当前站点的仓位
  - **When** 系统在到站后执行仓位识别
  - **Then** 系统自动列出这些仓位/任务作为本次到站待取料清单，不要求操作员扫码

- **AC-2（开锁前移动联锁）**
  - **Given** 已生成待取料清单，且按 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A 判定 AGV 当前处于移动状态
  - **When** 系统准备下发开锁指令
  - **Then** 系统拒绝本次开门/开锁，不得下发开锁指令

- **AC-3（批量开锁成功）**
  - **Given** AGV 未在移动
  - **When** 车载端已持久化目标集合并向相关 IO 模块发送批量开锁
  - **Then** 同一模块使用一次 `0x0F`；跨模块按模块分组并行发送；全部发送后逐仓核验锁 DI，成功仓位允许操作员取出产品

- **AC-4（开锁超时，异常锁定）**
  - **Given** 某仓位仓门未能在规定时间内正常打开
  - **When** 系统核验开锁结果
  - **Then** 系统提示该仓位开锁异常，将其标记为"异常锁定"，不自动重复开锁；其它已打开仓位继续取货和关门

- **AC-6（跨模块部分成功）**
  - **Given** 目标仓位跨多个 IO 模块
  - **When** 部分模块批量写成功、部分模块通信失败或结果未知
  - **Then** HMI 分别显示成功、失败和未知仓位；成功仓位继续处理，失败或未知仓位读取实时 DO/DI 后进入恢复，整车在全部目标处理或服务端明确处置前不得离站

- **AC-5（打开后实物不符，异常锁定）**
  - **Given** 某仓位打开后，操作员核验发现该仓位内实际无产品，或存放的产品与系统记录的子批号不符
  - **When** 操作员上报该仓位状态异常
  - **Then** 系统将该仓位标记为"异常锁定"，暂停对该仓位的后续操作；该 AGV 上其他待取料仓位不受影响

## Related 关联

- **Use Cases：** 支撑 [[uc-010-unload-completed-lot-at-destination-station|UC-010]]；开锁前依赖 [[uc-004-slot-door-safety-interlock|UC-004]]
- **Business Rules：** 遵循 [[br-013-multi-basket-loading|BR-013]]（按装载明细/仓位识别）、[[br-014-transport-task-types-and-fixed-stations|BR-014]]（目标站点合法性已在任务冻结时确定）
- **Functional Requirements：** 识别与开锁完成后由 [[fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation|FR-009]] 承接关门核验与状态回滚
- **Non-Functional Requirements：** 自动识别、开锁与异常锁定等关键操作须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-018|TC-018]]：自动识别待取料清单
- [[TC-019|TC-019]]：移动联锁拒绝开锁
- [[TC-020|TC-020]]：批量开锁成功
- [[TC-021|TC-021]]：开锁超时，异常锁定
- [[TC-022|TC-022]]：打开后实物不符，异常锁定

## Notes 备注

- 本 FR 不核验"该任务是否属于本次派车范围"：任务此时已装载在 AGV 上、目标站点已在装载时确定，不存在扫错子批号的问题（与 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]] 的核验目的不同，两者不重复）。
- 任务的目标站点判定过程本身不在本 FR 核验范围内（视为已在装载/下发阶段正确确定，见 UC-010 Assumption）。
