# 完成双端联合测试并修复跨仓缺陷

Type: task
Mode: AFK
Status: claimed
Blocked by: 08, 09, 17

## Question

如何使用同一协议候选、精确两端 commit 和确定性环境执行 W2G-IS-00～07 全部 G3：正常端到端旅程、重复/乱序/延迟、不同内容冲突、断联安全收尾、进程崩溃重启、结果重放、RIoT UNKNOWN 对账和恢复分支，并把发现的问题修回责任仓库后重新跑受影响门禁？

开发期间每个切片应已进行候选联合运行；本票负责冻结前的完整回归和跨仓一致性收口。证据必须绑定 ProtocolReleaseIdentity 候选、IntegrationSliceId、双方 commit、配置哈希和测试结果，任何核心 FAIL/INCONCLUSIVE 都阻断发布候选。

## Progress

已用真实 `ControlServer_MVP@8fae66f65cde41d1b1c64a328661860ee16a481a`、真实 `OnboardHmi_MVP@398a957662cacb6c0f49ddd78da12d896a1469be`、协议候选 `72ddde595165468520d9f3a46b25e4aa4eec0c3f` 和 manifest `e878d89e820535fe1eb64b85681b9c2994fb98646309e6ba768219c5c8735f2e` 完成首次真实对真实联合运行。全新 ControlServer SQLite 迁移、八仓 HTTP IO Simulator、五步恢复、`READY`、Heartbeat/HeartbeatAck、`/health/ready` 及持久 session generation 均成功；另一次非空 pending-result 恢复正确得到 `RECOVERY_REQUIRED / PENDING_FACT_RECONCILIATION_REQUIRED`。

联合审计发现 Onboard 恢复报告的 checkpoint、`pendingResults` 和 `reasonCodes` 偏离候选 Schema，已修复并推送 `398a957`；Release 构建 0 warning/0 error，57/57 测试通过，修复后 W2G-IS-00～07 的 Onboard G2 已全部串行重跑 PASS，证据在产品仓库忽略目录 `artifacts/g2/issue10-398a957-post-fix/`。

正式 G3 仍被阻断，不能关闭本票：当前运行时双方发送 `ProtocolReleaseIdentity.tag = candidate-72ddde5`，不满足候选 Schema 的 `^protocol-v` 约束，而任何正式 tag/批准记录必须先由两名真实协议负责人解决票 16 的 manifest/批准闭环；ControlServer 生产 TCP 处理器目前只连接恢复快照和 Heartbeat，Demand/worklist/站点/批量操作/异常恢复命令尚未真实对真实分发；真实 RIoT、车辆、Map 和站点绑定也未提供，且路线图禁止用 RIoT 模拟器替代。

机器可读证据位于 `evidence/g3/20260825-local-candidate/`，绑定两端 commit、协议 manifest、配置哈希 `6adb5e67565221a8f13f7f4a55cf4867fe6f2a1e8aa4485da90901ff85421620` 和运行脚本哈希 `cd66a26ddaa6c629eec0fb82735804fd76b87651884d67c347e58ebed5f1063c`。W2G-IS-00～07 均如实记录为 `INCONCLUSIVE`；功能性 happy path 成功不被扩大为完整切片 G3 PASS。

### 2026-08-25 — 正式协议迁移与真实双进程 smoke

协议票 17 解决后，两端已迁移并远程推送到正式 `protocol-v0.1.0@3ad309ffd5f9a48a6cf390b51a81da2f47c814dd`、manifest `92c19e74affe876902e1c64aa5cdbca845f5dbc93a8c82014a16627a26deb8d3`：ControlServer 为 `ControlServer_MVP@02c2f3ca168f14d09f3fa1fc01b9654ff7e833ff`，OnboardHmi 为 `OnboardHmi_MVP@c41160c34c411f0f602f7c695e8c880ac6c19ae4`。迁移后两端完整 Release 测试分别 17/17 与 57/57 PASS；正式 manifest 下双方 W2G-IS-00～07 的 16 份 G2 结果全部 PASS，证据集合 SHA-256 为 `d576049c74eb424859f9ed622f7ec4905f8ae3f7884f13fbd2885195acc23ce9`。

真实 ControlServer Host、真实 Onboard 会话客户端和独立八仓 HTTP IO Simulator 已再次运行：空恢复到 `READY`，带 pending result 的恢复稳定到 `RECOVERY_REQUIRED / PENDING_FACT_RECONCILIATION_REQUIRED`，正式 release 身份、五步握手、心跳、健康端点和持久 session generation 均正确；测试后 58005/58006/58007 监听已回收。机器证据位于 ControlServer 忽略目录 `artifacts/g3/issue10-protocol-v0.1.0-02c2f3c-c41160c-smoke/run-result.json`，其 `runKind` 明确为 `REAL_PEER_SMOKE_NOT_G3`，不得把部分通过扩大为八切片 G3。

本票仍保持 `claimed`：当前终端可连通 RIoT `172.19.206.222:8888`，但没有 `CONTROL_SERVER_RIOT_CALL_API_KEY`；MesIngest `58004` 未运行且没有 `CONTROL_SERVER_MES_INGEST_SHARED_SECRET`；没有具名 `vehicleKey`、生命周期、`mapId`、机台与关卡 `stationId`；生产 TCP 仍未实现恢复/心跳以外的 Demand、worklist、站点操作和异常恢复命令分发。路线图禁止以猜测身份或 RIoT 模拟器替代这些前置，因此 W2G-IS-00～07 G3 继续为 `INCONCLUSIVE`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-25 — 用户重新指定 OnboardHmi 开发责任

用户明确要求 OnboardHmi 由其同事王昆开发，AI 只留下文档。后续本票不得再由 AI 修改 OnboardHmi 产品代码；`bc56fa9` 是王昆的初始基线，`2eeecf6`、`f265cd8`、`398a957`、`c41160c` 是使用当前 Git 身份提交的 AI 候选，不能归因为王昆本人开发或批准。已在 OnboardHmi 仓库新增 `docs/ONBOARD_DEVELOPER_HANDOFF.md`，将正式协议身份、八切片责任、现有候选范围、缺口、验证命令和人员接管记录交给王昆。完整 G3 必须等待其本人确认的 Onboard commit；本票继续保持 `claimed`。

用户进一步确认不保留 AI 产品候选作为当前实现。远程 `OnboardHmi_MVP@05bf9f4781828dcd4e63cbb7349e4cebd6a25a85` 已用可追溯 revert 恢复到王昆 `bc56fa9` 产品树，仅保留 README 与交接文档；基线 Release 构建 0 warning/0 error、48/48 单测 PASS。此前绑定 `398a957` 或 `c41160c` 的 Onboard G2/smoke 证据现在仅是历史红线资料，不得用于候选冻结或 G3。后续联合测试必须等待王昆的新实现 commit 和本人确认。

王昆的两项下一步工作已只以文档形式推送：`8005-agv-onboard-hmi/OnboardHmi_MVP@a6f05fb` 新增 `docs/WANG_KUN_FIRST_INTEGRATION_WORK_PACKAGE.md`，定义 HMI 第一次联调范围、代码入口、正式消息面、联调顺序与验收；`slots-simulator/main@d5ab183` 新增 `docs/EXTERNAL_AUTOMATION_CONTROL_API.md`，定义 Modbus 数据面与 loopback HTTP 环境/故障控制面、revision 并发规则和黑盒测试。两次提交均未修改产品代码或构建输入，后续实现等待王昆本人提交。

### 2026-08-26 — 王昆当前实现接入与恢复 smoke 收口

远程已出现王昆本人实现 `OnboardHmi_MVP@045514770da9858a8a49196dede276192e4f2a1b` 和 simulator `main@fb5f7c593742bf98bc3957b8729a38aad5321f28`；两端当前共同绑定经两名负责人批准并发布的 `protocol-v0.1.1@1531489e42e328f28bfe0c51ed3f8c56e5ce0279`、manifest `a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f`。外部批准证明重新下载哈希与 release 登记的 `89f67c…90cb` 一致。

王昆提交在无 CRLF 转换的干净 clone 中通过协议 G1、Release build、format、Unit 62/62、W2G G2 13/13、边界/UI 静态审计；simulator 核心 18/18 与 HTTP/Modbus 14/14 通过。ControlServer 修复后完整 18/18 测试、format 和 W2G-IS-00～07 八份 G2 全部通过。

真实 ControlServer + 真实 OnboardHmi + 独立 simulator 首次运行暴露确认哈希算法和 `SafetyStateSnapshot` ack kind 两项 ControlServer 偏差；已在远程 `ControlServer_MVP@3ceeee6dd243015b3f5fb94e9fea1d144dc4babf` 修复。修复后双方完成正式 release 会话、Capability、Safety 和 RecoveryStateReport，稳定得到 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`，不再出现 `CONTENT_HASH_MISMATCH`；所有监听均回收。详细证据见 [`2026-08-26 当前双端提交联合审计`](../evidence/g3/20260826-current-peer-audit.md)。

本票继续保持 `claimed`：OnboardHmi 尚未接入真实停稳/驻车 provider，ControlServer 尚无恢复/心跳以外的完整双向业务分发，且 MesIngest/RIoT 凭据及车辆、Map、站点身份仍缺失。W2G-IS-00～07 G3 继续为 `INCONCLUSIVE`，不得写 `## Answer` 或更新地图 Decisions so far。

### 2026-08-26 — ControlServer 车载业务入站持久链路

远程 `ControlServer_MVP@27d6dee858e6adac3bedd796ee9ba0789daefc1c` 已补齐王昆当前车载实现实际发送的 `SublotSubmitted`、`OperationProgress`、`OperationResult`、`PreDepartureSafetyCheckResult`、`SafetyStateChanged` 和 `SlotOperationCommandRejected` 入站路径：精确 wire SHA-256 的 `DurableAck` 与完整业务请求在同一 SQLite inbox 事务中提交；`OperationResult` 按 `slotOperationAttemptId + ForcedRecoveryGeneration` 防止同代换号/换内容，同时保留强制恢复后历史迟到结果与当前结果并存的既有语义；不安全 `SafetyStateChanged` 在确认后将会话 fail-close 到 `RECOVERY_REQUIRED / DEPARTURE_SAFETY_NOT_READY`。所有非握手消息现在也回读正式协议 envelope 身份。`SessionHello.credentialProof` 在 inbox 中固定写为 `[REDACTED]`，不把凭据明文落库。

新增 EF 迁移已在全新 SQLite 上依次通过初始迁移和 `DurableOnboardBusinessInbox`；Release 全解非增量构建 0 warning / 0 error、完整测试 20/20 PASS、format PASS。正式 `protocol-v0.1.1` 下 W2G-IS-00～07 八份 ControlServer G2 全部 PASS，均绑定上述 commit 和 manifest `a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f`；本机忽略目录 `artifacts/g2/issue10-27d6dee-pwsh/` 中八份 `gate-result.json` 的排序路径/文件哈希集合 SHA-256 为 `d5c2e7b4089a1cef6a4f49e5d644d10633abfb95f6b79a7a5bc908fc8a482f29`。首次误用 Windows PowerShell 5 时测试 3/3 已通过但 `utf8NoBOM` 证据写入失败，部分目录 `artifacts/g2/issue10-27d6dee/` 按红证据保留；正式八片证据使用 PowerShell 7 全新目录生成。

本票仍保持 `claimed`：本次只收口车载到服务端的持久入站链路，尚未实现 ControlServer 主动下发 journey/worklist、Sublot、SlotOperation、PreDepartureSafetyCheck 与恢复命令的生产编排；王昆端真实停稳/驻车 provider、MesIngest/RIoT 凭据及车辆、Map、站点身份也仍缺失。因此尚不能运行或宣称八切片真实 G3 PASS，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — ControlServer 主动旅程快照通道

远程 `ControlServer_MVP@746b02e3cd320b5574b92d25e133edf11b4fe265` 已补上真实服务端到车载的活动会话写通道和三类旅程投影发布器：`VehicleBusinessStateSnapshot`、`CurrentStopWorklistSnapshot`、`UpcomingStopPlanSnapshot`。会话只有在五步恢复返回 `READY` 后才暴露给业务发送端，安全状态 fail-close 后立即摘除；握手响应与主动业务消息共用串行写门，避免 NDJSON 交织。每个快照在网络发送前先以完整 wire JSON 写入 SQLite `ProtocolOutbox`，同一 `messageId` 的跨时间重试复用首次 `sentAt` 并逐字节重放，异内容稳定拒绝，已确认消息不再发送。

车载返回的 `SnapshotAppliedAck` 现在按 correlation、snapshot kind、原 wire SHA-256 和 projection revision 四项核对后才设置 `AcknowledgedAt`；双向 `DurableAck` 也已接入同一出站确认路径。Release 非增量全解构建 0 warning / 0 error，完整测试 23/23 PASS，format PASS。正式 `protocol-v0.1.1` 下受影响的 `W2G-IS-01` G2 5/5、`W2G-IS-06` G2 7/7 均绑定上述 commit PASS；本机忽略目录 `artifacts/g2/issue10-746b02e-is01/` 与 `issue10-746b02e-is06/` 两份 `gate-result.json` 的排序路径/文件哈希集合 SHA-256 为 `d68a4d932e2b302b7eed6de61ed9eefbbf8e57911c3150d10a1780711526b632`。

本票继续保持 `claimed`：本次建立了可被生产编排调用的旅程快照发送与确认基础，但尚未把 MesIngest Demand 接入自动受理、RIoT 到站事实和 worklist/plan revision 生成串成运行时编排，也未下发 `SublotEntryRequested`、`SlotOperationCommand`、`PreDepartureSafetyCheck` 或恢复命令。因此仍不能把此增量称为真实双端业务 G3；MesIngest/RIoT 凭据及车辆、Map、站点身份和王昆端真实停稳/驻车 provider 仍是后续门禁。

### 2026-08-26 — ControlServer 核心旅程命令可靠下发

远程 `ControlServer_MVP@cdaf34eb4763b6c30aa0369718bda880dce21d07` 已在既有活动会话/outbox 通道上补齐 `SublotEntryRequested`、`SlotOperationCommand` 与 `PreDepartureSafetyCheck` 三类核心旅程命令。服务端按正式 Schema 固定 Sublot 扫码/键盘录入方式与 revision 失效语义，强制 LOAD 使用关联 Sublot 消息且终态为 `OCCUPIED`、UNLOAD 不带 correlation 且终态为 `EMPTY`，校验 UUID、lowercase SHA-256、1～8 号仓位的有界唯一升序集合和安全版本。三类命令均在网络发送前写入 SQLite `ProtocolOutbox`，同一 `messageId` 同内容逐字节重放、异内容拒绝，并在精确 `DurableAck` 后停止发送。

Release 非增量全解构建 0 warning / 0 error，完整测试 26/26 PASS，format PASS。正式 `protocol-v0.1.1` 下受影响的 `W2G-IS-01`、`W2G-IS-02`、`W2G-IS-03`、`W2G-IS-04`、`W2G-IS-06` 五份 ControlServer G2 均绑定上述 commit 和 manifest `a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f` PASS；本机忽略目录 `artifacts/g2/issue10-cdaf34e-w2g-is-*/` 中五份 `gate-result.json` 的排序路径/文件哈希集合 SHA-256 为 `7f866b31e092b82fdc421bd6b263597244cd126956ce1d9a92c1e98db6e7d0eb`。

本票仍保持 `claimed`：新增的是可被生产编排调用的可靠命令发送面，尚未把 MesIngest Demand、RIoT 到站/移动事实和本地 journey 状态机串成自动业务编排，也未覆盖恢复命令族；真实 MesIngest/RIoT 凭据及车辆、Map、站点身份和王昆端真实停稳/驻车 provider 仍缺失。因此没有运行或宣称 W2G-IS-00～07 真实 G3 PASS，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 车载操作结果到服务端业务事实闭环

远程 `ControlServer_MVP@4dcd7b64bb5103a59e4cd5c4d17e8e33937d129f` 已修复命令发送与结果处理之间的生产断点。`SlotOperationCommand` 现在把完整仓位操作身份、操作类型、目标仓位集、ForcedRecoveryGeneration 和精确 wire 命令与 `ProtocolOutbox` 在同一 SQLite 事务中建立，数据库提交成功前不会向车载发送；新增迁移 `DurableOperationBusinessOutcome` 保存该操作类型及车载结果的内容哈希、结局、物理证据和观察时间。

ControlServer 收到 `OperationResult` 后会按王昆当前实现实际使用的业务内容序列重新计算并核验 `resultContentSha256`，再按 `slotOperationAttemptId + ForcedRecoveryGeneration` 持久去重。安全完整的 LOAD 结果提交整批 `OCCUPIED + LOCKED + RESET` 事实；安全完整的 UNLOAD 结果在返回 `DurableAck` 前原子提交 UnloadBatch、StopClosureCommit、Demand success 和 TransportDemandCompletion；不完整、失败或物理证据不安全的结果只持久化并把操作/Demand 转入 `RecoveryRequired`，不会误报完成；旧 ForcedRecoveryGeneration 的迟到结果继续只作历史证据。

SQLite 三段迁移已在全新临时数据库依次应用成功；Release 全量测试 28/28 PASS，锁定还原后的全解构建 0 warning / 0 error，format 与 `git diff --check` 通过。正式 `protocol-v0.1.1` 下受影响的 `W2G-IS-01`、`02`、`03`、`04`、`06`、`07` 六份 G2 均绑定上述 commit PASS；本机忽略目录 `artifacts/g2/issue10-4dcd7b6-w2g-is-*/` 中六份 `gate-result.json` 的排序路径/文件哈希集合 SHA-256 为 `a1944c0c2ea73e44007ee2055b1df6ee59d22d5563f5760eb3351a6018be48e4`。

本票继续保持 `claimed`：本次闭合了核心仓位命令到业务事实的可靠路径，但尚未把 MesIngest 自动受理、RIoT 两段移动/到站对账、worklist/plan revision、Sublot 输入和安全检查串成单一运行时旅程状态机，也未覆盖恢复命令族。真实 MesIngest/RIoT 凭据、具名车辆/Map/站点身份及王昆端真实停稳/驻车 provider 仍未提供，因此仍不能运行或宣称 W2G-IS-00～07 真实 G3 PASS，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — MesIngest 精确受理提交点与取货派发编排

远程 `ControlServer_MVP@dc8f915347253dc2b662c0394d4f8c437c7803da` 已把 MesIngest 完整目录事实接入受理提交点：HTTP 适配器现在读取并校验正式 V2 目录中的 `SeriesId`、TransportDemandKey、Generation、DemandRevision、CreatedAt、ValueObservedAt、PollTrace/ProjectionCommit 身份及全部 `LiveMesFields`，同时要求正文 HistoryEpoch/CatalogRevision 与 weak ETag 一致；新增 SQLite 迁移把这些不可变决定事实完整冻结在 `AcceptedDemands`，而不再只保存 DemandId、业务键和 revision。

新增生产 `JourneyIntakeCoordinator` 只接收已经完成硬准入的候选。它在任何 RIoT 副作用前执行无条件最终完整目录读取：无关候选造成 CatalogRevision 前进但目标决定元组不变时，原子提交最终 revision 下的 AcceptedDemandSnapshot 与 TO_PICKUP intent；HistoryEpoch 或任一决定事实漂移、候选消失时，保持数据库和 RIoT 零副作用。只有提交成功后才进入既有稳定 upperId 的对账／建单链路，建单响应仍须由独立 upperId 读取确认。

Release 全解非增量构建 0 warning / 0 error，完整测试 30/30 PASS，聚焦编排与 MesIngest 契约测试 6/6 PASS；全新临时 SQLite 已依次应用初始迁移、`DurableOnboardBusinessInbox`、`DurableOperationBusinessOutcome` 与 `ExactAcceptedDemandSnapshot`。正式 `protocol-v0.1.1` 下 `W2G-IS-01` G2 8/8 PASS，证据位于产品仓库忽略目录 `artifacts/g2/issue10-dc8f915-w2g-is-01/`，`gate-result.json` SHA-256 为 `5796b723d1579e3536280c201c8b6a0bb1fb743dfd73efa77862e6f8f9eddf30`；远程分支已回读到同一 commit。

本票继续保持 `claimed`：本次提供了可供运行时调用的精确受理与取货派发核心，但尚未实现目录 polling、完整硬准入/backlog/单车排他和配置映射，也未把取货到站、worklist/Sublot、装货、安全检查、TO_GATE 移动与卸货串成自动状态机。真实 MesIngest/RIoT 凭据、具名车辆/Map/站点身份及王昆端真实停稳/驻车 provider 仍未提供，因此没有运行或宣称 W2G-IS-00～07 真实 G3 PASS，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 单车单 Demand 持久排他占用

远程 `ControlServer_MVP@cc6e2b97e4308fa14b519edf9a0089d0da7d6d14` 已补上受理事务缺失的车辆排他事实。新的 `VehicleDispatchLease` 与完整 AcceptedDemandSnapshot、`TO_PICKUP` OrderIntent 在同一 SQLite 事务中提交；同一 `VehicleKey` 的未释放租约由数据库部分唯一索引硬性阻断第二个不同 Demand，即使不同 TransportDemandKey 也不能预绑忙车。只有完整安全卸货把 UnloadBatch、StopClosureCommit、Demand success 和 TransportDemandCompletion 原子提交时才释放租约；不安全结果、`RecoveryRequired`、RIoT UNKNOWN 和其它未收敛状态继续占住原 Demand 与车辆。

新增迁移会从上一版数据库的 AcceptedDemand 与 `TO_PICKUP` 意图回填租约：既有成功任务使用完成时间标记已释放，未收敛任务保持活动；如果历史数据库已经存在同车多项未收敛任务，唯一索引会令升级安全失败而不是猜测保留哪一项。聚焦租约／迁移测试 3/3、完整 Release 测试 32/32、format、`git diff --check` 和全解决方案构建 0 warning / 0 error 均通过。正式 `protocol-v0.1.1` 下受影响的 `W2G-IS-01` 10/10、`W2G-IS-04` 4/4、`W2G-IS-07` 3/3 G2 全部绑定上述 commit PASS；本机忽略目录 `artifacts/g2/issue10-cc6e2b9-w2g-is-*` 中三份 `gate-result.json` 的排序路径／文件哈希集合 SHA-256 为 `5e9955faea48bbcaaba6160d942d5ef249152ec05aa3fb9bcc47300c8bbaae60`。

本票继续保持 `claimed`：本次关闭的是受理层的单车排他安全空洞，尚未实现目录 polling、完整静态／动态硬准入与 backlog 排序，也未把取货到站、worklist/Sublot、装货、安全检查、TO_GATE 移动和卸货串成单一运行时旅程状态机。真实 MesIngest/RIoT 凭据、具名车辆/Map/站点身份及王昆端真实停稳/驻车 provider 仍缺失，因此仍不能运行或宣称 W2G-IS-00～07 真实 G3 PASS，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 启动阶段性 G3：正式双端恢复与不动车重连

已用真实 `ControlServer_MVP@cc6e2b97e4308fa14b519edf9a0089d0da7d6d14`、王昆当前 `OnboardHmi_MVP@045514770da9858a8a49196dede276192e4f2a1b`、`slots-simulator/main@fb5f7c593742bf98bc3957b8729a38aad5321f28` 和正式 `protocol-v0.1.1@1531489e42e328f28bfe0c51ed3f8c56e5ce0279` 启动 `W2G-IS-00`／`W2G-IS-06` 的不动车阶段性 G3。隔离运行使用全新 ControlServer SQLite、全新 Onboard journal 和临时 loopback 端口；没有 RIoT 建单、移动命令或伪造车辆安全信号。

最终有效运行依次完成全新首连、OnboardHmi 复用 journal 的进程重启、ControlServer 复用数据库的进程重启，session generation 稳定为 `1 → 2 → 3`；每阶段后续 12 秒未发生意外 generation 变化。三次均按真实缺失的停稳/驻车 provider 正确 fail-close 到 `RECOVERY_REQUIRED / DEPARTURE_SAFETY_NOT_READY`，`/health/ready` 为 HTTP 503，全部 stderr 为空。服务端重启期间 OnboardHmi 记录一次预期会话不可用并在 2 秒后自动重连；结束时的 transport warning 来自测试主动杀进程。机器结果 SHA-256 为 `fb0f708efb8cce42d1d64b728312f8a91775d6469918d28816057c08c3297304`，完整证据见 [`2026-08-26 阶段性 G3：真实双端、不动车`](../evidence/g3/20260826-staged-no-movement-cc6e2b9-0455147/SUMMARY.md)。

前两次启动器运行因证据收尾缺陷作废：一次在进程退出前读取锁定日志，一次把稳定快照写成 `null`；两次均未被提升为 PASS，修复后才以全新数据库/journal 第三次重跑。当前只宣称 `STAGED_G3_REAL_PEERS_NO_MOVEMENT` 通过，完整 IS-00 与 IS-06 仍为 `INCONCLUSIVE`：正式 TLS/具名生产身份、全部拒绝/冲突/恢复向量和业务消息 drop/delay/duplicate/异内容/首结果重放尚未覆盖。完整旅程仍受 ControlServer 自动编排、外部凭据与身份、以及真实停稳/驻车 provider 阻断。本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 阶段性 G3 红结果已路由至 OnboardHmi

Owning repository: `https://github.com/trytoreachpeak0/8005-agv-onboard-hmi`

Owner issue/artifact: [`RecoveryStateReport` 首 Ack 丢失红证据](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/blob/a1e32dd8960b11b2792f252837029d0a6f1dda90/evidence/g3/20260826-recovery-ack-drop-cc6e2b9-0455147/SUMMARY.md)

Published branch/commit: `OnboardHmi_MVP@a1e32dd8960b11b2792f252837029d0a6f1dda90`

Impact on this ticket: `FAIL_CROSS_REPOSITORY_RECOVERY_REPLAY` 继续阻断相关 G3 向量；本票保持 `claimed`，等待归属仓修复与新证据。

### 2026-08-26 — ControlServer 生产 Journey Worker

远程 `ControlServer_MVP@9c0d53091618d126a8c231004b4a7560d6e8daa0` 已交付默认禁用、完整配置才可启用的生产 Journey Worker。它用 .NET `BackgroundService`、Options 启动验证、scoped DI 和 EF SQLite 持久状态把 MesIngest polling、完整静态／动态硬准入、确定性 backlog、单车租约、`JourneyIntakeCoordinator`、RIoT 两段移动、可信到站、Onboard snapshot/worklist/Sublot、LOAD、发车安全、TO_GATE、UNLOAD 与四事实原子完成串成单一可重启旅程。跨进程继续复用原 Demand、车辆、两段 movement、操作和消息身份；缺失／陈旧／冲突证据以及旧库中没有 runtime 的未收敛 Demand 均 fail closed。

按 accepted ADR 新增服务端持久 StationTaskTypeAdmission：具名部署以单调版本事务导入并审计，同版本异内容或倒退拒绝；Sublot 提交时预检，LOAD 操作、outbox 与允许决策快照在同一事务中复检并冻结策略版本。SUBLOT_BOX_COUNT 只允许同源相对路径和新鲜、精确绑定 Sublot 的正数结果；RIoT 到站同时核对 state 5、orderId、冻结车辆/Map/目的站、IDLE/停稳/无任务占用与 Onboard 安全事实。

Release 全量测试 60/60、聚焦 Journey／准入／边界测试 32/32、format、全新 SQLite 七段迁移和全解决方案构建 0 warning / 0 error 均通过。正式 `protocol-v0.1.1` 下受影响的 `W2G-IS-01`、`02`、`03`、`04`、`06` 五份 G2 全部绑定上述 commit 与 manifest `a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f` PASS；五份 `gate-result.json` 的排序路径／文件哈希集合 SHA-256 为 `10062cb6e5b279477c70565e1baae37e7086e09f85778dd354a68333ccc591bb`。命令、逐片哈希、迁移证据和资格边界见 [`2026-08-26 ControlServer 生产 Journey Worker`](../evidence/controlserver/20260826-production-journey-worker.md)。

本票继续保持 `claimed`：本次只完成生产 Journey Worker；恢复／补偿命令、RIoT UNKNOWN 状态机 G2、ForcedRecoveryGeneration 与迟到结果策略仍留给下一项，阶段性 G3 runner 也未在本任务启动。真实 MesIngest/RIoT 凭据、具名生产身份、真实车辆动作和完整 G3/RC 均未获得资格，因此不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — ControlServer 恢复命令与持久状态机 G2

远程 `ControlServer_MVP@ea3050de8e813247706680517000000a5d387b50` 已完成本路线第 2 项。RIoT movement intent 现在在首次 create 前持久写入 `CREATE_ATTEMPTED`，重启后的 UNKNOWN／NotFound 只沿原 `upperId` 对账而不盲目重建；Active／Terminal 结果必须精确匹配冻结的 order、车辆、Map 和目的站身份，Terminal 也持久化。进程重启后从 SQLite 恢复同一 journey、Demand、车辆租约、两段 movement intent、slot operation 及 Onboard 消息身份；正式 `protocol-v0.1.1` 的恢复会话、恢复动作、resume、cancellation、compensation、correction、fault-cargo 和 forced-mechanical 命令均使用持久 inbox/outbox，未新增私有或占位协议。

`ForcedRecoveryGeneration` 现在单调推进并栅栏旧 generation 的未确认 outbox；旧代迟到结果仅进入历史证据，不能覆盖当前恢复决定。失败、不安全、歧义和未收敛结果继续占用原 Demand 与车辆，不会重复 RIoT 建单、重复 Onboard 命令、重复仓门副作用、释放租约或重复完成。恢复凭据只由环境变量引用，持久 inbox 固定写 `[REDACTED]`。全新 SQLite 直达最新迁移以及从 `VersionedStationTaskAdmission` 升级均通过，数据库证据 SHA-256 分别为 `4e562d9a230a7db7d6fca2cbc9278acd7c399fe502053bac1137478b6d642d03`、`ebbb49cd99bf91ec32096beb4af3ebe3aeaa57b086122a6d751e4adf963baab6`。

Release 完整测试 68/68 PASS（0 skipped），format、`git diff --check` 和全解决方案构建均通过，构建为 0 warning / 0 error。正式协议 `protocol-v0.1.1@1531489e42e328f28bfe0c51ed3f8c56e5ce0279`、manifest `a467c0c4b03cbf54fae985ceade256ff13225581babad7f46d90449b7f16389f` 下 W2G-IS-00～07 八份本端 G2 全部绑定 `ea3050d` PASS，合计执行 95 个按切片筛选的测试；机器证据在 ControlServer 忽略目录 `artifacts/g2/issue10-recovery-g2-ea3050d/`，索引 SHA-256 为 `e20f83bf4e14646fab9a2217f050fe396eac96579377c9911020c15157d47d9d`。高置信 secret 扫描为 0，58004／58005／58007 无监听，相关 ControlServer／Onboard／simulator／G2 进程为 0；ControlServer、OnboardHmi、protocol、simulator 工作区均清洁，ControlServer 远端已回读到同一提交。本任务未使用任何外部凭据，未真实建单或动车，也未修改受保护的 OnboardHmi、simulator 或协议仓。

第 2 项结论为完成，本票仍保持 `claimed`。剩余阻断仍包括真实 MesIngest／RIoT 凭据与具名车辆、Map、站点身份，王昆端真实停稳／驻车 provider 及其受保护仓库中的现有跨仓恢复重放阻断；本任务绝对未启动、设计实现或运行第 3 项阶段性 G3 runner，也不把本端 Fake／G2 证据表述为 G3 或 RC。第 3 项必须由主任务在本任务完整结束后另开新 chat；此处不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。
