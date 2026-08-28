---
id: FR-018
type: functional-requirement
title: "Slot Light Curtain Function Test 仓位光幕功能测试"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-016"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-051", "TC-052", "TC-053", "TC-054"]
aliases: ["FR-018"]
---

# FR-018 Slot Light Curtain Function Test 仓位光幕功能测试

## Description 需求描述

系统应当在目标仓位仓门已开启的前提下，依次核验光幕状态在三个阶段是否与实际一致：测试开始前应为"无遮挡"；维护人员放入测试物体或用手遮挡后应变为"有遮挡"；移除测试物体/遮挡后应恢复"无遮挡"。三个阶段均核验通过，系统记录本次测试结果为"正常"；任一阶段核验不通过，系统必须将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，并记录本次测试结果为"异常"。

## Rationale 制定原因

将 [[uc-016-slot-light-curtain-function-test|UC-016]] 描述的光幕传感器"有/无遮挡"基础通断功能验证能力落实为可单独验收的能力切片，确保光幕硬件基础能力异常时能够被及时发现并阻止业务误用，避免影响 [[uc-001-load-completed-lot-into-slot|UC-001]]/[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]/[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 等业务流程依赖光幕核验的准确性。

## Origin 需求来源

- [[uc-016-slot-light-curtain-function-test|UC-016]] Normal Flow 第 2~7 步、Postcondition、Exception Flow E2.1、E4.1、E6.1

## Acceptance Criteria 验收标准

- **AC-1（测试开始前光幕状态异常）**
  - **Given** 目标仓位仓门已开启，仓位内实际为空
  - **When** 系统读取该仓位光幕状态显示为"有遮挡"，且清空仓位后仍显示"有遮挡"
  - **Then** 系统判定该仓位光幕异常，标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"

- **AC-2（三阶段核验均通过，记录正常）**
  - **Given** 目标仓位仓门已开启，测试开始前光幕状态确为"无遮挡"
  - **When** 维护人员依次放入测试物体/遮挡光幕、再移除测试物体/遮挡，系统分别读取到光幕状态正确变为"有遮挡"、再恢复"无遮挡"
  - **Then** 系统记录本次测试结果为"正常"（维护人员、仓位号、时间戳）

- **AC-3（遮挡后光幕仍显示无遮挡，标记异常）**
  - **Given** 测试开始前光幕状态核验通过（"无遮挡"）
  - **When** 维护人员放入测试物体/遮挡光幕后，系统读取的光幕状态仍显示"无遮挡"
  - **Then** 系统判定该仓位光幕异常（检测不到遮挡），标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"

- **AC-4（移除遮挡后光幕仍显示有遮挡，标记异常）**
  - **Given** 遮挡阶段核验通过（光幕已正确变为"有遮挡"）
  - **When** 维护人员移除测试物体/遮挡后，系统读取的光幕状态仍显示"有遮挡"
  - **Then** 系统判定该仓位光幕异常（无法恢复检测为无遮挡），标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"

## Related 关联

- **Use Cases：** 支撑 [[uc-016-slot-light-curtain-function-test|UC-016]]；测试前提（仓门已开启）由 [[uc-015-slot-door-unlock-open-test|UC-015]] 的开门操作提供
- **Business Rules：** 无
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 测试结果记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-051|TC-051]]：测试开始前光幕状态异常
- [[TC-052|TC-052]]：三阶段核验均通过，记录正常
- [[TC-053|TC-053]]：遮挡后光幕仍显示无遮挡，标记异常
- [[TC-054|TC-054]]：移除遮挡后光幕仍显示有遮挡，标记异常

## Notes 备注

- 本 FR 不验证光幕的检测精度/灵敏度（如能否检测极小遮挡物），只验证"有/无明显遮挡"两种典型场景下的基础通断功能是否正常（见 UC-016 Assumption 第 2 条）。
- 本 FR 不与本批其他 FR（FR-017、FR-019）建立 `related_fr` 强依赖，理由见 FR-017 Notes。
- 测试使用的"测试物体"由维护人员自行准备，本 FR 不规定具体物体的规格（见 UC-016 Assumption 第 1 条）。
