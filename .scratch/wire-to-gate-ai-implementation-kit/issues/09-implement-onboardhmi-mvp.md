# 实现并自测 OnboardHmi MVP

Type: task
Mode: AFK
Status: resolved
Blocked by: 07

## Question

如何在 `OnboardHmi_MVP` 分支按 W2G-IS-00～07 实现可运行 OnboardHmi：连接/session/readiness、能力/安全/journal 报告、原型 A 生产 UI、扫码与装货确认、八仓顺序物理闭环、自动卸货、可靠结果重放、断联安全收尾、重启恢复、Fake ControlServer、健康检查、配置与结构化日志？

每个切片必须先写或更新自动化测试，再实现最小生产代码，运行本端 G2 和 Fake ControlServer 场景并保存绑定 commit/协议候选的证据。UI 必须映射选定原型 A 的窗口层级、布局、状态和交互。本轮同时交付独立八仓 IO 模拟器，并让生产 OnboardHmi 只通过正式 IO 抽象消费它；模拟结果不能称为真实 IO 或目标硬件通过。

## Answer

已在远程 `OnboardHmi_MVP` 完成并推送生产提交 `398a957662cacb6c0f49ddd78da12d896a1469be`，精确绑定协议候选 `72ddde595165468520d9f3a46b25e4aa4eec0c3f` 与 manifest SHA-256 `e878d89e820535fe1eb64b85681b9c2994fb98646309e6ba768219c5c8735f2e`。实现包括精确候选身份校验、五步 session/recovery/readiness、活动心跳及掉线闭锁、SQLite `OnboardExecutionJournal`、批量八仓物理闭环执行器、持久去重/可靠结果/重启恢复、断联时只收尾冻结 `ActiveUnlockSet`、正式 `ISlotIoProvider` HTTP 适配器、独立八仓 IO Simulator、Fake ControlServer 与 Conformance 工具。联合审计发现的恢复报告 checkpoint、`pendingResults` 结构和 `reasonCodes` 解析偏差也已在该提交修复。

生产组合根已接入候选 ControlServer 会话：凭据只从配置指定的环境变量读取；只有既有执行链可操作、候选连接在线且候选业务状态为 `READY` 时才允许扫码，心跳丢失会锁存 `CONTROL_SERVER_CONNECTION_LOST` 并禁止新操作。默认生产 IO 入口通过 `SlotIoModuleClientAdapter` 消费业务状态 Provider，不直接暴露 DI 极性。IO Simulator 默认监听 `127.0.0.1:58006`，八仓初始均为 `online + EMPTY + LOCKED + RESET + CLEAR`，支持 Offline、ResponseTimeout、Unknown、LockFeedbackAbnormal、OutputStuck、RequestLost、ResponseLost 和 Crashed 故障注入。

原型 A 已作为生产 UI 权威映射到新的 1024×768 WPF 主窗口，保持“顶部车辆与四状态—左侧旅程—中央唯一任务/动作—右侧固定 2×4 八仓”结构和 fail-closed 提示；原型项目、假数据和原型专用词没有进入生产依赖。未运行需单独授权且成本较高的 Golden WPF tier 2/3，因此本票不声称取得目标工控机视觉批准。

验证结果：冻结 SDK `8.0.424` / runtime `8.0.30` 的 Release 全解决方案构建为 0 warning、0 error；车载自动化测试 57/57 通过、0 skip。独立 IO Simulator、Fake ControlServer 和真实车载 Conformance 三进程完成八仓读取、精确候选五步恢复、SQLite journal、`READY` 和 Heartbeat/HeartbeatAck；真实 ControlServer 还正确接收非空 pending result 并返回 `RECOVERY_REQUIRED / PENDING_FACT_RECONCILIATION_REQUIRED`。最终提交后串行运行 W2G-IS-00～07，测试数分别为 1、1、1、2、1、1、1、2，八个 G2 全部 PASS；证据保存在产品仓库忽略目录 `artifacts/g2/issue10-398a957-post-fix/`，每份 `gate-result.json` 均绑定上述实现 commit、协议 commit 和 manifest hash。

本票只关闭 OnboardHmi 候选实现与本地 G2。真实 ControlServer 的 Demand/站点/批量仓位命令分发尚未完全替换旧规则执行链，协议仍为 `CANDIDATE_UNAPPROVED`；双仓 G3、真实 RIoT/车辆/IO、安装包、Golden WPF 用户预览及现场验收仍由后续票据负责，不能据此宣称整个 MVP 或真实移动闭环完成。

## Superseded — 2026-08-25

用户随后明确决定 OnboardHmi 必须由王昆从本人提交 `bc56fa9aebd98e8cd488fa1f30a0d95bfd40c93e` 基线自行开发，AI 只留下交接文档。远程 `OnboardHmi_MVP@05bf9f4781828dcd4e63cbb7349e4cebd6a25a85` 已通过可追溯 revert 移除 `2eeecf6`、`f265cd8`、`398a957`、`c41160c` 的全部 AI 产品代码；与 `bc56fa9` 的当前树比较仅剩 `README.md` 和 `docs/ONBOARD_DEVELOPER_HANDOFF.md` 两项文档差异。王昆基线使用本机 .NET 9 SDK完成 Release 构建，结果 0 warning/0 error，原有 48/48 单测通过。

因此上方 `## Answer` 只保留为已经发生过的 AI 候选历史，不再代表当前产品状态、王昆本人实现、有效 Onboard G2 或后续 G3 输入。新的 Onboard 完成结论必须等待王昆本人提交和确认。
