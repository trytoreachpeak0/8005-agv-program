# Round 31（2026-07-22）— 软件急停长监视：是否单独进 HANG

## 问题

Round27 曾记「软件急停可延迟数分钟后进 HANG」。现场纠正：软件急停本身也**不会**因延迟而进 HANG。
本轮用长订单 + 长监视复核；若数分钟至约 10–15min 仍为 `EXECUTING`，则修订 Q-035 / BC-ORDER-015。

## 步骤

1. 基线：IDLE、online、急停 OK、抱闸 MOVABLE
2. 多段 move 长单 → 等 `EXECUTING`
3. API `triggerEmergency` → `CAN_RECOVER`
4. 监视 ≥10min：是否出现 `orderState=9`
5. 清场：`cancelEmergency` + cancel 订单

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
