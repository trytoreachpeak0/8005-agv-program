# 19 — 实施非计划历史重置确认

**What to build:** 当无备份数据库不可恢复丢失时，让系统建立新 HistoryEpoch、阻断外部当前读取，并要求授权运维人员明确接受旧历史与墓碑已丢失的风险后再开放。

**Blocked by:** 17 — 实施 StoragePressurePause 与本地恢复.

**Status:** ready-for-human

- [x] 系统区分普通 Host 重启、计划空库切换和非计划不可恢复重建；普通重启不换纪元。
- [x] 非计划重建创建新 HistoryEpoch，并记录需要 HistoryResetAcknowledgement 的持久状态。
- [x] 确认前 ExternallyReadableDemandCatalog 和执行承诺读取持续返回 503 INGEST_NOT_CURRENT，诊断与新纪元建立进度仍可读。
- [x] RestartBarrier、成功轮次、磁盘恢复或服务重启都不能代替 HistoryResetAcknowledgement。
- [x] 本地管理命令验证授权身份和目标 HistoryEpoch，并审计旧墓碑不可恢复的风险接受、前后状态与时间。
- [x] 确认不声称恢复旧墓碑；确认后只在新纪元开放，旧 snapshot、cursor、cache 和条件身份全部被拒绝。
- [x] 复用 Ticket 17 的 MesIngestLocalAdministration、审计、503 和空库 bootstrap seam，不新建第二套管理命令或恢复状态框架。
- [x] 三种启动路径、错误纪元、重复确认和 reference consumer 行为先用最小空库与确定性状态测试覆盖；不删除真实业务库、不生成历史数据。
- [x] 真实 SQL Server 只运行一个非计划重建/确认成功路径和一个错误纪元拒绝路径；开发期用聚焦测试，关闭时运行一次 Tier 1。
- [x] 正常验证目标在 45 分钟内完成并保持 Failed: 0、Skipped: 0；只有纪元持久化或 503 边界无法由最小空库证明时才扩大矩阵。

## Comments

- 三种 bootstrap 路径现由既有 `HistoryEpochBootstrapIntent` 空库 seam 明确区分：默认首次建库与计划空库不要求确认，非计划不可恢复重建持久写入确认要求；普通 Host 重启保持原 HistoryEpoch 和确认状态。三个空成功轮次、RestartBarrier 完成、健康空间观测及 Host 重启均不能清除要求。
- 复用并泛化 Ticket 17 的单一 `MesIngestLocalAdministration` 与审计边界：同一 CLI 新增 `acknowledge-history-reset` 子命令，同一授权/本机/精确数据库上下文验证目标 HistoryEpoch，并在 `LocalAdministrationAudits` 中记录执行身份、原因、精确风险接受、前后状态与 Host UTC。重复确认幂等；直接改状态列或错误纪元均不能形成有效确认。
- 确认前生产目录、HTTP `/api/v2/externally-readable-demand-catalog` 和 reference consumer 无条件执行承诺读取均返回 503 `INGEST_NOT_CURRENT`；Current Attention 仍公开新 HistoryEpoch 的诊断项。确认后目录只返回新纪元空目录，不声称恢复旧墓碑；旧条件 ETag/缓存身份抛出 `HISTORY_EPOCH_MISMATCH`，既有 Demand Series/Error Search/Readability Audit 测试继续证明旧 snapshot/cursor 跨纪元拒绝。
- TDD 逐个纵向完成领域策略、三启动路径、持久 503、CLI/审计和旧纪元条件身份。真实 SQL 只保留 `Unrecoverable_rebuild_stays_not_current_until_the_exact_risk_acknowledgement` 成功路径与 `Wrong_epoch_and_direct_status_edit_cannot_acknowledge_the_unrecoverable_rebuild` 拒绝路径；使用最小空库与空成功轮次，不删除业务库、不物化业务历史。
- 两轴 review 固定点为 `f6490760`。初审修复了三个 finding：C#/SQL 操作与风险常量漂移、测试生成业务 observation、无效审计 ID 暴露；最终 Standards 与 Spec 均为 `No findings`。变更文件 `dotnet format --verify-no-changes`、`git diff --check` 及非增量 solution build 均通过（0 warnings、0 errors）。
- 首次 Tier 1 暴露 4 个冻结预期/规范快照回归（848 通过、4 失败、0 跳过）：schemaVersion 26、六类 Attention、旧纪元条件身份强制刷新、canonical OpenAPI Attention enum。仅同步对应测试/快照后精确窄测 4/4 通过。最终从 `mes/ingest/csharp` 运行 `dotnet test MesIngest.Tests`：852 通过、0 失败、0 跳过，12 分 3 秒。显式门禁为真实默认 SQL Server（Enterprise Evaluation，非 LocalDB）、ProductMajor 16、compatibility 160。
- 未修改 `MesIngest.Watch` UI/XAML、Wpf.Ui、布局、UI Automation、DPI 或视觉基线，未运行 Tier 2/3，也没有人工视觉事项。Ticket 20 未实施；Ticket 19 已关闭其 blocker，可以在本提交人工复核后串行进入 Ticket 20。
