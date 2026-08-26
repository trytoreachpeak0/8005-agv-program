# 取得王昆的 OnboardHmi 与 IO 模拟器决定

Type: grilling
Mode: HITL
Status: resolved
Blocked by: 01

## Question

王昆是否接受 OnboardHmi 与协议仓库邀请，并决定 OnboardHmi 的语言/UI 框架、运行时、持久化方式、构建测试入口，以及八仓 IO 模拟器的协议、进程边界、地址、八仓初始状态和故障注入方式？

决定必须兼容 1024×768、100% 缩放、Windows 10/11 虚拟工控机、鼠标操作、Enter 结束符和普通键盘，并保持原型 A 为生产布局/交互权威。OnboardHmi 同样遵守“成熟复用优先”：UI 框架、MVVM、日志、配置、SQLite/迁移、Modbus、JSON/Schema 和测试尽量使用维护活跃、许可证兼容、版本可锁定的成熟库；只自行实现车载领域状态机、安全/恢复不变量、生产 UI 映射和薄适配器。最迟须在 2026-08-25 冻结到仓库；若无法及时取得，必须将其标为截止风险，而不是由 ControlServer 开发者替王昆无声决定。

## Comments

### 2026-08-25 — 第 1 轮决策前沿（等待王昆本人回复）

1. **仓库访问**：是否已用 `SocialKKKK` 接受 `8005-agv-onboard-hmi` 和 `8005-agv-protocol` 的两项邀请，并在王昆自己的开发机上验证 OnboardHmi 的 clone/fetch/push 以及协议仓库的 clone/fetch？推荐立即完成，回复只写账户、仓库、分支和成功/失败，不粘贴任何凭据。
2. **OnboardHmi 技术基线**：是否接受 C# / .NET 8 WPF 的推荐基线：与 ControlServer 对齐 SDK `8.0.424`、runtime `8.0.30`，`net8.0-windows` / `win-x64` 自包含非单文件发布；原生 WPF XAML 映射原型 A；Generic Host/DI/配置；`CommunityToolkit.Mvvm`；EF Core SQLite `8.0.30` 单写者 journal；Serilog JSONL；xUnit `3.2.2`；统一 `dotnet restore/build/test/publish` 和 `test-wire-to-gate` 入口？同时请回复目标虚拟工控机的 Windows 版本/版本号与 x64 架构。
3. **八仓 IO 模拟器**：是否接受独立 `.NET 8` 进程 `OnboardIoSimulator`，只在 `127.0.0.1:58006` 暴露版本化 HTTP/JSON 测试契约，生产 HMI 只依赖正式 `ISlotIoProvider` 抽象？推荐八仓初始均为 `online + EMPTY + LOCKED + unlock output RESET + light curtain clear`，全局急停释放；提供确定性 reset/revision，并可注入离线、超时/过期、占用 UNKNOWN、锁反馈异常、输出粘连、结果丢失/未知和进程崩溃/重启。它不模仿未知的真实 IO 协议，也不生成真实硬件资格。

王昆可直接回复“Q1 实际结果；Q2 接受推荐/改为…；Q3 接受推荐/改为…”。未取得本人回复前，不由其他开发者或 AI 代答。

## Answer

王昆本人已于 2026-08-25 完成仓库访问验证并冻结 OnboardHmi/IO 技术决定，不再由 ControlServer 开发者或 AI 代答。

### 仓库与权限

- `8005-agv-onboard-hmi` 的 clone/fetch/push 均成功，已向 `main` 真实推送车载端初始代码，提交为 `bc56fa9`。
- `8005-agv-protocol` 的 clone/fetch 成功，`push --dry-run` 成功；没有为权限测试制造无意义 commit。
- 两仓与所需分支的权限可用。因本机无 GitHub CLI，Git Credential Manager 不显示凭据用户名，所以终端证据只证明权限有效，不将凭据账户无证据地写为 `SocialKKKK`。

### OnboardHmi 技术基线

冻结 C# / .NET 8 / WPF / x64，接受 `CommunityToolkit.Mvvm`、EF Core SQLite、Serilog 和 xUnit。当前车载代码已使用 C#、.NET 8、WPF 与 xUnit；现有自定义 MVVM 基类和文件日志可渐进迁移，不得为迁移破坏已有业务逻辑。SQLite 只持久化车载操作 journal、待确认结果与幂等状态，不把 ControlServer 业务数据库责任下沉到车载端。

当前开发机身份为 Windows 11 家庭中文版，系统版本/Build `10.0.26200` / `26200`，64 位，`x64` / `win-x64`；已安装 .NET 8 Runtime 与 Windows Desktop Runtime `8.0.29`，现有项目目标为 `net8.0` / `net8.0-windows`。这只是开发机资格，另一台虚拟工控机必须在安装验证时独立回读，不得沿用本机结论。

双端共同使用的 SDK/runtime 基线、目标框架、NuGet 版本和兼容约束必须在候选协议仓库登记并绑定精确 manifest；它是实施兼容性元数据，不把两端私有实现细节错当成 wire payload。候选骨架仍以 ControlServer 已冻结的 SDK `8.0.424`、runtime `8.0.30` 为对齐目标；开发机当前 `8.0.29` 的实际偏差必须在构建前消解或以可重复的 pinned SDK 构建。

### 八仓 IO 模拟器

冻结为独立 .NET 8 进程，默认在可配置的 `127.0.0.1:58006` 上提供版本化 HTTP/JSON 接口。车载业务层只依赖正式 `ISlotIoProvider`；模拟器由 `HttpSimulatorSlotIoProvider` 接入，真实硬件另用 `ModbusSlotIoProvider` 或获批的硬件 Provider，不让模拟器契约渗入业务状态机。

八仓初始均为在线、空仓、门已锁、开锁输出已复位、光幕清晰；支持离线、响应超时、状态 `UNKNOWN`、锁反馈异常、输出粘连、请求/结果丢失和模拟器崩溃/恢复。对业务层只暴露 `Empty / Occupied / Clear / Blocked / Unknown` 等规范状态，不暴露容易反转误解的 DI 原始值。当前现场极性事实为空仓时光幕 `DI=1`、有货时 `DI=0`，它只存在真实 Provider 的转换边界。

现有旧 IO 模拟器虽是独立 .NET 8 进程，但使用 `127.0.0.1:1502` Modbus TCP；它不会被无声当成新 `58006` HTTP/JSON 契约。后续通过正式 Provider 适配或改造模拟器，并始终只声明车载软件闭环，不声明真实 IO 协议或硬件资格。
