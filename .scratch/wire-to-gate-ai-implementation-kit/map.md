# WIRE_TO_GATE 一周可运行 MVP 交付路线图

Label: wayfinder:map

## Destination

最迟于 2026-08-29 17:00（Asia/Taipei）开发、测试并发布一个可安装、可启动、可操作的 `WIRE_TO_GATE MVP Release Candidate`，而不是只交付需求文档、AI Spec 或开发启动包。原定截止为 2026-08-28 17:00，该截止已在正式 G3／RC 仍为 `INCONCLUSIVE` 的状态下逾期；2026-08-28 用户只顺延截止日期，交付范围与完成定义一字不改。剩余时间不足一个工作日，因此这是无缓冲的极限冲刺；任何关键输入延误都会直接进入发布风险，不得以文档完成替代软件完成。

最终软件由三个版本绑定的远程仓库共同组成：

- `8005-agv-control-server`：可运行的 ControlServer、持久化、MesIngest/RIoT 适配器、Fake 对端和自动化测试；
- `8005-agv-onboard-hmi`：可运行的 OnboardHmi、原型 A 的生产映射、车载 journal、IO 抽象/Fake 和自动化测试；
- `8005-agv-protocol`：两端共同消费的不可变协议 release、Schema、样例、错误码、向量和一致性 runner。

“一周 MVP 软件完成”至少要求：从干净环境按公开步骤构建或安装；两端可以启动并建立会话；在受控测试环境中完成一个 WIRE_TO_GATE Demand 从受理、取货、多仓装货、移动、关卡批量卸货到原子完成的端到端闭环；关键重复、断联、重启和恢复场景通过；版本、配置、日志、证据和已知限制可追溯；发布物已推送远程并由用户完成可用性验收。核心路径不得是占位页、伪实现或只能阅读的文档。

八仓 IO 在本轮采用独立模拟器实现并作为 OnboardHmi 的受控测试输入；它不证明真实 IO 模块、接线、锁或光幕资格。MesIngest 复用当前已有实现。RIoT 不建设也不接受模拟器作为集成替代，因此真实 RIoT 测试环境、车辆/Map/站点绑定和凭证是完整移动闭环的硬门禁；缺失时不得把不含真实移动的演示称为整个 MVP 端到端完成。

## Notes

- 用户已澄清：一周交付对象是整个可用 MVP 软件，不是文档、Spec、ZIP 或开发启动交接。Spec、协议资产和实施票只是降低双人并行开发与最终对接风险的开发手段。
- 本地图承接已结束的 [`WIRE_TO_GATE 单场景 MVP 与双仓库协作路线图`](../wire-to-gate-mvp/map.md) 及其已接受范围、348 条需求适用性表、02～12 决策、原型 A、协议治理和 W2G-IS-00～07；不重新扩展产品范围。
- 三个真实远程仓库已经创建。ControlServer 使用 `main`/`ControlServer_MVP`，OnboardHmi 使用 `main`/`OnboardHmi_MVP`，协议仓库使用 `main` 和不可变 tag/release。`SocialKKKK` 的 OnboardHmi 与协议邀请已发出，接受前写权限仍是阻断。
- 2026-08-25：完成 ControlServer 技术栈研究、王昆的 Onboard/IO 决策、完整核心协议面、薄 Spec、两个项目骨架和第一条失败测试；不得把时间用于重复整理 Markdown、DOCX 或便携 ZIP。
- 2026-08-26～27：按 W2G-IS-00～07 做纵向切片；双方对同一协议身份并行实现，每完成一个小切片立即运行本端 G2、对端 Fake 和候选联合测试，失败先修复再进入依赖切片；不得等两端“全部完成”后首次联调。
- 2026-08-29 17:00 前：冻结候选，跑全量 G1/G2/G3、安装/启动/重启冒烟和真实 RIoT 移动闭环，修复阻断缺陷，生成发布物并由用户验收。未通过核心路径验收不得用“文档齐全”替代软件交付。
- 双方可使用不同 AI、skill、IDE 和任务流程；协作只固定协议 release 身份、IntegrationSliceId、分支、标准命令、证据格式和变更批准规则。
- 技术实现遵守“成熟复用优先”：能由维护活跃、许可证兼容、版本可锁定且具有官方文档的现成库、SDK、框架或工具可靠完成的通用能力，不自行重写。TLS、JSON/JSON Schema、日志、配置、依赖注入、数据库迁移、重试、测试运行器、Modbus 等优先选用成熟组件；只自行实现 WIRE_TO_GATE 特有的领域状态机、事务边界、安全不变量、协议 payload 和必要的薄适配器。引入前必须核验当前维护状态、支持平台、许可证、安全记录和退出方案，不直接复制不明来源代码。
- 产品实现必须遵守根 `CONTEXT.md`、accepted ADR、最终需求适用性表和原型 A。原型 A 是 OnboardHmi 布局与交互权威，生产代码不得依赖原型项目或假数据。
- 候选协议允许隔离分支实现和联合测试；只有两名真实负责人确认精确 commit/manifest/hash 后才能创建不可变 ProtocolRelease。AI 不得代替任何人员批准跨端契约。
- 产品代码不强制 PR，但每次跨端变更必须绑定精确协议候选或 release。远程交付不接受仅本地完成或 ZIP 替代。
- 凭据、证书和密钥只登记安全引用，不进入 Git、发布包、日志或测试证据。
- 本路线授权开发三个仓库中的 MVP 产品代码、测试、构建输入和发布资产；执行时各仓库仍须遵守自身 AGENTS/CONTEXT 与测试门禁。Golden WPF tier 2/3、真实车辆动作和工厂试运行仍需届时单独授权并满足安全条件。
- 2026-08-25 用户重新划定 OnboardHmi 分工：车载端产品代码由王昆从本人 `bc56fa9` 基线开发；后续 AI 只为车载端保留开发交接文档，不再自行修改 OnboardHmi 产品代码，除非用户日后再次明确授权。远程 `OnboardHmi_MVP@05bf9f4` 已用可追溯 revert 把当前产品树恢复到 `bc56fa9`，仅保留 README 和交接文档；历史中的 AI 候选提交不能表述为王昆已开发或批准。
- 2026-08-28 22:45 原截止逾期：正式 G3／RC 仍为 `INCONCLUSIVE`，用户决定只把截止顺延到 2026-08-29 17:00，范围与完成定义不变。
- 2026-08-28 用户划定 RIoT 责任边界：RIoT owner 不提供技术支持，也不会修改 RIoT 程序，因此不得再把「等 owner 确认合同语义」当作路线阻断；「HTTP 200 但实际未建单」由用户定性为 RIoT 自身缺陷，本项目只负责实现正确的建单链路。建单安全性据 `OBSERVED` 级 BC-ORDER-004 改由服务端 upperId 幂等保证（重复提交返回 `0610008 订单已存在`，不建第二单），已在 `ControlServer_MVP@21f1dd6` 落地，不再需要一次性 permit。RIoT Behavior Lab 与 SDK（`8005---AGV` 仓）是 RIoT 行为的权威依据。

## Decisions so far

<!-- 已解决票据才在此保留一行摘要；详细答案只存在票据中。 -->

- [冻结一周可运行 MVP 的完成定义与最薄实施输入](issues/01-audit-current-handoff-for-ai-implementation-readiness.md) — 复用哈希未漂移的旧权威，新增工作流中立的 D1～D7 软件完成门禁、八切片代码工作包、协作状态机、14 项缺口账本和 2026-08-28 压缩冲刺入口，明确文档或开发启动不构成交付。
- [研究并冻结 ControlServer 最小技术栈](issues/02-research-and-freeze-controlserver-stack.md) — 冻结自包含 .NET 8 单体 Windows Service、原始 TLS/NDJSON TCP、EF Core SQLite 单写者、安装期迁移、外部秘密、结构化日志和真实边界测试，实施不再重开框架选型。
- [登记真实仓库、外部输入、权限与责任边界](issues/03-register-real-product-repositories-and-access-boundaries.md) — 回读确认三仓及分支、冻结 Fake/目标软件/工厂三层资格与安全责任边界，并将终端 Git 凭据缺失升格为独立前置票。
- [取得王昆的 OnboardHmi 与 IO 模拟器决定](issues/04-obtain-onboard-stack-and-io-simulator-decisions.md) — 本人确认仓库可读写并推送初始代码，冻结 .NET 8/WPF/x64、有界的 SQLite journal 与可配置 HTTP/JSON 八仓模拟器，保留开发机/虚拟工控机和模拟/真实 IO 的资格边界。
- [打通三仓终端认证、克隆与推送能力](issues/05-provision-authenticated-product-repository-access.md) — 确认当前终端以 Git Credential Manager 的 `trytoreachpeak0` 通道访问三仓，在规划仓库外建立三个干净独立工作目录并通过 fetch/push dry-run，未产生测试 commit 或远程变更。
- [生成并验证完整 MVP 候选协议面](issues/06-generate-the-candidate-shared-protocol-assets.md) — 在协议仓库 `main` 推送当前候选 `72ddde5`，交付 54 种消息、57 个 Schema、1,395 个正反例、19 条轨迹和 8 个切片；G1 对 manifest `e878d8…35f2e` 通过，候选保持未批准且将发布批准自引用闭环升格为票 16。
- [生成双仓薄 Spec、项目骨架与可执行测试入口](issues/07-generate-the-portable-controlserver-ai-spec.md) — 在 `ControlServer_MVP@6ff2d7c` 与 `OnboardHmi_MVP@2eeecf6` 推送精确 SDK/依赖/协议身份、薄 Spec、Fake/端口、统一脚本和可发现的首条红测试；两端构建零警告，车载旧测试 48/48 通过，明确骨架不等于 MVP。
- [实现并自测 ControlServer MVP](issues/08-implement-controlserver-mvp.md) — 在远程 `ControlServer_MVP@8fae66f` 交付 SQLite 持久状态核、五步恢复、可靠协议、MesIngest/RIoT 薄适配器、Host 与 Fake；Release 零警告、17/17 测试及绑定精确协议候选的八切片 G2 全部通过，真实 RIoT/G3/协议批准仍留后续门禁。
- [实现并自测 OnboardHmi MVP](issues/09-implement-onboardhmi-mvp.md) — AI 候选曾在 `398a957` 完成本地 G2，但用户随后指定王昆从本人 `bc56fa9` 基线开发；远程 `05bf9f4` 已回退全部 AI 产品代码，只保留交接文档，故旧候选不再是当前 Onboard 实现或有效 G3 输入。
- [解决协议清单与批准记录的发布闭环](issues/16-resolve-protocol-manifest-approval-finalization-cycle.md) — 两名真实负责人批准内容 manifest/外部 attestation 分离；协议 `main@3ad309f` 已实现审批中立稳定 manifest、双 Schema/G1 校验和无 commit 自引用的 Release Asset 流程，正式 tag 留待两人批准新 commit/hash。
- [最终批准并发布不可变协议版本](issues/17-finalize-and-publish-the-approved-protocol-release.md) — 两名真实负责人批准精确 commit/hash，正式 G1 通过，annotated tag 与 GitHub Release `protocol-v0.1.0` 已发布且外部批准证明哈希独立回读一致。

## Not yet specified

无。

## Out of scope

- WIRE_TO_GATE 以外的 MES 运输类型、多车调度、多 Sublot 混装、顺路运输、跨地图运输和路径优化。
- 自动充电、充电排队、备用桩改派；MVP 只保留电量准入和人工充电保持/恢复边界。
- MES 完工回写、外部 PDA 集成、完整管理后台、高级运营大盘和长期报表。
- 未经单独授权自动执行真实车辆动作、Golden WPF tier 2/3、工厂 P0～P7 或真实物料试运行。
- 把 Fake 通过、协议生成、Spec 完成、构建成功或 README 齐全单独表述为整个 MVP 软件完成。
- 为赶工删除已接受的安全、持久化、幂等、断联或恢复约束，或用手工演示掩盖核心路径缺失。
