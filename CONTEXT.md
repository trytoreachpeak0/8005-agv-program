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

### AGV 档案与生命周期

**AgvIdentity（AGV 身份）**:
ControlServer 首次接入车辆时创建、以永久不变的本地 `agvId` 表达的车辆身份；归档、恢复和 RIoT 重新登记均不改变它。
_Avoid_: deviceKey、车辆名称、IP 地址、当前 RIoT 登记

**RiotVehicleBinding（RIoT 车辆绑定）**:
一个 AgvLifecycleGeneration 内 `agvId` 与当前 RIoT `deviceKey` 的唯一映射；它可以在恢复时换版并保留完整历史，但不承担车辆身份判定。
_Avoid_: AgvIdentity、永久车辆 ID、覆盖旧 deviceKey、同一 deviceKey 同时绑定多个活动 AGV

**AgvLifecycleGeneration（AGV 生命周期代次）**:
同一 AgvIdentity 的一次连续服役周期；每次从归档恢复时递增，用于隔离连接、订单、消息和当前运行状态，旧代次只能作为历史证据。
_Avoid_: VehicleConnectionSession 代次、创建新 agvId、恢复后续接旧运行态、清除历史

### 人员身份与权限

**维护管理员（MaintenanceAdministrator）**:
以个人账号密码登录、负责 8005 日常现场维护的权限角色；可管理未归档车辆和仓位可用性、执行仓门及 IO 功能测试、核对 IO 映射、处理异常并在安全门禁通过后解除人工急停，但不能恢复归档 AGV，也不能修改或激活 IO 映射、管理账号权限、修改系统级配置或软件版本。
_Avoid_: 小管理员、维护人员共享账号、R-09/R-11/R-13 系统角色

**系统管理员（SystemAdministrator）**:
仅授予软件维护人员、拥有全部 8005 系统权限的最高权限角色，包括维护管理员能力、归档 AGV 恢复、账号与角色管理、仓位模型与模板维护、IO 映射维护和激活、系统级参数、外部接口配置、凭证及软件版本维护；它是唯一可发起并确认归档 AGV 恢复的角色，全部权限仍不能覆盖车辆停稳、仓门安全、状态未知阻断等安全事实门禁。
_Avoid_: 最大管理员、超级账号、安全门禁覆盖者

**管理员个人账号（PersonalAdministratorAccount）**:
唯一绑定一名自然人的账号密码身份，只能授予 MaintenanceAdministrator 或 SystemAdministrator 之一；每个账号只允许一个活动登录会话，新登录终止并记录旧会话，不同人员必须分别建立账号，全部查看与变更审计均归属该具体人员。密码只可由 SystemAdministrator 设置，MaintenanceAdministrator 不能自行改密；设置新密码不终止当前会话，新密码从下次登录生效。
_Avoid_: 岗位共享账号、通用管理员、多人共用密码、同账号并发登录
_Note_: 该词条描述的是已批准的需求语义，**不是当前实现**。完整产品本期不建人员认证与账号（2026-09-04 用户定案，完整产品图票 05）；现有形态是一个全场共用的环境变量做定时安全比较，**不识别自然人、也不区分 MaintenanceAdministrator 与 SystemAdministrator**，而 `administratorRole` 是消息 payload 里由客户端自行声明的字符串。故任何按个人账号归属的审计在当前实现下都不可归属自然人。

**管理员撤权（AdministratorAccessRevocation）**:
系统管理员停用管理员个人账号或降低其角色后立即终止该账号的活动登录和异常处置权限；此前已经发出但结果未知的动作继续由系统对账并保留审计，后续处置须由另一具备权限的个人账号重新登录接手。
_Avoid_: 延迟撤权、撤权即取消已发动作、删除历史审计、被撤权会话继续操作

**当前人员访问模型（CurrentHumanAccessModel）**:
8005 当前只接受操作员工号识别、维护管理员个人账号和系统管理员个人账号三种人员访问身份，暂不设置独立只读账号角色；没有维护职责的厂内 IT 或生产管理人员不登录系统。
_Avoid_: R-01～R-15 权限角色、隐含只读账号、为查看而授予维护管理员

**管理员操作审计记录（AdministratorActionAuditRecord）**:
维护管理员或系统管理员每次操作形成的不可改写事实，记录个人账号、当时角色和登录会话、时间、终端与来源地址、操作对象、原因、前后状态以及请求、执行和最终核验结果；失败、超时和结果未知与成功操作同等保留。管理员可以查看和导出，但任何管理员都不能修改或删除记录。
_Avoid_: 仅成功日志、共享账号审计、管理员可编辑日志、无操作对象的泛化记录

### 仓位操作与恢复

**断联仓位操作收敛（ConnectionLossSlotContainment）**:
车载上位机与服务端失联后限制仓位操作风险范围的保护策略：禁止扩大当前开锁集合；已经开始或发送结果不确定的开锁集合完成安全收尾后暂停，且不设置自动取消超时，直至重连对账并获得服务端明确授权。若只是通信断联且物理状态始终有效，服务端授权到达后车载端直接继续，不要求操作员重复确认；若同时存在锁 DI 等硬件故障，则必须在 ExceptionRecoverySession 中完成处理并留下 HardwareRecoveryRecord。连接恢复本身不构成授权。
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

**仓位操作完成（SlotOperationCompleted）**:
一次仓位操作指令的每个目标仓位都达到当前开锁集合安全收尾所定的最终态——装货为 `OCCUPIED + 锁闭 + 开锁输出已复位`，卸货为 `EMPTY + 锁闭 + 开锁输出已复位`——并在结果中逐仓如实上报，这次仓位操作才算完成。两端共用这一个定义：车载上位机只在此时上报完成，服务端按同一条件逐仓复核后才承认完成，任何一端都不另立判据。任一目标仓位未开始、状态未知、锁未闭或开锁输出未确认复位，都不是完成；其中装货在本站期限过后仍读到明确相反状态的是确定失败，其余进入恢复。
_Avoid_: 工作流跑完即完成、关门即成功、部分仓位达成即完成、结果已被确认即完成、两端各自判完成

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

**SlotTemplate（仓位模板）**:
可由多个仓位共同引用的受控业务规格，定义仓位长、宽、高及兼容的花篮类型，但不定义载重；已发布修订由服务端统一供全部引用车辆使用，不触发 IO 配置换版或实际 IO 核验。
_Avoid_: 单仓位配置副本、仓位位置、载重模板、IO 模板

**SlotPosition（仓位位置）**:
仓位在车辆上的规范物理位置值，其中已经包含原“所属面”的方位信息，不再另设独立所属面字段。当前八仓车型取 `FRONT`（1～4 号，前侧仓门）与 `REAR`（5～8 号，后侧仓门）两组，车辆停靠 AREA 机台站点时只能开启其中一组。
_Avoid_: SlotSide、所属面字段、界面数组索引、IO 通道位置、用 LEFT/RIGHT 称呼前后两组、在规则里按仓号区间写死分组

**VehicleSlotTemplate（整车仓位模板）**:
可供多个同构 AGV 复用的整车仓位组合，定义物理仓位集合及每仓的 SlotPosition、SlotTemplate 引用，但不包含车辆 IO 映射；单车不得直接覆盖布局，差异必须建立新模板或新版本。
_Avoid_: 单车布局覆盖、IO 配置模板、无版本仓位清单

**SlotModelVersion（仓位模型版本）**:
ControlServer 对 VehicleSlotTemplate 的仓位集合、物理编号、SlotPosition 和 SlotTemplate 引用关系发布的不可变拓扑版本，一个版本可以绑定多辆同构 AGV；SlotTemplate 的尺寸或兼容性修订不改变该拓扑版本。
_Avoid_: 草稿模板、单车私有布局、IO 配置版本、尺寸兼容性版本

**OnboardSlotLayoutSnapshot（车载仓位布局快照）**:
ControlServer 从 SlotModelVersion 面向特定 AGV 生成、由车载上位机持久化的只读布局投影；它以物理仓位号表达每仓的 SlotPosition 和 SlotTemplate，供车载 HMI 正确展示，但不包含 IO 映射，也不是车载端可独立编辑的模型主数据。
_Avoid_: IO 配置、临时界面缓存、车载仓位模型

**SlotIoBinding（仓位 IO 绑定）**:
车载上位机以物理仓位号为键保存的逐仓开锁输出、锁闭反馈、仓内光幕及可选附加传感器映射；点位数量、传感器种类和原始信号极性属于车型或车辆配置，不是跨车型常量。当前一仓一门，因此仓门不建立独立于 SlotIdentity 的身份。
_Avoid_: IO 通道列表、DoorId、按界面位置绑定 IO、把 8005 点位或极性硬编码为通用规则

**SlotOperability（仓位可操作性）**:
车载上位机依据有效 IO 映射、模块在线性和实时安全执行条件形成的仓位硬件能力；它不改变 SlotIdentity，也不自动改变仓位业务内容，服务端人工启用不能覆盖车载端判定的不可操作。
_Avoid_: 仓位存在性、业务空闲、人工启用/禁用

**仓位管理可用性（SlotAdministrativeAvailability）**:
服务端保存的人工启用/禁用业务策略；车载 HMI 须在仓门真实位置展示。未被活动 Sublot 占用时禁用立即生效；已被活动 Sublot 占用时进入待禁用（Disable Pending），该 Sublot 经服务端确认结束后生效。它不能替代或覆盖仓位可操作性。
_Avoid_: SlotOperability、硬件故障、删除仓位

**IoConfigDraft（IO 配置草稿）**:
ControlServer 保存但尚未激活的 IO 映射候选版本，由系统管理员在服务端配置维护界面编辑并提交给目标车辆验证；保存或提交草稿不影响当前生效配置、仓位可操作性或真实 IO。
_Avoid_: 车载端本地草稿、当前配置、离线生效配置、已激活配置

**ConfigurationMaintenanceConsole（配置维护界面）**:
ControlServer 面向系统管理员提供的仓位模型、SlotTemplate 和 IO 映射受控维护入口，承载查看、编辑、多选、草稿复制、审计和候选版本提交，但第一版不提供文件批量导入；车载上位机不提供平行的配置编辑入口。
_Avoid_: 车载维护编辑界面、本地配置文件直改、无审计配置入口

**SlotConfigurationReadiness（仓位配置就绪）**:
已发布 SlotModelVersion 中全部仓位均具有完整且经过实际核对的 SlotIoBinding；新 AGV 可以在未就绪时先登记，但整车不得投运，未配置或未验证仓位也不得被业务分配或人工强制放行。
_Avoid_: 登记完成、部分仓位可投运、仅通过格式校验、管理员强制就绪

**SlotConfigurationVerification（仓位配置核验）**:
仓位集合、物理编号、SlotPosition 或 IO 映射、极性、传感器和脉冲参数发生硬件相关变更后，对整车全部仓位执行的双向实际核对；它确认开锁输出与物理仓门、输出复位、锁反馈、光幕语义、通道唯一性及模型版本一致，任一仓位失败都会阻断整个候选版本。
_Avoid_: 只测改动仓位、格式校验、抽样测试、部分通过即可激活

**SlotMetadataChange（仓位资料变更）**:
只修改 SlotTemplate 的长、宽、高或花篮兼容性的服务端共享业务资料变更；一次发布供全部引用车辆的新任务使用，不进入 VehicleConfigurationMaintenance，也不重做实际 IO 核验。
_Avoid_: 仓位拓扑变更、IO 配置变更、逐车模板激活、载重变更

**SlotAssignmentTemplateSnapshot（仓位分配模板快照）**:
任务取得仓位分配或预留时固定的 SlotTemplate 修订，活动任务沿用它直至结束，不因后续 SlotMetadataChange 中途失效；新任务使用发布时的最新修订。
_Avoid_: 动态模板引用、发布即重判在途任务、中途取消、未记录兼容性版本

**SlotHardwareConfigurationChange（仓位硬件配置变更）**:
修改仓位集合、物理编号、SlotPosition、IO 点位、极性、传感器或脉冲参数的变更；它必须进入 VehicleConfigurationMaintenance，并经过整车 SlotConfigurationVerification 和原子激活。
_Avoid_: 尺寸修订、花篮兼容性修订、普通资料维护、在线热改

**ActiveSlotConfiguration（生效仓位配置）**:
目标车辆当前实际使用的整车配置版本，由一个已发布 SlotModelVersion 与完整 SlotIoBinding 集合共同组成；它只能在整车核验通过后原子切换，不能逐仓混用新旧版本，结果未知时也不能被推定已生效。
_Avoid_: 逐仓生效配置、部分激活、服务端期望版本、未核验草稿

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
VehicleConnectionSession 完成认证后，由服务端在能力同步、未结操作及积压结果对账、物理与业务状态核对均通过且不存在 ManualChargingHold 等业务保持时明确授予的业务状态；只有处于该状态才可开始扫码、接收新仓位操作或恢复移动。
_Avoid_: TCP 已连接、TLS 已认证、心跳正常、电量上升即自动重新投运
_Note_: 它是 **fail-closed 谓词链的派生量，不是可写状态字段**——「谓词链无命中」即业务就绪。归档恢复、暂停分配、配置维护、电量不足各是链上的一个独立谓词，互不覆盖，因此阻断原因不会被一个笼统的 Disabled 值吞掉。「投运」这个动作写的是一个供谓词读取的已投运标志位，不是把状态设为就绪，故「检查通过也不自动投运」是该形态的直接结果而非另一条规则。

**VehicleBusinessStateSnapshot（车辆业务状态快照）**:
ControlServer 面向单台 AGV 发布的带版本完整业务投影，只表达 VehicleBusinessReadiness、ManualChargingHold、电量事实未知及结构性业务阻断；它不复制 Demand、停靠计划、车载物理安全或仓位执行状态。
_Avoid_: 单体旅程状态机、CurrentStopWorklistSnapshot、SafetyStateSnapshot、车载端自行推导业务就绪

**VehicleRecoveryRequired（车辆待恢复态）**:
车辆连接在线，但恢复对账存在无法自动解释的差异，或者锁 DI 等关键硬件反馈失效、无法证明仓门安全状态时，服务端拒绝授予 VehicleBusinessReadiness 并等待人工处置的状态；该状态仍允许心跳、诊断和恢复协议通信。硬件反馈恢复有效本身不能解除该状态，须由具备 ExceptionRecoveryPermission 的人员在异常处置会话中记录处理结果，并由系统重新核验全部门禁。
_Avoid_: 断线、离线、自动换仓、自动补偿清空、带病接新业务

**异常处置权限（ExceptionRecoveryPermission）**:
允许维护管理员或系统管理员处理仓内传感器/锁硬件异常、车辆本体故障和被困货物的统一权限；它随个人 MaintenanceAdministrator 或 SystemAdministrator 账号授予，不再按 R-09/R-11/R-13 等岗位角色分别配置。持权人验证个人身份后可独立完成整套异常处置；无权限人员可报告、协助或接管货物，但不能操作异常处置界面。断电、抱闸和强制机械开锁等现场动作仍要求实际执行人具备相应作业资质并被记录，作业资质不是系统审批步骤。
_Avoid_: 审批人、双人复核、共享账号、岗位角色授权、逐人附加恢复权限、身份验证即忽略安全门禁

**异常处置会话（ExceptionRecoverySession）**:
具备 ExceptionRecoveryPermission 的人员验证一次个人身份后，为一个异常事件、一台车辆及该事件涉及的任务和目标仓位集合建立的短期操作上下文；会话内可连续选择修复续行、受控取货、强制机械取出、实物交接和恢复车辆，不逐动作审批或重复认证，系统自动记录全部选择、命令、结果和实物交接。人员交接、切换车辆、扩大目标仓位范围、主动退出、事件关闭、父登录会话结束或权限撤销时立即结束；当前不设空闲超时，短暂断线后只有同一人员、同一事件且会话仍有效时，完成最新状态对账即可继续，断线期间不得扩大范围。会话不能绕过停车、目标范围、可取得的仓位物理证据或恢复对账；状态未知时只能先完成断电、抱闸等物理隔离并执行必要救援，车辆继续保持隔离直至事实可验证。普通放错只在离站前由既有 LoadCorrection 处理，离站后不进入本会话纠正。
_Avoid_: 审批工单、逐动作二次认证、跨人员复用、跨车辆通用会话、临时扩大仓位、永久登录权限、断线期间扩权、未知状态强制恢复

**RecoveryActionId（恢复动作选择编号）**:
ExceptionRecoverySession 中一次具名恢复路径选择的稳定身份；相同编号只允许完全相同的事件、人员、车辆、Demand、仓位范围和动作内容，传输重试沿用原编号，修改任何选择必须建立新编号。
_Avoid_: MessageId、SlotOperationAttemptId、跨会话复用、修改原选择

**HardwareRecoveryRecord（硬件恢复记录）**:
异常处置人员在 ExceptionRecoverySession 中记录具体硬件的检查、处理和现场结果而自动形成的审计事实；它不是审批，也不能代替锁 DI、光幕、输出回读等实时物理证据，系统只有在相关物理与业务门禁同时通过后才恢复原操作或仓位资格。
_Avoid_: HardwareRecoveryConfirmation、维修批准、信号恢复即自动续行、人工覆盖无效传感器、换仓、创建新装货尝试

**VehicleConfigurationMaintenance（车辆配置维护态）**:
服务端只为已停稳、整车空仓且没有活动仓位操作、任务或预留的车辆持久化该整车非业务状态；系统管理员激活候选版本即同时表达重新投运意图，维护连接中断或自动版本、指纹、能力及安全对账未全部通过时持续隔离，全部通过后自动退出。
_Avoid_: 逐仓在线配置审批、车辆离线、断线继续激活、激活后二次人工审批、普通仓位禁用

**RecoveryHandshake（恢复握手）**:
车辆首次连接和重连共用的业务就绪流程：依次建立带代次的连接会话、同步完整车载能力、上报未结操作与恢复检查点、补报并确认积压结果，最后由服务端返回 READY 或 RECOVERY_REQUIRED。
_Avoid_: TCP 握手、首次连接快捷通道、重连后直接接业务

**ProtocolEnvelope（协议消息外壳）**:
车载—服务端每条 NDJSON 消息共用的固定结构，包含 protocolVersion、messageType、messageId、correlationId、agvId、sessionGeneration、sentAt 和 payload；业务字段只放在 payload 中。
_Avoid_: 每种消息自定义顶层元数据、裸 payload、用 slotOperationAttemptId 代替 messageId

**ProtocolVersion（车载通信协议版本）**:
ProtocolEnvelope 中标识完整通信契约的整数；第一版固定为 1。同版本只能增加接收方可忽略的可选字段，任何必填字段、字段语义或强制流程的破坏性变更都必须升级版本。
_Avoid_: 软件版本号、按消息独立版本、运行时猜测兼容

**ProtocolRelease（协议发布包）**:
共享协议仓库中一次不可修改的完整契约发布，包含同一协议剖面的 Schema、manifest、错误码、合法／非法样例、一致性向量、兼容性说明和批准证据；它可以在 ProtocolVersion 不变时因兼容材料增加而产生新版本。
_Avoid_: ProtocolVersion、实现软件版本、main 分支当前内容、可覆盖 tag、单个 Schema 文件

**ProtocolReleaseIdentity（协议发布身份）**:
两个实现仓库、模拟对端和验收证据共同锁定某个 ProtocolRelease 的复合身份，由仓库、release 版本、不可变 tag、完整 commit、ProtocolVersion、协议剖面及 manifest、Schema bundle 和向量哈希共同确定；任一分量不同都不是同一契约。
_Avoid_: 只写 tag、只写 commit、跟踪 main、两端各自维护版本号

**IntegrationSlice（跨端联调切片）**:
以稳定 IntegrationSliceId 标识、能够由共享协议向量和确定性故障脚本独立复现的一段控制服务端与车载端之间的跨端能力；它固定前置切片、输入、逐步输出、持久事实、禁止副作用和最终状态，并分别经过双模拟对端门禁及精确两端候选构建的真实联合运行。只有双端能力才立切片：服务端与 RIoT、MES 或人之间的单端能力不是切片，需要多个并发会话才能表达的行为（例如多车并发）在保形向量的单会话格式下也无法成为切片，两者的验收由 SemiPhysicalScenarioLayer 与 FieldAcceptanceWindow 承担——不立切片不等于不验，只是判据不在门禁模型里。IntegrationSliceId 属于某个 IntegrationSliceFamily，不跨协议大版本沿用。切片完成不是产品发布批准，也不能替代工厂试运行。
_Avoid_: 团队任务编号、仓库开发阶段、一次“大联调”、只对 Fake 通过即完成、现场成功倒推通过、把单端工程算作切片

**IntegrationSliceFamily（切片家族）**:
某一个 ProtocolRelease 之下全部 IntegrationSlice 的完整编号集合，由 id 前缀、编号规则、切片总数、顺序与前置关系共同确定；家族随协议大版本整体换代而不是逐个增补，旧家族随其不可变 tag 原地冻结，其门禁证据此后只能被引用为“前一代的对应切片”，不能被复用为新家族的通过结论。
_Avoid_: 跨版本沿用编号、两套编号并存于同一 index、把批次或业务分簇编进 IntegrationSliceId、以家族更名代替证据重跑

**ImplementationBatch（实施批次）**:
完整产品实施顺序的单位，由该批次内的需求条目集合、无需求条目载体的工程项清单，以及它对其它批次的依赖边共同确定；每条依赖边必须能归约为一条已推翻的架构不变量、一条协议冻结面前置、一条切片 prerequisites，或一条现场前置。它与 IntegrationSliceFamily 正交——切片是联调证据的单位，批次是实施顺序的单位，一个批次含零到多个切片，一个切片只属一个批次；也因此批次编号不进 IntegrationSliceId。一个批次可以完全没有需求条目载体：协议冻结面落地与多车化都是真实工程量，却都不在需求条目上产生新行。
_Avoid_: 按体量均衡切批次、以“先做这个更稳妥”作依赖理由、把批次等同于切片、只按需求条目排期而漏掉无载体工程、把批次编号写进切片 id 或证据目录

**SemiPhysicalScenarioLayer（半实物场景层）**:
一条把真控制服务端、真车载端与真仓位 IO 接在一起、由脚本无人值守驱动并对被测方自身状态（服务端数据库、各替身控制面快照）断言的自动化验证层；它介于进程内单元测试与现场试运行之间，是唯一能观测跨端时序的自动化层。它有两套装置：合成装置用协议对端替身，真装置用车载端产品程序与真 Modbus 模拟器；两者不可互换，合成对端没有 IO、journal、操作员与本地时钟新鲜度判定，而真装置的车载端与仓位模拟器绑死——缺少 Modbus 则全部仓位报未知，出发安全恒为否，会话永远不就绪。它通过不代表现场合格：没有真实 RCS、真车、交通管制与真实 IO 硬件。
_Avoid_: 把它当成现场验收的替代、只跑合成装置就声称跨端行为已验、用 sleep 代替判据、绕过被测方直接摆出终态再断言、在合成对端上复现只有真车载端才有的逻辑

**AcceptanceExitCriteria（验收出口条件）**:
一个 ImplementationBatch 算作完成所需满足的判据集合，由三部分构成——进程内测试全绿且新能力有新增覆盖、该批次的半实物场景在 CI 上连续三次通过、以及该批次绑定的每个 IntegrationSlice 四道门禁全部通过。现场判据不属于它，那由 FieldAcceptanceWindow 单独承担，因为现场前置的就绪时间不由项目控制。出口条件可以含负向判据，例如证明某个门禁在参数缺失时确实阻断；当某条需求在当前现场配置下自然不触发时，出口条件必须指定一个可复现的替代证据来源，不得以“不触发”充当通过。
_Avoid_: 以“不触发即通过”结案、只给正向判据而不验阻断、把现场判据混进批次出口、一次通过即认定稳定、靠切片计数覆盖没有切片的工作

**FieldAcceptanceWindow（现场验收窗口）**:
一次占用真实车辆、真实厂区与现场人员的受控验收，按现场前置就绪而不是按批次号排期。它不是门禁——切片的门禁数组不含它，其证据独立归档，与门禁证据分目录。每个窗口有明确的进入门槛（代码就绪加现场前置完成）与逐条出口判据；首次涉及车辆自主行为的窗口必须有人跟随全程，多车放开按车辆数分阶段进行而不是一次全开。生产从 MVP 部署转到 v2 线的那一次窗口另有规定，见 V2ProductionCutover。
_Avoid_: 每个批次各清一次场、把现场证据写进门禁目录、以现场成功倒推门禁通过、首次自主行为无人跟随、在同一次窗口里叠加多个未验证的新能力

**V2ProductionCutover（生产切换到 v2）**:
生产调度从 MVP 部署一次性转到 v2 线的 FieldAcceptanceWindow。进入门槛是切换路径上全部 ImplementationBatch 的出口条件达成、MVP 修复同步的必需项合入、空载急停演练完成，以及等待点、固定站点绑定与充电桩名册等现场前置就绪。窗口内按四个阶段放开：一台车一趟只带一条需求，两台车，三台车，最后开启一车多需求；每个阶段在跑的每项能力都至少完整走通一次且无需人工处置后才进入下一阶段，出现安全类异常即停在当前阶段。仓位分侧、自动充电与空闲返回从第一阶段起同时首次上线，是「不在同一次窗口叠加多个未验证新能力」的明确例外：分侧无法单独关闭，自动充电不允许以人工充电替代。唯一回退是换回切换前的 MVP 部署与数据，不修改 MVP 代码。
_Avoid_: 单车切换后另择窗口放开多车、切换后继续开发 MVP、以修改 MVP 代码作为回退、前三个阶段开启一车多需求、以关闭分侧或改用人工充电降低切换风险、把持货等单当作相对 MVP 的倒退

**FakePeerIdentity（模拟对端身份）**:
一次一致性运行所使用 Fake Onboard 或 Fake ControlServer 的可复现复合身份，由其所在实现仓库、完整 commit、构建产物哈希、ProtocolReleaseIdentity、测试 harness contract 版本及支持的 IntegrationSliceId 集合共同确定；Fake 只模拟协议可观察行为，不声称证明真实 IO、RIoT 或生产持久化能力。
_Avoid_: 仅软件版本字符串、latest Fake、共享协议仓库中的第三套生产实现、用 Fake 结果代替真实对真实联调

**ConformanceRunIdentity（一致性运行身份）**:
一次不可改写的一致性或联调运行的完整证据身份，绑定 runId、IntegrationSliceId、两端完整 commit 与构建摘要、ProtocolReleaseIdentity、适用的 FakePeerIdentity、runner/harness 版本、向量集合哈希、环境配置摘要、时间和结果；任一绑定分量变化都必须建立新运行，不能沿用旧通过结论。
_Avoid_: CI 最新结果、分支名、只记 protocol tag、重跑覆盖旧失败、跨构建复用通过证据

**FactoryPilotConfigurationSnapshot（工厂试运行配置快照）**:
一次受控工厂试运行候选的不可改写配置身份，绑定两端构建、ProtocolReleaseIdentity、适用一致性证据、MesIngest 只读契约、AGV 与连接凭证引用、RIoT 环境和车辆绑定、Map／Station、八仓配置、目标硬件、人员责任及物料资格；只保存秘密引用和核验结果，任一影响判定的字段变化都必须形成新快照并重过受影响门禁。
_Avoid_: 现场口头清单、latest、只锁软件版本、保存真实密钥、在原快照手改字段

**FactoryPilotRunIdentity（工厂试运行身份）**:
一次空车彩排、目标硬件验收或真实物料旅程的不可改写证据身份，绑定 FactoryPilotConfigurationSnapshot、实际 Demand／Sublot／物料、车辆与地图站点、全部前置运行、参与人员证明、时间、结果和原始证据哈希；失败和重跑使用不同 runId，PASS 只适用于该精确身份且不等同于产品发布批准。
_Avoid_: 最后一次绿灯、最佳录像、覆盖失败、跨配置复用、试运行通过即批准发布

**WireToGateMvpProtocolProfile（WIRE_TO_GATE MVP 协议剖面）**:
ProtocolVersion 1 中为 WIRE_TO_GATE 单 Demand、双移动段旅程明确列出的必需且允许消息集合；它复用同一协议外壳和既有语义，不是新的 ProtocolVersion，剖面外消息在该 release 中必须稳定拒绝。
_Avoid_: 实现全部长期协议能力、另建专用协议版本、未声明消息也尽量接受
_Note_: 它是 **ProtocolVersion 1 的剖面**，定义里的两个限定词（ProtocolVersion 1、单 Demand 双移动段）在完整产品下均不成立；完整产品由 AgvFullProductProtocolProfile 承载。两者**不是同一个剖面的两个版本**，而是两个剖面，各自绑定自己的 ProtocolVersion。（2026-09-04，完整产品图票 06）

**AgvFullProductProtocolProfile（完整产品协议剖面）**:
ProtocolVersion 2 中为 8005 完整产品明确列出的必需且允许消息集合，覆盖六类运输任务、多车、多 Demand 多停靠、自动充电、等待点、仓位配置激活与告警上报；它复用同一协议外壳和既有语义，剖面外消息在该 release 中必须稳定拒绝。其 profileId 字面值为 `AGV_FULL_PRODUCT`——与 WIRE_TO_GATE_MVP 同构，是阶段名而不带版本号，版本活在 ProtocolVersion 与 ProtocolReleaseVersion 里。
_Avoid_: WireToGateMvpProtocolProfile、另建第三个协议版本、把 profileId 当版本号、未声明消息也尽量接受

**MessageId（消息编号）**:
一条协议消息的稳定唯一编号，用于消息去重以及通过 correlationId 对应 ACK 或响应；同一消息的传输重试沿用原编号，新语义消息使用新编号。
_Avoid_: 仓位操作尝试编号、运输任务 ID、每次重发的新编号

**MessageDeliveryClass（消息交付类别）**:
每种 messageType 固定声明的传递语义：可靠业务/安全消息使用持久化接受 ACK，请求消息使用关联响应，遥测消息允许丢失，心跳确认只用于连接存活判断。
_Avoid_: 所有消息统一 ACK、由调用处临时决定是否重试、ACK 即执行完成

**DurableAck（持久接受确认）**:
接收方只在完成 DurableAcceptance 后对可靠业务或安全消息返回的通用确认；它通过 correlationId 指向原 MessageId，只证明接收责任已转移，不表达业务批准、物理执行或动作完成。
_Avoid_: 类型化业务拒绝、OperationResult、发送成功、进入内存队列

**SnapshotAppliedAck（快照采用确认）**:
接收方原子采用某类完整快照及其 revision 后返回的通用确认；它不把旧 revision 重新变成当前状态，也不证明快照之外的业务或物理门禁成立。
_Avoid_: DurableAck、逐条事件 ACK、快照内容即动作授权

**ProtocolProblem（协议问题）**:
在合法外壳仍可安全关联时返回的结构化协议诊断，表达 Schema、会话代次、未知或剖面外 messageType 等问题；稳定原因码可用于判断，显示文案只供人员阅读，不能承载业务拒绝。
_Avoid_: 通用业务 Error、解析显示文案、用协议问题表示物理失败、无法解析外壳时强行回应

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
车载上位机依据锁传感器的有效反馈形成的仓门是否锁闭的物理事实；当前硬件没有独立的门关闭传感器，因此系统不能直接观测“仓门打开或关闭”。只有有效锁反馈明确证明锁闭才属于安全锁闭，明确未锁闭、反馈无效或未知都属于“仓门未能证明安全锁闭”，按不安全处理。
_Avoid_: 独立仓门关闭状态、直接检测仓门打开、操作员目视确认、根据开锁输出反推门已锁闭、未知时推定锁闭

**开锁输出回读（UnlockOutputReadback）**:
车载上位机从 IO 模块读取的开锁 DO 实际状态；只有回读确认为复位（无效）时，才证明控制端没有继续施加开锁信号。
_Avoid_: 最后一次写入值、软件期望值、仅凭脉冲计时结束推断复位

**SlotOccupancyState（仓位占用状态）**:
车载上位机根据仓内光幕及其数据有效性归一化得到的 OCCUPIED、EMPTY 或 UNKNOWN；有效遮挡表示有货，有效无遮挡表示空仓，光幕故障或 IO 数据无效时必须为 UNKNOWN。8005 的仓内光幕只用于检测物体，不是人员安全光幕，也不构成车辆移动安全联锁。
_Avoid_: 光幕原始 DI、操作员口头确认、业务仓位内容、人员安全光幕、移动安全联锁

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

**UnmappedPackageCoverage（未覆盖 PACKAGE）**:
TransportDemand 的 `PACKAGE` 有值、但没有匹配到已批准花篮容量规则的覆盖缺口；它不影响 TransportDemand 的生成或保留。8005 任务/装货准备模块必须形成 LoadPreparationAlert，逐条保存全部受影响记录，并按 PACKAGE 汇总为可追踪表格；MesIngest 只原样保留 PACKAGE，不负责容量覆盖报警。容量规则补齐前，服务端无法形成 ExpectedBasketCount，必须在仓位分配和开锁前阻断。不得用默认容量、相似名称或人工估算静默补齐。
_Avoid_: PACKAGE 缺失、删除未覆盖需求、默认容量、只保留去重名称而丢失明细

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
StopClosureCommit 前，已核验操作员针对放错产品且已经锁闭的已装仓位发起、服务端在原仓位操作尝试编号下授权、车载端安全执行 `OCCUPIED→EMPTY→OCCUPIED` 原仓位更换并追加审计的恢复过程；它是普通存放错误唯一的系统纠正窗口，不撤销或改写已经形成的 LoadBatch 提交事实。纠错期间退出 StationDepartureWaiting 并停止离站倒计时，重新安全闭环后从完整时长开始；车辆离站后不再提供存放纠正。
_Avoid_: OperationCancel、LoadCompensationRecovery、撤销 LoadBatch 提交、整批清空

**CorrectionId（纠错编号）**:
一次 LoadCorrection 请求、授权与结果的稳定业务身份；它绑定原 DemandId、SlotOperationAttemptId 和原仓位范围，相同编号内容不得变化，也不能创建新的装货尝试。
_Avoid_: MessageId、替代 SlotOperationAttemptId、换仓、重放时换编号

**LoadCorrectionPending（装货纠错待重放）**:
错误花篮已经从原仓位取出、但正确花篮尚未重新放入时的可恢复等待态；原任务、SUBLOT、目标仓位、提交事实和 StationOperationGuard 均保持，后续装货暂停，只能继续在原仓位重放或转为清空并取消。
_Avoid_: 纠错成功、部分装货成功、自动取消、恢复后跳过该仓位

**CurrentStopWorklist（当前停靠作业清单）**:
服务端向车载界面提供的当前停靠只读业务投影，包含本次停靠已排定的待装任务和车上目标为当前站点的待卸任务；车载端可以展示并提交操作请求，但不拥有任务事实。
_Avoid_: StationTaskProjection、仅待装任务列表、全局可准入任务列表、车载任务库

**CurrentStopWorklistSnapshot（当前停靠作业清单快照）**:
服务端针对当前 AGV 与站点生成的带 worklistRevision 完整作业投影；车辆到站、作业变化、任务取消、临时 SUBLOT 获准纳入或重连时整表下发，车载端只接受更新版本并整体替换显示。
_Avoid_: StationTaskListSnapshot、增量增删事件、车载端合并任务、无版本列表

**装货任务入口模式（LoadTaskEntryMode）**:
服务端维护、带版本且全项目统一的装货入口选择，只能是 `SUBLOT_ENTRY`（扫码或键盘输入 SUBLOT）或 `WORKLIST_SELECTION`（从最新 CurrentStopWorklist 选取待装 DemandId）；界面任一时刻只呈现当前模式，已开始 Sublot 固定沿用开始时版本。
_Avoid_: 两种入口同时显示、按车辆或站点切换、车载端自行切换、切换后改写活动 Sublot

**作业清单选任务（WorklistTaskSelection）**:
`WORKLIST_SELECTION` 模式下，当前站点有权且已核验的现场操作员从最新 CurrentStopWorklist 选择可开始的待装 DemandId，并在核对完整 SUBLOT、任务类型、起终点及应装花篮数后确认；服务端以最新 worklistRevision 复核通过前不得开门。
_Avoid_: 一点即开门、从过期清单开门、选择仓位代替选择任务、班组长逐次批准

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
服务端为当前 AGV 排定的后续业务停靠序列；车辆已经驶向的当前下一站是本次移动的已承诺停靠，执行中出现的新 TransportDemand 不得改变它，但经完整业务准入后可以加入或调整其后的未执行停靠。车载界面只读展示接下来去哪些站点以及各站作业目的，不据此自行规划或编辑路线。
_Avoid_: RIoT 路线、固定不可变行程、行驶中改变当前下一站、空仓或距离近即自动追加任务、车载端推导路线

**UpcomingStopPlanSnapshot（后续停靠计划快照）**:
服务端生成的带 planRevision 完整后续停靠投影；计划增删、换序或状态变化时整体替换，断线后最后版本只能作为明确标记过期的只读信息。
_Avoid_: 逐站增删事件、无版本计划、离线可执行路线

**PlannedStopMutationBoundary（计划停靠变更边界）**:
车辆正在驶向的当前下一站不可删除或换序；其后的未执行停靠可在满足 DispatchZoneContinuity 和既有 Demand 延迟保护时调整，尚未取货且已取消的 Demand 可以移除，但任何已装车 Demand 的目的站必须保留到卸货完成。
_Avoid_: 行驶中改当前下一站、删除已装车 Demand 的目的站、取消一个 Demand 即删除仍有作业的停靠、无门禁任意换序

**EnRoutePickupDeliveryDelay（顺路取货配送延迟）**:
评估向当前车辆追加新 TransportDemand 时，新计划相对追加前计划对任一既有 Demand 预计到达其终点时间造成的最大增量；既有 Demand 无论已装车或仅已被当前计划接受都受保护，无法可靠计算任一增量时不得追加。
_Avoid_: 新任务离车辆的距离、行程总时长增量、只检查首个或已装车 Demand、无法计算仍按顺路处理

**OnboardVehicleOverview（车载车辆概览）**:
车载界面并列呈现运行、通信与业务就绪、当前作业、安全与联锁四个维度的组合视图；前三类使用相应权威投影，本车安全与联锁始终以车载实时 IO 事实为准。
_Avoid_: 单一车辆状态枚举、用业务状态覆盖安全状态、全部状态来自同一数据源

**StationTaskTypeAdmission（站点任务类型准入）**:
服务端维护的 stationId 与 taskType 多对多允许关系；存在 `(stationId, taskType)` 记录才允许在该站点输入对应任务的 SUBLOT，缺失、未知或未配置均默认拒绝。
_Avoid_: 按任务原站点判断、车载端白名单、同时维护两套正反向配置

**VehicleTaskTypeAdmission（车辆任务类型准入）**:
服务端维护的 agvId 与 taskType 多对多允许关系；只有存在 `(agvId, taskType)` 的 TransportDemand 才能把该车作为承载候选，缺失、未知或未配置均默认拒绝。同一车辆获准的多个任务类型可以同时承载，无需另设类型配对表；它不分配具体 DemandId，也不替代 StationTaskTypeAdmission。
_Avoid_: 指定单条 Demand 的长期配置、默认所有车辆承载全部任务类型、任务类型配对矩阵、StationTaskTypeAdmission

**DispatchZone（调度分区）**:
客户在一张 RIoT Map 内对 8005 可执行 MES AREA 维护的业务分组，用于同时确定 AREA 执行范围以及约束、偏好车辆候选；每个 DispatchZone 只归属一个以 mapId 标识的 Map，TransportDemand 仍覆盖全厂，只有其 MesAreaEndpoint 的 AREA 存在有效 DispatchZoneAreaAssignment 时才进入选任务范围。
_Avoid_: 跨 Map 分区、对全厂 TransportDemand 强制分区、车辆当前位置分区、路线分区

**DispatchZoneAreaAssignment（调度分区 AREA 归属）**:
一个 MES AREA 到一个 DispatchZone 的有效正向映射；存在映射表示该 AREA 属于 8005 执行范围，并同时确定其调度分区与 AreaSlotPositionAssignment，缺少开门侧指派的映射不成立；未映射 AREA 的 TransportDemand 在选任务时静默跳过且不报警。
_Avoid_: 未映射即配置异常、自动猜测分区、为范围外 AREA 报警、从 MesIngest 删除 Demand、脱离本映射另维护一份 AREA 开门侧表

**AreaSlotPositionAssignment（区域号仓位位置指派）**:
DispatchZoneAreaAssignment 为每个纳入 8005 执行范围的 MES AREA 指定的唯一 SlotPosition 分组，表示车辆为该 AREA 的 Demand 装货或卸货时只能开启这一组仓门；纳入执行即必须指派，未映射的 AREA 不需要指派。以 AREA 而非站点为键，因为站点可删除重建而 AREA 稳定：站点删除重建或 AREA 换到其它站点时，指派原样沿用。开哪一组只由 Demand 的 AREA 决定，与停靠的站点无关：同一站点可以挂指派了不同分组的 AREA，车辆在一次停靠内为各 Demand 分别开启各自的分组，系统不按站点检查指派是否一致。Demand 在分配仓位时冻结当时的指派，之后的指派变化不改变已冻结的 Demand。
_Avoid_: SlotSide、开门侧绑定站点号、从站名、车辆朝向或站点朝向推导、从停靠站点推导开哪组、按站点检查开门侧一致性、要求一个站点只挂一组 AREA、为未映射 AREA 要求指派或报警、在途 Demand 随指派变化改开另一组

**DispatchZoneEnRoutePickupPolicy（调度分区顺路取货策略）**:
每个 DispatchZone 独立规定途中追加本区新 TransportDemand 时允许的最大 EnRoutePickupDeliveryDelay；值为零或未配置表示本区禁止途中追加，不继承全项目默认值。
_Avoid_: 全项目统一延迟、未配置即自动允许、距离阈值、路线实现参数

**DispatchZoneContinuity（调度分区连续性）**:
同一 UpcomingStopPlan 中属于同一 DispatchZone 的 TransportDemand 必须形成一个连续区段；车辆离开该分区区段后，本轮计划不得再次返回该分区。跨分区只允许在同一 Map、车辆通过各分区硬准入且满足其它业务门禁时单向推进。
_Avoid_: A→B→A 分区往返、以软偏好代替连续性、跨 Map 分区组合

**DispatchZoneVehicleAdmission（调度分区车辆准入）**:
某调度分区允许服务车辆的硬边界；只有明确获准的 AGV 才能承接归属该分区的 TransportDemand，距离近、顺路、空仓或等待过久均不能扩大该集合。
_Avoid_: 分区车辆偏好、自动跨区借车、以排序权重代替准入

**DispatchZoneVehiclePreference（调度分区车辆偏好）**:
在已经通过 DispatchZoneVehicleAdmission 且落入同一 RouteCostEquivalenceBand 的车辆中表达优先选择的显式软层；非优先车辆仍是准入范围内的回退候选，偏好层可省略，不能覆盖硬准入或把明显更远车辆拉入同层。
_Avoid_: 扩大分区准入、偏好车辆不可用即跨区、自由数值调度权重、偏好压过明显路径成本差、软硬模式开关

**DispatchRankingTier（派车排序层级）**:
任务与车辆通过全部硬准入后采用的字典序比较层；高层结果先于低层因素决定候选顺序，低层因素不得以权重抵消已经确定的高层优先级。
_Avoid_: 单一综合评分、跨层权重抵消、把硬门禁折算为软分数

**TaskFirstDispatchSelection（任务优先派车选择）**:
每轮先按派车排序层级确定最高优先的单个 TransportDemand 或已批准复合任务集合，再只为该任务选择合格车辆；不得先挑空闲车辆再从其附近任务中反向选择。
_Avoid_: 车辆优先选任务、最近任务优先于任务层级、空闲车辆自行挑单

**UnassignedDemandBacklog（未分配需求积压）**:
当前没有车辆能够立即承接或合法追加时，TransportDemand 保持在共享未分配集合中并持续累积 TransportDemandWaitingAge；不得预绑定或为某台忙车排专属队列，任一车辆容量或状态变化后重新执行 TaskFirstDispatchSelection。
_Avoid_: 忙车专属任务队列、未来车辆预留、等待车辆时暂停老化、后来空闲车辆不能接手

**StructuralDispatchBlock（结构性派车阻断）**:
地图不一致、站点缺失、全部路线不可达、必要准入配置缺失，或 ExpectedBasketCount 超过所需 SlotPosition 分组物理仓位数等使 TransportDemand 不存在任何潜在合法车辆的状态；它必须立即形成按任务与原因去重的告警并持续更新，不等待防饥饿阈值。车辆只是忙碌、容量暂满（含所需分组暂时空仓不足）或单车位站点暂被占用属于 UnassignedDemandBacklog，达到分区批准阈值后才升级告警。
_Avoid_: 暂时没空车即结构性阻断、结构性无解仍等待老化阈值、每轮重复新建相同告警、告警后绕过门禁、把所需分组暂时空仓不足当作结构性阻断、把仓位临时禁用造成的不足当作超出分组物理仓位数

**TransportTaskTypePriorityBand（运输任务类型优先级带）**:
运输任务类型在派车排序中的初始业务层级；`STAGING_TO_WIRE` 单独处于最高带，其余五类任务处于同一普通带，普通带内部不再凭任务类型区分先后。
_Avoid_: 为其余五类臆造优先顺序、把任务类型优先级折算为可被低层因素抵消的分数

**DispatchStarvationPromotion（派车防饥饿升级）**:
TransportDemandWaitingAge 达到批准阈值后进入高于所有未超时任务类型优先级带的排序层；超时任务之间按等待时长排序，升级不改变或绕过任何任务、车辆、站点与安全硬准入。
_Avoid_: `STAGING_TO_WIRE` 永久压住普通任务、超时自动绕过门禁、超时任务随机排序、清零后重新等待

**DispatchStarvationThresholdCalibration（派车防饥饿阈值标定）**:
每个 DispatchZone 依据现场车辆从接受任务到再次具备接单资格的完整周期独立标定一个 DispatchStarvationPromotion 阈值，周期必须包含空驶、运输和全部人工装卸时间并由当前基线最终批准人确认；同一区内所有任务类型共用该阈值，系统不提供通用默认值或 1～3 分钟上限，未批准阈值时只累计 TransportDemandWaitingAge、不执行跨任务类型升级。标定证据须同时报告完整任务周期与本地建单至成功绑车等待的中位数、P95、最大值，以及采样期车辆数、任务量和人工装卸情况；系统不自动把任一统计值或倍数设为阈值。
_Avoid_: 全项目统一阈值、按任务类型设置不同阈值、开发期拍定分钟数、只测纯行驶时间、沿用 1～3 分钟假设、未标定即启用升级

**PublicStationIncumbentPreference（公共站点在点车辆优先）**:
已经占用某个 FixedTaskStation 的车辆，在通过全部安全、业务、能力和分区硬准入后，只对货物实际取货起点就是该站点的 TransportDemand 取得一个高于非在点车辆的 DispatchRankingTier；它不是硬准入，公共站点只是任务终点时不适用，在点车辆不合格时自然比较下一层的其他合格车辆。
_Avoid_: 公共点车辆永久归属、公共点在点硬门禁、以在点覆盖硬门禁、在点车辆不合格即阻塞任务、车辆位于任务终点也视为就地取货、普通距离加分

**VehicleMarginalRouteCost（车辆新增行程成本）**:
把已选 TransportDemand 或复合任务集合分配给某台合格车辆后，相对该车分配前既有计划增加的预计行程代价；满足途中追加门禁的在途车辆与空闲车辆均以此参加同一选车比较，不因“在途”或“空闲”身份自动优先。该增量自插入位的前一站起算而非自车辆物理位置起算——车辆当前位置到其计划下一站的行程在插入前后完全相同，做差时必然抵消，故计划锚给出的是精确增量而非近似；无既有计划的车辆锚在其当前所在站点，不在任何站点上时该车本项证据缺失。
_Avoid_: 车辆到最近任务的直线距离、空闲车固定优先、在途车固定优先、覆盖 EnRoutePickupDeliveryDelay、以车辆物理位置为锚计算增量、以直线距离补齐锚不到站点的车辆

**RouteCostEvidenceBoundary（路径成本证据边界）**:
可达性由 StationReachability 判定，判为不可达的车辆退出本轮候选且属常态；可达性已经确认但 VehicleMarginalRouteCost 缺失、过期或不可比较时，保留该车并跳过路径成本排序层、记录原因后继续比较后续层。RouteGraphSnapshot 整体陈旧时可达性同样无法确认，本轮不派车。任何直线距离或弱替代值都不得冒充路径成本；快照陈旧导致的证据缺失才是少见异常边界，图上不可达不是。本边界只管选车阶段的排序与候选筛选，不含建单前置可达确认——后者仍由实时 RIoT RouteCost 承担，见 ResolvedTransportStation。
_Avoid_: 可达性未知仍派车、直线距离证明可达、图上不可达即告警、个别车排序成本缺失即整轮停派、以陈旧快照的成本继续排序、弱替代冒充路径成本

**RouteCostEquivalenceBand（路径成本等价带）**:
同一 DispatchZone 内经现场批准的 VehicleMarginalRouteCost 容差；明显更低的新增行程成本仍优先，差值落入容差的车辆视为同一排序层，依次比较 DispatchZoneVehiclePreference、距离上次成功接单时间及 DispatchBatteryEligibility 的末级电量裁决。未批准非零容差时按零容差运行而不阻断派车，只有成本完全相同才进入后续层；它不覆盖任务防饥饿、容量、顺路延迟或其它硬门禁。
_Avoid_: 未批准容差即停派、默认猜测非零容差、较远车辆固定轮转、自由数值调度权重、车辆公平性压过任务优先级

**DeterministicDispatchTieBreak（确定性派车并列裁决）**:
任务业务层全部相同时按本地创建时间、再按 DemandId 稳定排序；车辆业务层全部相同时优先从未成功接单者、再按上次成功接单时间从早到晚、最后按 agvId 稳定排序。同一输入必须得到同一结果，不使用随机选择。
_Avoid_: 随机派车、依赖数据库未声明顺序、最终并列时人工抢单、同一输入结果漂移

**DispatchBatteryEligibility（派车电量资格）**:
车辆当前电量必须高于 MandatoryChargeEntryThreshold，且预计完成已选任务后仍不低于经批准的最低任务后电量余量，才可进入选车候选；任务执行中越过充电入口阈值不打断当前任务，完成后立即进入待充电流程。电量未知或任一条件不足时 fail-closed 排除，通过后电量只在其它选车层全部相同时以预计任务后余量较高者裁决。
_Avoid_: 达到充电入口阈值仍接普通新任务、执行中低电转去充电、当前电量直接代替任务后余量、电量未知按正常、低电量软扣分后仍派车

**MandatoryChargeEntryThreshold（强制充电入口阈值）**:
空闲车辆当前电量达到或低于该阈值时，必须停止承接普通新任务并进入待充电流程；该阈值不得低于 DispatchBatteryEligibility 使用的最低任务后电量余量，以免形成既不能接单又不触发充电的电量区间。
_Avoid_: 建议充电软阈值、达到阈值仍接普通任务、任务执行中途强制转充电、低于最低任务后余量的充电入口

**ChargingCompletionThreshold（充电完成阈值）**:
车辆充电电量达到该阈值时开始正常结束本次充电；它必须严格高于 MandatoryChargeEntryThreshold，但达到阈值本身不证明订单已经收敛、车辆已经离桩或充电桩预占可以释放。
_Avoid_: 与充电入口相等的完成阈值、达到电量即视为离桩、达到电量即释放充电桩、充电桩空闲证明

**ManualChargingHold（人工充电保持）**:
WIRE_TO_GATE MVP 在已知低电或预计任务后余量不足时为车辆建立的非业务状态；它阻断普通新任务与新的 8005 移动意图，但不表示系统已经选桩、建单、控制或确认充电。执行中的运输先安全完成，电量未知则保持独立的事实未知阻断而不冒充本状态。
_Avoid_: 自动充电周期、电量未知、任务中途转去充电、选择充电桩、达到阈值即自动解除

**ManualChargingReturnToService（人工充电重新投运）**:
维护管理员或系统管理员以个人身份请求结束 ManualChargingHold 后，由服务端根据新鲜的完成阈值、非充电、停稳、订单收敛、位置、能力及安全事实重新授予 VehicleBusinessReadiness 的受控过程；请求或电量上升本身都不是重新投运结果。
_Avoid_: 普通操作员放行、遥测自动放行、充电完成即接单、跳过恢复对账

**ChargingPolicyVersion（充电策略版本）**:
面向车辆或受控车辆分组激活的不可变策略，固定 DispatchBatteryEligibility 的最低任务后电量余量、MandatoryChargeEntryThreshold、ChargingCompletionThreshold、ChargingProgressObservationPolicy 和候选充电桩集合；具体参数是投运前必须以车辆电池规格、典型任务耗电、最远安全返回距离、遥测精度、正常充电曲线和现场测试证据批准的现场配置，需求基线不写死数值，也不允许开发默认值。编辑草稿与激活新版本均不要求先禁用车辆；新版本只用于激活后的新派车决定和新充电周期，既有搬运任务以及已经排队、预占、建单或充电的周期继续使用各自固定的原版本，空闲车辆在激活后立即按新版本重新判断，无已批准版本的车辆不得投运。
_Avoid_: 基线虚构统一百分比、开发默认值、无批准版本投运、在线覆盖当前策略、修改即中断任务、修改即撤销预占、正在充电时切换完成阈值、保存草稿即生效、修改策略必须停用整车

**ChargingProgressObservationPolicy（充电进展观察策略）**:
ChargingPolicyVersion 中用于确认充电是否实际取得电量进展的受控参数组合，包含开始充电后的稳定期、连续观察窗口和窗口内最小电量增量；只有车辆持续处于 `batteryState=CHARGING`、身份绑定一致、遥测连续新鲜且尚未达到 ChargingCompletionThreshold 时，完整窗口内增量不足才形成已确认无进展。任一失联、数据缺口、读取失败或事实冲突都只形成结果未知，不得冒充无进展。
_Avoid_: 单次电量不变、全车型通用分钟数、未标定默认增量、数据缺口算零增长、失联即无进展

**已确认充电无进展（ConfirmedChargingNoProgress）**:
满足 ChargingProgressObservationPolicy 的完整观察条件后，确认车辆虽持续报告正在充电但未取得经批准最小电量增量的业务事实；首次确认即同时触发原桩 ChargingStationAllocationHold 与车辆 VehicleChargingEligibilityHold，结束并核验当前充电后进入既有清桩流程，不重复观察、不在原桩自动重启，也不换桩试充。停止结果未知时保持车辆原位、原预占与两侧暂停，直至对账或现场处置取得可核查结果。
_Avoid_: 单次零增长、重复观察到低电、原桩自动重启、换桩诊断、停止结果未知时清桩或释放预占

**ChargingRIoTVehicleObservationLoss（充电车辆 RIoT 观测失联）**:
充电周期中无法从 RIoT 取得车辆位置、订单、运动或充电状态的结果未知状态；它立即阻断该车新业务与充电资格并保持原充电桩预占，按车辆仍可能占据桩位处理，但不发送依赖未知前置条件的新停止、重启或移动命令，也不把充电桩登记为故障。持续时间只按受控运维阈值提升告警与现场响应紧迫度，永远不自动结束订单、释放预占或改派；恢复观测或取得授权现场事实后必须完成对账，只有明确证明非预期停止才升级为 ConfirmedChargingInterruption。
_Avoid_: 失联即充电中断、失联即充电桩故障、超时结束订单、超时释放预占、失联时盲发停止或移动、恢复通信即推定正常

**ChargingBatteryTelemetryLoss（充电电池遥测缺失）**:
车辆位置、订单及其它运行事实仍可取得，但 `batteryState` 或电量当前无法读取的充电进展未知状态；期间暂停 ChargingCompletionThreshold 与 ChargingProgressObservationPolicy 的判断并保持原订单和预占，持续时间只升级告警而不自动结束、释放或改派，数据恢复后只以新的连续样本重新开始观察，不用缺失前旧值补算窗口。
_Avoid_: 遥测缺失算零增长、旧值当当前值、遥测恢复后补算缺口、超时自动结束或释放、仅凭电池数据缺失判定车辆或充电桩故障

**DispatchSlotEligibility（派车仓位资格）**:
车辆只有在每条 Demand 所需 SlotPosition 分组内的可用仓位数量、规格、载重及当前已载任务兼容性全部满足已选单个或复合任务集合时才可进入候选；其它分组的空仓不计入，通过后不因剩余空仓更多而取得排序优势。
_Avoid_: 仓位不足软扣分后仍派车、剩余空仓越多越优先、把车型不兼容折算为评分、按整车空仓总数判断容量、一条 Demand 跨分组拆装

**StationSlotAccessConstraint（站点仓位开启约束）**:
车辆停靠 AREA 机台站点时，装货与卸货都只允许开启该 AREA 的 AreaSlotPositionAssignment 分组内的仓位；关卡、烘箱、三光、氮气柜以及作为卸货点的派工待送不受此约束。
_Avoid_: 只约束卸货、只约束装货、公共站点单侧开门

**DestinationSlotPositionLoading（按目的地定装货仓位）**:
在公共站点装载送往 AREA 机台的 Demand 时，两组仓门都可开启，但该 Demand 的全部花篮必须装入目的 AREA 被指派的 SlotPosition 分组，不得跨组拆分。
_Avoid_: 按装货点就近装、先装后调仓、跨组拆装一条 Demand、把清洗间或氮气柜当作独立的集中装货点

**SlotPositionGroupFull（仓位分组装满）**:
多需求装货中，车辆的某个 SlotPosition 分组已无空仓，或存在一条除该分组空仓外其余准入全部通过、只因车上已装或已预留的货物占用该分组仓位而无法整批装入的候选 Demand 的状态；它只表示这一组装不下，其它分组照常接单。被其它门禁拒绝、ExpectedBasketCount 超过该分组物理仓位数或因本车仓位禁用而装不下的候选不构成分组装满。
_Avoid_: 前侧装满即整车装满、被其它门禁挡住的候选也算装不下、超大 Demand 触发装满、按整车空仓总数判断、八仓全满才算装满

**VehicleFull（车辆装满）**:
多需求装货中，车辆的全部 SlotPosition 分组都处于 SlotPositionGroupFull 的状态；进入后车辆不再等待新 Demand，完成已承诺的待装 Demand 后前往卸货，但在离开当前计划最后一个装货停靠之前出现能够装入的候选仍可追加，追加后重新判断。
_Avoid_: 一侧装满即出发、有候选装不下且此刻没有其它候选即出发、按整车空仓总数判满、装满即取消已承诺的待装 Demand、装满后原地等待

**CargoHoldingWait（持货等单）**:
车辆载有货物、装货阶段未结束且尚有 SlotPosition 分组未装满时，停在最后装货的站点等待能够装入的候选 Demand 的状态；某分组暂无候选与车辆完全没有候选都属于此状态。期间能够装入的候选照常追加，状态在 VehicleFull、持货超时或 WaitingStationYield 时结束；车辆能够服务的 DispatchZone 均禁止途中追加时不进入此状态。
_Avoid_: 零候选即出发、前往等待点等单、空载等单、在禁止途中追加的分区空等、把等单时长计入 EnRoutePickupDeliveryDelay、持货超时后继续等单

**WaitingStationYield（等单让站）**:
处于 CargoHoldingWait 的车辆所停站点被任一其它车辆承诺为下一停靠（装货或卸货）时，该车立即结束等单与装货阶段、不再接受新的待装 Demand 并前往卸货的规则；它不打断任何阻断离站的作业或异常状态，须待其安全收敛并通过离站安全核验后才移动，也不阻止其它车辆被派往该站。
_Avoid_: 对方车辆到站才让站、驱赶正在装卸或录入的车辆、让站即站点独占、让站后继续接单、为等单车辆设派车优先权

**MapDispatchEligibility（地图派车资格）**:
TransportDemand 所属 DispatchZone 的 Map 与 AGV 当前所在 Map 必须是同一个 mapId，车辆才能承接该 Demand；无法确认车辆当前 Map 时，该车退出全部派车候选并产生车辆级状态提示，重新取得明确 Map 后恢复参与。任务类型、分区车辆准入、距离近、路线可达或存在空仓均不能覆盖地图不一致或未知。
_Avoid_: 跨 Map 派车、地图未知仍派车、只按地图名称判断、以路线可达代替当前地图一致

**AdmissionDecisionSnapshot（准入决定快照）**:
服务端在 OperationCommitPoint 前按当前 StationTaskTypeAdmission 再次校验并冻结的 stationId、taskType、规则版本和允许结论；后续规则变更不撤销已经发出的仓位操作。
_Avoid_: 每个仓位执行前重新准入、配置变更中断当前操作、无版本审计

**AdmissionPolicyStore（准入策略存储）**:
服务端数据库中的 StationTaskTypeAdmission 当前关系、单调 admissionPolicyVersion 和变更审计；第一版由软件人员通过受控部署脚本或原子导入维护，不提供运行时配置界面。
_Avoid_: 车载配置文件、手工无审计改库、双端各存一份

**LoadTaskCancellation（装货任务取消）**:
车辆离站前由已核验操作员针对一个 DemandId 发起的任务终止流程；未产生物理装载时可直接终结，已经部分或全部装载时，对该任务实时确认为 OCCUPIED 的目标仓位执行批量开锁并全部清空，最终使该任务完整目标仓位范围均达到 EMPTY、由锁传感器确认锁闭且开锁输出回读确认为复位。其它 SUBLOT 的仓位、任务与确认记录不受影响；但同车另一 SUBLOT 尚处于物理装货或清空过程中时不得穿插本次取消，必须等待其完成或取消到稳定边界。服务端可靠接受 ALL_EMPTY 并发布新版作业清单后，释放仓位可以用于新的 SUBLOT。获得服务端取消授权时尚未锁闭的当前装货仓位可以直接取出并以 EMPTY 安全收尾；正式提交后发起取消属于保留原确认与提交事实的补偿，不是撤销或抹除历史。
_Avoid_: 瞬间撤回 SlotOperationCommand、只清空所选任务的部分仓位、取消一个 SUBLOT 时整车清空、车辆离站后的普通取消

**CancellationId（取消编号）**:
一次 LoadTaskCancellation 请求、范围授权、物理清空和业务终结的稳定身份；它绑定一个 DemandId 与服务端冻结的完整目标仓位范围，重复传输不得扩大或改写范围。
_Avoid_: MessageId、TransportDemandKey、跨 Demand 复用、取消中途换范围

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

**操作员工号识别（OperatorNumberIdentification）**:
操作员手工输入工号并由服务端校验其有效性后形成的本站操作者声明；它不是账号密码登录，也不能证明输入者就是工号本人。
_Avoid_: 操作员登录、操作员认证、工号密码

**普通操作权限（OperatorAccess）**:
由有效操作员工号在当前 OperationSession 内取得的低风险生产操作范围，只覆盖本车、本停靠及其关联 Sublot 和仓位，并允许请求本车急停；任意开锁、硬件或 IO 测试、映射维护、仓位或车辆管理禁用、异常恢复、急停解除、系统配置和全车队管理均不属于该权限。
_Avoid_: 维护权限、管理员权限、整车任意开仓、跨车辆操作

**当前停靠仓门操作权限（CurrentStopSlotAccess）**:
普通操作员在 OperationSession 有效且 StopClosureCommit 尚未形成时，只能开关本次停靠中待处理或正在处理的 Sublot 所关联仓位；这些仓位的处理顺序和重复开关次数不受固定顺序限制，但整车其它仓位以及已经不属于本次待处理范围的仓位不得凭普通操作权限开启。StopClosureCommit 形成后，该权限立即结束。
_Avoid_: 整车任意开仓、跨停靠开仓、完工后继续使用普通操作权限、固定逐仓顺序、只允许开门一次

**车载操作员上下文（OnboardOperatorContext）**:
车载上位机持久化的当前经服务端有效性校验的申报工号及校验引用；新装货 Sublot 默认沿用，用户只可在没有活动或待服务端确认的 Sublot 时主动更换且新工号必须重新经服务端校验。掉线、重启不清除；服务端提交 StopClosureCommit 后清除，不等待车辆实际开始移动。卸货身份核验策略关闭时不要求也不虚构操作员。
_Avoid_: 每个仓位重新输入、掉线自动清除、同一 Sublot 中途换人

### 需求基线治理

**首版发布前补充证据快照（PreReleaseSupplementalEvidenceSnapshot）**:
首个正式需求基线尚未发布时，对初始证据快照之后新增或变化的需求性材料建立的独立、不可变证据观察；它保留自己的截止时间、Git 与工作区身份、逐文件哈希和分类结果，不修改初始快照，也不自动批准其中内容进入基线。
_Avoid_: 改写初始快照、只补一份已知规格、补拍即批准、用当前工作树覆盖历史观察

**首版前来源替代（PreBaselineSourceSupersession）**:
首个正式需求基线发布前，后续获批来源对较早来源中的同一义务作出的修改、废弃或本质替代关系；首版只收录最终有效规范义务，证据保留完整来源层叠与精确差异，但不为从未成为正式基线要求的旧语句虚构永久 REQ 身份。
_Avoid_: 发布明知过时的历史首版、把较新时间自动当作替代证据、为未入基线旧语句伪造 deprecated REQ、丢失来源差异

### 可追溯性

**OnboardTechnicalLog（车载技术日志）**:
车载上位机保存的 IO 通信、信号变化、安全判断、执行阶段、配置和本地异常证据。
_Avoid_: 服务端业务审计、每轮 IO 数据全量上送

**车载技术日志留存策略（OnboardTechnicalLogRetentionPolicy）**:
OnboardTechnicalLog 自产生起至少保留 30 天，车载存储须按验收负载配置到足以满足该期限，容量限制不得提前覆盖未满 30 天的记录；关键安全与业务事件仍须实时摘要到 ControlServer，并按业务审计留存策略保存。
_Avoid_: 容量先到先删、只保留错误不保留上下文、用车载日志替代服务端审计、全部原始 IO 持续上送

**BusinessAuditRecord（业务审计记录）**:
服务端保存的人员、会话、仓位业务、上下层命令结果、调度动作和异常处置记录。
_Avoid_: 车载原始 IO 日志、普通界面进度

**业务审计留存策略（BusinessAuditRetentionPolicy）**:
BusinessAuditRecord 与 AdministratorActionAuditRecord 自写入起至少在线保留 180 天并可查询、导出，容量限制不得导致未满 180 天的记录提前删除；超过 180 天后的继续保留、归档或清理由系统管理员配置，变更本身必须形成管理员操作审计记录。
_Avoid_: 容量满即提前删除、管理员手工删除单条记录、未审计修改留存期、用车载技术日志替代业务审计

**操作确认与实物不一致（OperatorConfirmationMismatch）**:
系统控制链完整且正确时，操作员确认的 WorklistTaskSelection 与事后查明的实际装入 SUBLOT 不一致的审计分类；它关联确认人供调查，但不单凭确认记录证明实际放货人或自动作纪律、法律定责，控制链或现场证据不完整时保持责任待查。
_Avoid_: 操作员自动有责、确认人必然是实际放货人、系统异常归责现场、证据不足强制定责

**LoadCompensationChoice（装货整批清空选择）**:
LoadBatch 因关键硬件故障暂停后，异常处置人员在 ExceptionRecoverySession 中选择“不再继续原装货、改为整批清空”并填写 LoadCompensationReasonCode 的操作意图；它不需要审批或再次认证，也不因选择而立即取消任务，系统仍须在目标范围和物理清空闭环成立后提交终态。
_Avoid_: LoadCompensationDecision、审批、逐动作二次认证、无原因选择、自由文本代替原因码、选择即任务终态

**LoadCompensationReasonCode（装货整批清空原因码）**:
LoadCompensationChoice 的首版受控原因枚举：`HARDWARE_NOT_RECOVERABLE_ON_SITE` 表示现场无法恢复故障车辆并继续原装货，`PRODUCTION_ABORTS_CURRENT_LOAD` 表示现场选择不再继续本次装货，`OTHER` 表示其它原因且必须填写非空备注。原因码只解释为何清空，不改变补偿完成后终结原搬运需求的统一后果。
_Avoid_: 硬件故障点位码、自由文本原因、空原因、未知原因码

**LoadCompensationRecovery（装货补偿恢复）**:
LoadBatch 暂停后，异常处置人员在会话中作出 LoadCompensationChoice，系统核验范围和安全门禁后引导取出该任务已经放入以及状态不确定的全部产品；全部相关仓位安全证明为空后，服务端释放整批预留并将原搬运需求终结为 `CANCELLED_BY_LOAD_COMPENSATION`，不再为该 DemandId 自动派车。
_Avoid_: 硬件故障自动触发、消息直接取消、逐仓部分入账、只取出失败仓产品

**LoadCompensationRequired（装货待补偿）**:
服务端接受有效 LoadCompensationChoice 后为暂停的 LoadBatch 保持的业务状态；它不是任一硬件故障的自动结果，须在同一异常处置流程中完成 LoadCompensationRecovery。
_Avoid_: 硬件故障自动转入、操作已取消、自动重新开门、允许车辆离站

**LoadCompensationCommand（装货补偿指令）**:
服务端在核验原操作确实处于 LoadCompensationRequired 后，使用原仓位操作尝试编号下发可靠恢复指令；它授权车载端按执行日志逐仓引导人工清空，不是通用 OperationCancelCommand。
_Avoid_: 新装货操作、离线清空、数据库回滚

**UnloadCompletionRequired（卸货必须完成）**:
车辆到达目的站并满足既有卸货安全条件后直接开始开仓卸货，不存在到站接收确认或操作员取消窗口；异常或人员尚未取货时只能保持卸货未完成、暂停或排障，车辆不得离开，直至所有目标仓位完成取空和锁门。RIoT 移动订单只按实际状态收敛，不因人员未取货而撤销。
_Avoid_: 到站取消、部分卸货后取消、把产品放回后回滚、人员未取货即释放车辆、因未取货撤销移动订单

**完工后业务差错（PostCompletionBusinessMismatch）**:
8005 本地任务已经完成并释放车辆后才发现的拿错、漏拿或存错；它不重开、回滚、纠正或改写原任务终态与原始审计，也不在 8005 内产生重送任务或新的 MES 运输需求。普通放错在离站后将错就错完成一对一输送，最多记录差错事实；只有产品因传感器、锁或车辆故障实际被困在仓内时才进入 ExceptionRecoverySession。
_Avoid_: 重开原任务、修改原完成时间、覆盖原审计、复用原任务补运、8005 回写 MES、把遗留物取出当作重送

**完工后遗留物取出（PostCompletionResidualLoadRecovery）**:
8005 已因仓内光幕漏检而把仓位判为空并结束本地任务、但产品实际仍锁在仓内时，在 ExceptionRecoverySession 的维护开门模式中对该物理仓位执行的受控取出。车辆必须停在任一普通站点、已停稳、满足开门安全条件且不在充电桩位置；充电桩会遮挡后侧仓门，因此不得执行遗留物取出，也不要求另设维护专用位置。目标仓位不得仍有服务端货物、任务绑定或未收敛仓位操作；取出后必须重新锁闭仓门并确认开锁输出复位。系统只在该仓位最近一次已完成操作唯一且此后没有其它仓位操作或任务绑定时自动附上原任务作为审计线索，无法唯一确定时不关联且不允许人工指定。该恢复不证明产品身份或传感器已验证取出，不重开原任务、不产生重送或新 MES 需求，也不修改 MES。确认遗留物漏检后立即隔离该仓位；异常处置人员完成检查并形成 HardwareRecoveryRecord，系统重新核验有效信号后才恢复。若无法证明故障仅限该仓位，则整车进入 VehicleRecoveryRequired；若其它仓位安全状态可独立证明，则仓门锁闭且开锁输出复位后只隔离故障仓位，不必整车停用。
_Avoid_: 普通操作员任意开仓、把维护开门等同普通操作权限、充电桩位置开仓、强制设置维护专用位置、人工猜选原任务、把自动关联当作产品身份、漏检后继续分配仓位、信号暂时恢复即重新启用、重开原任务、创建重送任务、8005 回写 MES

**维护开门模式（MaintenanceDoorAccessMode）**:
异常处置人员在 ExceptionRecoverySession 中使用的受控开仓能力；一次身份验证后可重复开关本事件范围内的多个合格仓位，不逐仓审批或重复认证。合格仓位是服务端没有活动 Sublot、运输任务、其它货物业务绑定或未收敛仓位操作的物理仓位；其 SlotOccupancyState 为 OCCUPIED 或 EMPTY 都不影响进入范围，OCCUPIED 且无业务绑定时另形成 SlotStateMismatch。每个实际开启的仓位仍须完成锁闭和开锁输出复位，模式期间整车保持停站并阻止新移动和仓位作业，退出后重新完成 PreDepartureSafetyCheck。
_Avoid_: 审批入口、逐仓重复认证、跨异常开仓、开启仍绑定 Sublot 或任务的仓位、以光幕状态覆盖服务端业务绑定、维护中移动车辆、未重新安全核验即继续移动

### 鉴权

> **获批端点的逐条清单在 [`docs/riot-call-allowlist.md`](docs/riot-call-allowlist.md)。** 本节的
> 词条定义分层与治理规则，那份文档才是「哪个 HTTP 方法 ＋ 哪条路径获批」的查阅入口，并且标注了
> 每一条的基线载体。需求基线仍是真相源，那份文档是它的汇编。

**RIoT 调用授权层级（RIoTCallAuthorizationTier）**:
8005 按每个具体 RIoT 操作的业务后果、可逆性和安全影响确定授权层级，并绑定接口、HTTP 方法、适用环境与 schema 版本；不能仅按只读或写入粗分风险。
_Avoid_: RIoT 读写分级、所有写接口同级、按 HTTP 动词推断授权

**观察与计算调用（ObservationAndComputationCall）**:
最低风险的 RIoT 调用层级，仅包含 8005 `DispatchLoop` 所需的 build、地图、站点、可调度车辆、指定车辆状态和订单状态查询，以及无副作用的 RouteCost、NearStationQuery、订单剩余路径代价、订单轨迹、代价单位和动态路由代价查询；设备全量清单、日志、配置、原始物模型和管理查询不属于本层。
_Avoid_: 所有 GET、所有查询接口、管理诊断接口

**RIoT 调用默认拒绝（RIoTCallDefaultDeny）**:
生产环境只允许 ControlServer 从具名 Facade 调用已批准的接口、方法、环境与契约版本；RawEscape、生成客户端和任意 URL 调用不向业务代码开放，重新生成 SDK 不自动扩大白名单。该限制只约束谁可调用 RIoT，不限制 ControlServer 连接车载端、数据库或其它已批准依赖。
_Avoid_: SDK 中存在即获准、只读即获准、ControlServer 只能连接 RIoT

**RIoT 调用授权治理（RIoTCallAuthorizationGovernance）**:
当前白名单由本次需求基线最终批准人批准；软件负责人或实施负责人可提案并可因风险立即收紧或暂停调用，但扩大白名单、降低安全门槛或恢复安全暂停必须再次取得最终批准人明确批准。已批准规则内的自动调用无需逐次人工审批。
_Avoid_: 实现即授权、负责人单方扩权、每次自动调用都人工审批、暂停等同永久删除

**RIoT 调用审计（RIoTCallAudit）**:
每次状态变更调用记录操作、目标、来源、原因、环境/build/快照、关联号、前后状态、传输与业务结果、重试及最终结论；车载匿名解除记为本地匿名确认，服务端按钮使用现有会话身份，所有秘密必须过滤。查询只审计失败、结果未知、安全异常和汇总指标，审计不替代状态回查也不作为请求重放源。
_Avoid_: 保存凭证明文、全量永久记录普通查询、用审计代替回查、从审计重放写请求

**常规建单调用（RoutineOrderCreationCall）**:
8005 唯一获准自动建单的 RIoT 调用层级，普通搬运、前往充电桩和其它已批准移动意图都只允许以稳定 upperId、已核验车辆、地图和目标站点通过 `byDefaultMissions` 创建，并须先确认车辆可调度、RouteCost 可达且未占用 RIoT 车辆订单名额。它有两种获准形态：普通搬运与空闲返回是**单段 move**；前往充电桩是 **`move(目标桩) + act(78, param1=1)`**，因为 8005 自建充电机制而不使用 RIoT 本体充电调度，离桩由下一张订单触发、`act(78,2,0)` 由 RIoT 自动插入。两种形态的稳定 upperId、门禁与对账要求完全相同。充电建单不设专属重试次数；结果未确认时保留车辆、充电意图、目标桩和预占的原绑定，统一按 RIoTRetryReconciliation 先对账后重试，不得换号、重新选桩、重复建单、提前释放预占或表示已经前往/开始充电。
_Avoid_: 任意建单、模板建单、订单组合、改单、优先插队、充电专属盲重试、结果未知时换桩换号、未确认即表示前往充电

**保护性任务干预（ProtectiveOrderIntervention）**:
在已批准保护条件成立时，8005 应用可自动调用 OrderHold 暂停本项目移动单，并须回查确认订单已进入 HELD；OrderContinue 不因暂停获批而自动获得调用资格。
_Avoid_: 暂停与继续同级授权、调用成功即视为已暂停、任意人工暂停

**受控业务终止（ControlledOrderTermination）**:
8005 应用只可依据已批准业务原因取消自身创建且能关联 TransportDemand 的订单，并使用回查确认的字符串 orderId；取消响应不代表终止完成，必须继续核验订单终态。
_Avoid_: 任意订单取消、跨系统订单取消、响应成功即取消完成

**RIoT 调用结果确认（RIoTCallOutcomeConfirmation）**:
查询与计算调用须验证传输、业务 code、必需字段、范围和新鲜度；状态变更响应只表示请求受理，须独立回查目标后置状态。超时无法确认时进入结果未知并停止依赖该结果的后续动作，先对账、仅在能证明安全时以原业务幂等标识重试。
_Avoid_: HTTP 成功即完成、业务 code 成功即状态已变、结果未知时盲目重试

**未识别物模型值（UnrecognizedThingModelValue）**:
RIoT 属性或服务结果出现未经已批准物模型版本与适用范围定义的原始值时形成的显式未知事实；8005 保留原值和来源上下文，只阻断依赖该语义的路径，无法继续证明车辆安全时才升级为整车业务阻断。`multiLoadState` 不属于 8005 消费范围。
_Avoid_: 默认枚举值、按缺号补义、丢弃原值、未知值即整车故障

**RIoT 重试对账（RIoTRetryReconciliation）**:
查询只对暂时传输/服务错误有限退避重试，鉴权、参数和普通业务失败不盲重试；建单先按原 upperId 对账且不得换号，状态变更先回查后置状态并仅在原前置条件仍成立时重试。仓门不安全移动保护中的 triggerEmergency 可持续重试至确认急停并逐次告警，其它结果未知均阻断依赖动作；次数与退避时长留给正式 spec 配置。
_Avoid_: 换 upperId 重建、固定错误自动重试、写操作超时即重发、用重试次数掩盖结果未知

**CallApiKey**:
RIoT 网页「调用密钥设置」中的长期密钥，是 ControlServer 调用目标 RIoT 环境的唯一默认 Bearer 凭证；每个环境独立，禁止进入车载端、仓库、样例、日志或业务响应。密钥是否轮换完全由软件负责人和实施负责人共同人工判断，系统只报告事实而不按时间或事件自动更换。
_Avoid_: API key（泛称）、跨环境共用密钥、车载凭证、网页密钥（口语）、静态 token（易与登录短时 token 混淆）

**AccessToken**:
经 `admin/login`（或 refresh）取得的短时访问凭证；8005 仅允许人工应急备用，不作常态自动登录，且不得保存进仓库、日志或车载端。
_Avoid_: 默认运行凭证、自动登录、token（单独使用时歧义）、Bearer（指头格式而非凭证种类）

**AdminLogin**:
人工应急时用用户名密码换取 AccessToken 的备用鉴权方式；ControlServer 不常态保存用户名或密码，登录成败不能只看 HTTP 状态。
_Avoid_: 自动登录、默认鉴权、登录（单独使用时歧义）、鉴权（上位概念）

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

**MapStationCatalogSnapshot（地图站点目录快照）**:
8005 对 `RIOT-8005-RUNTIME` 当前全部有效 Map 及每张 Map 全部 Station 完整观测后原子发布的不可变目录修订，以来源环境/build、观测时段、数量、内容指纹和本地单调修订保持身份。它供 AREA 解析、FixedTaskStation 绑定与变化检测，不包含 Edge 或几何路网，也不取代实时 RouteCost。
_Avoid_: 路网拓扑快照、Edge 快照、实时 RIoT 查询结果

**MapStationCatalogFreshness（地图站点目录新鲜度）**:
当前 MapStationCatalogSnapshot 距最近一次全量成功确认是否仍在投运前批准的最大未确认时长内；内容未变化的完整观测也会重新确认新鲜度。无快照或超过边界时禁止新的站点解析、相关配置激活和 RIoT move 建单，但不取消或改写已经存在的 RIoT 订单。
_Avoid_: 只按内容修订创建时间判断、刷新失败即删除旧快照、超时仍按最新目录、超时自动取消在途订单

**ResolvedTransportStation（已解析运输站点）**:
TransportDemand 从当时新鲜的 MapStationCatalogSnapshot 取得并冻结的 `mapId + stationId` Station 身份，连同当时名称、目录修订及所依赖的 TaskTypePublicStationRuleVersion/PublicStationBindingSetVersion 用于历史解释；后续目录、规则或绑定变化不得自动重映射。创建每个新的 RIoT move 订单前，该身份仍须存在于当前新鲜目录、未被 PublicStationBindingHold 阻断并通过 RouteCost，已经存在的订单不因目录或配置变化被自动取消。此处的 RouteCost 是**建单前置可达确认**——问的是「这台车此刻能不能到这个站」，起点恒为车当前位置，与 StationReachability 的站到站图判定是两个阶段的两件事，两者都要通过；两者分歧时阻断建单并告警。
_Avoid_: 动态 Station 引用、按新名称自动换站、目录或绑定变化重写既有任务、暂停中仍创建新 move、用历史快照直接建新单

**AREA 命名机台站点（AreaNamedMachineStation）**:
一张 Map 内以一个至三个合法 MES AREA 编码拼成 `stationName` 的机台侧 Station，系统只按该命名规则自动建立 AREA 解析关系且不提供显式覆盖；AREA 无唯一匹配时阻断相关新任务。
_Avoid_: 人工 AREA 映射、StationAreaOverride、把公共业务点按 AREA 解析、无法唯一解析时自动择一

**PublicStationFunction（公共站点功能）**:
固定公共作业区域地点类别（派工待送、烘箱、关卡、三光、氮气柜）的旧称，产品不再维护这一分类：FixedTaskStation 按任务类型绑定，TaskTypePublicStationRuleVersion 只记起点/终点，PublicStationBindingHold 与目录变化影响也按任务类型计。需要说明一个公共站点是什么地方时，用任务类型与 Station 名称表达；协议中的同名字段保持为空。
_Avoid_: 按 PublicStationFunction 绑定站点、按功能暂停、按功能计算目录变化影响、在任务类型规则中维护功能、同一 Station 承担多个功能

**MapPublicStationRequirementSet（地图公共站点需求集）**:
一张 Map 上当前获准启用、需要 FixedTaskStation 的任务类型集合；某个任务类型在该 Map 具有有效绑定后才可投运，未启用的任务类型不强制配置。
_Avoid_: 每张 Map 无条件配齐全部任务类型的站点、目录已同步即业务就绪、缺失绑定时默认站点、按 PublicStationFunction 列需求

**TaskTypePublicStationRuleVersion（任务类型公共站点规则版本）**:
不可变地固定每个受支持 TASK_TYPE 的 FixedTaskStation 是运输起点还是终点；新规则只在相关 Map 已具有对应任务类型的有效绑定后才可激活，既有 TransportDemand 保留冻结版本。
_Avoid_: 在规则中保存站点、在规则中维护 PublicStationFunction、缺少固定站点时先启用任务类型、规则变更重写既有任务

**FixedTaskStation（任务固定站点）**:
8005 项目把已同步的具体 Station 按 `mapId + TASK_TYPE` 唯一显式绑定得到的公共业务点；每个任务类型在每张 Map 上最多一个，TransportDemand 使用同图本任务类型的这一绑定，并禁止跨图运输。同一 Station 不得被多个任务类型绑定，确需复用须以新的现场证据重新批准。
_Avoid_: 固定 AREA、从 MES 行读取的第二个端点、AREA 显式覆盖、按名称自动推断、按 PublicStationFunction 绑定、同图同任务类型站点集合、多个任务类型共用 Station

**PublicStationBindingSetVersion（公共站点绑定集版本）**:
一张 Map 的完整不可变 TASK_TYPE—Station 绑定集，同时固定 MapPublicStationRequirementSet、TaskTypePublicStationRuleVersion 和校验所用的 MapStationCatalogSnapshot 修订；只能全图原子激活，回滚也是经当前事实重校验的新激活。
_Avoid_: 逐任务类型即时覆盖、混用新旧绑定、旧版本直接翻回当前、回滚改写历史

**PublicStationBindingHold（公共站点绑定暂停）**:
维护管理员或系统管理员对明确 Map 与 TASK_TYPE 立即收紧的受审计门禁，它阻断该任务类型对其 FixedTaskStation 发起新的站点使用，不连带其他任务类型，也不删除绑定或改写已有 RIoT 订单；恢复必须由系统管理员重新校验和激活。
_Avoid_: 删除绑定、定时自动恢复、暂停后既有订单自动取消、普通操作员暂停、按 PublicStationFunction 暂停、连带暂停其他任务类型

**SingleBerthStationClaim（单车位站点占用权）**:
一个 Station 在同一时刻只允许由一台已到达车辆占用，或由一台已承诺前往的车辆预占；任一状态成立时，其他车辆不得承接下一站为该 Station 的新任务。
_Avoid_: 只检查当前占位、不检查在途预占、两车同时承诺同一站点

**NearStationQuery**:
在候选 Station 集合中，按路径代价选出最近的起点或终点 Station（对应 RIoT `queryNearestStart` / `queryNearEnd`）；返回的是 stationId，不是折线几何。
_Avoid_: 最短路径（易被理解成几何 path）、路径规划结果

**RouteCost**:
指定 Map 上某车到某 Station 的路径代价（mm）；非负且可读为可达，`-1` 表示不可达（含车不在该图等）。建单前可达判断依据此值，不能只看建单业务成功码。
_Avoid_: 距离（易被理解成直线距离）、最短路径几何

### 订单与车辆控制

**建单确认中（OrderCreationConfirmationPending）**:
TransportDemand 已独占选定 AGV 与稳定 `upperId`、但尚未按该 `upperId` 确认唯一 RIoT 订单存在的派发状态；期间该 TransportDemand 与 AGV 均不参与其它派发，只有取得对应 OrderRef 后才能进入运输进行中。
_Avoid_: 进行中、建单已失败、结果未知时释放绑定、换车换 upperId、重复建单

**建单拒绝分流（OrderCreationRejectionDisposition）**:
常规建单被明确拒绝且按原 `upperId` 确认订单不存在后的三类业务归宿：临时服务或容量问题在原前提仍成立时保留绑定并以原 `upperId` 有限重试；仅当前车辆失去资格时释放该车并把 TransportDemand 退回调度；需求、端点、契约或鉴权问题则释放车辆但阻断该 TransportDemand。
_Avoid_: 任何拒绝都立即重派、任何拒绝都永久占车、车辆无关问题换车轮询、修复前自动重派被阻断需求

**RIoT 订单接管确认（RIoTOrderAdoptionConfirmation）**:
按稳定 `upperId` 取得唯一非终态订单，并确认其指定车辆及当前 AgvLifecycleGeneration、地图和起终点均与原业务意图一致后，8005 取得完整 OrderRef 并把建单确认中转为运输进行中的业务事实；多单、字段不一致或终态订单都不构成接管确认。
_Avoid_: 查到即接管、HTTP 成功即进行中、接管字段不一致订单、把终态订单先标记进行中

**建单结果双重未知（OrderCreationOutcomeIndeterminate）**:
常规建单调用无法确认结果，且按原 `upperId` 对账也无法可靠证明订单存在或不存在的业务状态；它持续保留 TransportDemand、AGV 和 `upperId` 的独占绑定，不因等待超时、重试次数或任何管理员操作直接释放；管理员只能重新对账、暂停后续调用或登记经独立核验的 RIoT 结果。
_Avoid_: 超时即不存在、重试耗尽即释放、换车换号、结果未知时重派、管理员强制视为不存在

**建单重试暂停（OrderCreationRetryHold）**:
同一业务意图使用原 `upperId` 的有限建单重试已耗尽，且最新对账可靠确认订单不存在时的派发阻断状态；它释放车辆但保留 TransportDemand、原业务意图与 `upperId`，只有 RIoT 服务恢复且派发前提重新核验后才可受控恢复。
_Avoid_: 重试耗尽仍长期占车、自动换车冲击外部故障、换 upperId、服务未恢复即自动重派

**派发代次（DispatchGeneration）**:
一个 TransportDemand 的一次完整 RIoT 订单创建意图，以唯一稳定 `upperId` 贯穿建单、结果未知、对账和同意图重试；匹配订单终态完成对账后该代次闭合，任何后续重新派发必须建立新代次和新 `upperId`。
_Avoid_: 每次重试换 upperId、终态后复用旧 upperId、不可追溯的重新派发

**WireToGateMovementLeg（关卡运输移动段）**:
一次执行计划中严格串行的 `TO_PICKUP` 或 `TO_GATE` 单段移动；每段拥有独立的 MovementLegId、DispatchGeneration、OrderIntent、稳定 `upperId` 和冻结目标，同一时刻最多一段未收敛。段属于计划而不属于某一条 TransportDemand——一段可以同时服务多条 Demand（多条共用同一取货站，或共用关卡终点），因此段与 Demand 是多对多而非从属关系。
_Avoid_: 多站 RIoT 订单、两段共用 upperId、同时建两段订单、MovementLegId 代替 DemandId、一段只服务一条 Demand

**派发唯一性门禁（DispatchUniquenessGuard）**:
每个 DemandId 同时只能有一个未闭合 DispatchGeneration，每辆 AGV 同时只能被一个未确认或未终结的本项目订单占用；并发竞争失败者不得覆盖已有绑定，只能重新读取当前事实。
_Avoid_: 一个需求同时双派发、一车多个未结订单、后写覆盖先绑定、审计日志代替唯一性门禁

**派发审计链（DispatchAuditTrail）**:
一个 DispatchGeneration 的不可改写事实链，记录 DemandId、TransportDemandKey、`upperId`、AGV 身份与生命周期、地图和起终点、派发前提快照、每次调用与对账结果、状态转换、重试、释放、重派原因及人工证据的提交人和来源；它用于追溯而不代替 RIoT 状态核验。
_Avoid_: 只记成功调用、只记最终状态、可编辑派发历史、从审计链重放请求

**订单终态对账（OrderTerminalReconciliation）**:
建单确认期间按 `upperId` 发现匹配订单已处于 `SUCCESS`、`FAILED`、`CANCELLED` 或 `DELETED` 时，将 OrderRef 与车辆实际位置、目标站点、运动与安全状态、订单名额和 TransportDemand 有效性收敛为唯一业务结论的过程；它不先把任务标记为进行中，也不直接授权重新派发。
_Avoid_: 终态即重派、SUCCESS 即无条件完工、FAILED 即车辆已安全释放、终态先标记进行中

**OrderRef**:
`byDefaultMissions` 建单成功后返回的订单标识：数值 `id`、字符串 `orderId`、调用方 `upperId`，以及当时的 `orderState`。后续查单/取消/命令按对应标识选用。
_Avoid_: Order（泛称）、任务号（口语）

**DispatchEnable**:
允许车辆参与后续 RIoT 调度，使符合条件的新订单可从 QUEUEING 推进到 EXECUTING；应用建单前必须独立确认 ON_LINE，不能依赖建单接口拒绝 OFF_LINE 车辆。
_Avoid_: 开机、恢复当前订单、上线（易与网络在线混淆）、enable（裸字段名）

**DispatchDisable**:
阻止车辆承接后续 RIoT 调度，但不阻止建单接口接受新订单进入 QUEUEING，也不暂停、取消或终止当前 EXECUTING 订单；获授权人员可在当前订单执行中调用，调用后必须回查 OFF_LINE。
_Avoid_: 关机、中断当前订单、禁止建单、下线（易与断网混淆）、disable（裸字段名）

**管理员禁用（AdministrativeVehicleDisable）**:
获授权人员主动设置的本地业务状态，用于阻止车辆接受新的搬运、充电或停靠任务，但不表达车辆已经故障，也不处置当前订单；它与 VehicleFaultIsolation 独立且可以同时存在。
_Avoid_: 故障、不可用（泛称）、DispatchDisable（RIoT 控制动作）、禁用即终止当前任务

**车辆故障隔离（VehicleFaultIsolation）**:
表达车辆因故障处置而退出业务调度并须经独立安全收敛后才能恢复的业务状态；它不复用 AdministrativeVehicleDisable，底层调度阻断动作也不等同于故障已确认或已解除。
_Avoid_: 已禁用、DispatchDisable、离线（单一观测事实）、故障自动恢复

**车辆故障硬证据白名单（VehicleFaultHardEvidenceAllowlist）**:
允许系统自动把具体车辆升级为 VehicleFaultIsolation 的版本绑定事实集合；当前只包含新鲜的 `emergencyState=CAN_NOT_RECOVER`。物模型 `sysState`、`lastErrorCode`、`hardwareErrorCode`、`faultCodesList`、离线、导航失败和订单 `FAILED` 均不在当前白名单，新增项须绑定环境、build、车型/固件、语义、严重度和清除条件并再次批准。
_Avoid_: 字段名像故障即可采用、当前 TSL 即生产绑定、错误码非零即故障、观察到一次即扩白名单

**车辆故障现场确认（VehicleFaultFieldConfirmation）**:
具备 ExceptionRecoveryPermission 的人员在异常处置会话中确认具体车辆须进入隔离的受审计事实；它不需要审批或再次认证，软件或网络异常本身仍不能证明单车故障。
_Avoid_: 双人必签、逐动作二次认证、共享账号、软件或网络诊断即单车故障、确认即处置货物

**车辆故障恢复闭环（VehicleFaultRecoveryClosure）**:
异常处置人员在同一 ExceptionRecoverySession 中记录检查和修复结果后，由系统独立核验位置、订单、运动、急停、仓门、开锁输出、货物绑定和未结操作均无未知或冲突，才解除 VehicleFaultIsolation 的闭环；发生 ForcedMechanicalCargoRecovery 时，还必须修复锁、DO、锁反馈、光幕和相关 IO，完成空仓/有物、锁闭、输出复位测试，并在 ForcedRecoveryGeneration 内重新对账。闭环不需要第二角色批准或再次认证，解除只恢复资格评估，不自动继续订单或派发任务。
_Avoid_: 双角色审批、逐动作二次认证、人工覆盖未知事实、解除即 OrderContinue、解除即下新单

**疑似车辆故障阻断（SuspectedVehicleFaultBlock）**:
新鲜但尚不足以证明车辆故障的离线、通信或导航异常所形成的保护状态；它立即阻断新的车辆派发并保留证据，但不把症状升级为 VehicleFaultIsolation，也不授权终止任务或处置车上货物。持续时间只提升告警和现场响应紧迫度，永远不能单独证明车辆故障；升级必须取得车辆级硬证据或授权人员的现场确认。只有通信与车辆状态重新满足统一的新鲜度/连续稳定门槛，且订单、位置、运动、急停、仓门、货物绑定和未结调用均完成无冲突对账时才可自动解除；任一事实未知时不可人工强解，解除只恢复资格评估。
_Avoid_: 已确认故障、超时即故障、单个 FAILED 即故障、继续试派验证、告警升级即事实升级、通信恢复即解除、人工覆盖未知事实、解除即继续订单

**故障隔离订单保护（FaultIsolationOrderContainment）**:
车辆进入 SuspectedVehicleFaultBlock 或 VehicleFaultIsolation 时，对本项目当前执行订单自动调用 OrderHold 并回查 HELD 的保护动作；它与禁止新派车同时生效，不能以 Cancel 代替停车。OrderHold 不可用、结果未知或车辆未及时停下时继续保持全部阻断并形成高优先级安全升级，EmergencyStop 条件由独立安全决定收敛；取得实际停车证据前不得表示车辆已安全停稳。
_Avoid_: 隔离状态即已停车、Cancel 即停车、调用成功即 HELD、暂停失败后继续业务、未停车先开仓

**故障隔离未装任务改派（FaultIsolationUnloadedReassignment）**:
车辆进入 VehicleFaultIsolation 后，仅当原 RIoT 订单已确认终结、没有已提交 LoadBatch、没有活动或未知结果的仓位操作，且服务端可证明车上没有该任务产品时，解除原车辆绑定并让原 DemandId 重新参加正常派车的业务连续性处理；它不是取消，不写入 TransportDemandSuppression，也不创建新需求实例。
_Avoid_: 新 DemandId、故障取消、按开过门推定已装货、订单结果未知时解绑、未知货物状态时改派

**故障车载货保全（FaultedVehicleCargoHold）**:
车辆隔离时为已有装货事实或货物状态未知的任务保留原 DemandId、车辆、仓位、产品与订单绑定的业务状态；它不得直接改派，只能在车辆恢复并重新核验后继续原任务，或经授权完成现场取货后终止原任务。等待时间只提升告警与响应紧迫度，不自动选择路径或取消任务。
_Avoid_: 自动改派、超时取消、超时自动取货、解除车辆绑定、把等待视为任务终态

**故障车载货续行（FaultedVehicleCargoContinuation）**:
车辆完成 VehicleFaultRecoveryClosure 后，让仍处于 FaultedVehicleCargoHold 的原 DemandId 继续由原载货车辆执行的受控路径；原 RIoT 订单仍为 HELD 且身份一致时走 OrderContinue，原订单已明确终结且相关阻断已收敛时可在正常派车与安全门禁下为同一 DemandId 建立关联旧订单的新移动单。订单结果未知、身份/位置/路线冲突或已经形成 FaultCargoRecoveryRecord 时禁止续行。
_Avoid_: 新 DemandId、改派其它车辆、换号绕过未知结果、故障解除即自动继续、补救终止后复活

**故障载货取出选择（FaultCargoRecoveryChoice）**:
异常处置人员在 ExceptionRecoverySession 中选择“不再等待故障车辆恢复、改为现场取货并终止原载货任务”的操作路径；它不需要审批或再次认证，也不因选择而立即终止任务，系统仍须核验停车、目标仓位和完整取货交接闭环。
_Avoid_: FaultCargoRecoveryDecision、审批、逐动作二次认证、故障隔离即自动选择、选择即任务终态

**故障载货取出模式（FaultCargoRecoveryAccessMode）**:
作出有效 FaultCargoRecoveryChoice 后，异常处置人员在车辆已确认停稳且当前订单已 HELD/终结，或已经完成断电、抱闸等效现场物理隔离时，开启仍绑定原载货任务的指定仓位进行取货的受控模式；VehicleFaultIsolation 和 DispatchDisable 均不能代替防移动证明。无需另一角色审批，协助人员可以取货但不得操作事件范围外的仓位。
_Avoid_: MaintenanceDoorAccessMode、审批、故障隔离即停稳、DispatchDisable 即停稳、RIoT 结果未知且未物理隔离仍开仓、顺便开启其它仓位

**故障载货补救记录（FaultCargoRecoveryRecord）**:
正常受控取货时，故障车载货全部按原任务目标仓位达到 `EMPTY + 锁闭 + 开锁输出复位`，并由具名人员接管产品后由系统自动形成不可变交接记录；ForcedMechanicalCargoRecovery 时，可由具名的 ForcedCargoHandoffRecord 代替电子空仓证明来关闭货物取出与交接的业务问题，但不能证明仓门、传感器或车辆恢复。记录绑定异常处置会话、取出选择、原 DemandId、TransportDemandKey、车辆、仓位、产品/Sublot、现场位置、处置人与接管人及时间；身份明确的完整交接与原任务 `TERMINATED_BY_FAULT_CARGO_HANDOFF` 终态及 TransportDemandSuppression 原子提交，产品身份未知时相关任务保持待盘点。
_Avoid_: 人工运输任务、成功送达、MES 完工、部分任务终止、无接管人取出、取出后等待 MES 扫码

**强制机械取出（ForcedMechanicalCargoRecovery）**:
锁无法通过 DO 弹开，或锁反馈、光幕、占用检测等事实已失真时，在 ExceptionRecoverySession 中先完成断电、抱闸或等效机械隔离，再由具备现场作业资质者以应急机械方式开锁或拆卸并救出货物的最后手段；系统停止重复发送开锁 DO，并把可证明的受影响仓位或 IO 模块标记为物理状态未知，范围无法确定时隔离整车。人工证据可关闭货物取出与交接，但不能恢复仓位或车辆业务资格。
_Avoid_: 重试 DO 撞运气、故障隔离即机械安全、强制开锁即仓位恢复、人工目视替代锁与传感器验证、影响范围未知仍只隔离单仓

**强制恢复代次（ForcedRecoveryGeneration）**:
ForcedMechanicalCargoRecovery 开始时建立的车辆恢复边界；它使此前全部仓位命令、传感器快照、执行检查点和迟到结果失去更新当前状态的资格，只保留为历史证据。后续状态必须基于修复后的实时 IO、业务绑定和本代次对账重新建立。
_Avoid_: 继续沿用旧 SlotOperationAttemptId、迟到成功覆盖强制处置、从旧快照猜恢复状态、删除历史证据

**强制取出交接记录（ForcedCargoHandoffRecord）**:
强制机械取出后，由异常处置人员记录并由具名接管人确认的产品身份、原车辆/仓位、原 DemandId/TransportDemandKey、取出方式、处置人与时间；身份明确时它证明货物已经救出并完成责任交接，允许关闭对应货物业务，但不证明电子空仓、仓门安全或设备恢复。产品身份不明时只形成实物记录并保持相关任务待盘点。
_Avoid_: 仓位恢复确认、车辆恢复确认、未知产品猜绑定、人工运输成功、MES 完工

**EmergencyStop**:
车辆急停态及软件触发/解除；当仓门未能证明安全锁闭，或车辆故障阻断已经要求停车，而 `OrderHold` 后无法同时证明订单已 `HELD` 和车辆已停稳，且车辆仍在移动或因监控失败无法排除继续移动时，8005 自动用 `triggerEmergency` 兜底并持续回查急停与停车状态。它只负责运动保护，不等待固定超时、不以 Cancel 代替停车，也不自动取消或终结订单、释放业务绑定、证明订单已 HELD，或在解除后自动继续移动。
_Avoid_: 普通暂停、一般异常处置、固定超时后才急停、Cancel 代替停车、急停即订单暂停或终结、解除即续行、无来源与安全证明的自动解除、中断（与 interrupt 不同）

**停稳证明（ProvenVehicleStop）**:
证明车辆实际停止的正面事实组合：新鲜的 `movementState` 明确为非移动状态、连续多次位置观测保持不变，且期间没有新的移动迹象；具体连续次数和时间窗口由统一监控策略规定。订单 `HELD`、急停状态或单次静止查询均不能单独构成停稳证明，任一必要事实未知时保持未证明。
_Avoid_: OrderHold 成功、急停调用成功、单次速度或位置快照、状态未知时推定停稳

**远程急停失效处置（RemoteEmergencyStopFailureResponse）**:
远程 `triggerEmergency` 失败、超时或结果未知且仍无停稳证明时的持续保护状态：急停状态未确认前按受控退避持续重试并回查；确认 `CAN_RECOVER` 或 `CAN_NOT_RECOVER` 后停止重复触发，只持续监控停稳证明；原因消除前急停意外恢复 `OK` 时立即重触发。系统发出最高优先级现场告警，并在停稳得到证明或完成现场物理隔离前始终按车辆可能仍在移动处理；现场已有的物理急停可由任何现场人员立即操作且不要求系统登录或审批，断电、抱闸等专业隔离只由具备相应作业资质者执行。
_Avoid_: 调用失败即放弃、急停已确认仍盲目刷调用、急停已确认即视为停车、告警即视为停车、等待审批后按物理急停、无资质断电或解抱闸

**紧急停车事件（EmergencyStopIncident）**:
从仓门或车辆故障停车义务升级为软件急停、远程急停失效或现场物理停车处置后形成的安全事件；无停稳证明时保持最高优先级并要求现场确认车辆和隔离危险区域，取得停稳证明后仍以高优先级保持至全部原因消除、对账和恢复动作确认完成。人员“已知悉”只记录响应，不能停止重试、解除急停或业务阻断，也不能关闭事件。
_Avoid_: 告警确认即关闭、停稳即恢复、急停调用成功即结束、普通业务告警

**软件急停发起权限（SoftwareEmergencyInitiationPermission）**:
遵循“停车宽、恢复严”的安全权限：系统满足条件时自动触发；现场人员可从车载端无需登录地为本车请求；服务端已登录且有车辆查看权限的人员可为明确选中的车辆请求，均不要求二次认证或审批并须记录来源、身份（若有）、车辆、原因和结果。它只允许发起停车，不授予解除急停或恢复业务的权限。
_Avoid_: 发起急停审批、发起急停二次认证、发起权限自动包含解除权限、无目标车辆的批量急停

**软件急停解除（SoftwareEmergencyRelease）**:
8005 只能对已进入 `CAN_RECOVER` 的软件急停调用 `cancelEmergency`；系统自动触发的急停只有在全部触发原因消除、仓门安全、具备停稳证明，并完成订单、位置、故障状态和未结调用对账后才自动解除，同时存在多个原因时缺一不可。人员手动请求、外部系统触发或来源不明的急停不自动解除，必须由人员明确请求；`CAN_NOT_RECOVER` 禁止软件解除，调用后必须回查 `emergencyState=OK`。
_Avoid_: CAN_NOT_RECOVER 强制解除、部分原因消除即解除、手动或未知来源自动解除、只看 RIoT 不看车载安全状态、调用成功即解除

**仓门不安全移动急停保持（DoorUnsafeMovementEmergencyLatch）**:
车辆在仓门未能证明安全锁闭时发生移动或失去停稳证明后，8005 自动触发并持续保持软件急停；外部系统提前解除时立即重触发并告警，只有车载端确认全部仓门安全锁闭且开锁输出复位后才退出保持。已授权正常装卸只维持 StationOperationGuard，不告警或急停；授权外异常但已有停稳证明时阻断移动并高优先级告警，出现移动或停稳证明失效才进入本状态。
_Avoid_: 一次性急停调用、车辆停下即解除、外部解除即放行、正常装卸开仓即告警或急停、静止异常永不升级

**RIoT 唯一车辆控制边界（RIoTOnlyVehicleControlBoundary）**:
8005 系统只通过当前环境和 schema 版本中获批的 RIoT API 控制车辆，不接入单机系统控制面，也不绕过 RIoT 发送 Modbus 或其它底层车辆指令。
_Avoid_: 直控单机系统、Modbus 控车、绕过 RIoT 的车辆指令

**RIoT 车型行为兼容假设（RIoTVehicleBehaviorCompatibilityAssumption）**:
300C 与 300E 共用同一物模型，8005 默认两者对已批准 RIoT 操作具有相同状态值和行为逻辑，因此 300C riot-lab 结论可作为 300E 的当前行为依据而不要求投产前逐项实车复验；每次调用仍须执行 RIoTCallOutcomeConfirmation，观察到差异时立即停止依赖该假设。
_Avoid_: 已在 300E 实测、不同车型必然不同、兼容假设免除结果确认

**RIoT 跨 Build 兼容（RIoTCrossBuildCompatibility）**:
受控 OpenAPI 与 8005 运行环境来自 v2.2.0.14，而 riot-lab 行为测试运行在 2.2.0.30；仅当接口路径、方法和字段仍匹配时默认沿用跨 build 行为结论，发现差异时只阻断对应操作并保留其它已确认能力。
_Avoid_: 两个 build 已完全等价、单项差异推翻全部接口、兼容假设免除结果确认

**OrderHold**:
将移动单置于 HELD（暂停执行）的控制；与 EmergencyStop、interrupt 不同。
_Avoid_: 暂停（泛称）、急停

**OrderContinue**:
从 HELD 恢复继续执行（CONTINUE_FROM_HELD）；仅当 8005 订单仍确认为 HELD、原暂停原因消除、重连与未结操作对账完成、重新通过 PreDepartureSafetyCheck 且服务端生成本次明确授权后，应用才可调用并须回查已离开 HELD。
_Avoid_: 网络恢复即继续、操作员直接继续、恢复（泛称，易与急停解除混淆）、resume（裸英文）、HangContinue

**HangContinue**:
从 OrderHang 尝试拉回 EXECUTING（CONTINUE_FROM_HANG）；8005 只可对已批准原因白名单中的普通 HANG、在对应次数上限内自动调用并回查已离开 HANG，未知原因和充电失败不得使用。
_Avoid_: OrderContinue、充电失败继续、未知原因自动继续、无限重试、resume（泛称）

**PriorityExec**:
将队列中指定订单提升为优先执行，而不必先清空同车其它队列单；当前 8005 不调用该能力，只保留为未来重新评审的候选。
_Avoid_: 当前项目白名单、插队（口语）、优先级字段（建单时的 priority 语义不同）

**RIoT 车辆订单名额（RIoTVehicleOrderQuota）**:
8005 按下单时的 appointVehicleKey 保证每车至多一个未明确终结的本项目 RIoT 订单；QUEUEING、EXECUTING、PAUSED、HANG、优先队列、SUSPENDED 和未知状态均占用名额，独立回查确认终态才释放 RIoT 名额。释放名额不等于允许再派：FAILED 仍触发失败订单派车阻断。
_Avoid_: 只查 RIoT 当前分配车辆、HANG 不计数、未知状态释放名额、FAILED 后直接再派、每车多队列单

**BusinessFailure**:
RIoT 在 HTTP 已成功（或可判定）的前提下，用业务 `code` 表达的失败；具名 Facade 将其表现为统一异常，而不是留给调用方拆包。
_Avoid_: HTTP 错误（传输层）、不可达（RouteCost=-1，属领域结果）

**ArrivalAtStation**:
车辆已到达目的 Station 的车侧可观测信号；在成功移动单上往往早于订单 SUCCESS。
_Avoid_: 订单完成、可再派

**StationOperationArrivalGate（站点作业到站门禁）**:
对应订单已确认 SUCCESS、车辆 IDLE、没有未结或未知调用、订单及当前 Map/Station 与冻结目标一致，并有新鲜停稳与安全事实时形成的站点作业准入；ArrivalAtStation 只能提示进度，不能单独满足本门禁。
_Avoid_: 到站信号即开仓、currentPosition 单字段证明角色、同坐标猜测站点、订单成功但位置矛盾仍作业

**ReadyForNextOrder**:
可以安全下发下一单的条件：订单已 SUCCESS、车辆已 IDLE，且没有未结调用、未知结果或失败订单派车阻断；不等于 ArrivalAtStation 或任意 RIoT 终态。
_Avoid_: 到站即可派、FAILED 即可再派、AWAITING_ORDER（单独作为充分条件）

**失败订单派车阻断（FailedOrderDispatchBlock）**:
RIoT 订单回查确认为 FAILED 后形成的车辆级派车阻断；FAILED 通常指向 RIoT 内部故障，8005 必须提示管理员诊断并解决，不能仅因订单已成终态就下发下一单。
_Avoid_: FAILED 自动清障、终态即空闲、失败后自动重派

### 异常滞留与 MES 策略

**PausedZeroDrop**:
某个任务类型在已有健康非零基线后突然降为零时进入的保护状态；保护期间暂停该类型需求的消失计数与 GONE 判定，直到连续健康非零轮次达到恢复条件。进入与解除都须保留为可追溯事件。
_Avoid_: 零任务、暂停（泛称）、PAUSED_ZERO_DROP 告警（仅指进入事件时）

**QueueingStall**:
订单已创建成功但长期停留在 QUEUEING、迟迟不进入 EXECUTING 的滞留；可执行订单通常很快进入 EXECUTING，轮询周期较长时甚至观察不到短暂 QUEUEING。长期可见通常表示车辆距可执行路线过远、车辆状态不允许执行、车辆未启用或其它执行前置不成立，且 RIoT 不会因此自动变为 FAILED。
_Avoid_: 挂起（泛称）、OrderHang、HELD、急停

**QUEUEING 滞留自动恢复边界（QueueingStallAutomaticRecoveryBoundary）**:
8005 应自动恢复由自身造成、原因已消除且安全条件可独立证明的可恢复阻断，包括恢复自身的临时 DispatchDisable 和自身触发的 CAN_RECOVER 软件急停，并逐次回查结果。人工、外部系统或来源未知的禁用/急停，以及 CAN_NOT_RECOVER、物理不可移动或安全不可证明的状态保持阻断并转人工。
_Avoid_: 所有 QUEUEING 都转人工、超时即取消重建、覆盖人工禁用、低电量绕过安全门槛

**RIoT QUEUEING 原生诊断（RIoTNativeQueueingDiagnosis）**:
RIoT 针对指定车辆和订单返回长期未分配原因及建议的原生只读诊断；原始原因与建议是诊断证据，不是8005控制动作授权。只有经目标 build 实测、纳入批准映射并通过独立状态与安全核验的原因才可触发自动恢复，未知或变化的自由文本只告警转人工。
_Avoid_: 直接执行 suggestList、把自由文本当稳定枚举、诊断成功即允许移动

**低电量防御性升级（LowBatteryDefensiveEscalation）**:
订单阻断期间电量降至既有充电或接单阈值时，只提高告警紧迫度并继续阻断新的搬运派车；充电阈值是正常能源调度输入，不授权取消、重建积压订单或绕过移动安全门槛。诊断指向8005缺陷或原因未知时须保留故障现场，不能以低电恢复掩盖问题。
_Avoid_: 低电即清队列、自动取消重派充电、用防御逻辑掩盖下单缺陷

**OrderHang**:
订单 `orderState=HANG` 的滞留；与 QueueingStall、HELD、急停冻结（可仍为 EXECUTING）都不同。充电失败与普通 HANG 策略分离：普通分支可按原因尝试 HangContinue；充电分支不以 HangContinue 为默认。HangContinue 接口成功码不等于订单已离开 HANG。
_Avoid_: 挂起（泛称）、QUEUEING 滞留、HELD、急停

**ChargeHangReassign**:
充电失败 OrderHang 后，由 MES 自动改派前往其它充电桩再充的策略；改派前须 CANCEL 旧 HANG。备用桩先从该车配置允许的充电站集合中排除刚失败的站点，再仅保留 RIoT 当前地图中有效、占用与预占状态均可确认且当前未被占用或预占的站点；任一资格状态未知时 fail-closed 排除，最后才对已过滤集合做 NearStationQuery。改派车辆与普通待充电车辆进入 BR-007 的同一待充电排队集合，统一按当前电量排序；“刚发生充电失败”本身不产生独立优先级。选桩结果只有成功取得 ChargingStationExclusiveReservation 后才能用于创建 RIoT 充电订单。
_Avoid_: HangContinue、人工改充（若未采用）

**充电桩独占预占（ChargingStationExclusiveReservation）**:
充电桩在同一时刻最多归属于一台车辆的排他业务占用；候选计算本身不取得预占，只有一个车辆可以原子地取得该桩的预占权，未取得者不得创建前往该桩的 RIoT 订单并继续留在待充电排队集合。预占从选桩承诺延续到车辆前往、物理充电及其结果确认期间；订单或充电结果未知时继续保持，不得释放给其它车辆。正常充电只有在充电已停止或完成、原车辆已离开桩位且桩位恢复空闲后才能释放；到站前取消只有在旧订单已确认取消终态、且车辆确认不会继续前往或占据该桩后才能释放。仅达到完成电量、仅发出取消命令或仅收到接口成功均不足以释放。
_Avoid_: 查询为空闲即下单、同桩双重预占、下单结果未知即释放、达到完成电量但车辆仍占位即释放、未释放先抢占

**充电桩占用（ChargingStationOccupancy）**:
充电桩被任意车辆实际占据的物理资源状态；车辆只要仍停在桩位上即为占用，不论是否正在充电，也不论是否登记、受控或管辖于 8005。8005 的本地预占记录不能覆盖该物理事实；发现非 8005 管辖车辆占位时同样禁止选桩，无法确认所有相关车辆的占位状态时按 UNKNOWN 处理并 fail-closed 排除。
_Avoid_: 未充电即空闲、只监控 8005 车辆、本地无预占即空闲、外部车辆占位可忽略

### 监控与告警

**监控看板刷新策略（MonitoringDashboardRefreshPolicy）**:
车队与仓位看板每 2 秒从 ControlServer 获取一次最新状态，并支持人工刷新；该周期只是界面更新节奏，不是设备读取周期或读取超时。设备读取尚未完成时不得因经过一个刷新周期就判定失败，也不得启动重叠读取；连接或读取是否失败由对应数据来源的既有判定负责。
_Avoid_: 每次刷新直接读取设备、2 秒读取超时、刷新未取得新值即判失败、重叠设备读取

**监控数据不可用（MonitoringDataUnavailable）**:
看板无法从对应设备取得当前事实的状态，须明确区分设备连接失败与信息读取失败；主看板不得继续把最后一次成功值呈现为当前值，最后一次成功值只可在排障详情中连同采集时间查看。
_Avoid_: 已过期、旧值继续作为当前值、刷新成功即恢复、隐藏失败原因

**告警可见对象策略（AlertAudiencePolicy）**:
与当前 AGV、当前停靠或当前操作直接相关的告警显示在对应 OnboardHmi；全部 8005 告警集中显示在 ControlServer，并允许维护管理员和系统管理员查看。查看告警不扩大处置权限；第一版不发送短信、邮件或企业微信，也不恢复 R-12/R-13 为系统授权角色。
_Avoid_: 告警可见即有处置权、只在车载端显示、只在服务端显示、隐含外部推送、恢复旧岗位角色

**站点期限后仓门未闭升级（StationDoorOpenEscalation）**:
装货站期限到期而本次装货仍有仓门未能证明安全锁闭、本站因而不结束并持续等待时，由现场规程按到期后经过的时长把响应责任依次交给当站操作员、班组长与维护管理员的升级方式；时长只转移响应岗位、提升紧迫度，不结算、不取消、不放行车辆，也不证明任何故障。仓门已经关上而等待仍未解除时不按时长升级，直接交维护管理员排查锁反馈与 IO。班组长在此是现场岗位而非系统身份，升级不授予任何系统权限；关门本身不表达取消意图，放弃这次装货只能由已核验操作员发起装货任务取消。
_Avoid_: 超时即取消、关空门即放弃、升级即故障、升级即授权、第一版推送通知、按时长强行放车

### MES 焊线工序与运输任务

**MesTaskUnionRound（MES 联合查询轮次）**:
对六类运输候选执行一次 MES_TASK_UNION Oracle 语句所得的完整轮次；六个 UNION ALL 分支共享同一语句级一致性快照，结构完整但字段值异常的原始行仍属于 SUCCESS 证据，只有执行或结构契约不能成立的 FAILURE / INCOMPLETE 才保持 Demand 投影不变。
_Avoid_: 六次独立查询、成功的部分快照、调用方自行声明 snapshotComplete

**MesIngest**:
MES 任务接入：轮询只读 MES 快照、对账并投影 TransportDemand；GONE 后同一业务键再现时可以产生新的本地投影实例。它不读取调度侧取消抑制，也不决定是否创建业务任务或派车。
_Avoid_: MES 模块（泛称）、任务服务（易含调度）、调度取消过滤器、薄模块（口语）

**当前 MES 只读边界（CurrentMesReadOnlyBoundary）**:
当前 8005 范围内所有组成部分只可读取 MES，不执行完工、卸货、过站、入库或其它 MES 写操作，也不通过工作流或外部调用代替现场流程推动 MES 状态变化；搬运与卸货结果只形成 8005 本地业务终态和审计事实，既不等同于 MES 业务完成，也不以 MES 写回成功作为完成条件。任何 MES 写回能力均属于未来重新评审范围，须在接口、权限、幂等、失败及结果未知处置获得版本绑定批准后才能进入新的基线。
_Avoid_: 本地存储也只读、8005 本地完成即 MES 完成、间接触发其它系统代写 MES、先实现写回再补评审、复用查询权限写 MES

**MES 后续操作责任（MesDownstreamActionOwnership）**:
正常卸货后所需的 MES 入站、过站、接收或其它状态变化，由目的站对应的现场责任人通过既有 PDA/MES 流程承担；责任随目的站业务角色确定，不固定归属于 AGV 装货操作员，8005 也不代办或接管该责任。
_Avoid_: 8005 完工回写、AGV 操作员统一代办、目的站责任人不明时由系统猜测

**MES 后续操作非阻塞（MesDownstreamActionNonBlocking）**:
8005 在物理卸货完成并满足安全结束条件后立即结束本地任务并释放车辆，不等待现场人员完成 PDA/MES 操作，也不等待或轮询 MES 状态变化来判定本地完成；后续只读观察到的 MES 变化不得回溯改变已经成立的本地卸货终态。8005 不显示 MES 后续操作提醒，不要求现场人员确认此类提醒，也不建立 MES 后续待办、确认状态或异常审计事件；只保留自身物理卸货、本地任务终态和车辆释放的正常业务审计。
_Avoid_: MES 状态变化作为卸货完成条件、等待 PDA 确认后放车、用轮询消失替代本地物理结果、MES 后续操作提示或确认、MES 后续待办或未确认告警

**目的站接收非门禁（DestinationReceiptNonGate）**:
车辆到达目的站并满足既有卸货安全条件后，8005 直接开始开仓卸货，不先征询目的站人员是否接收，也不提供暂不收货、拒收或稍后接收的业务状态；开仓后的货物取出仍按既有卸货物理闭环收敛，目的站人员后续是否以及何时执行其自身流程不构成 8005 的任务门禁。
_Avoid_: 到站接收确认、暂不收货等待、拒收状态、等待目的站后续流程才开仓

**TransportSelectionAlert（选任务告警）**:
8005 项目在从已保留的 TransportDemand 中选择可执行需求时，因起点或终点无法解析、命中执行排除规则或其它执行资格无法成立而形成的后续业务告警；它不由 MesIngest 产生，也不删除或改写 TransportDemand。
_Avoid_: IngestAlert、MES 查询失败、删除不可执行需求、把调度资格判断塞回接入层

**LoadPreparationAlert（装货准备告警）**:
8005 项目在已选运输需求进入仓位分配和装货准备时，因 PACKAGE 容量未覆盖、ExpectedBasketCount 无法形成或其它装货前置条件不成立而产生的业务告警；它不由 MesIngest 产生，也不允许用人工估算绕过阻断。
_Avoid_: IngestAlert、TransportSelectionAlert、默认花篮容量、报警后仍开锁

**TransportDemandWaitingAge（运输需求等待时长）**:
从 TransportDemand 在 8005 首次创建起连续累积的本地等待时间；任何业务门禁、车辆短缺或资源占用都不暂停或重置它，但只有任务当前通过硬准入时才参与派车排序。
_Avoid_: MES `DATES`、仅可派时长、门禁阻断时暂停、恢复可派后重新计时

**FactoryMesTaskQueryVersion（工厂 MES 任务查询版本）**:
工厂 IT 正式提供、用于形成当前六类候选集合的具体 SQL 版本；每版必须绑定提供方、接收日期与 SHA-256。对当前版本的信任不自动延伸到未知未来版本；任务类型、输出字段或筛选语义变化时必须重新审查。
_Avoid_: 永久信任任意同名 SQL、无来源版本、只按文件名识别查询

**MesAreaEndpoint（MES AREA 机台端点）**:
TransportDemand 中由 `EQP + AREA` 表达的唯一机台端点；TASK_TYPE 决定它的运输方向：`STAGING_TO_WIRE` 中是终点，其余五类任务中是起点。另一端由 FixedTaskStation 提供，不从 MES 推导第二个 AREA。
_Avoid_: 两个 MES AREA 端点、只凭 AREA 忽略 EQP、根据 STEP 猜测方向

**EquipmentAreaAssignment（机台区域归属）**:
一台 MES 机台归属一个 AREA 的地点关系；该关系由设备主数据中的 EQP 与 AREA 决定，工序不参与唯一性判断。当前一个 AREA 可以对应多台机台，客户完成后续调整后才计划收敛为 AREA 与机台一一对应；当前业务判断不得提前假设未来的一一对应已经成立。
_Avoid_: 用 STEP 限定机台—AREA 唯一性、一台机台多个 AREA、把当前多机台共享 AREA 当成已满足目标、提前依赖未来一一对应

**AreaEqpUniquenessMonitor（AREA 机台唯一性监控）**:
8005 对 DispatchZoneAreaAssignment 中每个 AREA 持续验证其在设备主数据中恰好对应一个 EQP 的项目工具；服务启动、分区 AREA 归属变更时立即检查，并按可配置周期重复检查。结果为零、多台、查询失败或超过新鲜度期限时形成选任务告警并暂停新的相关选任务，已在执行中的任务不受影响；EQP 是否对应多个 AREA 由客户 MES 自身卡控，8005 不做反向重复检查。
_Avoid_: 只取第一台机台、按 STEP 检查、使用过期结果继续选任务、影响已执行任务、全厂 EQP 反向唯一性检查、MesIngest 告警

**MesIngestWatch**:
面向现场实施与运维工程师的只读 MES 接入运维台，用于判断接入健康、核验 TransportDemand、分析 IngestAlert 与 MES→MesIngest 链路延迟；它不拥有投影真相，也不执行调度或生产操作命令。
_Avoid_: 生产操作 HMI、调度台、TransportDemand 编辑器、只看列表的盯盘页

**MesIngestLocalAdministration（MesIngest 本地管理）**:
仅由数据库主机上的授权运维人员执行、用于提交 HistoryResetAcknowledgement 或恢复 StoragePressurePause 等高风险运行状态的管理边界；MesIngestWatch 只呈现状态和指引，不承载这些写操作。
_Avoid_: Watch 业务按钮、远程管理 API、直接修改业务表、普通只读 Host 查询

**MesIngestCutoverRun（MesIngest 切换运行）**:
由唯一 CutoverRunId 标识、在一次计划停机窗口内完成墓碑播种、新库门禁和旧库自动删除的一次性受控运行；它结束后临时删库权限随之失效，不能变成常驻 Host 后台任务。
_Avoid_: 日常 Host 启动、无人值守重试、按名称前缀批量删库、长期迁移模式

**NewMesIngestContract（新版 MesIngest 契约）**:
Host、Watch 与 reference consumer 同时使用的唯一 V2 业务读取契约；身份由精确 contractVersion、schemaVersion 和完整 capability ID/version 集合共同组成，规范文档固定为 `/openapi/v2.json`。任何身份差异都先拒绝业务解释，不把缺字段、未知状态、附加能力或客户端单页过滤当作兼容降级；旧 V1 只可作为 Development 隔离面存在。
_Avoid_: 仅比较主版本、宽松 capability 子集、旧 DTO fallback、用 `/openapi/v1.json` 证明 V2、生产双契约

**HistoryEpoch（历史纪元）**:
一次连续可追溯 MesIngest 数据库历史的稳定身份；计划空库切换或不可恢复的数据库重建会产生新纪元，所有快照、目录与游标身份都不得跨纪元复用。
_Avoid_: HostSessionId、ProjectionCommitId、CatalogRevision、应用版本

**HistoryResetAcknowledgement（历史重置确认）**:
数据库无备份丢失后，由运维人员明确接受旧历史和 ArchivedDemandKeyTombstone 已不可恢复、授权新 HistoryEpoch 重新开放外部当前读取的确认事实。
_Avoid_: Host 自动重启、RestartBarrier 完成、Watch 关闭错误横幅、自动重试

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

**RetentionEligibleDemandSeries（可清理需求系列）**:
已经归档、当前 Demand 不处于 `VISIBLE` 或 `LONG_GONE_BUT_VISIBLE`、且没有活动 DemandSeriesCurrentCondition 或 DemandSeriesErrorPeriod 的 DemandSeries；任一新观测、条件或事件都会取消其历史清理倒计时。
_Avoid_: 单纯超过创建时间、仍可见的归档 Series、仍有活动错误的 Series

**ArchivedDemandKeyTombstone（归档需求键墓碑）**:
RetentionEligibleDemandSeries 的详细历史清理后永久保留的最小 TransportDemandKey 归档事实；它维持原 Series 身份与不可重新外读的结论，使后来重现仍属于 `LONG_GONE_BUT_VISIBLE`。
_Avoid_: 完整归档历史、可恢复 DemandSeries、临时缓存、允许旧键重新成为新 Series

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
错误检索默认查看截至 ErrorSearchAsOf 的最近 7 天，并提供最近 24 小时、7 天、15 天和全部历史；全部历史仍由 Host 有界分页。
_Avoid_: 默认全部历史、Watch 下载后本地分页、沿用 IngestAlert LastSeenAt 窗口

**ErrorSearchRollingWindow（错误检索滚动窗口）**:
最近 24 小时、7 天和 15 天分别表示以 ErrorSearchAsOf 为终点的精确 `24`、`7×24`、`15×24` 小时；显示可转换为带时区标识的用户本地时间，但不按本地自然日或午夜取整。
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
绑定完整规范化筛选、固定顺序、ErrorSearchAsOf 和契约版本的 keyset 位置；结构无效或验签失败返回 `INVALID_ERROR_SEARCH_CURSOR`，已验签但跨快照、筛选、窗口、顺序、页大小或契约复用返回 `ERROR_SEARCH_CURSOR_MISMATCH`，引用的投影提交不再保留则返回 410 `ERROR_SEARCH_SNAPSHOT_NOT_FOUND`。Watch 保留旧结果并提示失败，不自动冒充第一页。
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

**OverviewAttentionExplanation（概览关注解释）**:
与 OverviewAttentionEvent 在同一概览快照中冻结的结构化操作员解释，用明确事件语义、业务对象和最小诊断事实回答“发生了什么”；它保留语义下钻所需身份，但不是 Watch 事后追加查询或原始事件 JSON。
_Avoid_: 只有技术大类的标题、逐行补查当前详情、把原始事件码当作正常界面文案、完整原始观测

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
一轮完整成功 MES 快照中属于同一 TransportDemandKey 的全部原始行；在其原始观测可用窗口内必须按原样提供给 Watch，不能通过任选、补值或冻结旧值掩盖源数据。
_Avoid_: 只保留第一行、用历史值填充当前 NULL、只保存外部合格数据

**RawObservationAvailabilityWindow（原始观测可用窗口）**:
DemandRawObservation 自所属 PollTrace 完成起保证可按 PollTrace 与 ProjectionCommit 完整读取的 15×24 小时 Host UTC 窗口；窗口外清理表示历史已过期，不能解释为源轮次当时没有观测。
_Avoid_: 自然月、MES `DATES` 窗口、全部历史永久在线、Watch 缓存期限

**StoragePressurePause（存储压力暂停）**:
Host 因持久化空间低于安全边界而在读取 MES 前进入的保护状态；它保留并继续提供最后成功投影，但没有取得新快照或判定 Demand 缺席的权威。
_Avoid_: Oracle 查询失败、查询后落库失败、继续轮询但丢弃证据、自动伪造 GONE

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
外部程序在创建 OrderIntent 或开始调度的执行承诺点，经最终读取确认后连同 HistoryEpoch、CatalogRevision 与接受时间保存的不可变合格 Demand 事实；后续实时变化或退出目录不得改写它，旧纪元快照不得跨纪元复用。
_Avoid_: Ingest 冻结 TransportDemand、当前目录缓存、用最新 MES 数据改写历史决策证据

**DemandRevision（需求修订号）**:
MesIngest 对一个 Demand 世代当前决定事实的单调修订号；外部程序在执行承诺点必须最终重读并精确核对它，但它不是业务身份或远程调用幂等键。
_Avoid_: CatalogRevision、DemandId、DispatchRevision

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
绑定 ReadabilityAuditSnapshot、规范化筛选、AreaFilterProfile 的 MesArea 值集合、固定顺序和契约版本的 keyset 位置；结构无效或验签失败返回 `INVALID_READABILITY_AUDIT_CURSOR`，已验签但跨快照、筛选、AREA、顺序、页大小或契约复用返回 `READABILITY_AUDIT_CURSOR_MISMATCH`，引用的投影提交不再保留则返回 410 `READABILITY_AUDIT_SNAPSHOT_NOT_FOUND`。失败时保留旧结果，不自动冒充第一页。
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
当前 MesIngestWatch 实例用于缩小 DemandSeries 与资格审计页面显示范围的本地命名配置，内容是一组合法 MesArea；两页共享当前选择并按 MesArea 精确匹配。显示范围以用户显式应用时持久化的 AREA 序列快照为权威：文件编辑、非法、删除或进程重启均不自行改变范围，只有再次显式应用才替换快照，文件漂移按解析后的 AREA 序列而非注释、空行或其它原始文本差异判定。它不改变 WatchDemandProjection、外部可读资格、ExternallyReadableDemandCatalog 或 Dispatch 的 AREA 范围。
_Avoid_: AREA 白名单、调度范围、外部可读规则、以 Area 文件当前内容作为生效范围、文件变化自动改范围、用 SQL Server 或 Oracle 结果代替本地活动快照证据

**TransportDemandKey（运输需求业务键）**:
由 SUBLOT 与 WorkType（MES `TASK_TYPE`）组成，标识该 SUBLOT 在当前工序类型中的同一搬运候选，也是调度侧本地取消的永久抑制边界；同一 SUBLOT 命中其它 WorkType 时属于不同业务键。
_Avoid_: DemandId、只用 SUBLOT、SUBLOT+STEP、MES 需求编号、取消后重建同键任务

**TransportDemandSuppression（运输需求抑制）**:
调度以 TransportDemandKey 记录的永久禁止业务执行事实；`CANCELLED_BY_OPERATOR`、`CANCELLED_BY_LOAD_COMPENSATION`、`CANCELLED_BY_STOP_COMPLETE`、`CANCELLED_BY_STATION_TIMEOUT` 与 `TERMINATED_BY_FAULT_CARGO_HANDOFF` 均写入该事实，单纯 `MES_DISAPPEARED` 或 `GONE` 不写入。命中后不得创建、恢复或派发业务任务，但被取消或终止的具体实例仍以 DemandId 保留终态，MesIngest 的事实投影不受影响；它不因时间、轮询、`GONE`、重启或新 DemandId 自动解除，当前版本不提供解除入口。
_Avoid_: DemandId 抑制、只按 SUBLOT 拉黑、从 MesIngest 隐藏候选、自动过期、`GONE` 后解除

**TransportDemandCompletion（运输需求完成事实）**:
在 WIRE_TO_GATE MVP 适用性剖面中，ControlServer 在本地运输成功与安全闭环后，与 DemandId 成功终态原子保存的永久事实；它以 TransportDemandKey 为键，引用完成 DemandId、AcceptedDemandSnapshot 中的 DemandRevision 审计副本、完成时刻与完成证据，阻止同键持续可见、GONE 后新 DemandId 或重启造成重复执行，但不同 WorkType 不受影响。
_Avoid_: TransportDemandSuppression、MES 完工、按 DemandId 临时防重、GONE 后自动解除

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

**WireToGate**:
运输任务类型代码 `WIRE_TO_GATE`：焊线或键合完工机台 → 同图固定关卡站点。它以 MesIngest 发布的完整 WorkType 为业务边界，下游不再按 STEP、EQP 或文本将焊线与键合二次分类。
_Avoid_: 只按口语“焊线完工”缩窄范围、下游自行重新判定 TASK_TYPE、焊线和键合分为两种本地任务

**StagingToWire**:
运输任务类型代码 `STAGING_TO_WIRE`：同图固定派工待送站点 → MES 指定的焊线或键合机台，即机台叫料。起终点规则与其余五类相反（起点固定区域，终点取查询 EQP/AREA）。清洗完工送焊线、氮气柜送焊线或键合都属于这一类，不另建任务类型。
_Avoid_: 清洗送焊线任务、氮气柜送焊线任务、CLEANING_TO_WIRE、按产品实际存放处另选取货站点

**WireToNitrogen**:
运输任务类型代码 `WIRE_TO_NITROGEN`：WireBond1 机台 → 固定氮气柜站点。起终点规则同 `WIRE_TO_GATE`（起点取查询 EQP/AREA，终点固定区域）。PDA 扫码入柜后该行从 MES 快照消失；之后再上 WireBond2 由既有 `STAGING_TO_WIRE` 覆盖，不另建任务类型。不含键合。
_Avoid_: WIRE_TO_N2、WIRE1_TO_N2_CABINET、氮气柜任务（无代码名）

**8005 项目独占充电桩（ProjectExclusiveChargingStation）**:
在 8005 独占充电桩名册中以 `RIoT 地图 + 站点标识`登记、经批准限定为只服务 8005 项目车辆的充电站点，是 8005 自动充电与充电失败改派的唯一充电桩类型。
_Avoid_: 共享充电桩、归属未知充电桩、仅凭当前无车占位推定为项目独占

**8005 独占充电桩名册（ProjectExclusiveChargingStationRegistry）**:
项目级的受控充电桩身份集合，以 `RIoT 地图 + 站点标识`记录每个 8005 项目独占充电桩及其批准和变更记录；每辆 AGV 的候选充电桩集合只能是该名册的子集。
_Avoid_: 每车候选充电桩配置、RIoT 全部充电站点、无审计的人工勾选列表

**地图等待点集合（MapWaitingPointPool）**:
8005 从一张 RIoT 地图的普通站点中受控登记的专用车辆待命站点集合，供已经结束当前用途、没有下一业务目标且需要进入待命的车辆共用；等待点不得同时承担业务或充电角色，也不得与这些角色站点共享物理坐标。充电失败清桩时它是自动腾空原桩的优先去向，但授权确认的其它安全位置仍可完成清桩；候选点必须位于当前地图、身份有效、路线可达且未被占用或预占，无合格点时原地排队并告警，不猜测其它站点。
_Avoid_: 每次任务完成都返回、达到充电完成阈值即返回、清桩必须到等待点、复用业务站或充电站、不同角色站点坐标重合、每桩专属等待点、单点无竞争、按站点名猜测、临时最近站点

**站点业务角色（StationOperationalRole）**:
8005 赋予一个普通 RIoT 地图站点的受控用途分类，例如业务作业、车辆待命或充电；RIoT 站点身份只表示地图位置，不自动成为 8005 的任一业务角色。角色不能由站点名称、坐标或现场习惯猜测，必须绑定明确的 RIoT 地图与站点身份。
_Avoid_: RIoT 原生业务站点类型、按名称识别等待点或充电点、同坐标即同一业务身份、未登记角色自动生效
_Note_: 8005 自建充电机制下充电桩是**普通站点**，RIoT 的 `type` 与 `user_define_properties` 都不标识它（`type=2` 是 RIoT 本体充电机制的标记，本项目不走那条路），故 ProjectExclusiveChargingStationRegistry 是充电桩身份的**唯一**来源且不可与 RIoT 交叉校验；等待点同理。另注 SingleBerthStationClaim（公共业务点）、WaitingPointExclusiveClaim（等待点）与 ChargingStationExclusiveReservation（充电桩）是**同一个站点独占原语**在三种站点角色上的实例，共用同一张按 `(MapId, StationId)` 键的独占记录，不是三套机制。

**等待点车辆适用范围（WaitingPointVehicleScope）**:
MapWaitingPointPool 中每个等待点对同一 RIoT 地图内车辆的适用边界：默认允许该地图全部车辆参与选择，也可配置明确车辆白名单；一旦存在白名单，只有名单内车辆具备该点资格。适用范围只提供候选资格，不能绕过地图一致、路线可达、占用、预占和数据新鲜度等运行门禁。
_Avoid_: 所有等待点强制逐车绑定、配置白名单后仍允许其它车辆、跨地图默认开放、把候选资格当作当前可用

**车辆用途占有（VehiclePurposeClaim）**:
服务端对一辆 AGV 当前由搬运、充电、清桩/维护或空闲返回中的哪一种用途独占使用的业务事实；既有用途或结果未知时持续占有，只有该用途按自己的收敛边界结束后才能释放给另一用途。强制充电高于普通搬运，普通搬运高于空闲返回，空闲返回只在没有其它合法用途时取得占有。
_Avoid_: 各流程分别抢车、结果未知即释放、空闲返回预留车辆、用优先级抢占已开始用途

**空闲返回资格（IdleReturnEligibility）**:
车辆已经结束当前用途、没有下一业务目标或未结订单、没有充电/清桩/维护门禁，当前电量高于 MandatoryChargeEntryThreshold，且本轮 TaskFirstDispatchSelection 没有为其选定搬运用途时，才具备返回地图等待点的资格。
_Avoid_: 完成一步即返回、强制充电车辆先去等待点、有未结订单仍返回、空闲返回压过搬运

**空闲返回承诺（IdleReturnCommit）**:
服务端基于同一份新鲜资格快照，原子取得车辆的 IDLE_RETURN VehiclePurposeClaim 与一个具体等待点的 WaitingPointExclusiveClaim 后形成的当前用途承诺；承诺形成后不因新到搬运任务或更低电量车辆而抢占，直至到点收敛或按已确认失败规则释放。
_Avoid_: 只选点不占车、只占车不预占点、建单后改去新任务、结果未知时撤销承诺

**等待点独占（WaitingPointExclusiveClaim）**:
一辆车辆对具体地图等待点从已承诺前往到实际停留期间的单车独占关系；到点后由在途预占转为在点占用，只有确认该车已经离开才释放给下一辆车。
_Avoid_: 候选即占有、到点即释放、下达离点订单即释放、同一点同时预占多车

**空闲返回待定（IdleReturnPending）**:
车辆具备 IdleReturnEligibility 但当前没有可原子取得的合格等待点时保持原位的可恢复状态；它不取得 VehiclePurposeClaim 或 WaitingPointExclusiveClaim，因此后续强制充电或合法搬运仍可先取得车辆，相关事实变化后再重新评估并对持续等待告警。
_Avoid_: 无点仍建单、猜测临时站点、待定即预留车辆、定时盲目重复下单

**充电桩健康不可观测（ChargingStationHealthUnobservable）**:
8005 项目充电桩不联网且不对项目系统提供故障或健康状态；系统无法从一次充电失败直接确定充电桩是否故障，也无法自动证明它已恢复。
_Avoid_: 充电任务失败即证明充电桩故障、等待超时即证明充电桩恢复、从 RIoT 车辆状态反推充电桩健康

**已确认充不上（ConfirmedUnableToCharge）**:
8005 在车辆、订单、预占和目标充电桩身份一致，车辆已到该桩并实际执行开始充电后，依据无未知或冲突的新鲜事实确认充电未成立的业务事实；RIoT 自身内部重试结束后的首次严格确认失败即形成该事实，8005 不再对原车原桩追加开始充电重试，也不据此对车辆或充电桩归责。
_Avoid_: 充电类 HANG、未到桩、导航不可达、车辆不可执行、自由文本失败提示、结果未知、同车同桩项目层追加重试、充电桩故障

**已确认充电中断（ConfirmedChargingInterruption）**:
车辆、订单、预占与充电桩身份一致且曾以新鲜连续事实确认正在充电，但在未达到 ChargingCompletionThreshold、也没有正常停止命令时，以无未知或冲突的事实确认充电非预期停止的业务结果；它同时触发原桩 ChargingStationAllocationHold、当前车辆 VehicleChargingEligibilityHold 与既有清桩流程，但不自动区分人为关闭、充电桩急停、车辆问题、充电桩问题或其它原因，也不授权原桩自动重启或车辆逐桩试充。
_Avoid_: 单次状态抖动、数据过期、读取失败、车辆失联、正常完成、正常停止、只暂停充电桩、自动归责充电桩、原桩自动重启、车辆逐桩试充

**车辆充电资格暂停（VehicleChargingEligibilityHold）**:
确认充不上、充电中断或充电无进展但尚未查明原因时，对当前车辆施加的临时能源业务门禁；车辆不得预占或尝试其它充电桩，也不得承接普通搬运任务，但在位置、订单、运动与安全事实完整时仍可受控清桩并前往等待点或维修位置。现场证据确认原因只在充电桩或人为操作且车辆充电能力核验正常时可单独解除车辆侧暂停；确认车辆问题或原因仍未知时继续保持，且不妨碍已核验正常的原充电桩独立恢复。
_Avoid_: 整车永久故障、逐桩试车、换桩即诊断、暂停车辆即阻止安全清桩、恢复充电桩即恢复车辆、原因未知自动恢复

**充电失败撤桩（ChargeFailureStationClearance）**:
确认充不上、充电中断或充电无进展后，将车辆与原充电桩安全物理分离的资源交接；系统确认车辆已到达地图等待点，或授权现场人员确认车辆已移至安全位置且原桩已腾空，任一证明均可完成清桩。清桩只释放原桩预占并保持充电桩暂停，既不恢复桩的分配资格，也不恢复车辆的充电资格；两者分别核验和恢复。
_Avoid_: 取消终态即腾桩、必须到达等待点才能闭环、人工清桩一律禁止派车、清桩即解除充电桩暂停、清桩后立即派另一辆生产车试桩、用普通调度代替维护诊断

**清桩中（ChargingStationClearancePending）**:
已确认充不上、充电中断或充电无进展且充电桩已暂停，但相关车辆尚未以系统到达事实或人工清桩确认证明已腾空原桩的过渡状态；期间原充电桩预占和暂停均保持。
_Avoid_: 订单已取消、充电桩已恢复、车辆已就绪

**人工清桩确认（ManualStationClearanceConfirmation）**:
维护管理员或系统管理员以个人账号确认相关车辆已移至安全位置且原充电桩已腾空的受审计事实；它只完成清桩，不直接决定充电桩恢复、车辆充电资格或车辆业务就绪。
_Avoid_: 双人必签、普通操作员确认、清桩即解除充电桩暂停、清桩即恢复或阻断车辆派车

**充不上现场确认（UnableToChargeFieldConfirmation）**:
严格系统事实不完整时，由维护管理员或系统管理员以个人账号确认具体车辆已在具体充电桩实际尝试开始充电但充电未建立的现场事实；它不补写订单事实也不作故障归因。
_Avoid_: 普通生产操作员确认、共享账号确认、人工覆盖身份冲突、充电桩故障确认

**充电桩暂停分配（ChargingStationAllocationHold）**:
8005 保留充电桩在 ProjectExclusiveChargingStationRegistry 中的稳定身份，但因确认充不上、充电中断、充电无进展或授权维修而暂停向全部项目车辆分配的受审计门禁；授权维修用该门禁实现运行时退出候选，不建立计划维护流程，也不临时删除名册身份。只有现场检查或维修后的明确人工恢复才能解除，永久拆除、改名、换地图或退出 8005 才修改名册。
_Avoid_: 充电桩已故障、临时删除名册、逐车移除候选、独立计划维护流程、定时自动恢复、换车试桩

**充电桩暂停事件（ChargingStationAllocationHoldEvent）**:
一次暂停分配的不可变审计记录，绑定唯一事件、触发类型、充电桩名册身份与版本、时间及原始证据；由确认充不上、充电中断或充电无进展触发时还须绑定车辆、预占、订单和关键观测且根因保持 `UNKNOWN`，由授权维修触发时记录发起人、维修原因与预计处置但不虚构故障。重复提交同一事件只返回原结果。
_Avoid_: 重复暂停记录、可编辑失败原因、维修意图冒充已确认故障、无身份或时间的汇总告警

**充电桩恢复确认（ChargingStationRecoveryConfirmation）**:
维护管理员或系统管理员在清桩完成或确认没有活动占用，并经现场检查、维修或处置后以个人账号提交、绑定原暂停事件与充电桩名册身份、明确允许该桩重新参与分配的业务事实；它不表示系统已取得充电桩健康遥测。恢复只重开正常选桩资格评估，不证明桩位空闲、不自动重试原订单也不自动取得新预占；它与相关车辆的对账和充电资格恢复互不等待。
_Avoid_: 第二管理角色代确认、普通操作员恢复、定时恢复、换车试桩、无新事件代次校验的恢复

### 实施范围与顺序

**架构不变量（AllocationArchitectureInvariant）**:
当前已实施的服务端分配语义或跨端契约中，一条被现行代码或协议 schema 强制成立、且任何新条目
若要推翻就必须重做既有实现的性质。完整产品语境下已识别八条：车辆占用必由一条 TransportDemand
引起、全系统至多一辆车与一条未收敛 journey、一次承诺等于一条 Demand 加固定两段行程、站点没有
独占概念、车载对 Demand 是只读投影绝不发现选择或绑定、站点任务类型准入必在装货腿检查并冻结
（见 LoadLegAdmissionBinding）、车载持有并声明自身仓位配置而服务端只记录不裁决，以及仓位可互换、
任何仓位服务任何站点。它描述现状，不是需求，也不是设计目标。**这个集合是逐步识别出来的，
不是一次穷举得到的**：前五条来自票 02，第六条由票 13 在判定 `STAGING_TO_WIRE` 方向反转时补充识别，
第七条由票 05 补充识别，第八条由 program#70 在前后仓位分侧需求中补充识别，
因此后续票据遇到「某条新能力似乎要重做既有实现」时，应先检查它是否推翻了一条尚未列出的不变量。
_Avoid_: 设计原则、架构约束（泛称，二者不含「现已被强制成立」这一层）、把它当作需求条目引用、
把已列出的条目当作封闭集合

**重构类条目（ArchitectureBreakingItem）**:
其实现要求推翻至少一条架构不变量的需求条目。判定是条目的内在性质，与实施先后无关，也与该条目
是否属于全新能力无关——一项全新能力若完全建立在新原语之上而不推翻任何既有前提，仍是增量类条目。
_Avoid_: 大改造、新功能、重做（三者都把「全新」误当作「推翻既有」）

**增量类条目（IncrementalItem）**:
其实现不推翻任何架构不变量的需求条目。合法形态只有两种：在既有 fail-closed 资格链上增加一个
可独立求值的谓词，或在分配核心之外新增表、审计、界面与配置版本。增量类条目仍可能硬依赖某条
不变量已被推翻，也仍可能强制改变协议消息面——两者与本分类正交。
_Avoid_: 小改动、锦上添花、纯配置（三者都暗示工作量小或可省，本词不含此义）

**多停靠执行计划（MultiStopExecutionPlan）**:
一辆车在一次派发中承载的、按站点排定的多条 TransportDemand 的完整停靠序列；计划而非单条 Demand
才是行程段、停靠顺序与运行阶段的归属主体。它取代「一次承诺等于一条 Demand 加固定两段行程」这一
前提，因此同一站点可有多条待装或待卸 Demand，而车辆的运行阶段必须按停靠或按 Demand 而不是按车
表达。
_Avoid_: 复合任务、任务批、订单合并（三者都暗示多条 Demand 被合并成一条，而本词要求每条
Demand 保留自身任务类型、起终点、状态、取消、仓位和审计边界）

**证据受限实施（EvidenceLimitedImplementation）**:
需求要求的门禁与代码路径已完整实现，但其判据依赖的外部证据当前不可得，故运行时恒走该需求自身
规定的保守分支。它是一种**已实施**形态而非未完成形态：条目要排进批次、要写代码、要有验收证据，
只是证据形态只能证明「门禁正确拒绝」而非「正确放行」。外部证据具备后无需改代码即自动生效。
_Avoid_: 延后、未实现、降级实现、占位实现（四者都暗示需求没做完，而本词恰恰相反——门禁是完整
的，缺的是外部输入）

**需求变更待批（PendingRequirementChange）**:
条目要实施，而且要按与基线文本不同的形态实施；据此产出一份 RequirementChangeProposal，提案在
批准前不改基线，实施据修订后的文本执行。它既不是延后（工作照做）、也不是范围外（在目标之内）、
更不是 EvidenceLimitedImplementation（后者恒走需求自身规定的保守分支，本形态则是偏离需求文本）。
提案未批准前，该条目的验收证据不得表述为「符合」被偏离的那条需求，正确写法是「实施形态与基线
原文存在一条已知且已记录的偏离，处置见 CP-NNNN」。剖面里它按正常条目排期，批次归属不因它变化。
_Avoid_: 需求作废、废弃、例外、豁免（四者都暗示需求文本失效或被绕过，而本词要求文本照改，只是
改之前先如实记录偏离）

**需求变更提案（RequirementChangeProposal）**:
承载 PendingRequirementChange 的实体，编号 CP-NNNN（四位十进制，不把年份或批次编进 id）。含
状态、目标基线版本、逐条修订项（每项给基线原文、建议修订文与修订说明），以及提案边界——哪些
相关条目经核查不需要修订及其理由。批准人是需求基线的批准人一人，**与 ProtocolRelease 要求两名
不同产品负责人签 attestation 不是同一件事**。批准后按语义递增基线版本、重算 Baseline SHA-256、
打新的 annotated tag；**旧 tag 与已归档证据一律不动**——证据绑定的是它当时的基线哈希，换版后
旧证据仍然有效地证明它当时证明的那件事，需要重证时建立新运行。
_Avoid_: 需求澄清、勘误、补丁（三者都暗示不改变文义，而本词的修订项以改变文义为常态）、ADR
（后者记录设计决定，不改需求文本）

**确认页回显（ConfirmationEcho）**:
车载端在提交作业清单选任务时一并回传的、它实际展示给操作员的业务字段副本（完整 SUBLOT、任务
类型、起点、终点及应装花篮数），供服务端逐字段比对以证明展示内容与权威清单一致。它把「完整
展示」从不可验证的界面实现要求变成可验证的跨端契约，且不规定车载端如何呈现。
_Avoid_: 界面截图、渲染哈希、录像留证（三者被基线明确排除，结构化事实足以复核）、仅回传
DemandId（无法区分系统展示错误与操作员放货错误）

**路网图快照（RouteGraphSnapshot）**:
控制服务端自 RIoT 取得并持有的、某一时刻某张 Map 的完整有向站点图，是全部站到站路径代价与
StationReachability 判定的唯一依据。它由设计态部分（边、站点及其到节点的定位）与运行态部分
（当前被移除的边与站点）合成，两部分各自刷新；任一部分取不到、或取证条件已变时快照**整体**
进入陈旧态，此时既不产出任何路径代价，也不产出任何可达性结论。它不承载建单前置可达确认，
那一道门禁仍由实时 RIoT RouteCost 承担。
_Avoid_: 地图缓存、路网缓存（二者不含「陈旧即整体失效」这一层）、以陈旧快照继续计算、
设计态与运行态同周期刷新、局部陈旧仍产出部分结论

**站点可达性（StationReachability）**:
在当前 RouteGraphSnapshot 上，自某站点节点是否存在到另一站点节点的有向路径。图上不可达是本项目
作业图的**常态而非异常**——现场实测每个站点平均只能到达其余站点的九成，且存在与任何站点互不可达
的孤立站点——因此判为不可达的车辆或候选静默退出本轮比较，不告警，不计入异常。它与
RouteCostEvidenceBoundary 所述的成本证据缺失是两件事：前者是图给出的确定结论，后者是图本身不可用。
它也不同于建单前置可达确认：那是下单动作前的独立门禁，由实时 RIoT RouteCost 承担，两者都要通过。
_Avoid_: 直线距离可达、把图上不可达当作异常告警、可达性与成本证据缺失合并处置、
以 RIoT 的单次查询结果替代图判定、以本判定顶替建单前置可达确认


**装货腿准入绑定（LoadLegAdmissionBinding）**:
现行实现把 StationTaskTypeAdmission 的检查、携带与冻结全部绑定在运输的装货那一腿上：准入身份只允许
挂在 LOAD 命令上，准入决策快照也只在 LOAD 路径按 SlotOperationAttemptId 冻结，UNLOAD 不携带准入参数。
它是一条架构不变量而非设计选择——由于准入表的键是「站点 × 任务类型」而站点侧取 MES AREA 机台站，
凡是 AREA 机台端为卸货端的任务类型（当前只有 `STAGING_TO_WIRE`），准入该检查的那一腿恰好是被禁止
携带准入身份的那一腿，因此推翻它必须重做准入的归属而不是调换参数。
_Avoid_: 准入发生在取货站（措辞把「装货腿」与「AREA 机台站」当成同一件事，而方向反转后二者分离）、
在 UNLOAD 上补一份准入检查而不动冻结归属（会产生两份可能不一致的准入事实）、
把它当作实施细节（它决定 `STAGING_TO_WIRE` 是重构类而非增量类，是票 09 的排序输入）

**等待点离点确认（WaitingPointDepartureConfirmation）**:
判定一辆车已实际离开其占用的等待点、从而可以释放 WaitingPointExclusiveClaim 的一致证据组合：
车辆 currentMap 仍是该等待点所在地图、currentPosition 不再精确匹配该等待点、车辆处于运动态，
且全部证据新鲜无冲突；四项同时成立才判离点。它对称于到点确认（REQ-0295）却没有对应的需求条目，
是实施决策而非需求——基线只在 REQ-0293 里说「确认车辆实际离点后才释放」，未规定证据构成。
_Avoid_: 下达离点订单即释放（REQ-0293 明文禁止）、由下一段行程的到点反推离点（车可能长期停驻，
独占永不释放）、单值 currentPosition 变化即判离点、把换图当作离点

**停靠目的类别（StopPurposeCategory）**:
一个计划停靠是为了业务装卸、前往等待点还是前往充电桩，三值 BUSINESS／WAITING_POINT／CHARGER。
它与「取货还是卸货」以及「站点是 AREA 机台站点还是 FixedTaskStation」两个维度正交：后两者只在 BUSINESS
下有意义，而等待点与充电桩停靠两者皆无。它是计划里可以存在不由 TransportDemand 引起的停靠这一
事实的表达方式。
_Avoid_: 把等待点或充电桩登记为 FixedTaskStation、用 legType 的一个新值同时表达目的与方向、
认为每个计划停靠都对应至少一条 Demand

**车辆用途占有与派发唯一性门禁的层次关系**:
VehiclePurposeClaim 约束的是用途层——一辆车同一时刻只有一种用途，该占有跨越该用途期间的全部
订单；DispatchUniquenessGuard 约束的是订单层——每辆 AGV 同时只被一个未终结订单占用。一次搬运
用途包含 2 至 9 个订单，车辆在相邻两个订单之间没有活跃订单行，此时只有用途层的占有仍然成立。
二者并存不冗余，缺任一层都会留下空窗。
_Avoid_: 用订单唯一索引代替用途占有、认为释放订单即释放用途、把两层唯一性合并成一张表
