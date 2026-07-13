---
id: DR-012
type: decision-record
title: "现在就支持多 IO 模块拼接"
status: decided
created: 2026-07-10
updated: 2026-07-10
related_fr: ["FR-014", "FR-001", "FR-005"]
related_uc: ["UC-001", "UC-005", "UC-010", "UC-018"]
aliases: ["DR-012"]
---

# DR-012 现在就支持多 IO 模块拼接

## Decision 决策

一个模拟器实例（一台 AGV）现在就要支持配置模拟多个物理 IO 模块，每个模块各自是独立的 Modbus TCP 服务端，不作为"以后再扩展"的预留能力。

各模块端点默认仅绑定 `localhost`，端口必须在实例内唯一；跨主机联调时可显式配置其他监听地址。模块数量不设置固定软件上限，但配置必须通过端口冲突、模板容量和主机资源边界校验，规则见 [[dr-004-configurable-slot-count|DR-004]]。

## Rationale 理由

已知实际仓位数量会超过单个 IO 模块 16 DO/16 DI 的容量（见 [reference/C2000-A2-KDDA0A0-AD6_寄存器表.md](../reference/C2000-A2-KDDA0A0-AD6_寄存器表.md)），一台 AGV 需要用多个物理 IO 模块才能覆盖全部仓位；每个模块是独立的 Modbus TCP 服务端（对应说明书里"IO 模块工作模式"寄存器 40151 的"服务器模式"，真实设备各自有自己的 IP）。这不是一个未来可能出现的边界情况，而是当前已知会发生的真实部署形态，如果现在按"单模块"假设去实现，后续几乎必然返工，因此现在就按多模块拼接设计。

这与 [[dr-007-multi-agv-support|DR-007]]（一个进程实例模拟一台 AGV，多台 AGV 用多实例）不冲突，是两层不同的问题：DR-007 管的是"一台 AGV 用几个进程"，本决策管的是"一台 AGV 内部要模拟几个物理 IO 模块"。一个模拟器进程（一台 AGV）内部可以同时维护多个 IO 模块的模拟状态。

## Alternatives Considered 备选方案

- 曾考虑先按单模块（16 DO/16 DI）实现，等真的遇到仓位数超限再扩展——因已经明确知道会超限，选择现在直接支持多模块，避免可预见的返工。

## Related 关联

[[fr-014-multi-io-module-simulation|FR-014]]、[[fr-001-configurable-slot-count-and-io-mapping|FR-001]]、[[fr-005-modbus-tcp-slave-protocol|FR-005]]、[[dr-007-multi-agv-support|DR-007]]
