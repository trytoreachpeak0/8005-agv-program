---
id: FR-006
type: functional-requirement
title: "自动化控制 API"
status: review
created: 2026-07-09
updated: 2026-07-10
related_uc: ["UC-001", "UC-002", "UC-005", "UC-006", "UC-010", "UC-018"]
related_dr: ["DR-003", "DR-006", "DR-012", "DR-014"]
related_fr: ["FR-002", "FR-003", "FR-004", "FR-007", "FR-010", "FR-014"]
aliases: ["FR-006"]
---

# FR-006 自动化控制 API

## Description 需求描述

提供一套独立于 Modbus 协议、默认仅监听 localhost 的 HTTP/JSON 控制 API，代表人工操作、测试前置构造或故障注入，供开发编写自动化测试脚本调用。API 不提供“开锁”或“开门”动作；开锁只能由被测主系统通过 Modbus DO 下发，正常成功时弹簧自动弹门。面向仓位的人工动作是“关门、放料、取出”。

仓位是否占用不作为独立状态存储，始终由该仓位光幕 DI 推导：光幕有遮挡即为已占用，无遮挡即为空闲。API 支持批量设置指定仓位集合的光幕遮挡状态，以及一键将全部仓位设为空闲，用于构造 UC-002、UC-006 和异常流程的前置条件。

故障 API 支持按指定 IO 模块实例注入 Modbus TCP 主动断连或不响应，并支持显式清除；也支持 [[fr-003-exception-scenario-simulation|FR-003]] 定义的仓位级故障注入和清除。对不满足状态机前置条件的动作，API 返回明确的 4xx HTTP 错误和可机器解析的 JSON 错误码，且仓位状态、DI/DO、故障与计时器均保持不变。

## Origin 需求来源

服务于 `../00-vision/vision-and-scope.md` 第 2 节"自动化测试能力"目标；使用方式依据 [[dr-006-users-and-automation-style|DR-006]]（脚本/API 驱动，不依赖人工点击 GUI）。间接支撑 [[fr-002-slot-state-machine-normal-flow|FR-002]]~[[fr-004-mis-stored-product-retrieval|FR-004]] 所有场景的自动化编排。

## Acceptance Criteria 验收标准

- API 使用 HTTP/JSON，默认只绑定 localhost；除非配置显式修改监听地址，否则不能从非本机地址访问。
- 每个仓位的关门、放料、取出动作均有对应的可编程调用方式；API 和 WPF 均不提供开锁或开门动作，开锁只接受 Modbus DO，开门是开锁成功的机构结果。
- 占用状态不独立存储，所有查询和状态迁移中的"空闲/已占用"均由光幕 DI 当前值推导。
- 可一次提交多个仓位及各自目标遮挡值；也可一键将全部仓位光幕设为无遮挡，使全部仓位推导为空闲。
- 非法状态迁移返回明确的 4xx 状态码、JSON 错误码和原因，调用前后的所有运行状态完全一致。
- 可指定某个 IO 模块注入"主动断开 Modbus TCP 连接"或"保持连接但不响应"故障，并可按模块清除；未指定模块不受影响。
- 同一仓位的并发动作按接收顺序串行执行；不同仓位的动作可并行执行，不以全局锁相互阻塞。
- 开发可以不依赖 GUI（[[fr-007-wpf-visualization-panel|FR-007]]），仅通过脚本/代码调用控制 API 完整跑通一个 UC-001 正常流程 + 若干异常分支的测试序列。
- 控制 API（及复用它的 WPF 面板）可用于开发手动核对 IO 点位映射配置的正确性：通过 Modbus 下发某仓位开锁 DO 后观察对应锁状态 DI，或通过 API 触发某仓位光幕遮挡并观察软件侧读取到的点位编号，等价于根目录 [UC-018 IO 点位映射表核对测试](../../../requirement-documents/03-use-cases/uc-018-io-point-mapping-verification-test.md) 的核对方式，不需要另外开发专门的核对工具。

## Related Use Case 关联用例

服务于 UC-001、UC-002、UC-005、UC-006、UC-010 的自动化验证；其中 UC-002/UC-006 使用批量光幕与一键全空闲构造前置条件。根目录 [UC-018 IO 点位映射表核对测试](../../../requirement-documents/03-use-cases/uc-018-io-point-mapping-verification-test.md) 可直接使用本 API/WPF 面板完成核对。

## Verification 验证方式

- **TC-FR-006-001（待建立）**：Given 服务按默认配置启动；When 从本机调用 HTTP/JSON 状态接口并从非本机地址尝试连接；Then 本机请求可达，非本机请求不可达，且 API 清单中不存在开锁或开门接口。
- **TC-FR-006-002（待建立）**：Given 仓位未满足放料前置条件并记录其全部运行状态；When 调用放料接口；Then 返回明确的 4xx、JSON 错误码与原因，且状态、DI/DO、故障和计时器与调用前一致。
- **TC-FR-006-003（待建立）**：Given 多个仓位的光幕状态不同；When 批量设置各仓位遮挡值后调用一键全空闲；Then 批量设置逐仓位生效，随后全部光幕 DI 为无遮挡且全部仓位推导为空闲。
- **TC-FR-006-004（待建立）**：Given 实例配置两个 IO 模块且均有客户端连接；When 对模块 A 注入不响应、清除后再注入主动断连；Then 两种故障分别生效且均可清除，模块 B 全程正常响应。
- **TC-FR-006-005（待建立）**：Given 仓位 A、B 均可执行动作；When 同时向 A 提交两个动作并向 B 提交一个动作；Then A 的两个动作按接收顺序串行，B 可与 A 并行完成。
