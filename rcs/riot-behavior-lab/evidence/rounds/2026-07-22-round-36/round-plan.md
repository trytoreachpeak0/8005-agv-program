# Round 36（2026-07-22）— 暂停（HELD）补充

## 已有（Round10，不重复当主结论）

- 执行中 `CMD_ORDER_HELD` → `orderState=7`，`USER_FORCE_IDLE`，`MT_PAUSED`
- `CMD_ORDER_CONTINUE_FROM_HELD` → 回 EXECUTING → SUCCESS
- `interrupt` 不能当暂停

## 本轮补测

| 标签 | 内容 |
|------|------|
| P1 | map30 复核：HELD → CONTINUE_FROM_HELD → 是否可 SUCCESS |
| P2 | HELD 后 `CMD_ORDER_CANCEL` → 是否 CANCELLED + 车 IDLE |
| P3 | 错用命令：EXECUTING 时 CONTINUE_FROM_HELD；HELD 时 CONTINUE_FROM_HANG |
| P4 | 一单 HELD 中，同车再建一单 → QUEUEING 还是怎样 |

## 范围

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`
- 地图：api测试2 map30
- 前置：定位成功、开机、急停 OK、抱闸 MOVABLE、IDLE
