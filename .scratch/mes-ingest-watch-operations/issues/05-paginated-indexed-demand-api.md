# 05 — 分页、索引化 TransportDemand 读取 API

**What to build:** 直接升级 `/api/demands` 为有界游标分页和服务端筛选/排序，默认只读 VISIBLE 并按 DATES 降序；没有旧外部消费者需要保留裸数组兼容。

**Blocked by:** 01 — 时间契约; 04 — 增量投影存储

**Status:** ready-for-agent

- [ ] `/api/demands` 返回 `items/nextCursor/hasMore`，任何调用均有 page size 硬上限
- [ ] 默认 `status=VISIBLE&sortBy=dates&direction=desc`，DemandId 为稳定次排序键
- [ ] 支持 status、TASK_TYPE、SUBLOT、DATES/GoneAt 范围和 allow-list sort columns
- [ ] GONE 默认按 `GoneAt >= now-24h`；调用方可显式扩大，所有 VISIBLE 无时间限制
- [ ] `/api/demands/{demandId}` 主键精确查询保持可用
- [ ] DemandId 列表查询支持完整精确或至少 6 位 lowercase hex prefix；非法字符/过短前缀返回 400
- [ ] 根据实际执行计划建立 Status+DATES+DemandId、TASK_TYPE+SUBLOT、GoneAt+DemandId 等索引，不在列上套破坏 seek 的函数
- [ ] cursor 不暴露可篡改内部 SQL；非法/排序不匹配 cursor 返回稳定 400
- [ ] 契约测试覆盖全局排序、翻页无重无漏、并发新增、组合筛选、旧裸数组已移除

## Comments

- API default ordering uses MesCurrentStepEnteredAt (`dates`), never MesLastSeenAt.

