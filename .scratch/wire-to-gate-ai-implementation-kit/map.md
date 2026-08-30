# WIRE_TO_GATE 一周可运行 MVP 交付路线图

Label: wayfinder:map

## Destination

最迟于 2026-08-30 17:00（Asia/Taipei）开发、测试并发布一个可安装、可启动、可操作的 `WIRE_TO_GATE MVP Release Candidate`，而不是只交付需求文档、AI Spec 或开发启动包。原定截止为 2026-08-28 17:00，先顺延至 2026-08-29 17:00，该次截止同样在正式 G3／RC 仍为 `INCONCLUSIVE` 的状态下逾期；2026-08-29 用户第二次只顺延截止日期，交付范围与完成定义一字不改。剩余时间约一个工作日，因此这是无缓冲的极限冲刺；任何关键输入延误都会直接进入发布风险，不得以文档完成替代软件完成。

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
- 2026-08-29 第二次截止逾期：当日已首次打通取货段与到站后第一段（旅程达到 `AwaitingSublot`），但正式 G3／RC 仍为 `INCONCLUSIVE`，剩余五段业务流程需真实现场逐段调试。用户第二次只把截止顺延到 2026-08-30 17:00，范围与完成定义仍不变。
- 2026-08-30 第三次截止逾期：17:00 时点上核心验收尚未开跑；当晚 19:26 在 RC 生产形态下走通完整闭环，服务安装与干净安装验收也已 PASS。范围与完成定义仍不变，剩下的是发布授权（票 12）与交接（票 15），以及归车载端只读仓的 HMI 缺陷（票 27）。
- 本机网络会伪造 RIoT 可达性：Clash 全局模式下内核给 `172.19.206.222` 选 Clash TUN 源地址，ICMP 与 TCP connect 对任意端口、乃至不存在的主机全部「成功」；`vEthernet (Default Switch)` 又占着 `172.19.192.1/20` 覆盖该地址。判定 RIoT 可达只能用返回 body 的 HTTP 往返，不能用 ping 或 TCP connect。
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
- [把故障注入泛化到业务消息面](issues/18-generalise-fault-injection-to-business-messages.md) — 硬编码 drop 换成四动作规则表，合成对端在四种业务消息上取得重复／冲突／同会话结果重放／延迟／乱序证据，十二条断言绑 `3d8b00c`+`304e6ad` 全 PASS（`ControlServer_MVP@6a678a1`）；`OperationResult` 与 `SlotOperationCommand` 经证实需带 demand 的运行，已具名列为不可达而非默认覆盖。
- [覆盖断联安全收尾与恢复分支向量](issues/19-cover-disconnect-closure-and-recovery-branches.md) — 判据是「是否需要一行 `StationOperations`」：`FORCED_MECHANICAL_RECOVERY` 是唯一无需 demand 的接受路径，由它承载中途断联（命令被丢弃断连后按新会话代从同一 outbox 行重放，无重复命令行）与代际向量（1→2 单调推进，旧代结果只进历史证据，成功结果仍置 `RecoveryRequired` 而非完成）；其余七种恢复动作只在授权边界取证，RIoT UNKNOWN 对账证实不可达并路由回票据 10。十九条断言绑 `3d8b00c`+`304e6ad` 全 PASS（`ControlServer_MVP@9a94c3b`），八条单点变异全部被断言检出。
- [进程崩溃重启 runner 归位并重绑](issues/20-relocate-and-rebind-the-restart-runner.md) — 脚本归位为 ControlServer 仓 `scripts/run-staged-g3-restart.ps1`，四个 peer commit 改为解析主 runner `param()` 块默认值读回而非重述，规划仓副本已删；二十条断言绑 `3d8b00c`+`304e6ad`+`fb5f7c5`+`1531489e` 全 PASS（`ControlServer_MVP@3c699d9`），三十条单点变异全检出。重启事实由 OS 进程身份承担——`serverInstanceId` 经证实是每连接一个而非每进程一个；跨重启身份取自两端存储（车载 journal epoch 不变、两侧重启前行原样保留、三条 `RecoveryStateReport` messageId 两端同集合）。Demand 与车辆租约因 `VehicleDispatchLeases` 以 `DemandId` 为主键，在不建单形态下证实不可达，与票据 18 的 `OperationResult` 并入带 demand 的运行。

- [完成双端联合测试并修复跨仓缺陷](issues/10-run-cross-repository-mvp-integration.md) — 八类 G3 向量集齐，按「是否需要一行 `StationOperations`」分三种形态承担：现场授权闭环、staged 合成对端注入、带 demand 的存储恢复。最后两类经证实**不需要移动车辆，且移动帮不上忙**——RIoT UNKNOWN 是每次新代次建单的必经路径，`OperationResult` 首次接受只在「命令已下发、结果未到」的存储上可达，而真实车载端会立刻回结果。二十条断言绑 `3d8b00c`+`304e6ad`+`fb5f7c5`+`1531489e` 全 PASS，三十六条单点变异全检出（`ControlServer_MVP@acc8a6d`）；票 20 遗留的跨重启 Demand／租约复用一并收口。产品代码未改，W2G-IS-00～07 与 RC 仍为 `INCONCLUSIVE`。

- [构建并验证可安装的 MVP 发布候选](issues/11-build-and-verify-the-portable-delivery-package.md) — 一条命令从 `ControlServer_MVP@2eeb6f0` + `OnboardHmi_MVP@304e6ad` + `protocol-v0.1.1` 组装出含两端 self-contained 二进制、联合 manifest、868 个文件 SHA-256、依赖／许可证清单与秘密扫描的 RC；协议身份从产物读回而非重述，车载端从一次性克隆构建、只读仓零写入。隔离第二实例（58405／58407）上二十六条断言全 PASS，五条可证伪性检查证明绿能变红，生产服务全程未动。修掉三个真缺陷（相对路径按进程 CWD 解析、根证书导入弹框卡死非交互安装、服务无持久日志），另报告四项未修发现。**不构成发布物已推送远程**（二进制不进 Git，GitHub Release 属票 12／15），W2G-IS-00～07 与 RC 仍 `INCONCLUSIVE`（`ControlServer_MVP@ee54988`）。

- [复核尚未经过审查的服务端现场修复与发布/runner 改动](issues/21-review-the-unreviewed-server-and-runner-changes.md) — Standards + Spec 双轴复核 `ea8dc98..ee54988` 共 31 个 commit，**发现两个真产品代码缺陷**：`worklistRevision` 从不持久化（唯一写入点恒为 1，gate 的 `+1` 读时算，新 demand 新 runtime 行即重置，同一 AGV 第二趟按 ADR-0048 必然被车载端幂等 ACK 或丢弃，甚至复演 `3d8b00c` 的连接被拆——车载端会话间是否重置 revision 是待确认的未知数）；`f48e616` 的四处 settle 只有两处有回归保护，删掉 safety check 那处 tier 1 全绿，而那正是其 commit message 自述的故障本体。另记录五项脚本／证据偏差（票 20 留了等价的 `-CommitBindingSource` 漂移口、票 11 的二十六条断言只是 markdown 无机器可读记录且证据目录缺 manifest／SHA256SUMS／秘密扫描产物、发布脚本的扫描结果不设闸、三个 runner 逐字复制公共函数）与三票已披露的范围偏差。三处现场 fix（`12eddf2`+`31569f5`、`3d8b00c` 单趟那一半）经证实真锚在缺陷上。缺陷修复路由至新建的票 22。

- [修掉跨趟 worklist revision 与两处 settle 的回归缺口](issues/22-close-the-worklist-revision-and-settle-coverage-defects.md) — 动手前那个未知数由**只读检查车载端仓**解掉，两条既定路径（问王昆／双 demand staged 运行）都不需要：`OnboardHmi_MVP@304e6ad` 把已采用快照持久在 SQLite、**键只有 MessageType**、永不删除、每次重连在 SessionHello 前从 journal 还原，所以**不在会话间也不按 demand 重置**——第二趟是必然被拒，且形态是更硬的 `SNAPSHOT_REVISION_REGRESSION`（1 < 2）而非内容冲突。缺陷范围也比复核所述宽：`ToRuntimeRow` 把 `VehicleBusinessRevision`／`WorklistRevision`／`PlanRevision` **三个**都写死为 1，三条快照流同时回退。修复是新 runtime 行从该 `AgvId` 已存储最高值 +2 起算（一趟发出存储值与 +1 两个 revision），无新表无迁移；**否掉了「per (AgvId, StationId) 计数器」**——车载端按 MessageType 记账不按站点，按站点各自计数会让同一趟取货与关卡双双落在 1，正是 `3d8b00c` 修掉的冲突。缺陷二补两条断言覆盖安全检查与卸货命令的 settle。三处变异各自证红（revision 实际序列 `[1, 2, 1]`；两条 settle 的失败 messageId 不同故互相独立）。Release 0 warning、`dotnet format` 干净、230 passed / **0 skipped**、八片 G2 全 PASS 绑 `127b137`（`ControlServer_MVP@127b137` + 证据 `@0e4d471`，**尚未推送**）。新发现两项本票范围外：ACK 丢失会让快照在更高 revision 之后重发而同样触发 regression（票 23）；车载端「更低 revision 抛异常拆连接」与 ADR「丢弃并返回当前版本」偏差，归只读仓需用户指定目的地。

- [收口票 21 记录的五项脚本／证据层偏差](issues/24-close-the-script-and-evidence-deviations.md) — 做 1、3、4，不做 2、5。主体是第 4 项：发布脚本的扫描结果从「写进 JSON」升成 `Assert-ReleaseScanGate` 闸门，任何 finding、任何密钥材料文件、任何**不在具名允许清单内**的 UNRESOLVED 许可证都中止发布；允许清单只有三个自建 RIoT SDK 包、逐个具名，所以**新**的无许可证依赖会失败而不是并进计数。闸门放在 `inventory/` 落盘之后、manifest 之前，失败留证据但绝不出包；报错只给「路径:行号:规则名」。同时修掉 `Get-PackageLicense` 的 `%USERPROFILE%` 硬编码——它与缺闸门是**互相掩护**的一对：设了 `NUGET_PACKAGES` 的机器上许可证全 UNRESOLVED 而照常出包。第 1 项拆掉 `run-staged-g3-restart.ps1` 的 `-CommitBindingSource` 覆盖口（读回的四个 commit 不变）；第 3 项把 RC 的 manifest／SHA256SUMS／inventory 抄进证据目录，**归档前先验证两个根哈希仍与票 11 记录一致**——并因此撞出一件证据完整性问题：仓内 `text=auto eol=lf` 会把 manifest 从 171,544 字节存成 162,774，checkout 出来的哈希不再是证据宣称的值，已加 `-text` 并从对象库回读验证。第 2 项拒绝事后把 markdown 表格转写成 `assertions` 数组——那是转写不是观测，却长得像 harness 输出，比诚实的表格更坏；真修法是下次安装验证自己发射，属票 13／12。第 5 项（三个 runner 抽公共模块）不做：失败形态是启动即抛异常、响亮且立刻，而改动要同时动三个零测试覆盖、承载全部证据的 runner。两个 harness 用 **AST 从提交进仓的脚本取出规则与闸门**并与基线 `0e4d471` 并排，17 条断言全 PASS，红侧逐条直接证出（植入 apiKey 抛错、基线被证明根本没有闸门、报错不含植入值、`.pfx` 抛错、未列清单的 UNRESOLVED 抛错、reader 会毫无怨言接受带假 commit 的副本）。闸门不追溯，故另证 `2eeb6f0` 那份既有 RC **能通过**新闸门。未触产品代码、未跑 tier 1（`ControlServer_MVP` 证据 + 脚本改动，**尚未推送**）。

- [快照重发顺序对上车载端的单调 revision 规则](issues/23-settle-snapshot-redelivery-order-against-monotonic-revision.md) — **不可达，未改产品代码**。假设漏掉的一环是「重发本身就是修复」：车载端 `304e6ad` 的采用、落 journal、回 ACK 是三条顺序语句，中间那个提前 return 在一个 `void` 辅助方法内部，所以**重复快照会被再次 ACK**；而服务端每个迭代开头重发全部未确认行，一次丢失的 ACK 下个迭代就补上，远早于关卡分配更高 revision。`AdoptingPeer` 复刻车载端判据并按迭代缓冲 ACK，精确丢掉「断连那刻还在飞的那一批」：9 个单迭代窗口（含关卡那一迭代）全干净，且每次都断言对端确实持有过两个 revision——绿不是空的；检测器**证明会响**（ACK 永不到达时三条流全部复现「持有 2 却被投递 1」）；边界是**连续五个迭代 3～7**，任意一次成功送达即收口。而那五个迭代恰是旅程消费 `SublotSubmitted` 与 `PreDepartureSafetyCheckResult` 的区间，二者与 ACK 同向同连接，故该对端不存在——票 22 看到的 `1, 2, 1, 2` 交错是 fixture 永不 ACK 的产物，不是可达序列。**具名残留风险**：服务端正确性依赖一条协议未要求的对端行为（重复必须再 ACK），沉默的合规对端会让它可达且自维持；闸门形态已存在于恢复流的 `QueueSessionSnapshotAsync`，推广到三种旅程快照即可、无需迁移，风险归改动该对端行为或换绑对端的人。13 条断言全 PASS，Release 0 warning、`dotnet format` 干净、tier 1 **243 passed / 0 skipped**（`ControlServer_MVP@d243abf`，**尚未推送**）。**不阻断票 12。**

- [把发布候选重建到含票 22／24 修复的 commit](issues/25-rebuild-the-release-candidate-on-the-fixed-commit.md) — 票 11 那份 RC 绑 `2eeb6f0`，其后 `127b137` 改了 `WireToGateStore.cs`（票 22 的 revision 跨趟修复）、`1fd23ac` 才给发布脚本装上扫描闸门，所以它是一份**已知第二趟会被车载端拒绝**且未经闸门的二进制，拿去做票 13 的部署验证等于验错东西。新 RC 从 `d243abf` + `304e6ad` + `protocol-v0.1.1` 建成（`w2g-rc-20260830-d243abf`，272 MB／868 文件），协议侧九个字段与旧 manifest 逐字相同——只有服务端动了。**原定判据被自己的对照证伪**：同源同 SDK 的车载端托管程序集也 DIFF，故此处托管构建不可复现（每次新 MVID），「哈希变了」对内容什么都不证明，该判据弃用而非当证据报出。改用元数据级真判据——`127b137` 新增的 `SeedSnapshotRevisionsAsync` 在旧产物 ABSENT、新产物 PRESENT，而既有方法名两边都 PRESENT，红侧与检测器有效性同时成立；行为证据仍只是 `d243abf` 的 tier 1（243 passed / 0 skipped）。两端 0 warning（脚本 throw 设闸）、扫描闸门 PASS（允许清单仅三个具名 RIoT SDK 包）、868 条哈希全量 ALL OK 且证明会红（副本改一字节 GREEN→RED）。**未安装、未启动、未跑旅程**——那属票 13／12；旧 RC 未删，车载端仓零写入（本地仍 `bbfbc52`、干净），未触产品代码故未跑 tier 1。证据 `evidence/rc/20260830-issue25-rebuild-d243abf/`。

- [验证真实适配器、目标部署与硬件边界](issues/13-qualify-target-adapters-and-deployment.md) — 用户到场并给出安全 GO，仍**未动车、未建单**：不是授权缺失也不是时钟，而是部署链在 readiness 上断掉，移动段不可达。对票 25 那份 RC（不是票 11 的 `2eeb6f0`）跑隔离资格验证，19 条断言 11 PASS／5 FAIL／3 INCONCLUSIVE，且是**机器可读断言的第一次真实发射**——收掉票 21 第 2 项／票 24 拒绝事后转写的那个缺口。PASS：服务端从 RC 目录直接启动并自动迁移、八仓 IO 模拟器、车载端↔服务端会话（`SessionRecoveries=1`／`ProtocolInbox=19`）、MesIngest（`JourneyBacklog=282` 真实需求在流）、`RiotDispatchAuditEvents=0` 证明未建单。真实 RIoT 降级 INCONCLUSIVE（网络可达 PASS，但读路径不落持久行且只在受理后才走到）；屏幕／触摸／扫码枪与真实八仓 IO 按外部输入缺失具名 INCONCLUSIVE。**主发现**：`OnboardMessageProcessor.cs:56` 在 SessionHello 无条件置 `RecoveryRequired`，干净安装三次运行全部停在那里，`/health/ready` 恒 503、282 条 backlog 零受理，故票 14 的「从干净安装开始完成一个完整场景」在当前 RC 上走不通——开票 26 承载并挂成 14 的阻断。**次发现**：RC 服务端出厂即现场真值，车载端出厂却是样例值（`wireToGate.enabled=false`、`agvId=AGV-8005-01`、`onboardBuildCommit` 过期、`vehicleSafety.endpoint` 是 `.invalid` 占位符），本轮只在副本里改正、RC 本体未改。**三条判据被自己杀掉并留档**：搜服务端日志的会话检测器永远不可能变绿（那份日志 64,373 行全是 EF SQL，从不打印消息类型名），503 探早于车载端启动读到的是闸门在工作，「连接被强制关闭」是我自己的 kill；两个适配器判据靠 grep 连接串误判为绿，第三版全改为读派生行并各带同库内保持为 0 的对照表。证据 `evidence/g3/20260830-issue13-target-qualification/`。
- [定位干净安装停在 RecoveryRequired 的那一步](issues/26-settle-clean-install-readiness-stuck-at-recovery-required.md) — 真实回读证伪「恢复报告没发」：阻断是资格 harness 沿用开发默认、漏配可信车辆停稳投影；同一握手仅改变停稳事实即 `RECOVERY_REQUIRED→READY`，公开 RC 步骤已补齐 HTTPS 信任、车辆身份与新鲜 STOPPED 预检（`ControlServer_MVP@81cb9cf`）。

- [执行可用 MVP 验收并关闭阻断缺陷](issues/14-run-usable-mvp-acceptance.md) — **核心验收 PASS，逐项资格分开给不合并**。干净安装验收 23 PASS／0 FAIL（868 哈希、HTTPS 安全投影 200 且无凭据 401、真实 RIoT `STOPPED`、`readiness=Ready`、`/health/ready` 503→200、受理 1 条、`StationTaskTypeAdmissions=205` 让票 13 的 RIoT 读路径 INCONCLUSIVE 终于成立、重启 generation 1→2 回到 Ready），两条单字段变异各自证红。现场闭环 generation 7 在 RC 生产形态下走通取货→装货→发车安全→`TO_GATE`→关卡卸货→原子完成，`Stage=Completed`、`SessionGeneration` 全程 1、5 分 42 秒、两条真单各一次建单；**这补上了 08-29 那次闭环（绑 `3d8b00c`）之后五个未现场复跑的提交**，并证实生产形态的安全闸门在移动中拦、停稳后自动放行而不卡死旅程。gen4／5／6 未通**全是本目录脚手架缺陷**，产品四次行为一致。服务安装由用户以管理员跑隔离实例 PASS（九检查、NDJSON 落盘），ACL 硬化由 agent 侧读被拒独立证实。开工前还解掉一个假绿：Clash 全局模式让安全投影恒 `RIOT_READ_TIMEOUT`，而 ICMP 与 TCP-connect 对任意端口乃至不存在的主机全绿——**票 13 的 `NET-RIOT PASS` 用的正是这种探针**。**具名 FAIL 归只读车载端仓**：生产形态下 `DisabledRuleGateway.IsConnected` 恒 false 把 HMI 状态机钉死在 `Connecting`，业务不进横幅与操作记录，`RecoveryRequired` 无操作员出口，已开票 27 路由。真实八仓 IO 与车载目标终端硬件仍 INCONCLUSIVE（`ControlServer_MVP@9daeef4`）。

- [审阅可运行 MVP 候选并授权正式发布](issues/12-review-the-local-kit-and-authorize-remote-publication.md) — **用户批准发布**：tag 绑 `9daeef4`、资产为完整 RC 上传（PRIVATE 仓，知情现场真值随包分发）、六项已知限制原样进发布说明；拟用 tag `w2g-mvp-rc-0.1.0`。审阅**回读产物而非转述票据**，并撞出两件票据没写的事实：车载端 `304e6ad` 经 `merge-base --is-ancestor` + `rev-list --left-right` 证实**就是 origin 当前 tip**（本地 `bbfbc52` 是它祖先、落后一个，不是领先，该仓无 agent 写入）；`81cb9cf..9daeef4` 排除 `evidence/` 后 diff **为空**且 `src` 在 `d243abf..HEAD` 无提交，故 tag 目标与 RC 二进制产品代码同源。868 条哈希本会话现场复验 `OK=868 / MISMATCH=0 / MISSING=0`，**红侧证明会响**（翻一个字符即 MISMATCH）。门禁：tier 1 243/0/**0 skipped**、G2 8/8 PASS 绑同一 manifest `a467c0c4…`、验收 23 PASS／0 FAIL、闭环 gen7 `Completed`、安装与卸载 PASS、扫描闸门 finding 0 且 3 个 UNRESOLVED 逐个具名在清单内。5 条 INCONCLUSIVE 中三条已被补齐，**真正剩两条硬件资格**（车载目标终端、真实八仓 IO）。新发现一项手册缺陷：`upperId` 含 demandId，故新 demand 用 `dispatchGeneration=1` **不会**撞单，只有重跑同一 demand 才须换代次——**不改包**（手册在 868 条哈希内，改它要重建 RC），由票 15 写进包外 Release 说明。已具名约束票 15：只在服务端仓建 tag／release，**不得为凑齐三仓写入只读的车载端仓**，协议 `protocol-v0.1.1` 不再动，上传前不得修改包内任何文件。票 27 未决，其 HMI 缺陷仍须作为已知限制第 1 项进发布说明。

- [发布并交接可运行 WIRE_TO_GATE MVP](issues/15-complete-candidate-based-ai-development-start-handoff.md) — **已发布**：`8005-agv-control-server` 的 annotated tag `w2g-mvp-rc-0.1.0` 绑 `9daeef4`（GitHub 侧 tag 对象 peel 证实，且该 commit 就是 `ControlServer_MVP` 当前 tip；`gh` 报的 `targetCommitish=main` 是建 tag 用的分支字段，易误读，已具名留档），该仓唯一一个 release，三个资产全部 `uploaded`。**包内一字节未改**——打包前 `OK=868 MISMATCH=0`、打包后 `OK=868 BAD=0`，手册第 11 节的 `dispatchGeneration` 更正写在**包外** Release 说明里正是为此。四条判据都是回读取证而非上传返回码：远程资产**下回来重算**三个哈希全 MATCH（红侧翻一字符 MISMATCH）；解压到新目录跑**手册第 3 节原文脚本输出 0 行**、翻一字节输出恰好 1 行 `MISMATCH RELEASE-CANDIDATE.md`；协议身份补上票 12 没验的车载端侧——二进制内嵌 `1531489e`／`a467c0c4`／`e04296e9` 与服务端逐字一致，**第四个 `vectorsSha256` 据实记为车载端 ABSENT**（构建期资产，运行时不需要，故不能笼统说「两端完全一致」），三个真值各翻一字符全 ABSENT、一个真在别处的真值也 ABSENT 故绿不空；端到端由票 14 的 generation 7 承担，本票未动车未建单。交接主体是包内手册第 1～13 节，Release 说明只做包外三件事。**票 27 的 HMI 缺陷作为已知限制第 1 项原样进说明**，标注去向未定、落定后回补。**只完成两个仓**：车载端只读仓零 tag 零 release（本会话对其零写入，协议仓亦未动），那一份开票 28 交用户或王昆。未触产品代码故未跑 tier 1。

- [处置生产形态下车载端 HMI 不反映 WIRE_TO_GATE 且无恢复出口](issues/27-route-the-onboard-production-shape-hmi-defect.md) — **转交件起了作用，路由由现实作出**：只读 fetch 发现 owner 已在 `OnboardHmi_MVP@31263b1`（08-30 20:06，现场闭环之后）修掉可见性半边，本仓对该仓全程零写入。两半性质不同：可见性**已修但不在本 RC 内**（本资产建自 `304e6ad`，要它必须重建候选，故本轮未构建未验证）；恢复出口**根本不是车载端能单独修的**——owner 弹回的四点服务端约束在我们可写的 `9daeef4` 上逐条读代码核对**全部属实**（`AdvanceForcedRecoveryGenerationAsync` 只在 `FORCED_MECHANICAL_RECOVERY` 分支内、`WireToGateStore.cs:1352-1372` 对同 attempt 同代次的新 `ResultId` 抛冲突、重放原结果被 replay 忽略），故 `RESUME_AFTER_REPAIR` 没有可收敛的结果身份，车载端 fail-closed 是唯一正确行为而非占位。三选一接口方案涉及协议仓与双人批准，**AI 不代批**，判为本地图范围外。**收掉票 15 的唯一尾巴**：线上 Release 说明已知限制第 1 项从「去向尚未落定」改写为 1a／1b 两段（编号不重排），只动包外、868 条哈希与三个资产一字未改；四条回读取证（改前副本逐字忠实、改后 `VERBATIM MATCH`、三资产 `uploaded` 尺寸不变、tag 对象仍 `0c4d1103…`），比对器翻一字符即证红。给 owner 的答复件在仓外，不代选方案并明说不要等答复。未触产品代码故未跑 tier 1。

- [在车载端只读仓创建对应的版本 tag](issues/28-create-the-onboard-repository-release-tag.md) — **由用户执行，agent 对该只读仓零写入**：annotated tag `w2g-mvp-rc-0.1.0`（与服务端同名）已建在 `8005-agv-onboard-hmi`，**显式绑 40 位完整 SHA `304e6ad`**——本票唯一真风险是打错目标，owner 当日 20:06 推的 `31263b1` 用 `HEAD` 或分支名就会被错标成本轮版本，`merge-base --is-ancestor` 证实该修复**不在** tag 内。不建 Release：缺的只是该仓自身的不可变引用，二进制已随服务端 release 分发过一次，再建空 Release 只会与刚在票 27 改过的包外说明两头漂移。四条判据全是回读取证——ref 是 tag 对象 `bee6224f…`、peel 出的 commit 与 `release-manifest.json` 的 `components.onboardHmi.commit` 逐字一致、annotation 正文本地与远程同 sha256 `0eb3bba8…`、该仓仍零 release 且两分支与服务端 tag／三资产／协议仓两 tag 全未动；**同一归一化下**把正文 `0.1.0` 翻成 `0.1.9` 即 DIFFERS，红侧成立。具名残留：tag 不携带二进制，托管构建每次新 MVID，复核车载端产物的权威来源仍是包内 868 条 SHA-256 而非从此 tag 重建。未触产品代码故未跑 tier 1。

## 地图状态

**已走完。** Destination 在票 15 成立（RC 已发布并由用户验收），票 27 收掉发布说明的最后一条尾巴，
票 28 补齐第三个仓的不可变引用。三个版本绑定仓库现各有一个指向本轮 RC 的不可变引用：
`8005-agv-control-server@w2g-mvp-rc-0.1.0`（→ `9daeef4`，唯一带资产的 release）、
`8005-agv-onboard-hmi@w2g-mvp-rc-0.1.0`（→ `304e6ad`，无 release）、
`8005-agv-protocol@protocol-v0.1.1`（→ `1531489e`）。无开放票据，无未定 fog。
`RESUME_AFTER_REPAIR` 结果身份收敛与 runner 公共模块抽取见下方 Out of scope，均属 RC 之后另起一轮。

## Not yet specified

无。

## Out of scope

- WIRE_TO_GATE 以外的 MES 运输类型、多车调度、多 Sublot 混装、顺路运输、跨地图运输和路径优化。
- 自动充电、充电排队、备用桩改派；MVP 只保留电量准入和人工充电保持/恢复边界。
- MES 完工回写、外部 PDA 集成、完整管理后台、高级运营大盘和长期报表。
- 未经单独授权自动执行真实车辆动作、Golden WPF tier 2/3、工厂 P0～P7 或真实物料试运行。
- 把 Fake 通过、协议生成、Spec 完成、构建成功或 README 齐全单独表述为整个 MVP 软件完成。
- 为赶工删除已接受的安全、持久化、幂等、断联或恢复约束，或用手工演示掩盖核心路径缺失。
- `RESUME_AFTER_REPAIR` 的结果身份收敛（票 27 揭出）。当前协议下 `SlotOperationResumeCommand` 复用原 `slotOperationAttemptId` 且无独立结果消息，而服务端以 `(slotOperationAttemptId, forcedRecoveryGeneration)` 唯一接受 `OperationResult`、`RESUME_AFTER_REPAIR` 又不推进代次，故恢复 workflow 两条路都不收敛，车载端只能 fail-closed。收敛须两端选定三个方案之一（resume 命令带新 identity／服务端在活动 `recoveryActionId` 下允许授权替代结果／协议新增独立 resume result），至少一个要动审批门禁的协议仓、需双人批准，并须新增带 demand 的联合回归且证据不得继承 2026-08-30 的红运行。本地图 Destination 在票 15 已成立、发布时六条已知限制已被接受，故这是 RC 之后的独立一轮，不是本轮的续。owner 侧记录见车载端仓 `31263b1` 的 `docs/W2G_PRODUCTION_HMI_RECOVERY_GAP.md`。
- 把三个 G3 runner 的重复公共函数抽成共享模块（票 21 第 5 项、票 24 第 5 项）。失败形态是启动即抛异常，响亮且立刻，不污染证据；而改动要同时动三个零测试覆盖、承载本地图全部证据的脚本。与到达 RC 无关，RC 之后另起。
