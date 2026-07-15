---
id: FR-007
type: functional-requirement
title: "Task Cancellation Eligibility Check and State Rollback 任务取消资格核验与状态回滚"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-006"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-015", "TC-016", "TC-017"]
aliases: ["FR-007"]
---

# FR-007 Task Cancellation Eligibility Check and State Rollback 任务取消资格核验与状态回滚

## Description 需求描述

系统应当在操作员从待处理任务列表中选中某任务并点击"取消运送"后，核验该任务当前状态是否为"新建"或"进行中"（尚未完成、尚未取消），并核验该任务名下是否尚未有任何仓位处于"已占用"状态。两项核验均通过时，系统将该任务状态更新为"已取消"，并将其从该站点的待处理/可装载任务列表中移除，同时记录本次取消操作（操作员、任务、子批号、时间戳）；任一核验不通过时，系统必须拒绝本次取消请求并给出明确原因。

## Rationale 制定原因

允许操作员在装载开始前及时取消不再需要执行的任务，同时防止对已完成、已取消或已装载产品的任务发起取消，避免数据不一致或已装产品无人处理；将 [[uc-006-cancel-transport-task-upon-arrival|UC-006]] 的系统核验与状态转换能力收敛为可单独验收的切片。UC-006 本身流程简单、不涉及设备/硬件交互，因此不像 UC-001/UC-005/UC-010 那样拆成"核验"与"执行"两条 FR，单条 FR 即可完整覆盖。

## Origin 需求来源

- [[uc-006-cancel-transport-task-upon-arrival|UC-006]] Normal Flow 第 2.1、2.2、3、4 步及 Exception Flow E2.1、E2.2

## Acceptance Criteria 验收标准

- **AC-1（核验通过，取消并记录）**
  - **Given** 目标任务当前状态为"新建"或"进行中"，且该任务名下没有任何仓位处于"已占用"状态
  - **When** 操作员选中该任务并点击"取消运送"
  - **Then** 系统将该任务状态更新为"已取消"，从该站点待处理/可装载任务列表中移除，并记录本次取消操作（操作员、任务、子批号、时间戳）

- **AC-2（任务状态不满足条件，拒绝）**
  - **Given** 目标任务当前状态已是"已完成"或"已取消"
  - **When** 操作员点击"取消运送"
  - **Then** 系统拒绝本次取消请求，提示"该任务当前状态不可取消"，并刷新待处理任务列表

- **AC-3（任务已装载仓位，拒绝）**
  - **Given** 目标任务名下已有一个或多个仓位处于"已占用"状态
  - **When** 操作员点击"取消运送"
  - **Then** 系统拒绝本次取消请求，提示"该任务已装载产品，不能直接取消"

## Related 关联

- **Use Cases：** 派生自 [[uc-006-cancel-transport-task-upon-arrival|UC-006]]；与 AC-3 拒绝路径衔接的纠错动作见 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]（取出已装载产品后方可重新取消）
- **Business Rules：** 无
- **Functional Requirements：** 无（本 FR 独立成条，不与其他 FR 配对）
- **Non-Functional Requirements：** 核验通过与拒绝结果均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]] 的关键操作可审计要求

## Verification 验证方式

- [[TC-015|TC-015]]：核验通过，取消并记录
- [[TC-016|TC-016]]：任务状态不满足条件，拒绝
- [[TC-017|TC-017]]：任务已装载仓位，拒绝

## Notes 备注

- 本操作不需要班组长审批（见 UC-006 Precondition 备注）；取消结果不同步/回写给 MES，只在本地数据库处理。
- 取消不做物理删除，任务状态更新为"已取消（Cancelled）"，记录保留用于追溯。
- 若目标任务已装载部分/全部仓位，需先执行 [[fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback|FR-006]]（对应 UC-005）取出产品，待仓位恢复"空闲"后再重新发起本 FR。
