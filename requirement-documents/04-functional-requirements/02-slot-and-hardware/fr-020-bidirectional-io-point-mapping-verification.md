---
id: FR-020
type: functional-requirement
title: "Bidirectional IO Point Mapping Verification 双向 IO 点位映射核对"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-018"]
related_br: []
related_fr: ["FR-021"]
related_nfr: ["NFR-002"]
related_tc: ["TC-058", "TC-059", "TC-060"]
aliases: ["FR-020"]
---

# FR-020 Bidirectional IO Point Mapping Verification 双向 IO 点位映射核对

## Description 需求描述

系统应当对目标仓位的 IO 点位映射配置进行双向核对：方向一，系统按配置向该仓位下发开锁 DO 指令，核对维护人员现场目视确认发生反应的物理仓位是否与配置中该 DO 点位对应的仓位编号一致；方向二，核对维护人员现场手动触发某物理仓位传感器后，系统读取到的 DI 变化仓位编号是否与该物理仓位一致。两个方向均核对通过，系统记录该仓位映射核对结果为"通过"；任一方向核对不通过，系统必须将涉及的仓位标记为"映射异常"，暂停对该仓位的业务分配。

## Rationale 制定原因

将 [[uc-018-io-point-mapping-verification-test|UC-018]] 描述的"配置层面点位—物理位置对应关系是否正确"双向核对能力落实为可单独验收的能力切片，确保 IO 映射配置错误不会被误判为对应仓位硬件本身正常，避免 [[uc-015-slot-door-unlock-open-test|UC-015]]、[[uc-016-slot-light-curtain-function-test|UC-016]]、[[uc-017-slot-door-state-detection-test|UC-017]] 等硬件功能测试结果被误指向错误的物理仓位。

## Origin 需求来源

- [[uc-018-io-point-mapping-verification-test|UC-018]] Normal Flow 第 2~6 步、Postcondition、Exception Flow E2.3、E3.3

## Acceptance Criteria 验收标准

- **AC-1（双向核对均通过，记录映射通过）**
  - **Given** 系统已按配置向目标仓位下发开锁 DO 指令，且维护人员已现场手动触发该物理仓位的传感器
  - **When** 维护人员核对确认：方向一中实际发生反应的物理仓位与配置中该 DO 点位对应的仓位编号一致；方向二中系统读取到的 DI 变化仓位编号与实际触发的物理仓位一致
  - **Then** 系统记录该仓位映射核对结果为"通过"

- **AC-2（方向一核对不通过，标记映射异常）**
  - **Given** 系统已按配置中指向该仓位的 DO 点位下发开锁指令
  - **When** 维护人员核对发现实际发生反应（弹开）的物理仓位与配置中该 DO 点位对应的仓位编号不一致
  - **Then** 系统将涉及的仓位标记为"映射异常"，暂停对其业务分配，记录本次核对结果

- **AC-3（方向二核对不通过，标记映射异常）**
  - **Given** 维护人员已现场手动触发某个物理仓位的传感器
  - **When** 维护人员核对发现软件侧显示的 DI 变化仓位编号与自己实际触发的物理仓位不一致
  - **Then** 系统将涉及的仓位标记为"映射异常"，暂停对其业务分配，记录本次核对结果

## Related 关联

- **Use Cases：** 支撑 [[uc-018-io-point-mapping-verification-test|UC-018]]；是 [[uc-015-slot-door-unlock-open-test|UC-015]]、[[uc-016-slot-light-curtain-function-test|UC-016]]、[[uc-017-slot-door-state-detection-test|UC-017]] 能够正确工作的更底层前提
- **Business Rules：** 无
- **Functional Requirements：** 依赖 [[fr-021-slot-to-io-point-mapping-create-modify-validation|FR-021]] 先创建的映射配置作为核对对象；核对不通过时需回到 FR-021 修正配置后重新核对
- **Non-Functional Requirements：** 核对结果记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-058|TC-058]]：双向核对均通过，记录映射通过
- [[TC-059|TC-059]]：方向一核对不通过，标记映射异常
- [[TC-060|TC-060]]：方向二核对不通过，标记映射异常

## Notes 备注

- 本 FR 验证的是配置层面"点位—物理位置"对应关系是否正确，与 FR-017/018/019 验证"某个仓位的硬件本身是否正常工作"是不同维度的问题；若映射配置本身错误，即使被误指向的仓位硬件完全正常，那三条 FR 的测试结果也会被误判到错误的仓位上（见 UC-018 描述）。
- 两个方向均依赖维护人员现场目视/手动触发的人工判断准确性，系统本身无法独立交叉验证（见 UC-018 Assumption 第 2 条）。
- 是否需要提供"批量自动核对"手段，当前按维护人员逐个手动核对描述，如需自动化辅助待后续补充（见 UC-018 Notes 待补充事项第 3 条）。
