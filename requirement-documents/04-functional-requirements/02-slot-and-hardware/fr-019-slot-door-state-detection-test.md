---
id: FR-019
type: functional-requirement
title: "Slot Door State Detection Test 仓门开关状态识别测试"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-017"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-055", "TC-056", "TC-057"]
aliases: ["FR-019"]
---

# FR-019 Slot Door State Detection Test 仓门开关状态识别测试

## Description 需求描述

系统应当在维护人员打开目标仓位仓门后，读取该仓位门状态 DI 信号并核验是否正确变为"开启"；维护人员随后关闭该仓门，系统再次读取门状态 DI 信号并核验是否正确变为"关闭"。两个方向的信号均与实际物理状态一致时，系统记录本次测试结果为"正常"；任一方向的信号与实际不一致时，系统必须将该仓位标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，并记录本次测试结果为"异常"。

## Rationale 制定原因

将 [[uc-017-slot-door-state-detection-test|UC-017]] 描述的"门实际物理开合状态"与"系统读取的门状态 DI 信号"一致性验证能力落实为可单独验收的能力切片，确保门状态反馈信号异常时能够被及时发现，避免影响 [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-004-slot-door-safety-interlock|UC-004]]、[[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 等业务流程依赖门状态信号判断仓门是否已正常打开/关闭的准确性。

## Origin 需求来源

- [[uc-017-slot-door-state-detection-test|UC-017]] Normal Flow 第 2~6 步、Postcondition、Exception Flow E3.1、E5.1

## Acceptance Criteria 验收标准

- **AC-1（开启、关闭两方向均核验通过，记录正常）**
  - **Given** 维护人员依次打开、关闭目标仓位仓门
  - **When** 系统分别读取该仓位门状态 DI 信号，均与门的实际物理开合状态一致（打开时为"开启"、关闭时为"关闭"）
  - **Then** 系统记录本次测试结果为"正常"（维护人员、仓位号、时间戳）

- **AC-2（仓门已打开但信号仍显示关闭，标记异常）**
  - **Given** 维护人员已打开目标仓位仓门
  - **When** 系统读取的该仓位门状态 DI 信号未变化，仍显示"关闭"，与门实际已打开的物理状态不一致
  - **Then** 系统判定该仓位门状态传感器/反馈信号异常，标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"

- **AC-3（仓门已关闭但信号仍显示开启，标记异常）**
  - **Given** 维护人员已关闭目标仓位仓门
  - **When** 系统读取的该仓位门状态 DI 信号未变化，仍显示"开启"，与门实际已关闭的物理状态不一致
  - **Then** 系统判定该仓位门状态传感器/反馈信号异常，标记为"异常锁定"或"测试未通过"，暂停对该仓位的业务分配，记录本次测试结果为"异常"

## Related 关联

- **Use Cases：** 支撑 [[uc-017-slot-door-state-detection-test|UC-017]]；测试动作可衔接 [[uc-015-slot-door-unlock-open-test|UC-015]] 的开关门操作一并进行
- **Business Rules：** 无
- **Functional Requirements：** 无
- **Non-Functional Requirements：** 测试结果记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-055|TC-055]]：开启、关闭两方向均核验通过，记录正常
- [[TC-056|TC-056]]：仓门已打开但信号仍显示关闭，标记异常
- [[TC-057|TC-057]]：仓门已关闭但信号仍显示开启，标记异常

## Notes 备注

- 本 FR 假定维护人员对仓门实际物理开合状态的判断是准确的（测试基准本身可信），系统读取的 DI 信号是被核验的对象，而不是反过来用系统信号验证维护人员的判断（见 UC-017 Assumption 第 1 条）。
- 本 FR 不与本批其他 FR（FR-017、FR-018）建立 `related_fr` 强依赖，理由见 FR-017 Notes。
- 门状态信号具体来源于电子锁自带的开关反馈还是独立的门磁传感器，本 FR 不区分具体硬件形式，统称"门状态 DI 信号"（见 UC-017 Notes 待补充事项第 2 条）。
