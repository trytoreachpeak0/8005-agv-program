# 24 — 迁移发布脚本、smoke 和验证说明

**What to build:** 让发布、安装、smoke 和验证工作流只使用已冻结的新版 MesIngest 契约，从发布包启动真实 Service 与 Watch 后能够验证单条正式 Oracle 查询、SQL Server 持久化、版本化读取、CatalogRevision 条件读取和关键 Watch 行为，而不再调用或教授旧 Demand、IngestAlert incident 或 DemandChangeFeed 流程。

**Blocked by:** 15 — 正式单语句 Oracle Round source；17 — 冻结完整新版 API/OpenAPI 契约、旧端点暂留；23 — 共享黄金机 UI 集成验收与基线

**Status:** ready-for-agent

- [ ] 发布、安装、卸载、release smoke、Watch acceptance、工厂验证和返回清单统一使用新版契约发现、轮询证据、需求系列、资格审计、错误检索、当前关注、概览和 ExternallyReadableDemandCatalog 能力。
- [ ] 所有已知打包与验证调用方停止请求旧 DemandChangeFeed、bootstrap high-watermark、SYNC_CURSOR_EXPIRED、旧 IngestAlert incident、字段冻结和旧分页 DTO；验证文本不再建议下游持久业务镜像。
- [ ] 发布包只包含一份正式 MES_TASK_UNION 查询原稿，并能证明 Service 和 Watch 使用同一版本化契约；文件或脚本化轮次可以在无工厂 Oracle 时驱动同一生产入口做可重复 smoke。
- [ ] smoke 验证首次目录正文、CatalogRevision/ETag、同修订 304、新版只读 API 鉴权、契约严格匹配、SQL Server 重启持久化，以及关闭 Watch 后 Service 继续轮询和提供 API。
- [ ] 验证说明明确区分本机或黄金机证据、真实兼容 SQL Server 门禁和工厂 Oracle 验收；未运行的外部门禁必须记录为具名 skip，不能把替代环境通过写成现场通过。
- [ ] 配置模板、命令输出和证据不包含 Oracle、SQL Server、API 或黄金机凭据；远程绑定缺少共享密钥时拒绝启动或拒绝业务数据访问，日志与返回包遵循脱敏边界。
- [ ] 包装后的 Watch smoke 若需要启动、操作或截图真实 WPF，必须通过 gpt_win11 交互计划任务执行；PowerShell Direct 只做部署、监控和证据取回。
- [ ] 当票 23 已批准的 PNG/XML/UIA/DPI 输出未变化时，包装 smoke 只验证已发布二进制的启动、连接和关键功能，不重复像素候选、10 次稳定、基线提升或 DPI clone；若包装差异造成 UI 输出变化，则明确使相应票 23 场景失效并只重跑受影响门禁。
- [ ] 自动化校验发布包中不再出现旧端点、旧配置项或旧契约说明，并证明运行时 OpenAPI 与包内版本化 OpenAPI 一致。
