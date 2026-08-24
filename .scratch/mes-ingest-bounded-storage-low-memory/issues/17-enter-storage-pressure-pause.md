# 17 — 实施 StoragePressurePause 与本地恢复

**What to build:** 实现 StoragePressurePause 的完整端到端状态机：数据库卷接近耗尽时在查询 MES 前暂停，并只允许数据库主机上的授权人员通过 MesIngestLocalAdministration 明确恢复。

**Blocked by:** 16 — 运行 Host 每小时有预算清理.

**Status:** ready-for-human

- [x] 从实际数据库文件解析并验证受监控卷，不允许用未解析环境变量、通配路径或错误磁盘代替。
- [x] 剩余空间低于 15% 时产生严重存储告警，低于 10% 时在调用 MES 查询之前原子进入 StoragePressurePause。
- [x] 暂停期间不调用 MES、不取得新 PollTrace、不推进缺席、GONE、归档或 TaskTypeProtection 恢复。
- [x] Watch 诊断、最后成功投影和仍在窗口内的历史继续可读。
- [x] ExternallyReadableDemandCatalog 与执行承诺读取返回 503 INGEST_NOT_CURRENT，不返回陈旧目录或空集合。
- [x] 空间回升、清理成功、Host 重启或连续成功健康检查都不能自动恢复轮询。
- [x] 本地恢复命令验证授权身份、精确目标数据库、当前暂停状态、安全空间和数据库可读写健康。
- [x] 成功恢复审计执行身份、原因、HistoryEpoch、前后状态和 Host UTC；未授权、错误纪元/数据库或健康失败时保持暂停。
- [x] Watch 不增加恢复按钮，远程 Host API 不暴露恢复写操作，直接修改 SQL 状态不构成合法确认。
- [x] 可控卷空间与脚本化轮次端到端覆盖 15%/10% 边界、查询前门禁、重启、恢复、幂等和失败后不开放外部读取。
- [x] 恢复后的下一轮遵守正常调度而非补跑，真实 SQL Server Tier 1 最终 Failed: 0、Skipped: 0。
- [x] 使用可注入的卷空间读取 seam 和最小真实数据库健康检查，不实际填满磁盘、不等待空间变化，也不建设跨平台存储监控框架。
- [x] 所有阈值、暂停、恢复、错误身份和审计分支先用确定性策略测试覆盖；真实 SQL Server 只运行一个暂停/恢复成功路径和一个代表性拒绝路径。
- [x] 开发期运行聚焦状态机/CLI/HTTP 测试，关闭时运行一次真实 SQL Server Tier 1；验证部分目标在 60 分钟内完成并保持 Failed: 0、Skipped: 0。

## Comments

- Host 查询前门禁现在由 `StoragePressureGuardedPollRunner` 统一复用于持续轮询和 one-shot；实际 `sys.database_files` 文件身份解析到唯一物理卷，可注入的空间 reader 在 `<15%` 写严重告警、`<10%` 原子写持久暂停。暂停没有自动清除路径，空间回升、Host 重启和直接把状态列改成 `HEALTHY` 都会因缺少匹配恢复审计继续判定为暂停。
- SchemaVersion 提升到 26，新增单行存储压力状态和不可变恢复审计。CurrentIngestAttention/Watch 继续只读展示数据库、卷、可用百分比和暂停身份；历史/PollTrace 读取仍可用，ExternallyReadableDemandCatalog 及 reference consumer 的无条件执行承诺读取返回 HTTP 503 `INGEST_NOT_CURRENT`。没有 Watch 恢复按钮或远程恢复 API。
- 打包新增 `administration/MesIngest.LocalAdministration.exe resume-storage-pressure`。命令只从命名环境变量取连接串，并验证 Windows 集成 SQL 身份为 `db_owner`/`sysadmin`、执行机匹配 SQL `MachineName`、精确数据库/HistoryEpoch、持久暂停、安全空间 `>=15%`、数据库 `ONLINE`/`READ_WRITE`；成功事务审计身份、原因、前后状态、纪元和 Host UTC，重试幂等。
- TDD 聚焦候选最终 75/75 通过、0 跳过；真实 SQL 两个代表路径 2/2 通过、0 跳过。test-gap 注入“忽略恢复审计即可开放”的突变后目标真实 SQL 测试失败，恢复源码后重新通过。两轴 code review 最终 Standards/Spec 均为 `No findings`。
- 首轮 Tier 1 暴露两个测试契约回归（840 通过、2 失败、0 跳过）：Watch wire fixture 缺少 storage diagnostics，HistoryEpoch 破坏性 schema 测试未先移除两个新增外键；修复后的精确窄测 2/2 通过。最终从 `mes/ingest/csharp` 运行 `dotnet test MesIngest.Tests`：842 通过、0 失败、0 跳过，11 分 10 秒；SQL Server ProductMajor 16、compatibility 160，非 LocalDB，因此本票 SQL 路径没有仓库所述的跳过覆盖限制。
- 已读取 `docs/agents/fluent-ui.md` 与 `docs/agents/golden-renderer.md`。未运行 Tier 2/3：用户明确禁止，且本票没有 XAML、布局、Wpf.Ui 控件、DPI 或视觉基线改动；只在既有 Current Attention 行中增加只读文字/证据映射。未创建、批准或推广任何 baseline，也未创建 golden scheduled task。若维护者要求对新增文字状态做正式视觉预览，仍需在 `gpt_win11` 交互桌面运行最窄 Tier 2 并人工审阅。
