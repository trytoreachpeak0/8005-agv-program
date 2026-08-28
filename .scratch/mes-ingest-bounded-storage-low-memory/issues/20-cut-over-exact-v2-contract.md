# 20 — 完成精确 V2 契约整体切换

**What to build:** 把已经迁移的 HistoryEpoch、历史过期和当前性语义作为一个精确 NewMesIngestContract 身份同时交付给 Host、Watch 和 reference consumer，而不增加并行 V3 或旧 DTO 降级。

**Blocked by:** 19 — 实施非计划历史重置确认.

**Status:** ready-for-human

- [x] 同时提升精确 contractVersion 与 schemaVersion，并更新完整 capability ID/version 集合。
- [x] 所有相关响应、snapshot、cursor、410 和 503 契约在唯一 /api/v2 与规范文档中完整声明。
- [x] Host 在业务解释前拒绝 contract、schema 或 capability 身份不精确匹配的调用方。
- [x] Watch 与 reference consumer 作为同一包迁移到新身份，不保留旧 DTO fallback、缺字段兼容或长期双路由。
- [x] 旧纪元、旧 contract、旧 schema 和跨筛选 cursor 的错误码与 HTTP 语义具有契约测试。
- [x] 复用现有 contract freeze、OpenAPI 生成、wire DTO 和 compatibility classifier，只做精确身份的 expand/contract 收尾；不增加 V3、兼容适配层或新的代码生成流程。
- [x] 开发期只运行聚焦 OpenAPI/contract/Host HTTP/Watch client/reference consumer 测试，关闭时生成一次规范并运行一次真实 SQL Server Tier 1。
- [x] 正常验证目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0；只有生成规范与运行端点不一致时才增加发布冒烟。

## Comments

- `NewMesIngestContract` 已整体切到 `2026.08.new-mes-ingest.v2.1`、schema `28` 和九项 capability `2.0`；路径与操作集合保持唯一只读 `/api/v2`，没有新增 V3、旧 DTO fallback、双路由、兼容适配层或代码生成流程。SQL 空库 bootstrap/已有 schema 校验、发布包、release smoke 与 factory acceptance 同时冻结该身份。
- 中心 `RequireExactCompatibility` 现在一次比较 contractVersion、schemaVersion 与完整 capability ID/version 集合，并稳定拒绝缺失、额外、重复、旧 version、缺字段及 null capability。Watch 与 reference consumer 都复用该 matcher，在任何业务解释前完成 `/api/v2/contract` 精确检查；每份业务 snapshot/目录响应继续校验精确 contractVersion。
- 既有 HistoryEpoch、历史过期 410 `MES_INGEST_HISTORY_EXPIRED`、当前性 503 `INGEST_NOT_CURRENT`、旧纪元 `HISTORY_EPOCH_MISMATCH` 以及 Demand Series/Readability Audit/Error Search 跨筛选 cursor/snapshot 拒绝语义保持在同一 wire DTO 与唯一 Host HTTP/OpenAPI surface。canonical `pack/openapi/v2.json` 通过既有 export seam 只生成一次，并新增 schemaVersion `28` 与 capability version `2.0` 的精确枚举。
- TDD 纵向 red→green 覆盖冻结 identity、Watch 旧 capability version、reference consumer 整体身份和 OpenAPI schema 精确枚举。聚焦 OpenAPI/contract/Host HTTP/Watch/reference consumer/历史错误语义门禁在真实 SQL Server 上为 132 通过、0 失败、0 跳过；review finding 的受影响完整类复跑为 34 通过、0 失败、0 跳过；release package identity 为 22 通过、0 失败、0 跳过。
- 两轴 review 固定点为 `c698a354`。Standards 初审发现 null capability 会泄漏空引用而不是稳定 contract failure，已增加中心与 Watch wire 回归并修复；二审 Standards 与 Spec 均为 `No findings`。`git diff --check` 通过。
- 最终从 `mes/ingest/csharp` 只运行一次 `dotnet test MesIngest.Tests`：854 通过、0 失败、0 跳过，11 分 48 秒。三个门禁变量均显式设置；连接真实默认 SQL Server（Enterprise Evaluation，非 LocalDB），ProductMajor 16、compatibility 160。
- 未修改 `MesIngest.Watch` UI/XAML、Wpf.Ui、布局、UI Automation、DPI 或视觉基线，未运行 Tier 2/3，也没有人工视觉事项。Ticket 20 已关闭 Ticket 21 的 blocker；本提交经人工复核后可以串行进入 Ticket 21。
