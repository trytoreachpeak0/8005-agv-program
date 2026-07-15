---
type: template-guide
title: "Functional Requirement Template Guide 功能需求文档模板说明"
status: reference
created: 2026-07-14
updated: 2026-07-14
aliases: ["FR 模板说明", "fr-template-guide", "Functional Requirement Template Guide"]
---

# Functional Requirement Template Guide 功能需求文档模板说明

> 本文档是**说明性质的参考文档**，不是一条功能需求本身，因此 frontmatter 中 `type` 为 `template-guide` 而不是 `functional-requirement`，不会被 [[traceability-matrix|需求追溯矩阵]] 的 Dataview 查询统计进“功能需求总览”。本文档以 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]]、[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] 为参考范例，说明 `04-functional-requirements` 目录下所有 FR 文档应遵循的标准结构与写作要求。

## 1. FR 与 UC / BR / NFR 的边界

| 类型 | 回答什么 | 不该写什么 |
| - | - | - |
| Use Case | 谁在什么场景下完成什么目标（流程、异常分支） | 把整条流程拆成系统能力清单 |
| Business Rule | 业务硬约束（与是否由本系统实现无关也可成立） | “系统如何落实该规则”的实现能力 |
| **Functional Requirement** | 系统**必须具备的可验证能力切片** | Trigger / Normal Flow / Exception Flow（那是 UC 的职责） |
| Non-Functional Requirement | 系统**如何表现得好**（可度量质量属性） | 把“登录”“开锁”等功能能力写成 NFR |

追溯方向：`Business Rule → Use Case → Functional Requirement → Test Case`；NFR 横切约束 FR（及必要时 UC）。

## 2. Frontmatter 属性字段说明

| 字段 Field | 说明 Description |
| - | - |
| `id` | 功能需求编号，格式 `FR-XXX`（3 位数字） |
| `type` | 固定为 `functional-requirement`；追溯矩阵按此字段筛选，务必不要写错 |
| `title` | 标题，英文 + 中文 |
| `status` | `draft` / `reviewed` / `approved` 等 |
| `priority` | `high` / `medium` / `low` / `TBD` |
| `created_by` / `updated_by` | 创建人 / 最后更新人 |
| `created` / `updated` | 创建 / 最后更新日期 |
| `related_uc` | 派生来源或支撑的用例编号数组 |
| `related_br` | 落实/强制的业务规则编号数组 |
| `related_fr` | 依赖或被依赖的其他功能需求 |
| `related_nfr` | 本 FR 必须满足的质量属性 |
| `related_tc` | 验证本 FR 的测试用例 |
| `aliases` | 通常至少包含编号本身，便于 `[[FR-XXX]]` 短链接 |

> 编号、优先级、创建/更新人及日期等基本信息统一放在 frontmatter，正文不再重复维护一份“基础信息”表格。

## 3. 正文结构与各章节说明（按建议顺序）

1. **Description 需求描述**：用“系统应当……”写出**一条**可验证能力；不要把整个 UC 抄进 Description。
2. **Rationale 制定原因**：说明为什么需要该能力（业务风险、规则强制、验收口径），避免“因为代码已经这样写了”。
3. **Origin 需求来源**：用 wikilink 指向 UC / BR / Vision / 访谈纪要；可多源。
4. **Acceptance Criteria 验收标准**：**统一 Given / When / Then**。每条 AC 必须能判定通过或失败；至少覆盖成功路径与关键拒绝/失败路径。
5. **Related 关联**：说明关系类型（派生自、落实、依赖、受 NFR 约束），不要只罗列编号。
6. **Verification 验证方式**：优先关联 `[[TC-xxx|TC-xxx]]`；TC 未建时可写验证策略（测试 / 评审 / 演示），并在 Notes 标明待补 TC。
7. **Notes 备注**：边界、与客户确认中的 TBD、与其他 FR/UC 的取舍说明。

## 4. 粒度与编号约定

* 文件命名：`fr-XXX-kebab-case-英文标题.md`，`XXX` 与 frontmatter 中的 `id` 保持一致。
* **默认一个 UC 拆多条 FR**，而不是“一个 UC = 一条 FR”。优先从 UC 的系统核验点、系统动作、异常处理能力处切片。
* 横切共享能力（如统一审计写入）可独立成 FR，并被多个 UC 的 FR 引用；可度量的质量目标应进 NFR，而不是塞进某条 FR 的附带一句。
* Acceptance Criteria 建议编号为 `AC-1`、`AC-2`……，便于评审与测试对照。

## 5. 与 Templater 脚本模板的关系

`_templates/template-functional-requirement.md` 是 Obsidian Templater 插件使用的可执行脚本模板，用于在 `04-functional-requirements` 下新建笔记时生成骨架。本文档是给人阅读的文字说明。两者配合：新建时先用 Templater 生成骨架，再对照本指南与 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]] / [[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] 填写内容。
