# 10 — Alerts 的 OpenAPI / sortBy allow-list 与实现一致

**What to build:** Alerts 列表的 `sortBy` 允许值在运行时校验、Swagger/OpenAPI 与发布包静态 `openapi/v1.json` 三者一致；不得把 Demand 的 allow-list（如 `dates`）误套到 Alerts 导致文档宣称可排、请求却 400。

**Blocked by:** None — can start immediately

**Status:** ready-for-human

## Parent / References

- Issue: `.scratch/mes-ingest-watch-operations/issues/12-swagger-openapi-read-contract.md`
- Spec: `.scratch/mes-ingest-watch-operations/spec.md`（Alert 只读 API）
- Handoff finding: Demand `sortBy` allow-list applied to Alerts；pack advertises `dates`, query rejects

不新增写接口；本票只修契约与实现对齐。

## Repro

1. 打开 `/openapi/v1.json` 与 pack 静态副本，查看 Alerts `sortBy` 枚举/说明是否含 `dates`。
2. 请求 `GET /api/alerts?sortBy=dates`（及文档列出的其它值）。
3. 对比 Demand 与 Alerts 的实际允许列。

期望失败态（现状）：文档/过滤器套用 Demand 列表；`dates` 对 Alerts 返回 400。

## Regression tests

- [ ] 合约测试：OpenAPI 中 Alerts `sortBy` 枚举 ⊆ 运行时 accept 集合，且覆盖实现支持的每一列
- [ ] `sortBy=dates` 若非 Alert 合法列：文档不得列出；列出的合法列返回 200 且排序生效
- [ ] 静态 pack OpenAPI 与现场 `/openapi/v1.json` 对该段描述一致
- [ ] Demand allow-list 回归不受影响

## Acceptance criteria

- [ ] Alerts 文档与 `AlertListQuery` 一致，无虚假可排字段
- [ ] 非法 sortBy 仍稳定 400；合法值可排
- [ ] OpenAPI 契约测试覆盖 live 与 pack 静态副本
