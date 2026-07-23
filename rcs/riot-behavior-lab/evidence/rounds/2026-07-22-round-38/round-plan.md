# Round 38（2026-07-22）— 单机「去站点」过程中建单 / HANG+CONTINUE

## 前提

单机「移动」= **让 AGV 前往某个站点**，要求已定位且在路线/站点上。

## M1 — 单机去站点过程中，RIoT 建单

1. 车 IDLE、已定位、在站点上
2. **人工**：单机系统让车去某站点（开始移动）
3. 监视到 `MT_RUNNING` / speed>0 后，RIoT `byDefaultMissions` 建移动单
4. 观察订单：QUEUEING / EXECUTING / 其它，以及车侧状态
5. 清场

## H1 — 订单 HANG 后，单机去站点过程中 CONTINUE

1. RIoT 长单 → EXECUTING
2. **人工**：单机取消移动 → 进 HANG
3. **人工**：单机系统再让车去某站点（开始移动）
4. 移动过程中发 `CONTINUE_FROM_HANG`
5. 观察能否恢复执行
6. 清场

## 不作

- 「先 QUEUE 再单机去站点」：与可操作前提互斥（急停等），记 NA

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
