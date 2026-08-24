# 03 — 外部改文件时编辑器自动同步

**What to build:** 用户在 Watch 里查看某个 AREA 配置的同时，另一个程序（记事本、VS Code 等）修改并保存了同一个文件。编辑器内容自动更新为文件的新内容，而用户的光标位置、选中范围和滚动位置保持不动——每次外部保存都让光标跳回开头，比冲突提示还难用。「从磁盘加载」按钮随之移除。

本 ticket 只处理缓冲干净的情形。缓冲为脏时的并发冲突属于 06。

**Blocked by:** 02

**Status:** done

- [x] 外部修改并保存后编辑器内容自动更新
- [x] 更新后光标位置、选中范围、滚动位置保持
- [x] 磁盘内容与编辑器当前内容逐字节相同时不触发重载
- [x] 本进程自身写盘产生的事件被抑制，不导致重载与光标跳动
- [x] 文件正被外部写入而读取失败时按退避重试，重试耗尽才报错
- [x] 事件回调切回 UI 线程后才更新界面
- [x] 「从磁盘加载」按钮不复存在，引用它的测试断言同步调整
- [x] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。2026-08-21 统一验收已完成，证据与结论记录在
> [`spec.md`](../spec.md) 的 Golden renderer acceptance 一节。

## Comments

### 实现记录

- 选中配置的编辑缓冲为干净状态时，目录事件经既有去抖窗口解释后自动读取当前 TXT；只有正文逐字符变化才替换 `TextBox.Text`。替换前后保存并恢复公开可观察的 `CaretIndex`、`SelectionStart`、`SelectionLength`、精确水平/垂直滚动偏移和键盘焦点。缓冲为脏时仍保持本地输入，冲突处理留给 ticket 06。
- 外部读取使用 50 / 100 / 200 ms 退避。独占写锁、原子替换期间的瞬时 `PROFILE_NOT_FOUND`、以及分段写 UTF-8 时的临时 `INVALID_UTF8` 都进入同一重试；全部耗尽后才在 UI Dispatcher 上显示错误，旧编辑内容不被清空。
- store 在自身原子 `Save` / `SaveAs` 后记录写后指纹，并在短抑制窗口内丢弃命中同一指纹的重复 watcher 批次；若磁盘随后出现不同指纹，外部变化仍正常发布。
- 删除 `AreaProfileFileReloadButton` 及处理器；tier 1 组合测试与 tier 2 源码断言/生产 journey 已同步为自动跟随语义。黄金机按票据约定未单独运行。

### 验证记录

- 定向存储与 UI 组合 seam：`24 passed / 0 skipped / 0 failed`，全部使用手动事件源和注入时钟，无真实等待。
- `dotnet build MesIngest.sln --no-incremental -v minimal`：`0 warnings / 0 errors`；包含 `MesIngest.Watch.UiTests` 编译。
- 主工作区首次 tier 1：`497 passed / 82 skipped / 1 failed`；唯一失败来自既有未跟踪发布产物 `dist/MesIngest/scripts/cutover/CutoverSqlTools.ps1`，与本票无关且未删除用户产物。
- 提交 `513aba8` 的隔离 clean worktree 重新运行 `dotnet test MesIngest.Tests -v minimal`：`497 passed / 82 environment-gated skipped / 0 failed`。验证后已移除该临时 worktree。
- `/code-review` Standards 与 Spec 两轴复核均为 `0 finding`；评审提出的精确滚动偏移、瞬时缺失/半写 UTF-8 重试、重复代码及命名问题均在最终复核前修正。
