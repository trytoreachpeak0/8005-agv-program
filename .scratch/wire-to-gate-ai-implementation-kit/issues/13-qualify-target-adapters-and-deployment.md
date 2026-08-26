# 验证真实适配器、目标部署与硬件边界

Type: task
Mode: HITL
Status: open
Blocked by: 11

## Question

在用户授权且安全条件满足后，如何在指定目标环境验证 ControlServer 连接现有 MesIngest 和真实 RIoT，以及 OnboardHmi 的屏幕、触摸、扫码枪和八仓 IO 模拟器，执行安装、配置、启动、连接、只读冒烟以及获准的最小 RIoT 移动，并记录每个适配器是 PASS、FAIL 还是因外部输入 INCONCLUSIVE？真实八仓 IO 资格留作后续硬件门禁，不阻断本轮模拟 IO 软件交付。

不得用 Fake 或 HTTP mock 替代真实 RIoT 集成，不得把测试凭据写入仓库或证据。任何车辆移动或现场部署必须在当轮得到明确授权并由具名安全负责人监督；未授权时本票只能完成只读核验并记录阻断。IO 模拟器动作不属于真实车辆 IO 输出，但仍须明确标识为模拟。
