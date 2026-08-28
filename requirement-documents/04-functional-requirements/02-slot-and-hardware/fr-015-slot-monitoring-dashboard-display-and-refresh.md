---
id: FR-015
type: functional-requirement
title: "Slot Monitoring Dashboard Display and Refresh 仓位监控看板展示与刷新"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-011"]
related_br: []
related_fr: []
related_nfr: []
related_tc: ["TC-042", "TC-043"]
aliases: ["FR-015"]
---

# FR-015 Slot Monitoring Dashboard Display and Refresh 仓位监控看板展示与刷新

## Description 需求描述

系统应当在班组长/生产管理者打开仓位监控看板界面时，读取本地数据库中各多仓位 AGV 全部仓位的最新状态记录，按 AGV/仓位号展示仓位状态（空闲/已占用/异常锁定）、仓门开关状态，以及"已占用"仓位关联的子批号与搬运任务信息（任务号、目标/交货站点、任务当前状态）；并按预设周期自动刷新或支持手动刷新。刷新时若数据读取异常，系统必须保留上一次成功读取到的数据并标注最后刷新时间，不得因读取失败而清空或展示过期未标注的数据。

## Rationale 制定原因

将 [[uc-011-view-slot-monitoring-dashboard|UC-011]] 描述的只读展示与定时/手动刷新能力落实为可单独验收的能力切片，保证班组长/生产管理者能够依据看板数据做出准确的现场管理决策（如判断是否有仓位长时间"异常锁定"、协调装卸进度），同时避免刷新异常时误导为"最新真实状态"。

## Origin 需求来源

- [[uc-011-view-slot-monitoring-dashboard|UC-011]] Normal Flow 第 1~4 步、Postcondition 第 1 条及 Exception Flow E3.1

## Acceptance Criteria 验收标准

- **AC-1（正常展示仓位状态与关联信息）**
  - **Given** 本地服务器与数据库运行正常
  - **When** 班组长/生产管理者打开仓位监控看板，或看板按周期/手动触发刷新
  - **Then** 系统读取并展示各仓位状态（空闲/已占用/异常锁定）、仓门开关状态；若某仓位为"已占用"，同时展示其关联的子批号及搬运任务信息（任务号、目标/交货站点、任务当前状态），与本地数据库当前记录一致

- **AC-2（刷新时数据读取异常，保留旧数据并标注）**
  - **Given** 看板已展示上一次成功读取到的数据
  - **When** 系统按周期或手动触发刷新时，读取本地数据库/服务发生异常
  - **Then** 系统提示"数据刷新失败，请稍后重试"，保留上一次成功读取到的数据，并标注该数据的最后刷新时间，不得与最新真实状态混淆；系统持续尝试重新读取

## Related 关联

- **Use Cases：** 支撑 [[uc-011-view-slot-monitoring-dashboard|UC-011]]；展示内容来源于 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-006-cancel-transport-task-upon-arrival|UC-006]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 等业务 UC 产生的仓位/任务状态变化，本 FR 只负责如实展示，不改变、不核验其业务合法性
- **Business Rules：** 无
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 无（见下方 Notes 说明）

## Verification 验证方式

- [[TC-042|TC-042]]：正常展示仓位状态与关联信息
- [[TC-043|TC-043]]：刷新时数据读取异常，保留旧数据并标注

## Notes 备注

- 本 FR 不登记 `related_nfr`：[[uc-011-view-slot-monitoring-dashboard|UC-011]] 是纯只读查询，不改变任何仓位/任务状态，Postcondition 未要求记录审计，与 [[fr-010-arrival-status-update-and-operation-panel-navigation|FR-010]] 的既定处理方式一致，不强行附加 NFR-002。
- 本 FR 不与本批其他 FR（FR-016）配对：看板展示与仓位启用/禁用是两个独立的能力，仅存在"展示"与"被展示对象状态变化"的间接关系，不属于同一能力切片的拆分。
- 具体展示字段最终清单、UI 布局、自动刷新周期、可见范围（是否按车间/产线过滤）等细节仍为 TBD，见 UC-011 Notes。
