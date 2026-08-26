# 发布并交接可运行 WIRE_TO_GATE MVP

Type: task
Mode: HITL
Status: open
Blocked by: 12

## Question

如何创建并回读三个远程仓库的正式 tag/release，发布经过批准的安装物与哈希，并把安装、配置、启动、停止、健康检查、日志、恢复、回滚、已知限制和支持责任交给使用者，使其无需旧会话即可实际运行本次 MVP？

交接必须证明远程 release 可访问、干净环境安装可复现、ControlServer 与 OnboardHmi 报告同一 ProtocolReleaseIdentity、核心端到端场景 PASS；真实硬件或现场未获资格时必须醒目标记，不得把受控测试可用扩大为工厂生产可用。

开发文档可以随软件附带，但不能成为交付主体，也不能替代任何失败的软件门禁。最终交付判定是“程序能安装、运行并完成规定业务闭环”，而不是“AI 可以开始开发”。
