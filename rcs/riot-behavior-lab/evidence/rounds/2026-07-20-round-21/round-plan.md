# Round 21（2026-07-20）— 旋钮三档：开机 / 解抱闸 / 关机

## 问题

车上旋钮三档对应 RIoT 哪些字段？MES 如何判定？

| 档位 | 物理含义 |
|---|---|
| 开机 | 正常可调度运行（当前档） |
| 解抱闸 | 可人工推动 |
| 关机 | 关断 |

## 候选观测面

- `getVehicleInfo`：`breakSwitchState`、`mode`、`controlState`、`hardwareState`、`powerMode`、`operationState`（previousState）、`sysState`
- `runtime/properties`：`breakSwState`、`operationState`、`sysState`、`powerState`、`hstate`
- `runtime/status`：关机后是否变 `offline`

## 步骤

1. E0：开机基线
2. 人工切 **解抱闸** → S1 采样
3. 人工切 **关机** → S2 采样
4. 人工切回 **开机** → S3 恢复确认 + 可选短距再派

## 授权

用户可按指示切换旋钮三档。
