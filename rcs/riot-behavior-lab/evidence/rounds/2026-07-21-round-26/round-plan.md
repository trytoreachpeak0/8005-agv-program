# Round 26（2026-07-21）— 交管等待状态只读探测

## 目的

在车已处于交管等待时，确认 MES 能否用 API 判断「因交管而等别的车」。

## 范围

- 仅只读；车：`BROKERX-52501bcbe60f4723bc815f24fc763c1e`（用户当场提供交管窗口）
- 不调用 `DELETE /traffic/` 或按车清占用

## 结论（可检测）

1. **车态主信号（推荐）**  
   `GET .../getVehicleInfo/{key}` → `vehicle.movementState = MT_WAIT_FOR_CHECKPOINT`  
   同时：`procState=PROCESSING_ORDER`，`speed=0`，常 `noStation/noNode=true`

2. **交管「正在申请/等待」资源**  
   `GET /api/task/v1/traffic/appliedResource` → `result[<deviceKey>]` 有条目（本轮：node/edge 资源，如 `node-map-11.4`、`edge-map-11.36`）  
   同车在 `lockedResource` 中**无**条目（等别人，自己尚未锁到）

3. **最近一次交管申请失败详情（原因可读）**  
   `GET /api/task/v1/traffic/checkFailDetail/{deviceKey}`  
   - `type=edgeGroup`  
   - `lockedVehicleIds` = 占用方车 key  
   - `detail` 文案含被占用的资源组与对方车

4. **汇总视图**  
   `allTrafficResourceDetail`：该车 `appliedEdge/appliedNode` 非空，`locked*` 为空

## MES 建议判据

- **是否交管等待**：`movementState == MT_WAIT_FOR_CHECKPOINT`（订单执行中）  
  或 `appliedResource.result` 含本车 key  
- **等谁/为何**：读 `checkFailDetail/{key}` 的 `lockedVehicleIds` / `detail`  
- 不必理解交管算法；解除后预期 `movementState` 离开 WAIT，且 `appliedResource` 中本车条目消失

## 证据

`runs/X-vehicle-traffic-hint.json`、`X-applied-this-vehicle.json`、`X-checkFailDetail.json`、`X-resourceDetail-this-vehicle.json`
