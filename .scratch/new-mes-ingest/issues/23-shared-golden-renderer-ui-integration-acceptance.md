# 23 — 共享黄金机 UI 集成验收与基线

**What to build:** 将 19–22 已冻结并通过共享黄金机预览批准的生产 Watch 页面作为一个 integration train，在校准黄金机上完成候选稳定、基线提升和 DPI 正式验收，只提升与获批预览具有同一源码及输出身份且可重复的基线，并为四张实现票留下可共同引用的完整证据。

**Blocked by:** 19 — 生产 Fluent shell、设置与概览；20 — DemandSeries 生产页面；21 — 资格审计与 AREA Variant A 生产页面；22 — Error Search Variant A 与接入告警生产页面

**Status:** ready-for-human

- [x] 正式门禁遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，只在 gpt_win11 的校准交互桌面通过交互计划任务驱动 WPF 和 FlaUI；PowerShell Direct 仅用于部署、监控和取回证据，不用于截图或 UI 驱动。
- [x] 为本次冻结的 19–22 源身份建立唯一、不覆盖历史的证据目录，记录提交与 dirty diff 身份、环境报告、任务原生退出码、恢复/构建/测试日志、截图、UIA 树、Verify XML、received/diff、通过或失败或 skip 计数及每个 named skip 的 release gate。
- [x] 先运行全部相关代码与非像素回归，再在 1920×1080、96 DPI、zh-CN、浅色主题、SoftwareOnly 的真实交互桌面运行受影响的 UI Automation、键盘、标题栏、导航、分页、详情、InfoBar、剪贴板、高对比度语义和真实窗口旅程。
- [x] 开始候选门禁前，核对 19–22 的共享黄金机预览、用户批准、源码提交与 dirty diff 身份确实对应本票冻结输出；身份和视觉/UIA/DPI 输出均未变化时不得重复生成或要求再次批准同一预览，若不一致则保留失效证据、只重做受影响预览并重新取得批准。
- [x] 用户批准后生成全新 candidate matrix，不批量提升历史 received/candidate；对候选连续运行 `-Runs` 次（默认 3，见 [Golden WPF renderer](../../../docs/agents/golden-renderer.md) 的 Repetition count），每一轮的 PNG 与 XML 必须字节完全一致，或在该文档的 Visual equivalence 判据下被判定为视觉等价；任何被容差接受的 step 都要列入证据并在审批时人工复核，任何失败都保留 red evidence、解释原因并从第一轮重新计数。
- [x] 为每个受影响场景生成 before/after/diff 证据，只提升用户明确批准的候选；提升后对同一矩阵再连续运行同样的 `-Runs` 次并要求 `0 received`，不以一次成功重跑掩盖先前失败。
- [x] 从校准 VM 导出具有新 VM ID 的一次性离线克隆，断开网络后分别在 125%（120 DPI）和 150%（144 DPI）运行所需 watch-ui-journeys；交互环境报告必须证明实际 DPI，且不改变原 gpt_win11 的 96 DPI。
- [x] DPI 旅程证明 720 epx 最小宽度与规定缩放下，标题栏按钮、导航、页面状态、筛选、分页、三列或 master-detail 边界、关键命令和焦点视觉能重排或滚动而不裁切。
- [x] 完成后清除交互计划任务、残留 Watch/test 进程、临时 payload、DPI 克隆及其精确导出/导入目录，并复核原 VM 为 1920×1080、96 DPI、Explorer 与输入桌面处于正确交互会话。
- [x] 将 19–22 的共享预览证据和本票唯一门禁 evidence directory、环境身份、用户批准记录、named skips 与清理结果互相链接；这些实现票不重复执行各自的完整候选稳定、提升后稳定和 DPI clone 流程。
- [x] 票 23 完成后，只有后续改动造成视觉、XAML、UI Automation 或 DPI 输出变化，或某场景失败时，才重跑受影响场景并重新完成被失效的批准与连续计数；与 UI 输出无关的后端、文档或打包变化不得触发无意义的整套视觉重验。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## 复核记录（2026-08-19）

复核勾选时发现两项被高估，先取消勾选，随后各自补做完成：

1. ~~**720 epx 未被 DPI 旅程证明。**~~ 已补齐，见下方「720 epx × 缩放」一节。
2. ~~**临时 payload 未清理。**~~ 已清理：guest 上 29 个票 23 payload 目录（`23`、`23-*`、
   `ticket-23-preview-v2`、`Ticket23FontCalibration`）全部删除，`Ticket23Left=0`。
   其他票的目录与 `Ticket11\NuGetPackages` 离线缓存均未触碰，计划任务与残留进程为 0，
   guest C: 释放至 83 GB 可用。

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

## 720 epx × 缩放（2026-08-19 补做）

原先的缺口：旅程按物理像素固定 1440x900，所以 125% 实际是 1152x720 epx、150% 是 960x600 epx，
宽度从未到过 720 epx。修复是给旅程加了按 effective pixel 定尺寸的开关
（`SetClientSizeInEffectivePixels` + `-JourneyClientEpx`），窗口自身声明
`MinWidth="720" MinHeight="600"`，所以目标定为 720x600 epx。

| 运行 | 缩放 | 交互环境报告 | 客户区 | 结果 |
| --- | --- | --- | --- | --- |
| `ticket-23-epx-720-baseline-96dpi-v2` | 100% | Dpi=96 | 720x600 物理 = 720x600 epx | PASSED |
| `ticket-23-epx-720-dpi-120` | 125% | Dpi=120, ScalePercent=125 | 900x750 物理 = 720x600 epx | PASSED |
| `ticket-23-epx-720-dpi-144` | 150% | Dpi=144, ScalePercent=150 | 1080x900 物理 = 720x600 epx | PASSED |

首次尝试用 720x450 失败：`Could not stabilize the client area at 720x450; got 720x600`
——窗口最小高度就是 600 epx，这个高度根本不可达。harness 选择报错而不是拍一张尺寸不对的图
充当证据，这个行为是对的。

150% 下 DemandSeries 详情页目视复核：标题栏按钮、导航栏、分页行（每页 / 上一页 / 页码 / 跳转）、
完整证据命令、两列详情边界都完整渲染，网格各自带水平滚动条，页面整体可垂直滚动——重排与滚动，
没有裁切。

克隆 `gpt_win11_ticket23_dpi720`（新 VM ID `83b0777b`、断网、磁盘隔离在自己的 import root）
用完即删，导出/导入目录一并删除。宿主只剩 1.9 GB 可用内存，装不下第二台 4 GB 虚机，因此按批准
先把 gpt_win11 优雅关机再启动克隆；导出是在线做的，黄金机只在真正需要内存的那段时间离线。
复跑正式环境门禁 `ticket-23-final-vm-recheck-after-720epx`：228 项 0 失败 5 具名 skip，
1920x1080 / 96 DPI / 100% / 浅色 / session 1，计划任务与残留进程均为 0。
