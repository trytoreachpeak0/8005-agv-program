# 02 — 目录里新增/删除的配置自动进出列表

**What to build:** 用户往配置目录里放一个新的 AREA 配置 TXT，不需要任何操作，它就出现在左侧筛选配置列表里；把文件删掉，它就从列表消失。页面顶部的「重新加载」按钮随之移除。列表刷新时用户当前选中的配置不变、焦点不被抢走。

本 ticket 只实现自身需要的事件解释规则——去抖、伴生文件过滤、扩展名二次校验。删除延迟确认与改名跟随属于 04，缓冲区溢出兜底属于 12。事件解释是逐个 ticket 加厚的，不在这里一次写完。

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] 配置目录新增 TXT 后列表自动出现该项，无需手动操作
- [ ] 目录中删除 TXT 后列表自动移除该项
- [ ] 列表刷新不改变当前选中项，不抢走焦点
- [ ] 编辑器伴生文件不进入列表：点开头的、非 TXT 扩展名的、带隐藏或系统属性的
- [ ] 一次性放入多个文件时列表只刷新一次
- [ ] 页面级「重新加载」按钮不复存在，引用它的测试断言同步调整
- [ ] 目录事件源作为 `WatchAreaFilterProfileStore` 的可选构造参数注入，与既有的时钟、删除委托注入模式一致
- [ ] 测试使用手动驱动的事件源与 `FakeTimeProvider`，**不出现真实等待**
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
