# 识别现有 IngestAlert 与 MES 任务形态

Type: task
Status: resolved
Blocked by: 01

## Question

当前 MesIngest 代码、只读 API/OpenAPI、数据库投影与现有样例中，系统实际会产生哪些 IngestAlert code/severity，每类在什么条件下出现；MES 输入行与本地 TransportDemand 分别有哪些字段、任务类型和状态，它们之间如何映射？

## Answer

2026-08-07 以当前 Core 生产分支、Oracle `MES_TASK_UNION` 查询契约、正式只读 API DTO 和脱敏样例为事实源完成盘点。原型中的 `DUPLICATE_ACTIVE_KEY`、`MES_DATA_STALE` 和 `HOST_UNREACHABLE` 不是生产 `IngestAlert` code；前两者是原型占位文案，后者是 Watch 本地连接事件。

### 系统实际会产生的 IngestAlert

| Code | Severity | 范围 | 触发条件与对投影的影响 |
| --- | --- | --- | --- |
| `POLL_FAILURE` | `ERROR` | 全局 | MES 快照读取失败，包括超时或查询/连接阶段异常；当轮投影完全不变。 |
| `POLL_INCOMPLETE` | `ERROR` | 全局 | 快照缺少必需列，或行中 `TASK_TYPE`/`SUBLOT`/`DATES` 无效而无法构成完整快照；当轮投影完全不变。 |
| `DUPLICATE_RECONCILE_KEY` | `ERROR` | `TASK_TYPE + SUBLOT` | 同一快照内同一业务键出现多行；仅阻断该键的新建/更新，已有 VISIBLE 实例保持不变，其它键继续对账。 |
| `PAUSED_ZERO_DROP` | `ERROR` | `TASK_TYPE` | 某任务类型曾有不少于配置阈值的健康非零数量（默认 10）后骤降为 0；暂停该类型的消失计数和 GONE，默认连续 2 个成功非零轮次后解除。 |
| `FIELD_DRIFT` | `ERROR` | Demand 实例 | 同一 VISIBLE 业务键的 `AREA`/`EQP`/`STEP`/`DATES`/`PACKAGE` 与创建时冻结值不同；保留冻结投影，只更新本轮仍可见的观察信息。 |
| `REAPPEAR_AFTER_GONE` | `WARNING` | 新 Demand 实例 | 曾经 GONE 的同一 `TASK_TYPE + SUBLOT` 再次出现；允许创建新 `DemandId`，details 保留前一个 GONE id 与新 id。 |

告警对外形态为 `alertId/code/severity/taskType/sublot/demandId/message/details/firstSeenAt/lastSeenAt/occurrenceCount/isActive/resolvedAt/createdAt`。相同事件身份与 details fingerprint 持续存在时更新 `lastSeenAt` 并累加次数；原因消失时标记 resolved，默认保留 365 天。`AREA_EMPTY` 与 `AREA_UNPARSEABLE` 是 TransportDemand 上的 `locationRiskCode`，不是 IngestAlert。

### MES 任务输入行与六类 TASK_TYPE

MES 输入行统一为 7 列：`TASK_TYPE`、`SUBLOT`、`AREA`、`EQP`、`STEP`、`DATES`、`PACKAGE`。`TASK_TYPE`、`SUBLOT`、`DATES` 是接入必需值；`DATES` 表示产品进入当前 MES 工序的时间，`STEP` 是下一工序标签。查询使用 `UNION ALL`，不在 SQL 中去重或加上线时间过滤。

| TASK_TYPE | 业务搬运含义 | MES 分支特征 |
| --- | --- | --- |
| `DIE_TO_WIRE_STAGING` | 装片机台 → 焊线/键合派工待送区 | 下一工序为焊线或键合，状态为入库，取最后完工的装片设备与时间。 |
| `DIE_TO_OVEN` | 装片机台 → 烘箱间 | 下一工序为装片烘烤/装片压力烘烤，状态为入站，取最后完工的装片设备与时间。 |
| `WIRE_TO_GATE` | 焊线/键合机台 → 人工质检关卡区 | 下一工序为焊线关卡，状态为入库，来源设备工序为焊线或键合。 |
| `WIRE_TO_OPTICAL` | 焊线/键合机台 → 三光区 | 下一工序为三光检验，状态为完工，来源设备工序为焊线或键合。 |
| `STAGING_TO_WIRE` | 焊线/键合派工待送区 → 指定焊线/键合机台 | 当前工序为焊线或键合，状态为入站，`EQP` 是目标机台，`DATES` 取 `lasttime`。 |
| `WIRE_TO_NITROGEN` | 焊线1机台 → 固定氮气柜 | 下一工序仅为焊线2，状态为入库，来源设备工序仅为焊线，不包含键合。 |

脱敏公开样例 `latest.csv`（2026-07-24 第 10 轮）共 672 行：`DIE_TO_WIRE_STAGING` 105、`DIE_TO_OVEN` 94、`WIRE_TO_GATE` 84、`WIRE_TO_OPTICAL` 52、`STAGING_TO_WIRE` 246、`WIRE_TO_NITROGEN` 91。这些是样例快照数量，不是实时现场数量。一行的典型外观如下：

```text
TASK_TYPE=DIE_TO_OVEN
SUBLOT=Q26063224-8
AREA=C6-14
EQP=3ZPS136
STEP=装片烘烤
DATES=2026-07-24T13:55:34
PACKAGE=SOP8/PP(150mil)(12R)
```

### 本地 TransportDemand 投影形态

MesIngest 用大小写敏感、不做归一化的 `TASK_TYPE + SUBLOT` 作为 `TransportDemandKey`，但为每个本地实例分配独立稳定 `DemandId`。创建时冻结七个 MES 字段，并增加：

- `status`: 仅 `VISIBLE` 或 `GONE`；默认连续 2 个成功快照缺失后转为 GONE。
- `mesLastSeenAt` 与 `disappearCount`: 记录 Host 观测时间和连续消失轮数。
- `locationRisk`/`locationRiskCode`: AREA 空值为 `AREA_EMPTY`；AREA 不符合“字母 + 两位数 + `-` + 两位数，且两个数字段不能为 00”时为 `AREA_UNPARSEABLE`。
- `createdAt`/`goneAt`: 本地实例创建和终结时间。
- `alerts`: 只读 Demand DTO 内嵌与该 `DemandId` 精确相关，或在无 DemandId 时与同一 `TASK_TYPE + SUBLOT` 相关的告警。全局 poll 告警不会嵌入某个 Demand。

同一业务键从 GONE 再现时保留旧 GONE 实例、新建新 `DemandId`；这是本地投影实例更替，不代表 MES 提供了自有任务 id。
