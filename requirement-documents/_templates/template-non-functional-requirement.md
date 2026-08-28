<%*
const nfrNum = await tp.system.prompt("非功能需求编号数字部分（3位，如 001）", "");
const nfrId = "NFR-" + nfrNum.padStart(3, "0");
const nfrTitleEn = await tp.system.prompt("Non-Functional Requirement Title 非功能需求标题（英文）", "");
const nfrTitleCn = await tp.system.prompt("非功能需求标题（中文）", "");
const nfrCategory = await tp.system.prompt("质量属性类别 category（如 availability / auditability / performance / security / safety）", "availability");
const today = tp.date.now("YYYY-MM-DD");
-%>
---
id: <% nfrId %>
type: non-functional-requirement
title: "<% nfrTitleEn %> <% nfrTitleCn %>"
status: draft
priority: TBD
category: <% nfrCategory %>
created_by: TBD
updated_by: TBD
created: <% today %>
updated: <% today %>
related_uc: []
related_fr: []
related_tc: []
aliases: ["<% nfrId %>"]
---

# <% nfrId %> <% nfrTitleEn %> <% nfrTitleCn %>

## Description 需求描述

TBD 待补充（一句话质量目标）

## Category 质量属性类别

`<% nfrCategory %>`

> 常用取值：`performance` / `availability` / `reliability` / `security` / `safety` / `usability` / `scalability` / `maintainability` / `auditability` / `compatibility` / `operability`

## Context / Stimulus 工况与刺激

TBD 待补充（在何种负载、班次、故障或业务场景下讨论本指标）

## Metric / Scale 度量指标

TBD 待补充（度量什么：可用性百分比、响应时间、留存天数等）

## Target / Fit Criterion 目标与适合标准

> 优先使用 Given / When / Then，或等价的可判定数值目标。无数字且无测量方法视为未完成。

- **FC-1**
  - **Given** TBD
  - **When** TBD
  - **Then** TBD

## Measurement Method 测量方法

TBD 待补充（如何测量：健康检查、压测、日志抽查、现场验收等）

## Origin / Rationale 来源与制定原因

TBD 待补充（如：[[vision-and-scope|愿景与范围]]、客户 IT/EHS、合规）

## Related 关联

- **Functional Requirements：** TBD（横切约束哪些 FR）
- **Use Cases：** TBD（影响哪些场景；全局 NFR 可写“全系统”）

## Verification 验证方式

TBD 待补充（关联对应 Test Case 或专项验收；TC 未建时可先写验证策略）

## Notes 备注

TBD 待补充（排除项、与外部系统职责边界、待客户确认的数值等）
