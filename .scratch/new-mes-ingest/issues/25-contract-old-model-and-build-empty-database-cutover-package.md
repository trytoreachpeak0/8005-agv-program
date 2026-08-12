# 25 — 删除旧模型并形成空库切换发布包

**What to build:** 在所有生产调用方都已迁到新版契约后收缩 expand 阶段的兼容脚手架，交付只认识新版 schema、领域语言、API 和 Watch 的完整发布包，并在一次性数据库上演练可审计的停机、备份、精确目标确认、旧库删除、新空库 bootstrap 与整套旧版回退。

**Blocked by:** 18 — Watch 单 Host 非视觉会话与刷新内核；19 — 生产 Fluent shell、设置与概览；20 — DemandSeries 生产页面；21 — 资格审计与 AREA Variant A 生产页面；22 — Error Search Variant A 与接入告警生产页面；23 — 共享黄金机 UI 集成验收与基线；24 — 迁移发布脚本、smoke 和验证说明

**Status:** ready-for-agent

- [ ] 删除旧 FrozenMesFieldSet/FieldDrift/ReappearAfterGone 语义、IngestAlert incident 生命周期、DemandChangeFeed、Feed Sequence、bootstrap high-watermark、SYNC_CURSOR_EXPIRED、旧 DTO/端点、旧配置和旧 schema 升级路径；领域、Host、Watch、OpenAPI、测试和文档不再引用这些契约。
- [ ] 最终 schema 只从空数据库建立新版 PollTrace、ProjectionCommit、DemandSeries、TransportDemand 世代、原始观测、事件、当前条件、错误期间、资格、当前关注和 CatalogRevision 所需结构，不迁移或推测旧业务历史。
- [ ] 运行时代码、Watch、常规安装和卸载逻辑绝不自动删除数据库；删除只存在于要求人工停机、备份和精确目标确认的受控切换演练。
- [ ] 在一次性目标数据库执行完整切换演练：停止旧 Host、Watch 和外部消费者，记录备份，核对精确实例和库名，删除旧库，由新 Host 建立空 schema，并以首个完整 SUCCESS bootstrap 可证明的新历史。
- [ ] 演练证明错误当前条件使用 BOOTSTRAPPED_CURRENT_CONDITION 而不伪造旧开始时间，旧 TransportDemand、IngestAlert 和 ChangeFeed 记录不会进入新库。
- [ ] 回退演练只通过停止新版并恢复整套旧程序、旧配置和独立旧数据库备份完成；新程序不得读取旧库，旧程序不得读取新库，也不宣称支持滚动或新旧混跑。
- [ ] 最终包包含 Service、Watch、唯一正式查询、空配置模板、安装与卸载脚本、版本化 OpenAPI 和新版验证说明，且通过真实兼容 SQL Server 的主要 seam、事务、重启、鉴权和打包回归。
- [ ] 票 23 的证据在最终包未改变视觉、XAML、UI Automation 或 DPI 输出时保持有效，本票只引用其冻结源和证据身份，不重复黄金机像素或 DPI 门禁；若本票引入相关输出变化，则标明失效场景并只重跑票 23 中受影响的预览、批准、稳定与清理要求。
- [ ] 自动化证明仓库和发布产物不再包含真实凭据、旧契约入口或能够对未确认实例执行 DROP 的无人值守路径，并保存切换与回退演练的目标身份、结果和清理证据。
