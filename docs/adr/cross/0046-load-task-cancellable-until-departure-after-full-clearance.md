# 装货任务离站前可取消，但必须整批清空

> *2026-09-18：本文讲批量开锁（BatchUnlock）的部分由 [ADR-cross-0061](0061-one-slot-door-unlocked-at-a-time.md) 取代——业务仓位操作一次只开一扇仓门，按分组再按仓位号依次打开；已随 `CP-0004` 批准生效（2026-09-18，需求基线 `v1.4.0`），具体取代哪几句见该文 Consequences。其余正文不变。*

> *2026-09-29：光幕明确 `EMPTY`、而锁闭或开锁输出复位不能证明的那一格，由 [ADR-cross-0063](0063-light-curtain-empty-settles-load-side-business-door-proof-gates-release.md) 取代本文`LoadCancelPending` 完成条件中锁闭与输出复位的部分——货物业务照常结清，锁闭证明改为车辆放行条件；已随 `CP-0009` 批准生效（2026-09-29，需求基线 `v1.8.0`），具体见该文 Consequences。其余正文不变。*

同事初稿 §2.1 原称车载端不理解任务，§2.2 将站点任务和业务时机归服务端，§23 提议通用 OperationCancelCommand。准确边界应是“车载端不拥有任务事实，但必须知道并展示本次停靠需要处理的业务”。现场需要车载界面在 CurrentStopWorklist 中展示当前停靠的待装与待卸任务，并允许操作员取消可取消的装货任务，以避免该任务再次触发车辆回到当前站点。

车载端按 ADR-cross-0048 接收并显示服务端 CurrentStopWorklistSnapshot。任务项按 ADR-cross-0047 使用现有 DemandId 标识，至少包含 DemandId、SUBLOT、作业类型、ExpectedBasketCount、完成/剩余数量、状态、关联仓位摘要和服务端裁定的可用操作。已核验操作员可以提交取消请求，服务端负责验证、持久化、更新调度并返回新快照；车载端不能只在本地隐藏任务。

装货任务在车辆尚未离开当前站点时允许取消，物理阶段决定取消方式：

- SlotOperationCommand 尚未发送且没有物理装载：车载端获得取消授权后确认没有关联目标仓位，直接报告 ALL_EMPTY。
- 正在装货、只装了一部分，或者已经整批自动提交但 StopClosureCommit 尚未发生：服务端授权开始取消并进入 LoadCancelPending；车载端停止打开后续装货仓位。授权到达时当前装货仓门已经打开的，操作员可以直接取出或不再放入花篮，使该仓位以 `EMPTY + 锁闭 + 开锁输出已复位` 收尾并计为已清空仓位，不要求先完成 OCCUPIED 装货再重新开门；其它实时确认为 OCCUPIED 的目标仓位依据原 SlotOperationAttemptId 的执行日志和实时光幕形成批量开锁集合，一次性打开并引导操作员全部取出。（2026-10-21 注，`CP-0021`，待批准：装了一部分时另可申请「剩下的不装」，那不是取消，不清空已装仓位，见 `REQ-0368` 与文末修订记录。）
- 车辆已离站：普通任务取消不可用，后续只能建立异常卸出业务流程。

LoadCancelPending 的完成条件不是“停止继续装货”，而是所选 DemandId 的全部目标仓位均由仓内光幕确认 EMPTY、由锁传感器确认仓门锁闭、开锁输出回读确认为复位且安全状态有效。“全有或全无”以单个 SUBLOT/LoadBatch 为边界，不是整车边界：同车其它 SUBLOT 的仓位不属于本次取消授权范围，不打开、不清空，其任务、确认记录和业务占用保持不变。

虽然花篮没有身份 ID，但服务端已经保存逐仓 SlotBusinessState 与 SUBLOT 的映射，且每个 LoadBatch 的正确归属由已核验操作员确认。因此系统可以确定本次取消应清空的物理仓位范围；光幕负责证明这些仓位已经 EMPTY，不负责重新识别其它仓位中的产品身份。

同车允许已经装好的多个 SUBLOT 并存，但物理仓位操作不跨 SUBLOT 并发或穿插。若另一 SUBLOT 仍在装货、纠错、补偿或取消，服务端不得授权本次取消；必须等待当前 SUBLOT 整批装完并确认，或完成它自己的清空取消，到达没有活动仓位操作的稳定边界后，再开始清空所选 DemandId。已经装好并处于稳定状态的其它 SUBLOT 不阻塞本次取消。

取消清空的批量开锁遵守 ADR-cross-0035 的 BatchUnlock：已经 EMPTY 的目标仓位不加入开锁集合，OCCUPIED 仓位全部加入；同一 IO 模块使用一次多线圈写，跨模块按模块分组并行发送，不承诺跨设备电气原子性。开锁是批量的，但完成证据仍按仓位独立形成，任一目标仓位未证明 EMPTY 或机构未安全复位时都不能完成取消。

车载端可靠上报 LoadCancellationResult 后，服务端才将任务终结为 `CANCELLED_BY_OPERATOR`，释放 SublotReservation 和仓位占用，并持久化取消抑制记录，使该任务不再进入后续派车。清空未完成或发生故障时保持 LoadCancelPending 和 StationOperationGuard，车辆不得离站。

服务端接受 ALL_EMPTY、完成取消并下发更高 revision 的 CurrentStopWorklistSnapshot 后，本次释放的仓位重新成为可分配仓位。车辆尚未离站时可以继续扫描新的 SUBLOT 并复用这些仓位，但新 SUBLOT 仍须独立通过任务范围、StationTaskTypeAdmission、容量与 SublotReservation 校验；同车保留的其它 SUBLOT 不受影响。服务端依据取消后的剩余任务和新增任务重新计算 UpcomingStopPlan。

LoadBatch 已经正式提交时，LoadTaskCancellation 是追加的补偿事实，不删除、不覆盖原 LoadBatch 自动提交记录。最终有效状态可以变为 `CANCELLED_BY_OPERATOR`，但业务审计必须保留原装货操作员、原提交事实、取消发起人及时间、逐仓清空结果和服务端取消完成时间。提交事实不可改写不妨碍 StopClosureCommit 前执行本补偿流程。

原 SlotOperationCommand 没有被撤回或改写；LoadTaskCancellation 是同一 SlotOperationAttemptId 下追加的补偿性物理阶段。它与硬件故障后由人工决定并经服务端授权的 LoadCompensationRecovery 使用相同的车载清空执行能力，且都会终结原 DemandId；普通取消终结为 `CANCELLED_BY_OPERATOR`，装货补偿终结为 `CANCELLED_BY_LOAD_COMPENSATION`，两者的准入权限、物理恢复状态和审计原因不同，普通取消不能绕过 LoadCompensationDecision。

当前开锁仓位从装货切换为取消清空必须以服务端 LoadCancellationAuthorization 为前提。等待授权期间、请求被拒绝时或连接失联时，车载端不得自行改变原装货语义；断联仍按 ADR-cross-0003 完成当前开锁集合的普通装货安全收尾，重连对账并重新获得授权后才能进入取消清空。

车载端发起取消和显示裁决的具体消息交互遵守 ADR-cross-0052；点击取消不能直接修改本地 CurrentStopWorklist。

**Status**: accepted（部分由 [ADR-cross-0065](0065-staging-pickup-departs-on-full-or-operator-departure.md) 修订：STAGING_TO_WIRE 固定起点的取货停靠不提供未装任务的取消，清空取消完成后放回待派，2026-10-14 随 `CP-0012` 批准；未装任务的取消在该停靠恢复、终结并抑制，2026-10-15 随 `CP-0014` 批准；均见文末修订记录）

**Considered Options**:
- 仓位指令发出后完全禁止用户取消（拒绝：无法满足现场放弃任务并避免车辆再次回站的需求）
- 用户点击后立即把任务标为取消，不要求清空（拒绝：业务状态会与车内实际产品冲突）
- 离站前始终可申请取消，已装载时整批清空后才完成取消（采纳）

**Consequences**:
- 初稿 §2.1 应改为“车载端不拥有任务事实，但可显示 CurrentStopWorklist、UpcomingStopPlan 与 OnboardVehicleOverview，并提交授权范围内的操作请求”。
- 初稿 §10 和 §23 应以 CurrentStopWorklistSnapshot、LoadCancellationStartRequested、LoadCancellationAuthorization 和 LoadCancellationResult 替换通用 OperationCancelCommand。
- 服务端只返回 AUTHORIZED 或 REJECTED，不判断 DIRECT_CANCEL/CLEAR_REQUIRED，也不下发逐仓 LoadCancellationCommand。
- canCancel 在待处理、所选 SUBLOT 装货中、待整批确认和已装完未离站阶段为 true；若同车另一 SUBLOT 正在执行物理仓位操作则暂时为 false，进入取消处理中或车辆离站后也为 false。
- 取消记录必须包含 DemandId、SUBLOT、AGV、站点、OperationSession、操作员和时间，以及逐仓清空证据；当前项目不要求操作员选择或填写取消原因。
- 正式提交后的取消必须以追加记录表达，不得删除或改写 LoadBatch 提交历史。
- 一台车装有多个 SUBLOT 时，取消只清空所选 DemandId 的完整目标仓位；其它 SUBLOT 可以继续保留在车上。
- 同车不同 SUBLOT 的装货、纠错、补偿和取消物理动作必须串行，不能让两个 SlotOperationAttemptId 同时拥有当前开锁集合。
- 取消释放的仓位只在服务端完成取消并发布新版 CurrentStopWorklistSnapshot 后才可复用；车载端不能仅凭本地光幕 EMPTY 提前开始新 SUBLOT。
- 取消必须形成服务端持久化抑制依据，不能因重启、断线或 MES 再次轮询而重新创建相同站点任务。

## 修订记录

- **2026-10-14，待送点取货停靠不提供未装任务的取消，清空取消改为放回待派（`CP-0012`，[ADR-cross-0065](0065-staging-pickup-departs-on-full-or-operator-departure.md)）。**用户原话（经调度 C11 转达）：
  「在staging的地方取消装货没有意义啊，我肯定要装货的」。
  - 范围：**仅 STAGING_TO_WIRE 固定起点（`REQ-0324`）的取货停靠**。机台取货停靠照本文，一字不改。
  - 本文首项「SlotOperationCommand 尚未发送且没有物理装载」的取消在该停靠不提供：车载端不显示，服务端拒绝（`ACTION_NOT_ALLOWED_IN_STATE`）。
  - 第二项（正在装货、只装了一部分、已整批自动提交）的清空照本文进行，清空范围、`LoadCancelPending` 的完成条件与串行要求都不变；
    但完成后**不**终结为 `CANCELLED_BY_OPERATOR`、**不**写取消抑制，该需求从本旅程释放、放回待派，仍为已受理（`REQ-0211` 修订文）。
    理由：v2 对 MesIngest 只读，抑制等于这批料 v2 再也不派；在待送点，取消的意思只能是「这一篮这趟不带」。
- **2026-10-15，待送点取货停靠恢复扫码前取消，按条取消、终结并抑制（`CP-0014`，program#191）。**
  - 上一条修订记录里「首项……的取消在该停靠不提供」作废：待送点上「SlotOperationCommand 尚未发送且没有物理装载」的取消照本文，
    以 `CANCELLED_BY_OPERATOR` 终结并写取消抑制，与机台取货相同（用户 10-15 选「彻底取消」）。车载端列出全部未装的需求，每条各有取消入口，
    不要求先选择再取消（`REQ-0211` 修订文）。
  - 第二项（已开始装货的清空）在待送点仍放回待派，不变。

- **2026-10-21，多篮装货可申请「剩下的不装」，经服务端授权后按已装篮数完成（`CP-0021`，program#213，`REQ-0368`，待批准）。**
  用户 10-21 定（经 Coordinator13 转达）：剩下的篮子「这条任务就算完成」，车按实际装上的篮数送完，系统不再管，不发人工搬运告警。
  减篮不是本文的取消：不进 `LoadCancelPending`、不清空已装仓位、不以 `CANCELLED_BY_OPERATOR` 终结、不写抑制，按已装的 k 篮完成（`REQ-0211` 修订文）。
  本文的取消范围、整批清空与串行要求不变；减篮同样要求同车没有别的物理仓位操作在进行。
