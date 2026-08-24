# 生成并发布首个当前需求基线 v1.0.0

Type: task
Status: open
Blocked by: 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183

## Question

在全部最终批准批次均已关闭且每个 `REQ-0001`～`REQ-0348` 都有明确、可核查的逐项结论后，如何生成可独立阅读的 `requirements/baselines/current-requirements-v1.0.0.md`，记录批准人与批准证据，核验完整版本文件及 SHA-256，并完成 Git commit、带说明 tag `requirements-baseline-v1.0.0` 和 `requirements/current-baseline.md` 唯一当前指针？

发布任务必须失败式核对批准批次清单与 payload 身份；任何拒绝、待修订、缺失批准或身份漂移都阻止发布。不得修改、合并、删除或静默改写原始需求材料。

## Evidence

- [最终批准批次清单](../evidence/v1-final-approval-batches/v1-final-approval-batches.tsv)
- [首版规范需求候选总账](../evidence/v1-canonical-candidates/v1-canonical-requirement-candidates.tsv)
- [决定基线版本的存储与变更治理形式](09-baseline-release-storage-and-change-governance.md)
