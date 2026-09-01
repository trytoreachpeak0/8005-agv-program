# 生成双仓薄 Spec、项目骨架与可执行测试入口

Type: task
Mode: AFK
Status: resolved
Blocked by: 02, 03, 04, 05, 06

## Question

如何在同一候选协议身份和 W2G-IS-00～07 边界下，把最薄可执行 `docs/ai-spec/`、生产项目骨架、配置样例、Fake 对端、测试项目和统一构建入口分别落入真实 ControlServer 与 OnboardHmi 开发分支，使双方第 1 天结束前可以开始写产品代码并运行第一个失败测试？

两套 Spec 必须给出各切片的权威、事务/持久化边界、接口契约、失败与恢复路径、验收和禁止副作用，并准确落到真实项目、命名空间、配置、构建/测试入口和允许修改文件。车载骨架必须建立原型 A 的生产映射入口并区分 Fake IO 与真实 IO；服务端骨架必须建立 MesIngest/RIoT 的端口与 Fake。不得把生成骨架或 Spec 误报为 MVP 软件实现完成。

## Answer

已在两个真实开发分支生成、验证并推送同一候选协议身份下的最薄可执行骨架。两端都绑定协议候选 commit `72ddde595165468520d9f3a46b25e4aa4eec0c3f` 与 manifest SHA-256 `e878d89e820535fe1eb64b85681b9c2994fb98646309e6ba768219c5c8735f2e`，并冻结 `global.json` SDK `8.0.424`、`net8.0`/`net8.0-windows`、C# 12、`win-x64`、中央 NuGet 版本和锁文件。当前机器使用隔离 SDK `C:\Users\szy\Desktop\xinji\dotnet-8.0.424\dotnet.exe` 验证；脚本可通过 `WIRE_TO_GATE_DOTNET_EXE` 选择精确 SDK，不硬编码本机路径。

ControlServer 已推送 `ControlServer_MVP` 提交 `6ff2d7c`。仓库包含 Domain/Application/Infrastructure/Host、Windows Service 入口、SQLite DbContext、MesIngest/RIoT/Onboard/持久化端口、Fake Onboard、Conformance 工具、`docs/ai-spec/`、W2G-IS-00～07 索引和统一 build/test 脚本。`Release` 构建实测 0 warning/0 error；W2G-IS-01 首条测试被 xUnit v3/VSTest 真实发现并按预期红灯，失败点是 Demand 受理与 ToPickup 意图尚未原子实现，而不是测试发现失败。

OnboardHmi 已先将 `OnboardHmi_MVP` 快进到王昆真实推送的 `bc56fa9` 初始代码，再推送骨架提交 `2eeecf6`。仓库保留既有可运行基线并增加正式 `ISlotIoProvider` 业务抽象、候选会话规划入口、HTTP 模拟/真实硬件 Provider 分离边界、原型 A 到生产 WPF 的映射文档、`docs/ai-spec/` 和统一脚本；旧 xUnit 测试迁移到冻结的 xUnit v3 运行栈。`Release` 构建实测 0 warning/0 error，既有测试 48/48 通过；W2G-IS-00 首条候选握手测试被真实发现并按预期红灯，失败点是 `SessionHello` 尚未从物化协议 Schema 实现。

两仓提交前均完成差异检查和秘密扫描。上述结果只表示开发骨架、导航和首条红测试可用，不表示 W2G-IS-00～07 产品代码、G2/G3、安装包或整个 MVP 已完成；协议仍为 `CANDIDATE_UNAPPROVED`。
