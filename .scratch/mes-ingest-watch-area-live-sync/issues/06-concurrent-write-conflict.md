# 06 — 并发写入冲突处理

**What to build:** 用户正在输入的同时，另一个程序修改了同一个配置文件。两边的修改都不能被静默丢弃：界面给出明确的二选一——保留我的修改，或使用磁盘版本。提示显示期间自动落盘暂停，否则提示会被随后的写盘绕过。

若正在编辑的文件被外部删除而用户尚有未落盘的输入，编辑器内容原样保留并转为未命名草稿，提供另存为入口——绝不能因为别人删了文件就把用户打的字扔掉。

自动落盘把脏窗口压缩到一秒量级，因此这是罕见回退路径，界面上不为它预留视觉重量，但必须实现：省略等同于静默吞掉他人修改。不做三路合并。

**Blocked by:** 05

**Status:** done

- [x] 缓冲为脏且磁盘已变更时，落盘不静默覆盖，给出二选一
- [x] 选择保留本地时磁盘被覆盖并更新指纹基准
- [x] 选择使用磁盘时本地输入被丢弃并重载
- [x] 冲突提示显示期间自动落盘暂停
- [x] 正在编辑的文件被外部删除且缓冲为脏时，内容保留、转未命名草稿、提供另存为入口
- [x] 同样情形下缓冲干净时，列表移除该项并把选中项移到相邻项
- [x] 冲突检测复用既有的指纹乐观并发，**不新增基准机制**
- [x] tier 1 全绿

实现记录：

- 冲突提示未解决前，切换选中配置与 `Ctrl+S` 都会被拒绝并说明原因，否则离开提示
  等于替用户做了二选一。切换页面不会丢弃任何一份——页面只切换可见性，缓冲、
  提示与磁盘版本都在，切回来继续选择。
- 「保留我的修改」由 `WatchAreaFilterProfileStore.OverwriteWithLocalEdit` 在同一把
  事务锁内读当前指纹再写，避免提示期间落地的第三方写入被静默覆盖。仍是既有的
  指纹乐观并发，没有第二套基准。
- 已知边界：冲突未解决时直接关闭窗口，未落盘的缓冲随进程一并丢失。阻止关窗
  与自动替用户选一份都不可取，spec 亦未定义该出口，故不在本 ticket 处理。

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。2026-08-21 统一验收已完成，证据与结论记录在
> [`spec.md`](../spec.md) 的 Golden renderer acceptance 一节。
