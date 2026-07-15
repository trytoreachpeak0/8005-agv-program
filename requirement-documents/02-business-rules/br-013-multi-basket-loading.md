---
id: BR-013
type: business-rule
title: "Multi-Basket Loading 多花篮装载规则"
status: draft
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-001", "UC-002", "UC-005", "UC-010"]
related_br: ["BR-012", "BR-014"]
aliases: ["BR-013"]
---

# BR-013 Multi-Basket Loading 多花篮装载规则

## Rule Statement 规则内容

### 1. 两层数据模型

1. 运输任务与实体花篮不得使用同一幂等粒度：
   - 运输任务唯一键 = `任务类型 + SUBLOT`（见 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]）
   - 装载明细唯一键 = `运输任务ID + 花篮序号（basket_sequence）`
2. 系统不追踪实体花篮条码。追溯精度为：`SUBLOT + 花篮序号 + AGV 仓位`。
3. 一个 SUBLOT 可对应一个或多个花篮；每次成功装入一篮占用一个仓位，并生成递增的花篮序号。

### 2. IT 提供花篮数量时

1. MES 候选任务创建后可记录预计花篮数。
2. 每次扫码装入一篮并占用一个仓位。
3. 实际装载数量达到预计数量后，任务可自动结束装载。
4. 数量不一致时进入人工确认或异常处理。

### 3. IT 不提供花篮数量时（当前默认）

现场统一采用“重复扫码确认新增一篮”，不提供独立的“新增一篮”按钮：

1. 员工扫描 SUBLOT，系统定位唯一的待取货运输任务并装入第一篮。
2. 员工再次扫描同一 SUBLOT 时，系统弹出“确认新增一篮”提示；员工确认后才计入新的一篮。
3. 系统为该篮分配下一个可用仓位并开门。
4. 每次成功关门后生成递增的花篮序号。
5. 员工点击“该 SUBLOT 装载完成”，系统结束该任务本次装载。

不得仅凭短时间内重复读到相同条码就直接认定第二篮（须防抖、二次确认、仓门状态校验与装载完成确认）。

### 4. 开关门与阶段语义

1. 装货与卸货均由系统自动打开对应仓门；用户关闭仓门即确认该仓位本次操作完成。
2. 系统须结合当前任务阶段区分“装货关门”与“卸货关门”，并更新仓位占用状态。
3. “开始装货”边界（第一个仓门成功打开）对 MES 消失对账的影响见 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]。

### 5. IT 接口切换

若未来 IT 提供花篮数量/标识接口，可切换为第 2 节按预计数量结束装载；未提供前继续使用第 3 节兜底。切换不得改变运输任务幂等键与装载明细分层模型。

## Rationale 制定原因

同一 SUBLOT 常对应多篮实物，若仍按“一任务一篮”建模会导致重复建任务或无法追溯分仓。重复扫码二次确认可在无花篮主数据的情况下区分真多篮与扫码抖动/误扫，同时避免增加现场独立按钮带来的操作分叉。

## Source 来源

2026-07-13 MES 任务模型确认（见 `mes/AGV系统业务与MES任务模型.md` 第 9、13.3 节）：

- 两层幂等模型、不追踪实体花篮条码。
- 花篮现场兜底交互确定为“重复扫码确认新增一篮”。
- IT 是否提供花篮数量接口为可边开发边定事项。

## Related Use Cases 关联用例

- [[uc-001-load-completed-lot-into-slot|UC-001]]：装载流程及“重复扫码新增一篮”备选路径。
- [[uc-002-confirm-task-completion|UC-002]]：装载完成后的确认完成（含“该 SUBLOT 装载完成”语义）。
- [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]：取出错放产品时对装载明细/仓位占用的回退。
- [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：终点站按仓位（花篮）开门卸货。
- [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]、[[br-014-transport-task-types-and-fixed-stations|BR-014]]：任务唯一性与任务类型定义。
