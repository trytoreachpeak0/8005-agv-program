# 13 — 交付 V2 发布包并执行完整非回归验收

**What to build:** 基于已对齐并重新批准的 UI、Ticket 01–10 回归证据以及 Ticket 11/12 新基线，重新生成可发布交付物，并证明 V2 没有破坏既有 MesIngest 领域、Host 只读契约、外部同步能力或黄金视觉契约。

**Blocked by:** 12 — 完成 FlaUI 旅程、真实窗口基线与失败证据

**Status:** ready-for-agent

**Rebuild decision (2026-08-09):** 本票不继承旧包或旧验收结论。只有 Ticket 11、12 的新证据闭环后才能开始；Prototype、旧冻结候选和未批准基线不得进入发布物。

- [ ] 发布产物包含正式 V2 Watch、所需运行时依赖、配置样例和四套本机 Windows 验收入口；throwaway 原型、参考图假数据、旧冻结候选及测试 fake Host 不进入生产包。
- [ ] 配置样例覆盖单 Host 基址、安全凭据注入方式、1–300 秒请求超时、连接日志保留和必要的本机偏好说明，不包含真实凭据。
- [ ] 汇总 Ticket 11 的 Ticket 01–10 逐票回归证据、19 场景 XAML/PNG 新基线、Ticket 12 的五个真实窗口基线和 50 次稳定性结果；每项证据可追溯到源码、环境和运行日志。
- [ ] Core、Host、HTTP、SQL 条件测试、现有 Watch 非回归、独立 xUnit v3 UI 测试、Verify.Xaml 和 FlaUI 入口全部通过；任何跳过必须逐项说明并由用户批准，SQL 环境缺失不得默认为发布通过。
- [ ] 运行时与离线 OpenAPI 保持一致，正式业务接口继续只有只读 GET；DemandChangeFeed、cursor、时间语义、Alert code 和 TransportDemand 投影不发生未版本化变化。
- [ ] 在干净目录离线安装发布包，在黄金机从打包产物而非源码启动并重跑发布烟测，证明软件渲染、配置、日志、字体和本机偏好没有依赖开发目录。
- [ ] 人工验收确认启动约 10 秒内可判断连接、轮询、活动 IngestAlert 和 VISIBLE TransportDemand；Demand/Alert 页面与 D/E 视觉契约一致，全部 V2 页面与设置符合批准规格。
- [ ] 发布清单明确记录 Ticket 11、12、13 均为 2026-08-09 重建版本，旧视觉证据不可作为本次发布签字依据。

## Comments

- 2026-08-09：用户要求在生产 UI 对齐选定设计、Ticket 01–10 回归以及 Ticket 11/12 新证据完成后重建本票。发布门禁不得把环境性跳过、旧基线或源码目录运行误写为完整验收。
