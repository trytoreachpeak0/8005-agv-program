---
id: traceability-matrix
type: traceability
---

# 需求追溯矩阵 Traceability Matrix

> 本页面使用 Dataview 插件自动从各类需求文档的 frontmatter 字段生成，不需要手工维护。只要在对应文档的 frontmatter 里正确填写 `related_uc` / `related_br` / `related_fr` / `related_nfr` / `related_tc` 等字段，下方表格会自动更新。
>
> 追溯方向：`Business Rule 业务规则 → Use Case 用例 → Functional Requirement 功能需求 → Test Case 测试用例`；`Non-Functional Requirement 非功能需求` 横切约束 FR（及必要时 UC），并可由 TC 验证。

## 1. Business Rules 业务规则总览

```dataview
table
  status as "状态",
  title as "标题",
  related_uc as "关联用例"
from "02-business-rules"
where type = "business-rule"
sort id asc
```

## 2. Use Cases 用例总览

```dataview
table
  status as "状态",
  priority as "优先级",
  primary_actor as "主要参与者",
  related_br as "关联业务规则",
  related_uc as "关联用例"
from "03-use-cases"
where type = "use-case"
sort id asc
```

## 3. Functional Requirements 功能需求总览

```dataview
table
  status as "状态",
  priority as "优先级",
  related_br as "关联业务规则",
  related_uc as "关联用例",
  related_nfr as "关联非功能需求",
  related_tc as "关联测试用例"
from "04-functional-requirements"
where type = "functional-requirement"
sort id asc
```

## 4. Non-Functional Requirements 非功能需求总览

```dataview
table
  status as "状态",
  priority as "优先级",
  category as "质量属性类别",
  related_fr as "关联功能需求",
  related_uc as "关联用例",
  related_tc as "关联测试用例"
from "08-non-functional-requirements"
where type = "non-functional-requirement"
sort id asc
```

## 5. Test Cases 测试用例总览

```dataview
table
  status as "状态",
  related_fr as "关联功能需求",
  related_uc as "关联用例"
from "05-test-cases"
where type = "test-case"
sort id asc
```

## 6. 覆盖率检查 Coverage Check

以下查询用于找出"尚未被任何 Use Case 关联"的业务规则，便于评审时发现遗漏：

```dataview
list
from "02-business-rules"
where type = "business-rule" and (related_uc = null or length(related_uc) = 0)
```

以下查询用于找出"尚未关联任何 Test Case"的功能需求，便于检查测试覆盖是否完整：

```dataview
list
from "04-functional-requirements"
where type = "functional-requirement" and (related_tc = null or length(related_tc) = 0)
```

以下查询用于找出"尚未关联任何 Test Case"的非功能需求：

```dataview
list
from "08-non-functional-requirements"
where type = "non-functional-requirement" and (related_tc = null or length(related_tc) = 0)
```
