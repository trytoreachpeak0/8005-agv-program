---
id: UC-002
type: use-case
title: "Complete Current Loading Stop 结束本站装货作业"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-08
updated: 2026-07-31
primary_actor: "当前已通过装货身份核验的生产操作员"
secondary_actor: "服务端、车载上位机、RIoT"
frequency: "操作员希望不再等待本站其它 Sublot 时"
related_uc: ["UC-001", "UC-006", "UC-010", "UC-041", "UC-043", "UC-046"]
related_br: []
aliases: ["UC-002"]
---

# UC-002 结束本站装货作业

## 描述

操作员在车辆处于 StationDepartureWaiting 时点击“本站装货完成”，表达不再等待当前站点其它 Sublot 的意图。单个 LoadBatch 已在全部目标仓位物理闭环后自动提交，本用例不确认或提交单个 Sublot。若仍有尚未开始的待装任务，界面明确显示数量并要求二次确认；确认后服务端以 StopClosureCommit 原子取消剩余任务、结束本站和操作会话，再同步投影、安全核验并请求车辆离站。

### 待送点取货停靠：出发（`CP-0012`）

仅适用于 STAGING_TO_WIRE 固定起点的取货停靠，机台取货停靠照本用例其余部分。

- **触发**：已核验操作员在车载屏点「出发」并二次确认。按钮只在待送点取货停靠显示；车辆处于持货等单，且没有仓位操作进行中、没有纠错或取消处理中时可按。
- **前置条件**：「车辆处于 StationDepartureWaiting」改为「车辆处于待送点取货停靠的装货阶段」（待送点没有离站等待期限）。
- **正常流程**：
  1. 二次确认时显示「没装的 N 条将放回，等下一趟」，不说「取消」。
  2. 车载端发送 `CurrentStopDepartureRequested`（protocol v4），带站点、所见清单版本、出发请求号与操作员；作业会话可为空（持货等单时清单为空、会话为空）。
  3. 服务端按站点与清单版本认出停靠，核验状态，以 `CurrentStopDepartureResult` 回答接受或拒绝。
  4. 接受时服务端结束装货阶段（`closedReason` 为 `OPERATOR_DEPARTED`）：本停靠尚未开始装货的待装需求从本旅程释放、放回待派，不取消、不写抑制；结束作业会话、清除操作员上下文。
  5. 下发最新清单与计划（有未装需求被放回时，空清单的 `stopEndedReason` 为 `OPERATOR_DEPARTED`），离站安全核验（`checkPurpose = DEPARTURE`）通过后，前往已装货物的卸货停靠。
- **备选 A1 一篮未装**：没装的全部放回，本旅程结束，车留在原地，屏上没有清单、不能扫码。
- **异常 E1**：仓位操作进行中、纠错或取消处理中、清单版本过时、站点不符、身份失效时拒绝（`ACTION_NOT_ALLOWED_IN_STATE`、`WORKLIST_REVISION_STALE`、`STATION_MISMATCH`），在 `CurrentStopDepartureResult.problem` 里返回明确原因。
- **异常 E2**：重复的出发请求（同一请求号）只执行一次，服务端重放同一份结果。
- **锚需求**：旅程上第一条受理的需求在别的需求还挂在旅程上时放不回去；已装了一篮以上、锚恰好没装时，实现要换锚或另想办法，不能因此拒绝出发。

### 机台取货停靠装货完成后：出发（`CP-0014`）

仅适用于机台取货停靠（STAGING_TO_WIRE 固定起点以外的取货停靠）。

- **触发**：已核验操作员在车载屏点「出发」并二次确认。按钮在本停靠作业清单上的需求都已装完、本站至少一篮之后显示，不论车在持货等单还是只剩站点离站等待；装货前、等录入时不显示。没有仓位操作进行中、没有纠错或取消处理中时可按。（`CP-0015` 按实现改正，原写「车上」；本站一篮没装、旅程还要继续时不显示出发，离站等待自动结束，见 `UC-006`「机台取货停靠：取消后本站空了立即离站」。）
- **正常流程**：与上一节第 2、3、5 步相同（`CurrentStopDepartureRequested`／`CurrentStopDepartureResult`）。第 4 步改为：车在持货等单时，服务端按持货期限此刻到期处理，`closedReason` 为 `OPERATOR_DEPARTED`，后面计划里尚未开始装的追加停靠放回待派，不取消、不写抑制；装货阶段已结束时不改装货阶段。两种情形都结束本站作业会话，不再等站点离站等待期限的剩余部分，立即请求离站。第 1 步的二次确认要说清按了就不能再纠错；有追加停靠被放回时说出数量。
- **异常**：同上一节 E1、E2；另外本停靠装货完成之前拒绝（`ACTION_NOT_ALLOWED_IN_STATE`）。
- **清单版本过期**：出发请求所带清单版本已过期、但新旧两版在本站已装与待做项上没有实质差别时照样受理，有实质差别时照旧以 `WORKLIST_REVISION_STALE` 拒绝（`CP-0015`，`REQ-0354` 修订文）。

## 触发条件

当前已核验操作员点击“本站装货完成”。

## 前置条件

1. 车辆处于 StationDepartureWaiting。
2. 当前站不存在必须完成的卸货、活动或未收敛的仓位操作。
3. CurrentStopWorklistSnapshot 与 UpcomingStopPlanSnapshot 为最新。
4. 当前操作员身份和 OperationSession 仍有效。

## 正常流程

1. 车载端向服务端提交 CurrentStopLoadingComplete 请求，包含操作员引用和所见 worklistRevision。
2. 服务端重新核验身份、StationDepartureWaiting 和当前权威作业清单。
3. 若仍有尚未开始的待装任务，服务端返回剩余数量，车载端显示“结束本站将取消剩余 N 个任务”并要求二次确认。
4. 操作员确认后，服务端执行 StopClosureCommit：
   1. 原子终结当前停靠；
   2. 将剩余待装 DemandId 记为 `CANCELLED_BY_STOP_COMPLETE`，写入取消抑制和操作员审计；
   3. 结束 OperationSession 并清除 OnboardOperatorContext。
5. 服务端下发最新 CurrentStopWorklistSnapshot 与 UpcomingStopPlanSnapshot，等待车载端确认采用。
6. 服务端执行 PreDepartureSafetyCheck，通过后向 RIoT 请求前往下一 PlannedStop。

## 备选流程

### A1 没有剩余待装任务

步骤 3 不要求二次确认，步骤 4 不产生任务取消，只提交当前停靠结束和审计。

### A2 没有下一站

空载车辆进入停车点流程；载有已提交 Sublot 的车辆原地保持并报警。

## 异常流程

### E1 资格失效

服务端发现待卸任务、活动或未收敛仓位操作、投影过期、身份失效或 DepartureSafe 不成立时，拒绝结束本站并返回明确原因。

### E2 与新操作竞态

若装货或纠错请求先成功持久化，本站结束请求被拒绝；若 StopClosureCommit 先成功，新操作被拒绝且不得复活已取消任务。

### E3 StopClosureCommit 失败

任一任务取消、本站终结或审计写入失败时整笔回滚，本站保持未结束。

### E4 发车失败

本站结束保持有效，不恢复任务和会话；界面显示“本站已结束，等待发车重试”并报警。

## 后置条件

1. 本站完整结束，或完整保持未结束，不存在部分取消状态。
2. 已提交 LoadBatch 和其纠错审计不被改写。
3. 发车前最新业务投影已确认且实时安全核验通过。

## 关联用例

- [[uc-001-load-completed-lot-into-slot|UC-001]]：单个 LoadBatch 的自动提交。
- [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：针对一个已开始或已提交 DemandId 的清空并取消。
- [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：待卸任务必须先完成。
- [[uc-041-return-idle-agv-to-parking-point|UC-041]]：空载且无下一站时的停车点流程。
- [[uc-043-verify-identity-and-manage-operation-session|UC-043]]：身份核验和 StopClosureCommit 后会话清理。
- [[uc-046-handle-station-departure-wait-timeout|UC-046]]：无人操作时自动触发同一整站结束边界（待送点取货停靠没有等待期限，不触发）。
