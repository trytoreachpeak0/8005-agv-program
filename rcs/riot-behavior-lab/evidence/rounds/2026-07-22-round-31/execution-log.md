# Round 31 执行日志 — 软件急停长监视（修订 Round27 B）

## 结果

- 订单：`riot-behavior-lab-R31-Bsw-20260722-095006`（多段 move，map30）
- `triggerEmergency` → `code=0`，`emergencyState=OK→CAN_RECOVER`，订单保持 `EXECUTING(3)`
- 监视约 **900s（15min）**：一直 **`orderState=3`**，`progress=11` 冻结，`proc=PROCESSING_ORDER`，`break=MOVABLE`，`faultCodes` 空
- **未出现 `HANG(9)`**
- 清场：`cancelEmergency` + cancel → `emerg=OK`，`proc=IDLE`，订单 `CANCELLED(2)`

## 结论（修订）

软件急停与硬件急停同类：**不会单独**把执行中订单打进 `HANG`；表现是 `EXECUTING` + 进度冻结 + `CAN_RECOVER`。
Round27 B 曾记「延迟数分钟后进 HANG」——以本轮长监视为准予以**纠正**；若急停期间另有故障态，可间接挂起，按故障路径处理，不建模为「软急停⇒HANG」。

调用方：用 `emergencyState=CAN_RECOVER` 识别；恢复靠 `cancelEmergency`（订单仍在 EXECUTING 时继续走即可，不必等 HANG / CONTINUE）。
