# slots-simulator 架构设计模板

> 状态：Draft  
> 维护者：TODO  
> 最后更新：YYYY-MM-DD  
> 依据：FR-001～FR-015、DR-001～DR-015

## 1. 文档目的

说明系统如何拆分、模块如何协作、状态由谁维护，以及关键运行流程。本文回答“代码应该如何组织”，不重复需求文档中的业务背景。

## 2. 设计目标

- 模拟真实 IO 模块的 Modbus TCP 行为。
- WPF 与 Headless Host 共用同一套核心逻辑。
- 同一仓位操作串行，不同仓位可以并行。
- 配置、状态重置和故障注入具有确定性，便于自动化测试。

### 2.1 非目标

- 不实现 AGV 移动、MES、RIOT、任务和站点业务。
- 不在控制 API 中提供开锁能力。
- 不维护独立于光幕 DI 的占用状态。

## 3. 解决方案结构

> 学习提示：这里写“项目职责和依赖”，不要只列文件夹名称。

```text
SlotsSimulator.sln
├─ src/
│  ├─ SlotsSimulator.Core/          状态机、寄存器、配置、故障模型
│  ├─ SlotsSimulator.Modbus/        Modbus TCP 适配
│  ├─ SlotsSimulator.Api/           HTTP/JSON 控制 API
│  ├─ SlotsSimulator.Host/          Headless 进程入口
│  └─ SlotsSimulator.Wpf/           WPF 可视化与配置编辑
└─ tests/
   ├─ SlotsSimulator.UnitTests/
   ├─ SlotsSimulator.ProtocolTests/
   └─ SlotsSimulator.IntegrationTests/
```

### 3.1 依赖方向

```text
Wpf ─┐
Host ├─> Api ─┐
     └─> Modbus ├─> Core
               ┘
```

约束：

- `Core` 不引用 WPF、ASP.NET Core 或具体 Modbus 库。
- WPF 通过与自动化脚本相同的应用服务/API 操作状态，不直接修改寄存器。
- 协议层只负责协议转换，不复制仓位规则。

## 4. 核心模块

| 模块 | 职责 | 输入 | 输出 | 不负责 |
| --- | --- | --- | --- | --- |
| Slot Runtime | 仓位动作与顺序约束 | Modbus/API 事件 | 状态快照、领域事件 | 业务任务 |
| Register Bank | 地址、权限、原子读写 | Modbus 请求 | 寄存器值/异常 | HTTP 错误 |
| IO Mirror | DO/DI 正常镜像 | DO、实际遮挡 | 锁 DI、光幕 DI | 故障策略配置 |
| Fault Manager | 注入和清除故障 | API 命令 | 故障状态 | 主系统告警 |
| Configuration | Schema、语义校验、热重载 | JSON | 有效配置快照 | 自动修复错误配置 |

> TODO：为每个模块补充建议接口，例如 `ISlotRuntime`、`IRegisterBank`。

## 5. 关键数据模型

```text
SimulatorInstance
 ├─ AgvId
 ├─ Modules[]
 │   ├─ ModuleId
 │   ├─ Endpoint
 │   └─ RegisterBank
 └─ Slots[]
     ├─ SlotId
     ├─ IoMapping
     ├─ DoorState
     ├─ ActualObstruction
     └─ DerivedOccupancy
```

不变量：

1. `DerivedOccupancy = LightCurtainDI == Obstructed`。
2. 开锁命令仅来自 Modbus DO。
3. 故障注入是 DO/DI 或遮挡/DI 镜像的唯一例外。
4. 仓位映射必须引用存在的模块和合法通道。

## 6. 并发模型

- 每个仓位拥有独立串行命令队列或互斥边界。
- 不同仓位可以并行处理。
- Modbus 批量写必须先整体校验，再一次性提交。
- reset 和配置切换是实例级原子操作。
- 脉冲计时器回调必须携带版本/取消令牌，避免 reset 后旧回调写回。

> TODO：确定采用 `Channel<T>`、锁还是 Actor 模型，并说明理由。

## 7. 关键运行流程

### 7.1 启动

1. 读取 JSON。
2. 执行 JSON Schema 校验。
3. 执行跨字段和资源校验。
4. 创建 Core 状态。
5. 启动各模块 Modbus 端点。
6. 启动 HTTP API。
7. 全部端点可用后就绪探针返回 Ready。

### 7.2 完整 reset

1. 阻止新状态变更进入。
2. 取消延迟任务和脉冲计时器。
3. 清除仓位/模块故障。
4. 光幕恢复无遮挡，DO 恢复配置初值。
5. 模式和脉宽恢复当前有效配置默认值。
6. 其余寄存器恢复模板/实例默认值。
7. 原子发布新状态并恢复请求处理。

### 7.3 配置热重载

1. 在临时快照中校验并预创建资源。
2. 预检端口、模块和映射。
3. 原子持久化配置并切换运行态。
4. 任一步失败时，磁盘和运行态都保留旧版本。

## 8. 可观测性

- 日志字段：时间、实例、模块、仓位、来源、事件、旧状态、新状态、关联 ID。
- 健康检查：进程存活。
- 就绪检查：API 与全部启用的 Modbus 端点可接受请求。
- TODO：定义日志格式、级别和文件轮转策略。

## 9. 安全与部署

- 默认绑定 `localhost`。
- 改为局域网地址必须显式配置。
- 首期不做认证和 TLS；共享网络部署依赖防火墙。
- 多 AGV 使用多进程、独立配置和端口。

## 10. 待确认事项

- [ ] Modbus 库选型
- [ ] HTTP 框架和 OpenAPI 生成方式
- [ ] JSON Schema 校验库
- [ ] 日志库与输出格式
- [ ] 并发实现机制
- [ ] 热重载时现有 TCP 连接的处理策略

## 11. 完成标准

- 每个项目的职责和依赖方向无歧义。
- 关键流程能够对应到 FR 和测试用例。
- 所有待确认项已转为决策记录或明确延期。
