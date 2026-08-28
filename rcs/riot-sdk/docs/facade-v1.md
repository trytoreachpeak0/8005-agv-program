# Facade V1 方法清单

对应 [ADR-sdk-0003](../../../docs/adr/sdk/0003-v1-facade-method-scope.md)。入口为 `RiotSession`；未列出的能力走 `Raw` / RawEscape。业务失败抛 `RiotApiException`（[ADR-sdk-0005](../../../docs/adr/sdk/0005-facade-throws-on-business-failure.md)）。C# / Python 对等（[ADR-sdk-0004](../../../docs/adr/sdk/0004-v1-csharp-python-parity.md)）。

## Session

| C# | Python | 说明 |
|---|---|---|
| `new RiotSession(options)` | `RiotSession(options)` | CallApiKey 默认鉴权时可省略 Login |
| `LoginAsync` / `RefreshTokenAsync` | `login` / `refresh_token` | AdminLogin 备用路径 |
| `Device` / `Tasks` / `Order` / `Maps` | `device` / `tasks` / `order` / `maps` | 模块 Facade |

## Auth

| C# | Python | 契约 |
|---|---|---|
| `RiotOptions.CallApiKey` | `RiotOptions.call_api_key` | BC-AUTH-002 / ADR-sdk-0001 |
| `LoginAsync` | `login` | BC-AUTH-001 |

## Device

| C# | Python | 契约 |
|---|---|---|
| `ListDevicesAsync` | `list_devices` | 设备分页查询（非可调度车发现）；解包 page，业务失败抛异常 |
| `GetDeviceStatusStatisticsAsync` | `get_device_status_statistics` | 设备状态统计；解包 DTO，业务失败抛异常 |
| `TriggerEmergencyStopAsync` | `trigger_emergency_stop` | BC-VEH-005；成功后以车态确认 |
| `CancelEmergencyStopAsync` | `cancel_emergency_stop` | BC-VEH-005；成功后以车态确认 |

## Tasks（调度 / 车 / 路径 / 订单命令）

| C# | Python | 契约 |
|---|---|---|
| `GetDispatchableVehiclesAsync` | `get_dispatchable_vehicles` | BC-VEH-002 |
| `ResolveDeviceKeyAsync` | `resolve_device_key` | BC-VEH-002 |
| `GetRouteCostAsync` | `get_route_cost` | BC-ROUTE-001；`-1` 为领域结果 |
| `QueryNearestEndAsync` | `query_nearest_end` | NearStationQuery |
| `QueryNearestStartAsync` | `query_nearest_start` | NearStationQuery |
| `CancelOrderAsync` | `cancel_order` | BC-ORDER-003 |
| `OrderHoldAsync` | `order_hold` | BC-ORDER-006 |
| `OrderContinueAsync` | `order_continue` | BC-ORDER-006；勿用于 HANG |
| `HangContinueAsync` | `hang_continue` | BC-ORDER-015；成功码 ≠ 已离开 HANG |
| `DispatchEnableAsync` | `dispatch_enable` | BC-VEH-003 |
| `DispatchDisableAsync` | `dispatch_disable` | BC-VEH-003 |
| `GetVehicleCardAsync` | `get_vehicle_card` | 身份校验后的车辆卡片事实 |
| `GetVehicleExecutionFactsAsync` | `get_vehicle_execution_facts` | 车辆/任务双半事实；缺失或 key 不匹配即失败 |

## Order

| C# | Python | 契约 |
|---|---|---|
| `CreateMoveOrderAsync` | `create_move_order` | BC-ORDER-001 / BC-ORDER-005；map/station 必须为正数，返回 upperId 必须与请求一致 |
| `GetOrderByUpperIdAsync` | `get_order_by_upper_id` | BC-ORDER-005 |
| `FindOrderByUpperIdAsync` | `find_order_by_upper_id` | BC-ORDER-019 / ADR-sdk-0009；四态查找，只有 HTTP 404 为 NotFound |
| `GetOrderByOrderIdAsync` | `get_order_by_order_id` | BC-ORDER-005 |
| `ListOrdersByStatesAsync` | `list_orders_by_states` | 带完整分页覆盖元数据的订单状态页；状态过滤器逐项发送 |
| `PriorityExecAsync` | `priority_exec` | BC-ORDER-014；参数为字符串 `orderId` |

## Maps

| C# | Python | 契约 |
|---|---|---|
| `ListMapsAsync` | `list_maps` | BC-MAP-001 |
| `ListStationsAsync` | `list_stations` | BC-MAP-002 |
| `ListStationsStrictAsync` | `list_stations_strict` | 严格目录读取；坏行、空结果和重复 stationId 均失败 |

## 领域类型（Core）

| C# | Python |
|---|---|
| `DispatchableVehicle` | `DispatchableVehicle` |
| `Map` / `Station` | `Map` / `Station` |
| `RouteCost` | `RouteCost` |
| `OrderRef` | `OrderRef` |
| `OrderLookupResult` / `OrderSnapshot` | `OrderLookupResult` / `OrderSnapshot` |
| `VehicleCard` / `VehicleExecutionFacts` | `VehicleCard` / `VehicleExecutionFacts` |
| `OrderStatePage` / `OrderStateRecord` | `OrderStatePage` / `OrderStateRecord` |
| `DispatchableVehicleLookup.ResolveDeviceKey` | `resolve_device_key` |
| `ReadyForNextOrder.IsReady` | `is_ready_for_next_order` |
| `RiotApiException` | `RiotApiException` |
| `RiotBusinessResponse`（内部 ADR-sdk-0005 辅助） | `is_success_code` / `require_response` / `require_result` / `ensure_success` |

Python 包根导出见 `riot_sdk.__all__`。

## 明确不在 V1 具名 Facade 内

见 [ADR-sdk-0008](../../../docs/adr/sdk/0008-v1-explicit-non-goals.md)：interrupt、`task/v1/order` 建单主路径、几何 path、阻塞 Wait*、用 devices 列表发现可调度车、多段 mission DSL、CallApiKey 轮换策略。

可再派纯判定辅助已交付（[ADR-sdk-0007](../../../docs/adr/sdk/0007-ready-helpers-no-blocking-wait.md)）：`ReadyForNextOrder.IsReady` / `is_ready_for_next_order`；不内置阻塞 Wait*。
