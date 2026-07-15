---
id: FR-012
type: functional-requirement
title: "Session Establishment, Reuse and Lock-Stage Transition 会话建立、跨操作复用与锁定阶段迁移"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-043", "UC-001", "UC-005", "UC-010", "UC-044"]
related_br: []
related_fr: ["FR-011", "FR-013"]
related_nfr: ["NFR-002"]
related_tc: ["TC-031", "TC-032", "TC-033"]
aliases: ["FR-012"]
---

# FR-012 Session Establishment, Reuse and Lock-Stage Transition 会话建立、跨操作复用与锁定阶段迁移

## Description 需求描述

系统应当在 [[fr-011-identity-and-role-verification-via-mes|FR-011]] 核验通过后，建立与本次到站绑定的操作会话，记录操作人身份（工号/姓名）、AGV、站点及会话开始时间，初始处于"未开始仓门操作"阶段。会话有效期内，操作员执行 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]]、[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 等仓门操作时，系统须复用该会话，不需要重复验证身份，但各操作记录均须关联当前会话的操作人身份。会话内首次发生仓门打开动作后，系统须将会话状态由"未开始仓门操作"更新为"仓门操作已锁定"。

## Rationale 制定原因

避免同一次到站内每次装卸操作都重复核验身份，同时通过"锁定阶段"机制保证一旦开始装卸就不允许中途换人，落实"同一次到站的装卸操作应由同一人完成始终"的业务要求；是 [[uc-001-load-completed-lot-into-slot|UC-001]]/[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]/[[uc-010-unload-completed-lot-at-destination-station|UC-010]]/[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 等仓门操作类 FR 记录操作人身份时依赖的公共能力。

## Origin 需求来源

- [[uc-043-verify-identity-and-manage-operation-session|UC-043]] Normal Flow 第 3、4、5、5.1 步、Postcondition 第 1~3 条

## Acceptance Criteria 验收标准

- **AC-1（核验通过后建立会话，未开始仓门操作阶段）**
  - **Given** [[fr-011-identity-and-role-verification-via-mes|FR-011]] 核验已通过
  - **When** 系统建立本次到站绑定的操作会话
  - **Then** 系统记录操作人身份、AGV、站点及会话开始时间，会话初始处于"未开始仓门操作"阶段；界面显示当前已验证的操作人身份，允许后续操作

- **AC-2（会话内复用，不重复验证身份）**
  - **Given** 当前站点/终端存在有效操作会话
  - **When** 操作员在会话内执行一次或多次 [[uc-001-load-completed-lot-into-slot|UC-001]]/[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]/[[uc-010-unload-completed-lot-at-destination-station|UC-010]]/[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 等仓门操作
  - **Then** 系统复用当前会话，不要求重复验证身份，但该操作记录须关联当前会话的操作人身份

- **AC-3（首次仓门操作触发锁定阶段）**
  - **Given** 当前会话处于"未开始仓门操作"阶段
  - **When** 会话内发生首次仓门打开动作
  - **Then** 系统将该会话状态更新为"仓门操作已锁定"

## Related 关联

- **Use Cases：** 支撑 [[uc-043-verify-identity-and-manage-operation-session|UC-043]]；被 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]]、[[uc-044-reopen-slot-after-incomplete-retrieval|UC-044]] 的仓门操作复用，作为其记录操作人身份的依据
- **Business Rules：** 无
- **Functional Requirements：** 依赖 [[fr-011-identity-and-role-verification-via-mes|FR-011]] 完成的身份核验；会话结束规则见 [[fr-013-session-termination-rules|FR-013]]
- **Non-Functional Requirements：** 会话建立、复用及阶段迁移均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-031|TC-031]]：核验通过后建立会话（未开始仓门操作阶段）
- [[TC-032|TC-032]]：会话内复用不重复验证身份
- [[TC-033|TC-033]]：首次仓门操作触发锁定阶段

## Notes 备注

- 本 FR 不覆盖 [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：该操作不打开任何仓门，不影响会话阶段（见 [[fr-013-session-termination-rules|FR-013]] AC-1）。
- 会话粒度按每次 AGV 到站建立，不是操作员班次级别的会话；不设置独立的空闲超时机制（见 UC-043 Assumption 第 1 条，TBD 待补充）。
