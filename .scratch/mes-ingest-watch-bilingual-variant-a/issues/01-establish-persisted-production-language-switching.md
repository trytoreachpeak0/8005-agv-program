# 01 — 建立可持久化的生产语言切换基础

**What to build:** 让使用者能够从生产 Watch 的“设置 → 显示与布局”在 `简体中文` 与 `English` 之间切换，并让整个应用获得一个可供各页面独立迁移的集中、强类型语言和值语义基础。首次启动固定使用简体中文；保存、重启、旧偏好迁移和损坏值回退均不得丢失其它有效显示与刷新偏好。

**Blocked by:** None — can start immediately.

**Status:** done

- [x] 未保存语言偏好时以简体中文启动，语言选项始终以 `简体中文` 和 `English` 自称显示。
- [x] 保存 English 后当前生产窗口立即更新，重启后仍恢复 English；保存失败时运行时语言不产生模糊的半提交状态。
- [x] 旧偏好缺少语言字段时迁移为简体中文并保留刷新、窗口和 Inspector 布局；未知或损坏语言安全回退且应用仍可启动。
- [x] 应用组合根拥有唯一共享语言状态，新窗口继承当前值，现有窗口可观察同一状态；切换不读取 Windows 显示语言，也不修改 Host 或业务配置。
- [x] 集中、强类型目录同时覆盖固定文本、参数化文本、已知码、未知码回退、六种值/查询语义、绝对/相对时间及语言相关数量格式，调用方不能用任意字符串键或页面私有字典取文案。
- [x] 切换语言不增加 Host 请求，不改变当前页面、规范筛选代码、选择或焦点，也不通过重建业务 ViewState 完成翻译。
- [x] 建立清晰的页面实现所有权边界，使 Error Search 与接入告警等后续并行迁移不需要同时编辑同一页面专属实现单元。
- [x] 生产实现不引用 FluentPrototype，不携带 Tag 字典、视觉树遍历、假数据、评审条或原型语言按钮。
- [x] Read [docs/agents/golden-renderer.md](../../../docs/agents/golden-renderer.md).
- [x] Ran the required golden-machine suites through an interactive task.
- [x] User approved the final real-window preview (visual changes only).
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.
