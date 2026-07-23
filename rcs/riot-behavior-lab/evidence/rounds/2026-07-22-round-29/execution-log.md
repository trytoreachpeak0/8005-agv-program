# Round 29 执行日志 — 本体异常态下建新单

## 状态

**完成**（A/B/F）

## 环境

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`，map30 api测试2
- 建单：`byDefaultMissions` 单段 move；监视约 90s

## 结果汇总

| 场景 | 建单前车态 | 建单 | 90s 内 | 车侧 |
|------|------------|------|--------|------|
| A 硬件急停 | `CAN_NOT_RECOVER` + IDLE | `code=0` | **一直 `QUEUEING(1)`**，`execute=--` | 仍 IDLE |
| B 软件急停 | `CAN_RECOVER` + IDLE | `code=0` | **一直 `QUEUEING(1)`**，`execute=--` | 仍 IDLE |
| F 解抱闸 | `UNMOVABLE` + `CONTROL_STATE_ERR` + IDLE | `code=0` | **一直 `QUEUEING(1)`**，`execute=--` | 仍 IDLE |

证据：`A-summary.json` / `B-summary.json` / `F-summary.json` 及对应 `*-watch-samples.json`

## 结论

本体异常（急停 / 解抱闸）且车空闲时：**新单可成功创建，但不会进入 EXECUTING，滞留 QUEUEING**（与未定位、OFF_LINE、断连同类）。

建单前应读：`emergencyState`、`breakSwitchState`（及已有 `locationState` / 调度上下线）。
