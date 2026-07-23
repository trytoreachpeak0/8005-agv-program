# Round 37 执行日志 — 单机系统点暂停

## 订单

`riot-behavior-lab-R37-OnboardPause-20260722-131300`

## 观察

### 1) 单机点暂停（非 RIoT HELD）

- `movementState=MT_PAUSED`，`speed=0`
- **订单仍为 `EXECUTING(3)`**，`proc=PROCESSING_ORDER`
- **不是** `orderState=7 HELD`，也不是 `HANG(9)`
- `emergencyState=OK`

### 2) RIoT 命令探针（仍单机暂停时）

| 命令 | code | 效果 |
|------|------|------|
| `CONTINUE_FROM_HELD` | **100020** | 无效（订单不是暂停态） |
| `CONTINUE_FROM_HANG` | **100021** | 无效 |
| `CMD_ORDER_HELD` | **0** | 订单 `3→7`，`proc=USER_FORCE_IDLE`，仍 `MT_PAUSED` |

### 3) 单机恢复 + CONTINUE_FROM_HELD

- 单机恢复后采样：`orderState=7`，`move=MT_FINISHED`，`proc=USER_FORCE_IDLE_FINISHED`
- `CONTINUE_FROM_HELD` → **`code=0`** → 回 `EXECUTING` / `MT_RUNNING`
- 最终 **`SUCCESS(5)`**，`progress=100`，mission `resultCode=900`「订单完成」

## 结论

1. **单机暂停 ≠ RIoT HELD**：只反映在车运动态 `MT_PAUSED`，订单可仍为 EXECUTING。  
2. 仅靠 `CONTINUE_FROM_HELD/HANG` **不能**解除单机暂停。  
3. 可行恢复路径（本轮）：单机恢复后，若订单已被打成 HELD(7)，再用 `CONTINUE_FROM_HELD` 可继续并 SUCCESS。  
4. 若业务只遇到单机暂停、订单仍为 3：应先在单机恢复；是否还需 RIoT HELD/CONTINUE 视当时 `orderState` 而定。

## 未覆盖（已由 B 补测覆盖）

见下方 **B — 仅单机暂停/恢复**。

## B — 仅单机暂停/恢复（不发 RIoT HELD）

- 订单：`riot-behavior-lab-R37-OnboardPause-20260722-132036`
- 单机暂停：`orderState=3` + `MT_PAUSED`
- **仅单机恢复**（全程未发 HELD/CONTINUE）：自行回到 `MT_RUNNING`，最终 **`SUCCESS(5)`**，`progress=100`

## 结论（修订）

1. **单机暂停 ≠ RIoT HELD**：车 `MT_PAUSED`，订单可仍 EXECUTING。  
2. **仅单机恢复即可继续跑完**（本轮 B），无需 RIoT CONTINUE。  
3. RIoT `CONTINUE_FROM_HELD/HANG` **不能**解除单机暂停（本轮 A 探针）。  
4. 若误把订单打成 RIoT HELD(7)：需单机恢复 + `CONTINUE_FROM_HELD`（本轮 A 路径）。
