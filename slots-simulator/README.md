# slots-simulator

多仓位 AGV 的仓位（格口）硬件模拟器，用于替代 Modbus Poll/Slave 等通用调试工具，为开发联调和自动化测试提供支持。

## 为什么需要这个项目

真实的多仓位仓门开关、物料放取都依赖人工操作，如果每次联调或回归测试都要人到现场手动开关仓门、放取产品，效率很低，也无法纳入持续集成。通用的 Modbus Slave 工具虽然能模拟寄存器读写，但无法模拟"开门→放料→关门"这类带时序和状态迁移的业务流程，也没有可编程的自动化能力。

本项目的目标：

1. **对被测系统透明**：在协议层（Modbus TCP）完全模拟真实 IO 模块的行为，被测系统的 IO 对接代码切换真实硬件/模拟器无需修改。
2. **可视化直观**：提供图形界面展示每个仓位的锁 / 门 / 光幕状态，便于开发日常联调（仅供内部自测，不面向客户演示）。
3. **自动化测试能力**：提供默认仅监听 `localhost` 的 HTTP/JSON 控制 API，允许测试脚本驱动“关门、放料、取出、故障注入/清除”等人工或环境动作，从而实现无人值守的自动化回归测试。开锁及弹簧自动弹门由被测主系统通过 Modbus 写 DO 触发，API 不提供绕过协议链路的开锁或开门入口。

**范围明确不包含**：AGV 移动状态模拟、RIOT/MES 对接模拟（本项目无硬件层面的移动安全联锁），以及单实例内的多 AGV 建模（多台 AGV 用多个实例分别模拟）。完整范围说明见 [`docs/00-vision/vision-and-scope.md`](./docs/00-vision/vision-and-scope.md)。

**关于 CI：** 当前阶段只服务开发自测，不搭建正式 CI 流水线，但核心逻辑（状态机、Modbus Slave、控制 API）的架构设计需要支持脱离 WPF 独立无界面运行，为未来接入 CI 预留空间，避免返工（见 FR-009、FR-010）。

**当前协议与配置基线：** Modbus TCP 计划支持 `0x01/02/03/05/06/0F/10`，核心动态寄存器为 DO、DI、DO 工作模式和 DO 脉冲宽度；配置采用 JSON + JSON Schema，WPF 计划提供完整配置编辑与校验后热重载。占用状态由光幕 DI 推导，业务超时和任务业务逻辑由主系统负责。详细边界以 [`docs/02-decisions/`](./docs/02-decisions/README.md) 为准。

## 技术栈

- **.NET 8**
- **WPF**（图形界面，用于可视化仓位状态与手动操作）

## 状态

关键需求与决策已澄清，仍有少量跨系统/测试项 TBD；代码尚未搭建，以上均为规划状态。

- 完整文档中心：[`docs/`](./docs/README.md)（愿景、需求、决策、设计、测试、实施计划）
- Agent 项目约定：[`AGENTS.md`](./AGENTS.md)

## 关联文档

- [UC-001 放入完工产品到仓位](../requirement-documents/03-use-cases/uc-001-load-completed-lot-into-slot.md)
- [UC-005 取出仓位中存错的产品](../requirement-documents/03-use-cases/uc-005-retrieve-mis-stored-product-from-slot.md)
- [UC-004 仓门开启安全联锁](../requirement-documents/03-use-cases/uc-004-slot-door-safety-interlock.md)（本模拟器不涉及，详见决策记录）
- [Vision and Scope](../requirement-documents/00-vision/vision-and-scope.md)
- [软件开发计划](../develop_plan/软件开发计划(2026-07-08至2026-07-31).md)
