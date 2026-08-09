# 11 — 对齐选定 UI、回归 Ticket 01–10 并重建 Verify.Xaml 基线

**What to build:** 将正式 `MesIngest.Watch` 对齐已选择的 Prototype D/E 设计，在不破坏 Ticket 01–10 行为与自动化 seam 的前提下完成全量回归；经用户确认真实黄金机截图后，再建立新的确定性 Verify.Xaml 基线。

**Blocked by:** 无；Ticket 01–10 的当前实现与验收条件是本票必须保持并重新证明的回归契约，不是可以假定已完成的前置结论

**Status:** ready-for-agent

**Reset decision (2026-08-09):** 用户拒绝当前生产 UI。Ticket 11 从零重建，不继承旧完成结论。现有 `verified`/`received`、窗口候选和稳定性结果只作历史参考，不得视为新 UI 的批准基线。

- [ ] 以 `MesIngest.Watch.Prototype` 的 `--variant=D` 和 `--variant=E` 为视觉权威，生产窗口对齐顶部 64px 工具栏、194px 导航、260px 筛选侧栏、主结果/关系卡片区、底部 28px 状态栏，以及参考图的颜色、圆角、间距、字号、行高和信息密度。
- [ ] Demand 页默认视觉层级与参考图一致：核心任务列优先、选中任务结论与相关 Alert 卡片持续可见；全部规格字段、详情、复制、服务端排序和 cursor 能力仍可到达。
- [ ] Alert 页默认视觉层级与参考图一致：活动/已解除、Severity/Code/范围和相关 Demand 目标易于理解；精确 DemandId、业务键、任务类型、全局范围以及 REAPPEAR 旧/新实例不得被压成伪精确关联。
- [ ] 顶部连接状态、当前页刷新/取消/自动刷新和底部状态表达适配生产状态机；保留既有 AutomationId、AutomationProperties.Name、键盘操作和测试 seam，只有语义确实变化时才允许同步更新测试。
- [ ] 为 D/E 结构锚点建立快速、确定性、可自动失败的设计一致性测试；至少验证根布局尺寸、关键区域可见性、核心文案/控件和关系卡片，不以肉眼截图作为唯一回归信号。
- [ ] 完整运行 Ticket 01–10 回归矩阵：本地单元/契约测试、`watch-vm-tests`、黄金机交互式 UI 回归、100% DPI 主场景以及 Ticket 10 的 125%/150% DPI UIA/布局烟测；结果逐票映射，任何失败不得用更新截图掩盖。
- [ ] 所有跳过项必须列名、原因和所属票；当前 19 个 SQL 环境测试不得被写成“全量通过”，并作为 Ticket 13 发布门禁的显式未决项。
- [ ] 在黄金机生成 Demand、Alert、Overview、Settings 的真实预览，由用户明确确认“与设计一致”后，才允许进入 Verify.Xaml 基线阶段。
- [ ] 使用 Verify.Xaml 4.2.1，在 100% DPI、浅色主题、中文区域、固定字体和 `SoftwareOnly` 下重建 `1440×900` 的 15 个场景与 `2560×1440` 的 4 个场景；旧 approved 文件不得原地批量覆盖。
- [ ] 假数据覆盖六类 TASK_TYPE、七个 MES 输入字段、全部 TransportDemand 投影字段、六类生产 IngestAlert 和中文长文本，并保持固定时钟、固定排序和脱敏。
- [ ] 环境不满足活动桌面、分辨率、DPI、主题、区域、字体或渲染模式时停止视觉套件并报告差异，不写入 received 或新基线。
- [ ] 新矩阵连续 10 次 XAML/PNG 完全一致后，逐场景生成 before/after/diff 提案；禁止全局像素容差、大面积 mask 和一次性接受全部候选。

## Comments

- 2026-08-09：当前 UI 的黄金机单次候选渲染仅用于设计检查，不构成 Ticket 11 验收、10 次稳定性结论或基线批准。先完成 Ticket 1–10 回归，之后从本票重新开始视觉基线工作。

- 2026-08-09：用户提供的两张参考图与 `watch-redesign-selected-v2` 的 D/E PNG SHA-256 完全一致。当前生产候选与参考图的显著像素差异分别为 Demand `32.82%`、Alert `32.13%`；黄金环境和源码同步均已排除，因此本票首先修复生产 XAML 对齐，而不是调整渲染机。
