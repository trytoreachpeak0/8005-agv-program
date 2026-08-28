---
id: FR-023
type: functional-requirement
title: "Slot Model Publish with Dual Authentication and Immutable Versioning 型号发布二次认证与不可变版本生成"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-038"]
related_br: ["BR-008"]
related_fr: ["FR-022", "FR-024"]
related_nfr: ["NFR-002"]
related_tc: ["TC-069", "TC-070", "TC-071", "TC-072"]
aliases: ["FR-023"]
---

# FR-023 Slot Model Publish with Dual Authentication and Immutable Versioning 型号发布二次认证与不可变版本生成

## Description 需求描述

系统应当在操作人员对一个已通过 [[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] 格式校验、且仓位规格已填写完整的 `Draft` 版本发起发布时，先要求填写发布原因并展示与该型号上一个 `Published` 版本的差异（面、仓位新增/删除/位置或规格变化），再要求操作人员再次刷卡或认证；认证通过后，系统必须以原子事务生成新的、内容不可变的 `Published` 版本（含稳定 `modelId`、单调递增 `version`、全局唯一 `modelVersionId`、面列表、仓位定义、发布时间、发布人、内容校验值），并记录审计。仓位规格仍缺失或不合法、二次认证失败，或发布事务任一环节（持久化、状态转换、内容校验值、审计写入）失败，系统必须拒绝发布并保持原状态不变，不产生部分可用的新版本。

## Rationale 制定原因

发布是[[br-008-agv-slot-model-versioning|BR-008]]定义的高风险操作——一旦发布，面、仓位编号、位置、跨格及规格均不可再原地修改，且新版本会成为之后 AGV 接入时可选用并被永久绑定为快照的依据（见 [[uc-019-register-agv-from-rcs|UC-019]]）。要求二次认证与发布前差异展示，是为了防止误操作或未授权人员产生一个内容有误却已"钉死"的版本；要求原子事务与规格完整性前置校验，是为了避免出现"AGV 后续绑定了一个仓位定义不完整的版本"这类无法挽回的数据问题。

## Origin 需求来源

- [[uc-038-maintain-agv-slot-model|UC-038]] Normal Flow 第 7~9 步、Exception Flow E5.4、E8.1、E9.1
- [[br-008-agv-slot-model-versioning|BR-008]] 第 2、5 条

## Acceptance Criteria 验收标准

- **AC-1（规格完整、认证通过，原子生成不可变新版本）**
  - **Given** 目标 `Draft` 已通过格式校验且仓位规格填写完整，操作人员已填写发布原因并查看与上一 `Published` 版本的差异
  - **When** 操作人员再次刷卡或认证成功
  - **Then** 系统以原子事务生成新的不可变 `Published` 版本（含 `modelId`、单调递增 `version`、全局唯一 `modelVersionId`、面与仓位定义、发布时间、发布人、内容校验值），记录审计

- **AC-2（仓位规格仍缺失或不合法，拒绝发布）**
  - **Given** 目标 `Draft` 中存在仓位的尺寸或最大载重未填写，或数值不合法
  - **When** 操作人员发起发布
  - **Then** 系统拒绝发布，提示具体缺失或不合法的字段，`Draft` 状态保持不变

- **AC-3（二次认证失败，不发布）**
  - **Given** 操作人员已提交发布请求
  - **When** 再次刷卡或认证失败、超时、身份与当前操作人不一致，或权限不足
  - **Then** 系统不生成新版本，保留原 `Draft` 状态，记录失败审计

- **AC-4（发布事务失败，整体回滚）**
  - **Given** 二次认证已通过
  - **When** 版本持久化、状态转换、内容校验值计算或审计写入任一环节失败
  - **Then** 系统回滚整个操作，不产生新版本或部分状态变更，并提示稍后重试

## Related 关联

- **Use Cases：** 支撑 [[uc-038-maintain-agv-slot-model|UC-038]] 发布环节；生成的 `Published` 版本是 [[uc-019-register-agv-from-rcs|UC-019]] 接入 AGV 时可选用并绑定快照的来源
- **Business Rules：** 落实 [[br-008-agv-slot-model-versioning|BR-008]] 第 2 条（发布不可变版本）、第 5 条（发布二次认证）
- **Functional Requirements：** 依赖 [[fr-022-slot-model-draft-field-and-layout-validation|FR-022]] 完成的草稿格式校验与规格完整性标记；发布后的版本可被 [[fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation|FR-024]] 停用，二者共同构成 UC-038 高风险操作链
- **Non-Functional Requirements：** 发布操作与结果须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]（[[uc-038-maintain-agv-slot-model|UC-038]] Postcondition 4 明确要求审计）

## Verification 验证方式

- [[tc-069-publish-success-immutable-version|TC-069]]：规格完整、认证通过，原子生成不可变新版本
- [[tc-070-publish-incomplete-spec-reject|TC-070]]：仓位规格仍缺失或不合法，拒绝发布
- [[tc-071-publish-dual-auth-fail-reject|TC-071]]：二次认证失败，不发布
- [[tc-072-publish-transaction-fail-rollback|TC-072]]：发布事务失败，整体回滚

## Notes 备注

- 新发布版本只影响其发布时间之后、尚未接入的 AGV 通过 UC-019 新接入时的可选范围；已接入 AGV 继续使用原快照，不受新版本影响（见 [[br-008-agv-slot-model-versioning|BR-008]] 第 4 条），本 FR 不覆盖该影响范围的具体验证，留给 [[fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging|FR-026]] 覆盖"接入时按快照生成仓位实例"的部分。
- 版本号不得重用，发布失败也不得覆盖另一个已成功发布的版本（BR-008 第 2 条第 5 点），AC-4 的回滚语义已隐含此约束，本 FR 不单独拆 AC 覆盖"版本号冲突"这一实现细节。
