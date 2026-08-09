# 12 — 完成 FlaUI 旅程、真实窗口基线与失败证据

**What to build:** 让维护者通过正式 Watch 窗口验证五条高价值操作旅程，并在失败时获得足够、脱敏且可追溯的证据，以便将本机交互式 Windows 验收作为可靠发布门禁。

**Blocked by:** 11 — 对齐选定 UI、回归 Ticket 01–10 并重建 Verify.Xaml 基线

**Status:** ready-for-agent

**Rebuild decision (2026-08-09):** 冻结原因已经由 Ticket 11 的新视觉契约解决。本票重新规格化但仍被 Ticket 11 阻塞；不得复用旧完成勾选或旧基线批准，只有用户确认新 UI 后才能实际开始。

- [ ] 使用 FlaUI.UIA3 5.0.0 在对齐后的正式 `MesIngest.Watch.exe` 上重建冷启动概览、VISIBLE/GONE 分页及任务详情、Alert → Demand 定位、慢请求取消并保留旧结果、离线后恢复连接五条真实窗口旅程。
- [ ] 固定五个 `1440×900` 客户区高价值终态真实窗口基线；125%/150% DPI 只执行布局和 UIA 烟测，不进行像素比较。
- [ ] 统一本机入口在已登录交互式 Windows 会话中串行运行 `watch-vm-tests`、`watch-xaml-visual`、`watch-ui-journeys` 和 `watch-window-visual`，程序集和桌面交互均不得并行。
- [ ] 失败证据包含 expected/actual/diff、received XAML、关键步骤截图、UIA tree、Watch 日志、标准输出/错误、fake Host 请求时间线、步骤/异常/超时和环境清单，且全部脱敏。
- [ ] 测试首次失败保持失败，重跑仅用于诊断；成为发布门禁前连续通过 50 次，flaky 判定、隔离责任和最长 7 天修复期限按规格执行。
- [ ] 基线更新包含原因、关联票、before/after/diff 和环境清单，并要求非提交者复核；交互、文案、层级或状态色变化还需产品或业务确认。
- [ ] 五条旅程和窗口候选全部使用 Ticket 11 已批准的新 UI 基线目录；旧 Ticket 12 候选只能作为历史对照，不能复制、改名或直接晋升。
- [ ] 交付一份新旧证据索引，能够区分旧冻结运行、Ticket 11 新 XAML 基线、Ticket 12 新窗口基线和 50 次稳定性结果。

## Comments

- 2026-08-09：用户明确冻结 Ticket 12，并决定先回归 Ticket 1–10。当天生成的单次黄金机 `received` 候选只用于发现布局问题，不是批准基线，也不计入 10 次或 50 次稳定性门禁。现有 FlaUI/证据代码可作为重做时的参考，但所有 Ticket 12 验收结论重新打开。

- 2026-08-09：用户要求在 Ticket 11 完成设计对齐与 Ticket 01–10 回归后重建本票。状态改为已规格化的 `ready-for-agent`，但依赖关系仍禁止提前执行。

- 已实现正式 `MesIngest.Watch.exe` + loopback HTTP fake Host 的五条 FlaUI 旅程、固定客户区捕获、UIA 动态值、脱敏证据包、四套串行入口和桌面互斥锁。
- 像素模式固定 Host 端口和显示时间，使用不受桌面遮挡影响的客户区渲染捕获；非像素 UIA 套件仍使用生产时钟和横幅停留行为。两轮诊断中五个终态逐一 SHA-256 完全一致。
- 用户取消现在透传为取消结果，不再被 HTTP 客户端改写成带随机 elapsed/correlationId 的 Host 错误；旧结果和“已取消”提示均保留。
- 当前桌面不是规格要求的 `zh-CN` 校准环境，因此未生成或批准五个 `*.verified.png`，也未声称完成 10 次候选稳定性或 50 次完整门禁连跑。
- 人工交接：在 100% DPI、浅色、`zh-CN`、`China Standard Time`、指定字体的已登录 Windows 桌面先运行 `Test-WatchWindowBaselineStability.ps1 -Configuration Release -Runs 10 -ArtifactsDirectory <new-dir>`；再为五个候选分别运行 `New-WatchWindowBaselineProposal.ps1 -ChangeType Initial ...`，由非提交者复核后放入 `WindowBaselines`；最后运行 `Test-WatchUiGateStability.ps1 -Configuration Release -Runs 50 -ArtifactsDirectory <new-dir>`。
