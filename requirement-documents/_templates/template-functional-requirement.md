<%*
const frNum = await tp.system.prompt("功能需求编号数字部分（3位，如 001）", "");
const frId = "FR-" + frNum.padStart(3, "0");
const frTitleEn = await tp.system.prompt("Functional Requirement Title 功能需求标题（英文）", "");
const frTitleCn = await tp.system.prompt("功能需求标题（中文）", "");
const today = tp.date.now("YYYY-MM-DD");
-%>
---
id: <% frId %>
type: functional-requirement
title: "<% frTitleEn %> <% frTitleCn %>"
status: draft
priority: TBD
created_by: TBD
updated_by: TBD
created: <% today %>
updated: <% today %>
related_uc: []
related_br: []
related_fr: []
related_nfr: []
related_tc: []
aliases: ["<% frId %>"]
---

# <% frId %> <% frTitleEn %> <% frTitleCn %>

## Description 需求描述

TBD 待补充（系统应当……的可验证能力陈述；一条 FR 只描述一个能力切片）

## Rationale 制定原因

TBD 待补充（为什么需要本能力；避免仅写实现细节）

## Origin 需求来源

TBD 待补充（如：[[uc-001-load-completed-lot-into-slot|UC-001]]、[[br-001-dispatch-task-range|BR-001]]、愿景/访谈）

## Acceptance Criteria 验收标准

> 统一使用 Given / When / Then。每条 AC 必须可判定通过或失败。

- **AC-1**
  - **Given** TBD
  - **When** TBD
  - **Then** TBD

## Related 关联

- **Use Cases：** TBD（派生自 / 支撑，如 [[uc-001-load-completed-lot-into-slot|UC-001]]）
- **Business Rules：** TBD（落实 / 强制，如 [[br-001-dispatch-task-range|BR-001]]）
- **Functional Requirements：** TBD（依赖 / 被依赖）
- **Non-Functional Requirements：** TBD（须满足的质量约束，如 [[nfr-001-service-availability|NFR-001]]）

## Verification 验证方式

TBD 待补充（关联对应 Test Case，如 [[TC-001|TC-001]]；TC 未建时可先写验证策略：测试 / 评审 / 演示）

## Notes 备注

TBD 待补充（边界、与客户确认的 TBD 数值、拆分/合并历史等）
