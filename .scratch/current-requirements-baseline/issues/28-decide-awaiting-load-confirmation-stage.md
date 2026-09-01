# 决定装货待整批确认阶段是否存在

Type: grilling
Status: resolved
Blocked by: 15, 20

## Question

当前装货流程是否仍存在“待整批确认”阶段；若已由自动 `LoadBatch` 提交与离站前纠错取代，取消资格、状态名称、旧文档兼容和相关用例/验收条目应以什么边界表达？

## Answer

最终批准人于 2026-08-03 确认：当前业务模型不存在单个 Sublot 的“待整批确认”阶段。一个 Sublot 的全部目标仓位达到 `OCCUPIED + 锁闭 + 开锁输出已复位` 且安全状态有效时，服务端立即形成 `LoadBatchCommitClosure` 并自动整体提交 `LoadBatch`，不等待 `LoadFinalConfirmation`。提交后仍须允许操作员继续输入其它 Sublot，但该等待属于站点级 `StationDepartureWaiting`；输入另一个有效 Sublot 后退出该等待，为它建立新的 `LoadBatch`，且不再确认前一个 Sublot。

状态词汇不为旧阶段建立一对一替代名：尚未完成全部目标仓位时使用 `ProvisionalLoadState`，其中无进展等待使用 `PartialLoadInactivity`；全部仓位安全闭环时形成 `LoadBatchCommitClosure`；随后等待其它 Sublot 时使用 `StationDepartureWaiting`。`AWAITING_LOAD_CONFIRMATION` 与 `LoadFinalConfirmation` 不进入当前模型。

普通取消的最晚业务边界是 `StopClosureCommit` 成功，而不是车辆实际移动。所选 `DemandId` 在尚未开始、部分装货中或 `LoadBatch` 已自动提交三种阶段均可于该边界前申请取消；只要已有实物装入，就必须完成该 LoadBatch 的整批清空后才能取消。自动提交后的取消以追加补偿事实表达，不得删除或改写原提交记录。`StopClosureCommit` 成功后，即使 RIoT 尚未移动车辆或移动失败，也不得重新开放本站执行普通取消。

旧材料只保留证据与追溯兼容：ADR 0045 保留为被 ADR 0054 替代的历史材料；ADR 0046 中“待整批确认”属于残留旧措辞，不作为当前需求。当前基线不提供旧状态或命令的别名；若数据库、接口或代码仍持有旧枚举，其迁移属于后续实现工作，不在本票内预判。

相关当前用例、功能需求与验收候选必须表达并验证：物理安全闭环后无需人工确认即自动提交；提交后进入 `StationDepartureWaiting` 并可接受另一个 Sublot；未开始、部分装货和已提交三阶段在 `StopClosureCommit` 前的取消及有实物时的整批清空；已提交批次取消时保留原提交历史；`StopClosureCommit` 后即使车辆未移动也拒绝普通取消。活跃条目不得继续使用 `AWAITING_LOAD_CONFIRMATION` 或 `LoadFinalConfirmation`。
