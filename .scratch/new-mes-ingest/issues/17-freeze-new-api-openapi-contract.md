# 17 — 冻结完整新版 API/OpenAPI 契约、旧端点暂留

**What to build:** 冻结供新版 Host、Watch 和外部消费者共同实现的完整版本化 API/OpenAPI 契约，把 Poll 证据、DemandSeries、外部可读目录、资格审计、错误目录与检索、受限证据、CurrentIngestAttention 和一致概览统一成可独立消费的明确协议。开发期暂时保留现有旧端点以便后续调用方分批迁移并保持工作树可验证，但新版契约不适配旧 DTO，旧端点不进入新版契约发现；这种暂留只是一段开发排序，不授权生产兼容、滚动升级或新旧 Host/Watch/消费者混合运行。

**Blocked by:** 08 — 提供 DemandSeries 冻结快照列表与详情；09 — ExternallyReadableDemandCatalog 与 reference consumer；10 — ReadabilityAuditSnapshot 查询与详情；11 — ErrorSearchAsOf 列表、窗口与分面；12 — 错误详情与受限原始证据；13 — CurrentIngestAttention 当前关注读取；14 — 一致 WatchOverviewSnapshot；15 — 正式单语句 Oracle Round source；16 — ProjectionCommit 原子性与并发可靠性门禁

**Status:** ready-for-human

- [x] 新版契约发现返回唯一、可比较的契约版本和能力集合；Host 与 Watch 版本不精确匹配时明确拒绝业务解释，不做缺字段、旧状态或客户端单页过滤降级。
- [x] OpenAPI 完整描述 Poll 健康与证据、DemandSeries 列表/详情/世代/事件、`ExternallyReadableDemandCatalog`、`ReadabilityAuditSnapshot`、SeriesErrorCatalog、ErrorSearch 列表/分面/详情/受限原始证据、CurrentIngestAttention 与 `WatchOverviewSnapshot`，且同一能力只定义一套新版 DTO 语义。
- [x] 契约固定字段含义、必填/可空性、稳定枚举、UTC 与带 offset 时间表达、契约版本、快照身份、ProjectionCommit、`CatalogRevision`、精确总数、默认/最大页大小、稳定排序和错误响应；OpenAPI 示例不会使用冻结字段、旧 incident 或 DemandChangeFeed 术语。
- [x] 资格和错误游标分别绑定各自快照、规范化筛选、顺序与版本，并具有可区分的篡改、过期和不匹配错误；目录条件读取的 ETag/304 不被误写成审计或错误分页 Cursor。
- [x] 运行时契约测试证明实际响应、认证要求、访问控制、条件请求、分页、大小上限、错误码与发布的 OpenAPI 一致，客户端可仅凭契约实现成功、空结果、陈旧快照和失败路径。
- [x] Watch 业务能力在契约中保持只读；若发布 WatchRefreshTrace 遥测入口，它是独立、鉴权、白名单、追加、幂等、限流且有大小限制的技术通道，不能承载 TransportDemand、错误或其它业务投影写入。
- [x] 暂留旧端点被明确标记为 legacy/development-only，不出现在新版能力发现，不被新版 reference consumer 或 Watch 契约测试调用，也不要求新 DTO 与旧 schema/API 双写或互转。
- [x] 发布门禁明确阻止“旧端点仍启用”的构建被宣称为 ADR-mes-0017 的生产切换完成；生产上线前必须停止旧 Host、Watch 与消费者并由后续收缩/切换工作移除或禁用旧契约，不能把本票解释为生产混跑支持。
- [x] 契约快照和兼容性测试能区分有意新增、破坏性变更与文档漂移；冻结后任何字段换义、枚举复用、主分类改变或端点语义分叉都会产生可观察失败并要求显式重新决策。
