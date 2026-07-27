# 09 — WPF 盯盘薄客户端

**What to build:** WPF 仅作只读 HTTP 客户端：展示/筛选/排序 VISIBLE 与 GONE、告警与最近轮询健康；查询失败与 PAUSED_ZERO_DROP 有醒目横幅；关闭窗口不停 Service；稍后启动可重连同一 API。

**Blocked by:** 03 — MES 数据质量诊断; 07 — Windows Service 持续单飞轮询

**Status:** done

- [x] WPF 只调用与外部程序相同的只读 HTTP 契约，不直连 SQL Server
- [x] 可按 TASK_TYPE、SUBLOT、status、last seen 筛选/排序需求列表
- [x] 可查看告警与最近轮询健康（时间、耗时、行数、成功/失败）
- [x] 查询失败与 PAUSED_ZERO_DROP 有醒目横幅，避免空板被误认为无任务
- [x] 关闭 WPF 后 Windows Service 继续轮询并服务 API
- [x] 稍后单独启动 WPF 可重连运行中 Service 并显示当前投影

## Comments

- Added `MesIngest.Watch` (`net8.0-windows` WPF) as a separate process thin client against `GET /api/demands`, `/api/alerts`, `/api/poll-health`.
- Client-side filter/sort + banner derivation covered by light unit tests (`DemandListProjectorTests`, `WatchBannerStateTests`); no SQL / poll hosting in Watch.
- Default BaseUrl `http://127.0.0.1:5088`; override via `appsettings.json` or `MesIngestWatch__*` env vars.
- 2026-07-27: Post-review follow-ups → `14-watch-banner-before-first-poll` (404 poll-health before first round → empty board); `16-watch-env-config-binding` (env prefix does not bind into `Watch` section).
