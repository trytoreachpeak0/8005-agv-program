# 27 — 降低打包 Watch 的冷启动耗时

**What to build:** 让从安装包首次启动的 `MesIngest.Watch.exe` 在校准黄金机上明显更快地显示主窗口，并把改善做成可持续观测的证据，而不是一次性调参。

**Blocked by:** 无

**Status:** needs-triage

## 背景

票 24 把「打包 Watch 启动耗时」从人工目测改成了发布烟测里的实测：
`Stopwatch` 从 `Process.Start` 计到 `MainWindowHandle` 非零，实测值写入
`release-smoke-result.json` 的
`servicePollOwnership.watchIndependence.startupToMainWindowMs`。

实测（2026-08-19，gpt_win11，1920x1080 / 96 DPI / SoftwareOnly，同一份产物）：

| 轮次 | startupToMainWindowMs |
| --- | --- |
| `run-20260819-165547` | 14,009.7 |
| `run-20260819-170420` | **6,330.2** |
| `run-20260819-172045` | 14,040.1 |

分布明显双峰，两个 14.0 秒的点彼此只差 30 毫秒，这不像纯噪声，更像是有一条会命中
的慢路径（例如某次首用初始化、缓存未命中或资源争用）。查因时先解释这个双峰，
而不是取平均。

票 13 当初把人工检查项命名为 `startup-within-10-seconds`，但全仓库只有
`Invoke-GoldenRendererValidation.ps1` 的 `$requiredChecks` 里出现过这个名字，
从来没有任何测量支撑它。票 24 按实测把上限改为 25 秒、检查项改名为
`startup-within-25-seconds`，并明确记录这是**按实测设定，不是把失败调绿**。

## 已排除的原因

- **不是应用逻辑。** `App.OnStartup` 只做 `WatchOptionsLoader.Load`、
  `WatchProcessFileLocations.Resolve`、`WatchV2ApplicationComposition.Create`，
  `CreateMainWindow()` 只读两个小偏好文件就 `Show()`；契约发现与首屏数据是
  `initializeOnLoaded: true` 在 `Loaded` 之后才发起，不阻塞窗口出现。
- **不是 Host 或 SQL Server。** 计时只覆盖 Watch 进程自身到窗口出现。

剩余怀疑集中在自包含发布的冷启动本身：JIT、程序集加载、WPF 与 Wpf.Ui
Fluent 主题资源字典的首次解析，叠加 4 GB 虚机与 SoftwareOnly 渲染。

## 需要判断的事

- [ ] 拆解 14 秒的构成（进程创建 / 运行时启动 / 程序集加载 / BAML 与主题字典解析），
      用可复现的测量而不是猜测。
- [ ] 评估 ReadyToRun 或分层编译设置对冷启动的影响，并确认它不改变 UI 输出——
      若改变 PNG/XML/UIA/DPI 输出，按票 23 规则使相应场景失效并只重跑受影响门禁。
- [ ] 评估 Fluent 主题字典的加载方式是否可延后或裁剪。
- [ ] 区分「黄金机资源受限」与「产物本身偏慢」：同一产物在物理机上的冷启动作为对照。
- [ ] 改善后按新的实测值收紧 `-PackagedWatchStartupBudgetSeconds` 默认值与
      `startup-within-NN-seconds` 检查项名，两者必须同步。

## 备注

黄金机计时噪声不小：同一份代码的两轮发布烟测总耗时为 50.7 s 与 73.0 s。
任何结论都要基于多次测量，不能用单次数字定上限。
