# 01 — 建立 Variant A 窗口级通知主链

**What to build:** 让 Watch 使用者在真实主工作区窗口中获得第一条可用的 Variant A 独立通知卡片主链：通知覆盖页面而不推动内容，真实显式操作能够显示成功或失败结果，重复事件能够合并，通知能够按期限自动结束，并且重要通知不会被低优先级结果挤掉。

**Blocked by:** None — can start immediately.

**Status:** done

## Final Golden evidence

- 2026-08-27 Ticket 03 最终生产状态完整 `watch-ui-journeys`：96 DPI、120 DPI、144 DPI 均为 1 passed / 0 failed / 0 skipped。证据：`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/final-96-20260827-114310`、`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/dpi-120-final-20260827-112746`、`mes/ingest/csharp/.artifacts/golden-renderer/ticket-03/dpi-144-final-20260827-112746`。

规格依据：[Variant A 通知规格](../spec.md)。本票涉及 Watch UI，必须遵守 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)。选中的 Variant A 原型是布局与交互权威；生产代码不得引用原型项目、假数据或评审控件。

- [x] 实现窗口拥有的单一通知协调入口和语义事件契约；来源键由事件类别、页面或全局作用域及真实业务身份组成，不能使用随机标识或轮询时间破坏合并。
- [x] 在真实工作区窗口中提供非布局参与的通知覆盖层：桌面态位于内容区右上方、标题栏及页面标题上下文之下，空栈不占页面空间，`ContentDialog` 的层级仍高于通知。
- [x] 按选中原型实现独立卡片的核心结构与信息层级，包括严重度轨、图标、严重度文字、标题、受控说明、可选动作、合并次数、剩余时间和独立关闭；不得出现 A/B/C、场景按钮或原型评审文案。
- [x] 至少接通一个真实显式设置操作的成功与失败闭环；成功显示 3 秒，操作失败显示 8 秒并提供可执行的下一步，而初始加载和自动刷新开始/成功不创建 toast。
- [x] 使用可注入时间推进验证 3/5/8 秒规则，不得在测试中真实等待；业务计时不依赖真实 `DispatcherTimer` 状态机。
- [x] 同源事件合并到现有卡片，更新真实文案与次数、回到栈顶，并把剩余期限提升到当前剩余时间与该严重度默认期限中的较大值。
- [x] 栈按最新创建或合并时间倒序且最多显示三张卡片；第四项按错误、警告、成功/信息的优先级及同级最旧规则淘汰，不建立隐藏回放队列。
- [x] 关闭一张卡片只移除该卡片；新卡片不得主动抢走页面当前焦点，真实动作使用既有导航或命令服务。
- [x] 通过真实生产工作区窗口 seam 覆盖上述核心行为，只添加能发现回归的最窄测试，不为内部集合或计时实现建立重复测试接口。
- [x] 实现期间只运行覆盖当前行为的最窄测试选择；全部生产改动完成后只运行一次 tier 1 `dotnet test MesIngest.Tests`，记录通过、失败、跳过数以及未配置 SQL Server 环境时的命名跳过。
- [x] 本票不得提前运行 tier 2 或 tier 3；后续 UI 修改会使视觉证据失效，最终 Golden 预览与用户批准统一由 Ticket 03 完成。

## Golden renderer checklist

- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

Ticket 03 完成最终 Golden 验证后，应把同一最终生产状态的证据引用回本票；在此之前不得声称本票已获得视觉批准。
