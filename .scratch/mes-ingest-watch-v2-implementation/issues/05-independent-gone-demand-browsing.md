# 05 — 完成独立 GONE TransportDemand 浏览

**What to build:** 让操作员在与 VISIBLE 完全隔离的浏览上下文中追溯最近 GONE TransportDemand，并能安全扩大时间范围、分页、排序和返回之前的成功窗口。

**Blocked by:** 04 — 完成 VISIBLE TransportDemand 单页浏览

**Status:** done

- [x] GONE 默认查询为最近 24 小时、GoneAt 倒序、DemandId 稳定次排序和 limit 100；允许显式修改 GoneAt 起止范围。
- [x] GONE 独立保存草稿/已提交查询、单页成功窗口、cursor 路径、当前页、选择、详情、最后成功时间和刷新状态，不与 VISIBLE 串页或共享 cursor。
- [x] VISIBLE 与 GONE 标签切换时立即恢复各自缓存；首次进入无缓存标签立即加载，已有缓存且未启用自动刷新时不额外请求。
- [x] GONE 支持与规格一致的 TASK_TYPE、SUBLOT、DemandId、服务端排序、重置、前后翻页、cursor 一次恢复和失败原子保留行为。
- [x] 当前页重取、翻页失败、导航取消和旧响应回达均通过 fake Host 场景验证，不得清空或混合另一标签的数据。
