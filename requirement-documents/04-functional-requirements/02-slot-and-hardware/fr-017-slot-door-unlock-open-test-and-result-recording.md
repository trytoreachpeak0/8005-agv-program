---
id: FR-017
type: functional-requirement
title: "Slot Door Unlock/Open Test and Result Recording 仓门开锁开启测试与结果记录"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-015"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-048", "TC-049", "TC-050"]
aliases: ["FR-017"]
---

# FR-017 Slot Door Unlock/Open Test and Result Recording 仓门开锁开启测试与结果记录

## Description 需求描述

系统应当在维护人员选择目标仓位并发起"开锁测试"后，向该仓位下发开锁（DO）指令，并核验该指令是否被 IO 模块正常接收；维护人员现场判定仓门是否正常弹开/开启后，系统记录本次测试结果（维护人员、仓位号、结果：正常/异常、时间戳）。指令下发失败或仓门未能正常弹开时，系统必须将测试结果记录为"异常"，并将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的后续业务分配。

## Rationale 制定原因

将 [[uc-015-slot-door-unlock-open-test|UC-015]] 描述的"开锁指令下发 → 现场判定 → 结果记录"能力落实为可单独验收的能力切片，确保仓门机械/电子锁环节的维护测试结果可追溯，且异常仓位不会被业务流程误用。

## Origin 需求来源

- [[uc-015-slot-door-unlock-open-test|UC-015]] Normal Flow 第 2、2.1、3、3.1、5 步、Postcondition、Exception Flow E2.1、E3.1

## Acceptance Criteria 验收标准

- **AC-1（开锁测试通过，记录正常）**
  - **Given** 维护人员已选择目标仓位并发起开锁测试
  - **When** 系统下发的开锁指令被 IO 模块正常接收，且维护人员现场确认该仓位仓门正常弹开/开启
  - **Then** 系统记录本次测试结果为"正常"（维护人员、仓位号、时间戳）

- **AC-2（开锁指令下发失败，记录异常）**
  - **Given** 维护人员已发起开锁测试
  - **When** 系统核验发现该开锁指令未能被 IO 模块正常接收（如通信超时、IO 模块无响应）
  - **Then** 系统提示该仓位开锁指令下发异常，记录本次测试结果为"异常"

- **AC-3（仓门未能正常弹开，标记异常锁定）**
  - **Given** 开锁指令已被 IO 模块正常接收
  - **When** 维护人员现场核验发现该仓位仓门未能正常弹开/开启
  - **Then** 系统将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"

## Related 关联

- **Use Cases：** 支撑 [[uc-015-slot-door-unlock-open-test|UC-015]]；测试通过后建议配合 [[uc-014-enable-disable-slot|UC-014]] 完成"禁用→测试→启用"闭环，但非强制 Precondition
- **Business Rules：** 无
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 测试结果记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-048|TC-048]]：开锁测试通过，记录正常
- [[TC-049|TC-049]]：开锁指令下发失败，记录异常
- [[TC-050|TC-050]]：仓门未能正常弹开，标记异常锁定

## Notes 备注

- 本 FR 依赖维护人员现场目视判断仓门是否"正常弹开/开启"作为测试结果依据，系统本身不具备独立于人工判断的自动化机械动作检测手段（见 UC-015 Assumption 第 2 条）。
- 本 FR 不与本批其他 FR（FR-018、FR-019）建立 `related_fr` 强依赖：UC 文档中三者互为"建议衔接执行"的顺序关系（同一次巡检可连续测试），但均非彼此的 Precondition 强制要求，因此各自独立成 FR，不互相登记。
- 本 FR 独立于 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 等业务流程的核验逻辑，不复用、也不受其业务核验约束。
