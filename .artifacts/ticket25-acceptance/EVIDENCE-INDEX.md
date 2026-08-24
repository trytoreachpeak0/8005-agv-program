# Ticket 25 — 打包发布门禁验收证据

**结论：PASSED**（2026-08-19 23:12:24 +08:00）

`GOLDEN_RENDERER_VALIDATION_PASSED: suite=watch-package-release`

## 运行身份

| 项 | 值 |
| --- | --- |
| 证据目录 | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-25/run-20260819-225413-watch-package-release` |
| Guest 运行目录 | `C:\MesIngest\25\run-20260819-225413-watch-package-release` |
| 源提交 | `23ba5ff7e78158349639f32fda85360a1692962d` |
| Dirty | 否 |
| Payload SHA-256 | `CCEF85C2AC9DF2939E9C2C6F8DA7B0756ECF45F113F36FD323B108E6114C243A` |
| 发布包 manifest SHA-256 | `701E6C75B1C4D54217AEDA8FAD413EA542D0A8BBF499733CEE67B6B5F305F2BB` |
| 计划任务退出码 | 0 |
| `release-gates-passed.json` | `READY_FOR_HOST_CLEANUP_AND_FINALIZATION` |

## 环境

`Test-GoldenRendererEnvironment.ps1` 前后各一次，`Differences: []`：
GPT-WIN11 / 交互 session 1 / Explorer 在会话内 / 1920x1080 / 96 DPI / 100% /
浅色 / zh-CN / China Standard Time / Microsoft YaHei UI + Consolas / SoftwareOnly。

## 门禁结果

| 阶段 | 结果 | 证据 |
| --- | --- | --- |
| 发布包构建与校验 | `MESINGEST_RELEASE_PACKAGE_VALID`，911 个文件 | `host-package-build.log` |
| 发布烟测 | **PASSED** | `Results/release-smoke/release-smoke-result.json` |
| 全量回归 | **533 total / 533 executed / 533 passed / 0 failed / 0 skipped** | `Results/core-host-http-sql/{summary.json,core-host-http-sql.trx}` |
| 打包 Watch 验收 | `watch-vm-tests`（149 项 0 失败）+ `watch-ui-journeys`（1 项 0 失败），16 张截图 + UIA 树 | `Results/packaged-watch-acceptance/` |
| 人工验收 | Zhengyu Shao，2026-08-19 22:52:19，SHA-256 `B5469B7C…` | `.artifacts/ticket25-acceptance/manual-acceptance.json` |
| 清理 | 计划任务已注销、残留进程 0、post-cleanup 环境复核 PASSED | `cleanup.json`、`environment-after-host-cleanup.json` |

回归用例数由票 24 的 937 降至 533，是本票删除 48 个退役 shell 测试文件的直接结果，
不是丢失覆盖：黄金机与本机两侧计数一致，且本轮 **0 skip**。

## 烟测逐项证据

真实 SQL Server（`192.168.200.1` / `MesIngest_Ticket25_Smoke`，专用可丢弃空库，
启动前 `preflightUserTableCount = 0`，SQL 认证 + DPAPI 凭据）：

| 检查 | 实测 |
| --- | --- |
| 契约身份 | `2026.08.new-mes-ingest.v2.0` / schema 17 / `EXACT_VERSION_SCHEMA_AND_CAPABILITIES` / 9 项能力精确匹配 |
| 运行时 vs 包内 OpenAPI | 完整 JSON 语义严格一致 |
| **退役配置键（本票新增）** | 注入 `ChangeFeedRetentionHours` 后包内 Host **拒绝启动**，退出码 `-532462766`，且核对 stderr 确为 `retired keys` 而非端口冲突 |
| 退役端点 | `/api/contract`、`/api/demands`（含详情）、`/api/alerts`、`/api/poll-health`、`/api/demand-changes`、`/openapi/v1.json` **全部 404** —— 本票之后是端点不存在，而非被开关关闭 |
| Service/Watch 同一契约 | `MesIngest.Core.dll` 两端字节一致（`4dbc0952…`） |
| 轮次来源 | `FILE_REPLAY` / `liveOracleAttested=false` / `oracleConnectionAttempted=false` |
| 目录首次正文 | count=2，`catalogRevision=2`，ETag `W/"catalog-r2"` |
| 同修订条件读取 | **304**，无正文 |
| 受限原始证据鉴权 | 无密钥 403 / 错密钥 403 / 正确密钥 400（鉴权已过） |
| 远程绑定无密钥 | 拒绝启动，且核对拒绝原因确为缺 SharedSecret |
| Service 独占轮询 | 无 Watch 进程时 `pollTraceHighWater` 7 → 8 → 21 持续前进 |
| 关闭 Watch 后 | Host 仍在服务并继续轮询 |
| Watch 启动耗时 | **14,231.6 ms**，25 秒上限内 |
| SQL Server 重启持久化 | 强杀重启后目录条目集合与 `catalogRevision` 不变 |

## 具名 skip

打包 Watch 验收有 5 个 skip，**精确匹配**预期具名集合
（`skippedMatchesExpectedNamedSet: true`），原因
`STABILITY_GATE_ENTRY_POINT_AND_GOLDEN_FIXTURES_EXCLUDED_FROM_RELEASE_PAYLOAD`：

- `WatchWindowCandidateEquivalenceTests.Candidate_directories_are_visually_equivalent`
  —— 稳定性门禁自身的入口点；
- `WatchWindowVisualEquivalenceGoldenFixtureTests` 的 4 个用例 —— 需要
  `MESINGEST_WATCH_GOLDEN_FIXTURES` 指向真实黄金截图，而 payload 故意排除 `.artifacts`。

全量回归 **0 skip**。工厂 Oracle 验收不在本门禁范围（`liveOracleAttested=false`），
仍按 `FACTORY-VALIDATION.md` 在现场完成，归票 26。

## 票 23 视觉验收的复用与其边界

`ticket23VisualBaselinesReused: true`，依据
`PACKAGING_DID_NOT_CHANGE_APPROVED_PNG_XML_UIA_OR_DPI_OUTPUT`。

**这一轮没有对票 23 的 11 份生产窗口基线做像素比对。** 复用结论建立在两件事上：
本票未改动 `WatchWorkspaceWindow` 及其 XAML（删除的是退役 shell 自己的场景与基线），
以及非像素套件全绿加签字人对 10 张黄金机截图的复核。该保留说明已在签字时明确告知
批准人，并记录在 `manual-acceptance.json.reviewedEvidence.ticket23ReuseCaveatShownToApprover`。
若日后需要更硬的证据，应另跑 `-Suite watch-window-visual` 做真正的基线比对。

## 达成过程中修复的缺陷

共跑 5 轮，前 4 轮的红全部是真问题，逐条修复而非重跑掩盖：

1. **17 个 SQL 门禁测试仍注入 `EnableLegacyDevelopmentEndpoints`**（80 红）。
   这些文件只在真实 SQL Server 应答时才构造 Host，本机全部 skip，所以 tier 1 报绿。
   修复：删除注入，并新增一条不需要 VM 的守卫——任何源码都不得用
   `MesIngestHostOptions.RetiredConfigurationKeys` 里的键配置 Host（提交 `4836702`）。
2. **烟测库未清空**（第 2 轮）。上一轮烟测已 bootstrap 出 19 张表，而烟测要求真正的空库。
   非代码问题；此后每轮前用一次性 fixture 先删后建。
3. **票 25 新增的三个扫描依赖 `git ls-files`**（3 红）。黄金机跑的是 robocopy 源码副本，
   既非 git 工作树、客户机也没有 git。修复：改为直接遍历源码树，排除
   `bin`/`obj`/`TestResults`/`.artifacts`/`.git`，并永不打开 `*.Local.json`（提交 `23ba5ff`）。

第 1、3 两条都属于同一类盲区：**本机 tier 1 看不见只在真实 SQL Server 或 payload 上才成立的前提**。
第 1 条修复时补的守卫已经把这类问题拉回 tier 1；第 3 条则通过去掉外部工具依赖，
使扫描在本机与 payload 上语义相同。

## 遗留（不属于本票）

- 黄金机 payload 由 robocopy 整个 `mes/ingest/csharp` 生成，只排除
  `bin`/`obj`/`TestResults`/`.artifacts`，因此 `MesIngest.Host/appsettings.Local.json`
  连同现场 Oracle 口令一并进入 VM。这是票 24 之前就存在的行为，发布包本身有
  `Publish-MesIngest.ps1` 的剥离逻辑（`credentials must not ship`），受影响的只是验证 payload。
- 打包 Watch 冷启动 14.2 s，仍在票 27 的观察范围内。
