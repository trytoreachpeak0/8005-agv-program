# Round 37（2026-07-22）— 单机系统点暂停（非 RIoT HELD）

## 问题

在 AGV **单机系统**里点暂停（不是 RIoT `CMD_ORDER_HELD`）时：
- 订单 `orderState` / 车 `movementState` / `procState` 变成什么？
- 是否进 HELD(7) 或 HANG(9) 或仍 EXECUTING？
- `CONTINUE_FROM_HELD` / `CONTINUE_FROM_HANG` / RIoT `HELD` / CANCEL 哪个有效？

## 步骤

1. 长单 → EXECUTING
2. 人工在单机点暂停
3. 密采样；试 CONTINUE_FROM_HELD、CONTINUE_FROM_HANG；按结果决定是否再试 HELD/CANCEL
4. 清场

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
