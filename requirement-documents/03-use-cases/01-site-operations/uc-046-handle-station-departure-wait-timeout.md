---
id: UC-046
type: use-case
title: "Handle Station Departure Wait Timeout 处理站点离站等待超时"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-31
updated: 2026-07-31
primary_actor: "服务端（系统内部过程）"
secondary_actor: "车载上位机、RIoT"
frequency: "每次 AGV 在可装货站点进入可离开等待态时"
related_uc: ["UC-001", "UC-002", "UC-006", "UC-010", "UC-041", "UC-043"]
related_br: []
aliases: ["UC-046"]
---

# UC-046 处理站点离站等待超时

## 描述

多仓位 AGV 在可继续装货的站点进入 StationDepartureWaiting 后，服务端启动可配置的离站等待期限并向车载端提供截止时间。期限内若开始装货或纠错则退出等待；若无人继续操作，到期后服务端原子结束本站、取消全部尚未开始的待装任务，并在投影同步和实时安全核验通过后安排车辆前往下一站或停车点。

## 触发条件

服务端确认车辆处于 StationDepartureWaiting。

## 前置条件

1. RIoT 已可信确认车辆到站并停止。
2. 车载端在线且处于 VehicleBusinessReadiness。
3. 最新 CurrentStopWorklistSnapshot 与 UpcomingStopPlanSnapshot 已被车载端确认。
4. 当前站点由服务端裁定允许继续装货。
5. 当前站不存在必须完成的卸货、活动或未收敛的仓位操作，DepartureSafe 为 true。

## 正常流程

1. 服务端按 StationDepartureWaitPolicy 取得项目默认时长或当前站点覆盖值，形成本轮截止时间；第一版默认 5 分钟。
2. 车载端全程显示剩余时间和到期将取消的剩余任务数量；最后 60 秒变黄，最后 10 秒变红并逐秒闪烁。
3. 期限内发生以下任一业务进展时结束本轮等待：
   1. 服务端成功接受装货开始请求；
   2. 服务端成功接受 LoadCorrection 请求；
   3. 操作员按 [[uc-002-confirm-task-completion|UC-002]] 主动结束本站。
4. 若期限届满且超时提交先于任何装货或纠错请求成功持久化，服务端执行 StopClosureCommit：
   1. 原子终结当前停靠；
   2. 将全部尚未开始的待装 DemandId 记为 `CANCELLED_BY_STATION_TIMEOUT` 并写入取消抑制和系统审计；
   3. 结束 OperationSession 并清除 OnboardOperatorContext。
5. 服务端重新计算并下发 CurrentStopWorklistSnapshot 与 UpcomingStopPlanSnapshot，等待车载端确认采用。
6. 服务端执行 PreDepartureSafetyCheck；通过后才向 RIoT 下发前往下一 PlannedStop 的移动任务。
7. 若没有下一 PlannedStop：
   1. 空载车辆进入现有停车点分配流程；
   2. 载有已提交 Sublot 的车辆原地保持并报警。

## 备选流程

### A1 新增待装任务

倒计时期间新增待装 DemandId 时，服务端先下发更高版本 CurrentStopWorklistSnapshot；车载端确认采用后，重新开启完整等待时长。

### A2 完成一个 Sublot 或纠错

LoadBatch 自动提交或 LoadCorrection 安全闭环后，车辆重新满足 StationDepartureWaiting 时，从完整时长重新计时。

### A3 没有剩余待装任务

期限届满时不产生任务取消，仅提交当前停靠结束并继续第 5～7 步。

## 异常流程

### E1 断联或业务未就绪

车载端断联、恢复未完成或投影过期时，本轮截止时间立即失效；不得取消任务或发车。完成 RecoveryHandshake 和最新投影对账后，重新计满。

### E2 部分装货或仓位操作未收敛

存在部分 LoadBatch、LoadCorrectionPending、活动开锁集合、状态未知或必须完成的卸货时，不进入 StationDepartureWaiting。无物理进展达到同一等待时长时只告警，车辆不得离站。

### E3 整站结束事务失败

本站结束、剩余任务取消或审计任一持久化失败时整笔回滚，本站保持未结束，车辆不得移动。

### E4 发车失败

StopClosureCommit 已完成但 RIoT 下发失败时，不复活任务或操作会话；车辆显示“本站已结束，等待发车重试”并报警。

## 后置条件

1. 本站已经原子结束，或仍保持完整的未结束状态，不存在部分取消后离站。
2. 已提交 LoadBatch 不受影响；剩余未开始任务使用明确终态并按 DemandId 抑制重复派发。
3. 发车前车载端已采用最新业务投影且实时安全核验通过。

## 关联用例

- [[uc-001-load-completed-lot-into-slot|UC-001]]：装货开始、LoadBatch 自动提交和部分装货中断。
- [[uc-002-confirm-task-completion|UC-002]]：操作员主动结束本站，复用相同 StopClosureCommit。
- [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：已开始或已提交任务的清空并取消，不属于超时批量取消。
- [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：必须先完成卸货，纯卸货站不进入本 UC。
- [[uc-041-return-idle-agv-to-parking-point|UC-041]]：空载且无下一站时的停车点去向。
- [[uc-043-verify-identity-and-manage-operation-session|UC-043]]：StopClosureCommit 结束会话并清除工号。
