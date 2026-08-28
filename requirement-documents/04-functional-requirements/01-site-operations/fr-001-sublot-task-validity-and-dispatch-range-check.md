---
id: FR-001
type: functional-requirement
title: "Sublot Task Validity and Dispatch Range Check 子批号任务有效性与派车范围核验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-001"]
related_br: ["BR-001"]
related_fr: ["FR-002"]
related_nfr: ["NFR-001", "NFR-002"]
related_tc: []
aliases: ["FR-001"]
---

# FR-001 Sublot Task Validity and Dispatch Range Check 子批号任务有效性与派车范围核验

## Description 需求描述

系统应当在站点装载流程中，根据操作员扫描或手动输入的子批号（SUBLOT），核验本地是否存在对应的、尚未完成且未被取消的搬运任务，并进一步核验该任务是否属于本次 AGV 派车所关联的任务范围（按 [[br-001-dispatch-task-range|BR-001]] 定义）。任一项核验失败时，系统必须拒绝继续分配仓位与开锁，并向操作员给出明确失败原因。

## Rationale 制定原因

防止错装、跨派车范围装载导致错送/混料；将 [[uc-001-load-completed-lot-into-slot|UC-001]] 中 1.1 / 1.2 系统核验点落实为可单独验收的系统能力，并强制执行 BR-001 的派车范围硬约束。

## Origin 需求来源

- [[uc-001-load-completed-lot-into-slot|UC-001]] Normal Flow 1.1、1.2 及 Exception Flow E1.1、E1.2
- [[br-001-dispatch-task-range|BR-001]]（本次派车任务范围的生成与判定）

## Acceptance Criteria 验收标准

- **AC-1（任务存在且有效）**
  - **Given** 本地数据库中存在子批号 S 对应的搬运任务，且状态既非 Done 也非 Cancelled；操作员已建立有效到站操作会话
  - **When** 操作员扫描或手动输入子批号 S
  - **Then** 系统判定“任务有效性”核验通过，并进入派车范围核验（不因输入方式是扫码或手动而改变核验规则）

- **AC-2（子批号无效：不存在 / 格式错误 / 已完成或已取消）**
  - **Given** 出现以下任一情况：本地查无子批号 S；手动输入格式非法；或 S 对应任务状态为 Done / Cancelled
  - **When** 操作员提交子批号 S
  - **Then** 系统拒绝继续装载（不分配仓位、不下发开锁），并提示“子批号不存在、格式错误，或对应任务已完成/已取消”类明确原因

- **AC-3（属于本次派车范围）**
  - **Given** 子批号 S 对应有效任务 T，且 T 属于当前 AGV 本次派车任务范围（允许 T 的目标站点与操作员当前物理站点不完全相同，只要 T 在范围内）
  - **When** 系统执行派车范围核验
  - **Then** 核验通过，允许进入后续空闲仓位分配与开锁流程

- **AC-4（不属于本次派车范围）**
  - **Given** 子批号 S 对应有效任务 T，但 T 不属于当前 AGV 本次派车任务范围
  - **When** 系统执行派车范围核验
  - **Then** 系统拒绝为该子批号分配仓位与开锁，并提示核验不通过（任务不在本次派车范围）

## Related 关联

- **Use Cases：** 派生自 [[uc-001-load-completed-lot-into-slot|UC-001]]（装载扫码/手输核验）；不覆盖 UC-001 的开锁、光幕与落库能力（见 FR-002）
- **Business Rules：** 强制落实 [[br-001-dispatch-task-range|BR-001]]
- **Functional Requirements：** 核验通过后由 [[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] 承接开锁与占位确认
- **Non-Functional Requirements：** 核验能力本身依赖 [[nfr-001-service-availability|NFR-001]] 约束的业务服务可用性；核验结果与拒绝原因须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]] 的关键操作可审计要求（具体审计字段以 NFR/后续审计 FR 为准）

## Verification 验证方式

对应 Test Case 待建。建议至少覆盖：有效任务通过、查无/格式错误/Done/Cancelled 拒绝、范围内邻站任务通过、范围外任务拒绝。验证策略：功能测试 + 用例走查。

## Notes 备注

- 本 FR **不**重复核验 MES 工序/任务类型与 moveType 匹配；该校验由任务同步阶段（见 [[uc-007-sync-transport-task-from-mes|UC-007]]）完成。本 FR 只核验本地任务是否仍有效，以及是否属于本次派车范围。
- “本次派车任务范围”的生成与维护细节以 BR-001 为准；本 FR 只要求系统按该规则做 fail-closed 判定。
- `related_tc` 暂空，待 `05-test-cases` 补录后回填。
