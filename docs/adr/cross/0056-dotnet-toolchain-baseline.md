# 全工作区统一 .NET 工具链基线，并靠构建失败而非文档来维持

工作区的四个可写 .NET 仓库统一到一套工具链：SDK **8.0.424**（`rollForward: disable`）、运行时目标 **net8.0** 或 **net8.0-windows**、测试栈 **xunit.v3 3.2.2** + **Microsoft.NET.Test.Sdk 18.8.1** + **xunit.runner.visualstudio 3.1.5**。禁用 xunit v2、NUnit、MSTest 与 coverlet.collector。基线不靠 agent 自觉遵守文档，而是由四层机制维持，任何一层被违反都直接导致 `dotnet build` 失败或检查脚本返回非零。

采纳这条的直接原因是 2026-09-02 的一次盘点：`8005-mes-ingest` 与 `riot-sdk` 都没有 `global.json`，于是它们用机器上装的 **SDK 10.0.302** 去构建 net8 目标；同一个仓库里 `MesIngest.Tests` 是 xunit 2.4.2 而 `MesIngest.Watch.UiTests` 是 xunit.v3 3.2.2；`8005-agv-program` 明明没有任何 `.csproj`，却带着一份从拆分前继承来的 `global.json`。这些都不是谁写错了，而是没有任何机制阻止它发生——每个 agent 在自己那次任务里选的版本都是合理的。

**Status**: accepted

**Considered Options**:
- 只把基线写进各仓 `CLAUDE.md`，靠 agent 阅读遵守（拒绝：软约束，不读就失效，正是漂移的成因）
- 建立 monorepo 或共享 MSBuild 包统一配置（拒绝：七个仓库分属两人、两个只读，且共享包本身又需要版本管理）
- 每仓落地四层强制机制，真相来源写在本 ADR（采纳）

**Consequences**:
- 第一层 `global.json` 锁死 SDK，`rollForward: disable` 使版本不匹配时直接报错而不是静默回落。
- 第二层 `Directory.Packages.props` 集中管理版本，配 `CentralPackageVersionOverrideEnabled=false`，项目内联 `Version=` 会触发 NU1008。
- 第三层 `Directory.Build.props` 统一 `TargetFramework` 与 `LangVersion`；`8005-mes-ingest` 同时有 net8.0 与 net8.0-windows 两种目标，那里只统一 `LangVersion`。
- 第四层 `Directory.Build.targets` 的禁用包守卫在构建期报 `<Error>`。它随 `MesIngest.Tests` 的 v3 迁移一起启用——先装守卫会让该项目立刻构建失败，而留豁免等于留后门。
- 工作区根的 `check-toolchain.ps1` 扫描全部七个仓库并列出偏离；可写仓有偏离则退出码为 1。`8005-agv-onboard-hmi` 与 `slots-simulator` 属于 Kun Wang，只报告不修改，也不影响退出码。
- `8005-agv-onboard-hmi` 自身也存在同类分裂（`SQCD.Agv.UnitTests` 是 xunit v2、`SQCD.Agv.WireToGateG2Tests` 是 v3），`slots-simulator` 的两个测试项目则完全没有测试框架，是 `OutputType=Exe` 的自建断言程序。这些通过 issue 告知，不代为修改。
- `8005-agv-program` 无代码，其 `global.json` 已删除。
- 升级基线时改本 ADR 与各仓的三个 props 文件，`check-toolchain.ps1` 顶部的 `$Baseline` 随之更新，不允许个别仓单独领先或落后。
