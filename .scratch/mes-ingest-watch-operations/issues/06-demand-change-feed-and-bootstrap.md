# 06 — Demand 变更账本与权威 Bootstrap

**What to build:** 为持有 TransportDemand 本地镜像的下游程序提供持久化、断点续传的 CREATED/GONE 变更流；游标过期时以全部 VISIBLE + 最近 24 小时 GONE 权威重建。

**Blocked by:** 04 — 增量投影存储; 05 — 分页 Demand API

**Status:** done

- [x] SQL Server 新增单调 BIGINT sequence 的 DemandChangeFeed 表/存储适配器
- [x] 只发布 CREATED 与 GONE；不发布 MesLastSeenAt、DisappearCount、PollHealth、Alert
- [x] Demand INSERT/GONE UPDATE 与 feed append 同一事务提交
- [x] 变更项包含 sequence、DemandId、changeType、changedAt 和稳定的变化后业务 payload
- [x] `GET /api/demand-changes?afterSequence=&limit=` 有界分页，返回 next/high watermark/earliest available
- [x] 默认保留 48 小时，可配置；过期游标返回 HTTP 410 `SYNC_CURSOR_EXPIRED`
- [x] Bootstrap 获取一致 high watermark、全部 VISIBLE、`GoneAt >= now-24h` 的 GONE；客户端权威替换而非 merge
- [x] Bootstrap 完成后消费 high watermark 之后的 feed，证明并发 CREATED/GONE 不丢失
- [x] 测试多个独立消费者、重复页幂等、Host 重启、过期与 reappear 新 DemandId

## Comments

- Bootstrap is a client procedure over existing `/api/demands` + `/api/demand-changes` (no dedicated bootstrap endpoint). Catch-up applies CREATED/GONE payloads into the replaced VISIBLE+recent-GONE mirror.
- `MesIngest:ChangeFeedRetentionHours` defaults to 48; `0` retains permanently.
