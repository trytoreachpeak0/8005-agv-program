# MesIngestWatch V2 UI 对齐与验收重建

## Notes

- 2026-08-09 用户拒绝当前生产 UI：黄金机截图与已选择设计稿在 Demand 页面有 `32.82%`、Alert 页面有 `32.13%` 显著像素差异。
- 黄金机环境契约已通过，宿主与来宾关键源码 SHA-256 一致，因此偏差来自生产 XAML 与视觉场景实现，不是 DPI、主题、字体或源码同步。
- 当前生产 UI 只移植了“深色导航、筛选侧栏、双向关系解释”的概念，没有移植选定 D/E 设计的完整视觉壳。
- Ticket 11、12、13 全部按本地图重建。旧实现和旧证据只作历史参考，不继承完成状态。
- Ticket 01、02、07、08、09、10 的票面状态目前仍是 `ready-for-agent`，Ticket 03–06 为 `done`；本次不伪造关闭状态，Ticket 11 必须用逐票回归证据重新证明 01–10 后才能完成。

## Decisions-so-far

- 视觉权威是 `MesIngest.Watch.Prototype` 的 D/E 两个选定场景：
  - Demand → Alerts：`--variant=D`，参考图 `watch-redesign-selected-v2/demand-to-alerts-1440x900.png`，SHA-256 `5D4BB9F10C79BAD1289518A8ED237317875A418A9446682D41AFC1FD324C87A4`；
  - Alert → Demands：`--variant=E`，参考图 `watch-redesign-selected-v2/alert-to-demands-1440x900.png`，SHA-256 `E0F1BF277691665A231DA069D0B3B8A763AFCA62C76CF003023C3B23FC9DAC5C`。
- 参考图约束生产窗口的视觉层级、骨架、间距、颜色、表格密度和关系卡片表达；假数据值和原型硬编码不进入生产。
- Ticket 01–10 继续约束真实行为、Host 会话、筛选/排序/cursor、详情/复制、刷新/取消/陈旧状态、UIA 和偏好。视觉对齐不得删除或伪造这些能力。
- 当参考图与功能规格存在张力时，保留功能语义，并将次要字段或操作放入设计允许的详情区、渐进展开或当前页工具区；不得另造新的信息架构。
- Prototype 仍是 throwaway 视觉来源，禁止把它的假数据和硬编码直接复制为生产状态模型；生产 UI 必须复用现有绑定、查询状态机和测试 seam。
- 当前 `verified`、`received`、窗口候选和单次黄金机截图全部不是新 UI 的批准基线；旧文件保留用于追溯，不覆盖、不批量接受。
- 黄金视觉环境固定为 `gpt_win11` 的 1920×1080、100%/96 DPI、浅色主题、`zh-CN`、`China Standard Time`、Microsoft YaHei UI、Consolas、WPF `SoftwareOnly` 和已登录交互桌面。

## Dependency map

```text
Ticket 01–10 已实现行为与测试 seam
                ↓
Ticket 11 生产 UI 对齐 D/E 设计
          + Ticket 01–10 完整回归
          + 重建 Verify.Xaml 基线
                ↓
Ticket 12 重建 FlaUI 旅程、真实窗口基线与稳定性证据
                ↓
Ticket 13 重建发布包、完整非回归和人工发布验收
```

## Frontier

- 当前唯一可执行前沿：`11-deterministic-verify-xaml-baselines.md`。
- Ticket 12 在 Ticket 11 完成并由用户确认新黄金机截图前不得开始。
- Ticket 13 在 Ticket 12 的新证据门禁完成前不得开始。

## Fog

- 动态真实值不要求与参考图逐像素相同；结构锚点和固定假数据场景必须可自动比较。
- 19 个 SQL Server 环境测试目前会跳过。Ticket 11 的 UI 行为回归必须列出这些跳过；Ticket 13 发布验收前必须在可用 SQL 环境运行或取得用户对每项跳过的明确批准。
