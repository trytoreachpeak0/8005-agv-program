# 02-decisions 决策记录

本目录存放 `slots-simulator` 需求澄清过程中与用户（邵正宇）确认的关键决策，编号格式为 `DR-001`、`DR-002` ...（Decision Record，决策记录）。记录目的是避免后续遗忘"为什么这么定"，格式参考根目录 UC 文档的"经与用户确认"惯例。

新建决策记录时，参照 [`../_templates/template-decision-record.md`](../_templates/template-decision-record.md) 指向的根目录模板结构手动创建，不要复制模板内容到本目录维护第二份。`decision-record` 这个文档类型本身也是因为本子项目的需要才新增的，但统一维护在根目录 `requirement-documents/_templates/`，供仓库内其他子项目复用。

## 清单

- [[dr-001-tech-stack|DR-001 技术栈与 WPF 完整配置编辑/热重载]]
- [[dr-002-simulation-scope|DR-002 模拟范围——只模拟仓位 IO，不模拟 AGV 移动/RIOT]]
- [[dr-003-first-batch-scenarios|DR-003 首批覆盖场景、构造方式与术语边界]]
- [[dr-004-configurable-slot-count|DR-004 仓位数量——不设固定上限，严格校验实际边界]]
- [[dr-005-modbus-protocol-fidelity|DR-005 Modbus 功能码、动态寄存器与批量写原子性]]
- [[dr-006-users-and-automation-style|DR-006 HTTP/JSON 自动化 API——只模拟人工/环境动作]]
- [[dr-007-multi-agv-support|DR-007 多 AGV 支持——单实例单 AGV，多台用多实例]]
- [[dr-008-ci-readiness|DR-008 CI 接入能力与业务超时职责边界]]
- [[dr-009-slot-layout-model|DR-009 仓位版面布局模型——任意 N 个面、矩形跨格与并排展示]]
- [[dr-010-do-control-mode|DR-010 DO 运行时参数、脉冲重触发与仓位并发]]
- [[dr-011-full-register-table-fidelity|DR-011 JSON+Schema 寄存器模板与动态核心]]
- [[dr-012-multi-io-module-support|DR-012 现在就支持多 IO 模块拼接]]
- [[dr-013-door-state-not-independent-io-point|DR-013 门状态与占用状态均为派生状态]]
- [[dr-014-fault-injection-mirror-exception|DR-014 点位脱钩与模块断连/不响应故障，可显式清除]]
- [[dr-015-do-power-on-state-vs-reset|DR-015 上电寄存器、配置默认值与完整 reset 边界]]
