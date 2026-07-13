---
id: DR-007
type: decision-record
title: "多 AGV 支持——单实例单 AGV，多台用多实例"
status: decided
created: 2026-07-09
updated: 2026-07-10
related_fr: ["FR-008"]
related_uc: []
aliases: ["DR-007"]
---

# DR-007 多 AGV 支持——单实例单 AGV，多台用多实例

## Decision 决策

一个模拟器实例只模拟一台 AGV 的仓位集合；需要同时模拟多台 AGV 时启动多个独立实例（各自不同端口/配置）。

## Rationale 理由

> **更新说明（2026-07-10）**：本条理由最初写的是"现场一台 AGV 对应一个 IO 模块"，该说法已被 [[dr-012-multi-io-module-support|DR-012]] 更新确认的现场事实推翻——一台 AGV 实际需要多个物理 IO 模块才能覆盖全部仓位。本决策"单实例单 AGV"的结论本身不受影响（DR-012 已说明两者是不同层次的问题，互不冲突），仅更正下面第 1 条理由的表述，避免继续误导读者。

1. 架构上仍然贴合"一个进程 = 一台 AGV"的映射关系——但这不等于"一个进程 = 一个 IO 模块"：一台 AGV 内部可能需要多个物理 IO 模块才能覆盖全部仓位（详见 [[dr-012-multi-io-module-support|DR-012]]）。"一个进程模拟一台 AGV"与"一台 AGV 对应几个 IO 模块"是两个独立的层次，本决策只解决前者，后者由 DR-012/[[fr-014-multi-io-module-simulation|FR-014]] 负责。
2. 用户本人指出"Modbus slave 也是一个进程对应一个 Modbus 的模拟设备"，与单实例单 AGV 的方案在概念上一致，不需要额外的多设备抽象层。（同样需要注意：这里的"一个 Modbus 的模拟设备"现在应理解为"一个进程内可同时模拟多个 Modbus 设备端点"，即 DR-012/FR-014 的多模块模型，而不是一个进程只对应一个 Modbus 端点。）
3. 状态隔离更彻底：两人各自调试不同 AGV 场景时不会互相干扰；一个实例卡死不影响其他实例。
4. 当前范围明确不涉及跨 AGV 协同场景（那属于 RIOT/调度层职责，见 [[dr-002-simulation-scope|DR-002]]），因此不需要在单实例内做多 AGV 建模。

## Alternatives Considered 备选方案

曾提出"单个实例内部同时模拟多台 AGV（内部维护 AGV 列表）"的方案，优点是测试脚本只需连一个入口、跨车协同场景编排更方便，但因协议层通常一个端口对应一个设备、多设备建模需要额外抽象层，且当前不涉及跨车协同场景，未采纳。

## Related 关联

[[fr-008-single-instance-single-agv|FR-008 单实例单 AGV]]、[[dr-012-multi-io-module-support|DR-012 现在就支持多 IO 模块拼接]]（两者是不同层次的问题，见上方更新说明）
