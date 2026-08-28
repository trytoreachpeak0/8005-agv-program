# Round 38 执行记录 — 单机「去站点」过程中建单 / HANG+CONTINUE

车：`BROKERX-aee2f93d717546cf9510c98c854fe83e` · 地图：api测试2 map30

## M1 — 单机去站点过程中 RIoT 建单

| 步骤 | 结果 |
|---|---|
| 单机开始去站点 | `MT_RUNNING`，`proc=IDLE` |
| 移动中建单 `...M1-20260722-135149` | `code=0`，立即 **`QUEUEING(1)`**，`execute=--` |
| 单机仍在跑（约 2+ min） | 订单**一直 QUEUEING**，不抢占单机任务 |
| 单机到站 `st=3` `MT_FINISHED` | 约 2s 内订单 → **`EXECUTING(3)`**，`PROCESSING_ORDER` |

结论：单机去站点占用期间，新 RIoT 单进队不执行；单机到位空闲后才开跑。

## H1 — HANG 时单机去站点过程中 CONTINUE

| 步骤 | 结果 |
|---|---|
| RIoT 长单执行中 | `...H1-20260722-135632` → EXECUTING |
| 单机取消移动 | → **`HANG(9)`**，`failReason=订单被取消,导致订单挂起`，`m0=901` |
| 单机再去站点（HANG 中） | `MT_RUNNING`，`proc=INNER_FORCE_IDLE` |
| 移动中 `CONTINUE_FROM_HANG` | API **`code=0`**，但订单**仍 HANG(9)**；`failReason` 变为 **「启动移动任务时,上一个任务在运行」** |
| 单机到站 `st=6` `MT_FINISHED` 后再 CONTINUE | API `code=0`，订单 **9→3 EXECUTING**，随后 **SUCCESS(5)** |

结论：**移动过程中 CONTINUE 不可真正恢复**（接口成功≠状态恢复）；须等单机任务结束后再 CONTINUE。

## 不作

「先 QUEUE 再单机去站点」：与可操作前提互斥（急停等），NA。

## 产物

`runs/M1-*`、`runs/H1-*`（含 `H1-summary-midmove.json` 为移动中 CONTINUE 快照）
