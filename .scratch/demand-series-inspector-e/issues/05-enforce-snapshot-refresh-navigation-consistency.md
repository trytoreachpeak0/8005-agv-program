# 05 — 保证冻结快照、刷新和精确导航一致性

**What to build:** 让 Inspector 在快速选取、自动刷新、页面切换和跨工作流下钻中始终保持身份与证据一致：只有当前 Host、Series、冻结快照和聚焦世代仍匹配的响应才能提交，失败或晚到响应不会把旧证据放到新目标之下。

**Blocked by:** 03 — 呈现再现原因与完整 MES 边界证据；04 — 交付真实事件调查与相关事件跳转。

**Status:** ready-for-human

**UI authority:** [Fluent UI guidance](../../../docs/agents/fluent-ui.md) · [Golden Renderer workflow](../../../docs/agents/golden-renderer.md)

- [x] Session 将稳定列表选择与详情加载表达为两个公开操作；Inspector 关闭时的选择或普通 DemandSeries 导航不会获取不可见详情。
- [x] 选择切换立即显示新 Series 身份并清除旧正文；详情只在 Host generation、SeriesId、冻结 snapshot reference 和 focused DemandId 全部匹配时原子提交。
- [x] 关闭 Inspector、目标变更、Host 切换和应用关闭会取消或失效化 pending request，晚到响应不能覆盖当前调查。
- [x] 同 Series 刷新保留仍存在的 focused DemandId、事件过滤、选中错误/证据上下文、列宽和滚动位置；失效身份回落到明确默认状态。
- [x] 切换 Series 清除 generation-specific focus、过滤和证据状态，不把旧 Series 内部上下文带入新目标。
- [x] 当前目标刷新失败时保留最后成功详情并显示 stale/error；目标切换失败时只显示请求目标失败态，不保留上一 Series 正文。
- [x] 刷新后选中项离开结果集时清除选择与详情，不静默选择另一 Series。
- [x] 离开 DemandSeries 页面暂停该页面刷新，同时允许已打开 Inspector 保留最后成功 presentation 和快照时间；返回页面后再恢复刷新。
- [x] 来自 overview、qualification audit、error search 和 current attention 的精确导航定位 Series、显示 Inspector、呈现 source snapshot comparison，并用可选 `FocusedDemandId` 建立初始世代焦点。
- [x] 公开 Session/协调器测试覆盖 closed-no-fetch、冻结快照传播、过期响应拒绝、当前目标陈旧保留、切换目标清理、页面暂停和精确下钻。
- [x] 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

- 2026-08-21：实现与双轴审查修复完成并通过最终 Tier 1：`Passed 623 / Failed 0 / Skipped 82 / Total 705`。82 项均为未配置 `MES_INGEST_TICKET01_SQLSERVER`、`MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR`、`MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL` 时按仓库约定跳过的真实 SQL Server 集成测试；本票据未改 SQL。
- 2026-08-21：`/code-review` 的 Standards 与 Spec 复核均确认无剩余硬缺口；审查中发现的新旧冻结快照混合、真实滚动视口保留、overview 之外三条精确下钻测试缺口均已修复。
- 2026-08-21：本次增加 Inspector 加载/失败/陈旧 `InfoBar` 和 Current Attention 精确下钻命令，属于 WPF UI 变更。按 `AGENTS.md` 未自行进入 Tier 2/3；需用户授权后在交互式 golden VM 上运行最窄受影响套件并完成预览审批。
- 2026-08-21：用户授权后，从干净提交 `a4a1fdfe` 在 `gpt_win11` 交互桌面运行最窄完整 Tier 2：`watch-ui-journeys`，结果 `Total 1 / Failed 0 / Skipped 0`。唯一证据目录：`mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-05/run-20260821-232048-watch-ui-journeys`。运行前、运行后与清理后的环境检查均通过 1920×1080、96 DPI；scheduled task 已注销，残留进程为 0。
- 2026-08-21：首次 Tier 2 红色证据保留在 `run-20260821-231438-watch-ui-journeys`；它发现 UI 测试项目仍调用已移除的 `SelectDemandSeriesAsync`。迁移到稳定选择与显式详情加载后，本地 Release 构建 `0 warning / 0 error`，受影响 Session 测试 `27/27` 通过，并以 `a4a1fdfe` 提交。
