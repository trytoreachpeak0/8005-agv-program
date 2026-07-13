---
id: UC-007
type: use-case
title: "Sync Transport Task from MES 从 MES 同步生成搬运任务"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-09
updated: 2026-07-09
primary_actor: "Local Server 本地服务器（系统内部过程，非人工角色）"
secondary_actor: MES
frequency: "System polls MES on a fixed cycle; the specific interval is TBD. Given the number of moveTypes and stations, this is expected to run far more frequently than any single manual UC (e.g. UC-001). 系统按固定周期轮询 MES，具体周期待定；由于需要覆盖多种 moveType、多个站点，预期执行频率远高于任何单一人工操作类 UC（如 UC-001）"
related_uc: ["UC-001", "UC-003", "UC-008"]
related_br: ["BR-001"]
aliases: ["UC-007"]
---

# UC-007 Sync Transport Task from MES 从 MES 同步生成搬运任务

## Description 描述

本地服务器按固定周期轮询 MES：针对每一种搬运类型（moveType），系统使用该 moveType 对应的、预先配置好的 MES 查询 SQL 分别拉取数据，查询结果可再按 `area`（区域）、`eqp`（机台）进行过滤（并非所有 area/eqp 的数据都需要生成任务）。系统对每条返回数据核验其是否满足生成任务的条件，并按去重规则核验是否已存在对应的本地任务记录，避免同一子批号/任务因多次轮询被重复读取而重复创建。校验通过且未被去重命中的数据，会被转换为本地任务记录（状态为"新建 New"），并带上对应的 moveType 标记，供后续派车、装载等下游用例（如 [[uc-001-load-completed-lot-into-slot|UC-001]]）使用。

> 本 UC 只覆盖"本地服务器如何从 MES 拉取、校验、去重、转换并生成本地任务记录"这一过程本身，不包含"本次派车任务范围如何划分"（见 [[br-001-dispatch-task-range|BR-001]]）、AGV 导航移动（见 [[uc-003-agv-arrives-at-designated-station|UC-003]]）等下游过程。

## Trigger 触发条件

本地服务器达到预设的轮询周期（具体周期 TBD）。

## Precondition 前置条件

**System & Interface 系统与接口**

1. MES 接口在线可用。MES interface is online and reachable.
2. 每一种 moveType 均已配置好对应的 MES 查询 SQL（可附带 area/eqp 过滤条件），该配置已生效。Each moveType has a corresponding, currently active MES query SQL configuration (optionally with area/eqp filters).

> 该 moveType-SQL-area/eqp 映射配置的具体维护方式（配置界面、生效范围、版本管理等）不在本 UC 中展开，属于基础数据配置范畴，具体形式 TBD（见 Notes）。

## Postcondition 后置条件

**Task & Data 任务与数据**

1. 通过校验且未被去重命中的 MES 数据，在本地数据库中生成新的搬运任务记录，状态为"新建（New）"，并带有对应的 moveType 标记。New transport task record(s) are created in the local database with status "New" and the corresponding moveType tag.
2. 已存在对应本地任务记录的数据不会被重复创建。Data that already has a corresponding local task record is not duplicated.
3. 本次同步过程（涉及的 moveType、拉取到的数据量、新建任务数、跳过/异常数量、时间戳）被记录到本地数据库，用于追溯。This sync run (moveTypes involved, records fetched, tasks newly created, records skipped/exceptioned, timestamp) is logged for traceability.

## Assumption 假设

1. MES 返回的原始数据本身是准确的，本 UC 不核验其真实性（如某条数据是否真实反映产线实际情况），只核验其是否满足生成本地任务的条件。The raw data returned by MES is assumed to be accurate; this UC does not verify its real-world truthfulness, only whether it satisfies the conditions for generating a local task.
2. 子批号当前工序、任务类型是否满足对应 moveType 的要求的具体判定规则暂未确定，TBD 待补充（对应术语表第 8 节 `NG_STEP_ERROR`/`NG_TASK_ERROR`/`NG_LOT_CLOSED` 等核验错误码，具体触发条件待后续与 MES/IT 侧确认）。The specific rules for determining whether a sublot's current step/task type satisfies a given moveType's requirements are not yet finalized (TBD).

## Normal Flow 正常流程

### 7.0 Sync Transport Task from MES

1. 系统达到预设轮询周期，开始本轮同步
2. 系统逐个 moveType 执行其对应的 MES 查询 SQL，查询结果按该 moveType 配置的 area/eqp 过滤条件（若有）筛选
   2.1 系统核验本次 MES 查询/通信是否正常（见 Exception Flow E2.1）
3. 系统对每条返回数据核验是否满足生成本地任务的条件（如工序、任务类型是否满足对应 moveType 要求，具体规则 TBD）
   3.1 若某条数据校验不通过，判定核验不通过（见 Exception Flow E3.1）
4. 系统对校验通过的数据按去重规则（如 `productLot + machineNo + finishTime` 或 MES 事务 ID）核验是否已存在对应的本地任务记录
   4.1 若命中已存在的本地任务记录，判定为重复数据（见 Exception Flow E4.1）
5. 系统将校验通过且未被去重命中的数据转换为本地任务记录，状态标记为"新建（New）"，并带上对应 moveType
6. 系统记录本次同步日志（涉及 moveType、拉取数量、新建数量、跳过/异常数量、时间戳）

## Alternative Flow 备选流程

不存在需要区分的备选流程：无论本轮同步涉及一种还是多种 moveType，系统均按 Normal Flow 逐个 moveType 依次查询、校验、去重、转换，不存在触发方式或步骤不同的分支路径。No alternative flow is needed: regardless of how many moveTypes are involved in a given sync cycle, the system processes each moveType through the same query/validate/deduplicate/convert steps described in the Normal Flow.

## Exception Flow 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow 中触发该异常的具体步骤（或子步骤）一一对应：

* E2.1 MES 接口通信异常/超时
* E3.1 数据校验不通过（不满足对应 moveType 要求）
* E4.1 去重命中，数据已存在对应本地任务记录

### E2.1 MES 接口通信异常/超时

1. 系统按第 2 步向 MES 发起查询
2. 系统按第 2.1 步核验，发现本次查询通信异常或超时，未能取得该 moveType 的数据
3. 系统自动重试（具体重试次数/间隔 TBD）
4. 若重试仍失败且达到预设阈值（次数/时长，具体数值 TBD），系统触发告警提示（如界面告警、上报 IT/软件维护人员 R-12），本轮该 moveType 的同步跳过，等待下一轮轮询周期重试
5. IT/软件维护人员排查并修复 MES 接口/网络异常后，后续轮询周期恢复正常同步

### E3.1 数据校验不通过

1. 系统按第 3 步对某条 MES 数据核验其工序、任务类型是否满足对应 moveType 要求
2. 系统核验不通过（具体判定规则 TBD，对应术语表 `NG_STEP_ERROR`/`NG_TASK_ERROR`/`NG_LOT_CLOSED` 等错误码）
3. 系统不为该条数据生成本地任务记录，记录本次校验不通过的异常日志（子批号、moveType、错误码、时间戳）
4. 该条数据在后续轮询周期中若状态发生变化（如工序更新为满足要求），可在下一轮重新被校验并生成任务；具体是否需要人工介入处理长期校验不通过的数据，TBD 待补充

### E4.1 去重命中

1. 系统按第 4 步对某条校验通过的数据核验是否已存在对应的本地任务记录
2. 系统命中已存在的本地任务记录（去重键一致）
3. 系统跳过该条数据，不重复创建本地任务记录，也不视为异常，不记录告警

## Notes 备注

* 本 UC 是从 [[uc-001-load-completed-lot-into-slot|UC-001]] 中长期隐含依赖的前提中拆分出来的：UC-001 的 Precondition 第 5 条及相关备注多次提到"任务已从 MES 同步到本地数据库""moveType 已在生成时标记好"，但该同步生成过程本身此前从未被写成独立 UC；`vision-and-scope.md` 主要特性清单中"MES 任务获取、解析、去重、转换"（第 1、9 项）也明确将其列为核心功能，因此确认拆分为本 UC。
* 经与用户确认：每一种搬运类型（moveType）对应一条独立的 MES 查询 SQL；查询结果可再按 `area`、`eqp` 过滤，并非所有 area/eqp 的数据都需要生成任务。具体每个 moveType 对应哪条 SQL、哪些 area/eqp 会被过滤，属于基础数据配置内容，本 UC 不列具体配置清单，只描述这一机制本身；该配置的维护方式（配置界面、版本管理等）TBD 待补充。
* 经与用户确认：本 UC 的去重专指"同一子批号/任务被多次轮询读取到时，避免重复创建本地任务记录"这一场景（对应 [[terminology-glossary|术语表]] 第 4 节已定义的去重规则：按 `productLot + machineNo + finishTime` 或 MES 事务 ID）；MES 侧本身是否会返回重复/冲突数据，视为超出本 UC 讨论范围的 Assumption。
* 经与用户确认：MES 接口通信异常/超时时，系统自动重试，达到预设阈值后触发告警提示；具体重试次数、超时阈值、告警对象等细节 TBD 待补充。
* 子批号工序/任务类型是否满足对应 moveType 要求的具体判定规则（对应 `NG_STEP_ERROR`/`NG_TASK_ERROR`/`NG_LOT_CLOSED` 等错误码的触发条件）尚未最终确认，本 UC 中相关步骤先标注 TBD，待后续与用户/MES-IT 侧进一步确认后补充。
* 本 UC 与 [[br-001-dispatch-task-range|BR-001]] 的分工边界：本 UC 关注"任务记录本身如何从 MES 产生、进入本地数据库"，属于任务的"生成"阶段；BR-001 关注"本次派车任务范围如何从已生成的任务集合中划分"，属于任务生成之后、派车下发时的"分配"阶段，两者是上下游关系，不重叠。

## Related Use Cases 关联用例

* [[uc-001-load-completed-lot-into-slot|UC-001]]：本 UC 生成的本地任务记录（及其 moveType 标记）是 UC-001 Precondition 第 5 条"该站点存在至少一个已从 MES 同步到本地数据库的搬运任务"的数据来源；UC-001 扫码核验环节不再重复核验 MES 工序/任务类型，正是因为已由本 UC 在生成时完成校验。
* [[uc-003-agv-arrives-at-designated-station|UC-003]]：本 UC 生成的任务是 RIOT/调度系统下发移动任务（即"一次派车"）、AGV 前往站点的前提数据基础，但本 UC 本身不涉及派车下发与导航过程。
* [[br-001-dispatch-task-range|BR-001]]：本 UC 生成的任务集合是该业务规则"本次派车任务范围"划分的基础数据来源，两者分工边界见 Notes。
* [[uc-008-dispatch-move-order-to-riot|UC-008]]：本 UC 生成的"新建（New）"状态任务是 UC-008 向 RIOT 下发移动任务时的待下发任务来源；UC-008 关注"AGV 空闲后如何确定并下发下一个移动任务给 RIOT"，属于本 UC（生成阶段）的下游过程。

## Other Information 其他信息

