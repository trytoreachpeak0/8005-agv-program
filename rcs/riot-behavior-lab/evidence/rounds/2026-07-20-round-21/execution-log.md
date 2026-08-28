# Round 21 执行日志（2026-07-20）— 旋钮三档：开机 / 解抱闸 / 关机

## 环境

- 测试车：`新基测试300c协作1`
- 旋钮由用户手工切换；API 只读观测

## 三档对照（稳态）

| 档位 | `runtime/status` | `breakSwitchState` | `breakSwState` | `controlState` |
|---|---|---|---|---|
| **开机** | `online` | **`MOVABLE`** | **`1` (OFF)** | **`CONTROL_STATE_OK`** |
| **解抱闸** | `online` | **`UNMOVABLE`** | **`2` (ON)** | 常变 **`CONTROL_STATE_ERR`** |
| **关机** | **`offline`** | 末值常 `UNMOVABLE` | 属性常空 | `CONTROL_STATE_ERR` |

说明：

- 物模型 `breakSwState`：`0=NA,1=OFF,2=ON`（属性名「解抱闸状态」）
- 调度枚举 `breakSwitchState`：`MOVABLE`/`UNMOVABLE` 与直觉相反——**解抱闸档反而是 `UNMOVABLE`**
- MES 推荐主判据：
  - 开机 vs 解抱闸：看 `breakSwState`（或 `breakSwitchState`），**不要**只看 `mode`（本轮三档多为 `MODE_AUTO`）
  - 关机：看 `runtime/status.type=offline`（与 Round20 设备断连同信号面）

## 过程摘要

1. **E0 开机基线**：`online` / `MOVABLE` / `breakSwState=1` / `control=OK`
2. **解抱闸**：约数十秒后采到 `UNMOVABLE` + `breakSwState=2`；settle 中 `control`→`ERR`
3. **关机**：旋钮关机时车端电源停止给 **5G 模块**供电，本机经 5G 访问 RIoT 会中断（HTTP 超时）——**不是** RIoT 服务宕机，也**不是**状态字段“滞后”。网络恢复后补采到 `status=offline`
4. **切回开机**：5G/链路恢复后可再读到车态；回到 `MOVABLE`+`breakSwState=1`+`control=OK`
5. **恢复后再派**：可建单并进 `EXECUTING`；120s 未到站已 cancel（完整 SUCCESS 非本轮必达）

## 证据

- 开机：`E0-boot-baseline.saved.json` / `SNAP-boot-final.json` / `S-hit-boot-restore.json`
- 解抱闸：`S-hit-release-brake.json` / `S-settle-release-brake.json`
- 关机：`S-hit-power-off.json` / `S-settle-power-off.json`
- 再派：`S3-create.json` / `S3-samples.json` / `E9-final.json`
