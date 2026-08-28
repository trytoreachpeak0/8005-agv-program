---
id: FR-026
type: functional-requirement
title: "Atomic AGV Record Creation, Slot Instance Generation and Audit Logging AGV 档案原子创建、仓位实例生成与审计"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-019"]
related_br: ["BR-002", "BR-008"]
related_fr: ["FR-025"]
related_nfr: ["NFR-002"]
related_tc: ["TC-080", "TC-081"]
aliases: ["FR-026"]
---

# FR-026 Atomic AGV Record Creation, Slot Instance Generation and Audit Logging AGV 档案原子创建、仓位实例生成与审计

## Description 需求描述

系统应当在 [[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] 校验通过后，以同一事务完成：创建唯一的本地 AGV 档案并保存 RCS/RIOT 车辆 ID 映射；保存本地名称、车型、服务区域、最低接单电量、调度权重、维护备注，以及绑定的多仓位 AGV 模型型号、版本号和内容校验值快照；按该快照自动生成对应的仓位实例记录（仓位编号、所属面、位置、规格）；将新 AGV 状态置为"已禁用"；记录本次接入操作及配置内容到审计日志。若无法从 RCS/RIOT 取得完整车辆列表，系统不允许凭空手工创建 RCS 车辆 ID，必须提示接口异常并记录日志。

## Rationale 制定原因

接入操作会同时产生"AGV 档案""模型版本快照绑定""仓位实例记录"三份相互关联的数据，若不以同一事务完成，可能出现"AGV 档案已建但仓位实例缺失"这类无法通过正常业务修复的中间状态（呼应 [[br-008-agv-slot-model-versioning|BR-008]] Fail-closed 规则）。新 AGV 默认"已禁用"是为了避免配置或现场检查尚未完成的车辆立即参与自动任务分配（[[uc-013-enable-disable-agv|UC-013]] 需另行手动启用）。

## Origin 需求来源

- [[uc-019-register-agv-from-rcs|UC-019]] Normal Flow 第 8~10 步、Postcondition、异常流程"查询失败"
- [[br-008-agv-slot-model-versioning|BR-008]] 第 3 条、Fail-closed 规则

## Acceptance Criteria 验收标准

- **AC-1（校验通过，原子创建档案、绑定快照、生成仓位实例并记录审计）**
  - **Given** [[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] 的全部校验均已通过，管理员已确认保存
  - **When** 系统执行接入事务
  - **Then** 系统在同一事务中创建本地 AGV 档案（含 RCS/RIOT 车辆 ID 映射、本地配置、绑定的模型型号/版本号/内容校验值快照）、按快照生成对应仓位实例记录、将 AGV 置为"已禁用"，并记录审计日志；管理员被提示完成检查后可通过 [[uc-013-enable-disable-agv|UC-013]] 启用车辆

- **AC-2（RCS/RIOT 车辆列表查询失败，不允许凭空创建）**
  - **Given** 管理员正在接入流程中
  - **When** 系统无法取得完整的 RCS/RIOT 车辆列表
  - **Then** 系统不允许凭空手工创建 RCS 车辆 ID，提示接口异常并记录日志

## Related 关联

- **Use Cases：** 支撑 [[uc-019-register-agv-from-rcs|UC-019]] 保存/创建环节；生成的仓位实例是 [[uc-014-enable-disable-slot|UC-014]]、[[uc-018-io-point-mapping-verification-test|UC-018]]、[[uc-039-maintain-slot-io-point-mapping|UC-039]] 后续操作的对象
- **Business Rules：** 落实 [[br-008-agv-slot-model-versioning|BR-008]] 第 3 条（快照绑定与仓位实例生成）及其 Fail-closed 规则（接入事务失败必须整体回滚）；创建结果影响 [[br-002-agv-allocation-eligibility|BR-002]] 第 9 条依赖的仓位数据来源
- **Functional Requirements：** 依赖 [[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] 完成的前置校验
- **Non-Functional Requirements：** 接入操作及配置内容须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]（[[uc-019-register-agv-from-rcs|UC-019]] Postcondition 5 明确要求审计）

## Verification 验证方式

- [[tc-080-registration-atomic-creation-success|TC-080]]：校验通过，原子创建档案、绑定快照、生成仓位实例并记录审计
- [[tc-081-registration-rcs-query-fail-reject|TC-081]]：RCS/RIOT 车辆列表查询失败，不允许凭空创建

## Notes 备注

- 本 FR 不覆盖"接入事务中若仓位实例生成失败如何回滚"这一实现细节的独立 AC——[[br-008-agv-slot-model-versioning|BR-008]] Fail-closed 规则已明确"整次接入必须回滚，不得产生中间状态"，AC-1 的"同一事务"表述已隐含该约束，暂不单独拆分失败回滚场景的 AC，待后续如需要单独验收再补充。
- 车型（AGV 底座）与本 FR 绑定的多仓位模型是两个独立概念，本 FR 不做二者的一致性校验（该校验不适用，见 [[fr-025-agv-registration-eligibility-and-slot-model-version-validation|FR-025]] Notes）。
