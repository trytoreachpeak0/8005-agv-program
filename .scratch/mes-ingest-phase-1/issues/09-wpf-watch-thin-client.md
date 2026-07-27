# 09 — WPF 盯盘薄客户端

**What to build:** WPF 仅作只读 HTTP 客户端：展示/筛选/排序 VISIBLE 与 GONE、告警与最近轮询健康；查询失败与 PAUSED_ZERO_DROP 有醒目横幅；关闭窗口不停 Service；稍后启动可重连同一 API。

**Blocked by:** 03 — MES 数据质量诊断; 07 — Windows Service 持续单飞轮询

**Status:** ready-for-agent

- [ ] WPF 只调用与外部程序相同的只读 HTTP 契约，不直连 SQL Server
- [ ] 可按 TASK_TYPE、SUBLOT、status、last seen 筛选/排序需求列表
- [ ] 可查看告警与最近轮询健康（时间、耗时、行数、成功/失败）
- [ ] 查询失败与 PAUSED_ZERO_DROP 有醒目横幅，避免空板被误认为无任务
- [ ] 关闭 WPF 后 Windows Service 继续轮询并服务 API
- [ ] 稍后单独启动 WPF 可重连运行中 Service 并显示当前投影
