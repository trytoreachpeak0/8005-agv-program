# 01-requirements 功能需求

本目录存放 `slots-simulator` 的功能需求文档，编号格式为 `FR-001`、`FR-002` ...（本子项目独立编号，不与根目录 `requirement-documents/04-functional-requirements/` 混用）。

新建功能需求时，参照 [`../_templates/template-functional-requirement.md`](../_templates/template-functional-requirement.md) 指向的根目录模板结构手动创建，不要复制模板内容到本目录维护第二份。

## 清单

- [[fr-001-configurable-slot-count-and-io-mapping|FR-001 可配置仓位数量与 IO 点位映射]]
- [[fr-002-slot-state-machine-normal-flow|FR-002 仓位状态机与正常流程]]
- [[fr-003-exception-scenario-simulation|FR-003 异常场景模拟能力]]
- [[fr-004-mis-stored-product-retrieval|FR-004 取出纠错场景支持]]
- [[fr-005-modbus-tcp-slave-protocol|FR-005 Modbus TCP Slave 协议层]]
- [[fr-006-automation-control-api|FR-006 自动化控制 API]]
- [[fr-007-wpf-visualization-panel|FR-007 WPF 可视化面板]]
- [[fr-008-single-instance-single-agv|FR-008 单实例单 AGV]]
- [[fr-009-headless-host|FR-009 无 GUI 独立运行能力（Headless Host）]]
- [[fr-010-automation-test-infrastructure|FR-010 自动化测试基础设施能力]]
- [[fr-011-configurable-slot-layout|FR-011 可配置仓位版面布局]]
- [[fr-012-do-pulse-level-control-mode|FR-012 可配置 DO 点位脉冲/电平控制模式]]
- [[fr-013-configurable-register-table-template|FR-013 可配置寄存器表模板与 DO/DI 数量上限]]
- [[fr-014-multi-io-module-simulation|FR-014 多 IO 模块实例模拟]]
- [[fr-015-destination-station-unload-support|FR-015 终点站取出流程支持]]
