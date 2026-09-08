# 一趟旅程承载多个需求，装满或持货超时才前往关卡

需求基线从一开始就是"一次停靠处理多个任务、一趟行程经过多个停靠"：ADR-cross-0048 的
CurrentStopWorklistSnapshot 描述"当前到达站点有哪些待装、待卸和复合作业"，ADR-cross-0053 的
UpcomingStopPlan 是"按顺序排列的 PlannedStop"且服务端可以增删或重排尚未执行的停靠，
ADR-cross-0055 与 FR-004 在结束本站时终结的是"全部尚未开始的待装 DemandId"——都是复数。
**MVP 的实现把它收窄成了一趟一单、取货与关卡两段，而这个收窄被写进了协议 schema 和 G1 断言，
于是它从"暂时只做一单"变成了"契约规定只能一单"。**本 ADR 解除该收窄，并补上基线未覆盖的一件事：
车辆在装货阶段究竟什么时候停止收货、转而前往关卡。

收窄点有四处，`protocol-v0.1.1` 与 ControlServer 各两处：
`CurrentStopWorklistSnapshot.payload.items` 的 `maxItems: 1`；
`UpcomingStopPlanSnapshot.payload.legs` 的 `maxItems: 2`、`sequence` 上限 2 与只有
`TO_PICKUP`/`TO_GATE` 两个 `legType`；ControlServer 的 `JourneyRuntimeRow` 以 `DemandId` 为主键，
每条消息的 messageId、取货站点与装货 attempt 都只有一份；以及
`tools/g1-validate.mjs` 里把第一处直接断言成了 W2G-IS-01 的责任边界
（`check(worklistItems?.maxItems===1, "W2G-IS-01 worklist must contain at most one committed Demand")`），
所以改 schema 而不改 G1 会当场判红。四处必须一起动。

**一趟旅程承载一个停靠序列，每个停靠承载多个 DemandId。**旅程的身份不再是需求的身份：
`JourneyRuntimeRow` 改以旅程自身的标识为主键，需求以从属行挂在停靠下。停靠序列由服务端编排并可
重排，车载端按 ADR-cross-0053 只读整体替换。

**装货阶段在"装满"或"持货超时"两者先到者发生时结束，随即前往关卡。**装满指车辆可用仓位已不足以
承载下一个候选需求的 `ExpectedBasketCount`——不是仓位全满，因为一个需求要整批装下才有意义。
持货超时的期限是 **30 分钟**，**从第一个 LoadBatch 安全闭环那一刻起算**，不是从受理起算，也不是从
第一次到站起算：货真正上车之前不存在持货风险，而到站之后可能根本没有货可装（那种情况由
ADR-cross-0055 的站点停留超时处理，与本条无关）。空载时持货超时不适用。

**持货超时到期时不打断正在进行的仓位操作。**若期限到达时某个 LoadBatch 正在执行，等该批安全闭环后
立即结束装货阶段，不再接受新的待装需求。这与 ADR-cross-0055 "活动仓位操作阻断倒计时离站"是同一条
原则：物理安全的收敛优先于调度期限。

**本条与 ADR-cross-0055 是两个独立的期限，不互相替代。**0055 的 StationDepartureWaitTimeout
（默认 5 分钟）回答"这一次停靠还要不要继续等人操作"，到期结束的是**本站**；本条的持货上限回答
"这趟车还要不要继续收货"，到期结束的是**整个装货阶段**。前者在每个 LoadBatch 闭环后重新计满，
后者从第一批闭环起单调走完，不因新的停靠而重置——否则不断有新单进来的车永远不会去关卡。

**Status**: proposed

**Considered Options**:
- 维持一趟一单（拒绝：违背 0046/0048/0053/0055 的基线，且关卡往返次数变成仓位数的倍数，
  一台八仓位车按单单跑要跑八个来回才装满一次）
- 只按"装满"触发（拒绝：没有后续需求时，车辆会拿着半车货在取货区无限等待）
- 只按时间触发（拒绝：期限未到而仓位已满时，后续需求无处可放，判定会退化成"装不下就报错"）
- 装满或持货超时，先到者生效（采纳）
- 持货超时从受理或首次到站起算（拒绝：那两个时刻车上可能一件货都没有，会把"没货可装"误判成"持货过久"，
  而那是 0055 的职责）

**Consequences**:
- 这是**协议 v0.2.0**，不是补丁：`legs`、`items` 的上限与 `legType` 枚举都属于
  `8005-agv-protocol/CLAUDE.md` 定义的 breaking 变更（required/type/enum/含义/副作用），
  要递增 ProtocolVersion 与 release-major。两端 W2G-IS-00 到 W2G-IS-07 的
  G1/G2/G3 证据**全部作废**，需重跑；发布需要两位 product owner 在 approval attestation 上签名。
- `tools/g1-validate.mjs` 中锁定 `maxItems===1` 的那条 W2G-IS-01 责任边界断言必须同步改写，
  否则 schema 一放宽 G1 立刻判红。**改协议 schema 与改 G1 是同一次改动的两半。**
- `scripts/test-wire-to-gate.ps1` 里硬编码的四个协议身份哈希
  （`$expectedProtocolCommit`、`$expectedManifestSha256`、`$expectedSchemaBundleSha256`、
  `$expectedVectorsSha256`）在发布后要一并更新，否则 CONTROL_SERVER_G2 会以
  `Protocol manifest hash mismatch` 拒绝启动。
- `JourneyRuntimeRow` 重建并迁移：主键换成旅程标识，需求、停靠、每停靠的消息 id 与装货 attempt
  拆成从属表。现有单单旅程在迁移中视为"一个停靠、一个需求"的退化形态。
- 车载端的 CurrentStopWorklist 与 UpcomingStopPlan 渲染要能承载多项与多段，属于
  `8005-agv-onboard-hmi`，按 `w2g/*` 分支加 PR 的路径交付。
- **一并对齐第一期落地时自造的两个理由码。**ControlServer 现在用
  `CANCELLED_BY_SUBLOT_WAIT_TIMEOUT` 与 `CANCELLED_BY_OPERATOR_BEFORE_LOAD`，而基线登记的是
  `CANCELLED_BY_STATION_TIMEOUT`（等待到期）与 `CANCELLED_BY_STOP_COMPLETE`（操作员确认本站完成），
  见 FR-004、FR-031、UC-002、UC-046。同一件事有两套名字会让审计对不上。
- **取消抑制仍未实现，本次一并补。**ADR-cross-0047 与 FR-004 要求上述两个理由码原子写入
  `TransportDemandSuppression`（按 TransportDemandKey = 任务类型 + SUBLOT）。ControlServer 目前
  没有这张表，取消只更新 `AcceptedDemands` 的状态——同一个 DemandId 不会被重选，但 MesIngest 为
  跨 GONE 再现分配新 DemandId 时，同一个 SUBLOT 会作为新实例重新进入候选，车辆会被再次派往同一个
  空站点。单单模型下这只是缺陷，多单模型下每个停靠都可能踩到。
- L2 场景层要新增"一趟多单"的基线场景，现有三条新场景
  （`load-cancelled-before-sublot`、`sublot-wait-timeout`、`auto-charge-endurance`）中按单单假设写的
  断言要重写。合成对端的应答缓存键已在第一期改成带业务身份，多单场景不再受"一个会话只能装一次货"
  的限制。
