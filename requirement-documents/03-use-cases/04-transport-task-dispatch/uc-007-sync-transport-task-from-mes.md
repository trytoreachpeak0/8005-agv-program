---
id: UC-007
type: use-case
title: "从 MES 同步生成搬运任务"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-09
updated: 2026-07-14
primary_actor: "本地服务器（系统内部过程，非人工角色）"
secondary_actor: MES
frequency: "固定延迟轮询：每轮合并查询完成后默认等待 10 秒再开始下一轮（见 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]）"
related_uc: ["UC-001", "UC-003", "UC-008", "UC-023", "UC-024", "UC-026"]
related_br: ["BR-001", "BR-003", "BR-012", "BR-014"]
aliases: ["UC-007"]
---

# UC-007 从 MES 同步生成搬运任务

## 描述

本地服务器按 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]] 以固定延迟轮询 MES：使用带固定任务类型（[[br-014-transport-task-types-and-fixed-stations|BR-014]]）的 `UNION ALL` 合并 SQL 拉取六类运输候选，完成字段校验、AREA 站点解析（[[br-003-area-station-mapping|BR-003]]）、按 `任务类型 + SUBLOT` 去重与本地对账后，创建或刷新本地任务、取消取货前已消失任务，并处理异常骤降保护与重启恢复基线。本 UC 不包含派车范围划分（[[br-001-dispatch-task-range|BR-001]]）与导航下发。

## 触发条件

上一轮合并查询已完成，且固定延迟等待时间已到；或系统启动后需要建立恢复快照。

## 前置条件

**系统与接口**

1. MES Oracle 只读查询链路可用，且仅能执行预置合并 SELECT（见 BR-012）。
2. 六类任务合并 SQL 已配置并生效；上线基线时间过滤由应用层执行。
3. RCS/RIOT 地图同步得到的表 A/表 B（及显式覆盖）可供 AREA 解析（见 BR-003）；解析失败时任务仍可创建但进入位置异常。

## 后置条件

**任务与数据**

1. 新的 `任务类型 + SUBLOT` 在本地生成运输任务，并冻结 EQP、AREA、DATES 与起终点 `station_name`（若可解析）。
2. 仍存在的本地任务更新 `mes_last_seen_at`，消失计数归零；取货前连续 2 次成功查询消失的任务被取消并撤销相关取货路线。
3. 本轮查询开始/完成时间、耗时、结果数量、成功/失败及同步统计写入本地日志。
4. 涉及类型的 `PAUSED_ZERO_DROP` 状态、消失计数与每类型数量基线按 BR-012 持久化更新。

## 假设

1. 客户 IT 提供的 5 组筛选 SQL 业务逻辑正确；本系统不修改其对入库/入站/完工/STEP 的使用方式，只按任务类型解释结果。
2. MES 返回的 `lot` 业务上表示 SUBLOT；接口输出统一称为 SUBLOT。

## 正常流程

### 7.0

1. 系统确认可开始本轮查询（非重叠；若为重启后第一次完整查询，按 BR-012 建立恢复基线）
2. 系统执行合并 SQL，取得完整快照
   2.1 核验查询通信成功、结果完整、未超时（见 E2.1）
3. 系统按 `TASK_TYPE` 映射为 BR-014 任务类型，标准化字段（去首尾空格）
4. 系统校验 EQP/AREA/DATES 及同行冲突
   4.1 EQP 为空、同一 EQP 多 AREA、同一 SUBLOT 多任务类型等 → 阻断性异常（见 E4.1）
5. 系统按 `任务类型 + SUBLOT` 归并重复行，并与本地任务对账
   5.1 新键 → 创建任务；已存在 → 刷新 last_seen；应用层过滤上线基线以前记录不建任务
6. 系统按 BR-003 解析 AREA 并冻结 `station_name`；无法解析则标记位置异常（见 E6.1）
7. 对完整成功快照中仍缺失、且未开始装货的本地任务累计消失；达连续 2 次则取消并撤销取货路线（见 E7.1）；装货边界见 BR-012 / UC-001
8. 按 BR-012 更新各类型数量基线与 `PAUSED_ZERO_DROP`（见 E8.1）
9. 记录本轮同步日志，等待固定延迟后进入下一轮

## 备选流程

### 7.1 系统重启后的第一次完整查询

1. 执行与 7.0 相同的合并查询与新任务创建
2. 已有任务重新出现：更新 last_seen、消失计数归零
3. 已有任务未出现：本次不累计消失、不取消
4. 每类型数量写入恢复基线；为 0 时不覆盖重启前最后正常非 0 数量
5. 从下一次完整成功查询起恢复 7.0 正常对账

## 异常流程

* E2.1 MES 查询超时/失败/不完整
* E4.1 字段或同行冲突（阻断性 MES 数据异常）
* E6.1 AREA 无法解析或冲突 → 位置异常
* E7.1 取货前 MES 记录消失 → 取消任务
* E8.1 异常骤降进入 `PAUSED_ZERO_DROP`
* E9.1 已取消任务再次出现 → 人工确认
* E10.1 MES 连接中断时的在途处理

### E2.1 MES 查询超时/失败/不完整

1. 本轮不创建新任务、不累计消失、不批量取消；产生接口报警
2. 不启动重叠的下一轮；恢复后从完整成功快照继续
3. 连续 3 轮失败产生高级报警（阈值见 BR-012）

### E4.1 字段或同行冲突

1. EQP 为空、同一 EQP 不同 AREA、同一 SUBLOT 同轮命中多类型（含关卡/三光互斥）等
2. 标记阻断性异常并上报，不得自动选择冲突值创建相互冲突的运输任务
3. 记录异常日志（SUBLOT、类型、EQP/AREA、原因、时间戳）

### E6.1 位置异常

1. AREA 为空、格式不合法、反查不到或命中多个 `station_name`
2. 任务进入 LOCATION_ERROR，不得进入分配与下发
3. 不因后续 MES 补全自动恢复；诊断信息颗粒度见 BR-003

### E7.1 取货前消失取消

1. 连续 2 次完整成功查询未出现，且尚未打开该任务第一个仓门
2. 取消任务、记录“MES记录已消失”，立即撤销相关取货停靠点与路线

### E8.1 PAUSED_ZERO_DROP

1. 某类型上一轮正常非 0 数量 ≥ 配置阈值（默认 10）且本轮为 0
2. 暂停该类型消失计数与取消，报警；其他类型不受影响
3. 连续 2 轮该类型数量 > 0 后自动解除，无人工解除入口

### E9.1 GONE 后同键再次出现或命中调度抑制

1. GONE 后同一 TransportDemandKey 再次出现时，MesIngest 保留旧 GONE 实例、分配新的本地 DemandId 并产生对账告警；不在接入层阻断，也不读取调度状态
2. 调度消费投影时若该 TransportDemandKey 命中本地取消的永久抑制，则不创建或恢复业务任务、不派车；这不改变 MesIngest 的投影

### E10.1 MES 连接中断

1. 已装货/已取货任务继续本地执行
2. 未开始装货但已派车任务暂停前往，待恢复与完整快照确认

## 备注

* 2026-07-14：自 `mes/AGV系统业务与MES任务模型.md` 融合已确认规则，替换原 TBD（去重键、轮询、判定、重试等）；细则以 BR-012、BR-014、BR-003 为准。
* 本 UC 与 BR-001 分工：本 UC 负责任务“生成/对账”，BR-001 负责派车“范围划分”。
* Mock 任务不走本 UC 的 MES 对账路径（见 BR-012）。

## 关联用例

* [[uc-001-load-completed-lot-into-slot|UC-001]]：消费本 UC 生成的任务；第一个仓门打开后改变 MES 消失取消边界。
* [[uc-003-agv-arrives-at-designated-station|UC-003]]：派车到站的下游过程。
* [[br-001-dispatch-task-range|BR-001]]：派车任务范围。
* [[uc-008-dispatch-move-order-to-riot|UC-008]]、[[uc-023-allocate-transport-tasks-to-agv|UC-023]]：分配与下发。
* [[uc-024-maintain-area-station-mapping|UC-024]]：显式覆盖与解析诊断维护。
* [[uc-026-select-template-and-create-workflow-instance|UC-026]]：候选任务匹配模板创建流程实例。
* [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]、[[br-014-transport-task-types-and-fixed-stations|BR-014]]、[[br-003-area-station-mapping|BR-003]]。

## 其他信息

