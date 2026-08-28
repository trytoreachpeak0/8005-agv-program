# 02 — 建立正式 Watch UI 测试宿主与 fake Host

**What to build:** 让正式 MesIngestWatch 可以在确定性的本机 Windows 测试环境中由独立 UI 测试套件启动，并通过与生产相同的查询和浏览接口连接可编排的 fake Host，从第一张产品票起就能验证真实会话、取消和页面行为。

**Blocked by:** 01 — 建立 V2 四页产品壳与单 Host 会话闭环

**Status:** ready-for-agent

- [ ] 建立独立 xUnit v3 UI 测试项目，保留现有 xUnit v2 Core、Host、HTTP 和 Watch 非回归测试，不要求一次性迁移旧测试。
- [ ] 测试可启动正式 Watch 进程或正式窗口组合根，而不是复制一套绕过生产查询、取消、代次或原子提交规则的测试页面接口。
- [ ] fake Host adapter 可确定性控制契约、PollHealth、Demand、Alert、精确 Demand 查询、延迟、HTTP 错误、解码错误、cursor 失效和取消后的迟到响应。
- [ ] fake 数据、请求时间线、日志和测试输出不得含生产数据或明文凭据，并可按 Host 会话区分请求。
- [ ] 提供串行运行的最小本机测试入口；桌面会话不可用时明确报告环境不满足，而不是把环境失败报告成产品失败。
