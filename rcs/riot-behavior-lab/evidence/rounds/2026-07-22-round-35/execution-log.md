# Round 35 执行日志 — L1 开机后无法定位：HANG / CONTINUE

## L1 结果

- 订单：`riot-behavior-lab-R35-L1noloc-20260722-123103`
- 执行中关机 → offline 期间仍 `EXECUTING`
- 开机后**未定位**（`locationState=ERROR`，`control=ERR`），不取消：
  - 很快 **`HANG(9)`** + `INNER_FORCE_IDLE`
  - `m0_resultCode=0`，`failReason` 空（无电机偶发码）
- `CONTINUE_FROM_HANG` → **`code=0`**，订单 **`9→3`**
- 随后约 2min：保持 `orderState=3`，但 `loc` 仍未 RUNNING 时表现为 `proc=AWAITING_ORDER`、`move=MT_NA`、`progress` 不前进（**未真正跑起来**）
- 已 cancel 清场

## 结论

| 步骤 | 表现 |
|------|------|
| 关机期间 | EXECUTING（同 Round32） |
| 开机 + 未定位 + 不取消 | **进 HANG**（同 Round34 准确定位路径的「会进 HANG」） |
| CONTINUE（仍未定位） | 可离开 HANG 回到 EXECUTING，但**无法有效执行**（等定位） |

对照 Round34（开机定位准确）：CONTINUE 后可回 `MT_RUNNING`。  
错定位不测：见 Q-038。
