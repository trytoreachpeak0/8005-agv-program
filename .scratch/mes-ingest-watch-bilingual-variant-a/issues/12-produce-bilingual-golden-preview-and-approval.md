# 12 — 生成双语生产预览并完成视觉批准

**What to build:** 在完整集成版本上生成可与已批准 Variant A 原型比较的真实生产窗口中文和英文预览，让用户基于相同数据、窗口、选择和滚动状态确认最终视觉结果及响应式可用性。

**Blocked by:** 11 — 组装完整双语版本并执行发布契约.

**Status:** done

- [x] 在运行任何 tier 2 前向用户说明分钟级成本并取得明确授权；不默认使用全量 suite。
- [x] 通过交互式 Golden 桌面运行覆盖双语主窗口和 Inspector 的最窄完整 suite，不使用 RDP、Enhanced Session 或 PowerShell Direct 截图。
- [x] 中文和英文使用相同 Host 数据、1440×900 窗口、D-001846/AREA 来源未提供选择、筛选及可比滚动位置。
- [x] 预览覆盖概览、Variant A 资格审计、需求系列与 Inspector、错误检索、AREA 编辑/冲突、接入告警、设置、通知和 720 epx 窄窗状态。
- [x] 125%/150% DPI 只在 disposable offline clone 验证，证据证明实际 DPI，完成后删除克隆并复核原 VM 仍为 1920×1080、96 DPI。
- [x] 向用户展示最终真实窗口预览并取得明确批准；任何后续 UI 变化都会使该批准失效。
- [x] 记录源提交、dirty-diff identity、环境、任务结果、全部截图/UIA/日志、通过/失败/跳过和每个跳过的发布归属。
- [x] 不执行 tier 3、稳定性三跑、候选基线生成、基线提升或历史候选批量批准，除非用户另行授权。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Final validation evidence

Final post-fix `watch-ui-journeys` matrix, each with `Total: 1, Failed: 0, Skipped: 0` and 18 bilingual production screenshots:

- 96 DPI, 1440×900: `run-20260828-023605-watch-ui-journeys`
- 96 DPI, 720×600 epx: `run-20260828-024129-watch-ui-journeys`
- 120 DPI, 1440×900: `run-20260828-025328-watch-ui-journeys`
- 120 DPI, 720×600 epx: `run-20260828-025857-watch-ui-journeys`
- 144 DPI, 1440×900: `run-20260828-030432-watch-ui-journeys`
- 144 DPI, 720×600 epx: `run-20260828-030931-watch-ui-journeys`

Each run records source commit `f594d3902bc8b6d86d6e7e3ee5ce421c99774886`, the exact six-file dirty-diff identity carried into the payload, environment JSON, scheduled-task result, build/test logs, screenshots, UIA trees, fake-Host timeline and zero Golden skips. Earlier failed attempts remain preserved as red evidence and were not reused as passing evidence.

The disposable DPI clone and exact export/import workspace were deleted after the 120/144 DPI runs. `final-original-recheck-20260828-031518/environment.json` records the original `gpt_win11` at 1920×1080, 96 DPI, interactive Session 1 with Explorer present; cleanup reported zero Ticket 12 tasks and zero residual Host/Watch/test processes.

Final tier 1 on the fully promoted production/test inputs: `Failed: 0, Passed: 937, Skipped: 137, Total: 1074` (5m10s). The three real SQL Server environment variables were not configured, so their related tests skipped under the repository rule.

Final user-approved Tier 3 evidence:

- Candidate stability: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-ticket-12-text-masked-approved-candidate-2/run-20260828-133609-watch-window-stability/` — 3/3 runs passed; every run contains 11 candidate PNGs, 11 UIA Text mask sidecars and 11 mask overlays; 0 received.
- Proposal review: the same run's `Proposals/` directory contains 11 approval packages, each binding `after.png`, `after.text-mask.json` and `after.text-mask-overlay.png` by SHA-256. The workspace user is recorded as the non-submitter reviewer under the explicit 2026-08-28 approval.
- Promoted stability: `mes/ingest/csharp/.artifacts/golden-renderer/ticket-ticket-12-text-masked-promoted-final/run-20260828-135211-watch-window-promoted-stability/` — 3/3 runs passed, 0 received, 33 comparator-union mask overlays, and pre/post/cleanup environment checks passed.
- The only promoted tolerance evidence is `05-area-filter-profile`: 848 differences were wholly inside the approved UIA Text mask (`classification=text-masked`, `budgetedDifferingPixels=0`). No unmasked tolerance budget was consumed.
- A fail-closed calibration run remains preserved at `ticket-ticket-12-text-masked-approved-candidate/run-20260828-133002-watch-window-stability/`; it rejected a legitimate 47.24% text-heavy page under the initial 40% total-mask cap. The calibrated policy keeps the 15% single-region and 5% comparison-growth guards while setting the measured total cap to 55%.

## Implementation note

`WatchWorkspaceProductionJourneyTests.Operator_reviews_the_complete_production_workspace_and_records_the_shared_preview`
now owns the Ticket 12 evidence matrix inside the existing production journey. It uses one
loopback Host and one production process, pins the Variant A review identity to
`D-001846 · DIE_TO_OVEN · B240811-19` with AREA not provided by the source, captures the
same deterministic page selections in 简体中文 and English, and keeps the Inspector open
on the same generation while the shared language is committed. The evidence-only capture
names include their language and viewport; none are registered with
`WatchProductionBaselineMatrix`, so this change cannot overwrite or promote an approved
baseline. The existing `MESINGEST_WATCH_JOURNEY_CLIENT_EPX=720x600` path reuses the same
matrix for the narrow-window evidence.

No Tier 2 or Tier 3 command was run while adding the harness. After explicit user
authorization, the final Tier 2 matrix above was run and approved, followed by the fresh
candidate/proposal/promotion/promoted Tier 3 sequence recorded above. The user also directed
that future pixel comparisons exclude UIA Text regions; UIA, localization and journey
assertions remain the authority for textual correctness.
