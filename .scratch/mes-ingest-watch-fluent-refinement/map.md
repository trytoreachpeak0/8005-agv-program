# MesIngestWatch Fluent 窗口与列表体验完善

Status: wontfix

## Closure

2026-08-11：按用户要求关闭本地图及其全部未解决子票据，以便重新设定 Wayfinder。现有文件仅保留为历史记录，不再作为实现前沿或验收权威。

## Destination

正式 `MesIngest.Watch` 在继续使用 WPF-UI 的前提下，具备完整 Win11 Fluent 窗口交互、更大的 Demand/Alert 列表、可折叠筛选、按类型过滤、列表中可见的 DemandId，以及可选择复制的详情文本；相关行为通过自动化回归和黄金渲染机预览，最终候选连续验证 10 次并由用户批准。

## Notes

- 本地图经用户明确确认，允许把生产实现、自动化与黄金机验证带入地图，不只产出规划决策。
- 继续锁定 `WPF-UI` 4.3.0；主窗口使用 Wpf.Ui 的 Fluent 窗口与标题栏能力，不退回纯原生 WPF 仿制。
- Alert 的“类型”就是 `Code`；Demand 的“类型”是 `TASK_TYPE`。
- DemandId 是 TransportDemand 主键，放在 Demand 列表最左侧并常驻可见。
- Demand/Alert 筛选栏分别折叠；默认展开，只在当前运行期间记忆，不跨重启保存。
- 列表默认约占 Demand/Alert 页面可用高度的 70%，详情约占 30%，仍允许用分隔条调整并双击恢复默认。
- 复制重点是：选中 Demand 或 Alert 后，下方详情区域的值可用鼠标选择并复制；表格既有单元格/整行复制能力继续保留。
- 日常相关自动化各运行 1 次；最终黄金机候选的 Verify.Xaml、FlaUI 关键旅程和真实窗口视觉套件分别连续运行 10 次。该规则永久替代旧规格的 50 次完整门禁；失败或抖动时再增加诊断运行。
- 所有 UI/XAML、Wpf.Ui、布局、UIA 或视觉基线工作遵守 [`docs/agents/golden-renderer.md`](../../docs/agents/golden-renderer.md)。任何最终视觉候选必须先在 `gpt_win11` 的 1920×1080、96 DPI 交互桌面生成预览并由用户明确批准，之后才能晋升基线。
- 使用 `CONTEXT.md` 中的正式术语：TransportDemand、DemandId、IngestAlert、TransportDemandKey；界面不得把 Alert Code 或 TASK_TYPE 混称为业务主键。

## Decisions so far

<!-- 每个已解决票据在此只保留一行摘要和链接；详细答案只写在票据中。 -->

## Not yet specified

- 用户查看最终黄金机预览后可能提出的具体颜色、间距或信息密度微调；在预览出现前不预先拆票。
- 若连续 10 次门禁暴露特定渲染或 UIA 抖动，再根据红证据决定是否需要独立的稳定性修复票。

## Out of scope

- 不改变 Host API、TransportDemand/IngestAlert 领域语义、分页模型或业务只读边界。
- 不增加深色主题、多 Host 汇总、生产操作命令或告警处置能力。
- 不在用户批准最终黄金机预览前覆盖或晋升任何视觉基线。
