# Round 20 执行日志（2026-07-20）— 设备离线检测与恢复

## 环境

- 测试车：`新基测试300c协作1`，map30 / 站2
- 离线/上线由用户手工操作（断连通信）；非 Round13 的调度 `disable`

## 1) 检测（SUPPORTED）

| 字段 | 在线 | 设备离线后 |
|---|---|---|
| `runtime/status.type` | `online` | **`offline`** |
| 调度 `enable` / `integrationLevel` | `true` / `ON_LINE` | **不变** |
| `emergencyState` / `controlState` | `OK` | 不变 |

- MES 判定**设备离线**：`GET /api/device/v1/runtime/status/{deviceKey}` → `result.type != online`
- **不能**用调度 `ON_LINE` 代替设备在线；二者解耦（对照 Round13：调度 `OFF_LINE` 时设备仍可 `online`）
- 证据：`E0-baseline.json`、`S1-watch-offline-samples.json`、`S1-offline-hit.json`

## 2) 离线期间建单

- `byDefaultMissions` → **`code=0` 成功**，进 `QUEUEING(1)`，`execute=--`
- ~45s 内不进入 `EXECUTING`；cancel 可清
- 结论：设备离线**不在建单口拒绝**；会挂队列，需业务先查 `runtime/status`
- 证据：`S2-create-while-offline.json`、`S2-samples.json`

## 3) 上线恢复

- 用户恢复通信后约 1–2 分钟采到 `status=online`
- 调度字段全程 `ON_LINE`（本轮未改）
- 证据：`S3-watch-online-samples.json`、`S3-online-hit.json`

## 4) 恢复后再派

- 短距 `2→1`（代价 1590）建单成功，约 3s 进 `EXECUTING` / `PROCESSING_ORDER`
- 180s 窗口内未到站（`station` 保持 0），timeout cancel
- 结论：**上线后可再派并进入执行**；完整 SUCCESS 非本轮必达（路径/现场条件）
- 收尾：`E9-final.json`（cancel 中）→ `E9-settled.json`

## 与 Round13 对照

| 维度 | Round13 调度 disable | Round20 设备断连 |
|---|---|---|
| 主信号 | `integrationLevel=OFF_LINE` | `runtime/status=offline` |
| 另一侧 | 设备仍可 online | 调度仍可 ON_LINE |
| 离线建单 | 成功→QUEUEING | 成功→QUEUEING |
