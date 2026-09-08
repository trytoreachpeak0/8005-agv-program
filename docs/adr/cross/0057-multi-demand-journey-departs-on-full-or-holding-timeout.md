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

**操作员可以录入本次派车范围内的任意有效 SUBLOT，不限于当前站点那一个。**这是收窄的另一面，
和上面几条同源：一趟只有一单，清单里就只有一个 SUBLOT，于是
`SublotEntryRequested.expectedSublot` 成了单个字符串，车载端拿它做精确比对，输别的直接以
`SUBLOT_NOT_IN_WORKLIST` 挡在本地。FR-001 的 AC-3 要求的恰恰相反——"允许 T 的目标站点与操作员
当前物理站点不完全相同，只要 T 在范围内"——而 BR-001 把范围定义为"本次派车下发时关联的任务集合"，
明说它"可能同时涵盖多个相邻站点各自的搬运任务"，判据是集合归属而非距离。范围外的 SUBLOT 仍要拒
（AC-4），但那是服务端的判定，不是车载端拿一个字符串比出来的。

**录入之后的校验要在录入之后做，并且要把真实原因回给操作员。**BR-013 第 2 节把时机写死在
"操作员输入 SUBLOT 后"：服务端查 `SUBLOT_BOX_COUNT` 得到 `MAX_BOX_COUNT`，结合冻结的 `PACKAGE`
与已批准的花篮容量对照算出 `ExpectedBasketCount`；查询失败、无结果、数量非正、**`PACKAGE` 缺失、
容量未匹配或匹配冲突时本次装载报错并停止，不分配仓位、不发送开锁指令**。当前实现把这些整体提前到
了受理阶段的候选评分里（`PACKAGE_CAPACITY_NOT_UNIQUE`、`SUBLOT_BOX_COUNT_UNAVAILABLE`），后果是
这类需求根本不会进入作业清单，操作员扫到它时得到的提示是"不在清单里"——**原因是错的**，真正的原因
（这个 PACKAGE 没有登记容量）从来没有传到车前。协议里的 `SublotRejected` 正是为此定义的，它带
`problem` 与 `currentWorklistRevision`，而服务端至今一行都没有实现它。

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
- **理由码已对齐（不必等本条实施，已先行落地）。**第一期自造的
  `CANCELLED_BY_SUBLOT_WAIT_TIMEOUT` 与 `CANCELLED_BY_OPERATOR_BEFORE_LOAD` 已改为基线登记的
  `CANCELLED_BY_STATION_TIMEOUT` 与 `CANCELLED_BY_OPERATOR`。第二个的取值值得记一笔：起初以为该用
  `CANCELLED_BY_STOP_COMPLETE`，但那是 UC-002 里操作员点击「本站装货完成」的终态；本条实现的动作是
  ADR-cross-0046 首项——"SlotOperationCommand 尚未发送且没有物理装载"的取消——它明确终结为
  `CANCELLED_BY_OPERATOR`，与装货中取消同码，两者靠物理阶段和审计主体区分。
- **取消抑制已实现（同样先行落地）。**`TransportDemandSuppressions` 表按
  TransportDemandKey（任务类型 + SUBLOT）记录永久禁令，五个理由码
  （`CANCELLED_BY_OPERATOR`、`CANCELLED_BY_LOAD_COMPENSATION`、`CANCELLED_BY_STOP_COMPLETE`、
  `CANCELLED_BY_STATION_TIMEOUT`、`TERMINATED_BY_FAULT_CARGO_HANDOFF`）写入，候选评分以
  `TRANSPORT_DEMAND_SUPPRESSED` 挡下。首条禁令不被后来的覆盖，也没有解除入口。此前它一条都没写，
  包括已有的装货中取消路径。
- **仍未实现：ADR-cross-0046 要求这一幕也走 `LoadCancellationResult`**（"车载端获得取消授权后确认
  没有关联目标仓位，直接报告 ALL_EMPTY"），而 `LoadCancellationResult.slotResults` 是 `minItems: 1`，
  装不下没有仓位的 ALL_EMPTY。当前实现以"授权即终结"绕开该矛盾，形状与 0046 不同。放宽那个下限是
  schema 变更，随本条的 v0.2.0 一并处理。
- `SublotEntryRequested.expectedSublot` 从单个字符串改为本站可录入的候选集合，或改由服务端在收到
  `SublotSubmitted` 后判定归属——两者都是 breaking，随本条的 v0.2.0 一并定。同时实现
  `SublotRejected`：录入被拒时操作员要看到的是 `PACKAGE` 未登记、不在派车范围、任务已取消这类具体
  原因，而不是一句"不在清单里"。
- 受理阶段仍可保留 `PACKAGE`/箱数的预检以避免派出注定装不了的车，但它不能再是唯一一次检查：
  BR-013 要求录入后重算，因为容量对照表和 MES 的箱数都可能在派车之后变化。
- L2 场景层要新增"一趟多单"的基线场景，现有三条新场景
  （`load-cancelled-before-sublot`、`sublot-wait-timeout`、`auto-charge-endurance`）中按单单假设写的
  断言要重写。合成对端的应答缓存键已在第一期改成带业务身份，多单场景不再受"一个会话只能装一次货"
  的限制。
