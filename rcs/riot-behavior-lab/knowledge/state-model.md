# 可观测状态模型

## 建模原则

RIoT 暴露的是多个不同层次的状态面，目前没有证据表明它们可以合并成一个状态字段：

- 订单层：`orderState`
- mission 层：`missionState`
- 调度进程层：`procState`
- 车辆聚合层：`Vehicle.state`
- 设备物模型层：`sysState`、`movementState` 等
- 本项目业务层：本地任务和流程状态

因此状态模型以“同一时间轴上的并行观测”表示，不提前建立一对一映射。

## 静态已知状态

下面内容来自 Swagger、TSL 或生成代码，证据等级为 `SCHEMA`：

- `orderState` 声明了 QUEUEING、CANCELLED、EXECUTING、FAILED、SUCCESS、DELETED、PAUSED、SUSPENDED、HANG 等值。
- **FAILED**：schema 有、现场极少见；已知多与系统/地图异常相关（Q-024）。常规业务以 SUCCESS / CANCELLED / QUEUEING 滞留为主，不要为测 FAILED 去破坏现场地图。
- `missionState` 声明了未开始、执行中、完成、失败、取消等值。
- `procState` 声明了 AWAITING_ORDER、IDLE、PROCESSING_ORDER、IN_CANCEL、USER_FORCE_IDLE 等值。
- `Vehicle.state` 声明了 IDLE、EXECUTING、CHARGING、ERROR、PAUSE、UNKNOWN 等值。

这些列表只证明“契约中存在这些值”，不证明现场一定出现，也不证明转移条件。

## 当前已验证状态转移

### 位置归属：在站 ↔ 离站（Round 6，`OBSERVED`）

同一测试车、同一地图 `api测试` 上观测到：

| 场景 | `currentStation` | `stationNo` | `noStation` | `mapName` | 坐标 |
|---|---|---|---|---|---|
| 在站 | 1（站点1） | 1 | false | api测试 | 有 |
| 离站 | **0** | **0** | **true** | api测试（仍在） | 仍有 |

语义（BC-STATE-002）：站号 **0** = 当前未归属站点；不是丢图、不是 API 失败、也不是名叫“站点0”的站。

证据：[`../evidence/rounds/2026-07-20-round-6/runs/B2-off-station-snapshot.json`](../evidence/rounds/2026-07-20-round-6/runs/B2-off-station-snapshot.json)

### 成功移动单并行轨迹（Round 8，`OBSERVED`）

map29 站1→站2（站距拉长后，全程约 **52s**，57 个密采样点）：

```text
t≈0s    发单前：proc=IDLE, station=1, move=MT_FINISHED
t≈1s    order=1 QUEUEING, mission=0, proc=IDLE, station=1
t≈6s    order=3 EXECUTING, mission=1, proc=PROCESSING_ORDER, move=MT_RUNNING, station=0
        （此后 ~45s 持续 EXECUTING / RUNNING，坐标 y 从约 -477 移到约 -2440）
t≈52s   order=3 仍在, mission=1, proc=AWAITING_ORDER, move=MT_FINISHED, station=2  ← 物理到站
t≈53s   order=5 SUCCESS, mission=2, proc=IDLE, station=2                         ← 订单完成
```

关键观测：

1. **物理到站早于订单 SUCCESS**：先出现 `station=目的站` + `MT_FINISHED` + `AWAITING_ORDER`，约 1s 后才 `orderState=5`。
2. **`progress` 不可当路程进度**：一进入 EXECUTING 就变成 100，移动全程不变。
3. **`missionState`**：0（排队/未开始）→ 1（执行中）→ 2（完成）；完成时 `resultCode=900`。
4. **绑车**：`executeVehicleKey` 全程等于测试车。

证据：[`../evidence/rounds/2026-07-20-round-8/runs/E2-dense-samples.json`](../evidence/rounds/2026-07-20-round-8/runs/E2-dense-samples.json)

### 取消轨迹（Round 9，`OBSERVED`）

执行中纯 `move`：

```text
order=3 + PROCESSING_ORDER + MT_RUNNING
  --CMD_ORDER_CANCEL-->
order=2 CANCELLED + missionState=4 + proc=IDLE + MT_FINISHED
（站号可能为 0 / 离站）
  --再派-->
可再次 1→3→5 SUCCESS
```

`interrupt`（pause=true/false）在同样前置下被拒绝（`100036`），不产生上述转移。

证据：[`../evidence/rounds/2026-07-20-round-9/`](../evidence/rounds/2026-07-20-round-9/)

### HELD / CONTINUE 轨迹（Round 10，`OBSERVED`）

```text
order=3 + PROCESSING_ORDER + MT_RUNNING
  --CMD_ORDER_HELD-->
order=7 PAUSED + USER_FORCE_IDLE + MT_PAUSED（站号可为 0）
  --CMD_ORDER_CONTINUE_FROM_HELD-->
order=3 + PROCESSING_ORDER + MT_RUNNING
  -->
order=5 SUCCESS + IDLE
```

证据：[`../evidence/rounds/2026-07-20-round-10/`](../evidence/rounds/2026-07-20-round-10/)

### 幂等（Round 10）

相同 `upperId` 在 SUCCESS / EXECUTING 下再次建单 → 业务拒绝 `0610008`，状态面不变。

### 多段 move（Round 11，`OBSERVED`）

```text
order=1
→ order=3 + executingIndex=0 + move RUNNING
→ order=3 + executingIndex=1 + move RUNNING
→ order=5 SUCCESS + IDLE
```

### act 等待 + interrupt（Round 11）

进入 `missionType=act`（`actionId=129`）后 `interrupt` 仍拒绝 `100036`，订单可自然跑完 SUCCESS。

| 业务含义 | 当前可用信号（Round 8） | 勿单独依赖 |
|---|---|---|
| 已接单/在执行 | `orderState=3` 且 `procState=PROCESSING_ORDER` | 仅 `progress` |
| 移动中 | `movementState=MT_RUNNING` 且 `currentStation=0` | `orderState=3`  alone（到站瞬间仍可能是 3） |
| 物理到站 | `currentStation==destination` 且 `MT_FINISHED` | 仅 `orderState=5`（略滞后） |
| 订单完成 | `orderState=5` | 仅车侧 IDLE（可能更早出现 AWAITING_ORDER） |
| 可再派 | `orderState=5` 终态后 + `procState=IDLE` + 非 `processingOrder` | 仅 `AWAITING_ORDER`（到站瞬间会出现，订单未必 SUCCESS） |
