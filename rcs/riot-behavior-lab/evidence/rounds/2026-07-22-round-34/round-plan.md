# Round 34（2026-07-22）— 关机恢复重测（排除偶发电机故障）

## 问题

Round33 开机后进 HANG 时伴随 `320025`，现场判断为偶发。本轮重测同一路径，确认**无电机故障**时：拨回开机且不取消，订单是继续执行、进 HANG，还是其它。

## 步骤

1. 确认车健康：`emerg=OK`、`break=MOVABLE`、`control=OK`、`lastErrorCode=0`、无 fault
2. 长单 → EXECUTING
3. 拨关机 → offline（短持）
4. 拨回开机 → online，**不 cancel**
5. 监视终态；记录 `resultCode`/`faultCodes`，若再出现 320025 则本轮作废重做
6. 若进 HANG 且无电机错误 → 试 CONTINUE

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
