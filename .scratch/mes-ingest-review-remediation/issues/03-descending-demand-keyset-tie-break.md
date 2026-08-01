# 03 — Demand 降序 keyset 不因主排序并列丢行

**What to build:** `/api/demands` 在主排序列降序时，仍以 DemandId 为稳定次键完整遍历结果集；相同主排序值的多行不得在翻页时丢失或重复。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

## Parent / References

- Spec: `.scratch/mes-ingest-watch-operations/spec.md`（默认 `sortBy=dates&direction=desc`；DemandId 次键）
- Issue: `.scratch/mes-ingest-watch-operations/issues/05-paginated-indexed-demand-api.md`
- ADR: `docs/adr/mes/0008-full-source-snapshot-incremental-local-projection.md`（本地投影读取面）
- Handoff finding: Highest priority #3

不重新定义分页契约；本票修复降序 keyset 比较方向与次键组合。

## Repro

1. 植入多条相同主排序值（如相同 `dates`）、不同 DemandId 的 VISIBLE 行，总数超过一页。
2. 请求 `direction=desc`（及至少一种其它 allow-list 降序列），按 `nextCursor` 连续翻页直至 `hasMore=false`。
3. 对 InMemory 与 SQL 路径（若测试矩阵覆盖）核对并集。

期望失败态（现状）：InMemory 降序路径反转组合比较后，主排序并列的行在后续页被跳过。

## Regression tests

- [ ] 主排序值全相同、DemandId 递增：desc 翻页覆盖全部 ID，无漏无重
- [ ] 主排序值部分相同、跨页边界落在并列组内：仍无漏无重
- [ ] asc 与 desc 并集一致（仅顺序相反）；非法/排序不匹配 cursor 仍 400
- [ ] 默认 `dates desc` 契约测试更新为显式覆盖并列场景

## Acceptance criteria

- [ ] 任意 allow-list 排序列在 desc 下 keyset 翻页无漏无重
- [ ] DemandId 始终为稳定次排序键
- [ ] 分页契约测试证明并列主值跨页完整；Release 相关用例全绿
