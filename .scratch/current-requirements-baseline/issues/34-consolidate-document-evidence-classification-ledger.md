# 合并并核验文档级证据分类账

Type: task
Status: resolved
Blocked by: 31, 32, 33

## Question

把 R01–R13 的三份分区文档级分类账合并为一个可机器复核的总账，并对照固定无损清单验证候选调查材料零遗漏、零重复、路径与哈希一致、分类枚举一致、批准证据不被夸大；总账应输出哪些汇总和候选分组，才能安全地生成后续原子需求级分类票据？

## Answer

已建立规范主数据 [R01–R13 文档级证据分类总账](../evidence/document-classification/R01-R13-document-evidence-ledger.tsv)、可直接驱动后续票据的 [R01–R13 候选分组](../evidence/document-classification/R01-R13-candidate-groups.tsv)、失败式[重建/核验脚本](../evidence/document-classification/build-and-verify-consolidated-ledger.ps1)，并提供含 `Summary`、`Candidate Groups` 和 `Ledger` 的 [XLSX 审阅副本](../../../outputs/019fc6c3-bdc0-77e3-9227-561dc20d7284/R01-R13-document-evidence-ledger.xlsx)。

总账逐字段保留三份分区账的 20 个规范字段，只追加可重建的 `route_class` 和 `candidate_group_id`。重建与独立 `-VerifyOnly` 均通过：R01–R13 共 490/490 行，记录 ID 与路径重复为 0，对固定清单遗漏为 0，路径/字节数/SHA-256/材料角色/批次差异为 0，当前文件哈希漂移为 0，19 条相关 Git 状态勘误全部正确叠加。批准四要素仍全部为 `not-found`，`document_approval_state` 全部为 `not-approved-by-this-classification`，任何分类过程中的批准升级都会使脚本失败。

提取路由只归并为三个安全处置：301 份 `candidate` 仅进入原子拆分、追证、去重、冲突裁决和显式批准；4 份 R06 上游漂移旧稿保持 `blocked`；185 份 `excluded` 保留身份与证据指针，但不从该文档自身提取需求。三类合计严格回对 490。

301 份候选按 R01–R13 实际批次形成 13 个后续组；每组已固定候选记录 ID、数量对账、前置门槛、拟建票据名称和处理边界。已为这 13 组分别建立“拆分并分类…的原子候选”任务票；R13 组另由“补齐 RIoT 目标环境与受控接口快照证据”、“决定 RIoT 项目 API 白名单与调用安全边界”、“补齐 standard.oasis.300ul 物模型枚举证据”和“决定未知物模型枚举值的项目处理规则”共同阻塞。另建“决定 R06 上游漂移旧稿的版本归属与去留”保持 4 份阻塞材料不被静默遗忘。

XLSX 审阅副本的汇总公式读回为 490/301/4/185、13 个候选组逐组对账全部为 `OK`、公式错误扫描为零；三张工作表均已完成渲染与视觉检查。本票没有改变业务领域词汇或决定，因此不修改根 `CONTEXT.md`。
