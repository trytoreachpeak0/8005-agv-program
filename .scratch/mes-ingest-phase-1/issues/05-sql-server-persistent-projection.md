# 05 — SQL Server 持久投影

**What to build:** 用 SQL Server 替换内存投影存储，TransportDemand、告警与轮询健康写入数据库；进程重启后通过同一只读 HTTP 仍可读回已投影数据。本票只证明存得住、读得回，不实现复杂重启屏障语义。

**Blocked by:** 02 — TransportDemand 出现、消失与再现生命周期; 03 — MES 数据质量诊断

**Status:** ready-for-agent

- [ ] TransportDemand（含 DemandId、冻结字段、VISIBLE/GONE、seen/消失元数据）持久化到 SQL Server
- [ ] 告警与最近轮询健康持久化，重启后 HTTP 仍可读取
- [ ] WPF/外部程序仍只经只读 HTTP 访问，不直连库作为正式契约
- [ ] 内存 store 仍可用于单元/契约测试；SQL Server adapter 有真实往返集成冒烟（环境可用时）
- [ ] 凭证与连接串仅在本地配置，不进仓库
