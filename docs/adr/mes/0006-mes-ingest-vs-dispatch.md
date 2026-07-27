# MES 任务接入与调度拆开；第一期只交付接入投影

本地运输任务状态机若把 MES 快照对账与派车/装载/运送绑在同一模块，会阻塞「先做 MES 获取与盯盘」。决定将 **MesIngest（MES 任务接入）** 与调度系统拆开：第一期只实现接入——轮询 `MES_TASK_UNION`、幂等对账、重启恢复快照、`VISIBLE`/`GONE`、字段冻结与漂移告警、`PAUSED_ZERO_DROP`、只读 API 与盯盘页；产出 **TransportDemand**（稳定 `demand_id`）。调度自管派车状态并以 `demand_id` 挂接；人工永久抑制归调度，不写入接入侧。`TASK_TYPE+SUBLOT` 仅作对账与「同时最多一条 VISIBLE」约束，不作外部主键。同键在 GONE 后再现（小概率工序回退）发新 `demand_id` 并告警。

**Status**: accepted

**Considered Options**:
- 继续做完整本地任务状态机再暴露接口（拒绝：与调度耦合，挡第一期）
- 接入只吐原始快照、不做跨轮对账（拒绝：丢失恢复快照与消失语义）
- 外部只用 `TASK_TYPE+SUBLOT` 挂状态（弱拒绝：小概率回退时难分实例；保留为对账键）
- 接入 + 调度拆开，第一期只做接入投影（采纳）

**Consequences**:
- `AGV系统业务与MES任务模型.md` 中厚状态机仍描述目标调度行为，但实现上须按「接入 vs 调度」分期阅读；接入范围以本 ADR 为准。
- 调度看到的「当前可派」是接入的 VISIBLE 列表；抑制某键不会让 MES 投影消失。
