# 装货正式提交前允许原操作内纠错

同事初稿 §5.1 只输入 SUBLOT，§7 逐仓执行；花篮又没有单独身份，系统无法自动识别操作员放错了哪一篮。为允许用户在车辆离站前纠正放错产品，LoadBatch 正式提交前的任意装货阶段都允许在原操作内纠错。全部目标仓位物理装货完成后不立即正式提交，而是进入 `AWAITING_LOAD_CONFIRMATION`，等待 LoadFinalConfirmation。

操作员在当前仓门尚未锁闭时发现放错，可以在同一次当前仓位操作内取出错误花篮、放入正确花篮，再完成当前仓位；这不是 LoadCorrection。若放错仓位已经锁闭，车载端暂停打开后续装货仓位并请求 LoadCorrection，不要求先装完 SUBLOT 的剩余花篮。

车载界面持续显示 SUBLOT、ExpectedBasketCount 和全部目标仓位，已核验操作员可以选择：

- `整批确认无误`：提交 LoadFinalConfirmation。
- `有花篮放错，需要重新放置`：选择一个或多个已装物理仓位并请求 LoadCorrection。
- `取消本任务`：按 ADR-cross-0046 进入 LoadTaskCancellation，并清空该任务全部目标仓位。

LoadCorrection 必须由服务端在原 SlotOperationAttemptId 下通过可靠 `LoadCorrectionCommand` 授权，使用新的 MessageId。车载端一次只操作一个选定仓位，正确花篮必须放回原仓位；车载端必须观察到有效仓内光幕从 OCCUPIED 变为 EMPTY、再变为 OCCUPIED，最后由锁传感器确认仓门锁闭且开锁输出回读确认为复位，并可靠上报 `LoadCorrectionResult`。若 SUBLOT 尚未完成全部目标仓位，完成后恢复剩余装货；若已完成全部目标仓位，则重新进入 AWAITING_LOAD_CONFIRMATION。

错误花篮已经取出但正确花篮暂时无法取得时，操作进入 `LoadCorrectionPending`：允许先安全锁闭空仓位，但不把 EMPTY 当作纠错成功，不打开后续装货仓位，也不自动取消或自动进入整批补偿。原任务、SUBLOT、目标仓位、预留和 StationOperationGuard 全部保持；操作员之后只能继续在原仓位重放，或明确选择 ADR-cross-0046 的“清空并取消”。断线、重启或换班不得跳过这个待重放仓位。

只有 LoadFinalConfirmation、全部目标仓位 OCCUPIED、全部仓门由锁传感器确认锁闭、全部开锁输出回读确认为复位且安全状态有效同时满足时，服务端才整体提交 LoadBatch 并允许解除 StationOperationGuard。纠错过程中发生无法安全收尾或无法唯一解释恢复的机构故障时，保持原目标集合、预留和逐仓事实，停止新增开门并进入 VehicleRecoveryRequired；不得自动进入 LoadCompensationRequired。只有取得 R-09 或等效生产管理权限作出的 LoadCompensationDecision 后，才进入补偿流程。正确花篮暂时不可得本身不属于硬件故障。

普通 LoadCorrection 只允许在正式提交前且车辆尚未离站时使用。LoadBatch 已提交后发现放错，不允许以 LoadCorrection 直接重开仓修改终态；车辆尚未离站但操作员决定不再存放时按 ADR-cross-0046 清空并取消，车辆已经离站时必须走异常卸出并重新装货的独立业务流程。

**Status**: superseded by ADR-cross-0054

**Considered Options**:
- 每仓完成后立即提交，发现放错时直接重开仓（拒绝：会修改已提交终态并绕过业务授权）
- 放错一篮就整批清空补偿（拒绝：在提交前可安全定位仓位并更换，代价过大）
- 增加整批确认门槛，并在正式提交前的任意装货阶段允许服务端授权的原操作内纠错（采纳）

**Consequences**:
- 初稿 §5 和 §10 需要新增 AWAITING_LOAD_CONFIRMATION、LoadCorrectionRequested、LoadCorrectionCommand、LoadCorrectionResult 和 LoadFinalConfirmation。
- LoadCorrection 不创建新 SlotOperationAttemptId，不改变原任务、SUBLOT、目标仓位或预留，并且只在原仓位完成取出重放。
- 已锁闭仓位纠错期间暂停打开后续装货仓位；完成后恢复剩余装货或回到 AWAITING_LOAD_CONFIRMATION。
- `LoadCorrectionPending` 保持全部业务绑定与移动保护；它只有“原仓位继续重放”或“清空并取消”两个业务出口。
- 操作员确认是 SUBLOT 归属的业务证据；光幕仍只是 OCCUPIED/EMPTY 的物理证据。
- 服务端必须保持 SublotReservation 和 StationOperationGuard，直到最终提交或整批补偿完成。
- LoadBatch 正式提交但车辆尚未离站时仍可按 ADR-cross-0046 取消，但必须清空所选 DemandId 的全部目标仓位；同车其它 SUBLOT 不受影响。
- 车载断线时不得开始新的纠错开仓；重连后按 RecoveryHandshake 和服务端明确授权恢复。
