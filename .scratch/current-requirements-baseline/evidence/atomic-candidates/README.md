# 原子候选分类账

本目录按总账候选组逐批把固定文档拆为可独立审查的原子声明。它是候选与证据分类，不是当前需求基线，也不批准任何条目。

## 资产

- `R01-atomic-candidates.tsv`：规范主数据，共 3,091 条原子声明。
- `R01-atomic-candidates-summary.json`：按来源、类别、处置路线与冲突指针汇总的可重建摘要。
- `build_and_verify_r01_atomic_candidates.py`：从 13 份固定来源重建 TSV/摘要，并以失败式检查核验来源哈希、字段、连续 ID、来源覆盖、声明指纹和批准隔离。
- `extract_docx_structure.py`：只读提取 DOCX 段落与表格结构定位的辅助工具。
- [R01 原子候选 XLSX 审阅副本](../../../../outputs/019fc822-5233-78a0-8de6-14b894bf1f11/R01-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Conflict Register 与 Candidates 四张表；它不是规范主数据。
- `R02-atomic-candidates.tsv`：R02 规范主数据，共 1,206 条原子声明。
- `R02-atomic-candidates-summary.json`：R02 按来源、类别、处置路线与冲突指针汇总的可重建摘要。
- `build_and_verify_r02_atomic_candidates.py`：从总账固定的 19 份 R02 来源重建 TSV/摘要，并失败式核验来源哈希、字段、连续 ID、来源覆盖、声明指纹、内部建模隔离与批准状态。
- [R02 原子候选 XLSX 审阅副本](../../../../outputs/019fc847-5ff0-77b3-b61d-6d9b1e4e11cb/R02-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Conflict Register 与 Candidates 四张表；它不是规范主数据。
- `R03-atomic-candidates.tsv`：R03 规范主数据，共 3,095 条原子声明。
- `R03-atomic-candidates-summary.json`：R03 按来源、类别、处置路线与冲突指针汇总的可重建摘要。
- `build_and_verify_r03_atomic_candidates.py`：从总账固定的 46 份 R03 来源重建 TSV/摘要，并失败式核验来源身份与哈希、连续 ID、来源覆盖、业务候选/内部设计隔离、声明指纹和批准状态。
- [R03 原子候选 XLSX 审阅副本](../../../../outputs/019fca27-ded6-78d1-8185-64aa0e20dcbc/R03-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Conflict Register 与 Candidates 四张表；它不是规范主数据。
- `R04-atomic-candidates.tsv`：R04 规范主数据，共 1,192 条原子记录。
- `R04-atomic-candidates-summary.json`：R04 按来源、类别、处置路线、冲突指针与版本隔离汇总的可重建摘要。
- `build_and_verify_r04_atomic_candidates.py`：从总账固定的 31 份 R04 来源重建 TSV/摘要，并失败式核验来源身份与哈希、146 个 AC 定位、连续 ID、UC/BR 上游指针、声明指纹和批准状态。
- [R04 原子候选 XLSX 审阅副本](../../../../outputs/019fca67-9fff-7980-b212-daf354e681dd/R04-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Conflict Register 与 Candidates 四张表；它不是规范主数据。
- `R05-atomic-candidates.tsv`：R05 规范主数据，共 401 条场景级验收声明与追踪证据。
- `R05-atomic-candidates-summary.json`：R05 按来源、场景角色、候选类别、处置路线与冲突/追踪指针汇总的可重建摘要。
- `build_and_verify_r05_atomic_candidates.py`：从总账固定的 67 份 R05 来源重建 TSV/摘要，并失败式核验来源身份与哈希、四段场景结构、连续 ID、FR/UC 上游指针、声明指纹和批准隔离。
- [R05 原子候选 XLSX 审阅副本](../../../../outputs/019fca7f-d517-73a0-a52a-1790f66ff61e/R05-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Conflict Register 与 Candidates 四张表；它不是规范主数据。
- `R06-atomic-candidates.tsv`：R06 规范主数据，共 225 条场景级验收声明与追踪证据，并追加 4 条从当前 `FR-016` 建立的新身份候选。
- `R06-atomic-candidates-summary.json`：R06 按来源、场景角色、候选类别、处置路线与证据/范围指针汇总的可重建摘要。
- `R06-drifted-historical-evidence.tsv`：固定 `TC-044`～`TC-047` 的当前路径/哈希、旧提交/blob 与历史证据身份；这些记录不进入当前候选。
- `build_and_verify_r06_atomic_candidates.py`：从 52 份 R06 当前草案与固定当前 `FR-016` 重建 TSV/摘要，并失败式核验来源哈希、四段场景覆盖、执行证据缺口、旧稿版本隔离和四个新候选身份。
- [R06 原子候选 XLSX 审阅副本](../../../../outputs/019fca8e-d853-7022-9f17-f8973206bf37/R06-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Version Isolation 与 Candidates 四张表；它不是规范主数据。
- `R07-atomic-candidates.tsv`：R07 规范主数据，只包含 NFR-001 的 2 个 FC 与 NFR-002 的 3 个 FC，共 5 条未批准原子非功能候选。
- `R07-atomic-candidates-summary.json`：R07 按来源、NFR、质量属性、处置路线与 TBD/范围/验证指针汇总的可重建摘要。
- `build_and_verify_r07_atomic_candidates.py`：从总账固定的 2 份 R07 NFR 重建 TSV/摘要，失败式核验 15 份批次边界、2/13 提取路由、来源哈希、5 个 GWT FC、TBD 阈值、批准隔离与缺失验证证据。
- [R07 原子候选 XLSX 审阅副本](../../../../outputs/019fca9d-8881-7a41-9d8c-87fab86068c7/R07-atomic-candidates.xlsx)：包含 Summary、FC Review、Source Coverage 与 Candidates 四张表；它不是规范主数据。
- `R08-atomic-candidates.tsv`：R08 规范主数据，共 1,217 条词汇、领域事实、业务规则、物理约束、产品行为、技术设计与历史证据记录；首轮隔离的 29 条混合声明已可追溯拆为 72 条单一判断候选。
- `R08-atomic-candidates-summary.json`：R08 按来源、语义类别、处置路线、冲突/决定/证据指针及混合声明拆分覆盖汇总的可重建摘要。
- `build_and_verify_r08_atomic_candidates.py`：从总账固定的 19 份 R08 来源重建 TSV/摘要，并失败式核验 57 份批次边界、19/38 提取路由、制图时 `CONTEXT.md` 快照、旧术语表隔离、29→72 拆分来源链和批准状态。
- `R09-atomic-candidates.tsv`：R09 规范主数据，共 166 条 ADR 原子声明、范围与证据记录。
- `R09-atomic-candidates-summary.json`：R09 按来源、语义类别、处置路线及冲突/决定/环境证据指针汇总的可重建摘要。
- `build_and_verify_r09_atomic_candidates.py`：从总账固定的 12 份 R09 候选 ADR 重建 TSV/摘要，并失败式核验 18 份批次边界、12/6 提取路由、来源哈希、业务/外部契约/安全/本地设计隔离和批准状态。
- [R09 原子候选 XLSX 审阅副本](../../../../outputs/019fcaf9-5d19-7bd0-8e7a-6688227ed100/R09-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Decision Pointers 与 Candidates 四张表；它不是规范主数据。
- `R10-atomic-candidates.tsv`：R10 规范主数据，共 728 条模拟器范围、接口、配置、硬件刺激、证据与技术设计记录。
- `R10-atomic-candidates-summary.json`：R10 按来源、语义类别、处置路线及边界/证据指针汇总的可重建摘要。
- `build_and_verify_r10_atomic_candidates.py`：从总账固定的 16 份 R10 候选重建 TSV/摘要，并失败式核验 46 份批次边界、16/30 提取路由、来源哈希、主系统/供应商隔离和批准状态。
- [R10 原子候选 XLSX 审阅副本](../../../../outputs/019fcb04-ea36-7bb2-9805-020824d05417/R10-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Evidence Pointers 与 Candidates 四张表；它不是规范主数据。
- `R11-atomic-candidates.tsv`：R11 规范主数据，共 150 条外部数据契约、查询/工具设计、容量与装载安全、工厂验收条件和限定环境观察记录。
- `R11-atomic-candidates-summary.json`：R11 按来源、语义类别、处置路线、容量规则及查询授权/证据边界指针汇总的可重建摘要。
- `build_and_verify_r11_atomic_candidates.py`：从总账固定的 6 份 R11 候选重建 TSV/摘要，并失败式核验 11 份批次边界、6/5 提取路由、来源哈希、28 条容量规则、run/批准隔离和批准状态。
- [R11 原子候选 XLSX 审阅副本](../../../../outputs/019fcb0c-7791-7be3-89bf-b9b5ab964b02/R11-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Evidence Pointers 与 Candidates 四张表；它不是规范主数据。
- `R12-atomic-candidates.tsv`：R12 规范主数据，共 300 条历史 spec 的 story、领域语义、产品/运维行为、外部契约、默认值、技术设计与历史证据记录。
- `R12-atomic-candidates-summary.json`：R12 按来源、语义类别、处置路线及跨批次冲突/决定/证据指针汇总的可重建摘要。
- `build_and_verify_r12_atomic_candidates.py`：从总账固定的 2 份 R12 混合 spec 重建 TSV/摘要，并失败式核验 50 份批次边界、2/48 提取路由、来源哈希、50 个 Phase 1 story、8 个 Watch 语义来源项、批准隔离和指针覆盖。
- [R12 原子候选 XLSX 审阅副本](../../../../outputs/019fcb14-fb41-72a1-bcac-265d5507b151/R12-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Evidence Pointers 与 Candidates 四张表；它不是规范主数据。
- `R13-atomic-candidates.tsv`：R13 规范主数据，共 672 条 operation 级外部接口事实、项目接入说明、隐私/授权边界和物模型分析记录。
- `R13-atomic-candidates-summary.json`：R13 按来源、语义类别、处置路线、HTTP method、白名单处置、schema 副本去重与补充 TSL 证据汇总的可重建摘要。
- `build_and_verify_r13_atomic_candidates.py`：从总账固定的 16 份 R13 候选重建 TSV/摘要，并失败式核验 26 份批次边界、16/10 提取路由、550 个 OpenAPI operation、封闭白名单、四份 schema 副本去重、补充 TSL 哈希及批准隔离。
- [R13 原子候选 XLSX 审阅副本](../../../../outputs/019fcb25-26bc-7570-a14d-5e43cc010a6f/R13-atomic-candidates.xlsx)：包含 Summary、Source Coverage、Decision Pointers、Pointer Index 与 Candidates 五张表；它不是规范主数据。
- `R01-R13-consolidated-atomic-candidates.tsv`：合并后的规范主数据，共 12,452 条；完整保留各批原字段，并追加完全相同、规范化相同、语义审阅簇、审阅处置、建议批准批次、真实冲突和版本/范围指针，不删除或改写任何来源声明。
- `R01-R13-semantic-relations.tsv`：1,833 条可复核关系，其中完全相同 1,232 条、规范化相同 229 条、语义近似审阅 372 条；关系只要求共同审阅，不代表可以合并。
- `R01-R13-semantic-review-clusters.tsv`：1,065 个审阅簇及其代表行、成员、来源/批次覆盖、适用范围和版本指针；共覆盖 2,732 条候选记录。
- `R01-R13-source-derivations.tsv`：41 条由原账 `duplicate_or_derivation` 明示的来源/重叠关系；它们不传递权威性或批准。
- `R01-R13-conflict-review.tsv`：对六个既有 `CF-*` 指针逐项裁定是否毕业；四个真实业务冲突毕业为 HITL，AREA 映射差异按后续文本收敛保留为版本证据，模拟器内部不一致留在范围外技术复核。
- `R01-R13-approval-batch-suggestions.tsv`：把 6,449 条仍未批准的批准候选按领域和所需责任角色建议分为 102 个审阅批次，每批不超过 180 行或 120 个语义审阅单元；这只是后续形成规范候选条目后的批准路线建议。
- `R01-R13-consolidated-atomic-candidates-summary.json`：输入账本哈希、`CONTEXT.md` 词汇哈希、覆盖、关系、冲突与批准隔离统计。
- `build_and_verify_consolidated_atomic_candidates.py`：从 13 个规范账本重建全部合并产物，以失败式检查保证 12,452 条、候选 ID 唯一、原字段不漂移、全部仍为 `not-approved`、关系端点有效、四个 HITL 冲突不漂移及批准批次零漏项。
- `R01-R13-post-conflict-question-review.tsv`：对合并总账中 241 条 `hold-for-question-or-reframing` 记录的一对一规范复核账；保留原声明与指纹，只追加六类复核处置、上下文指针、理由和复核指纹。
- `R01-R13-post-conflict-question-review-summary.json`：按批次、来源、六类处置、已决覆盖和新 HITL 票汇总 241 条复核覆盖。
- `build_and_verify_post_conflict_question_review.py`：从固定哈希的合并总账重建复核账和摘要，失败式核验 241/241 一对一覆盖、零批准升级、六类处置全集、16 张 HITL 票元数据和候选映射。
- [R01–R13 合并审阅 XLSX](../../../../outputs/019fcb39-f5f0-7861-af1c-8a35895e8ae3/R01-R13-consolidated-atomic-candidates-review.xlsx)：包含 Summary、Batch Coverage、Conflict Review、Approval Batches、Semantic Clusters、Relations、Source Derivations 与 Consolidated 八张表；它不是规范主数据。

## R01–R13 跨批次合并、语义去重与冲突毕业边界

- 13 个上游账本先分别运行 `--verify-only`，全部通过后才参与合并；合并脚本同时固定每个输入 TSV 的 SHA-256 和当前根 `CONTEXT.md` 的词汇哈希。
- 完全相同关系按 NFC 后的原声明字节内容识别；规范化相同关系使用 NFKC、大小写/Markdown/空白统一和根 `CONTEXT.md` 规范词别名。语义近似先以稀有字符三元组召回，再用三元组、二元组和标识符相似度复核，并要求否定语义一致、领域范围相容。
- 所有关系都只是 `review-together-never-auto-merge`；命中不同版本/范围标记时强制为 `retain-separate-version-scope-and-review-link`。任何关系都不删除成员、不把代表行当成规范文本、不分配永久 `REQ-NNNN`，也不传递批准状态。
- 12,452 条中，6,449 条为仍可继续追源和批准的候选，3,114 条只作证据，2,451 条不进入需求批准，197 条等待真实冲突决策，241 条等待问题解决或重新原子化；全部 `approval_state=not-approved`。
- `CF-R01-001`、`CF-R01-002`、`CF-R09-001`、`CF-R09-002` 会改变业务后果且缺少足以自动择一的版本/范围批准证据，因此毕业为独立 HITL grilling 票。
- `CF-R01-003` 的旧纯人工 AREA 映射与当前文本已经收敛为“地图同步 + 命名规则自动派生 + 少量显式覆盖”，只保留为版本差异；`CF-R10-001` 属模拟器排除材料中的技术不一致，依票据 50 不进入本地图的主系统需求决定。
- 本次没有批准新的领域词汇，因而没有修改根 `CONTEXT.md`；合并只消费其规范词以提高审阅匹配，不从词汇文件反向赋予候选权威性。

## 冲突决定后问题复核边界

- 固定复核输入为合并总账 SHA-256 `b176262228842f6e5564f1f5d227321bb28932e498b254890a48cff952fd37f4` 中全部 241 条 `hold-for-question-or-reframing` 记录；输入哈希或行数漂移时脚本拒绝沿用旧复核。
- 241 条逐条归档为：6 条已批准决定覆盖、98 条重复/只作证据、9 条超出当前目的地、86 条毕业为 16 个 HITL 问题、16 条仍须原子重构、26 条仍缺目标环境或版本绑定证据。
- 复核账从不修改上游总账，不删除或合并来源声明，不分配永久需求 ID，不把缺证据、实现细节或历史交付边界伪装成业务决定；所有来源批准状态继续为 `not-approved`。
- HITL 票只承载能精确表述且会改变候选需求的问题；同一主题的多来源证据共同指向一张票，但每条来源仍在复核账中独立保留。

## R02 拆分与分类边界

- 只处理总账 `R02` 候选组固定的 19 份文档：两份愿景/边界文档、一份角色清单、十五份 BR 和一份非纯索引的流程步骤目录。6 个模板、2 个导航/编辑 README 不从自身提取。
- Markdown 列表项与段落按句界拆分；表格以角色、任务类型、步骤类型或项目维度作为身份前缀，再按语义字段拆分，避免把整行多个可独立判断的属性捆成一个批准单元。
- YAML frontmatter、标题、代码块、空白与纯分隔符不生成候选。`Source`、`Rationale` 和 `Related` 内容保留为来源、理由与追溯证据，但进入 `evidence-only`，不从自身批准为需求。
- `R02-19` 的默认管理员规则单独分类为“用户澄清摘要”；`R02-20` 仅把文档自述的“英文+数字、无强制定期更换”密码口径保留为用户澄清摘要，其余登录名、长度、保留标识与存储做法按文档自己的声明隔离为分析人员拟定的内部建模，不允许整份批准。
- `R02-21`～`R02-23` 保持为可追至未批准 MES 综合文档的上游派生候选；`R02-26` 的步骤类型、输入输出、重试与安全边界保持为内部规范派生，不能从目录自身升级为业务需求。
- 所有 1,206 条记录的 `approval_state` 均为 `not-approved`；本批没有分配永久 `REQ-NNNN`，也没有把 `draft`、“已确认”、具名 profile、Git 历史或内部引用当作批准证据。

## R02 冲突与版本差异登记

- `CF-R01-001`：7 条直接涉及 `TASK_TYPE/moveType + SUBLOT` 与替代幂等键口径的 R02 声明。
- `CF-R01-002`：19 条直接涉及当前 MES 只读、回写占位或禁止写操作的 R02 声明。
- `CF-R01-003`：35 条直接涉及 AREA 自动派生、显式覆盖、冻结与步骤调用的 R02 声明。
- `AD-R01-001`：10 条直接涉及六类任务及 `WIRE_TO_NITROGEN` 版本差异的 R02 声明。

这些指针沿用 R01 已登记的问题，不在 R02 票据中裁决，也不提前新增 HITL 票。地图要求先完成其余批次原子化与跨批次去重；届时仍成立的真实冲突才毕业为独立决策票。

## R02 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `needs-source-and-explicit-approval` | 562 | 愿景、范围、角色或内部综合规则仍缺原始来源与明确批准 |
| `needs-upstream-source-and-explicit-approval` | 102 | 可追到未批准 MES 上游，但还缺权威上游版本与最终批准 |
| `needs-source-measurement-and-explicit-approval` | 8 | 数值成功指标还缺测量定义、分母、时间窗和测量责任人 |
| `needs-original-clarification-and-explicit-approval` | 19 | 用户澄清摘要还缺原始对话/会议记录及发言人授权绑定 |
| `hold-for-conflict-decision` | 45 | 命中既有跨批次真实冲突线索，批准前须在去重后复核 |
| `needs-question-resolution` | 19 | 文档自身标明 TBD、未定、待确认或远期评估 |
| `evidence-only` | 261 | 来源、理由、追溯或文档治理证据 |
| `exclude-from-requirement-approval` | 190 | 分析人员拟定或内部流程/步骤建模，不从自身批准为需求 |

19 份来源逐份有记录，候选 ID 零重复，21 条后出现记录指向相同规范化文本的首条记录；这只处理精确重复，不表示可以删除或合并语义近似项。

## R03 拆分与分类边界

- 只处理总账 `R03` 候选组固定的 46 份 Markdown 用例：22 份 `R03-C` 业务用例候选和 24 份 `R03-I` 内部设计推演；模板指南和空白待办不从自身提取。
- 段落按句界拆分，编号/项目符号逐条保留流程步骤身份，表格按带角色、步骤、场景、状态或类型身份的语义单元拆分；每条保留原始行号、章节路径和完整上下文。
- YAML frontmatter、标题、代码块、空白与纯分隔符不生成候选。备注、来源自述、关联用例与作者说明只作 `evidence-only`，不从自身批准为需求。
- `R03-C` 中可独立审查的用户目标、参与者条件和业务行为进入 `needs-source-and-explicit-approval`；明确的 API、SQL、字段、持久化、状态机、轮询、快照、事务或幂等实现细化隔离为 `embedded-internal-design-derivation`，不得随整份 UC 一起批准。
- `R03-I` 中的流程、接口、安全、权限与审计推演分别保留类别，但统一进入 `exclude-from-requirement-approval`；需要业务化时须先取得权威来源并重写为独立批准单元。50 条带 TBD、待确认、待定或未明确内容的声明保持 `needs-question-resolution`。
- 所有 3,095 条记录的 `approval_state` 均为 `not-approved`；本批没有分配永久 `REQ-NNNN`，也没有把 `draft`、Notes 中的“用户确认”、关联 BR/UC、Git 历史、ADR 或当前实现当作批准证据。

## R03 冲突与版本差异登记

- `CF-R01-001`：5 条直接涉及 `任务类型 + SUBLOT` 业务键/幂等口径的 R03 声明。
- `CF-R01-002`：3 条直接涉及 MES 只读或回写边界的 R03 声明。
- `CF-R01-003`：41 条直接涉及 AREA 自动派生、解析、显式覆盖或表 A/表 B 模型的 R03 声明。
- `AD-R01-001`：3 条直接涉及五类/六类运输任务版本差异的 R03 声明。

这些指针补足了既有跨批次问题的 R03 侧证据，但不在本票中裁决，也没有暴露需要提前新增的独立冲突票。待其余批次原子化和跨批次语义去重完成后，仍成立的真实冲突才进入 HITL。

## R03 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `needs-source-and-explicit-approval` | 872 | 业务用例行为候选仍缺权威来源与逐项明确批准 |
| `hold-for-conflict-decision` | 2 | R03-C 业务候选直接命中既有跨批次冲突线索 |
| `needs-question-resolution` | 50 | 文档自身标明 TBD、待确认、待定或未明确 |
| `evidence-only` | 638 | 来源自述、备注、作者说明与关联追溯证据 |
| `exclude-from-requirement-approval` | 1,533 | R03-I 设计推演及 R03-C 中嵌入的内部技术细化 |

46 份来源逐份有记录，候选 ID 零重复，167 条后出现记录只按规范化声明指纹标记精确重复；语义近似项继续等待 R01–R13 全部拆分后的跨批次去重。

## R04 拆分与分类边界

- 只处理总账 `R04` 候选组固定的 31 份 `draft` FR；8 份“暂无 FR”占位 README、写作指南和根索引继续留在文档级排除路线，不从自身提取功能要求。
- Description 段落按句界拆分；Acceptance Criteria 的 146 个 AC 标题只作定位证据，每个 Given、When、Then 及其可独立判断的分句分别成行，并保留完整原行、章节路径与行号。
- 每条记录从 frontmatter 固定 `related_uc`、`related_br`、`related_fr` 与 `related_nfr`，同时保留调查总账中的形成历史；没有 Origin 节的 FR 也不会失去 Related 指针，但其上游证据强度不因此提高。
- Rationale、Origin、Related、Verification 与 Notes 只进入 `evidence-only`；TC 覆盖、ADR `accepted`、Git 作者、`draft` 和当前实现都不构成批准。明确的代码/API/数据结构实现细化进入 `exclude-from-requirement-approval`。
- 功能声明按前置、触发、结果、权限、安全联锁、状态迁移、原子性/一致性、错误处置、HMI 与审计等维度分类；它们只进入 `needs-upstream-source-and-explicit-approval`，不能从 FR 自身直接批准。
- R04-02～15、17、18、20、22 共 18 份来源携带 `AD-R04-001` 版本范围指针，隔离 `ecd0fd8→493ac5a` 的语义替换；旧稿与新稿互不继承批准状态。
- 所有 1,192 条记录的 `approval_state` 均为 `not-approved`，本批没有分配永久 `REQ-NNNN`。

## R04 冲突与版本差异登记

- `CF-R01-001`：1 条功能候选直接涉及同一 SUBLOT 命中其它任务类型时的永久抑制边界，保持 `hold-for-conflict-decision`，等待跨批次去重后复核。
- `AD-R04-001`：4 条来源/备注证据直接描述 FR 旧语义被 LoadBatch、StopClosureCommit 或 ADR 替代；其余 18 份相关来源在 `duplicate_or_derivation` 中保留版本范围。它是版本差异指针，不是本票自行裁决的真实冲突。
- `CF-R01-002`、`CF-R01-003` 与 `AD-R01-001` 在本批没有直接命中；审阅副本仍保留零命中登记，避免跨批次问题被静默遗漏。

本批没有暴露需要在其余批次原子化与跨批次语义去重前提前新增的独立 HITL 冲突票。

## R04 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `needs-upstream-source-and-explicit-approval` | 635 | 内部派生功能或验收候选仍缺权威上游版本与逐项明确批准 |
| `hold-for-conflict-decision` | 1 | 直接命中既有运输需求业务键/抑制冲突线索 |
| `evidence-only` | 555 | AC 定位、来源、理由、关联、验证、备注和版本证据 |
| `exclude-from-requirement-approval` | 1 | 明确的内部消息标识实现细化，不从自身批准为需求 |

31 份来源逐份有记录，候选 ID 零重复，49 条后出现记录只按规范化声明指纹标记精确重复；语义近似项继续等待 R01–R13 全部拆分后的跨批次去重。

## R05 拆分与分类边界

- 只处理总账 `R05` 候选组固定的 67 份现场操作 TC：38 份 `R05-C1` 上游 FR/AC 镜像草稿与 29 份 `R05-C2` 显著固化内部设计的草稿；所有来源均为 `draft`、未执行且未批准。
- 每份 TC 的 Preconditions、Test Steps、Expected Result 与 Verifies 分别拆为前置、动作、结果和追踪证据；共形成 101 条前置、87 条动作、146 条结果与 67 条验证指针，67 份来源均覆盖四种角色。
- 业务验收、身份/权限/即时认证、硬件与安全、车载—服务端/MES 接口、HMI/操作体验以及内部状态机/架构主张使用不同类别和批准缺口；不能用某一责任人的批准覆盖其它职责范围。
- 所有 401 条记录的 `approval_state` 均为 `not-approved`，没有分配永久 `REQ-NNNN`；5 条后出现记录只按规范化声明指纹标为精确重复，不合并语义近似项。

## R05 冲突与追踪质量登记

- `CF-R01-001`：8 条记录直接涉及 `TransportDemandKey`、同一 SUBLOT 的任务类型边界或取消抑制；其中 5 条业务/接口候选进入 `hold-for-conflict-decision`，3 条内部设计主张继续隔离，等待全部批次原子化和跨批次去重后复核。
- `TQ-R05-001`：11 份来源、58 条记录继承文件名与当前正文语义漂移；固定哈希和正文仍可审阅，但未来应修复路径/标题追踪，不能按文件名推断声明。

本批没有发现需要在跨批次去重前新增的独立 HITL 冲突票；验证指针、目录覆盖宣称与上游 `related_tc` 的质量问题继续作为证据指针保留，不把计划验收、可执行测试规范和某次执行结果混为同一对象。

## R05 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `needs-upstream-source-and-explicit-approval` | 112 | 业务验收候选仍缺权威上游版本与逐项明确批准 |
| `needs-security-role-owner-and-explicit-approval` | 69 | 身份、权限、即时认证与原因码仍缺职责范围内批准 |
| `needs-safety-hardware-authority-and-explicit-approval` | 49 | 安全、硬件、IO 与恢复主张仍缺版本绑定和责任人批准 |
| `needs-interface-owner-source-and-explicit-approval` | 28 | 车载—服务端/MES 接口主张仍缺受控接口版本与责任人批准 |
| `needs-operator-product-owner-and-explicit-approval` | 20 | HMI 与操作体验仍缺操作/产品责任人和适用范围批准 |
| `hold-for-conflict-decision` | 5 | 业务/接口候选命中既有 TransportDemandKey 冲突线索 |
| `evidence-only` | 67 | FR/AC 验证指针，只作追踪证据 |
| `exclude-from-requirement-approval` | 51 | 内部状态机、原子性、持久化或架构主张，不从 TC 自身批准 |

## R06 拆分与分类边界

- 只把总账 `R06` 候选组固定的 52 份未阻塞草案（`TC-042`～`TC-043`、`TC-048`～`TC-097`）按 Preconditions、Test Steps、Expected Result 与 Verifies 拆分；共形成 54 条前置、59 条动作、60 条结果与 52 条验证指针，52 份来源均覆盖四种场景角色。
- 每条记录保留 TC、FR、UC、来源路径/哈希与精确位置；`source_claim_status` 固定为未批准、未执行的内部派生验收草案，批准缺口同时保留构建、环境、执行人、时间、实际结果、Pass/Fail 与附件哈希，不能把预期结果误作执行结果。
- 仓位硬件/IO/安全、操作界面、受控接口、身份认证、车队配置生命周期、业务验收与内部状态/事务派生使用不同类别和职责路线；AGV 启停与仓位启停虽然术语相似，仍以 `SB-R06-001` 固定对象范围，不跨对象复用身份。
- 所有 229 条记录的 `approval_state` 均为 `not-approved`，没有分配永久 `REQ-NNNN`；14 条后出现记录只按规范化声明指纹标记精确重复，不合并语义近似项。

## R06 版本隔离与新身份

- `TC-044`～`TC-047` 不修改、不复用且不进入当前候选；它们继续绑定旧提交 `ecd0fd89c51c6602eda13f37b7c2e9fe181e5aad`、各自 TC blob 与旧 `FR-016` blob，并在 `R06-drifted-historical-evidence.tsv` 中保持为未批准历史验收草案。
- 当前 `FR-016`（总账 `R04-17`、SHA-256 `bd9df8d49efd21941ec36aade3976ca4a0e1ff58eb64cf2626a3796b8ca35920`）的 AC-1～AC-4 分别建立 `R06-N001`～`R06-N004`，覆盖“立即禁用”、“待禁用”、“启用不覆盖车载硬件不可操作”和“批量独立结果”。这些是新身份、不是旧 TC 的改写或复用，也不继承批准状态。
- `AD-R06-001` 固定旧稿与当前语义的版本隔离，`EX-R06-001` 固定 52 份草案的执行证据缺口，`SB-R06-001` 固定 AGV 与仓位启停的对象边界；本票不裁决跨批次语义近似项。

## R06 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `evidence-only` | 52 | FR/AC 验证指针，只作追踪证据，同时保留无执行证据标记 |
| `exclude-from-requirement-approval` | 6 | 内部事务、快照或状态派生，不从 TC 自身批准 |
| `needs-fleet-configuration-owner-and-explicit-approval` | 49 | 车队模型、车辆配置与生命周期候选仍缺责任人、版本与逐项批准 |
| `needs-interface-owner-source-and-explicit-approval` | 11 | RIoT/RCS、同步或指令边界仍缺受控接口版本与责任人批准 |
| `needs-operator-product-owner-and-explicit-approval` | 35 | 看板、提示与操作体验仍缺产品/操作责任人与范围批准 |
| `needs-safety-hardware-authority-and-explicit-approval` | 54 | 仓门、光幕、IO、硬件可操作性与 fail-closed 主张仍缺硬件版本和安全责任人批准 |
| `needs-security-role-owner-and-explicit-approval` | 6 | 二次认证、授权或维护态准入仍缺职责范围内批准 |
| `needs-upstream-source-and-explicit-approval` | 16 | 业务验收及四个当前 `FR-016` 新身份候选仍缺权威上游版本和逐项批准 |

## R07 拆分与分类边界

- 只处理总账 `R07-03` 的 NFR-002 与 `R07-04` 的 NFR-001；两份追溯规则/动态查询、NFR 模板指南、根索引和 9 份类别占位 README 共 13 份材料不从自身提取需求。
- 以原文 `Given / When / Then` 完整 FC 为单个批准单元：NFR-002 的审计完整性、180 天留存与 5 分钟查询可见性各一条；NFR-001 的班次可用性与非计划中断 RTO 各一条。
- `candidate_class` 固定质量属性，`statement_text` 和 `source_context` 保留 FC 与原文阈值，`applicable_scope` 固定 8005 范围；`duplicate_or_derivation` 独立保留度量口径、建议测量方法、内/外范围、上游关联和来源形成关系。
- NFR-002 的来源只是内部愿景可追溯目标、未批准 UC-034 及内部“不得绕过审计”约束；NFR-001 只来自内部稳定性目标和连续作业分析。它们都不是客户 SLA、数据留存制度或具名授权证据。
- 所有 5 条记录的 `approval_state` 均为 `not-approved`，没有分配永久 `REQ-NNNN`；建议的健康检查、日志、时钟模拟、抽样或自动断言只是测量/验证方法，不是已执行的验收证据。

## R07 TBD、范围与验证指针

- `TBD-R07-001`：NFR-002 的 180 天留存和 5 分钟可见性仍是草稿阈值，须绑定客户质量/IT/安全制度、具名批准范围与固定版本。
- `TBD-R07-002`：NFR-001 的 99.5% 可用性和 15 分钟 RTO 仍是草稿 SLA，须由客户运维/IT 批准班次、时间窗、计算式与事故起止点。
- `SC-R07-001`：关键审计事件目录、最低字段集与业务结果到审计记录的 1:1/聚合对应规则未冻结。
- `Q-R07-001`：UC-021 正常流只写“记录操作人、时间和原因”；它是否足以把 FR-029 纳入关键审计目录仍是范围歧义，不在本票代替业务方裁决。
- `SC-R07-002`：外部 MES、RCS/RIoT、AP、IO 和 AGV 导致的中断在原文中被排除或分开统计，但责任归因、部分降级与核心接口可用定义尚未固定。
- `EX-R07-001`：5 个 FC 的 `related_tc` 均为空，且无构建、环境、执行人、执行时间、实际结果、Pass/Fail 和附件哈希。

上述指针保留后续批准与跨批次复核边界，本票没有把它们提前裁决为当前需求。

## R07 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `needs-quality-security-it-policy-and-explicit-approval` | 3 | 审计完整性、留存与查询可见性仍缺客户制度、冻结口径、责任人与逐项批准 |
| `needs-operations-it-sla-and-explicit-approval` | 2 | 班次可用性与 RTO 仍缺客户 SLA、计算/事故口径、外部归因规则和逐项批准 |

2 份来源逐份有 FC 记录，候选 ID 零重复，5 条声明指纹均唯一；其余 13 份 R07 材料保持文档级证据或排除路由，没有被静默转换为原子候选。

## R08 拆分与分类边界

- 只处理总账 `R08` 候选组固定的 19 份材料：制图时的根 `CONTEXT.md`、17 份同时含业务/物理候选与设计的跨域 ADR，以及旧 `glossary/terminology-glossary.md`；R08 其余 38 份纯技术决定或已替代历史材料保持文档级路由，不在本票重复提取。
- 根 `CONTEXT.md` 按 130 个词汇块处理：定义中的每个可独立判断声明分开，130 组 `_Avoid_` 作为独立的规范名称/禁用同义词候选。本批次使用地图固定 Git 基点 `1469d6309d00b0abb792f6cd686aed68286e638e` 恢复制图时语义内容，并保留初始快照的工作树字节 SHA-256 `221b4e69…f937de`；不会把后续已批准写回的新内容倒灌进 R08 旧快照。
- 17 份 ADR 的正文、列表和结果分开提取；`Status: accepted`、来源自述、取舍理由和形成关系只作证据。业务规则、领域定义、身份/权限、物理事实、产品界面行为与技术设计使用不同分类和批准缺口。首轮隔离的 29 条混合声明经“拆分 R08 业务义务与技术机制混合声明”机械拆为 72 条单一判断候选；每条保留相同来源位置与完整 `source_context`，并在 `duplicate_or_derivation` 中记录原候选 ID、原声明指纹和拆分面向。原始 `CONTEXT.md` 与 ADR 未被改写。
- 旧术语表的 109 个完整表格行和 11 条范围/治理/变更自述全部保留为历史证据，不直接进入批准。“确定领域词汇唯一入口与旧术语表关系”只固定根 `CONTEXT.md` 的唯一运行时入口与澄清—批准—即时写回闭环，不追溯批准旧术语表或整份 `CONTEXT.md`。

## R08 冲突、证据与词汇闭环指针

- `RES-R08-001` 把 ADR 0018/0055 的操作员上下文清除不一致路由到已解决的“决定操作员上下文的清除时点”；`RES-R08-002` 把 `AWAITING_LOAD_CONFIRMATION` / `LoadFinalConfirmation` 残留路由到已解决的“决定装货待整批确认阶段是否存在”。它们是已批准决定的上下文指针，不把原 ADR 版本整份升级为已批准。
- `RES-R08-003` 覆盖两个词汇载体的全部记录，确保任何后续获批词汇只通过根 `CONTEXT.md` 固定闭环生效；本票没有改动 `CONTEXT.md`。
- `EVID-R08-001` 把 8005 仓位数、DI/DO、光幕、门磁、弹簧弹门和移动联锁等物理主张路由到“补齐 8005 仓位硬件身份与现场信号证据”；`CF-R01-001` 和 `CF-R01-002` 保留 TransportDemandKey 及 MES 只读/回写的跨批次冲突线索。
- 1,217 条记录全部保持 `not-approved`，没有分配永久 `REQ-NNNN`。49 条后出现记录只按规范化声明指纹标记精确重复，不自动删除或合并语义近似项；`needs-atomic-reframing-before-approval` 已降为 0。

## R08 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `evidence-only` | 238 | ADR 状态/理由、载体自述和旧术语表历史证据 |
| `exclude-from-requirement-approval` | 291 | 嵌入的跨域技术设计，只保留单独技术决定复核 |
| `needs-business-owner-and-explicit-approval` | 248 | 跨域业务流程、生命周期和不变量候选 |
| `needs-domain-owner-and-explicit-approval-before-context-update` | 268 | 领域定义、标准名称与禁用同义词，获批后才能走 `CONTEXT.md` 闭环 |
| `needs-hardware-field-evidence-and-explicit-approval` | 35 | 8005 物理事实、现场信号和硬件约束 |
| `needs-operator-product-owner-and-explicit-approval` | 48 | 车载展示、操作提示与倒计时行为 |
| `needs-role-authority-and-explicit-approval` | 89 | 身份核验、角色、权限、凭证和业务授权边界 |

## R09 拆分与分类边界

- 只处理总账 `R09` 候选组固定的 12 份材料：8 份 MES ADR 与 4 份 SDK ADR；`ADR-mes-0009`、中央索引及 4 份纯 SDK 技术决定继续保持文档级排除，不从自身抽取需求候选。
- 每份 ADR 的主张、列表与 Consequences 按可独立判断的句子或具名能力拆分；`Status: accepted`、Considered Options、Implementation、代码存在和 Lab 观察只作 `evidence-only`，不传递业务、外部契约或安全批准。
- 业务异常处置与 Demand 生命周期、外部 MES/RIoT 契约、鉴权/急停/凭证安全、产品能力范围和本地技术设计使用独立类别与批准缺口。24 条 C#/Service/WPF/SQL Server/Kiota/SDK 分层等本地技术决定进入 `exclude-from-requirement-approval`，不会随混合 ADR 一并送业务批准。
- 最终 166 条记录全部保持 `not-approved`，没有分配永久 `REQ-NNNN`。11 条后出现记录只按规范化声明指纹标记精确重复，不自动合并语义近似项。

## R09 冲突、决定与环境证据指针

- `CF-R01-001` 和 `CF-R01-002` 继续连接 TransportDemandKey 及 MES 只读/回写的跨批次冲突线索；R09 不在全部批次原子化和语义去重前自行裁决。
- `CF-R09-001` 保存 QueueingStall 清积压与 UC-008 队列 0/1 口径的待复核差异；`CF-R09-002` 保存充电改派 Near 选桩与 BR-007 可用/占用/预占/电量条件的待复核差异。
- `Q-R09-001` 将 `N=2` 与 UC-012 的重试次数 TBD 保持为分阶段问题，避免把“发起改派失败”和“充电 HANG 后改派”擅自合并。
- `RES-R09-001` 连接“决定工厂 MES 验证的批准与完整性证据门槛”；`RES-R09-002` 与 `EVID-R09-001` 连接 RIoT API 白名单/安全边界及受控 OpenAPI 快照。它们约束证据使用方式，但不把原 ADR 整份升级为已批准需求。

## R09 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `evidence-only` | 71 | ADR 状态、备选项、实现与观察来源，只作证据 |
| `exclude-from-requirement-approval` | 24 | 本地技术栈、投影、分页、SDK 分层与生成机制 |
| `needs-bound-external-contract-and-explicit-approval` | 11 | MES/RIoT 外部契约仍缺目标环境、版本/哈希和授权责任人 |
| `needs-business-owner-and-explicit-approval` | 25 | Stall、HANG、充电改派与 Demand 生命周期业务规则 |
| `needs-business-owner-bound-contract-and-explicit-approval` | 11 | 同时依赖业务决定和外部接口行为的候选 |
| `needs-product-owner-and-explicit-approval` | 8 | 第一版/第一期产品能力和非目标范围 |
| `needs-question-resolution` | 2 | 原 ADR 自身仍留给后续决定的范围问题 |
| `needs-responsible-owner-and-explicit-approval` | 6 | Consequence 中尚未确定责任域的下游义务 |
| `needs-security-authority-bound-contract-and-explicit-approval` | 8 | 鉴权、凭证、急停和调用安全边界 |

## R10 拆分与分类边界

- 只处理总账 `R10` 候选组固定的 16 份材料：`slots-simulator` 愿景与 15 份状态为 `review` 的 `FR-*`。R10 其余 30 份 DR、设计规格、测试/实施计划、索引、模板和供应商材料保持文档级排除，不从这些材料重复抽取原子候选。
- 愿景和 FR 的需求描述、范围与验收条件按可独立判断的句子或列表项拆分；Origin、Related/关联、背景与决策依据只作来源/追踪证据，Verification 中预留的 Given/When/Then 只作测试计划证据，不能反向证明实现或验收通过。
- 模拟器自身的能力、仓位/故障刺激、接口/协议、配置/校验、内部操作 UI 与测试运行能力分别分类。固定的 WPF、HTTP/JSON、JSON Schema、localhost、Headless/进程与热重载机制等技术选择进入 `exclude-from-requirement-approval`，不会随工具范围候选一并送业务批准。
- 主系统 UC、任务、站点、业务超时、异常锁定、已禁用及现场拓扑主张只保留为线索；供应商型号、寄存器和功能码内容按用户范围决定只保留清单/来源证据。两者均不得从模拟器规划反推为主系统当前需求或外部约束。
- 最终 728 条记录全部保持 `not-approved`，没有分配永久 `REQ-NNNN`。11 条后出现记录只按规范化声明指纹标记精确重复，不自动合并语义近似项。

## R10 主系统边界、现场证据与设计缺口指针

- `BOUND-R10-001` 固定模拟器材料只证明拟提供的硬件刺激，不批准主系统 UC、业务状态、超时、任务或站点规则。
- `EVID-R10-001` 连接“补齐 8005 仓位硬件身份与现场信号证据”，复核八仓点位、原始极性、500 ms 脉冲、无门磁/移动联锁及弹簧弹门等 8005 范围事实；该指针不批准整份 R10 规划。
- `SCOPE-R10-001` 执行用户“供应商手册可以忽略”的范围决定，厂商型号、寄存器和功能码内容不进入本次当前基线候选或外部约束。
- `CF-R10-001` 保留排除材料中的锁 DI 镜像 DO、故障枚举落后等内部不一致；`GAP-R10-001` 保留 Unit Identifier、地址换算、Pulse OFF、PDU 上限、多客户端/超时及库选型尚未冻结的协议设计缺口。

## R10 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `needs-simulator-product-owner-and-explicit-approval` | 183 | 模拟器产品范围、配置、UI 与测试运行能力仍须工具产品责任人逐项批准 |
| `needs-simulator-interface-owner-and-explicit-approval` | 88 | Modbus 与控制接口行为仍须完整、版本化接口口径和责任人批准 |
| `needs-simulator-hardware-behavior-owner-and-explicit-approval` | 42 | 仓位状态、故障刺激及硬件反馈模拟需绑定现场事实后批准 |
| `exclude-from-requirement-approval` | 67 | 固定技术机制与本地设计选择，仅进入独立技术复核 |
| `main-system-or-field-lead-evidence-only` | 30 | 主系统责任或现场事实线索，不从模拟器规划反推 |
| `vendor-content-out-of-scope-evidence-only` | 6 | 按用户范围决定，仅保留供应商内容的清单和来源证据 |
| `source-or-traceability-evidence-only` | 69 | 背景、来源和 UC/FR/DR 关联只作追踪证据 |
| `test-plan-evidence-only` | 243 | 预留验证步骤只作测试规划，不是通过证据 |

## R11 拆分与分类边界

- 只处理总账 `R11` 候选组固定的 6 份材料：工厂首轮执行与回传清单、3 份 query README、PACKAGE 容量 CSV 与容量规则 README。R11 的索引、生成视图、catalog 和 3 份 run 目录保持文档级排除；run 只通过清单中的限定观察摘要建立指针，不从目录自身重复提取需求。
- Markdown 按段落句子和列表项拆分；代码块只保留在上下文文件中，不把执行命令当需求。容量 CSV 每一数据行作为一个不可再拆的“字面匹配类型 + PACKAGE pattern + 每花篮最大盒数 + active 状态”审批单元，固定为 27 条 exact 和 1 条 prefix。
- 外部 MES 字段/对象/筛选语义、查询产品边界、查询设计、身份/隐私、容量换算与装载 fail-closed 行为、工厂验收条件、凭据处理、执行工具和限定 run 观察分别分类；不得整份批准 query README 或工厂清单。
- `MES_TASK_UNION` 的 `TASK_TYPE + SUBLOT` 冲突行为、`OP_OPERATOR_IDENTITY` 的身份解析与岗位授权边界、`SUBLOT_BOX_COUNT` 的数据契约与 ExpectedBasketCount/开锁前阻断分别保留。`UNION ALL`、SQL 原稿位置、bundle、目录和导入机制作为派生查询/工具设计或追踪证据隔离。
- 150 条记录全部保持 `not-approved`，没有分配永久 `REQ-NNNN`。2 条后出现记录只按规范化声明指纹标记精确重复；语义近似和跨批次重复继续等待全部批次完成后处理。

## R11 查询授权、观察证据与容量来源指针

- `RES-R11-001` 与 `BOUND-R11-001` 固定已解决边界：登记的只读查询可以自行运行，但运行授权不批准查询契约、筛选、容量、验收条件或性能阈值；这些仍须绑定来源版本、适用范围并由用户逐项批准。
- `EVID-R11-001` 把 2026-07-24 三份 run 限定为当时环境、SQL 和数据时间下的参考观察，不能形成正式验收、长期性能保证或需求批准。
- `EVID-R11-002` 保存 28 条容量规则的原始客户表、逐行迁移对账、具名提供/批准人、厂区/产品/生效期和版本绑定缺口；迁移 CSV 不得自行补足这些证据。
- `SCOPE-R11-001` 固定活跃样本不是 PACKAGE 全集，100 个未匹配聚合值和 `TOLL-` 字面前缀不能靠近似或外推补值；`GAP-R11-001` 保存两份独立查询尚缺受控环境、查询版本和脱敏 run 的证据缺口。
- `CF-R01-001` 与 `CF-R01-002` 继续连接 TransportDemandKey 及 MES 只读边界的跨批次线索。本票未发现需要在跨批次语义去重前新增的独立 HITL 冲突票。

## R11 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `exclude-from-requirement-approval` | 27 | 查询组织、bundle/导入流程、生成视图和本地工具设计 |
| `historical-governance-evidence-only` | 8 | 已被“决定工厂 MES 验证的批准与完整性证据门槛”替代的批准/哈希可选规则 |
| `limited-environment-observation-evidence-only` | 13 | 三份 2026-07-24 run 的环境限定结果摘要 |
| `source-or-traceability-evidence-only` | 15 | SQL/TOML 位置、客户原始分支、实验计划和容量来源说明 |
| `needs-acceptance-owner-and-explicit-approval` | 16 | 字段/质量、六分支差异、性能、负载与证据包验收条件 |
| `needs-bound-external-data-contract-and-explicit-approval` | 10 | 六类查询、操作员身份和料盒数的外部数据契约 |
| `needs-business-owner-bound-data-contract-and-explicit-approval` | 1 | 重复业务键的硬失败与局部阻断行为 |
| `needs-capacity-source-scope-and-explicit-approval` | 36 | 28 条容量值、参考数据字段和补表治理 |
| `needs-loading-safety-owner-bound-data-source-and-explicit-approval` | 11 | 容量匹配、ExpectedBasketCount 与装载前 fail-closed 行为 |
| `needs-identity-and-security-owner-and-explicit-approval` | 2 | 身份核验/审计用途与岗位授权分离 |
| `needs-identity-owner-bound-data-contract-and-explicit-approval` | 1 | 身份无结果时不得建立操作会话 |
| `needs-security-owner-and-explicit-approval` | 6 | 工厂凭据与敏感数据处理 |
| `needs-security-owner-bound-data-contract-and-explicit-approval` | 3 | 绑定变量、只读查询和人员数据脱敏 |
| `needs-product-owner-and-explicit-approval` | 1 | SUBLOT_BOX_COUNT 不参与六类轮询的范围边界 |

## R12 拆分与分类边界

- 只处理总账 `R12` 候选组固定的 2 份混合 spec：`MesIngest Phase 1` 和 `MesIngest Watch Operations and Scalable Read Model`。R12 其余 31 张实施/偏差修复票与 17 张 review remediation 票继续保持文档级排除，不从它们重复生成需求。
- Markdown 段落、列表和编号 story 按可独立判断的句子/分号语义拆分；每条保留精确行号、完整上下文、来源哈希、总账当前适用性和显式上游引用。最终形成 300 条：Phase 1 spec 130 条，Watch spec 170 条。
- Phase 1 的 50 个 user story 逐项覆盖；Watch 的 8 个 `Confirmed Domain Semantics` 来源项和 65 个 Functional Requirements 来源项零遗漏。`ready-for-agent`、`confirmed`、测试策略和文档输出都只作内部状态/实施历史，不传递需求批准。
- 需求语义已分开为 TransportDemand 生命周期、MES 外部数据契约、Watch 用户与运维行为、读 API/下游同步契约、Alert 事件语义、安全边界、可调默认值、产品范围与本地技术/测试决定。44 条纯技术/测试机制进入 `exclude-from-requirement-approval`；混合语句保持待重新原子化，不与业务义务捆绑批准。
- 300 条记录全部保持 `not-approved`，没有分配永久 `REQ-NNNN`。唯一精确重复是两份 spec 的 `Status: ready-for-agent`，只建立后出现指针，不删除历史记录。

## R12 冲突、决定、证据与词汇闭环指针

- `BOUND-R12-001` 覆盖全部 300 条，固定“2 份 spec 提取，48 张实施/评审票不提取”的边界。`CF-R01-001/002` 继续保留 TransportDemandKey / DemandId / GONE 后再现和 MES 只读/回写的跨批次线索；`AD-R01-001` 继续隔离五类/六类任务的版本差异。
- `RES-R11-001` 与 `BOUND-R11-001` 命中 14 条，把历史 spec 中“客户批准 SQL”的自述限制在已解决的“查询运行授权不等于需求批准”边界内；`EVID-R11-001` 命中 2 条，禁止将厂区耗时观察升级为正式验收或长期性能保证。
- `RES-R08-003` 命中 13 条历史领域语义/词汇声明，确保它们即使与当前 `CONTEXT.md` 用词一致，也不从 spec 反向获得权威；只有经 `grilling` / `domain-modeling` 澄清和用户批准后才能继续通过根 `CONTEXT.md` 闭环生效。本批没有新批准词汇，因此不修改 `CONTEXT.md`。
- 当前只复用已经票据化或已解决的跨批次线索；本批没有发现需要在全部批次原子化与跨批次语义去重之前新建的独立 HITL 真实冲突票。

## R12 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `evidence-only` | 30 | 状态、测试策略、文档输出与实施历史只作证据 |
| `exclude-from-requirement-approval` | 44 | 本地技术栈、存储、架构、实现和测试机制不从历史 spec 批准 |
| `needs-acceptance-owner-and-explicit-approval` | 1 | 工厂人工验证条件需绑定验证对象、环境与责任人 |
| `needs-atomic-reframing-before-approval` | 2 | 产品范围与实施机制混合，需分开后再判定责任人 |
| `needs-bound-external-data-contract-and-explicit-approval` | 4 | MES 字段、SQL 及完整快照边界需绑定受控来源 |
| `needs-business-owner-and-explicit-approval` | 26 | TransportDemand 生命周期与消失/再现行为需业务批准 |
| `needs-business-owner-bound-data-contract-and-explicit-approval` | 9 | 业务行为同时依赖 MES 字段与快照契约 |
| `needs-domain-owner-and-explicit-approval-before-context-update` | 11 | 历史领域语义必须经词汇闭环批准后才可生效 |
| `needs-interface-owner-and-explicit-approval` | 21 | 读 API、分页、ChangeFeed 与 Bootstrap 契约需接口责任人批准 |
| `needs-operations-owner-and-explicit-approval` | 40 | Alert 事件、恢复、横幅与运维证据行为需运维责任人批准 |
| `needs-operator-product-owner-and-explicit-approval` | 40 | Watch 显示、筛选、排序、复制、状态与布局需操作员产品责任人批准 |
| `needs-product-owner-and-explicit-approval` | 27 | 产品能力、交付范围与 Out of Scope 需产品范围批准 |
| `needs-responsible-owner-and-explicit-approval` | 40 | 可调默认值、阈值、保留期和大小上限需分配责任人后批准 |
| `needs-security-owner-and-explicit-approval` | 5 | 凭证、绑定、SharedSecret 与敏感数据边界需安全批准 |

## 拆分边界

- Markdown 的列表项、段落句子和表格语义单元分别拆分；表格始终保留完整行上下文，避免只取结论而丢失事项、角色、场景或验收项目。
- DOCX 使用只读 OOXML 结构定位，段落以 `Pnnnn`、表格行以 `TnnRnnn` 标识。当前环境没有 LibreOffice，无法渲染页面；因此没有声称完成页码、签章或版式复核，也没有修改任何 DOCX。
- `R01-10` 只提取既定路由中的第四条项目范围、10.1 基本配置、10.4 性能、10.6 售后/生效、10.7～10.9 验收。项目已填条款与未签署的通用模板义务使用不同类别，均保持未批准。
- `R01-11` 的项目身份、数量、型号、成本、交期与生产计划分别保留；只有范围身份可作为技术需求的候选证据，责任人与排期继续是项目计划证据。
- `R01-13` 当前 Markdown 与 `R01-14` 的 2026-07-14 冻结 DOCX 分开提取。后者不得继承当前 Markdown 的新增内容或假定外发/确认；规范化文本 SHA-256 相同的后出现记录才标为 `exact-duplicate-of`。
- `R01-15` 已逐条人工核对图中的系统边界、参与方和数据/控制流，并以图中对象或边作为定位；没有让图自动继承任一正文版本的批准状态。
- 代码块、空白模板行、纯分隔符和无语义占位不生成原子候选。建议动作、内部实现、历史状态和来源说明仍可留作证据，但走 `evidence-only` 或 `exclude-from-requirement-approval`，不会变成客户需求。

## 字段边界

- `candidate_id` 是本次分类账的稳定候选身份，不是永久 `REQ-NNNN`；只有最终批准后才分配基线需求 ID。
- `statement_text` 保存本次可独立判断的声明，`source_context` 保存其完整原行/段上下文；`source_path`、`source_sha256` 与 `exact_location` 共同固定来源。
- `candidate_class` 区分业务、接口、角色、用例、验收、未决问题、内部设计、历史证据、自称关闭决定和未签署协议等性质。
- `source_claim_status` 只说明材料如何自我表述或如何形成，不赋予权威性。
- `duplicate_or_derivation` 保存文档级形成关系和精确文本重复指针。语义近似项尚未合并，等待 R01–R13 全部拆分后的跨批次去重。
- `conflict_pointer` 只登记需要后续判断的冲突或版本差异线索，不在本票中替用户裁决。
- 所有 3,091 条记录的 `approval_state` 都是 `not-approved`，批准缺口统一保留具名批准人、日期、范围和版本/哈希绑定四项。58 条自称“已关闭”的决定仍保持未批准；137 条协议候选仍保持未签署/未生效隔离。

## 冲突与版本差异登记

### `CF-R01-001` — 运输需求业务键/幂等键口径

- `R01-04` 与 `R01-05` 主张 `TASK_TYPE + SUBLOT`。
- `R01-17` 主张 `product_lot + machine_no + finish_time` 或 MES 事务 ID。
- 两者会改变重复任务、取消抑制和 GONE 后再现语义，不能靠文档新旧或当前代码自行选择。待跨批次去重后若仍成立，应生成 HITL grilling 票据。

### `CF-R01-002` — 当前阶段 MES 是否只读

- `R01-04`、`R01-05`、当前 `R01-13` 与系统上下文图主张当前阶段只读 MES、不回写。
- `R01-17` 多处把卸车后的 MES 回写列为流程或服务器职责，部分位置写成“回写或提示 OP/PDA”的二选一。
- 需要分开确认“系统义务”“人工/PDA 后续动作”和“远期能力”，不能把二选一措辞自动解释成只读结论。

### `CF-R01-003` — AREA 映射模型的跨批次冲突线索

- `R01-05` 明确记录：既有 UC-024/BR-003 的人工维护、版本化显式映射模型，与地图同步、命名规则自动派生加少量显式覆盖的模型存在差异。
- 当前 R01 文档已经主要采用自动派生模型，但被引用的 UC/BR 位于后续 R03/R02 候选组；本票只保留精确冲突指针，待那些批次拆分后复核，不提前认定真实冲突仍存在。

### `AD-R01-001` — 五类与六类运输任务的版本差异

- `R01-14` 冻结在 2026-07-14，仅列五类运输任务。
- 当前 `R01-04`、`R01-05` 与 `R01-13` 已列六类，新增 `WIRE_TO_NITROGEN`。
- 现有日期与生成链足以隔离版本，但不足以证明第六类已获客户批准；因此这是 apparent difference，不是自动覆盖或真实冲突裁决。

## 汇总

| 处置路线 | 数量 | 含义 |
| --- | ---: | --- |
| `needs-source-and-explicit-approval` | 2,323 | 有需求候选语义，但来源权威与最终批准均未建立 |
| `hold-for-conflict-decision` | 59 | 命中明确冲突指针，批准前必须先裁决 |
| `needs-question-resolution` | 172 | 文档自身标明未决，不能改写成肯定要求 |
| `needs-signature-source-and-explicit-approval` | 70 | 项目特定协议条款缺签署/生效与最终批准 |
| `needs-signature-scope-and-explicit-approval` | 67 | 通用协议模板义务还需证明适用于本项目 |
| `evidence-only` | 187 | 历史状态、来源、治理或项目计划证据 |
| `exclude-from-requirement-approval` | 213 | 内部设计或运行时组织方式，不从自身批准为需求 |

13 份来源逐份有记录，候选 ID 零重复，915 条后出现记录已指向相同规范化文本的首条记录；这只处理精确重复，不表示 915 条可直接删除或合并。

## 复核

在仓库根目录使用工作区依赖提供的 Python 运行：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r01_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=3091`、`sources=13`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=915`、`conflict_rows=82`，并给出 13 个来源各自的记录数。`--verify-only` 会重新抽取全部来源并逐字段比较现有主账，任何来源哈希漂移、生成结果漂移、批准升级或声明指纹失配都会失败。

R03 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r03_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=3095`、`sources=46`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=167`、`conflict_rows=49`，并给出 46 个来源各自的记录数。

R04 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r04_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=1192`、`sources=31`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=49`、`conflict_rows=5`，并验证 146 个 Acceptance Criteria 定位与 31 个来源的 UC/BR 指针。

R05 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r05_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=401`、`sources=67`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=5`、`conflict_or_traceability_rows=66`，并验证 67 份来源都同时覆盖前置、动作、结果和验证指针四种场景角色。

R06 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r06_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=229`、`scenario_rows=225`、`new_identity_candidates=4`、`sources=52`、`historical_sources=4`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=14`、`evidence_or_scope_rows=72`，并验证 52 份草案都覆盖四种场景角色、当前 `FR-016` 四类语义拥有新身份、旧 `TC-044`～`TC-047` 保持历史隔离。

R07 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r07_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=5`、`sources=2`、`excluded_not_extracted=13`、`duplicates=0`、`approval_upgrades=0`、`missing_related_tc_rows=5`，并验证 NFR-001 的 2 个 FC、NFR-002 的 3 个 FC、全部 TBD/范围/验证指针和 13 份不提取材料的路由边界。

R08 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r08_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=1217`、`sources=19`、`excluded_not_extracted=38`、`context_terms=130`、`glossary_table_rows=109`、`exact_duplicate_rows=49`、`reframed=29->72`、`mixed_route_remaining=0`、`approval_upgrades=0`，并验证 19 份来源全覆盖、旧术语表全部留在历史证据路由、29 个原混合候选逐一保留原 ID/指纹来源链、全部记录保持未批准，以及 `RES-R08-001/002/003`、`EVID-R08-001` 的指针命中。

R09 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r09_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=166`、`sources=12`、`excluded_not_extracted=6`、`exact_duplicate_rows=11`、`approval_upgrades=0`，并验证 12 份来源全覆盖、6 份纯技术/索引材料不提取、所有记录保持未批准、24 条本地技术决定隔离，以及 `CF-R01-001/002`、`CF-R09-001/002`、`RES-R09-001/002`、`EVID-R09-001` 的指针命中。

R10 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r10_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=728`、`sources=16`、`excluded_not_extracted=30`、`exact_duplicate_rows=11`、`approval_upgrades=0`，并验证 16 份候选来源全覆盖、30 份 DR/设计/测试/计划/索引/模板/供应商材料不抽取、全部记录保持未批准，以及 `BOUND-R10-001`、`EVID-R10-001`、`SCOPE-R10-001`、`CF-R10-001`、`GAP-R10-001` 的指针命中。

R11 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r11_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=150`、`sources=6`、`excluded_not_extracted=5`、`capacity_rules=28`、`exact_duplicate_rows=2`、`approval_upgrades=0`，并验证 6 份候选来源全覆盖、5 份索引/生成视图/run 不重复抽取、27 条 exact 与 1 条 prefix 容量规则逐行保留、全部记录保持未批准，以及 `CF-R01-001/002`、`RES-R11-001`、`BOUND-R11-001`、`EVID-R11-001/002`、`SCOPE-R11-001`、`GAP-R11-001` 的指针命中。

R12 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r12_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=300`、`sources=2`、`excluded_not_extracted=48`、`phase1_stories=50`、`watch_semantics=8`、`watch_fr_items=65`、`exact_duplicate_rows=1`、`approval_upgrades=0`，并验证 2 份混合 spec 全覆盖、31 张实施/偏差修复票与 17 张评审修复票不提取、全部记录保持未批准，以及 `CF-R01-001/002`、`AD-R01-001`、`RES-R08-003`、`RES-R11-001`、`BOUND-R11-001`、`EVID-R11-001`、`BOUND-R12-001` 的指针命中。

## R13 拆分与分类边界

- 只从总账固定的 16 份候选提取：`R13-01`、`R13-04` 和 14 份受控 OpenAPI 原始快照；两份已忽略供应商手册、三份本地 SDK 设计/测试文档、一份规范化生成输入和四份 SDK schema 副本继续留在排除路线。
- 14 份 OpenAPI 按 exact method + path 一行一个 operation，共 550 行；每行保留 operationId、summary、tags、参数、request body、responses、security、快照、环境与源 build。OpenAPI 中存在接口绝不等于项目获准调用。
- 封闭白名单只把 20 个项目 operation 标为已批准集成行为证据，把登录/刷新 token 两个 operation 标为仅人工应急的条件式鉴权备用；其余 528 个 operation 一律为 `not-authorized`。所有 schema 行仍保持 `not-approved`，因为 schema 不是项目批准记录，批准来源只由 `RES-R13-API-001` 指向的决策票承载。
- `R13-01` 的平台描述、项目使用方式、环境访问、接口发现、凭据与仓库导航分别拆分；`admin/admin` 只保留为不安全示例，不得进入生产配置或基线。
- `R13-04` 的静态枚举内容、跳号/不一致/无说明字段、修复建议和旧处置结论分别拆分。原始 TSL 以路径、53,458 字节和 SHA-256 作为补充证据接入，但来源版本、环境、build、固件和 8005 适用性仍未绑定；补枚举、黑盒反推或应用层建议不得升级为权威语义，冲突处由票据 38/39 的答案覆盖。
- `R13-23`～`R13-26` 分别与 `R13-06`、`R13-09`、`R13-13`、`R13-16` 字节相同，按哈希映射后不重复生成 operation 候选；`.normalized/imap.json` 内容不同但属于本地生成输入，也不冒充原始快照。

## R13 汇总

| 项目 | 数量 |
| --- | ---: |
| 原子记录 | 672 |
| OpenAPI operation | 550 |
| Markdown 原子声明 | 122 |
| 获批项目 operation | 20 |
| 条件式人工应急鉴权 operation | 2 |
| 未授权 operation | 528 |
| 未提取的排除文档 | 10 |
| 去重的字节相同 schema 副本 | 4 |
| 精确重复后出现记录 | 15 |
| 批准升级 | 0 |

R13 使用同一运行方式：

```powershell
& '<workspace-python>' '.scratch\current-requirements-baseline\evidence\atomic-candidates\build_and_verify_r13_atomic_candidates.py' --verify-only
```

成功结果必须报告 `total=672`、`sources=16`、`openapi_operations=550`、`markdown=122`、`excluded_not_extracted=10`、`schema_copies_deduped=4`、`not-authorized=528`、`exact_duplicate_rows=15`、`approval_upgrades=0`，并验证 16 份候选全覆盖、14 份 schema 均缺 `info.version` 且绑定受控 snapshot/environment/source build、四份副本字节相同、补充 TSL 身份与哈希不漂移，以及 `BOUND-R13-001`、`RES-R13-ENV-001`、`RES-R13-API-001`、`RES-R13-TSL-001`、`RES-R13-ENUM-001`、`SECRET-R13-001`、`ALIAS-R13-001`、`OVERRIDE-R13-001` 的指针命中。
