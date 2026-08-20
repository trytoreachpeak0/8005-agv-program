# 04 — 删除延迟确认与改名跟随

**What to build:** 主流编辑器保存文件的方式是「写临时文件再替换或改名」，在文件系统层面表现为删除紧接着新建——本项目自身的原子写入也是如此。因此用户在别处保存配置文件时，这个配置不应该在列表里闪烁或短暂消失。文件被改名时，正在编辑它的界面跟随到新名字，而不是弹出「文件已删除」的误报。

**Blocked by:** 03

**Status:** done

- [x] 外部编辑器保存导致的「删除后立即重现」不被判定为删除，列表无闪烁
- [x] 延迟确认窗口过后文件仍不存在，才判定为真删除
- [x] 判定为内容更新时按 03 的同步规则处理
- [x] 文件被改名时列表项改名并重排
- [x] 正在编辑的文件被改名时界面跟随到新名字，不提示已删除
- [x] 上述时序全部由 `FakeTimeProvider` 驱动，测试中**不出现真实等待**
- [x] tier 1 全绿

## Golden renderer checklist

- [x] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。

## Comments

### 实现记录

- `WatchAreaFilterProfileStore` 增加 500 ms 删除确认窗口；`Deleted` 先进入注入时钟驱动的待确认状态，同名 `Created` / `Changed` 会取消删除并进入既有 250 ms 去抖内容更新路径。`Changed → Deleted` 交错会撤销旧的待发布更新，避免在确认窗口前刷新缺失文件。
- 已解释目录变更增加明确的 old/new 改名载荷。生产窗口收到改名后先迁移选中配置与草稿身份，再重读/重排列表；干净缓冲从新路径读取，脏缓冲保留本机文本但改用新文件名，因此不会走旧文件缺失错误路径。
- 存储与 UI 组合 seam 均使用 `ManualTimerTimeProvider`（本仓库的 FakeTimeProvider）和手动目录事件源；新增测试文件中没有 `Sleep`、真实 `Task.Delay` 或轮询等待。

### 验证记录

- 定向存储与 UI seam：`29 passed / 0 skipped / 0 failed`。
- `dotnet build MesIngest.sln --no-incremental -v minimal`：`0 warnings / 0 errors`。
- 主工作区 Tier 1：`502 passed / 82 environment-gated skipped / 1 failed`；唯一失败由既有未跟踪发布产物 `dist/MesIngest/scripts/cutover/CutoverSqlTools.ps1` 触发，未删除或修改该用户产物。
- 提交 `af97056` 的隔离 clean worktree 执行 `dotnet test MesIngest.Tests -v minimal`：`502 passed / 82 environment-gated skipped / 0 failed`；验证后已清理临时 worktree。
- 按票据约定未运行 Tier 2 / Tier 3；黄金机验证留到整个特性完成后统一进行。
