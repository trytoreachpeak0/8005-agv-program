---
id: FR-024
type: functional-requirement
title: "Slot Model Retire with Dual Authentication and Historical Reference Preservation 型号停用二次认证与历史引用保留"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-038"]
related_br: ["BR-008"]
related_fr: ["FR-023"]
related_nfr: ["NFR-002"]
related_tc: ["TC-073", "TC-074", "TC-075"]
aliases: ["FR-024"]
---

# FR-024 Slot Model Retire with Dual Authentication and Historical Reference Preservation 型号停用二次认证与历史引用保留

## Description 需求描述

系统应当在操作人员对一个 `Published` 版本发起停用时，先要求填写非空停用原因并展示当前引用该版本的 AGV 数量及清单，再要求操作人员再次刷卡或认证；认证通过后，系统必须以原子操作将该版本置为 `Retired`，使其不再允许被 [[uc-019-register-agv-from-rcs|UC-019]] 选用于新接入，同时保证已引用该版本的历史 AGV 及其仓位实例继续有效、不受影响，并记录审计。二次认证失败，或停用操作任一环节（状态转换、审计写入）失败时，系统必须拒绝停用并保持原 `Published` 状态不变。

## Rationale 制定原因

停用与发布同属 [[br-008-agv-slot-model-versioning|BR-008]] 定义的高风险操作，需要同等强度的二次认证与审计（第 5 条）。停用只应影响"之后能否被选用于新接入"，绝不能影响已经绑定该版本快照的历史 AGV（第 4 条）——展示引用清单并明确告知"历史引用不会被修改或失效"，是为了让操作人员在停用前清楚该操作的实际影响范围，避免误以为停用会连带处理这些历史车辆。

## Origin 需求来源

- [[uc-038-maintain-agv-slot-model|UC-038]] Alternative Flow A1.1、Exception Flow E8.1、E9.1
- [[br-008-agv-slot-model-versioning|BR-008]] 第 4、5 条

## Acceptance Criteria 验收标准

- **AC-1（认证通过，原子停用且历史引用不受影响）**
  - **Given** 操作人员已为某个 `Published` 版本填写非空停用原因，并已查看当前引用该版本的 AGV 数量及清单
  - **When** 操作人员再次刷卡或认证成功
  - **Then** 系统原子地将该版本置为 `Retired`，记录审计；该版本不再允许被 UC-019 选用于新接入，已引用该版本的历史 AGV 及其仓位实例保持不变、继续有效

- **AC-2（二次认证失败，不停用）**
  - **Given** 操作人员已提交停用请求
  - **When** 再次刷卡或认证失败、超时、身份与当前操作人不一致，或权限不足
  - **Then** 系统不停用，保留原 `Published` 状态，记录失败审计

- **AC-3（停用事务失败，回滚）**
  - **Given** 二次认证已通过
  - **When** 状态转换或审计写入任一环节失败
  - **Then** 系统回滚整个操作，不产生部分状态变更，并提示稍后重试

## Related 关联

- **Use Cases：** 支撑 [[uc-038-maintain-agv-slot-model|UC-038]] 停用环节
- **Business Rules：** 落实 [[br-008-agv-slot-model-versioning|BR-008]] 第 4 条（新版本影响范围与历史保留）、第 5 条（停用二次认证）
- **Functional Requirements：** 停用的目标版本来自 [[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]] 已生成的 `Published` 版本
- **Non-Functional Requirements：** 停用操作与结果须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]（[[uc-038-maintain-agv-slot-model|UC-038]] Postcondition 4 明确要求审计）

## Verification 验证方式

- [[tc-073-retire-success-historical-refs-unaffected|TC-073]]：认证通过，原子停用且历史引用不受影响
- [[tc-074-retire-dual-auth-fail-reject|TC-074]]：二次认证失败，不停用
- [[tc-075-retire-transaction-fail-rollback|TC-075]]：停用事务失败，回滚

## Notes 备注

- 本 FR 不覆盖"已归档车辆的恢复""Retired 版本重新启用"等场景——[[br-008-agv-slot-model-versioning|BR-008]] 第 1 条明确不允许 `Retired` 退回 `Published`/`Draft`，因此不存在对应的正向 AC。
- 停用不产生物理删除，`Published`/`Retired` 版本及曾被引用的 `Draft` 均不得物理删除（BR-008 第 6 条），本 FR 的 AC 均以"状态转换"而非"删除"描述，与该约束一致。
