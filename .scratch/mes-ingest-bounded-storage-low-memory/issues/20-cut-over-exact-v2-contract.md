# 20 — 完成精确 V2 契约整体切换

**What to build:** 把已经迁移的 HistoryEpoch、历史过期和当前性语义作为一个精确 NewMesIngestContract 身份同时交付给 Host、Watch 和 reference consumer，而不增加并行 V3 或旧 DTO 降级。

**Blocked by:** 19 — 实施非计划历史重置确认.

**Status:** ready-for-agent

- [ ] 同时提升精确 contractVersion 与 schemaVersion，并更新完整 capability ID/version 集合。
- [ ] 所有相关响应、snapshot、cursor、410 和 503 契约在唯一 /api/v2 与规范文档中完整声明。
- [ ] Host 在业务解释前拒绝 contract、schema 或 capability 身份不精确匹配的调用方。
- [ ] Watch 与 reference consumer 作为同一包迁移到新身份，不保留旧 DTO fallback、缺字段兼容或长期双路由。
- [ ] 旧纪元、旧 contract、旧 schema 和跨筛选 cursor 的错误码与 HTTP 语义具有契约测试。
- [ ] 复用现有 contract freeze、OpenAPI 生成、wire DTO 和 compatibility classifier，只做精确身份的 expand/contract 收尾；不增加 V3、兼容适配层或新的代码生成流程。
- [ ] 开发期只运行聚焦 OpenAPI/contract/Host HTTP/Watch client/reference consumer 测试，关闭时生成一次规范并运行一次真实 SQL Server Tier 1。
- [ ] 正常验证目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0；只有生成规范与运行端点不一致时才增加发布冒烟。
