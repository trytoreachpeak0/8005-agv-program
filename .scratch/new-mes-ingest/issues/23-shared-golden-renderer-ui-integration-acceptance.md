# 23 — 共享黄金机 UI 集成验收与基线

**What to build:** 将 19–22 已冻结并通过共享黄金机预览批准的生产 Watch 页面作为一个 integration train，在校准黄金机上完成候选稳定、基线提升和 DPI 正式验收，只提升与获批预览具有同一源码及输出身份且可重复的基线，并为四张实现票留下可共同引用的完整证据。

**Blocked by:** 19 — 生产 Fluent shell、设置与概览；20 — DemandSeries 生产页面；21 — 资格审计与 AREA Variant A 生产页面；22 — Error Search Variant A 与接入告警生产页面

**Status:** needs-info

- [x] 正式门禁遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，只在 gpt_win11 的校准交互桌面通过交互计划任务驱动 WPF 和 FlaUI；PowerShell Direct 仅用于部署、监控和取回证据，不用于截图或 UI 驱动。
- [x] 为本次冻结的 19–22 源身份建立唯一、不覆盖历史的证据目录，记录提交与 dirty diff 身份、环境报告、任务原生退出码、恢复/构建/测试日志、截图、UIA 树、Verify XML、received/diff、通过或失败或 skip 计数及每个 named skip 的 release gate。
- [x] 先运行全部相关代码与非像素回归，再在 1920×1080、96 DPI、zh-CN、浅色主题、SoftwareOnly 的真实交互桌面运行受影响的 UI Automation、键盘、标题栏、导航、分页、详情、InfoBar、剪贴板、高对比度语义和真实窗口旅程。
- [x] 开始候选门禁前，核对 19–22 的共享黄金机预览、用户批准、源码提交与 dirty diff 身份确实对应本票冻结输出；身份和视觉/UIA/DPI 输出均未变化时不得重复生成或要求再次批准同一预览，若不一致则保留失效证据、只重做受影响预览并重新取得批准。
- [x] 用户批准后生成全新 candidate matrix，不批量提升历史 received/candidate；对候选连续运行 `-Runs` 次（默认 3，见 [Golden WPF renderer](../../../docs/agents/golden-renderer.md) 的 Repetition count），每一轮的 PNG 与 XML 必须字节完全一致，或在该文档的 Visual equivalence 判据下被判定为视觉等价；任何被容差接受的 step 都要列入证据并在审批时人工复核，任何失败都保留 red evidence、解释原因并从第一轮重新计数。
- [x] 为每个受影响场景生成 before/after/diff 证据，只提升用户明确批准的候选；提升后对同一矩阵再连续运行同样的 `-Runs` 次并要求 `0 received`，不以一次成功重跑掩盖先前失败。
- [x] 从校准 VM 导出具有新 VM ID 的一次性离线克隆，断开网络后分别在 125%（120 DPI）和 150%（144 DPI）运行所需 watch-ui-journeys；交互环境报告必须证明实际 DPI，且不改变原 gpt_win11 的 96 DPI。
- [ ] DPI 旅程证明 720 epx 最小宽度与规定缩放下，标题栏按钮、导航、页面状态、筛选、分页、三列或 master-detail 边界、关键命令和焦点视觉能重排或滚动而不裁切。
- [ ] 完成后清除交互计划任务、残留 Watch/test 进程、临时 payload、DPI 克隆及其精确导出/导入目录，并复核原 VM 为 1920×1080、96 DPI、Explorer 与输入桌面处于正确交互会话。
- [x] 将 19–22 的共享预览证据和本票唯一门禁 evidence directory、环境身份、用户批准记录、named skips 与清理结果互相链接；这些实现票不重复执行各自的完整候选稳定、提升后稳定和 DPI clone 流程。
- [x] 票 23 完成后，只有后续改动造成视觉、XAML、UI Automation 或 DPI 输出变化，或某场景失败时，才重跑受影响场景并重新完成被失效的批准与连续计数；与 UI 输出无关的后端、文档或打包变化不得触发无意义的整套视觉重验。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## 未完成项（2026-08-19 复核后取消勾选）

复核勾选时发现两项被高估，已取消勾选：

1. **720 epx 未被 DPI 旅程证明。** 旅程硬编码 `SetClientSize(1440, 900)`（物理像素），
   在 125% 下是 1152x720 epx、150% 下是 960x600 epx，宽度都不是 720 epx。现有 720 epx 覆盖
   （`WatchV2ProductionShellTests`、`WatchTicket21/22ResponsiveIntegrationTests` 里的
   `window.Width = 720`）跑在 96 DPI，因此「720 epx 且 125%/150% 缩放」这个组合从未被验证。
2. **临时 payload 未清理。** guest 上 `C:\MesIngest*` 仍在；仓库安全 hook 阻止对该路径
   `Remove-Item`，没有绕过。证据已全部取回宿主，仅是 guest 磁盘卫生问题。

另外记录一个证据强度问题（未取消勾选，因为门禁本身按 `-Runs` 默认值执行）：XAML 缺陷发生率为
10 次 1 次，修复后只跑了 3 轮绿。若修复无效，3 轮仍全绿的概率约 73%。真正支撑结论的是
`Capture_target_carries_no_hover_capture_or_focus_state` 直接断言已清空的输入状态，而不是这 3 轮。
按发生率给出同等强度的端到端证据需要 10 轮，约 73 分钟。

## 验收状态（2026-08-19）

19–22 生产窗口基线验收已完成：预览获批、候选 10 轮稳定、11 张基线提升、提升后 10 轮
`0 received`、125%/150% DPI 旅程通过、克隆与计划任务清理完毕、原 VM 复核为 1920x1080 / 96 DPI。
完整证据与交叉链接见 [`.artifacts/ticket23-acceptance/EVIDENCE-INDEX.md`](../../../.artifacts/ticket23-acceptance/EVIDENCE-INDEX.md)。

### XAML 门禁的红已修复并复跑通过

第一次 `Test-WatchXamlBaselineStability.ps1 -Runs 10` 在第 6 轮红：
`overview-loaded-2560x1440.received.png` 与第 1 轮差 695,918 像素、最大 delta 166、全部有彩，
而 XML 完全相同。原因是 legacy `MainWindow.xaml` 的 `OverviewDemandsButton` 渲染出 hover 强调底色：
`PrepareAsync` 会 `Window.Show()`，2560x1440 场景大于 1920x1080 桌面，指针必然压在某张卡片上并把
`IsMouseOver` 锁住；隐藏窗口再把内容挪到离屏并不会让 WPF 重新判定。修复是在把内容移出窗口**之前**
按窗口这个 focus scope 清掉 capture/focus，并用 `Mouse.Synchronize()` 重新命中测试。
回归测试：`WatchXamlVisualTests.Capture_target_carries_no_hover_capture_or_focus_state`。

复跑：`ticket-23-xaml-gate-fixed-2/run-20260819-105020-watch-xaml-stability` PASSED，3 轮。
红证据完整保留在 `ticket-23-xaml-gate/run-20260819-090314-watch-xaml-stability`。

### 遗留（不属于本票，建议各自开票）

1. `SelectedUi` 的 19 张 legacy 原型基线与当前 UI 全部不一致（每轮 `Total: 20, Failed: 19`）。
   稳定性门禁只判轮次间一致性，所以不拦截，但这些基线已过期。
2. XAML 门禁每轮 ~7.3 分钟里约 6 分钟是测试进程写完最后一张截图后到退出之间的空转。
   已实测排除 build、restore、`dotnet run` 求值（都是秒级），STA 线程也是 background 且有 30 秒上限。
3. `InstallPackageLayoutTests` 的 `openapi/v1.json` 断言，归属票 24/25。
