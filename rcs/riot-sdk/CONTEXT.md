# RIoT SDK

调用本项目所用斯坦德 RIoT 实例的客户端边界：鉴权、可调度资源发现，以及订单与车辆相关操作的对外语言。

## Language

### 鉴权

**CallApiKey**:
RIoT 网页「调用密钥设置」中的长期密钥，作为业务接口默认的 Bearer 凭证。
_Avoid_: API key（泛称）、网页密钥（口语）、静态 token（易与登录短时 token 混淆）

**AccessToken**:
经 `admin/login`（或 refresh）取得的短时访问凭证；第一版中仅作备用鉴权路径。
_Avoid_: token（单独使用时歧义）、Bearer（指头格式而非凭证种类）

**AdminLogin**:
用用户名密码换取 AccessToken 的备用鉴权方式；登录成败不能只看 HTTP 状态。
_Avoid_: 登录（单独使用时歧义）、鉴权（上位概念）

### 消费边界

**DispatchLoop**:
MES/调度侧完成一次派车所需的最小闭环：鉴权、发现可调度车与地图站点、建单、观察终态、必要时取消或中断。
_Avoid_: 全量 RIoT API、实验探针集

**DispatchableVehicle**:
可通过 task 侧车辆清单发现、用于 appointVehicleKey 的车；不是 devices 列表中的门/电梯等非车设备。
_Avoid_: Device（泛称）、可调度设备

### 对外入口

**Session**:
指向单一 RIoT 实例的共享会话；第一版推荐的唯一稳定入口，其下挂载具名 Facade 方法。
_Avoid_: 客户端（泛称）、连接、Generated 客户端

**RawEscape**:
经 Session 暴露的未封装 Kiota 调用面；仅作临时逃逸，不属于稳定契约。
_Avoid_: 正式 API、稳定 Facade

### 地图与站点

**Map**:
RIoT 中一张可调度地图；业务上用 `mapId` 标识，可读名为地图 `name`。
_Avoid_: 图层、楼层图（除非特指 floor 字段）

**Station**:
某张 Map 上的站点；必须与 `mapId` 成对使用，站点 `id` 跨图不保证唯一。
_Avoid_: 点位（泛称）、目的地（业务语义更宽）

**NearStationQuery**:
在候选 Station 集合中，按路径代价选出最近的起点或终点 Station（对应 RIoT `queryNearestStart` / `queryNearEnd`）；返回的是 stationId，不是折线几何。
_Avoid_: 最短路径（易被理解成几何 path）、路径规划结果

**RouteCost**:
指定 Map 上某车到某 Station 的路径代价（mm）；非负且可读为可达，`-1` 表示不可达（含车不在该图等）。建单前可达判断依据此值，不能只看建单业务成功码。
_Avoid_: 距离（易被理解成直线距离）、最短路径几何

**OrderRef**:
`byDefaultMissions` 建单成功后返回的订单标识：数值 `id`、字符串 `orderId`、调用方 `upperId`，以及当时的 `orderState`。后续查单/取消/命令按 BC-ORDER-005 选用对应标识。
_Avoid_: Order（泛称）、任务号（口语）

### 车辆调度控制

**DispatchEnable**:
把车纳入调度可接单（对应现场 enable / 上线路径）；与设备通电不是同一概念。
_Avoid_: 开机、上线（易与网络在线混淆）、enable（裸字段名）

**DispatchDisable**:
把车移出调度接单（对应现场 disable / 下线路径）；不自动等同于取消执行中订单。
_Avoid_: 关机、下线（易与断网混淆）、disable（裸字段名）

**EmergencyStop**:
车辆急停态及软件触发/解除；是否恢复以车侧急停态为准，不以单次 HTTP 成功为唯一依据。
_Avoid_: 暂停（与 HELD 不同）、中断（与 interrupt 不同）

### 订单控制

**OrderHold**:
将移动单置于 HELD（暂停执行）的控制；与 EmergencyStop、interrupt 不同。
_Avoid_: 暂停（泛称）、急停

**OrderContinue**:
从 HELD 恢复继续执行（CONTINUE_FROM_HELD）。
_Avoid_: 恢复（泛称，易与急停解除混淆）、resume（裸英文）、HangContinue

**HangContinue**:
从 OrderHang 尝试拉回 EXECUTING（CONTINUE_FROM_HANG）；与 OrderContinue 命令不同，不可混用。接口成功码不等于订单已离开 HANG。
_Avoid_: OrderContinue、resume（泛称）

**PriorityExec**:
将队列中指定订单提升为优先执行，而不必先清空同车其它队列单。
_Avoid_: 插队（口语）、优先级字段（建单时的 priority 语义不同）

**BusinessFailure**:
RIoT 在 HTTP 已成功（或可判定）的前提下，用业务 `code` 表达的失败；具名 Facade 将其表现为统一异常，而不是留给调用方拆包。
_Avoid_: HTTP 错误（传输层）、不可达（RouteCost=-1，属领域结果）

**ArrivalAtStation**:
车辆已到达目的 Station 的车侧可观测信号；在成功移动单上往往早于订单 SUCCESS。
_Avoid_: 订单完成、可再派

**ReadyForNextOrder**:
可以安全下发下一单的条件：订单已 SUCCESS 且车辆已 IDLE；不等于 ArrivalAtStation。
_Avoid_: 到站即可派、AWAITING_ORDER（单独作为充分条件）

### 异常滞留

**QueueingStall**:
订单已创建成功但长期停留在 QUEUEING、通常 `executeVehicleKey` 为 `--`、迟迟不进入 EXECUTING 的滞留现象。常见诱因包括不可达、假车 key、车未纳入调度等；RIoT 不会因此自动变为 FAILED。策略属 MES 编排，不在 SDK 具名 Facade 内。
_Avoid_: 挂起（泛称）、HANG、暂停（HELD）

**OrderHang**:
订单 `orderState=HANG` 的滞留；充电失败与普通 HANG 策略分离。普通分支可按原因尝试 HangContinue；充电分支不以 HangContinue 为默认。HangContinue 接口成功码不等于订单已离开 HANG。
_Avoid_: 挂起（泛称）、QUEUEING 滞留、HELD
