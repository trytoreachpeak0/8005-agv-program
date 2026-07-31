---
id: FR-021
type: functional-requirement
title: "Slot-to-IO Point Mapping Create/Modify Validation 仓位—IO点位映射创建/修改校验"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-14
updated: 2026-07-14
related_uc: ["UC-039"]
related_br: []
related_fr: ["FR-020"]
related_nfr: ["NFR-002"]
related_tc: ["TC-061", "TC-062", "TC-063"]
aliases: ["FR-021"]
---

# FR-021 Slot-to-IO Point Mapping Create/Modify Validation 仓位—IO点位映射创建/修改校验

## Description 需求描述

系统应当在操作人员为目标仓位实例录入或修改车载 IO 点位映射（开锁 DO、锁状态 DI、光幕 DI）并确认保存时，校验同一 IO 模块的同一通道号是否已被重复占用，以及必填点位是否均已填写。现场没有独立门状态 DI，不得把锁状态 DI 和门状态 DI 配置成两个点位。校验通过后，候选配置进入待核对状态；只有车辆处于配置维护态、整车无货并完成实际 IO 验证后才可原子激活。

## Rationale 制定原因

补齐 [[uc-018-io-point-mapping-verification-test|UC-018]] Assumption 中明确指出的需求缺口——"仓位—DO/DI 点位映射表是系统中已存在的一份配置数据，不负责该配置最初如何生成/录入"，为设备安装、新接入 AGV 等场景下首次录入映射提供有据可依的创建/修改能力，并在保存前拦截明显的配置错误（通道冲突、必填缺失），减少后续 [[fr-020-bidirectional-io-point-mapping-verification|FR-020]] 核对不通过的概率。

## Origin 需求来源

- [[uc-039-maintain-slot-io-point-mapping|UC-039]] Normal Flow 第 1~6 步、Postcondition、Exception Flow E3.1、E3.2

## Acceptance Criteria 验收标准

- **AC-1（校验通过，保存为待核对状态）**
  - **Given** 操作人员已为目标仓位实例录入或修改点位信息（开锁 DO、锁状态 DI、光幕 DI）
  - **When** 系统校验通道号未被重复占用，且必填点位均已填写，操作人员确认保存
  - **Then** 系统将该仓位映射配置状态置为"待核对"，记录变更内容、操作人、时间戳

- **AC-2（通道重复占用，拒绝保存）**
  - **Given** 操作人员提交的配置中，某 IO 模块的某通道号已被本仓位其他点位类型或另一仓位占用
  - **When** 系统执行保存前校验
  - **Then** 系统拒绝保存，提示冲突的具体 IO 模块、通道号及已占用该通道的仓位/点位类型

- **AC-3（必填点位缺失，拒绝保存）**
  - **Given** 操作人员提交的配置中，开锁 DO 点位或锁状态 DI 点位未填写
  - **When** 系统执行保存前校验
  - **Then** 系统拒绝保存，提示缺失的具体点位类型

## Related 关联

- **Use Cases：** 支撑 [[uc-039-maintain-slot-io-point-mapping|UC-039]]；维护的仓位实例来源于 [[uc-038-maintain-agv-slot-model|UC-038]] 型号版本在 [[uc-019-register-agv-from-rcs|UC-019]] 接入时自动生成
- **Business Rules：** 无
- **Functional Requirements：** 保存后的配置需经 [[fr-020-bidirectional-io-point-mapping-verification|FR-020]] 双向核对确认正确性；核对不通过时需回到本 FR 修正配置
- **Non-Functional Requirements：** 配置变更记录须满足 [[nfr-002-audit-completeness-and-retention|NFR-002]]

## Verification 验证方式

- [[TC-061|TC-061]]：校验通过，保存为待核对状态
- [[TC-062|TC-062]]：通道重复占用，拒绝保存
- [[TC-063|TC-063]]：必填点位缺失，拒绝保存

## Notes 备注

- 本 FR 不校验录入的点位标识在 IO 模块侧是否真实存在、是否与实际物理位置一致——该正确性由 [[fr-020-bidirectional-io-point-mapping-verification|FR-020]] 的双向核对来验证，本 FR 只做格式/唯一性等静态校验（见 UC-039 Assumption 第 2 条）。
- 批量导入多个仓位映射配置（UC-039 Alternative Flow A2.1）是否支持、具体文件格式仍为 TBD，本 FR 暂不单独拆 AC 覆盖，待后续与用户确认后补充。
- 仓位在"待核对"状态下能否被业务流程正常分配使用，本 FR 暂按"保存但不强制阻断业务分配"描述，具体是否需要强制阻断待与用户确认（见 UC-039 Notes 待补充事项第 1 条）。
