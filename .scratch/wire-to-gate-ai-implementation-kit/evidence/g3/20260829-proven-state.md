# 2026-08-29 现场联调已证明的状态

本文只记录**已有证据支撑**的结论，不含推测或计划。剩余工作与阻断另见
[`20260829-remaining-work.md`](20260829-remaining-work.md)。

## 绑定身份

| 组件 | 版本 |
| --- | --- |
| ControlServer | `ControlServer_MVP@8caf7465b1096903d1f84d6d4788472b0c3c665a` |
| OnboardHmi | `OnboardHmi_MVP@84b7f3f66ff2f867b18121760f38e26e0bbd6fa5`（王昆实现，配置未做任何覆盖）|
| slots-simulator | `main@fb5f7c593742bf98bc3957b8729a38aad5321f28` |
| 协议 | `protocol-v0.1.1@1531489e42e328f28bfe0c51ed3f8c56e5ce0279` |
| MesIngest | 本机 `http://127.0.0.1:5088`，contract `2026.08.new-mes-ingest.v2.4` |
| RIoT | `http://172.19.206.222:8888` |

车辆 `老厂前线新多仓位1` = `BROKERX-0c20ff0600d644869a6a80c186065d85`，地图 25
（`老厂前线new`），关卡站点 210。四项身份均经 RIoT 只读回读与已部署配置逐字核对一致。

## 一、真实建单链路成立（首次真实移动）

`order-2093389168079142912`（数值 id `1676913`），`upperId`
`W2G-94993971b3624edf81bc712d160e444a-PICKUP-1`，对应 SUBLOT `Q26081298-1|WIRE_TO_GATE`。

- RIoT 只读对账 `orderState = 5`（`1 QUEUEING → 3 EXECUTING → 5 SUCCESS`），
  01:24:06 建单、01:26:22 完成
- 车辆 `stationNo` 由 **210 → 21**（`N2-5_N3-5`），真实完成取货段移动
- 审计链恰为 `PRE(UNKNOWN/精确 absent) → ARMED → CREATE_REQUEST → CREATE_RESPONSE(ACCEPTED)
  → POST(UNKNOWN) → POST(TERMINAL)`，无重复
- `CreateAttemptCount = 1`

**第一条 PRE 即精确 absent-at-observation，全程未使用任何一次性 permit**——BC-ORDER-004
upperId 幂等建单链路的现场有效性至此成立。

证据：`8005-agv-control-server` `evidence/g3/20260829-authorized-single-real-create/`

## 二、at-most-once 与幂等在现场成立

后续一次运行中，全新数据库按决定性 `upperId` 重建同一 intent，对账**命中首轮遗留的同一订单
并直接确认**：

- `Status = CONFIRMED`，`OrderId = order-2093389168079142912`
- `CreateAttemptCount = 0` —— **未建第二单**
- 该次运行对 RIoT 零 mutation，车辆未移动

证据：`8005-agv-control-server` `evidence/g3/20260829-placeholder-fix-confirms-leg/`

## 三、建单开关（fail-closed 操作联锁）在现场成立

开关关闭时，一条真实 Demand 完成受理并推进到 `AwaitingPickupArrival`，稳定停在
`BlockReasonCode = PICKUP_CreateDispatchDisabled`，且：

| 字段 | 值 |
| --- | --- |
| `Status` | `PENDING_RECONCILIATION` |
| `CreateAttemptCount` / `CreateAttemptId` | 0 / null |
| `DispatchAuditVersion` / `DispatchAuditSequence` | 1 / **0** |
| `RiotDispatchAuditEvents` 总行数 | **0** |

审计链一行未写，intent 保留完整建单资格——「关闭态演练不消耗资格」由单元测试升格为真机证据。

证据：`8005-agv-control-server` `evidence/g3/20260829-intake-gate-fix-verification/`

## 四、受理链路在出厂车载配置下成立

未对车载配置做任何覆盖时，受理数由修复前的 0 变为 1，另有 6 条 `ELIGIBLE`；运行 2 分 35 秒
后仍在正常推进，远超修复前 30 秒的受理窗口。

WIRE_TO_GATE 判定分布（其中 `OUT_OF_SCOPE_AREA` 为 `C*`／`D*`／`Q*` 区，本就不在地图 25 上，
判定正确）：

| ReasonCode | 典型条数 |
| --- | --- |
| `OUT_OF_SCOPE_AREA` | 8～10 |
| `ELIGIBLE` | 4～6 |
| `ACCEPTED` | 1 |
| `PACKAGE_CAPACITY_NOT_UNIQUE` | 1 |
| `AREA_STATION_NOT_FOUND` | 1 |

## 五、五步恢复与到站判定在真实双端成立

- 会话在真实双端下达到 `Ready / READY`、`DepartureSafe=1`、`/health/ready` 200
  （此前各次均 fail-close 在 `DEPARTURE_SAFETY_NOT_READY`）
- 车辆停在目标站后，`IsTrustedArrivalAsync` **判定到站成功**并触发
  `PublishPickupStateAsync`，发出 `VehicleBusinessStateSnapshot`／
  `CurrentStopWorklistSnapshot`／`UpcomingStopPlanSnapshot` 三条快照

## 六、安全门禁按设计 fail-closed

一次绑定运行在车辆 `movementState=MT_NA`（手动开回、无已完成 RIoT 移动任务）时，于任何
mutation 之前安全中止：零审计行、零订单、车辆未移动、端口回收。Round-41 谓词中仅
`RIOT_MOVEMENT_NOT_FINISHED` 一条不满足，其余全部通过。

证据：`8005-agv-control-server` `evidence/g3/20260829-second-create-safe-abort/`

## 本日落地的产品修复

| 修复 | commit | 性质 |
| --- | --- | --- |
| 建单 dispatch 默认关闭开关 | `1a0158c` | 恢复「误开 runtime 不会建单」联锁 |
| 受理门禁两条（`supportsBatchUnlock`、快照新鲜度→会话活性）| `74ddda2` / `9a42582` | 解除现场完全无法受理 |
| `"--"` 占位符与 `orderState 5 → 已确认` | `addc2fa` | 解除 intent 永不可确认 |
| `ProtocolProblem` 不再拆连接 | `bf22a48` | 保留对端诊断，止住连接被杀 |
| 快照 `observedAt` 取信封冻结 `sentAt` | `8caf746` | payload 不再嵌漂移时钟 |

每一处均：Release 构建 0 warning／0 error、`dotnet format` 通过、完整测试全绿 0 skip、
W2G-IS-00～07 八片 G2 全 PASS 并绑定精确 commit、可回滚本机部署 PASS。最终测试数 220/220。

## 明确未证明的事项

正式 W2G-IS-00～07 的 G3 与 RC 仍为 `INCONCLUSIVE`。取货到站之后的所有阶段（装货、安全检查、
`TO_GATE` 移动、关卡批量卸货、原子完成）均未走通，原因见剩余工作文档。
