# 01 — 建立 V2 四页产品壳与单 Host 会话闭环

**What to build:** 让现场实施与运维工程师从正式 MesIngestWatch 启动进入四页只读产品壳，并能安全应用一个 Host 配置、验证契约和查看最近轮询健康；任何 Host 切换都必须先使旧会话及其业务数据永久失效。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

- [ ] 启动默认进入“概览”，左侧导航固定提供“概览”“MES 任务 / TransportDemand”“IngestAlert”“设置”，不出现性能分析、诊断、遥测或生产操作入口。
- [ ] 设置页可输入并应用单个 Host 基址、掩码只读凭据和合法范围为 1–300 秒的请求超时；页面和日志均不得回显凭据。
- [ ] 应用新 Host 时先取消旧请求并使旧会话代次失效，清空四个业务视图的列表、详情、选择、查询、cursor、最后成功时间和旧错误，然后回到概览。
- [ ] 新会话先验证契约，再读取 PollHealth；鉴权失败、网络失败和契约不兼容均明确显示原因，且不得继续显示或读取旧 Host 业务数据。
- [ ] 一个集中只读查询模块统一承担鉴权、超时、correlation id、契约/HTTP/解码错误分类、取消和 DTO 映射；页面不得自行拼接认证头或解释 Host 错误体。
- [ ] 保留 MesIngest Core、Host 只读业务契约和 DemandChangeFeed 外部契约，不增加业务写接口，也不把 throwaway 原型直接提升为正式实现。
