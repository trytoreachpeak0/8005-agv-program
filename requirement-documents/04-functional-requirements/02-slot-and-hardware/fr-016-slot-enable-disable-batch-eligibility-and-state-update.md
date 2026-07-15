---
id: FR-016
type: functional-requirement
title: "Slot Enable/Disable Batch Eligibility and State Update 仓位启用/禁用批量核验与状态更新"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-014"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-044", "TC-045", "TC-046", "TC-047"]
aliases: ["FR-016"]
---

# FR-016 Slot Enable/Disable Batch Eligibility and State Update 仓位启用/禁用批量核验与状态更新

## Description 需求描述

系统应当在操作人员选中一个或多个仓位并点击"禁用"或"启用"按钮后，对每个被选中的仓位分别核验其当前状态是否满足条件：点击"禁用"时须为"空闲（Idle）"，点击"启用"时须为"已禁用（Disabled）"。核验通过的仓位分别更新为"已禁用"或恢复为"空闲（Idle）"；核验不通过的仓位跳过、不做改变，且不影响本次请求中其余仓位的处理。系统必须记录本次操作（操作人、涉及仓位清单及各自处理结果、操作类型：禁用/启用、时间戳），并在界面汇总展示成功与被跳过的仓位及原因。

## Rationale 制定原因

将 [[uc-014-enable-disable-slot|UC-014]] 中"禁用后不再被业务分配、仅允许对空闲仓位禁用、批量请求中单个仓位异常不影响其余仓位"的系统核验与状态迁移能力落实为可单独验收的能力切片，保证禁用/启用操作不会破坏正在进行中的装卸业务数据一致性。

## Origin 需求来源

- [[uc-014-enable-disable-slot|UC-014]] Precondition 第 2、3 条、Normal Flow 第 1~6 步、Postcondition、Exception Flow E3.1、E4.1

## Acceptance Criteria 验收标准

- **AC-1（禁用核验通过，状态更新）**
  - **Given** 目标仓位当前状态为"空闲（Idle）"
  - **When** 操作人员点击"禁用"
  - **Then** 系统将该仓位状态置为"已禁用（Disabled）"，不再出现在 [[uc-001-load-completed-lot-into-slot|UC-001]] 分配空闲仓位时的可选范围内

- **AC-2（禁用核验不通过，跳过）**
  - **Given** 目标仓位当前状态为"已占用（Occupied）"或"异常锁定"
  - **When** 操作人员点击"禁用"
  - **Then** 系统跳过该仓位的禁用操作，提示"禁用失败：当前非空闲状态"；本次请求中其余满足条件的仓位不受影响，仍按计划继续禁用

- **AC-3（启用核验通过，状态更新）**
  - **Given** 目标仓位当前状态为"已禁用（Disabled）"
  - **When** 操作人员点击"启用"
  - **Then** 系统将该仓位状态恢复为"空闲（Idle）"，清除禁用标记，重新可被 UC-001 分配使用

- **AC-4（启用核验不通过，跳过）**
  - **Given** 目标仓位当前并非"已禁用"状态
  - **When** 操作人员点击"启用"
  - **Then** 系统跳过该仓位的启用操作，提示"无需启用：当前并非禁用状态"；本次请求中其余满足条件的仓位不受影响，仍按计划继续启用

## Related 关联

- **Use Cases：** 支撑 [[uc-014-enable-disable-slot|UC-014]]；本 FR 维护的"已禁用"状态是 [[uc-001-load-completed-lot-into-slot|UC-001]] 分配空闲仓位时的排除条件
- **Business Rules：** 无
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 禁用/启用操作及批量处理结果均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-044|TC-044]]：禁用核验通过，状态更新
- [[TC-045|TC-045]]：禁用核验不通过，跳过
- [[TC-046|TC-046]]：启用核验通过，状态更新
- [[TC-047|TC-047]]：启用核验不通过，跳过

## Notes 备注

- 本 FR 以"每个被选中的仓位"为最小核验单位：批量请求中各仓位独立核验、独立处理，一个仓位的跳过不影响其他仓位，写法参照 [[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]] 对批量场景中单个异常不阻塞整体的处理方式。
- 本 FR 不涉及对仓位电子锁/光幕等硬件的禁用操作，也不联动 RIOT，是纯本地系统层面的调度开关（见 UC-014 Assumption 第 1 条）。
- 禁用/启用操作角色（`primary_actor`）本次未最终确定，见 UC-014 Notes 待补充事项，不影响本 FR 的核验与状态迁移逻辑本身。
