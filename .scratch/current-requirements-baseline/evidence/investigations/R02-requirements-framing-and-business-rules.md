# R02 需求库框架、愿景、干系人与业务规则调查

## 调查边界与方法

本资产只调查[material-inventory.tsv](../material-inventory/material-inventory.tsv) 中 `batch_id=R02` 的 27 行：6 个模板、2 份愿景/边界文档、1 份干系人清单、15 条 BR、1 份 BR 目录、1 份流程步骤目录和 1 份需求库入口。清单字节哈希按 PowerShell `Get-FileHash -Algorithm SHA256 -LiteralPath <path>` 在当前工作树重算，**27/27 匹配，0 漂移**。哈希、字节数、`last_write_utc` 和快照 `git_status` 均以清单为准；下表只写 SHA-256 前 12 位便于阅读。

分类依据[01 权威与分类规则](../../issues/01-authority-and-classification-evidence-rules.md)、[04 原子批准粒度](../../issues/04-atomic-requirement-approval-granularity.md)与[06 历史边界](../../issues/06-current-baseline-history-boundary.md)：只有具名授权人、日期、适用范围和具体版本/等价对象绑定的可核查批准才能赋予权威性。**Git 作者/提交者、提交说明、frontmatter `status`、文内 `Source`/“已确认”自述、链接完整性和实现现状都不是批准。**

## 形成历史总览

R02 主体在五个可核查提交中形成：`96eb203` (2026-07-13 08:32 +08:00，首次引入需求库、早期模板/愿景/BR)；`0b2246c` (2026-07-13 13:18，加入系统边界、工作流规则和步骤目录)；`48a74dc` (2026-07-14 08:17，加入 AREA、仓位模型、停靠/充电等并修改多份文档)；`ecd0fd8` (2026-07-15 12:58，加入 NFR 模板、账号、MES、花篮、路径等 BR 并继续改写)；`493ac5a` (2026-07-31 18:33，修改干系人、BR-001/012/013/014、目录及需求库入口)。逐路径使用 `git log --follow --format='%h|%aI|%an|%s' --name-status -- <path>` 核对；详细序列编码在下表。

部分 BR 指向 `mes/AGV系统业务与MES任务模型.md`或 `mes/宿迁长电AGV项目MES数据接口需求确认.md`；二者在 `5718541` (2026-07-16) 成为迁移指针，当前唯一维护正文分别是 [`mes/docs/AGV系统业务与MES任务模型.md`](../../../../mes/docs/AGV系统业务与MES任务模型.md) 和 [`mes/docs/宿迁长电AGV项目MES数据接口需求确认.md`](../../../../mes/docs/宿迁长电AGV项目MES数据接口需求确认.md)。前者明说是“整合”文档并混合“已确认/建议实现/待确认”，后者声称客户 IT 提供/批准查询，但两者均未附具名批准人、批准记录、范围与版本绑定；因此这条链可证明仓库内部派生，不能证明权威批准。

## 27/27 文档级证据矩阵

编码：`96`=`96eb203`，`0b`=`0b2246c`，`48`=`48a74dc`，`ec`=`ecd0fd8`，`49`=`493ac5a`。“无”表示本批未找到合格批准，不表示内容已废弃或错误。

| # | 固定文件（SHA-256 前 12）/形成 | 来源与派生链 | 批准证据与范围 | 当前适用性、性质与后续原子指针 |
|---:|---|---|---|---|
| 01 | [template-business-rule.md](../../../../requirement-documents/_templates/template-business-rule.md) `ba14637d8a90`；`96` 新增 | Templater 脚本只生成 BR 编号、`draft` 字段与 Rule/Rationale/Source/Related 空节；全为 `TBD` | 无；不存在可批准的实例内容 | **纯记录结构/模板**；可继续用于建档，不提取需求。后续对实例逐条核实 Source。 |
| 02 | [template-decision-record.md](../../../../requirement-documents/_templates/template-decision-record.md) `ba0310a4996e`；`96` | 决策记录空壳；默认 `status: decided` 是模板字段，不是决策行为证据 | 无；默认状态未绑定任何人/日期/版本 | **纯记录结构/模板**；不得从 `decided` 反推批准。 |
| 03 | [template-functional-requirement.md](../../../../requirement-documents/_templates/template-functional-requirement.md) `ba4f4f17fd43`；`96→ec` | 扩充为含 Origin、Given/When/Then、Verification 的 FR 记录形式；内容仍为 `TBD` | 无 | **纯记录结构/模板**；只定义粒度与追溯字段，不表达 FR。 |
| 04 | [template-non-functional-requirement.md](../../../../requirement-documents/_templates/template-non-functional-requirement.md) `c53a8577b8f8`；`ec` | 定义 NFR category、metric、fit criterion、measurement/origin 字段；全为占位 | 无 | **纯记录结构/模板**；不独立生成质量目标。 |
| 05 | [template-test-case.md](../../../../requirement-documents/_templates/template-test-case.md) `640b7c2d7e8f`；`96` | 定义 Preconditions/Steps/Expected/Verifies 空结构 | 无 | **纯记录结构/模板**；不是验收结果或需求。 |
| 06 | [template-use-case.md](../../../../requirement-documents/_templates/template-use-case.md) `3b2dac1c9c77`；`96` | 定义 Actor/Flow/Assumption 等用例空结构 | 无 | **纯记录结构/模板**；不独立表达场景要求。 |
| 07 | [system-context.md](../../../../requirement-documents/00-vision/system-context.md) `60e2206dc80d`；`0b→ec` | 无 Source 节；以内部 wikilink 综合 stakeholder、UC、BR 和步骤目录，同时区分当前 MES 只读与未来回写 TBD | 无；没有图/文本版本的具名边界批准 | **来源未知的内部派生边界综合**；对 8005 系统边界有高相关性，但必须按外部实体、接口方向、当前/未来范围拆分并批准。 |
| 08 | [vision-and-scope.md](../../../../requirement-documents/00-vision/vision-and-scope.md) `c5dbdd400b99`；`96→0b→48→ec` | 无原始访谈/合同引用；混合背景叙述、8 个目标、98%/2%/3 分钟/10 分钟等指标、边界链接、具名干系人和内部派生优先级 | 无；文内人名只是 profile，无批准动作/日期/版本；初始与后续发布范围均“未定” | **来源未知的混合愿景草稿**；逐条拆背景、目标、成功指标、范围/排除、依赖与优先级，数值指标优先要求原始来源与测量口径。 |
| 09 | [stakeholders-and-user-classes.md](../../../../requirement-documents/01-stakeholders/stakeholders-and-user-classes.md) `f8d5f0ca428f`；`96→0b→48→49` | 文首自述将 vision 大类、`简易需求文档.md` 场景与后续 UC/BR 拆成 R-01…R-15；是内部角色/权限综合，不是原始花名册或授权文件 | 无；角色编号、兼任规则和二次认证均未绑定具名业务/安全批准；R-15 登录权限明示待确认 | **来源未知的内部派生角色模型**；按每个角色、职责、兼任、权限和二次认证规则拆分，追回部门负责人/权限矩阵。 |
| 10 | [BR-001](../../../../requirement-documents/02-business-rules/br-001-dispatch-task-range.md) `e90caa36f480`；`96→0b→ec→49` | Source 将 2026-07-14 复合停靠等追到 MES 模型第 8 节，早期部分仅写“客户现场访谈、AGV/RIOT 调度方案”，无访谈原件 | 无；`status: draft`，“已确认”小标未绑定人/记录/版本 | **部分可追至未批准内部上游的派生 BR**；拆分任务范围、复合停靠、等待、车载可见性和各 TBD。 |
| 11 | [BR-002](../../../../requirement-documents/02-business-rules/br-002-agv-allocation-eligibility.md) `dd3acb8484ed`；`0b→48→ec` | Source 只有“2026-07-13 需求确认”摘要，另由 BR-014/015 派生优先级/路径排序 | 无；无具名确认记录或适用车型/环境范围 | **来源未知的内部综合 BR**；将硬性可分配条件与软排序因子分开原子化。 |
| 12 | [BR-003](../../../../requirement-documents/02-business-rules/br-003-area-station-mapping.md) `7b25e92d5e66`；`0b→48` | Source 列三次 2026-07-13 自述确认（初始/两表/诊断颗粒度），无会议/对话或 RCS 接口版本 | 无；无 R-12/R-13 或地图权威方批准 | **来源未知的内部建模 BR**；按表 A、表 B、编码格式、覆盖版本、冻结和 fail-closed 拆分。 |
| 13 | [BR-004](../../../../requirement-documents/02-business-rules/br-004-workflow-template-matching.md) `e10d2a634ade`；`0b→48` | Source 只有 2026-07-13 “流程模板需求确认”三点摘要；其余优先级/唯一性/fail-closed 是内部规则展开 | 无 | **来源未知的内部派生 BR**；拆匹配输入、候选范围、排序、覆盖、失败语义。 |
| 14 | [BR-005](../../../../requirement-documents/02-business-rules/br-005-workflow-template-versioning.md) `798aad13791f`；`0b` | Source 仅 2026-07-13 模板状态/不可变快照/二次认证摘要；无上游原件 | 无 | **来源未知的内部派生 BR**；状态转换、新版影响范围、迁移禁止、发布/停用分别原子化。 |
| 15 | [BR-006](../../../../requirement-documents/02-business-rules/br-006-workflow-step-execution.md) `0ff765a61ad4`；`0b` | Source 仅 2026-07-13 顺序/跳过/重试/等待、幂等/审计/fail-closed 摘要；与步骤目录同提交形成 | 无 | **来源未知的内部派生 BR**；将控制结构、状态、重试、人工处置、安全步骤拆分。 |
| 16 | [BR-007](../../../../requirement-documents/02-business-rules/br-007-charging-pile-allocation-and-queueing.md) `a5cef3093c15`；`0b→48` | Source 只有 2026-07-13 本系统选桩和电量优先摘要 | 无；无车型、桩、站点和现场负责方范围 | **来源未知的内部排队 BR**；资源占用、排序、可/不可抢占分开批准。 |
| 17 | [BR-008](../../../../requirement-documents/02-business-rules/br-008-agv-slot-model-versioning.md) `5f8911ad0f36`；`48` | Source 自述“用户提出/确认”，并明说仓位定义“参照 `slots-simulator`”、版本做法参照 BR-005；这是需求摘要+实现/内部类比的混合链 | 无；实现参照不赋予业务批准 | **来源未知的混合派生 BR**；将仓位业务属性与模拟器设计选择分开。 |
| 18 | [BR-009](../../../../requirement-documents/02-business-rules/br-009-parking-point-allocation-and-queueing.md) `bc212f95287f`；`48` | Source 只有 2026-07-13 触发/候选/优先级摘要；排队结构明说参照 BR-007，FIFO 是内部差异化设计 | 无 | **来源未知的类比派生 BR**；停靠触发、候选有效性、FIFO、优先级与并发锁分开。 |
| 19 | [BR-010](../../../../requirement-documents/02-business-rules/br-010-default-administrator-account.md) `9843f98e918e`；`ec` | Source 写 2026-07-14 “与用户澄清问答”，但不含对话记录、用户身份或版本指针 | 无；安全影响大但无 IT/安全授权人批准 | **来源未知的用户澄清摘要/BR**；账号唯一性、不可停用、初始密码、超级权限、审计逐项确认。 |
| 20 | [BR-011](../../../../requirement-documents/02-business-rules/br-011-account-and-password-format.md) `e5a2ae6c041d`；`ec` | Source 明确只把“英文+数字、不高复杂度/定期更换”称为确认；**其余登录名格式、密码长度、保留标识和存储方式自述为“需求工程常规基线拟定”** | 无；即使自述确认的最低密码部分也无具名记录 | **原始要求摘要与纯分析派生混合 BR**；两类必须分开原子化，不得整份确认。 |
| 21 | [BR-012](../../../../requirement-documents/02-business-rules/br-012-mes-task-idempotency-and-reconciliation.md) `d8f77fc533fd`；`ec→49` | Source 指向 MES 模型第 4–7/12–13 节，同时引用“10 轮平均约 3.13s”实测；上游是混合综合文档，性能观察也不等于要求批准 | 无；未绑定客户 IT 批准的 SQL/查询目录版本 | **可追至未批准内部上游的派生 BR**；幂等键、轮询、消失、冻结、上线基线、Mock、只读和性能目标/观察分开。 |
| 22 | [BR-013](../../../../requirement-documents/02-business-rules/br-013-multi-basket-loading.md) `ac51b3a50f7b`；`ec→49` | Source 指向 MES 模型第 9/13.3 节的 2026-07-31 “业务确认”摘要；无原始业务记录 | 无 | **可追至未批准内部上游的派生 BR**；花篮身份、数量权威、换算、仓位占用、批量开门分开。 |
| 23 | [BR-014](../../../../requirement-documents/02-business-rules/br-014-transport-task-types-and-fixed-stations.md) `98cd58e70e4a`；`ec→49` | Source 指向 MES 模型和 MES 接口确认文档；两个当前路径的迁移指针可追至 `mes/docs`，但上游没有合格批准链 | 无；“第六类于 2026-07-24 加入正式查询”是形成声明，非批准记录 | **可追至未批准内部上游的派生 BR**；六个任务类型、每个起/终点、固定站、优先级和上下游等待逐项核实。 |
| 24 | [BR-015](../../../../requirement-documents/02-business-rules/br-015-path-cost-and-dispatch-ranking.md) `5b6708cec847`；`ec` | Source 只有 2026-07-14 从 RIOT 读路网并与紧急度权衡的自述确认；无 RIOT API/地图版本或会议记录 | 无 | **来源未知的内部派生 BR**；路径成本定义、权重、硬优先级、降级和 TBD 分开确认。 |
| 25 | [02-business-rules/README.md](../../../../requirement-documents/02-business-rules/README.md) `9a99ee7f963b`；`96→ec→49` | 说明目录、模板、Dataview 用法，只列 BR-001 及 BR-012–015，未无损索引全部 15 条 BR；条目摘要是下游文档的重复 | 无 | **不完整导航索引/记录结构**；不独立提取需求，后续只用于指向原 BR，并勘误缺失链接。 |
| 26 | [workflow-step-catalog.md](../../../../requirement-documents/02-business-rules/workflow-step-catalog.md) `c62f70569c04`；`0b→48→ec→49` | `type: reference,status: draft`；无 Source 节，通过 UC/BR 链接派生步骤类型，但同时新增可跳过/重试、输入输出和安全边界等规范性内容；`catalog_version` 仍为 `2026.07.13`，与后续多次实质修改未绑定 | 无；无软件发布/安全评审记录或目录版本哈希 | **内部派生规范/参考目录，非纯索引**；按每个步骤类型的语义、安全标记、幂等/重试和上游 UC/BR 逐项核实。 |
| 27 | [requirement-documents/README.md](../../../../requirement-documents/README.md) `b247854f21d7`；`96→0b→48→ec→49` | Obsidian vault 入口：目录结构、ID/wikilink/frontmatter、插件和编辑流程。它定义 `approved` 的字符串语义，不提供任何实例的批准记录；开头的 BR-001∼008/UC-001∼038 口径已不能完整表示当前集合 | 无；这是仓库编辑规约，不是业务授权或基线批准 | **需求库入口/编辑与索引结构**；可用于导航与工具使用，不从其生成系统需求。 |

## 分类结论与缺口

1. **原始要求：文档级 0/27 可证明。** R02 未保存可核查的原始访谈、邮件、会议纪要、客户签批或对话导出。BR 中的“需求确认/业务确认/用户澄清”只是无绑定的摘要；BR-011 更明示了确认摘要与分析人员拟定内容混合。
2. **纯记录结构：6 个模板；导航/编辑索引：2 个 README。** 它们可规定如何记录，但不能独立证明记录了什么已批准需求。BR README 虽被清单路由为 candidate-requirement，实际内容仍是不完整索引。
3. **派生/综合材料：其余 19 份。** 其中 BR-001/012/013/014 有可核查的仓库内部 MES 上游，但上游仍未权威批准；其余愿景、干系人、BR 和步骤目录是无原始记录的内部综合或类比设计。没有发现足以把某具体版本分类为“AI 生成或修改但尚未确认”的直接生成记录；“供 AI 协作”或 AI 阅读用途不等于 AI 作者证据。
4. **批准：27/27 都不能凭本批证据进入当前基线。** 所以批准范围均为“未建立”，不得因 `draft`/“已确认”、同一 Git 作者或下游 UC/FR/TC 引用而升级。
5. **后续证据请求：** 对 2026-07-13/14/31 的确认提供原始对话/会议/邮件、具名发言人及授权、日期、适用 8005/车型/站点/阶段范围和对应文档哈希；对 MES 链提供客户 IT 批准的 QUERY_ID/SQL 版本、执行范围与批准记录；对 workflow catalog 提供安全评审与发布版本绑定。后续原子条目按上表指针拆分，不得整份批准；若同范围合格来源之间出现实质冲突，另建 HITL 票，本调查不自行裁决。
