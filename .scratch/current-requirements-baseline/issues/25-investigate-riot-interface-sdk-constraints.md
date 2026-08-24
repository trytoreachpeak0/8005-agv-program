# 调查 RIoT 外部接口与 SDK 约束

Type: research
Status: resolved
Blocked by: 11, 26

## Question

对无损清单 R13 批次中的厂商接口文档、物模型、OpenAPI 快照、项目接入说明和 SDK 规格，逐份核实来源、厂商/环境版本、捕获时间、项目适用范围和可核查批准证据；如何区分外部契约约束、项目需求、SDK 设计和仅证明观察现状的接口/配置快照，并按需引用 E03/E04 现状证据而不从实现反推需求？

## Answer

已完成 [R13 RIoT 外部接口与 SDK 约束调查](../evidence/investigations/R13-riot-interface-sdk-constraints.md)：固定清单中的 26/26 份材料均已按路径与 SHA-256 核验，并应用 3 条 Unicode 路径 Git 状态勘误。按用户 2026-08-03 的范围指示，两份供应商 PDF 标记为 `OUT-OF-SCOPE / ignored`，只保留清单、哈希和来源审计；其余 24 份分为项目说明、本地分析、14 份静态 schema、4 份字节相同的 schema 副本、1 份规范化生成输入和 3 份 SDK 设计/测试说明。没有任何一份同时具备明确来源、目标厂商/环境版本、捕获时间、项目适用范围与批准证据，因此可直接进入当前基线的外部接口约束为 0。报告还确认 Swagger 全部缺少 `info.version`、normalized `1.0.0` 只是本地缺省、两个地址缺少环境映射、共享 `admin/admin` 不应进入生产基线，并明确 E03 实验授权和 E04 生成物都不能替代需求批准。
