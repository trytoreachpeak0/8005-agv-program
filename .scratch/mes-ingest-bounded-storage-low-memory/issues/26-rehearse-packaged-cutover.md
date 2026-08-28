# 26 — 完成整包切换演练

**What to build:** 用实际发布包在隔离 SQL Server 实例中加速演练计划停机流程，证明 Host、Watch、reference consumer、墓碑、门禁、证据与精确旧库删除能作为一个产品运行，同时以实测步骤耗时判断现场能否落入 30–60 分钟窗口。

**Blocked by:** 25 — 只删除已证明的精确旧库.

**Status:** ready-for-human

- [x] 演练从可识别旧 contract/schema 和归档键的旧库开始，停止旧 Host 后创建独立新库与新 HistoryEpoch。
- [x] 只播种墓碑，启动精确新包并完成连续三轮成功投影，验证主要 Watch API、目录和 reference consumer。
- [x] 成功路径在全部门禁通过后删除隔离旧库、撤销临时权限，并留下数据库外证据与 Windows 事件。
- [x] 使用脚本化轮次和可控时间立即完成三轮投影及等待边界，不真实等待生产轮询间隔或停机窗口。
- [x] 一个代表性门禁失败演练证明新旧库保留、运行失败退出、没有后台重试或遗留删库权限；其它失败条件复用 Tickets 23/25 的确定性证据。
- [x] 记录每一步实际耗时并外推现场人工步骤，证明流程可在 30–60 分钟窗口内完成，失败处置和向前修复说明可操作。
- [x] 演练只使用隔离环境和测试数据，不连接或删除真实生产数据库，不把证据当作备份。
- [x] 发布包身份、contract/schema、HistoryEpoch、CutoverRunId、测试结果与所有 skip 被完整记录。
- [x] 不新建第二套演练编排；复用最终发布包和 cutover 入口，正常演练与一次真实 SQL Server Tier 1 的目标总时长在 60 分钟内。

## Comments

- 2026-08-25：复用最终发布包与既有 `Invoke-MesIngestCutoverRun.ps1` 完成隔离实库演练；未创建第二套生产编排。最终包来自 clean commit `0373531ba90cf0f5b525d84af505e3bf17f52afb`，`Release/win-x64`，manifest SHA-256 `15cb4db5c4d07cb85f61b03c28192f728ed15b484e9a44252d31454c675643fa`，1,372 files，contract/schema `2026.08.new-mes-ingest.v2.1/28`，Service/Watch contract bytes identical。cutover 在开始与删库前均复用 shipped `Test-PackageIdentity` 验证完整 bytes。
- 2026-08-25：本机默认真实 `LAB-WIN-01\MSSQLSERVER` 为 SQL Server `16.0.1190.2`、compatibility `160`、非 LocalDB。成功 RunId `83ef2385-a383-4777-a554-a519fcbfeac3`：旧库 `MesIngest_Ticket26_S_9502db75d61c4d808c3ac0c457ebf7dd_Old`，新库 `MesIngest_Ticket26_S_93174e1372f14dc2b916558a57e56436_New`，HistoryEpoch `1e2dd82d-55ad-48dd-b622-4b48fd55cd23`；11 gates 全过后只删除精确旧库，principal `REVOKED_AND_PRINCIPAL_DROPPED` / absent，新库在断言时保留，随后作为测试资源清理。
- 2026-08-25：失败 RunId `8ff96d54-591e-460b-845b-3a9ea653d7aa`：旧库 `MesIngest_Ticket26_F_b8c64334d89240898faddc40f7563452_Old`，新库 `MesIngest_Ticket26_F_6967b605aa31461f8d0a53e2ecc50f6b_New`，HistoryEpoch `5a6ce5bd-239f-46e4-9662-8dfb8026a19f`；`CUTOVER_HTTP_GATE_UNREACHABLE` 后观察五秒，两库保留、child 0、无后台重试、principal `NOT_GRANTED_AND_VERIFIED_ABSENT`，然后显式清理测试资源。最终数据库/login/process/task 残留均为 0，真实 MesIngest service 未触碰。
- 2026-08-25：实际最终包 Host 通过两个 OS-owned task 创建可识别旧库；删库门禁只接受 `Disabled`、`Enabled=false`、zero trigger/restart 的 task，精确解析 SQL `Initial Catalog`，三次绑定 executable/action hashes 并拒绝旧库 Host 进程。脚本化演练总计 `48.801s`；成功 `16.071s`，失败 `12.937s`，逐步耗时及人工 `40min` 外推见 `evidence/ticket26-packaged-cutover-2026-08-25/README.md`。现场仍需确认实例/路径/变更记录与 no-backup acknowledgement、填写本地 secret、停止真实旧 Host、人工审阅 pre-delete 证据并归档数据库外结果；失败只允许新 RunId 向前修复。
- 2026-08-25：focused package/gate tests `8 passed / 0 failed / 0 skipped`。最终 Tier 1 从 `mes/ingest/csharp` 显式连接上述 SQL Server 16/compatibility 160 执行一次：`887 passed / 0 failed / 0 skipped`，`4m44s`；TRX SHA-256 `f7d069b44a2657a3da07b27131f422413dd1245b8fa02b682654cc1759506a20`，887 个结果全 Passed。两轴最终 review：Standards Pass / 0 hard findings；Spec/Scope Pass / 0 functional findings / scope creep 0 / Ticket 27 implementation 0。本票未改 Watch UI，Tier 2/3 不适用且未运行。完整证据见 `evidence/ticket26-packaged-cutover-2026-08-25/`。
