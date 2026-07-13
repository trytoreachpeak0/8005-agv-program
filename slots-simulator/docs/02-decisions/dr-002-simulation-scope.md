---
id: DR-002
type: decision-record
title: "模拟范围——只模拟仓位 IO，不模拟 AGV 移动/RIOT"
status: decided
created: 2026-07-09
updated: 2026-07-09
related_fr: ["FR-002"]
related_uc: []
aliases: ["DR-002"]
---

# DR-002 模拟范围——只模拟仓位 IO，不模拟 AGV 移动/RIOT

## Decision 决策

模拟器只覆盖仓位硬件（电子锁、光幕）这一层，不模拟 AGV 本体移动状态，不对接/模拟 RIOT。

## Rationale 理由

用户确认本项目**没有硬件层面的移动安全联锁**——根目录 [UC-004 仓门开启安全联锁](../../../requirement-documents/03-use-cases/uc-004-slot-door-safety-interlock.md) 描述的"仓门开启期间检测 AGV 是否移动"这类联锁逻辑，如果存在，是主系统软件层的判断逻辑，不是仓位硬件本身要暴露的状态量，因此不需要模拟器提供"AGV 是否移动"这个信号。

## Alternatives Considered 备选方案

曾考虑"仓位 IO + 一个简化的 AGV 是否移动开关"和"仓位 IO + AGV 移动 + 简化 MES，端到端全链路模拟"两种更大范围的方案，均因上述理由未采用。

## Related 关联

[[fr-002-slot-state-machine-normal-flow|FR-002 仓位状态机与正常流程]]
