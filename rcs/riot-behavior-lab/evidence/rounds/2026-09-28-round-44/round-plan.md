# Round 44（2026-09-28）：HELD 订单叠加软件急停、解除之后

## 1. 研究目标

- 服务对象：`8005-agv-control-server#335`（在途门锁未证明锁闭时先 `OrderHold`、按不住再急停；门锁恢复后自动解除急停，用户 2026-09-28 选方案 A）。
- 本轮要回答：
  1. 订单已被 `CMD_ORDER_HELD` 打成 `HELD(7)`、车已停稳时，再 `triggerEmergency` → `cancelEmergency`，订单是否仍是 `7`、车是否仍保持静止（至少 60 秒观察窗口）。
  2. 解除之后 `CMD_ORDER_CONTINUE_FROM_HELD` 是否仍然有效（回到 `EXECUTING(3)` 并跑到 `SUCCESS(5)`）。
  3. （第二格，用户确认后才做）急停锁住期间发 `CMD_ORDER_CONTINUE_FROM_HELD`，是否被接受；接受的话，解除急停后车会不会自己走。
- 已有知识为什么不够：`BC-ORDER-006` 只覆盖「HELD ↔ CONTINUE_FROM_HELD」，没有急停；`BC-ORDER-015` / Round31 只覆盖「EXECUTING 时急停」，那种情况下单一直是 `EXECUTING`，**`cancelEmergency` 之后车会自己接着走**。HELD 叠加急停这个组合没有任何轮次测过。
- 明确不回答：硬件急停（`CAN_NOT_RECOVER`）；HANG；多段单；车载端与服务端行为（本轮不起任何 ControlServer 实例）。

## 2. 环境元数据

- RIoT：8005 生产 RIoT `http://172.19.206.222:8888`（与 Round 43 同一套；与 Round 1～42 的跨项目测试环境不是同一套）。平台版本 `UNKNOWN`。
- 凭据：控制端环境变量 `CONTROL_SERVER_RIOT_CALL_API_KEY`，不落任何文件。
- 路由：执行脚本每次启动都用 `Find-NetRoute` 核对，经 Clash 虚拟网卡就拒绝发请求。
- 地图：只用 `mapId=26`（`老厂前线new_wk`）。
- 测试车：`agv02` 或 `agv03` 之一（见 §4），身份按 `remote-ops/fleet.md` 的 `deviceKey` 取；脚本对 `agv01` 的 `deviceKey` 硬拒绝。
- 执行器：本目录 `run-round44.ps1`，沿用 Round 19 / 36 的做法（直接 HTTP，急停 body 用 `BC-VEH-005` 的 UI 形状），每次调用一个阶段。

## 3. 范围与授权

- 用户 2026-09-28 在现场，原话「RIoT 做吧」，经 Coordinator 8 转达。这是**同意做这项实测**，不是放行每一步：本计划经调度转用户确认后才发第一条会让车动的命令。
- 已批准写操作（确认后）：对测试车建单（单段 `move`，地图 26）、`CMD_ORDER_HELD`、`CMD_ORDER_CONTINUE_FROM_HELD`、`CMD_ORDER_CANCEL`（只对本轮建的单）、`triggerEmergency`、`cancelEmergency`（只对测试车）。
- 明确不做：对 `agv01` 或任何其它车的任何写操作；任何批量、全局、地图编辑接口；取消不是本轮建的订单；硬件急停。
- 工作区规则：`Ask first` 第 1 类（会动车、会发急停），逐次授权，现场有人盯、物理急停可按，车空载。

## 4. 前置状态（执行前由 `baseline` 阶段自动核对，不满足即拒绝继续）

- 测试车 `currentMap=老厂前线new_wk`、`locationState=LOCATION_STATE_RUNNING`、在某个站点上（`currentStation≠0`）、`emergencyState=OK`、`breakSwitchState=MOVABLE`、在线、`procState=IDLE`、不在执行订单、车速 0。
- 测试车名下没有任何未完成订单（按 `appointVehicleKey` 或 `executeVehicleKey` 过滤 `1/3/7/9`），`existedInGroup` 为空（不会被车组派单抢到）。
- 不用 `hmi#170` 正在做 IO 只读验证的那一台。
- 现场：车空载，有人在车旁，物理急停可按。

2026-09-28 15:34 的只读基线（见 `runs/`，`pre-baseline`）：两台车都**不满足**——都停在路网外，`agv02` 当时报 25 号图、置信度 45%，`agv03` 未定位；15:39 复查时 `agv02` 已切到 26 号图但 `locationState=ERROR`，`agv03` 仍在 25 号图。已报调度请现场处理。

## 5. 执行顺序（运行 A：主格）

每一步是脚本的一个阶段，`MATCH` 才进下一步；`MISMATCH` 就停，报告，不临场加步骤。

| # | 阶段 | 发什么 | 预期（事先写定的判据） | 回读 |
| --- | --- | --- | --- | --- |
| 0 | `baseline` | 只读 | §4 全部满足 | 车辆详情、车辆卡片、未完成订单 |
| 1 | `routecheck` | `getRouteCostsBy`（只读规划查询） | 起点→终点、终点→起点都可达，代价 10～40 米 | 代价与 message |
| 2 | `create` | `byDefaultMissions`，单段 `move` 到终点 D，`appointVehicleKey`=测试车 | `code=0`；90 秒内 `orderState=3`、`executeVehicleKey`=测试车，且真的在走（车速≠0 或坐标累计移动 ≥300 mm） | 约每 0.8 秒一次 |
| 3 | `held` | `CMD_ORDER_HELD` | `code=0`；15 秒内 `orderState=7`，车静止并持续 5 秒（参考 `BC-ORDER-006`：`USER_FORCE_IDLE`、`MT_PAUSED`） | 同上 |
| 4 | `trigger` | `triggerEmergency` | `code=0`；15 秒内 `emergencyState=CAN_RECOVER`；锁住后再看 10 秒，`orderState` 仍是 `7`，车静止 | 同上 |
| 5 | `release` | `cancelEmergency` | `code=0`；15 秒内 `emergencyState=OK`；期间 `orderState` 保持 `7`，车静止 | 同上 |
| 6 | `observe` | 不发命令 | 60 秒内每秒一次：`orderState` 始终 `7`、车速始终 0、坐标不变、`emergencyState` 始终 `OK` | 每秒一次 |
| 7 | `continue` | `CMD_ORDER_CONTINUE_FROM_HELD` | `code=0`；20 秒内 `orderState=3` 且真的在走 | 约每 0.8 秒 |
| 8 | `run-to-end` | 不发命令 | 240 秒内 `orderState=5`、`currentStation=D` | 约每 1.2 秒 |
| 9 | `final` | 只读 | 名下无未完成订单，`emergencyState=OK`，`IDLE`，静止 | 同上 |

**第 6 步的预期是「保持 HELD、不动」，这是本轮真正要验证的假设，不是已知事实。**Round31 里 EXECUTING 的单在解除急停后会自己走；HELD 的单会不会也这样，正是要回答的问题。所以第 5、6 步一旦看到车在动或订单离开 `7`，脚本**立即再发 `triggerEmergency`** 并停下（见 §7）。那样的结果本身就是答案（「HELD 在急停解除后不可靠」），不会接着往下做。

## 6. 运行 B：第二格（需用户单独确认；主格全部 MATCH 才做）

从 D 出发、终点回到起点 S（同一条路反向），这样做完车回到起点。

| # | 阶段 | 发什么 | 预期 |
| --- | --- | --- | --- |
| B0～B4 | `baseline`、`create`、`held`、`trigger` | 同运行 A 的 0、2、3、4 | 同左 |
| B5 | `continue-in-emergency` | 急停锁住期间发 `CMD_ORDER_CONTINUE_FROM_HELD` | **没有事先的预期**，任何返回码都记为发现；只要求 20 秒内车不动、仍 `CAN_RECOVER` |
| B6 | `release` | `cancelEmergency` | 分两种：B5 被拒（订单仍 `7`）→ 按运行 A 的第 5、6 步判，车不该动；B5 被接受（订单变成 `3`）→ 解除后车**可能**会自己朝终点 S 走——这就是运行 A 第 7 步本来就会做的那段行驶，同一条已确认的路，所以允许它走完，改按第 8 步判 `SUCCESS` |
| B7 | `continue`（仅当 B6 后仍是 `7`） | `CMD_ORDER_CONTINUE_FROM_HELD` | 同运行 A 第 7 步 |
| B8～B9 | `run-to-end`、`final` | — | 车回到 S，`SUCCESS`，无未完成订单 |

B6 的两种分支在确认时一并确认：**如果用户不同意「解除后车可能自己走完」这一点，就不做运行 B。**

## 7. 中止条件

任一出现即停，不重试、不临场加步骤，报调度：

1. **车在不该动的时候动了**（第 3 步 5 秒稳定之后、第 4～6 步、B4～B5，以及 B5 被拒时的 B6）：判据是任一车速 >0.005，或两次采样间坐标移动 >50 mm，或第 5、6 步 `orderState` 离开 `7`。→ 脚本立即 `triggerEmergency`，回查到 `CAN_RECOVER` 后停下；同时请现场按物理急停。订单保持原样，等人工决定。
2. 订单的 `executeVehicleKey` 变成测试车以外的车；或测试车名下出现不是本轮建的订单。→ 若车在动先按 1 处理；不动则停下报告，不碰别人的单。
3. 任一命令返回非 `0`，或回读在时限内没有达到预期。车静止时直接停下报告；车在动时先按 1 处理。
4. `emergencyState=CAN_NOT_RECOVER`，或 `cancelEmergency` 15 秒内读不到 `OK`：车是停着的，停下报告，转现场与 RIoT 人员，不反复调用。
5. 车辆卡片 `currentMap` 不再是 `老厂前线new_wk`、掉线、`locationState` 离开 `LOCATION_STATE_RUNNING`，或 RIoT 连续请求失败。
6. 现场任何人要求停，或物理急停被按下。

## 8. 急停之后怎么释放

- 本轮不起任何 v2 ControlServer 实例（调度确认 v2 实例没在跑）；factory01 上的 MVP 服务只管 `agv01`，不读不碰。所以释放由本实验自己做：`cancelEmergency`，并回查到 `emergencyState=OK` 才算解开（`BC-VEH-005`，2026-09-15 实测约 3.6 秒）。
- 测试车名下没有别的在途单（第 0 步核对；有就不开始）。如果中止时本轮的单还在 `7` 或 `3`：车静止、急停锁着的情况下先 `CMD_ORDER_CANCEL`（`BC-ORDER-006`：HELD 可直接取消到 `CANCELLED(2)`），回读到 `2` 后，**再**问调度要不要 `cancelEmergency`——先取消订单再解急停，解开时车上没有可执行的单，不会走。

## 9. 收尾

- 正常路径：运行 A 车停在 D，运行 B 车回到 S；两单都 `SUCCESS`，无需取消。
- 只做运行 A：车停在 D（一个站点上），`final` 核对无未完成订单、`OK`、`IDLE`。车要不要开回原位由现场决定，本轮不再发单。
- 异常路径：按 §8 取消本轮的单、解除急停，`final` 核对。

## 10. 状态

`等待人工`：测试车尚未在 26 号图上定位（2026-09-28 15:39）。
