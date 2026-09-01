# WIRE_TO_GATE 单场景 MVP 与双仓库协作路线图

Label: wayfinder:map

## Destination

形成一份经批准、可直接交给两名开发者及其 AI 实施的《WIRE_TO_GATE 单场景 MVP 范围与验收规格》，同时固定 ControlServer 与 OnboardHmi 分属两个仓库时的共享协议发布、双模拟对端、一致性测试、联合切片与现场验收交接方式。

## Notes

- 本地图只解决产品范围、跨端契约、协作和验收决策，最终交付规格与双仓库实施交接包；不开发 ControlServer、OnboardHmi，不创建远程共享协议仓库。
- 已发布的 `requirements/baselines/current-requirements-v1.0.0.md` 保持不可修改，`requirements/current-baseline.md` 不切换。MVP 是实施适用性剖面，不把未纳入首期的长期需求自动废弃；若未来永久改变产品范围，另走主版本需求基线流程。
- MVP 只接受 MesIngest 发布的完整 `WIRE_TO_GATE` WorkType，同时覆盖焊线与键合；下游不按 STEP、EQP 或文本二次分类。
- MVP 同一时刻只执行一个 TransportDemand／Sublot，但允许该 Sublot 使用其需要的多个安全可用仓位；不假设每个 Sublot 只占一仓。
- 最终验收为受控工厂试运行：先通过离线与假接口门禁，再用一台指定 AGV、一张 Map、真实 MesIngest、RIoT 和物料完成一次机台取货到关卡卸货。
- 机台取货通过 OnboardHmi 与车载扫码设备确认；关卡由 OnboardHmi 按当前任务和在车业务状态自动批量卸货，不再次扫描 Sublot、不输入工号或等待接收确认。外部 MES PDA 流程独立，8005 不等待、不读取也不回写该结果。
- ControlServer 与 OnboardHmi 由两名开发者在各自的 Git 仓库实施。另建独立轻量共享协议仓库，以带 tag 的不可变 protocol release、完整 commit、Schema SHA-256 与测试向量作为两端唯一契约权威；不跟踪 `main`，不使用 Git submodule，不在两个实现仓库平行维护协议副本。
- 共享协议以 JSON Schema、协议 manifest、合法/非法消息样例、错误码、交付类别和一致性测试向量为执行权威；Markdown 只解释业务含义。
- 双端从第一天使用 Fake Onboard 与 Fake ControlServer，以稳定 IntegrationSliceId 对齐实施票、协议版本、对端 Fake 版本和共同测试证据；不等双端各自完成后再首次联调。
- 任何共享协议变更都必须同时更新 Schema、样例、一致性测试和兼容性说明，并由两名开发者本人确认；AI 不得代替任一开发负责人批准跨端契约。
- 用户是 MVP 产品范围与最终发布的唯一批准人；共同协议 release 由用户与车载端开发同事共同确认。现场人员提供验收证据，但不自动改变需求或协议。
- 跨端决策须遵守根 `CONTEXT.md` 及 `docs/adr/cross/` 中已接受的权威边界，特别是 NDJSON ProtocolEnvelope、精确 ProtocolVersion、消息交付类别、RecoveryHandshake、车载 IO 独占权威、服务端任务/仓位集决策权与车载物理执行权。
- 需要产品判断或最终批准的票据使用 `grilling` 与 `domain-modeling`；任何新领域词一旦定案立即写回根 `CONTEXT.md`。

## Decisions so far

<!-- 已解决票据才在此保留一行摘要；详细答案只存在票据中。 -->

- [建立 MVP 需求适用性证据矩阵](issues/01-build-mvp-requirement-applicability-evidence-matrix.md) — 固定 v1.0.0 基线哈希后，对 348 条需求零遗漏给出 83 条直接必须、90 条交互／安全依赖、46 条首期延后和 129 条本场景不适用的候选路由，所有收窄与冲突继续交由具名 HITL 票批准。
- [决定 Demand 受理、执行身份与完成后防重边界](issues/02-decide-demand-acceptance-execution-identity-and-completion-deduplication.md) — 以承诺点最终重读、HistoryEpoch 约束和 DemandId 唯一执行实例身份冻结受理事实，并用独立的 TransportDemandCompletion 与既有取消抑制分别永久阻断成功和取消后的同键重复执行。
- [决定单 Demand 选择、并发与等待策略](issues/03-decide-single-demand-selection-concurrency-and-waiting-policy.md) — 单车单 Demand 先过静态硬准入，再按等待年龄、创建时间与 DemandId 稳定选取；忙碌和低电保持共享等待，结构性无解即时告警且首期不启用未标定的防饥饿阈值。
- [决定机台取货、多仓装货、关卡卸货与成功边界](issues/04-decide-pickup-loading-gate-unloading-and-success-boundary.md) — 机台输入只确认已受理 Demand，服务端冻结篮数与完整仓位集并批量闭环装卸；关卡无需再次输入，全部空仓安全证据与本地成功、StopClosureCommit 和 TransportDemandCompletion 原子提交且不等待 PDA/MES。
- [决定 MVP 多仓容量、安全联锁与异常恢复最小集](issues/05-decide-minimum-multislot-safety-and-recovery-set.md) — 保留完整八仓身份、批量物理闭环、Guard、持久幂等、断联安全收尾、重启对账与移动安全内核，并纳入最小 ExceptionRecoverySession；首期以预置配置和具名管理员运行，延后完整管理 UI 与复杂车队能力。
- [决定 MVP RIoT 移动、建单对账与人工充电边界](issues/06-decide-riot-movement-order-reconciliation-and-manual-charging-boundary.md) — 以两段严格串行的单段移动、逐段稳定意图与完整到站门禁闭合机台到关卡旅程，未知和重启沿原意图对账，低电只进入具名管理员重新投运的人工充电保持。
- [决定 ControlServer—OnboardHmi 职责边界与 MVP 消息面](issues/07-decide-controlserver-onboard-responsibilities-and-mvp-message-surface.md) — 以 ProtocolVersion 1 的显式 WIRE_TO_GATE MVP 剖面固定服务端业务权威、车载物理权威、完整 messageType allowlist、五类交付、通用 ACK、业务幂等与五步恢复对账。
- [验证 OnboardHmi 单场景操作原型](issues/08-validate-onboard-single-scenario-interaction-prototype.md) — 用户明确豁免本票的车载端开发同事评审并选定 A“旅程导引台”为生产交互与布局权威，完整八仓、四维状态、断联恢复和异常处置边界固定，未验证的真实车载可用性转入实施与试运行验收。
- [决定共享协议仓库的发布内容与变更治理](issues/09-decide-shared-protocol-repository-release-and-change-governance.md) — 以复合 ProtocolReleaseIdentity 固定单一不可变契约，逐消息冻结 Schema、错误码、样例与向量，并保留两名开发者本人确认每个 release 的强制门禁。
- [决定双仓库一致性门禁、模拟对端与联调切片](issues/10-decide-cross-repository-conformance-harness-and-integration-slices.md) — 以共同向量、确定性虚拟时间、双 Fake 复合身份、八个稳定 IntegrationSliceId 和 G0～G3 门禁绑定两端精确构建及不可改写联合证据。
- [决定受控工厂试运行配置、执行顺序与验收证据](issues/11-decide-controlled-factory-pilot-configuration-and-acceptance-evidence.md) — 以不可改写配置与运行身份串行执行 P0～P7，只在精确候选、目标硬件、空车彩排和一次真实物料旅程全部具证时通过，并以严格清场和永久红色证据守住安全边界。
- [最终批准 MVP 精确需求适用性清单](issues/12-approve-exact-mvp-requirement-applicability-profile.md) — 绑定 v1.0.0 基线与最终 TSV 身份，零遗漏批准 85 条直接必须、101 条交互／安全依赖、31 条首期延后和 131 条本场景不适用，并保留 Lifecycle 与外部批准边界。
- [汇编 WIRE_TO_GATE MVP 规格与双仓库实施交接包](issues/13-assemble-mvp-specification-and-two-repository-handoff-package.md) — 以最终 348 行清单和 02～12 决议汇编模块化版本绑定包，固定两仓、协议、W2G-IS-00～07、共同向量与 P0～P7 交接，同时保留所有真实人员和外部证据门禁。
- [确认 WIRE_TO_GATE MVP 规格与实施交接](issues/14-accept-final-mvp-specification-and-implementation-handoff.md) — 用户以严格限域的规划交接评审豁免接受精确哈希绑定包并结束路线图；车载端开发同事未评审、未批准，真实协议 release、生产映射、G0～G3 与现场门禁继续保留。

## Not yet specified

无。

## Out of scope

- `WIRE_TO_GATE` 以外的五种 MES 运输任务的产品实施和现场验收。
- 多车调度、复合任务、多 Sublot 混装、顺路运输、路网评分优化和跨地图运输。
- 自动充电、充电排队、备用桩改派和空闲返回优化；MVP 只保留必要电量准入与人工充电边界。
- MES 完工、卸货或状态回写，以及外部 PDA 集成。
- 完整管理后台、高级报警分析、运营大盘、完整 MesIngestWatch 建设与长期报表。
- 在本地图内修改、废弃或重发已批准需求基线，以及把延后需求冒充为永久取消。
- ControlServer、OnboardHmi、共享协议实现仓库或现场环境的实际开发、创建、部署和发布。
