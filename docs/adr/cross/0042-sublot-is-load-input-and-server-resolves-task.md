# 装货输入是 SUBLOT，服务端解析任务和花篮数

同事初稿 §5.1 使用“站点总任务码”描述装货扫码内容。项目实际不存在独立于子批次的“总任务码”：操作员在车载界面扫描或输入的就是 Sublot，不存在另一个 SublotId。正式领域用语统一为 Sublot（子批次），不再使用 SublotInput、TaskCode 或“总任务码”。

车载上位机采集 Sublot 字符串并通过 `SublotSubmitted` 原样提交，不解析任务、不查询花篮数，也不允许操作员手工填写数量。服务端根据 Sublot 查询任务/MES，必须解析出唯一有效任务及 ExpectedBasketCount，校验 Sublot 是否正确、当前站点是否允许该任务以及仓位容量，并按 ADR-cross-0041 验证：

`ExpectedBasketCount == SlotOperationCommand.slots.Count`

Sublot 不存在、对应任务不唯一、任务状态不允许装货、当前站点不满足 ADR-cross-0049 的 StationTaskTypeAdmission、料盒数查询失败或结果不是正整数、冻结 PACKAGE 缺失或无法唯一匹配批准容量、花篮数量无法换算或为零、已有 ADR-cross-0043 规定的 SublotReservation、或者可用仓位不足以容纳整批时，服务端拒绝本次输入，不分配仓位、不下发 SlotOperationCommand。掉线期间不得校验或开始新的 Sublot。

初稿消息名同步调整：

- `ScanRequestCommand` 改为 `SublotEntryRequested`。
- `TaskCodeSubmitted` 改为 `SublotSubmitted`。
- `TaskCodeRejected` 改为 `SublotRejected`。

成功时不需要额外 `SublotAccepted`；服务端完成全部校验和预留后直接进入 SlotOperationCommand 流程。卸货继续遵守初稿 §6，不要求输入 SUBLOT，由服务端根据到站任务确定完整卸货仓位。

**Status**: accepted

**Considered Options**:
- 保留“总任务码”作为 SUBLOT 的界面别名（拒绝：会让开发人员误以为存在两个不同业务编号）
- 车载端解析 SUBLOT 并允许操作员补填花篮数（拒绝：车载端不拥有任务与 MES 业务事实）
- 车载端只提交 SUBLOT，服务端解析唯一任务和权威花篮数（采纳）

**Consequences**:
- 车载界面、日志、协议和测试统一显示“子批号/SUBLOT”，不再显示“总任务码”或 TaskCode。
- ExpectedBasketCount 在 OperationCommitPoint 前由服务端冻结，不能从已分配仓位数反推或由用户修改。
- 服务端业务审计记录提交的 Sublot、解析出的任务、ExpectedBasketCount、Sublot 仓位分配和操作员会话，不记录不存在的单篮身份。
- 车载执行日志为防止误关程序导致上下文丢失，可以持久化当前 Sublot 字符串作为恢复引用；它不因此拥有服务端任务事实。
- 当前 Sublot 只有全部目标仓位完成、结果上传并得到服务端确认后才结束；此前不得输入下一个 Sublot 或更换工号。
- 后续接口确认稿应整体替换 §5.1、§10 和相关示例中的总任务码/TaskCode 术语。
