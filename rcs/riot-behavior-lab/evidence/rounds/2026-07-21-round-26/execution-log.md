# Round 26 执行日志 — 交管等待只读

## 状态

**完成**：交管等待与解除后对比均已采到。

## 交管中（解除前）

| 来源 | 现象 |
|------|------|
| getVehicleInfo | `movementState=MT_WAIT_FOR_CHECKPOINT`，`PROCESSING_ORDER`，`speed=0` |
| appliedResource | 本车有申请中的 node/edge 资源 |
| lockedResource | **无**本车（未占用，在等） |
| checkFailDetail | `type=edgeGroup`，占用方 `BROKERX-f2b50ed…`（华士厂内AGV） |

## 解除后（2026-07-21 16:49:37）

| 来源 | 现象 |
|------|------|
| getVehicleInfo | `movementState=MT_RUNNING`，`speed≈0.2`，仍 `PROCESSING_ORDER` |
| appliedResource | **无**本车 |
| resourceDetail | `applied*` 空；`lockedEdge/lockedNode` 有值（行驶中正常占路权） |
| checkFailDetail | `result=null` |

## MES 判据（结论）

- **交管等待中**：`movementState == MT_WAIT_FOR_CHECKPOINT`（辅：`appliedResource` 含本车）
- **已解除/在跑**：`MT_RUNNING`（或其它非 WAIT）；本车从 `appliedResource` 消失，转为持有 `locked*` 资源属正常
- 原因可读：`checkFailDetail/{key}`（等待时）；解除后可为空

## 证据

等待：`X-vehicle-traffic-hint.json` / `X-applied-this-vehicle.json` / `X-checkFailDetail.json`  
解除：`R-release-compare.json` / `R-getVehicleInfo.json` / `R-appliedResource.json`
