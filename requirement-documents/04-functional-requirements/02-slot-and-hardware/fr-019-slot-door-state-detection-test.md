---
id: FR-019
type: functional-requirement
title: "Lock Feedback and Door Latch Test 锁反馈与仓门闩合测试"
status: draft
priority: medium
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-30
related_uc: ["UC-017"]
related_br: []
related_fr: []
related_nfr: ["NFR-002"]
related_tc: ["TC-055", "TC-056", "TC-057"]
aliases: ["FR-019"]
---

# FR-019 Lock Feedback and Door Latch Test 锁反馈与仓门闩合测试

## Description 需求描述

系统不得配置或读取独立“门状态 DI”。测试开始时锁 DI 应为“锁闭”；有效开锁脉冲应使弹簧自动弹门且锁 DI 变为“未锁”；脉冲 DO 自动复位后锁 DI 仍应保持“未锁”；维护人员关闭仓门并使锁舌重新闩合后，锁 DI 才应变回“锁闭”。

系统须记录各阶段的 DO 回读、锁 DI 和维护人员目视结果。开锁后仓门未弹开、锁 DI 未变化、DO 未复位或关门后锁 DI 未锁闭时，均不得宣称测试成功，也不得自动重复开锁。

## Rationale 制定原因

现场一仓一门，电子锁带弹簧弹门机构，但没有独立门磁。锁 DI 与 DO 是两个独立事实；用 DO 复位推断关门，或把锁 DI 描述成独立门位传感器，都会产生错误的安全结论。

## Origin 需求来源

- [[uc-017-slot-door-state-detection-test|UC-017]] Normal Flow、Exception Flow E3.1、E4.1、E6.1

## Acceptance Criteria 验收标准

- **AC-1（完整机构流程通过）**
  - **Given** 初始锁 DI 为“锁闭”
  - **When** 执行开锁脉冲、目视确认弹簧弹门、等待 DO 复位并人工关门闩合
  - **Then** 锁 DI 依次为“锁闭→未锁→未锁→锁闭”，系统记录测试通过
- **AC-2（开锁或弹门失败）**
  - **When** 开锁后仓门未弹开，或锁 DI 未变为“未锁”
  - **Then** 不重复开锁，记录失败并将仓位判为硬件不可操作
- **AC-3（关门未可靠闩合）**
  - **When** 维护人员关门后锁 DI 仍为“未锁”
  - **Then** 不得把仓门视为安全锁闭，提示重新关门；持续失败时记录测试失败
- **AC-4（脉冲输出未复位）**
  - **When** 超过脉宽和通信余量后 DO 回读仍有效
  - **Then** 报告 IO 输出故障并停止测试

## Verification 验证方式

- [[TC-055|TC-055]]：完整机构流程通过
- [[TC-056|TC-056]]：开锁后仓门未弹开或锁 DI 未变化
- [[TC-057|TC-057]]：关门后锁 DI 未锁闭

## Notes 备注

- 锁 DI 为“未锁”不能单独证明门板已经处于某个几何位置；正常开锁的实际弹门结果由机构和维护人员目视共同验证。
- 测试只在车辆配置维护态、整车无货时执行。
