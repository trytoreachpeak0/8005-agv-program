# WIRE_TO_GATE MVP Definition of Done

以下门禁必须对同一组三仓 commit、同一协议身份和同一发布候选成立。任一核心门禁 FAIL/INCONCLUSIVE 即未完成。

## D1 — 协议与身份

- W2G-IS-00～07 所需 messageType 均有严格 Schema、合法/非法样例、稳定错误码、共同向量和机器切片索引。
- G1 从干净 checkout 重算 manifest、Schema bundle、向量和文件哈希后零差异 PASS。
- szy 与王昆本人确认精确协议 commit/manifest；随后才创建不可变 `protocol-v<semver>` tag/release。
- 两端启动时报告并验证同一完整 ProtocolReleaseIdentity；不匹配时拒绝进入 READY。

## D2 — 可构建、安装和启动

- 两个产品仓库从干净 checkout 使用 README 中唯一标准命令构建和测试。
- 发布候选包含版本 manifest、配置样例、数据库初始化/迁移、启动/停止方式、健康检查、日志路径和回滚说明。
- 在指定 Windows 环境完成安装、首次启动、正常停止和进程重启；不依赖原开发会话、未提交文件或 IDE 状态。
- 所有秘密由外部配置注入，仓库、日志、错误响应和发布物秘密扫描无可用凭据。

## D3 — 正常业务闭环

- 两端完成 session、能力/安全/恢复报告和五步 RecoveryHandshake，最终进入 READY。
- ControlServer 从现有 MesIngest V2 最终重读并恰好受理一个完整 WIRE_TO_GATE Demand，不重复受理或建单。
- 真实 RIoT 对同一车辆、Map、取货站和关卡站分别形成可对账的 TO_PICKUP 与 TO_GATE 移动并取得可信到站事实。
- OnboardHmi 完成一次 Sublot 输入、服务端校验、八仓模拟器上的冻结仓位集装货闭环、发车前新鲜安全检查和关卡自动批量卸货。
- 全部目标仓位最终 EMPTY、锁闭、开锁输出复位；服务端仅产生一个 StopClosureCommit 和一个 TransportDemandCompletion，不等待或回写 PDA/MES。

## D4 — 幂等、断联与恢复

- 相同 MessageId/业务键重放首个结果且无重复副作用；相同 ID 不同内容稳定冲突。
- 在 ACK、请求、结果、RIoT UNKNOWN、开锁准备/执行/结果和业务提交边界执行 drop/delay/duplicate/disconnect/crash/restart 后，系统保持原业务身份并得到唯一安全结论。
- 断联不得扩大 ActiveUnlockSet；安全收尾后暂停，重连必须重新握手并取得明确继续或 RECOVERY_REQUIRED。
- 任一歧义、UNKNOWN 或身份不匹配不得猜测成功、重复移动、重复开锁或静默 READY。

## D5 — OnboardHmi 与 IO 模拟器

- 1024×768、100% 缩放下，原型 A 的窗口层级、固定八仓位置、四维状态、当前作业、断联/恢复和安全阻断无关键裁切或危险滚动。
- 鼠标可完成全部触摸主流程；扫码键盘输入以 Enter 恰好提交一次，普通键盘可作为备用输入。
- 八仓模拟器与生产 HMI 只通过正式 IO 抽象交互，支持 EMPTY/OCCUPIED/UNKNOWN、锁反馈、开锁输出回读、模块离线和确定性故障脚本。
- 模拟器 PASS 只证明软件仓位闭环，不声称真实 IO、锁、光幕或车载硬件通过。

## D6 — 一致性与证据

- 每个 W2G-IS-00～07 均有 G1、双方 G2 和绑定精确两端构建的 G3 PASS；不存在未关闭的核心 FAIL/INCONCLUSIVE。
- 每次运行记录 runId、切片、两端 commit/build digest、协议身份、Fake 身份、runner/向量/配置哈希、结果和原始证据指针。
- 失败证据永久保留；修复使用新 runId，不覆盖旧结果。

## D7 — 发布和验收

- 三仓 release/tag 和安装物均已推送远程，可回读，SHA-256 与批准候选一致。
- 用户从干净环境按公开步骤启动两端并完成一次规定闭环，确认安装、操作、重启恢复、日志可诊断性和已知限制。
- 最终结论分别声明：软件/IO 模拟器可用、真实 RIoT 集成、目标车硬件资格、工厂试运行资格；不得把前一层 PASS 外推到后一层。

## 不允许为赶期删除

精确协议身份、每车凭证/TLS、持久 inbox/outbox/journal、幂等、发车前新鲜安全检查、断联安全收尾、重启对账、UNKNOWN 阻断、仓位结果逐仓闭环、原子完成和失败证据均不可砍除。

本周可以明确延后：真实八仓 IO 和工控机资格、真实物料 P0～P7、完整管理后台、高级报表、其它 WorkType、多车调度和自动充电。

