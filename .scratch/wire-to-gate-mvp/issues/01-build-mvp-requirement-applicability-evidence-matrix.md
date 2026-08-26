# 建立 MVP 需求适用性证据矩阵

Type: task
Status: resolved
Blocked by:

## Question

如何在不修改 `current-requirements-v1.0.0.md` 的前提下，把 `REQ-0001`～`REQ-0348` 逐条路由为「MVP 直接必须」、「MVP 交互／安全依赖」、「首期延后」或「本场景不适用」，并为每条保留原始需求 ID、分类理由、依赖链、风险、对 ControlServer／OnboardHmi／共享协议的影响及待 HITL 决策指针？

本票只建立零遗漏、可复核的事实矩阵和候选分类，不代替用户批准 MVP 精确适用清单，不把延后项标记为 deprecated。

## Evidence

- [`requirements/baselines/current-requirements-v1.0.0.md`](../../../requirements/baselines/current-requirements-v1.0.0.md)
- [`requirements/current-baseline.md`](../../../requirements/current-baseline.md)
- [决定基线版本的存储与变更治理形式](../../current-requirements-baseline/issues/09-baseline-release-storage-and-change-governance.md)

## Answer

已在不修改需求基线和当前指针的前提下，建立逐条可复核的候选适用性证据矩阵：

- [矩阵摘要与阅读规则](../evidence/requirement-applicability-matrix-summary.md)
- [348 条完整 TSV 矩阵](../evidence/requirement-applicability-matrix.tsv)
- [可重复生成与完整性校验脚本](../evidence/build-requirement-applicability-matrix.ps1)

矩阵固定绑定 `current-requirements-v1.0.0.md` 的 SHA-256 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`，覆盖 `REQ-0001`～`REQ-0348` 共 348 条，零重复、零遗漏。每行保留原始 ID、源链接、标题、原始 Scope、候选分类、分类理由、依赖链、误分风险、ControlServer／OnboardHmi／共享协议影响和待 HITL 决策指针。

候选路由结果为：

- `MVP 直接必须`：83 条；
- `MVP 交互／安全依赖`：90 条；
- `首期延后`：46 条；
- `本场景不适用`：129 条。

这些数量和逐条结论都只是证据路由，不是最终产品批准，也不改变任何原条目的 Lifecycle。`REQ-0189`、`REQ-0194`、`REQ-0205`、`REQ-0212`～`REQ-0220` 和 `REQ-0328` 等包含“整条范围外但小条款可能保留”或“原多车语义需收窄为单车门禁”的项目，已在摘要和对应行中显式标旗，并分别路由到“决定单 Demand 选择、并发与等待策略”“决定机台取货、多仓装货、关卡卸货与成功边界”等既有票据；没有发现必须新增、且现有决策票无法承接的独立问题。

生成脚本会在产出前验证当前指针、基线哈希、348 个规范块、每个 ID 恰好一个候选分类以及连续唯一的 ID 集合。最后一次生成的矩阵 SHA-256 为 `ea573a59f76f87e2637a72e7e0781bf2a08c0befa5651ac19ff40d0501d229d2`。
