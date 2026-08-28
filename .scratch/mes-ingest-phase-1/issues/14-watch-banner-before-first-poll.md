# 14 — 首轮轮询前盯盘须有失败/未就绪横幅

**What to build:** Service 已起但尚未完成首轮成功轮询时，`GET /api/poll-health` 为 404、Watch 得到 null health，不得把空板当成「无任务」。须有醒目横幅（未就绪 / 尚无健康轮询），满足 Story 37。

**Blocked by:** None — can start immediately（09 已完成；本票为 review Spec A2 跟进）

**Status:** ready-for-human

- [x] Host 尚无 `LatestPollHealth` 时，Watch（或等价客户端）不把「demands 空 + health null」呈现为安静无工作状态
- [x] 横幅文案区分：HTTP 拉取失败 vs 尚无 poll-health（首轮前）vs 最近一轮失败（`Success: false`）
- [x] `WatchBannerState`（或等价）单测覆盖：health=null 且无 fetchError 时仍显示未就绪/失败类横幅
- [x] 不要求改变「首轮前 poll-health 404」的 Host 契约，除非产品另选 200+空体；若改 Host 须同步契约测试与 README

## Comments

- 2026-07-27: From `/code-review ffe1f49` Spec A2 (light) / Story 37. Evidence: `MesIngestApiClient.FetchPollHealthAsync` maps 404 → null; `WatchBannerState.From(null, null)` yields no fetch-failure banner → empty board looks like no work. Ticket 09 acceptance: 查询失败与 PAUSED_ZERO_DROP 有醒目横幅。
- 2026-07-27: Implemented — `WatchBannerState.From(null, null)` now shows not-ready banner; HTTP / not-ready / poll-failure copy distinguished; Host 404 contract unchanged.
