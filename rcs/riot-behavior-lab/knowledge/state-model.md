# 可观测状态模型

## 建模原则

RIoT 暴露的是多个不同层次的状态面，目前没有证据表明它们可以合并成一个状态字段：

- 订单层：`orderState`
- mission 层：`missionState`
- 调度进程层：`procState`
- 车辆聚合层：`Vehicle.state`
- 设备物模型层：`sysState`、`movementState` 等
- 本项目业务层：本地任务和流程状态

因此状态模型以“同一时间轴上的并行观测”表示，不提前建立一对一映射。

## 静态已知状态

下面内容来自 Swagger、TSL 或生成代码，证据等级为 `SCHEMA`：

- `orderState` 声明了 QUEUEING、CANCELLED、EXECUTING、FAILED、SUCCESS、DELETED、PAUSED、SUSPENDED、HANG 等值。
- `missionState` 声明了未开始、执行中、完成、失败、取消等值。
- `procState` 声明了 AWAITING_ORDER、IDLE、PROCESSING_ORDER、IN_CANCEL、USER_FORCE_IDLE 等值。
- `Vehicle.state` 声明了 IDLE、EXECUTING、CHARGING、ERROR、PAUSE、UNKNOWN 等值。

这些列表只证明“契约中存在这些值”，不证明现场一定出现，也不证明转移条件。

## 当前已验证状态转移

尚无完整订单时间序列，因此目前没有可晋升为 `OBSERVED` 或 `INFERRED` 的订单状态转移。

## 第一条目标轨迹

最小闭环应在统一时间轴记录：

```text
实验事件
  × orderState
  × missionState
  × procState
  × Vehicle.state
  × currentStation
  × sysState
  × movementState
```

至少标记以下外部事件：

- 提交订单
- RIoT 返回订单标识
- 车辆开始移动
- 车辆物理进入目标站
- 订单完成
- 车辆重新可接单

只有当外部事件和状态采样可以稳定对齐后，才能定义“已接单”“移动中”“已到站”“已完成”等项目判定规则。
