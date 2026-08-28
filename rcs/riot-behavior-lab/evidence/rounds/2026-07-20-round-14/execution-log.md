# Round 14 执行日志（2026-07-20）

## 环境

- baseUrl: `http://172.10.1.72:8888`
- 测试车: `新基测试300c协作1` / `BROKERX-aee2f93d717546cf9510c98c854fe83e`
- mapId=29；鉴权: callApiKey
- 脚本: `run-round14.ps1`

## 摘要结论

1. **按车拉「当前积压」不能只靠 `executeVehicleKey`**：QUEUEING 单的 `executeVehicleKey` 为 `"--"`，会被该过滤漏掉。
2. **未文档化的 `appointVehicleKey` 查询参数不可靠**：传入后仍返回其它车的非终态单（本轮混入 `orderState=9` 磨划晶圆AGV2），视为**被忽略**。
3. **可用做法**：`filterByState=1,3,7,9` 拉非终态，再按 `appointVehicleKey == 本车 OR executeVehicleKey == 本车` 客户端过滤。
4. **清队**：对 QUEUEING(1) / HELD(7) 发 `CMD_ORDER_CANCEL` 成功；清完后车回 `IDLE`，新单可立即 `EXECUTING`。

## E0 基线

- 初始 `procState=INNER_FORCE_IDLE`，`executeVehicleKey`+非终态筛到 1 条遗留 → 已 cleanup。
- 证据: `runs/E0-*.json`

## S1 过滤器探针（空闲时）

| 查询 | 结果 |
|---|---|
| `executeVehicleKey` 无状态 | total=20（含历史终态） |
| `executeVehicleKey` + states 1/3/7 | total=0 |
| `appointVehicleKey`（undoc）+ states | total=0（空闲时碰巧干净） |
| `filterByState=1` 全局 | total=0 |
| `executeVehicleName` + states | total=0 |

证据: `runs/S1-filter-probes.json`

## S2 制造积压

| 单 | upperId 前缀 | 观测 |
|---|---|---|
| A | R14-A-exec | `orderState=3`，`execute`=本车 |
| B | R14-B-queue | `orderState=1`，`execute=--` |
| C | R14-C-queue | `orderState=1`，`execute=--` |

积压时列表对照：

| 查询 | total | 是否含 B/C 队列 |
|---|---|---|
| `executeVehicleKey` + 1/3/7/9 | **1**（仅 A） | **否** |
| `appointVehicleKey` + 1/3/7/9 | 4（含 A/B/C + **其它车 HANG**） | 含 B/C，但**串车** |
| `filterByState=1` 全局 + 客户端按本车 appoint/execute | 2 | **是** |

随后对 A `CMD_ORDER_HELD` → `orderState=7`，`procState=USER_FORCE_IDLE`，`MT_PAUSED`。  
`executeVehicleKey`+states 能看到 HELD 的 A（仍有 execute key），**仍看不到** B/C。

证据: `runs/S2-*.json`

## S3 清队 + 新单

- Cancel B(1)、C(1)、A(7) 均 `code=0` → 均 `orderState=2`
- 车侧回到 `IDLE`；非终态列表 total=0
- 新建 N：进入 `orderState=3 EXECUTING`（验证清队后新单可生效）
- 再 cancel N 收尾 → `IDLE`，非终态 0

证据: `runs/S3-*.json`，`runs/S4-*.json`

## 对 MES/SDK 的直接建议

清本车积压推荐流程：

1. `GET /api/order/v1/orderRecord?pageNum=1&pageSize=100&filterByState=1&filterByState=3&filterByState=7&filterByState=9`
2. 客户端保留 `appointVehicleKey==本车 || executeVehicleKey==本车`
3. 对 `orderState∈{1,7,9}`（按需含 `3`）逐单 `CMD_ORDER_CANCEL`
4. 等到 `getVehicleInfo`：`IDLE` 且非 `processingOrder`
5. 再发新单

**禁止**只依赖 `executeVehicleKey=` 本车去“看见队列”；**禁止**依赖 undoc 的 `appointVehicleKey` 查询参数。
