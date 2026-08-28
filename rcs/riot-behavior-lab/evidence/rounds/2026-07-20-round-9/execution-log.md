# Round 9 执行日志

## 基线

- 测试车 ON_LINE / enable / IDLE @站2
- 建单：`byDefaultMissions`

## E3 interrupt（执行中纯 move）

- 订单进入 `orderState=3` + `MT_RUNNING` 后调用：
  - `POST /api/task/v1/order/interrupt`
  - body：`{"orderId":"<string orderId>","pause":true}`
- **结果失败**：`code=100036`，`message=中断订单的当前子任务索引不为移动任务`
- 随后 ~10s 采样：订单仍 `3` / `PROCESSING_ORDER` / `MT_RUNNING`，**无暂停/挂起**
- 证据：`E3-interrupt-call.json`，`E3-after-interrupt-samples.json`

## 善后 cancel（同一笔 interrupt 失败单）

- `POST /api/task/v1/order/command/{orderId}`  
  body：`{"commandType":"CMD_ORDER_CANCEL","disableVehicle":false,"reason":"..."}`
- **成功** `code=0` → 很快 `orderState=2 CANCELLED`，车 `IDLE` / `MT_FINISHED`
- 取消后车可能停在**离站**（`currentStation=0`），但仍可接单
- 证据：`E3-cleanup-cancel-attempts.json`，`E3-cleanup-samples.json`

## EC 执行中 cancel（独立一笔）

- 同样在 `3`+`MT_RUNNING` 时发 `CMD_ORDER_CANCEL`
- **成功**：`orderState=2`，`missionState=4`，`procState=IDLE`，`finalState=true`
- `executeVehicleKey` 仍为测试车
- 证据：`EC-cancel-call.json`，`EC-after-cancel-samples.json`

## 恢复对照

- cancel 后离站再建单，跑到站2：`orderState=5` + `IDLE` @站2
- 证据：`ER-recovery-samples.json`

## 结论摘要

| 操作 | 纯 move 执行中 | 终态/车侧 |
|---|---|---|
| `interrupt`+`pause=true` | **拒绝** `100036`，状态不变 | — |
| `command` `CMD_ORDER_CANCEL` | **有效** | `orderState=2`，车 IDLE（可离站） |
| 取消后再派 | 可用 | 可再次 SUCCESS |
