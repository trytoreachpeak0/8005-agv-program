# 冻结一周可运行 MVP 的完成定义与最薄实施输入

Type: task
Mode: AFK
Status: resolved

## Question

现有 MVP 规格、两仓交接、协议交接、契约向量、集成切片、需求适用性表、accepted ADR 和原型 A，相对“一周内开发、测试并发布整个可运行 WIRE_TO_GATE MVP”还缺少什么；怎样把缺口压缩成第 1 天可冻结的完成定义、最薄 Spec、代码工作包和双仓协作契约？

本票必须在同一轮生成：可执行的 MVP Definition of Done；工作流中立的三仓入口；每个 W2G-IS-00～07 的最小代码工作包；候选冻结、双方 Fake/G2、逐切片联合运行、协议变更、证据失效和正式 release/G3 的协作状态机；截止 2026-08-28 17:00 的压缩日程和砍项禁区。产物必须足够让任意 AI 开始写代码，但不得重复撰写已有需求正文。

答案必须区分已具权威、可由 AI 安全决定、必须补成机器资产、必须由人员决定和必须由环境提供；不得把缺少硬件误报为文档错误，也不得要求同事使用 Matt、Codex 或特定工作流。本票应在第 1 天完成，不能成为后续产品开发的长文档阶段。

## Answer

审计结论：旧交接包已经完整固定业务范围、348 条需求适用性、跨端职责、协议治理、W2G-IS-00～07、共同向量、原型 A 和现场门禁；24 项资产的 SHA-256 重新计算后全部与旧 manifest 一致。无需再写一份需求文档。相对“可运行软件”真正缺失的是机器协议资产、两个产品实现、标准构建/测试/发布入口、真实联合证据和人员批准。

本票生成以下工作流中立的最薄实施基线：

- [`START-HERE.md`](../starter/START-HERE.md)：三仓入口、权威顺序、环境事实和每次开工步骤；
- [`definition-of-done.md`](../starter/definition-of-done.md)：D1～D7 软件完成门禁与不可砍安全底座；
- [`slice-work-packages.tsv`](../starter/slice-work-packages.tsv)：W2G-IS-00～07 的两端最小代码输出、联合出口和证据；
- [`collaboration-contract.md`](../starter/collaboration-contract.md)：候选冻结、G1/G2/G3、真实批准、逐切片联调、协议变更和证据失效状态机；
- [`gap-ledger.tsv`](../starter/gap-ledger.tsv)：已具权威、AI 可决定、机器资产、人员决定和环境输入的 14 项缺口账本；
- [`compressed-sprint-plan.md`](../starter/compressed-sprint-plan.md)：截至 2026-08-28 17:00 的极限冲刺顺序和砍项禁区；
- [`asset-manifest.tsv`](../starter/asset-manifest.tsv)：上述六项内容的字节数和 SHA-256。

完成定义不再把“AI 可以开始开发”算成交付：必须有两个可安装运行的产品、同一不可变协议身份、现有 MesIngest、真实 RIoT 移动、八仓 IO 模拟器闭环、W2G-IS-00～07 的 G1/双方 G2/G3、干净环境安装/重启和用户端到端验收。

当前阻断已明确分流：ControlServer 技术栈由研究票冻结；OnboardHmi/IO 方案和 GitHub accepted 状态由王昆确认；RIoT 技术车辆 ID及取货/关卡站由安全注入 CallApiKey 后只读解析并由用户确认。真实 IO/工控机和真实物料试运行明确延后，不冒充本周软件资格。

验证结果：旧权威 manifest `24/24` 通过；本地 Markdown 链接失败 `0`；切片 TSV `8/8` 且 ID 唯一；缺口 TSV `14` 行可解析；`git diff --check` 无错误。未执行产品测试，因为本票只生成实施基线，没有产品代码或构建输入变更。
