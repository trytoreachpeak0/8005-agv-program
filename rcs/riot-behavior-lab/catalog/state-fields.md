# 状态字段目录

本目录用于防止把不同层次的状态混成一个状态机。静态取值来自 Swagger、TSL 或生成代码，证据等级为 `SCHEMA`。

## 订单层

### `orderState`

- 来源：Order 模块订单记录。
- 静态取值：QUEUEING、CANCELLED、EXECUTING、FAILED、SUCCESS、DELETED、PAUSED、SUSPENDED、HANG 等。
- 当前业务可用性：只能展示原值；到站、完成和可重新派单的映射尚未验证。

### `missionState`

- 来源：Order mission。
- 静态取值：未开始、执行中、完成、失败、取消。
- 当前业务可用性：只能展示原值；与父订单终态的先后关系尚未验证。

## 调度与车辆层

### `procState`

- 来源：Task `VehicleTaskInfo`。
- 静态取值：AWAITING_ORDER、IDLE、PROCESSING_ORDER、IN_CANCEL、USER_FORCE_IDLE 等。
- 当前业务可用性：不能单独用于判定队列为空或车辆已到站。

### `Vehicle.state`

- 来源：Task 车辆聚合模型。
- 静态取值：IDLE、EXECUTING、CHARGING、ERROR、PAUSE、UNKNOWN。
- 当前业务可用性：不能单独映射为本地业务任务状态。

## 设备物模型层

### `sysState`

- 来源：`standard.oasis.300ul` TSL。
- 静态取值：0～24，具体标识见原始物模型。
- 当前业务可用性：按原值记录；尚未与 RIoT 订单时间轴对齐。

### `movementState`

- 来源：`standard.oasis.300ul` TSL。
- 内容：移动任务及路径相关复合状态。
- 当前业务可用性：按完整结构记录；跳号枚举保持 `UNKNOWN`。

### `multiLoadState`

- 来源：`standard.oasis.300ul` TSL。
- 类型：裸整数。
- 当前业务可用性：禁止依据具体数值做业务判断，直至厂商说明或安全实验完成。

## 业务判定规则

“已接单”“移动中”“已到站”“已完成”“队列为空”等属于项目判定，不是某个字段的同义词。每条判定必须：

1. 指明使用哪些状态面和位置字段。
2. 指明采样新鲜度和连续确认次数。
3. 处理字段缺失、接口失败和状态冲突。
4. 指向支持该规则的实验轮次。

当前尚无满足条件的业务判定规则。
