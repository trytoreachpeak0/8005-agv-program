# 拆分并分类 MES 与 SDK 业务及外部约束的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R09 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 12 份候选文档，如何先分离业务行为、外部契约、安全主张与本地技术设计，再对前三者中的需求候选建立原子条目、来源/范围、派生/重复关系、冲突和批准缺口，而不让纯技术决定进入需求批准？

## Answer

已完成总账固定的 12/12 份 R09 候选 ADR 的原子拆分与证据分类，规范主数据为 [R09 原子候选分类账](../evidence/atomic-candidates/R09-atomic-candidates.tsv)，可重建汇总为 [R09 原子候选摘要](../evidence/atomic-candidates/R09-atomic-candidates-summary.json)，提取边界、分类规则、冲突/决定/环境证据指针见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fcaf9-5d19-7bd0-8e7a-6688227ed100/R09-atomic-candidates.xlsx)。

- R09 的 18 份材料边界已失败式固定：只提取 12 份候选 ADR，`ADR-mes-0009`、中央索引及 4 份纯 SDK 技术决定共 6 份保持文档级排除。每份候选都有记录，来源记录 ID、路径和 SHA-256 零漏项。
- 主张、列表与 Consequences 按可独立判断的句子或具名能力拆分；`Status: accepted`、Considered Options、Implementation、代码存在和 Lab 观察统一只作证据，不能传递业务、外部契约或安全批准。
- 最终形成 166 条记录：71 条状态/备选/实现证据，24 条本地技术设计，25 条 MES 调度或 Demand 生命周期业务规则，11 条依赖外部契约的业务行为，11 条外部系统契约，8 条产品能力范围，8 条安全/安全控制边界，6 条待确定责任域的下游义务及 2 条原文未决问题。24 条 C#/Service/WPF/SQL Server/Kiota/SDK 分层等本地设计全部进入 `exclude-from-requirement-approval`。
- `CF-R01-001/002` 继续保留 TransportDemandKey 与 MES 只读/回写冲突；`CF-R09-001` 保存 QueueingStall 清积压与 UC-008 队列 0/1 口径差异，`CF-R09-002` 保存充电改派选桩与 BR-007 可用/占用/预占/电量条件差异，`Q-R09-001` 隔离 `N=2` 与 UC-012 不同失败阶段的 TBD。这些都等待全部批次原子化和跨批次语义去重后再判断是否毕业为 HITL 票。
- `RES-R09-001` 连接“决定工厂 MES 验证的批准与完整性证据门槛”；`RES-R09-002` 与 `EVID-R09-001` 连接 RIoT API 白名单/调用安全边界和受控 OpenAPI 快照。它们限制证据如何使用，但没有把原 ADR 整份升级为已批准需求。
- 166 条记录全部 `not-approved`、零永久 `REQ-NNNN`；11 条后出现记录只按规范化声明指纹标记精确重复，未删除或合并语义近似项。

独立失败式 `--verify-only` 通过：`total=166`、`sources=12`、`excluded_not_extracted=6`、`exact_duplicate_rows=11`、`approval_upgrades=0`；指针命中为 `CF-R01-001=8`、`CF-R01-002=5`、`CF-R09-001=10`、`CF-R09-002=7`、`Q-R09-001=9`、`RES-R09-001=8`、`RES-R09-002=29`、`EVID-R09-001=29`。XLSX 的 12 份来源对账均为 `OK`，汇总公式与指针计数已对账，公式错误扫描为零，并完成四张工作表的视觉检查。
