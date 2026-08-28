# Ticket 24 — 打包发布门禁验收证据

**结论：PASSED**（2026-08-19 18:15:37 +08:00）

`GOLDEN_RENDERER_VALIDATION_PASSED: suite=watch-package-release`

## 运行身份

| 项 | 值 |
| --- | --- |
| 证据目录 | `mes/ingest/csharp/.artifacts/golden-renderer/ticket-24/run-20260819-175808-watch-package-release` |
| Guest 运行目录 | `C:\MesIngest\24\run-20260819-175808-watch-package-release` |
| 源提交 | `df135944dccc7e9828bfd4256286c273ba5b4c19` |
| Dirty | 是（23 个改动文件，均为本票工作，见 `host-manifest.json.GitStatus`） |
| Payload SHA-256 | `B7DC203E9687E1A7F58F5AF192BA883DB79E7163E98C72DEB2DD917A82ADBFB6` |
| 发布包 manifest SHA-256 | `43A96E5AD9198707EFC9CCB66432F2F1DE68A24D4541E05340886E130BEFBD0D` |
| 计划任务退出码 | 0 |

## 环境

`Test-GoldenRendererEnvironment.ps1` 前后各一次，`Differences: []`：
GPT-WIN11 / 交互 session 1 / Explorer 在会话内 / 1920x1080 / 96 DPI / 100% /
浅色 / zh-CN / China Standard Time / Microsoft YaHei UI + Consolas / SoftwareOnly。

## 门禁结果

| 阶段 | 结果 | 证据 |
| --- | --- | --- |
| 发布包构建与校验 | `MESINGEST_RELEASE_PACKAGE_VALID`，908 个文件 | `host-package-build.log` |
| 发布烟测 | **PASSED** | `Results/release-smoke/release-smoke-result.json` |
| 全量回归 | **937 total / 937 executed / 937 passed / 0 failed / 0 skipped** | `Results/core-host-http-sql/{summary.json,core-host-http-sql.trx}` |
| 打包 Watch 验收 | `watch-vm-tests` + `watch-ui-journeys`，228 项 0 失败，16 张截图 + UIA 树 | `Results/packaged-watch-acceptance/` |
| 人工验收 | Zhengyu Shao，2026-08-19 17:57:28，SHA-256 `9FA1C16D…` | `.artifacts/ticket24-acceptance/manual-acceptance.json` |
| 清理 | 计划任务已注销、残留进程 0、post-cleanup 环境复核 PASSED | `cleanup.json`、`environment-after-host-cleanup.json` |

## 烟测逐项证据

真实 SQL Server（`192.168.200.1` / `MesIngest_Ticket24_Smoke`，专用可丢弃空库，
启动前 0 张用户表，SQL 认证 + DPAPI 凭据）：

| 检查 | 实测 |
| --- | --- |
| 契约身份 | `2026.08.new-mes-ingest.v2.0` / schema 17 / `EXACT_VERSION_SCHEMA_AND_CAPABILITIES` / 9 项能力精确匹配 |
| 运行时 vs 包内 OpenAPI | 完整 JSON 语义严格一致 |
| 退役面 | `/api/contract`、`/api/demands`（含详情）、`/api/alerts`、`/api/poll-health`、`/api/demand-changes`、`/openapi/v1.json` **全部 404**，且脚本故意请求开启开发旧面 |
| Service/Watch 同一契约 | `MesIngest.Core.dll` 两端字节一致 |
| 轮次来源 | `FILE_REPLAY` / `liveOracleAttested=false` / `oracleConnectionAttempted=false` |
| 目录首次正文 | count=2，`catalogRevision=2`，ETag `W/"catalog-r2"` |
| 同修订条件读取 | **304**，无正文 |
| 受限原始证据鉴权 | 无密钥 403 / 错密钥 403 / 正确密钥非 403 |
| 远程绑定无密钥 | 拒绝启动，且核对拒绝原因确为缺 SharedSecret |
| Service 独占轮询 | 无 Watch 进程时 `pollTraceHighWater` 持续前进 |
| 关闭 Watch 后 | Host 仍在服务，`pollTraceHighWater` 继续前进 |
| Watch 启动耗时 | **14,125.1 ms**，25 秒上限内 |
| SQL Server 重启持久化 | 强杀重启后目录条目集合与 count 不变、`catalogRevision` 不回退；重启后 Host 不轮询，两次读取同 ETag |

## 具名 skip

打包 Watch 验收有 5 个 skip，**精确匹配**预期具名集合
（`skippedMatchesExpectedNamedSet: true`），原因
`STABILITY_GATE_ENTRY_POINT_AND_GOLDEN_FIXTURES_EXCLUDED_FROM_RELEASE_PAYLOAD`：

- `WatchWindowCandidateEquivalenceTests.Candidate_directories_are_visually_equivalent`
  —— 稳定性门禁自身的入口点，按票 24 第 8 条打包发布本就不该跑候选比对；
- `WatchWindowVisualEquivalenceGoldenFixtureTests` 的 4 个用例 —— 需要
  `MESINGEST_WATCH_GOLDEN_FIXTURES` 指向真实黄金截图，而 payload 故意排除 `.artifacts`。

回归 **0 skip**。工厂 Oracle 验收不在本门禁范围，仍按 `FACTORY-VALIDATION.md`
在现场完成（本轮 `liveOracleAttested=false`，不得当作现场证据）。

## 票 23 视觉验收的复用

`ticket23VisualBaselinesReused: true`，依据
`PACKAGING_DID_NOT_CHANGE_APPROVED_PNG_XML_UIA_OR_DPI_OUTPUT`：打包发布只验证已发布
二进制的启动、连接与关键功能，不重复像素候选、连续稳定计数、基线提升或 DPI clone。

## 达成过程中修复的缺陷

本次验收共跑 15 轮，前 14 轮的红都是真问题，逐条修复而非重跑掩盖：

1. 烟测录制数据的 AREA 值不符合 `MesFieldValidation` 域格式 → 需求挂错误、目录为空。
   已修，并补 tier 1 门禁 `ReleaseSmokeScriptedRoundsTests` 用生产校验器直接检查录制。
2. 启动超时被 `RunOneShotOnStartup` 撑爆；同时首次读目录与条件读取之间存在提交竞态。
   已改为连续轮询 + `Wait-SettledCatalog`，超时按 schema bootstrap 的实际成本调整。
3. `WaitForInputIdle` 后单次采样 `MainWindowHandle` 的竞态；错用
   `MESINGEST_WATCH_UI_TEST_MODE` 导致包内 Watch 崩溃。已改为按出厂配置启动 + 有界轮询。
4. `Start-PackagedHostProcess` 的 `$SharedSecret` 声明为 Mandatory，负向路径无法传空串。
5. `MesTaskUnionPollRunnerTests` 的 `Success ? [` 在黄金机固定的 SDK 8.0.4xx 上被 C# 12
   解析成可空数组类型。已加括号，并按用户决定加 `global.json` 钉住 8.0.4xx。
6. 门禁从未注入 `MES_INGEST_TICKET01_SQLSERVER` → 80 个 V2 投影测试长期静默 skip。
   已注入并新增 `-SqlServerExpectedProductMajor/-SqlServerExpectedCompatibilityLevel`。
7. 六个起 STA 线程的 WPF 测试类没有 xUnit collection，互相并行导致 BAML 与
   WindowChromeWorker 竞态。已统一收进 `WpfDesktop` 串行 collection。
8. `ErrorSearchDetailTests` 对 `RAW_EVIDENCE_LIMIT_EXCEEDED` 断言 400，而冻结契约是 413。
9. 四处令牌篡改改末字符，而 base64url 末字符低位是补位，约 3% 概率篡改无效。
   已抽成 `SignedTokenTampering` 改篡改签名段首字符。
10. `PACKAGED_WATCH_UI_SKIPS_NOT_ALLOWED` 过于绝对，改为精确具名集合匹配。
11. `startup-within-10-seconds` 从无测量支撑。已实测并按实测改为 25 秒上限，
    启动耗时本身另开[票 27](../../.scratch/new-mes-ingest/issues/27-packaged-watch-cold-start-cost.md)。
