---
id: FR-027
type: functional-requirement
title: "AGV Enable/Disable State Transition and Pending-Effect Handling AGV 启用/禁用状态迁移与待生效处理"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-013"]
related_br: ["BR-002"]
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-082", "TC-083", "TC-084", "TC-085", "TC-086"]
aliases: ["FR-027"]
---

# FR-027 AGV Enable/Disable State Transition and Pending-Effect Handling AGV 启用/禁用状态迁移与待生效处理

## Description 需求描述

系统应当在管理员对某台 AGV 点击"禁用"时，核验其当前 RIOT 任务队列是否为空：为空则立即将该 AGV 状态置为"已禁用"；不为空则先置为"禁用待生效"，当前正在执行的任务不受影响，继续执行至完成或取消，队列重新变空后系统自动将其转为"已禁用"。管理员点击"启用"时，系统将处于"已禁用"或"禁用待生效"的该 AGV 恢复为其原本应有的正常状态，清除禁用相关标记。对已处于"已禁用"/"禁用待生效"状态重复点击"禁用"，或对非禁用状态点击"启用"，系统必须提示当前状态并忽略本次操作，不重复记录。每次实际生效的操作（操作人、AGV、操作类型、时间戳）均须记录到本地数据库。

## Rationale 制定原因

禁用是纯本地调度开关，只影响该 AGV 是否会被继续派发新任务，不应打断其当前正在执行的任务（无论是搬运还是充电）；"禁用待生效"这一过渡状态使操作既能立即生效于"不再接新任务"，又不需要人工二次确认当前任务何时结束。该状态是 [[br-002-agv-allocation-eligibility|BR-002]] 第 2 条"未处于已禁用/禁用待生效"这一硬性可分配条件的直接数据来源，也是 [[uc-008-dispatch-move-order-to-riot|UC-008]]、[[uc-012-manually-dispatch-agv-to-charge|UC-012]] Precondition 新增核验项的落地依据。

## Origin 需求来源

- [[uc-013-enable-disable-agv|UC-013]] Normal Flow 第 3~5 步、Exception Flow E3.1、E4.1、Postcondition

## Acceptance Criteria 验收标准

- **AC-1（禁用且队列为空，立即禁用）**
  - **Given** 管理员对一台当前非禁用状态的 AGV 点击"禁用"
  - **When** 系统核验该 AGV 当前 RIOT 任务队列为空
  - **Then** 系统立即将该 AGV 状态置为"已禁用"，记录操作人、AGV、操作类型、时间戳

- **AC-2（禁用且队列不为空，先禁用待生效再自动转为已禁用）**
  - **Given** 管理员对一台当前非禁用状态的 AGV 点击"禁用"，且该 AGV 当前 RIOT 任务队列不为空
  - **When** 系统核验队列非空，将该 AGV 状态置为"禁用待生效"；当前任务不受影响，继续执行至完成或取消，队列重新变空
  - **Then** 系统自动将该 AGV 状态转为"已禁用"，无需人工二次确认

- **AC-3（启用，恢复正常状态）**
  - **Given** 管理员对一台处于"已禁用"或"禁用待生效"的 AGV 点击"启用"
  - **When** 系统核验该 AGV 确实处于上述状态之一
  - **Then** 系统将该 AGV 状态恢复为其原本应有的正常状态，清除禁用相关标记，记录操作人、AGV、操作类型、时间戳

- **AC-4（重复点击禁用，忽略）**
  - **Given** 某台 AGV 已处于"已禁用"或"禁用待生效"状态
  - **When** 管理员再次点击"禁用"
  - **Then** 系统提示该 AGV 当前已处于禁用（或禁用待生效）状态，忽略本次重复操作，不重复记录

- **AC-5（对非禁用状态点击启用，忽略）**
  - **Given** 某台 AGV 当前处于正常（非禁用）状态
  - **When** 管理员点击"启用"
  - **Then** 系统提示该 AGV 当前无需启用，忽略本次操作，不重复记录

## Related 关联

- **Use Cases：** 支撑 [[uc-013-enable-disable-agv|UC-013]]；维护的启停状态被 [[uc-008-dispatch-move-order-to-riot|UC-008]]、[[uc-012-manually-dispatch-agv-to-charge|UC-012]] Precondition 核验，也被 [[uc-022-view-agv-fleet-and-availability|UC-022]] 展示
- **Business Rules：** 维护 [[br-002-agv-allocation-eligibility|BR-002]] 第 2 条依赖的启停状态数据
- **Functional Requirements：** 无强依赖
- **Non-Functional Requirements：** 操作记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]（[[uc-013-enable-disable-agv|UC-013]] Postcondition 4 明确要求记录用于追溯）

## Verification 验证方式

- [[tc-082-enable-disable-immediate-disable-empty-queue|TC-082]]：禁用且队列为空，立即禁用
- [[tc-083-enable-disable-pending-then-auto-disable|TC-083]]：禁用且队列不为空，先禁用待生效再自动转为已禁用
- [[tc-084-enable-disable-enable-restore-normal|TC-084]]：启用，恢复正常状态
- [[tc-085-enable-disable-repeat-disable-ignore|TC-085]]：重复点击禁用，忽略
- [[tc-086-enable-disable-invalid-enable-ignore|TC-086]]：对非禁用状态点击启用，忽略

## Notes 备注

- 本 FR 是纯本地调度开关，不调用 RIOT 接口对该 AGV 做设备级禁用/暂停/断电（见 UC-013 Assumption 第 1 条），"禁用"是否需要联动 RIOT 设备级禁用仍为 TBD，不在本 FR 范围内。
- 操作角色（`primary_actor`）范围是否需要从 AGV 运维/调度管理员扩展到班组长/生产管理者仍为 TBD（见 UC-013 Notes 待补充事项第 1 条），不影响本 FR 描述的核验与状态迁移逻辑本身。
- "RIOT 任务队列是否为空"具体走本地缓存记录还是即时查询 RIOT 接口仍为 TBD（见 UC-013 前置条件第 1 条），本 FR 不区分具体实现方式。
