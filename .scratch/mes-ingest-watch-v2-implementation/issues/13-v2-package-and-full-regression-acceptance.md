# 13 — 交付 V2 发布包并执行完整非回归验收

**What to build:** 基于已对齐并重新批准的 UI、Ticket 01–10 回归证据以及 Ticket 11/12 新基线，重新生成可发布交付物，并证明 V2 没有破坏既有 MesIngest 领域、Host 只读契约、外部同步能力或黄金视觉契约。

**Blocked by:** 12 — 完成 FlaUI 旅程、真实窗口基线与失败证据

**Status:** ready-for-human

**Golden renderer contract:** [`docs/agents/golden-renderer.md`](../../../docs/agents/golden-renderer.md)

- [x] Read `docs/agents/golden-renderer.md`.
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only; Ticket 12 approval remains valid because Ticket 13 does not change production UI pixels).
- [x] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI after the final approval-bearing release run.

**Rebuild decision (2026-08-09):** 本票不继承旧包或旧验收结论。只有 Ticket 11、12 的新证据闭环后才能开始；Prototype、旧冻结候选和未批准基线不得进入发布物。

- [x] 发布产物包含正式 V2 Watch、所需运行时依赖、配置样例和四套本机 Windows 验收入口；throwaway 原型、参考图假数据、旧冻结候选及测试 fake Host 不进入生产包。
- [x] 配置样例覆盖单 Host 基址、安全凭据注入方式、1–300 秒请求超时、连接日志保留和必要的本机偏好说明，不包含真实凭据。
- [x] 汇总 Ticket 11 的 Ticket 01–10 逐票回归证据、19 场景 XAML/PNG 新基线、Ticket 12 的五个真实窗口基线和 50 次稳定性结果；每项证据可追溯到源码、环境和运行日志。
- [ ] Core、Host、HTTP、SQL 条件测试、现有 Watch 非回归、独立 xUnit v3 UI 测试、Verify.Xaml 和 FlaUI 入口全部通过；任何跳过必须逐项说明并由用户批准，SQL 环境缺失不得默认为发布通过。
- [x] 运行时与离线 OpenAPI 保持一致，正式业务接口继续只有只读 GET；DemandChangeFeed、cursor、时间语义、Alert code 和 TransportDemand 投影不发生未版本化变化。
- [x] 在干净目录离线安装发布包，在黄金机从打包产物而非源码启动并重跑发布烟测，证明软件渲染、配置、日志、字体和本机偏好没有依赖开发目录。
- [ ] 人工验收确认启动约 10 秒内可判断连接、轮询、活动 IngestAlert 和 VISIBLE TransportDemand；Demand/Alert 页面与 D/E 视觉契约一致，全部 V2 页面与设置符合批准规格。
- [x] 发布清单明确记录 Ticket 11、12、13 均为 2026-08-09 重建版本，旧视觉证据不可作为本次发布签字依据。

## Comments

- 2026-08-09：用户要求在生产 UI 对齐选定设计、Ticket 01–10 回归以及 Ticket 11/12 新证据完成后重建本票。发布门禁不得把环境性跳过、旧基线或源码目录运行误写为完整验收。

- 2026-08-10：发布实现、包内容拒绝清单、完整 OpenAPI 对比、隔离偏好/日志烟测、四套包内 Watch 验收入口和逐文件 SHA-256 清单已实现。黄金机预审运行 `run-20260810-131320-watch-package-release` 从打包产物通过 83 个 VM 测试、20 个 Verify.Xaml 场景测试、5 个 FlaUI 旅程和 5 个窗口基线，全部 0 skip；该包因构建时源码 dirty 且早于最终 review 修复，只作诊断，不是发布签字包。

- 2026-08-10：Core/Host/HTTP 本机非回归为 499 passed / 0 failed，19 个 SQL Server 条件测试因既无 `MES_INGEST_SQLSERVER` 也无 LocalDB 而逐项跳过。门禁现在要求审批 JSON 的测试名与实际 skip 集合完全一致，且 UI 四套出现任何 skip 都失败；在用户逐项批准或提供 SQL Server 前不得勾选完整回归。人工发布验收同样必须提供四项确认 JSON。完整记录见 [`../evidence/ticket13-release-acceptance-2026-08-10.md`](../evidence/ticket13-release-acceptance-2026-08-10.md)。
