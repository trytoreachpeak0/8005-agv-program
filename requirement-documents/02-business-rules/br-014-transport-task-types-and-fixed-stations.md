---
id: BR-014
type: business-rule
title: "Transport Task Types and Fixed Stations 五类搬运任务类型与固定站点定义"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-007", "UC-001", "UC-010", "UC-023", "UC-008", "UC-024"]
related_br: ["BR-001", "BR-003", "BR-012", "BR-013"]
aliases: ["BR-014"]
---

# BR-014 Transport Task Types and Fixed Stations 五类搬运任务类型与固定站点定义

## Rule Statement 规则内容

### 1. 任务类型

任务类型由本系统定义，用于区分同一 SUBLOT 在不同生产阶段产生的运输需求。MES 的 `STEP` 不能替代本系统任务类型。稳定代码与业务含义如下：

| 代码 | 业务含义 |
| --- | --- |
| `DIE_TO_WIRE_STAGING` | 装片机台 → 焊线/键合派工待送区 |
| `DIE_TO_OVEN` | 装片机台 → 烘箱间 |
| `WIRE_TO_GATE` | 焊线/键合机台 → 人工质检关卡区 |
| `WIRE_TO_OPTICAL` | 焊线/键合机台 → 三光区 |
| `STAGING_TO_WIRE` | 焊线/键合派工待送区 → 指定焊线/键合机台 |

### 2. 起终点判定

1. **DIE_TO_WIRE_STAGING / DIE_TO_OVEN**：起点为查询结果中 EQP/AREA 映射到的装片机台站点；终点分别为固定的派工待送区站点、固定的烘箱间站点。
2. **WIRE_TO_GATE / WIRE_TO_OPTICAL**：起点为查询结果中 EQP/AREA 映射到的焊线或键合机台站点；终点分别为固定的关卡区站点、固定的三光区站点。关卡区/三光区可为公共区域，当前不要求送到区内具体机台。
3. **STAGING_TO_WIRE**：起点为固定的派工待送区（即第 1 类任务终点）；终点为查询结果中 EQP/AREA 映射到的指定焊线或键合机台站点。
4. AREA → 站点解析与冻结规则见 [[br-003-area-station-mapping|BR-003]]；任务幂等与对账见 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]。

### 3. 四个固定区域站点

1. 焊线/键合派工待送区、烘箱间、关卡区、三光区各自配置一个固定 `station_name`（字符串，不是数字 `station_id`）。
2. 通过配置文件或数据库维护，可动态修改；程序不得写死实际地图值。修改只影响之后创建的新任务。
3. 具体地图站点名由现场地图建好后填入，不阻塞只读接入与本地任务状态机开发。

### 4. 互斥与优先级（业务层）

1. `WIRE_TO_GATE` 与 `WIRE_TO_OPTICAL` 互斥：同一 SUBLOT 不得同时命中（见 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]）。
2. `STAGING_TO_WIRE`（第 5 类机台叫料）任务优先级最高；调度与分配侧的进一步规则见 [[br-001-dispatch-task-range|BR-001]]、[[br-002-agv-allocation-eligibility|BR-002]]。
3. 若同一 SUBLOT 的上游任务（如送往派工待送区）仍在执行，而 MES 已产生第 5 类下游任务：不取消上游；下游进入等待上游卸货完成后再释放调度。

### 5. 取货合法性（与混装相关）

1. 取货必须在运输任务声明的起点完成。
2. 在装片机台不得收取起点属于焊线/键合区域或派工待送区的产品。
3. AGV 到达焊线/键合机台后，在仓位与路线条件满足时，可收取该机台已完工、需送关卡或三光的产品；配送与取货可形成“送一批、取一批”复合停靠（范围生成细节见 BR-001）。

## Rationale 制定原因

MES SQL 按工序筛选，但同一 SUBLOT 会在不同阶段产生多条运输需求；用稳定任务类型区分路线与幂等空间，并用可配置固定终点避免把地图站点硬编码进程序。第 5 类叫料优先与上下游等待规则，用于避免机台等料时误取消仍在途的上游任务。

## Source 来源

2026-07-13 及此前确认（见 `mes/AGV系统业务与MES任务模型.md` 第 2.4、3、8、10.4、13 节；`mes/宿迁长电AGV项目MES数据接口需求确认.md` 第 0.2 节）：

- 五类任务起终点与固定区域配置方式。
- 第 5 类最高优先级、上下游等待、混装与复合停靠原则。

## Related Use Cases 关联用例

- [[uc-007-sync-transport-task-from-mes|UC-007]]：按任务类型从 MES 生成带 moveType 的本地任务。
- [[uc-001-load-completed-lot-into-slot|UC-001]]、[[uc-010-unload-completed-lot-at-destination-station|UC-010]]：在声明起点装货、在声明终点卸货。
- [[uc-023-allocate-transport-tasks-to-agv|UC-023]]、[[uc-008-dispatch-move-order-to-riot|UC-008]]：按类型优先级与合法起终点分配并下发。
- [[uc-024-maintain-area-station-mapping|UC-024]]：维护 AREA 解析及固定区域站点配置相关能力。
- [[br-001-dispatch-task-range|BR-001]]、[[br-003-area-station-mapping|BR-003]]、[[br-012-mes-task-idempotency-and-reconciliation|BR-012]]、[[br-013-multi-basket-loading|BR-013]]。
