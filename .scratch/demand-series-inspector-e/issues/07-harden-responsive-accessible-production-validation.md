# 07 — 完成响应式、无障碍和生产验证门禁

**What to build:** 将完整 E 调查工作台加固为可发布的生产体验：在最小窗口和常用分辨率下不裁切，在键盘与 UI Automation 下完整可操作，并以仓库 Tier 1 和经用户授权的 Golden Renderer 流程验证所有关键调查状态。

**Blocked by:** 06 — 完成普通顶层窗口生命周期与布局持久化。

**Status:** ready-for-human

**UI authority:** [Fluent UI guidance](../../../docs/agents/fluent-ui.md) · [Golden Renderer workflow](../../../docs/agents/golden-renderer.md)

- [x] Inspector 在 720×600 最小尺寸下纵向重排并可滚动；紧凑上下文、Tab、世代列表、事实、MES 证据和事件均可达且不裁切。
- [x] 1440×900 与 1920×1080、100%/96 DPI 下保持 E 信息层级、紧凑密度和可读性，世代列表在多项数据下继续虚拟化。
- [x] 打开/显示动作、一级 Tab、世代导航、当前/选中状态、形成原因、相关事件、事件过滤、stale/failure、absence/conflict 和证据网格具有稳定且有意义的 AutomationProperties。
- [x] 720×600 下键盘 Tab 顺序完整可预测；Enter、Space、Tab 切换、过滤和世代选择不依赖鼠标，Escape/Alt+F4 遵守窗口约定。
- [x] 生产壳测试证明旧内联详情、splitter 和 toggle 已完全移除，列表满高且没有并存的第二套详情实现或 runtime feature flag。
- [x] 自动化场景覆盖空列表、初始首行、第一代单侧证据、归档前再现、归档后 `LONG_GONE_BUT_VISIBLE`、未知原因、重复原始行、多世代滚动、相关事件、stale detail 和 target-switch failure。
- [x] 从 `mes/ingest/csharp` 运行完整 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过；不把 Golden Renderer 计入“full test suite”。
- [x] Tier 2/3 不自行运行：先说明所选最窄 suite、预计成本和验证目的，并取得用户许可。
- [x] Golden-machine 预览必须来自校准的 `gpt_win11` interactive task；本机、PowerShell Direct、RDP 或未批准 candidate 不构成视觉验收。
- [ ] 任何 baseline promotion 都在用户审阅最终真实窗口预览并明确批准后进行，保留 red evidence，并遵守 candidate stability、before/after/diff 和 promoted-baseline `0 received` 顺序。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-22 — implementation ready for golden-machine review

- Hardened the accepted E production window at the existing 900 epx breakpoint:
  the compact Series/snapshot context, selected-generation identity/actions, and
  event filters reflow into bounded rows at 720×600; the generation workbench
  remains vertically scrollable, while 1440×900 and 1920×1080 retain the 300 epx
  virtualized generation navigator and side-by-side evidence workspace.
- Added explicit task-scoped keyboard tab order and dynamic UI Automation names
  for Series identity, current presence, selected/current generation, formation
  reason, event filters, and evidence. Target-switch failure now clears the old
  reason tooltip, boundary text, MES count, body items, and UIA help/name state.
- Focused Inspector/lifecycle/layout/production-shell gate: 67 passed, 0 failed,
  0 skipped. `MesIngest.Watch.UiTests` also builds with 0 warnings and 0 errors.
- Final Tier 1 `dotnet test MesIngest.Tests`: 641 passed, 0 failed, 82 skipped,
  723 total in 1m23s. All 82 skips are the existing SQL Server environment gate because
  `MES_INGEST_TICKET01_SQLSERVER`,
  `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR`, and
  `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL` were not set.
- Tier 2/3 and final visual acceptance remain unchecked pending explicit user
  authorization for the calibrated `gpt_win11` interactive workflow.
- The post-implementation two-axis review found one Fluent spacing violation,
  one responsive-layout duplication smell, and one 720×600 keyboard-coverage
  gap. The spacing now follows the 8/12/16/24 rhythm, shared reflow uses one
  helper, and real Tab traversal covers both event and conflict-evidence grids.

### 2026-08-22 — golden-machine Tier 2 previews ready for user approval

- After explicit user authorization, ran the narrow `watch-ui-journeys` suite
  twice from clean detached commit `7111f77c` on the calibrated interactive
  `gpt_win11` desktop. No Tier 3 suite or baseline comparison/promotion ran.
- 720×600 evidence-only run (`JourneyClientEpx=720x600`): 1 passed, 0 failed,
  0 skipped. Unique evidence directory:
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-07/run-20260822-031219-watch-ui-journeys-720x600`.
- Default 1440×900 run on the 1920×1080/96 DPI desktop: 1 passed, 0 failed,
  0 skipped. Unique evidence directory:
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-07/run-20260822-031653-watch-ui-journeys-1440x900`.
- Both pre/post environment gates reported 1920×1080, 96 DPI, interactive
  Explorer, light theme, zh-CN, China Standard Time, required fonts, and
  SoftwareOnly rendering. Both cleanups reported no scheduled task, no residual
  process, successful post-cleanup environment recheck, and zero named skips.
- The isolated validation worktree was clean, copied evidence was retained in
  the main workspace, and the temporary worktree was removed. Final visual user
  approval remains unchecked pending review of the real Inspector screenshots.
