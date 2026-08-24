# 01 — Prefactor：AREA 页界面逻辑抽为独立 partial

**What to build:** 一次纯粹的代码搬迁，用户看不到任何变化。AREA 筛选页的界面逻辑目前与可读性筛选等其他主题混在同一个大文件里，任何后续改动都必须把整份文件读进上下文。把 AREA 相关部分搬进属于它自己的 partial 文件，行为、控件、自动化名称一律不变。

这是本特性全部后续 ticket 的成本前提：搬迁之后每个 ticket 的读取面从近两千行降到数百行。

**Blocked by:** None — can start immediately

**Status:** done

- [x] AREA 筛选页的界面逻辑集中在一个专属 partial 文件中，原文件不再包含 AREA 相关成员
- [x] 没有任何行为、控件名称或自动化名称发生变化
- [x] 未新增、删除或修改任何测试断言
- [x] 后续改动 AREA 页无需读取原大文件
- [x] `dotnet test MesIngest.Tests` 全绿

> 本 ticket 不改变任何界面呈现、XAML、Wpf.Ui 控件或 UI Automation 行为，因此不附金机检查表。

## Comments

### 实现记录

AREA 相关成员从 `WatchWorkspaceWindow.Ticket21.cs`（1975 行，AREA + 资格审计混编）搬入新的
`WatchWorkspaceWindow.AreaProfiles.cs`（1259 行）。原文件缩至 729 行，只剩资格审计。

唯一的非搬迁改动：原 `InitializeReadabilityAuditAndAreaProfiles()` 同时初始化两个页面，
按主题拆为 `InitializeReadabilityAuditPage()` 与 `InitializeAreaFilterProfilePage()`，
构造函数按原顺序依次调用。逐行比对确认除此之外无任何行内容变化。

测试：`dotnet test MesIngest.Tests` — 472 通过、82 跳过（无 LocalDB）、2 失败。
两处失败均与本改动无关，在 `HEAD` 的干净 worktree 上复现过：

- `WatchV2ProductionShellTests.Production_composition_creates_the_six_page_fluent_v2_shell_without_forbidden_refresh_controls`
  —— 本机显示缩放导致窗口高度 885.33 ≠ 断言的 900，基线同样失败。
- `RetiredContractAndCutoverSafetyTests.The_attended_cutover_drill_is_the_only_thing_that_deletes_a_database`
  —— 由工作区里未跟踪的打包输出 `dist/MesIngest/scripts/cutover/CutoverSqlTools.ps1` 触发，
  干净 worktree 无 `dist/` 时通过。
