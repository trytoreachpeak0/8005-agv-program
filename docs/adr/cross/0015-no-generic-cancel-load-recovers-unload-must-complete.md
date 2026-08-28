# 不提供瞬时通用取消；装货清空后可取消，卸货必须完成

上下层协议不提供能够瞬间撤回 SlotOperationCommand 的通用 `OperationCancelCommand`。装货硬件故障时保持原目标集合、预留与逐仓事实，停止新增开门并等待人工处置，不自动进入 LoadCompensationRequired。只有取得 R-09 或等效生产管理权限作出的 LoadCompensationDecision 后，才按 ADR-cross-0039 进入 LoadCompensationRecovery；操作员主动取消未处于关键硬件故障恢复的装货任务时按 ADR-cross-0046 执行 LoadTaskCancellation。凡进入清空流程，都必须使相关目标仓位恢复 EMPTY、由锁传感器确认仓门锁闭且开锁输出回读确认为复位后，服务端才能释放整批预留。原操作、物理清空和最终业务终态均保留审计记录。

卸货操作采用 UnloadCompletionRequired，不存在取消分支；发生异常时只能暂停、排障并继续，直到所有目标仓位取空、锁闭并可靠上报。

**Status**: accepted

**Considered Options**:
- 用通用取消命令停止剩余仓位并把批次标为取消（拒绝：已发生的物理装卸不会随消息回滚）
- 装货与卸货均允许人工恢复到操作前状态后取消（拒绝：卸货业务要求目标产品必须全部取出）
- 装货在整批物理清空后允许取消或补偿终结，卸货必须完成（采纳）

**Consequences**:
- 初稿 §23 的通用 `OperationCancelCommand` 不进入正式协议，改为装货专用 LoadCancellationStartRequested/Authorization/Result。
- 装货硬件故障待人工处置、取消清空、人工决定后的失败补偿或卸货全部完成前，StationOperationGuard 保持有效，车辆不得离站。
- 装货指令的原始内容仍遵守 ADR-cross-0016 不可撤回；取消是同一仓位操作尝试编号下新增的物理清空阶段。
