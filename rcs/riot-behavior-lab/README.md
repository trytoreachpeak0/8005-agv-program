# RIoT Behavior Lab

**RIoT Behavior Lab（RIoT 行为实验室）**用于通过可重复的黑盒实验，建立本项目所用斯坦德 RIoT 实例的接口契约、可观测状态模型和异常行为知识。

本项目不宣称了解 RIoT 的“内部状态”。在没有源码、数据库或平台内部日志时，只记录接口可观测事实，以及由多次事实支持的行为推断。

## 1. 回答什么问题

- 现场实际存在什么接口，请求和响应结构是什么？
- Swagger、物模型、SDK 与现场返回是否一致？
- `orderState`、`missionState`、`procState`、车辆状态和物模型状态如何共同变化？
- 哪个信号可以可靠判断接单、移动、到站、完成、取消和异常？
- 重复提交、错误参数、暂停、中断和恢复的真实行为是什么？
- RIoT 升级、地图变化或车型变化后，既有结论是否仍成立？

## 2. 证据等级

每条知识结论必须标记来源等级，禁止把推测写成事实：

- `OFFICIAL`：厂商正式文档或明确答复。
- `SCHEMA`：Swagger、TSL 等静态契约声明。
- `OBSERVED`：现场请求、响应或状态轨迹直接观测。
- `INFERRED`：由多次观测支持，但尚无内部资料证实。
- `UNKNOWN`：含义未知；只允许原样记录，不允许用于业务判断。

来源冲突时不静默合并：保留各自说法，在 [`hypotheses/open-questions.md`](./hypotheses/open-questions.md) 登记，并通过实验或厂商确认解决。

## 3. 分层结构

```text
riot-behavior-lab/
├─ governance/       安全边界、人工干预和证据治理
├─ sources/          外部事实源索引，不复制 Swagger/TSL 原件
├─ catalog/          API、字段、枚举与跨层标识关系（含接口研究范围）
├─ hypotheses/       未决问题、假设和验证优先级
├─ experiments/      可复用实验定义
├─ runner/           执行器边界与后续自动化入口
├─ evidence/         按轮次保存的不可覆盖现场证据
├─ knowledge/        已验证行为契约和状态模型
└─ fixtures/         从证据晋升、供 SDK 测试消费的稳定样例
```

数据只能沿下面方向晋升：

```text
sources + hypotheses
        ↓
experiments
        ↓
evidence/rounds
        ↓
knowledge + fixtures
```

`evidence` 是“当时实际发生了什么”，历史不得覆盖；`knowledge` 是当前可以采用的结论；`fixtures` 是供客户端测试使用的派生资产，不能反过来作为现场行为证据。

## 4. 与仓库其他资产的边界

- [`../riot_swagger/`](../riot_swagger/)：全量 OpenAPI 原始快照，属于 `SCHEMA` 证据。
- [`../riot_ithing_model/`](../riot_ithing_model/)：设备属性、服务和枚举原始快照，属于 `SCHEMA` 证据。
- [`../riot-sdk/`](../riot-sdk/)：调用 RIoT 的客户端实现，是实验工具和 fixture 消费方，不是真实行为的权威来源。
- [`../../requirement-documents/`](../../requirement-documents/)：本项目业务需求。业务假设可以引用本实验室的已验证知识，但不能直接引用未验证假设。

## 5. 开始一轮实验

1. 阅读 [`governance/safety-boundaries.md`](./governance/safety-boundaries.md)。
2. 确认 `environment.local.json` 中现场地址、测试车和备注仍有效。
3. 对照 [`catalog/api-research-scope.md`](./catalog/api-research-scope.md)，确认本轮 API 落在「现在就需要进行研究」。
4. 从 [`hypotheses/open-questions.md`](./hypotheses/open-questions.md) 选择本轮要回答的问题。
5. 在 [`experiments/catalog.md`](./experiments/catalog.md) 选择对应实验；没有对应实验时先补实验定义。
6. 新建 `evidence/rounds/<date>-round-N/`，记录环境版本、批准范围和前置状态。
7. 执行时保存完整脱敏请求、响应及时间序列；摘要写入 `execution-log.md`。
8. 结束后先更新证据，再判断是否足以更新 [`knowledge/`](./knowledge/) 或晋升 [`fixtures/`](./fixtures/)。

## 6. 人工干预协议

现场测试中，API 做不到或继续执行不安全时，状态改为 `等待人工` 并停止后续写操作：

1. 在本轮日志写明需要人工完成的动作、建议回复和复查接口。
2. 用户完成现场动作后只需回复结果。
3. 先用只读接口复查，再恢复实验。
4. 人工干预不扩大本轮已经批准的 API 写操作范围。

## 7. 当前基线

- Round16：`curRemainCost` 在 EXECUTING 阶梯下降；map28 可派可跑（本轮未等到 SUCCESS）；`orderRecordPriorityExec` 插队有效（Q-026/027，BC-ROUTE-001/ORDER-014）。
- Round15：Route GET/POST @ map28 — costs 跨图=-1；Near* 纯拓扑；动态 GET 可空。
- 暂不测：`POST /api/task/v1/order/route/{vehicleKey}`、`POST .../currentMapExistNotFinalOrderTask/{mapId}`（已入「以后可能需要」）。
- 下一优先：MES/SDK 对接清单，或补 map28 完整 SUCCESS。

快速入口：

- [`evidence/rounds/2026-07-20-round-16/`](./evidence/rounds/2026-07-20-round-16/) — remain / map28 / 优先执行
- [`evidence/rounds/2026-07-20-round-15/`](./evidence/rounds/2026-07-20-round-15/) — Route Controller
- [`knowledge/behavioral-contracts.md`](./knowledge/behavioral-contracts.md)
