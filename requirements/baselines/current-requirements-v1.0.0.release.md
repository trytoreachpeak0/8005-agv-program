# 当前需求基线 `v1.0.0` 发布记录

## 发布身份

- Baseline Version: `v1.0.0`
- Versioned Requirement File: `requirements/baselines/current-requirements-v1.0.0.md`
- File SHA-256: `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`
- Content Git Commit: `b9f321228b534a3b316d3ac1abede05176ed6a70`
- Annotated Git Tag: `requirements-baseline-v1.0.0`
- Previous Approved Version: `none`
- Released At: `2026-08-24T15:26:34Z`

## 版本批准记录

- Approver: 用户本人（本地图默认且唯一最终批准人）
- Approved At: `2026-08-24T15:16:06Z`
- Approved Scope: 8005 多仓位 AGV 项目的 `REQ-0001`–`REQ-0348`；每条更窄范围以版本文件中的 Scope 为准
- Approved Version Identity: `v1.0.0` + `requirements/baselines/current-requirements-v1.0.0.md` + SHA-256 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`
- Approval Evidence: [集中审批记录](../../.scratch/current-requirements-baseline/evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md)、[最终批准批次清单](../../.scratch/current-requirements-baseline/evidence/v1-final-approval-batches/v1-final-approval-batches.tsv)及每条需求所列批准票
- Authority Evidence: [确定当前基线的最终批准人](../../.scratch/current-requirements-baseline/issues/03-final-baseline-approver.md)
- Requirement Coverage: `REQ-0001`–`REQ-0348`，348 条，零重复、零遗漏
- Candidate Ledger SHA-256: `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`
- Approval Manifest SHA-256: `3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843`

## 变化依据

- Added: `REQ-0001`–`REQ-0348`；首个批准基线，无更早批准版本
- Modified: `None`
- Deprecated: `None`
- Version Classification Evidence: [决定基线版本的存储与变更治理形式](../../.scratch/current-requirements-baseline/issues/09-baseline-release-storage-and-change-governance.md)规定首个批准基线使用 `v1.0.0`

## 当前版本指针

- Pointer File: `requirements/current-baseline.md`
- Pointer Target: `requirements/baselines/current-requirements-v1.0.0.md`
- Pointer Verification: annotated tag `requirements-baseline-v1.0.0` 解析到包含本发布记录和唯一当前指针的 Git tree；Content Git Commit 可独立恢复精确版本文件

## 正式发布检查

- [x] 完整版本化需求文件存在，且内容 SHA-256 为 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`。
- [x] Content Git Commit `b9f321228b534a3b316d3ac1abede05176ed6a70` 可恢复该精确文件与路径。
- [x] annotated tag `requirements-baseline-v1.0.0` 由发布流程创建并指向包含本发布记录的发布 commit。
- [x] 批准记录绑定最终批准人、时间、范围、精确文件 SHA-256 和可核查证据。
- [x] 95 张最终批准票覆盖 348 条需求，均为 `resolved` 且各有一个当前 Answer。
- [x] 版本号与首个批准基线的实际性质一致。
- [x] `requirements/current-baseline.md` 只指向本版本。
- [x] 不存在需要保留的上一批准版本或发布记录。
