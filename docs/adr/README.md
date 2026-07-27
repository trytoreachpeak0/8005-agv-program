# ADR Index

Architecture Decision Records for the whole repo. Cite as `ADR-<category>-<NNNN>` (e.g. `ADR-sdk-0005`, `ADR-cross-0001`, `ADR-mes-0002`).

## cross — 跨子系统

| ID | Title |
|---|---|
| [ADR-cross-0001](cross/0001-v1-facade-shaped-for-mes-dispatch.md) | 第一版 Facade 按 MES 派车闭环定形，Lab 共用 |
| [ADR-cross-0002](cross/0002-hang-continue-named-facade.md) | HangContinue 与 OrderContinue 分开具名封装 |

## sdk — RIoT SDK

| ID | Title |
|---|---|
| [ADR-sdk-0001](sdk/0001-default-auth-callapikey.md) | 第一版默认鉴权使用 CallApiKey |
| [ADR-sdk-0002](sdk/0002-v1-seam-session-named-methods-raw-escape.md) | RiotSession 具名方法为主，Raw 为逃逸舱 |
| [ADR-sdk-0003](sdk/0003-v1-facade-method-scope.md) | 第一版必须封装的 Facade 能力范围 |
| [ADR-sdk-0004](sdk/0004-v1-csharp-python-parity.md) | 第一版 C# 与 Python 同步交付 |
| [ADR-sdk-0005](sdk/0005-facade-throws-on-business-failure.md) | 具名 Facade 统一将业务失败转为 RiotApiException |
| [ADR-sdk-0006](sdk/0006-imap-via-kiota.md) | Map/Station 经 imap OpenAPI 纳入 Kiota 生成 |
| [ADR-sdk-0007](sdk/0007-ready-helpers-no-blocking-wait.md) | 可再派判定辅助，不内置阻塞 Wait |
| [ADR-sdk-0008](sdk/0008-v1-explicit-non-goals.md) | 第一版明确排除的能力 |

## mes — MES / 调度策略

| ID | Title |
|---|---|
| [ADR-mes-0001](mes/0001-queueing-stall-handling.md) | QueueingStall：预防 + 下单前清积压；超时只报警 |
| [ADR-mes-0002](mes/0002-order-hang-handling.md) | OrderHang：充电与普通分支分开 |
| [ADR-mes-0003](mes/0003-charging-hang-auto-reassign.md) | 充电 OrderHang 由 MES 自动改派 |
| [ADR-mes-0004](mes/0004-charge-hang-station-selection.md) | 充电改派选桩：允许集合内 NearStationQuery |
| [ADR-mes-0005](mes/0005-charge-hang-retry-limit.md) | 充电自动改充重试上限 N=2 |
| [ADR-mes-0006](mes/0006-mes-ingest-vs-dispatch.md) | MES 任务接入与调度拆开；第一期只交付接入投影 |
| [ADR-mes-0007](mes/0007-mes-ingest-tech-stack.md) | MesIngest 第一期：Service + WPF + SQL Server |
