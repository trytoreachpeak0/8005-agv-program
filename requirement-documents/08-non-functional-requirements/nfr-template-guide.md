---
type: template-guide
title: "Non-Functional Requirement Template Guide 非功能需求文档模板说明"
status: reference
created: 2026-07-14
updated: 2026-07-14
aliases: ["NFR 模板说明", "nfr-template-guide", "Non-Functional Requirement Template Guide"]
---

# Non-Functional Requirement Template Guide 非功能需求文档模板说明

> 本文档是**说明性质的参考文档**，不是一条非功能需求本身，因此 frontmatter 中 `type` 为 `template-guide` 而不是 `non-functional-requirement`，不会被 [[traceability-matrix|需求追溯矩阵]] 统计进“非功能需求总览”。本文档以 [[nfr-001-service-availability|NFR-001]]、[[nfr-002-audit-completeness-and-retention|NFR-002]] 为参考范例。

## 1. NFR 定位（Karl / 质量属性）

NFR 描述系统的**质量属性**：在给定工况下，系统应达到何种可度量表现。它横切多条 FR，而不是替代 FR。

| 应写入 NFR | 应写入 FR / UC / BR |
| - | - |
| 可用性目标、响应时间上限、审计留存天数 | “系统应能开锁 / 核验子批号”等能力 |
| 安全认证强度、失败默认拒绝的度量口径 | UC-004 等业务安全联锁流程本身 |
| 与 Vision 中 Quality 约束对应的可验收指标 | 业务规则原文（BR） |

**无明确度量指标且无测量方法的 NFR，视为未完成。**

## 2. Frontmatter 属性字段说明

| 字段 Field | 说明 Description |
| - | - |
| `id` | 非功能需求编号，格式 `NFR-XXX` |
| `type` | 固定为 `non-functional-requirement` |
| `title` | 标题，英文 + 中文 |
| `status` | `draft` / `reviewed` / `approved` 等 |
| `priority` | `high` / `medium` / `low` / `TBD` |
| `category` | 质量属性类别（见下） |
| `created_by` / `updated_by` | 创建人 / 最后更新人 |
| `created` / `updated` | 创建 / 最后更新日期 |
| `related_uc` | 影响的用例（全局 NFR 可为空或仅列代表性 UC） |
| `related_fr` | 横切约束的功能需求 |
| `related_tc` | 验证本 NFR 的测试用例或专项验收条目 |
| `aliases` | 通常至少包含编号本身 |

### category 常用取值

`performance` / `availability` / `reliability` / `security` / `safety` / `usability` / `scalability` / `maintainability` / `auditability` / `compatibility` / `operability`

## 3. 正文结构与各章节说明

1. **Description**：一句话质量目标。
2. **Category**：与 frontmatter 一致。
3. **Context / Stimulus**：在何种班次、负载、故障或业务场景下谈该指标（否则目标无法验收）。
4. **Metric / Scale**：度量什么（单位、统计口径）。
5. **Target / Fit Criterion**：必须达到的目标；优先 Given / When / Then，或等价可判定数值陈述。
6. **Measurement Method**：如何测量（健康检查、压测、日志抽查、现场验收等）。
7. **Origin / Rationale**：来自 Vision、客户 IT/EHS、合规等。
8. **Related**：说明横切到哪些 FR / UC；全局项写清“全系统”及例外。
9. **Verification**：关联 TC 或专项验收；未建 TC 时可先写策略。
10. **Notes**：排除项（如不含 RCS 侧网络抖动）、待客户确认的数值 TBD。

## 4. 编号与命名约定

* 文件命名：`nfr-XXX-kebab-case-英文标题.md`。
* Fit Criterion 建议编号为 `FC-1`、`FC-2`……。
* 业务语义的安全规则继续放 BR/UC；“故障安全响应时间、审计保留、权限失败默认拒绝”等可度量项进 NFR。

## 5. 与 Templater 脚本模板的关系

`_templates/template-non-functional-requirement.md` 用于在 `08-non-functional-requirements` 下新建笔记时生成骨架。本文档解释每章应写什么；样例见 [[nfr-001-service-availability|NFR-001]]、[[nfr-002-audit-completeness-and-retention|NFR-002]]。
