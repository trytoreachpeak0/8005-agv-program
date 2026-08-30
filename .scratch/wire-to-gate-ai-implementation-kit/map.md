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

## Not yet specified

无。

## Out of scope

- WIRE_TO_GATE 以外的 MES 运输类型、多车调度、多 Sublot 混装、顺路运输、跨地图运输和路径优化。
- 自动充电、充电排队、备用桩改派；MVP 只保留电量准入和人工充电保持/恢复边界。
- MES 完工回写、外部 PDA 集成、完整管理后台、高级运营大盘和长期报表。
- 未经单独授权自动执行真实车辆动作、Golden WPF tier 2/3、工厂 P0～P7 或真实物料试运行。
- 把 Fake 通过、协议生成、Spec 完成、构建成功或 README 齐全单独表述为整个 MVP 软件完成。
- 为赶工删除已接受的安全、持久化、幂等、断联或恢复约束，或用手工演示掩盖核心路径缺失。
- 把三个 G3 runner 的重复公共函数抽成共享模块（票 21 第 5 项、票 24 第 5 项）。失败形态是启动即抛异常，响亮且立刻，不污染证据；而改动要同时动三个零测试覆盖、承载本地图全部证据的脚本。与到达 RC 无关，RC 之后另起。
