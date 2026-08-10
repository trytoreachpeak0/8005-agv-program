# 12 — 完成 FlaUI 旅程、真实窗口基线与失败证据

**What to build:** 让维护者通过正式 Watch 窗口验证五条高价值操作旅程，并在失败时获得足够、脱敏且可追溯的证据，以便将本机交互式 Windows 验收作为可靠发布门禁。

**Blocked by:** 11 — 对齐选定 UI、回归 Ticket 01–10 并重建 Verify.Xaml 基线

**Status:** done

**Golden renderer contract:** [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md)

- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

**Rebuild decision (2026-08-09):** 冻结原因已经由 Ticket 11 的新视觉契约解决。本票重新规格化但仍被 Ticket 11 阻塞；不得复用旧完成勾选或旧基线批准，只有用户确认新 UI 后才能实际开始。

- [x] 使用 FlaUI.UIA3 5.0.0 在对齐后的正式 `MesIngest.Watch.exe` 上重建冷启动概览、VISIBLE/GONE 分页及任务详情、Alert → Demand 定位、慢请求取消并保留旧结果、离线后恢复连接五条真实窗口旅程。
- [x] 固定五个 `1440×900` 客户区高价值终态真实窗口基线；125%/150% DPI 只执行布局和 UIA 烟测，不进行像素比较。
- [x] 统一本机入口在已登录交互式 Windows 会话中串行运行 `watch-vm-tests`、`watch-xaml-visual`、`watch-ui-journeys` 和 `watch-window-visual`，程序集和桌面交互均不得并行。
- [x] 失败证据包含 expected/actual/diff、received XAML、关键步骤截图、UIA tree、Watch 日志、标准输出/错误、fake Host 请求时间线、步骤/异常/超时和环境清单，且全部脱敏。
- [x] 测试首次失败保持失败，重跑仅用于诊断；成为发布门禁前连续通过 50 次，flaky 判定、隔离责任和最长 7 天修复期限按规格执行。
- [x] 基线更新包含原因、关联票、before/after/diff 和环境清单，并要求非提交者复核；交互、文案、层级或状态色变化还需产品或业务确认。
- [x] 五条旅程和窗口候选全部使用 Ticket 11 已批准的新 UI 基线目录；旧 Ticket 12 候选只能作为历史对照，不能复制、改名或直接晋升。
- [x] 交付一份新旧证据索引，能够区分旧冻结运行、Ticket 11 新 XAML 基线、Ticket 12 新窗口基线和 50 次稳定性结果。

## Comments

- 2026-08-09：用户明确冻结 Ticket 12，并决定先回归 Ticket 1–10。当天生成的单次黄金机 `received` 候选只用于发现布局问题，不是批准基线，也不计入 10 次或 50 次稳定性门禁。现有 FlaUI/证据代码可作为重做时的参考，但所有 Ticket 12 验收结论重新打开。

- 2026-08-09：用户要求在 Ticket 11 完成设计对齐与 Ticket 01–10 回归后重建本票。状态改为已规格化的 `ready-for-agent`，但依赖关系仍禁止提前执行。

- 2026-08-10：用户复核五张黄金机真实窗口预览并明确回复“批准”。代码审查发现第一次 10 连跑发生在批准前，不符合 `golden-renderer.md` 的批准顺序；该次候选与随后开始的部分 50 连跑均保留为程序性无效历史证据，不计入门禁。修复审查问题后从批准后的新候选矩阵重新计数。

- 已实现正式 `MesIngest.Watch.exe` + loopback HTTP fake Host 的五条 FlaUI 旅程、固定客户区捕获、UIA 动态值、脱敏证据包、四套串行入口和桌面互斥锁。
- 像素模式固定 Host 端口和显示时间，使用不受桌面遮挡影响的客户区渲染捕获；非像素 UIA 套件仍使用生产时钟和横幅停留行为。两轮诊断中五个终态逐一 SHA-256 完全一致。
- 用户取消现在透传为取消结果，不再被 HTTP 客户端改写成带随机 elapsed/correlationId 的 Host 错误；旧结果和“已取消”提示均保留。
- 2026-08-10：审查修复后按强制顺序重新完成：用户批准预览 → 新候选 10/10 字节一致 → before/after/diff 提案与复核 → 晋升基线 10/10、0 received → 完整四套门禁 50/50 连续通过。125% 使用 Ticket 11 的离线克隆证据；150% 在新离线 disposable clone 上 5/5 通过并完整删除。原 `gpt_win11` 最终复核为 1920×1080、96 DPI，计划任务与残留进程均为 0。完整证据见 [`../evidence/ticket12-flaui-window-baselines-2026-08-10.md`](../evidence/ticket12-flaui-window-baselines-2026-08-10.md)。
