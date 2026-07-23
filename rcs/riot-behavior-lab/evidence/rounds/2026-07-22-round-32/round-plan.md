# Round 32（2026-07-22）— 执行中旋钮关机：是否进 HANG

## 问题

关机态建新单已确认长期 QUEUEING（Round30 P）。本轮测：**订单已 EXECUTING 时拨关机**，是否进 `orderState=9 HANG`，以及如何恢复。

## 步骤

1. 基线 IDLE、online
2. 多段长单 → `EXECUTING`
3. 人工拨**关机**；脚本等 `runtime/status=offline`
4. 监视约 10–15min 是否 HANG
5. 清场：cancel；人工拨回开机

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
- 前提：5G 独立供电（关机后 API 仍可达）
