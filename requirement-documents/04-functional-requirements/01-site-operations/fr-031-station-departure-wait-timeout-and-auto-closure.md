---
id: FR-031
type: functional-requirement
title: "Station Departure Wait Timeout and Automatic Stop Closure 站点离站等待超时与自动结束"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-31
updated: 2026-07-31
related_uc: ["UC-002", "UC-046"]
related_br: []
related_fr: ["FR-003", "FR-004", "FR-013"]
related_nfr: ["NFR-002"]
related_tc: ["TC-103", "TC-104", "TC-105", "TC-106", "TC-107", "TC-108", "TC-109", "TC-110", "TC-111", "TC-112", "TC-113"]
aliases: ["FR-031"]
---

# FR-031 Station Departure Wait Timeout and Automatic Stop Closure 站点离站等待超时与自动结束

## Description 需求描述

系统应在可继续装货站点的车辆满足 StationDepartureWaiting 时，由服务端启动可配置、不可由操作员延长的离站等待期限，并向车载端显示剩余时间。期限届满后，系统须原子结束本站、取消全部尚未开始的待装任务，再同步最新作业与后续计划、执行实时安全核验并安排车辆离站；活动或未收敛仓位操作、待卸任务、断联和状态未知必须阻断该流程。

## Rationale 制定原因

避免无人继续装货或无人点击“本站装货完成”时车辆无限占用业务站点，同时保持任务取消、仓位物理安全、会话清理和调度移动的一致性。

## Origin 需求来源

- 2026-07-30～2026-07-31 需求确认会话
- [[uc-046-handle-station-departure-wait-timeout|UC-046]]
- ADR-cross-0055

## Acceptance Criteria 验收标准

- **AC-1（开始条件与权威）**
  - **Given** 车辆可信到站并停止、车载业务就绪、最新作业和计划投影已确认，当前为可继续装货站点，且没有待卸或未收敛仓位操作
  - **When** 车辆进入 StationDepartureWaiting
  - **Then** 服务端按项目默认 5 分钟或站点覆盖值形成截止时间，车载端只显示该截止时间
  - **待送点例外（`CP-0012`）**：仅适用于 STAGING_TO_WIRE 固定起点的取货停靠，不形成离站等待截止时间，下发的 `stationDepartureDeadlineAt` 为空；离站由 `REQ-0354` 所列装货阶段的结束驱动

- **AC-2（重新计满）**
  - **Given** 车辆曾处于 StationDepartureWaiting
  - **When** 一个 LoadBatch 或 LoadCorrection 安全闭环、放弃尚未产生物理动作的操作，或新增待装 DemandId 的新版清单被车载确认
  - **Then** 系统从完整时长重新计时，不继承旧剩余时间

- **AC-3（禁止人为续时）**
  - **Given** 倒计时正在进行
  - **When** 操作员触屏、打开页面、完成身份核验、无效扫码或尝试“继续等待”
  - **Then** 截止时间保持不变；系统不提供暂停或延长入口
  - **待送点例外（`CP-0012`）**：仅适用于 STAGING_TO_WIRE 固定起点的取货停靠，没有截止时间可续；操作员可以请求出发提前结束（UC-002）

- **AC-4（界面提醒）**
  - **Given** 倒计时正在进行
  - **When** 车载端展示等待状态
  - **Then** 全程显示剩余时间和到期将取消的任务数量，最后 60 秒黄色、最后 10 秒红色逐秒闪烁，不要求声音
  - **待送点例外（`CP-0012`）**：仅适用于 STAGING_TO_WIRE 固定起点的取货停靠，不显示倒计时，显示「无倒计时」或等待客户出发一类的文字，文案另定。`CP-0014` 起，车上已装至少一篮后显示持货倒计时（`cargoHoldingDeadlineAt`，`REQ-0354`），新需求派进本站时倒计时重新开始；站点离站倒计时仍不显示

- **AC-5（超时原子结束）**
  - **Given** 期限届满且车辆仍满足 StationDepartureWaiting
  - **When** 服务端先成功取得超时结束的原子状态转换
  - **Then** 本站结束、全部尚未开始的待装 DemandId 以 `CANCELLED_BY_STATION_TIMEOUT` 终结、审计和取消抑制一次性持久化；已提交 LoadBatch 不受影响
  - **待送点例外（`CP-0012`）**：仅适用于 STAGING_TO_WIRE 固定起点的取货停靠，不会到期，因而不以 `CANCELLED_BY_STATION_TIMEOUT` 终结任何需求，也不触发站点超时的放回与次数上限

- **AC-6（开始操作与超时竞态）**
  - **Given** 装货或纠错请求与超时结束并发
  - **When** 服务端处理两者
  - **Then** 以先成功持久化者生效；操作先成功则超时失效，超时先成功则拒绝新操作且不复活任务

- **AC-7（部分装货只告警）**
  - **Given** LoadBatch 只有部分目标仓位完成，或存在 LoadCorrectionPending
  - **When** 最后一次有效物理进展后达到同一等待时长
  - **Then** 系统只产生装货中断告警，不自动提交、取消或离站

- **AC-8（卸货与站点范围）**
  - **Given** 当前为纯卸货站或装卸混合站仍有待卸任务
  - **When** 仓位暂时物理安全
  - **Then** 不启动离站等待；纯卸货站卸完直接结束，混合站完成全部卸货且仍可继续装货后才启动

- **AC-9（断联恢复）**
  - **Given** 倒计时期间车载端断联或业务就绪失效
  - **When** 服务端检测到该状态
  - **Then** 本轮截止时间失效且不得取消或发车；恢复握手与最新投影对账完成后重新计满

- **AC-10（提交后发车顺序）**
  - **Given** StopClosureCommit 已成功
  - **When** 系统准备移动
  - **Then** 先关闭 OperationSession、清除 OnboardOperatorContext、让车载采用最新作业和计划投影并通过 PreDepartureSafetyCheck，最后才向 RIoT 下发移动

- **AC-11（无下一站路由）**
  - **Given** 本站已结束且没有下一 PlannedStop
  - **When** 系统选择后续去向
  - **Then** 空载车辆进入停车点流程；载有已提交 Sublot 的车辆原地保持并报警

- **AC-12（发车失败不回滚本站）**
  - **Given** StopClosureCommit 已成功
  - **When** RIoT 移动下发失败
  - **Then** 任务和会话不恢复，车辆保持“本站已结束，等待发车重试”并报警

## Related 关联

- **Use Cases：** [[uc-046-handle-station-departure-wait-timeout|UC-046]]；人工结束由 [[uc-002-confirm-task-completion|UC-002]] 复用同一提交边界
- **Functional Requirements：** FR-003 核验 StationDepartureWaiting；FR-004 提交 StopClosureCommit；FR-013 处理会话终结
- **Non-Functional Requirements：** 所有状态转换、取消原因和移动结果须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

由 TC-103～TC-113 覆盖正常计时、重置、自动取消、部分装货、混合站、断联、竞态、路由、界面、发车失败与 LoadBatch 自动提交。

## Notes 备注

- 配置变更只影响下一轮新建期限，不追溯修改已经开始的本轮截止时间。
- 车载端显示倒计时不构成取消或发车权威。
- 待送点取货停靠的例外见 `CP-0012`（AC-1、AC-3、AC-4、AC-5）；该停靠的仓门长时间未闭告警另找触发，只告警不结束。
- 机台取货停靠装货完成后操作员出发时，本站离站等待提前结束，不留纠错宽限（`REQ-0354`，`CP-0014`）。这不是 AC-3 禁止的续时，是提前结束，与 UC-002 原有的「本站装货完成」同一类。
- 机台取货停靠上，旅程仍有其它未结需求、本停靠的需求均已终结、本站一篮未装、没有待做或正在装的需求时，本站离站等待立即结束，下发的截止时间即为此刻；车在持货等单中时照旧持货等单（`REQ-0354`，`CP-0015`）。这同样不是 AC-3 禁止的续时，是提前结束；也不是 AC-5 的超时结束，没有尚未开始的待装需求可以 `CANCELLED_BY_STATION_TIMEOUT`。
- AC-5 的超时终结照原文执行，不放回待派、不按到期次数再次派车；每条被终结的需求形成人工搬运告警，并在看板站点超时抑制清单中列出，MES 关单后告警消除、从清单移除（`REQ-0365`，`CP-0016`）。control-server#703 曾在实现上改为放回待派、第 3 次起终结，v5 起撤回；v4 生产在换装前仍按上限 2 放回、第 3 次起终结并告警。清单只收站点期限到期终结的需求，同码终结的确定装货失败不列入。
