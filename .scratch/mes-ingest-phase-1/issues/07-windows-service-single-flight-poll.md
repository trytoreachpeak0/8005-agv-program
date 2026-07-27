# 07 — Windows Service 持续单飞轮询

**What to build:** 正式 Windows Service 宿主持续轮询：同一时刻仅一轮在飞，本轮完成后再等待可配置延迟再开下一轮；本地可用文件快照源模式跑通 Service→SQL Server→HTTP；不开或关闭 WPF 时 Service 与只读 API 仍运行。

**Blocked by:** 06 — 重启恢复与首轮安全屏障

**Status:** ready-for-agent

- [ ] Windows Service 常驻承载 poll 循环与 Kestrel 只读 API
- [ ] 轮询为单飞：禁止并发、重叠或堆积查询
- [ ] 轮询采用完成后等待（默认 10s），延迟与查询超时可配置
- [ ] 文件快照源可作为本地/开发运行模式接入同一 poll 宿主
- [ ] 失败或不完整轮不创建新 VISIBLE、不累计消失，并产生接口告警
- [ ] 无 WPF 时 Service 仍轮询并服务 HTTP
- [ ] 可演示：改文件快照或等待多轮后，HTTP 投影随之更新
