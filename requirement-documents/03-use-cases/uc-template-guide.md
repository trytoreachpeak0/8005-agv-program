---
type: template-guide
title: "Use Case Template Guide 用例文档模板说明"
status: reference
created: 2026-07-09
updated: 2026-07-09
aliases: ["UC 模板说明", "uc-template-guide", "Use Case Template Guide"]
---

# Use Case Template Guide 用例文档模板说明

> 本文档是**说明性质的参考文档**，不是一个用例（Use Case）本身，因此 frontmatter 中 `type` 为 `template-guide` 而不是 `use-case`，不会被 [[traceability-matrix|需求追溯矩阵]] 的 Dataview 查询统计进"用例总览"表格。本文档以 [[uc-001-load-completed-lot-into-slot|UC-001]] 为参考范例，说明本项目 `03-use-cases` 目录下所有 UC 文档应遵循的标准结构、各章节的含义与写作要求，供后续新增/修改 UC 文档时参考。

## 1. Frontmatter 属性字段说明

| 字段 Field | 说明 Description |
| - | - |
| `id` | 用例编号，格式 `UC-XXX`（3 位数字） |
| `type` | 固定为 `use-case`；追溯矩阵按此字段筛选，务必不要写错 |
| `title` | 用例标题，英文 + 中文 |
| `status` | 文档状态，如 `draft`（草稿）、后续可扩展 `reviewed`/`approved` 等 |
| `priority` | 优先级：`high` / `medium` / `low` / `TBD` |
| `created_by` / `updated_by` | 创建人/最后更新人 |
| `created` / `updated` | 创建/最后更新日期 |
| `primary_actor` | 主要参与者 |
| `secondary_actor` | 次要参与者（如无可填 `None 无`，如未确定可填 `TBD`） |
| `frequency` | 使用频率说明 |
| `related_uc` | 关联的其他用例编号数组，用于追溯矩阵 |
| `related_br` | 关联的业务规则编号数组，用于追溯矩阵 |
| `aliases` | Obsidian 别名，通常至少包含用例编号本身，便于 `[[UC-XXX]]` 短链接跳转 |

> 用例编号、名称、创建/更新人及日期、参与者、优先级、使用频率等基本信息统一放在 frontmatter 中维护（以 [[uc-001-load-completed-lot-into-slot|UC-001]] 为准），正文不再重复维护一份"Basic Information 基础信息"表格，避免同一信息在两处维护、容易改漏、改不一致。

## 2. 正文结构与各章节说明（按建议顺序）

1. **Description 描述**：用 2-4 句话概述该用例做什么、涉及哪些角色和关键动作。
2. **Trigger 触发条件**：什么事件/条件促使该用例被发起执行。
3. **Precondition 前置条件**：用例开始执行前，系统需要**主动核验**、核验不通过则拒绝进入流程的条件。建议按 `System & Interface`、`Equipment & Hardware`、`Task & Data`、`Personnel & Authorization` 等类别分组列出，便于分类追溯。
4. **Postcondition 后置条件**：用例正常执行完成后，系统/数据/设备应达到的状态，分类方式同 Precondition。
5. **Assumption 假设**（新增章节）：编写文档时**默认成立、系统不会也不需要逐次去核验**的前提假设，用于界定本用例的讨论边界。与 Precondition 的区别：Precondition 核验不通过会被系统拦截并转入 Exception Flow；Assumption 不通过则意味着实际场景超出了本用例的讨论范围，需要额外场景/用例来覆盖，而不是本用例的异常分支。例如 [[uc-001-load-completed-lot-into-slot|UC-001]] 中"生产操作员扫码后不会放入非产品类的其他东西"，就是假设操作员会正常操作，系统不会去逐次核验仓位里放的是不是"产品"，这类误用场景不在 UC-001 讨论范围内。若某用例暂无需要特别说明的假设，可先填 `TBD 待补充`。
6. **Normal Flow 正常流程**：以 `<用例序号>.0` 编号（如 UC-001 的正常流程用 `1.0`），逐步描述最主要的一条成功路径，步骤下可用 `1.1`/`1.2` 等子编号列出该步骤中系统需要核验的检查点。
7. **Alternative Flow 备选流程**：与 Normal Flow 达成相同目标、但触发方式或个别步骤不同的分支路径，编号为 `<用例序号>.1`、`<用例序号>.2`……，并注明与 Normal Flow 的差异点；如经确认某用例不存在需要单独区分的备选流程（如 [[uc-002-confirm-task-completion|UC-002]]），可直接说明原因，不必强行编造分支。
8. **Exception Flow 异常流程**：每条异常以 `E<步骤号>` 编号，与 Normal/Alternative Flow 中触发该异常的具体步骤（或子步骤）一一对应（例如 `E1.2` 对应第 1.2 步核验失败的情形），建议先在本节开头列出所有异常编号及一句话摘要，再逐条展开处理流程。
9. **Notes 备注**：记录该用例的拆分/合并历史、编号约定说明、与其他用例的取舍边界、与用户澄清 TBD 问题的决策记录等不适合放进上面各结构化章节的补充说明。
10. **Related Use Cases 关联用例**：列出与本用例相关的其他用例（`[[uc-xxx|UC-xxx]]`），并说明具体的关联关系（依赖、互斥、先后顺序等），而不仅仅是罗列编号。
11. **Other Information 其他信息**（新增章节）：预留的自由信息区，用于存放不适合归入以上任何标准章节、但仍需要记录在该用例文档中的其他内容（如外部参考资料、待跟进事项等）。目前 UC-001~UC-005 中本章节均暂为空，仅作为章节占位，后续如有需要再补充内容。

## 3. 编号与命名约定

* 文件命名：`uc-XXX-kebab-case-英文标题.md`，`XXX` 与 frontmatter 中的 `id` 保持一致。
* Normal Flow 用 `<用例序号>.0` 编号，Alternative Flow 用 `<用例序号>.1`/`.2`……，两者内部的检查点用 `.1`/`.2` 等子编号。
* Exception Flow 统一用 `E<步骤号>` 编号，与触发它的 Normal/Alternative Flow 步骤号一一对应。

## 4. 与 Templater 脚本模板的关系

`_templates/template-use-case.md` 是 Obsidian Templater 插件使用的可执行脚本模板，用于快速创建新的 UC 文档骨架（已同步更新，包含 Assumption、Other Information 两个新章节）。本文档（`uc-template-guide.md`）则是给人阅读的文字说明，解释每个字段/章节"为什么这样写、应该写什么"，两者配合使用：新建用例时先用 Templater 脚本生成骨架，再对照本指南填写内容。
