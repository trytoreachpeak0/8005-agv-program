# 02 — Watch HTTP Timeout、陈旧状态与本地连接事件账本

**What to build:** 参数化当前写死的 15 秒 HttpClient timeout，保留最后成功数据，按故障阶段记录 WatchConnectionEvent，并避免断线时每个刷新周期刷屏。

**Blocked by:** 01 — 统一时间契约

**Status:** ready-for-agent

- [ ] 新增 `Watch:RequestTimeoutSeconds`，默认 30，合法范围 1–300；支持 `MesIngestWatch__RequestTimeoutSeconds`
- [ ] 非法配置启动失败并指出配置键和值，不静默夹紧或回退
- [ ] 每个 `/api/demands`、`/api/alerts`、`/api/poll-health` 失败能指出 endpoint、阶段、耗时和 timeout
- [ ] 不做单次立即重试；继续 single-flight，由下一次定时刷新重试
- [ ] 任一失败时保留最后成功 snapshot，并计算 last-success/stale duration
- [ ] 首次失败、每 5 分钟持续摘要、恢复事件包含次数和持续时间
- [ ] JSONL 日志写入 `%LocalAppData%\MesIngest.Watch\logs\`，默认 30 天/100 MB，可配置并先到先清理
- [ ] 测试故障去重、恢复、Host 重启、日志轮转和敏感信息不落盘

## Comments

- Watch connection failures are local client evidence and must not be written back as Host IngestAlerts.

