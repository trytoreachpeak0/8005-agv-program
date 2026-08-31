# 异机明文形态下的跨机联调

Type: task
Mode: HITL
Status: resolved
Blocked by: 02, 06

## Question

到此为止两端都只在各自单侧验证过。本票第一次让改后的两端在**真正的异机**形态下建立会话——这正是
本轮改造的目标形态，也是原先被两端 loopback 守卫挡住的场景。

必须证明的：

- 服务端在非 loopback 地址上以明文 TCP 监听，车载端从另一台机器连上并完成 `SessionHello` →
  `SessionAccepted` 握手；
- 车载端经明文 HTTP 读到车辆安全投影，`vehicleKey` 精确匹配、`motionState` 与 `observedAt` 满足
  `maximumEvidenceAgeMs`，会话据此进入 `Ready` 而非停在 `RecoveryRequired`；
- 断连与重连：拔网线／停服务后车载端按 `reconnectDelaysMs` 重连，会话代次推进符合预期，journal
  epoch 与快照 revision 行为与 TLS 形态下一致——**传输层换了不应改变协议层行为**，这是本票的核心
  断言方向。

票 01 追加的一项取证（Answer 第 7 节）：**双向错配实验**。新旧两端互连不做协商，只保证失败可识别，
因此本票要特意各跑一次并记下真实错误文本——老车载端（`useTls=true`）连新服务端（明文），以及新车载端
（明文）连老服务端（TLS 非 loopback）。两个方向的错误文本进证据，票 04 的手册据此写错误对照表。没有
这张表，现场会把版本错配误判成「网络不通」。

已知的取证陷阱，直接继承上一轮：

- **本机网络会伪造可达性**。Clash 全局模式下 ICMP 与 TCP connect 对任意端口乃至不存在的主机全部
  「成功」。判定对端可达只能用**返回 body 的往返**，不能用 ping 或 TCP connect。这条在明文形态下
  更危险：没有 TLS 握手失败作为兜底信号，连错主机可能表现为静默挂起而非报错。
- 判据必须证明会响：例如把服务端停掉后同一检测器应当变红，而不是继续绿。

Mode 为 HITL：需要第二台机器（虚拟工控机或等价环境）与网络配置，agent 无法单独完成。若异机条件
暂不具备，**不得用同机 loopback 冒充异机通过**——loopback 恰恰是改造前就已经工作的场景，用它取证
等于什么都没证明。条件不具备时据实记为阻塞并说明缺什么。

## Answer

**跨机明文形态成立。** 完整证据见服务端仓
`evidence/g2/20260901-plaintext-transport-ticket07/`（`SUMMARY.md` 是入口）。

### 0. 异机环境怎么来的

用户 2026-09-01 选定：复制金机 `gpt_win11.vhdx` 父盘新建一台独立 VM，动态内存 1024–3072MB。
**金机全程未启动、检查点未合并、零写入**，克隆盘是父盘的只读副本。VM 改名 `PLAINTEXT-OBU-07`、
配静态 IP，与宿主在 Hyper-V `Huawei` 内部交换机上：

| 角色 | 机器 | 身份 |
| --- | --- | --- |
| 服务端（明文） | 宿主 `LAB-WIN-01` `192.168.200.1` | `ControlServer_MVP@65841df` |
| 车载端（明文） | guest `PLAINTEXT-OBU-07` `192.168.200.50` | `OnboardHmi_MVP@238b46e` |
| 车载端（TLS 期，仅错配 A） | 同一 guest | `OnboardHmi_MVP@31263b1` |
| 服务端（TLS 期，仅错配 B） | 同一宿主，58105/58107 | `ControlServer_MVP@3d8b00c7` |

两个地址是真正的不同主机，**全程无一处 loopback 冒充**。两个车载端包都在
`F:\w2g-ticket07` 的一次性克隆里 publish，`8005-agv-onboard-hmi` 工作树 0 改动、HEAD 未移动。

### 1. 判可达只用返回 body 的往返

绿：`GET /health/live` → `200 {"status":"live"}`；`GET /api/onboard/v1/vehicle-safety` → `200` 带
投影 JSON。红侧对照三条都响：无监听端口 → `由于目标计算机积极拒绝，无法连接。`；无主机地址 →
`HttpClient.Timeout` 超时；无 `Authorization` → `HTTP 401`。本机内部网段上 ping 恰好是诚实的
（`192.168.200.77` 返回 False），但判据仍只用 body 往返。

### 2. 明文链路实际承载了什么

服务端日志逐字：`Onboard NDJSON listener started on 192.168.200.1:58005; transport=plaintext`、
`Now listening on: http://192.168.200.1:58007`。

全程建立 4 次会话，`ProtocolInbox` 每次会话一套完整开场，完全对称：`SessionHello: 4`、
`CapabilitySnapshot: 4`、`SafetyStateSnapshot: 4`、`RecoveryStateReport: 4`，另有
`Heartbeat: 108`、`SafetyStateChanged: 89`。**全部跨机器边界以明文 NDJSON 传输**。链路 B 侧车载端
经明文 HTTP 读到投影，`vehicleKey` 与 `BROKERX-0c20ff0600d644869a6a80c186065d85` 精确匹配、
`observedAt` 新鲜。

### 3. 断连重连：传输层换了没有改变协议层行为

中途停服务端，车载端侧按 `reconnectDelaysMs` 重连并逐字记为
`上层会话不可用：由于目标计算机积极拒绝，无法连接。。将在2秒后重连。`，随后
`上层会话已建立：generation=2`。四次会话代次 1→2→3→4 单调推进，协议层无异常。

**明文形态的失败形状值得进手册**：这里是干脆的连接拒绝，没有 TLS 握手失败作为兜底信号。

### 4. 进程不依赖远程会话

从 PowerShell Direct 会话内启动的车载端会随会话关闭被杀（日志停在正常行、非崩溃）。最终一轮改用
`Win32_Process.Create` 脱离启动，再从**另一个独立会话**采样：进程存活、`generation=4`、两条链路
socket（`:58005` 与 `:58007`）均可观测。

### 5. Ready：部分达成，边界写清楚

会话**没有**进入 `Ready`，但原因不在传输层。终态为 `ReasonCode: DEPARTURE_SAFETY_NOT_READY`，
`SafetyReasonCodes = ["LOCK_NOT_CLOSED","SLOT_STATE_UNKNOWN","UNLOCK_OUTPUT_NOT_RESET",
"VEHICLE_STATE_UNKNOWN"]`，分两类：

- **前三项是 guest 没有 Modbus IO 硬件**（`ModbusTcpIoModuleClient` 持续超时）。这是车载端本地
  IO 事实，与两条被测链路无关；要清掉需要真实槽位硬件，那是票 10 现场验收的范围。
- **`VEHICLE_STATE_UNKNOWN` 已被证明可清除**，而且是用对照证的，不是断言：

  | | 上游 RIoT | `SafetyReasonCodes` |
  | --- | --- | --- |
  | 绿 | 可达 | `LOCK_NOT_CLOSED, SLOT_STATE_UNKNOWN, UNLOCK_OUTPUT_NOT_RESET` |
  | 红 | 停掉 | 同样三项**外加** `VEHICLE_STATE_UNKNOWN` |

  即：车载端经明文 HTTP 取到的投影内容**真的在驱动**服务端会话安全状态，检测器会响，不是恒绿空壳。
  它间歇复现是因为替身 RIoT 往返约 2 秒（`responded 200 in 2022 ms`），逼近车载端
  `maximumEvidenceAgeMs: 5000` 的预算。

上游 RIoT 由 `fake-riot.py` 替身，按 Round-41 谓词应答。RIoT 在服务端**上游**，不属于两条被测链路，
但投影是 fail-closed 的：没有可达 RIoT 就只能恒为 `UNKNOWN`，Ready 这条判据将根本无法被触发。
`fake-riot-requests.log` 记录了 SDK 实际请求的真实路由。

### 6. 双向错配对照表（票 04 手册据此写）

**A — TLS 期车载端（`useTls=true`）→ 明文服务端**

| 侧 | 真实文本 |
| --- | --- |
| 车载端 | `上层会话不可用：Received an unexpected EOF or 0 bytes from the transport stream.。将在2秒后重连。` |
| 服务端 | `Onboard connection ended with a protocol or transport error.` |

`SessionHello` 计数**未增加**，该构建没有任何消息进入协议层。车载端无限重连、不退出——静默故障形态，
且文本只字未提 TLS，现场极易误判为「网络不通」。

**B — 明文车载端 → TLS 期服务端**

| 侧 | 真实文本 |
| --- | --- |
| 车载端链路 A | `上层会话不可用：ControlServer在会话恢复期间关闭了连接。。将在2秒后重连。` |
| 车载端链路 B | `An error occurred while sending the request.` |
| 服务端 | `System.Security.Authentication.AuthenticationException: Cannot determine the frame size or a corrupted frame was received.` |

TLS 期服务端库 `ProtocolInbox: 0 行`、`SessionRecoveries: 0 行`。

**方向 B 的车载端措辞是最危险的一条**：「ControlServer 在会话恢复期间关闭了连接」听起来像业务层恢复
问题，而不是传输形态不匹配；只有服务端侧点出了真因。手册必须写明这类故障要读**服务端**日志。

另一条该进手册的：明文车载端的 `VehicleSafetySettings.Validate` 只接受 `Uri.UriSchemeHttp`，所以
「改成 https 就行」在这个构建上根本无法表达——错配现场只会产出「明文 HTTP 打向 TLS 端口」，本票跑的
正是这个形态。

### 7. 用 Production 而非 Development 跑，这是有意的

`environment=Production` 是唯一会让 `WireToGateSettings.Validate` 与
`VehicleSafetySettings.Validate` 执行 `IsForbiddenProductionHost` 的模式，而该守卫**直接拒绝
loopback**。也就是说本票的配置从原理上就不可能用 loopback 蒙混过关。查实
`RuleGatewaySettings` 与 `IoModuleSettings` 的 production 分支只拒占位值、不拒 loopback，所以它们
可以留在 `127.0.0.1`——这是 Production 模式可行的前提。

运行中配置回读：`useTls` 不存在、`serverCertificateSha256` 不存在、全文无 `https`。

**顺带实测发现**：TLS 期车载端 `31263b1` 随包的 `appsettings.json` 有 `useTls` 但**根本没有**
`serverCertificateSha256` 键，且 `vehicleSafety.endpoint` 是 `https://`。给该键赋值抛
`SetValueInvocationException`，与地图 Notes 那条 PowerShell 语义一致，必须用 `Add-Member`。
这也从另一侧印证了票 12「两侧 dev 配置都无此键」的核实结论。

### 8. 隔离

- 生产 `ControlServer.Host` 全程保持 `127.0.0.1:58005/58007` 未受影响；票 07 的服务端绑
  `192.168.200.1` 的同名端口，地址不同不冲突。
- `CurrentUser\Root` 在 TLS 期实验前、中、后均为 **44 张**。那张一次性 PFX 用 .NET API 直接生成到
  文件，**从未导入任何证书存储**，票 03 的信任存储证据保持完整。
- 证据目录内凭据出现 0 次、密钥材料文件 0 个。

### 9. 遗留

- 让会话真正走到 `Ready` 需要车载端侧真实 Modbus 槽位硬件（或一个可信的 IO 桩）。本票判为
  **不该在此处糊过去**：造 IO 桩本身需要验证其正确性，有引入假绿的风险，而票 10 的真车闭环本就是
  验这条的地方。
- 克隆 VM `plaintext_onboard_07` 与 stage 目录 `F:\w2g-ticket07` 保留着，票 08/09 若要复用异机
  形态可直接接上；不再需要时可整体删除，对金机与三个仓均无影响。
