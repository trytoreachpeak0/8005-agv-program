---
id: FR-006
type: functional-requirement
title: "Multi-Slot Unlock, Retrieval and Occupancy Rollback 多仓位批量开锁、取出与占位回滚"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-005", "UC-004"]
related_br: []
related_fr: ["FR-005"]
related_nfr: ["NFR-002"]
related_tc: ["TC-009", "TC-010", "TC-011", "TC-012", "TC-013", "TC-014"]
aliases: ["FR-006"]
---

# FR-006 Multi-Slot Unlock, Retrieval and Occupancy Rollback 多仓位批量开锁、取出与占位回滚

## Description 需求描述

系统应当在 [[fr-005-mis-stored-retrieval-eligibility-check|FR-005]] 核验通过后，在通过移动安全联锁核验的前提下，一次性向目标子批号关联的全部仓位下发开锁指令（不支持只开其中部分仓位）；操作员取出产品并关闭仓门后，依据光幕检测确认各仓位内确实已无产品残留，将这些仓位状态由"已占用"回滚为"空闲"，清除仓位—子批号映射关系，并记录本次取出操作（操作员、原子批号、仓位号、时间戳）。开锁失败、打开后发现仓位实际为空、或关门后光幕仍检测到残留时，系统必须按约定标记异常锁定或要求重新处理，不得静默完成回滚。

## Rationale 制定原因

将 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 中"批量开锁—取出—关门—光幕核验—回滚"的系统侧能力收敛为可验收切片，保证纠错取出后的仓位状态与现场实物、追溯数据一致，同一子批号下的其他仓位不因单个仓位异常而被阻塞。

## Origin 需求来源

- [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] Normal Flow 第 3~6 步及 Exception Flow E3.1、E3.2、E5.1
- [[uc-004-slot-door-safety-interlock|UC-004]] Flow A（开锁前移动核验）

## Acceptance Criteria 验收标准

- **AC-1（开锁前移动联锁）**
  - **Given** 已通过 FR-005 核验，且按 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A 判定 AGV 当前处于移动状态
  - **When** 系统准备下发批量开锁指令
  - **Then** 系统拒绝本次开门/开锁，不得下发开锁指令

- **AC-2（批量开锁成功）**
  - **Given** AGV 未在移动
  - **When** 系统一次性向该子批号关联的全部仓位下发开锁指令，且各仓门在规定时间内正常打开
  - **Then** 系统允许操作员从全部仓位中取出产品

- **AC-3（开锁超时，异常锁定）**
  - **Given** 其中某仓位仓门未能在规定时间内正常打开
  - **When** 系统核验开锁结果
  - **Then** 系统将该仓位标记为"异常锁定"，暂停对该仓位的后续操作；该子批号关联的其他仓位不受影响，仍按计划打开

- **AC-4（打开后实际为空，异常锁定）**
  - **Given** 某仓位打开后，操作员核验发现该仓位内实际没有产品，与系统记录不一致
  - **When** 操作员上报该仓位状态异常
  - **Then** 系统将该仓位标记为"异常锁定"，暂停分配该仓位；该子批号关联的其他仓位不受影响，可正常继续取出流程

- **AC-5（关门后光幕确认清空，回滚成功）**
  - **Given** 全部仓位仓门已关闭，光幕检测确认各仓位内确实已无产品残留
  - **When** 系统执行关门后核验与回滚
  - **Then** 该子批号关联的全部仓位状态由"已占用"回滚为"空闲"，清除仓位—子批号映射关系；记录本次取出操作（操作员、原子批号、仓位号、时间戳）；相关搬运任务状态保持"进行中"

- **AC-6（关门后光幕检测残留，要求重新处理）**
  - **Given** 操作员已关闭某仓位仓门，但光幕仍检测到产品残留
  - **When** 系统执行关门后核验
  - **Then** 系统不得将该仓位回滚为"空闲"，提示该仓位取出未完成并要求操作员重新打开该仓位，直至光幕确认无残留后才允许按 AC-5 回滚

## Related 关联

- **Use Cases：** 支撑 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]；开锁前依赖 [[uc-004-slot-door-safety-interlock|UC-004]]
- **Business Rules：** 无
- **Functional Requirements：** 前置核验依赖 [[fr-005-mis-stored-retrieval-eligibility-check|FR-005]]
- **Non-Functional Requirements：** 开锁、异常锁定、回滚落库等关键操作须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-009|TC-009]]：移动联锁拒绝开锁
- [[TC-010|TC-010]]：批量开锁成功
- [[TC-011|TC-011]]：开锁超时，异常锁定
- [[TC-012|TC-012]]：打开后实际为空，异常锁定
- [[TC-013|TC-013]]：关门后光幕确认清空，回滚成功
- [[TC-014|TC-014]]：关门后光幕检测残留，要求重新处理

## Notes 备注

- 本 FR 不要求班组长审批（见 UC-005 Precondition 备注），也不记录"取出原因"字段，只记录操作员、原子批号、仓位号、时间戳。
- 支持反复纠错：同一仓位/子批号取出后若重新装载又发现有误，可再次触发本 FR，不限制纠错次数。
- 任务一旦通过 [[uc-002-confirm-task-completion|UC-002]] 确认完成后才发现存错，如何处理不在本 FR 范围内，需要额外的退料/异常处理流程（TBD，见 UC-005 Notes）。
