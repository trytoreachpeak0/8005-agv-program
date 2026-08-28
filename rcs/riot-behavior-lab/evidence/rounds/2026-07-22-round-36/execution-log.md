# Round 36 执行日志 — 暂停（HELD）补充（地图调整后重跑）

## 环境

- 车：`BROKERX-aee2f93d717546cf9510c98c854fe83e`，api测试2 map30
- 前两次 attempt 因地图/网关问题作废；本轮为有效结论

## P1 — HELD → CONTINUE_FROM_HELD → SUCCESS

- HELD `code=0` → `orderState=7`，`USER_FORCE_IDLE`，`MT_PAUSED`
- CONTINUE_FROM_HELD `code=0` → 回 EXECUTING
- 最终 **`orderState=5 SUCCESS`**，`progress=100`，车 `IDLE`
- uid：`…R36-P1-20260722-130456`

## P2 — HELD 后 CANCEL

- HELD → `orderState=7`
- `CMD_ORDER_CANCEL` `code=0` → **`CANCELLED(2)`**，车 **`IDLE`**
- uid：`…R36-P2-20260722-130711`

## P3 — 错用 CONTINUE

| 时机 | 命令 | 结果 |
|------|------|------|
| EXECUTING | `CONTINUE_FROM_HELD` | **`100020`**「订单不是暂停状态…」，状态仍为 3 |
| HELD(7) | `CONTINUE_FROM_HANG` | **`100021`**，状态仍为 7 |
| HELD(7) | `CONTINUE_FROM_HELD` | **`0`**，可恢复 |

## P4 — 暂停中再建单

- A 保持 HELD(7) 时建 B：`code=0` → B 约 60s **一直 QUEUEING(1)**，`executeVehicleKey=--`
- A 仍为 7，不自动被 B 抢占

## 结论（补充 BC-ORDER-006）

1. 暂停/恢复主路径在 map30 复核成立，可跑到 SUCCESS。  
2. HELD 可用 CANCEL 清掉。  
3. CONTINUE 命令必须配对：HELD↔`CONTINUE_FROM_HELD`；HANG↔`CONTINUE_FROM_HANG`；混用分别 `100020`/`100021`。  
4. 车被 HELD 占用时，同车新单进 QUEUEING 不执行。
