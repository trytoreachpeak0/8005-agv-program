---
id: FR-030
type: functional-requirement
title: "AGV Fleet Dashboard Display and Eligibility Reasoning AGV 车队看板展示与可分配原因推导"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-022"]
related_br: ["BR-002"]
related_fr: []
related_nfr: []
related_tc: ["TC-095", "TC-096", "TC-097"]
aliases: ["FR-030"]
---

# FR-030 AGV Fleet Dashboard Display and Eligibility Reasoning AGV 车队看板展示与可分配原因推导

## Description 需求描述

系统应当读取已接入 AGV 的本地档案、启停/归档状态、配置、本地未完成作业，以及 RCS/RIOT 在线/位置/电量/任务队列状态和仓门/光幕/安全设备状态，按 [[br-002-agv-allocation-eligibility|BR-002]] 计算每台车的"可分配/不可分配"结论及具体原因（可组合展示，如"已禁用 + 电量不足 + 仓门状态未知"），并展示车辆列表及详情。当外部状态（RCS/RIOT 或 IO/安全设备）读取失败时，系统必须保留最近一次状态及其时间戳，明确标记为"过期/未知"，并将该车辆判定为不可分配，不得使用默认正常值继续展示为可分配。本能力只读，不修改任何车辆、任务或配置数据。

## Rationale 制定原因

"RCS/RIOT 队列为空"只说明车辆没有移动任务，不代表本地业务已完成，若看板仅依赖该状态展示"空闲"，会误导调度人员做出错误判断（见 [[br-002-agv-allocation-eligibility|BR-002]] Rationale）。要求外部状态读取失败时 fail-closed 标记为不可分配、而非静默沿用旧的"可分配"判断，是避免因接口抖动或超时造成的误判被继续用于人工决策。

## Origin 需求来源

- [[uc-022-view-agv-fleet-and-availability|UC-022]] Normal Flow 第 2~7 步、异常流程"状态读取失败"、Exception Flow E4.1、Postcondition

## Acceptance Criteria 验收标准

- **AC-1（正常展示车辆列表并按 BR-002 计算可分配结论）**
  - **Given** 管理员打开 AGV 车队页面，本地档案、配置、本地作业状态，以及 RCS/RIOT 与仓门/光幕/安全状态均可正常读取
  - **When** 系统按 [[br-002-agv-allocation-eligibility|BR-002]] 计算每台车的可分配结论
  - **Then** 系统展示车辆列表（本地名称、RCS ID、车型、启停/归档状态、位置、电量、任务、仓门、可分配结论），管理员可打开详情查看完整配置、当前作业、状态时间戳和不可分配原因

- **AC-2（外部状态读取失败，保留旧数据并标记过期未知）**
  - **Given** 管理员正在查看或刷新车队页面
  - **When** RCS/RIOT 状态读取失败
  - **Then** 系统保留最近一次状态及其时间戳，明确标记为过期/未知，将该车辆判定为不可分配，记录接口异常并告警

- **AC-3（IO 或安全状态读取失败，标记未知并判定不可分配）**
  - **Given** 管理员正在查看或刷新车队页面
  - **When** 某台车辆的仓门、光幕或安全状态读取失败
  - **Then** 系统将对应状态标记为未知，判定该车辆不可分配，并显示具体缺失项

## Related 关联

- **Use Cases：** 支撑 [[uc-022-view-agv-fleet-and-availability|UC-022]]；消费 [[uc-019-register-agv-from-rcs|UC-019]] 提供的档案、[[uc-020-maintain-agv-dispatch-profile|UC-020]] 提供的配置、[[uc-013-enable-disable-agv|UC-013]] 提供的启停状态、[[uc-021-archive-agv|UC-021]] 提供的归档状态
- **Business Rules：** 按 [[br-002-agv-allocation-eligibility|BR-002]] 计算可分配结论及 Fail-closed 规则
- **Functional Requirements：** 无强依赖
- **Non-Functional Requirements：** 无（本 UC 为纯只读查询，不修改任何数据，Postcondition 未显式要求记录审计，处理方式与 [[fr-010-arrival-status-update-and-operation-panel-navigation|FR-010]]、[[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]] 一致）

## Verification 验证方式

- [[tc-095-fleet-dashboard-normal-display|TC-095]]：正常展示车辆列表并按 BR-002 计算可分配结论
- [[tc-096-fleet-dashboard-rcs-status-fail-stale|TC-096]]：外部状态读取失败，保留旧数据并标记过期未知
- [[tc-097-fleet-dashboard-io-safety-status-fail-unknown|TC-097]]：IO 或安全状态读取失败，标记未知并判定不可分配

## Notes 备注

- 状态刷新周期、过期阈值和告警去重策略仍为 TBD（见 UC-022 Notes），本 FR 不对具体数值做约束。
- 本 FR 与 [[fr-015-slot-monitoring-dashboard-display-and-refresh|FR-015]] 的关系：FR-015 关注仓位监控，本 FR 关注车辆主档、综合状态和任务分配资格，两者是不同维度的看板，不合并。
- 查看已归档车辆（UC-022 Alternative Flow A6.1）时，系统展示归档档案及历史信息但不显示为可分配，本 FR 暂不单独拆 AC 覆盖该筛选场景，行为已隐含在 AC-1 的"启停/归档状态"展示中。
