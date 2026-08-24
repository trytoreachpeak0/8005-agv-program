# 拆分并分类仓位模拟器范围需求的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R10 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 16 份候选文档，如何只就仓位模拟器自身范围拆分原子候选，记录来源、适用范围、派生/重复关系、冲突和批准缺口，并隔离主系统线索、供应商内容、设计、测试计划和实施计划，不从规划文本反推主系统需求？

## Answer

已完成总账固定的 16/16 份 R10 候选材料的原子拆分与证据分类，规范主数据为 [R10 原子候选分类账](../evidence/atomic-candidates/R10-atomic-candidates.tsv)，可重建汇总为 [R10 原子候选摘要](../evidence/atomic-candidates/R10-atomic-candidates-summary.json)，提取边界、分类规则与边界指针见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fcb04-ea36-7bb2-9805-020824d05417/R10-atomic-candidates.xlsx)。

- R10 的 46 份材料边界已失败式固定：只提取愿景与 15 份 `review` 状态的 `FR-*`；30 份 DR、设计规格、测试/实施计划、索引、模板和供应商材料保持文档级排除。每份候选都有记录，来源记录 ID、路径和 SHA-256 零漏项。
- 最终形成 728 条记录：243 条预留测试计划证据、69 条来源/背景/追踪证据、67 条嵌入技术设计、183 条模拟器产品范围/配置/UI/测试运行候选、88 条模拟器接口/协议候选、42 条仓位行为/故障刺激候选、30 条主系统或现场线索及 6 条供应商派生主张。
- `BOUND-R10-001` 固定不从模拟器硬件刺激反推主系统 UC、业务状态、超时、任务或站点规则；`EVID-R10-001` 连接已解决的“补齐 8005 仓位硬件身份与现场信号证据”，只复核 8005 八仓、点位/极性、500 ms 脉冲、无门磁/移动联锁及弹簧弹门事实。
- `SCOPE-R10-001` 执行用户“供应商手册可以忽略”的范围决定，供应商型号、寄存器和功能码内容只保留清单/来源证据，不进入当前基线候选或外部约束；模拟器自身若要求特定协议行为，仍须从工具范围与完整接口规格独立批准。
- `CF-R10-001` 保留排除材料中的锁 DI 镜像 DO、故障枚举落后等内部不一致；`GAP-R10-001` 保留 Unit Identifier、地址换算、Pulse OFF、PDU 上限、多客户端/超时及库选型未冻结的协议设计缺口。它们属于后续技术复核上下文，不毕业为本地图的主系统需求决定票。
- 728 条记录全部 `not-approved`、零永久 `REQ-NNNN`；11 条后出现记录只按规范化声明指纹标记精确重复，未删除或合并语义近似项。WPF、HTTP/JSON、JSON Schema、localhost、Headless/进程与热重载等固定技术机制已进入 `exclude-from-requirement-approval`。

独立失败式 `--verify-only` 通过：`total=728`、`sources=16`、`excluded_not_extracted=30`、`exact_duplicate_rows=11`、`approval_upgrades=0`；指针命中为 `BOUND-R10-001=96`、`EVID-R10-001=98`、`SCOPE-R10-001=77`、`CF-R10-001=48`、`GAP-R10-001=124`。XLSX 的 16 份来源对账均为 `OK`，汇总公式与指针计数已对账，公式错误扫描为零，并完成四张工作表的视觉检查。
