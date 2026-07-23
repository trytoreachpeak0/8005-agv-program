# Round 18 执行日志（2026-07-20）

## 环境

- 测试车：`新基测试300c协作1`，`ON_LINE` + `IDLE`
- 地图：**api测试2 / mapId=30**（7 站）
- 起点：站点 5（在站）
- 目的：补测 Q-028 — 换图后完整跑单到 `SUCCESS`（map28 Round16/17 未到站）
- 脚本：`run-round18.ps1`

## 结论摘要

### S1：`5 → 6` 完整 SUCCESS

- 建单前代价：站6=`2870`（同图最短正代价）
- 轨迹：`QUEUEING(1)` → `EXECUTING(3)` → `SUCCESS(5)`
- 执行中 `remain` 阶梯下降：`2620 → 1320 → 1070 → 0`，到站后回哨兵 `Long.MAX`
- 终态：`orderState=5`，`finalState=true`，`missionResultCode=900`，车停 **站点6**，`IDLE` / `MT_FINISHED`
- 全程约 **33s**

### S2：再派 `6 → 5` 亦 SUCCESS

- 代价约 `3120`；再次 `1→3→5`，车回 **站点5**
- 说明 map30 上可连续再派，与 map29 Round8 同构

### 与 map28 对照

- Round16/17（map28）：可派可跑，但窗口内卡在近终点 `remain` 不归零，未采到完整 SUCCESS
- Round18（map30）：短距闭环与再派均 SUCCESS

## 证据

- `E0-baseline.json` / `E0-map-resolve.json` / `E0-cost-candidates.json`
- `S1-create.json` / `S1-dense-samples.json` / `S1-final-order.json`
- `S2-redispatch-create.json` / `S2-redispatch-samples.json` / `S2-redispatch-final.json`
- `E9-final.json`
