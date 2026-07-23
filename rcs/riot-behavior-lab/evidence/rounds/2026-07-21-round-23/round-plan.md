# Round 23（2026-07-21）— 定位 / 未定位状态检测与再派

## 问题（Q-032）

- 已定位 vs 未定位时，哪些字段可靠变化？
- 未定位时建单 / 路由会怎样？
- 重新定位后字段如何恢复？能否再派？

## 与「在站/离站」的区别

- Round6 BC-STATE-002：`currentStation=0` = **未归属站点**，仍可能 `locationState=RUNNING`（定位正常、只是离站）
- 本轮：测 **定位开关/定位丢失**（`locationState` / `confidence` 等），不是站归属

## 范围

- 仅测试车：`新基测试300c协作1`
- 读：`getVehicleInfo`、`runtime/status`、`runtime/properties`
- 可选写：`stopLocation` / `startLocation` API 探针；未定位期间短距建单（可 cancel）
- 人工：网页或车端「停止定位」「重新定位」

## 步骤

1. E0：已定位基线（用户确认当前已定位）
2. 人工：停止定位
3. S1：密采样未定位字段
4. S2：未定位期间建单 / 路由探针
5. 人工：重新定位
6. S3：确认恢复；可选短距再派
