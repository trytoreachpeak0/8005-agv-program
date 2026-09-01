# 调查历史本地 spec 与实施票据

Type: research
Status: resolved
Blocked by: 11

## Question

对无损清单 R12 批次中的既有本地 spec 与 issue，逐份核实其来源、形成/关闭历史、批准证据、当前版本适用性和与原始需求的派生关系；哪些记录可能保存需求决定，哪些仅是实施计划、修复任务或已过期上下文？

## Answer

完整调查见 [R12 历史本地 spec 与实施票据调查](../evidence/investigations/R12-historical-local-specs-and-issues.md)。固定清单中的 50/50 份材料均已核实且 SHA-256 零漂移。两份 spec 最可能保存需求决定摘要，但都混合业务语义、内部设计、技术栈、默认值和实施验收；31 张 Phase 1/Watch issue 是实施纵切、后续缺陷或工厂验证任务，17 张 Review Remediation issue 是代码审查发现、回归修复和实现偏差证据。

`ready-for-agent`、`done`、勾选验收项、测试通过和修复提交都只证明内部实施/关闭历史，50/50 均缺少批准四要素，不能直接进入当前需求基线。后续应以 spec 的每个 story、Confirmed Domain Semantic、功能条目和默认值为原子指针，分别追回 MES 原始证据、查询目录、ADR 或具名客户/IT 记录；实施票只用于验证当时代码如何实现或偏离上游。
