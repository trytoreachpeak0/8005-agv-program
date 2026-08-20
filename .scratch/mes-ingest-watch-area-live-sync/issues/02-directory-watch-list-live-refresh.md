# 02 — 目录里新增/删除的配置自动进出列表

**What to build:** 用户往配置目录里放一个新的 AREA 配置 TXT，不需要任何操作，它就出现在左侧筛选配置列表里；把文件删掉，它就从列表消失。页面顶部的「重新加载」按钮随之移除。列表刷新时用户当前选中的配置不变、焦点不被抢走。

本 ticket 只实现自身需要的事件解释规则——去抖、伴生文件过滤、扩展名二次校验。删除延迟确认与改名跟随属于 04，缓冲区溢出兜底属于 12。事件解释是逐个 ticket 加厚的，不在这里一次写完。

**Blocked by:** 01

**Status:** done

- [x] 配置目录新增 TXT 后列表自动出现该项，无需手动操作
- [x] 目录中删除 TXT 后列表自动移除该项
- [x] 列表刷新不改变当前选中项，不抢走焦点
- [x] 编辑器伴生文件不进入列表：点开头的、非 TXT 扩展名的、带隐藏或系统属性的
- [x] 一次性放入多个文件时列表只刷新一次
- [x] 页面级「重新加载」按钮不复存在，引用它的测试断言同步调整
- [x] 目录事件源作为 `WatchAreaFilterProfileStore` 的可选构造参数注入，与既有的时钟、删除委托注入模式一致
- [x] 测试使用手动驱动的事件源与 `FakeTimeProvider`，**不出现真实等待**
- [x] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。

## Comments

### 实现记录

**目录事件源**（新文件 `MesIngest.Watch/WatchAreaProfileDirectoryEvents.cs`）：
`IWatchAreaProfileDirectoryEventSource` 只发原始事件（`Created`/`Changed`/`Deleted`/`Renamed`
加文件名），默认实现 `WatchAreaProfileDirectoryWatcher` 是包裹 `FileSystemWatcher` 的薄适配层，
按 spec 不单测。

**事件解释**留在 `WatchAreaFilterProfileStore`，作为可选构造参数 `directoryEventSource` 注入，
与 `timeProvider`、`deleteProfileFile` 同一模式。store 对外只暴露已解释的 `DirectoryChanged`
（载荷是本次窗口内受影响的配置名集合）。本 ticket 实现的规则：

- 去抖：`DirectoryChangeDebounceWindow` = 250 ms，用注入的 `TimeProvider.CreateTimer`。
  窗口锚在**一批事件里的第一个**上，不随后续事件顺延——否则持续写盘的编辑器可以把刷新
  无限期推后。
- 伴生文件过滤 + 扩展名二次校验：点开头、非 `.txt`、名字不能作为本地文件名的一律丢弃
  （`FileSystemWatcher` 的 `*.txt` 过滤会命中 8.3 短名，所以 `plan.txtbackup` 必须在回调里再挡一次）。
- 隐藏/系统属性的 TXT 既不通知也不进入 `EnumerateProfiles`。

watcher 生命周期归 store：`StartWatchingDirectory()` 幂等启动、启动失败时回滚到未启动状态以便重试，
`Dispose()` 停止并释放去抖定时器。自身写入抑制、删除延迟确认、编辑器改名跟随、溢出兜底不在本
ticket，留给 03/04/12。

`Renamed` 保留为「新旧两个名字都算目录变化」，不是提前做 04 的改名跟随：本项目自身的原子写入与
记事本、VS Code 的保存都是「写临时文件再改名」，忽略 `Renamed` 会让新增的配置进不了列表。
04 要做的是**编辑器**跟随到新名字。

**界面**：`AreaProfileReloadButton` 与 `OnAreaProfileReloadClick` 删除；窗口在构造时订阅
`DirectoryChanged`，回调切回 UI 线程后只刷新列表——`ReloadAreaProfileRows(..., reloadSelectedDraft: false)`
不重新读取选中配置的正文，因此编辑器缓冲、光标、滚动位置一律不动（跟随磁盘内容是 03 的事），
也不调用任何 `Focus`。事件源经 `WatchV2ApplicationComposition.Create` 可注入，与
`areaProfileDirectoryLauncher` 同一模式。

**测试**：

- 存储层 `MesIngest.Tests/WatchAreaFilterProfileDirectoryWatchTests.cs`（10 例）——真实临时目录 +
  `ManualTimerTimeProvider` + 手动事件源，全类 43 ms，无真实等待。
- 界面层 `MesIngest.Tests/WatchAreaProfileLiveListTests.cs`（7 例）——真实生产窗口，断言重新加载
  按钮不存在、新增/删除自动进出列表、刷新后选中项/草稿/编辑器光标/逻辑焦点不变、伴生文件不进列表、
  目录不可监视时给出降级提示。
- 抽出两个共享测试件：`ManualTimerTimeProvider.cs`（原来 `WatchV2ProductionShellTests` 里的私有副本）
  与 `StaTestRunner.cs`。`WatchV2AutoRefreshTests` 有未提交的在途改动，未一并合并它那份副本。
- tier 2 的 `WatchTicket21AreaAndResponsiveIntegrationTests` 原来点「重新加载」并断言 InfoBar 文案，
  改为写入文件后等待列表自动跟随（真实 watcher + 去抖，10 s 超时）。

测试：`dotnet test MesIngest.Tests` — 489 通过、82 跳过（无 LocalDB）、2 失败。两处失败与本改动无关，
与 ticket 01 记录的是同两例：

- `WatchV2ProductionShellTests.Production_composition_creates_the_six_page_fluent_v2_shell_without_forbidden_refresh_controls`
  —— 本机显示缩放导致窗口高度 885.33 ≠ 断言的 900。
- `RetiredContractAndCutoverSafetyTests.The_attended_cutover_drill_is_the_only_thing_that_deletes_a_database`
  —— 由工作区里未跟踪的打包输出 `dist/MesIngest/scripts/cutover/CutoverSqlTools.ps1` 触发。

### 评审留下的两点，本 ticket 不处理

- `docs/agents/watch-ui-system.md` 要求自动刷新的页面显示被动的刷新上下文。AREA 页不走
  自动刷新间隔体系，spec 把「同步时刻」放进编辑器底部状态条，属于布局 ticket 09。
- `EnumerateProfiles` 现在隐藏带隐藏/系统属性的 TXT，而 `Load`/`Save`/`Delete` 仍能作用于它们。
  界面走不到这条路径（`SaveAs` 用 `File.Exists` 仍会拒绝覆盖，`Save`/`Delete` 需要来自列表的指纹），
  改动存储层语义超出本 ticket。
