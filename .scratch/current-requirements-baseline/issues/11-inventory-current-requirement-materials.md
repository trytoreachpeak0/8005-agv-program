# 建立当前需求性材料的无损清单

Type: task
Status: resolved
Blocked by: 10

## Question

基于初始证据快照，如何无损列出当前工作目录中所有可能表达需求、约束、验收标准或业务决定的材料，并把代码、测试、配置和日志仅标为现状证据，从而得到后续可按单次会话规模切分的调查批次？

## Answer

已基于固定的初始证据快照建立当前需求性材料的无损路由清单；生成过程只读取快照，没有重新扫描工作区或覆盖任何原始材料身份：

- 快照与清单均为 1,809 条；逐路径复核为零重复、零漏项、零未分类，且原有 `git_status`、`sha256`、`bytes`、`last_write_utc` 零差异。
- 角色口径共记录 476 条需求/验收/决定/来源/外部约束/词汇/模板索引候选，1,260 条 `current-state-evidence`，以及 73 条 `repository-governance`。候选只表示需要调查，不表示真实、当前、适用、无冲突或已批准。
- 代码/实现、测试与实验、配置、日志、样本、接口转储和运行结果全部只标为现状证据；其中 14 条 RIoT OpenAPI/配置快照随外部接口调查批次提供支持，其余现状证据进入 E01–E05 按需引用批次，不单独升级为需求调查票。
- 候选材料按来源群组与单次会话规模形成 R01–R13 共 13 个调查批次，并已各自建立后续 research 票。每批必须逐份核实来源身份、时间、版本/历史、具名批准证据、批准范围、当前适用性、重复/派生关系及缺失证据；不得整批批准。
- 调查只产生文档级证据分类和后续原子条目指针。真实冲突仍须逐项建立 HITL grilling 票，最终基线仍只能收录经最终批准的原子需求。

Assets:

- [材料路由清单](../evidence/material-inventory/material-inventory.tsv) — SHA-256 `a26f4dd4405b962b3a087e8b42e912791d2fea7f388ffe54979504ce751d3bf7`
- [批次口径、数量与调查约束](../evidence/material-inventory/batches.md) — SHA-256 `7501376ec5156a1a171b8c5cda485b039a2e9b3c7d6a7970b24f6a042dfcda56`
- [可重复生成与对账脚本](../evidence/material-inventory/build-inventory.ps1)
