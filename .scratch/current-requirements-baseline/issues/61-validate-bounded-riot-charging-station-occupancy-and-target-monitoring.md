# 验证有界的 RIoT 充电桩占用与目标监控接口

Type: task
Status: resolved
Blocked by: 36, 37

## Question

在不逐车查单、不分页扫描全部历史或活动订单、也不以高频调用压垮 RIoT 的前提下，验证目标环境 `RIOT-8005-RUNTIME`、build `v2.2.0.14` 是否存在可供 8005 有界监控全部相关车辆的只读快照能力。优先验证受控 OpenAPI 中的 `GET /api/task/vehicles`：

- 是否包含同一 RIoT 环境内未登记或不受 8005 管辖、但可能使用 8005 候选充电桩的车辆；
- `currentPosition` 能否可靠证明车辆当前占据某个充电桩站点；
- `endStationNo`、`orderTaskId`、`taskType=CHARGE` 及相关状态能否可靠证明车辆正在前往某个充电桩；
- 分页边界、字段新鲜度、任务终结后的清除行为以及断线、未知和短暂不一致的表现；
- 在代表性车辆规模和安全轮询频率下的响应大小、延迟、失败率及 RIoT 资源影响，并给出明确的调用预算；
- 能否以每轮一到少量有界车辆快照请求构建本地占用投影，而无需逐车查询订单或扫描订单列表。

验证必须使用已知占用、正在前往、任务终结、非 8005 车辆和状态未知的对照场景。若该接口不能证明覆盖完整、语义可靠且负载可接受，则不得把“本地没有预占”解释为空闲；应记录需要 RIoT 提供的专用充电桩占用/目标订阅接口或现场物理占用信号。若验证通过，后续决策仍须明确批准该具体只读接口、环境、字段契约、轮询预算和 fail-closed 规则后才能加入生产白名单。

## Comments

### 2026-08-04 — 目标环境不可达，用户授权改用测试环境代理验证

用户明确确认 `RIOT-8005-RUNTIME` 当前不可达，并指示使用 `RIOT-CROSS-PROJECT-TEST`。本票保持 `claimed`；测试环境 build `2.2.0.30` 的结果只作为代理行为证据，不得改写为 `RIOT-8005-RUNTIME v2.2.0.14` 的实测事实。

已建立 [Round 42 全车快照验证计划](../../../rcs/riot-behavior-lab/evidence/rounds/2026-08-04-round-42/round-plan.md) 与只读执行器。前导探针返回 18 辆车，并已观察到三个可由独立地图元数据核对的充电占用样本、17 辆非本地测试车和多种未知状态；当前没有 `taskType=CHARGE` 的在途样本，完整分页、轮询和字段清除验证仍待执行。

## Answer

用户明确授权在 `RIOT-8005-RUNTIME` 不可达时改用 `RIOT-CROSS-PROJECT-TEST`；因此本票结论严格绑定测试环境后端 build `v2.2.0.30`，只作为与 `v2.2.0.14` 受控 OpenAPI 同路径、同声明字段的代理行为证据，不冒充目标环境实测。完整计划、脱敏原始响应、投影和摘要见 [Round 42](../../../rcs/riot-behavior-lab/evidence/rounds/2026-08-04-round-42/)。

### 已验证的能力

- `getAllVehicleKeys` 与 `GET /api/task/vehicles?pageNum=1&pageSize=100` 返回同一组 18 个唯一 vehicle key，无缺失或额外项；其中 17 辆不是本地配置的 8005 测试车，证明该接口在测试环境不是按本项目登记集合隔离返回。
- `pageSize=1/5` 的相邻页按预期切分，`pageSize=100` 单页覆盖当前规模；但响应没有总数、页数、next cursor、服务端快照版本或观测时间。因此当前规模需要每轮一张快照，并至少每 60 秒用一次独立 key 集合核对完整性；独立 key 超过 100 或集合不等时必须停止单页投影。
- 三辆其它项目车辆在 24 轮中持续报告 `batteryState=CHARGING`，其 `(currentMap,currentPosition)` 分别命中 `ZY_WB_Map/308 夹抱充电桩`、`ZY_WB_Map/378 充电桩-新` 与 `尊阳电镀线opt/7 充电站点`。只有这个地图限定二元组加充电/现场对照可以支持“已经在桩上”；裸 `currentPosition` 不够。
- 普通任务自然完成时，`taskType=NORMAL / orderTaskId / endStationNo` 从 `PROCESSING_ORDER` 经一次 `AWAITING_ORDER`，在下一轮约 5 秒内清空并进入 `IDLE / MT_FINISHED`。这证明普通任务字段会清除，但不能外推 CHARGE 的清除时序。
- 24/24 张全车快照成功；5 秒串行轮询下延迟 min/median/p95/max 为 123/139/168/186 ms，响应为 15,458/15,688/15,698/15,699 bytes，客户端观测失败率 0%。可复现的测试上限是单请求串行、每 5 秒最多一次快照（12 次/分钟、约 188 KB/分钟），每 60 秒最多再做一次 key 核对，总计不超过 13 次 GET/分钟；15 秒超时，不复用失败前的旧快照，连续三次失败即停用并 fail-closed。

### 未通过的关键门槛

- 24 轮没有任何 `taskType=CHARGE` 在途样本；三辆正在充电的车辆反而均为 `taskType/orderTaskId/endStationNo=null`。所以尚不能证明 `taskType=CHARGE + endStationNo + orderTaskId` 完整覆盖其它车辆“正在前往某桩”的目标，也不能证明 CHARGE 终结后的清除行为。
- 多辆在线、移动中或异常车辆为 `currentPosition=0`，断线车为 `status=0 / locationState=ERROR`；因此 `0`、缺字段、断线、定位错误或短暂不一致只能表示未知，绝不能解释为空闲。
- 没有服务端 CPU、数据库、队列或饱和度指标；客户端 0% 失败和低延迟不能证明无 RIoT 资源影响。上述调用预算只记录测试环境已承受的保守上限，不是生产授权。
- `RIOT-8005-RUNTIME v2.2.0.14` 未执行同样对照，跨 build 代理结果不能升级为目标环境事实。

结论是：当前快照足以作为“已在充电桩上”的辅助占用证据，但不足以单独证明某桩“空闲且没有外部车辆正在前往”。在目标环境实测覆盖自然 CHARGE 在途/终结对照并另行批准具体接口、字段与预算之前，8005 必须把“本地没有预占但外部占用或目标不可确认”判为未知并 fail-closed；需要专用充电桩占用/目标订阅、现场物理占用信号或人工确认补足，不能逐车查单或扫描全部订单列表。
