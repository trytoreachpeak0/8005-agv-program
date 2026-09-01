# R07 追溯规则与非功能需求调查

## 调查边界与方法

本资产只调查[material-inventory.tsv](../material-inventory/material-inventory.tsv) 中 `batch_id=R07` 的 15 行：2 份追溯规则/矩阵文件、2 份 NFR、9 份空分类占位 README、1 份 NFR 模板指南与 1 份 NFR 根索引。对每一路径重新执行 `Get-FileHash -Algorithm SHA256 -LiteralPath <path>`，**15/15 与清单完整 SHA-256 一致，0 漂移**；字节数、`last_write_utc` 和快照 `git_status` 以清单为准。

证据判定依据[01 权威与分类证据规则](../../issues/01-authority-and-classification-evidence-rules.md)、[04 原子批准粒度](../../issues/04-atomic-requirement-approval-granularity.md)与[06 历史回溯边界](../../issues/06-current-baseline-history-boundary.md)。逐文件阅读 frontmatter、度量口径、Fit Criterion (FC)、Origin、Related、Verification、Notes 和 Dataview 查询，并使用 `git log --follow` 核对形成史。Git 作者/提交说明、frontmatter `status`、“黄金样例”、追溯链可渲染、实现/测试结果都不能替代“具名授权人 + 日期 + 范围 + 具体版本”批准。

## 形成历史与总体结论

- [traceability-matrix.md](../../../../requirement-documents/06-traceability/traceability-matrix.md) 在 `96eb203` (2026-07-13 08:32 +08:00) 首次引入，于 `ecd0fd8` (2026-07-15 12:58) 改为当前递归 Dataview 查询形式；R07 其余 14 份都在 `ecd0fd8` 形成，没有后续路径修改。提交作者只证明仓库编辑历史，不证明需求授权。
- 只有 NFR-001/002 表达可独立判断的质量属性候选，共 5 个 FC；两者都是 `draft`，Origin 指向内部愿景/UC/限制条款，不是原始客户 SLA、质量制度或合规要求。NFR-001 的 **99.5%/15 分钟**、NFR-002 的 **180 天/5 分钟**均在原文明示标为 TBD/草稿，不是客户承诺。
- 追溯矩阵是**派生查询定义**，不是当时结果快照；渲染结果完全依赖各文档 frontmatter 的正确性。分类规则是**内部归档/索引规则**；其表格仍写站点作业 FR-001∼014，未包含后续 `493ac5a` 新增的 FR-031，证明它不是当前全集的自证权威索引。

## 15/15 文档级证据矩阵

下表 SHA 为 SHA-256 前 12 位；完整值见固定清单。`96`=`96eb203`，`ec`=`ecd0fd8`。“无批准”只表示本批证据不足，不表示内容错误或已废弃。

| # | 固定材料（SHA 前 12）/历史 | 来源、批准与范围 | 当前适用性、性质与后续原子指针 |
|---:|---|---|---|
| 01 | [classification-rules.md](../../../../requirement-documents/06-traceability/classification-rules.md) `920256d9b19b`；`ec` | `type/status: reference`；来源是仓库当时目录/frontmatter 结构；无业务批准对象、无授权范围 | **派生分类/归档规则，非需求**。可用于当前写作归档，但 FR 数量表已漏 FR-031；后续对规则本身与“现有文件清单”分开维护。 |
| 02 | [traceability-matrix.md](../../../../requirement-documents/06-traceability/traceability-matrix.md) `65ce992234ac`；`96→ec` | 来源是五类文档 frontmatter；页面只定义 Dataview 查询与缺口查询，不保存生成结果；无批准 | **派生追溯查询/矩阵定义，非需求或批准记录**。可用于发现缺链，但“有链接”不证明上游或下游已批准。 |
| 03 | [NFR-002](../../../../requirement-documents/08-non-functional-requirements/auditability/nfr-002-audit-completeness-and-retention.md) `0789acda32d6`；`ec` | `draft/high/auditability`；Origin 指愿景可追溯目标、UC-034 查询导出及流程模板不得绕过审计；无具名质量/IT/客户批准，批准范围未建立 | **可独立判断的内部派生 NFR 候选**。按 FC-1 完整性、FC-2 留存、FC-3 可见延迟拆分；“关键操作”目录/最低字段集仍是初稿，180 天/5 分钟待确认；`related_tc: []`。 |
| 04 | [NFR-001](../../../../requirement-documents/08-non-functional-requirements/availability/nfr-001-service-availability.md) `ed84af4491a9`；`ec` | `draft/high/availability`；Origin 只指愿景“运行稳定/稳定完成场景”和现场连续作业分析；无客户 SLA、班次时窗、运维负责方或具名批准 | **可独立判断的内部派生 NFR 候选**。按 FC-1 班次可用性与 FC-2 RTO 拆分；99.5%/15 分钟及外部依赖排除边界均待授权确认；`related_tc: []`。 |
| 05 | [compatibility/README.md](../../../../requirement-documents/08-non-functional-requirements/compatibility/README.md) `b3fbd1c4f5a9`；`ec` | 无 NFR 实例、无批准对象；只以 MES/RCS/RIOT/IO 为未来互操作性指标示例 | **空白分类占位/索引**；示例不形成需求。 |
| 06 | [maintainability/README.md](../../../../requirement-documents/08-non-functional-requirements/maintainability/README.md) `4710ca85041d`；`ec` | 无 NFR/批准；只列配置变更成本、日志诊断性示例 | **空白分类占位/索引**；不提取指标。 |
| 07 | [nfr-template-guide.md](../../../../requirement-documents/08-non-functional-requirements/nfr-template-guide.md) `ef3b13a83a7a`；`ec` | `type: template-guide,status: reference`；以 NFR-001/002 为写作范例，定义 category、Context/Metric/FC/Measurement/Origin 结构；无业务批准 | **纯记录/写作结构，非 NFR**。“无度量与测量方法视为未完成”是内部质量门槛，不是客户质量目标。 |
| 08 | [operability/README.md](../../../../requirement-documents/08-non-functional-requirements/operability/README.md) `97e8357441f5`；`ec` | 无 NFR/批准；只列部署、监控、告警、值守示例 | **空白分类占位/索引**。 |
| 09 | [performance/README.md](../../../../requirement-documents/08-non-functional-requirements/performance/README.md) `ac352c7b360e`；`ec` | 无 NFR/批准；只列响应时间/吞吐/并发示例 | **空白分类占位/索引**。 |
| 10 | [08-non-functional-requirements/README.md](../../../../requirement-documents/08-non-functional-requirements/README.md) `185c21ab0eb8`；`ec` | 模板、指南、“黄金样例”、category 和 Dataview 导航；无业务批准 | **NFR 库根索引/编辑说明**，非 NFR。“黄金样例”只指写作形式，不批准 NFR-001/002 内容。 |
| 11 | [reliability/README.md](../../../../requirement-documents/08-non-functional-requirements/reliability/README.md) `ffcc99890024`；`ec` | 无 NFR/批准；只列故障率、MTTR、一致性示例 | **空白分类占位/索引**。 |
| 12 | [safety/README.md](../../../../requirement-documents/08-non-functional-requirements/safety/README.md) `af62db06c6d7`；`ec` | 无 NFR/批准；区分可度量功能安全指标与 UC-004 业务联锁流程 | **空白分类占位/边界说明**；“故障安全响应时间/失败默认拒绝”是未来类型示例，非已定指标。 |
| 13 | [scalability/README.md](../../../../requirement-documents/08-non-functional-requirements/scalability/README.md) `e77fd52df576`；`ec` | 无 NFR/批准；只列仓位/AGV/并发任务增长示例 | **空白分类占位/索引**。 |
| 14 | [security/README.md](../../../../requirement-documents/08-non-functional-requirements/security/README.md) `eb0b2107c7e2`；`ec` | 无 NFR/批准；只列认证强度、权限、加密示例并与 UC-004 业务安全区分 | **空白分类占位/边界说明**；不能从示例推导密码/加密要求。 |
| 15 | [usability/README.md](../../../../requirement-documents/08-non-functional-requirements/usability/README.md) `1484f06fd220`；`ec` | 无 NFR/批准；只列界面易用性/培训上手时间示例 | **空白分类占位/索引**。 |

## 后续原子化与证据请求

1. **NFR-001：**将班次时窗、“可用”判定口径、99.5%、RTO 15 分钟、计划维护排除、MES/RCS/AP/IO/AGV 外部依赖归因和测量方法分成可独立批准条目；请求客户运维/IT 的 SLA、班次定义、计算式、维护窗口和不可用归因规则，并绑定具名批准与版本。
2. **NFR-002：**将关键事件目录、最低字段集、成功/拒绝完整性、180 天留存、5 分钟可见性、查询/导出范围、外部日志排除和测量方法分开；请求客户质量/IT/安全方针、数据分类与留存制度、UC-034 授权范围和具名批准。
3. **追溯记录：**后续基线应保存绑定某一固定 Git/材料快照的实际矩阵结果或可重复导出，不能只保留动态查询文本；将“有链接”、“源已批准”、“派生转换经核对”和“验证已通过”分成不同状态，不从 Dataview 可见性反推权威性。
4. 9 份占位 README 不产生需求条目；只用于标记待建 NFR 类别。若后续合格来源发生实质冲突，建立独立 HITL 票，本调查不自行裁决或批准。
