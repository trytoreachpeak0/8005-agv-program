# 调查 MES 数据、查询与工厂验证约束

Type: research
Status: resolved
Blocked by: 11, 26

## Question

对无损清单 R11 批次中的 MES 业务入口、查询契约、参考数据和工厂验证清单，逐份核实来源、版本、具名批准证据、适用环境与当前项目范围；如何区分外部数据约束、验收条件、派生查询设计与只证明现状的实验/运行证据？

## Answer

完整调查见 [R11 MES 数据、查询与工厂验证约束调查](../evidence/investigations/R11-mes-data-query-validation-constraints.md)。固定清单中的 11/11 份材料均已核实且 SHA-256 零漂移；工厂首轮清单已应用 Git 状态勘误并恢复 7 月 16 日初版与 7 月 27 日六分支实测回填版历史。0/11 具备完整批准四要素。

客户 SQL 表/字段/筛选、28 条 PACKAGE 容量和限定工厂环境观察是外部数据约束候选；统一查询、失败语义和 exact/prefix 匹配等是派生设计或业务行为；工厂清单的字段、六分支、质量和性能指标是验收候选；索引、生成视图和三份 run 只提供导航或限定环境现状。7 月 16 日“必须批准并保存哈希”与 7 月 27 日“不再要求批准文件/哈希”缺少具名替代决定，另建 HITL 票；本票不自行排序，也不把 run completed、勾选或 `requires_approval=false` 当批准。
