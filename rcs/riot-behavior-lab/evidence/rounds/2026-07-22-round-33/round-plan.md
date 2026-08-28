# Round 33（2026-07-22）— 执行中关机后不取消，拨回开机看订单去向

## 问题

Round32：执行中关机约 15min 仍 `EXECUTING`，但随后 **cancel 清场**，未观察恢复路径。
本轮：**不 cancel**，关机一段时间后拨回开机，看订单是继续跑完 / 进 HANG / 卡住 / 其它终态。

## 步骤

1. 长单 → `EXECUTING`
2. 人工拨关机 → 确认 `runtime=offline`（短等约 1–2min 即可，不需 15min）
3. 人工拨回开机 → 确认 `runtime=online`
4. **不 cancel**，监视订单至 SUCCESS / HANG / 其它终态或超时（约 10min）
5. 若卡住再按需 cancel / CONTINUE 探针

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
