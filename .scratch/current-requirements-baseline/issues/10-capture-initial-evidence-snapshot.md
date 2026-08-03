# 固定初始需求证据快照

Type: task
Status: resolved
Blocked by: 07

## Question

在不修改任何原始需求材料的前提下，记录盘点开始时的时间、分支、Git HEAD、工作区状态、候选文档路径、版本控制状态和内容哈希，形成可重复核验的初始证据快照。

## Answer

已于 2026-08-03 10:50:41–10:50:48（Asia/Taipei；UTC 02:50:41–02:50:48）完成初始需求证据快照：

- Git 基点为分支 `szy_document_dev`、HEAD `1469d6309d00b0abb792f6cd686aed68286e638e`、上游 `origin/szy_document_dev`。
- 以当前工作目录实际字节为准，共记录 1,809 个宽口径候选文档；其中 1,704 个为 `tracked-clean`、105 个为 `untracked`。候选身份不代表它是需求或具有权威性。
- 每个候选文件记录仓库相对路径、Git 状态、SHA-256、字节数和最后修改 UTC；独立复核结果为零重复、零缺失、零哈希差异。
- 原始工作区状态另行原样保存，其中包括用户既有的 5 个未提交 C# 文件修改；这些修改只作为工作区状态登记，未被本票修改或认定为正确需求。
- 依赖、构建产物、测试产物、IDE 与缓存目录默认排除。本地图新建的治理目录 `.scratch/current-requirements-baseline/` 也不作为待恢复需求候选，以避免自引用，但完整显示在工作区状态中。
- 文件发现无错误。以后发现当前候选策略之外的需求证据时，必须建立新快照，不得静默改写本次观察。

Assets:

- [快照说明与采集身份](../evidence/initial-snapshot/snapshot.md)
- [候选文档清单](../evidence/initial-snapshot/candidate-documents.tsv)
- [原始工作区状态](../evidence/initial-snapshot/worktree-status.txt)
- [可重复采集脚本](../evidence/initial-snapshot/capture.ps1)
- [文件发现错误记录](../evidence/initial-snapshot/discovery-errors.txt)
