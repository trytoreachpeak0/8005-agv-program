---
id: WORKFLOW-STEP-CATALOG
type: reference
title: "Workflow Step Catalog 预置流程步骤目录"
status: draft
created: 2026-07-13
updated: 2026-07-13
catalog_version: "2026.07.13"
related_uc: ["UC-001", "UC-003", "UC-004", "UC-007", "UC-008", "UC-009", "UC-010", "UC-023", "UC-025", "UC-026", "UC-027", "UC-028", "UC-029"]
related_br: ["BR-001", "BR-002", "BR-003", "BR-004", "BR-005", "BR-006"]
aliases: ["Workflow Step Catalog", "预置步骤目录"]
---

# Workflow Step Catalog 预置流程步骤目录

## 1. 目录用途与通用约束

本目录定义流程模板可选用的预置步骤类型。模板管理员只能选择步骤、填写该步骤公开的受限参数，并按 [[br-006-workflow-step-execution|BR-006]] 配置顺序、允许的条件跳过、有限重试或等待外部事件；不能改变步骤实现。

通用约束：

1. 每个步骤输入、输出、幂等键、尝试次数、时间、执行结果和错误都必须审计。
2. “可跳过”表示该类型允许在模板中配置预置条件跳过，不表示运行时可以任意越过；标记为“否（安全）”的强制安全步骤禁止跳过。
3. “可重试”表示允许按步骤定义配置有限自动重试，不表示所有错误均可重试；业务冲突、权限失败、安全失败和结果未知必须遵守 [[br-006-workflow-step-execution|BR-006]]。
4. 下表“关联 UC/BR”用于需求追溯；步骤仍须遵守实例绑定的 [[br-005-workflow-template-versioning|BR-005]] 快照和 [[br-004-workflow-template-matching|BR-004]] 匹配结果。
5. 输入中的“引用”是受类型约束的任务、流程、站点、车辆、仓位或接口配置引用，不允许管理员填写 SQL、脚本、URL、HTTP 方法或任意请求体。

## 2. MES 步骤

| 步骤类型 | 可跳过 | 可重试 | 输入 | 输出 | 关联 UC/BR | 安全边界 |
| --- | --- | --- | --- | --- | --- | --- |
| `MES_CANDIDATE_RECEIVE` 候选接收 | 否 | 是 | 轮询批次 ID、预置查询结果引用、任务来源 | 原始候选快照、接收数量 | [[uc-007-sync-transport-task-from-mes\|UC-007]]、[[uc-027-execute-workflow-steps\|UC-027]] | 只接收预置只读查询结果；查询失败/不完整时不得生成候选，不得执行 SQL。 |
| `MES_CANDIDATE_VALIDATE` 候选校验 | 否 | 否 | 候选快照、`moveType`、字段及业务校验规则 ID | 校验通过候选或标准错误码 | [[uc-007-sync-transport-task-from-mes\|UC-007]]、[[br-004-workflow-template-matching\|BR-004]] | EQP、AREA、任务类型等关键值未知或冲突时 fail-closed；不得猜测或自动修正业务值。 |
| `MES_CANDIDATE_DEDUPLICATE` 去重 | 否 | 是 | 已校验候选、`moveType + SUBLOT` 幂等键、本地任务索引 | 新候选/重复/冲突结论 | [[uc-007-sync-transport-task-from-mes\|UC-007]]、[[br-006-workflow-step-execution\|BR-006]] | 去重存储不可用或同一 SUBLOT 多类型冲突时不得建单；不得用 `SUBLOT + STEP` 替代正式幂等键。 |
| `MES_TASK_CREATE` 建单 | 否 | 是 | 唯一候选、冻结的 AREA/EQP/起终点、模板版本快照 | 业务任务 ID、初始状态、绑定快照 ID | [[uc-007-sync-transport-task-from-mes\|UC-007]]、[[uc-026-select-template-and-create-workflow-instance\|UC-026]]、[[br-003-area-station-mapping\|BR-003]]、[[br-005-workflow-template-versioning\|BR-005]] | 建单、幂等占位和快照绑定必须原子；位置或模板不确定时不得进入可执行状态；正式 MES 任务禁止人工创建。 |
| `MES_WRITEBACK_TBD` 回写占位 | 否 | 否 | TBD：经评审确认的回写契约引用、业务任务结果 | TBD：回写回执及对账结果 | [[uc-002-confirm-task-completion\|UC-002]]、[[uc-027-execute-workflow-steps\|UC-027]] | **占位、禁止启用。** 回写内容、接口、权限、幂等、重试和补偿完成评审前不得发布到模板、不得复用查询账号或提供任意 SQL/API。 |

## 3. 调度步骤

| 步骤类型 | 可跳过 | 可重试 | 输入 | 输出 | 关联 UC/BR | 安全边界 |
| --- | --- | --- | --- | --- | --- | --- |
| `DISPATCH_RESOLVE_AREA_STATION` AREA 映射 | 否 | 是 | 冻结 AREA/EQP、映射有效时刻 | 起终点站点、站点类型、映射版本或位置异常 | [[uc-024-maintain-area-station-mapping\|UC-024]]、[[br-003-area-station-mapping\|BR-003]] | 映射缺失、停用、异常或站点无效时进入位置异常；不得任选站点。已冻结任务不得被新映射改写。 |
| `DISPATCH_BUILD_TASK_SCOPE` 任务范围 | 否 | 是 | 可调度任务、冻结起终点、依赖关系、容量需求 | 本次派车任务集合及范围 ID | [[uc-023-allocate-transport-tasks-to-agv\|UC-023]]、[[br-001-dispatch-task-range\|BR-001]] | 位置异常、依赖未满足或不合法取货点的任务不得进入范围；不得靠合并任务绕过校验。 |
| `DISPATCH_SELECT_AGV` 选车 | 否（安全） | 是 | 任务范围、车辆实时状态、能力/电量/仓位配置 | 唯一 AGV 或不可分配原因 | [[uc-022-view-agv-fleet-and-availability\|UC-022]]、[[uc-023-allocate-transport-tasks-to-agv\|UC-023]]、[[br-002-agv-allocation-eligibility\|BR-002]] | 强制安全步骤。在线、空闲、仓门、光幕、电量或本地作业任一未知即不可分配。 |
| `DISPATCH_SUBMIT_RCS_MOVE` RCS 下发 | 否（安全） | 是（先对账） | AGV、任务范围、固定站点序列、稳定幂等键、预置接口配置引用 | RCS/RIOT 移动任务 ID、受理状态 | [[uc-008-dispatch-move-order-to-riot\|UC-008]]、[[br-002-agv-allocation-eligibility\|BR-002]] | 强制安全步骤。下发前复核移动联锁；超时结果未知时先按业务键查询，不得盲目重发；不得配置任意 URL/API。 |

## 4. 移动步骤

| 步骤类型 | 可跳过 | 可重试 | 输入 | 输出 | 关联 UC/BR | 安全边界 |
| --- | --- | --- | --- | --- | --- | --- |
| `MOVE_WAIT_DEPARTURE` 等待离站 | 是 | 否 | RCS 移动任务 ID、起点、预期 AGV | 已离站事件及时间 | [[uc-009-monitor-move-order-until-arrival\|UC-009]]、[[uc-027-execute-workflow-steps\|UC-027]] | 仅可在无需确认离站的预置流程中跳过；若后续动作依赖离站事实则必须等待。事件必须匹配 AGV、任务和站点。 |
| `MOVE_WAIT_ARRIVAL` 等待到站 | 否 | 否 | RCS 移动任务 ID、目标站点、预期 AGV | 到站事件、到站时间和站点 | [[uc-003-agv-arrives-at-designated-station\|UC-003]]、[[uc-009-monitor-move-order-until-arrival\|UC-009]] | 未收到可认证且关联一致的到站事件不得开放站点作业；超时进入异常处理，不得默认到站。 |
| `MOVE_CONFIRM_STATUS` 状态确认 | 否（安全） | 是 | RCS 任务 ID、AGV、预期位置/状态 | 已确认状态或不一致异常 | [[uc-003-agv-arrives-at-designated-station\|UC-003]]、[[uc-009-monitor-move-order-until-arrival\|UC-009]]、[[br-002-agv-allocation-eligibility\|BR-002]] | 强制安全步骤。RCS 状态与本地事件不一致或读取失败时阻断开门、装卸和后续移动。 |

## 5. 人工步骤

| 步骤类型 | 可跳过 | 可重试 | 输入 | 输出 | 关联 UC/BR | 安全边界 |
| --- | --- | --- | --- | --- | --- | --- |
| `HUMAN_AUTHENTICATE_AUTHORIZE` 认证与授权 | 否（安全） | 是 | 工牌/个人身份凭据引用、所需角色/权限、操作上下文 | 操作人 ID、授权结论、认证时间 | [[uc-001-load-completed-lot-into-slot\|UC-001]]、[[uc-010-unload-completed-lot-at-destination-station\|UC-010]]、[[uc-025-maintain-workflow-template\|UC-025]] | 强制安全步骤。不得使用共享账号；认证失败、权限不足或身份未知时阻断危险操作，不记录明文凭据。 |
| `HUMAN_SCAN_MATERIAL` 扫码 | 是 | 是 | 扫描设备、预期编码类型、任务/站点上下文 | 原始扫描摘要、标准化 SUBLOT/物料标识、匹配结论 | [[uc-001-load-completed-lot-into-slot\|UC-001]]、[[uc-010-unload-completed-lot-at-destination-station\|UC-010]] | 仅非扫码业务模板可跳过；受控物料或模板要求核验时不得跳过。抖动去重不得虚构第二篮。 |
| `HUMAN_LOAD_UNLOAD_MATERIAL` 装取料 | 否 | 否 | 已授权人员、任务、仓位、物料、作业方向 | 装/取料事实、数量/花篮序号、仓位占用结果 | [[uc-001-load-completed-lot-into-slot\|UC-001]]、[[uc-010-unload-completed-lot-at-destination-station\|UC-010]]、[[uc-004-slot-door-safety-interlock\|UC-004]] | 必须在正确站点和已授权仓位执行；不得在门锁/光幕/任务范围未知时开始，也不得仅凭按钮点击认定物理动作完成。 |
| `HUMAN_CONFIRM_OPERATION` 人工确认 | 是 | 否 | 待确认动作、任务/仓位、提示内容、操作人 | 确认/拒绝、原因、时间 | [[uc-002-confirm-task-completion\|UC-002]]、[[uc-006-cancel-transport-task-upon-arrival\|UC-006]]、[[uc-027-execute-workflow-steps\|UC-027]] | 不得用普通人工确认替代传感器、安全联锁、二次认证或未授权审批；高风险确认必须使用专门权限和原因。 |

## 6. 硬件步骤

| 步骤类型 | 可跳过 | 可重试 | 输入 | 输出 | 关联 UC/BR | 安全边界 |
| --- | --- | --- | --- | --- | --- | --- |
| `HARDWARE_UNLOCK_SLOT` 开锁 | 否（安全） | 是（先查状态） | AGV/柜体、仓位、预置 IO 映射、授权作业 ID | 开锁命令回执、锁/门状态 | [[uc-004-slot-door-safety-interlock\|UC-004]]、[[uc-015-slot-door-unlock-open-test\|UC-015]] | 强制安全步骤。任务、人员、仓位、站点和联锁全部明确有效后才可开锁；结果未知先查状态，不得重复脉冲。 |
| `HARDWARE_WAIT_DOOR_CLOSED` 关门 | 否（安全） | 否 | 仓位、门状态点位、超时 | 已关门状态及时间或超时异常 | [[uc-004-slot-door-safety-interlock\|UC-004]]、[[uc-017-slot-door-state-detection-test\|UC-017]] | 强制安全步骤。仅明确的当前关门信号可成功；未知/抖动/超时不得放行移动。 |
| `HARDWARE_CHECK_LIGHT_CURTAIN` 光幕确认 | 否（安全） | 是 | 仓位/区域、光幕点位、有效性窗口 | 无遮挡/遮挡/未知及采样时间 | [[uc-004-slot-door-safety-interlock\|UC-004]]、[[uc-016-slot-light-curtain-function-test\|UC-016]] | 强制安全步骤。必须读取当前有效状态；通信失败或未知按遮挡处理，不得使用过期成功值。 |
| `HARDWARE_VERIFY_SAFETY_INTERLOCK` 安全联锁 | 否（安全） | 是 | 全部仓门、门锁、光幕、IO 通信、急停及移动条件 | 允许移动或逐项阻断原因 | [[uc-004-slot-door-safety-interlock\|UC-004]]、[[uc-008-dispatch-move-order-to-riot\|UC-008]]、[[br-002-agv-allocation-eligibility\|BR-002]] | 强制安全步骤。所有条件必须明确正常才允许移动；任一未知、异常或审计失败均 fail-closed。 |

## 7. 异常处理步骤

| 步骤类型 | 可跳过 | 可重试 | 输入 | 输出 | 关联 UC/BR | 安全边界 |
| --- | --- | --- | --- | --- | --- | --- |
| `EXCEPTION_RETRY_STEP` 重试 | 是 | 否 | 失败步骤、错误分类、当前尝试次数、重试策略 | 已安排重试或不可重试结论 | [[uc-028-handle-workflow-step-exception\|UC-028]]、[[br-006-workflow-step-execution\|BR-006]] | 只允许重试目录标记可重试且错误可恢复的原步骤；不得重试安全拒绝、永久错误或结果未知的副作用。 |
| `EXCEPTION_RAISE_ALERT` 告警 | 是 | 是 | 严重级别、错误码、任务/流程/设备上下文、通知策略 ID | 告警 ID、投递状态 | [[uc-011-view-slot-monitoring-dashboard\|UC-011]]、[[uc-028-handle-workflow-step-exception\|UC-028]] | 告警发送失败不得清除原异常；不得在模板中填写任意收件地址、Webhook 或外部 API。 |
| `EXCEPTION_WAIT_HUMAN` 等待人工 | 是 | 否 | 异常、所需角色/权限、允许处置项、超时 | 授权处置决定、原因、操作人或超时 | [[uc-005-retrieve-mis-stored-product-from-slot\|UC-005]]、[[uc-006-cancel-transport-task-upon-arrival\|UC-006]]、[[uc-028-handle-workflow-step-exception\|UC-028]] | 只能执行开发预置处置项；身份、权限和原因必须审计。人工不得直接跳过强制安全步骤或改写模板快照。 |
| `EXCEPTION_TERMINATE` 异常结束 | 否 | 否 | 异常原因、最后安全状态、关联任务、补偿/隔离结果 | 流程 `ExceptionTerminated`、业务任务协调请求、审计摘要 | [[uc-006-cancel-transport-task-upon-arrival\|UC-006]]、[[uc-028-handle-workflow-step-exception\|UC-028]]、[[br-006-workflow-step-execution\|BR-006]] | 结束流程不等于业务任务自动完成/取消；必须先停止后续副作用、保持安全状态，并通过预置协调规则处理业务任务。 |

## 8. 步骤类型扩展与管理边界

只有开发人员通过受控的软件发布流程才能新增或修改步骤类型。扩展步骤类型至少必须完成：

1. 定义稳定且不可复用的步骤类型代码、参数 Schema、输入输出类型和版本兼容策略。
2. 定义幂等键、副作用边界、超时、可重试错误、不可重试错误和崩溃恢复方式。
3. 明确是否可跳过、是否可重试、是否属于强制安全步骤，并提供自动化测试和安全评审证据。
4. 定义只允许引用的预置接口适配器和配置项；外部凭据由安全配置管理，不进入模板。
5. 更新本目录版本并验证已有 `Published` 模板和历史快照仍可解释；不兼容变更必须使用新的步骤类型代码。

生产流程管理员、R-12、R-13 或其他管理员均不得：

- 编写或上传脚本、表达式代码、插件、程序集或可执行文件。
- 在模板中输入 SQL、命令行、任意 URL、HTTP 方法、请求头或请求体。
- 创建“通用 API 调用”“通用数据库操作”或“执行代码”等步骤。
- 修改预置步骤实现、绕过参数 Schema、提升重试上限至无限或取消强制安全标记。
- 通过手动模板匹配覆盖绕过上述限制。

发现未知步骤类型、目录版本不兼容、参数超出 Schema 或运行时适配器未注册时，模板发布和实例执行均必须 fail-closed。

## 9. Related Rules and Use Cases 关联规则与用例

- [[br-004-workflow-template-matching|BR-004]]：只匹配引用本目录有效步骤的已发布模板。
- [[br-005-workflow-template-versioning|BR-005]]：模板和实例快照记录步骤目录版本，历史不可物理删除。
- [[br-006-workflow-step-execution|BR-006]]：定义步骤顺序、跳过、重试、等待、幂等、审计和 fail-closed 语义。
- [[uc-025-maintain-workflow-template|UC-025]]：管理员从本目录选择和配置步骤，并在发布时校验步骤类型和安全约束。
- [[uc-026-select-template-and-create-workflow-instance|UC-026]]：负责匹配和快照实例化。
- [[uc-027-execute-workflow-steps|UC-027]]、[[uc-028-handle-workflow-step-exception|UC-028]]、[[uc-029-view-workflow-instance-progress|UC-029]]：分别负责受控执行、异常处置和进度查看。
