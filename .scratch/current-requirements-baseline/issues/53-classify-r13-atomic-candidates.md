# 拆分并分类 RIoT 受控接口、集成与物模型的原子候选

Type: task
Status: resolved
Blocked by: 34, 36, 37, 38, 39

## Question

在目标环境与受控接口快照、API 白名单/调用安全边界、`standard.oasis.300ul` 物模型枚举证据和未知枚举处理规则都明确后，依据总账 [R13 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 16 份候选文档，如何按 operation/行为和可独立批准语义拆分原子候选，将外部接口事实、项目集成行为、隐私/授权边界与本地 SDK/物模型设计分开，并对 schema 副本去重？

## Answer

已完成总账固定的 16/16 份 R13 候选的原子拆分与证据分类，规范主数据为 [R13 原子候选分类账](../evidence/atomic-candidates/R13-atomic-candidates.tsv)，可重建汇总为 [R13 原子候选摘要](../evidence/atomic-candidates/R13-atomic-candidates-summary.json)，拆分、授权隔离、物模型证据和副本去重边界见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fcb25-26bc-7570-a14d-5e43cc010a6f/R13-atomic-candidates.xlsx)。

- 共形成 672 条记录：14 份受控 OpenAPI 原始快照逐 operation 拆为 550 条；项目接入说明与物模型问题清单拆为 122 条 Markdown 原子声明。16 份来源逐份覆盖，全部保持 `not-approved`，没有分配永久 `REQ-NNNN`。
- OpenAPI 行绑定 `RIOT-OPENAPI-8005-202607-EARLY-01`、`RIOT-8005-RUNTIME` 和源 build `v2.2.0.14`，每行保留 method/path、operationId、summary、tags、参数、request body、responses 与 security。20 个 operation 被标为既有决策批准的项目集成行为证据，登录/刷新 token 两个 operation 只标为人工应急鉴权备用；其余 528 个 operation 即使存在于 Swagger 也全部保持 `not-authorized`。schema 行本身不承载批准，授权来源只由“决定 RIoT 项目 API 白名单与调用安全边界”承载。
- `R13-01` 已把平台描述、项目使用、环境访问、接口发现、凭据和仓库导航分开；`admin/admin` 只保留为不安全示例，不能成为生产凭据或基线配置。
- `R13-04` 已把静态枚举内容、跳号/不一致/无说明字段、修复建议和旧处置结论分开。原始 TSL 以 53,458 字节、productKey/profile 和 SHA-256 接入为补充证据，但来源版本、环境、build、固件及 8005 适用性继续保持未知；补枚举、黑盒反推和应用层旧建议不得替代票据 38/39 的批准答案。
- 四份 SDK schema 副本已分别按哈希映射到 `device.json`、`imap.json`、`order.json`、`task.json` 原始快照，字节相同且不重复生成候选；本地 SDK 设计/测试文档、规范化生成输入和已忽略供应商手册继续不提取。
- 受控 schema 的订单命令参数名 `orderKey` 与批准决策采用的业务称呼 `orderId` 已登记为显式别名边界，没有把它升级为新真实冲突；本批没有在跨批次语义去重前新增 HITL 冲突票。
- 本票没有形成新的领域词汇决定；根 `CONTEXT.md` 中的 RIoT 授权层级、默认拒绝、`UnrecognizedThingModelValue`、`CallApiKey` 等既有词汇与分类结果一致，因此不修改词汇入口。

独立失败式 `--verify-only` 通过：`total=672`、`sources=16`、`openapi_operations=550`、`markdown=122`、`excluded_not_extracted=10`、`schema_copies_deduped=4`、`not-authorized=528`、`exact_duplicate_rows=15`、`approval_upgrades=0`。XLSX 的 16 份来源对账全部为 `OK`，处置路线、HTTP method、白名单处置和决策指针公式均与摘要一致，公式错误扫描为零，并完成五张工作表的视觉检查。
