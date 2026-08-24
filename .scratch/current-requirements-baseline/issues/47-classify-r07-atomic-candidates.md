# 拆分并分类非功能需求的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R07 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 2 份候选文档，如何按 fit criterion 级别拆分原子非功能候选，固定质量属性、度量口径、范围、来源、冲突和批准缺口；追溯材料、索引和空占位不从自身提取？

## Answer

已完成总账固定的 2/2 份 R07 NFR 候选的 FC 级拆分与证据分类，规范主数据为 [R07 原子候选分类账](../evidence/atomic-candidates/R07-atomic-candidates.tsv)，可重建汇总为 [R07 原子候选摘要](../evidence/atomic-candidates/R07-atomic-candidates-summary.json)，边界、字段、TBD/范围/验证指针及处置路线见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fca9d-8881-7a41-9d8c-87fab86068c7/R07-atomic-candidates.xlsx)。

- R07 批次的 15 份材料边界已失败式固定：只提取 `R07-03` NFR-002 与 `R07-04` NFR-001；追溯规则/动态查询、NFR 模板、根索引和 9 份类别占位 README 共 13 份材料保持文档级证据或排除路由，没有从自身生成候选。
- NFR-002 形成 3 条：关键事件审计完整性、180 天留存、5 分钟查询可见性；NFR-001 形成 2 条：正常生产班次可用性 99.5% 和单次非计划中断 RTO 15 分钟。每条保留完整 Given/When/Then、质量属性、度量口径、建议测量方法、8005 范围、原始路径/SHA-256/行定位、来源形成关系和职责对应的批准缺口。
- 3 条审计性候选进入 `needs-quality-security-it-policy-and-explicit-approval`，2 条可用性/恢复性候选进入 `needs-operations-it-sla-and-explicit-approval`；内部愿景、未批准 UC/FR 和编辑者提供的“黄金样例”都没有被误作客户 SLA、留存制度或授权证据。
- `TBD-R07-001` 固定 180 天/5 分钟仍待客户质量/IT/安全批准，`TBD-R07-002` 固定 99.5%/15 分钟仍待客户运维/IT 批准；`SC-R07-001` 保留关键事件目录/最低字段集/对应规则未冻结，`SC-R07-002` 保留外部依赖归因和部分降级口径未固定，`Q-R07-001` 保留 UC-021/FR-029 是否应纳入关键审计目录的范围歧义。依地图既定顺序，这些指针等待其余批次原子化与跨批次去重后复核，本票未提前代替业务方裁决。
- `EX-R07-001` 固定全部 5 个 FC 均无 `related_tc`、构建、环境、执行人、执行时间、实际结果、Pass/Fail 和附件哈希；建议的健康检查、日志、时钟模拟与抽样不是已执行证据。
- 5 条记录全部 `not-approved`、零永久 `REQ-NNNN`，声明指纹零重复。本票只分类和隔离既有证据，没有批准新的领域词汇或业务决定，因此未修改根 `CONTEXT.md`。

独立失败式 `--verify-only` 通过：`total=5`、`sources=2`、`excluded_not_extracted=13`、`duplicates=0`、`approval_upgrades=0`、`missing_related_tc_rows=5`；指针命中为 `EX-R07-001=5`、`Q-R07-001=1`、`SC-R07-001=1`、`SC-R07-002=2`、`TBD-R07-001=2`、`TBD-R07-002=2`。XLSX Summary 公式为总数/NFR-001/NFR-002/来源/批准升级/缺少 TC = `5/2/3/2/0/5`，两个来源对账均为 `OK`，公式错误扫描为零，并完成四张工作表的视觉检查。
