# 决定充电阈值、配置变更与异常生命周期

Type: grilling
Status: resolved
Blocked by: 63

## Question

触发充电、最低接单和充电完成阈值之间应保持什么关系；修改车辆充电策略时是否必须先禁用车辆；下单、开始充电、充电中断、电量不增长或车辆失联分别允许多少重试、何时告警或结束，并如何衔接票据 59、62 已批准的选桩、失败确认、全车暂停、清桩和恢复边界？

## Evidence rows

`R03-A1672`、`R03-A1673`、`R03-A1711`、`R03-A1712`、`R03-A1714`、`R03-A1749`、`R03-A1758`、`R09-A0027`。

## Comments

- 2026-08-06：用户批准将触发充电阈值明确为 MandatoryChargeEntryThreshold（强制充电入口阈值）：无活动任务且当前电量达到或低于该阈值时，不得再接普通新任务并进入待充电流程；正在执行的任务即使途中越过该阈值也继续完成，完成后立即进入待充电流程。最低接单电量不是另一个当前电量开关，而是 DispatchBatteryEligibility 对预计任务完成后最低电量余量的硬门禁。只有接单时当前电量高于强制充电入口阈值，且预计任务完成后电量不低于最低任务后余量，才能接单；强制充电入口阈值不得低于最低任务后余量，以免形成既不能接单又不触发充电的电量区间。
- 2026-08-06：用户批准 ChargingCompletionThreshold（充电完成阈值）必须严格高于 MandatoryChargeEntryThreshold，以形成明确的充电回差；达到完成阈值只开始正常结束本次充电，不等于订单已经收敛、车辆已经离开充电桩或充电桩预占已经释放，后续仍须遵守既有订单、离桩、占用和预占收敛边界。
- 2026-08-06：用户批准修改充电策略不必先禁用车辆。编辑和保存草稿不影响运行；只有满足 `ChargingCompletionThreshold > MandatoryChargeEntryThreshold >= 最低任务后电量余量` 的不可变 ChargingPolicyVersion 才能激活。新版本只用于激活后的新派车判断和新充电周期，已经接受的搬运任务以及已经排队、取得充电桩预占、建单或正在充电的周期继续使用各自固定的原策略快照，不得因配置热切换而中断、撤销预占或改变完成阈值；空闲车辆在激活后立即按新版本重新判断，候选充电桩集合变更也只影响新周期。
- 2026-08-06：用户批准需求基线只固定三个电量阈值的语义、关系与变更治理，不写死具体百分比。具体数值必须在投运前依据车辆电池规格、典型任务耗电、最远安全返回距离和现场测试结果形成有批准人、适用车辆范围及生效时间的 ChargingPolicyVersion；没有已批准数值的车辆不得投运，系统不得采用未批准的开发默认值。后续每次调整均发布新版本并保留批准依据。
- 2026-08-06：用户批准车辆到达充电桩后，若 RIoT 已完成自身内部重试，“开始充电”仍以经验证失败结果结束并最终进入 `HANG`，首次严格事实组合即形成 ConfirmedUnableToCharge；8005 对原车辆、原充电桩追加开始充电重试次数为 0，立即按既有规则暂停该桩、清桩并使车辆回到统一电量队列。响应超时或结果未知不构成确认失败，不能盲目重试，必须保持预占并先对账。
- 2026-08-06：用户批准充电移动订单完全继承通用 RoutineOrderCreationCall 与 RIoTRetryReconciliation，不设置充电专属的重试次数。明确拒绝、传输超时或结果未知时保留车辆、充电意图、目标充电桩和 ChargingStationExclusiveReservation 的原绑定，不得重新选桩、换 upperId、创建第二张订单、释放预占或把车辆表示为正在前往/已经开始充电；电量下降只提高告警紧迫度。何时可证明订单不存在并以同一业务意图重试、何时释放绑定，继续由[决定 RIoT 建单未确认时任务绑定、重试与释放边界](80-decide-riot-order-creation-uncertainty-binding-retry-release.md)统一收敛。
- 2026-08-06：用户批准建立 ConfirmedChargingInterruption：车辆、订单、预占和目标充电桩身份一致，之前已以新鲜连续事实确认 `batteryState=CHARGING`，但在未达到 ChargingCompletionThreshold 且没有正常停止命令时，随后以无未知或冲突的经验证失败或 `HANG` 事实确认充电非预期停止。该结果不在原桩自动重新开始充电，触发原桩对全部 8005 车辆暂停分配，并进入既有订单收敛、清桩、统一队列和人工恢复流程；单次状态抖动、数据过期、读取失败或车辆失联不能形成该事实。
- 2026-08-06：用户补充 ConfirmedChargingInterruption 的真实原因可能包括人为关闭充电桩、拍下充电桩急停按钮、车辆问题或充电桩问题；该术语只表达已确认的中断结果，在取得可核查现场证据前不得自动归责。
- 2026-08-06：用户批准原因未知时实行双向临时隔离：原充电桩进入 ChargingStationAllocationHold，当前车辆进入 VehicleChargingEligibilityHold。车辆不得立即改派其它充电桩或承接普通搬运任务，但在安全与运动事实完整时可受控清桩并前往等待点或维修位置；现场证据确认仅为人为关闭、充电桩急停或充电桩侧问题且车辆充电能力核验正常后，可独立恢复车辆充电资格，充电桩仍等待自身恢复确认；确认车辆问题时可独立恢复已核验正常的充电桩而继续隔离车辆；原因未知时两侧均不自动恢复。用户明确指出该门禁防止故障车辆逐桩重试并把所有充电桩依次登记为不可用，导致其它车辆失去充电能力。
- 2026-08-06：用户批准用受控 ChargingProgressObservationPolicy 判定“电量不增长”：车辆持续处于 `batteryState=CHARGING`，车辆、订单、预占与充电桩身份一致，遥测连续、新鲜且无失联、读取失败或事实冲突，跳过开始充电后的正常稳定期后，在完整观察窗口内电量增幅未达到最小增量，且尚未达到 ChargingCompletionThreshold，才形成已确认无进展。稳定期、观察时长和最小增量依据车辆遥测精度、正常充电曲线与现场测试批准并进入 ChargingPolicyVersion，不在需求基线中虚构统一数值；任何数据缺口或冲突只形成结果未知。
- 2026-08-06：用户批准完整观察窗口首次确认电量无进展后形成 ConfirmedChargingNoProgress，不继续重复观察或自动重启。原充电桩进入 ChargingStationAllocationHold，当前车辆进入 VehicleChargingEligibilityHold，不在原桩重试或改派其它桩；系统请求结束当前充电订单并核验停止，确认后进入既有清桩流程。停止结果未知时保持车辆原位、原预占和两侧暂停并继续对账，现场诊断后车辆与充电桩按各自证据独立恢复。
- 2026-08-06：用户批准将“车辆失联”拆分为三类。VehicleConnectionSession 失效沿用既有车载—服务端连接规则：充电中不只因此停止充电或判桩异常，阻断该车新业务并继续通过 RIoT 观察，重连后完成恢复对账。ChargingRIoTVehicleObservationLoss 表示 RIoT 无法取得车辆位置、订单、运动或充电状态：立即暂停该车业务和充电资格，保持原桩预占并按车辆仍可能占桩处理，不发送依赖未知前置条件的新停止、重启或移动命令，不登记充电桩故障，立即告警并持续对账；持续时间只升级告警，不自动归因。ChargingBatteryTelemetryLoss 表示只有 `batteryState` 或电量无法读取：暂停完成阈值与无进展判断，保持原订单和预占；遥测恢复后只用新鲜连续事实重新开始观察，不用缺失前旧值补算窗口。只有恢复观测后明确证明充电非预期停止，才升级为 ConfirmedChargingInterruption 并双向隔离。
- 2026-08-06：用户批准任何充电观测失联或电池遥测缺失的持续超时都只按受控运维阈值升级告警和现场响应，不得自动结束订单、释放充电桩预占、移动车辆、改派其它充电桩或登记充电桩故障。只有重新取得新鲜状态完成对账，或取得授权人员对车辆、订单和桩位事实的现场确认后，才能继续、正常结束或清桩；恢复后分别按持续正常、已经完成或 ConfirmedChargingInterruption 的真实结果收敛，告警升级时长永远不是资源释放计时器。
- 2026-08-06：用户批准不建立独立“计划维护”流程。充电桩通常只在维修时退出运行时候选：维护管理员或系统管理员设置 ChargingStationAllocationHold，保留 ProjectExclusiveChargingStationRegistry 中的稳定身份并立即阻止新预占；若已有车辆且无紧急风险，待当前周期正常完成、车辆离桩后维修，存在安全风险时任何现场人员可直接操作物理急停并按 ConfirmedChargingInterruption 双向隔离。维修完成后通过 ChargingStationRecoveryConfirmation 重新参加资格评估；只有永久拆除、改名、换地图或退出 8005 才修改名册，不以临时删除或逐车修改候选集合实现维修暂停。

## Answer

用户于 2026-08-06 逐项批准并最终确认以下充电阈值、配置生效与异常生命周期：

1. **三个电量阈值具有不同判定时点并满足硬关系。** DispatchBatteryEligibility 使用预计任务完成后的最低电量余量；MandatoryChargeEntryThreshold 是空闲车辆停止承接普通新任务并进入待充电流程的当前电量门槛；ChargingCompletionThreshold 是开始正常结束本次充电的目标电量。配置必须满足 `ChargingCompletionThreshold > MandatoryChargeEntryThreshold >= 最低任务后电量余量`。正在执行的任务途中越过充电入口阈值不被中断，完成后立即进入待充电流程；达到完成阈值不等于订单收敛、车辆离桩或预占释放。
2. **ChargingPolicyVersion 受证据批准且按周期冻结。** 需求基线只固定语义、关系与治理，不虚构具体百分比、稳定期、观察时长或最小增量，也不允许开发默认值；参数须依据车辆电池规格、任务耗电、最远安全返回距离、遥测精度、正常充电曲线和现场测试在投运前批准，无已批准版本的车辆不得投运。编辑、保存和激活不要求先禁用车辆；新版本只作用于新派车判断和新充电周期，既有任务、排队、预占、建单与充电周期继续使用原策略快照。
3. **充电建单不建立专属重试制度。** 充电移动订单继承 RoutineOrderCreationCall 与 RIoTRetryReconciliation，结果未确认时保持车辆、充电意图、目标桩与预占绑定，不换 upperId、不换桩、不重复建单、不释放预占，也不表示已经前往或开始充电；电量下降只升级告警。绑定、同号重试与释放的通用边界由[决定 RIoT 建单未确认时任务绑定、重试与释放边界](80-decide-riot-order-creation-uncertainty-binding-retry-release.md)统一收敛。
4. **严格确认无法开始充电后，8005 原桩追加重试为 0。** RIoT 已完成自身内部重试后仍以经验证失败和最终 `HANG` 形成 ConfirmedUnableToCharge，即暂停原桩、清桩并进入统一电量队列；超时或结果未知不构成确认失败，须保持预占并先对账。
5. **已确认中断和无进展均采用双向临时隔离。** 已确认正在充电但在完成阈值前、无正常停止命令时非预期停止，形成 ConfirmedChargingInterruption；持续 `batteryState=CHARGING` 但经 ChargingProgressObservationPolicy 完整稳定期和观察窗口仍未取得最小电量增量，形成 ConfirmedChargingNoProgress。两者都同时触发 ChargingStationAllocationHold 与 VehicleChargingEligibilityHold，不在原桩重启、不换桩试充，结束并核验旧订单后清桩；结果未知时保持原位、预占与两侧暂停。
6. **中断结果与根因归属分离。** 人为关闭、物理急停、车辆问题、充电桩问题或外部供电都可能产生同一中断结果；原因未知时不得自动归责。车辆与充电桩按各自现场证据独立恢复，避免故障车辆逐桩试错并依次暂停全部充电桩。
7. **“车辆失联”按观测来源分开。** VehicleConnectionSession 失效只阻断车辆新业务并继续通过 RIoT 观察；ChargingRIoTVehicleObservationLoss 保持原桩预占、按车辆仍可能占桩处理且不盲发停止、重启或移动命令；ChargingBatteryTelemetryLoss 暂停完成阈值和无进展判断，恢复后以新鲜连续样本重新观察。任何失联或遥测缺失的持续超时都只升级告警和现场响应，永不自动结束订单、释放资源、改派、移动或登记桩故障。
8. **维修使用暂停分配而非临时删除身份。** 维护管理员或系统管理员用 ChargingStationAllocationHold 使待维修充电桩退出运行时候选，同时保留 ProjectExclusiveChargingStationRegistry 中的稳定身份；已有车辆且无紧急风险时等待当前周期正常完成后维修，有安全风险时任何现场人员可直接操作物理急停并按中断流程收敛。维修完成后通过 ChargingStationRecoveryConfirmation 恢复资格；只有永久拆除、改名、换地图或退出 8005 才修改名册。

上述术语与边界已同步写入根 [`CONTEXT.md`](../../../CONTEXT.md)。
