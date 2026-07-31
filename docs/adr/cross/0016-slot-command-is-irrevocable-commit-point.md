# 仓位操作指令一经发出即不可撤回

服务端首次发出 `SlotOperationCommand` 即到达 OperationCommitPoint；无论车载端是否已经开始开锁，服务端都不得撤回或替换该操作。Sublot 解析、任务与站点有效性、ADR-cross-0050 定义的 AdmissionDecisionSnapshot、ExpectedBasketCount、装卸类型、目标仓位清单、执行方式和业务预留必须在发送前完成检查并冻结。发送结果未知时沿用原仓位操作尝试编号对账或重发相同内容；车载端因硬件或安全条件明确拒绝属于执行失败，不把原指令改写成另一项操作。

**Status**: accepted

**Considered Options**:
- 第一个开锁动作前允许服务端撤回装货操作（拒绝：发送后接收与执行状态可能未知，撤回会引入竞态）
- 车载端接受 ACK 后才不可撤回（拒绝：ACK 丢失时服务端无法可靠判断是否已经承诺）
- 指令首次发出即不可撤回，所有业务检查前置（采纳）

**Consequences**:
- 服务端必须以持久化 outbox 或等效一致性边界先冻结指令内容和业务预留，再发送消息。
- 发现 SUBLOT、花篮数量、仓位或业务条件错误不能靠撤回指令补救；必须防止错误越过 OperationCommitPoint。
- 某目标仓位发生硬件故障后不得用其它空闲仓位替换；原目标集合和逐仓事实保持不变，停止新增开门并等待人工处置。
- 原指令不能被撤回，但未处于关键硬件故障恢复的装货任务可按 ADR-cross-0046 在原仓位操作尝试编号下进入 LoadTaskCancellation；硬件故障先等待人工处置，只有取得 R-09 或等效生产管理权限作出的 LoadCompensationDecision 后才按 LoadCompensationRecovery 执行；卸货继续遵守 UnloadCompletionRequired。
