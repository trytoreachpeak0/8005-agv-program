# Round 23 执行日志 — 定位 / 未定位

## 状态

完成（Q-032 `SUPPORTED`）

## 记录

### E0 已定位基线

- `locationState=LOCATION_STATE_RUNNING`，`prop_locationState=3`，`confidence=58`
- `status=online`，`controlState=OK`，`station=0`（离站但仍定位）
- `mapName=api测试2`
- 证据：`runs/E0-localized-baseline.json`

### S1 停止定位后

- `locationState=ERROR`，`prop_locationState=1`，`prev_locationState=1`
- `controlState=CONTROL_STATE_ERR`，聚合 `state=ERROR`
- `confidence` 仍为 58（不可单独当「仍定位」）
- `status` 仍 `online`，调度 `ON_LINE`/`enable` 不变；`mapName`/坐标仍可读
- 证据：`runs/S1-hit-unlocalized.json`

### S2 未定位期间探针

- 路由（map29 探针）：站1/2 → `costs=-1` unreachable；站3/4/5 → `code=10006`
- 建单：`byDefaultMissions` 仍 `code=0`，订单挂 `QUEUEING`，约 25s 未进 EXECUTING
- 已 cancel 清理成功
- 证据：`runs/S2-*`

### S3 重新定位

- 过渡：`prop_locationState` 曾见 `1 → 2 → 4 → 3`
- 稳态：`locationState=LOCATION_STATE_RUNNING`，`prop=3`，`confidence=99`，`control=OK`，`state=IDLE`
- 证据：`runs/S3-hit-localized.json` / `S3-watch-localized-samples.json`

### S4 重定位后再派（map30）

- 目的站 3，`cost=250`，进 `EXECUTING` → `SUCCESS`（约 35s）
- 终态：`station=3`，`loc=RUNNING`，`proc=IDLE`
- 证据：`runs/S4-*` / `E9-final.json`

## 结论摘要

| 场景 | 主信号 | 旁证 |
|---|---|---|
| 已定位 | `locationState=LOCATION_STATE_RUNNING` 且 `prop_locationState=3` | `control=OK`；`confidence` 可高可低 |
| 未定位 | `locationState=ERROR` 且 `prop_locationState=1` | `control=ERR`，`state=ERROR` |
| 勿混淆 | `currentStation=0` = 离站，**不等于**未定位 | 未定位时坐标/`mapName` 仍可能可读 |
| 未定位建单 | 可 `code=0` 进 `QUEUEING`，短时不执行 | 路由常 unreachable |
| 恢复 | 重定位后可再派并 `SUCCESS` | 中间态可见 prop `2`/`4` |
