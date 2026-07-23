# Round 8（2026-07-20）

## 1. 研究目标

- 在用户拉长 map29 站1↔站2 距离后，完整观测一笔指定车移动订单的**状态流转**。
- 重点：`orderState`、`missionState`、`procState`、`movementState`、站号/坐标的时间序列（Q-002 / Q-005 部分）。

## 2. 范围

- 仅测试车 `新基测试300c协作1`
- mapId=29；本轮方向：站1 → 站2
- 建单：`POST /api/order/v1/add/byDefaultMissions`（BC-ORDER-001）
- 不用车辆组；不做 cancel/interrupt（本轮只观测成功路径）

## 3. 授权

- 用户：拉长站点距离后，允许完整测试任务操作与状态流转。

## 4. 基线摘要

- 上线：`ON_LINE` / `enable=true` / `IDLE` / station=1
- 新站坐标：站1 y=-480；站2 y=-2440（较 Round7 的 -1520 更远）
- D1 代价：1960（Round7 约 1040）
