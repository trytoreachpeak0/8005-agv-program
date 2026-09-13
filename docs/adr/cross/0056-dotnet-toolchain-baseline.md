# 全工作区统一 .NET 工具链基线，并靠构建失败而非文档来维持

工作区的四个可写 .NET 仓库统一到一套工具链：SDK **8.0.425**（`rollForward: disable`）、运行时目标 **net8.0** 或 **net8.0-windows**、测试栈 **xunit.v3 3.2.2** + **Microsoft.NET.Test.Sdk 18.8.1** + **xunit.runner.visualstudio 3.1.5**。禁用 xunit v2、NUnit、MSTest 与 coverlet.collector。基线不靠 agent 自觉遵守文档，而是由四层机制维持，任何一层被违反都直接导致 `dotnet build` 失败或检查脚本返回非零。

采纳这条的直接原因是 2026-09-02 的一次盘点：`8005-mes-ingest` 与 `riot-sdk` 都没有 `global.json`，于是它们用机器上装的 **SDK 10.0.302** 去构建 net8 目标；同一个仓库里 `MesIngest.Tests` 是 xunit 2.4.2 而 `MesIngest.Watch.UiTests` 是 xunit.v3 3.2.2；`8005-agv-program` 明明没有任何 `.csproj`，却带着一份从拆分前继承来的 `global.json`。这些都不是谁写错了，而是没有任何机制阻止它发生——每个 agent 在自己那次任务里选的版本都是合理的。

**Status**: accepted

**Considered Options**:
- 只把基线写进各仓 `CLAUDE.md`，靠 agent 阅读遵守（拒绝：软约束，不读就失效，正是漂移的成因）
- 建立 monorepo 或共享 MSBuild 包统一配置（拒绝：七个仓库分属两人、两个只读，且共享包本身又需要版本管理）
- 每仓落地四层强制机制，真相来源写在本 ADR（采纳）

**Consequences**:
- 第一层 `global.json` 锁死 SDK，`rollForward: disable` 使版本不匹配时直接报错而不是静默回落。
- 第二层 `Directory.Packages.props` 集中管理版本。**这一层没有构建期强制力，本条原先写的「内联 `Version=` 会触发 NU1008」是错的**（2026-09-04 在 `8005-mes-ingest` 落地时实测推翻）：CPM 生效时 NuGet 在项目求值早期就把 `Version` 元数据抹掉，一个写着 `Oracle.ManagedDataAccess.Core 23.6.0` 的项目照样解析到中央的 `23.9.0`，没有 NU1008、没有警告，连 MSBuild target 里读到的 `%(PackageReference.Version)` 都是空的。`CentralPackageVersionOverrideEnabled=false` 管的是 `VersionOverride` 属性，不是 `Version`。**后果是版本本身不会漂移——中央值总是赢——但写了内联版本的人不会被告知它被忽略了。**捕获它只能靠读源码文本，那是 `check-toolchain.ps1` 的职责（它已有这个分支）。不要再为此写 MSBuild 守卫：写过一个，它对每一个本该失败的用例都静默通过，已删除。
- 第三层 `Directory.Build.props` 统一 `TargetFramework` 与 `LangVersion`；`8005-mes-ingest` 同时有 net8.0 与 net8.0-windows 两种目标，那里只统一 `LangVersion`。
- 第四层 `Directory.Build.targets` 的禁用包守卫在构建期报 `<Error>`。它随 `MesIngest.Tests` 的 v3 迁移一起启用——先装守卫会让该项目立刻构建失败，而留豁免等于留后门。**2026-09-04 在 `8005-mes-ingest` 落地并验证：**故意加一个 `<PackageReference Include="xunit" />` 会得到 `error W2G0056` 并 Build FAILED，而同一次构建里 `xunit.v3` 不受影响——守卫用 item identity 精确匹配，`xunit.v3` 不是 `xunit`。同日 `8005-agv-control-server` 与 `riot-sdk` 也各自装上并验证（分别用 `NUnit` 和 `coverlet.collector` 试出 `error W2G0056`），**三个可写 .NET 仓四层齐备**。`8005-agv-protocol` 是 node 项目，没有 `.csproj`，不适用。守卫在各仓是独立拷贝——这些仓是彼此独立的克隆、没有共享包——所以改动它时三份要一起改。
- 工作区根的 `check-toolchain.ps1` 扫描全部七个仓库并列出偏离；可写仓有偏离则退出码为 1。`8005-agv-onboard-hmi` 与 `slots-simulator` 属于 Kun Wang，只报告不修改，也不影响退出码。
- `8005-agv-onboard-hmi` 自身也存在同类分裂（`SQCD.Agv.UnitTests` 是 xunit v2、`SQCD.Agv.WireToGateG2Tests` 是 v3），`slots-simulator` 的两个测试项目则完全没有测试框架，是 `OutputType=Exe` 的自建断言程序。这些通过 issue 告知，不代为修改。
- `8005-agv-program` 无代码，其 `global.json` 已删除。
- 升级基线时改本 ADR 与各仓的三个 props 文件，`check-toolchain.ps1` 顶部的 `$Baseline` 随之更新，不允许个别仓单独领先或落后。**协议仓 `compatibility/implementation-version-matrix.json` 的 `sharedDevelopmentBaseline` 也要一起改**——它是 `global.json` 之外唯一一份基线复述，`check-toolchain.ps1` 拿它的 `dotnetSdk` 对照 `$Baseline`、`dotnetRuntime` 对照已装基线 SDK 自带的运行时。在此之前 G1 拿脚本里硬编码的同一对字符串去断言它，于是 8.0.425 升级时两份一起过期、一起绿了一天（[#36](https://github.com/trytoreachpeak0/8005-agv-program/issues/36)）。
- **2026-09-09 基线由 8.0.424 抬到 8.0.425，起因是 Windows Update 而非主动选型。**.NET SDK 的补丁更新经 Microsoft Update 分发，会**替换**同一 feature band 内的旧版本：控制端当天装了 `KB5126052` 与 `KB5124008` 之后，`C:\Program Files\dotnet\sdk` 下只剩 `8.0.425`，`8.0.424` 的目录不复存在，机器上也没有第二份，于是四个仓在那台机器上全部构建失败——**这正是第一层机制的预期表现，不是故障**。选择抬基线而不是把旧版本装回去，是因为该渠道已经取不回旧版本，而 `rollForward: disable` 的价值在于版本明确、可复现，不在于停在某个具体数字。**升级时 CI runner（`win11-01`）必须一起升**，否则它会变成唯一落后的那台，而门禁证据正是在它上面产出的。
