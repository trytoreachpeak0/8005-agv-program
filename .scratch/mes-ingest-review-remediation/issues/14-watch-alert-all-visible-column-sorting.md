# 14 — Alerts 所有可见列下推服务端排序

**What to build:** Alerts 网格的每个可见列都必须支持列头升降序，并在 Host 的完整结果集上稳定排序；Watch 不得仅排序当前页，也不得以禁用列头来规避上游“两表所有可见列可排序”的契约。

**Blocked by:** 13 — Watch Alerts 支持完整游标分页

**Status:** done

- [x] Code、Severity、AlertId、first seen、last seen、TASK_TYPE、SUBLOT、DemandId 与 Message 全部具有服务端排序 token
- [x] Host parser、内存/SQL 查询、游标编码与比较使用同一 allow-list；AlertId 始终作为稳定次排序键
- [x] 每列第一次点击升序、第二次降序并显示方向箭头；自动刷新与 Load more 保持当前列和方向
- [x] 含 null、相同主值及跨页边界的 asc/desc 翻页均无重无漏
- [x] 运行时 OpenAPI 与发布包静态 OpenAPI 同步公布完整 Alerts 排序契约，非法 token 仍稳定返回 400
- [x] 多页真实 HTTP + Watch 集成测试证明排序作用于完整结果集，而不是当前内存页

## Comments

- 2026-08-01: Added all nine Alerts sort tokens end-to-end through Watch, Host parser, shared InMemory/SQL paging, cursor payload/comparison, runtime OpenAPI, and packaged static OpenAPI. Nullable text fields sort null-first asc/null-last desc; AlertId is the stable ascending tie-break for non-AlertId primary sorts.
- 2026-08-01: Real Host HTTP tests traverse every token in asc/desc with nulls, tied primary values, and page size 2. A 205-alert real Host + Watch test verifies SUBLOT sorting survives Load more and preserve-window automatic refresh. Full isolated LocalDB suite: 385 passed.
