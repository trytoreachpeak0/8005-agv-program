# 2026-08-29 现场联调已证明的状态

本文只记录**已有证据支撑**的结论，不含推测或计划。剩余工作与阻断另见
[`20260829-remaining-work.md`](20260829-remaining-work.md)。

## 绑定身份

| 组件 | 版本 |
| --- | --- |
| ControlServer | `ControlServer_MVP@3d8b00c7558ae700358f1f995a5ac75d12a3250c`（证据提交 `8b6b0ad`；现场已验证到 `f48e616`，`3d8b00c` 尚未现场复跑）|
| OnboardHmi | `OnboardHmi_MVP@304e6ad9952a41d5c0d50c0c4e79bab5c8804bd6`（王昆实现，配置未做任何覆盖）|
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

## 七、到站之后第一段成立（2026-08-29 晚新增）

同一台车、同一条 Demand 的复跑中，旅程**首次推进到 `AwaitingSublot`**：

| 指标 | 修复前 | 本次 |
| --- | --- | --- |
| `SessionHello`（会话建立次数）| 22 | **1** |
| `ProtocolContentConflictException` | 51 | **0** |
| 车载 `ProtocolProblem` | 20 | **0** |
| 三条旅程快照被确认 | 0 / 3 | **3 / 3** |
| `SublotEntryRequested` | 从未发出 | **已发出** |
| `Stage` | `AwaitingPickupArrival` | **`AwaitingSublot`** |

订单 `order-2093605636779671552` `CONFIRMED`，车辆由 210 移动到 21（`N2-5_N3-5`）后
`MT_FINISHED`、空载。另以生产代码对生产代码完成跨仓互操作验证：真实 `OnboardJourneyPublisher`
产出的 wire 被真实 `WireToGateProtocolSerializer` 逐字节复现，三个阶段 ACK 全部接受。

证据：`8005-agv-control-server` `evidence/g3/20260829-arrival-to-sublot-field-verify/`

## 八、装货到关卡到站走通（2026-08-29 深夜新增）

同一台车、同一条 Demand 的六次绑定运行把旅程从 `AwaitingSublot` 推进到 `AwaitingUnloadResult`，
每次修复恰好推进一段：

| 运行 | 服务端 | 到达 `Stage` | 阻断 |
| --- | --- | --- | --- |
| `loadfix` | `060dba9` | `AwaitingLoadResult` | `ONBOARD_SESSION_NOT_READY` |
| `resulthash` | `ea8dc98` | `AwaitingDepartureSafety` | `PRE_DEPARTURE_SAFETY_NOT_VALID` |
| `safetywait` | `12eddf2` | `AwaitingDepartureSafety` | `PRE_DEPARTURE_SAFETY_NOT_VALID` |
| `correlation` | `31569f5` | `AwaitingGateArrival` | `GATE_CreateDispatchDisabled` |
| `gate` | `f48e616` | `AwaitingUnloadResult` | 无 |
| `fullloop` | `f48e616` | `AwaitingUnloadResult` | `ONBOARD_SESSION_NOT_READY` |

最终运行 `fullloop` 的终态事实：

- **两段真实移动**，均 `CreateAttemptCount = 1`：`TO_PICKUP` → 站点 21
  （`order-2093689119296323584`）、`TO_GATE` → 站点 210（`order-2093690819126099968`），
  两者 `CONFIRMED`
- **装货 `Committed`**，Sublot `Q26081298-1` 仓位 `[1]`，结果 `OverallOutcome = COMPLETED`
- 子批录入与发车安全检查各消费一条对端答复（`ConsumedSublotMessageId`、
  `ConsumedSafetyResultMessageId` 均已落值）
- 六次运行 `host.err.log` 全部 0 字节

`safetywait` 是当日方法论教训的现场记录：`12eddf2` 落地后阻断码一字未变，推翻了「十二个条件里
只有时效不满足」的判断——真因是 `correlationId` 关联对象，由 `31569f5` 修复。

证据：`8005-agv-control-server` `evidence/g3/20260829-load-to-gate-field-verify/`

## 九、端到端闭环走通（2026-08-29 深夜，`3d8b00c` + generation 3）

同车同 Demand，`gen3` 运行**全程走通**：受理 → 建单 → 取货移动 → 到站认定 → 三条快照确认 →
子批录入 → 装货 → 发车安全检查 → `TO_GATE` 移动 → 关卡到站 → 关卡批量卸货 → 四事实原子完成。
旅程终态 `Stage = Completed`、无阻断码，全程 1 分 58 秒。操作员 `S0020310`。

| 指标 | `fullloop`（`f48e616`）| `gen3`（`3d8b00c`）|
| --- | --- | --- |
| `Stage` | `AwaitingUnloadResult` | **`Completed`** |
| `SessionHello` | 74 | **1** |
| `ProtocolProblem` | 74 | **0** |
| `SnapshotAppliedAck` | 4 | **6** |
| `ProtocolOutbox` 未确认 | 3 条 | **0** |
| 四事实（ub／sc／tc）| 0／0／0 | **1／1／1** |
| 车辆租约 | 未释放 | **已释放** |

两段真实移动均 `CreateAttemptCount = 1`：`TO_PICKUP` → 站点 21
（`order-2093706784945602560`）、`TO_GATE` → 站点 210（`order-2093707175561134080`）。
四事实在同一时刻 `22:28:03.0683663+08:00` 提交，时间戳逐位一致。收尾 `portsReleased = true`、
`hostStderrEmpty = true`。

证据：`8005-agv-control-server` `evidence/g3/20260829-closed-loop-gen3/`

## 本日落地的产品修复

| 修复 | commit | 性质 |
| --- | --- | --- |
| 建单 dispatch 默认关闭开关 | `1a0158c` | 恢复「误开 runtime 不会建单」联锁 |
| 受理门禁两条（`supportsBatchUnlock`、快照新鲜度→会话活性）| `74ddda2` / `9a42582` | 解除现场完全无法受理 |
| `"--"` 占位符与 `orderState 5 → 已确认` | `addc2fa` | 解除 intent 永不可确认 |
| `ProtocolProblem` 不再拆连接 | `bf22a48` | 保留对端诊断，止住连接被杀 |
| 快照 `observedAt` 取信封冻结 `sentAt` | `8caf746` | payload 不再嵌漂移时钟 |
| 出站 wire 可被对端逐字节复现 + 重放冻结 `sentAt` | `b426ef6` | 解除到站后第一次 ack 被拒与断连 |
| MesIngest `demandId` 归一化为规范 UUID | `f94483c` | 解除取货阶段 `DemandId must be a UUID` |

| 结果哈希按对端口径重算 | `ea8dc98` | 解除装货结果被判内容冲突与两秒重放 |
| 发车安全证据在有效期内判读 | `12eddf2` | 答复在有效期内被判读 |
| 接受对端实际使用的关联方式 | `31569f5` | 解除发车安全检查被拒（真因） |
| 业务结果答复的命令不再被无限重放 | `f48e616` | 解除关卡重连被历史命令拆连接 |
| 每个停靠点用自己的 `worklistRevision` | `3d8b00c` | 解除关卡工作单被判 revision 冲突（已于 `gen3` 现场验证）|

每一处均：Release 构建 0 warning／0 error、`dotnet format` 通过、完整测试全绿 0 skip、
可回滚本机部署 PASS。

**八片 G2 绑定的更正**：`ea8dc98`～`f48e616` 五批 G2 的 `implementationCommit` 均为各自修复的
父提交（每批都在修复已进工作树、尚未提交时跑，取的是当时 HEAD），故「绑定精确 commit」这条
门禁当时并不成立。已在干净的 `3d8b00c` 上重跑：完整测试 **228/228、0 skip**，八片 G2 全 PASS 且
均绑定 `3d8b00c`，合计 137 个筛选测试、0 skip，集合 SHA-256
`a3c0401caa404473b24d243cd5fd3db99604c23d70a14a9064ced1b9054c003d`。

## 明确未证明的事项

正式 W2G-IS-00～07 的 G3 与 RC 仍为 `INCONCLUSIVE`。端到端闭环走通只覆盖票据 10 要求的**八类
向量中的第一类**（正常端到端旅程）。其余七类——重复／乱序／延迟、不同内容冲突、断联安全收尾、
进程崩溃重启、结果重放、RIoT UNKNOWN 对账、恢复分支——均无当前双端 commit 下的现场结果；
多数只有本端 G2 或绑定旧 commit 的阶段性 staged G3。清单与下一步见剩余工作文档。

功能性 happy path 成功不被扩大为完整切片 G3 PASS。
