# 决定补充快照中未批准规范候选的首版去留

Type: grilling
Status: resolved
Blocked by: 85

## Question

补充证据快照识别出 `mes/queries/mes-task-union/README.md` 是 2026-08-03 初始快照后发生字节变化、但未被「决定首版基线如何处理初始快照后的替代性需求」绑定批准的第五份规范候选；它的声明应作为当前 8005 MES 外部数据/查询约束进入 `v1.0.0` 原子候选形成，降级为查询实现与验证支持证据，还是保留为历史材料？

决定必须核实该文件的来源、变化差异、适用环境、与四份获批规格及既有 R11 原子候选的重复/替代关系，并明确本决定只控制候选形成资格，不构成整份文件或任何原子条目的最终基线批准。

## Evidence

- [固定并分类首版发布前补充证据快照](85-capture-and-classify-pre-release-supplemental-evidence-snapshot.md)
- [决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)
- [调查 MES 数据、查询与工厂验证约束](23-investigate-mes-data-query-validation-constraints.md)
- [拆分并分类 MES 数据、查询与工厂验证的原子候选](51-classify-r11-atomic-candidates.md)

## Answer

依据用户在[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)中给出的“后续 HITL 默认采用推荐值”授权，本票在明确展示推荐结论、取舍与证据边界并完成独立只读核验后，采用推荐值：当前 `mes/queries/mes-task-union/README.md` **降级为查询实现、发布完整性和验证导航的支持证据，不作为第五份 `v1.0.0` 规范来源层，也不从当前文件重新生成原子需求候选**。该授权不扩张到新增外部权限、破坏性操作或路线范围变化。

### 来源、身份与变化

- 初始快照固定旧文件 SHA-256 `e8b7ed1c34d7d541f2833fc66a34a361c3ba818fa9b6df0daf36e93268d255f0`；补充快照固定当前 tracked-clean blob `7a3e17d31af06f5b48d455ef58c5109024a8b00d`、SHA-256 `d1db74528691bca0b00e09342398e15e6f38b0c7cb9a8132b6f67e85aa4c72e9`，且采集本身的批准效果明确为 `none-by-capture`。
- 补充窗口内唯一修改来自 2026-08-14 的实现提交 `89b6dca9392fcb54d0bc07befe94f925a4a55321`（`feat(mes-ingest): complete ticket 15 Oracle round source`）：一是把旧“同键多行视为硬失败”改为重复候选保留进 `SUCCESS` 轮次、再由投影层确定性处理；二是加入发布包唯一 SQL 路径、SHA-256 `54a140ad2ca6e67413b24d0566991adcd665f6514a742b417b4ed818fbe439ae`、邻接 manifest 与缺失/篡改/第二份 SQL 的拒绝机制。其余内容未变，实际 `query.sql` 在补充窗口内也未发生字节变化。
- 直接来源是《新版 MesIngest 整体替换规格书》的实现票“正式单语句 Oracle Round source”及其代码、测试和发布包工作。该票明确没有获批的真实 Oracle 11g 端点，工厂探针为 `NOT_EXECUTED`；因此 README 和实现提交可以证明落地形态，不能独立证明客户批准、现场通过或外部契约适用性。

### 与获批规格及 R11 的关系

- 《新版 MesIngest 整体替换规格书》早于本次 README 修改，且已经绑定用户批准；它已经规定单条只读六分支语句级快照、异常字段和重复行仍进入 `SUCCESS`、重复观测的投影规则、唯一正式查询原稿及发布包只携一份正式副本。README 的两处新差异是该获批来源的派生实现说明，不是独立上游规范。
- 《MesIngest 有界存储与低内存运行规格书》只继续要求完整 `MES_TASK_UNION` 并排除修改 SQL 或改为增量源；AREA 实时同步规格与 Inspector E 规格分别只替代 `AreaFilterProfile` 和 DemandSeries 详情信息架构。三者均不把 README 提升为新的来源层，也不与本分类冲突。
- 初始 README 已完整形成 `R11-A0063`～`R11-A0078` 共 16 条记录。未变化内容不得因补拍再次原子化；其中外部数据契约候选继续保留原证据与批准缺口，查询组织、实验和本地治理机制继续按既有路线作为支持证据或排除出需求批准。
- 旧 `R11-A0069` 的“同键多行硬失败”由当前获批新版规格替代：旧字节与旧条目只保留为 **PreBaselineSourceSupersession** 历史证据，不创建虚构的 deprecated REQ；当前重复观测义务从获批新版规格形成最终候选，而不是从 README 再造一条。新增的精确路径、manifest 和拒绝机制只作实现与版本完整性证据。

### 适用范围与批准边界

- 当前 README 只支持 8005 MesIngest 六类 Oracle 单语句只读查询包、生产发布包和对应验证的证据链；它不证明 PACKAGE 全集、其它查询、其它项目/Oracle 实例、客户 SQL 授权或真实 Oracle 11g 现场通过。
- 当前文件仍准确描述活跃查询包，因此不把整份文件降为历史材料；只有已被替代的旧重复键措辞作为历史证据。
- 本决定只控制首版候选形成资格：不批准整份 README，不批准任何既有或新增原子条目，不消除客户来源、环境绑定或逐条最终批准缺口，也不修改四份获批规格的来源层叠关系。

没有形成新的领域词汇或改变现有术语含义，因此无需修改 `CONTEXT.md`。本决定解除“建立 v1.0.0 规范候选总账”的阻塞。
