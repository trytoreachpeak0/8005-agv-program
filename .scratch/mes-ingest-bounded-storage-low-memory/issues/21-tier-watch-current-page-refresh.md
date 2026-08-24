# 21 — 完成 Watch 刷新与保护状态呈现

**What to build:** 在一次 Watch 实现与视觉验证中完成当前页 30/60 秒刷新、Inspector 单一读取边界，以及 StoragePressurePause 和历史重置状态呈现，不增加高风险写能力。

**Blocked by:** 20 — 完成精确 V2 契约整体切换.

**Status:** ready-for-agent

- [ ] Overview 与 CurrentIngestAttention 默认 30 秒，DemandSeries、ReadabilityAudit 与 ErrorSearch 默认 60 秒。
- [ ] 自动刷新始终只作用于当前可见页和当前页窗口；切页停止旧页计时并按目标页档位重新调度。
- [ ] 刷新继续单飞、不排队、可取消；失败或取消保留最后成功窗口并明确其时间。
- [ ] Inspector 不拥有 Host client、Timer、refresh loop、独立缓存或 snapshot，只接收同一冻结上下文的 presentation。
- [ ] 默认设置、持久化设置、页面切换、慢请求和 Inspector 行为由确定性时间与生产 Watch 测试覆盖。
- [ ] 保持现有 Fluent 页面层级与自动刷新设置语义，不增加手动刷新或启用/禁用命令。
- [ ] 全局状态栏和概览健康区以文本、图标和可访问名称呈现 StoragePressurePause 与历史重置状态，不只依赖颜色。
- [ ] 暂停状态显示原因、最后成功 PollTrace、最后成功投影时间、earliest available 和精确本地恢复指引。
- [ ] 历史重置状态显示新 HistoryEpoch、建立进度、当前 503 原因和 HistoryResetAcknowledgement 本地指引。
- [ ] Watch 不增加恢复、确认、删库或其它管理按钮；ScriptedFakeHost 覆盖正常、15% 告警、暂停、待确认重建、确认后恢复和 Host 离线。
- [ ] 保留现有已接受生产窗口层级、页面结构、间距和交互，不发明替代信息架构。
- [ ] 复用现有 workspace、refresh coordinator、Inspector coordinator、状态栏、概览健康区和 ScriptedFakeHost；不新建页面、导航层、状态框架或第二套 UI 自动化夹具。
- [ ] Read [Fluent UI rules](../../../docs/agents/fluent-ui.md) and [golden renderer](../../../docs/agents/golden-renderer.md) before implementation.
- [ ] 对全部合并改动只运行一次最窄且完整的 golden-machine suite；运行前说明成本并取得用户批准。
- [ ] User approved the final real-window preview.
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
- [ ] 开发期只运行聚焦 Watch 非像素测试和一次 Tier 1；获批后只运行一个覆盖全部受影响状态的完整 Tier 2 suite，不运行 Tier 3、不推广基线、不为同一候选重复预览。
- [ ] 正常代理工作目标在 3 小时内完成，不含等待用户批准的墙钟时间；若预览暴露真实视觉差异，按 Golden Renderer 规则升级，不以时间目标跳过修复。
