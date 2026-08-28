---
id: FR-014
type: functional-requirement
title: "Slot Reopen, Residue Clearance Confirm and State Restoration 残留仓位重新打开、清空核验与状态恢复"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-044", "UC-010", "UC-004", "UC-002"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-038", "TC-039", "TC-040", "TC-041"]
aliases: ["FR-014"]
---

# FR-014 Slot Reopen, Residue Clearance Confirm and State Restoration 残留仓位重新打开、清空核验与状态恢复

## Description 需求描述

系统应当在 [[uc-010-unload-completed-lot-at-destination-station|UC-010]] 取料关门并取得有效锁闭反馈后，若稳定光幕状态仍为 OCCUPIED，在通过移动安全联锁核验的前提下自动再次输出开锁脉冲弹开该仓门，供操作员取出残留产品；操作员重新关闭仓门后，依据光幕检测确认该仓位内确已清空，将该仓位状态恢复为 UC-010 预期的"空闲"，并记录本次重新打开、取出残留及重新核验的过程。若重新关闭后仍检测到残留，系统继续自动弹开，不设可强制放行的次数上限；UNKNOWN 或机构状态无效时暂停恢复。

## Rationale 制定原因

保证终点站取料结果与现场实物一致，避免因关门光幕误判或产品未取尽而错误地将仓位标记为"空闲"、影响后续任务分配；将 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 的核心处理能力收敛为可验收切片。

## Origin 需求来源

- [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] Normal Flow 第 1~7 步及 Exception Flow E6.1
- [[uc-004-slot-door-safety-interlock|UC-004]] Flow A（开锁前移动核验）

## Acceptance Criteria 验收标准

- **AC-1（开锁前移动联锁，拒绝开锁）**
  - **Given** 目标仓位处于"仓门已关闭，但光幕检测到残留产品"的异常状态，且按 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A 判定该 AGV 当前处于移动状态
  - **When** 系统准备下发重新开锁指令
  - **Then** 系统拒绝本次开门/开锁，不得下发开锁指令

- **AC-2（重新打开成功）**
  - **Given** 该 AGV 未在移动
  - **When** 系统向目标仓位下发开锁指令
  - **Then** 系统重新打开该仓位仓门，供操作员取出残留产品

- **AC-3（重新关闭光幕确认清空，恢复空闲并记录）**
  - **Given** 操作员重新关闭该仓位仓门后，光幕检测确认该仓位内确已清空
  - **When** 系统执行重新关闭后核验
  - **Then** 系统将该仓位状态恢复为 UC-010 预期的"空闲"；记录本次重新打开、取出残留及重新核验的过程（操作员、仓位号、时间戳）

- **AC-4（重新关闭后仍有残留，要求再次打开）**
  - **Given** 操作员重新关闭该仓位仓门后，光幕仍检测到产品残留
  - **When** 系统执行重新关闭后核验
  - **Then** 系统提示该仓位取出仍未完成并自动再次弹开仓门，重复 AC-2~AC-3，直至光幕确认已清空；不设强制放行次数上限，UNKNOWN 时暂停恢复

## Related 关联

- **Use Cases：** 支撑 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]]；由 [[uc-010-unload-completed-lot-at-destination-station|UC-010]] Exception Flow E4.1 转入触发；重新打开前依赖 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A；处理完毕、仓位恢复"空闲"后流程返回 UC-010 继续；相关任务的最终完成仍由 [[uc-002-confirm-task-completion|UC-002]] 触发，不在本 FR 范围内
- **Business Rules：** 无
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 重新打开、取出记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-038|TC-038]]：移动联锁拒绝开锁
- [[TC-039|TC-039]]：重新打开成功
- [[TC-040|TC-040]]：重新关闭光幕确认清空，恢复空闲并记录
- [[TC-041|TC-041]]：重新关闭后仍有残留，要求再次打开

## Notes 备注

- 本 FR 不区分首次还是多次重新打开：无论第几次检测到残留，均按 AC-2~AC-4 重复处理，直至光幕确认清空（见 UC-044 备选流程说明）。
- 若反复多次仍无法清空，操作员应上报班组长或设备/电气维护人员核实是否为光幕误报或产品卡滞等设备问题（见 UC-044 Exception Flow E6.1 第 4 步）；本 FR 不覆盖该上报后的具体处理机制。
- 本 FR 不与本批其他 FR（FR-010~FR-013）配对：UC-044 是独立的仓位处理场景，与 UC-043 会话生命周期的三段拆分不属于同一能力切片。
