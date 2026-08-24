# 合并并语义去重 R01–R13 原子候选

Type: task
Status: resolved
Blocked by: 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54

## Question

在 R01–R13 各批原子候选及 R08 混合声明重新拆分完成后，如何把各批规范主数据归并为一个可机器重建和失败式核验的原子候选总账，统一字段与指针枚举、保留多来源证据和版本/适用范围隔离，并分别识别精确重复、规范化重复、语义近似、派生关系和仍可能真实冲突的候选簇；总账应输出哪些可复核的聚类、来源覆盖、冲突候选和批准批次建议，才能让需要业务判断的真实冲突毕业为独立 HITL 票而不在去重过程中合并、删除、批准或重写原始声明？

## Answer

已完成 R01–R13 跨批次合并与语义去重，规范主数据为 [R01–R13 合并原子候选总账](../evidence/atomic-candidates/R01-R13-consolidated-atomic-candidates.tsv)，配套产物包括 [语义关系账](../evidence/atomic-candidates/R01-R13-semantic-relations.tsv)、[语义审阅簇](../evidence/atomic-candidates/R01-R13-semantic-review-clusters.tsv)、[来源派生关系](../evidence/atomic-candidates/R01-R13-source-derivations.tsv)、[冲突复核账](../evidence/atomic-candidates/R01-R13-conflict-review.tsv)、[批准批次建议](../evidence/atomic-candidates/R01-R13-approval-batch-suggestions.tsv)、[可重建摘要](../evidence/atomic-candidates/R01-R13-consolidated-atomic-candidates-summary.json)和[重建/失败式核验脚本](../evidence/atomic-candidates/build_and_verify_consolidated_atomic_candidates.py)。另提供八张表的 [XLSX 审阅副本](../../../outputs/019fcb39-f5f0-7861-af1c-8a35895e8ae3/R01-R13-consolidated-atomic-candidates-review.xlsx)；XLSX 不是规范主数据。

- 13 个上游账本先分别独立运行 `--verify-only`，全部通过。合并后保持 12,452/12,452 条、301 个唯一来源身份（302 个批次—来源归属，`R04-17` 被 R04/R06 有意复用）、候选 ID 零重复、原字段逐值保留、批准升级为 0；每个输入 TSV 和本次用于规范词匹配的根 `CONTEXT.md` 都固定 SHA-256。
- 关系账包含 1,833 条：1,232 条完全相同、229 条规范化相同、372 条语义近似审阅关系，形成 1,065 个审阅簇并覆盖 2,732 条记录；另从原账声明中恢复 41 条来源/重叠关系。所有关系只要求共同审阅，命中不同版本/范围时强制保留隔离，绝不自动合并、删除、批准、重写声明或分配永久 `REQ-NNNN`。
- 审阅处置为：6,449 条仍未批准的批准候选、3,114 条证据、2,451 条不进入需求批准、197 条等待真实冲突决定、241 条等待问题解决或重新原子化。6,449 条批准候选已按领域和所需责任角色建议切成 102 批，每批最多 180 行或 120 个语义审阅单元；这些只是候选规范文本形成后的批准路线建议，不构成批准票或基线条目。
- 六个既有冲突指针逐项复核：`CF-R01-003` 的旧纯人工 AREA 映射与当前 BR-003/UC-024 已收敛为“地图同步 + 命名规则自动派生 + 少量显式覆盖”，因此只保留版本差异；`CF-R10-001` 属票据 50 已排除的模拟器技术复核，不进入本地图主系统需求决定。其余四组会改变业务结果且没有足以自动择一的版本/范围批准证据，已分别毕业为 [决定运输需求身份、对账键与取消抑制边界](56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md)、[决定当前 MES 只读与卸货、完工回写边界](57-decide-current-mes-readonly-and-completion-writeback-boundary.md)、[决定 QUEUEING 滞留与下单前清积压策略](58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md)和[决定充电失败改派的备用桩筛选与排队关系](59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md)四张 HITL grilling 票；本票没有替用户回答。
- 合并脚本生成后立即自核验，独立 `--verify-only` 再次通过。XLSX 的 Summary 公式读回为 12,452 条、301 个唯一来源、1,833 条关系、1,065 个簇、6,449 条未批准候选、102 个建议批次、4 个毕业冲突、0 个批准升级；13 个批次全部 `OK`，公式错误扫描为零，八张工作表均完成渲染检查，最终 XLSX ZIP 完整性检查无损坏且含八张 worksheet。
- 本票没有批准新的领域词汇，因此 `domain-modeling` 检查后不修改根 `CONTEXT.md`；其规范词只用于提高匹配质量，不能从词汇文件反向赋予候选权威性。
