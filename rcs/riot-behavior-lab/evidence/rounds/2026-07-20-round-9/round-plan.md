# Round 9（2026-07-20）

## 1. 研究目标

- Q-006（部分）/ Q-012：`interrupt` 与 `cancel` 在执行中订单上的真实效果与善后。
- 对照成功路径（Round 8）的状态面。

## 2. 范围

- 仅测试车；map29；`byDefaultMissions` 建单
- E3：`POST /api/task/v1/order/interrupt`（`pause=true`，最小 body）
- Cancel：`POST /api/task/v1/order/command/{orderKey}` + `CMD_ORDER_CANCEL`（`disableVehicle=false`）
- 不做：对终态/不存在 orderId 的反例（可后补）；不做全局清理

## 3. 授权

- 用户：允许测 cancel / interrupt。

## 4. 安全

- 写操作仅带测试车 key；interrupt 后必须善后到可接单，再测 cancel。
- 若车长期挂起：API cancel → 仍失败则停测升级人工。
