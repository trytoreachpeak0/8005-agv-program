# `v1.0.0` 规范需求候选总账

本目录是首版当前需求基线的**候选形成层**，不是已批准基线，也不是正式发布文件。`REQ-NNNN` 仅为候选永久身份预留；只有下一张最终批准票把候选的精确规范文本、范围、验证方法和批次文件身份绑定给最终批准人后，预留身份才可进入正式 `v1.0.0`。

## 规范产物

- `v1-canonical-requirement-candidates.tsv`：348 条当前规范候选。每条保存唯一规范文本、候选 `REQ`、适用范围、来源层、精确定位、原文、blob/SHA-256、来源权威、形成方式、首版前替代关系、旧候选指针、冲突处置、验证方法和最终批准缺口。
- `v1-legacy-source-disposition.tsv`：R01–R13 的 12,452 条旧原子声明逐行去留账。原文身份和原批准状态不变；363 条可以追到已解决决定的当前候选来源，3,172 条只作证据，2,399 条排除或超出范围，6,518 条仍为未批准且不得提升。
- `v1-canonical-requirement-candidates-summary.json`：计数、来源层分布、两个 TSV 的 SHA-256 和硬门禁结果。
- `build_and_verify_v1_candidate_ledger.py`：确定性重建与失败式核验入口。

## 形成规则

1. 四份在票据《决定首版基线如何处理初始快照后的替代性需求》中绑定精确身份的规格，按 `L1` 基础层及 `L2`–`L4` 局部后置层读取。生成前逐份重算 SHA-256；任一漂移立即失败。
2. 规格中的 `Implementation Decisions` 是候选规范文本层；`Solution`、`User Stories`、`Testing Decisions`、实现/视觉证据和 `Out of Scope` 仍留在原来源中，不再分配第二个候选身份。这样避免同一义务同时从 user story 和最终实现决定获得两个 `REQ`。
3. 产品/领域 HITL 决定以其 `Answer` 中的决定单元进入 `L5`。治理方法、证据快照、历史分类和发布流程票不混入产品需求。
4. 只在规范文本与适用范围完全相同时自动折叠；不做语义自动合并。后置来源的覆盖范围采用 PreBaselineSourceSupersession 明示，不凭时间或相似度推断替代。
5. R01–R13 旧声明绝不直接取得 `REQ`。能由冲突/问题复核账精确追到决定票的行只建立来源指针；其余保持证据、排除或未批准状态，不因当前候选形成而升级。
6. 四份规格获批的是“作为候选来源的精确文件身份”，既有 HITL 获批的是决定内容；两者都不替代首版对每条最终规范文本、范围和验证方法的最终批准。

## 复核

从仓库根目录运行：

```powershell
& '<bundled-python>' '.scratch\current-requirements-baseline\evidence\v1-canonical-candidates\build_and_verify_v1_candidate_ledger.py' --verify-only
```

核验要求：348 个候选身份连续且唯一、规范文本哈希逐条匹配、四份批准来源漂移为 0、12,452 条旧声明零遗漏零重复、旧声明批准升级为 0、所有候选均保持 `candidate-awaiting-final-item-approval`。
