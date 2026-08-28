---
id: FR-022
type: functional-requirement
title: "Slot Model Draft Field and Layout Validation 型号草稿字段与版面校验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-038"]
related_br: ["BR-008"]
related_fr: ["FR-023"]
related_nfr: ["NFR-002"]
related_tc: ["TC-064", "TC-065", "TC-066", "TC-067", "TC-068"]
aliases: ["FR-022"]
---

# FR-022 Slot Model Draft Field and Layout Validation 型号草稿字段与版面校验

## Description 需求描述

系统应当在操作人员为多仓位 AGV 模型的某个 `Draft` 版本配置面列表与仓位定义（仓位编号、所属面、起始行/列、跨行数/跨列数、规格）并确认保存时，校验：面标识与仓位编号在该型号版本内唯一；行、列、跨行数、跨列数均为正整数且仓位矩形完全落在所属面内；同一面内任意两个仓位矩形不重叠。以上任一校验不通过，系统必须拒绝保存并提示具体冲突项，不产生部分保存的草稿。校验通过时，若仓位规格（尺寸、最大载重）尚未填写完整，系统仍允许保存为 `Draft`，但须明确标记该版本当前不满足发布条件；规格已填写完整时正常保存为可继续编辑或发布的 `Draft`。

## Rationale 制定原因

[[br-008-agv-slot-model-versioning|BR-008]] 第 2 条要求发布必须基于一个校验通过的 `Draft`；将唯一性、越界、重叠这三类格式/几何层面的校验在草稿保存阶段就前置拦截，可以避免带有明显定义错误的草稿进入后续发布流程，也让维护人员在编辑阶段就能及时发现并修正冲突，而不必等到尝试发布时才发现。允许规格暂时不完整即可保存草稿（[[uc-038-maintain-agv-slot-model|UC-038]] Alternative Flow A6.1），是为了支持"先搭好面与仓位版面结构，再逐步补全规格"的渐进式编辑方式，与强制发布前必须完整（见 [[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]]）互不矛盾。

## Origin 需求来源

- [[uc-038-maintain-agv-slot-model|UC-038]] Normal Flow 第 3~6 步、Alternative Flow A6.1、Exception Flow E5.1、E5.2、E5.3、E5.4
- [[br-008-agv-slot-model-versioning|BR-008]] 第 2 条

## Acceptance Criteria 验收标准

- **AC-1（格式校验与规格均通过，保存为可发布的 Draft）**
  - **Given** 操作人员已为某型号的 `Draft` 版本配置面列表及仓位定义（编号、所属面、起始行/列、跨行数/跨列数、规格）
  - **When** 系统校验面标识与仓位编号均唯一、行列与跨格均为正整数且矩形不越界、同一面内仓位矩形互不重叠，且每个仓位的规格字段均已填写完整
  - **Then** 系统保存为 `Draft`，且该版本满足后续发布所需的字段完整性条件

- **AC-2（面标识或仓位编号重复，拒绝保存）**
  - **Given** 操作人员提交的草稿中，存在重复的面标识或仓位编号
  - **When** 系统执行保存前校验
  - **Then** 系统拒绝保存，提示冲突的具体标识

- **AC-3（行/列/跨格非正整数或矩形越界，拒绝保存）**
  - **Given** 操作人员提交的草稿中，某仓位的起始行、起始列、跨行数或跨列数为零、负数，或超出所属面的行数/列数范围
  - **When** 系统执行保存前校验
  - **Then** 系统拒绝保存，提示具体仓位及越界原因

- **AC-4（同一面内仓位矩形重叠，拒绝保存）**
  - **Given** 操作人员提交的草稿中，同一面内两个仓位的占用矩形存在共享的基础格
  - **When** 系统执行保存前校验
  - **Then** 系统拒绝保存，提示冲突的仓位编号及重叠位置

- **AC-5（规格缺失或不合法，允许暂存草稿但标记未达发布条件）**
  - **Given** 操作人员提交的草稿已通过唯一性、越界、重叠三类格式校验，但某仓位的尺寸或最大载重未填写，或数值不合法（如负数）
  - **When** 系统执行保存前校验
  - **Then** 系统仍保存为 `Draft`，同时展示尚未满足的发布条件，不允许该草稿被直接发布

## Related 关联

- **Use Cases：** 支撑 [[uc-038-maintain-agv-slot-model|UC-038]] 草稿编辑环节
- **Business Rules：** 落实 [[br-008-agv-slot-model-versioning|BR-008]] 第 2 条的发布前校验要求
- **Functional Requirements：** 校验通过且规格完整的 `Draft` 是 [[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]] 发布操作的前提输入；发布失败或回滚后仍会退回本 FR 描述的草稿状态
- **Non-Functional Requirements：** 草稿变更记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]（[[uc-038-maintain-agv-slot-model|UC-038]] Postcondition 4 明确要求审计变更前后内容）

## Verification 验证方式

- [[tc-064-draft-validation-pass-and-publishable|TC-064]]：格式校验与规格均通过，保存为可发布的 Draft
- [[tc-065-draft-duplicate-face-or-slot-id-reject|TC-065]]：面标识或仓位编号重复，拒绝保存
- [[tc-066-draft-out-of-bounds-reject|TC-066]]：行/列/跨格非正整数或矩形越界，拒绝保存
- [[tc-067-draft-overlap-reject|TC-067]]：同一面内仓位矩形重叠，拒绝保存
- [[tc-068-draft-incomplete-spec-save-not-publishable|TC-068]]：规格缺失或不合法，允许暂存草稿但标记未达发布条件

## Notes 备注

- 校验规则与 `slots-simulator` 项目对仓位版面布局的建模、校验方式一致（[[dr-009-slot-layout-model|DR-009]]，见 [[uc-038-maintain-agv-slot-model|UC-038]] 描述与 [[br-008-agv-slot-model-versioning|BR-008]] 第 2 条），保证两个系统对"面 + 统一基础网格 + 连续矩形跨格"的理解一致。
- 本 FR 只覆盖草稿阶段的格式/几何校验与规格完整性标记，不覆盖发布/停用本身的二次认证与原子生成版本，那部分见 [[fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning|FR-023]]。
- 面/仓位数量本身没有上限校验（见 UC-038 Notes 第 6 条），本 FR 不对数量设置阈值。
