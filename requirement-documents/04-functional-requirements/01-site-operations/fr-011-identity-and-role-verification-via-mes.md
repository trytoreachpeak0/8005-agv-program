---
id: FR-011
type: functional-requirement
title: "Identity and Role Verification via MES 身份与岗位权限核验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-30
related_uc: ["UC-043"]
related_br: []
related_fr: ["FR-012", "FR-013"]
related_nfr: ["NFR-002"]
related_tc: ["TC-027", "TC-028", "TC-029", "TC-030"]
aliases: ["FR-011"]
---

# FR-011 Identity and Role Verification via MES 身份与岗位权限核验

## Description 需求描述

系统应按项目级装货/卸货身份核验策略决定是否要求工号。8005 项目装货开启、卸货关闭。策略开启时，车载端采集扫描工牌或手动输入的工号，服务端调用 MES 核验身份及岗位权限；新工号校验成功后才能用于新的 Sublot。策略关闭时不得要求输入工号，也不得虚构操作员。

只有不存在活动、部分或未收敛的 Sublot 时才允许主动更换工号。同一 Sublot 在 LoadBatch 自动提交闭环完成前拒绝换人；掉线和重启沿用原工号，不重复验证。

## Acceptance Criteria 验收标准

- **AC-1（新工号核验通过）**
  - **Given** 项目策略要求身份核验，且当前不存在活动 Sublot
  - **When** 服务端确认 MES 返回有效人员且岗位权限满足要求
  - **Then** 服务端记录核验结果，车载端持久化新工号及核验引用
- **AC-2（核验失败）**
  - **When** 人员不存在、MES 异常或权限不足
  - **Then** 不更新当前工号，不允许以该工号开始新 Sublot，并记录审计
- **AC-3（活动 Sublot 内拒绝更换）**
  - **Given** 当前 Sublot 尚未形成 LoadBatch 自动提交闭环
  - **When** 用户尝试输入新工号
  - **Then** 拒绝更换并保留原绑定
- **AC-4（卸货策略关闭）**
  - **Given** 8005 到站卸货
  - **Then** 不要求工号，审计记录卸货身份核验策略关闭

## Notes 备注

- 策略粒度是项目，不按 AGV、站点或单次操作覆盖。
- 扫描工牌与手动输入工号使用同一核验流程。
- 掉线或重启不视为换人或离站。
- R-09 为 LoadCompensationDecision 刷卡属于独立审批认证，不是生产操作员换人；不得用审批身份覆盖当前 Sublot 已绑定工号。
