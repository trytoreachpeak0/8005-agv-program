# 06 — 并发写入冲突处理

**What to build:** 用户正在输入的同时，另一个程序修改了同一个配置文件。两边的修改都不能被静默丢弃：界面给出明确的二选一——保留我的修改，或使用磁盘版本。提示显示期间自动落盘暂停，否则提示会被随后的写盘绕过。

若正在编辑的文件被外部删除而用户尚有未落盘的输入，编辑器内容原样保留并转为未命名草稿，提供另存为入口——绝不能因为别人删了文件就把用户打的字扔掉。

自动落盘把脏窗口压缩到一秒量级，因此这是罕见回退路径，界面上不为它预留视觉重量，但必须实现：省略等同于静默吞掉他人修改。不做三路合并。

**Blocked by:** 05

**Status:** ready-for-agent

- [ ] 缓冲为脏且磁盘已变更时，落盘不静默覆盖，给出二选一
- [ ] 选择保留本地时磁盘被覆盖并更新指纹基准
- [ ] 选择使用磁盘时本地输入被丢弃并重载
- [ ] 冲突提示显示期间自动落盘暂停
- [ ] 正在编辑的文件被外部删除且缓冲为脏时，内容保留、转未命名草稿、提供另存为入口
- [ ] 同样情形下缓冲干净时，列表移除该项并把选中项移到相邻项
- [ ] 冲突检测复用既有的指纹乐观并发，**不新增基准机制**
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
