# HangContinue 与 OrderContinue 分开具名封装

第一版 SDK 同时提供 OrderContinue（`CONTINUE_FROM_HELD`）与 HangContinue（`CONTINUE_FROM_HANG`），不合并为按 orderState 自动选命令的单一 Continue。Lab 已证混用分别返回 `100020`/`100021`。MES 普通 OrderHang 策略消费 HangContinue；充电失败改派不把 HangContinue 当默认恢复。

**Status**: accepted
