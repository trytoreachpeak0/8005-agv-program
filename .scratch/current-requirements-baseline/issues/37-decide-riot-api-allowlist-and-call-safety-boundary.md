# 决定 RIoT 项目 API 白名单与调用安全边界

Type: grilling
Status: resolved
Blocked by: 25, 36

## Question

在目标环境与接口版本完成绑定后，8005 项目获准调用哪些 RIoT API、读写和危险操作分别由谁授权；登录 token、CallApiKey 或其它身份凭据的获取、保管、轮换、失效和最小权限边界是什么；错误、超时、重试、幂等和急停等调用应遵守哪些项目规则，如何把批准结果绑定到具体 schema 版本与适用环境？

## Answer

用户本人作为当前需求基线最终批准人，确认 8005 采用按具体操作的业务后果、可逆性和安全影响分层的封闭白名单；不能按 GET/POST 或只读/写入粗分。白名单绑定 `RIOT-8005-RUNTIME`、运行 build `v2.2.0.14` 和 OpenAPI 快照 `RIOT-OPENAPI-8005-202607-EARLY-01`。该快照来自 `v2.2.0.14`；同一套 OpenAPI 客户端后来用于 `2.2.0.30` 环境的 300C riot-lab 测试。300C 与 300E 共用同一物模型，用户明确批准默认两车型状态值与行为逻辑相同；跨 build 行为只在接口路径、方法和字段仍匹配时沿用，且所有调用仍须独立确认结果。

### 当前获批调用

1. **观察与计算**：build 查询；地图和站点查询；可调度车辆和指定车辆状态查询；按 upperId/orderId 查询订单；以及所有已确认的无副作用路由读取，包括动态路由代价、代价单位、车辆到站 RouteCost、最近起点/终点、订单剩余路径代价和订单轨迹。具体包括当前 Facade 使用的地图/车辆/订单查询，以及 `GET /api/version/v1/infos`、`GET /api/task/v1/task/getVehicleInfo/{deviceKey}`、`GET /api/task/v1/route/`、`GET /api/task/v1/route/curRemainCost/{orderKey}`、`GET /api/task/v1/route/getCostUnit`、`POST /api/task/v1/route/getRouteCostsBy`、`POST /api/task/v1/route/queryNearEnd`、`POST /api/task/v1/route/queryNearestStart` 和 `POST /api/task/v1/order/route/{vehicleKey}`。使用 POST 的查询仍按无副作用语义管理；两个清除动态路由代价的 DELETE 不获批。
2. **常规建单**：只允许 `POST /api/order/v1/add/byDefaultMissions` 创建指定车辆、地图和站点的单段 move；须使用稳定 upperId，并先验证车辆 ON_LINE、RouteCost 可达且该车未占用 RIoT 车辆订单名额。模板建单、订单组合、改单不获批。
3. **受控订单命令**：只允许 `POST /api/task/v1/order/command/{orderId}` 的 `CMD_ORDER_CANCEL`、`CMD_ORDER_HELD`、`CMD_ORDER_CONTINUE_FROM_HELD` 和 `CMD_ORDER_CONTINUE_FROM_HANG`。取消仅作用于 8005 自己创建并可关联 TransportDemand 的订单；OrderHold 可在已批准保护条件下自动触发；OrderContinue 只有在暂停原因消除、重连/未结操作对账完成、重新通过 PreDepartureSafetyCheck 且服务端生成本次明确授权后才能调用；HangContinue 只用于已批准原因白名单中的普通 HANG、受次数上限约束，未知原因和充电失败不使用。
4. **调度可用性**：允许 `POST /api/task/vehicles/updateVehicleIntegrationLevel` 的 `serviceId=enable|disable`。它只决定车辆是否承接后续调度：disable 不阻止建单进入 QUEUEING，也不暂停或终止当前 EXECUTING 订单；应用建单前必须独立确认 ON_LINE，并在调用后回查实际状态。
5. **条件式软件急停**：允许 `POST /api/device/v1/command/sync/service/{deviceKey}/{serviceId}` 的 `triggerEmergency|cancelEmergency`，但只按以下规则使用。车辆在仓门未安全锁闭时移动、无 RIoT 订单可供 OrderHold 且无其它获批 RIoT 停车动作时，8005 自动 triggerEmergency 并进入持续保持；外部系统提前解除且仓门仍不安全时立即重触发并告警。车载端和服务端都可请求解除任何 CAN_RECOVER 软件急停锁存；CAN_NOT_RECOVER 时禁止调用。解除前车载端必须确认车辆停止、全部仓门安全锁闭、开锁输出复位及 DepartureSafe；车载端无需身份，服务端沿用现有登录会话且不再输入工号，解除后须回查 emergencyState=OK。

白名单到此封闭。PriorityExec 只保留为未来候选；interrupt、JUMP_FROM_HANG、REJECTED、一键停靠、放行、指定充电、定位开始/停止、地图/路线资源/车辆/模板/配置修改、物模型任意写入、系统管理、清理、上传、RawEscape、生成客户端和其它未具名调用全部不授权。8005 只通过获批 RIoT API 控车，不接入单机控制面，也不绕过 RIoT 发送 Modbus 或其它底层车辆指令。

### 单车订单名额

8005 按下单记录中的 appointVehicleKey 保证每车至多一个未明确终结的本项目 RIoT 订单；不能依赖 executeVehicleKey 查询 QUEUEING 归属。QUEUEING、EXECUTING、PAUSED、HANG、优先队列、SUSPENDED 和未知状态均计入，只有独立回查确认为 CANCELLED、FAILED、SUCCESS 或 DELETED 才释放名额。

### 鉴权与权限治理

ControlServer 使用目标环境独立的 CallApiKey 作为默认 Bearer 凭证；OnboardHmi 不持有 RIoT 凭证，AdminLogin/AccessToken 只作人工应急备用。CallApiKey 原值可以由有权人员在 RIoT 原生页面查看，也必须存在于 ControlServer 部署密钥存储，但 8005 不额外提供查看入口，不把原值复制到 Git、普通配置、数据库、日志、审计或业务响应；审计只记指纹。密钥是否轮换完全依靠人工判断，不设时间或事件自动规则；软件负责人或实施负责人可提出，双方确认并协调执行。

当前白名单由用户批准。软件负责人或实施负责人可提案，也可因风险立即收紧或暂停调用；扩大白名单、降低安全门槛或恢复安全暂停必须再次取得用户明确批准。生产业务代码只可经具名 Facade 调用，默认拒绝 RawEscape 和任意 URL；SDK/OpenAPI 更新不自动扩权。该限制只约束 RIoT 的调用源为 ControlServer，不限制 ControlServer 连接车载端、数据库或其它已批准依赖。

### 结果确认、错误与重试

查询/计算须验证 HTTP、业务 code、必需字段、范围和新鲜度；状态变更响应只表示请求已受理，必须独立回查目标后置状态。查询只对暂时传输或服务错误有限退避重试，401/403、参数错误和普通业务失败不盲重试。建单超时先按原 upperId 对账，已存在则接管，不存在才用相同 upperId 重试，绝不换号。其它状态变更超时先回查，只有目标未达到且原前置条件仍成立时才可重试；仓门不安全移动保护中的 triggerEmergency 可持续重试到确认急停并逐次告警。任何结果未知都阻断依赖动作；具体次数和退避时长留给正式 spec 配置。

如果运行时 build 或接口契约变化，观察调用继续用于识别和诊断，普通写操作暂停；危险状态中的 OrderHold/triggerEmergency 仍可尝试并回查。软件负责人和实施负责人完成人工兼容性判断、用户批准恢复后才开放其它写操作；若连接到错误环境，则除环境识别外全部禁止。

### 审计

所有状态变更逐次记录操作、目标、触发来源、原因、环境/build/快照、关联号、调用前状态、HTTP/业务结果、回查后状态、重试及最终结论；车载匿名解除记为“车载本地匿名确认”，服务端按钮记录现有会话身份。查询只记录失败、结果未知、安全异常和汇总指标；所有凭证和秘密必须过滤。审计不替代状态回查，也不作为请求重放源。
