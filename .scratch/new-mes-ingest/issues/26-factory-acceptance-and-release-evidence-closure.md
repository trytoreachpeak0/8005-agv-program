# 26 — 工厂验收与发布证据闭环

**What to build:** 使用最终空库切换发布包在工厂环境分别验证 Oracle 只读接入、SQL Server 持久化、Service 独立运行、版本化 API、目录条件读取和 Watch 六页，将可复核且脱敏的证据、具名 skip 和现场结论汇总为发布签字输入，而不把实验室或黄金机结果冒充工厂通过。

**Blocked by:** 25 — 删除旧模型并形成空库切换发布包

**Status:** ready-for-agent

- [ ] 记录最终发布包、源提交、配置模板、正式 MES_TASK_UNION 查询和目标环境身份的哈希或不可歧义版本，并证明现场使用的正是票 25 产物。
- [ ] 在真实 Oracle 11g 环境运行 Thin 模式只读探针，证明一次执行唯一正式六分支 UNION ALL 语句、列契约、命令超时、只读边界和凭据脱敏；现场确有需要时再以同一业务入口复验 Thick + Instant Client。
- [ ] 运行多个完整 MesTaskUnionRound 并记录 SUCCESS、FAILURE 或 INCOMPLETE 的 PollTrace、规范摘要、行数、查询版本和投影结果；任何失败或结构不完整轮次都不能伪造 Demand 消失或修改业务投影。
- [ ] 在现场兼容 SQL Server 上证明 ProjectionCommit 原子持久化、Service 重启后历史一致、RestartBarrier 边界、TaskTypeProtection、CatalogRevision 单调及读取快照不撕裂。
- [ ] 验证契约发现和鉴权、ExternallyReadableDemandCatalog 首次完整正文、同 Revision 的 304、主要 Series/资格/错误/当前关注/概览读取，以及远程绑定缺少或使用错误共享密钥时的数据访问保护。
- [ ] 在工厂交互桌面核验 Watch 的概览、需求系列、资格审计、错误检索、AREA 筛选、接入告警、设置与紧凑 Host 状态，确认契约匹配、自动刷新、失败保留、分页、详情和跨页下钻使用真实 Host 数据。
- [ ] 关闭 Watch 后继续观察 Service 完成轮询、写入 SQL Server 并提供 API，证明运维客户端不拥有轮询或业务投影生命周期。
- [ ] 工厂 Watch 核验用于证明最终包装与现场连接，不因 UI 输出未变化而重复票 23 的候选、10 次像素稳定、基线提升或 DPI clone；若现场发现实际 UI、UI Automation 或 DPI 回归，则保留失败证据并将对应场景退回票 23 的受影响门禁。
- [ ] 收集任务退出码、环境和时钟信息、Oracle/SQL/API/Watch 结果、必要截图或 UIA 证据、清理结果及脱敏证据哈希；不得包含凭据、客户敏感原始行或未获准的任意日志。
- [ ] 每个未执行、失败或受现场条件阻塞的检查都以具体名称、原因、责任方和 release gate 记录为 skip 或 red evidence；只有实际完成的项目才能进入现场通过结论。
- [ ] 形成可由发布负责人和现场人员复核的最终验收摘要，分别列明已通过、未通过、具名 skip、剩余风险和回退准备度。
