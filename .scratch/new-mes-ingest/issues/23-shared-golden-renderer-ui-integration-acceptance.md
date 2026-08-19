# 23 — 共享黄金机 UI 集成验收与基线

**What to build:** 将 19–22 已冻结并通过共享黄金机预览批准的生产 Watch 页面作为一个 integration train，在校准黄金机上完成候选稳定、基线提升和 DPI 正式验收，只提升与获批预览具有同一源码及输出身份且可重复的基线，并为四张实现票留下可共同引用的完整证据。

**Blocked by:** 19 — 生产 Fluent shell、设置与概览；20 — DemandSeries 生产页面；21 — 资格审计与 AREA Variant A 生产页面；22 — Error Search Variant A 与接入告警生产页面

**Status:** needs-info

- [x] 正式门禁遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，只在 gpt_win11 的校准交互桌面通过交互计划任务驱动 WPF 和 FlaUI；PowerShell Direct 仅用于部署、监控和取回证据，不用于截图或 UI 驱动。
- [x] 为本次冻结的 19–22 源身份建立唯一、不覆盖历史的证据目录，记录提交与 dirty diff 身份、环境报告、任务原生退出码、恢复/构建/测试日志、截图、UIA 树、Verify XML、received/diff、通过或失败或 skip 计数及每个 named skip 的 release gate。
- [ ] 先运行全部相关代码与非像素回归，再在 1920×1080、96 DPI、zh-CN、浅色主题、SoftwareOnly 的真实交互桌面运行受影响的 UI Automation、键盘、标题栏、导航、分页、详情、InfoBar、剪贴板、高对比度语义和真实窗口旅程。
- [x] 开始候选门禁前，核对 19–22 的共享黄金机预览、用户批准、源码提交与 dirty diff 身份确实对应本票冻结输出；身份和视觉/UIA/DPI 输出均未变化时不得重复生成或要求再次批准同一预览，若不一致则保留失效证据、只重做受影响预览并重新取得批准。
- [ ] 用户批准后生成全新 candidate matrix，不批量提升历史 received/candidate；对候选连续运行 `-Runs` 次（默认 3，见 [Golden WPF renderer](../../../docs/agents/golden-renderer.md) 的 Repetition count），每一轮的 PNG 与 XML 必须字节完全一致，或在该文档的 Visual equivalence 判据下被判定为视觉等价；任何被容差接受的 step 都要列入证据并在审批时人工复核，任何失败都保留 red evidence、解释原因并从第一轮重新计数。
- [x] 为每个受影响场景生成 before/after/diff 证据，只提升用户明确批准的候选；提升后对同一矩阵再连续运行同样的 `-Runs` 次并要求 `0 received`，不以一次成功重跑掩盖先前失败。
- [x] 从校准 VM 导出具有新 VM ID 的一次性离线克隆，断开网络后分别在 125%（120 DPI）和 150%（144 DPI）运行所需 watch-ui-journeys；交互环境报告必须证明实际 DPI，且不改变原 gpt_win11 的 96 DPI。
- [x] DPI 旅程证明 720 epx 最小宽度与规定缩放下，标题栏按钮、导航、页面状态、筛选、分页、三列或 master-detail 边界、关键命令和焦点视觉能重排或滚动而不裁切。
- [x] 完成后清除交互计划任务、残留 Watch/test 进程、临时 payload、DPI 克隆及其精确导出/导入目录，并复核原 VM 为 1920×1080、96 DPI、Explorer 与输入桌面处于正确交互会话。
- [x] 将 19–22 的共享预览证据和本票唯一门禁 evidence directory、环境身份、用户批准记录、named skips 与清理结果互相链接；这些实现票不重复执行各自的完整候选稳定、提升后稳定和 DPI clone 流程。
- [ ] 票 23 完成后，只有后续改动造成视觉、XAML、UI Automation 或 DPI 输出变化，或某场景失败时，才重跑受影响场景并重新完成被失效的批准与连续计数；与 UI 输出无关的后端、文档或打包变化不得触发无意义的整套视觉重验。
- [x] Read `docs/agents/golden-renderer.md`.
- [ ] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## 进行中的验收状态（2026-08-19）

生产 19–22 的窗口基线验收已完成：预览获批、候选 10 轮稳定、11 张基线提升、提升后 10 轮
`0 received`、125%/150% DPI 旅程通过、克隆与计划任务清理完毕、原 VM 复核为 1920x1080 / 96 DPI。
完整证据与交叉链接见 [`.artifacts/ticket23-acceptance/EVIDENCE-INDEX.md`](../../../.artifacts/ticket23-acceptance/EVIDENCE-INDEX.md)。

**未勾选的三项都被同一个红卡住**：`Test-WatchXamlBaselineStability.ps1 -Runs 10` 在第 6 轮
失败，`overview-loaded-2560x1440.received.png` 与第 1 轮不一致（695,918 像素、最大 delta 166、
全部有彩、XML 完全相同）。这是 legacy `MainWindow.xaml` 的 `OverviewDemandsButton` 卡片渲染出
蓝色强调底色，属于交互态泄漏到截图，不是抗锯齿噪声，视觉等价判据会（正确地）拒绝它。
已提升的 11 张生产基线不受影响。红证据保留在
`mes/ingest/csharp/.artifacts/golden-renderer/ticket-23-xaml-gate/run-20260819-090314-watch-xaml-stability`。

待办：修复 `WatchXamlVisualTests` 截图前不中和指针/焦点的问题（窗口路径已有
`MovePointerOffWindow()` 与三帧一致检查，XAML 路径完全没有），然后从第 1 轮重新计数。
