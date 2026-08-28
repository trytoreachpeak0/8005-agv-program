---
id: UC-043
type: use-case
title: "现场人员身份核验与操作会话管理 Verify Site Personnel Identity and Manage Operation Session"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
primary_actor: "生产操作员（按场景引用 R-01~R-08，见 [[stakeholders-and-user-classes|干系人与用户角色清单]]）"
secondary_actor: "MES（返回人员身份及岗位权限）"
frequency: "项目策略要求身份核验且用户输入或主动更换工号时"
related_uc: ["UC-001", "UC-002", "UC-003", "UC-005", "UC-006", "UC-010", "UC-044", "UC-046"]
related_br: []
aliases: ["UC-043"]
---

# UC-043 现场人员身份核验与操作会话管理

## 描述

操作员在车载上位机扫描工牌或手动输入工号，服务端调用 MES 核验身份及岗位权限。身份核验策略按装货和卸货分别采用项目级统一配置，不按 AGV、站点或单次操作临时切换。8005 项目装货身份核验开启，卸货身份核验关闭。

一次到站的操作会话可以连续处理多个 Sublot。车载端持久化当前已核验工号，新 Sublot 默认沿用；同一 Sublot 从首次开锁到全部结果上传并形成 LoadBatch 提交闭环期间不得更换工号。前一 Sublot 完成后，用户可以主动输入新工号，新工号必须重新校验。掉线或车载程序重启不清除工号、不要求重复验证；人工或超时 StopClosureCommit 后清除。

活动 Sublot 因关键硬件故障等待处置时，R-09 可在当前界面刷自己的卡，为 LoadCompensationDecision 完成二次认证。该刷卡只形成独立审批身份，不属于更换生产操作员；原 Sublot 工号、OnboardOperatorContext 和 OperationSession 保持不变。

8005 卸货不输入工号。若其它项目以后在项目级开启卸货身份核验，则复用本 UC；策略关闭时审计记录策略版本和“未要求操作员”，不得伪造人员身份。

## 触发条件

1. 8005 装货前车载端不存在已核验工号。
2. 当前没有活动、部分或未收敛的 Sublot，用户主动选择更换工号。
3. 其它项目的项目级策略要求在相应装卸流程前核验身份。

## 前置条件

1. 车载端与服务端连接正常，服务端可调用 MES。
2. 当前车辆已经到站并处于站点操作保护状态。
3. 若触发原因是更换工号，则当前不存在活动、部分或未收敛的 Sublot。

## 后置条件

1. 核验成功后，服务端记录工号、人员信息、权限、AGV、站点、策略版本和核验时间；车载端持久化当前工号及核验引用。
2. 新装货 Sublot 在首次开锁前绑定当前已核验工号；直到该 Sublot 全部目标仓位完成并形成 LoadBatch 自动提交闭环前，不允许更换。
3. 掉线或重启后恢复原工号和活动 Sublot 绑定，不重新核验。
4. 人工或超时 StopClosureCommit 后结束本次到站操作会话并清除车载工号。
5. 核验失败时不更新当前工号，也不允许提交新的 Sublot。

## 正常流程

1. 操作员扫描工牌或手动输入工号。
2. 车载端将工号提交服务端。
3. 服务端调用 MES 校验人员身份和岗位权限。
4. 核验成功后，服务端建立或更新本次到站的操作员上下文并记录审计。
5. 车载端持久化并显示当前工号。
6. 操作员输入 Sublot；服务端校验 Sublot、任务、站点和仓位容量。
7. 服务端首次发出该 Sublot 的仓位操作指令时，将当前工号绑定到该 Sublot。
8. 该 Sublot 全部仓位完成并形成 LoadBatch 自动提交闭环后，解除不可换人边界；下一 Sublot 默认沿用当前工号。
9. StopClosureCommit 成功后，服务端结束到站操作会话，车载端清除工号；后续移动失败不恢复。

## 备选流程

### A1. 沿用当前工号

当前工号已经核验且用户没有主动更换时，新的 Sublot 直接沿用，不重复调用 MES。

### A2. 在两个 Sublot 之间更换工号

1. 前一 Sublot 已经形成 LoadBatch 自动提交闭环。
2. 用户选择“更换操作员”并输入新工号。
3. 系统重新执行正常流程第 2～5 步。
4. 下一 Sublot 绑定新工号。

### A3. 卸货身份核验关闭

8005 到站卸货时不执行本 UC 的工号输入流程。服务端按当前站点和在车业务状态识别可卸仓位，审计记录卸货身份核验策略关闭。

### A4. R-09 在活动 Sublot 中完成整批清空审批

1. 原生产操作员保持绑定活动 Sublot。
2. R-09 在当前界面刷自己的卡并通过整批清空决定所需的权限和二次认证核验。
3. 系统将 R-09 记录为 LoadCompensationDecision 决策人，不更新当前生产操作员工号、不结束或重建 OperationSession。

## 异常流程

### E1. 活动 Sublot 中尝试换人

系统拒绝更换，提示必须等待当前 Sublot 形成 LoadBatch 自动提交闭环。R-09 按 A4 刷卡完成整批清空审批不属于换人，不触发本异常。

### E2. 身份或权限校验失败

系统保留原工号（如有），显示稳定失败原因，不允许使用未经核验的新工号开始 Sublot。

### E3. 掉线或重启

车载端保留当前工号、活动 Sublot 和执行日志；恢复后不重复验证原工号，按恢复对账流程继续。掉线期间不得校验新工号或开始新 Sublot。

## 备注

- 工号是到站期间的默认操作员信息，但不可切换边界是当前 Sublot，不是整次到站第一次开门。
- R-09 的审批身份与生产操作员身份并存；审批不修改 OnboardOperatorContext 或 Sublot 操作员绑定。
- 操作会话不设置空闲超时；掉线暂停也不自动结束。
- 车载端只持久化恢复所需的工号和核验引用，不复制 MES 人员主数据。
- 管理配置端的账号会话与本 UC 的现场操作会话彼此独立。

## 关联用例

- [[uc-001-load-completed-lot-into-slot|UC-001]]：8005 装货前需要有效工号，每个 Sublot 固定绑定一名已核验操作员。
- [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：8005 卸货身份核验关闭，不要求输入工号。
- [[uc-003-agv-arrives-at-designated-station|UC-003]]：到站后建立操作会话。
- [[uc-002-confirm-task-completion|UC-002]]：操作员主动结束本站时通过 StopClosureCommit 清除工号。
- [[uc-046-handle-station-departure-wait-timeout|UC-046]]：无人操作超时结束本站时使用相同清除边界。

## 其他信息
