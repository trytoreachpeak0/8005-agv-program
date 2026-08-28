# Round 30（2026-07-22）— 未定位 / 离路线过远：建单与执行中是否进 HANG

## 问题

用户现场经验：车**未定位**，或**当前位置离路线太远**时，下单后订单会「一直 hang」。
需用事实区分：是 `orderState=9 HANG`，还是长期 `QUEUEING`（同类 Round29 / Q-032），或先 `EXECUTING` 再挂起。

## 场景

| 标签 | 条件 | 测法 |
|------|------|------|
| L | 未定位（`locationState≠RUNNING`） | IDLE 下停定位 → 建单监视；可选：执行中再停定位 |
| D | 离路线过远（仍定位，但位置偏离路径） | 人工把车推离路线 → 建单监视；可选：执行中再推离 |

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2（map30）
- 监视：建单后约 90–120s；若进 EXECUTING 可延长到出现 HANG / 终态

## 每场景

1. 基线 IDLE、已定位、无残留单
2. 进入条件（人工停定位 / 推离路线）
3. 建单 + 采样 orderState / executeVehicleKey / locationState / failReason / mission result
4. 若进 HANG：试 `CONTINUE_FROM_HANG`（看是否可软件恢复）
5. cancel 清场；恢复定位 / 推回路线
