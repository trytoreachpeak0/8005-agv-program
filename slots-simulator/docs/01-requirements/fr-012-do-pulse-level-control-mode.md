---
id: FR-012
type: functional-requirement
title: "可配置 DO 点位脉冲/电平控制模式"
status: review
created: 2026-07-10
updated: 2026-07-10
related_uc: []
related_dr: ["DR-010", "DR-011", "DR-014", "DR-015"]
related_fr: ["FR-001", "FR-002", "FR-003", "FR-010", "FR-013"]
aliases: ["FR-012"]
---

# FR-012 可配置 DO 点位脉冲/电平控制模式

## Description 需求描述

每个 DO 点位（如"开锁指令"）可独立配置初始控制模式和初始脉冲宽度：

- **电平控制（Level）**：DO 的值完全由主系统的 Modbus 写入决定，模拟器不自动改变。DO=1（True）表示"通"，DO=0（False）表示"不通"。
- **脉冲控制（Pulse）**：可配置该点位的脉冲时长。主系统写入 DO=1（True）后，模拟器内部计时，到达运行时有效脉冲时长后自动将该点位复位为 0（False），无需主系统显式写 0（模拟脉冲继电器/IO 模块自身复位的硬件行为）。

配置中的模式与脉冲宽度是启动及 reset 的默认值：启动时写入该模块模板定义的 DO 工作模式寄存器（首个模板为 40412～40427）和 DO 脉冲宽度寄存器（首个模板为 40428～40443）。启动完成后，以这些运行时寄存器的当前值为准；主系统合法写入后立即改变相应 DO 的后续行为，不要求修改配置。reset 将模式、脉冲宽度和 DO 电平恢复为配置默认值。配置热重载更新 reset 默认值，但不覆盖现有通道的运行时寄存器值；新增通道按新配置初始化。

结合电磁锁的物理特性（通电开锁、断电闩锁）：对应的锁状态（DI 反馈）实时镜像该 DO 点位的当前值，因此脉冲模式下锁会在脉冲超时后随 DO 自动复位而自动重新闩上，这一镜像关系详见 [[fr-002-slot-state-machine-normal-flow|FR-002]]。

## Origin 需求来源

用户新提出的需求：现场仓位锁是电磁铁，DO 为 1 时锁一直打开，DO 为 0 时电磁铁断电锁自动闩上；现场驱动 DO 的 IO 模块可能是电平输出，也可能是脉冲输出（脉冲继电器模块），模拟器需要能还原两种驱动方式的差异。设计判断（按点位独立配置、锁状态镜像 DO 电平）详见 [[dr-010-do-control-mode|DR-010]]。

## Acceptance Criteria 验收标准

- JSON 配置中每个 DO 点位除模块和通道映射外，可独立设置 `control_mode: Level | Pulse` 和合法范围内的 `pulse_width_ms`；两者纳入 JSON Schema、完整示例及启动/热重载严格校验。
- 启动时，配置默认值初始化模板声明的 DO 工作模式和脉冲宽度寄存器；运行期间寄存器当前值是控制模式和脉宽的唯一权威来源。
- 主系统对 DO 工作模式或脉冲宽度 RW 寄存器的合法写入立即生效；非法模式或超出模板范围的脉宽写入按协议失败且保留原值。
- reset 将 DO 电平、工作模式寄存器和脉冲宽度寄存器恢复到当前有效配置的默认值，不读取 DO 上电状态寄存器。
- 配置保存后立即热重载：新默认值供后续 reset 使用且不覆盖既有通道当前运行时寄存器值；新增加的通道立即按新默认值初始化。
- 电平模式：DO 值严格跟随主系统的最近一次写入，模拟器不做任何自动改变。
- 脉冲模式：每次有效写入 DO=1 均触发或重触发脉冲；重触发时取消原到期时刻，并从最后一次有效 ON 写入时刻起按当时运行时脉宽重新完整计时。写入被协议校验拒绝时不得重触发。
- 该 DO 对应的锁状态（DI）反馈与 DO 当前值保持同步（DO=1→解锁，DO=0→锁定），包括脉冲模式下的自动复位场景。
- 除 [[fr-003-exception-scenario-simulation|FR-003]] / [[dr-014-fault-injection-mirror-exception|DR-014]] 明确允许的故障注入外，锁状态 DI 不得脱离 DO 当前电平。

## Related Use Case 关联用例

无直接对应，属于模拟器还原硬件驱动特性的需求。

## Verification 验证方式

- **TC-FR-012-001（编号预留）**
  - **Given** 配置为 Pulse 且脉宽为 500 ms 的 DO 通道
  - **When** 启动模拟器后读取对应工作模式与脉冲宽度寄存器
  - **Then** 寄存器分别为 Pulse 和 500 ms，DO 初始电平为配置默认值
- **TC-FR-012-002（编号预留）**
  - **Given** Pulse 模式 DO 已由一次有效 ON 写入开始计时
  - **When** 超时前再次有效写入 ON
  - **Then** 原计时被替换，DO 从最后一次 ON 起经过完整运行时脉宽后才复位为 OFF
- **TC-FR-012-003（编号预留）**
  - **Given** 模拟器已启动且主系统已合法修改工作模式和脉宽寄存器
  - **When** 后续触发对应 DO
  - **Then** 行为采用寄存器当前模式和脉宽，而不是配置初始值
- **TC-FR-012-004（编号预留）**
  - **Given** 运行时寄存器值已偏离当前有效配置默认值
  - **When** 调用 reset
  - **Then** DO 电平、工作模式与脉宽均恢复为配置默认值，锁状态 DI 同步镜像 DO
- **TC-FR-012-005（编号预留）**
  - **Given** 运行中的通道已有合法运行时模式和脉宽
  - **When** 保存并成功热重载新的模式或脉宽默认值
  - **Then** 当前运行时寄存器值不被覆盖，随后 reset 使用新默认值

## Related 关联

[[fr-001-configurable-slot-count-and-io-mapping|FR-001]]（点位地址映射）、[[fr-002-slot-state-machine-normal-flow|FR-002]]（锁状态与 DO 电平的镜像关系）、[[fr-003-exception-scenario-simulation|FR-003]]（镜像关系的故障注入例外）、[[fr-010-automation-test-infrastructure|FR-010]]（reset）、[[fr-013-configurable-register-table-template|FR-013]]（工作模式与脉宽寄存器定义）、[[dr-010-do-control-mode|DR-010]]、[[dr-011-full-register-table-fidelity|DR-011]]、[[dr-014-fault-injection-mirror-exception|DR-014]]、[[dr-015-do-power-on-state-vs-reset|DR-015]]。
