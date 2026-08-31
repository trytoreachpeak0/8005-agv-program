# 异机明文形态下的跨机联调

Type: task
Mode: HITL
Status: open
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
