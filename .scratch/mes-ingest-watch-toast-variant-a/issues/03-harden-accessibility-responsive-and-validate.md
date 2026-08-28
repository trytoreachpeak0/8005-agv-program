# 03 — 完成可访问性、响应式与最终生产验证

**What to build:** 让最终 Variant A 通知在键盘、屏幕阅读器、高对比度、深浅主题、窄窗、高 DPI、减少动态及窗口前后台切换下都能可靠使用，并以一次最终生产状态的集成与 Golden 验证证明完整功能正常。

**Blocked by:** 02 — 迁移反馈、故障生命周期与 AREA 阻塞选择。Ticket 02 已严格依赖 Ticket 01；两票完成前不得开始本票。

**Status:** done

规格依据：[Variant A 通知规格](../spec.md)。本票涉及 Watch UI、布局、UIA、DPI 与视觉证据，必须遵守 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)。

- [x] 鼠标进入通知 host 或键盘焦点位于任一卡片时暂停所有可见卡片倒计时；鼠标和焦点都离开后从剩余时间继续，不重新开始期限。
- [x] 新通知不抢焦点；动作和关闭按钮进入正常 Tab 顺序，至少为 32×32 epx，并具有稳定自动化名称、工具提示和可见焦点状态。
- [x] 使用单一 `Polite` live region 只播报新的语义事件一次；倒计时、合并重绘、主题切换及持续故障重复刷新不重复朗读，恢复作为新事件可单独播报。
- [x] 严重度、标题、说明、合并次数、动作与关闭均具有明确可访问语义；浅色、深色、高对比度和非活动窗口不依赖颜色表达分组或严重度，正文与操作文字达到至少 4.5:1 对比度。
- [x] 桌面态通知栈约 380 epx 宽并与内容右侧 24 epx 外边距对齐；窄态以真实碰撞触发顶部单列，覆盖 760×820 原型状态和 720 epx 产品最小宽度，保留紧凑导航加 12 epx 的左安全间距及 12 epx 右边距。
- [x] 125% 与 150% DPI 下文字换行、动作、关闭、焦点框和对话框完整可见；不得修改校准 Golden VM 的 96 DPI，缩放验证使用规定的离线一次性克隆。
- [x] 标准动态使用约 180 ms 的透明度和 8–12 epx 垂直位移，并能平滑表达新增、合并、关闭和溢出；Windows 减少动态开启时移除位移和栈移动，只保留直接切换或透明度变化。
- [x] 主窗口关闭时取消计时器、事件订阅和动作回调；已经排队的 UI 更新在发现窗口已释放后安全退出。
- [x] 通过真实生产工作区窗口 seam 覆盖规格中的静默刷新、3/5/8 秒、合并与溢出、故障周期、导航、选择清除、前后台、焦点暂停、UIA、响应式、减少动态和两个 AREA 对话框；使用 fake clock，不得真实等待。
- [x] 实现期间只运行当前失败行为的最窄测试；全部生产改动完成后只运行一次 tier 1 `dotnet test MesIngest.Tests`，记录失败、通过、跳过数及全部命名跳过。
- [x] 在运行 tier 2 前取得用户针对本次最终状态的明确授权；未授权时不得自行运行、不得以本地桌面或原型截图声称视觉通过。
- [x] 获得授权后，仅运行覆盖主生产窗口通知状态的最窄适用完整 Golden suite，不使用 `-Suite all`；正式通过不能用 narrowed run 代替。
- [x] 在校准 Golden 桌面生成可与 1440×900 三卡栈、760×820 窄窗减少动态和 AREA 冲突状态直接比较的真实生产预览，并由用户审阅批准。
- [x] 将最终生产状态的 Golden 证据同时引用回 Ticket 01 与 Ticket 02；任何后续 UI 修改都会使此前视觉批准失效。
- [x] 不运行 tier 3、稳定性三跑、候选基线生成或提升，除非用户另行明确要求验证或提升基线。

## Golden renderer checklist

- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

- 2026-08-27：用户批准不透明 Variant A 通知预览；最终生产背景使用不透明 Fluent 主题资源。
- 最终 focused 导航回归：1 passed / 0 failed / 0 skipped。
- 最终 tier 1：`dotnet test MesIngest.Tests`，810 passed / 0 failed / 133 skipped / 943 total。全部命名跳过记录于 `mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/orchestration-final-96-20260827-114310/tier1-final-named-skips.txt`；未配置真实 SQL Server 三项环境变量。
- 最终完整 `watch-ui-journeys`：96 DPI、120 DPI、144 DPI 均为 1 passed / 0 failed / 0 skipped。证据分别位于 `mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/final-96-20260827-114310`、`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/dpi-120-final-20260827-112746`、`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/dpi-144-final-20260827-112746`。
- 既有 preflight、系统 toast 污染与 journey 红证据全部保留；最终克隆已删除，scheduled tasks/processes 为 0，原 VM 复查为 1920×1080、96 DPI、`ClientAreaAnimation=True`、toast registry 不存在。
- 未运行 tier 3、稳定性三跑、候选基线生成或提升。
