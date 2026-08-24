# 决定操作员上下文的清除时点

Type: grilling
Status: resolved
Blocked by: 15, 20

## Question

在当前站点作业模型中，操作员上下文应只在用户主动离站时清除，还是在手动或超时触发 `StopClosureCommit` 后即清除；断线、恢复、自动超时和下一 Sublot/站点分别应继承还是重新核验哪一类身份上下文？

## Answer

最终批准人于 2026-08-03 确认：`OnboardOperatorContext` 与一次到站的 `OperationSession` 共用结束边界；人工或 `StationDepartureWaitTimeout` 触发的 `StopClosureCommit` 成功时，立即结束该 `OperationSession` 并清除车载端当前已核验工号及其核验引用，不等待车辆实际移动。`StopClosureCommit` 失败时两者均不得部分清除；提交成功后的 RIoT 发车失败也不得恢复旧会话、旧工号或重新开放本站操作。

同一 `OperationSession` 内，新装货 Sublot 默认沿用当前已核验工号；只有不存在活动或待服务端确认的 Sublot 时，才允许核验并切换当前工号。每个 Sublot 在首次开锁前冻结其生产操作员绑定，该历史绑定和业务审计不随 `OnboardOperatorContext` 的切换或清除而改写。断线、车载重启、恢复握手及 `VehicleConnectionSession` 换代均不构成清除边界，必须恢复原操作会话、当前工号和未结 Sublot 绑定。

`StopClosureCommit` 后的下一次停靠必须建立新的 `OperationSession`；若相应装卸策略要求身份核验，则须重新核验，不能继承上一停靠的 `OnboardOperatorContext`。8005 当前装货身份核验开启、卸货身份核验关闭；卸货策略关闭时不建立或虚构操作员身份，只记录策略版本和“未要求操作员”。异常处置中的维护确认人与生产管理审批人是独立审计身份，不替换生产操作员、Sublot 绑定或 `OnboardOperatorContext`。

该决定采用“本站业务是否仍开放”作为身份上下文生命周期边界，而不采用“车辆是否已经物理移动”或“用户是否主动离站”作为边界；因此解决了 ADR-cross-0018 与 ADR-cross-0055 在自动超时场景中的冲突，选择后者的 `StopClosureCommit` 语义作为本次当前需求基线候选的批准结论。
