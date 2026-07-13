---
id: FR-015
type: functional-requirement
title: "终点站取出流程支持"
status: review
created: 2026-07-10
updated: 2026-07-10
related_uc: ["UC-010"]
related_dr: ["DR-003", "DR-006", "DR-013", "DR-014"]
related_fr: ["FR-002", "FR-003", "FR-004", "FR-006", "FR-007"]
aliases: ["FR-015"]
---

# FR-015 终点站取出流程支持

## Description 需求描述

模拟器通过统一的仓位动作支持终点站取出流程。WPF 与自动化控制 API 对每个仓位提供语义一致的四个动作：`开门`、`关门`、`放料`、`取出`；终点站流程复用这些动作，不另建专用动作或状态机。主系统可对一个或多个仓位执行"开门→取出→关门"，开门前的开锁仍由 Modbus DO 及其锁状态 DI 规则控制。

仓位是否"占用"不作为独立可写状态保存，而是始终由光幕 DI 当前值推导：光幕 DI 表示有遮挡时为已占用，无遮挡时为空闲。正常情况下，放料使光幕 DI 进入有遮挡状态，取出使其进入无遮挡状态；故障注入时按 [[fr-003-exception-scenario-simulation|FR-003]] 与 [[dr-014-fault-injection-mirror-exception|DR-014]] 的规则呈现异常反馈。

目标站点匹配、产品身份/批次记录及"实物是否与系统记录一致"均属于被测主系统职责，不由模拟器存储、匹配或判定。模拟器只提供可观察的硬件状态和动作结果，使主系统能够完成这些校验及异常处理。

本 FR 与 [[fr-004-mis-stored-product-retrieval|FR-004]]（对应根目录 UC-005 主动纠错取出）虽然业务触发原因不同，但对模拟器而言使用相同的四个统一动作、[[fr-002-slot-state-machine-normal-flow|FR-002]] 状态机和 [[fr-003-exception-scenario-simulation|FR-003]] 故障注入能力；差异由主系统的流程编排和记录校验承担。

## Origin 需求来源

根目录 [UC-010 终点站取出产品存料](../../../requirement-documents/03-use-cases/uc-010-unload-completed-lot-at-destination-station.md)。该 UC 是在 slots-simulator 首批需求梳理（[[dr-003-first-batch-scenarios|DR-003]]）之后才补写的，此前未被纳入模拟器覆盖范围内，属于遗漏后的补充；覆盖范围更新依据见 DR-003。

## Acceptance Criteria 验收标准

- WPF 与自动化控制 API 均暴露 `开门`、`关门`、`放料`、`取出` 四个统一动作，名称、前置条件、状态变化和错误语义一致；终点站取出与纠错取出均复用这些动作。
- `开门` 仅在锁状态 DI 表示已解锁时成功；`关门` 更新门的内部物理状态，但门状态不映射为独立 DI（见 [[dr-013-door-state-not-independent-io-point|DR-013]]）。
- `放料` 与 `取出` 更新仓位内实际遮挡情况；正常反馈下分别令光幕 DI 表示有遮挡与无遮挡。占用状态在所有界面、API 和流程中均由光幕 DI 推导，不维护第二份可写占用标志。
- 支持 UC-010 所需的硬件异常观测：开锁失败复用故障注入；开门后无产品表现为光幕 DI 无遮挡；关门后残留表现为光幕 DI 仍有遮挡。产品身份或记录是否匹配由主系统判断。
- 模拟器不接收或解释目标站点、产品身份、批次记录，不自动筛选待取仓位；主系统负责目标站点匹配、产品记录校验并向选定仓位发起动作。
- 同一仓位的动作必须按到达顺序串行执行，前一动作完成后下一动作才可改变该仓位状态；不同仓位的动作可并行执行且状态、故障与结果互不阻塞。
- 某一仓位的动作失败或异常不得自动取消、回滚或阻塞其他仓位的动作。

## Related Use Case 关联用例

[UC-010 终点站取出产品存料](../../../requirement-documents/03-use-cases/uc-010-unload-completed-lot-at-destination-station.md)。

## Verification 验证方式

- **TC-FR-015-001（编号预留）**
  - **Given** 仓位已解锁、光幕 DI 表示有遮挡
  - **When** 依次执行开门、取出、关门
  - **Then** 动作均成功，取出后光幕 DI 表示无遮挡且派生占用状态为空闲
- **TC-FR-015-002（编号预留）**
  - **Given** WPF 和自动化控制 API 指向相同初始状态的仓位
  - **When** 分别通过两种入口执行开门、关门、放料、取出
  - **Then** 四个动作的前置条件、状态变化和错误语义一致
- **TC-FR-015-003（编号预留）**
  - **Given** 同一仓位同时收到多个动作，另一个仓位也收到动作
  - **When** 模拟器处理这些请求
  - **Then** 同一仓位按到达顺序串行处理，不同仓位并行处理且互不阻塞
- **TC-FR-015-004（编号预留）**
  - **Given** 已注入开锁失败、空仓或关门后残留场景
  - **When** 主系统执行终点站取出流程
  - **Then** 模拟器仅通过锁状态 DI、光幕 DI 和动作结果暴露相应硬件现象，不替主系统判定业务异常
- **TC-FR-015-005（编号预留）**
  - **Given** 主系统持有目标站点和产品记录，模拟器仅持有仓位硬件状态
  - **When** 主系统完成匹配校验并对选定仓位发起统一动作
  - **Then** 模拟器无需接收业务记录即可完成动作，且不自行选择或拒绝目标仓位

## Related 关联

[[fr-002-slot-state-machine-normal-flow|FR-002]]（统一动作复用正常状态机）、[[fr-003-exception-scenario-simulation|FR-003]]（故障注入与异常硬件反馈）、[[fr-004-mis-stored-product-retrieval|FR-004]]（纠错取出复用相同动作）、[[fr-006-automation-control-api|FR-006]]（统一动作 API）、[[fr-007-wpf-visualization-panel|FR-007]]（统一动作 WPF 入口）、[[dr-003-first-batch-scenarios|DR-003]]（UC-010 纳入范围）、[[dr-006-users-and-automation-style|DR-006]]（WPF/API 一致）、[[dr-013-door-state-not-independent-io-point|DR-013]]（门状态无独立 DI）、[[dr-014-fault-injection-mirror-exception|DR-014]]（光幕反馈例外）。
