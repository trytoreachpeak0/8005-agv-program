---
id: FR-002
type: functional-requirement
title: "Slot Unlock, Occupancy Confirm and State Persist 目标仓位开锁、占位确认与状态落库"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-001", "UC-004", "UC-014"]
related_br: ["BR-013"]
related_fr: ["FR-001"]
related_nfr: ["NFR-001", "NFR-002"]
related_tc: []
aliases: ["FR-002"]
---

# FR-002 Slot Unlock, Occupancy Confirm and State Persist 目标仓位开锁、占位确认与状态落库

## Description 需求描述

系统应当在子批号核验通过后，为装载需求分配空闲仓位（排除已通过 [[uc-014-enable-disable-slot|UC-014]] 禁用的仓位），在通过移动安全联锁核验后向 IO 模块下发目标仓位开锁指令；并在操作员关门后，依据光幕检测确认仓位内确有产品，将仓位状态由空闲更新为已占用、记录仓位与子批号（及花篮序号，如适用）对应关系，并持久化本次装载操作追溯信息。开锁失败、空闲状态与实物不符、或关门后光幕未检测到产品时，系统必须按约定拒绝继续或转入异常锁定/重试，不得静默记为装载成功。

## Rationale 制定原因

将 [[uc-001-load-completed-lot-into-slot|UC-001]] 中“开仓—放料—关门—占位确认—落库”的系统侧能力收敛为可验收切片，保证装载结果与现场实物、追溯数据一致，并为后续确认完成（UC-002）与存错取出（UC-005）提供正确的仓位状态基础。

## Origin 需求来源

- [[uc-001-load-completed-lot-into-slot|UC-001]] Normal Flow 第 1.3、2～4 步及 Exception Flow E1.3、E2.1、E2.2、E4.1；后置条件中的仓位状态与装载记录
- [[uc-004-slot-door-safety-interlock|UC-004]] Flow A（开锁前移动核验）
- [[uc-014-enable-disable-slot|UC-014]]（禁用仓位不参与分配）
- [[br-013-multi-basket-loading|BR-013]]（同一 SUBLOT 多花篮时的装载明细键，如适用）

## Acceptance Criteria 验收标准

- **AC-1（空闲仓位分配）**
  - **Given** [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]] 核验已通过，且存在满足数量要求的空闲仓位（已排除禁用仓位）
  - **When** 系统为该子批号分配目标仓位
  - **Then** 仅从未禁用且状态为空闲的仓位中分配；禁用仓位不得被选中

- **AC-2（空闲仓位不足）**
  - **Given** 可用空闲仓位数量不满足装载需求
  - **When** 系统尝试分配仓位
  - **Then** 系统提示空闲仓位不足，不分配仓位、不下发开锁

- **AC-3（开锁前移动联锁）**
  - **Given** 已确定目标仓位，且按 [[uc-004-slot-door-safety-interlock|UC-004]] Flow A 判定 AGV 当前处于移动状态
  - **When** 系统准备下发开锁指令
  - **Then** 系统拒绝本次开门/开锁，不得下发开锁指令

- **AC-4（开锁成功与开门核验）**
  - **Given** AGV 未在移动，目标仓位可开锁
  - **When** 系统下发开锁指令且仓门在规定时间内正常打开
  - **Then** 系统允许操作员向该仓位放料；若规定时间内未打开，则提示开锁异常，将该仓位标记为异常锁定，并在存在其他空闲仓位时允许改分仓位（无其他空闲仓位则提示联系维护）

- **AC-5（关门后占位确认成功）**
  - **Given** 目标仓位仓门已关闭，光幕检测到仓位内有产品
  - **When** 系统执行关门后核验与落库
  - **Then** 仓位状态由空闲变为已占用；记录仓位与子批号对应关系；记录操作员、子批号、仓位号、时间戳等装载追溯信息；任务状态保持进行中（不因本 FR 自动变为完成）

- **AC-6（关门后光幕未检测到产品）**
  - **Given** 操作员已关闭仓门，但光幕未检测到产品
  - **When** 系统执行关门后核验
  - **Then** 系统不得将本次记为装载成功；提示装载异常并要求重新打开确认；直至光幕确认有产品后才允许按 AC-5 落库

## Related 关联

- **Use Cases：** 支撑 [[uc-001-load-completed-lot-into-slot|UC-001]]；开锁前依赖 [[uc-004-slot-door-safety-interlock|UC-004]]；分配时排除 [[uc-014-enable-disable-slot|UC-014]] 禁用仓位。任务最终完成不在本 FR（见 [[uc-002-confirm-task-completion|UC-002]]）；存错取出不在本 FR（见 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]）
- **Business Rules：** 多花篮装载明细键遵循 [[br-013-multi-basket-loading|BR-013]]（适用时）
- **Functional Requirements：** 前置核验依赖 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]]
- **Non-Functional Requirements：** 开锁与落库能力依赖 [[nfr-001-service-availability|NFR-001]] 约束的业务服务可用性；开锁、异常锁定、占位落库等关键操作须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

对应 Test Case 待建。建议覆盖：正常开锁与落库、仓位不足、移动中拒绝开锁、开锁超时异常锁定、关门无产品拒绝成功落库。验证策略：功能测试 + 与 IO/光幕联调（可用模拟器）。

## Notes 备注

- 本 FR 描述的是**主业务系统**能力：经 IO 模块驱动电子锁并采集光幕；不直接连接电子锁/光幕硬件（见 [[vision-and-scope|愿景与范围]] 限制条款）。
- “打开后实物与系统空闲不一致”（UC-001 E2.2）要求异常锁定并暂停分配；具体解除锁定的维护流程可另拆 FR/UC，本 FR 要求至少具备标记异常锁定且不得继续向该仓位装载的行为。
- 仓门开启超时告警（UC-001 E3.1）的升级策略仍有 TBD，本 FR 黄金样例暂不把“超时后强制升级”列为必须 AC。
- `related_tc` 暂空，待补录后回填。
