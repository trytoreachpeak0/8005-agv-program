---
id: FR-001
type: functional-requirement
title: "可配置仓位数量与 IO 点位映射"
status: review
created: 2026-07-09
updated: 2026-07-13
related_uc: ["UC-018"]
related_dr: ["DR-004", "DR-005", "DR-009", "DR-010", "DR-011", "DR-012", "DR-013"]
related_fr: ["FR-005", "FR-007", "FR-011", "FR-012", "FR-013", "FR-014"]
aliases: ["FR-001"]
---

# FR-001 可配置仓位数量与 IO 点位映射

## Description 需求描述

模拟器启动时按配置文件（或界面配置，见 [[fr-007-wpf-visualization-panel|FR-007]]）加载"这个实例模拟几个仓位、每个仓位的 DO/DI 分别映射到哪些 Modbus 地址"，不写死在代码中。

仓位的显示布局（所属面、左上角行列、`rowSpan`、`columnSpan`）由 [[fr-011-configurable-slot-layout|FR-011]] 单独定义，属于同一个仓位配置项下的另一部分字段，不与本 FR 的 IO 点位映射混在一起维护——本 FR 只关注协议地址，不关注界面上摆在哪个位置或占据多少基础格。

仓位的 DO/DI 点位映射不是裸的协议地址，而是"引用某个 IO 模块实例 + 该模块内的通道号"两级寻址（见 [[fr-014-multi-io-module-simulation|FR-014]]），且通道号范围受该模块所套用寄存器表模板（见 [[fr-013-configurable-register-table-template|FR-013]]）声明的 DO/DI 数量约束，不能超出。

配置还为每个 DO 点位声明控制模式与脉冲宽度的默认值。模块启动时以这些默认值初始化对应运行时寄存器；启动完成后，以主系统通过 Modbus 写入的运行时寄存器值为准，配置文件不持续覆盖运行时值。调用状态重置接口时，对应寄存器恢复为配置默认值。

## Origin 需求来源

模拟器自身的可配置性需求，源自 [[dr-004-configurable-slot-count|DR-004]]（仓位数量可配置）与 [[dr-005-modbus-protocol-fidelity|DR-005]]（真实设备寄存器表已经明确，但仓位到“模块实例 + 通道”的项目级布线映射仍需可配置）。

## Acceptance Criteria 验收标准

- 通过 WPF 或外部方式修改配置中的仓位数量并通过完整校验后，配置立即原子热重载生效，不需要改代码或重启进程；热重载失败时继续使用上一份有效配置。
- 每个仓位至少可配置：开锁指令（DO）、锁状态（DI）、光幕/物体检测（DI）三类点位地址。
- 真实点位表确认后，能够直接更新配置文件适配，不需要改动模拟器代码。
- 每个 DO 点位除地址外，还可以按 [[fr-012-do-pulse-level-control-mode|FR-012]] 独立配置电平/脉冲控制模式，两者是同一个点位配置项下的不同字段。
- 每个仓位的 DO/DI 点位配置指定所属的 IO 模块实例与模块内通道号；通道号超出该模块所套用寄存器表模板（[[fr-013-configurable-register-table-template|FR-013]]）声明的 DO/DI 数量时，视为配置错误。
- 每个 DO 点位可配置控制模式与脉冲宽度默认值；启动时初始化对应运行时寄存器，运行期间寄存器写入立即成为当前有效值，状态重置时恢复配置默认值。
- 配置存在重复点位映射、未知模块引用、越界通道或不符合模板数据范围的默认值时，启动失败并明确指出配置项，不得静默修正。

## Related Use Case 关联用例

[UC-018 IO 点位映射表核对测试](../../../requirement-documents/03-use-cases/uc-018-io-point-mapping-verification-test.md)；其余仓位相关用例间接依赖本 FR 的映射配置。

## Verification 验证方式

- **TC-FR-001-001（预留）**：Given 配置声明两个 IO 模块、多个仓位及合法的模块通道映射；When 启动模拟器；Then 仓位数量、模块归属和 DO/DI 通道均与配置一致，无需修改代码。
- **TC-FR-001-002（预留）**：Given 配置包含未知模块、重复映射或超出模板上限的通道；When 启动模拟器；Then 启动被拒绝，并返回可定位到具体配置项的错误。
- **TC-FR-001-003（预留）**：Given 某 DO 的配置默认控制模式为 Pulse、脉冲宽度为 500 ms；When 启动后通过 Modbus 改为 Level 和 1000 ms，再调用状态重置；Then 运行期间使用写入值，重置后恢复 Pulse 和 500 ms。
