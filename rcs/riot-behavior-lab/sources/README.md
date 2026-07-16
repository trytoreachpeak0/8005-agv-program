# 事实源索引

本目录只登记事实源及其可信边界，不复制仓库中已有的原始文件。

## 当前来源

### RIoT OpenAPI

- 路径：[`../../riot_swagger/`](../../riot_swagger/)
- 证据等级：`SCHEMA`
- 用途：端点、HTTP 方法、参数、请求/响应结构和字段说明。
- 限制：不能证明现场版本一致，也不能证明状态转移、幂等、错误码和副作用语义。

### RIoT 物模型

- 路径：[`../../riot_ithing_model/`](../../riot_ithing_model/)
- 证据等级：`SCHEMA`
- 用途：按 `productKey` 描述设备属性、事件、服务和部分枚举。
- 限制：当前只有部分车型；跳号枚举和裸错误码保持 `UNKNOWN`。

### RIoT SDK

- 路径：[`../../riot-sdk/`](../../riot-sdk/)
- 证据等级：生成模型为 `SCHEMA`，手写逻辑不自动成为现场事实。
- 用途：交叉核对 OpenAPI、执行实验、消费 fixture。
- 限制：当前仅覆盖 device、task、order 及部分鉴权。

### 现场实验

- 路径：[`../evidence/rounds/`](../evidence/rounds/)
- 证据等级：`OBSERVED`
- 用途：证明指定环境、版本、时间和前置条件下实际发生的行为。
- 限制：单次观测不能直接推广到所有版本和环境。

## 版本记录要求

每轮实验至少记录：

- RIoT 平台版本；无法获取时明确写 `UNKNOWN`。
- Swagger 快照或摘要版本。
- 物模型 `productKey` 与版本。
- 地图标识及可获取的地图版本。
- 测试车 `deviceKey`（脱敏时保留稳定别名）和车型。
- 实验目录版本或 Git 提交号。
