---
id: FR-013
type: functional-requirement
title: "Session Termination Rules 会话结束规则与锁定期强制约束"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-043", "UC-002", "UC-006"]
related_br: []
related_fr: ["FR-011", "FR-012"]
related_nfr: ["NFR-002"]
related_tc: ["TC-034", "TC-035", "TC-036", "TC-037"]
aliases: ["FR-013"]
---

# FR-013 Session Termination Rules 会话结束规则与锁定期强制约束

## Description 需求描述

系统应当保证操作会话仅通过以下两种方式结束：会话处于"未开始仓门操作"阶段时，由操作员主动提前结束；会话已进入"仓门操作已锁定"阶段后，仅能通过操作员完成 [[uc-002-confirm-task-completion|UC-002]] 确认完成结束。[[uc-006-cancel-transport-task-upon-arrival|UC-006]] 取消运送无论在会话哪个阶段执行，都不得结束或改变会话状态。会话已进入锁定阶段后，若操作员尝试手动结束，系统必须拒绝该请求。

## Rationale 制定原因

落实"同一次到站装卸应由同一操作员完成始终、不支持中途换人"的业务要求，同时保留"尚未开始装卸时可换人重新核验"的灵活性；明确 [[uc-006-cancel-transport-task-upon-arrival|UC-006]] 不影响会话状态，避免取消操作被误用为绕过锁定的结束方式。

## Origin 需求来源

- [[uc-043-verify-identity-and-manage-operation-session|UC-043]] Normal Flow 第 6、7、8 步、Postcondition 第 4~6 条、Alternative Flow A6.1、Exception Flow EA6.2

## Acceptance Criteria 验收标准

- **AC-1（UC-006 取消不影响会话）**
  - **Given** 操作员在会话内任意阶段执行 [[uc-006-cancel-transport-task-upon-arrival|UC-006]] 取消运送
  - **When** UC-006 处理完成
  - **Then** 会话阶段与有效性均不受影响，不因此结束或改变会话状态

- **AC-2（完成 UC-002 正常结束会话）**
  - **Given** 会话处于"仓门操作已锁定"阶段
  - **When** 操作员完成 [[uc-002-confirm-task-completion|UC-002]] 确认完成
  - **Then** 系统结束当前会话，记录结束时间及结束方式（"UC-002 确认完成"），界面恢复为"未验证"状态

- **AC-3（未锁定阶段主动提前结束）**
  - **Given** 会话仍处于"未开始仓门操作"阶段
  - **When** 操作员点击"结束会话"（该操作不要求核验身份，终端前任何人均可执行）
  - **Then** 系统结束当前会话，记录结束时间及结束方式（"操作员主动提前结束"），界面恢复为"未验证"状态

- **AC-4（锁定阶段拒绝手动结束）**
  - **Given** 会话已处于"仓门操作已锁定"阶段
  - **When** 操作员尝试点击"结束会话"
  - **Then** 系统拒绝该请求，提示"本次到站操作已开始，必须先完成 UC-002 确认完成才能结束会话"

## Related 关联

- **Use Cases：** 支撑 [[uc-043-verify-identity-and-manage-operation-session|UC-043]]；正常结束依赖 [[uc-002-confirm-task-completion|UC-002]] 确认完成；[[uc-006-cancel-transport-task-upon-arrival|UC-006]] 不影响会话状态
- **Business Rules：** 无
- **Functional Requirements：** 依赖 [[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] 建立与维护的会话阶段；与 [[fr-011-identity-and-role-verification-via-mes|FR-011]] 共同构成 UC-043 会话生命周期的三段拆分（核验 / 建立复用与锁定迁移 / 结束规则）
- **Non-Functional Requirements：** 会话正常结束与拒绝结束均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-034|TC-034]]：UC-006 取消不影响会话
- [[TC-035|TC-035]]：完成 UC-002 正常结束会话
- [[TC-036|TC-036]]：未锁定阶段主动提前结束
- [[TC-037|TC-037]]：锁定阶段拒绝手动结束

## Notes 备注

- 未锁定阶段的"结束会话"本身不核验身份，终端前任何人均可执行；顶替场景通过"他人先结束会话、再由新人核验身份"两步实现，不设计单独的强制顶替入口（见 UC-043 Assumption 第 2 条）。
- 本 FR 不处理"结束会话后重新核验、建立新会话"的具体过程，该过程由 [[fr-011-identity-and-role-verification-via-mes|FR-011]]、[[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] 覆盖。
