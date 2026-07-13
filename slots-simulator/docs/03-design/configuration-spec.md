# 配置规格模板

> 状态：Draft  
> 最后更新：YYYY-MM-DD  
> 需求依据：FR-001、FR-007、FR-011、FR-012、FR-013、FR-014

## 1. 目的

定义模拟器 JSON 配置的结构、默认值、校验规则和热重载语义。最终应从本文件生成或同步维护 `slots-simulator.schema.json`。

## 2. 配置原则

- 配置格式统一为 JSON。
- JSON Schema 负责类型、必填项和基本范围。
- 应用层负责跨对象引用、端口占用、映射冲突和资源预检。
- 不设置固定的模块数、仓位数上限，但必须受硬件模板和机器资源约束。
- 默认监听 `localhost`。
- WPF 保存采用原子事务；失败时磁盘和运行态都保留旧配置。

## 3. 顶层结构

```json
{
  "schemaVersion": "1.0",
  "instance": {},
  "api": {},
  "registerTemplates": [],
  "modules": [],
  "slots": [],
  "layout": {}
}
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `schemaVersion` | 是 | 配置结构版本 |
| `instance` | 是 | 单 AGV 实例标识和运行参数 |
| `api` | 是 | HTTP API 监听配置 |
| `registerTemplates` | 是 | IO 模块寄存器模板 |
| `modules` | 是 | 模块实例与 Modbus 端点 |
| `slots` | 是 | 仓位、映射、默认输出参数 |
| `layout` | 是 | WPF 分面网格布局 |

## 4. 完整示例

> 这是学习示例，不代表最终字段名已经决定。

```json
{
  "schemaVersion": "1.0",
  "instance": {
    "agvId": "AGV-8005-01"
  },
  "api": {
    "host": "localhost",
    "port": 5080
  },
  "registerTemplates": [
    {
      "templateId": "C2000-A2-KDDA0A0-AD6",
      "source": "../reference/C2000-A2-KDDA0A0-AD6_寄存器表.md",
      "doCount": 16,
      "diCount": 16,
      "registerMap": "TODO: 改为结构化地址段"
    }
  ],
  "modules": [
    {
      "moduleId": "io-front",
      "templateId": "C2000-A2-KDDA0A0-AD6",
      "modbus": {
        "host": "localhost",
        "port": 15021,
        "unitId": 1
      }
    },
    {
      "moduleId": "io-rear",
      "templateId": "C2000-A2-KDDA0A0-AD6",
      "modbus": {
        "host": "localhost",
        "port": 15022,
        "unitId": 1
      }
    }
  ],
  "slots": [
    {
      "slotId": "S01",
      "io": {
        "unlockDo": { "moduleId": "io-front", "channel": 1 },
        "lockStateDi": { "moduleId": "io-front", "channel": 1 },
        "lightCurtainDi": { "moduleId": "io-front", "channel": 2 }
      },
      "doDefaults": {
        "controlMode": "level",
        "pulseWidthMs": 500,
        "initialValue": false
      },
      "position": {
        "faceId": "front",
        "row": 1,
        "column": 1,
        "rowSpan": 1,
        "columnSpan": 2
      }
    }
  ],
  "layout": {
    "faces": [
      {
        "faceId": "front",
        "displayName": "前侧",
        "rows": 2,
        "columns": 4,
        "doorDirection": "left"
      }
    ]
  }
}
```

## 5. 字段定义模板

对每个字段都按以下格式补齐：

### `slots[].position`

- `faceId`：仓位所属面 ID，必填。
- `row`：仓位占用矩形左上角所在行，从 `1` 开始，必填。
- `column`：仓位占用矩形左上角所在列，从 `1` 开始，必填。
- `rowSpan`：连续跨越的基础格行数，正整数，默认值 `1`。
- `columnSpan`：连续跨越的基础格列数，正整数，默认值 `1`。
- 每个面采用统一尺寸的基础格；仓位占用区域固定为连续矩形，不支持任意格集合、绝对像素坐标或仓位级旋转。
- 未提供两个 span 字段的旧配置按 `1×1` 解析。

### `slots[].doDefaults.pulseWidthMs`

- 类型：integer
- 必填：是
- 单位：ms
- 默认值：TODO
- 最小/最大值：依据硬件表填写
- 热重载：影响后续写入；不覆盖当前运行时寄存器
- reset：恢复为当前有效配置中的该值
- 错误示例：负数、超出硬件范围、非整数

## 6. Schema 校验

应由 JSON Schema 覆盖：

- 必填字段和 `additionalProperties` 策略
- 字符串长度和格式
- 端口范围 `1..65535`
- 行列从 1 开始
- `rowSpan`、`columnSpan` 为正整数且默认值均为 `1`
- 枚举值，如 `level/pulse`
- 数字范围，如脉冲宽度
- 数组元素基本结构

## 7. 应用层语义校验

| 编号 | 规则 | 失败信息应包含 |
| --- | --- | --- |
| CFG-001 | `moduleId`、`slotId`、`templateId` 唯一 | 重复 ID 与路径 |
| CFG-002 | 模块引用的模板存在 | 模块和模板 ID |
| CFG-003 | 仓位映射引用的模块存在 | 仓位、字段、模块 ID |
| CFG-004 | 通道不超过模板 DO/DI 容量 | 通道值和允许范围 |
| CFG-005 | 同一模块同类点位不得重复映射 | 冲突仓位 |
| CFG-006 | 监听地址与端口组合不冲突 | 冲突模块/API |
| CFG-007 | 仓位矩形完全落在对应面网格内：`row + rowSpan - 1 <= rows` 且 `column + columnSpan - 1 <= columns` | 面、起始行列、span、允许边界 |
| CFG-008 | 同一面任意两个仓位的占用矩形不得覆盖同一基础格 | 两个冲突仓位及相交格范围 |
| CFG-009 | 启动/热重载前端口可绑定 | 地址、端口、系统错误 |
| CFG-010 | 主机资源足以启动新端点 | 资源类型和预算 |

## 8. 热重载语义

### 8.1 原子流程

1. 解析候选 JSON。
2. Schema 校验。
3. 语义校验。
4. 在临时上下文中预创建/预绑定资源。
5. 原子持久化文件并切换运行态。
6. 释放旧资源。

任一步失败：

- 不覆盖磁盘中的上一份有效配置。
- 不改变运行态。
- 返回可定位到字段或资源的错误。

### 8.2 运行状态迁移

> TODO：逐类定义热重载时如何处理现有状态。

| 变更 | 建议策略 |
| --- | --- |
| 仅布局变化 | 保留仓位运行状态 |
| 新增仓位 | 按默认空闲态创建 |
| 删除仓位 | 拒绝或删除；TODO 决策 |
| 修改 IO 映射 | TODO：保留物理状态还是重置该仓位 |
| 修改模块端口 | 预启动新端点后切换 |
| 修改 DO 默认值 | 只影响下次 reset，不覆盖当前运行值 |

### 8.3 跨格占用与冲突算法

仓位 `S` 覆盖的闭区间为：

```text
rows(S) = [row, row + rowSpan - 1]
columns(S) = [column, column + columnSpan - 1]
```

同一面内两个仓位 `A`、`B` 同时满足“行区间相交”和“列区间相交”时即发生重叠，整份候选配置必须拒绝。仅边界相邻但未共享基础格不算重叠。空白基础格允许存在。

热重载改变起始坐标或 span 时，按完整候选布局重新执行越界和两两重叠校验；任一错误都不得部分应用。

## 9. 配置版本与迁移

- `schemaVersion` 必填。
- 不支持的主版本必须拒绝并给出提示。
- TODO：决定是否自动迁移旧配置；若支持，必须备份原文件。

## 10. 待产出物

- [ ] `slots-simulator.schema.json`
- [ ] `examples/minimal.json`
- [ ] `examples/two-modules-eight-slots.json`
- [ ] 配置错误码清单
- [ ] 热重载状态迁移决策
