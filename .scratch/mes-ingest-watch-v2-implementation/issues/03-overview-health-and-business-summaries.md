# 03 — 完成概览健康结论与业务摘要

**What to build:** 让操作员在启动后约 10 秒内从概览判断 Host 是否可连接、最近 MesIngest 轮询是否健康、当前是否有活动 IngestAlert，以及当前页有哪些 VISIBLE TransportDemand。

**Blocked by:** 01 — 建立 V2 四页产品壳与单 Host 会话闭环; 02 — 建立正式 Watch UI 测试宿主与 fake Host

**Status:** done

- [x] 一次概览刷新并发读取 PollHealth、活动 IngestAlert 第一页和 VISIBLE TransportDemand 第一页，共享 Host 会话、请求代次与取消，但三个资源分别原子提交。
- [x] 概览明确区分连接失败、契约不兼容、尚无轮询、最近轮询失败、PausedZeroDrop、活动 ERROR、仅 WARNING、健康和部分失败，颜色之外同时使用文字或图标。
- [x] PollHealth 显示 outcome、endedAt、duration、最近 MES 快照 rowCount、failureStage 和暂停的 TASK_TYPE；rowCount 不得冒充当前 VISIBLE Demand 总数。
- [x] Alert 与 Demand 卡片在 `hasMore=false` 时显示精确 `0..100`，在 `hasMore=true` 时显示 `100+`；Demand 的 TASK_TYPE 汇总明确标注“当前页”。
- [x] 任一子请求失败时，其卡片保留自己的最后成功值和时间并标为陈旧；其它成功卡片可更新，整页标为“部分失败”而不是伪装成同一快照。
- [x] Alert 和 Demand 卡片可进入对应页面的默认查询，不为导航徽标额外启动后台刷新。

## Comments

- 2026-08-08: Implemented a dedicated overview session and projection, concurrent resource fetch with per-resource errors, four production overview cards, bounded counts/current-page TASK_TYPE summaries, stale retention, and default-query card navigation. Added query concurrency, state/projection, and formal composition-root UI tests.
