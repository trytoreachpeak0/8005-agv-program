# Round 42 执行日志（2026-08-04）

## 当前状态

`COMPLETED`

`RIOT-8005-RUNTIME` 当前不可达。用户已明确授权改用 `RIOT-CROSS-PROJECT-TEST`；本轮只形成 build `2.2.0.30` 的代理行为证据，不替代目标环境实测。

## 已完成的前导探针

- `GET /api/task/vehicles?pageNum=1&pageSize=100` 返回 HTTP 200 / `code=0`，18 辆车，响应 15,696 bytes、200 ms。
- 18 辆车中只有一辆是本地配置的测试车，其余 17 辆证明该接口不是按 8005 登记集合隔离返回。
- 三辆其它项目车辆报告 `batteryState=CHARGING`：
  - `ZY_WB_Map / currentPosition=308`，独立站点元数据为“夹抱充电桩”；
  - `ZY_WB_Map / currentPosition=378`，独立站点元数据为“充电桩-新”；
  - `尊阳电镀线opt / currentPosition=7`，独立站点元数据为“充电站点”。
- 同一快照存在断线、定位错误和 `currentPosition=0` 样本，可用于确认未知状态必须 fail-closed。
- 前导样本没有 `taskType=CHARGE`，因此尚未覆盖“正在前往充电桩”；不能把在途目标字段视为已验证。

## 完整采样结果

- build 识别返回后端 `v2.2.0.30`，与本轮环境绑定一致。
- `getAllVehicleKeys` 与 `pageNum=1&pageSize=100` 都得到同一组 18 个唯一 vehicle key，无缺失、无额外项；其中 17 辆不是本地配置的测试车。
- 分页参数真实生效：`pageSize=1` 的第 1/2 页各返回相邻的一辆，`pageSize=5` 的第 1/2 页各返回相邻的五辆；但顶层只有 `code/message/msgDetail/result/tid`，没有 total、pageCount、next cursor、服务端快照版本或观测时间。
- 24 次全车快照全部成功，串行间隔 5 秒：延迟 min/median/p95/max 为 123/139/168/186 ms；响应大小 min/median/p95/max 为 15,458/15,688/15,698/15,699 bytes；客户端观测失败率 0%。没有 RIoT 服务端 CPU、数据库、队列或饱和度指标，因此不能声称已证明无服务端资源影响。
- 三辆其它项目车辆在全部 24 轮均报告 `batteryState=CHARGING`，其 `(currentMap,currentPosition)` 分别命中 `ZY_WB_Map/308 夹抱充电桩`、`ZY_WB_Map/378 充电桩-新` 和 `尊阳电镀线opt/7 充电站点`。这支持用地图限定的二元组加充电状态识别“已经在桩上”，不支持只用裸站点号。
- 同一快照里多辆在线、离站或异常车辆为 `currentPosition=0`；断线车同时为 `status=0 / locationState=ERROR`。因此 `0`、缺字段或错误状态不能解释为空闲，也不能沿用上一轮位置。
- 一辆执行普通任务的车辆先报告 `taskType=NORMAL / orderTaskId / endStationNo=151 / PROCESSING_ORDER`，随后出现一次 `AWAITING_ORDER`，下一轮在约 5 秒内清空任务字段并变为 `IDLE / MT_FINISHED / currentPosition=151`。这只证明普通任务字段会在终结后清除，不证明 CHARGE 的终结清除契约。
- 24 轮没有出现任何 `taskType=CHARGE` 在途样本；三辆正在充电的车辆反而均为 `taskType/orderTaskId/endStationNo=null`。因此无法验证这些字段对“正在前往充电桩”的覆盖、时序或新鲜度。

## 调用预算结论

本轮可复现的测试上限为：单一在途请求、每 5 秒最多一次 `pageSize=100` 快照，即 12 次/分钟、约 188 KB/分钟响应流量；每 60 秒最多再做一次 `getAllVehicleKeys` 完整性核对，总计不超过 13 次 GET/分钟。超时 15 秒，失败不复用旧快照；连续 3 次失败停止投影并 fail-closed。若独立 key 数超过 100、集合不相等、出现重复/缺失或 build/字段契约变化，立即停止使用单页投影。

这是测试环境中已承受的保守上限，不是生产白名单授权，也不是服务端资源安全证明。

## 结论

`GET /api/task/vehicles` 在 build `2.2.0.30` 能以两次有界 GET 覆盖当前 18 辆车，并能识别已在桩上的其它项目车辆；但它不能在本轮证明外部车辆的充电在途目标，也没有可核查的新鲜度或服务端负载证据。`RIOT-8005-RUNTIME v2.2.0.14` 又未实测，因此当前不得把该接口作为“空闲且未被外部车辆预占”的唯一证明。

在获得目标环境实测并覆盖自然 CHARGE 在途/终结对照，或 RIoT 提供专用充电桩占用与目标订阅之前，8005 必须把“本地没有预占但外部占用/目标不可确认”判为未知并 fail-closed；需要由现场物理占用信号、专用接口或人工确认补足。
