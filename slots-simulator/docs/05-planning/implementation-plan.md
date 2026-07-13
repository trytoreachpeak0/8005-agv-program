# slots-simulator 实施计划模板

> 状态：Draft  
> 计划负责人：TODO  
> 开始日期：YYYY-MM-DD  
> 目标日期：YYYY-MM-DD

## 1. 计划原则

- 每个阶段都必须产生可运行、可测试的增量。
- 先实现纯 Core，再接协议和 UI。
- AI 每次只领取边界清楚、可独立验收的小任务。
- 未写清输入、输出和验收命令的任务不能进入开发。
- 不把未来 CI、业务系统或 UI 美化混入首期。

## 2. 开工前检查

- [ ] [`../03-design/architecture.md`](../03-design/architecture.md) 已评审
- [ ] [`../03-design/slot-state-machine.md`](../03-design/slot-state-machine.md) 无关键 TODO
- [ ] [`../03-design/modbus-implementation-spec.md`](../03-design/modbus-implementation-spec.md) 地址换算已确定
- [ ] [`../03-design/control-api.openapi.yaml`](../03-design/control-api.openapi.yaml) 通过校验
- [ ] [`../03-design/configuration-spec.md`](../03-design/configuration-spec.md) 已产生 JSON Schema 和示例
- [ ] [`../04-testing/test-plan.md`](../04-testing/test-plan.md) 已建立 P0 测试
- [ ] 第三方依赖已有决策记录

## 3. 里程碑

### M0：工程骨架与质量门禁

目标：解决方案可以构建和测试。

任务：

- 创建 .NET 8 solution 和项目。
- 建立依赖方向约束。
- 配置格式化、nullable、分析器和测试框架。
- 添加最小构建/测试说明。

验收：

```powershell
dotnet build
dotnet test
```

完成定义：零编译错误，基础测试可运行。

### M1：Core 状态模型

目标：无网络条件下完成仓位规则。

任务：

- SlotSnapshot 和状态变量
- 动作 Guard
- 占用推导
- 故障模型
- per-slot 串行化
- 可注入时间和 Pulse 计时器
- 完整 reset

验收：FR-002、FR-003、FR-004、FR-012 的核心单元测试通过。

### M2：配置系统

目标：合法配置可加载，非法配置被准确拒绝。

任务：

- JSON 模型
- JSON Schema
- 语义校验
- 最小和多模块示例
- 配置快照
- 原子热重载事务

验收：FR-001、FR-011、FR-013、FR-014 配置测试通过。

### M3：Modbus TCP

目标：主系统能像连接真实模块一样连接模拟器。

任务：

- 寄存器模板和 RegisterBank
- 地址换算
- 七个功能码
- 权限和异常码
- DO/DI 动态行为
- 多模块独立端点
- 批量写原子性

验收：协议测试矩阵通过，可使用独立客户端读写。

### M4：HTTP/JSON API

目标：自动化脚本可驱动所有人工/环境动作。

任务：

- 按 OpenAPI 实现端点
- 错误模型
- 批量遮挡和全空闲
- 故障注入/清除
- reset、状态查询、健康/就绪

验收：OpenAPI 契约测试和 FR-006、FR-010 测试通过。

### M5：Headless Host

目标：无 WPF 独立运行。

任务：

- 命令行参数
- 配置路径
- 结构化日志
- 启动就绪
- Ctrl+C/终止信号
- 端口释放

验收：FR-008、FR-009 生命周期测试通过。

### M6：WPF

目标：开发可视化操作和完整配置编辑。

任务：

- 分面布局
- 状态实时刷新
- 四种物理动作
- 故障操作
- 配置编辑和实时校验
- 原子保存及热重载

验收：FR-007、FR-011 关键场景通过。

### M7：端到端场景

目标：覆盖首批 UC 所需硬件条件。

任务：

- UC-001 正常和异常
- UC-002 前置组合
- UC-005 取出
- UC-006 全空闲
- UC-010 终点站取出
- 多实例/多模块

验收：FR→TC 追溯中所有首期条目通过。

## 4. AI 任务卡模板

每次让 AI 开发时，复制以下格式：

```markdown
任务：实现 [具体能力]

输入文档：
- FR/DR：
- 设计章节：
- OpenAPI/Schema：

允许修改：
- src/...
- tests/...

禁止修改：
- 协议契约
- 其他里程碑代码

行为要求：
1.
2.

验收：
- 运行命令：
- 必须通过的测试：
- 预期输出：

完成后请报告：
- 修改文件
- 关键设计
- 验证结果
- 未解决问题
```

## 5. 单任务拆分示例

不推荐：

> “把 Modbus 模拟器全部写完。”

推荐：

1. 实现寄存器地址描述和值存储，不接网络。
2. 实现权限与异常映射测试。
3. 接入 `0x01/0x02/0x03` 读取。
4. 接入单点写。
5. 接入批量写和原子性。
6. 接入 DO/DI 动态副作用。
7. 增加第二个模块端点集成测试。

## 6. 风险与应对

| 风险 | 信号 | 应对 |
| --- | --- | --- |
| 地址差一 | 与真机/客户端读数不一致 | 先锁定地址换算测试向量 |
| 网络库泄漏到 Core | 单元测试需启动网络 | 强制依赖方向 |
| reset 后旧任务回写 | 测试偶发失败 | 取消令牌+版本号 |
| 热重载部分成功 | 磁盘/运行态不一致 | 预检+原子事务 |
| AI 一次改动过大 | 难以评审、测试不全 | 使用任务卡和文件范围 |

## 7. 进度表模板

| 里程碑 | 状态 | 负责人 | 开始 | 完成 | 阻塞 |
| --- | --- | --- | --- | --- | --- |
| M0 | Not Started | TODO | | | |
| M1 | Not Started | TODO | | | |
| M2 | Not Started | TODO | | | |
| M3 | Not Started | TODO | | | |
| M4 | Not Started | TODO | | | |
| M5 | Not Started | TODO | | | |
| M6 | Not Started | TODO | | | |
| M7 | Not Started | TODO | | | |

## 8. 完成定义

一个任务只有同时满足以下条件才算完成：

- 实现符合对应 FR、DR 和设计规格。
- 新增/更新自动化测试。
- 构建与相关测试通过。
- 无新增诊断错误。
- 文档契约与代码一致。
- 不留下未记录的 TODO 或临时绕过。
