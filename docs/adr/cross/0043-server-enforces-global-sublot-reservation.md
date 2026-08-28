# 服务端保证 SUBLOT 的全局唯一占用

同事初稿 §5.1 描述单车提交 SUBLOT 后由服务端解析并下发仓位列表，但没有覆盖多台 AGV 同时提交同一 SUBLOT 的竞争。ControlServer 是跨车辆业务事实权威，必须通过持久化 SublotReservation 保证同一 SUBLOT 同时最多关联一个未终结的装卸操作。

`SublotSubmitted` 通过全部业务校验后，服务端在同一事务内创建 SlotOperationAttemptId、绑定 SUBLOT、AGV、OperationSession 和目标仓位预留，并写入待发送指令或等效 outbox。数据库约束必须阻止第二个未终结绑定，不能只依赖“先查询不存在、再插入”的应用层检查。竞争失败返回稳定原因码 `SUBLOT_ALREADY_RESERVED`。

若在 OperationCommitPoint 前发现能力变化或其它前置条件失败，服务端可以在记录原因后结束未发送的尝试并释放预留。SlotOperationCommand 一经发送，SublotReservation 必须保持到下列业务终点：

- 装货整批成功：转为该 SUBLOT 在指定 AGV 和仓位上的正式业务占用。
- 装货硬件故障：等待人工处置期间保持；若修复后继续原操作，则保持到该操作终结；若取得 LoadCompensationDecision，则保持到 LoadCompensationRecovery 完成。
- 操作员取消装货任务：保持到 ADR-cross-0046 的全部目标仓位清空后才释放。
- 卸货开始：当前站点目标仓位由正式在车占用转入当前 UnloadBatch；一个 UnloadBatch 可以包含多个 Sublot。
- 8005 卸货逐仓完成：某仓位达到 `EMPTY + 锁闭 + 开锁输出已复位` 后独立清除该仓位业务占用；当前 Sublot 仍有未完成目标仓位时，全局预留不得提前释放。
- 当前 Sublot 的全部在车仓位均已按服务端业务规则完成交付且不存在未结操作时，才结束该 Sublot 的本次在车业务占用。

车载断线、服务端重启、ACK 超时或操作暂停都不是释放条件。重复的同一 MessageId 或同一未结 SlotOperationAttemptId 按幂等规则返回既有绑定；来自其它车辆或操作会话的竞争提交必须拒绝。

**Status**: accepted

**Considered Options**:
- 各车载端自行防止重复 SUBLOT（拒绝：车载端之间没有全局视图）
- 服务端查询是否存在后再创建，不加持久化唯一约束（拒绝：并发请求仍可能同时通过）
- 服务端以事务和数据库约束建立全局唯一 SublotReservation（采纳）

**Consequences**:
- 服务端需要可持久化的 SUBLOT 活动状态或等效唯一索引，覆盖待发送、执行中、待取消清空、待补偿和卸货中状态。
- `SUBLOT_ALREADY_RESERVED` 应返回当前绑定车辆和状态的可展示信息，但不向车载端暴露不必要的 MES 数据。
- 人工不能通过删除在线状态解除占用；异常释放必须走可审计恢复流程。
- SublotReservation 与 VehicleConnectionSession 生命周期分离，车辆离线不会丢失业务所有权。
- 后续接口确认稿应在 §5.1 和 §14 增加同 SUBLOT 并发提交场景。
