# 跨接口标识关系

本文件记录标识的职责和待验证关系。除明确标记外，当前内容来自静态 schema，证据等级为 `SCHEMA`。

## 订单与实验

- `localExperimentId`：行为实验室生成，只用于组织证据，不发送给 RIoT。
- `upperId`：上层系统订单唯一标识候选；是否具有唯一约束或幂等语义仍为 `UNKNOWN`。
- `orderId`：RIoT 订单数字或字符串标识，具体类型以调用接口返回为准。
- `orderKey`：部分命令和查询使用的订单键；与 `orderId` 是否一一对应仍为 `UNKNOWN`。

## 车辆与设备

- `deviceKey`：device/物模型视角的设备标识。
- `vehicleKey`：task 调度视角的车辆标识。
- `appointVehicleKey`：建单时指定执行车辆的字段。
- `executeVehicleKey`：订单实际执行车辆的字段。

当前假设：同一测试车的 `deviceKey` 与 `vehicleKey` 可能取值相同，但在现场交叉查询确认前，不按同一概念硬编码。

## 地图与站点

- `mapId`：地图标识。
- `stationId`：地图中的站点标识。
- `stationName`：业务可读站点名称；本项目 MES `AREA` 映射依赖它。
- `destination`：mission 中的目的站字段，静态说明指向站点 ID。

`stationId` 是否跨地图唯一、地图更新后是否稳定，都保持 `UNKNOWN`。每轮证据必须同时保存 `mapId` 和 `stationId`。

## 物模型动作

- `services[].identifier`：TSL 中的动作服务标识。
- `serviceId`：device command API 使用的服务标识。
- `functionKey`：order mission 关联物模型动作的字段。
- `actionId`：task 或车端动作使用的数字标识。

这四者的映射不能仅靠名称猜测。每个已确认映射必须指向具体 `productKey`、物模型版本和现场实验。

## 关联记录要求

每个写实验至少保存：

```text
localExperimentId
→ upperId
→ RIoT 返回的 orderId/orderKey
→ appointVehicleKey/executeVehicleKey
→ mapId/destination
```

字段缺失时写 `UNKNOWN`，不要用另一个字段的值代填。
