---
id: NFR-001
type: non-functional-requirement
title: "Service Availability During Production Shifts 生产班次内业务服务可用性"
status: draft
priority: high
category: availability
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: []
related_fr: ["FR-001", "FR-002"]
related_tc: []
aliases: ["NFR-001"]
---

# NFR-001 Service Availability During Production Shifts 生产班次内业务服务可用性

## Description 需求描述

在约定的生产班次内，多仓位 AGV 业务服务（支撑站点作业、任务核验、仓位控制指令下发与状态查询等核心能力）应保持可度量的高可用性，使现场可按系统流程持续完成搬运相关作业。

## Category 质量属性类别

`availability`

## Context / Stimulus 工况与刺激

- 适用：客户约定的正常生产班次窗口内的持续运行。
- 刺激：业务服务进程/接口不可达、健康检查失败、核心写路径持续失败导致站点作业无法进行。
- 不包括：已公告的计划内维护窗口；MES、RCS/RIOT、现场无线 AP、IO 模块或 AGV 本体等**外部系统/基础设施**自身不可用（本 NFR 只约束本业务系统服务可用性；外部依赖导致的业务中断单独统计或排除，见 Notes）。

## Metric / Scale 度量指标

- **可用性** = 班次内“业务服务可用时间” / “班次总时间”。
- **可用**定义（初稿）：健康检查通过，且核心业务接口（至少包括：子批号/任务核验、仓位开锁指令下发、仓位与任务状态查询）可在约定超时内返回成功或明确业务错误（非连接失败/网关超时/5xx 持续失败）。

## Target / Fit Criterion 目标与适合标准

> 具体百分比待与客户运维/IT 确认；以下为可评审的草稿目标，结构完整可作范例。

- **FC-1**
  - **Given** 一个已约定的正常生产班次（计划内维护已排除）
  - **When** 按 Measurement Method 统计该班次业务服务可用性
  - **Then** 可用性 ≥ **99.5%**（TBD：最终值以客户确认的 SLA 为准）

- **FC-2**
  - **Given** 业务服务发生非计划中断
  - **When** 运维按运行手册恢复
  - **Then** 单次非计划中断的恢复时间目标（RTO）≤ **15 分钟**（TBD：最终值待确认）

## Measurement Method 测量方法

1. 对业务服务提供健康检查（或等价就绪探针），按固定间隔采样。
2. 结合网关/应用日志统计核心接口的连接失败、超时与 5xx；与健康检查结果合并计算不可用区间。
3. 计划内维护窗口事先登记并在统计中排除。
4. 试运行/验收期按班次出具可用性报告；争议区间以日志时间戳为准。

## Origin / Rationale 来源与制定原因

- [[vision-and-scope|愿景与范围]]：质量为约束——须保证运行稳定性，不能因自动化搬运带来生产风险；成功指标要求系统稳定完成主要搬运场景。
- 现场班次连续作业依赖业务服务持续可用，否则核验/开锁等 FR 能力无法交付。

## Related 关联

- **Functional Requirements：** 横切约束 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]]、[[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]] 等核心站点作业能力所依赖的服务存活与可达性（全系统；不限于上述两条）。
- **Use Cases：** 全局；代表性场景为站点装载等现场作业 UC。

## Verification 验证方式

对应专项可用性验收 / Test Case 待建。建议：健康检查与故障注入（停服务）验证统计口径；试运行期按班次出报告对照 FC-1。

## Notes 备注

- **99.5% / 15 分钟**为草稿目标，Notes 标明 TBD，确认前不得当作已对客户承诺的 SLA。
- 本 NFR 不覆盖 RCS 路径规划失败、MES 掉线、IO 模块断连等外部责任域；这些应在集成/依赖可用性中另述或在事件复盘中标注根因归属。
- `related_fr` 仅列出当前黄金样例 FR 作为代表；后续核心 FR 增多时应扩展关联或在指南中约定“全局 NFR 可不枚举全部 FR”。
