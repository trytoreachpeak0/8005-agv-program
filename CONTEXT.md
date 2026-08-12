# 8005 多仓位 AGV

宿迁长电多仓位 AGV 项目的统一领域用语：覆盖 MES/调度编排与 RIoT SDK 消费边界。实现细节见各子系统代码与 `docs/adr/`。

## Language

### 部署角色

**ControlServer（服务端）**:
跨车辆共享的中央业务主体，掌握全局搬运任务与调度事实。
_Avoid_: 本地服务器（易与车载节点混淆）、后台（泛称）

**OnboardHmi（车载上位机）**:
随单台多仓位 AGV 部署、面向本车现场操作与仓位硬件的边缘业务节点；一台 AGV 对应一台。
_Avoid_: 上位机（脱离上下文时歧义）、操作台、客户端（泛称）

**OperatorTerminal（操作终端）**:
不随 AGV 移动的固定访问终端；若项目部署此类终端，不与车载上位机混称。
_Avoid_: 上位机、车载上位机

### 仓位操作与恢复

**断联仓位操作收敛（ConnectionLossSlotContainment）**:
车载上位机与服务端失联后限制仓位操作风险范围的保护策略：禁止扩大当前开锁集合；已经开始或发送结果不确定的开锁集合完成安全收尾后暂停，且不设置自动取消超时，直至重连对账并获得服务端明确授权。若只是通信断联且物理状态始终有效，服务端授权到达后车载端直接继续，不要求操作员重复确认；若同时存在锁 DI 等硬件故障，则必须另行取得 HardwareRecoveryConfirmation。连接恢复本身不构成授权。
_Avoid_: 断线续跑、自动取消超时、连接恢复即续跑、重连后重复人工确认

**当前开锁集合（ActiveUnlockSet）**:
本次物理操作中已经发出开锁命令或发送结果不确定的仓位集合；装货与卸货均可包含批量打开的多个仓位。跨 IO 模块批量开锁途中失联时，只包含已经发送或发送结果不确定的模块分组，尚未发送的分组不得加入。
_Avoid_: 整个指令仓位清单、尚未开始的仓位、仅收到成功反馈的仓位

**当前开锁集合安全收尾（SafelyFinishActiveUnlockSet）**:
车载上位机只允许完成当前开锁集合中已经开始的物理动作：普通装货仓位必须达到 `OCCUPIED + 锁闭 + 开锁输出已复位`，卸货或取消清空仓位必须达到 `EMPTY + 锁闭 + 开锁输出已复位`，并形成可恢复对账的逐仓结果；它不表示整个装货批次或到站卸货操作已经完成。连接在线且已经取得 LoadCancellationAuthorization 时，当前装货仓位可以切换为取消清空；授权或持久化切换完成前发生断联时仍按普通装货收尾，切换完成后发生断联时则按取消清空收尾。
_Avoid_: SafelyFinishCurrentSlot、立即中止已开门仓位、只关门不完成本次放入/取出、完成整个剩余批次

**仓位目标态闭环（ExpectedSlotOccupancyClosureLoop）**:
每次仓门锁闭反馈到达后，车载上位机立即核对当前操作要求的 SlotOccupancyState：装货及纠错重放要求 OCCUPIED，卸货、装货补偿和取消清空要求 EMPTY；若读到明确相反状态，则自动再次弹锁并引导操作员重新放入或取出，直至锁闭后的占用状态符合预期，不设可强行放行的重试次数上限。操作员可以暂停并呼叫维护，但 StationOperationGuard 保持；状态为 UNKNOWN 时暂停并进入恢复，不自动猜测或循环开锁。
_Avoid_: 关门即成功、操作员按钮覆盖光幕、占用不符仍继续后续仓位、UNKNOWN 时自动重开

**OnboardExecutionJournal（车载执行日志）**:
车载上位机为当前仓位操作保留的最小可恢复记录，至少包含当前仓位操作尝试编号、指令摘要、装卸类型、目标仓位集合与执行方式、关键执行阶段、当前开锁集合、逐仓结果、当前 Sublot 引用、车载操作员上下文以及待确认应答结果；它用于识别重复命令、恢复执行进度并可靠补报结果，不是运输任务副本。开锁等不可逆副作用必须先写入准备阶段再执行。
_Avoid_: 车载任务库、本地业务数据库、离线任务系统

**可唯一解释恢复（UniquelyExplainableRecovery）**:
车载重启后，持久化执行阶段与重新读取的实时 IO 只能导出一个安全结论、一个逐仓结果语义和一个合法下一步时，允许恢复当前开锁集合；实时物理状态始终以重读 IO 为准。若存在多个可能解释、状态冲突或任一相关状态为 `UNKNOWN`，则进入车辆待恢复态。
_Avoid_: 只比较有货/无货、用关机前 IO 快照覆盖实时 IO、从头重试

### 仓位事实

**Slot（仓位）**:
AGV 上具有稳定物理编号、独立门锁与占用检测能力的固定储物位置，是所有仓位相关领域名称的统一词根。
_Avoid_: Compartment、仓格、舱位

**SlotIdentity（仓位身份）**:
由 AGV 标识与物理仓位号共同确定的稳定身份；不会因 IO 映射变更、硬件不可用或配置缺失而消失。
_Avoid_: IO 通道、配置数组索引、可用仓位

**OnboardSlotLayoutSnapshot（车载仓位布局快照）**:
服务端权威仓位模型面向特定 AGV 生成、由车载上位机持久化的只读布局投影；它以物理仓位号表达仓位所属面、位置和跨度，供车载 HMI 正确展示，但不包含 IO 映射，也不是车载端可独立编辑的模型主数据。
_Avoid_: IO 配置、临时界面缓存、车载仓位模型

**SlotIoBinding（仓位 IO 绑定）**:
车载上位机以物理仓位号为键保存的逐仓开锁输出、锁闭反馈和仓内光幕等 IO 映射；当前一仓一门，因此仓门不建立独立于 SlotIdentity 的身份。
_Avoid_: IO 通道列表、DoorId、按界面位置绑定 IO

**SlotOperability（仓位可操作性）**:
车载上位机依据有效 IO 映射、模块在线性和实时安全执行条件形成的仓位硬件能力；它不改变 SlotIdentity，也不自动改变仓位业务内容，服务端人工启用不能覆盖车载端判定的不可操作。
_Avoid_: 仓位存在性、业务空闲、人工启用/禁用

**仓位管理可用性（SlotAdministrativeAvailability）**:
服务端保存的人工启用/禁用业务策略；车载 HMI 须在仓门真实位置展示。未被活动 Sublot 占用时禁用立即生效；已被活动 Sublot 占用时进入待禁用（Disable Pending），该 Sublot 经服务端确认结束后生效。它不能替代或覆盖仓位可操作性。
_Avoid_: SlotOperability、硬件故障、删除仓位

**IoConfigDraft（IO 配置草稿）**:
车载上位机保存但尚未激活的 IO 映射候选版本；它可以离线编辑和静态校验，但只有车辆进入配置维护态后才可激活，保存草稿不影响当前生效配置或真实 IO。
_Avoid_: 当前配置、离线生效配置、已激活配置

**OnboardCapabilitySnapshot（车载能力快照）**:
车载上位机向服务端公开的仓位数量、物理仓位号、逐仓可操作性、抽象不可用原因、能力版本和观测时间；不包含任何 IO 映射细节。
_Avoid_: IO 配置、DO/DI 映射、寄存器快照

**批量开锁（BatchUnlock）**:
车载上位机对一个已持久化目标仓位集合执行的批量物理动作：同一 IO 模块内优先使用 Modbus `0x0F` 写多个线圈；跨模块时按模块分组并行发送，全部已计划分组发送完成后才统一进入反馈检查。跨模块不承诺电气意义的绝对同时；每个仓位的锁反馈、输出复位和结果仍独立判断。
_Avoid_: 逐仓完整状态机串行执行、跨设备原子事务、某仓失败即回滚已开仓门

**VehicleConnectionSession（车辆连接会话）**:
服务端为某个 AGV 当前唯一有效的车载长连接分配的带代次通信上下文；新代次生效后，旧代次消息不再被接受。
_Avoid_: OperationSession、TCP 连接本身、slotOperationAttemptId

**ConnectionLivenessPolicy（连接存活策略）**:
车载上位机每 2 秒发送心跳，任一侧收到合法协议消息都刷新本侧存活时间；TCP 明确断开时立即判定失联，连接未断但连续 6 秒没有收到合法消息时判定失联。参数按项目统一配置，不按车辆单独调整。
_Avoid_: 单次心跳丢失即断线、只依赖 TCP 状态、每车不同超时

**VehicleBusinessReadiness（车辆业务就绪态）**:
VehicleConnectionSession 完成认证后，由服务端在能力同步、未结操作及积压结果对账、物理与业务状态核对均通过时明确授予的业务状态；只有处于该状态才可开始扫码、接收新仓位操作或恢复移动。
_Avoid_: TCP 已连接、TLS 已认证、心跳正常

**VehicleRecoveryRequired（车辆待恢复态）**:
车辆连接在线，但恢复对账存在无法自动解释的差异，或者锁 DI 等关键硬件反馈失效、无法证明仓门安全状态时，服务端拒绝授予 VehicleBusinessReadiness 并等待人工处置的状态；该状态仍允许心跳、诊断和恢复协议通信。硬件反馈恢复有效本身不能解除该状态，仍须取得 HardwareRecoveryConfirmation 并由服务端明确授权。
_Avoid_: 断线、离线、自动换仓、自动补偿清空、带病接新业务

**HardwareRecoveryConfirmation（硬件恢复人工确认）**:
硬件反馈重新有效且实时状态可以核验后，由 R-11 设备/电气维护人员或被显式授予等效维护权限的人员，以个人身份明确确认故障已经处理、允许服务端评估恢复原操作的业务事实；普通生产操作员仅凭生产操作权限不得提交。确认必须审计确认人、时间、车辆、仓位和故障原因。它不能代替锁 DI、光幕、输出回读等物理证据；服务端只有同时取得有效物理证据和该确认，才可授权原仓位、原 LoadBatch、原 SlotOperationAttemptId 继续。
_Avoid_: 信号恢复即自动续行、人工覆盖无效传感器、普通生产操作员代确认、共享账号确认、换仓、创建新装货尝试

**VehicleConfigurationMaintenance（车辆配置维护态）**:
服务端为低频仓位布局或 IO 配置换版持久化的整车非业务状态；期间阻断新任务和移动，只有车载本地验证、完整能力对账和服务端明确重新投运均完成后才能退出。
_Avoid_: 逐仓在线配置审批、车辆离线、普通仓位禁用

**RecoveryHandshake（恢复握手）**:
车辆首次连接和重连共用的业务就绪流程：依次建立带代次的连接会话、同步完整车载能力、上报未结操作与恢复检查点、补报并确认积压结果，最后由服务端返回 READY 或 RECOVERY_REQUIRED。
_Avoid_: TCP 握手、首次连接快捷通道、重连后直接接业务

**ProtocolEnvelope（协议消息外壳）**:
车载—服务端每条 NDJSON 消息共用的固定结构，包含 protocolVersion、messageType、messageId、correlationId、agvId、sessionGeneration、sentAt 和 payload；业务字段只放在 payload 中。
_Avoid_: 每种消息自定义顶层元数据、裸 payload、用 slotOperationAttemptId 代替 messageId

**ProtocolVersion（车载通信协议版本）**:
ProtocolEnvelope 中标识完整通信契约的整数；第一版固定为 1。同版本只能增加接收方可忽略的可选字段，任何必填字段、字段语义或强制流程的破坏性变更都必须升级版本。
_Avoid_: 软件版本号、按消息独立版本、运行时猜测兼容

**MessageId（消息编号）**:
一条协议消息的稳定唯一编号，用于消息去重以及通过 correlationId 对应 ACK 或响应；同一消息的传输重试沿用原编号，新语义消息使用新编号。
_Avoid_: 仓位操作尝试编号、运输任务 ID、每次重发的新编号

**MessageDeliveryClass（消息交付类别）**:
每种 messageType 固定声明的传递语义：可靠业务/安全消息使用持久化接受 ACK，请求消息使用关联响应，遥测消息允许丢失，心跳确认只用于连接存活判断。
_Avoid_: 所有消息统一 ACK、由调用处临时决定是否重试、ACK 即执行完成

**DurableAcceptance（持久化接受）**:
接收方已将可靠消息及其去重依据写入可恢复存储后返回 ACK 的状态；它只证明接收责任已经转移，不证明消息要求的动作已经执行完成。
_Avoid_: 动作完成、界面已显示、仅写入内存队列

**VehicleCredential（车辆连接凭证）**:
分配给单台 AGV、用于向服务端证明其连接身份的独立凭证；必须与 `agvId` 匹配，不能由多车共享。
_Avoid_: agvId、IP 地址、全项目共用密码

**SlotPhysicalState（仓位物理状态）**:
车载上位机依据本车 IO 形成的仓门锁闭状态、开锁输出回读、光幕、通信有效性及执行阶段事实。
_Avoid_: 仓位状态（未区分业务含义）、服务端仓位状态

**仓门锁闭状态（SlotDoorLockState）**:
车载上位机依据锁传感器的有效反馈形成的仓门是否锁闭的物理事实；当前硬件没有独立的门关闭传感器，因此系统不把“门已关闭”作为另一项可观测状态。
_Avoid_: 独立仓门关闭状态、操作员目视确认、根据开锁输出反推门已锁闭

**开锁输出回读（UnlockOutputReadback）**:
车载上位机从 IO 模块读取的开锁 DO 实际状态；只有回读确认为复位（无效）时，才证明控制端没有继续施加开锁信号。
_Avoid_: 最后一次写入值、软件期望值、仅凭脉冲计时结束推断复位

**SlotOccupancyState（仓位占用状态）**:
车载上位机根据仓内光幕及其数据有效性归一化得到的 OCCUPIED、EMPTY 或 UNKNOWN；有效遮挡表示有货，有效无遮挡表示空仓，光幕故障或 IO 数据无效时必须为 UNKNOWN。
_Avoid_: 光幕原始 DI、操作员口头确认、业务仓位内容

**DetectableLoadConstraint（可检测产品约束）**:
允许放入仓位的花篮必须具有足以稳定遮挡仓内光幕的尺寸和放置姿态；过小或无法被光幕可靠检测的物品禁止进入本系统业务流程。
_Avoid_: 任意物品均可存放、以客户误用覆盖传感器判定、软件估算尺寸

**OneBasketPerSlot（一仓一篮）**:
每个物理仓位最多存放一个花篮，每个任务中的花篮必须各自分配一个目标仓位；子批号花篮数量必须等于 SlotOperationCommand.slots 数量。
_Avoid_: 一仓多篮、多个花篮共用一个光幕占用结论、花篮数与仓位数不一致

**AnonymousBasket（无身份花篮）**:
当前项目中没有独立身份 ID、不可逐个追踪的花篮；服务端只记录某物理仓位属于哪个 SUBLOT，并以占用仓位数量表达该子批号的花篮数量。
_Avoid_: 虚构花篮序号、仓位到花篮 ID 映射、逐篮追溯

**SlotBusinessState（仓位业务状态）**:
服务端维护的仓位分配、预留、所载 SUBLOT 及关联运输任务等业务事实；当前项目不包含单个花篮身份。
_Avoid_: 仓位状态（未区分物理含义）、光幕状态

**SlotStateMismatch（仓位状态不一致）**:
SlotPhysicalState 与 SlotBusinessState 无法相互印证的异常；解除前对相关新操作采用状态不明即阻断。
_Avoid_: 自动同步、以光幕覆盖业务、以数据库覆盖 IO

**DepartureSafe（离站安全许可）**:
车载上位机基于最新本车 IO 事实给出的仓位机构离站安全判定；它只是服务端请求车辆移动的必要前提，不是发车命令或持续有效的保证。
_Avoid_: 发车完成、操作成功、永久安全标志

**PreDepartureSafetyCheck（发车前安全核验）**:
服务端每次请求车辆移动前，向车载上位机取得的实时 DepartureSafe 判定及其检查标识、观测时间和安全状态版本；旧操作结果不能替代本次核验。
_Avoid_: OperationResult 快照、历史 departureSafe、永久发车许可

**DepartureSafetyRevoked（离站安全许可失效）**:
服务端请求车辆移动后，车载上位机发现 DepartureSafe 已由 true 变为 false 的高优先级安全事件；服务端收到后必须自动阻止或停止移动。
_Avoid_: 普通告警、仅提示人工、安全状态日志

**SafetyStateProjection（安全状态投影）**:
服务端根据车载端可靠发布的 SafetyStateChanged 保存的最新抽象安全视图，包含 DepartureSafe、安全状态版本、受影响物理仓位、原因码和观测时间；它用于阻断与诊断，但不是物理事实权威，也不能代替发车前实时核验。
_Avoid_: 原始 DI/DO 快照、IO 配置、永久发车许可

**SafetyStateSnapshot（安全状态快照）**:
车载端为恢复或版本缺口对账提供的当前完整抽象安全状态及 safetyStateVersion；它可以包含逐仓抽象安全结论，但不包含原始 DI/DO 或 IO 映射。
_Avoid_: SafetyStateChanged、原始 IO 快照、OperationResult

**SafetyStateUnknown（安全状态未知）**:
服务端发现 safetyStateVersion 未知、回退或不连续后进入的保护状态；完整 SafetyStateSnapshot 对账完成前阻断新仓位操作和移动，已在移动时按既有分级规则介入。
_Avoid_: 默认安全、普通告警、立即要求人工恢复

**StationOperationGuard（站点操作保护）**:
服务端从授权扫码或下发仓位操作开始，为指定 AGV 保持的移动调度阻断状态；直到车载端安全结束操作前，不允许产生新的移动指令。
_Avoid_: 发车前单次检查、界面锁定、车载任务锁

**MovementConnectionLossHold（行驶断链暂停）**:
车辆正在执行由本系统发起的移动任务时，服务端确认 VehicleConnectionSession 失效后，通过 RIoT OrderHold 请求并核验停车的保护动作；只有重连对账、重新完成 PreDepartureSafetyCheck 并取得服务端明确授权后，才可执行 OrderContinue。
_Avoid_: 急停、通信恢复即自动续行、允许车辆继续到站

**仓位操作尝试编号（SlotOperationAttemptId）**:
服务端为一次多仓装货或卸货物理尝试生成的稳定唯一编号，贯穿指令接受、逐仓或批量执行、结果补报、暂停续行和恢复对账；通信重发沿用原编号，终态后重新尝试使用新编号。
_Avoid_: OperationId、运输任务 ID、messageId、终态后重新执行仍用旧编号

**LoadBatch（装货批次）**:
一个任务、一个子批号及其 1～N 个花篮组成的业务原子单元，由一个仓位操作尝试编号按 OneBasketPerSlot 关联数量相等的完整目标仓位集合；只有所有产品全部装入并安全锁闭后才整体提交，不能以部分装入作为成功终态。
_Avoid_: 单个仓位装货、逐仓业务提交、多个子批号的混合操作

**Sublot（子批次）**:
装货时操作员在车载界面扫描或输入的 SUBLOT 字符串及其代表的业务子批次；不存在另一个 SublotId。车载端只提交该值并在活动操作的最小恢复记录中保留引用，服务端负责查询关联信息、校验站点与任务并维护完整生命周期。卸货不输入 Sublot，由服务端根据在车业务状态和当前站点识别。
_Avoid_: SublotId、SublotInput、总任务码、TaskCode、车载端解析任务

**ExpectedBasketCount（应装花篮数）**:
V1 中服务端根据 Sublot 的料盒数与任务冻结 PACKAGE 的已批准容量换算、并在 OperationCommitPoint 前冻结的权威花篮数量；操作员和车载端不得手工修改。无法唯一取得或换算时，本次装货在分配仓位和开锁前失败。
_Avoid_: 估算值、最低参考值、用户输入数量、车载光幕计数、目标仓位数反推业务数量

**SublotReservation（子批号占用）**:
服务端对一个 DemandId、SUBLOT、当前 AGV、OperationSession 和仓位操作尝试编号建立的全局唯一持久化绑定；同一 SUBLOT 同时只能属于一个未终结装卸操作，断线和重启不得自动释放。
_Avoid_: 车载本地锁、连接在线标记、查询后再写的临时判断

**ProvisionalLoadState（装货暂态）**:
服务端在 LoadBatch 执行期间保存的任务、子批号、完整仓位预留和逐仓物理进度；它用于恢复和补偿，不表示子批号已经正式存入。
_Avoid_: 正式入库、逐仓已入账、车载业务数据库

**部分装货中断（PartialLoadInactivity）**:
LoadBatch 只有部分目标仓位完成装货、其余目标仓位尚未完成时形成的未收敛等待；即使当前仓门均已锁闭且 DepartureSafe 暂时为 true，也不属于 StationDepartureWaiting。它沿用 StationDepartureWaitPolicy 的时长，每个目标仓位达到 `OCCUPIED + 锁闭 + 开锁输出已复位` 时从完整时长重新计算无进展期限；期限届满只告警，不自动提交、取消或离站，操作员只能继续完成整批装货，或清空整批并取消。
_Avoid_: 站点离站等待超时、部分装货成功、物理安全即允许离站

**装货批次提交闭环（LoadBatchCommitClosure）**:
一个 Sublot 的全部目标仓位均达到 `OCCUPIED + 锁闭 + 开锁输出已复位` 且安全状态有效时形成的自动整批提交边界；服务端不再等待操作员对该 LoadBatch 进行额外确认。
_Avoid_: LoadFinalConfirmation、逐仓业务提交、站点全部放货完成

**LoadCorrection（装货纠错）**:
StopClosureCommit 前，已核验操作员针对放错产品且已经锁闭的已装仓位发起、服务端在原仓位操作尝试编号下授权、车载端安全执行 `OCCUPIED→EMPTY→OCCUPIED` 原仓位更换并追加审计的恢复过程；它不撤销或改写已经形成的 LoadBatch 提交事实。纠错期间退出 StationDepartureWaiting 并停止离站倒计时，重新安全闭环后从完整时长开始。
_Avoid_: OperationCancel、LoadCompensationRecovery、撤销 LoadBatch 提交、整批清空

**LoadCorrectionPending（装货纠错待重放）**:
错误花篮已经从原仓位取出、但正确花篮尚未重新放入时的可恢复等待态；原任务、SUBLOT、目标仓位、提交事实和 StationOperationGuard 均保持，后续装货暂停，只能继续在原仓位重放或转为清空并取消。
_Avoid_: 纠错成功、部分装货成功、自动取消、恢复后跳过该仓位

**CurrentStopWorklist（当前停靠作业清单）**:
服务端向车载界面提供的当前停靠只读业务投影，包含本次停靠已排定的待装任务和车上目标为当前站点的待卸任务；车载端可以展示并提交操作请求，但不拥有任务事实。
_Avoid_: StationTaskProjection、仅待装任务列表、全局可准入任务列表、车载任务库

**CurrentStopWorklistSnapshot（当前停靠作业清单快照）**:
服务端针对当前 AGV 与站点生成的带 worklistRevision 完整作业投影；车辆到站、作业变化、任务取消、临时 SUBLOT 获准纳入或重连时整表下发，车载端只接受更新版本并整体替换显示。
_Avoid_: StationTaskListSnapshot、增量增删事件、车载端合并任务、无版本列表

**站点离站等待态（StationDepartureWaiting）**:
车辆位于服务端裁定可继续装货的当前站点，且没有必须完成的卸货、活动或未收敛的仓位操作，仓位机构满足 DepartureSafe，车载端处于 VehicleBusinessReadiness 且当前作业与后续计划投影均为最新时，可以等待操作员继续装货或结束本站的业务状态；它不等同于已经取得发车许可。纯卸货站完成本站卸货后直接结束停靠，不进入该状态；装卸混合站必须先完成卸货。
_Avoid_: DepartureSafe（仅物理必要条件）、作业已完成、可以自行开走

**站点离站等待超时（StationDepartureWaitTimeout）**:
服务端在车辆每次进入 StationDepartureWaiting 时掌握的完整等待期限，车载界面显示剩余时间；完成一个 LoadBatch、放弃尚未产生物理动作的装货或从其它操作重新进入该状态时均重新计满，不继承上一段剩余时间。期限届满后服务端结束本站，取消全部尚未开始的待装 DemandId；已经提交的 LoadBatch 不受影响，没有剩余待装任务时只结束停靠。当前站存在待卸任务或任何活动、未收敛仓位操作时不得触发超时离站；截止瞬间的装货开始与超时结束在服务端原子互斥，以先成功持久化者生效。车载端断联时本轮截止时间立即失效，恢复握手与最新投影对账完成并重新进入 StationDepartureWaiting 后从完整时长重新计时。倒计时期间新增待装 DemandId 时，服务端在车载端确认包含该任务的新版 CurrentStopWorklistSnapshot 后重新计满；任务删除、排序或普通状态刷新不重置。
_Avoid_: 收料超时（范围过窄）、卸货超时、操作中超时、强制跳站

**站点离站等待策略（StationDepartureWaitPolicy）**:
服务端维护的项目级等待时长、可选站点覆盖及站点是否允许继续装货的裁定；第一版项目默认值为 5 分钟，车载端只接收并显示服务端给出的本次截止时间，不保存或裁定业务配置。操作员不能暂停、延长或通过普通触屏、打开页面、身份核验和无效扫码重置期限，只有服务端先成功接受装货开始或纠错请求才退出本轮等待。
_Avoid_: 车载本地超时配置、每端独立倒计时、继续等待按钮、无业务结果的操作续时

**本站装货完成（CurrentStopLoadingComplete）**:
当前已通过装货身份核验的操作员确认当前站点不再继续等待其它 Sublot 的站点级结束意图；服务端重新校验操作会话并审计工号、站点、AGV、剩余取消任务数量和时间。它不参与任何单个 LoadBatch 的提交，也不替代装货批次提交闭环；若仍有尚未开始的待装 DemandId，车载端明确提示数量并经二次确认后，由服务端按与 StationDepartureWaitTimeout 相同的整站结束流程取消，没有剩余待装任务时直接结束停靠。
_Avoid_: LoadFinalConfirmation、单个 Sublot 完成、批次提交按钮

**PlannedStop（计划停靠项）**:
后续停靠计划中的一个业务站点及其顺序、停靠目的和任务摘要；它不表示 RIoT 导航使用的路径节点。
_Avoid_: 地图路径节点、转弯点、避障路径

**UpcomingStopPlan（后续停靠计划）**:
服务端为当前 AGV 排定、仍可由调度调整的后续业务停靠序列；车载界面用它说明接下来去哪些站点以及各站作业目的，不据此自行规划或编辑路线。
_Avoid_: RIoT 路线、固定不可变行程、车载端推导路线

**UpcomingStopPlanSnapshot（后续停靠计划快照）**:
服务端生成的带 planRevision 完整后续停靠投影；计划增删、换序或状态变化时整体替换，断线后最后版本只能作为明确标记过期的只读信息。
_Avoid_: 逐站增删事件、无版本计划、离线可执行路线

**OnboardVehicleOverview（车载车辆概览）**:
车载界面并列呈现运行、通信与业务就绪、当前作业、安全与联锁四个维度的组合视图；前三类使用相应权威投影，本车安全与联锁始终以车载实时 IO 事实为准。
_Avoid_: 单一车辆状态枚举、用业务状态覆盖安全状态、全部状态来自同一数据源

**StationTaskTypeAdmission（站点任务类型准入）**:
服务端维护的 stationId 与 taskType 多对多允许关系；存在 `(stationId, taskType)` 记录才允许在该站点输入对应任务的 SUBLOT，缺失、未知或未配置均默认拒绝。
_Avoid_: 按任务原站点判断、车载端白名单、同时维护两套正反向配置

**AdmissionDecisionSnapshot（准入决定快照）**:
服务端在 OperationCommitPoint 前按当前 StationTaskTypeAdmission 再次校验并冻结的 stationId、taskType、规则版本和允许结论；后续规则变更不撤销已经发出的仓位操作。
_Avoid_: 每个仓位执行前重新准入、配置变更中断当前操作、无版本审计

**AdmissionPolicyStore（准入策略存储）**:
服务端数据库中的 StationTaskTypeAdmission 当前关系、单调 admissionPolicyVersion 和变更审计；第一版由软件人员通过受控部署脚本或原子导入维护，不提供运行时配置界面。
_Avoid_: 车载配置文件、手工无审计改库、双端各存一份

**LoadTaskCancellation（装货任务取消）**:
车辆离站前由已核验操作员针对一个 DemandId 发起的任务终止流程；未产生物理装载时可直接终结，已经部分或全部装载时，对该任务实时确认为 OCCUPIED 的目标仓位执行批量开锁并全部清空，最终使该任务完整目标仓位范围均达到 EMPTY、由锁传感器确认锁闭且开锁输出回读确认为复位。其它 SUBLOT 的仓位、任务与确认记录不受影响；但同车另一 SUBLOT 尚处于物理装货或清空过程中时不得穿插本次取消，必须等待其完成或取消到稳定边界。服务端可靠接受 ALL_EMPTY 并发布新版作业清单后，释放仓位可以用于新的 SUBLOT。获得服务端取消授权时尚未锁闭的当前装货仓位可以直接取出并以 EMPTY 安全收尾；正式提交后发起取消属于保留原确认与提交事实的补偿，不是撤销或抹除历史。
_Avoid_: 瞬间撤回 SlotOperationCommand、只清空所选任务的部分仓位、取消一个 SUBLOT 时整车清空、车辆离站后的普通取消

**整站结束取消（StopClosureCancellation）**:
StationDepartureWaiting 中结束本站时，由服务端一次性终结全部尚未开始的待装 DemandId；等待到期记为 `CANCELLED_BY_STATION_TIMEOUT`，操作员确认本站装货完成记为 `CANCELLED_BY_STOP_COMPLETE`。两者均持久抑制对应 TransportDemandKey 再次接入且不影响已经提交的 LoadBatch；同一 SUBLOT 以后命中其它 WorkType 时属于不同业务键。
_Avoid_: CANCELLED_BY_OPERATOR、LoadTaskCancellation、清空已装仓位、按 SUBLOT 永久拉黑

**整站结束提交（StopClosureCommit）**:
服务端将当前停靠终结、全部剩余待装 DemandId 的取消终态与审计作为不可分割的业务边界；任一部分不能成立时本站保持未结束。提交时立即结束 OperationSession 并清除 OnboardOperatorContext；随后须让车载端采用最新作业清单与后续计划并重新通过 PreDepartureSafetyCheck 才能请求移动，移动下发失败不撤销已经提交的整站结束，也不重新开放本站操作。
_Avoid_: 点击即发车、逐任务部分取消后离站、移动失败后复活任务

**整站结束后去向（PostStopClosureRouting）**:
本站结束后有下一 PlannedStop 时前往该站；无下一站且车辆空载时进入既有停车点分配流程，无可用停车点则原地排队。无下一站但仍载有已提交 Sublot 属于调度计划异常，车辆原地保持并报警，不自动前往停车点。
_Avoid_: 无下一站一律停车、载货原地静默等待、车载端自行选站

**LoadCancelPending（装货取消待清空）**:
已接受装货取消请求但目标仓位尚未全部确认 EMPTY 的服务端状态；期间 SUBLOT 与仓位占用、StationOperationGuard 均保持，车辆不得离站。
_Avoid_: 已取消、可释放仓位、仅显示提醒

**LoadCancellationAuthorization（装货取消授权）**:
服务端对 LoadCancellationStartRequested 的关联响应，结果为 AUTHORIZED 或 REJECTED；AUTHORIZED 只允许车载端进入该 DemandId 的清空流程，物理清空范围与完成判定仍由车载执行日志和实时 IO 决定。
_Avoid_: DIRECT_CANCEL/CLEAR_REQUIRED、服务端逐仓指挥、点击即业务取消

**UnloadBatch（卸货批次）**:
一次到站时服务端识别出的本站全部可卸仓位组成的批量物理操作，可包含多个 Sublot，由一个仓位操作尝试编号关联目标集合并采用批量开锁。其业务提交粒度受卸货 Sublot 完整性策略控制；8005 项目关闭该策略，因此逐仓达到物理完成条件后即可独立清空该仓位业务状态。
_Avoid_: 必然等同于单个 Sublot、必然整批业务原子、要求操作员输入 Sublot

**ProvisionalUnloadState（卸货暂态）**:
服务端在启用卸货 Sublot 完整性策略的项目中保存的逐仓取出进度；8005 项目关闭该策略，不使用它延迟已完成仓位的业务清空。
_Avoid_: 8005 默认卸货状态、要求把已取出产品放回

**OperationCommitPoint（仓位操作承诺点）**:
服务端首次发出仓位操作指令的不可撤回边界；SUBLOT、站点、AdmissionDecisionSnapshot、业务有效性、花篮数量、仓位清单和预留必须在此之前确认。
_Avoid_: 车载端接受 ACK、第一扇门打开、装入第一件产品

**ProvenRecoveryCheckpoint（可证明恢复点）**:
OnboardExecutionJournal 记录的执行阶段能够与重启后的实时 IO 和服务端操作事实相互印证的位置；只有从该位置才允许恢复原操作。
_Avoid_: 内存中的最后一步、从头重试、仅凭数据库推断

**OperatorVerificationPolicy（操作员核验策略）**:
项目级统一、分别决定装货与卸货前是否必须核验操作员身份的策略；8005 项目装货启用、卸货关闭，不允许按 AGV、站点或单次操作临时切换。
_Avoid_: 单一装卸开关、车载本地开关、按车辆绕过、现场临时选择

**卸货 Sublot 完整性策略（UnloadSublotIntegrityPolicy）**:
项目级统一决定卸货业务状态是否按 Sublot 整体提交的策略；8005 项目关闭，因此本站全部可卸仓位可以跨 Sublot 批量开锁，并在每仓达到 `EMPTY + 锁闭 + 开锁输出已复位` 后独立清空业务状态。策略不能按站点或单次卸货临时切换。
_Avoid_: 操作员临时选择、批量开锁必然整批提交、装货完整性策略

**OperationSession（操作会话）**:
服务端为一次到站建立的现场操作上下文，关联 AGV、站点、项目策略和审计，可连续处理多个 Sublot。需要身份核验时，每个 Sublot 在首次开锁前绑定当时已核验工号，同一 Sublot 内不得更换；一个 Sublot 经服务端确认完成后可以核验并切换工号。掉线和重启保留当前绑定，不重复验证。
_Avoid_: 管理端登录会话、车载登录、班次会话

**车载操作员上下文（OnboardOperatorContext）**:
车载上位机持久化的当前已核验工号及核验引用；新装货 Sublot 默认沿用，用户只可在没有活动或待服务端确认的 Sublot 时主动更换且新工号必须重新经服务端校验。掉线、重启不清除；服务端提交 StopClosureCommit 后清除，不等待车辆实际开始移动。卸货身份核验策略关闭时不要求也不虚构操作员。
_Avoid_: 每个仓位重新输入、掉线自动清除、同一 Sublot 中途换人

### 可追溯性

**OnboardTechnicalLog（车载技术日志）**:
车载上位机保存的 IO 通信、信号变化、安全判断、执行阶段、配置和本地异常证据。
_Avoid_: 服务端业务审计、每轮 IO 数据全量上送

**BusinessAuditRecord（业务审计记录）**:
服务端保存的人员、会话、仓位业务、上下层命令结果、调度动作和异常处置记录。
_Avoid_: 车载原始 IO 日志、普通界面进度

**LoadCompensationDecision（装货整批清空决定）**:
LoadBatch 因关键硬件故障暂停后，由 R-09 班组长或被显式授予等效生产管理权限的人员在提交前完成即时二次认证、选择 LoadCompensationReasonCode 后作出的“不再继续原装货、改为整批清空”的生产业务决定；R-09 可在当前生产操作员界面完成审批，但其决策身份独立记录，不替换 Sublot 绑定的生产操作员或接管 OperationSession。已有登录会话、R-11 的 HardwareRecoveryConfirmation 和普通生产操作员的清空申请均不能代替该决定；同一人兼任维护和生产管理角色时，只有同时具备两项独立权限才能分别完成两项动作。
_Avoid_: 无原因决定、自由文本代替原因码、审批即换人、审批即接管会话、仅凭已有会话确认、HardwareRecoveryConfirmation、普通离站前清空并取消、设备维护人员自动决定、普通生产操作员单独决定

**LoadCompensationDecisionAuthProof（装货整批清空决定认证证据）**:
R-09 为一次具体 LoadCompensationDecision 即时二次认证形成的单次证据，绑定确认人、DemandId、SlotOperationAttemptId 和决定内容；相同消息重发只能取得该次提交的已有结果，不能授权另一决定或在业务校验失败后再次提交。
_Avoid_: 可复用时间窗口、已有登录会话、跨任务审批令牌、失败后继续使用

**LoadCompensationReasonCode（装货整批清空原因码）**:
LoadCompensationDecision 的首版受控原因枚举：`HARDWARE_NOT_RECOVERABLE_ON_SITE` 表示现场无法恢复故障车辆并继续原装货，`PRODUCTION_ABORTS_CURRENT_LOAD` 表示生产决定不再继续本次装货，`OTHER` 表示其它原因且必须填写非空备注。原因码只解释为何清空，不改变补偿完成后终结原搬运需求的统一后果。
_Avoid_: 硬件故障点位码、自由文本原因、空原因、未知原因码

**LoadCompensationRecovery（装货补偿恢复）**:
LoadBatch 暂停后，取得 LoadCompensationDecision 和服务端授权，人工才取出该任务已经放入以及状态不确定的全部产品；全部相关仓位安全证明为空后，服务端释放整批预留并将原搬运需求终结为 `CANCELLED_BY_LOAD_COMPENSATION`，不再为该 DemandId 自动派车。
_Avoid_: 硬件故障自动触发、消息直接取消、逐仓部分入账、只取出失败仓产品

**LoadCompensationRequired（装货待补偿）**:
服务端取得有效 LoadCompensationDecision 后为暂停的 LoadBatch 保持的业务状态；它不是任一硬件故障的自动结果，必须等待后续明确授权并完成 LoadCompensationRecovery。
_Avoid_: 硬件故障自动转入、操作已取消、自动重新开门、允许车辆离站

**LoadCompensationCommand（装货补偿指令）**:
服务端在核验原操作确实处于 LoadCompensationRequired 后，使用原仓位操作尝试编号下发可靠恢复指令；它授权车载端按执行日志逐仓引导人工清空，不是通用 OperationCancelCommand。
_Avoid_: 新装货操作、离线清空、数据库回滚

**UnloadCompletionRequired（卸货必须完成）**:
卸货操作一旦开始便不存在取消分支；异常只能暂停、排障并继续，直至所有目标仓位完成取空和锁门。
_Avoid_: 部分卸货后取消、把产品放回后回滚

### 鉴权

**CallApiKey**:
RIoT 网页「调用密钥设置」中的长期密钥，作为业务接口默认的 Bearer 凭证。
_Avoid_: API key（泛称）、网页密钥（口语）、静态 token（易与登录短时 token 混淆）

**AccessToken**:
经 `admin/login`（或 refresh）取得的短时访问凭证；第一版中仅作备用鉴权路径。
_Avoid_: token（单独使用时歧义）、Bearer（指头格式而非凭证种类）

**AdminLogin**:
用用户名密码换取 AccessToken 的备用鉴权方式；登录成败不能只看 HTTP 状态。
_Avoid_: 登录（单独使用时歧义）、鉴权（上位概念）

### 消费边界与入口

**DispatchLoop**:
MES/调度侧完成一次派车所需的最小闭环：鉴权、发现可调度车与地图站点、建单、观察终态、必要时取消或中断。
_Avoid_: 全量 RIoT API、实验探针集

**DispatchableVehicle**:
可通过 task 侧车辆清单发现、用于 appointVehicleKey 的车；不是 devices 列表中的门/电梯等非车设备。
_Avoid_: Device（泛称）、可调度设备

**Session**:
指向单一 RIoT 实例的共享会话；第一版推荐的唯一稳定入口，其下挂载具名 Facade 方法。
_Avoid_: 客户端（泛称）、连接、Generated 客户端

**RawEscape**:
经 Session 暴露的未封装 Kiota 调用面；仅作临时逃逸，不属于稳定契约。
_Avoid_: 正式 API、稳定 Facade

### 地图与站点

**Map**:
RIoT 中一张可调度地图；业务上用 `mapId` 标识，可读名为地图 `name`。
_Avoid_: 图层、楼层图（除非特指 floor 字段）

**Station**:
某张 Map 上的站点；必须与 `mapId` 成对使用，站点 `id` 跨图不保证唯一。
_Avoid_: 点位（泛称）、目的地（业务语义更宽）

**NearStationQuery**:
在候选 Station 集合中，按路径代价选出最近的起点或终点 Station（对应 RIoT `queryNearestStart` / `queryNearEnd`）；返回的是 stationId，不是折线几何。
_Avoid_: 最短路径（易被理解成几何 path）、路径规划结果

**RouteCost**:
指定 Map 上某车到某 Station 的路径代价（mm）；非负且可读为可达，`-1` 表示不可达（含车不在该图等）。建单前可达判断依据此值，不能只看建单业务成功码。
_Avoid_: 距离（易被理解成直线距离）、最短路径几何

### 订单与车辆控制

**OrderRef**:
`byDefaultMissions` 建单成功后返回的订单标识：数值 `id`、字符串 `orderId`、调用方 `upperId`，以及当时的 `orderState`。后续查单/取消/命令按对应标识选用。
_Avoid_: Order（泛称）、任务号（口语）

**DispatchEnable**:
把车纳入调度可接单（对应现场 enable / 上线路径）；与设备通电不是同一概念。
_Avoid_: 开机、上线（易与网络在线混淆）、enable（裸字段名）

**DispatchDisable**:
把车移出调度接单（对应现场 disable / 下线路径）；不自动等同于取消执行中订单。
_Avoid_: 关机、下线（易与断网混淆）、disable（裸字段名）

**EmergencyStop**:
车辆急停态及软件触发/解除；是否恢复以车侧急停态为准，不以单次 HTTP 成功为唯一依据。
_Avoid_: 暂停（与 HELD 不同）、中断（与 interrupt 不同）

**OrderHold**:
将移动单置于 HELD（暂停执行）的控制；与 EmergencyStop、interrupt 不同。
_Avoid_: 暂停（泛称）、急停

**OrderContinue**:
从 HELD 恢复继续执行（CONTINUE_FROM_HELD）。
_Avoid_: 恢复（泛称，易与急停解除混淆）、resume（裸英文）、HangContinue

**HangContinue**:
从 OrderHang 尝试拉回 EXECUTING（CONTINUE_FROM_HANG）；与 OrderContinue 命令不同，不可混用。接口成功码不等于订单已离开 HANG。
_Avoid_: OrderContinue、resume（泛称）

**PriorityExec**:
将队列中指定订单提升为优先执行，而不必先清空同车其它队列单。
_Avoid_: 插队（口语）、优先级字段（建单时的 priority 语义不同）

**BusinessFailure**:
RIoT 在 HTTP 已成功（或可判定）的前提下，用业务 `code` 表达的失败；具名 Facade 将其表现为统一异常，而不是留给调用方拆包。
_Avoid_: HTTP 错误（传输层）、不可达（RouteCost=-1，属领域结果）

**ArrivalAtStation**:
车辆已到达目的 Station 的车侧可观测信号；在成功移动单上往往早于订单 SUCCESS。
_Avoid_: 订单完成、可再派

**ReadyForNextOrder**:
可以安全下发下一单的条件：订单已 SUCCESS 且车辆已 IDLE；不等于 ArrivalAtStation。
_Avoid_: 到站即可派、AWAITING_ORDER（单独作为充分条件）

### 异常滞留与 MES 策略

**PausedZeroDrop**:
某个任务类型在已有健康非零基线后突然降为零时进入的保护状态；保护期间暂停该类型需求的消失计数与 GONE 判定，直到连续健康非零轮次达到恢复条件。进入与解除都须保留为可追溯事件。
_Avoid_: 零任务、暂停（泛称）、PAUSED_ZERO_DROP 告警（仅指进入事件时）

**QueueingStall**:
订单已创建成功但长期停留在 QUEUEING、通常迟迟不进入 EXECUTING 的滞留；RIoT 不会因此自动变为 FAILED。常见诱因包括不可达、假车 key、车未纳入调度等；解脱策略属 MES 编排。
_Avoid_: 挂起（泛称）、OrderHang、HELD、急停

**OrderHang**:
订单 `orderState=HANG` 的滞留；与 QueueingStall、HELD、急停冻结（可仍为 EXECUTING）都不同。充电失败与普通 HANG 策略分离：普通分支可按原因尝试 HangContinue；充电分支不以 HangContinue 为默认。HangContinue 接口成功码不等于订单已离开 HANG。
_Avoid_: 挂起（泛称）、QUEUEING 滞留、HELD、急停

**ChargeHangReassign**:
充电失败 OrderHang 后，由 MES 自动改派前往其它充电桩再充的策略；改派前须 CANCEL 旧 HANG；选桩在配置允许的充电站集合内做 NearStationQuery（排除失败站）。
_Avoid_: HangContinue、人工改充（若未采用）

### MES 焊线工序与运输任务

**MesTaskUnionRound（MES 联合查询轮次）**:
对六类运输候选执行一次 MES_TASK_UNION Oracle 语句所得的完整轮次；六个 UNION ALL 分支共享同一语句级一致性快照，结构完整但字段值异常的原始行仍属于 SUCCESS 证据，只有执行或结构契约不能成立的 FAILURE / INCOMPLETE 才保持 Demand 投影不变。
_Avoid_: 六次独立查询、成功的部分快照、调用方自行声明 snapshotComplete

**MesIngest**:
MES 任务接入：轮询只读 MES 快照、对账并投影 TransportDemand；GONE 后同一业务键再现时可以产生新的本地投影实例。它不读取调度侧取消抑制，也不决定是否创建业务任务或派车。
_Avoid_: MES 模块（泛称）、任务服务（易含调度）、调度取消过滤器、薄模块（口语）

**MesIngestWatch**:
面向现场实施与运维工程师的只读 MES 接入运维台，用于判断接入健康、核验 TransportDemand、分析 IngestAlert 与 MES→MesIngest 链路延迟；它不拥有投影真相，也不执行调度或生产操作命令。
_Avoid_: 生产操作 HMI、调度台、TransportDemand 编辑器、只看列表的盯盘页

**PollTrace（轮询追踪）**:
一次 MesIngest 轮询从读取 MES_TASK_UNION 到本地处理结束的不可重复因果记录；无论结果为 SUCCESS、FAILURE 或 INCOMPLETE，都以稳定标识、查询版本、规范化内容摘要和行数证据关联该轮各阶段，但不包含后来发起的 Watch 查询。
_Avoid_: WatchRefreshTrace、把时间相近的 Watch 请求当作同一 trace

**WatchRefreshTrace（Watch 刷新追踪）**:
一次 MesIngestWatch 页面刷新从触发到页面呈现的因果记录；以稳定标识关联该次刷新的只读请求与客户端阶段，并显式引用其读取到的 PollTrace。
_Avoid_: PollTrace、每个 HTTP 请求各自冒充完整页面刷新

**WatchTelemetryIngest（Watch 遥测接入）**:
Watch 向 Host 追加刷新追踪证据的受限观测通道；它不创建或修改 TransportDemand、IngestAlert、PollHealth 或其它业务投影，因此不改变 MesIngestWatch 的业务只读边界。
_Avoid_: 业务写 API、任意日志上传、TransportDemand 回写

**ProjectionVisibilityLag（投影可见滞后）**:
Watch 将某轮已提交投影呈现给操作员所经历的时间，按同一 PollTrace 的投影提交时间到页面呈现时间计算；无法关联 PollTrace 或跨机时钟校准误差超限时为未知。
_Avoid_: MES `DATES` 值、把时间接近推断为同一轮投影

**PerformanceState（性能状态）**:
由有足够样本的链路耗时统计经阈值和迟滞规则得出的 `HEALTHY`、`DEGRADED`、`CRITICAL` 或 `INSUFFICIENT_DATA` 状态；它解释系统性能趋势，不是 IngestAlert，也不替代即时故障状态。
_Avoid_: IngestAlert、PollHealth、单次最大耗时直接判红

**IngestAlert**:
MesIngestWatch 面向运维查询展示的当前异常投影；它可以来自 DemandSeriesCurrentCondition、PollRunFailure 或 TaskTypeProtection，但不是拥有独立生命周期的领域实体。
_Avoid_: DemandSeriesIssue、Issue SeriesKey、每轮告警消息、WatchConnectionEvent、横幅

**DemandSeries**:
以 TransportDemandKey（SUBLOT + WorkType）标识的一条 MES 搬运候选完整生命周期；只记录该 SUBLOT 在这一工序类型内的变化，第一次在本地 Poll 中观察到该复合键时开始，连续 GONE 满 12 小时后归档。
_Avoid_: TransportDemand、告警实例、同键归档后新建的 Series

**DemandSeriesEvent**:
DemandSeries 生命周期中已经发生的不可变事实；只在首次发生、事实变化、条件消失或状态转换时记录，不把每轮相同观测重复写成事件。
_Avoid_: DemandSeriesIssue、可变告警状态、每轮 MES 快照行

**DemandSeriesCurrentCondition**:
根据 DemandSeriesEvent 推导出的当前异常视图，用于回答某个 Series 现在存在哪些异常；它不是独立领域事实，也不拥有 Issue ID、Issue SeriesKey 或 Revision。
_Avoid_: DemandSeriesIssue、事件历史、告警聚合根

**SeriesErrorCatalog（Series 错误目录）**:
由 MesIngest 领域契约拥有并随 Host/API 版本发布的全部 SeriesErrorCode 定义；它规定稳定含义、唯一主分类、固定严重度和展示文案，Watch 只能读取而不能另建本地目录。
_Avoid_: Watch 错误白名单、数据库可编辑分类、运行时自定义错误码

**SeriesErrorCode（Series 错误码）**:
Series 错误规则的稳定机器标识；发布后不得换义或复用，每个代码恰好属于一个 SeriesErrorCategory，具体字段或关联对象由错误主体区分。
_Avoid_: IngestAlert code、用户可编辑名称、每个字段值一个新错误码

**RequiredMesFieldMissing（MES 必填字段缺失）**:
错误码 `REQUIRED_MES_FIELD_MISSING` 表示当前 Demand 世代的必填 MES 字段没有值，主体为 `AREA`、`EQP`、`STEP`、`DATES` 或 `PACKAGE`，主分类为 `DATA_COMPLETENESS`。
_Avoid_: FIELD_DRIFT、每个字段各建一个错误码、用旧值填充 NULL

**InvalidMesFieldFormat（MES 字段格式无效）**:
错误码 `INVALID_MES_FIELD_FORMAT` 表示当前 Demand 世代的字段值存在但不符合领域格式，第一版主体仅为 `AREA`，主分类为 `DATA_FORMAT`。
_Avoid_: FIELD_DRIFT、AREA 自动规范化、字段缺失

**DuplicateTransportDemandKeyError（重复运输需求键错误）**:
错误码 `DUPLICATE_TRANSPORT_DEMAND_KEY` 表示当前 Demand 世代存在 DuplicateTransportDemandKeyObservation，主体引用该 DemandId，主分类为 `OBSERVATION_CONFLICT`。
_Avoid_: DUPLICATE_RECONCILE_KEY、为每条重复原始行分别建期间

**SublotMultipleWorkTypesError（子批次多工序类型错误）**:
错误码 `SUBLOT_MULTIPLE_WORK_TYPES` 在每个受影响 DemandSeries 的当前 Demand 世代分别形成，SubjectKind 为 `WORK_TYPE_MEMBERSHIP`，同轮涉及的全部 WorkType 作为可变化证据，主分类为 `OBSERVATION_CONFLICT`。
_Avoid_: 跨 Series 共享错误期间、只记录一个 WorkType、合并 DemandSeries

**LongGoneButVisibleError（长期消失后仍可见错误）**:
错误码 `LONG_GONE_BUT_VISIBLE` 表示 Series 归档后又观察到 TransportDemandKey，Target 为所属 Series、SubjectKind 为 `ARCHIVED_SERIES_VISIBILITY`，异常 DemandId 只作证据，主分类为 `LIFECYCLE_CONFLICT`。
_Avoid_: REAPPEAR_AFTER_GONE、归档恢复、每个异常 Demand 世代强制重开期间

**SeriesErrorCategory（Series 错误主分类）**:
SeriesErrorCatalog 中用于导航、互斥计数和分页的稳定分类；第一版分为 `DATA_COMPLETENESS`、`DATA_FORMAT`、`OBSERVATION_CONFLICT`、`LIFECYCLE_CONFLICT`，每个 SeriesErrorCode 只有一个主分类。
_Avoid_: 错误标签、多分类归属、Watch 本地分组

**DemandSeriesErrorPeriod（需求系列错误期间）**:
由 `SeriesId + SeriesErrorCode + Target + SubjectKind` 标识的可唯一归属错误从出现或复发到消失的连续期间；相同身份持续存在时，错误值或关联对象集合变化只追加证据而不切断期间，条件消失即关闭，后来再现必须新开。
_Avoid_: 每轮错误、IngestAlert incident、全局轮询故障、无法归属 Series 的任务类型保护

**SeriesErrorPeriodEndReason（Series 错误期间结束原因）**:
完整成功 MesTaskUnionRound 提供明确反证后记录的 `CONDITION_CLEARED` 或 `DEMAND_GONE`；轮询失败、不完整、Host 断联和 Watch 刷新失败都不能结束错误期间。
_Avoid_: 未再收到即恢复、连接失败即关闭、把 Demand 消失写成数据修复

**SeriesErrorPeriodEvidence（Series 错误期间证据）**:
错误期间的开启、诊断值或关联对象变化、涉及 Demand 世代、PollTrace 引用以及结束事实；相同内容持续存在不按轮询重复记录，也不以 OccurrenceCount 代替历史事实。
_Avoid_: 每轮重复事件、IngestAlert OccurrenceCount、只保留最后一条消息

**SeriesErrorBootstrap（Series 错误初始建立）**:
新错误模型部署后的首个完整成功 MesTaskUnionRound 将当时存在的错误以该轮时间开启，并标记 `BOOTSTRAPPED_CURRENT_CONDITION`；不转换旧 IngestAlert 历史，也不推测部署前开始时间。
_Avoid_: 从旧 incident 猜测期间、失败轮次完成 bootstrap、回扫制造历史错误

**SeriesErrorScope（Series 错误作用域）**:
错误期间的目标边界：Demand 世代级使用 `DEMAND:<DemandId>`，不得跨 DemandId 延续；Series 级使用 `SERIES:<SeriesId>`，可以跨世代持续但须保留逐世代证据。
_Avoid_: UI 分组、错误分类、把新 Demand 世代并入旧的 Demand 级期间

**SeriesErrorSubject（Series 错误主体）**:
错误规则作用的稳定对象种类，例如 `AREA`、`PACKAGE`、`RAW_OBSERVATION_SET`、`WORK_TYPE_MEMBERSHIP` 或 `ARCHIVED_SERIES_VISIBILITY`；实际错误值和关联对象集合只属于证据，不进入身份键。
_Avoid_: 为每个 MES 字段复制规则码、把错误值或 WorkType 集合放入身份键、展示文案

**SeriesErrorEvidenceTime（Series 错误证据时间）**:
Host 在产生错误事实的完整 MesTaskUnionRound 中记录的 UTC 时间；它决定错误期间边界和历史查询，不使用 MesSourceDate。
_Avoid_: MES `DATES`、Watch 本机接收时间、无 offset 的本地时间

**ErrorSearchMatch（错误检索命中）**:
DemandSeriesErrorPeriod 与所选错误条件及 UTC 半开查询区间 `[from, to)` 存在交集时形成的一次检索命中；结果以 DemandSeries 去重，详情保留跨 Demand 世代的全部命中证据。
_Avoid_: 只查窗口内首次发生、按 LastSeenAt 过滤、每个 DemandId 单独作为列表结果

**ErrorSearchActivityState（错误检索活动状态）**:
相对当前错误筛选条件在查询时刻汇总的 `ACTIVE` 或 `ENDED`：存在任一匹配的活动 DemandSeriesErrorPeriod 时为 `ACTIVE`，只有已经结束的历史命中时为 `ENDED`；详情以 SeriesErrorPeriodEndReason 区分条件恢复与 Demand 消失。
_Avoid_: RECOVERED、Series 全局健康状态、时间窗结束时状态、把 Demand 消失称为修复

**ErrorSearchAsOf（错误检索查询时点）**:
Host 在错误检索首个分页请求开始时冻结并由后续游标沿用的 UTC 时点；未显式给出 `to` 时它也是查询区间的排他上界，并用于判定匹配条件的当前活动状态。
_Avoid_: 每页重新取当前时间、Watch 客户端时间、时间窗结束时的历史回放状态

**ErrorSearchSnapshot（错误检索历史快照）**:
按同一 ErrorSearchAsOf 从 DemandSeriesEvent 重建的列表、分面数量、活动状态和证据详情一致视图；该时点之后的新开、变化或关闭只在刷新后的新快照中出现。
_Avoid_: 当前投影拼接、翻页时混入新事件、列表与详情使用不同 asOf

**ErrorSearchTimeInterval（错误检索时间区间）**:
错误期间和查询窗口都使用 UTC 半开区间 `[start, end)`；边界相接不算重叠，活动期间在快照内以 ErrorSearchAsOf 为临时排他上界，全部历史表示无下界至 asOf。
_Avoid_: 双端包含、自动交换 from/to、把显式 to 静默截断到 asOf

**ErrorSearchDefaultWindow（错误检索默认窗口）**:
错误检索默认查看截至 ErrorSearchAsOf 的最近 7 天，并提供最近 24 小时、7 天、30 天和全部历史；全部历史仍由 Host 有界分页。
_Avoid_: 默认全部历史、Watch 下载后本地分页、沿用 IngestAlert LastSeenAt 窗口

**ErrorSearchRollingWindow（错误检索滚动窗口）**:
最近 24 小时、7 天和 30 天分别表示以 ErrorSearchAsOf 为终点的精确 `24`、`7×24`、`30×24` 小时；显示可转换为带时区标识的用户本地时间，但不按本地自然日或午夜取整。
_Avoid_: 今天、本周、本月、无时区日期输入、本地零点边界

**ErrorSearchDefaultState（错误检索默认状态）**:
错误检索默认同时包含 `ACTIVE` 与 `ENDED`；概览等入口若只表达当前错误，必须显式携带 `ACTIVE` 条件。
_Avoid_: 默认只看活动、依赖页面隐含默认值表达当前错误

**SeriesErrorCodeEvolution（Series 错误码演进）**:
SeriesErrorCatalog 可以新增代码或将旧码标为 deprecated，但不得改变已发布代码的含义、主分类、作用域或严重度；新规则只从部署生效时产生事实，不回扫并重写旧历史。
_Avoid_: 物理删除旧码、复用代码、静默重分类、部署后追溯制造历史错误

**SeriesErrorSeverity（Series 错误严重度）**:
SeriesErrorCatalog 为每个代码固定的历史解释属性；第一版五个代码均为 `ERROR`，DTO 保留该值但错误检索页不显示只有单值的严重度筛选或分面。
_Avoid_: IngestAlert severity、期间动态升降级、单值筛选控件

**ErrorSearchAreaScope（错误检索 AREA 范围）**:
错误检索不受当前 AreaFilterProfile 静默影响；未来若增加 AREA 条件，必须是页面上的显式筛选并能单独选择 `UNKNOWN` 与 `INVALID`。
_Avoid_: 共享当前 AREA 配置、因 AREA 缺失或非法而隐藏错误、Dispatch AREA 范围

**ErrorSearchFilter（错误检索条件）**:
分类、错误码、活动状态、时间和标识等不同维度之间取交集，同一维度多值取并集，空选择表示不限；错误码隐含唯一主分类，不接受互相矛盾的分类与错误码组合。
_Avoid_: 空字符串作为真实值、Series 全局健康状态、矛盾条件静默返回空集

**ErrorSearchIdentifierMatch（错误检索标识匹配）**:
SeriesId、DemandId 和 SeriesErrorCode 去除首尾空白后按不区分大小写精确匹配，SUBLOT 去除首尾空白后按不区分大小写包含匹配；DemandId 命中任一世代时返回所属 Series，但只标记满足全部条件的错误证据。
_Avoid_: 正则、通配符、模糊纠错、把所属 Series 的全部证据冒充命中

**ErrorSearchResultOrder（错误检索结果顺序）**:
Host 在完成筛选、DemandSeries 去重和汇总后，依次按匹配范围内 `ACTIVE` 优先、最近匹配证据时间降序、SeriesId 升序稳定排序，再使用绑定完整规范化筛选、顺序和 ErrorSearchAsOf 的 keyset 游标分页。
_Avoid_: Watch 本地去重、分页后过滤、AlertId tie-break、跨筛选复用游标

**ErrorSearchPage（错误检索结果页）**:
ErrorSearchSnapshot 中默认 100、最多 200 个按固定 ErrorSearchResultOrder 排列的 DemandSeries，并返回精确 totalSeriesCount；第一版不开放任意列排序。
_Avoid_: 估算总数、错误期间总数、客户端分页、任意排序

**ErrorSearchCursor（错误检索游标）**:
绑定完整规范化筛选、固定顺序、ErrorSearchAsOf 和契约版本的 keyset 位置；无效、篡改或不匹配时 Host 返回 `INVALID_ERROR_SEARCH_CURSOR`，Watch 保留旧结果并提示失败，不自动冒充第一页。
_Avoid_: 跨筛选复用、静默重解释、翻页失败自动刷新第一页

**ErrorSearchFacetCount（错误检索分面数量）**:
排除自身维度后计算的去重 DemandSeries 数：分类数量应用时间、状态与标识条件，状态数量应用时间、分类/错误码与标识条件；错误码的主分类互斥，但 Series 可命中多类，因此全部数量不等于分类数量之和。
_Avoid_: 错误期间数、证据数、分类数量机械相加、受自身选择压缩的 facet

**ErrorSearchEvidenceDetail（错误检索证据详情）**:
所选 Series 中只展示满足当前分类、错误码和时间窗的错误期间及证据，并标明与窗口重叠但边界位于窗口外的期间；完整世代与全部事件通过需求系列页查看。
_Avoid_: 偷偷混入未命中错误、在错误页复制完整 Series 历史、裁掉窗口外的期间边界

**ErrorSearchResultSummary（错误检索结果摘要）**:
结果行显示 SeriesId、SUBLOT、WorkType、活动或已结束状态、匹配错误码与主分类、最近匹配证据时间、命中期间数、Demand 世代数以及当前或最后可信 MesArea；无可信 AREA 时明确显示未知或无效。
_Avoid_: 长错误消息、把未知 AREA 留空、Series 全局健康摘要

**ErrorSearchDiagnosticEvidence（错误检索诊断证据）**:
详情默认展示字段、观测值、期望规则、相关 DemandId 或 WorkType、证据时间和 PollTrace；完整 DemandRawObservation 仅经有大小上限和敏感字段白名单的按需展开查看。
_Avoid_: 首屏复制完整原始行、任意日志、无限大小响应、未脱敏字段

**ErrorSearchRefreshState（错误检索刷新状态）**:
刷新成功后仍命中的 Series 按 SeriesId 在新快照中重选，不再命中时清除详情并提示；刷新失败保留并明确标注上次成功快照及失败时间，旧结果不得冒充新筛选的结果。
_Avoid_: 新旧快照混显、失败即清空、在新筛选旁展示旧筛选结果

**ErrorSearchEmptyResult（错误检索空结果）**:
只有查询成功且零命中时才表示该条件和时间范围内没有错误历史，并可提供清除筛选入口；尚未完成、失败或取消均不得显示无错误，零命中也不代表系统健康。
_Avoid_: 加载中即无错误、失败即健康、把检索空集作为接入健康结论

**ErrorSearchExport（错误检索导出）**:
第一版不导出错误历史；筛选快照、权限、脱敏和大数据量导出须在确有现场需求时另行定义。
_Avoid_: 前端导出当前页、同步导出全部历史、未经脱敏的原始证据

**CurrentIngestAttention（当前接入关注项）**:
接入告警页展示当前需要关注的运维异常，可包含活动 Series 错误和无法归属 Series 的轮询或 WorkType 异常；Series 项直接引用稳定错误身份并跳转错误检索，不另建 fingerprint incident 生命周期。
_Avoid_: 已恢复错误历史、错误检索副本、Series 错误的独立 IngestAlert incident

**WatchOverviewSnapshot（Watch 概览快照）**:
Host 在同一投影提交时点给出的当前接入态势：包含需求系列、外部可读资格、活动 Series 错误、当前接入关注项的精确摘要及跨页重点动态；各部分必须共享同一快照身份和时间。
_Avoid_: 各页第一页拼盘、不同成功时间的卡片组合、用零错误或零阻断单独证明健康

**OverviewSeriesSummary（概览 Series 摘要）**:
当前 AreaFilterProfile 范围内的精确去重 DemandSeries 总数及 Tracking、Archived 等生命周期分面，并单独列出 GONE 与 LongGoneButVisible 等关注数量；分面可以重叠，不机械相加。
_Avoid_: Demand 数量、第一页数量、把关注项当作互斥生命周期

**OverviewReadabilitySummary（概览资格摘要）**:
当前 AreaFilterProfile 范围内的精确 TransportDemand 总数、READABLE 数和 NOT_READABLE 数；单位始终为 Demand 世代，三者来自同一 ReadabilityAuditSnapshot 口径。
_Avoid_: DemandSeries 数量、Catalog 条目数除以 Series、不同投影时点的分子分母

**OverviewErrorSummary（概览错误摘要）**:
不受 AreaFilterProfile 影响的当前 `ACTIVE` Series 精确数，以及截至概览快照最近 7 天曾命中的去重 Series 数；两项都使用 ErrorSearch 既定语义。
_Avoid_: IngestAlert incident 数、最近 24 小时假数据、默认包含 ENDED 的错误页数量

**OverviewIngestAttentionSummary（概览接入关注摘要）**:
当前 CurrentIngestAttention 的精确项数及类型、严重度构成，只表达当前关注项，不包含已经结束的历史。
_Avoid_: IngestAlert 历史总数、错误期间总数、Watch 连接横幅数量

**OverviewAttentionEvent（概览关注事件）**:
WatchOverviewSnapshot 中由真实状态转换形成、值得跨页下钻的近期事实，例如 Series 生命周期转换、错误期间开闭、轮询失败或恢复及 TaskTypeProtection 变化；静态总数本身不是动态。
_Avoid_: 页面摘要变化猜测、当前数量排行、重复轮询观测、旧 IngestAlert occurrence

**OverviewAttentionOrder（概览关注顺序）**:
概览只显示最近 24 小时内最新的五个 OverviewAttentionEvent，按发生时间降序和稳定事件标识排序；同一领域转换只出现一次，没有事件时明确表示近期无重点动态而不宣称系统健康。
_Avoid_: 无限动态流、每页各取一条、静态卡片补位、空列表即健康

**OverviewNavigationIntent（概览导航意图）**:
概览卡片或子摘要指向目标页的明确查询含义；整卡进入目标页默认范围，子摘要携带对应显式条件，错误卡固定进入最近 7 天的 `ACTIVE` Series，所有跳转从第一页开始。
_Avoid_: 依赖目标页隐含默认值、沿用旧游标、点击后丢失摘要含义

**OverviewAreaContext（概览 AREA 上下文）**:
概览中的 AreaFilterProfile 名称、AREA 数量和本地状态，以及它对需求系列与资格审计摘要的显示范围；它不影响错误检索或接入告警，也不属于 Host 业务快照事实。
_Avoid_: 全局业务范围、错误检索 AREA 条件、Dispatch AREA 范围、把本地配置时间当作投影时间

**OverviewStaleness（概览陈旧状态）**:
Host 概览刷新失败时保留的上一份完整 WatchOverviewSnapshot 及其时点，并与当前失败时间和实时 Host 连接状态明确区分；不得把新旧业务卡混成一个当前快照。
_Avoid_: 单卡静默保旧、失败即清空、当前离线时隐藏最后成功摘要

**LongGoneButVisible**:
DemandSeries 已归档后，同一 TransportDemandKey 再次出现在 MES 快照中的异常事实；它记录到原 DemandSeries，并生成供 Watch 查看实时原始数据的新 TransportDemand，但该 Demand 不属于 ExternallyReadableDemand。
_Avoid_: ReappearAfterGone、归档恢复、向外部程序开放归档后 Demand

**WorkType（工序类型）**:
DemandSeries 所属的工序维度，由 MES 查询字段 `TASK_TYPE` 表示；同一 SUBLOT 出现在不同 WorkType 时属于不同 TransportDemandKey 和不同 DemandSeries，同时出现在多个 WorkType 是需要在各相关 Demand 上展示的数据异常。
_Avoid_: STEP、把同一 SUBLOT 的全部可查询工序合并成一个 Series

**SublotMultipleWorkTypesObservation（子批次多工序类型观测）**:
同一 SUBLOT 在一份完整 MES 快照中同时出现于多个 WorkType 的异常事实；每个复合键仍生成独立 TransportDemand 并保存各自原始数据，但全部相关 Demand 都不能进入外部可读集合。
_Avoid_: 合并成一个 DemandSeries、只保留一个 TASK_TYPE、因异常而隐藏 Demand

**MesSourceDate（MES 来源时间值）**:
查询字段 `DATES` 提供的必填来源值，在 TransportDemand 中随每轮唯一 MES 观测实时更新并记录变化事件；其来源会随 TASK_TYPE 分支变化，不能用作 DemandSeries 开始时间或生命周期计时基准。
_Avoid_: MesCurrentStepEnteredAt、MesDataAge、DemandSeries StartedAt、MesLastSeenAt

**DemandLastSeenAt（Demand 最后看见时间）**:
本地最后一次在完整成功 MesTaskUnionRound 中看见该 Demand 原始行的时间；缺席证据只更新 GoneConfirmedAt，不得把缺席轮次伪装成最后看见时间。
_Avoid_: MesSourceDate、GoneConfirmedAt、用 GONE 轮次覆盖最后看见时间

**MesNextStep（MES 下一工序）**:
SUBLOT 下一步将进入的 MES 工序，由查询字段 `STEP` 提供；空值不会阻止 TransportDemand 生成，但会成为可见的数据异常并阻断外部读取，不参与 TransportDemandKey。
_Avoid_: 当前工序、SUBLOT+STEP 业务键、字段为空就隐藏 Demand

**MesPackage（MES 封装形式）**:
查询字段 `PACKAGE` 提供的产品封装形式，在 TransportDemand 中随唯一 MES 观测实时更新；空值不会阻止 Demand 生成，但会成为可见的数据异常并阻断外部读取。
_Avoid_: 字段为空就隐藏 Demand、外部程序补写的封装、首次值永久冻结

**DemandRawObservation（Demand 原始观测）**:
一轮 MES 快照中属于同一 TransportDemandKey 的全部原始行；无论字段空值、单行还是重复多行都保留给 Watch，不能通过任选、补值或冻结旧值掩盖源数据。
_Avoid_: 只保留第一行、用历史值填充当前 NULL、只保存外部合格数据

**DuplicateTransportDemandKeyObservation（重复运输需求键观测）**:
同一 SUBLOT + TASK_TYPE 在一份完整 UNION 快照中出现两条或更多条记录的异常事实；仍生成一个保存全部 DemandRawObservation 的 TransportDemand 并明确标注重复，但没有可信唯一单值投影，也不能进入外部可读集合。
_Avoid_: 多个不同 SUBLOT、正常批量快照、任选一行继续投影、因异常而隐藏 Demand

**LiveMesFieldSet（实时 MES 字段集）**:
TransportDemand 在唯一原始观测下实时呈现的 AREA、EQP、STEP、DATES、PACKAGE；每次变化覆盖当前值并记录事件，空值保持为真实 NULL 并形成具体字段异常。
_Avoid_: FrozenMesFieldSet、首次值基线、字段漂移、用旧值覆盖当前 NULL

**MesArea（MES 区域）**:
MES 设备主数据中标识设备所属区域的规范值，格式为 `^[A-Z][1-9][0-9]?-[1-9][0-9]?$`，例如 `A1-1`、`A11-11`；数字范围为 1–99，带多余前导零的 `A01-01` 不是同一值的合法别名，而是无效源数据。
_Avoid_: Station、Dispatch AREA 白名单、自动补零的 AREA、把非法 AREA 静默规范化

**TransportDemand**:
MesIngest 针对已观察 TransportDemandKey 产出的一条运输需求实例，主键为稳定 `demand_id`；它携带 DemandRawObservation、LiveMesFieldSet、当前异常和外部可读资格，数据异常不会阻止它生成或供 Watch 查看。
_Avoid_: 本地任务（厚状态机用语）、Order（RIoT 订单）、MES 行（未投影的原始查询行）

**ExternallyReadableDemand（外部可读 Demand）**:
当前唯一原始行的必填字段有效、没有任何当前数据异常、处于 VISIBLE 且所属 DemandSeries 未归档的 TransportDemand；外部可读目录只能暴露这个集合，异常 Demand 仍完整保留给 Watch。
_Avoid_: 全部 TransportDemand、WatchDemandProjection、把异常快照交给外部程序自行判断

**ExternallyReadableDemandCatalog（外部可读 Demand 目录）**:
MesIngest 提供的当前全部 ExternallyReadableDemand 集合；它不按调度程序的 WorkType、车间 AREA 范围、车辆或站点裁剪。外部程序按 CatalogRevision 条件读取并可随时丢弃本地缓存，不需要把它持久化成业务镜像，也不要求观察从未形成执行承诺的瞬时进出。
_Avoid_: EligibleDemandMirror、WatchDemandProjection、按调度范围裁剪的目录、需要 Cursor 恢复的外部副本

**CatalogRevision（目录修订号）**:
ExternallyReadableDemandCatalog 的单调版本；仅在集合成员或成员业务值改变时递增，使外部程序能够判定当前目录未变化而无需重新传输正文。
_Avoid_: Feed Sequence、业务任务版本、每轮 Poll 都递增的计数

**AcceptedDemandSnapshot（已接受 Demand 快照）**:
外部程序在创建 OrderIntent 或开始调度的执行承诺点，经最终读取确认后连同 CatalogRevision 与接受时间保存的不可变合格 Demand 事实；后续实时变化或退出目录不得改写它。
_Avoid_: Ingest 冻结 TransportDemand、当前目录缓存、用最新 MES 数据改写历史决策证据

**OrderIntent（建单意图）**:
外部程序在执行承诺事务中与 AcceptedDemandSnapshot 一起保存的可靠 RIoT 建单意图；它以稳定幂等键承接事务外远程调用，并把超时视为结果未知而不是自动失败。
_Avoid_: 已成功的 RIoT Order、在数据库事务内完成 HTTP、超时后换键重复建单

**WatchDemandProjection（Watch Demand 投影）**:
供 Ingest 与 Watch 查看全部 TransportDemand、原始行、实时字段、当前异常和外部阻断原因的运维投影；它不按 ExternallyReadableDemand 资格过滤。
_Avoid_: ExternallyReadableDemand 快照、只显示可调度 Demand、隐藏 NULL 或重复行

**ExternalReadabilityAudit（外部可读资格审计）**:
按一个冻结投影提交检查每个已生成 TransportDemand 当前是否属于 ExternallyReadableDemand，并解释全部通过项与阻断原因；结果单位是 Demand 世代，包含 VISIBLE、GONE、所属 Series 已归档及 LongGoneButVisible 的 Demand。
_Avoid_: DemandSeries 审计、只看当前 Catalog、资格历史回放、Dispatch 可派审计、UnassignedMesObservation

**ReadabilityAuditSnapshot（资格审计快照）**:
绑定一个投影提交时点的审计列表、精确总数、资格与原因分面及详情一致视图；它携带当时的 CatalogRevision，但不能仅用 CatalogRevision 代替自身快照身份。
_Avoid_: 当前投影拼接、翻页混入新提交、CatalogRevision 同义词

**ExternalReadabilityState（外部可读状态）**:
TransportDemand 在 ReadabilityAuditSnapshot 中的 `READABLE` 或 `NOT_READABLE` 资格结论；它与 Demand 的 VISIBLE/GONE 生命周期状态是不同维度。
_Avoid_: 可见/不可见、Demand 生命周期、Dispatch 可派状态

**ReadabilityBlocker（外部可读阻断原因）**:
使 TransportDemand 不属于 ExternallyReadableDemand 的稳定原因码；一个 Demand 可以同时具有多个原因，全部原因共同解释资格，任一原因筛选命中该 Demand，同一原因分面按 Demand 去重。
_Avoid_: 单一失败原因、错误消息文本、SeriesErrorCode、原因数量相加作为不可读总数

**ReadabilityBlockerCatalog（资格阻断目录）**:
由 MesIngest 领域契约发布且不可换义复用的 ReadabilityBlocker 定义；第一版覆盖 `DEMAND_GONE`、`SERIES_ARCHIVED`、`LONG_GONE_BUT_VISIBLE`、`DUPLICATE_TRANSPORT_DEMAND_KEY`、`SUBLOT_MULTIPLE_WORK_TYPES`、`REQUIRED_MES_FIELD_MISSING` 与 `INVALID_MES_FIELD_FORMAT`，字段主体作为结构化证据。
_Avoid_: Watch 本地原因字符串、IngestAlert code、每个字段复制阻断码、数据库可编辑目录

**LeadReadabilityBlocker（主要外部可读阻断原因）**:
Host 按稳定目录优先级为列表摘要选择的一个 ReadabilityBlocker；优先显示归档后可见、观测冲突和数据异常等当前可诊断问题，再显示 Demand GONE 与 Series 已归档，但它不改变完整原因集合或资格结论。
_Avoid_: 唯一真实原因、丢弃次要原因、Watch 本地排序规则

**ReadabilityAuditAreaScope（资格审计 AREA 范围）**:
当前 AreaFilterProfile 对资格审计的显示范围：Host 在计数和分页前按 Demand 当前可信单值 MesArea 精确筛选；不可信 AREA 不借历史值，只在“全部 AREA”中接受审计，且该范围不改变资格或 CatalogRevision。
_Avoid_: 外部可读规则、Dispatch AREA 白名单、客户端单页过滤、用历史 AREA 填补不可信当前值

**ReadabilityAuditResultOrder（资格审计结果顺序）**:
资格审计先列 `NOT_READABLE`，再按 LeadReadabilityBlocker 稳定优先级、DemandLastSeenAt 降序和 DemandId 升序排列；默认每页 100、最多 200，并返回当前筛选下的精确 Demand 总数。
_Avoid_: 按 Series 去重、估算总数、Watch 本地排序、任意列排序

**ReadabilityAuditFilter（资格审计条件）**:
资格状态、WorkType、阻断原因和标识等不同维度取交集，同一维度多值取并集，默认同时包含 READABLE 与 NOT_READABLE；DemandId 按去空白后不区分大小写精确匹配，SUBLOT 按不区分大小写包含匹配。
_Avoid_: 模糊 DemandId、正则、空字符串真实值、把 VISIBLE 当作资格状态

**ReadabilityAuditFacetCount（资格审计分面数量）**:
排除自身维度后计算的精确去重 Demand 数：资格分面应用其它条件与 AREA，原因分面只针对 NOT_READABLE 并应用其它条件与 AREA；一个 Demand 可计入多个原因，因此原因数之和不等于不可读总数。
_Avoid_: Series 数、阻断实例数、原因数量机械相加、分页后客户端计数

**ReadabilityAuditCursor（资格审计游标）**:
绑定 ReadabilityAuditSnapshot、规范化筛选、AreaFilterProfile 的 MesArea 值集合、固定顺序和契约版本的 keyset 位置；无效、过期或不匹配时明确失败并保留旧结果，不自动冒充第一页。
_Avoid_: 只绑定 CatalogRevision、跨 AREA 复用、静默刷新第一页、Watch 本地游标

**ReadabilityAuditDetail（资格审计详情）**:
同一审计快照中一个 Demand 的全部资格检查、完整阻断集合、可信字段或原始观测冲突、所属 Series、PollTrace、投影提交身份与 CatalogRevision；主要原因不能替代完整推导。
_Avoid_: 只显示一个原因、只显示最终布尔值、把 Dispatch 条件加入资格、详情读取另一快照

**ReadabilityAuditRefreshState（资格审计刷新状态）**:
刷新成功后仍存在且仍命中的 Demand 按 DemandId 在新快照中重选，不再命中时清除详情并提示；刷新失败保留旧筛选、旧快照及其范围标签，不把旧结果挂在新条件下。
_Avoid_: 新旧筛选混显、失败即清空、静默保留已移出范围的详情

**ReadabilityAuditEmptyResult（资格审计空结果）**:
只有审计查询成功且当前条件零命中时才表示没有符合条件的 Demand；失败、取消和加载中不得称为无 Demand，零个不可读 Demand 也不能单独证明接入健康。
_Avoid_: 空页即健康、失败即零、加载中空态

**ReadabilityAuditNavigationContext（资格审计跳转上下文）**:
从审计项进入需求系列时携带 SeriesId、聚焦 DemandId 和来源审计快照摘要；目标页读取自身当前快照并允许显示已经变化，范围外对象仍须由用户确认切换到“全部 AREA”后打开。
_Avoid_: 把旧资格结论冒充 Series 当前状态、静默绕过 AREA、丢失 Demand 世代定位

**AreaFilterProfile（AREA 筛选配置）**:
当前 MesIngestWatch 实例用于缩小 DemandSeries 与资格审计页面显示范围的本地命名配置，内容是一组合法 MesArea；两页共享当前选择并按 MesArea 精确匹配，它不改变 WatchDemandProjection、外部可读资格、ExternallyReadableDemandCatalog 或 Dispatch 的 AREA 范围。
_Avoid_: AREA 白名单、调度范围、外部可读规则、Area 文件

**TransportDemandKey（运输需求业务键）**:
由 SUBLOT 与 WorkType（MES `TASK_TYPE`）组成，标识该 SUBLOT 在当前工序类型中的同一搬运候选，也是调度侧本地取消的永久抑制边界；同一 SUBLOT 命中其它 WorkType 时属于不同业务键。
_Avoid_: DemandId、只用 SUBLOT、SUBLOT+STEP、MES 需求编号、取消后重建同键任务

**DemandId**:
TransportDemand 的本地稳定标识，也是车载 CurrentStopWorklist 精确选择当前任务实例的标识；调度等本地系统用它挂接状态，但它不是 MES 提供的需求编号，也不能代替 TransportDemandKey 的取消抑制。
_Avoid_: SUBLOT、另造 stationTaskId、MOCK_TASK_ID

**UnassignedMesObservation（未归属 MES 观测）**:
完整 MesTaskUnionRound 中因 SUBLOT 或 TASK_TYPE 缺失而无法形成 TransportDemandKey 的原始行；它属于 PollRun 运维证据，不生成 DemandSeries，但不能被静默丢弃。
_Avoid_: 随机归到相似 Demand、因无业务键而隐藏、成功的部分快照

**WireBond1**:
业务上的第一次焊线；MES 机台侧 step 名为 `焊线`（不是 `焊线1`）。仅焊线工艺有分道，键合无对等的 1/2。
_Avoid_: 焊线1（当作 MES step 名去查库）、键合1

**WireBond2**:
第二次焊线；MES 的 step 名就是 `焊线2`。产品在 WireBond1 完工后、进入 `焊线2`+`入库` 等待时，触发送氮气柜。
_Avoid_: 第二次焊线（口语替代正式 step 名）

**WireToNitrogen**:
运输任务类型代码 `WIRE_TO_NITROGEN`：WireBond1 机台 → 固定氮气柜站点。起终点规则同 `WIRE_TO_GATE`（起点取查询 EQP/AREA，终点固定区域）。PDA 扫码入柜后该行从 MES 快照消失；之后再上 WireBond2 由既有 `STAGING_TO_WIRE` 覆盖，不另建任务类型。不含键合。
_Avoid_: WIRE_TO_N2、WIRE1_TO_N2_CABINET、氮气柜任务（无代码名）
