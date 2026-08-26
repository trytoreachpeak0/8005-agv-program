# WIRE_TO_GATE 单场景 MVP 范围与验收规格

## 1. 目的与绑定身份

本规格把一个受控 `WIRE_TO_GATE` 旅程交接给相互独立的 ControlServer、OnboardHmi 实现仓库，以及一个独立轻量协议仓库。它绑定 [README](README.md) 中列出的需求基线与最终适用性 TSV 身份。任何实现都不得用同名的新文件替换已绑定资产，也不得只依据需求基线自行推断 MVP 适用性。

## 2. 范围内

- 只接受 MesIngest 发布的完整 `WorkType = WIRE_TO_GATE` Demand；同时覆盖焊线与键合来源，下游不得按 STEP、EQP 或文本重新分类。
- 一台指定 AGV、一张 Map，且同一时刻最多存在一个已受理／未结清的 DemandId。一个 Sublot 可需要 1～8 个匿名花篮，每个物理仓位恰好放置一个花篮。
- 两段严格串行的移动：先以 `TO_PICKUP` 前往被冻结的机台站，再以 `TO_GATE` 前往被冻结的关卡站。
- 在 OnboardHmi 通过扫码输入取货信息，同时保留完整 Sublot 的键盘备用输入；两者使用同一请求和校验路径。
- 冻结完整仓位集并批量装货；到达关卡后，根据当前任务和车载业务事实自动批量卸货，不进行第二次 Sublot 扫码、不输入工号，也不等待接收确认。
- 本地完成不依赖外部 PDA／MES 收货流程。8005 不等待、不读取也不写回该结果。
- 最小安全恢复、人工充电保持／复投运、协议一致性，以及受控工厂试运行证据。

## 3. 明确不在范围内

其他 WorkType、多车调度、多个并发 Demand／Sublot、复合或顺路取货、跨地图运输、自动充电、排队或充电桩故障改派、外部 PDA 集成或 MES 写回、完整配置／账号／报表 UI、远程仓库创建、生产实现与部署。被延后或判定本场景不适用的需求仍在 v1.0.0 基线中保持原 Lifecycle。

## 4. 端到端规范流程

1. ControlServer 读取 MesIngest 当前完整目录，只考虑符合条件的 `WIRE_TO_GATE` 候选，并执行硬准入：精确任务类型与区域准入、同一 Map、站点可解析、路线证据、VehicleBusinessReadiness、无未结副作用、适用仓位充足及已批准的电量策略。
2. 候选按连续等待时长降序、本地创建时间升序、DemandId 升序进行确定性排序。忙碌、临时容量不足，以及符合有效策略的低电／电量未知均保留在未分配积压中；结构性无解必须产生去重后的即时阻断。
3. 在执行任何动作或产生远程副作用前，ControlServer 必须无条件重读完整目录。只有 HistoryEpoch 相同且完整决策元组未变化时才允许受理。一个事务必须冻结 AcceptedDemandSnapshot 及相关身份、阻止活动／已抑制／已完成重复，并创建唯一的本地执行。DemandId 是执行身份；TransportDemandKey 是跨代次永久去重键。
4. ControlServer 调用 RIoT 前必须先持久化 `TO_PICKUP` OrderIntent。每次调用前都重新校验被冻结的 AGV 代次／绑定、Map、站点、路线、业务 readiness 和新鲜的 PreDepartureSafetyCheck。未知结果必须沿原 MovementLegId、DispatchGeneration 和 upperId 对账。
5. 单纯到站遥测不构成可信到站。只有独立确认 RIoT 订单成功、车辆为 IDLE、精确 Map／站点匹配、没有未结调用且停车／安全证据新鲜时，才能打开 StationOperationArrivalGate。
6. 在机台取货点，ControlServer 打开已绑定的 Sublot 输入。扫码与键盘均产生 `SublotSubmitted`。在分配仓位或发出任何操作命令前，服务端最终校验必须成功。
7. ExpectedBasketCount 必须根据已批准的 Sublot 读取结果和被冻结的 PACKAGE 容量规则，按 `ceil(MAX_BOX_COUNT / max_boxes_per_basket)` 计算。结果必须为 1～8，且可由一个完整适用仓位集容纳。不得使用默认值、估算值、部分装载，也不得事后替换仓位。
8. ControlServer 必须持久化 StationOperationGuard，冻结 Demand／Sublot／数量／有序仓位集和命令意图。OnboardHmi 必须在操作 IO 前持久接受原始 SlotOperationAttemptId 及命令内容。只有 OnboardHmi 可以控制 IO 与硬件安全。
9. 每个装货仓位都必须达到 `OCCUPIED + 锁闭 + 开锁输出复位`。只有全部目标仓位安全闭环后，才能整体提交 LoadBatch。在 StopClosureCommit 之前，经过授权的纠错使用原仓位，并审计 `OCCUPIED→EMPTY→OCCUPIED`。经过授权的取消／补偿只有在完整范围安全清空后才能结束。
10. 装货和机台停靠闭环安全提交后，ControlServer 必须另行持久化 `TO_GATE`，取得新的新鲜安全检查，并执行相同的移动／对账门禁。
11. 到达关卡后，StationOperationArrivalGate 自动触发一次完整 UNLOAD 操作。不得要求新的 Sublot／工号／PDA 输入。每个仓位都必须达到 `EMPTY + 锁闭 + 开锁输出复位`；在完整目标集结清前，Guard 始终保持。
12. 一个事务必须提交 `UnloadBatch + StopClosureCommit + Demand 成功 + TransportDemandCompletion`。MesIngest 中的消失、重新出现、刷新，或相同业务键生成新的 DemandId，都不得再次触发执行。本地成功旅程永远不依赖 PDA／MES 完成。

## 5. 权威职责划分

| 事实／动作 | ControlServer | OnboardHmi |
| --- | --- | --- |
| Demand、AcceptedDemandSnapshot、选择、TransportDemandKey 去重 | 唯一权威 | 只显示已绑定投影 |
| Map／站点、移动段、OrderIntent、RIoT 调用 | 唯一权威 | 绝不调用 RIoT，也不选择移动 |
| Sublot 校验、ExpectedBasketCount、仓位预留／集合、业务提交 | 唯一权威 | 不发现／重绑任务，也不修改仓位集 |
| SlotPhysicalState、IO、锁／光幕／输出、仓门序列 | 消费抽象证据 | 唯一权威，并拥有安全否决权 |
| SlotBusinessState | 唯一权威 | 只报告物理结果 |
| OnboardExecutionJournal 与 ProvenRecoveryCheckpoint | 消费报告 | 唯一权威 |
| StationOperationGuard 与业务 readiness | 持久化并决策 | 执行收到的状态及本地安全门禁 |
| UI 组合视图 | 发布带版本的投影 | 组合显示，但不得成为新的权威 |

## 6. 最小安全、持久化与恢复集合

- 八个稳定仓位身份始终存在，即使其中某个不可用。配置／IO 未知、过期、无效或冲突时必须阻断操作；任何管理员都不得制造“安全”事实。
- StationOperationGuard 覆盖输入、装货／卸货、纠错、取消、暂停和恢复。Guard 活动或未知时，所有移动入口必须阻断。
- 锁反馈用于证明锁闭；仓内光幕只产生 OCCUPIED／EMPTY／UNKNOWN。UNKNOWN 时不得循环猜测。已知但与目标相反的占用状态必须继续原闭环，不允许以次数上限强制成功。
- 可靠发送方必须先持久化意图再发送；接收方必须先持久化规范化内容、MessageId、哈希和已接受责任，再返回 DurableAck。相同 ID／相同内容重放首个结果；相同 ID／不同内容返回稳定冲突。
- 断联时不得扩张 ActiveUnlockSet。只允许 SafelyFinishActiveUnlockSet，随后在 Guard 下暂停。重连必须启动五步 RecoveryHandshake；连接或心跳恢复本身不构成授权。
- 重启必须结合 journal 和重读实时 IO。只有从唯一可解释的 ProvenRecoveryCheckpoint 才能继续。歧义、journal 缺失、UNKNOWN 或冲突都进入 VehicleRecoveryRequired。
- 最小 ExceptionRecoverySession 必须绑定一个具名管理员、一个事件、一辆车及固定任务／仓位范围。只允许四条路径：修复后继续、完整装货补偿至空、具名货物交接，或在合格物理隔离下强制机械恢复。货物交接不证明电子空仓、仓门安全或车辆 readiness。
- 低电量使用 ManualChargingHold。只有具名管理员可请求复投运，随后必须重新对账电量／非充电、IDLE、位置、订单、Guard、仓位、能力、安全和恢复状态。电量遥测回升本身不能恢复 readiness。

## 7. UI 权威与生产映射

生产 OnboardHmi 必须映射选定的 A 方案“旅程导引台”源文件：固定左侧旅程区；中央只显示当前步骤、权威事实和一个正常主动作；固定右侧显示 1～8 号仓位证据；并把移动、连接／业务 readiness、当前作业和安全／联锁拆成四个独立维度。B／C 方案只作为对照证据。生产映射必须由真实车载端开发者评审，并在目标分辨率、缩放、触摸方式、扫码结束符／焦点行为、键盘备用、观看距离和光照条件下完成最终测试。原型票的评审豁免不能满足此门禁。

## 8. 协议与一致性

运行时使用 NDJSON ProtocolEnvelope、精确整数 ProtocolVersion 匹配，以及明确的 `WireToGateMvpProtocolProfile` allowlist。精确 release 必须以复合 ProtocolReleaseIdentity 标识，绝不能只使用 `main`、分支或 tag。消息语义、字段、错误码与向量由[共享协议仓库交接](protocol-repository-handoff.md)固定。每次真实 release 都必须由两名真实开发者本人确认，AI 不得签署。

实施按稳定的 `W2G-IS-00` 至 `W2G-IS-07` 推进。G0 锁定完整且获得真实批准的 release；G1 证明共享资产内部一致；G2 证明每个真实组件、本仓维护的 Fake 及 Fake 自身；G3 证明两个精确真实构建可以共同工作。FAIL 和 INCONCLUSIVE 必须保留为不可修改证据。G2 不能替代 G3，G3 也不能替代工厂试运行。

## 9. 验收边界

工厂执行必须使用不可修改的 FactoryPilotConfigurationSnapshot 和 FactoryPilotRunIdentity，严格按 P0～P7 进行。只有此前全部门禁通过后，P6 才执行一次受控真实物料旅程。PASS 必须包含 P7 对账并满足全部不变量；FAIL 或 INCONCLUSIVE 必须停止推进并启动严格收敛／清场。一次 PASS 只证明该精确候选和配置，不构成 release 批准。

## 10. 需求适用性

最终 TSV 是逐行规范权威。实施团队必须把全部 186 条适用需求（85 条直接必须＋101 条交互／安全依赖）导入各自工作跟踪系统，并完整保留 TSV 中的理由和影响字段。31 条延后需求及 131 条不适用需求必须继续作为排除项可见，且保持原 Lifecycle 不变。任何重新分类都需要新的产品决策；实现代码、AI 解释和协议治理均无权改变分类。
