# 决定机台取货、多仓装货、关卡卸货与成功边界

Type: grilling
Status: resolved
Blocked by: 01, 02

## Question

MVP 中操作员如何在由 EQP／AREA 解析的焊线或键合机台站通过 OnboardHmi 扫描 Sublot，核对唯一 Demand 与 ExpectedBasketCount，将同一 Sublot 的多个花篮装入完整仓位集，随后在同图关卡 FixedTaskStation 卸空全部目标仓位？

需决定取货准入、扫码不匹配、装货承诺、关卡无需输入 Sublot 还是再次核对、人员确认、物理空仓与锁闭门禁，以及「8005 本地运输完成」与外部 MES PDA 流程的独立边界。

## Answer

用户于 2026-08-25 明确回复“全部使用推荐值”，逐项采用本票 Q1～Q3 的推荐方案，并确认以下 `WIRE_TO_GATE` MVP 边界：

1. **扫码只确认既有的唯一执行承诺。** ControlServer 必须已经按[决定 Demand 受理、执行身份与完成后防重边界](02-decide-demand-acceptance-execution-identity-and-completion-deduplication.md)受理一个 `WorkType = WIRE_TO_GATE` 的 `AcceptedDemandSnapshot`，并以其中的 `DemandId` 作为本地任务实例身份。OnboardHmi 扫描或输入的 Sublot 只能确认本车、当前 `OperationSession`、当前由 `EQP + AREA` 解析出的焊线或键合机台站上这个既有 Demand；扫码不得临时发现、受理、换绑或创建另一个 Demand，也不得让车载端按 STEP、EQP 或文本重判 WorkType。
2. **MVP 保留同一路径的键盘备用输入。** `SUBLOT_ENTRY` 界面以车载扫码为主，同时允许在 OnboardHmi 键盘输入完整 Sublot；两者都只产生同一种 `SublotSubmitted` 业务请求，使用完全相同的服务端最终校验、审计和拒绝语义。键盘输入不是第二种入口模式、人工越权或 Worklist 选任务，也不能修改花篮数、仓位集、Demand 或端点。
3. **扫码不匹配一律在开锁前 fail-closed。** 服务端必须验证提交值精确对应当前唯一 AcceptedDemandSnapshot，并重新核对 DemandId、TransportDemandKey、WorkType、当前任务状态、AGV、OperationSession、机台站、操作员核验、SublotReservation、站点准入、ExpectedBasketCount、完整仓位容量以及没有其它活动物理操作。Sublot 不存在或格式无效、对应零个或多个任务、不是当前已受理 Demand、Demand 来源事实漂移、站点或状态不允许、断联、容量不足、状态未知或任一校验失败时，均返回稳定拒绝原因，保持原任务等待，不分配仓位、不发送 `SlotOperationCommand`、不产生新的业务执行。
4. **ExpectedBasketCount 由服务端按唯一批准来源计算并冻结。** ControlServer 以扫描或输入的 Sublot 执行只读 `SUBLOT_BOX_COUNT` 查询，取得各工序历史料盒计数最大值的正整数 `MAX_BOX_COUNT`；再以 AcceptedDemandSnapshot 中冻结的 `PACKAGE` 唯一匹配已批准且当前有效的 `mes/reference/package-basket-capacity.csv` 容量规则，得到正整数 `capacity = max_boxes_per_basket`，并计算：

   `ExpectedBasketCount = ceil(MAX_BOX_COUNT / capacity)`

   该值必须在 `OperationCommitPoint` 前由服务端冻结，是本次装货不可修改的权威篮数。车载端和操作员不得输入、改写、追加或从目标仓位数量反推该值。查询失败、无结果、空值、零或负数、超时、冻结 PACKAGE 缺失、容量未命中或命中冲突、换算失败时，本次装货失败并形成可诊断的准备阻断；既有 Demand 不因此取消，但不得分仓或开锁。具体查询契约见 [`SUBLOT_BOX_COUNT`](../../../mes/queries/sublot-box-count/README.md)，容量执行权威见 [`package-basket-capacity.csv`](../../../mes/reference/package-basket-capacity.csv)。
5. **装货采用一仓一篮、完整集合、批量开锁和整批自动提交。** 服务端必须满足 `ExpectedBasketCount == SlotOperationCommand.slots.Count`，一次性选择、预留并冻结数量相等且全部具备业务与物理资格的完整目标仓位集合；可用仓位不足时整批拒绝，不允许部分装入、替换目标仓位或一仓多篮。OnboardHmi 在产生 IO 副作用前持久化完整命令与目标集合，按 IO 模块批量开锁；操作员可按任意顺序把无独立身份的花篮各放入一个目标仓位并关门。每仓都必须可靠达到 `OCCUPIED + 锁闭 + 开锁输出已复位`，且全部目标仓位安全状态有效后，ControlServer 才自动整体提交 LoadBatch；逐仓物理成功只是恢复和审计证据，不是部分装货成功，也不再要求额外 LoadFinalConfirmation。
6. **目标态不符时必须闭环，不能由人员按钮覆盖。** 装货关门后明确读到 EMPTY 时自动重新弹锁并引导重新放入；关卡卸货关门后明确读到 OCCUPIED 时自动重新弹锁并引导继续取空。两类操作都重复到目标占用态、锁闭反馈和开锁输出复位同时成立，不设可强行放行的重试次数上限。`SlotOccupancyState = UNKNOWN`、锁闭反馈无效、输出无法确认复位或通信/硬件状态不明时暂停并进入恢复，不自动猜测、盲目重开或宣布成功；异常恢复的最小范围继续由[决定 MVP 多仓容量、安全联锁与异常恢复最小集](05-decide-minimum-multislot-safety-and-recovery-set.md)收口。
7. **关卡卸货不再次输入 Sublot、工号或接收确认。** 车辆到达同图 `WIRE_TO_GATE` 关卡 `FixedTaskStation` 且满足卸货安全门禁后，服务端直接根据 AcceptedDemandSnapshot、当前站点、任务目标及在车仓位业务状态识别该 Demand 的完整目标仓位集合；OnboardHmi 不要求扫描 Sublot、不读取随货单据、不输入卸货工号，也不提供“接收、暂不收货、拒收、稍后接收”或到站取消入口。车载端按完整集合批量开锁，人员可任意顺序取货和关门；每仓可靠达到 `EMPTY + 锁闭 + 开锁输出已复位` 后可独立清除该仓位与 Sublot 的业务关联，其它仓位失败不得回滚已清空仓位，但全部目标仓位未完成或未明确异常收敛前，`StationOperationGuard` 保持且车辆不得离站。
8. **本地运输成功采用一个明确的原子边界。** 当该 Demand 的全部目标仓位结果已经由 ControlServer 可靠持久化并证明为 `EMPTY + 锁闭 + 开锁输出已复位`，且本次纯卸货停靠没有未收敛仓位操作时，ControlServer 在同一业务事务中完成 UnloadBatch、提交本停靠的 `StopClosureCommit`、将该 `DemandId` 置为本地成功终态，并创建以 TransportDemandKey 为永久键、引用完成 DemandId、接受时 DemandRevision、完成时间和逐仓闭环证据的 `TransportDemandCompletion`。任一组成部分不能提交时不得形成部分成功。逐仓业务清空可以先发生，但不能提前宣告整个 Demand 成功。
9. **发车安全检查不回滚已完成运输。** 本地成功事务提交后，ControlServer 仍须取得新的 `PreDepartureSafetyCheck`，并只在最新有效的 `DepartureSafe = true` 和其它移动门禁均成立时请求 RIoT 移动。安全检查失败、过期或结果未知时车辆继续保持，不得发车；它只决定车辆能否移动，不改变或回滚已经由全部卸货证据证明的本地运输成功、StopClosureCommit 或 TransportDemandCompletion。
10. **8005 本地成功与外部 PDA/MES 完全独立。** 8005 全部组成部分继续严格只读 MES，不执行完工、卸货、过站、接收、入库或其它写回，也不通过工作流代办现场流程。目的站责任人按既有 PDA/MES 流程独立完成后续业务；8005 不等待、轮询、读取或验证其结果，不显示后续提醒、待办或未确认告警，也不以之后观察到的 MES 变化改写本地终态。外部 PDA 尚未操作、MES 仍可见、随后 `GONE`、再现或服务重启，都不得重复执行已经具有 TransportDemandCompletion 的 TransportDemandKey。

关键约束证据包括：需求基线 `REQ-0158`～`REQ-0163` 的 MES 只读与本地完成边界、`REQ-0184` 与 `REQ-0193` 的机台端点和同图 FixedTaskStation、`REQ-0213` 与 `REQ-0218` 的 Sublot 输入和服务端最终裁决原则、`REQ-0221`～`REQ-0224` 的目的站直接卸货与完工后边界；以及 [`ADR-cross-0035`](../../../docs/adr/cross/0035-server-orders-slots-onboard-executes-array-order.md)、[`ADR-cross-0036`](../../../docs/adr/cross/0036-load-batch-commit-and-hardware-fault-hold.md)、[`ADR-cross-0037`](../../../docs/adr/cross/0037-unload-batch-clears-business-state-only-after-all-empty.md)、[`ADR-cross-0040`](../../../docs/adr/cross/0040-internal-light-curtain-is-slot-occupancy-evidence.md)、[`ADR-cross-0041`](../../../docs/adr/cross/0041-one-basket-per-physical-slot.md)、[`ADR-cross-0042`](../../../docs/adr/cross/0042-sublot-is-load-input-and-server-resolves-task.md)和 [`ADR-cross-0054`](../../../docs/adr/cross/0054-auto-load-commit-with-pre-departure-correction.md) 中已接受的跨端权威与闭环决定。
