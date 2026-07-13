---
id: FR-009
type: functional-requirement
title: "无 GUI 独立运行能力（Headless Host）"
status: review
created: 2026-07-09
updated: 2026-07-10
related_uc: ["UC-001", "UC-002", "UC-005", "UC-006", "UC-010"]
related_dr: ["DR-006", "DR-007", "DR-008", "DR-012"]
related_fr: ["FR-005", "FR-006", "FR-007", "FR-008", "FR-010", "FR-014"]
aliases: ["FR-009"]
---

# FR-009 无 GUI 独立运行能力（Headless Host）

## Description 需求描述

模拟器核心逻辑（状态机、多个 Modbus TCP Slave、HTTP/JSON 控制 API）可以在不启动 WPF 界面的情况下独立运行（如控制台程序），供未来接入 CI 或其他无人值守场景使用。WPF 面板（[[fr-007-wpf-visualization-panel|FR-007]]）只是核心逻辑的一种可选客户端，不是必须的启动入口。Headless 与 WPF 模式加载同一份 JSON 配置并使用同一套运行核心；控制 API 默认仅绑定 localhost。

## Origin 需求来源

服务于 `../00-vision/vision-and-scope.md` 第 2 节第 8 点"CI 接入能力（架构预留）"；理由详见 [[dr-008-ci-readiness|DR-008]]。

## Acceptance Criteria 验收标准

- 提供一种不依赖 WPF、不需要桌面会话即可启动的方式，加载与 WPF 模式相同的核心逻辑（状态机、全部 Modbus Slave、控制 API）。
- 该方式下 Modbus Slave 和控制 API 的行为与 WPF 模式下完全一致，被测系统无法区分二者差异。
- Headless 模式支持同仓位动作串行、不同仓位动作并行，行为与 WPF 模式一致。
- 控制 API 默认仅监听 localhost；只有配置显式指定其他监听地址时才允许远程访问。
- Headless 模式不设置固定模块数或仓位数上限，规模约束与 WPF 模式一致，仅来自硬件模板、端口、映射和机器资源。
- Headless 模式能加载 WPF 保存的 JSON 配置；WPF 保存并热重载配置不要求 Headless 进程同步接收该变更，独立进程在各自加载配置时生效。
- 当前只要求这个能力存在，不要求真正接入某个 CI 系统。

## Related Use Case 关联用例

为 UC-001、UC-002、UC-005、UC-006、UC-010 提供无人值守自动化运行载体，不直接实现主系统业务流程。

## Verification 验证方式

- **TC-FR-009-001（待建立）**：Given 一份包含多个 IO 模块和仓位的 JSON 配置；When 在无桌面会话环境启动 Headless Host；Then 所有 Modbus 端点、状态机和 HTTP/JSON 控制 API 均就绪且不启动 WPF。
- **TC-FR-009-002（待建立）**：Given WPF 与 Headless 分别加载同一配置和初始状态；When 对两者执行相同 Modbus 写入及 API 动作序列；Then 返回值、DI/DO、状态迁移和错误响应一致。
- **TC-FR-009-003（待建立）**：Given Headless Host 使用默认监听配置；When 从本机和非本机访问控制 API；Then 本机可访问而非本机不可访问。
- **TC-FR-009-004（待建立）**：Given 模板、端口和资源允许多个模块及大量仓位；When Headless Host 加载该配置并并发操作两个仓位；Then 配置不因固定数量上限被拒绝，同仓位请求串行而不同仓位请求可并行。
