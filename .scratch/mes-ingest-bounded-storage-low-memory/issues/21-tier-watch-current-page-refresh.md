# 21 — 完成 Watch 刷新与保护状态呈现

**What to build:** 在一次 Watch 实现与视觉验证中完成当前页 30/60 秒刷新、Inspector 单一读取边界，以及 StoragePressurePause 和历史重置状态呈现，不增加高风险写能力。

**Blocked by:** 20 — 完成精确 V2 契约整体切换.

**Status:** ready-for-human

- [x] Overview 与 CurrentIngestAttention 默认 30 秒，DemandSeries、ReadabilityAudit 与 ErrorSearch 默认 60 秒。
- [x] 自动刷新始终只作用于当前可见页和当前页窗口；切页停止旧页计时并按目标页档位重新调度。
- [x] 刷新继续单飞、不排队、可取消；失败或取消保留最后成功窗口并明确其时间。
- [x] Inspector 不拥有 Host client、Timer、refresh loop、独立缓存或 snapshot，只接收同一冻结上下文的 presentation。
- [x] 默认设置、持久化设置、页面切换、慢请求和 Inspector 行为由确定性时间与生产 Watch 测试覆盖。
- [x] 保持现有 Fluent 页面层级与自动刷新设置语义，不增加手动刷新或启用/禁用命令。
- [x] 全局状态栏和概览健康区以文本、图标和可访问名称呈现 StoragePressurePause 与历史重置状态，不只依赖颜色。
- [x] 暂停状态显示原因、最后成功 PollTrace、最后成功投影时间、earliest available 和精确本地恢复指引。
- [x] 历史重置状态显示新 HistoryEpoch、建立进度、当前 503 原因和 HistoryResetAcknowledgement 本地指引。
- [x] Watch 不增加恢复、确认、删库或其它管理按钮；ScriptedFakeHost 覆盖正常、15% 告警、暂停、待确认重建、确认后恢复和 Host 离线。
- [x] 保留现有已接受生产窗口层级、页面结构、间距和交互，不发明替代信息架构。
- [x] 复用现有 workspace、refresh coordinator、Inspector coordinator、状态栏、概览健康区和 ScriptedFakeHost；不新建页面、导航层、状态框架或第二套 UI 自动化夹具。
- [x] Read [Fluent UI rules](../../../docs/agents/fluent-ui.md) and [golden renderer](../../../docs/agents/golden-renderer.md) before implementation.
- [x] 对全部合并改动只运行一次最窄且完整的 golden-machine suite；运行前说明成本并取得用户批准。
- [x] User approved the final real-window preview.
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
- [x] 开发期只运行聚焦 Watch 非像素测试和一次 Tier 1；获批后只运行一个覆盖全部受影响状态的完整 Tier 2 suite，不运行 Tier 3、不推广基线、不为同一候选重复预览。
- [x] 正常代理工作目标在 3 小时内完成，不含等待用户批准的墙钟时间；若预览暴露真实视觉差异，按 Golden Renderer 规则升级，不以时间目标跳过修复。

## Comments

- 2026-08-24：实现前完整读取 Fluent/Golden 规则并在当前树、全部 Git refs/history、worktrees 与既有 evidence 中定位实际接受原型。设计权威为 `MesIngest.Watch.FluentPrototype` 的 SelectedShell（Overview A、Error Search A、AREA D、Inspector E）；生产映射保持单一 FluentWindow、TitleBar、LeftMinimal NavigationView、24px 外边距、12/16px 节奏、既有页面层级与交互，不引入原型项目、假数据、新页面或管理按钮。
- 2026-08-24：完成当前页 30/60 秒默认刷新、切页取消旧请求、单飞不排队、Overview 有界保护详情读取与独立 Protection slot；补齐 Current Attention wire 的 HistoryCleanup/StoragePressure/保护证据，状态栏、概览健康区和只读证据区完整呈现 warning、StoragePressurePause、HistoryReset、恢复与离线保留。Inspector 仍只消费冻结 presentation，不拥有 client、timer、refresh loop 或独立 snapshot。
- 2026-08-24：纵向 TDD 与两轴 review 完成。Standards 修复保护字段 data clump、隐藏 Current Attention 状态覆盖和全 AREA 详情导航缺口；Spec 修复 warning/pause 语义、筛选页覆盖专用保护槽、精确本地 CLI 及真实窗口状态编排。最终 Standards / Spec 均为 0 findings。聚焦 Watch 回归为 409 passed / 7 SQL-gated skipped；最终相关 UI 非像素组合回归为 43 passed / 1 golden-environment skip，隔离 Demand Series 前置修复为 2 passed / 0 skipped。
- 2026-08-25：最终 Tier 1 从 `mes/ingest/csharp` 运行 `dotnet test MesIngest.Tests`，显式设置真实默认 SQL Server（Enterprise Evaluation，非 LocalDB）、ProductMajor 16、compatibility 160；865 passed、0 failed、0 skipped，12 分 37 秒。
- 2026-08-25：每个 golden 候选只运行一次完整 `watch-production-preview`；用户逐次批准并在红色 evidence 后授权继续修复。五个红色 run 均保留：`run-20260824-225728-watch-production-preview`、`run-20260824-233828-watch-production-preview`、`run-20260824-235037-watch-production-preview`、`run-20260825-000958-watch-production-preview`、`run-20260825-001757-watch-production-preview`。修复均由对应日志/timeline/UIA 直接驱动，未覆盖 evidence。
- 2026-08-25：最终完整 Tier 2 `watch-production-preview` 通过。唯一成功 evidence 为 `mes/ingest/csharp/.artifacts/golden-renderer/ticket-21/run-20260825-002555-watch-production-preview`：`watch-vm-tests` 146 passed / 0 failed / 5 skipped；`watch-ui-journeys` 1 passed / 0 failed / 0 skipped。五个 named skips 均属于本 suite 未启用的 candidate/baseline fixture：`Candidate_directories_are_visually_equivalent`、`A_different_page_is_rejected`、`A_one_pixel_control_geometry_change_is_rejected`、`A_one_pixel_glyph_shift_is_rejected`、`The_recorded_antialiasing_flip_is_accepted`。未运行 Tier 3，未比较、批准、覆盖或推广 baseline。
- 2026-08-25：用户明确批准最终真实窗口 preview。Ticket 21 scheduled task 已注销、残留测试进程为 0；清理后原 VM 复核为 1920x1080、96 DPI、100% 缩放、Explorer Session 1，随后恢复关闭。一个 2026-08-21 的既有无关 PostCleanup task 保留未动。Ticket 21 实现与验收完成，状态转为 `ready-for-human`；Ticket 22 保持已并入/wontfix，不再单独实施。
