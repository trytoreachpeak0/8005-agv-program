# 汇编 WIRE_TO_GATE MVP 规格与双仓库实施交接包

Type: task
Status: resolved
Blocked by: 12

## Question

如何把全部已解决票据和最终批准的需求适用性清单汇编为一份无未决语义的《WIRE_TO_GATE 单场景 MVP 范围与验收规格》，并生成 ControlServer 实施交接、OnboardHmi 实施交接、共享协议仓库初始化交接、IntegrationSliceId 索引、契约测试向量要求和现场验收清单？

交接包必须让两个无共享上下文的 AI 仅依靠版本化资产即能识别当前协议身份、本端权威、对端假设、状态机、安全下限、测试命令、待人工批准点和禁止自行扩张的范围。

## Answer

### 决策依据与采用记录

本票依据用户对本 Wayfinder 后续各票采用推荐值的明确授权，在核对根 `CONTEXT.md`、实际 `docs/adr/cross/`、地图 Notes、全部已解决票 02～12、A“旅程导引台”源、需求基线以及最终 348 行 TSV 后，采用以下全部推荐值。该授权替代逐项等待，不表示用户曾逐题作答，也不表示两名真实开发者、车载端开发同事、现场人员、第三方或法定人员已经批准实际 release、构建、生产映射或试运行。

### 全部候选、推荐值与理由

1. **交付形态**：候选 A 为一份巨型 Markdown；候选 B 为一份主规格加 ControlServer、OnboardHmi、共享协议、切片、向量和试运行清单组成的模块化版本绑定包；候选 C 为只链接原票。**推荐并采用 B**。A 难以让两个仓库独立消费且机器索引薄弱，C 要求实现 AI 自行拼装语义；B 同时保留单一入口、仓库边界和机器可读索引。
2. **需求适用性权威**：候选 A 为在交接包重新摘录或改分 348 条；候选 B 为固定基线与最终 TSV 的 SHA-256，以 TSV 作为唯一逐条适用性权威，主规格只解释分类消费规则；候选 C 为只写 85+101 的适用条目而隐藏延后/不适用项。**推荐并采用 B**。它能证明零遗漏且不制造第二份分类权威；C 会丢失 Lifecycle 与排除边界。
3. **双仓实施分解**：候选 A 为按团队各写一份无共同编号的 backlog；候选 B 为两仓职责分别交接，但全部工作包使用稳定 W2G-IS-00～07 对齐；候选 C 为把双端实现放进同仓计划。**推荐并采用 B**。它继承切片语义、允许各仓独立 G2，又能用同一身份做 G3，且不改变两个仓库边界。
4. **共享协议交接**：候选 A 为在两个实现仓复制 Schema/向量；候选 B 为规定独立轻量协议仓目录、复合 ProtocolReleaseIdentity、逐 messageType 资产、错误码、向量、runner 与真实批准流程；候选 C 为交付语言特定共享 SDK/Fake。**推荐并采用 B**。它保持语言无关唯一契约，避免漂移和第三套业务实现；协议字段与语义仍严格继承票据 07/09，汇编不重写。
5. **测试命令**：候选 A 为编造当前仓库已有可执行命令；候选 B 为定义两个实现仓必须提供的同一非交互语义入口 `test-wire-to-gate --gate G2 --slice ... --protocol-manifest ... --output ...`，具体脚本语言由各仓实现；候选 C 为只写“运行测试”。**推荐并采用 B**。当前规划仓没有两个生产实现，A 不真实，C 不足以交接；B 固定输入、输出和身份验证而不虚构已运行测试。
6. **人工门禁表达**：候选 A 为用 `TBD`/占位批准先视作满足；候选 B 为把实际 release、两名开发者本人确认、生产 UI 映射、G0～G3、凭证、目标硬件、真实物料和 P0～P7 全部列为显式阻断门禁；候选 C 为沿用原型票豁免。**推荐并采用 B**。只有它不伪造外部事实，并严格保持原型豁免只限原票。
7. **规格冲突处理**：候选 A 为实现团队就近解释；候选 B 为最终 TSV 决定适用性、已解决票决定详细语义、根 CONTEXT/accepted ADR 提供领域与底层约束；遇到不能同时满足时停止并提出精确产品或 ProtocolChangeProposal，不得安全降级；候选 C 为较新实现覆盖文档。**推荐并采用 B**。它提供可审计的权威顺序，防止 AI 擅自改变协议、安全和恢复。
8. **现场验收交接**：候选 A 为通用 happy-path checklist；候选 B 为逐项移交不可改写 FactoryPilotConfigurationSnapshot/RunIdentity、P0～P7、目标硬件矩阵、一次真实物料、十项不变量、严格清场及 PASS/FAIL/INCONCLUSIVE；候选 C 为把 G3 或一次现场成功当发布批准。**推荐并采用 B**。它完整继承票据 11，且明确一次 PASS 只绑定精确候选，不等于发布批准。

### 已生成的版本化资产

入口为[《WIRE_TO_GATE MVP 规格与双仓库实施交接包》](../handoff/README.md)，包含：

- [MVP 范围与验收规格](../handoff/mvp-specification.md)：范围、排除、端到端状态机、权威、安全/持久化/恢复、原型映射、协议/一致性、试运行及需求消费；
- [ControlServer 实施交接](../handoff/controlserver-handoff.md)与[OnboardHmi 实施交接](../handoff/onboard-handoff.md)：逐切片责任、持久化/物理下限、Fake、统一测试入口和禁行项；
- [共享协议仓库初始化交接](../handoff/protocol-repository-handoff.md)：复合身份、release 树、完整消息族、禁止消息、交付/错误/批准治理；
- [IntegrationSliceId 索引](../handoff/integration-slices.tsv)：W2G-IS-00～07 的前置、输入、结果、共同向量、双端责任与完成门禁；
- [契约测试向量要求](../handoff/contract-vector-requirements.md)：语言无关 runner、合法/非法消息、19 条强制轨迹、判定和不可改写证据；
- [受控工厂试运行交接清单](../handoff/factory-pilot-checklist.md)：P0～P7、目标硬件、真实旅程、清场与 verdict；
- [资产身份清单](../handoff/asset-manifest.tsv)：24 个包内和绑定来源资产的逐文件 SHA-256。中文化后的 manifest SHA-256 为 `28ffd7459fc656dce598f15aa8598da500135e9c06f955a3e1da40e5fa4fac70`。

包固定绑定需求基线 SHA-256 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba` 和最终 TSV SHA-256 `0678fddb8cb0dc4b1df620257ac7076fc8658e3bda828f0de5c6e9f0fe0461de`。两者任一不符，交接包明确要求停止使用。

### 覆盖与验证

- 资产清单 24 行全部路径存在且 SHA-256 可重算；7 份 Markdown 的相对链接全部可解析。
- IntegrationSlice TSV 恰有 8 个唯一且按序的 `W2G-IS-00`～`W2G-IS-07`。
- 最终适用性 TSV 回读仍为 348 行，分类恰为 85/101/31/131。
- 包明确继承 02～12 的受理/防重、单 Demand、装卸成功、多仓安全恢复、RIoT、跨端权威/消息、A 原型、发布治理、双 Fake/G0～G3、P0～P7 和最终清单结论；没有改写协议字段、需求分类、原型权威或试运行门禁。
- 只执行结构化文件、链接、哈希与覆盖检查及 `git diff --check`；未因脏工作区运行产品测试，也未运行 Golden WPF tier 2/3。

### 本票没有完成的外部事实

本票没有创建远程或生产仓库，没有发布/批准真实 ProtocolRelease，没有取得两名开发者本人确认，没有实现 ControlServer/OnboardHmi/Fake/runner，没有运行 G0～G3，没有取得真实凭证、目标硬件映射、物料或现场批准，没有执行 P0～P7，也没有把一次 PASS 或原型豁免写成发布批准。这些仍由包内明确门禁阻断。
