# 15 — TransportDemands 所有可见列下推服务端排序

**What to build:** TransportDemands 网格的每个可见列都必须支持 Host 端稳定排序，补齐当前尚未支持的 status、AREA、EQP、STEP、PACKAGE、locationRisk 与 disappearCount，同时保留已有筛选、游标分页和默认 DATES 降序语义。

**Blocked by:** None — can start immediately

**Status:** done

- [x] Demand 网格所有可见列均可通过列头启动服务端排序，不再存在仅因缺少实现而禁用的可见列
- [x] Host parser、内存/SQL 查询、游标编码与比较支持新增列，并保持 DemandId 为稳定升序次键
- [x] nullable 文本、布尔值、计数值及相同主值在 asc/desc 跨页时均无重无漏
- [x] 第一次点击升序、第二次降序、方向箭头、刷新保持排序及错误 cursor 安全回首页语义不回归
- [x] 运行时与静态 OpenAPI 公布同一完整 Demand sortBy allow-list，非法 token 仍稳定返回 400
- [x] 多页真实 HTTP + Watch 集成测试覆盖每类新增排序值，并证明排序作用于完整结果集

## Comments

- 2026-08-01: Added status, AREA, EQP, STEP, PACKAGE, locationRisk, and disappearCount sorting end-to-end through Watch, Host parser, cursor payload/comparison, InMemory paging, and SQL Server keyset queries. DemandId remains the ascending stable tie-break for every non-DemandId primary sort.
- 2026-08-01: Nullable text sorts null-first ascending/null-last descending. Real Host + Watch pagination and LocalDB tests cover both directions, tied values, nulls, booleans, and counts with page size 2 and no gaps or duplicates.
- 2026-08-01: Runtime and packaged OpenAPI publish the same complete Demand allow-list; locationRiskCode remains rejected with HTTP 400. Full suite: 404 passed, 0 failed, 0 skipped; full solution build: 0 warnings, 0 errors.
- 2026-08-01: Review clarified that status sorting is necessarily a tied-primary sort because the existing API requires exactly one VISIBLE or GONE status partition; runtime/static OpenAPI now state this explicitly, and the HTTP + Watch cases verify both directions and stable cursor traversal within that partition.
