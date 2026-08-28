# 13 — Watch Alerts 支持完整游标分页

**What to build:** MesIngest.Watch 必须消费 Alerts API 的分页 envelope，让操作员能够访问首 100 条之后的告警；加载更多、自动刷新、排序变化与错误游标恢复须保持和 Demand 浏览一致的薄客户端语义。

**Blocked by:** None — can start immediately

**Status:** ready-for-human

- [x] Watch Alert 查询与浏览状态保存并使用 `nextCursor` / `hasMore`，不再丢弃服务端分页信息
- [x] Alerts 区域提供明确的已加载数量、是否还有更多及 Load more/等价滚动加载入口
- [x] 筛选或排序变化清回第一页；自动刷新在条件未变时保留当前已加载窗口
- [x] Alert cursor 非法、过期或与排序不匹配时安全重载第一页，不留下混合排序或重复行
- [x] 任一 Alert 页请求失败时保留最后成功窗口，并沿用现有连接横幅与事件记录语义
- [x] 真实 HTTP 契约测试使用超过 100 条告警，证明连续翻页无重无漏且能够访问最后一页

## Comments

- 2026-08-01: Watch now keeps independent Demand/Alert cursor windows. Alerts have their own loaded-count/end-state and Load more control; timer refresh rebuilds the loaded Alert window, while filter/sort reset returns to page one.
- 2026-08-01: Alert cursor 400 reloads page one without mixing windows. Other page failures retain the last successful Alert rows/cursor and flow through the existing Watch connection banner/event path.
- 2026-08-01: `WatchAlertBrowsePagingTests` covers append, preserve, cursor recovery, failure retention, and endpoint isolation. A real TestServer contract traverses 205 alerts with no gaps or duplicate AlertIds and reaches the final page.
