# Round 20（2026-07-20）— AGV 设备离线检测与恢复

## 问题

- 设备真正断连（非调度 `disable`）时，哪些字段变化？MES 如何判定「车离线」？
- 离线期间建单会怎样？
- 恢复上线后字段如何回到正常？能否再派单？

## 与 Round13 的区别

- Round13：调度 `serviceId=disable` → `integrationLevel=OFF_LINE`（API 可控）
- Round20：**设备连通性离线**（用户手工断连/关车通信），观察 `runtime/status` 等

## 范围

- 仅测试车：`新基测试300c协作1`
- 检测：`runtime/status`、`getVehicleInfo`、可选 `runtime/properties`
- 离线中：尝试短距建单（若可）
- 恢复后：确认 online + 可选短距 SUCCESS
- 不测：批量下线、非本车、改系统配置

## 步骤

1. E0：基线（预期 `status=online`，调度 `ON_LINE`）
2. 人工：用户让测试车离线
3. S1：密采样检测离线字段
4. S2：离线期间尝试建单（可 cancel）
5. 人工：用户让测试车上线
6. S3：确认恢复；可选短距再派
