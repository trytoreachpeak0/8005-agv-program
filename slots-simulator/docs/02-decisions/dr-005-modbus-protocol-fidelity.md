---
id: DR-005
type: decision-record
title: "协议保真度——现在就实现 Modbus TCP Slave"
status: decided
created: 2026-07-09
updated: 2026-07-10
related_fr: ["FR-001", "FR-005"]
related_uc: ["UC-018"]
aliases: ["DR-005"]
---

# DR-005 协议保真度——现在就实现 Modbus TCP Slave

## Decision 决策

不做"先用简化 HTTP 内部 API、以后再补协议层"的过渡方案，直接实现 Modbus TCP Slave；IO 点位映射通过配置文件或界面配置，不写死。

协议首批明确支持标准功能码 `0x01`（读线圈）、`0x02`（读离散输入）、`0x03`（读保持寄存器）、`0x05`（写单线圈）、`0x06`（写单保持寄存器）、`0x0F`（写多线圈）和 `0x10`（写多保持寄存器）。首批需要参与运行时行为的核心动态寄存器为 DO、DI、DO 工作模式和 DO 脉冲宽度；其余寄存器仍按 [[dr-011-full-register-table-fidelity|DR-011]] 完整建模，但不因此虚构尚未确认的设备副作用。

单次 `0x0F`/`0x10` 批量写必须原子提交：请求内任一地址、值或硬件边界校验失败时，整批均不生效，不允许部分写入。并发到达时按 [[dr-010-do-control-mode|DR-010]] 的仓位串并行规则执行。

## Rationale 理由

用户判断"相当于实现一个 Modbus slave"，且 IO 对接代码本身也要照着寄存器表和仓位映射写，两边最好一起对齐，避免后续再返工加协议层。真实设备寄存器表已经提供并由 DR-011 选定为首个模板依据；仓位到"模块实例 + 通道"的项目级点位分配仍应保持可配置，以适配不同 AGV 布线，而不是继续以"真实点位表 TBD"作为理由。

## Alternatives Considered 备选方案

曾提议"先做简化版内部 API，等点位表定了再补协议层，更快出效果"，用户未采纳，选择现在就把协议层做对。

## Related 关联

[[fr-001-configurable-slot-count-and-io-mapping|FR-001]]、[[fr-005-modbus-tcp-slave-protocol|FR-005]]
