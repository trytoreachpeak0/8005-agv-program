# 查单观测使用四态结果，空结果不等于 NotFound

RIoT SDK 的 `FindOrderByUpperId` 使用 `Found`、`NotFound`、`AbsentAtObservation`、`Indeterminate` 四种状态：

- `Found`：HTTP/业务成功，订单标识完整，且响应 `upperId` 与请求严格一致。
- `NotFound`：仅 HTTP 404。
- `AbsentAtObservation`：HTTP 200、业务成功，但响应没有或返回 null `result`。
- `Indeterminate`：响应包含对象，但必要标识不完整或 `upperId` 与请求不一致。

`AbsentAtObservation` 表达“本次观测没有取得对象”，不承诺订单从未被接收、不会异步出现或可以安全重建。`AbsentAtObservation` 与 `Indeterminate` 的编排消费方都必须 fail-closed。mutation 不内置自动重试；建单成功信封缺少结果仍抛 `order-ref-missing`。

SDK 自有 transport 明确关闭自动重试与重定向：C# 使用不挂 Kiota retry middleware 且 `AllowAutoRedirect=false` 的 `HttpClient`，Python 使用 `AsyncHTTPTransport(retries=0)` 且 `follow_redirects=False`。测试或宿主注入自有客户端时，宿主不得在该客户端上添加重试或重定向策略；ControlServer 的 RIoT typed client 同样遵守该限制。

C# 注入 `HttpClient` 时，其 `BaseAddress` origin 必须与 `RiotOptions.BaseUrl` 完全一致；raw observation 请求始终从 options 生成绝对 URI，避免 Bearer 被发送到其它主机。响应正文也必须在 HTTP timeout 内完整读取。建单除校验正数 map/station 外，还必须核对返回 `upperId` 与请求精确一致；不一致抛 `order-upper-id-mismatch`，不得把串单响应当作本次成功。

订单对象中的可选数值（例如 mission `destination` 与 `endStationNo`）允许 JSON `null`，SDK 必须将其保留为 nullable 值，不能让底层 JSON 类型异常把完整订单误降为 `Indeterminate`。安全消费方可在业务层使用其它已验证字段做显式回退；缺少全部目标证据时仍 fail-closed。

旧 `GetOrderByUpperId` 保持严格返回 `OrderRef` 或抛异常的兼容契约。新消费方使用具名 `FindOrderByUpperId`，不得直接依赖 Kiota 生成类型或 RawEscape 推断缺失语义。

依据：[BC-ORDER-019](../../../rcs/riot-behavior-lab/knowledge/behavioral-contracts.md#bc-order-019-detailbyupperid-的空结果只证明本次观测未见订单)。RIoT 负责人尚需确认空结果正式含义、冻结 POST 是否被接受，以及异步落单最大时限；确认前本决策不允许把空结果升级为 `NotFound`。

**Status**: accepted
