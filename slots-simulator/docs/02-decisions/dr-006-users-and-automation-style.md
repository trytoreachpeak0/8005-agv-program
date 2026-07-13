---
id: DR-006
type: decision-record
title: "使用者与自动化测试形式——仅供开发自测，脚本/API 驱动"
status: decided
created: 2026-07-09
updated: 2026-07-10
related_fr: ["FR-003", "FR-006", "FR-007", "FR-010"]
related_uc: ["UC-001", "UC-002", "UC-005", "UC-006", "UC-010", "UC-018"]
aliases: ["DR-006"]
---

# DR-006 使用者与自动化测试形式——仅供开发自测，脚本/API 驱动

## Decision 决策

模拟器仅服务邵正宇、王昆两人的开发自测，不面向客户演示，当前不要求接入正式 CI 流水线；自动化测试的形式是开发自己编写测试脚本调用模拟器的控制 API，不依赖人工点击 GUI。

控制 API 的协议确定为 **HTTP/JSON**，默认仅监听 `localhost`。如需跨主机访问，必须通过显式配置修改监听地址，不把对外暴露作为默认行为。

API 表示操作员/环境能够施加的物理动作，提供开门、关门、放料、取出、批量设置光幕、全空闲、完整 reset、故障注入与故障清除等能力；**不提供"开锁" API**。开锁是被测主系统通过 Modbus 写 DO 发出的控制命令，若 API/WPF 绕过 Modbus 直接开锁，就无法验证主系统 IO 控制链路。WPF 手动操作同样复用这些 HTTP/JSON 语义，不另开后门。

## Rationale 理由

用户选择"dev-self-test"和"script-api"，明确当前阶段的目标是替代开关门、放取物料等人工动作，而不是搭建完整的 CI/客户演示体系；GUI（[[fr-007-wpf-visualization-panel|FR-007]]）仅作为日常联调的辅助手段保留。将"开锁"保留在 Modbus 控制面，能确保自动化场景确实经过被测主系统的 DO 指令链路。

> 后续 [[dr-008-ci-readiness|DR-008]] 对"当前不要求接入正式 CI"这一点做了补充：不要求现在就接入，但架构上要保留可能性。

## Alternatives Considered 备选方案

曾考虑"也需要给客户/甲方演示，界面要更直观美观"和"需要接入 CI，无 GUI 情况下也能被脚本跑"两个更重的选项，用户未选择，明确当前只是开发自用。

## Related 关联

[[fr-003-exception-scenario-simulation|FR-003]]、[[fr-006-automation-control-api|FR-006]]、[[fr-007-wpf-visualization-panel|FR-007]]、[[fr-010-automation-test-infrastructure|FR-010]]
