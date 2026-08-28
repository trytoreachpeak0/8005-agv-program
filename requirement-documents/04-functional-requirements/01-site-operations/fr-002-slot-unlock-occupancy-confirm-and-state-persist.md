---
id: FR-002
type: functional-requirement
title: "Slot Unlock, Occupancy Confirm and State Persist 目标仓位开锁、占位确认与状态落库"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-31
related_uc: ["UC-001", "UC-004", "UC-014"]
related_br: ["BR-013"]
related_fr: ["FR-001"]
related_nfr: ["NFR-001", "NFR-002"]
related_tc: ["TC-113", "TC-114", "TC-115", "TC-116", "TC-117", "TC-118", "TC-120", "TC-122", "TC-123"]
aliases: ["FR-002"]
---

# FR-002 Slot Unlock, Occupancy Confirm and State Persist 目标仓位开锁、占位确认与状态落库

## Description 需求描述

系统应当在子批号核验通过后，用 `SUBLOT_BOX_COUNT`、冻结 `PACKAGE` 和批准的容量对照计算并冻结不可修改的 `ExpectedBasketCount`。计算失败时不分配仓位、不开锁；成功时一次分配数量相等的完整空闲仓位集合（排除已通过 [[uc-014-enable-disable-slot|UC-014]] 禁用的仓位），通过移动安全联锁后一次发起完整集合的批量开锁。操作员关门后，系统依据光幕检测确认仓位内确有产品，将仓位状态由空闲更新为已占用、记录仓位与子批号对应关系，并持久化本次装载操作追溯信息。花篮没有实体身份，系统不得根据装入顺序生成花篮序号。开锁失败、空闲状态与实物不符、或关门后光幕未检测到产品时，系统必须按约定拒绝继续或转入异常锁定/重试，不得静默记为装载成功。

## Rationale 制定原因

将 [[uc-001-load-completed-lot-into-slot|UC-001]] 中“开仓—放料—关门—占位确认—落库”的系统侧能力收敛为可验收切片，保证装载结果与现场实物、追溯数据一致，并为 LoadBatch 自动提交与存错取出（UC-005）提供正确的逐仓事实。

## Origin 需求来源

- [[uc-001-load-completed-lot-into-slot|UC-001]] Normal Flow 第 1.3～4 步及 Exception Flow E1.3、E1.4、E2.1、E2.2、E4.1；后置条件中的仓位状态与装载记录
- [[uc-004-slot-door-safety-interlock|UC-004]] Flow A（开锁前移动核验）
- [[uc-014-enable-disable-slot|UC-014]]（禁用仓位不参与分配）
- [[br-013-multi-basket-loading|BR-013]]（同一 SUBLOT 多花篮时的任务与仓位占用关系）

## Acceptance Criteria 验收标准

- **AC-0（权威花篮数量）**
  - **Given** [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]] 核验已通过
  - **When** 系统查询 `MAX_BOX_COUNT` 并用冻结 `PACKAGE` 匹配容量
  - **Then** 成功时冻结不可修改的 `ExpectedBasketCount = ceil(MAX_BOX_COUNT / capacity)`；查询或换算失败时显示可诊断错误，不分配仓位、不下发开锁

- **AC-1（完整空闲仓位分配）**
  - **Given** `ExpectedBasketCount` 已冻结，且存在足量空闲仓位（已排除禁用仓位）
  - **When** 系统为该子批号分配目标仓位
  - **Then** 一次分配数量等于 `ExpectedBasketCount` 的完整集合；仅从未禁用且状态为空闲的仓位中分配

- **AC-2（空闲仓位不足）**
  - **Given** 可用空闲仓位数量少于 `ExpectedBasketCount`
  - **When** 系统尝试分配仓位
  - **Then** 系统提示空闲仓位不足，不分配仓位、不下发开锁

- **AC-3（开锁前移动联锁）**
  - **Given** 已确定目标仓位，且按 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A 判定 AGV 当前处于移动状态
  - **When** 系统准备下发开锁指令
  - **Then** 系统拒绝本次开门/开锁，不得下发开锁指令

- **AC-4（批量开锁成功与开门核验）**
  - **Given** AGV 未在移动，完整目标仓位集合可开锁
  - **When** 系统一次发起完整集合的批量开锁，并逐仓核验开门反馈
  - **Then** 全部目标仓位在规定时间内正常打开时，系统允许操作员按任意顺序放料；若某仓位发生开锁、机构、通信或锁 DI 等关键反馈故障，则保留原目标集合、预留和逐仓事实，停止尚未发送以及任何新增开锁，禁止替换仓位和车辆离站，等待人工处置

- **AC-4.1（硬件故障不自动清空）**
  - **Given** 批量装货中某目标仓位发生硬件或关键反馈故障，且其它目标仓位可能已经放入花篮
  - **When** 系统进入故障等待状态
  - **Then** 不得自动打开已装仓位或要求清空该 SUBLOT；只有取得 R-09 或等效生产管理权限作出的 LoadCompensationDecision 且服务端授权后，才允许进入 LoadCompensationRecovery

- **AC-4.2（硬件恢复必须人工确认）**
  - **Given** 原故障仓位的通信、锁 DI、光幕和开锁输出回读等相关实时状态已经恢复有效且可唯一解释
  - **When** 尚未取得人工硬件恢复确认
  - **Then** 系统仍保持 VehicleRecoveryRequired，不得自行恢复；取得由 R-11 或被显式授予等效维护权限的人员以个人身份提交的 HardwareRecoveryConfirmation 后，仍须由服务端明确授权，才可在原目标仓位、原 LoadBatch、原 SlotOperationAttemptId 上继续；系统审计确认人、时间、车辆、仓位和故障原因

- **AC-4.3（无维护权限者不得确认硬件恢复）**
  - **Given** 车辆因关键硬件反馈故障处于 VehicleRecoveryRequired，当前登录人只有普通生产操作权限
  - **When** 当前登录人尝试提交 HardwareRecoveryConfirmation
  - **Then** 系统拒绝提交并保持 VehicleRecoveryRequired，不得开锁、续行或生成有效恢复确认

- **AC-4.4（班组长决定整批清空）**
  - **Given** LoadBatch 因关键硬件故障处于 VehicleRecoveryRequired，R-09 或被显式授予等效生产管理权限的人员已登录
  - **When** 该人员在提交前完成即时二次认证、选择有效受控原因码并可选填写备注，再以个人身份作出 LoadCompensationDecision
  - **Then** 服务端可将原 SlotOperationAttemptId 置为 LoadCompensationRequired，但不得因此自动开锁；仍须等待操作员发起并由服务端授权 LoadCompensationRecovery

- **AC-4.5（设备确认与清空决定权限分离）**
  - **Given** LoadBatch 因关键硬件故障处于 VehicleRecoveryRequired
  - **When** 仅有 R-11 维护权限或仅有普通生产操作权限的人员尝试作出 LoadCompensationDecision
  - **Then** 系统拒绝该决定并保持原业务目标；同一人只有同时具备 R-11 与 R-09 两项独立权限时，才可分别提交 HardwareRecoveryConfirmation 和 LoadCompensationDecision

- **AC-4.6（整批清空决定必须二次认证）**
  - **Given** 当前登录人具有 R-09 或等效生产管理权限，但尚未为本次 LoadCompensationDecision 完成有效的即时二次认证
  - **When** 当前登录人尝试提交该决定，或二次认证失败、已经失效、无法可靠记录
  - **Then** 系统拒绝提交，不生成 LoadCompensationDecision，不进入 LoadCompensationRequired，并保持 VehicleRecoveryRequired

- **AC-4.6.1（二次认证证据单次使用并强绑定）**
  - **Given** 已形成绑定确认人、DemandId、SlotOperationAttemptId 和决定内容的 LoadCompensationDecisionAuthProof
  - **When** 提交决定、重发同一消息，或尝试将证据用于不同任务、不同尝试、不同决定内容及业务校验失败后的新提交
  - **Then** 首次提交消费证据并可靠记录接受或拒绝结果；只有相同 MessageId 与相同内容的重发返回已有结果，其它使用均被拒绝并要求重新认证

- **AC-4.7（整批清空决定必须有受控原因码）**
  - **Given** R-09 或等效生产管理权限已通过本次二次认证
  - **When** 提交 LoadCompensationDecision
  - **Then** 原因码只能为 `HARDWARE_NOT_RECOVERABLE_ON_SITE`、`PRODUCTION_ABORTS_CURRENT_LOAD` 或 `OTHER`；空或未知原因码必须拒绝，前两项备注可空，`OTHER` 备注为空必须拒绝

- **AC-4.8（装货补偿清空后统一取消搬运需求）**
  - **Given** 已取得任一有效 LoadCompensationReasonCode 的 LoadCompensationDecision
  - **When** 原 SlotOperationAttemptId 完成 LoadCompensationRecovery
  - **Then** 原尝试终结为 `COMPENSATED` 并释放整批仓位预留，原 DemandId 终结为 `CANCELLED_BY_LOAD_COMPENSATION` 并形成持久化取消抑制，不再自动改派；三种原因码的业务后果一致，且不得误记为 `CANCELLED_BY_OPERATOR`

- **AC-5（关门后占位确认成功）**
  - **Given** 目标仓位仓门已关闭，光幕检测到仓位内有产品
  - **When** 系统执行关门后核验与落库
  - **Then** 记录该仓位的 OCCUPIED、锁闭、开锁输出复位、仓位与子批号映射及装载审计；尚有目标仓位未完成时保持 ProvisionalLoadState，全部目标仓位均完成且安全有效时自动整体提交 LoadBatch

- **AC-6（关门后光幕未检测到产品）**
  - **Given** 操作员已关闭仓门，但光幕未检测到产品
  - **When** 系统执行关门后核验
  - **Then** 系统不得将本次记为装载成功，自动再次输出开锁脉冲弹开仓门并提示补放；每次锁闭后重复核验，直至 OCCUPIED 才允许按 AC-5 落库，不设强制放行次数上限；UNKNOWN 或机构状态无效时暂停恢复

## Related 关联

- **Use Cases：** 支撑 [[uc-001-load-completed-lot-into-slot|UC-001]]；开锁前依赖 [[uc-004-slot-door-safety-interlock|UC-004]]；分配时排除 [[uc-014-enable-disable-slot|UC-014]] 禁用仓位；存错取出由 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 处理
- **Business Rules：** 多花篮的任务与仓位占用关系遵循 [[br-013-multi-basket-loading|BR-013]]
- **Functional Requirements：** 前置核验依赖 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]]
- **Non-Functional Requirements：** 开锁与落库能力依赖 [[nfr-001-service-availability|NFR-001]] 约束的业务服务可用性；开锁、异常锁定、占位落库等关键操作须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

对应 Test Case 待建。至少应覆盖：权威数量计算成功、各类查询/换算失败均不开锁、数量不可修改、目标仓位数严格相等、批量开锁与逐仓落库、仓位不足、移动中拒绝开锁、批量开锁部分失败、关门无产品拒绝成功落库。验证策略：功能测试 + 与 IO/光幕联调（可用模拟器）。

## Notes 备注

- 本 FR 描述的是**主业务系统**能力：经 IO 模块驱动电子锁并采集光幕；不直接连接电子锁/光幕硬件（见 [[vision-and-scope|愿景与范围]] 限制条款）。
- “打开后实物与系统空闲不一致”（UC-001 E2.2）要求异常锁定并暂停分配；具体解除锁定的维护流程可另拆 FR/UC，本 FR 要求至少具备标记异常锁定且不得继续向该仓位装载的行为。
- 仓门开启超时告警（UC-001 E3.1）的升级策略仍有 TBD，本 FR 黄金样例暂不把“超时后强制升级”列为必须 AC。
- `related_tc` 已包含 LoadBatch 自动提交、硬件故障保持、授权维护人员确认后恢复、普通生产操作员越权确认被拒绝，以及 R-09 整批清空决定、兼任权限边界、缺少有效二次认证和缺少有效原因码时拒绝提交的覆盖用例。
