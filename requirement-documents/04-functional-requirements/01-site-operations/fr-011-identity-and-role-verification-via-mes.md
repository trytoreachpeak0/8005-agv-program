---
id: FR-011
type: functional-requirement
title: "Identity and Role Verification via MES 身份与岗位权限核验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-043"]
related_br: []
related_fr: ["FR-012", "FR-013"]
related_nfr: ["NFR-002"]
related_tc: ["TC-027", "TC-028", "TC-029", "TC-030"]
aliases: ["FR-011"]
---

# FR-011 Identity and Role Verification via MES 身份与岗位权限核验

## Description 需求描述

系统应当在当前站点/终端不存在其他仍处于活动状态（未开始或已锁定阶段均算）的会话时，允许操作员发起身份核验：将扫描的工牌一维码或手动输入的工号提交 MES，核验 MES 是否返回有效的人员身份，以及该人员岗位权限是否满足当前站点/场景所需的操作权限；若当前站点/终端已存在活动会话，系统必须拒绝本次核验请求，须先结束该会话才允许发起新的核验。核验结果（通过/不通过及原因）均须记录审计。

## Rationale 制定原因

身份与权限核验是建立操作会话（见 [[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]]）的前置能力，确保每次到站的装卸操作都能追溯到具体个人且具备相应权限；限制"同一终端同一时刻只允许一个活动会话"，防止多人同时操作导致追溯混乱。

## Origin 需求来源

- [[uc-043-verify-identity-and-manage-operation-session|UC-043]] Precondition 第 4 条、Normal Flow 第 1、2、2.1、2.2 步、Exception Flow E2.1、E2.2

## Acceptance Criteria 验收标准

- **AC-1（存在活跃会话时拒绝发起核验）**
  - **Given** 当前站点/终端已存在其他仍处于活动状态（未开始或已锁定阶段均算）的会话
  - **When** 操作员尝试发起新的身份核验
  - **Then** 系统拒绝本次核验请求，提示须先结束当前会话

- **AC-2（核验通过）**
  - **Given** 当前站点/终端不存在活动会话，操作员扫描工牌一维码或手动输入工号
  - **When** 系统提交 MES 核验人员身份及岗位权限，MES 返回有效的人员身份，且该人员岗位权限满足当前站点/场景所需的操作权限
  - **Then** 系统判定核验通过，进入会话建立（见 [[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]]）

- **AC-3（人员身份不存在或 MES 返回异常，拒绝）**
  - **Given** 系统已提交扫码/工号至 MES 核验
  - **When** MES 返回"人员不存在"，或因网络/接口异常无法返回结果
  - **Then** 系统不建立会话，提示"身份核验失败，请重新扫码或联系管理员"，不泄露具体失败原因是否为账号不存在

- **AC-4（岗位权限不足，拒绝）**
  - **Given** MES 返回有效的人员身份
  - **When** 该人员岗位权限不满足当前站点/场景所需的操作权限
  - **Then** 系统不建立会话，提示"当前人员权限不足，无法在本站点操作"

## Related 关联

- **Use Cases：** 派生自 [[uc-043-verify-identity-and-manage-operation-session|UC-043]]（身份核验环节）；核验通过后由 [[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] 承接会话建立
- **Business Rules：** 无
- **Functional Requirements：** 核验通过后由 [[fr-012-session-establishment-reuse-and-lock-stage-transition|FR-012]] 承接会话建立与阶段迁移；与 [[fr-013-session-termination-rules|FR-013]] 共同构成 UC-043 会话生命周期的三段拆分（核验 / 建立复用与锁定迁移 / 结束规则）
- **Non-Functional Requirements：** 核验通过与拒绝结果均须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]] 的关键操作可审计要求

## Verification 验证方式

- [[TC-027|TC-027]]：存在活跃会话时拒绝发起核验
- [[TC-028|TC-028]]：核验通过
- [[TC-029|TC-029]]：人员身份不存在或 MES 返回异常，拒绝
- [[TC-030|TC-030]]：岗位权限不足，拒绝

## Notes 备注

- 手动输入工号（[[uc-043-verify-identity-and-manage-operation-session|UC-043]] Alternative Flow A1.1）与扫描一维码在核验环节完全等价，本 FR 不区分输入方式，两者共用同一套核验逻辑。
- "同一时刻只允许一个有效会话"的判定范围是"当前站点/终端"，不是全系统维度；具体会话如何结束、结束后如何重新核验建立新会话，见 [[fr-013-session-termination-rules|FR-013]]。
