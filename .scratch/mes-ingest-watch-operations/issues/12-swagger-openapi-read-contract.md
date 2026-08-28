# 12 — Swagger/OpenAPI 人工测试与合作者 API 指南

**What to build:** 为 MesIngest 正式只读 API 提供可执行 Swagger UI、OpenAPI JSON 和发布包静态契约，覆盖分页、同步、Alert 和鉴权。

**Blocked by:** 05 — 分页 Demand API; 06 — DemandChangeFeed; 10 — Alert API

**Status:** done

- [x] Host 暴露 `/swagger` 与 `/openapi/v1.json`，远程绑定时文档也默认启用
- [x] `/api/*` 继续遵循 SharedSecret；Swagger UI 提供 Bearer Authorize 并能实际执行 GET
- [x] 文档说明文档元数据可见与 API 数据鉴权的边界
- [x] 描述所有筛选、排序、page/cursor、410/400/401/404、示例和 page size 上限
- [x] 明确 dates=当前工序进入时间、step=下一工序、mesLastSeenAt=Host观察时间、goneAt=GONE转换时间
- [x] 描述 ChangeFeed 的 CREATED/GONE only、48h 默认 retention 和权威 Bootstrap
- [x] 发布目录包含静态 OpenAPI JSON，供离线合作者导入 Postman/代码工具
- [x] 不新增任何测试写接口、假 Demand/Alert 注入或状态修改 endpoint
- [x] 合约测试验证 OpenAPI 路径与实际 endpoint/鉴权一致

## Comments

- There are no existing external consumers requiring the old unpaged response shape.
- 2026-07-31: Implemented Swashbuckle `/swagger` + `/openapi/v1.json` (public docs; `/api/*` SharedSecret unchanged), DocumentFilter summaries/examples/400·401·404·410, pack `openapi/v1.json` + publish staging, OpenApiContractTests. Review follow-ups addressed: timezone prose, structured error responses, live↔static description/security parity.
