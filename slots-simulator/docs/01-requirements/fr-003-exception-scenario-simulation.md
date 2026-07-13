---
id: FR-003
type: functional-requirement
title: "异常场景模拟能力"
status: review
created: 2026-07-09
updated: 2026-07-10
related_uc: ["UC-001", "UC-005", "UC-010"]
related_dr: ["DR-003", "DR-008", "DR-010", "DR-014"]
related_fr: ["FR-002", "FR-004", "FR-006", "FR-010", "FR-012", "FR-014", "FR-015"]
aliases: ["FR-003"]
---

# FR-003 异常场景模拟能力

## Description 需求描述

支持模拟 UC-001 异常流程中与仓位硬件相关的场景，用于自动化测试主系统的异常处理逻辑。

业务超时的计时、判定与告警由主系统负责，模拟器不维护"已超时"业务状态。模拟器只提供可确定控制的硬件条件：锁状态 DI 或光幕 DI 可配置延迟变化、保持当前值而不跟随，以及门保持开启直至收到关门或状态重置动作。

## Origin 需求来源

根目录 [UC-001 放入完工产品到仓位](../../../requirement-documents/03-use-cases/uc-001-load-completed-lot-into-slot.md) 异常流程；覆盖范围依据 [[dr-003-first-batch-scenarios|DR-003]]。

## Acceptance Criteria 验收标准

覆盖场景：

- 仓位不足（通过测试前置构造使所有仓位的光幕 DI 均为"有遮挡"，主系统据此判定无可用仓位；模拟器不独立存储"已占用"）
- 开门后光幕检测到异物（未经放料动作即设置实际光幕遮挡，使光幕 DI 为"有遮挡"）
- 关门后光幕检测仍有残留（未执行取出或实际遮挡未清除时，关门动作不改变光幕 DI）
- DI 延迟反馈：可按点位设置锁状态 DI 或光幕 DI 在触发条件发生后延迟一个确定时长再变化，供主系统自行测试等待与超时分支。
- 开锁失败（DO→DI 脱钩，开方向）：下发开锁指令（DO 由 0 变为 1）后，锁状态 DI 保持"锁定"不跟随变化，模拟机械/电子锁故障。本项是 [[dr-010-do-control-mode|DR-010]] 镜像关系的例外场景，详见 [[dr-014-fault-injection-mirror-exception|DR-014]]。
- 闩锁/复位失败（DO→DI 脱钩，闩方向）：DO 变回 0（无论是主系统显式写入，还是脉冲模式超时后模拟器自动复位）后，锁状态 DI 保持"解锁"不跟随变回锁定，模拟锁虽已断电但未能真正闩上的故障。
- 光幕反馈脱钩故障：光幕 DI 卡死在故障注入发生时的值，之后不随仓位内实际遮挡情况变化更新，模拟光幕传感器/反馈线路本身失灵；与上面"开门后光幕检测到异物""关门后光幕检测仍有残留"两类场景不同——那两类场景下光幕本身工作正常，只是仓位实际状态不符合预期，本项是传感器/反馈本身失效。
- 长时间不关门（模拟器保持门开启，直至控制 API 收到关门动作或状态重置；是否超时及如何告警由主系统判定）
- IO 通信异常（可指定某一个 IO 模块实例，让模拟器主动断开该模块对应的 Modbus TCP 连接或不响应，其余模块不受影响；模块的划分对应 [[fr-014-multi-io-module-simulation|FR-014]] 的多模块实例模型，供主系统测试"部分模块失联、其余模块正常"这类更贴近真实多模块部署故障的场景，而不是笼统断开唯一一条连接）

每种异常场景均可通过控制 API（[[fr-006-automation-control-api|FR-006]]）的测试前置或故障注入能力单独构造和清除，且触发后对应的 Modbus 寄存器状态符合预期。控制 API 不提供开锁；需要开锁 DO 的场景仍由主系统通过 Modbus 写入。测试前置中的空闲/占用构造只通过设置实际光幕遮挡并观察光幕 DI 完成，不写入独立占用字段。

## Related Use Case 关联用例

[UC-001 放入完工产品到仓位](../../../requirement-documents/03-use-cases/uc-001-load-completed-lot-into-slot.md)、[UC-005 取出仓位中存错的产品](../../../requirement-documents/03-use-cases/uc-005-retrieve-mis-stored-product-from-slot.md) 与 [UC-010 终点站取出产品存料](../../../requirement-documents/03-use-cases/uc-010-unload-completed-lot-at-destination-station.md) 的硬件异常分支。

## Verification 验证方式

- **TC-FR-003-001（预留）**：Given 全部仓位通过测试前置设置为光幕有遮挡；When 主系统读取全部光幕 DI；Then 每个仓位均被推导为已占用，模拟器中不存在可与 DI 不一致的独立占用字段。
- **TC-FR-003-002（预留）**：Given 锁状态 DI 配置为延迟反馈；When 主系统写开锁 DO=1；Then 延迟期内 DI 保持锁定，达到配置时长后变为解锁，模拟器本身不产生业务超时结论。
- **TC-FR-003-003（预留）**：Given 已注入光幕反馈脱钩且光幕 DI 当前为无遮挡；When API 执行放料使实际遮挡成立；Then 光幕 DI 仍为无遮挡，派生占用仍为空闲，清除故障后 DI 与派生占用恢复跟随实际遮挡。
- **TC-FR-003-004（预留）**：Given 仓位已开门；When 不发送关门动作并等待超过主系统超时阈值；Then 模拟器持续保持门开启，由主系统产生超时处理，模拟器不改变为独立超时状态。
- **TC-FR-003-005（预留）**：Given 两个 IO 模块均已连接；When 对其中一个模块注入断连或不响应；Then 仅目标模块通信异常，另一模块继续正常读写。

## Related 关联

[[dr-010-do-control-mode|DR-010]]（锁状态镜像 DO 电平的正常规则）、[[dr-014-fault-injection-mirror-exception|DR-014]]（本 FR 中"开锁失败/闩锁失败/光幕反馈脱钩"三类场景是 DR-010 镜像关系唯一被允许打破的例外场景，定义详见该决策记录）、[[fr-014-multi-io-module-simulation|FR-014]]（IO 通信异常场景按模块实例粒度触发，详见本 FR 该条描述）。
