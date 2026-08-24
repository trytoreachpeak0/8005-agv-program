# 23 — 播种墓碑并运行无删除切换门禁

**What to build:** 在一个没有删库能力的 MesIngestCutoverRun 中完成旧库墓碑播种、数量/哈希证明、三轮投影、API、目录和精确数据库身份门禁，并生成数据库外证据。

**Blocked by:** 21 — 完成 Watch 刷新与保护状态呈现.

**Status:** ready-for-agent

- [ ] 旧库读取严格只选择构造 ArchivedDemandKeyTombstone 所需的已归档键与最小身份事实。
- [ ] 不迁移当前投影、PollTrace、DemandRawObservation、DemandSeries 详细图、事件、错误历史或业务原文。
- [ ] 对规范化墓碑集合计算稳定数量和哈希，旧库导出、新库导入与复核使用同一算法和版本。
- [ ] 新库导入幂等，重复键不产生重复墓碑，冲突身份使整次播种失败。
- [ ] CutoverRunId 绑定所有门禁、结果、证据、旧/新数据库身份和 HistoryEpoch。
- [ ] 门禁证明旧 Host 已停止、旧库无业务连接、墓碑证明一致、新 contract/schema 精确匹配且连续三轮投影成功。
- [ ] 主要 Watch API、ExternallyReadableDemandCatalog 和 reference consumer 在同一运行中通过，新目录不含墓碑键。
- [ ] 精确旧库身份门禁验证显式名称、非系统库、非新库、预期旧 schema/contract 和解析后的 SQL 数据目录。
- [ ] 任一读取、播种或门禁失败都保留新旧库、失败退出、不后台重试且不生成删除授权。
- [ ] 在数据库外写不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志，不包含业务原文。
- [ ] 复用既有 cutover SQL 工具、发布包验证、Host/reference consumer fixtures 和 Ticket 15 墓碑模型；不建设通用迁移引擎或新的部署编排平台。
- [ ] 哈希的大集合与顺序无关性使用内存生成数据验证；真实 SQL Server 只使用不超过 20 个墓碑的旧/新库，覆盖成功路径和一个代表性失败路径。
- [ ] 其余冲突、连接、身份、目录和门禁拒绝分支使用确定性 dry-run/策略测试，不为每个拒绝条件重复启动整包或创建数据库。
- [ ] 开发期运行聚焦 cutover/tombstone/gate 测试，关闭时运行一次真实 SQL Server Tier 1；正常验证目标在 90 分钟内完成并保持 Failed: 0、Skipped: 0。
- [ ] 生产 Host 与本票运行身份均不具备删库权限；时间目标不能放宽无删除边界。
