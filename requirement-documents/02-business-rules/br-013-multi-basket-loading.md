---
id: BR-013
type: business-rule
title: "Multi-Basket Loading 多花篮装载规则"
status: draft
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-001", "UC-002", "UC-005", "UC-010"]
related_br: ["BR-012", "BR-014"]
aliases: ["BR-013"]
---

# BR-013 Multi-Basket Loading 多花篮装载规则

## Rule Statement 规则内容

### 1. 任务与仓位占用模型

1. 运输任务唯一键为 `任务类型 + SUBLOT`（见 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]）。
2. 花篮没有实体条码、永久身份或任务内序号；系统不创建 `basket_sequence`，也不根据随机装入顺序赋予花篮身份。
3. 一个 SUBLOT 可对应一个或多个花篮；每篮占用一个仓位。服务端追踪 `SUBLOT + AGV + 仓位 + 占用时间段`，仓位占用记录的技术主键只用于持久化和审计，不代表花篮身份。

### 2. V1 权威花篮数量

1. 操作员输入 SUBLOT 后，服务端用 `SUBLOT_BOX_COUNT` 查询 `MAX_BOX_COUNT`，并结合任务创建时冻结的 `PACKAGE` 和已批准的花篮容量对照，计算 `ExpectedBasketCount = ceil(MAX_BOX_COUNT / capacity)`。
2. V1 将 `ExpectedBasketCount` 作为本次装载的权威数量，而不是估算值、最低值或可编辑参考值；操作员和车载端均不得修改。
3. 查询失败、无结果、数量为空或非正数、`PACKAGE` 缺失、容量未匹配或匹配冲突时，本次装载报错并停止，不分配仓位、不发送开锁指令，也不使用默认数量或现场追加花篮兜底。
4. 服务端必须一次分配与 `ExpectedBasketCount` 数量相等的完整空闲仓位集合；可用仓位不足时整批拒绝，不允许少开仓位或部分装载。
5. 检查通过后，系统一次发起完整目标仓位集合的批量开锁。花篮可以随机放入任一已打开目标仓位，每个仓位最多放一篮。

### 4. 开关门与阶段语义

1. 装货与卸货均由系统自动打开对应仓门；用户关闭仓门即确认该仓位本次操作完成。
2. 系统须结合当前任务阶段区分“装货关门”与“卸货关门”，并更新仓位占用状态。
3. “开始装货”边界（第一个仓门成功打开）对 MES 消失对账的影响见 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]。

### 5. 版本边界

未来版本可以另行评估把查询结果仅作为“最低花篮数量”或可调整参考值，但这不是 V1 行为，不能在未作新决策前通过配置、人工覆盖或异常流程引入。若未来要求追踪实体花篮身份，必须同时引入可附着在实物上的稳定标识和逐篮采集流程，不能复用装入顺序代替。

## Rationale 制定原因

同一 SUBLOT 常对应多篮实物，但花篮随机装入仓位且本身没有可验证身份。系统只需证明该 SUBLOT 占用了哪些仓位及数量；生成顺序号既不能附着到实物，也不能在换位后验证。V1 在输入 SUBLOT 后一次取得并冻结权威数量，才能一次打开等量仓门，避免操作员逐个请求开门。

## Source 来源

2026-07-31 业务确认（见 `mes/docs/AGV系统业务与MES任务模型.md` 第 9、13.3 节）：

- 运输任务与仓位占用分层，不追踪实体花篮条码或任务内花篮序号。
- V1 查询得到的花篮数量不可修改；无法计算时本次装载报错。
- 成功计算后一次批量打开等量仓门；未来“最低数量参考”不属于 V1。

## Related Use Cases 关联用例

- [[uc-001-load-completed-lot-into-slot|UC-001]]：权威数量计算、完整仓位分配与批量开门流程。
- [[uc-002-confirm-task-completion|UC-002]]：完整目标仓位闭环后的装载完成语义。
- [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]：取出错放产品时对仓位占用的回退。
- [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：终点站按仓位（花篮）开门卸货。
- [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]、[[br-014-transport-task-types-and-fixed-stations|BR-014]]：任务唯一性与任务类型定义。
