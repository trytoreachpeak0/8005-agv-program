---
id: BR-003
type: business-rule
title: "AREA-to-Station Mapping AREA—站点解析规则"
status: draft
created: 2026-07-13
updated: 2026-07-13
related_uc: ["UC-007", "UC-008", "UC-023", "UC-024", "UC-026", "UC-027", "UC-028", "UC-029"]
related_br: ["BR-001", "BR-002", "BR-004", "BR-005", "BR-006"]
aliases: ["BR-003"]
---

# BR-003 AREA-to-Station Mapping AREA—站点解析规则

## Rule Statement 规则内容

### 1. 两表解析模型

1. 系统维护两张表把 MES 的 AREA 解析为 AGV 可导航的地图站点：
   - 表 A（站点主数据）：`station_id ↔ station_name`，从 RCS/RIOT（即 RIOT 地图，与 AGV 地图为同一份）同步获得，一一对应，不允许人工新增、修改或删除。
   - 表 B（AREA 归属）：`station_name → area_code[]`（最多 3 个）。默认由拆分 `station_name` 自动派生：按下划线切分，每一段必须是合法的 area_code；当某个 `station_name` 无法按该规则拆分（命名不规范）时，允许通过第 3 节的显式覆盖记录人工补充其 `area_code` 列表。
2. `area_code` 编码格式固定为：字母 + 两位数字 + `-` + 两位数字；数字不足两位时补零（如 01、02），不存在 `00`，编号从 `01` 起。不符合该格式的字符串不能作为 area_code 参与解析。
3. `station_name` 的命名约定：由 1～3 个 `area_code` 用下划线拼接而成（如 `Q11-15_Q12-15_Q13-50`）；不满足该约定的 `station_name` 只能通过显式覆盖记录建立 area_code 归属，不能被系统当作命名不规范而拒绝同步或使用。
4. 一个非空 AREA 在同一时间只能解析出一个 `station_name`。若按表 B 反查同一 AREA 命中多个不同 `station_name`（无论来自自动派生还是显式覆盖记录），判定为数据/配置冲突，必须上报，不得由系统自动挑选其中之一。

### 2. 站点来源与有效性

1. `station_name` 与 `station_id` 均必须来自 RCS/RIOT 当前地图站点列表（表 A）；系统不得根据 AREA 名称或人工输入编造一个未被 RCS/RIOT 确认存在的站点。
2. 表 A 同步失败、结果不完整或站点状态无法确认时，采用 fail-closed：允许只读查看已缓存的表 A/表 B 及显式覆盖记录，禁止基于不完整数据新增、修改或重新启用显式覆盖记录，也不得用过期快照解析新出现的 AREA。
3. 已启用映射（自动派生或显式覆盖）所指向的 `station_name` 后续从表 A 中消失或失效时，系统应将该解析结果标记为异常；依赖它的新任务不得进入分配和下发。

### 3. 显式覆盖记录的版本与停用

1. 显式覆盖记录只用于表 B 无法按命名规则自动派生的 `station_name`；不物理删除，修改时关闭原有效版本并创建新版本，不再使用时停用。
2. 每个版本至少记录 `station_name`、`area_code` 列表、状态、生效时间、失效时间、操作人、原因和审计信息。
3. 新版本或停用只影响生效后创建的新任务；已创建任务继续使用创建时冻结的 `station_name` 快照，不因表 A/表 B/显式覆盖记录的后续变化自动更新。
4. 显式覆盖记录保存前必须再次刷卡或认证。

### 4. 任务使用规则

1. [[uc-007-sync-transport-task-from-mes|UC-007]] 创建任务时，必须按任务创建时刻的表 A、表 B（含当时生效的显式覆盖记录）解析 AREA，并只冻结解析得到的 `station_name`（不冻结 `station_id`）。
2. AREA 为空、AREA 编码格式不合法、反查不到 `station_name`、反查命中多个不同 `station_name`，均判定为“位置异常（LOCATION_ERROR）”或数据冲突，任务不得下发。
3. 起终点未成功解析并冻结 `station_name` 的任务，不得进入 [[br-001-dispatch-task-range|BR-001]] 的派车任务范围，也不得进入 [[uc-023-allocate-transport-tasks-to-agv|UC-023]] 的车辆分配。
4. [[uc-008-dispatch-move-order-to-riot|UC-008]] 向 RCS/RIOT 下发前，使用任务已冻结的 `station_name` 实时查表 A 取得当前 `station_id`；查不到有效 `station_id`（如地图已改名、站点已失效）时，任务转为位置异常，不下发，不重新解析 AREA 本身。`station_id` 只在下发调用的瞬间现查现用，不作为本系统的持久化字段，也不写入配置文件或数据库。

### 5. 流程步骤使用边界

1. 本规则的解析/查询能力可由 [[uc-026-select-template-and-create-workflow-instance|UC-026]] 和 [[uc-027-execute-workflow-steps|UC-027]] 作为预置能力调用，但流程只能读取、校验并冻结按本规则自动派生或由 UC-024 维护且生效的显式覆盖记录得到的解析结果。
2. [[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]、任何模板、条件跳过、重试或人工异常处置均不得修改表 A、猜测/替换站点、覆盖历史任务快照或绕过本规则的 fail-closed 条件。
3. 解析异常步骤只能失败或等待有权限人员通过 UC-024 新增/修正显式覆盖记录；流程实例状态不得替代任务的“位置异常”业务语义。

### 6. 解析失败与冲突的诊断信息

1. 系统重建表 B（每次地图同步后重新按命名规则拆分 `station_name`）时，对每一个未能拆分出合法 `area_code` 的 `station_name`，必须记录并可供 [[uc-024-maintain-area-station-mapping|UC-024]] 展示以下信息，不得只给出汇总数量或“解析失败”这类笼统结论：
   - 该站点的 `station_id` 与 `station_name`；
   - 具体失败原因（例如：`_` 分段数超过 3 个、存在分段不符合“字母 + 两位数字 + `-` + 两位数字”格式、分段数字为 `00`等）。
2. 第 4 节任务使用规则中判定为“位置异常”或“数据/配置冲突”的每一次发生，都必须记录并可供查询以下信息，不得只给出笼统的异常类型：
   - 触发判定所用的原始 AREA（若存在）；
   - 判定为“位置异常”时，涉及的 `station_name`（若已解析出但下发时查不到 `station_id`，还需给出该 `station_name`）及具体原因（如“AREA 编码格式不合法”“反查不到 station_name”“station_name 已从表 A 中失效/改名”）；
   - 判定为“数据/配置冲突”时，涉及的 AREA 及全部命中的 `station_name`/`station_id`列表。
3. 第 1 款（表 B 构建诊断）与第 2 款（任务/派车诊断）是两类不同粒度的信息，分别服务于 R-12/R-13 的例行巡检维护、以及具体业务任务的异常处置，两者都必须精确到具体 `station_id`/`station_name`/`AREA`，不得相互替代或合并为单一汇总指标。

## Rationale 制定原因

MES AREA 是生产位置编码，RCS/RIOT 地图站点是 AGV 可导航目标，两者语义不同。多数站点命名本身已经按“1～3 个 AREA 编码拼接”的规则表达了归属关系，若仍要求项目上线前人工逐条建立 AREA—站点映射，会造成大量重复、易错的手工录入工作。让系统默认按命名规则自动派生 AREA 归属，只对少数命名不规范的站点保留人工显式覆盖记录，既减少了维护负担，又通过版本化和二次认证保留了对例外情况的可审计、可追溯控制。

`station_id` 是 RCS/RIOT 用于下达移动指令的数字标识，会随地图重新编号或站点重建而变化；`station_name` 是可读、稳定的业务标识。统一使用 `station_name` 持久化，`station_id` 只在派车调用瞬间现查，可以避免地图变更导致历史数据或配置失效。

## Source 来源

2026-07-13 需求确认（首次）：

- R-12 和 R-13 均可维护映射。
- 地图站点必须从 RCS/RIOT 同步，不允许任意手工录入。
- 映射修改只影响新任务。
- 不再使用的映射采用停用并保留历史，不物理删除。

2026-07-13 需求确认（更新，两表模型）：

- RCS 地图即 RIOT 地图即 AGV 地图，三者是同一份；RCS 下发任务使用数字 `station_id`。
- 系统维护两张表：`station_id ↔ station_name`（从地图同步获得）与 `station_name → area_code[]`（最多 3 个）。
- `station_name` 命名方式为 1～3 个 `area_code` 用下划线拼接（如 `Q11-15_Q12-15_Q13-50`）；`area_code` 格式为字母 + 两位数字 + `-` + 两位数字，数字不足两位补零，不存在 `00`，从 `01` 起。
- 默认由该命名规则自动派生 AREA 归属，不要求项目上线前人工准备完整映射表；命名不规范的个别站点才需要人工新增显式覆盖记录，仍需 R-12/R-13 维护、二次认证和完整审计。
- 所有配置文件和数据库均不得保存 `station_id`，只保存 `station_name`；`station_id` 只在向 RCS/RIOT 发起派车调用的瞬间现查现用。

2026-07-13 需求确认（补充，失败诊断颗粒度）：

- 表 B 构建阶段无法自动拆分出合法 `area_code` 的 `station_name`，必须逐条报告 `station_id`、`station_name` 和具体失败原因。
- 任务/派车阶段判定为“位置异常”或“数据/配置冲突”时，必须列出具体的 AREA、`station_id`/`station_name` 和原因。
- 禁止只给汇总数量或“解析失败/冲突”这类笼统提示，确保维护人员能定位到具体站点并采取对应动作（补充显式覆盖记录、修正现场配置等）。

## Related Use Cases 关联用例

- [[uc-024-maintain-area-station-mapping|UC-024]]：查看自动解析结果，并执行显式覆盖记录的新增、修改、停用和审计。
- [[uc-007-sync-transport-task-from-mes|UC-007]]：任务创建时解析并冻结 `station_name`。
- [[uc-023-allocate-transport-tasks-to-agv|UC-023]]：排除位置异常或站点未冻结的任务。
- [[uc-008-dispatch-move-order-to-riot|UC-008]]：下发前用冻结的 `station_name` 现查 `station_id` 并正式下发。
- [[uc-026-select-template-and-create-workflow-instance|UC-026]]：消费并冻结本规则提供的站点解析结果，不能修改表 A/表 B 或显式覆盖记录。
- [[uc-027-execute-workflow-steps|UC-027]]：通过预置步骤调用解析校验/查询，并接收完成、失败或等待修复结果。
- [[uc-028-handle-workflow-step-exception|UC-028]]：解析异常时保持阻断，不能跳过或人工覆盖本规则。
- [[uc-029-view-workflow-instance-progress|UC-029]]：只读展示解析结果、位置异常、等待原因和步骤审计。
- [[br-001-dispatch-task-range|BR-001]]、[[br-002-agv-allocation-eligibility|BR-002]]：分别依赖有效冻结站点确定任务范围和车辆覆盖资格。
- [[br-004-workflow-template-matching|BR-004]]、[[br-005-workflow-template-versioning|BR-005]]、[[br-006-workflow-step-execution|BR-006]]：约束模板和流程执行，但均不能覆盖本规则的解析硬约束。
