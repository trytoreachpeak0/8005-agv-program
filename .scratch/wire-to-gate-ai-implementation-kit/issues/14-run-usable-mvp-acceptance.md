# 执行可用 MVP 验收并关闭阻断缺陷

Type: task
Mode: HITL
Status: resolved
Blocked by: 13, 26

## Question

如何让用户从干净安装开始，按公开操作步骤启动两端并完成一个完整 WIRE_TO_GATE 场景，同时验证停止/重启/恢复、日志与错误可诊断性；发现阻断缺陷后返回责任仓库修复、重建并只重跑受影响门禁，直到核心验收全部 PASS？

八仓 IO 模拟器环境 PASS 证明仓位软件闭环可安装并运行；完整 MVP 端到端 PASS 还必须使用现有 MesIngest 与真实 RIoT 完成获准的移动验证。只有车载目标硬件和后续真实 IO/现场步骤也具证时，才能进一步称为“目标车硬件可用”或“工厂试运行通过”。本票必须分别给出这些资格结论，不能用一个模糊的“可用”掩盖外部阻断。

## Answer

Owning repository: https://github.com/trytoreachpeak0/8005-agv-control-server

Owner issue/artifact: `evidence/g3/20260830-issue14-usable-mvp-acceptance/` 与
`evidence/g3/20260830-issue14-field-closed-loop/`

Published branch/commit: `ControlServer_MVP@9daeef4`（验收运行 `@e605ffa`，现场闭环 `@9daeef4`）

**逐项资格结论，不合并成一个「可用」：**

| 资格 | 结论 | 依据 |
| --- | --- | --- |
| 干净安装→启动→会话→就绪→受理→重启恢复 | **PASS** | 23 PASS / 0 FAIL / 5 INCONCLUSIVE |
| 完整 WIRE_TO_GATE 场景（含真实移动） | **PASS** | generation 7 `Stage=Completed`，5 分 42 秒 |
| 真实 MesIngest 适配器 | **PASS** | 真实 backlog 303 条，受理 1 条 |
| 真实 RIoT 适配器（读 + 建单） | **PASS** | 两条真单各一次成功；读路径落 205 行派生数据 |
| 八仓 IO | **模拟器 PASS，真实 IO INCONCLUSIVE** | `ioModule 127.0.0.1:1502` |
| 车载目标硬件（屏/触摸/扫码枪） | **INCONCLUSIVE** | 运行在开发工作站 |
| 服务安装、ACL、NDJSON 日志、卸载回滚 | **PASS** | 隔离实例装→跑→卸全过，生产部署未受影响 |
| 车载端 HMI 生产形态可用性 | **FAIL（归只读仓）** | 见下 |

**干净安装可用性验收（`evidence/g3/20260830-issue14-usable-mvp-acceptance/`）。** 对票 25 之后
新建的 RC `w2g-rc-20260830-81cb9cf` 按公开手册跑一次干净部署：868 个文件哈希全对（一字节翻转的
副本被同一校验器报出）；HTTPS 安全投影 200 且无凭据时 401；真实 RIoT 返回 `STOPPED` 且无
reason code；`上层会话已建立：generation=1，readiness=Ready`；`/health/ready` 从同一次运行几分钟前
的 `503 RECOVERY_HANDSHAKE_REQUIRED` 转为 `200 ready`；`AcceptedDemands=1`；
`StationTaskTypeAdmissions=205` 是 RIoT map 派生的持久行——票 13 只能给 INCONCLUSIVE 的那条现在
成立。重启后 `generation 1→2`、readiness 回到 `Ready`、`ProtocolInbox 34→52`、journal 增长未重建。
两条单字段变异各自证红：翻转钉住的证书哈希一位十六进制则完全建不起会话；改掉
`expectedVehicleKey` 则会话建起但 readiness 停在 `RecoveryRequired`。

**现场闭环（`evidence/g3/20260830-issue14-field-closed-loop/`）。** 用户现场安全 GO、操作员
`S0020310`、`dispatchGeneration=7`。generation 7 全程走通受理→建单→取货移动→到站→子批录入→
两仓装货→发车安全检查→`TO_GATE` 移动→关卡到站→批量卸货→原子完成，`Stage=Completed`、
`BlockReasonCode` 空、`SessionGeneration` 全程 1、5 分 42 秒、两条真单各一次建单成功
（10 条五步审计）、`Load`／`Unload` 均 `Committed`。2026-08-29 那次闭环绑的是 `3d8b00c`，本次补跑
`127b137`／`1fd23ac`／`d243abf`／`264615a`／`81cb9cf` 五个提交，且部署形态换成 RC 的生产形态
（生产模板整体替换、TLS 钉证书、HTTPS 安全投影）。由此证实一条 08-29 看不到的行为：车辆移动期间
readiness 落到 `DEPARTURE_SAFETY_NOT_READY`、服务端以 `ONBOARD_SESSION_NOT_READY` 挂起，停稳后
自动回 `Ready` 继续——安全闸门按设计工作且不卡死旅程，两次到站都是这个形态。

generation 4／5／6 未走通，**三次都是本目录脚手架的缺陷，产品行为四次一致且正确**：装卸助手替代
操作员在 120 秒 `operationTimeoutMs` 内关门，前三版分别是没有助手、空响应抛异常直接退出、
每轮重新推断意图导致货物状态来回翻。逐条原因见 SUMMARY.md。

**开工前解掉的一个假绿。** 本会话开始时安全投影恒为 `UNKNOWN / RIOT_READ_TIMEOUT`，根因是 Clash
处于全局模式（内核给 `172.19.206.222` 选的源地址是 Clash TUN 的 `198.18.0.1`），另有
`vEthernet (Default Switch)` 占用 `172.19.192.1/20` 覆盖了现场 RIoT 地址。期间 ICMP 8/8 通、TCP
connect 对 8899／9／12345／65001 乃至根本不存在的 `172.19.206.99` 全部成功——**票 13 的
`NET-RIOT PASS` 用的正是 TCP-connect 探针，其「8899 必须 False」的对照在该网络状态下不成立**。
只有返回 body 的 HTTP 往返才能区分。用户改回规则模式后立即恢复。记录在 `riot-path-red.json`。

**具名 FAIL，归只读仓 `8005-agv-onboard-hmi`。** 生产形态下 `App.xaml.cs` 注入
`DisabledRuleGateway`（`IsConnected` 恒 false），而 `OnboardController.ReevaluateIdleState` 要求
`_ruleGateway.IsConnected`，于是 HMI 状态机永久停在 `Connecting`：横幅一直是「正在等待仓门控制
设备和任务系统连接…」（尽管上层会话/仓门控制/发车安全/到站四项都正确显示），「操作记录」只有启动
两行，仓位卡进不了 `WaitingOperatorRecovery`。叠加 `WireToGateBusinessService` 以
`WireToGateRecoverySafetyFacts.Unknown` 求值、一律阻断服务端恢复动作（源码注释自述为
intentional），结果是**站点操作一旦落进 `RecoveryRequired`，现场操作员在随包 HMI 上没有任何前进或
撤销的手段**。gen4 的现场截图是该状态的证据。本仓只留此路由指针，不写入该项目内容；需要用户指定
可写目的地或转交王昆。

**服务安装（手册第 4 节）。** 前两次验收都是直接启动随包 host，因为 agent 会话没有管理员令牌；
用户随后以管理员跑了隔离安装（`ServiceName '8005 AGV ControlServer Ticket14'`、独立
InstallRoot／DataRoot／BackupRoot、端口 58505／58507、`-SkipMachineEnvironmentInjection`），
结果 `PASS`，九项检查全过：`package-hashes`、`sqlite-migrations-at-start`、
`https-chain-pinned-to-install-root`、`https-live-after-start`、`https-ready-after-start`、
`stop-start`、`restart`、`https-version`、`log-file-written`，产出
`controlserver-20260830.ndjson`，`firstStartReadiness` 为文档预期的
`503 RECOVERY_HANDSHAKE_REQUIRED`，`journeyRuntimeEnabled=false`、`riotMutationPerformed=false`、
`orderCreated=false`、`vehicleMoved=false`。**ACL 硬化是独立证实的而非脚本自报**：安装目录与数据根
对本 agent 的非管理员会话双双 `Access denied`，同时服务本身 `Running / LocalSystem / Automatic`
且在 58505／58507 上监听。

随后用户以管理员跑手册第 9 节的卸载（`-ConfirmUninstall`，不加 `-RemoveDataRoot`），结果 `PASS`，
同样独立核验而非采信脚本自报：服务已消失、安装目录已删除、数据根按预期保留（可用同一包重装）、
隔离端口 58505／58507 零残留。`trustedRootCertificatesRemoved=0` 与安装时的
`trustStore: none (pinned CA file)` 一致——安装从未写入证书存储，故无可移除项。生产服务
`8005 AGV ControlServer` 全程 `Running`，58005／58007 的 `OwningProcess` 在会话首尾都是同一个
PID 36960，证明隔离实例的安装与卸载都没有触碰生产部署。**安装→启动→停止→重启→卸载→回滚整条
生命周期至此在发布候选上闭合。**

**仍为 INCONCLUSIVE 的项，照录不隐藏**：真实八仓 IO（本轮由模拟器提供）、车载目标终端硬件
（屏幕／触摸／扫码枪，本轮运行在开发工作站）。W2G-IS-00～07 的切片门禁状态不由本票改变。
未触产品代码，故未跑 tier 1。
