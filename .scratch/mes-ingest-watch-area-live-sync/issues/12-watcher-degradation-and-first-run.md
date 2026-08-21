# 12 — 目录降级与首次创建

**What to build:** 配置目录被删除、改名或因其他原因无法监视时，界面明确告知用户列表可能不是最新的，并在目录恢复后自动重新开始监视——用户不该在毫不知情的情况下看着一份过期的列表。首次使用 Watch 时配置目录自动创建，用户不需要手工准备。

**Blocked by:** 02

**Status:** done

- [x] 监视失效时界面显示明确的降级提示
- [x] 目录恢复后自动重建监视并刷新列表
- [x] 文件系统事件缓冲区溢出时触发全量重扫，目录状态不丢失
- [x] 首次使用时配置目录自动创建
- [x] 目录不存在时列表呈现为空而非报错
- [x] 页面切走与窗口关闭时监视资源被释放
- [x] tier 1 全绿

## Golden renderer checklist

- [x] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。2026-08-21 统一验收已完成，证据与结论记录在
> [`spec.md`](../spec.md) 的 Golden renderer acceptance 一节。

## Comments

- 2026-08-21：`WatchAreaFilterProfileStore` 现在把目录监视建模为 `Watching` / `Degraded` / `Stopped` 状态；一秒健康检查发现目录删除或改名后停止事件源，目录恢复时自动重建并发出全量重扫。只读枚举与已应用状态读取不会为了取得事务锁而重建一个运行期已消失的目录，因此降级期间列表稳定呈现为空。
- `FileSystemWatcher.Error` 已接入事件源；`InternalBufferOverflowException` 会停止并重建 watcher，恢复后只发出一次全量重扫，随后增量事件继续有效。首次使用仍由 store 显式创建配置目录。
- AREA 页增加不可关闭的降级 `InfoBar`，监视恢复后自动关闭。进入 AREA 页才启动监视，切离页面调用 `StopWatchingDirectory`，返回时重启并全量刷新；窗口关闭最终释放事件源与全部计时器。
- TDD seam：`WatchAreaFilterProfileDirectoryWatchTests` 覆盖首次创建、运行期目录删除/恢复、启动失败自动恢复、缓冲区溢出重建和 Dispose；`WatchAreaProfileLiveListTests` 覆盖持久降级提示、恢复刷新以及页面/窗口生命周期。AREA 聚焦回归 146 passed；solution 非增量构建 0 warning / 0 error；最终 tier 1 `dotnet test MesIngest.Tests --verbosity minimal` 为 574 passed、82 skipped、0 failed。82 项均为本机无 LocalDB 时按 tier 1 规则跳过的 SQL Server 测试。
- `$code-review` 双轴复核发现并修正：目录消失与 watcher failure 同时发生时立即全量刷新为空；溢出重建首次失败时仍先重扫并继续定时恢复；生命周期由三个易混布尔值收敛为 `Stopped / Starting / Watching / Degraded` 与单一重扫事实；降级文案去重；工单状态使用 tracker 允许的 `ready-for-human`，等待整批金机人工验收。
- 未运行 tier 2/3；按本特性约定留待全部 ticket 完成后统一金机验证与用户预览。
