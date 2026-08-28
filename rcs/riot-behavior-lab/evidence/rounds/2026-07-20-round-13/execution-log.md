# Round 13 执行日志（2026-07-20）

目标：① disable 后建单；③ 失败/不可达路径；④ 执行中 disable。不做充电/停靠。

## E0

站 1，`ON_LINE` / `IDLE`。收尾站 2，`ON_LINE` / `IDLE`。

## S1：OFF_LINE 后建单

1. `serviceId=disable` → `enable=false`，`integrationLevel=OFF_LINE`
2. `byDefaultMissions` 同图短距 → **`code=0` 成功建单**，`orderState=1 QUEUEING`，`execute` 空
3. 立即 cancel → `orderState=2`；车仍 `OFF_LINE`
4. `enable` 恢复

**结论：调度下线不会在建单接口拒绝订单**；会进队列。业务必须自己先查 `ON_LINE`。

证据：`S1-disable.json`，`S1-create-while-offline.json`，`S1-unexpected-created-final.json`

## S3：跨图不可达（失败路径尝试）

1. `getRouteCostsBy` map26/站1：`costs=-1`，`vehicle route to station unreachable`
2. `byDefaultMissions` `mapId=26,destination=1` → **建单成功**，`orderState=1`
3. 观察 ~90s：一直 `QUEUEING`，`execute=--`，**未进入 `orderState=4 FAILED`**
4. cancel → `CANCELLED`

**结论：不可达目的站不会在建单时拒绝，也不会短时自动 FAILED；会挂在 QUEUEING。** 本轮未观测到 `orderState=4`。

证据：`S3-route-cost-map26.json`，`S3-create-unreachable.json`，`S3-unreachable-samples.json`

## S4：执行中 disable

1. 建单进 `EXECUTING` / `MT_RUNNING`
2. `serviceId=disable` → 车 `OFF_LINE`，但订单 **继续 `orderState=3` + `PROCESSING_ORDER` + `MT_RUNNING`**（采样全程无终态）
3. cancel 善后 + `enable` 恢复
4. 对照再派 SUCCESS

**结论：执行中 disable 不会自动取消/失败当前单；车被标下线但运动任务可继续。** 隔离车需先 cancel（或等 SUCCESS）再 disable，或接受“下线仍跑完当前单”。

证据：`S4-before-disable.json`，`S4-disable-call.json`，`S4-after-disable-samples.json`，`ER-samples.json`
