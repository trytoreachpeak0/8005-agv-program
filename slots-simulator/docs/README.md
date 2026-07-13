# slots-simulator 文档中心

本目录统一存放 `slots-simulator` 从需求到实施的全部项目文档。项目仍处于规划阶段，文档中的决定和模板不代表代码已经实现。

## 1. 阅读顺序

```text
00 愿景与范围
  ↓
01 功能需求：做什么、如何验收
  ↓
02 决策记录：为什么这样做
  ↓
03 详细设计：具体怎么实现
  ↓
04 测试计划：如何证明实现正确
  ↓
05 实施计划：按什么顺序开发
```

## 2. 目录结构

```text
slots-simulator/docs/
├─ README.md
├─ 00-vision/
│  └─ vision-and-scope.md
├─ 01-requirements/
│  ├─ README.md
│  └─ fr-001 ... fr-015
├─ 02-decisions/
│  ├─ README.md
│  └─ dr-001 ... dr-015
├─ 03-design/
│  ├─ architecture.md
│  ├─ slot-state-machine.md
│  ├─ modbus-implementation-spec.md
│  ├─ control-api.openapi.yaml
│  └─ configuration-spec.md
├─ 04-testing/
│  └─ test-plan.md
├─ 05-planning/
│  └─ implementation-plan.md
├─ reference/
│  └─ C2000-A2-KDDA0A0-AD6_寄存器表.md
└─ _templates/
   ├─ template-functional-requirement.md
   └─ template-decision-record.md
```

## 3. 文档入口

- [愿景与范围](./00-vision/vision-and-scope.md)
- [功能需求索引](./01-requirements/README.md)
- [决策记录索引](./02-decisions/README.md)
- [架构设计](./03-design/architecture.md)
- [仓位状态机](./03-design/slot-state-machine.md)
- [Modbus 实现规格](./03-design/modbus-implementation-spec.md)
- [控制 API 契约](./03-design/control-api.openapi.yaml)
- [配置规格](./03-design/configuration-spec.md)
- [测试计划](./04-testing/test-plan.md)
- [实施计划](./05-planning/implementation-plan.md)
- [硬件寄存器参考](./reference/C2000-A2-KDDA0A0-AD6_寄存器表.md)

## 4. 编号与命名

| 类型 | ID 格式 | 文件名格式 |
| --- | --- | --- |
| Functional Requirement | `FR-001` | `fr-001-xxx.md` |
| Decision Record | `DR-001` | `dr-001-xxx.md` |

FR/DR 在本子项目内独立编号，不与仓库根目录 `requirement-documents/` 的业务需求编号混用。

## 5. 引用规则

- 本项目 FR/DR 之间使用 Obsidian wikilink，例如 `[[fr-006-automation-control-api|FR-006]]`。
- 跨目录的设计、测试和计划文档使用普通 Markdown 相对链接。
- 引用仓库根目录业务 UC 时使用普通相对链接；FR/DR 文件中的相对路径以 `../../../requirement-documents/` 开头。
- `_templates/` 只保留指向根目录规范模板的占位说明，不复制维护第二份模板。

## 6. 与主项目需求的关系

仓库根目录 `requirement-documents/` 描述整个多仓位 AGV 系统的业务流程；本目录描述模拟器自身的需求、决策、设计、测试和实施方式。二者通过 `related_uc` 和正文链接保持追溯。

## 7. 当前技术基线

- Modbus TCP 支持 `0x01/02/03/05/06/0F/10`。
- 控制 API 为默认仅监听 `localhost` 的 HTTP/JSON，不提供开锁入口。
- 占用状态由光幕 DI 推导；同仓位串行、不同仓位并行。
- 配置采用 JSON + JSON Schema，WPF 支持校验后原子热重载。
- 业务超时和任务业务由主系统负责。

详细边界以 [决策记录](./02-decisions/README.md) 为准。
