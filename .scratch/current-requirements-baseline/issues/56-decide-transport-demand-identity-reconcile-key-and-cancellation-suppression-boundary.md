# 决定运输需求身份、对账键与取消抑制边界

Type: grilling
Status: resolved
Blocked by: 55

## Question

面对跨批次冲突 `CF-R01-001`：8005 当前需求应如何明确区分 TransportDemand 的稳定实例身份、MES 快照对账键、同时可见唯一性约束和本地取消后的永久抑制键；`TASK_TYPE + SUBLOT`、`product_lot + machine_no + finish_time`、MES 事务 ID 与 `DemandId` 各自是否存在、承担什么职责，GONE 后同键再现、同一 SUBLOT 命中不同任务类型、重复 MES 行及取消后持续可见时分别产生什么结果，并把批准结论绑定到当前适用 MES 契约、范围和版本？

## Answer

用户于 2026-08-04 逐项批准以下结论：

1. **当前 MES 业务对账键是 TransportDemandKey，即 `TASK_TYPE + SUBLOT`。** 它适用于当前 8005 正式 MES 六类运输任务。早期 `product_lot + machine_no + finish_time` 只保留为历史口径；当前统一查询不提供 MES 事务 ID，因此两者均不承担当前对账、唯一性或抑制职责。
2. **唯一性限定在完整快照和同时可见范围。** 同一次完整成功 MES 快照中，一个 TransportDemandKey 至多对应一行；同一时刻至多存在一个该键的 `VISIBLE` TransportDemand。若单次快照出现同键多行，即使各字段完全相同，也将该键判为数据冲突、报警并阻断，不得静默归并；其他未冲突键继续处理。
3. **同一 SUBLOT 同时命中多个任务类型是阻断性冲突。** 该 SUBLOT 在本轮的全部候选均不创建或刷新 TransportDemand，其他 SUBLOT 继续处理。不同时期依次命中不同任务类型时，各自形成不同 TransportDemandKey，可正常接入。
4. **DemandId 是本地 TransportDemand 实例身份。** MesIngest 在创建实例时生成，创建后在该实例全部生命周期内永久稳定且不复用，用于状态挂接、精确引用与历史审计；它不是 MES 事务 ID，不参与 MES 行去重，也不作为取消抑制键。
5. **`GONE` 后同键再现产生新实例。** 原 TransportDemand 与原 DemandId 永久保留为 `GONE` 历史；MesIngest 为再现候选创建新的 TransportDemand 和 DemandId，并产生“GONE 后再现”告警。新旧实例共享 TransportDemandKey，但不同时为 `VISIBLE`。MesIngest 不因调度抑制而隐藏或拒绝事实投影。
6. **本地取消终态挂 DemandId，禁止再次执行业务挂 TransportDemandKey。** 调度以 TransportDemandKey 保存 TransportDemandSuppression；命中后不得创建、恢复或派发业务任务，即使 MesIngest 因持续可见或 GONE 后再现生成了新 DemandId。同一 SUBLOT 在不同时期命中其他任务类型时属于不同键，不受原抑制影响。
7. **TransportDemandSuppression 永久且当前无解除入口。** 它不因时间、轮询、`GONE`、重启或新 DemandId 自动解除。未来若要允许合法的同键新搬运，必须先引入可靠的 MES 搬运发生编号，或另行批准具名授权并留痕审计的解除机制，不能静默放行。
8. **抑制只由本地取消产生。** `CANCELLED_BY_OPERATOR`、`CANCELLED_BY_LOAD_COMPENSATION`、`CANCELLED_BY_STOP_COMPLETE` 与 `CANCELLED_BY_STATION_TIMEOUT` 均原子写入 TransportDemandSuppression；单纯 `MES_DISAPPEARED` 或 `GONE` 不写抑制，同键以后再现时可作为新实例重新进入调度判断。
9. **版本与范围绑定。** 本结论绑定 Git 提交 `420c96c2f961aaffa42a5443fa42e6585b1c993f` 下 `mes/queries/mes-task-union/` 的当前查询包；输出字段为 `TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE`，其中 `query.sql` 的 SHA-256 为 `54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae`。它不适用于 Mock、其他项目或未来变更后的 MES 契约；若增加稳定 MES 事务 ID、改变 TASK_TYPE/SUBLOT 语义，或允许同键表达新的业务发生，必须重新审查本决定。

这些批准结论解决 `CF-R01-001`。既有 `CONTEXT.md` 和 ADR 只作为调查线索；本票及以上具名版本绑定是本次当前需求基线的批准记录。
