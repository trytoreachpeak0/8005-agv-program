# Ticket 17 test research — frozen V2 API/OpenAPI contract

## Bounded target inventory

- Public seam confirmed by `.scratch/new-mes-ingest/spec.md`: production
  versioned HTTP API and its published OpenAPI; real Round -> Host -> SQL ->
  HTTP is used where runtime state is required.
- Runtime surface: 17 GET-only routes in
  `MesIngest.Host/NewMesIngestEndpoints.cs`. All are currently excluded from
  API Explorer. Most list handlers manually parse `HttpRequest`, so generated
  OpenAPI cannot infer their query parameters, response schemas, or errors.
- Contract identity: `NewMesIngestContract` is still the ticket-16 placeholder
  `2026.08.new-mes-ingest.tracer.16` / schema 16. Discovery exposes no
  capability set or exact-match policy.
- Documentation: `MesIngestOpenApi` and `pack/openapi/v1.json` describe only
  legacy Development V1. Production V2 does not register Swagger/OpenAPI.
- Cursor credentials: ReadabilityAudit distinguishes invalid, mismatched, and
  missing-snapshot credentials. ErrorSearch currently maps both tampering and
  binding mismatch to `INVALID_ERROR_SEARCH_CURSOR`.
- Release boundary: Production already suppresses legacy routes, but package
  metadata still records `openApiStatus=DEFERRED_TO_TICKET_17` and ships no
  canonical V2 document.
- Existing conventions: .NET SDK 10.0.302, VSTest, xUnit 2, production
  `WebApplicationFactory<Program>`, disposable real SQL Server fixture, camelCase
  JSON, string domain vocabularies, static/live OpenAPI comparison.

## Explicit acceptance checklist

1. 新版契约发现返回唯一、可比较的契约版本和能力集合；Host 与 Watch 版本不精确匹配时明确拒绝业务解释，不做缺字段、旧状态或客户端单页过滤降级。
2. OpenAPI 完整描述 Poll 健康与证据、DemandSeries 列表/详情/世代/事件、`ExternallyReadableDemandCatalog`、`ReadabilityAuditSnapshot`、SeriesErrorCatalog、ErrorSearch 列表/分面/详情/受限原始证据、CurrentIngestAttention 与 `WatchOverviewSnapshot`，且同一能力只定义一套新版 DTO 语义。
3. 契约固定字段含义、必填/可空性、稳定枚举、UTC 与带 offset 时间表达、契约版本、快照身份、ProjectionCommit、`CatalogRevision`、精确总数、默认/最大页大小、稳定排序和错误响应；OpenAPI 示例不会使用冻结字段、旧 incident 或 DemandChangeFeed 术语。
4. 资格和错误游标分别绑定各自快照、规范化筛选、顺序与版本，并具有可区分的篡改、过期和不匹配错误；目录条件读取的 ETag/304 不被误写成审计或错误分页 Cursor。
5. 运行时契约测试证明实际响应、认证要求、访问控制、条件请求、分页、大小上限、错误码与发布的 OpenAPI 一致，客户端可仅凭契约实现成功、空结果、陈旧快照和失败路径。
6. Watch 业务能力在契约中保持只读；若发布 WatchRefreshTrace 遥测入口，它是独立、鉴权、白名单、追加、幂等、限流且有大小限制的技术通道，不能承载 TransportDemand、错误或其它业务投影写入。
7. 暂留旧端点被明确标记为 legacy/development-only，不出现在新版能力发现，不被新版 reference consumer 或 Watch 契约测试调用，也不要求新 DTO 与旧 schema/API 双写或互转。
8. 发布门禁明确阻止“旧端点仍启用”的构建被宣称为 ADR-mes-0017 的生产切换完成；生产上线前必须停止旧 Host、Watch 与消费者并由后续收缩/切换工作移除或禁用旧契约，不能把本票解释为生产混跑支持。
9. 契约快照和兼容性测试能区分有意新增、破坏性变更与文档漂移；冻结后任何字段换义、枚举复用、主分类改变或端点语义分叉都会产生可观察失败并要求显式重新决策。

## Reusable test infrastructure and baseline

- Reuse `Ticket01SqlServerFactAttribute`, `Ticket01SqlServerDatabase`,
  `Ticket01ProcessEnvironmentScope`, the `Ticket01SqlServer` collection,
  production V2 factory configuration, `RoundIngestor`, and controlled rounds.
- Reuse canonical LF and `JsonNode.DeepEquals` helpers from
  `OpenApiContractTests`; compare the complete V2 document, not only `paths`.
- Reuse existing catalog ETag, raw-evidence authorization, audit token, error
  token, and release-package fixture helpers.
- Baseline command passed before edits: 7/7 `OpenApiContractTests`, zero skips.
- Focused feedback command: `dotnet test MesIngest.Tests/MesIngest.Tests.csproj
  -c Release --no-restore --filter
  "FullyQualifiedName~MesIngest.Tests.NewMesIngestOpenApiContractTests"`.
