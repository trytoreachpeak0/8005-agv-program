# MesIngestWatch V2：WPF 自动化与视觉回归测试栈

研究日期：2026-08-04  
证据范围：官方文档、官方源码仓库、NuGet 元数据和 CI 平台文档。

## 决策摘要

采用一套分层而非单框架方案：

1. **关键操作旅程：保留 `FlaUI.UIA3 5.0.0`。** 它直接包装 Microsoft UI Automation，官方将 WPF 列为主要适用对象；5.0.0 明确增加 .NET 8 支持。仓库在 2026 年仍有活动，但正式版发布较慢，因此应锁定版本并通过原型压力测试验证，而不是无条件追随主分支。[FlaUI 官方说明](https://github.com/FlaUI/FlaUI)；[v5.0.0 发布说明](https://github.com/FlaUI/FlaUI/releases/tag/v5.0.0)；[FlaUI.UIA3 NuGet](https://www.nuget.org/packages/FlaUI.UIA3)
2. **页面级视觉回归：采用 `Verify.Xaml 4.2.1`。** 它能把 WPF `Window/Page/Control` 同时输出为 XAML 结构快照和 PNG 基线，适合使用固定假数据验证六个页面的正常、空、错误、离线和慢链路状态。官方明确提醒不同 Windows 版本会产生细微渲染差异，因此只能在固定环境中做强制门禁。[Verify.Xaml 官方仓库](https://github.com/VerifyTests/Verify.Xaml)；[Verify.Xaml NuGet](https://www.nuget.org/packages/Verify.Xaml)
3. **真实应用截图：由 FlaUI 在走完旅程后截取固定尺寸窗口，再交给 Verify/图像比较器产生 actual/expected/diff。** FlaUI 负责交互，不把它误当作完整的视觉 diff 产品；Verify.Xaml 负责确定性页面快照，真实窗口截图只覆盖少量高价值终态。
4. **测试承载：新建独立的 `MesIngest.Watch.UiTests`，使用 xUnit v3 + `Verify.XunitV3`。** 这样不必立即迁移现有全部测试；xUnit v3 的稳定包明确面向 .NET 8，`Verify.XunitV3` 在 2026-07-31 仍有正式发布。现有 xUnit v2 的 `Verify.Xunit` 已在 NuGet 标为 deprecated，不应给新套件引入。[xUnit v3 NuGet](https://www.nuget.org/packages/xunit.v3)；[Verify.XunitV3 NuGet](https://www.nuget.org/packages/Verify.XunitV3)；[xUnit v2→v3 迁移说明](https://xunit.net/docs/getting-started/v3/migration)
5. **CI：专用、自托管、交互式登录的 Windows runner，整机串行。** 固定 OS 镜像、主题、字体、语言、分辨率、100% DPI 和 .NET patch；agent 不作为 Windows Service 运行。Microsoft 明确要求桌面可见 UI 测试使用带自动登录的交互进程，并指出 RDP 断开造成锁屏会使测试失败。[Microsoft UI 测试 CI 约束](https://learn.microsoft.com/en-us/azure/devops/pipelines/test/ui-testing-considerations)；[Windows agent 的交互/自动登录模式](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/windows-agent)

## 仓库现状

- [`MesIngest.Tests.csproj`](../../../mes/ingest/csharp/MesIngest.Tests/MesIngest.Tests.csproj) 已引用 `FlaUI.UIA3 5.0.0`，目标为 `net8.0-windows`。
- [`MainWindowUiAutomationTests.cs`](../../../mes/ingest/csharp/MesIngest.Tests/MainWindowUiAutomationTests.cs) 只有一条“点击告警详情”的 UIA3 烟测；它在测试进程内手工创建 STA/Dispatcher 和 `MainWindow`，没有启动正式 Watch 可执行程序，尚不能证明真实启动、导航、分页、取消、离线恢复或慢 Host 时的响应性。
- 仓库当前未发现 GitHub Actions、Azure Pipelines 或同类 CI 配置，因此“作为合并门禁”需要新增运行环境和 required check，而不只是继续添加测试方法。

## 方案比较

| 方案 | 截至 2026-08-04 的状态 | 与 .NET 8 WPF 的关系 | 判断 |
|---|---|---|---|
| **FlaUI.UIA3 5.0.0** | 2025-02-25 发布，明确支持 .NET 8；官方组织页显示主仓库 2026-03 仍更新 | 原生 .NET，直接使用 UIA3；无 Node、WebDriver server 或 Developer Mode | **主选**。保留现有投资，补齐稳定定位、生命周期和诊断设施 |
| **Microsoft `winapp ui`** | 2026-07 才发布的 Public Preview/experimental 工具 | 官方表格宣称 WPF 支持完整 automation tree、属性、patterns 和截图；提供 CI 命令模式 | **观察/小范围试验**。太新，不作为 V2 唯一 required gate；可用于独立的 UIA tree 与截图诊断 [官方仓库](https://github.com/microsoft/winappCli)；[UI Automation 文档](https://learn.microsoft.com/en-us/windows/apps/dev-tools/winapp-cli/ui-automation) |
| **FlaUI.WebDriver** | FlaUI 官方组织维护，支持 .NET 8/WebDriver 协议 | 在 FlaUI 外再增加 server 和协议翻译层 | **不采用**。项目只有 C#/.NET 测试，没有跨语言或远程 WebDriver 需求，[官方仓库](https://github.com/FlaUI/FlaUI.WebDriver) |
| **Appium Windows Driver + WinAppDriver** | Appium 代理层仍活跃，但官方 README 警告底层 Microsoft WinAppDriver 已多年未维护；WinAppDriver 最后稳定版是 2020-11-05 | 支持 WPF，但需 Node/Appium/WinAppDriver/Developer Mode，多一组进程和版本 | **排除**。对单一 C# WPF 客户端没有收益，反而增加门禁故障面，[Appium Windows Driver 官方说明](https://github.com/appium/appium-windows-driver)；[WinAppDriver 官方仓库](https://github.com/microsoft/WinAppDriver) |
| **TestStack.White** | 官方仓库明确标为 deprecated；NuGet 0.13.3 发布于 2014，只目标 `net40` | 老 UIA 架构 | **排除**。官方本身指向 FlaUI 作为继任者，[官方仓库](https://github.com/TestStack/White)；[NuGet](https://www.nuget.org/packages/TestStack.White) |
| **直接调用 Microsoft UI Automation** | 平台 API 仍受支持 | 控制度最高，但需自行实现元素包装、等待、输入、恢复、截图与诊断 | **仅补缺口**。全面采用等同重造 FlaUI；WPF 自定义控件仍需 AutomationPeer，[WPF 自定义控件 UIA](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control) |

### 为什么现有 FlaUI 值得保留，但必须改造用法

FlaUI 官方说明 UIA3 对 WPF 工作良好，并可在包装层不足时访问原生 UIA 对象；NuGet 元数据显示 5.0.0 直接包含 `net8.0-windows7.0` 目标。因此当前版本与 Watch 技术栈匹配，不存在为了兼容 .NET 8 而迁移的理由。[FlaUI README](https://github.com/FlaUI/FlaUI)；[FlaUI.UIA3 5.0.0 元数据](https://www.nuget.org/packages/FlaUI.UIA3)

但当前测试把 UI 与测试放在同一进程，不能覆盖真实进程边界。V2 应改为：测试进程启动编译后的 Watch，可注入 fake Host 地址、固定用户设置路径和测试时钟；通过稳定 `AutomationProperties.AutomationId` 找元素；用 UIA `Invoke/Value/Selection` pattern 操作；仅在验证真实键盘、焦点和取消行为时使用坐标/键鼠输入。Microsoft 说明 AutomationId 是 UI 自动化定位的核心，但只保证同级唯一，仍需合理作用域；这意味着 ID 应作为公开的测试契约管理。[AutomationId 官方说明](https://learn.microsoft.com/en-us/dotnet/framework/ui-automation/use-the-automationid-property)

## 推荐测试结构

### 1. ViewModel/状态投影测试

这是最快且最稳定的必选门禁，覆盖导航状态、显式查询、分页游标栈、旧请求丢弃、取消、自动刷新不重入、陈旧状态和统计计算。它不需要图形桌面，应在普通 build agent 上并行执行。

### 2. Verify.Xaml 页面快照

每个页面使用确定性 ViewModel 和固定窗口尺寸直接验证 XAML + PNG：

- 概览：健康、部分退化、离线/陈旧；
- 运输需求：VISIBLE/GONE、正常/空/错误、详情面板、分页状态；
- 告警：聚合、历史、关联诊断；
- 性能：趋势、慢轮次、trace 下钻；
- 诊断：连接事件与导出状态；
- 设置：默认关闭自动刷新及频率配置。

Verify.Xaml 官方会同时保存结构化 XAML 和 PNG；结构快照能捕获布局属性变化，PNG 能捕获视觉变化，两者比单一截图更容易解释失败。[Verify.Xaml 用法与输出](https://github.com/VerifyTests/Verify.Xaml)

### 3. FlaUI 真实关键旅程

首批 required journeys：

1. 冷启动→概览首次加载→六页导航；
2. VISIBLE/GONE 切换→显式查询→下一页/上一页→刷新保留页与选中项；
3. Demand→Alert→Poll/trace 的关联下钻；
4. 手动刷新、启停自动刷新、慢请求不重入、取消请求；
5. Host 30 秒无响应时仍可导航并取消，旧响应不得覆盖新查询；
6. 断线→缓存陈旧标识→恢复连接；
7. 脱敏诊断包导出及完成提示。

关键业务断言使用 UIA 属性完成；每条旅程的终态可截窗口图，但不要在所有中间步骤做像素断言，以免维护成本失控。

## 视觉回归规则

- baseline PNG/XAML 纳入 Git；只能由人工评审后更新，CI 不得自动接受 received 文件。
- 固定浅色主题、中文 locale、指定字体、窗口客户区尺寸、测试数据、时钟、ID 和持续时间；关闭动画与系统通知。
- 测试进程可在专用测试启动参数下设置 WPF 软件渲染，以减少 GPU/驱动差异。Microsoft 说明 `RenderOptions.ProcessRenderMode = SoftwareOnly` 可避开许多外部渲染问题，但它只是偏好，仍可能被系统覆盖。[WPF ProcessRenderMode 官方说明](https://learn.microsoft.com/en-us/dotnet/api/system.windows.media.renderoptions.processrendermode)
- 不预先设置宽松容差。先在目标 runner 连跑 50 次，观察真实噪声后设定最小阈值；阈值和 mask 必须按截图记录理由，不能掩盖文字、图标、边距或状态色变化。
- 失败时上传 expected、actual、diff、UIA tree、Watch 日志、fake Host 请求日志和运行环境清单。
- 全窗口视觉回归先以非 required 的观察任务运行，连续稳定后才升级为 required；Verify.Xaml 的页面级快照可从原型阶段开始 required。

## Windows CI 合并门禁

推荐一个专用 Windows 11 或 Windows Server Desktop Experience VM：

- 以专用低权限测试账户自动登录，runner 作为交互进程启动，不作为 Windows Service；禁止睡眠、屏保和自动锁屏。
- 固定 1920×1080、100% DPI、主题、字体、语言、时区、OS patch、.NET 8 patch 和显示驱动；普通 RDP 断开会锁定会话，需按 Microsoft 指南切回 console session。
- 整台 runner 同时只执行一个 UI job；在测试程序集内也禁用并行，因为焦点、剪贴板、键鼠和桌面是共享状态。
- 每条测试独占设置/临时目录；setup 清理残留 Watch，teardown 关闭子窗口与进程。测试只连接本机确定性 fake Host，不依赖 MES、Oracle、SQL Server 或生产网络。
- 元素等待采用明确 deadline 和轮询，禁止用固定长 `Sleep`；测试失败可以采证，但不能用整条测试无条件重跑来伪造绿色。
- required checks 至少分成 `watch-vm-tests`、`watch-xaml-visual`、`watch-ui-journeys`。真实窗口像素门禁在校准期后再设为 required。

不建议视觉门禁使用 `windows-latest`：GitHub 官方 runner image 通常每周更新，且 `-latest` 会迁移到新 OS；这会直接污染字体与渲染基线。即使使用托管 runner 做探索，也应固定如 `windows-2025` 的显式标签；强视觉门禁仍以可冻结的自托管镜像为准。[GitHub runner images 的更新与迁移策略](https://github.com/actions/runner-images)；[GitHub-hosted runners 规格](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)

## 实施前验证门槛

在原型上完成一次短 POC，再把选择固化：

1. 为 DataGrid、虚拟化列表、分页器、图表和自定义控件导出 UIA tree，确认关键节点、名称、状态和 patterns 可见；不可见的自定义控件补 `AutomationPeer`。
2. 在目标 runner 上连续执行至少 50 次上述关键旅程，分别统计产品失败、框架失败和环境失败；框架/环境 flake 未降到可接受水平前不得作为 required gate。
3. 同一页面快照重复 50 次应零意外 diff；若有噪声，先固定环境或冻结动态数据，再考虑最小容差。
4. 用 30 秒 fake Host 延迟验证窗口不会“未响应”，期间可导航、取消，测试进程和 Watch 进程均无持续内存增长。
5. 将 `winapp ui` 只作为对照试验：若它在托管 Windows runner 上对本项目连续稳定，未来可用于轻量 smoke/诊断；在其 Public Preview 阶段不替换 FlaUI required journeys。

## 最终建议

**现在就决定：FlaUI.UIA3 5.0.0 + Verify.Xaml 4.2.1 + 独立 xUnit v3 UI 测试项目 + 专用交互式自托管 Windows runner。**

这套方案保留现有可用投入，同时把“功能正确”“页面结构/视觉正确”“真实操作链路正确”拆成各自可诊断的门禁。Appium/WinAppDriver、White 和 FlaUI.WebDriver 均不会改善当前单一 .NET WPF 项目的稳定性；新 `winapp ui` 值得跟踪，但截至本研究日期尚不适合承担唯一的合并门禁。
