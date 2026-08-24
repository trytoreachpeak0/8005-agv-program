# 拆分并分类 MES 数据、查询与工厂验证的原子候选

Type: task
Status: resolved
Blocked by: 30, 34

## Question

依据总账 [R11 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 6 份候选文档，如何将外部数据契约、查询设计、容量与装载安全、验收条件及限定环境现状拆分开，对需求/外部约束候选建立原子条目和证据链，并确保查询运行授权与需求批准仍严格分离？

## Answer

已完成总账固定的 6/6 份 R11 候选材料的原子拆分与证据分类，规范主数据为 [R11 原子候选分类账](../evidence/atomic-candidates/R11-atomic-candidates.tsv)，可重建汇总为 [R11 原子候选摘要](../evidence/atomic-candidates/R11-atomic-candidates-summary.json)，提取与分类边界见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fcb0c-7791-7be3-89bf-b9b5ab964b02/R11-atomic-candidates.xlsx)。

- R11 的 11 份材料边界已失败式固定：只提取工厂首轮执行与回传清单、3 份 query README、PACKAGE 容量 CSV 与容量规则 README；索引、生成视图、catalog 和 3 份 run 目录保持文档级排除，不从这些材料重复生成需求。
- 最终形成 150 条记录：工厂清单 62、统一任务查询 16、操作员身份查询 10、SUBLOT 料盒数查询 11、容量 CSV 28、容量规则说明 23。28 条容量规则逐行保留为 27 条 exact 与 1 条 prefix，不合并不同 PACKAGE 的容量审批单元。
- 已分开外部 MES 数据契约、查询/工具设计、容量与装载安全、身份/隐私、工厂验收条件、凭据处理和限定环境观察。27 条查询组织、bundle/导入、生成视图等技术机制进入 `exclude-from-requirement-approval`；13 条 2026-07-24 run 结果只作限定环境观察。
- `RES-R11-001` 与 `BOUND-R11-001` 固定“查询运行授权不等于需求批准”：登记只读查询可以自行运行，但查询契约、业务筛选、28 条容量、验收条件和性能阈值仍须锁定来源版本、适用范围并由用户逐项批准。旧清单中 8 条“批准/哈希可选”规则只作已替代的治理历史。
- `EVID-R11-001` 限定三份 run 不能形成正式验收或长期性能保证；`EVID-R11-002` 保留容量原始客户表、逐行迁移对账、提供/批准人、厂区/产品/生效期及版本绑定缺口；`SCOPE-R11-001` 禁止把活跃样本称为 PACKAGE 全集或用近似值补齐；`GAP-R11-001` 保留两份独立查询缺少受控脱敏 run 的证据缺口。
- `CF-R01-001/002` 继续连接 `TASK_TYPE + SUBLOT` 与 MES 只读边界的跨批次线索；本票没有发现需要在全部批次原子化和跨批次语义去重前新增的独立 HITL 冲突票。
- 150 条记录全部为 `not-approved`、零永久 `REQ-NNNN`；2 条后出现记录只按规范化声明指纹标记精确重复，不删除或合并语义近似项。

独立失败式 `--verify-only` 通过：`total=150`、`sources=6`、`excluded_not_extracted=5`、`capacity_rules=28`、`exact_duplicate_rows=2`、`approval_upgrades=0`；八类指针全部命中。XLSX 的 6 份来源对账均为 `OK`，汇总公式与指针计数已对账，公式错误扫描为零，并完成四张工作表的视觉检查和导出文件完整性测试。
