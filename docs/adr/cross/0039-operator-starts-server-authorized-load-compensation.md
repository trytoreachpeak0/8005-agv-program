# 操作员发起、服务端授权装货补偿

同事初稿 §2.2 将业务判断与仓位清单决定归服务端，§2.3 将开锁、门序列、DI/DO 和安全互锁归车载端；§23 提议的通用 OperationCancelCommand 已由 ADR-cross-0015 否决。装货硬件故障本身只会暂停并等待人工处置；只有 R-09 班组长或被显式授予等效生产管理权限的人员作出 LoadCompensationDecision 后，才采用原操作下的专用恢复阶段，而不是取消原指令或让车载端自行决定业务回滚。

流程如下：

1. 车载端发现仓位硬件或关键反馈故障后，停止尚未发送的开锁，不分配替代仓位，并可靠报告逐仓结果；锁 DI 等状态无法确认时进入 VehicleRecoveryRequired。
2. 服务端保持原 SlotOperationAttemptId、完整目标仓位、ProvisionalLoadState、整批预留和 StationOperationGuard，不自动转入 LoadCompensationRequired。
3. R-09 班组长或被显式授予等效生产管理权限的人员可以在普通生产操作员的当前作业界面即时再次刷卡或认证，并必须选择一个 LoadCompensationReasonCode。首版固定为：`HARDWARE_NOT_RECOVERABLE_ON_SITE`（现场无法恢复设备并继续原装货）、`PRODUCTION_ABORTS_CURRENT_LOAD`（生产决定不再继续本次装货）和 `OTHER`（其它原因）；前两项备注可选，`OTHER` 必须填写非空备注，空原因码和未知原因码均不得提交。仅有已登录会话不能作出 LoadCompensationDecision。二次认证形成的 LoadCompensationDecisionAuthProof 只绑定本次确认人、DemandId、SlotOperationAttemptId 和决定内容，不提供可复用有效时长。服务端在一次提交中消费该证据并持久化接受或拒绝结果；只有相同 MessageId 与相同内容的传输重发可以取得已有结果，换任务、换尝试、修改原因或备注，以及业务校验失败后再次提交都必须重新认证。认证、权限和业务状态均通过后，服务端记录原 Sublot 生产操作员、R-09 决策人、原因码和备注，接受决定并把原 SlotOperationAttemptId 置为 LoadCompensationRequired；R-09 的审批不替换 Sublot 操作员、不接管或重建 OperationSession。R-11 的 HardwareRecoveryConfirmation 只确认设备状态，普通生产操作员只能申请整批清空，两者均不能代替该业务决定；同一人兼任时必须同时具备两项独立权限并分别执行。其它详细记录字段和确认界面仍待单独确认。
4. 车载界面提示将取出本任务全部已放入或状态不确定的产品，但不得自动重新开门。
5. 已通过 OperationSession 核验的操作员在车载界面点击开始清空，车载端发送 `LoadCompensationRequested`。
6. 服务端核验人工处置决定、原 SlotOperationAttemptId、原目标仓位、逐仓结果和当前连接就绪状态后，下发同一 SlotOperationAttemptId 的可靠 `LoadCompensationCommand`。
7. 车载端将服务端授权范围与 OnboardExecutionJournal 中已完成或状态不确定的仓位核对一致后，按车载 IO 安全规则引导人工清空，并依据 ADR-cross-0040 的仓内光幕自动判定 EMPTY；两侧范围不一致、占用状态 UNKNOWN 或锁闭反馈仍无效时保持 VehicleRecoveryRequired，不猜测执行。
8. 车载端在相关仓位均为 EMPTY、由锁传感器确认锁闭且开锁输出回读确认为复位后可靠上报 `LoadCompensationResult`；服务端完成持久化和核验后才释放整批仓位预留，把原 SlotOperationAttemptId 结束为 `COMPENSATED`，并将原 DemandId 终结为 `CANCELLED_BY_LOAD_COMPENSATION`、持久化取消抑制，使它不再进入后续派车。三种 LoadCompensationReasonCode 的业务后果一致；原因码只用于解释与审计。

任一目标仓位未证明 EMPTY、锁闭反馈无效、开锁输出未复位、结果未被服务端可靠接受，或取消终态与取消抑制无法原子持久化时，均不得提前取消 DemandId 或释放预留；系统保持恢复状态和 StationOperationGuard，车辆不得离站。

服务端失联或 VehicleBusinessReadiness 未授予时只能显示待补偿状态，不能开始新的开锁动作。LoadCompensationCommand 是原 SlotOperationAttemptId 的恢复授权，使用新的 MessageId；它不改变初稿 §20 的 SlotOperationAttemptId 去重规则，也不是通用取消能力。

**Status**: accepted

**Considered Options**:
- 硬件故障后自动进入补偿并打开已装仓位（拒绝：故障可能使仓门锁闭状态不可验证，且人工尚未决定是否清空）
- 由 R-11 在确认硬件状态时同时决定整批清空（拒绝：设备安全判断与生产任务处置是不同职责，会让维护权限隐含获得生产取消权）
- 由普通生产操作员直接决定整批清空（拒绝：关键硬件状态曾经不可证明，不能复用正常离站前取消的低门槛）
- R-09 登录后直接确认，不再执行二次认证（拒绝：共享或遗留的登录会话可能把误触直接转化为整批清空决定）
- 二次认证在一段时间内可跨决定复用（拒绝：会把一次明确审批扩大为多个任务的隐式授权，也无法在业务校验失败后重新确认当前事实）
- 认证证据单次使用并绑定一个 DemandId、SlotOperationAttemptId 和完整决定内容；相同消息重发只返回已有结果（采纳）
- 只记录“已批准”或仅填写自由文本（拒绝：无法稳定统计、筛选和解释整批清空决策）
- 要求先退出生产操作员会话，再由 R-09 登录并审批（拒绝：会破坏同一 Sublot 固定生产操作员的追溯关系，并把审批误建模为作业接管）
- 复用普通任务取消的 `CANCELLED_BY_OPERATOR`（拒绝：会混淆普通操作员直接取消与 R-09 批准补偿的权限、流程和审计原因）
- 补偿清空使用专用 `CANCELLED_BY_LOAD_COMPENSATION`，三种补偿原因共享该终态（采纳）
- 服务端直接控制逐个 IO 动作（拒绝：违反 §2.3 和 ADR-cross-0004 的 IO 权限边界）
- 由 R-09 或等效生产管理权限作出整批清空决定，再由操作员发起、服务端授权恢复范围，车载端执行安全门序列（采纳）

**Consequences**:
- 初稿 §10 需要新增 LoadCompensationRequested、LoadCompensationCommand、LoadCompensationCommandAck 和 LoadCompensationResult/ACK。
- LoadCompensationRequested 属于请求—响应消息；命令与结果属于可靠消息并遵守 DurableAcceptance。
- 补偿流程必须沿用原 SlotOperationAttemptId，不能创建新的 LoadBatch；补偿完成后原物理尝试终结为 `COMPENSATED`，原 DemandId 终结为 `CANCELLED_BY_LOAD_COMPENSATION`，不再自动改派或创建补偿后重试尝试。
- 车载端必须在本地界面明确区分“待补偿”“等待服务端授权”“正在清空”和“补偿完成”。
- 补偿结束的“空仓”证据按 ADR-cross-0040 使用仓内光幕；不要求操作员额外提交空仓声明。
- “硬件故障待人工处置”必须与“已有 LoadCompensationDecision、待补偿”分开显示和持久化。
- HardwareRecoveryConfirmation、LoadCompensationDecision 和操作员开始清空是三个不同事实；同一人兼任多个角色也不得合并其权限核验。
- LoadCompensationDecision 必须关联本次提交前形成的单次 LoadCompensationDecisionAuthProof；证据与确认人、DemandId、SlotOperationAttemptId 或决定内容不匹配，已经被其它提交消费，或无法可靠记录时，保持 VehicleRecoveryRequired，不生成新决定。
- 相同 MessageId 与相同内容因 ACK 或响应丢失而重发时，服务端返回首次持久化的接受或拒绝结果，不再次消费认证、不生成第二个决定；同一证据在业务校验失败后不得用于新的提交。
- R-09 可在当前生产操作员界面完成二次认证，但审批证据不得修改 OnboardOperatorContext、Sublot 操作员绑定或 OperationSession；审计分别保留生产操作员和决策人。
- LoadCompensationDecision 首版原因码固定为 `HARDWARE_NOT_RECOVERABLE_ON_SITE`、`PRODUCTION_ABORTS_CURRENT_LOAD`、`OTHER`；前两项备注可选，`OTHER` 备注必填。原因码缺失、未知或不满足备注规则时不生成决定。
- 三种原因码共享“安全清空后取消原 DemandId”的后果，并在调度侧永久抑制对应 TransportDemandKey；本系统不等待或要求 MES 生成新需求。MES 候选在人工扫码过站前继续出现时，MesIngest 仍照常投影，调度保留抑制事实且不得重新派车。同一 SUBLOT 以后命中其它任务类型时属于不同业务键，可按新的工序需求处理。
- CurrentStopWorklist、调度和取消抑制必须把 `CANCELLED_BY_LOAD_COMPENSATION` 视为已取消终态，但审计和统计不得与 `CANCELLED_BY_OPERATOR` 合并为同一原因。
