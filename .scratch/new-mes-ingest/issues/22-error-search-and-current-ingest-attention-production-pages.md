# 22 — Error Search Variant A 与接入告警生产页面

**What to build:** 让运维人员在生产 Watch 中通过 Error Search Variant A 从错误分类定位曾经受影响的 DemandSeries 和真正命中的证据，同时在接入告警页只处理当前仍需关注的 Series 与全局接入问题；已恢复历史、当前风险和 AREA 显示范围不会再被混为一谈。

**Blocked by:** 11 — ErrorSearchAsOf 列表、窗口与分面；12 — 错误详情与受限原始证据；13 — CurrentIngestAttention 当前关注读取；18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览

**Status:** done

- [x] 实现与验证遵循 [MesIngest.Watch Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)，错误检索采用已确认的 Variant A“分类导航 + Series 结果 + 证据详情”三列布局，三列共享上下边界并填满可用内容高度。
- [x] 错误检索支持分类、错误码、ACTIVE/ENDED、24 小时、7 天、30 天或全部历史、SeriesId、DemandId 和 SUBLOT 条件，并明确显示冻结 ErrorSearchAsOf、UTC 半开窗口和当前规范化条件。
- [x] 结果按 DemandSeries 去重，显示稳定排序、精确总数、分面和服务端分页；详情只展示当前条件真正命中的期间与证据，并标明跨出窗口的期间边界和跨 Demand 世代关系。
- [x] 成功零命中只说明当前条件下没有历史；加载、取消、游标错误和刷新失败不会显示为空结果，刷新失败保留上一成功快照及其 AsOf 和条件。
- [x] 默认诊断证据可解释字段、观测值、规则、DemandId 或 WorkType、证据时间和 PollTrace；完整原始观测只能按需、有大小上限且受敏感字段白名单约束。
- [x] 接入告警只显示 CurrentIngestAttention，覆盖活动 Series 错误、PollRunFailure、TaskTypeProtection 和 UnassignedMesObservation；已结束 Series 错误从当前页消失但仍能在错误检索中找到。
- [x] Series 当前关注项引用稳定错误身份并能带显式条件下钻错误检索，不创建或展示另一套 fingerprint incident、人工确认或人工恢复语义。
- [x] Error Search 和接入告警不受 AreaFilterProfile 静默过滤；页面明确区分历史错误、当前关注、Host 连接失败和 Watch 刷新失败。
- [x] 分类、筛选、时间范围、分页、Series 选择、证据详情、关注项和下钻均具备稳定 UI Automation 名称、键盘焦点和非颜色状态表达，并在规定窗口尺寸和 DPI 下保持三列关系或可理解的响应式重排。
- [x] 本票与 19–21 属于同一共享 integration train：各票先完成非像素回归和实现，四票输出冻结后只向黄金机部署一次，集中运行实际受影响的 targeted suites、生成一套最终真实窗口预览并取得一次用户批准；同一批准与证据链接回填四票后它们才可完成并共同解锁票 23，不得按票重复运行完整 `all`、候选稳定、基线提升或 DPI clone。
- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

## Comments

### 2026-08-17 — Preview v8 批准，Ticket 22 完成

- 实现与修复冻结在 `7ec9bf073609eed7396aa36aae0f19e7b7a526f5`；正式 payload
  来自干净工作树，SHA-256 为
  `777C0D053D87C891AC99FA73BCD59CBEC50F626A0FD85E3D5C6AB15F8A91FDF0`。
- 共享 `watch-production-preview` 在校准 `gpt_win11`（1920×1080、96 DPI、
  interactive scheduled task）通过：VM tests 206 total / 205 passed / 0 failed /
  1 named skip，生产真实窗口 journey 1/1 passed。
- 唯一 skip 为
  `WatchWindowJourneyTests.Fluent_window_chrome_supports_keyboard_uia_double_click_and_drag`；
  原因是该检查要求由 `Invoke-WatchUiTests.ps1` 的正式桌面入口串行驱动，对应窗口旅程
  已在同一正式运行中通过，因此不阻断本实现票。
- 用户于 2026-08-17 在 Codex task `01a0005b-d029-7fb1-aeff-6ce8493cf391`
  对 Preview v8 回复“全部批准”。批准覆盖 19–22 共享生产预览，不等同于 baseline
  提升；candidate 10 次稳定、baseline 提升、提升后 10 次稳定及 125%/150% DPI clone
  仍由票 23 执行。
- 唯一证据目录：
  `mes/ingest/csharp/.artifacts/golden-renderer/ticket-19-22-prototype-alignment-preview-v8/run-20260815-205801-watch-production-preview`。
  `orchestration-result.json`、前后环境报告与 `cleanup.json` 均为 PASSED；计划任务不存在、
  残留进程为 0，原 VM 已复核为 96 DPI。
- 同一批准与证据已回填票 19–21；共享实现列车至此完成，票 23 已解除实现票阻塞。
