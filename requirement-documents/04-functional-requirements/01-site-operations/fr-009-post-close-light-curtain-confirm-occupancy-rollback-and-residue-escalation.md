---
id: FR-009
type: functional-requirement
title: "Post-Close Light Curtain Confirm, Occupancy Rollback and Residue Escalation 关门光幕清空核验、占位回滚与残留转异常处理"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-010", "UC-044"]
related_br: ["BR-013"]
related_fr: ["FR-008"]
related_nfr: ["NFR-002"]
related_tc: ["TC-023", "TC-024"]
aliases: ["FR-009"]
---

# FR-009 Post-Close Light Curtain Confirm, Occupancy Rollback and Residue Escalation 关门光幕清空核验、占位回滚与残留转异常处理

## Description 需求描述

系统应当在操作员关闭 [[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]] 识别并开锁的仓位后，依据光幕检测确认该仓位内确实已清空；确认清空时，将该仓位状态由"已占用"变为"空闲"、清除仓位—子批号映射关系，并记录本次取出操作（操作员、子批号、仓位号、站点、时间戳），任务状态保持"进行中"（不因本 FR 自动变为完成）。若关门后光幕仍检测到产品残留，系统不得将该仓位回滚为"空闲"，须转 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 处理。

## Rationale 制定原因

保证终点站取出结果与现场实物、追溯数据一致；任务不因关门+光幕核验自动完成，是因为同一站点可能同时是"存料站点"和"取料站点"，操作员可能还需继续装载其他任务才算完成本次到站（最终完成统一由 [[uc-002-confirm-task-completion|UC-002]] 触发）。

## Origin 需求来源

- [[uc-010-unload-completed-lot-at-destination-station|UC-010]] Normal Flow 第 4、4.1 步、Postcondition 及 Exception Flow E4.1
- [[br-013-multi-basket-loading|BR-013]]（按仓位/装载明细区分卸货关门与占用更新）

## Acceptance Criteria 验收标准

- **AC-1（关门后光幕确认清空，回滚成功并记录）**
  - **Given** 操作员已关闭目标仓位仓门，光幕检测确认该仓位内确实已清空
  - **When** 系统执行关门后核验
  - **Then** 该仓位状态由"已占用"变为"空闲"，清除仓位—子批号映射关系；记录本次取出操作（操作员、子批号、仓位号、站点、时间戳）；关联任务状态保持"进行中"

- **AC-2（关门后光幕检测残留，转 UC-044）**
  - **Given** 操作员已关闭目标仓位仓门，但光幕仍检测到产品残留
  - **When** 系统执行关门后核验
  - **Then** 系统不得将该仓位回滚为"空闲"，转 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 处理；直至 UC-044 处理完毕、仓位恢复"空闲"后，才允许按 AC-1 记录取出结果

## Related 关联

- **Use Cases：** 支撑 [[uc-010-unload-completed-lot-at-destination-station|UC-010]]；残留场景转 [[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]]；任务最终完成由 [[uc-002-confirm-task-completion|UC-002]] 触发，不在本 FR 范围内
- **Business Rules：** 遵循 [[br-013-multi-basket-loading|BR-013]]
- **Functional Requirements：** 前置识别与开锁依赖 [[fr-008-destination-station-auto-identify-and-batch-unlock|FR-008]]
- **Non-Functional Requirements：** 占位回滚与取出记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-023|TC-023]]：关门后光幕确认清空，回滚成功并记录
- [[TC-024|TC-024]]：关门后光幕检测残留，转 UC-044

## Notes 备注

- 若本次到站还有其他待取料仓位，操作员对每个仓位重复本 FR 的关门核验流程，逐个处理（见 UC-010 Normal Flow 第 5 步）；本 FR 描述的是单个仓位的关门核验能力。
- 确认完成前发现拿错/漏拿如何纠错仍是 UC-010 的 TBD 事项，本 FR 不覆盖。
