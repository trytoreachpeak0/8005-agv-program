# 19 — 生产 Fluent shell、设置与概览

**What to build:** 将已确认的信息架构重写为连接真实新版 Host 状态的生产 WPF Fluent shell，并交付设置和 Overview Variant A：运维人员能从一个窗口看见一致的业务摘要、跨页重点动态、紧凑 Host 状态与明确下钻，同时在离线或刷新失败时继续辨认上一份成功快照。

**Blocked by:** 14 — 一致 WatchOverviewSnapshot；18 — Watch 单 Host 非视觉会话与刷新内核

**Status:** done

- [x] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)；原型只提供信息层级依据，生产界面不直接复制原型假数据或硬编码视觉值。
- [x] 一个 FluentWindow、一个集成 TitleBar 和一个 NavigationView 构成唯一应用身份层；主导航包含概览、需求系列、资格审计、错误检索、AREA 筛选和接入告警，Host 状态与设置位于紧凑页脚。
- [x] 标题栏的拖动、双击最大化或还原、右键系统菜单、缩放、最小化、最大化或还原、关闭、键盘和 UI Automation 行为保持可用，应用身份不会在内容区重复出现。
- [x] 设置页只管理单 Host 连接、超时、各数据视图自动刷新间隔及允许的本地显示偏好；不提供手动刷新或自动刷新开关，应用连接设置时使用票 18 的会话隔离语义。
- [x] 概览按 Variant A 展示同一 WatchOverviewSnapshot 中的需求系列、资格、错误和当前关注摘要，以及最近 24 小时最多五条真实转换；每个卡片或子摘要携带显式目标查询并从目标页第一页开始。
- [x] AREA 配置名称、范围数量和本地状态作为 Watch 本地上下文单独叠加，不伪装成 Host 快照字段，也不影响错误或接入关注摘要。
- [x] 初始加载、成功、近期无动态、刷新中、Host 离线和刷新失败均有明确页面状态；失败整份保留上一成功概览，并以行内 InfoBar、快照时点和当前连接状态说明陈旧性，不把空动态或零错误单独宣称为健康。
- [x] 状态含义由文字、图标和可访问名称表达而非只靠颜色；页面命令、导航、卡片下钻、设置校验和 Host 页脚具备稳定 UI Automation 名称、键盘焦点与高对比度语义。
- [x] 1440×900 是主设计基线，2560×1440 能合理扩展，720 epx 最小宽度及 125%/150% DPI 下关键命令、状态、标题栏和焦点不会裁切。
- [x] 本票与 20–22 属于同一共享 integration train：各票先完成非像素回归和实现，四票输出冻结后只向黄金机部署一次，集中运行实际受影响的 targeted suites、生成一套最终真实窗口预览并取得一次用户批准；同一批准与证据链接回填四票后它们才可完成并共同解锁票 23，不得按票重复运行完整 `all`、候选稳定、基线提升或 DPI clone。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-14 — 非像素实现冻结，等待共享视觉列车

- 生产 `App` 已切换到唯一 V2 composition/window；设置、原子 Overview、AREA
  本地上下文、自动刷新通知、失败保留、第一页下钻和动态 UIA 已接入真实
  `MesIngestV2ApiClient -> WatchV2WorkspaceSession` 链路。
- Release build 为 0 warning / 0 error；Ticket 19 聚焦回归 62/62、真实窗口与
  ScriptedFakeHost 会话回归 27/27。独立 Standards 审查无剩余硬性违规，Spec
  非像素审查 PASS。
- 未勾选标题栏真实交互、高对比度、DPI、共享列车及黄金机条目：这些必须等
  tickets 20–22 一并冻结后，通过一次黄金机部署、真实窗口预览和一次用户批准
  共同回填，不能由本票单独提前宣称完成。
- 全 solution 一次运行：Watch UI 109 passed / 27 named environment skips；通用
  tests 695 passed / 99 SQL-environment skips / 3 failures。三项失败均位于本票未改
  文件；定向复跑后 legacy TitleBar drag 通过，剩余为既有 INSTALL 文档
  `openapi/v1.json` 断言和 latency 日志保留时钟断言。

### 2026-08-17 — 共享 Preview v8 批准并完成

- 冻结源码为 `7ec9bf073609eed7396aa36aae0f19e7b7a526f5`，工作树干净；共享
  `watch-production-preview` 在校准 `gpt_win11`（1920×1080、96 DPI）通过。
- VM tests 206 total / 205 passed / 0 failed / 1 named skip；生产真实窗口 journey
  1/1 passed。唯一 skip 为
  `WatchWindowJourneyTests.Fluent_window_chrome_supports_keyboard_uia_double_click_and_drag`，
  它要求由正式桌面 suite 驱动，对应窗口旅程已在本次正式入口通过。
- 用户于 2026-08-17 在 Codex task `01a0005b-d029-7fb1-aeff-6ce8493cf391`
  对 Preview v8 回复“全部批准”。本次只批准实现列车预览，未生成或提升 baseline；
  candidate 稳定、baseline 提升和正式 125%/150% DPI clone 仍由票 23 独占。
- 唯一证据目录：
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-19-22-prototype-alignment-preview-v8/run-20260815-205801-watch-production-preview`。
  Orchestration、前后环境与 cleanup 均为 PASSED；残留进程与任务为 0，原 VM 已复核为 96 DPI。
