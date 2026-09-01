# 验证真实适配器、目标部署与硬件边界

Type: task
Mode: HITL
Status: resolved
Blocked by: 11, 25

## Question

在用户授权且安全条件满足后，如何在指定目标环境验证 ControlServer 连接现有 MesIngest 和真实 RIoT，以及 OnboardHmi 的屏幕、触摸、扫码枪和八仓 IO 模拟器，执行安装、配置、启动、连接、只读冒烟以及获准的最小 RIoT 移动，并记录每个适配器是 PASS、FAIL 还是因外部输入 INCONCLUSIVE？真实八仓 IO 资格留作后续硬件门禁，不阻断本轮模拟 IO 软件交付。

不得用 Fake 或 HTTP mock 替代真实 RIoT 集成，不得把测试凭据写入仓库或证据。任何车辆移动或现场部署必须在当轮得到明确授权并由具名安全负责人监督；未授权时本票只能完成只读核验并记录阻断。IO 模拟器动作不属于真实车辆 IO 输出，但仍须明确标识为模拟。

## Answer

**资格结论：19 条断言 11 PASS / 5 FAIL / 3 INCONCLUSIVE。用户本轮到场并给出安全 GO，但车辆
未动、未建单——不是因为授权缺失，也不是因为时钟，而是因为部署链在 readiness 上断掉，移动这一
段根本不可达。**

验证对象是票 25 重建的 RC `C:\Users\szy\Desktop\w2g-rc-20260830-d243abf`（`d243abf` +
`304e6ad` + `protocol-v0.1.1`），**不是**票 11 那份过期的 `2eeb6f0`。隔离实例 58105／58107，
建单开关 `RiotCreateDispatch__enabled=false` 全程关闭，已安装的生产服务 `8005 AGV ControlServer`
未动。证据与 harness 在 `8005-agv-control-server` 的
`evidence/g3/20260830-issue13-target-qualification/`（`assertions.json` +
`Invoke-TargetQualification.ps1` + `onboard.log` + `host.out.excerpt.log`）。

`assertions.json` 是**机器可读断言的第一次真实发射**，顺带收掉票 21 第 2 项／票 24 拒绝事后
转写的那个缺口——票 24 说得对，真修法是「下次安装验证自己发射」，本票就是那一次。

### 逐适配器资格

| 适配器／面 | 结论 | 依据 |
| --- | --- | --- |
| ControlServer 部署（从 RC 目录直接启动） | **PASS** | `DEPLOY-START`：迁移自动应用，58105 起监听 |
| 八仓 IO 模拟器（Modbus 1502 + 控制面 58006） | **PASS（模拟）** | `IO-SIMULATOR`；车载端日志「已连接IO模块 127.0.0.1:1502」「启动IO安全快照验证通过」 |
| OnboardHmi ↔ ControlServer 会话 | **PASS** | `SESSION-ESTABLISHED` + `SESSION-STORED`：车载端日志「上层会话已建立：generation=1」，服务端 `SessionRecoveries=1`、`ProtocolInbox=19` |
| MesIngest（现有实例 `127.0.0.1:5088`） | **PASS** | `ADAPTER-MESINGEST`：`JourneyBacklog=282`，真实需求持续流入 |
| 真实 RIoT `172.19.206.222:8888` | **INCONCLUSIVE** | `NET-RIOT` 网络可达 PASS；但读路径不落任何持久行，且只在需求被受理后才走到——被下面的 readiness 阻断挡住 |
| 屏幕／触摸／扫码枪 | **INCONCLUSIVE** | 本轮跑在开发工作站，不是车载终端 |
| 真实八仓 IO 模块／接线／锁／光幕 | **INCONCLUSIVE** | 仅模拟器；按票据约定留后续硬件门禁，不阻断本轮模拟 IO 软件交付 |
| 获准的最小 RIoT 移动 | **未执行** | `SAFETY-NO-CREATE` PASS（`RiotDispatchAuditEvents=0`）。见下 |

### 本票最重要的发现：干净安装到不了 Ready

`OnboardMessageProcessor.cs:56` 在 SessionHello 时**无条件**把会话置为
`SessionReadiness.RecoveryRequired`；只有车载端随后发出 `RecoveryStateReport`、服务端走
`DecideReadinessAsync`（同文件 229 行）才可能转 `Ready`。

在干净 SQLite + 全新 journal 上观察 75～100 秒，三次运行**每次**都停在
`readiness=RecoveryRequired`，因此：

- `/health/ready` 恒 **503**（闸门只认 `Readiness='Ready'`）；
- `AcceptedDemands=0`、`JourneyRuntimes=0`——282 条 backlog 一条都没被受理；
- 因此 RIoT 读路径与整个移动闭环**在这份部署上不可达**。

这不是时间不够，是**票 14「从干净安装开始按公开步骤完成一个完整场景」在当前 RC 上走不通**。
已开票 26 承载，并挂成票 14 的阻断。

**边界（本票没证到的部分）**：没有确定它是产品缺陷还是缺一步公开操作步骤。历史上的完整闭环
用的是 stage 构建的车载端 + `Invoke-PeerRehearsal.ps1`，本轮用的是 RC 自带的 `onboard-hmi`
（同 commit `304e6ad`，publish 形态不同）。差异定位属票 26。

### RC 出厂配置：服务端是现场真值，车载端是样例值

服务端 `controlserver/appsettings.json` 出厂即现场身份（RIoT `172.19.206.222:8888`、地图 25、
关卡 210、车辆 key、MesIngest `127.0.0.1:5088`）——`CFG-SERVER-RIOT`、`CFG-SERVER-AGV` 均 PASS。
车载端 `onboard-hmi/appsettings.json` 出厂**不可用**：

| 断言 | 出厂值 | 应为 |
| --- | --- | --- |
| `CFG-ONBOARD-ENABLED` | `wireToGate.enabled = false` | `true`，否则车载端根本不发起连接 |
| `CFG-ONBOARD-AGV` | `agvId = AGV-8005-01` | `老厂前线新多仓位1` |
| `CFG-ONBOARD-COMMIT` | `a6f05fbc…1821e` | `304e6ad9…804bd6` |

另记：`vehicleSafety.endpoint` 是 `https://control.example.invalid/...` 占位符；
`ioModule.host` 出厂指向模拟器 `127.0.0.1:1502`，真实 `192.168.71.150:502` 被注释掉。
本轮为跑通把前三项在**副本**里改正，RC 本体未改。`CFG-ONBOARD-COMMIT` 归只读的车载端仓，
与票 11／25 是同一件事，仍等用户指定跟踪目的地。

**`CFG-ONBOARD-ENABLED` 的红侧**：`CFG-SERVER-RIOT` 读的是同一棵出厂树、同一个 reader 且为
PASS，所以这里的 FAIL 是文件本身，不是读取器。

### 三条被自己杀掉的判据（过程留档，不是失误清单）

第一版 harness 报出 5 个 FAIL，其中 **3 个是我自己检测器的问题**，逐条查清后才改：

1. `SESSION-ESTABLISHED` 搜服务端日志的 `SessionHello|SessionAccepted`——那份日志 64,373 行
   **全是 EF SQL，从不打印消息类型名**，该模式永远不可能变绿。它的「之前返回 False」对照
   只证明了「现在没匹配」，没证明「能匹配」，**等于没有对照**。改为读车载端日志的
   `上层会话已建立`，对照改成同一检测器在车载端启动前必须找不到。
2. `DEPLOY-HEALTH=503` 探测发生在车载端启动之前。readiness 闸门按设计要求存在
   `Readiness='Ready'` 的会话，那次 503 读到的是闸门在工作，不是部署失败。改为会话建立后再探
   （**仍然 503**，见上——这才是真发现）。
3. 「连接被对端强制关闭」的时间戳正是我自己 kill 车载端那一刻，是收尾不是缺陷。

同样地，`ADAPTER-RIOT-READONLY` 与 `ADAPTER-MESINGEST` 第一版靠 grep 日志里的 `RIoT`／
`MesIngest`／`5088` 判绿——那些命中的是连接串与建表语句，**不是适配器调用**。第三版全部改为
从库里读派生行（`JourneyBacklog`／`SessionRecoveries`／`ProtocolInbox`／`RiotDispatchAuditEvents`），
并各自带同库内保持为 0 的对照表，证明不是「所有表都被写满」。RIoT 因此诚实降级为 INCONCLUSIVE。

### 本轮未做的事

未安装到目标车载终端、未连真实八仓 IO、未建单、未动车、未用真实操作员身份
（`CONTROL_SERVER_OPERATOR_ID` 本轮为 `QUALIFICATION-READONLY`，建单开关全程关闭故不影响）。
未触产品代码，故未跑 tier 1。`dispatchGeneration` 仍未消耗，下一轮真实建单仍须为 **4**。
