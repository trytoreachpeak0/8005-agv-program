# 装货物理闭环后自动提交，整站结束前仍可纠错

为避免操作员已经放满一个 Sublot 却未点击确认而使车辆无限等待，LoadBatch 在全部目标仓位达到 `OCCUPIED + 锁闭 + 开锁输出已复位` 且安全状态有效时自动整体提交，不再使用 LoadFinalConfirmation。为了保留现场发现放错后的纠正能力，在 StopClosureCommit 前，已核验操作员仍可选择该 Sublot 的一个或多个原仓位请求 LoadCorrection；服务端授权后按原仓位执行 `OCCUPIED→EMPTY→OCCUPIED`，追加纠错审计但不撤销或改写原 LoadBatch 提交事实。纠错退出 StationDepartureWaiting 并停止离站倒计时，全部相关仓位重新安全闭环后从完整等待时长重新计时；整站已结束或车辆开始移动后不再允许普通纠错，只能进入任务取消或异常卸出流程。

**Status**: accepted

**Considered Options**:
- 等待操作员逐 Sublot 最终确认后才提交（拒绝：无人继续操作时车辆会无限停留）
- 物理闭环后自动提交，提交后只能整批清空取消（拒绝：车辆仍在本站时无法低成本纠正单仓放错）
- 物理闭环后自动提交，并在整站结束前保留服务端授权、追加审计的原仓位纠错（采纳）

**Consequences**:
- 删除 AWAITING_LOAD_CONFIRMATION 与 LoadFinalConfirmation；“本站装货完成”只结束当前停靠，不参与 LoadBatch 提交。
- LoadCorrection 可以发生在自动提交之后，但不得删除、撤销或改写原提交事实。
- StopClosureCommit 成为普通装货纠错的最晚业务边界。
