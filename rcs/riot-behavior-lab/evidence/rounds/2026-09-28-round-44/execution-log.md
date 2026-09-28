# Round 44 执行日志（2026-09-28）

## 记录规则

- 未执行步骤保持未执行，不提前填写结果。
- 时间使用带时区的 ISO 8601 格式（`+08:00`）。
- 原始请求与响应全文在 `runs/http.ndjson`（一行一次调用，凭据写作 `<redacted>`）；状态采样在 `runs/samples.ndjson`（一行一次采样，字段见 `runner/README.md` 的统一采样记录）。两个文件都按 `phase` 字段区分阶段。
- 人工动作与现场口头报告按收到的时间写进同一时间轴，注明经谁转达。

## 环境

- RIoT：`http://172.19.206.222:8888`，凭据取自 `CONTROL_SERVER_RIOT_CALL_API_KEY`。
- 路由：每次脚本启动都核对，全程 `InterfaceAlias=Wi-Fi`，不经 Clash。
- 执行者：Claude 实现会话（经 Coordinator 8 与现场用户沟通）。

## 授权记录

| 时间 | 来源 | 内容 |
| --- | --- | --- |
| 2026-09-28 下午 | 用户（人在现场）经 Coordinator 8 转达 | 原话「RIoT 做吧」：同意做这项实测，不是放行每一步 |
| 2026-09-28 约 15:4x | 调度 | 车定为 `agv03`；`agv02` 归 `hmi#170`，不碰 |
| 2026-09-28 约 15:5x | 用户经调度逐项确认 | 运行 A 确认，含中止条件 1 的自动再急停；运行 B 做，并同意「锁住期间 CONTINUE 被接受就让它沿原路走完」（前提是运行 A 全部符合预期）；每个会让车动的命令前先要一句「就位」 |
| 2026-09-28 约 16:0x | 用户经调度逐项确认 | 路段 N19 通道：A 走 101→99，B 走 99→97；通道现场没人、没障碍；`speed=0.3` 同意（建单被拒就停，实际更快不中止、记为发现）；HELD 由脚本在车确实走起来时自动发 |
| 2026-09-28 稍后 | 用户经调度 | **改选选段一，N19 作废**：S=`T05-06`（151），D=`T06-02_T07-02_T07-03`（155），A 走 S→D，B 走 D→S；`speed=0.3` 照旧。用户手动把车挪到 151 定位并确认两条通道没人没车；拿到确认、S↔D 路径代价核对通过、调度回「用户已确认，可以开始」并转来第一个「就位」之后才建单 |

## 时间轴

### 只读准备（不在 `runs/` 的部分）

15:34 前后在 scratchpad 做过一次只读探测（车辆详情、全车列表、地图列表、25/26 号图站点与边表、未完成订单、路径代价），用来选车选段；结论已写进 `round-plan.md` §4，原始文件未入库。

### `pre-baseline`（`runs/` 中 `phase=pre-baseline`）

| 时间 | 车 | 结果 |
| --- | --- | --- |
| 15:38:59 / 15:39:01 | agv02 / agv03 | 脚本首版有缺陷（`$x?.y` 被 PowerShell 当成变量名 `x?`），读数全空，判 `MISMATCH`。修脚本时这两次的 `runs/` 输出被整个删除后重跑，**这两行不在 `runs/` 里**；它们不含车的状态，只是 5 个只读 GET |
| 15:39:17 | agv02 | `MISMATCH`：`locationState=ERROR`，不在站上（此时已切到 26 号图） |
| 15:39:20 | agv03 | `MISMATCH`：`currentMap=老厂前线new`（25 号图），不在站上 |
| 15:41:21 | agv02 | `MISMATCH`：不在站上，且在移动（现场操作中） |
| 15:41:22 | agv03 | `MISMATCH`：26 号图、已定位，但不在站上 |
| 15:50:29 | agv03 | `MATCH`：26 号图、已定位、站 212（充电准备点1）、`OK`、`IDLE`、名下无单。该站不作起点，见 `round-plan.md` §4.2 |

`-Ready` 闸门自检（15:5x，`-Run gatecheck`）：`create` 不带 `-Ready` → `REFUSED`，退出码 4，未发出任何请求。

### 运行 A

#### A0 `baseline`（16:06:15，`phase=A-baseline`）— `MATCH`

agv03：`currentMap=老厂前线new_wk`，`LOCATION_STATE_RUNNING`（置信度 63%），`currentStation=151`（`T05-06`），坐标 `(-63559, -35704)`，`emergencyState=OK`，`breakSwitchState=MOVABLE`，`controlState=CONTROL_STATE_OK`，`status=1`，`procState=IDLE`，`processingOrder=false`，`movementState=MT_FINISHED`，两个接口车速均 `0.0`，电量 92%，`loadState=0`，`existedInGroup=[]`，名下未完成订单 0。

#### A1 `routecheck`（16:06:18，`phase=A-routecheck`）— 超出事先阈值，停

请求 `POST /api/task/v1/route/getRouteCostsBy` `{"mapId":26,"stationId":155,"deviceKeys":["BROKERX-7daca4ee…1127"]}`，返回 `costs=32270`、`message=ok`。

事先写的判据是「与自算 31021 相差 ≤1000」，实查多 **1249 mm**，超出，按计划停下报调度，未建单。

- 读到的：自算值是路网边表上 151→155 最短路 14 条边的 `cost` 之和，等于这些边的欧氏长度之和（31021 mm）。
- 推的：这不是另一条路线——去掉最短路上任一条边后，151→155 的最短路是 84795 mm，与 32270 相去甚远。差值更像是 RIoT 的代价比纯边长多计了一部分（这条路有两处 90° 拐角）。`BC-MAP-003` 里「`Edge.cost` 与 `getRouteCostsBy` 同量纲」原本就标为推断、没在同一对起终点上直接对比过；本次是第一次对比，差 4%。
- 阈值是本轮自定的，用来发现「RIoT 规划了另一条路」；是否在这个解释下继续，交用户决定。

### 运行 B

未执行。

## 本轮结论

未执行。
