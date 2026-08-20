# 07 — 显示范围快照语义与漂移状态

**What to build:** 明确并在界面上表达这条语义：**显示范围来自用户按下应用那一刻的 AREA 快照，不跟随文件**。用户编辑配置文件不会改变正在生效的显示范围，因此打字打到一半时 `DemandSeries` 与 `资格审计` 两个页面不会跟着抖动。

实时同步之后，当前应用的配置可能被别人改掉而用户毫不知情，因此漂移必须显式呈现，不能只体现为「应用按钮变亮」。

应用按钮五态（由原型确定，作用对象为选中项）：

| 选中项 | 文件校验 | 内容 vs 快照 | 按钮 |
| --- | --- | --- | --- |
| 非当前应用 | 有效 | — | 应用此配置（主按钮，可点） |
| 非当前应用 | 非法 | — | 应用此配置（禁用） |
| 当前应用 | 有效 | 一致 | 已应用（禁用） |
| 当前应用 | 有效 | 已漂移 | 重新应用（主按钮，可点） |
| 当前应用 | 非法 | 已漂移 | 重新应用（禁用），底部状态条说明原因 |
| 当前应用 | 文件已删除 | — | 重新应用（禁用），范围仍生效 |

**Blocked by:** 03

**Status:** ready-for-agent

- [ ] 编辑配置内容不改变当前显示范围
- [ ] 当前应用的配置发生漂移时，列表项与应用按钮均明确提示待重新应用
- [ ] 应用按钮的五态与上表一致
- [ ] 漂移判定比较解析后的 AREA 序列，仅修改注释或空行不判定为漂移
- [ ] 非法配置不能被应用，且当前显示范围保持不变
- [ ] 非法状态在编辑器底部状态条、文件标题行、左侧列表项三处均有提示
- [ ] 「当前应用」徽标不被非法或漂移状态顶替，两个维度并存显示
- [ ] 快照沿用既有的活动标记持久化，进程重启后显示范围仍然有效
- [ ] tier 1 全绿

## Golden renderer checklist

- [ ] Read [`docs/agents/golden-renderer.md`](../../../../docs/agents/golden-renderer.md).
- [ ] Ran the required golden-machine suites through an interactive task.
- [ ] User approved the final real-window preview (visual changes only).
- [ ] Recorded the unique evidence directory and all named skips.
- [ ] Cleaned scheduled tasks/processes and rechecked the original VM at 96 DPI.

> 本特性的金机验证在全部 ticket 完成后统一进行，单个 ticket 不单独上金机。
> 实现阶段以 tier 1 为准。
