# 06 — 完成普通顶层窗口生命周期与布局持久化

**What to build:** 让 Inspector 完整遵循普通 Windows 顶层窗口语义，并通过现有偏好安全恢复窗口布局。调查人员可以在多显示器上独立摆放、最小化和关闭 Inspector，而 Host 切换或应用退出不会留下旧证据、孤儿窗口或后台请求。

**Blocked by:** 05 — 保证冻结快照、刷新和精确导航一致性。

**Status:** ready-for-human

**UI authority:** [Fluent UI guidance](../../../docs/agents/fluent-ui.md) · [Golden Renderer workflow](../../../docs/agents/golden-renderer.md)

- [x] 只有显式打开/显示动作激活或恢复 Inspector；列表选择和刷新只更新内容，不恢复、置顶、激活或抢焦点。
- [x] 主窗口和 Inspector 可独立最小化；Inspector 无 Owner、`Topmost=false`，Alt+F4 正常关闭，Escape 不关闭窗口。
- [x] 关闭 Inspector 结束内部调查上下文并取消 pending detail；重开时加载当前列表选择，只恢复窗口布局。
- [x] Host 设置变更关闭 Inspector、清除旧 Host detail 并取消请求，但保留有效布局偏好。
- [x] 主窗口关闭时协调器主动关闭 Inspector、取消工作并确保应用无孤儿窗口或请求地干净退出。
- [x] “记住窗口尺寸”向后兼容升级为“记住窗口布局”，同一偏好统一控制主窗口和 Inspector 布局，旧偏好文档仍可加载。
- [x] 保存并恢复 Inspector 的正常尺寸、正常位置、显示器身份和最大化状态；关闭记忆偏好时不持久化这些值。
- [x] 无效坐标、显示器缺失或工作区变化时，将默认 1200×800、最小 720×600 的 Inspector 约束到当前可见工作区，不落在屏幕外。
- [x] 公开协调器/窗口测试覆盖显式激活、非激活更新、独立最小化、Alt+F4、Escape、关闭重开、Host 切换和应用退出。
- [x] 偏好测试覆盖旧格式、opt-out、normal bounds、maximized、monitor identity、无效坐标、缺失显示器和 visible-work-area clamp。
- [x] 从 `mes/ingest/csharp` 运行 Tier 1：`dotnet test MesIngest.Tests`，记录所有通过、失败和跳过。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-22 — implementation ready for golden-machine review

- Implemented explicit-only restore/activation, independent top-level lifecycle,
  close/reopen context reset, Host/application shutdown cleanup, and idempotent
  pending-detail cancellation.
- Extended the version-2 preference document compatibly: the legacy
  `rememberWindowSize` JSON key now drives the UI's “记住窗口布局” choice, while
  main and Inspector normal bounds, monitor identity, and maximized state are
  stored only when the choice is enabled.
- Focused lifecycle/layout/shell/preferences gate: 45 passed, 0 failed, 0 skipped.
- Final post-review Tier 1 `dotnet test MesIngest.Tests`: 637 passed, 0 failed,
  82 skipped, 719 total in 1m56s. All 82 skips are the existing SQL Server
  environment gate because `MES_INGEST_TICKET01_SQLSERVER`,
  `MES_INGEST_TICKET01_EXPECTED_PRODUCT_MAJOR`, and
  `MES_INGEST_TICKET01_EXPECTED_COMPATIBILITY_LEVEL` were not set.
- Six injected lifecycle/layout/opt-out/maximized pseudo-mutations were killed
  by the focused tests and reverted. The review-found same-Series focus leak
  also failed before `_focusedDemandId` cleanup and passed after the fix.
- Tier 2/3, final real-window preview approval, evidence capture, and VM cleanup
  remain unchecked because `AGENTS.md` requires explicit user authorization
  before entering the interactive golden-machine workflow.

### 2026-08-22 — golden-machine validation and visual approval complete

- After explicit user authorization, ran the narrow Tier 2
  `watch-ui-journeys` suite from clean commit `496842f3` on the interactive
  `gpt_win11` golden desktop. Result: 1 passed, 0 failed, 0 skipped.
- Unique evidence directory:
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-demand-series-inspector-e-06/run-20260822-003355-watch-ui-journeys`.
- The run and post-cleanup environment checks passed at 1920x1080 and 96 DPI;
  the scheduled task was absent after cleanup and residual process count was
  zero.
- The user reviewed and approved the final Settings, DemandSeries master,
  Inspector first-observation, and related-events production screenshots.
  Ticket 06 implementation and visual acceptance are complete.
- Tier 3 was not run; no visual baseline was created, promoted, or overwritten.
