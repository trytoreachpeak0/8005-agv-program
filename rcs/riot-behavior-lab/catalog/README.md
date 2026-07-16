# 语义目录

本层负责把分散在 Swagger、TSL、SDK 和现场证据中的标识组织起来，但不在这里记录实验过程。

## 应维护的四类目录

1. **操作目录**：模块、端点、请求模型、响应模型、鉴权方式和写操作风险。
2. **状态目录**：字段、静态取值、来源等级、已观测取值和业务可用性。
3. **标识关系**：`upperId`、`orderId`、`orderKey`、`deviceKey`、`vehicleKey`、`mapId`、`stationId` 的产生与关联方式。
4. **动作关系**：物模型 `service.identifier`、device API `serviceId`、order `functionKey` 和 task `actionId` 的映射。

## 收录规则

- Swagger 或 TSL 声明的值标记为 `SCHEMA`，不能写成“现场已确认”。
- 现场出现但静态契约没有说明的值，按原值记录为 `OBSERVED`，语义保持 `UNKNOWN`。
- 同名字段在不同模块中可能不是同一状态，不因名称相似而合并。
- 每个标识关系必须能指向来源文件或实验轮次。

当前实验卡仍保存在 [`../experiments/catalog.md`](../experiments/catalog.md)。后续应从真实实验中逐步形成操作、状态和标识目录，而不是一次性根据字段名猜测填满。

当前入口：

- [`identifiers.md`](./identifiers.md)：订单、车辆、地图和动作标识关系。
- [`state-fields.md`](./state-fields.md)：各层状态字段及当前业务可用性。
