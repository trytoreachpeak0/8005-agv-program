# 建立首版规范需求候选与来源层叠总账

Type: task
Status: resolved
Blocked by: 86

## Question

如何把四份身份已核验的获批规格、MesIngestWatch V2 已确认的跨版本一致边界、补充快照中经决定保留的其它规范候选，以及 R01–R13 原子候选与全部已解决 HITL 决定，合并成可逐项最终批准的 `v1.0.0` 规范需求候选总账？

任务必须为每个最终有效义务形成单一规范文本和候选永久 `REQ-NNNN`，保存全部来源层、逐层精确差异、PreBaselineSourceSupersession、适用范围、冲突处置、验证方法与批准状态；被替代、纯实现、历史或未批准内容必须可追溯但不得作为当前候选混入。

## Evidence

- [固定并分类首版发布前补充证据快照](85-capture-and-classify-pre-release-supplemental-evidence-snapshot.md)
- [决定补充快照中未批准规范候选的首版去留](86-decide-supplemental-unapproved-normative-candidate-disposition.md)
- [合并并语义去重 R01–R13 原子候选](55-consolidate-and-semantically-deduplicate-r01-r13-atomic-candidates.md)
- [复核冲突决定后仍待问题解决或重构的 241 条记录](63-review-post-conflict-unresolved-question-and-reframing-records.md)

## Answer

已建立可机器重建、失败式核验且等待逐项最终批准的 `v1.0.0` 规范需求候选总账。总账形成 **348 条唯一当前候选**，预留连续且不复用的 `REQ-0001`～`REQ-0348`；这些编号在本阶段只是候选永久身份，全部条目仍为 `candidate-awaiting-final-item-approval`，不得在下一张最终批准票关闭前视为正式基线要求。

### 当前规范层

- 四份在《决定首版基线如何处理初始快照后的替代性需求》中绑定精确文件身份的规格，重建前逐份复核 SHA-256，漂移为 0。为避免同一义务从 User Story 与最终决定重复取得两个身份，只以各规格的 `Implementation Decisions` 形成当前规范文本：基础新版 MesIngest 52 条、有界存储 37 条、AREA 实时同步 26 条、Inspector E 30 条，共 145 条。
- 产品/领域 HITL 决定以其 `Answer` 中的决定单元形成 203 条候选；治理方法、证据快照、历史分类、实现/验收证据和发布流程不混入产品需求。
- 只在规范文本与适用范围完全相同时自动折叠；不凭语义相似度自动合并。每条候选保存规范文本及 SHA-256、范围、来源层、精确位置、原文、来源身份与权威、形成方式、AI 参与、逐层差异、PreBaselineSourceSupersession、决定/旧候选指针、冲突处置、验证方法和最终批准缺口。
- L2–L4 只在票据 84 声明的局部范围覆盖 L1；旧 Phase 1、旧 V2、旧数据库/契约/Watch/IngestAlert 语义不创建虚构的 deprecated REQ。MesIngestWatch V2 只通过已核对的跨版本一致边界进入当前层；MES_TASK_UNION README 按票据 86 只作支持证据。

### 旧来源无损去留

- R01–R13 的 12,452 条旧原子声明已逐行写入独立来源去留账，候选 ID、原文身份、批准状态和适用范围零遗漏、零重复、零改写。
- 363 条可沿既有冲突/问题复核指针追到当前决定来源；3,172 条只作证据；2,399 条保持排除或超出当前范围；6,518 条保持未批准且不提升。
- 旧声明批准升级为 0。无法由既有明确指针证明逐条血缘的材料只保留在来源去留账，不以相似度猜测或伪造与当前 `REQ` 的关系。

### 复核结果

重建后又以 `--verify-only` 独立运行失败式核验：348 个候选身份连续且唯一、348 个规范文本哈希全部有效、348 条全部等待最终批准；12,452 条旧来源唯一且完整；四份批准来源身份漂移为 0；旧来源批准升级为 0。此票只形成候选，不替用户批准任何条目，也不修改原始需求材料或产品代码。

### Assets

- [候选总账](../evidence/v1-canonical-candidates/v1-canonical-requirement-candidates.tsv) — 348 条，SHA-256 `9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646`
- [旧来源逐行去留账](../evidence/v1-canonical-candidates/v1-legacy-source-disposition.tsv) — 12,452 条，SHA-256 `f25943a5496c16a98205bc23a45e5b4aa4a64f32e72a8bacb290d2414029fb65`
- [可重建摘要](../evidence/v1-canonical-candidates/v1-canonical-requirement-candidates-summary.json) — SHA-256 `edee2a7645625d713edb99f7bd3898227d3221bf66de4e09b745d6b42f193b3d`
- [形成与核验说明](../evidence/v1-canonical-candidates/README.md)
- [确定性重建/失败式核验脚本](../evidence/v1-canonical-candidates/build_and_verify_v1_candidate_ledger.py) — SHA-256 `236c37b184826746136920cec7ebf1097679600e3a70d5306858d488805b822b`

本票未形成新的领域词汇或改变既有词义，无需修改 `CONTEXT.md`。它解除《生成首版原子需求最终批准批次》的阻塞。
