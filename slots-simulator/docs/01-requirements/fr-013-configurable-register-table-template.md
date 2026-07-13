---
id: FR-013
type: functional-requirement
title: "可配置寄存器表模板与 DO/DI 数量上限"
status: review
created: 2026-07-10
updated: 2026-07-10
related_uc: []
related_dr: ["DR-005", "DR-011", "DR-015"]
related_fr: ["FR-001", "FR-005", "FR-010", "FR-011", "FR-012", "FR-014"]
aliases: ["FR-013"]
---

# FR-013 可配置寄存器表模板与 DO/DI 数量上限

## Description 需求描述

IO 模块的寄存器布局定义为 JSON 格式的可配置"模块类型模板"（如按型号命名），而不是把某一具体型号的寄存器地址写死在代码里。模板需完整覆盖真实设备说明书里的寄存器表——模块信息类（MAC 地址、设备型号、版本号）、网络配置类（IP、端口、子网掩码、网关、服务器/客户端模式等）、DO 相关（状态、上电状态、工作模式电平/脉冲——对应 [[fr-012-do-pulse-level-control-mode|FR-012]]、脉冲宽度）、DI 相关（当前值、正/负脉冲有效状态、脉冲计数、电平变化计数、滤波器参数、自动清零）。

首个模板以 [reference/C2000-A2-KDDA0A0-AD6_寄存器表.md](../reference/C2000-A2-KDDA0A0-AD6_寄存器表.md) 为依据建立。模板中声明的 DO 数量与 DI 数量，是该型号模块的硬性上限：仓位的 DO/DI 点位映射（[[fr-001-configurable-slot-count-and-io-mapping|FR-001]]）不能指向超出模板范围的通道。

只有 DO 当前值、DI 当前值、DO 工作模式和 DO 脉冲宽度具有模拟动态语义。模板中其余 RW 寄存器按权限和数据范围支持写入后读回保存值，但不触发网络重绑定、计数、滤波、自动清零或其他设备副作用；其余 RO 寄存器始终返回模板或模块实例覆盖的值。特别地，"DO 上电状态"寄存器组只保存 RW 值，不驱动模拟器的启动或 reset；该关系详见 [[dr-015-do-power-on-state-vs-reset|DR-015]]。

## Origin 需求来源

用户提供了真实 IO 模块（康耐德 C2000-A2-KDDA0A0-AD6）的完整寄存器表文档，确认寄存器位置是固定的、且模块的 DO/DI 数量有限（16 个 DO、16 个 DI）。设计判断（做成可配置模板、完整还原整份寄存器表、DO/DI 数量作为硬性上限）详见 [[dr-011-full-register-table-fidelity|DR-011]]。

## Acceptance Criteria 验收标准

- 寄存器表以 JSON 模板提供（而不是写死在代码常量里），修改/新增模板不需要改代码；提供模板 JSON Schema 和覆盖首个硬件模板全部字段的完整示例。
- 模板及实例配置可由 WPF 完整编辑并保存；保存成功后立即热重载。启动和热重载执行相同的 JSON Schema 与业务规则严格校验；失败时分别拒绝启动或原子拒绝变更。
- 模板需完整覆盖来源说明书里列出的每一类寄存器（地址、个数、权限、数据范围/说明、适用功能码）。
- 模板中定义的 DO 数量、DI 数量是明确的非负整数（如 16、16）；模拟器不额外设置固定通道总数上限，但每个模块实例严格受其模板声明的硬件通道数约束。
- 仓位 IO 点位映射（[[fr-001-configurable-slot-count-and-io-mapping|FR-001]]）引用某个模块通道时，若通道序号超出该模块所套用模板声明的 DO/DI 数量，视为配置错误，需要有明确的报错/拒绝行为，不能静默接受。
- 模板严格校验寄存器地址与数量合法、地址区间不重叠、权限与适用功能码一致、默认值位于数据范围内，并校验 DO/DI/模式/脉宽寄存器组与声明通道数一致；错误包含模板和字段路径。
- 仅 DO 当前值、DI 当前值、DO 工作模式、DO 脉冲宽度参与运行时动态行为；其中工作模式和脉宽的权威性、热重载与 reset 规则由 [[fr-012-do-pulse-level-control-mode|FR-012]] 定义。
- 除上述四类动态寄存器外，RW 寄存器仅校验、保存并读回写入值，不产生模拟副作用；RO 寄存器拒绝写入并返回模板默认值或模块实例覆盖值。
- 热重载对寄存器地址、权限、数量或端点拓扑的修改必须原子应用；无法安全应用时整次拒绝并保持所有模块的上一有效模板与服务状态。

## Related Use Case 关联用例

无直接对应，属于模拟器还原真实硬件寄存器布局的需求。

## Verification 验证方式

- **TC-FR-013-001（编号预留）**
  - **Given** 首个硬件模板的完整 JSON 示例
  - **When** 按 JSON Schema 和业务规则加载模板
  - **Then** 每类说明书寄存器均可按声明地址、权限和功能码访问
- **TC-FR-013-002（编号预留）**
  - **Given** 模板存在地址区间重叠、默认值越界或动态寄存器组数量与通道数不一致
  - **When** 启动或热重载该模板
  - **Then** 配置被整体拒绝并返回模板及字段路径，运行中的实例不发生部分变化
- **TC-FR-013-003（编号预留）**
  - **Given** 一个非动态 RW 寄存器和一个 RO 寄存器
  - **When** 分别执行合法写入
  - **Then** RW 值被保存并可读回但不产生副作用，RO 写入被拒绝且读取仍返回模板或实例值
- **TC-FR-013-004（编号预留）**
  - **Given** 仓位映射引用超出模块模板 DO/DI 数量的通道
  - **When** 启动或热重载配置
  - **Then** 配置被拒绝，错误指出模块、点位和允许的通道范围
- **TC-FR-013-005（编号预留）**
  - **Given** 模板内 DO/DI 通道数合法且系统资源足够
  - **When** 配置任意数量的模块实例以扩展总通道数
  - **Then** 模拟器不施加固定总通道数上限，每个实例仍严格遵守自身模板上限

## Related 关联

[[fr-001-configurable-slot-count-and-io-mapping|FR-001]]（点位映射引用本 FR 定义的模板与硬件通道上限）、[[fr-005-modbus-tcp-slave-protocol|FR-005]]（协议权限与功能码）、[[fr-010-automation-test-infrastructure|FR-010]]（reset）、[[fr-011-configurable-slot-layout|FR-011]]（统一 JSON、Schema、WPF 编辑和热重载能力）、[[fr-012-do-pulse-level-control-mode|FR-012]]（DO 工作模式与脉宽动态语义）、[[fr-014-multi-io-module-simulation|FR-014]]（每个模块实例套用一份模板）、[[dr-005-modbus-protocol-fidelity|DR-005]]、[[dr-011-full-register-table-fidelity|DR-011]]、[[dr-015-do-power-on-state-vs-reset|DR-015]]。
