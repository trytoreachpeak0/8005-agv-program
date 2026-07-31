---
id: FR-012
type: functional-requirement
title: "Session Establishment, Reuse and Sublot Binding 会话建立、复用与 Sublot 操作员绑定"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-043", "UC-001", "UC-005", "UC-010", "UC-044"]
related_br: []
related_fr: ["FR-011", "FR-013"]
related_nfr: ["NFR-002"]
related_tc: ["TC-031", "TC-032", "TC-033", "TC-121"]
aliases: ["FR-012"]
---

# FR-012 Session Establishment, Reuse and Sublot Binding 会话建立、复用与 Sublot 操作员绑定

## Description 需求描述

系统为一次到站建立操作会话，可连续处理多个 Sublot。需要身份核验时，车载端持久化当前已核验工号，新 Sublot 默认沿用；服务端在该 Sublot 首次开锁前冻结操作员绑定。绑定持续到全部目标仓位完成并形成 LoadBatch 自动提交闭环，同一 Sublot 内不得更换工号。前一 Sublot 完成后允许核验并切换工号。

掉线或车载程序重启后必须恢复当前工号、活动 Sublot 和绑定关系，不重新核验；不设置空闲超时。8005 卸货身份核验关闭，卸货操作不需要操作员绑定。

R-09 可在普通生产操作员的当前界面为 LoadCompensationDecision 刷卡并完成二次认证。该身份是独立审批证据，不替换当前 Sublot 生产操作员，不更新 OnboardOperatorContext，也不结束、接管或重建 OperationSession。

## Acceptance Criteria 验收标准

- **AC-1（到站会话可跨 Sublot 复用）**
  - **Then** 同一次到站可连续处理多个 Sublot，不为每个 Sublot 新建连接会话
- **AC-2（同一 Sublot 固定操作员）**
  - **When** 服务端首次发出该 Sublot 的仓位操作指令
  - **Then** 绑定当前已核验工号，直到 Sublot 形成 LoadBatch 自动提交闭环
- **AC-3（Sublot 间允许换人）**
  - **Given** 前一 Sublot 已形成 LoadBatch 自动提交闭环
  - **When** 新工号通过 FR-011 校验
  - **Then** 后续 Sublot 使用新工号
- **AC-4（掉线与重启恢复）**
  - **Then** 原工号和 Sublot 绑定从持久化状态恢复，不重复验证
- **AC-5（R-09 审批不替换生产操作员）**
  - **Given** 活动 Sublot 已绑定生产操作员 A，当前 OperationSession 有效
  - **When** R-09 B 在当前界面刷卡并通过 LoadCompensationDecision 的权限和二次认证核验
  - **Then** 系统分别记录 A 为生产操作员、B 为决策人；保持原 Sublot 绑定、OnboardOperatorContext 和 OperationSession，不执行换人、退出或会话接管

## Notes 备注

- 不再使用“整次到站首次开门后锁死同一操作员”的模型。
- 工号是到站期间默认值，Sublot 是不可切换边界。
- 审批身份不是生产操作员身份；二者必须独立记录。
