# 旁证记录 — 电机故障 320025（Round33 偶发，非关机恢复主结论）

## 说明

Round33 在「执行中关机 → 不取消 → 拨回开机」路径上，开机后曾观测到：

- `orderState=9 HANG`
- `resultCode=320025` / 文案「电机1错误,不能启动移动任务」
- `controlState=CONTROL_STATE_ERR`
- `CMD_ORDER_CONTINUE_FROM_HANG` 返回 `code=0`，但订单仍停在 9

**现场判断**：该电机错误为**偶发故障**，不应并入「关机恢复」因果结论。关机恢复主路径以 **Round34 重测**为准。

## 单独可记点（故障旁证）

- 存在 `320025` 时，CONTINUE 业务码可为 `0` 但订单不真正离开 HANG
- 调用方勿仅凭 CONTINUE=`0` 认定已恢复；应核对 `orderState` 与车态/`resultCode`

## 证据文件（Round33）

- `runs/S7-hang-detail-utf8.json`
- `runs/S6-cont-*.json`
- `execution-log.md`（已标注本故障为旁证）
