# Round 8 执行日志

## 环境与基线

- 测试车：`新基测试300c协作1`，`ON_LINE` / `enable=true` / `IDLE` / 站1
- 地图 map29：站1 y=-480；站2 y=-2440（用户拉长后）
- D1 代价：1960（Round7 约 1040）
- 建单：`POST /api/order/v1/add/byDefaultMissions`，目的站 2

## 执行

- `upperId` / `orderId`：见 `runs/E1-create.json`
- 密采样间隔约 0.8s，共 **57** 点；全程约 **52s**
- `executeVehicleKey` 全程测试车；无误派

## 状态流转（摘要）

| t | orderState | missionState | procState | movementState | station |
|---|---|---|---|---|---|
| 发单前 | — | — | IDLE | MT_FINISHED | 1 |
| ~1s | 1 | 0 | IDLE | MT_FINISHED | 1 |
| ~6s | 3 | 1 | PROCESSING_ORDER | MT_RUNNING | 0 |
| ~52s | 3 | 1 | AWAITING_ORDER | MT_FINISHED | 2 |
| ~53s | 5 | 2 | IDLE | MT_FINISHED | 2 |

- 物理到站（站2 + MT_FINISHED）早于 `orderState=5`
- `progress` 自进入 EXECUTING 起即为 100
- mission 完成 `resultCode=900`

## 证据

- `runs/E0-baseline.json`
- `runs/E1-create.json`
- `runs/E2-dense-samples.json`

## 结论

- Q-002 / Q-005 成功路径：`SUPPORTED` → state-model + BC-STATE-003
- 拉长站距后足以观测并行状态面；短距 Round7 窗口过窄的问题已缓解
