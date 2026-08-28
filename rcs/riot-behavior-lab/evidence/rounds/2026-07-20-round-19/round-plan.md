# Round 19（2026-07-20）— 急停检测与解除

## 问题

- 急停发生后，调度/物模型侧哪些字段变化？MES 如何判定「处于急停」？
- 解除急停应调用哪个 API？解除后字段如何恢复？解除后能否再派单？

## 范围

- 仅测试车：`新基测试300c协作1`
- 检测面：`GET /api/task/v1/task/getVehicleInfo/{deviceKey}`（`emergencyState` 等）+ 可选 `runtime/properties`
- 解除：物模型服务 `cancelEmergency`（`POST .../command/sync/service/{deviceKey}/cancelEmergency`）
- **不下发** `triggerEmergency`（由用户现场主动急停）
- 不测：`reset`（重启 SRC）、全局急停、非本车

## 步骤

1. E0：基线（预期 `emergencyState=OK`）
2. 人工：用户对测试车下发急停
3. S1：密采样检测字段变化
4. S2：调用 `cancelEmergency` 解除
5. S3：确认恢复 `OK`；可选短距再派验证可接单

## 授权

- 用户：可主动下发急停；允许 API 解除急停。
