# Round 22 执行日志（2026-07-21）— 旋钮三档复测（5G 独立供电）

## 环境

- 测试车：`新基测试300c协作1`
- 与 Round21 差异：**5G 模块独立供电**，关机不再切断客户端访问路径

## 三档对照（稳态）

| 档位 | API 可达 | `runtime/status` | `breakSwitchState` | `breakSwState` | `controlState` |
|---|---|---|---|---|---|
| **开机** | 是 | `online` | `MOVABLE` | `1` (OFF) | `OK` |
| **解抱闸** | 是 | `online` | `UNMOVABLE` | `2` (ON) | `ERR` |
| **关机** | **是** | **`offline`** | 末值 `UNMOVABLE` | 属性常空 | `ERR` |

### 相对 Round21 的关键结论

- Round21 关机时 API 超时，是车端给 5G 断电导致客户端断网。
- Round22：**关机时 `apiReachable=true` 且 `status=offline`**，证明判定应看 `runtime/status`，与客户端链路无关。

## 过程

1. E0 开机基线：`online` / `MOVABLE` / `bProp=1` / `control=OK`
2. 解抱闸：约 10s 内命中 `UNMOVABLE` + `bProp=2` + `control=ERR`
3. 关机：API 持续可达，约 15s 内命中 `status=offline`
4. 切回开机：经 `offline` → `online`（中间可见 `break=UNKNOWN` / `bProp=0`）→ 最终 `MOVABLE` + `bProp=1` + `control=OK`
5. 再派：恢复后 `station=0`，map30 全站 `costs=-1` unreachable，**跳过** SUCCESS 再派（记 `S4-redispatch-skipped.json`）

## 证据

- `E0-boot-baseline.json`
- `S-hit-release-brake.json` / `S-settle-release-brake.json`
- `S-hit-power-off.json` / `S-settle-power-off.json`
- `S-hit-boot.json` / `S-settle-boot.json`
- `E9-final.json` / `S4-redispatch-skipped.json`
