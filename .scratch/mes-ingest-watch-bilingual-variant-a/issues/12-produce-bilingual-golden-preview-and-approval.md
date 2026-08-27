# 12 — 生成双语生产预览并完成视觉批准

**What to build:** 在完整集成版本上生成可与已批准 Variant A 原型比较的真实生产窗口中文和英文预览，让用户基于相同数据、窗口、选择和滚动状态确认最终视觉结果及响应式可用性。

**Blocked by:** 11 — 组装完整双语版本并执行发布契约.

**Status:** needs-info

- [ ] 在运行任何 tier 2 前向用户说明分钟级成本并取得明确授权；不默认使用全量 suite。
- [ ] 通过交互式 Golden 桌面运行覆盖双语主窗口和 Inspector 的最窄完整 suite，不使用 RDP、Enhanced Session 或 PowerShell Direct 截图。
- [ ] 中文和英文使用相同 Host 数据、1440×900 窗口、D-001846/AREA 来源未提供选择、筛选及可比滚动位置。
- [ ] 预览覆盖概览、Variant A 资格审计、需求系列与 Inspector、错误检索、AREA 编辑/冲突、接入告警、设置、通知和 720 epx 窄窗状态。
- [ ] 125%/150% DPI 只在 disposable offline clone 验证，证据证明实际 DPI，完成后删除克隆并复核原 VM 仍为 1920×1080、96 DPI。
- [ ] 向用户展示最终真实窗口预览并取得明确批准；任何后续 UI 变化都会使该批准失效。
- [ ] 记录源提交、dirty-diff identity、环境、任务结果、全部截图/UIA/日志、通过/失败/跳过和每个跳过的发布归属。
- [ ] 不执行 tier 3、稳定性三跑、候选基线生成、基线提升或历史候选批量批准，除非用户另行授权。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

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

No Tier 2, Tier 3, Golden, stability, candidate-baseline, or promotion command was run while
adding this harness. The execution and approval checklist above intentionally remains open
until the user authorizes the interactive Golden run and reviews its retrieved evidence.
