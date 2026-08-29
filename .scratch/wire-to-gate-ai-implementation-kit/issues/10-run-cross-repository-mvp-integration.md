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

### 2026-08-26 — 第 3 项确定性阶段性 G3 runner 路由指针

第 3 项的唯一 source of truth 已按用户指定落在 `8005-agv-control-server`：runner／产品修复提交 `ControlServer_MVP@b4afdb3ce3d6ee2b84b78b09101af689f1cbde92`，正式证据提交 `ControlServer_MVP@8952603bffd9ff63858881fc8d38f8acf2c75d8a`，摘要为 [`Deterministic staged G3 split-transport result`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/8952603bffd9ff63858881fc8d38f8acf2c75d8a/evidence/g3/20260826-staged-g3-b4afdb3/SUMMARY.md)。TLS `SslStream` 身份／重复／冲突探针及 plaintext loopback 的真实 Onboard `RecoveryStateReport` 首 Ack drop 重放均 PASS；真实 Onboard+TLS 组合因没有受支持的已信任 loopback 证书而保持 `INCONCLUSIVE`，正式切片、完整 G3 和 RC 均未宣称 PASS。

本票继续保持 `claimed`；此处仅保留路由指针，不复制跨仓证据，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 阶段性 G3 恢复重放修复重跑指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Recovery replay fix staged G3 rerun`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/8f2d03752cdb592dcbd118523fbf82b49dd3c904/evidence/g3/20260826-staged-g3-rerun-8952603-15c6387/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@8f2d03752cdb592dcbd118523fbf82b49dd3c904`

Impact on this ticket: 先前 `RecoveryStateReport` 首 Ack 丢失跨 generation 重放阻断已用真实双端重跑 PASS；真实 Onboard+TLS 组合、W2G-IS-00～07 完整 G3 与 RC 仍为 `INCONCLUSIVE`，本票继续 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 真实 Onboard + TLS 信任授权边界

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Staged G3 real-Onboard TLS trust authorization boundary`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/ca2c20d1530af27ead98fc1dcab2cf39226e886e/evidence/g3/20260826-staged-g3-tls-rerun-87d539b-15c6387/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@ca2c20d1530af27ead98fc1dcab2cf39226e886e`

Impact on this ticket: runner 已实现真实 Onboard 经 TLS fault proxy 到 TLS ControlServer 的同一首 Ack 丢失重放向量，并改为只有显式 `-InstallTemporaryCurrentUserRoot` 才安装唯一测试根、记录指纹并在 `finally` 精确删除；Windows 在写入 `CurrentUser/Root` 前显示 Security Warning，本轮没有用户系统信任授权，故主动中止且核验根证书、端口和产品进程均未残留。不改 Root 的 `CurrentUser/TrustedPeople` 直接叶证书方案实测仍为 `UntrustedRoot`。同时当前终端三个所需凭据变量均未设置，MesIngest `127.0.0.1:58004` 与 RIoT `172.19.206.222:8888` 不可达，车辆／Map／取货站／关卡站配置仍为空占位。真实 Onboard+TLS、完整 W2G-IS-00～07 G3 与 RC 继续 `INCONCLUSIVE`；本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 真实 Onboard + TLS 恢复重放 PASS

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Deterministic real-Onboard TLS recovery replay result`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/264e98bbad7d39e0069710f6e2d7e8dc47d97a5d/evidence/g3/20260826-staged-g3-tls-final-696ee75-15c6387/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@264e98bbad7d39e0069710f6e2d7e8dc47d97a5d`

Impact on this ticket: 用户明确授权的唯一临时测试根已用于真实 Onboard → TLS fault proxy → TLS ControlServer 联合运行。generation 1 的 `RecoveryStateReport` 首 `DurableAck` 被丢弃并断开 TLS，generation 2 在新 TLS 连接上以同一 message ID 和同一业务 payload SHA-256 重放并成功接收 Ack，最终稳定到 `RecoveryRequired / CAPABILITY_SNAPSHOT_REQUIRED`。协议 G1、release/manifest/credential 拒绝、同 ID 同内容字节级重放、异内容稳定冲突、无移动副作用和 secret scan 全部 PASS；结果为 `STAGED_G3_TLS_RECOVERY_REPLAY_PASS`，`run-result.json` SHA-256 为 `5647b661223c9ed11f6363c143567614942f52bef4e4e3a768fc28a433290068`。机器证据确认 `temporaryTrustCleanupVerified=true`，运行后根证书、PFX、端口和产品进程均未残留。该向量的不确定性已关闭，但 `formalSlicePass=false`；缺少现场凭据、服务连通性和具名车辆／Map／站点身份使正式 W2G-IS-00～07、完整 G3 与 RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-26 — 正式 G3 现场门禁复核

当前终端重新核对了生产配置实际引用的秘密名称及 Process／User／Machine 三层环境：`CONTROL_SERVER_RIOT_CALL_API_KEY`、`CONTROL_SERVER_MES_INGEST_SHARED_SECRET`、`CONTROL_SERVER_ONBOARD_CREDENTIAL` 和 `CONTROL_SERVER_RECOVERY_AUTHENTICATION_PROOF` 均未配置；ControlServer 工作区内也没有可复用的本地安全引用文件。`172.19.206.222:8888` 的 RIoT TCP 已恢复可达，但 `127.0.0.1:58004` 的 MesIngest 仍未监听。具名 `agvId`／`vehicleKey`／生命周期 generation、`mapId`／map identity、取货站和关卡站双重身份及准入／路线配置仍未提供。

因此当前可安全执行的无移动 TLS 恢复重放已经完成，下一步必须由现场负责人通过安全通道注入上述秘密并确认具名身份／站点映射，同时启动真实 MesIngest；仅有 RIoT 端口可达不授权 API 调用或车辆动作。不得生成猜测身份、把测试随机 secret 当作现场凭据，或用 RIoT Fake 替代正式 G3。本票继续保持 `claimed`，正式 W2G-IS-00～07、完整 G3 与 RC 仍为 `INCONCLUSIVE`；不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — Map 25 动态机台站解析与现场身份接入指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Owner implementation: [`Dynamic Map pickup station resolution`](https://github.com/trytoreachpeak0/8005-agv-control-server/commit/69dede3b04472cfdb8de06b7d4f743e4677eeb6e)

Published branch/commit: `ControlServer_MVP@69dede3b04472cfdb8de06b7d4f743e4677eeb6e`

Impact on this ticket: ControlServer 已按已批准 REQ-0298／0321／0322／0324 使用获准的 Map Station 全量读取面，在 Map 25 按一至三个 AREA 编码命名规则解析机台站；每个 WIRE_TO_GATE Demand 以自身 AREA/EQP 唯一解析并冻结一个 pickup，零／多站或同 AREA 多 EQP 均 fail-closed，普通公共站点不误判，关卡精确绑定为 `关卡/210`。现场车辆冻结为 `老厂前线新多仓位1`、`BROKERX-0c20ff0600d644869a6a80c186065d85`、首次生命周期代次 `1`；MesIngest 更新到本机 `5088` 的 v2.2/schema 29 且 loopback 不强制 SharedSecret。完整 Release build 0 warning/0 error、82/82 tests PASS（0 skipped），四项高风险伪变异最终全部被测试捕获。真实 Map station 列表、RIoT 车辆/mapIdentity 回读仍需 CallApiKey；Onboard 具名凭据／真实 provider、完整现场配置和真实车辆动作授权仍未满足，故正式 W2G-IS-00～07、完整 G3 与 RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — Map 25 只读现场回验与 CallApiKey 持久化指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Map 25 read-only identity and station readiness`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/e4dd411387cb8f6198e6a36b45b4c7992fc8cf1d/evidence/g3/20260827-map25-readiness/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@e4dd411387cb8f6198e6a36b45b4c7992fc8cf1d`

Impact on this ticket: 获准的只读 RIoT 调用已精确回验车辆 key、`mapIdentity=老厂前线new`、Map 25 共 206 个 Station 及唯一 `关卡/210`；当前 MesIngest 17 个 WIRE_TO_GATE AREA/EQP 中 10 个唯一匹配、7 个无匹配、0 个歧义，缺失项继续 fail-closed。CallApiKey 已按部署负责人明确要求持久化到 Windows User 范围的 `CONTROL_SERVER_RIOT_CALL_API_KEY`，正文未进入 Git；本次没有创建 RIoT 订单或移动车辆。该配置增量 Release build 0 warning/0 error、82/82 tests PASS（0 skipped）。七个缺失 AREA、Onboard 凭据／真实停稳驻车 provider、电量阈值、容量规则和 SUBLOT_BOX_COUNT 仍阻断完整现场 G3，故本票继续 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — SUBLOT_BOX_COUNT 本地实现与发布历史阻塞指针

MesIngest owning worktree 已在本地 `codex/map25-sublot-box-count@cbf5717406db39b3182beac4233fa1fdb45b7406` 实现 v2.3/schema 29 的 hash-pinned、单绑定变量 `GET /api/v2/sublot-box-count`，并同步 OpenAPI、发布包／manifest／smoke／factory 验收和源仓证据。定向 Release 验证为 150 passed、0 failed、1 个外部 SQL 环境 skip；最终 Tier 1 为 806 passed、2 个未改动 WPF 视觉布局失败、133 个外部 SQL 环境 skip。ControlServer 消费端本地 `ControlServer_MVP@74b937c42dbe8b26c9d60d0332f5926622ba043e` 已固定精确 v2.3 capability id+version 集及路径，Release 完整测试 83/83 PASS。

用户已明确允许发布 MesIngest 分支及其 60 个既有未发布祖先。生产者已推送并远端回读为 `codex/map25-sublot-box-count@cbf5717406db39b3182beac4233fa1fdb45b7406`，随后消费者已推送并远端回读为 `ControlServer_MVP@74b937c42dbe8b26c9d60d0332f5926622ba043e`。完整证据保留在各 owning repository，本票只记录路由和阻塞。现场 MesIngest 仍为 v2.2，尚未部署 v2.3；七个 AREA、阈值／容量、Onboard 凭据与真实停稳驻车 provider、以及移动授权仍未闭合，因此本票继续 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — MesIngest v2.2→v2.3 身份迁移修复与管理员部署阻塞指针

Owning repository: `https://github.com/trytoreachpeak0/8005---AGV`

Owner evidence: `mes/ingest/evidence/g3/20260827-map25-sublot-box-count/SUMMARY.md`

Published branch/commit: `codex/map25-sublot-box-count@1d95e36395b162da9f033e514e12c967493dd12d`

Impact on this ticket: 首次 Host-only 部署暴露现场 SQL schema identity 仍为 v2.2，v2.3 按 51008 fail-closed 且未改库；归属仓已发布只允许完整结构匹配的 v2.2/schema 29 在 serializable 事务中单步更新 identity 的修复，真实 SQL schema 门禁 20/20、Release build 0 warning/0 error、Tier 1 808 passed/0 failed/136 external-SQL skips。后续 UAC 在管理员脚本执行前被取消，正式 Windows Service 当前停止，精确 `ea778a0` 重建的临时当前用户 v2.2 Host 正在 `127.0.0.1:5088` 提供只读服务；须以管理员身份重新进入 Codex 后部署已验证的 `1d95e363` Host-only 包。未调用 RIoT mutation、未动车；正式 W2G-IS-00～07 G3 与 RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — MesIngest v2.3 正式服务部署与 SUBLOT_BOX_COUNT 只读现场 PASS 指针

Owning repository: `https://github.com/trytoreachpeak0/8005---AGV`

Owner evidence: [`Map 25 SUBLOT_BOX_COUNT contract readiness`](https://github.com/trytoreachpeak0/8005---AGV/blob/abb84d2aef1fdba0da15392f58f75ea957e0584d/mes/ingest/evidence/g3/20260827-map25-sublot-box-count/SUMMARY.md)

Published product/evidence: `codex/map25-sublot-box-count@c362b37950185fbff64a067b7a834521257a130d` / `abb84d2aef1fdba0da15392f58f75ea957e0584d`

Impact on this ticket: 用户明确授权不备份 Host 和 SQL Server 的直接发布后，正式 `MesIngest` Windows Service 已用管理员权限部署到产品提交 `c362b379`，当前为 `Running`、`Auto`、`LocalSystem`；现场 SQL identity 为 v2.3/schema 29，历史 epoch、32-byte signing key 和 `NOT_REQUIRED` reset 状态保持有效。首次真实 Oracle 补充读取暴露并 fail-closed 为 ODP.NET `ORA-00911`，归属仓随后移除 canonical SQL 客户端语句终止符、把全部发布面锁定到 SHA-256 `9aaee872...a24`，新增 Thin／Thick 回归，并以最终 Tier 1 `808 passed / 0 failed / 136 external-SQL skips` 收口。现场从当前目录选取一个已脱敏 WIRE_TO_GATE Sublot 的只读调用已返回精确 `SUBLOT_BOX_COUNT` identity、正数 `maxBoxCount=4` 和 UTC 时间，空 Sublot 返回 HTTP 400；未调用 RIoT、未建单、未动车。

该增量只关闭 MesIngest／SUBLOT_BOX_COUNT 可部署前置项。七个 AREA/EQP 站点映射、电量阈值、获批容量配置、Onboard 具名凭据与真实停稳／驻车 provider，以及任何车辆动作授权仍未闭合；正式 W2G-IS-00～07 G3 与 RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — MesIngest v2.3 部署后现场门禁动态复核指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Map 25 field-gate snapshot after MesIngest v2.3 deployment`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/8dfd94eb6a60353ff21c003ebbe0b6e393fb1139/evidence/g3/20260827-map25-field-gates-post-v23/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@8dfd94eb6a60353ff21c003ebbe0b6e393fb1139`

Impact on this ticket: 只读复核确认 MesIngest v2.3／schema 29 与 `SUBLOT_BOX_COUNT` 保持在线，Map 25 仍为 206 个 Station、唯一 `关卡/210` 且无 AREA 歧义；但 MesIngest 当前目录在观察期间由 revision 1260 的 25 个 WIRE_TO_GATE AREA/EQP 变为 revision 1262 的 15 个，稳定短采样下有 8 个无匹配项，证明旧“七个缺失项”不是可冻结的静态清单，正式运行前必须原子重读并冻结 Map 与 MES 目录。权威需求没有给出可推断的电量数值或 PACKAGE 容量值，当前 11 种 PACKAGE 仍需具名负责人批准；受保护 Onboard 远端 `15c6387` 仍使用 fail-closed 的不可用车辆安全 provider，具名凭据也未配置。本次未调用 RIoT mutation、未建单、未动车；本票继续 `claimed`，正式 W2G-IS-00～07 G3 与 RC 仍为 `INCONCLUSIVE`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — AREA／电量／PACKAGE 与停稳投影门禁实现指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Map 25 capacity and vehicle-safety field-gate implementation`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/f9cad35551e7ccd44a489b7324fd3e53243d1f2d/evidence/g3/20260827-map25-capacity-safety-gates/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@f9cad35551e7ccd44a489b7324fd3e53243d1f2d`

Impact on this ticket: 用户逐项确认的 `N* + Map25` 双条件、30% 电量阈值、28 条初始 PACKAGE 容量规则、ControlServer 本地缺失 PACKAGE 去重／补数历史和 RIoT Round-41 fail-closed 停稳投影均已在归属仓实现并以 Release 101/101 tests PASS、九段 SQLite 迁移 PASS 收口；Machine-scope 具名凭据已验证存在但未披露值。受保护 Onboard 远端当前 HEAD 为王昆 `15c6387801fa2154fb69441eac460fea9d0999c5`，已包含恢复跨代次重放修复，但该精确 HEAD 的 `App.xaml.cs` 仍绑定 `UnavailableVehicleSafetySignalProvider`；须由王昆提交正式 HTTPS／证书信任客户端 provider 并确认新的精确 commit。当前 `MT_NA` 继续只能判 `UNKNOWN`，动态状态资格验证仍需单独动车授权。本票保持 `claimed`，正式 W2G-IS-00～07 G3 与 RC 仍为 `INCONCLUSIVE`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — ControlServer 分阶段部署与测试端点确认

用户确认先在当前本机部署 ControlServer，稳定后再迁移到另一台目标机器；Onboard 测试阶段也运行在当前本机，后续迁移到车辆触控屏 `172.19.162.210`。测试阶段 Onboard-facing HTTPS 端点冻结为 `https://localhost:58007`，证书至少包含 `localhost` SAN；`172.19.162.210` 是后续 Onboard 客户端地址，不是当前 ControlServer 服务端地址。最终 ControlServer 迁移时必须重新确认其服务端 DNS／IP 并据此签发或更换证书，不能沿用仅覆盖 `localhost` 的测试证书。该确认不构成部署、证书安装、RIoT 调用、订单创建或车辆移动授权；本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

用户进一步确认没有企业／内部 CA，并明确授权采用专用开发证书方案：创建仅用于本机测试的私有测试根和带 `localhost` SAN 的服务端叶证书，将测试根安装到当前 Windows 用户的受信任根存储，保持正常 TLS 验证，不使用证书绕过；ControlServer 迁移到最终机器时移除或替换该测试信任。证书生成和安装须在服务身份确认后执行，以便先冻结私钥位置、ACL 和读取主体；不得把私钥、PFX 密码或其他秘密写入 Git、日志或证据。

用户确认当前本机测试部署的 ControlServer Windows Service 使用 `LocalSystem`。该选择只冻结服务身份，不授权读取、复制或迁移当前 User-scope 的 `CONTROL_SERVER_RIOT_CALL_API_KEY`；LocalSystem 所需的 RIoT 秘密注入仍须单独明确授权。证书私钥与配置文件 ACL 应只授予 `SYSTEM`、Administrators 和部署所需主体，最终换机时重新评估服务身份。

用户随后明确授权：仅在获批的 ControlServer 部署期间，将现有 User-scope `CONTROL_SERVER_RIOT_CALL_API_KEY` 的原值复制到 Windows Machine scope，保留原 User-scope 值不变，使 `LocalSystem` 可读取。执行期间不得打印、哈希、记录、复制到 Git／发布物／日志／证据或通过聊天披露密钥正文；该授权不包含任何 RIoT API mutation、建单或车辆移动。

### 2026-08-27 — 本机 ControlServer 部署与 Schannel 修复指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Local ControlServer Windows Service deployment`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/4b136c1ea44f4fa4077db3080c3a0df2112dc0e4/evidence/g3/20260827-local-controlserver-deployment/SUMMARY.md)

Published product/installer/evidence: `ControlServer_MVP@1f14e7436423c6dae5c0dc1fdfabc0cfbb7c3799` / `160a6c86ef1098927926a86ee05cf7e595eb447e` / `4b136c1ea44f4fa4077db3080c3a0df2112dc0e4`

Impact on this ticket: 用户明确授权的 `localhost:58007`／专用开发根／`LocalSystem`／User→Machine RIoT 秘密复制本机部署已通过一次性最高权限任务完成，任务结束后已删除。真实 Kestrel 握手暴露并修复 Windows Schannel 不支持 ephemeral server key 的产品缺陷；聚焦握手测试 1/1、Release build 0 warning/0 error、完整 101/101 tests PASS。自包含包 manifest SHA-256 为 `0895f279e9a6a17e81725ed26f1037eb4b20f79a7706a03a3e874ec88a851cb0`，部署结果 SHA-256 为 `c321f7324727edb01ef7abd84b125daca02a86fe195fafa5ca763c0c9d7cc6c8`。独立回读确认服务 `Running`／`Auto`／`LocalSystem`、58005 TLS 与 58007 HTTPS 由同一服务监听、live/version 通过正式信任链、精确开发根与三项外部秘密引用存在、SQLite 受 ACL 保护；`JourneyRuntime` 保持关闭，未调用 RIoT mutation、未建单、未动车。该结果只关闭本机安装／启动／停止／重启／HTTPS 信任前置项；王昆 Onboard provider、凭据安全交付、无移动现场 preflight、正式 G3 与 RC 仍为 `INCONCLUSIVE`，本票继续 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

用户确认 Onboard credential 采用本机直接注入方案：测试阶段沿用当前机器既有的 Machine-scope `CONTROL_SERVER_ONBOARD_CREDENTIAL`；Onboard 迁移到车辆触控屏 `172.19.162.210` 时，只由用户或现场管理员在触控屏本机直接写入同名 Machine-scope 环境变量，不通过聊天、Git、日志、证据或向王昆传递明文。该确认不授权当前会话连接／修改车载触控屏，也不授权 RIoT mutation、建单或动车。

### 2026-08-27 — 本机可回滚升级与 Map 25 无移动预检指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Local ControlServer upgrade and Map 25 read-only preflight`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/ab8aab684ae9319cb29af60af3d4afa223f11b64/evidence/g3/20260827-local-upgrade-readonly-preflight/SUMMARY.md)

Published product／upgrade tooling／evidence: `ControlServer_MVP@5c726218f59d10d5929e7f5c0a39c1ebd4df52f1` / `c354ff8a85c5e5e389a9c926e24f68e5f60caa7d` / `ab8aab684ae9319cb29af60af3d4afa223f11b64`

Impact on this ticket: 本机 LocalSystem 服务已用可回滚升级器替换到修复 RIoT typed-client DI 歧义的产品提交；聚焦回归 1/1、Release 102/102 tests、format 和 build 均 PASS，升级后 stop/start/restart、TLS live/version 和认证安全投影通过。只读同一快照确认 MesIngest v2.3/schema 29、Map 25 共 206 站、精确 `关卡/210`、车辆在线/启用/IDLE/Map 匹配、34% 电量满足 30% 门槛且无活动订单；当前九个 N* AREA 中八个唯一解析、一个缺站，15 种 PACKAGE 中四种被 28 条规则覆盖、十一种未覆盖，安全投影因 `RIOT_MOVEMENT_NOT_FINISHED` 正确 fail-closed 为 `UNKNOWN`。一次诊断输出意外带出旧 Onboard Authorization header 后，该凭据已立即旋转为未输出的新 Machine／服务专属值，服务重启后认证 HTTP 200；完整安全事件和轮换证据只存在归属仓。JourneyRuntime 全程关闭，未调用 RIoT mutation、未建单、未动车。当前 Onboard 远端仍为受保护的 `15c6387`，上述业务缺口及未授权移动继续阻断正式 W2G-IS-00～07 G3／RC，因此本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — Onboard 6005c7a 本机 HTTPS provider／会话预检指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Onboard 6005c7a loopback session and vehicle-safety provider preflight`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/f89ec2d48de29351c00f929e1fdb3e2f7751a173/evidence/g3/20260827-onboard-6005c7a-loopback-session/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@f89ec2d48de29351c00f929e1fdb3e2f7751a173`

Impact on this ticket: 受保护 Onboard 远端已由王昆推进到 `OnboardHmi_MVP@6005c7a89558593f199b04b1810426bc2f4072ae`，正式 HTTPS／Windows 信任／Bearer／车辆身份及时效 fail-closed provider 已接入；一次性副本中的相关聚焦测试 25/25 PASS，Onboard 与 slots-simulator Release build 均为零 warning／error。用户授权的本机 loopback 运行确认 IO 模拟器 `READY`、Onboard 到已部署 ControlServer 58005 的 TLS/NDJSON 会话建立成功，双端一致收敛为 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`，HTTPS 安全投影继续为 `UNKNOWN / RIOT_MOVEMENT_NOT_FINISHED`；测试进程与端口已清理，未启用 JourneyRuntime、未调用 RIoT mutation、未建单、未动车。Onboard 两份配置仍误写会话端口 58015 而非权威 58005，该受保护 owner 缺陷已路由到上述可写集成证据，须由王昆在 Onboard 仓发布修复提交。当前 RIoT 外部状态、动态 Map／PACKAGE 业务缺口及移动授权继续阻断匹配 `READY` 和正式 W2G-IS-00～07 G3／RC；本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — Onboard 594cd14 会话端口修复只读验证

Owning repository: `https://github.com/trytoreachpeak0/8005-agv-onboard-hmi`

Owner fix: [`fix: align ControlServer transport port`](https://github.com/trytoreachpeak0/8005-agv-onboard-hmi/commit/594cd14e2dec17285dc1352134515e3cab4abfd2)

Routing status: 受保护 owner 由王昆本人推送修复；agent 仅在精确 commit 的一次性副本中只读验证，未修改 owner 工作树。

Impact on this ticket: 两份配置和 `WireToGateSettings` 默认值已统一到权威端口 58005；端口配置与 ControlServer HTTPS provider 聚焦回归 18/18 PASS、0 skip，完整解决方案 Release build 为 0 warning／0 error。静态端口配置阻塞已关闭；尚未在 `594cd14` 上重跑会写入 ControlServer 会话恢复表、临时 journal 和模拟器状态的运行态会话，因此本票继续保持 `claimed`，正式 W2G-IS-00～07 G3／RC 仍为 `INCONCLUSIVE`。

### 2026-08-27 — Onboard 594cd14 默认端口 loopback 运行指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Onboard 594cd14 default-port loopback preflight`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/0245a476654eabf8844bffe4c4d92f3a769c29ad/evidence/g3/20260827-onboard-594cd14-default-port-loopback/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@0245a476654eabf8844bffe4c4d92f3a769c29ad`

Impact on this ticket: 用户明确授权的本机无移动运行在没有任何 `wireToGate.port` 临时覆盖时，直接使用 `594cd14` Release 输出中的默认端口 58005 建立 TLS／NDJSON 会话；simulator 为 `READY`，session generation 2，双端一致为 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`，安全投影仍因 `RIOT_MOVEMENT_NOT_FINISHED` 为 `UNKNOWN`。Onboard／simulator 已停止且临时端口释放，JourneyRuntime 未启用，未调用 RIoT mutation、未建单、未动车、未访问车辆触控屏。该结果关闭 Onboard 端口修复的运行态不确定性，但正式 W2G-IS-00～07 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — Map 25 动态现场门禁刷新指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Map 25 dynamic field-gate refresh`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/233f7044607c2fc7e2cf1a2b6c24a4b690c66082/evidence/g3/20260827-map25-dynamic-gates-refresh/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@233f7044607c2fc7e2cf1a2b6c24a4b690c66082`

Impact on this ticket: 新的原子只读脱敏快照确认 MesIngest catalog revision 1469 下，Map 25 当前 11 个 N-scoped AREA 全部唯一解析，先前观察到的缺站已消失，再次证明正式运行前必须原子重读动态目录；11 种当前 PACKAGE 中 5 种被已批准规则覆盖、6 种仍需具名业务负责人提供或批准精确 boxes-per-basket。车辆其余静态门禁满足，但电量为 21%，低于已批准 30% 阈值；直接 RIoT 与 HTTPS 投影仍一致为 `UNKNOWN / RIOT_MOVEMENT_NOT_FINISHED`。完整证据只存在可写集成仓，原始 PACKAGE 身份未进入 Git。JourneyRuntime 保持关闭，未调用 RIoT mutation、未建单、未动车；正式 W2G-IS-00～07 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-27 — 本机测试电量门槛 10% 与 RIoT 状态边界指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Test-only battery threshold 10% and RIoT motion blocker`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/048a1beb0b636077f8189653173d28864c4de23f/evidence/g3/20260827-test-battery-threshold-10/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@048a1beb0b636077f8189653173d28864c4de23f`

Impact on this ticket: 用户明确要求当前本机测试实例把电量门槛由 30% 临时调整为 10%；UAC 执行保留了精确配置备份，重启后服务为 `Running`、HTTPS live 为 200，仓库默认值仍为 30%。只读复核时电量 19%，已通过 10% 门槛，并有 11 个当前 WIRE_TO_GATE 项通过静态 N/Map/获批容量筛选；动态目录同时再次出现一个缺站项，故正式运行前仍须原子重读并只选完整准入候选。直接 RIoT 与 HTTPS 投影继续一致为 `UNKNOWN / RIOT_MOVEMENT_NOT_FINISHED`；该原因要求 RIoT/车辆侧真实报告 `MT_FINISHED`，不得把 `MT_NA` 当作停止或放宽 fail-closed 判定。JourneyRuntime 保持关闭，未调用 RIoT mutation、未建单、未动车；正式 W2G-IS-00～07 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`。

### 2026-08-27 — Onboard fresh-journal SafetyStateChanged 身份碰撞指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Onboard fresh-journal SafetyStateChanged message identity collision`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/51466ccf861d574cff3c1947fa676d8b0c822328/evidence/g3/20260827-onboard-safety-message-id-collision/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@51466ccf861d574cff3c1947fa676d8b0c822328`

Impact on this ticket: 用户已明确授权一轮空载真实移动测试，但两种受控启动顺序都在建单前复现核心会话失败：`OnboardHmi_MVP@594cd14` 短暂到 `Ready` 后，首个 `SafetyStateChanged` 在收到 `DurableAck` 前被服务端断开，后续 generation 持续增长并停在 `RecoveryRequired / HANDSHAKE_INCOMPLETE`。只读代码与运行证据一致指向受保护 Onboard owner 的 fresh-journal messageId 碰撞：`WireToGateSessionClient.SendSafetyStateChangedAsync` 只用从 1 重置的 `safetyStateVersion` 生成稳定 UUID，不同 fresh journal 会以同一 messageId 发送不同 `observedAt`／payload。需由王昆在 Onboard owner 仓修复 durable identity 并覆盖“双 fresh journal 不同身份、同 journal 丢 Ack 原身份重放”回归；agent 未修改该仓。清理后 JourneyRuntime 已关闭、peers/临时端口已释放，车辆保持 IDLE／速度 0／无订单／`STOPPED`，未调用 RIoT mutation、未建单、未动车。正式 G3／RC 继续 `INCONCLUSIVE` 且至少存在核心会话 FAIL，本票保持 `claimed`。

### 2026-08-28 — Onboard f16425c 启动安全恢复竞态指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Onboard f16425c startup safety recovery blocker`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/755067c22d146473fa8d07293a9f81f442624efe/evidence/g3/20260828-onboard-safety-provider-startup-race/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@755067c22d146473fa8d07293a9f81f442624efe`

Impact on this ticket: 王昆的受保护 owner 提交 `OnboardHmi_MVP@f16425cf0848fe9dd810dec241fd0d92639fc11d` 已通过“双 fresh journal 同时间不同身份、同 journal 丢 Ack 原身份／内容重放”聚焦回归，并在本次真实 TLS 会话中不再出现原 `HANDSHAKE_INCOMPLETE`／message identity collision；但新的受控空载尝试在建单前持续停在 generation 46 的 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`。只读代码与运行证据强烈指向 Onboard 冷启动安全 provider 竞态：会话在首个新鲜 HTTPS `STOPPED` 样本到达前即提交 revision 1 的 fail-closed 安全快照，而后续 `SafetyStateChanged` 又被 `Ready` 门禁阻止，缺少从初始 unknown／unsafe 恢复到新鲜 safe 的确定路径。需由王昆在 owner 仓确认 revision 交互并修复，且不得把 unknown 当作 stopped。编排器已自动关闭 JourneyRuntime，Onboard／模拟器和临时端口已清理；最终只读复核为车辆 IDLE、速度 0、无订单、`STOPPED`、0 reason code，未调用 RIoT mutation、未建单、未动车。本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-28 — ControlServer safe revision 未发布 Ready 转换修复指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`ControlServer safety readiness transition blocker and fix`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/5ebd4a01d21624a92d0bc58fb5828a2ee2f4ba3e/evidence/g3/20260828-controlserver-safety-ready-transition/SUMMARY.md)

Published product/evidence: `ControlServer_MVP@4347a8fb9fcb80cb9f95680a6fd8b1a0b970358b` / `5ebd4a01d21624a92d0bc58fb5828a2ee2f4ba3e`

Impact on this ticket: 王昆的受保护 owner 提交 `OnboardHmi_MVP@777eff8bdc955e6bb6fdab74ec222e0bb6748def` 已通过 provider 首次刷新、RecoveryRequired 下更高 safety revision 和原 durable identity 回归；但新的授权运行仍在建单前停于 generation 47 的 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`。脱敏 simulator 复核确认 8/8 门关闭、锁反馈有效、解锁输出复位且无 fault；最终定位为可写 ControlServer 真实处理器与 owner Fake 行为不一致：safe `SafetyStateChanged` 落库并把服务端状态改为 Ready 后，生产端只返回 DurableAck，未把 `SessionReadiness / READY` 发布给 Onboard。归属仓 `4347a8f` 已改为始终返回 Ack + 最新 readiness，精确回归覆盖 Ready→RecoveryRequired→Ready、revision 3、空 reason codes 和持久化状态；聚焦 1/1、邻近 2/2、完整 103/103 tests、format 与 Release build 均 PASS，证据已推送 `5ebd4a0`。当前安装服务尚未升级到该产品提交；编排器已关闭 JourneyRuntime，peers／临时端口已清理，车辆 IDLE、速度 0、无订单、`STOPPED`、0 reason code，未调用 RIoT mutation、未建单、未动车。本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`，须先部署 `4347a8f` 再取得新的空载旅程授权。

### 2026-08-28 — 本机 ControlServer 4347a8f 可回滚升级指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Local ControlServer 4347a8f upgrade`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/1086e4eeb51d56f325075d707573841cd93fc83a/evidence/g3/20260828-local-controlserver-4347a8f-upgrade/SUMMARY.md)

Published product/evidence: `ControlServer_MVP@4347a8fb9fcb80cb9f95680a6fd8b1a0b970358b` / `1086e4eeb51d56f325075d707573841cd93fc83a`

Impact on this ticket: 用户同意仅升级本机 ControlServer 后，精确产品提交 `4347a8f` 已从干净 disposable clone 生成 self-contained `win-x64` 包；371 个 manifest payload 逐文件 SHA-256 校验 0 mismatch，manifest SHA-256 为 `29abd09e...ca24`。既有可回滚升级器在 JourneyRuntime=false 前置下完成 ACL 受限备份、原子替换、服务／live／version／restart 和认证只读 safety 检查，结果 PASS；独立复核为服务 Running／Automatic／LocalSystem、58005/58007 正常监听、协议 `protocol-v0.1.1`，车辆 IDLE、速度 0、无订单、battery 30%、直接与 HTTPS 均 `STOPPED` 且 0 reason code。JourneyRuntime 全程关闭，未启动 Onboard／simulator，未调用 RIoT mutation、未建单、未动车。ControlServer safe-revision Ready 转换修复已部署；正式 G3／RC 仍保持 `INCONCLUSIVE`，下一步必须对 `OnboardHmi_MVP@777eff8bdc955e6bb6fdab74ec222e0bb6748def` 取得新的空载真实旅程授权，本票继续 `claimed`。

### 2026-08-28 — 777eff8 已授权旅程因本地配置字段错误安全中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Authorized journey attempt: Onboard safety identity field mismatch`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/e42be20ca08792ace88b206ab0ccaad6b5abd0a7/evidence/g3/20260828-authorized-journey-attempt-777eff8-config-field-mismatch/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@e42be20ca08792ace88b206ab0ccaad6b5abd0a7`

Impact on this ticket: 用户明确授权 `OnboardHmi_MVP@777eff8bdc955e6bb6fdab74ec222e0bb6748def`、已部署 ControlServer `4347a8f`、JourneyRuntime、RIoT 建单及一次空载真实旅程。11:03 原子预检在四个完整候选、车辆 IDLE／速度 0／无订单、29% 电量通过已批准 10% 测试门槛、双源 `STOPPED`／0 reason code 下 PASS；JourneyRuntime 随后实际启用，但新 generation 48 会话保持 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`，故在建单前安全中止。Onboard journal 证明 `SafetyStateChanged` 已获 DurableAck，但本地启动助手错误写入未使用的 `vehicleSafety.vehicleKey`，而 `777eff8` 实际读取 `expectedVehicleKey`，导致 Onboard provider 正确 fail-closed 为 `VEHICLE_STATE_UNKNOWN`。一次性助手已改为写入正确字段并通过语法／精确 commit 绑定静态校验，但未在运行时启用状态下重试。最终 JourneyRuntime=false、服务 Running/live 200、peers 与临时端口清零、车辆 IDLE／速度 0／无订单、双源 `STOPPED`／0 reason code；无 RIoT mutation、未建单、未动车。由于本次授权已经实际启用 JourneyRuntime，下一次尝试须重新取得明确授权；本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`，不写 `## Answer`、不设 `resolved`、不更新地图 Decisions so far。

### 2026-08-28 — PowerShell 7 有效运行时无 intake 安全中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`PowerShell 7 effective runtime attempt: no journey intake`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/e964a15d69643650e75abe79e79b180be8897978/evidence/g3/20260828-pwsh7-effective-runtime-no-intake/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@e964a15d69643650e75abe79e79b180be8897978`

Impact on this ticket: 新的单次授权先暴露本地编排只改基础 `appsettings.json`、未改 `appsettings.Production.json` 的伪启用问题；当时有效 runtime 未启动且数据库为 0 runtime／0 backlog／0 accepted，故修正外部 enable/disable 助手为双层备份、写入、验证、回滚和停用后继续本次授权。PowerShell 7.6.5 提权编排随后确认基础与 Production 均 enabled=true、门槛 10%，worker 产生 267+ backlog，受保护 `777eff8` generation 51 达到 `Ready` 且 departureSafe=true；但全程仍为 0 runtime／0 order／0 operation／0 unresolved accepted／0 orphan／0 active lease。确认 ControlServer `JourneyRuntimeEngine.UpsertBacklogAsync` 的 backlog 指纹包含易变 `CatalogRevision/AcceptedAt`，后续轮询会把真实当前原因覆盖为 `DEMAND_DECISION_FACT_CHANGED`，因此本次无 intake 的精确业务原因不可从持久化 reason code 判定；25 秒只读目录对照跨 revision 1815→1816、数量 272→270，公共 270 项决策字段不变。Onboard 握手事实超过 30 秒证据时效后继续等待已无安全进展，禁止通过未授权重连增加 generation，故在建单前中止。最终双层 JourneyRuntime=false、服务 Running/live 200、peers／端口清零、车辆 IDLE／速度 0／无订单、双源 `STOPPED`／0 reason code；无 RIoT mutation、未建单、未动车。当前授权已因有效 Production runtime 启用而消耗；须先修复归属仓可观测性／intake 阻塞并取得新授权，本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — ControlServer backlog 批量 intake 修复与部署指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`ControlServer backlog admission fix and local deployment`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/4b2f0582248e95cbb85dd3af12d0e002156078e8/evidence/g3/20260828-controlserver-backlog-batch-deployment/SUMMARY.md)

Published product/evidence: `ControlServer_MVP@6a5de0149288e3fdcedb6f9ea694259f71f9bee2` / `4b2f0582248e95cbb85dd3af12d0e002156078e8`

Impact on this ticket: 用户明确授权修改、测试并部署 ControlServer。测试优先复现确认易变 `CatalogRevision/AcceptedAt` 会覆盖真实 backlog 原因，且 251 个候选触发 256 次 `SaveChanges`，消耗 Onboard 30 秒握手事实窗口；产品提交 `6a5de01` 改为只对稳定 intake 决策事实做 fingerprint、真实变化时更新基线，并预载 backlog 字典后批量保存。两个新回归先 0/2 FAIL、修复后 2/2 PASS；完整 JourneyRuntime 类 30/30、完整 ControlServer 105/105、0 skip，format PASS，Release build 0 warning/0 error。精确干净提交生成 self-contained win-x64 包，371 文件、manifest `d61cb025...b7d942`、0 hash mismatch；PowerShell 7 可回滚升级 PASS，独立复核服务 Running／Auto／LocalSystem、58005/58007 仅由服务监听、live/version 和认证 safety 通过。最终原子预检为车辆 IDLE、速度 0、无订单、双源 `STOPPED`／0 reason code；JourneyRuntime=false，未启动 peers、无 RIoT mutation、未建单、未动车。受保护 Onboard `84b7f3f` 只增加端到端 Ready 测试且一次性副本 1/1 PASS，不改变生产二进制。正式 G3／RC 仍为 `INCONCLUSIVE`；新的实车组合必须绑定已部署 `6a5de01` 与选定 Onboard commit 并重新取得明确授权，本票继续 `claimed`。

### 2026-08-28 — 84b7f3f 授权旅程因 peer 结果投影歧义安全中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Authorized journey attempt: peer monitor ambiguity safe abort`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/7b5ef75783a3b245dccec95b32f2ce58daadab45/evidence/g3/20260828-authorized-journey-84b7f3f-monitor-ambiguity-safe-abort/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@7b5ef75783a3b245dccec95b32f2ce58daadab45`

Impact on this ticket: 用户明确授权 `OnboardHmi_MVP@84b7f3f66ff2f867b18121760f38e26e0bbd6fa5`、已部署 ControlServer `6a5de01`、JourneyRuntime、RIoT 建单及一次空载真实旅程。固定权限任务恢复并确认 10% 门槛，原子预检 PASS；有效双层 runtime 启用后，新 generation 53 达到 `Ready`，但 peer 启动助手的直接结果因 ordered dictionary 投影错误全部为 null，无法作为可信监控回执，故按“任何歧义立即停止”在建单前重建 stop marker 并停用。最终双层 runtime=false、peers/临时端口清零、车辆 IDLE／速度 0／无订单、双源 `STOPPED`／0 reason code，无 RIoT mutation、未建单、未动车。投影已在停用后离线修正并验证，但本次授权已经消耗；正式 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，下一次尝试仍须新的精确授权。

### 2026-08-28 — 84b7f3f 零动作 peer readiness 演练指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Zero-motion peer readiness drill for Onboard 84b7f3f`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/275fa5b37231e02cd1920cc933cbe25e8e6155e7/evidence/g3/20260828-zero-motion-peer-readiness-drill-84b7f3f/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@275fa5b37231e02cd1920cc933cbe25e8e6155e7`

Impact on this ticket: 在双层 JourneyRuntime=false 且 stop marker 持续存在的零动作演练中，修正后的 peer 助手已返回完整非 null 结果并要求 `Ready / READY`；`84b7f3f` 新 generation 56、simulator Ready、HTTPS `STOPPED`／0 reason code，Onboard journal 的已确认安全变化为 departureSafe=true、vehicleStopped=true、unknownPresent=false。演练同时确认公共 sessions API 不提供 departureSafe，且 session `updatedAt` 不是 runtime 使用的 payload evidence 时间；真正的 Capability/Safety `observedAt` 只有 30 秒窗口且不因未变化状态自动刷新，故实车流程不能在 Ready 后额外等待 15～30 秒，必须保持 runtime 先启用、peers 后启动并立即 intake，同时由受保护 probe 每秒监控。最终 peers／端口清零、车辆安全、无 mutation／订单／移动；正式 G3／RC 仍为 `INCONCLUSIVE`，下一次实车仍需新的精确授权。

### 2026-08-28 — 84b7f3f 授权旅程因 batch-unlock 本地配置安全中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Authorized journey attempt: batch-unlock capability config safe abort`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/0ae4448fc0724cce98a93f36e3b42bea62f2b00f/evidence/g3/20260828-authorized-journey-84b7f3f-batch-unlock-config-safe-abort/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@0ae4448fc0724cce98a93f36e3b42bea62f2b00f`

Impact on this ticket: 新授权下原子预检有 6 个完整静态候选；双层 runtime 有效启用，`84b7f3f` generation 57 达到 `Ready / READY`，受保护 probe 确认 departureSafe=true，但 20 秒内始终 0 runtime／0 order／0 operation，故自动 stop。最后快照中恰有 6 项 `ONBOARD_FACTS_NOT_READY`；只读源代码定位为本地 peer 助手沿用 Onboard 安全默认 `supportsBatchUnlock=false`，而 ControlServer 对八仓批量解锁能力按设计 fail-closed。无需修改受保护 Onboard 或 ControlServer 产品代码；停用后助手已显式设为 true，语法与离线配置验证通过但未运行时重试。本次无 RIoT mutation、未建单、未动车，最终双层 runtime=false、peers/端口清零、车辆 `STOPPED`；正式 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，下一次尝试仍须新的精确授权。

### 2026-08-28 — 84b7f3f 授权旅程因 catalog-loop 动态事实过期安全中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Authorized journey attempt: catalog-loop freshness safe abort`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/f564cfa15cfac89c240d61d57bb9bf2f34a5c68a/evidence/g3/20260828-authorized-journey-84b7f3f-catalog-loop-freshness-safe-abort/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@f564cfa15cfac89c240d61d57bb9bf2f34a5c68a`

Impact on this ticket: 新授权显式使用 `supportsBatchUnlock=true`，运行配置与哈希均匹配；原子预检有 8 个完整静态候选，generation 59 达到 `Ready / READY`、departureSafe=true，但仍在 20 秒门禁内保持 0 runtime／0 order／0 operation。时间证据显示 Ready 为 13:23:06，而 9 项 `ONBOARD_FACTS_NOT_READY` 到 13:23:51 才更新，晚约 45 秒且超过 30 秒证据窗口。只读 ControlServer 代码确认 discovery 在长 catalog 循环前只读取一次 Onboard/RIoT 动态事实与 `now`，最终外部 mutation 前没有重读；因此简单改成 peers 先启动可能反而在长循环结束后使用过期事实建单，不能作为绕过方案。须先在 ControlServer 增加 just-before-intake 的同 generation 动态事实重读／时效门禁和时间推进回归，再测试部署。本次最终 runtime=false、peers/端口清零、车辆 `STOPPED`，无 RIoT mutation／订单／移动；正式 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`。

### 2026-08-28 — ControlServer 最终动态事实门禁修复与部署指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`ControlServer final dynamic-facts gate and local deployment`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/135095ddf8ac087a8f1ca722d34aa1ad539f105a/evidence/g3/20260828-controlserver-final-dynamic-facts-gate-deployment/SUMMARY.md)

Published product/evidence: `ControlServer_MVP@4153d8369262a5a574589258b6c32651bc043c79` / `135095ddf8ac087a8f1ca722d34aa1ad539f105a`

Impact on this ticket: 用户授权修改、测试和本机部署 ControlServer。产品现在在长候选处理后重读同 generation 的 Onboard/RIoT facts，并在最终 catalog refresh 后、持久化 AcceptedDemand/JourneyRuntime/OrderIntent 前再次执行同一门禁；任一失败写 `FINAL_DYNAMIC_FACTS_NOT_READY` 且不触发 RIoT。修复前时间推进回归观察到错误 AcceptedDemand，修复后聚焦 2/2、JourneyRuntime 32/32、全套 107/107、0 skip，format 与 Release 非增量构建均 PASS。精确 clean commit `4153d83` 的 self-contained 包含 371 文件、manifest `7b966c86...1dcc0`、0 mismatch；可回滚升级 PASS，随后固定任务恢复测试阈值 10%。最终原子预检为车辆 IDLE／速度 0／无订单、双源 `STOPPED`／0 reason、runtime=false、stop marker 存在，无 RIoT mutation／订单／移动。正式 G3／RC 仍为 `INCONCLUSIVE`；下一次实车须绑定已部署 `4153d83` 与选定 Onboard commit 并取得新授权。

### 2026-08-28 — 4153d83 授权旅程因独立安全监控凭据歧义中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Authorized journey attempt: independent safety monitor authentication safe abort`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/6bb7cae63b0ef81292a0b6f9174a6a20edb620cf/evidence/g3/20260828-authorized-journey-4153d83-monitor-auth-safe-abort/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@6bb7cae63b0ef81292a0b6f9174a6a20edb620cf`

Impact on this ticket: 用户明确授权 `OnboardHmi_MVP@84b7f3f66ff2f867b18121760f38e26e0bbd6fa5`、已部署 ControlServer `4153d8369262a5a574589258b6c32651bc043c79`、`supportsBatchUnlock=true`、JourneyRuntime、一个 RIoT 订单及一次空载真实旅程。固定检查和原子预检 PASS 后，双层 runtime 有效启用，generation 61 达到 `Ready / READY` 且受保护 probe 为 fresh、`departureSafe=true`、0 runtime／0 order／0 operation；但额外 HTTPS 安全监控误把 `CONTROL_SERVER_RIOT_CALL_API_KEY` 用于要求 `CONTROL_SERVER_ONBOARD_CREDENTIAL` 的端点并得到 401，无法满足双通道确认，故按“任何安全歧义立即停止”立刻中止且未重试。离线只读诊断确认凭据选择错误；停用后用正确命名凭据返回 HTTP 200／`STOPPED`／0 reason。最终双层 runtime=false、stop marker 存在、peers／临时端口清零、车辆 IDLE／速度 0／无订单、双源 `STOPPED`／0 reason，无 RIoT mutation／订单／移动。本次授权已因有效 runtime 启用而消耗；正式 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`，下一次尝试仍须新的精确授权。

### 2026-08-28 — 4153d83 授权旅程因 RIoT observation 时钟顺序缺陷中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Authorized journey attempt: RIoT observation clock-order safe abort`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/d03f0e7d0cb29b8b009ef006ef283a6957c7677e/evidence/g3/20260828-authorized-journey-4153d83-riot-observation-clock-safe-abort/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@d03f0e7d0cb29b8b009ef006ef283a6957c7677e`

Impact on this ticket: 新授权精确绑定 `OnboardHmi_MVP@84b7f3f66ff2f867b18121760f38e26e0bbd6fa5` 与已部署 ControlServer `4153d8369262a5a574589258b6c32651bc043c79`，并明确允许正确的 `CONTROL_SERVER_ONBOARD_CREDENTIAL` 只读监控。固定检查、原子预检和修正后 HTTPS 监控均 PASS；双层 runtime 有效启用后 generation 63 稳定在 `Ready / READY`、`departureSafe=true`，23 个监控样本均为 HTTPS `STOPPED`，但始终 0 runtime／0 order／0 operation，故在 Onboard 证据上限前主动中止。最后 probe 显示 16 个静态完整候选均为 `RIOT_VEHICLE_FACT_STALE`。只读源码定位为生产时钟顺序缺陷：发现循环在异步目录／车辆读取前捕获 `now=t0`，成功的 RIoT HTTP 读取在返回后才以本机时间写 `ObservedAt=t1`，候选门禁却把正常的 `t1>t0` 判为 future/stale，导致 eligible=0、永远到不了 intake；固定时钟测试掩盖了该路径。最终双层 runtime=false、stop marker 存在、peers／端口清零、车辆 IDLE／速度 0／无订单、双源 `STOPPED`／0 reason，无 RIoT mutation／订单／移动。须在 ControlServer 以读取完成后的时钟验证事实并增加推进时钟回归，再测试部署；本次旅程授权已消耗，正式 G3／RC 继续 `INCONCLUSIVE`，本票保持 `claimed`。

### 2026-08-28 — ControlServer RIoT observation 时钟顺序修复与部署指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`ControlServer RIoT observation clock-order fix and deployment`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/3e290412735a0288014db4edaa4afdf61ff28955/evidence/g3/20260828-controlserver-riot-observation-clock-fix-deployment/SUMMARY.md)

Published product/evidence: `ControlServer_MVP@193d6bbb1430b807b4db471975707cb6ce8c36fd` / `3e290412735a0288014db4edaa4afdf61ff28955`

Impact on this ticket: 用户授权修改、测试、推送并本机部署 ControlServer，明确排除受保护仓和实车动作。推进时钟回归 `VehicleReadsThatAdvanceClockUsePostReadTimeForAdmission` 在旧实现上 0/1 FAIL（AcceptedDemand 为空）；产品改为在 RIoT 车辆读取完成后捕获 `dynamicFactsNow` 并用于初始动态门禁，最终聚焦 1/1、JourneyRuntime 33/33、全套 108/108、0 skip，format PASS，Release 非增量构建 0 warning/0 error。精确干净产品提交 `193d6bb` 生成 self-contained win-x64 包：371 个 payload、manifest `2a10eddd...8c16b`、0 路径／长度／哈希／集合差；可回滚升级严格回读 source commit／manifest 匹配并 PASS。固定任务随后恢复 10% 阈值；最终固定检查和原子预检为双层 runtime=false、车辆 IDLE／速度 0／无订单、双源 `STOPPED`／0 reason、peers／端口清零、stop marker 存在，无 RIoT mutation／订单／移动。修复已部署，但本次授权不含实车；正式 G3／RC 继续 `INCONCLUSIVE`，下一次旅程须绑定已部署 `193d6bb` 与选定 Onboard commit 并取得新的逐次授权，本票保持 `claimed`。

### 2026-08-28 — 193d6bb 授权旅程因 RIoT 空 result 对账合同歧义中止

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`Authorized journey attempt: RIoT empty reconciliation result safe abort`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/840105116fe955be4c98757e70cbd5c7b7b16a60/evidence/g3/20260828-authorized-journey-193d6bb-riot-empty-result-safe-abort/SUMMARY.md)

Published branch/commit: `ControlServer_MVP@840105116fe955be4c98757e70cbd5c7b7b16a60`

Impact on this ticket: 新授权绑定 Onboard `84b7f3f66ff2f867b18121760f38e26e0bbd6fa5` 与已部署 ControlServer `193d6bbb1430b807b4db471975707cb6ce8c36fd`。时钟修复实际打通 intake：generation 65 稳定 `Ready / READY`，AcceptedDemand 与 JourneyRuntime 已持久化，唯一 TO_PICKUP OrderIntent 进入 `AwaitingPickupArrival`；但 intent 持续 `RESULT_UNKNOWN`／`orderConfirmed=false`，runtime 为 `PICKUP_ResultUnknown`，故按歧义门禁停止。脱敏只读 `detailByUpperId` 返回 HTTP 200、业务 code 0、无 `result`；产品只将 HTTP 404 视为确认不存在，因此 fail-close 为 Unknown，无法进入安全的 create 门。现有持久化／事件不能取证级证明 POST 是否发出，故不得宣称建单或零 mutation。停用后至约 8 分 38 秒车辆持续 IDLE／速度 0／无 order/task、双源 `STOPPED`／0 reason、未移动，双层 runtime=false、peers／端口清零、stop marker 存在；但有限观察不能永久排除远端 orphan，分类为 `SAFE_NOW / ORPHAN_NOT_YET_EXCLUDED`。须由 RIoT owner 确认 200/code0/no-result 的合同语义并提供该冻结 upper-id 的服务端审计或官方最大落单上界；确认后才可在 ControlServer 区分 Reconcile 空 result→NotFound 与 Create 空 result→Unknown，并对现有 `RESULT_UNKNOWN` 做显式受控恢复。普通新旅程授权不足以继续，本票保持 `claimed`，正式 G3／RC 继续 `INCONCLUSIVE`。

### 2026-08-28 — ControlServer 接入不可变 RIoT SDK

SDK repository: `https://github.com/trytoreachpeak0/8005---AGV`

SDK source: `codex/riot-sdk-controlserver-integration@e708f874fa3b76f9ed1cf39c2f97e4a026c13c10`

ControlServer product: `ControlServer_MVP@beb696587b58c37b962b50e002fa0651cbfe04d5`

Evidence pointers: [`BC-ORDER-019`](https://github.com/trytoreachpeak0/8005---AGV/blob/e708f874fa3b76f9ed1cf39c2f97e4a026c13c10/rcs/riot-behavior-lab/knowledge/behavioral-contracts.md#bc-order-019-detailbyupperid-%E7%9A%84%E7%A9%BA%E7%BB%93%E6%9E%9C%E5%8F%AA%E8%AF%81%E6%98%8E%E6%9C%AC%E6%AC%A1%E8%A7%82%E6%B5%8B%E6%9C%AA%E8%A7%81%E8%AE%A2%E5%8D%95)、[`ADR-sdk-0009`](https://github.com/trytoreachpeak0/8005---AGV/blob/e708f874fa3b76f9ed1cf39c2f97e4a026c13c10/docs/adr/sdk/0009-order-observation-four-state-result.md)、[`vendored package provenance`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/beb696587b58c37b962b50e002fa0651cbfe04d5/vendor/nuget/riot-sdk/0.1.0-controlserver.2/README.md)

Impact on this ticket: ControlServer 已移除 RIoT 手写 URL／DTO 解析，改为锁定 `RIoT.Sdk.Facade 0.1.0-controlserver.2`，三个运行包与符号包均从 SDK 精确干净 commit 打包并保存 SHA-256、nuspec repository commit 和 lock-file content hash。SDK 用四态区分 `Found`、仅 HTTP 404 的 `NotFound`、HTTP 200／code 0／无 result 的 `AbsentAtObservation` 与非完整／错 upper-id 的 `Indeterminate`；后两者在 ControlServer 仍 fail-closed 为 Unknown，mutation 不自动重试。接入测试发现 SDK C# 对 JSON null 可选数值的解析缺陷，已回写 SDK、增加 C#/Python 成对回归并以不可变 `.2` 取代未进入最终锁文件的 `.1`。SDK 最终 C# 76/76、Python 73 passed／1 环境 smoke skipped，ControlServer 聚焦 44/44、完整 139/139、0 skip，locked restore、format、Release build 0 warning／0 error，双方各 11/11 高风险伪变异被杀。此次未部署本机服务、未启用 JourneyRuntime、未访问真实 RIoT、未建单或移动车辆；固定只读任务随后返回码 0，并确认双层 runtime=false、测试阈值 10%、服务 Running／Auto、58005/58007 仅由服务持有且 HTTPS live。冻结 POST 服务端接收事实、空结果正式合同与异步落单最大上限仍待 RIoT owner，故本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — ControlServer 持久建单审计与本机部署指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`ControlServer durable RIoT create-attempt audit and local deployment`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/ff41f7729c223065c7e3419f0b9aacad56a9c7ca/evidence/g3/20260828-controlserver-riot-create-audit-deployment/SUMMARY.md)

Published product/evidence: `ControlServer_MVP@f07fe36ee9e8ba953a0e289d5641bf91caf513a3` / `ff41f7729c223065c7e3419f0b9aacad56a9c7ca`

Impact on this ticket: 用户授权在当前 SDK 接入上修改、测试并部署建单审计，同时明确要求 runtime 关闭、不启动 Onboard、不调用真实 mutation、不建单、不动车。产品新增 append-only phase ledger、nullable legacy-safe summary、ARM／START 同请求摘要、mutation 后独立查询证据、取消／异常 UNKNOWN 落盘、双层 receipt 去敏，并以 EF concurrency token 阻断旧快照覆盖已提交 attempt；旧记录保持 NULL 且不能获得建单资格。完整 Release 测试 156/156、0 skip，18/18 可观察高风险 mutation 被杀，Release build 0 warning／0 error，全新 SQLite 10 段迁移与唯一序列约束 PASS。精确产品 commit 的 self-contained win-x64 包含 382 个 payload、manifest `18f366b...b31b0ff0`；可回滚升级、全版本字段、已安装 payload 和固定检查均 PASS，最终双层 runtime=false、阈值 10%、服务 Running／Auto／LocalSystem、停止标记存在、peers／临时端口为 0、只读 safety 为 `STOPPED`／0 reason，明确无 RIoT mutation／订单／移动。该增量关闭的是 ControlServer 本地“是否已 arm、是否已 START、SDK 返回与后续查询结果”的取证空洞，不伪造 RIoT 服务端接收事实；下一次黑盒实验仍须新的逐次授权并绑定已部署 `f07fe36` 与选定 Onboard commit。本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — ControlServer AbsentAtObservation 实验门与本机部署指针

Integration repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Evidence artifact: [`ControlServer absent-at-observation experimental create gate`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/dd141fd05cd894ed1ba0c0e81303e08bbe38a418/evidence/g3/20260828-controlserver-absent-observation-experiment-deployment/SUMMARY.md)

Published product/evidence: `ControlServer_MVP@9056d3d4c5b96281069023fefb531aae13f5e7a9` / `dd141fd05cd894ed1ba0c0e81303e08bbe38a418`

Impact on this ticket: 用户仅授权在 ControlServer 实施、测试、推送、打包并本机部署默认关闭的实验门，全程保持 JourneyRuntime 禁用并排除真实 RIoT mutation、订单和车辆移动。产品以精确、未过期的一次性持久 permit 绑定完整身份，仅允许 SDK `Unknown + RECONCILE/AbsentAtObservation + null HTTP/business/result/failure` 证据进入；PRE 先落为 `RESULT_UNKNOWN`，permit 消费／ARM 原子落盘，START 在 Create 前落盘，并以审计序列及状态／attempt／authorization 并发令牌阻断迟到 PRE 和重复调用。最终 Release 218/218、G2 8/8、全新 SQLite 11 段迁移、包与安装校验、可回滚部署及固定禁用态检查均 PASS；已安装实验门=false、双层 runtime=false、阈值 10%、peers／临时端口为 0，明确无 mutation／订单／移动。该交付只建立下一次黑盒实验所需的 fail-closed 控制与取证基础，不授权真实旅程；本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — 首次许可影子因 MesIngest v2.4 契约漂移安全中止

Owner repository/evidence: [`8005-agv-control-server@931052d`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/931052df53472f317a82bf4b4cb26d79138bcb67/evidence/g3/20260828-authorized-absent-shadow-contract-drift-safe-abort/SUMMARY.md)

Impact on this ticket: 首次 mutation-blocked 影子已消耗逐次授权，并在任何业务受理或外部 mutation 前因 ControlServer 固定 v2.3、现场 MesIngest 已为 v2.4 而 fail-close；无 demand／runtime／intent／order／operation 或车辆移动。责任仓已精确升级到 v2.4、加固只读影子门并以 218/218 测试通过后推送 `ControlServer_MVP@931052d`，但新包未部署、第二次影子未运行。下一次只读许可影子必须绑定最终 package/tool/Python/peer 哈希并取得新的明确授权；本票继续 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — 许可影子前置权限假设安全中止与工具修复

Owner repository/evidence: [`8005-agv-control-server@04b1b7e`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/04b1b7e47de682b0e6000c97ac9981b62e5dd577/evidence/g3/20260828-authorized-shadow-preflight-permission-safe-abort/SUMMARY.md)

Impact on this ticket: 哈希绑定运行在 Host 启动前因非提升进程无权读取安装配置、失败路径重复写 ACL 而安全中止；未创建 Host／proxy／peer／shadow DB／permit，也无 RIoT 请求，故按“Host 启动即消耗”条款未消耗操作授权。责任仓改为对固定提升只读任务的完整安全有效态做严格类型化前后哈希，并在最终证据前只验证既有 ACL；独立复核为 mutation-blocked GO，错误身份负测已确认能写出 fail-close 结果。runner 与 package 身份已变化，仍须重新绑定授权后才可运行；本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — 安全时间戳前置误判修复与完整 preflight PASS

Owner repository/evidence: [`8005-agv-control-server@8577b41`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/8577b413697996a6dad4e57953eefa77f86100cd/evidence/g3/20260828-authorized-shadow-preflight-safety-timestamp-safe-abort/SUMMARY.md)

Impact on this ticket: 第二次绑定运行仍在 Host 启动前安全中止；原始安全 JSON 的 UTC offset 被 PowerShell 自动本地化后丢失，导致 runner 将正常 `STOPPED` 样本误判为未来约 8 小时。责任仓改为从 raw JSON 强制读取显式 offset，并新增不会启动 proxy／Host／peer 的完整 `-PreflightOnly`。最终 `8577b41`／manifest `30b33a60...a52e9` 的 preflight 已证明 tool/peer/Python/package、MesIngest v2.4、两次安全样本、生产 DB、安装有效态、端口、清理和 ACL 全部 PASS，`cleanupFailureCount=0`、`authorizationReusable=true`；操作授权仍未消耗，但实际 shadow 必须重新绑定最终 runner `d177d4a4...d344`。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — mutation-blocked 影子选中候选但许可提取窗口误判

Owner repository/evidence: [`8005-agv-control-server@b194977`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/b194977a4fd8b60f0702dae2243b919793d6ed42/evidence/g3/20260828-authorized-mutation-blocked-shadow-extractor-window-safe-abort/SUMMARY.md)

Impact on this ticket: 最终授权影子已启动隔离 Host／Onboard／simulator，故授权已消耗；generation 1 达到 `Ready / READY` 并产生唯一 AcceptedDemand／runtime／TO_PICKUP intent／active lease。代理最终 169 GET、0 blocked/forwarded mutation，0 order/create attempt/auth/station operation；38 个安全样本未观察到移动，生产 DB 与安装有效态前后不变，端口均回收。许可未签发，因为旧 extractor 要求 audit 全表恰一条，约 1.02 秒后状态机自然追加只读 POST reconciliation 即永久错过窗口。责任仓已改为停止后严格接受“1 个 exact PRE + 0..N 个同 identity、连续、无 create 痕迹的 exact POST”，并拒绝 NULL attempt count／任何 CREATE／order／arm／auth／receipt 偏差；独立安全复核选择离线静止 DB 提取而非 watcher。离线提取尚未授权或执行，本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — 停止态离线 permit 精确提取 PASS

Owner repository/evidence: [`8005-agv-control-server@41de6a9`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/41de6a94d641d630268aecdd7ccd4212c17878d8/evidence/g3/20260828-authorized-offline-permit-extraction/SUMMARY.md)

Impact on this ticket: 用户单独授权只读静止 shadow／production overlap 并只写受限 private permit 与 sanitized result。提取前后严格回读 tool/Python/original result/shadow DB bundle/production DB bundle/ACL/端口/进程均一致；唯一候选的 1 PRE + 75 POST 全部为同 identity、连续、零 create 痕迹的 `AbsentAtObservation`，production overlap=false。private 与 sanitized selection hash 一致，输出 SHA-256 已在责任仓脱敏证据登记；执行未启动 Host／proxy／peer、未访问 RIoT。permit 本身不授权 mutation、订单或车辆动作，下一步仍须实现并审查精确 one-shot real egress，再取得独立实车授权；本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — 改走人工单次建单 runbook

Owner repository/runbook: [`ControlServer_MVP@44c119e` 人工 runbook](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/44c119e115423959008cfd012ed9c236f76edf10/docs/authorized-absent-observation-manual-runbook.md)

Impact on this ticket: 用户选择不再建设一次性真实实验工具；未提交的 runner/proxy/state 扩展已全部撤销，责任仓仅保留一页人工执行清单。该清单复用已部署的产品内置一次性 permit 门、现有 private permit、停止态 shadow DB 和只读 same-upper-id 对账，明确请求不确定时不得再次 POST，并要求 finally 停止本次子进程和释放端口。此次只提交并推送文档，未启动 Host／proxy／peer，未连接 RIoT，未创建订单或触动车辆。下一步转交现场人员：先确认物理安全，再由用户对清单列出的明文 HTTP、无独立 egress interlock 等剩余风险给出新的逐次授权；在此之前本票保持 `claimed`，正式 G3／RC 仍为 `INCONCLUSIVE`。

### 2026-08-28 — 依据 upperId 幂等契约打通建单链路

Owner repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Published product: `ControlServer_MVP@21f1dd65ed6177f21de0e83479950c5c4a5ff13c`

Contract source: [`BC-ORDER-004`](https://github.com/trytoreachpeak0/8005---AGV/blob/codex/watch-bilingual-integration/rcs/riot-behavior-lab/knowledge/behavioral-contracts.md#bc-order-004-相同-upperid-重复提交被拒绝订单已存在)

Impact on this ticket: 用户明确 RIoT owner 不提供技术支持或程序修改，并将「HTTP 200 但实际未建单」定性为 RIoT 自身缺陷，只要求实现正确的建单链路。据此撤销原「等 RIoT owner 确认空结果合同语义」这一永远无法满足的阻断。依据 RIoT Behavior Lab 的 `OBSERVED` 级 BC-ORDER-004——`byDefaultMissions` 对已持有的同一 `upperId` 返回业务 `code=0610008 订单已存在`，不创建第二单也不回传原订单——服务端已强制 upperId 幂等，因此「建单前必须先证明订单不存在」不是安全必需，最坏情况只是拿到确定性的 0610008。ControlServer 新增 `RiotOrderObservationKind.AlreadyExists` 并将 `0610008` 映射为确定性已存在后转同 upperId 对账；精确 absent-at-observation 读取（HTTP 200／业务 code 0／无 result／无 failureCategory）现可直接建单，不再需要一次性 permit。`DispatchAuditVersion==1` 与 `CreateAttemptCount==0` 守卫保留，单个 intent 至多一次建单；非精确 Unknown（超时、传输失败、带 HTTP 码或业务码、result 存在）仍全部 fail-closed。已废除的「无 permit 即不得建单」测试整体移除，保留 fail-closed receipt 边界与 permit 持久化不变量，并新增覆盖新链路的三条测试（无 permit 精确 absent 建单一次并确认、0610008 对账到持有该 upperId 的订单、已有 attempt 后不再二次建单）。Release 构建 0 warning／0 error，`dotnet format` 通过，199/199 测试、0 skip，净变更 143 增／802 删。本次未打包、未部署、未访问真实 RIoT、未建单、未移动车辆。安全论证的依据由「前置查询证明不存在」换为「服务端 upperId 幂等」，若该契约在 Map 25 现场不成立则可能重复建单，用户已将此类偏差定性为 RIoT 缺陷。剩余阻断收敛为单一项：现场物理安全确认与真实建单的逐次授权。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-28 — 建单 dispatch 默认关闭开关与本机部署

Owner repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Published product: `ControlServer_MVP@1a0158c87c36fb2e3e0f4ddca1f7ed9c84d5672b`（文档与证据 `2d4bd77`）

Owner evidence: [`ControlServer 建单 dispatch 开关：实现、G2 与本机部署`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/2d4bd77/evidence/g3/20260828-controlserver-create-dispatch-gate-deployment/SUMMARY.md)

Impact on this ticket: 审计 `21f1dd6` 时发现它在取消 permit 的同时移除了一个未被记录的操作联锁——在该 commit 上 `JourneyRuntime:enabled=true` 加真实凭据即足以自动 POST 建单，而此前默认关闭的实验门意味着误开 runtime 也建不了单。已把「开启 runtime」与「授权真实下单」拆成两个独立开关：`RiotCreateDispatch:enabled` 默认关闭，缺失该配置段解析为 Denied，所有建单路径在 arm 之前返回 `CreateDispatchDisabled` 且不写任何东西，因此关闭态演练不消耗 intent 的建单资格，`JourneyRuntimeEngine` 只记 `BlockReasonCode`。持久 `DispatchAuditVersion==1` 与 `CreateAttemptCount==0` 守卫不变，单 intent 至多一次建单。Release 构建 0 warning／0 error，format PASS，208/208 测试、0 skip；正式 `protocol-v0.1.1` 下 W2G-IS-00～07 八份 G2 全部绑定 `1a0158c` PASS，集合 SHA-256 为 `5a3d5f075ec9745ec9c99e5809b68331f0ac88bae78f6336b6aba77a739e1f1d`。package manifest `3475c33e1962eafb0e076afb94bea496af8730a0551dd990c1fe822005f84c4b` 已可回滚部署到本机，升级结果 PASS，已安装 ProductVersion 回读为 `1a0158c`，双层 runtime=false、建单开关=false、实验门=false、只读安全为 `STOPPED`／0 reason、58005/58007 仅由服务持有，`riotMutationPerformed`／`orderCreated`／`vehicleMoved` 均为 false。同时重写了现场 runbook：原文仍按已废除的 permit 流程指挥现场，会让操作者误以为有一道并不在建单路径上的门在保护自己；新版给出真实安全论据（BC-ORDER-004 幂等 + 持久 at-most-once + 操作开关），并拆成「关闭态零 mutation 演练」与「单次授权建单后立即关回」两段。本次未启用 runtime、未启动 Onboard／simulator、未访问真实 RIoT、未建单、未移动车辆。剩余阻断仍是单一项：现场物理安全确认与真实建单的逐次授权。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 零 mutation 受理演练与现场身份回读

Owner repository/evidence: [`8005-agv-control-server@d855cc9`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/d855cc9/evidence/g3/20260829-zero-mutation-intake-rehearsal/SUMMARY.md)

Impact on this ticket: 用户提供 RIoT 调用密钥与现场身份后（MesIngest 为本机且无需凭据），已在建单开关关闭的前提下用真实 MesIngest v2.4（catalogRevision 2443）与真实 RIoT 完成一次隔离演练。四项身份只读回读与已部署配置逐字一致：`老厂前线新多仓位1` 在 23 台中精确唯一解析为 `BROKERX-0c20ff0600d644869a6a80c186065d85`，地图 25 的 206 个站点中 `210` 名称为 `关卡`，车辆 `mapName=老厂前线new`、`stationNo=210`、电量 45% 高于 30% 阈值。运行时对 202 条 Demand 完成判定，WIRE_TO_GATE 15 条中 8 条 `OUT_OF_SCOPE_AREA`、6 条 `ONBOARD_FACTS_NOT_READY`、1 条 `PACKAGE_CAPACITY_NOT_UNIQUE`；即有 6 条真实 Demand 已满足全部静态与动态门禁，只差车载端仓位事实。`AcceptedDemands`／`OrderIntents`／`RiotDispatchAuditEvents`／`JourneyRuntimes` 四表全为 0 行，不存在任何 arm 或 `CREATE_REQUEST`；网关唯一写方法 `CreateAsync` 只能经两个已加守卫的入口到达，故关闭态下不存在可达的 RIoT 写路径。隔离运行使用独立端口与独立数据库，未停止或改动已安装服务，stderr 为空、端口已释放。凭据只存在于子进程环境变量，未落文件、日志、证据或 Git；原始 SUBLOT／PACKAGE 身份未进入仓库。尚未观察到 `CreateDispatchDisabled` 的运行态证据——该分支目前只有单元测试覆盖，补齐需接入真实 Onboard 与 simulator。附带发现：本机 `8005-agv-onboard-hmi` 检出停在 `a1e32dd`，落后已发布 `84b7f3f` 共 9 个提交（是 merge-base，非分叉），其中包含冷启动安全就绪修复与端到端就绪回归，因此该检出的既有 Release 产物不能用于绑定证据的联合运行，后续须从一次性克隆按 `84b7f3f` 构建；该仓库只读，本次未做任何修改。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 零 mutation 双端演练取得拒绝分支运行态证据

Owner repository/evidence: [`8005-agv-control-server@693a3d2`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/693a3d2/evidence/g3/20260829-zero-mutation-peer-rehearsal/SUMMARY.md)

Impact on this ticket: 已用真实 MesIngest v2.4、真实 RIoT、从一次性克隆按 `84b7f3f` 构建的真实 OnboardHmi 和按 `fb5f7c5` 构建的 simulator，在 `JourneyRuntime` 开启、`RiotCreateDispatch` 关闭下完成隔离演练（全新 SQLite／journal，临时端口 58105／58107，已安装服务未停未改）。五步恢复首次在真实双端下达到 `Ready / READY`、`DepartureSafe=1`、`/health/ready` 200，此前各次均 fail-close 在 `DEPARTURE_SAFETY_NOT_READY`。为定位受理阻断，第二次运行在克隆副本中把车载 `supportsBatchUnlock` 由 false 覆盖为 true（**仅诊断用，不代表实现真的支持，故该次不具验收效力**），随后一条真实 WIRE_TO_GATE Demand 完成受理并产生唯一 AcceptedDemand／OrderIntent／JourneyRuntime／VehicleDispatchLease，旅程推进到 `AwaitingPickupArrival` 并稳定停在 `BlockReasonCode = PICKUP_CreateDispatchDisabled`。关键不变量取得真机证据：该 intent 的 `Status` 仍为 `PENDING_RECONCILIATION`、`CreateAttemptCount=0`、`CreateAttemptId=null`、`DispatchAuditVersion=1`、`DispatchAuditSequence=0`，`RiotDispatchAuditEvents` 零行——审计链一行未写，关闭态演练确实不消耗建单资格，此前只有单元测试覆盖的不变量因此升格为运行态证据。两次运行 stderr 均空，四个端口全部回收，无 RIoT mutation、无订单、无车辆移动。同时暴露两个受理阻断：其一，车载出厂配置 `wireToGate.supportsBatchUnlock=false`，而 `ReadOnboardFactsAsync` 对该值为假直接返回 null，导致所有 Demand 判为 `ONBOARD_FACTS_NOT_READY`，该配置由只读的 `8005-agv-onboard-hmi` 拥有，本仓库未写入其问题记录；其二，`CapabilitySnapshot` 与 `SafetyStateSnapshot` 每会话只发送一次而此后仅有 Heartbeat，但 ControlServer 要求两者新于 `maximumEvidenceAge=30` 秒，故一个会话的受理窗口只有前 30 秒——本次受理发生在快照后 2.4 秒才得以通过。第二项跨越两端（节奏属车载、阈值属服务端），归属需用户指定可写目标仓库后才能写入完整缺陷记录。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 两条受理阻断的归属判定：均属服务端

Owner repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Owner defect record: [`受理门禁建立在协议未定义的车载事实之上`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/ab10e22/docs/defects/20260829-intake-gates-on-unspecified-onboard-facts.md)

Impact on this ticket: 用户要求按归属分别落库。读码判定后两条均属服务端，因此未向只读的 `8005-agv-onboard-hmi` 写入任何内容。D-1：`protocol-v0.1.1` 的 `CapabilitySnapshot.schema.json` 把 `supportsBatchUnlock` 定义为无 description 的裸 boolean，协议 `docs/`／`integration-slices/`／`errors/` 均未定义其语义，且协议自身合法样例 `V-CapabilitySnapshot-MIN-001.json` 取值即为 `false`；车载端对该字段无任何行为分支，只在 `Configuration.cs` 读取并抄进快照，配 `false` 与协议样例一致不构成违约；本仓库是唯一把它当行为门禁的一方且仅此一处。王昆的实现实际支持多仓位命令——`WireToGateSlotOperationExecutor.ValidateCommand` 接受 `Slots.Count` 1～8 且要求去重升序，`ValidateBeforeOperation` 遍历每个仓位校验，`ExecuteExclusiveAsync` 以 `foreach` 串行执行并逐仓位写 journal 检查点——只是逐门串行而非多门同时开（与模拟器 `maxOpenDoors: 1` 一致），关卡批量卸货需要的正是前者。该门禁亦属冗余：发送 `SlotOperationCommand` 前 `FinalDynamicFactsReadyAsync` 已按真实 `AvailableSlots` 校验目标仓位，车载 `ValidateCommand` 亦会拒绝非法集合。D-2：协议对 `CapabilitySnapshot`／`SafetyStateSnapshot` 没有任何发送节奏或新鲜度要求，车载每会话发一次不违约；30 秒 `maximumEvidenceAge` 是服务端自行引入并错套在由 `SafetyStateChanged` 做变化通知的事实上，导致每个会话的受理窗口只有前 30 秒。建议修复：D-1 移除该字段作为受理前置、保留发送时点的真实校验；D-2 把车载能力与安全事实改为会话作用域、由后续快照或变化通知取代，`maximumEvidenceAge` 仅保留给真正轮询的 RIoT 车辆观测。两条修复落地前现场无法完成任何真实受理。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 两条受理门禁修复并在出厂车载配置下验证

Owner repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Published product: `ControlServer_MVP@9a42582654d7ca793499556522beb1547403fafb`

Owner evidence: [`受理门禁修复验证`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/ce72a29/evidence/g3/20260829-intake-gate-fix-verification/SUMMARY.md)

Impact on this ticket: 用户批准修复两条服务端缺陷，均已落地并验证。D-1 不再读取 `supportsBatchUnlock`——协议对其无任何语义定义、自身合法样例即为 `false`、车载无行为分支，且"能否操作这批仓位"在下发命令时已按 `AvailableSlots` 判定。D-2 把 `MaximumEvidenceAge` 从两个快照的 payload 时间移到「该会话代次最后一条入站消息的服务端接收时间」：协议未规定快照节奏、车载每会话只发一次，原做法把受理窗口压成 30 秒；而 `CurrentReadySessionAsync` 只读持久化 Ready 行、自身无活性成分，死掉的对端会永远显示 departure-safe，故必须保留活性下界，改用接收时间可不受对端时钟影响，任何入站消息均计入以覆盖首个 Heartbeat 之前的窗口；`MaximumEvidenceAge` 继续单独约束轮询得到的 RIoT 车辆观测。修复过程中自身引入并已修正一个缺陷：活性扫描遍历全部入站行时会遇到 `sessionGeneration` 为 `null` 的 `SessionHello` 信封并抛出，导致每次旅程迭代 fail-closed（现场表现为对端连上后再不被轮询），已改为按 token 类型判定并跳过，并新增回归测试。Release 构建 0 warning／0 error，format PASS，测试 211/211、0 skip；八片 G2 全部绑定 `9a42582` PASS，集合 SHA-256 `4bf7ba9c9b7cc3131d2dfe76e6012c0bd55cd390de46a09d2d446642a2c065d7`；package manifest `e40c1865e9e6753d58b3cc541dee074cfc55f38d069d9d2194e7b917e0ffdc28` 已可回滚部署到本机。**验证运行未对车载配置做任何覆盖**（`supportsBatchUnlock` 保持出厂 `false`）：受理数由修复前的 0 变为 1，另有 6 条 `ELIGIBLE`，旅程推进到 `AwaitingPickupArrival` 并稳定停在 `PICKUP_CreateDispatchDisabled`，最后更新时间为运行开始后约 2 分 35 秒，远超原 30 秒窗口；`Status` 仍为 `PENDING_RECONCILIATION`、`CreateAttemptCount=0`、`DispatchAuditSequence=0`、`RiotDispatchAuditEvents` 零行。stderr 空，四端口回收，无 mutation、无订单、无移动。剩余阻断：`PACKAGE_CAPACITY_NOT_UNIQUE` 需具名业务负责人提供精确 boxes-per-basket；现场物理安全确认与真实建单的逐次授权。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 授权单次真实建单：第一次真实端到端移动

Owner repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Owner evidence: [`授权单次真实建单`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/9c222b1/evidence/g3/20260829-authorized-single-real-create/SUMMARY.md)

Product: `ControlServer_MVP@9a42582654d7ca793499556522beb1547403fafb`

Impact on this ticket: 用户先给出现场物理安全 GO（关卡 210 → `N2-5_N3-5` 路线可通行），再授权单次真实建单，本票据此完成项目首次真实 RIoT mutation 与首次真实车辆移动。隔离进程（全新 SQLite／journal、临时端口 58105／58107，已安装服务全程未停未改且其 runtime 与建单开关保持关闭）以环境变量临时打开 `RiotCreateDispatch`，未写入任何持久配置。结果：真实订单 `order-2093389168079142912`（数值 id `1676913`）建单成功，`upperId` 为 `W2G-94993971b3624edf81bc712d160e444a-PICKUP-1`，对应 SUBLOT `Q26081298-1|WIRE_TO_GATE`；RIoT 只读对账 `orderState=5`（SUCCESS），01:24:06 建单、01:26:22 完成；车辆 `stationNo` 由 210 变为 21，停在目标取货站。at-most-once 成立：`CreateAttemptCount=1`、`DispatchAuditVersion=1`，审计链恰为 `PRE(UNKNOWN/absent) → ARMED → CREATE_REQUEST → CREATE_RESPONSE(ACCEPTED) → POST(UNKNOWN) → POST(TERMINAL)` 无重复；第 1 条即精确 absent-at-observation 且未使用任何一次性 permit，BC-ORDER-004 幂等建单链路的现场有效性至此得到证明。stderr 空，四端口回收。同时暴露一条严重结构缺陷：`ToObservationKind` 把 `5 SUCCESS` 与 `2 CANCELLED` 一并归为 `Terminal`，而 `EnsureMovementConfirmedAsync` 只在 `Confirmed`（仅由 `Active` 产生）时放行，故旅程只能在订单**仍在执行**时推进；按 RIoT Behavior Lab `state-model.md`「物理到站早于 `orderState=5` 约 1 秒」，而 `IsTrustedArrivalAsync` 要求物理到站、`pollInterval` 为 2 秒，因此正常成功的移动有很大概率把旅程永久卡在到站前一步——本次即错过该窗口，intent 变为 `TERMINAL_RECONCILIATION_REQUIRED`、runtime 停在 `AwaitingPickupArrival / PICKUP_TerminalReconciliationRequired`。取货段与关卡段同此结构，需单独立缺陷并修复。本次只完成 `TO_PICKUP` 一段，装货、安全检查、`TO_GATE` 与关卡卸货均未进行；车辆现停留在 `N2-5_N3-5` 且无活动订单。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 卡住旅程的根因是 `"--"` 占位符，已修复

Owner repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Published product: `ControlServer_MVP@addc2fab11d506b19d9a94c83537ed24d4233ef8`

Owner defect record: [`把 QUEUEING 订单的 "--" 占位符当成已绑定车辆键`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/b39ff59/docs/defects/20260829-queueing-order-placeholder-vehicle-key.md)

Impact on this ticket: 缺陷属服务端，已按用户指示修复（若属车载端则只报告不修改）。**更正上一条进度的归因**：并非「`5 SUCCESS` 被误并入 Terminal」也不是「1 秒竞态」。真正根因是 RIoT 在未绑定车辆前于 `executeVehicleKey` 返回字面量 `"--"`（BC-ORDER-012 与 BC-ORDER-013 第 2、4 条均有 `OBSERVED` 记载），而 `ToObservation` 只在该字段为 null／空白时才回退 `appointVehicleKey`，于是 `"--"` 被当成车辆键传下去，`MatchesFrozenIntent` 比对失败，intent 在自己建单成功数秒后被 `MarkUnknownAsync` 打成 `RESULT_UNKNOWN`；`RESULT_UNKNOWN` 再也回不到 `CONFIRMED`，`EnsureMovementConfirmedAsync` 因而永远不放行，其后的 `IsTrustedArrivalAsync` 得不到执行机会。到站判定本身一直要求 `Terminal && OrderState == 5`，设计正确，缺的只是一个已确认的 leg。修复两处：一是新增 `IsAssignedVehicleKey`，仅当 `executeVehicleKey` 非空白且不是 `"--"` 时视为已绑定，否则回退 `appointVehicleKey`（即 BC-ORDER-013 第 4 条规则，订单进入执行后真实键仍优先）；二是把 `orderState == 5` 从终态需人工对账分支拆出按已确认处理，否则「订单在首次 post-create 对账前就完成」的 leg（如车辆本就停在目标站）同样死在终态，物理到站仍由 `IsTrustedArrivalAsync` 独立证明。两处原用 `orderState 5` 表示终态的夹具改用 `2 CANCELLED`。Release 构建 0 warning／0 error，format PASS，测试 218/218、0 skip；八片 G2 全部绑定 `addc2fa` PASS，集合 SHA-256 `ad49671d9015af69f379da74d0c32292826db1efacfb088f55c42c04e93f8cb4`；package manifest `db0d1f91433f25fe0b647bccd20565343d9fb90106c61ba75c42725244fe37d2` 已可回滚部署本机，部署后 runtime 与建单开关均为关闭、无 mutation／订单／移动。`"--"` 解析已由五取值单元测试直接覆盖，但「建单 → CONFIRMED → 到站 → AwaitingSublot」完整链路需一次新的真实建单才能验证，那会再次移动车辆，须另取现场物理安全 GO 与逐次授权。用户已把车辆开回关卡（站点 210，空载，电量 34%）。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 第二次授权建单因 `MT_NA` 安全中止

Owner repository/evidence: [`8005-agv-control-server@f22d3d1`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/f22d3d1/evidence/g3/20260829-second-create-safe-abort/SUMMARY.md)

Product: `ControlServer_MVP@addc2fab11d506b19d9a94c83537ed24d4233ef8`

Impact on this ticket: 用户把车辆开回关卡并再次给出同一路线的现场 GO 与逐次授权，本次运行用于验证 `"--"` 占位符修复后的完整链路，但在任何 RIoT mutation 之前安全中止，未验证到目标链路。会话 fail-close 在 `RecoveryRequired / DEPARTURE_SAFETY_NOT_READY`、`DepartureSafe=0`、`/health/ready` 503；`RiotDispatchAuditEvents` 0 行，`AcceptedDemands`／`OrderIntents`／`JourneyRuntimes` 均 0 行，未 arm、未建单、车辆未移动、四端口回收、stderr 空。原因唯一：安全投影返回 `motionState=UNKNOWN`、`reasonCodes=["RIOT_MOVEMENT_NOT_FINISHED"]`，车辆 `movementState` 为 `MT_NA`（`moveTaskNo=0`）——用户手动开回，未产生已完成的 RIoT 移动任务，因而缺少「上一次移动已结束」的正向证据；首次建单时车辆刚由 RIoT 订单完成移动处于 `MT_FINISHED` 才得以通过。其余 Round-41 谓词（speed 0、emergency OK、brake MOVABLE、control OK、location RUNNING、无非终态订单）全部通过。判断这**不是**产品缺陷：Behavior Lab 中没有任何契约把 `MT_NA` 认定为安全停稳，唯一一次 `MT_NA` 观测（Round 35）出现在「`orderState=3` 执行中但车未真正跑起来」的情形，正是不该被当作安全的状态；在缺少证据前放宽该谓词等于削弱安全门禁，故未改代码。复跑前置：车辆需先完成一次 RIoT 移动订单进入 `MT_FINISHED`，且因受理门禁本身依赖该安全事实、无法经 ControlServer 自举，须由现场／RIoT 侧直接下发一次任意短程移动。另需注意电量已降至 31%，逼近已批准的 30% 阈值，低于阈值后受理将改为 `BATTERY_POLICY_NOT_SATISFIED` 阻断。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。

### 2026-08-29 — 到站推进首次可达，暴露跨代次快照重放死循环

Owner repository: `https://github.com/trytoreachpeak0/8005-agv-control-server`

Published product: `ControlServer_MVP@bf22a48d5d0e386e7af21d162800f7cf09b0032d`

Owner defect record: [`跨会话代次重放快照造成自我维持的重连死循环`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/4aac129/docs/defects/20260829-snapshot-replay-across-session-generations.md)

Impact on this ticket: 用户为车辆充电、派 RIoT 订单使其回到 `MT_FINISHED`，随后又把车派到站点 21（`N2-5_N3-5`），三次运行逐步推进。第一次（`create3`）证明 `"--"` 与 `orderState 5` 两处修复生效：intent 首次达到 `CONFIRMED`、`CreateAttemptCount=0`（决定性 upperId 命中首轮遗留的同一订单并直接确认，未建第二单），对 RIoT 零 mutation、车辆未移动，证据见 `651b97f`。车辆到达站点 21 后重跑，`IsTrustedArrivalAsync` **首次判定到站成功**并触发 `PublishPickupStateAsync` 发出 `VehicleBusinessStateSnapshot`／`CurrentStopWorklistSnapshot`／`UpcomingStopPlanSnapshot` 三条快照——这是此前完全不可达的代码路径。但随即进入死循环，`Stage` 无法推进到 `AwaitingSublot`。诊断分两步：先发现 ControlServer 不支持协议正式定义的 `ProtocolProblem`（有独立 schema 且在 manifest 中），收到即抛 `InvalidDataException` 并拆掉连接，既加剧重连又丢弃了唯一诊断，已修复为记录并保持会话（`bf22a48`，219/219 测试）；修复后对端原因显现为 `SNAPSHOT_REVISION_CONTENT_CONFLICT`。根因是三个设计选择在重连下互相矛盾：快照 `messageId` 由旅程状态决定性派生因而跨重连不变、`ProtocolOutbox` 冻结首次 wire 字节做逐字节重放、协议信封内嵌 `sessionGeneration`；冻结信封写着 `sessionGeneration=21` 而活动会话已是第 22 代，对端遂拒绝，连接结束，下一次发布因无已恢复对端抛 `IOException` 使旅程迭代 fail-closed，对端重连、代次再进、重放仍是旧信封——150 秒内会话重建 22 次，`ProtocolContentConflictException` 51 次、`IOException` 43 次，三条快照一条未确认。候选修法三种（messageId 纳入代次／重放时重新盖章／禁止跨代次重放），其中 `ReplayPendingForSessionAsync` 已接收 `sessionGeneration` 参数，提示原意可能就是只在同代次内重放，需先查清实际重放路径再定。取货到站之后的所有阶段目前不可达。本票保持 `claimed`，正式 G3／RC 保持 `INCONCLUSIVE`。
