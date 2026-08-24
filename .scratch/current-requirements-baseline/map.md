# 当前需求基线恢复与版本化治理

Label: wayfinder:map

## Destination

建立首个版本化的“当前需求基线”：在不修改、合并、删除或重写原始需求文档的前提下，只收录经最终批准、来源与适用范围可核查、且已消除已知真实冲突的需求条目，作为后续车载端、服务端与共同协议 spec 的可信输入；同时建立以后新增、修改、废弃需求并发布新基线版本的治理方式。

## Notes

- 本地图只规划并恢复需求基线，不设计系统、不编写正式 spec、不开发代码。
- 使用 `grilling` 处理一切需要业务判断或最终批准的决定；AI 不得代替批准人回答。
- 使用 `domain-modeling` 检查领域词汇，但现有 `CONTEXT.md` 与 ADR 在完成来源和批准状态验证前不自动视为权威需求。
- 根 `CONTEXT.md` 必须始终保持为 Matt Skills 的唯一运行时领域词汇入口；治理不得改变其既有读取路径或把旧术语表恢复为平行入口。
- Matt Skills 的术语闭环是本地图硬约束：术语经 `grilling`/`domain-modeling` 澄清和用户批准后即时写回 `CONTEXT.md`，下游 Skills 消费后发现的冲突再回到同一闭环；任何破坏闭环的决定必须升级给用户。
- 证据盘点采用宽口径：当前工作目录中的全部需求性材料，加上验证其来源、批准状态、适用范围、废弃关系或冲突所必需的历史证据。
- 当前 Git 基点（制图时观察）：分支 `szy_document_dev`，HEAD `1469d6309d00b0abb792f6cd686aed68286e638e`。正式证据快照由独立票据生成。
- 当前工作区已有未提交代码修改；它们属于用户现有工作，只登记为工作区状态，不作为正确需求，也不得被本地图工作覆盖。
- 地图与票据是本次新建的治理记录，不代表相关规则在历史上已经存在。
- 用户于 2026-08-03 明确供应商手册可忽略；本次只为无损性保留其路径、哈希与来源记录，不再把手册内容作为当前基线候选、外部约束来源或继续调查对象。

## Decisions so far

- [确定权威等级与分类证据规则](issues/01-authority-and-classification-evidence-rules.md) — 权威性只能来自具名、范围明确且版本绑定的可核查批准证据，不能由文档外观、时间或代码行为推断。
- [确定需求证据盘点边界](issues/02-requirement-evidence-universe.md) — 盘点当前仓库全部需求性材料，并仅在验证当前状态所需时追溯历史或外部引用。
- [确定当前基线的最终批准人](issues/03-final-baseline-approver.md) — 本次基线默认且唯一最终批准人为用户本人，除非其明确认可其他人的授权范围。
- [确定需求确认的条目粒度](issues/04-atomic-requirement-approval-granularity.md) — 默认按可独立判断的需求条目确认，不把整份文档自动视作同一权威单元。
- [确定冲突判定与升级规则](issues/05-conflict-classification-and-hitl-escalation.md) — 只有证据证明范围或版本不同才能判为表面冲突；真实冲突逐项进入 HITL。
- [确定当前基线的历史回溯边界](issues/06-current-baseline-history-boundary.md) — 不恢复完整历史基线，只按需追溯验证当前文档所必需的历史证据。
- [确定当前文档集合的快照方式](issues/07-current-document-snapshot-method.md) — 以实际工作目录、Git 基点、工作区状态和逐文件哈希共同固定盘点对象。
- [确定版本化基线模式](issues/08-versioned-baseline-model.md) — 固定每个已批准版本而非永久冻结需求；未来变更经审查后发布新的当前基线版本。
- [决定基线版本的存储与变更治理形式](issues/09-baseline-release-storage-and-change-governance.md) — 采用不可变版本快照、唯一当前指针、三段式版本号、四项发布凭据、永久需求 ID 与受控变更门禁。
- [固定初始需求证据快照](issues/10-capture-initial-evidence-snapshot.md) — 已固定 Git 基点、原始工作区状态及 1,809 个候选文档的版本控制状态与 SHA-256，独立复核无差异。
- [建立当前需求性材料的无损清单](issues/11-inventory-current-requirement-materials.md) — 1,809 条快照材料已零漏项路由为 13 个候选调查批次、5 个现状证据批次和 1 个仓库治理批次。
- [建立基线条目与变更提案模板](issues/12-create-baseline-record-templates.md) — 已把双层需求记录、永久 ID、独立发布凭据和七步变更门禁固化为可复核模板。
- [调查客户、项目协议与原始需求输入](issues/13-investigate-customer-project-source-materials.md) — R01 的 19 份材料均已逐件分类，但现有证据不足以在文档级批准任何当前需求。
- [调查需求库框架、愿景、干系人与业务规则](issues/14-investigate-requirements-framing-and-business-rules.md) — R02 的 27 份材料已逐件分类为记录结构、导航索引或内部派生材料，且均缺少完整批准链。
- [调查用例材料](issues/15-investigate-use-cases.md) — R03 的 48 份材料已分类为 22 份可送审 UC 候选、24 份内部设计推演、1 份指南与 1 份空白待办，且均无完整批准链。
- [调查功能需求材料](issues/16-investigate-functional-requirements.md) — R04 的 41 份材料已分类为 31 份未批准的内部派生 FR 候选、8 份占位 README、1 份写作指南与 1 份导航索引。
- [调查现场操作验收场景](issues/17-investigate-site-operation-acceptance-scenarios.md) — R05 的 67 份材料均为未批准且未执行的内部派生验收草案，其中至少 29 份显著固化内部设计。
- [调查仓位、硬件、车队及其余测试案例](issues/18-investigate-slot-hardware-fleet-acceptance-scenarios.md) — R06 的 65 份材料含 52 个未批准草稿候选、4 个派生漂移旧稿、8 个占位和 1 个索引，且没有测试执行证据。
- [调查追溯规则与非功能需求](issues/19-investigate-traceability-and-nonfunctional-requirements.md) — R07 仅有 2 份未批准 NFR 候选共 5 个 FC；其余材料是动态追溯、记录结构、索引或空白占位。
- [调查跨域词汇与架构决定](issues/20-investigate-cross-domain-vocabulary-and-decisions.md) — R08 的 57 份材料均无完整批准链，已区分业务候选、领域/物理事实与纯设计，并把三项明确不一致移入独立票据。
- [调查 MES 与 SDK 架构决定](issues/21-investigate-mes-sdk-decisions.md) — R09 的 18 份材料含 7 个需求/外部约束候选、5 个混合决定、5 个本地设计和 1 个索引，且均无完整批准链。
- [调查仓位模拟器需求与决定](issues/22-investigate-slot-simulator-materials.md) — R10 的 46 份材料主要是未实现且未批准的模拟器规划；其中供应商手册按用户后续指示仅保留清单记录，不进入当前基线判断。
- [调查 MES 数据、查询与工厂验证约束](issues/23-investigate-mes-data-query-validation-constraints.md) — R11 的 11 份材料已分离外部数据约束、验收候选、派生设计与限定环境证据，并把批准/哈希门槛冲突移入独立票据。
- [调查历史本地 spec 与实施票据](issues/24-investigate-historical-local-specs-and-issues.md) — R12 的 2 份 spec 仅是混合型决定摘要，48 张 issue 只保存实施、修复或实现偏差历史，50 份材料均无完整批准链。
- [调查 RIoT 外部接口与 SDK 约束](issues/25-investigate-riot-interface-sdk-constraints.md) — R13 的 26 份材料均无完整批准链；2 份供应商 PDF 已按用户指示排除，其余静态 schema、SDK 设计与观察证据不得反推项目需求。
- [修正初始快照的 Git 状态分类](issues/26-correct-initial-snapshot-git-status-classification.md) — 已用追加覆盖层把 58 条 Unicode 路径由假 `untracked` 修正为 `tracked-clean`，有效统计为 1762/47 且验证无残留。
- [决定操作员上下文的清除时点](issues/27-decide-operator-context-clear-boundary.md) — `OnboardOperatorContext` 与一次到站的 `OperationSession` 共用 `StopClosureCommit` 结束边界，断线与重启保留、下一停靠按策略重新核验。
- [决定装货待整批确认阶段是否存在](issues/28-decide-awaiting-load-confirmation-stage.md) — 单个 Sublot 物理闭环后自动提交，后续 Sublot 在站点级等待中继续输入，普通取消以 `StopClosureCommit` 为最晚边界。
- [确定领域词汇唯一入口与旧术语表关系](issues/29-decide-canonical-domain-vocabulary-source.md) — 根 `CONTEXT.md` 是 Matt Skills 唯一工作词汇入口，旧术语表只保留历史证据，术语经用户逐条批准并按固定闭环演进。
- [决定工厂 MES 验证的批准与完整性证据门槛](issues/30-decide-mes-factory-validation-approval-and-integrity-evidence.md) — 登记的只读查询可无逐次审批自行运行；run 只作限定环境参考，需求入基线仍须锁定来源并由用户逐项批准。
- [建立 R01–R05 文档级证据分类账](issues/31-classify-r01-r05-documents.md) — 已把 202 份材料零漏项归一到统一分类账，并以独立字段和失败式核验隔离文档分类、原子提取路由与最终批准。
- [建立 R06–R10 文档级证据分类账](issues/32-classify-r06-r10-documents.md) — 已把 201 份材料零漏项归一到统一分类账，并分别隔离测试草案、ADR/设计、模拟器规划、主系统线索与已排除的供应商资料。
- [建立 R11–R13 文档级证据分类账](issues/33-classify-r11-r13-documents.md) — 已把 87 份材料零漏项归一到统一分类账，并隔离 MES 外部约束/现状、历史实施票、待绑定 RIoT schema、SDK 派生物与已排除的供应商资料。
- [合并并核验文档级证据分类账](issues/34-consolidate-document-evidence-classification-ledger.md) — 490 份调查材料已零漏项、零重复归并为可复核总账，并安全分流为 301 份候选、4 份阻塞和 185 份不提取。
- [补齐 8005 仓位硬件身份与现场信号证据](issues/35-supply-slot-hardware-and-field-signal-evidence.md) — 用户直接确认 8005 全部 AGV 的八仓 IO、信号语义与机构事实，并限定未来车型须使用独立的可变绑定与极性。
- [补齐 RIoT 目标环境与受控接口快照证据](issues/36-supply-riot-environment-and-controlled-interface-snapshot-evidence.md) — 已区分 8005 运行实例与跨项目测试实例，并把 14 份 OpenAPI 原始文件绑定到 8005 环境、build、导出人及逐文件哈希。
- [决定 RIoT 项目 API 白名单与调用安全边界](issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md) — 已封闭分层白名单，固定单车订单名额、急停保持/解除、凭证治理、跨 build 兼容及结果确认规则。
- [补齐 standard.oasis.300ul 物模型枚举证据](issues/38-supply-standard-oasis-300ul-thing-model-evidence.md) — 已补登记原始 TSL 并固定其字节内容，同时明确来源版本未绑定时缺号、差异和错误码语义必须保持未知。
- [决定未知物模型枚举值的项目处理规则](issues/39-decide-unknown-thing-model-enum-handling.md) — 未识别值保留原值并按依赖范围阻断，安全不可证明时升级整车阻断，且仅可凭版本绑定证据和再次批准升级为已知。
- [决定 R06 上游漂移旧稿的版本归属与去留](issues/40-decide-r06-upstream-drifted-test-case-version-scope.md) — `TC-044`～`TC-047` 不改写并绑定为旧 `FR-016` 的未批准历史验收草案，当前验收语义使用新身份候选另行分类与批准。
- [拆分并分类客户、项目协议与原始输入的原子候选](issues/41-classify-r01-atomic-candidates.md) — 13 份 R01 来源已拆为 3,091 条未批准原子声明，精确重复、来源差异、未签署协议与四组冲突/版本线索均已隔离并可复核。
- [拆分并分类需求框架、愿景与业务规则的原子候选](issues/42-classify-r02-atomic-candidates.md) — 19 份 R02 来源已拆为 1,206 条未批准原子声明，并隔离用户澄清摘要、内部建模、上游派生及四组既有冲突/版本指针。
- [拆分并分类用例与流程的原子候选](issues/43-classify-r03-atomic-candidates.md) — 46 份 R03 来源已拆为 3,095 条未批准原子声明，并隔离业务用例行为、内部设计推演、50 条未决问题及四组既有冲突/版本指针。
- [拆分并分类功能需求的原子候选](issues/44-classify-r04-atomic-candidates.md) — 31 份 R04 来源已拆为 1,192 条未批准记录，固定 146 个 AC 定位、28 个唯一 UC/BR 上游指针及既有冲突/版本路由。
- [拆分并分类现场操作验收场景的原子候选](issues/45-classify-r05-atomic-candidates.md) — 67 份 R05 草稿已拆为 401 条未批准场景声明与追踪证据，并隔离业务、身份安全、硬件安全、接口、HMI、内部设计及既有冲突线索。
- [拆分并分类仓位、硬件与车队验收的原子候选](issues/46-classify-r06-atomic-candidates.md) — 52 份 R06 草稿已拆为 225 条场景记录，四份旧 TC 固定为历史证据，并以四个新身份隔离当前 FR-016 验收语义。
- [拆分并分类非功能需求的原子候选](issues/47-classify-r07-atomic-candidates.md) — NFR-001/002 已拆为 5 个未批准 FC，固定质量属性、度量/范围、TBD 阈值、责任批准与缺失验证证据。
- [拆分并分类跨域词汇、业务与物理事实的原子候选](issues/48-classify-r08-atomic-candidates.md) — 19 份 R08 来源已拆为 1,174 条未批准记录，并隔离词汇闭环、业务/物理/权限候选、技术设计、旧术语证据及 29 条待重新原子化的混合声明。
- [拆分并分类 MES 与 SDK 业务及外部约束的原子候选](issues/49-classify-r09-atomic-candidates.md) — 12 份 R09 候选 ADR 已拆为 166 条未批准记录，并分离业务规则、外部契约、安全边界、产品范围、证据与 24 条纯本地技术设计。
- [拆分并分类仓位模拟器范围需求的原子候选](issues/50-classify-r10-atomic-candidates.md) — 16 份 R10 候选已拆为 728 条未批准记录，并隔离模拟器范围、主系统/现场线索、供应商内容、技术设计与预留测试计划。
- [拆分并分类 MES 数据、查询与工厂验证的原子候选](issues/51-classify-r11-atomic-candidates.md) — 6 份 R11 来源已拆为 150 条未批准记录，并严格分离外部数据契约、查询/工具设计、容量与装载安全、验收条件、限定 run 观察及批准边界。
- [拆分并分类历史本地 spec 需求摘要的原子候选](issues/52-classify-r12-atomic-candidates.md) — 2 份历史混合 spec 已拆为 300 条未批准记录，覆盖 50 个 Phase 1 story、8 个 Watch 语义来源项和 65 个 FR 来源项，并将 48 张实施/评审票继续隔离为历史证据。
- [拆分并分类 RIoT 受控接口、集成与物模型的原子候选](issues/53-classify-r13-atomic-candidates.md) — 16 份来源已拆为 672 条未批准记录，逐 operation 隔离 20 个获批项目调用、2 个应急鉴权备用、528 个未授权调用及物模型未知边界，并去重四份 schema 副本。
- [拆分 R08 业务义务与技术机制混合声明](issues/54-reframe-r08-mixed-business-and-technical-claims.md) — 29 条混合声明已可追溯拆为 72 条业务、领域、产品或技术单一候选，混合路线清零且无批准升级。
- [合并并语义去重 R01–R13 原子候选](issues/55-consolidate-and-semantically-deduplicate-r01-r13-atomic-candidates.md) — 12,452 条已零删除、零批准升级归并，关系/审阅簇、冲突毕业和 102 个批准批次建议均可重建复核。
- [决定运输需求身份、对账键与取消抑制边界](issues/56-decide-transport-demand-identity-reconcile-key-and-cancellation-suppression-boundary.md) — 已固定 TransportDemandKey、DemandId、快照冲突、GONE 再现与四类本地取消永久抑制的职责，并绑定当前 8005 MES 查询契约。
- [决定当前 MES 只读与卸货、完工回写边界](issues/57-decide-current-mes-readonly-and-completion-writeback-boundary.md) — 当前 8005 严格只读 MES；目的站既有流程独立负责后续 MES 操作，8005 无提示、不等待且不建立后续待办或专门审计。
- [决定 QUEUEING 滞留与下单前清积压策略](issues/58-decide-queueing-stall-and-pre-dispatch-backlog-cleanup-policy.md) — 0/1 是硬下单门禁而非自动清理目标；已知且安全可证明的暂时阻断自动恢复，其余保留现场并升级，超时、FAILED 和低电量均不授权清积压。
- [补齐并验证 QUEUEING 长期滞留原因诊断 API](issues/60-supply-and-validate-queueing-stall-reason-api.md) — 已绑定 build 2.2.0.30，固定字符串 orderId、诊断短路与 fail-closed 映射；自由文本和 suggestList 只作证据，不能授权动作。
- [验证有界的 RIoT 充电桩占用与目标监控接口](issues/61-validate-bounded-riot-charging-station-occupancy-and-target-monitoring.md) — 测试环境快照可有界识别已在桩上的外部车辆，但未证明 CHARGE 在途目标、新鲜度、服务端负载或目标 build 适用性，不能单独证明空闲。
- [决定充电失败改派的备用桩筛选与排队关系](issues/59-decide-charge-failure-reassignment-station-filter-and-queueing-policy.md) — 改派与普通待充共用独占桩资格链和电量队列，原子预占不可抢占，充电失败后全车暂停该桩并仅可经现场审计恢复。
- [决定无联网充电桩的充电失败确认与暂停触发边界](issues/62-decide-offline-charger-failure-confirmation-and-allocation-hold-trigger.md) — 严格到桩充电失败事实或 R-11 现场确认才触发全车暂停，清桩可由到达等待点或受权人工确认闭环，桩与车随后依各自事实独立恢复。
- [复核冲突决定后仍待问题解决或重构的 241 条记录](issues/63-review-post-conflict-unresolved-question-and-reframing-records.md) — 241 条零遗漏归档为六类处置，86 条原子问题经一次错路由更正后收敛为 17 张 HITL 票，且原文、未批准状态和证据边界均未漂移。
- [决定 MES 运输候选的业务纳入与排除边界](issues/64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md) — 全厂 SQL 候选、字段完整性、PACKAGE 覆盖和 AREA→EQP 唯一性已分层封闭，AREA 执行名册后续由分区决定统一收敛。
- [决定复合运输、分区与多 SUBLOT 组合边界](issues/65-decide-composite-transport-zoning-and-multi-sublot-boundary.md) — 已固定独立 Demand 混载、Map→分区→AREA 执行链、车辆软硬准入、分区连续性、受控计划变更和分区级顺路延迟门禁。
- [决定派车评分、路网成本与无车响应升级规则](issues/66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md) — 采用任务优先的分层字典序、本地连续等待与分区现场标定防饥饿，并以在点软层、可比新增路程、分区偏好、公平性及末级电量完成确定性选车。
- [决定同站多任务取消与人工选任务开门边界](issues/67-decide-same-station-cancellation-and-operator-task-opening.md) — 取消继续按 DemandId 精确执行并按 TransportDemandKey 永久抑制；项目级入口模式在 SUBLOT 输入与受审计的作业清单选任务之间互斥切换。
- [决定到站拒收、取消与完工后纠错边界](issues/68-decide-destination-rejection-cancellation-and-post-completion-correction.md) — 到站直接卸货且无拒收或取消分支，业务差错不重送；无业务绑定仓位仅在受控维护开门模式中处理，漏检仓位隔离至维护恢复，MES 始终只读。
- [决定故障车辆隔离、货物处置与人工越权边界](issues/69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md) — 以一次身份验证的异常处置会话统一故障隔离、载货救援和强制机械取出，并用恢复代次把货物业务闭环与设备复原分离。
- [决定安全联锁失败升级与紧急停止边界](issues/70-decide-safety-interlock-failure-escalation-and-emergency-stop.md) — 仓内光幕退出安全联锁；仓门或故障停车义务无法取得停稳证明时立即升级软件急停，并以来源、全因消除、现场兜底和完整对账控制保持与解除。
- [决定人员登录、维护操作与高风险权限边界](issues/71-decide-human-login-maintenance-and-high-risk-permission-boundary.md) — 当前收敛为操作员工号识别、维护管理员和系统管理员三种身份，以一人一号、单会话、统一异常权限、即时撤权和不可改写审计控制高风险操作。
- [决定仓位模型与 IO 映射配置、验证和启用门禁](issues/72-decide-slot-io-mapping-activation-and-maintenance-policy.md) — 采用服务端两层共享模板与两级变更治理，只有硬件相关变化进入整车隔离、全量实测和原子激活，且不提供文件导入。
- [决定监控新鲜度、告警升级、重试与日志留存规则](issues/73-decide-monitoring-freshness-alert-retry-and-log-retention.md) — 车队/仓位看板采用 2 秒非重入刷新和明确不可用原因，告警按现有角色可见，业务审计与车载技术日志分别至少保留 180/30 天，MES 运维定义及调用特定重试转交对应后续票据。
- [决定账户恢复与密码增强策略](issues/74-decide-account-recovery-and-password-hardening-policy.md) — 当前只允许系统管理员按统一基础格式设置密码，首次改密仅用于具名系统管理员部署初始化；不做泄露恢复、策略增强或会话自动超时。
- [决定充电阈值、配置变更与异常生命周期](issues/75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md) — 固定 `C > T ≥ M`、版本化策略、充电异常双向隔离、失联不自动释放及维修暂停边界，禁止原桩盲重试和车辆逐桩试错。
- [决定归档 AGV 的恢复与身份连续性](issues/78-decide-archived-agv-restoration-and-identity-continuity.md) — 恢复沿用唯一 `agvId` 并开启新生命周期代次，RIoT 绑定可换版、运行态清零、历史保留，且只有系统管理员能在完整阻断、核验和审计边界内恢复。
- [决定 AREA 显式覆盖的维护与生效治理](issues/79-decide-area-override-maintenance-and-effectivity-governance.md) — 当前 8005 不提供 AREA 显式覆盖；机台站点只按 AREA 命名规则识别，公共业务点改用 PublicStationFunction 到 FixedTaskStation 的独立显式绑定。
- [决定 RIoT 建单未确认时任务绑定、重试与释放边界](issues/80-decide-riot-order-creation-uncertainty-binding-retry-release.md) — 以 DispatchGeneration 和稳定 `upperId` 封闭建单确认，只在唯一匹配订单通过接管核验后进入进行中，并对拒绝、双重未知、重试暂停、终态对账及重派建立唯一性与审计门禁。

## Not yet specified

- 开放 HITL 决策全部解决并形成规范候选基线条目后，依据当前 102 个可审查批次建议生成最终批准票据；批次可随规范条目数量和责任边界调整，只有批准结果可以进入首个基线版本。
- 批准完成后，生成首个可独立阅读、保留统一规范文本与不可变原始证据的当前需求基线版本；具体发布任务等待候选条目与批准批次明确后再生成。

## Out of scope

- 车载端、服务端和共同协议的正式 spec 编写。
- 系统设计、架构选择、接口设计和代码开发。
- 将当前代码行为自动认定为正确需求。
- 修改、合并、删除或静默改写任何原始需求文档。
- 为来源未知、范围不明或缺少批准证据的内容补全背景或猜测含义。
- 恢复与验证当前需求无关的完整项目历史。
- 供应商手册的协议语义、版本适用性与项目绑定判断；手册文件只保留无损清单中的路径、哈希与来源记录。
- 尚未存在的未来车型的具体仓位数、传感器集合、点位和信号极性；本次只固定其不得直接继承 8005 配置的范围边界。
