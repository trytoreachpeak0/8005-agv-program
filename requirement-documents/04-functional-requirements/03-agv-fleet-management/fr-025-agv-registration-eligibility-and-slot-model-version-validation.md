---
id: FR-025
type: functional-requirement
title: "AGV Registration Eligibility and Slot Model Version Validation AGV 接入资格与模型版本校验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-019"]
related_br: ["BR-002", "BR-008"]
related_fr: ["FR-026"]
related_nfr: ["NFR-002"]
related_tc: ["TC-076", "TC-077", "TC-078", "TC-079"]
aliases: ["FR-025"]
---

# FR-025 AGV Registration Eligibility and Slot Model Version Validation AGV 接入资格与模型版本校验

## Description 需求描述

系统应当在管理员为一台从 RCS/RIOT 选中的未接入车辆填写本地配置、独立选择一个多仓位 AGV 模型的版本，并确认保存前，校验：所选模型版本确实处于 `Published` 状态；该 RCS/RIOT 车辆 ID 未存在于任何未归档或已归档的本地档案中；车型、服务区域、最低接单电量、调度权重等必填配置均已填写且取值合法，且已选择某个模型版本。以上任一校验不通过，系统必须拒绝保存并提示具体原因，不产生部分创建的档案；全部校验通过后，方可进入 [[fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging|FR-026]] 描述的原子创建环节。

## Rationale 制定原因

AGV 接入一旦成功即会绑定不可更换的模型版本快照（[[br-008-agv-slot-model-versioning|BR-008]] 第 3 条）并进入车队用于任务分配（[[br-002-agv-allocation-eligibility|BR-002]]），因此在真正落库前必须先把三类可预见的错误——选用了不可用的模型版本、车辆 ID 重复接入、必填配置缺失或不合法——挡在校验阶段，避免产生错误绑定后只能靠"归档重接"这一代价较高的路径来纠正。

## Origin 需求来源

- [[uc-019-register-agv-from-rcs|UC-019]] Normal Flow 第 5~7 步、Exception Flow E6.1、E7.1、E7.2

## Acceptance Criteria 验收标准

- **AC-1（模型版本、车辆 ID 与配置均校验通过，允许继续接入）**
  - **Given** 管理员已选择一台未接入的 RCS/RIOT 车辆，填写本地名称、车型、服务区域、最低接单电量、调度权重、维护备注，并独立选择某个多仓位 AGV 模型的一个版本
  - **When** 系统校验该模型版本处于 `Published` 状态、该车辆 ID 未被任何本地档案占用、必填配置均已填写且合法
  - **Then** 系统允许管理员确认保存，进入原子创建环节

- **AC-2（所选模型版本不可用，拒绝保存）**
  - **Given** 管理员选择的模型版本当前处于 `Draft` 或 `Retired` 状态
  - **When** 系统校验该版本是否为 `Published`
  - **Then** 系统拒绝保存，提示"该型号版本不可用于接入"，引导管理员改选其他 `Published` 版本或联系型号维护人员发布新版本

- **AC-3（车辆已接入，拒绝重复创建）**
  - **Given** 目标 RCS/RIOT 车辆 ID 已存在于本地未归档或已归档的档案中
  - **When** 系统校验车辆 ID 唯一性
  - **Then** 系统拒绝重复创建，并引导管理员查看现有档案

- **AC-4（配置不完整或不合法，拒绝保存）**
  - **Given** 必填配置缺失，或车型、电量阈值、调度权重等值不合法，或未选择任何模型版本
  - **When** 系统执行保存前校验
  - **Then** 系统拒绝保存并逐项提示修正

## Related 关联

- **Use Cases：** 支撑 [[uc-019-register-agv-from-rcs|UC-019]] 接入前校验环节；所选版本来自 [[uc-038-maintain-agv-slot-model|UC-038]] 发布的 `Published` 版本
- **Business Rules：** 落实 [[br-008-agv-slot-model-versioning|BR-008]] 第 3 条"必须从 `Published` 版本中选择"；校验通过是进入 [[br-002-agv-allocation-eligibility|BR-002]] 候选集合的前提之一
- **Functional Requirements：** 校验通过后由 [[fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging|FR-026]] 完成实际的原子创建
- **Non-Functional Requirements：** 接入操作须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]（[[uc-019-register-agv-from-rcs|UC-019]] Postcondition 5 明确要求审计）

## Verification 验证方式

- [[tc-076-registration-validation-pass|TC-076]]：模型版本、车辆 ID 与配置均校验通过，允许继续接入
- [[tc-077-registration-model-version-not-published-reject|TC-077]]：所选模型版本不可用，拒绝保存
- [[tc-078-registration-duplicate-vehicle-id-reject|TC-078]]：车辆已接入，拒绝重复创建
- [[tc-079-registration-incomplete-config-reject|TC-079]]：配置不完整或不合法，拒绝保存

## Notes 备注

- 车型与多仓位 AGV 模型是两个独立概念，本 FR 不对二者做联动或一致性校验（见 [[uc-019-register-agv-from-rcs|UC-019]] Assumption 第 2 条、Notes）。
- 已归档车辆是否允许恢复、恢复后是否沿用原档案仍为 TBD（见 UC-019 Exception Flow E7.1、Notes），本 FR 暂不覆盖该场景的正向 AC，只覆盖"拒绝重复创建"本身。
