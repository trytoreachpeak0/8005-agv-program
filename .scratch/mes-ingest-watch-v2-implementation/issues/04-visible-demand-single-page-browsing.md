# 04 — 完成 VISIBLE TransportDemand 单页浏览

**What to build:** 让操作员以固定 100 行的服务端窗口浏览当前 VISIBLE TransportDemand，安全提交组合筛选、排序和 cursor 翻页，同时在慢 Host、失败、取消和迟到响应下始终保留正确的成功窗口。

**Blocked by:** 01 — 建立 V2 四页产品壳与单 Host 会话闭环; 02 — 建立正式 Watch UI 测试宿主与 fake Host

**Status:** done

- [x] VISIBLE 默认查询为 DATES 倒序、DemandId 稳定次排序、limit 100 且无时间窗；客户端不得下载全量历史或仅对当前页本地排序。
- [x] 支持六类 TASK_TYPE、SUBLOT、6–32 位小写十六进制 DemandId 前缀以及 DATES 起止筛选；输入作为草稿，只有本地校验和请求成功后才提交。
- [x] Host allow-list 中的列使用服务端排序并回到第 1 页；不可排序列不显示排序手势，“重置”成功后恢复默认查询。
- [x] 使用“上一页 / 第 N 页 / 下一页”和客户端保存的到达 cursor；只在 `hasMore=true` 且 nextCursor 非空时允许前进，不显示未知总页数或任意跳页。
- [x] 查询、排序、重置和翻页只有成功后才原子提交查询、页码、数据和 cursor 路径；失败或主动取消保留原已提交状态和成功窗口。
- [x] 当前页成功重取会截断其后的旧 cursor 路径；cursor 类 400 只自动回第 1 页一次并提示恢复结果，再次失败不得循环。
- [x] 被取消、被取代或属于旧 Host 的响应最终返回时，不得改变列表、页码、选择、详情、状态栏或横幅。

## Comments

- 2026-08-08：完成 VISIBLE 固定 100 行服务端查询、筛选草稿/提交状态、服务端排序、cursor 路径翻页、单飞取消、迟到响应隔离、cursor 400 单次恢复和选择保持。
- 验证：`MesIngest.Tests` 439 通过、19 个 SQL Server 测试按环境跳过；`MesIngest.Watch.UiTests` 17/17 通过。
