# Round 34 执行日志 — 关机恢复重测（无偶发电机故障）

## 结果

- 订单：`riot-behavior-lab-R34-PoffRec-20260722-105205`
- 关机期间：`runtime=offline`，订单保持 **`EXECUTING(3)`**
- 拨回开机、**不取消**：很快 **`HANG(9)`** + `INNER_FORCE_IDLE`
  - **无** `320025`；`failReason` 空；`m0_resultCode=0`
  - 车态：`control=OK`，`emerg=OK`，`break=MOVABLE`，`lastErrorCode=0`
- `CONTINUE_FROM_HANG` → **`code=0`**，订单 **`9→3 EXECUTING`**，`MT_RUNNING`
- 随后约 3min 监视：`orderState` 保持 3，但本窗 `progress` 未前进、`speed=0`（是否最终 SUCCESS 非本轮必达）
- 已 cancel 清场

## 结论（取代 Round33 主结论）

执行中关机 → 不取消 → 拨回开机：

1. **会进 HANG**（与偶发电机故障无关）
2. **可用 CONTINUE 拉回 EXECUTING**（本轮无电机错时成立）
3. Round33 的 `320025` 见旁证，不并入本因果

Round33 偶发记录：[../2026-07-22-round-33/incidental-motor-fault-320025.md](../2026-07-22-round-33/incidental-motor-fault-320025.md)
