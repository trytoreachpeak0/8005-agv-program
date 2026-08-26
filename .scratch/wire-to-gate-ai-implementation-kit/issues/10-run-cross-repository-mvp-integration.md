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
