# Round 29（2026-07-22）— 本体异常态下建新单：QUEUEING 还是 EXECUTING

## 问题

车空闲但本体异常时新建 `byDefaultMissions`：订单是长期 `QUEUEING`，还是进入 `EXECUTING`（再卡住）？

## 场景

| 标签 | 触发（人工/API） | 建单时机 |
|------|------------------|----------|
| A | 硬件急停 | IDLE + `CAN_NOT_RECOVER`（或急停态）后建单 |
| B | 软件急停 `triggerEmergency` | IDLE + `CAN_RECOVER` 后建单 |
| F | 旋钮解抱闸 | IDLE + `UNMOVABLE` 后建单 |

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
- 短距/中距单段 move 即可；监视约 60–90s 是否离开 QUEUEING

## 每场景

1. 确认 IDLE、无残留单
2. 进入异常态
3. 建单 + 密采样 orderState / executeVehicleKey / 车态
4. cancel 清场 + 恢复本体（松急停 / cancelEmergency / 拨开机）
