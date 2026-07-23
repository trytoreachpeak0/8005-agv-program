# Round 14（2026-07-20）— 按车查单与积压清队

## 问题

- **Q-025**：如何获取某一车辆的非终态订单（含 QUEUEING / EXECUTING / HELD），并取消队列中或挂起的积压单，使新订单可以生效？

## 目标

1. 确认 `GET /api/order/v1/orderRecord` 按车过滤的可用参数（SCHEMA：`executeVehicleKey`、`filterByState`；试探 `appointVehicleKey`）。
2. 制造积压：一单 EXECUTING + 至少一单 QUEUEING（可选再 HELD）。
3. 验证列表能否检出积压；对 QUEUEING/HELD 批量 `CMD_ORDER_CANCEL` 后，新单能否进入执行。

## 范围

- 只写测试车 `新基测试300c协作1`；mapId=29；短距 1↔2。
- 不做充电/停靠；不做 FAILED 诱导。

## 批准写接口

- `POST /api/order/v1/add/byDefaultMissions`
- `POST /api/task/v1/order/command/{orderId}`（`CMD_ORDER_CANCEL` / 可选 `CMD_ORDER_HELD`）
- 必要时 `updateVehicleIntegrationLevel`（`enable` 恢复）

## 步骤

1. E0 基线：车态 + 按车列表（非终态）
2. S1 只读探针：多种 filter 组合
3. S2 制造积压并列表对照
4. S3 取消 QUEUEING（及 HELD）后建新单验证
5. S4 收尾：取消残留、恢复 IDLE
