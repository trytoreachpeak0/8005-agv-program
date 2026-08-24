# MesIngest.Watch：DemandSeries 详情显示交互替代方案

研究日期：2026-08-20
范围：只调研当前 `MesIngest.Watch` 的 DemandSeries 主列表/详情布局；不修改产品代码，不运行 Tier 2 / Tier 3。

## 结论

按本次要求“Series 区和完整详情区都不能被挤压”，结论取决于是否要求两者**同时可见**：

- 不要求同时可见时，首选同页 stacked drill-in：列表占满内容区，Enter、双击或“查看详情”进入全页详情，返回后恢复筛选、页码、选中行和滚动位置。两个状态都拥有完整画布，并继续复用同一个冻结快照与 selection 状态。
- 要求同时可见、同时可操作时，固定大小的单窗口不可能同时满足；应增加单实例、非模态、owned 的 `DemandSeries Inspector` 详情窗口。它是唯一能让两边同时保持完整可操作面积、又互不遮挡的方案，最适合双屏值守。

删除主列表标题右侧带文字的 `ToggleSwitch`，改成现有 master-detail splitter 缝右端的无文字 chevron icon button，仍是一个成本较低的改善。它复用已经存在的 splitter 行，不新增布局行列，也不会让列表标题、副标题或详情标题为控制入口让位；但它只解决“控制入口占空间”，并不解决展开态下列表与详情共享高度的问题，因此不是严格要求下的最终方案。

不建议把当前完整详情塞进 Flyout 或模态对话框。Flyout 可作为将来的“快速预览”，但当前详情含多组生命周期、Demand 世代、事件与证据表格，属于需要稳定滚动和持续操作的主内容，不是轻量瞬时信息。

## 当前实现与今天改动的准确还原

今天的 Ticket 28 从提交 `fec1830` 开始引入详情折叠、上下 `GridSplitter`、内容测量列宽和分页修正，随后在 `63dc2a6` 中把 splitter 命中区提升到 32 epx、视觉线保持 4 epx，并把尺寸令牌化；`e5934c0` 更新正式 UI 旅程，最终在 `5fbf133` 对真实 WPF 窗口留下收起态证据。票据和验收记录见 [Ticket 28](../../new-mes-ingest/issues/28-demand-series-list-height-and-paging-readability.md)。

当前布局的关键事实：

- `DemandSeriesMasterDetailGrid` 使用三行：主列表 `1.2*`、splitter 32 epx、详情 `0.8*`。列表和详情分别有 256 epx 最小高度。[当前 XAML](../../../mes/ingest/csharp/MesIngest.Watch/WatchWorkspaceWindow.xaml)
- `DemandSeriesDetailVisibilityToggle` 位于主列表卡片标题的 `Auto` 行、右侧 `Auto` 列，显示“已展开/已收起”。它不是悬浮元素；它会占标题横向测量空间。标题或副标题因此换行时，`Auto` 行会变高，直接减少 DataGrid 高度。
- 关闭 Toggle 时，代码保存展开比例，将详情、splitter 设为 `Collapsed`，并把主列表行设为 `*`；重新打开时恢复上次比例。[当前 code-behind](../../../mes/ingest/csharp/MesIngest.Watch/WatchWorkspaceWindow.xaml.cs)
- 因而当前交互只提供两个状态：一是列表与详情共享高度，二是详情完全消失、列表独占高度。它没有提供一个既让完整列表和完整详情同时存在、又不占额外空间的第三种状态。
- 页面每 10 秒自动刷新。Ticket 20 还要求列表和详情绑定同一冻结快照，刷新成功按稳定 SeriesId 重选，失败、游标失效或对象离开范围时不能把旧详情挂到新快照。[Ticket 20](../../new-mes-ingest/issues/20-demand-series-production-page.md) 因此任何独立视图都必须复用现有 selection/snapshot 状态，不能另起一套详情查询。

真实 1440×900 黄金机预览清楚显示了现状：展开时列表约占上半区，详情只露出首屏的一部分；收起时列表卡片占满剩余页面，但 Toggle 仍在标题右侧。证据为 [展开态](../../../mes/ingest/csharp/.artifacts/golden-renderer/ticket-28/run-20260820-142214-watch-production-preview/watch-ui/20260820-142225-192/production-workspace-19-22/03-demand-series-detail.png) 和 [收起态](../../../mes/ingest/csharp/.artifacts/golden-renderer/ticket-28/run-20260820-142214-watch-production-preview/watch-ui/20260820-142225-192/production-workspace-19-22/03a-demand-series-master-only.png)。

## 方案比较

| 方案 | 是否新增布局占位 | 能否同时操作列表和详情 | 对当前复杂详情的适配 | 结论 |
| --- | --- | --- | --- | --- |
| **splitter seam chevron** | 否；复用现有 seam | 展开时可以，面积仍按 splitter 分配 | 完全复用当前详情 | **首选，替换当前 ToggleSwitch** |
| 同页 stacked drill-in：列表 → 详情 → 返回 | 否；两者复用同一内容矩形 | 不可以 | 很好；两边各自都能用完整画布 | 若多数任务是“选一个再深挖”，作为第二选择 |
| 非模态 owned Inspector 窗口 | 主窗口内不占位 | 可以；双屏时真正互不遮挡 | 最好 | 严格“同时完整显示”需求的唯一方案 |
| overlay drawer / Flyout | 否 | 名义上可以，但会遮住列表 | Flyout 只适合摘要；长表格焦点和嵌套滚动差 | 仅做快速预览，不承载完整详情 |
| ContextMenu / 双击 / Enter | 否 | 取决于它打开什么 | 适合作为冗余入口 | 必须配可发现的主入口；双击不能单独使用 |
| 页面 header/command bar 图标 | 不新增行，但占 header 横向空间 | 展开时可以 | 可实现 | 距离作用对象较远，不如 seam；单个命令不值得建 command bar |
| 模态 `ContentDialog` | 覆盖而不重排 | 不可以，主窗口被阻断 | 不适合持续查阅 | 排除 |

微软把 list/details 明确分为两种合法形态：side-by-side 同时显示，或 stacked 一次只显示一个 pane、从列表 drill down 到详情；后者可把两块内容都放在独立的完整页面中。[Microsoft：List/details pattern](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/list-details) `SplitView` 的 Overlay 模式也只是让 pane 覆盖 content，而 Inline 模式必然分割可用空间。[Microsoft：Split view](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/split-view) 这印证了上述空间约束：单窗口里没有一种既同时可见、又不分割或覆盖画布的布局。

## 推荐方案的行为细节

### 1. 用 seam chevron 替换标题 ToggleSwitch

- 展开态：在现有 32 epx splitter seam 的**最右端**叠放一个约 32×32 epx 的 icon button；其余 seam 仍是可拖动的 `GridSplitter`，4 epx 视觉线不变。按钮不新增 row、column 或 margin。
- 收起命令：图标表达“把下方详情向下收起”，可见 tooltip 和 UIA 名称为“收起需求系列详情”；执行后保存当前 `1.2* / 0.8*` 或用户拖动后的比例，详情收起，主列表获得可用高度。
- 收起态：在 master-detail 容器的 overlay/adorner 层保留一个小型“向上展开”pull-tab，贴在主列表卡片的右下边界；它不参与 `Measure`，不让分页条或 DataGrid 腾位置。不要为了容纳它保留一条 32 epx 空白 splitter 行。
- 展开命令：名称变为“展开需求系列详情”，恢复上一次会话内比例和同一个已选 Series；不重新请求、不清除 selection，也不把焦点强行跳进详情。
- 按钮区域不再承担拖动，splitter 的其余宽度继续承担拖动；按钮应靠右，避免像居中按钮那样切断最常用的中部拖拽区。
- 提供同一命令的快捷键（例如 `Alt+D`，最终以现有快捷键冲突检查为准）和列表 ContextMenu 项。双击可作为加速器，但不能是唯一入口。

这个方案保留 Ticket 28 已验证的状态机与高度恢复代码，只改变 affordance 的位置和外观。`ToggleSwitch` 从物理开关语义上虽能立即改变二元状态，但微软建议它用于可明确表述为 On/Off 的二元设置；如果 On/Off 不能自然描述交互，应考虑其他控件。[Microsoft：Toggle switches](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/toggles) “详情导航/折叠”更像局部 pane command，icon button/ToggleButton 比带“已展开/已收起”的设置开关更贴合。

### 2. 严格全尺寸需求：单实例非模态 Inspector

仅当运维人员确实需要一边扫列表、一边长期查看完整证据，尤其需要双屏时增加：

- 列表提供明确的“在详情窗口打开”，同时支持 Enter 或 ContextMenu；单击 selection 仍只选择，不应每移动一行就弹窗。
- 全应用只复用一个 `DemandSeries Inspector` 实例。默认 `Follow selection`，也可 `Pin` 当前 Series，避免列表自动刷新或切换选择时打断正在调查的对象。
- Inspector 不另起请求，消费主窗口当前冻结 snapshot/selection 投影；标题包含 SeriesId 与 snapshot 时点。对象离开新快照或刷新失败时保留上一成功详情，并显示现有 stale/failure 语义。
- 使用 WPF `Show()` 非模态打开，并设置 `Owner`；微软说明 `Show()` 不阻止用户操作其他窗口，owned window 可与 owner 建立关闭/最小化等关系。[Microsoft：WPF windows](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/windows/) [Microsoft：打开非模态窗口](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/windows/how-to-open-window-dialog-box)
- 这是一个新的正式窗口 surface，会增加窗口生命周期、FlaUI journey、UIA 树、DPI/主题以及黄金机视觉验证成本。Ticket 28 曾因这些成本否决“只为解决高度而立即拆窗”；只有得到明确双屏/并行操作需求后才值得承担。

## 为什么不优先 Flyout、drawer 或对话框

微软把 Flyout 定义为轻量、上下文相关、可快速 light-dismiss 的弹层，适合显示某项的补充说明或更长描述；点外、Esc、Back、窗口 resize 都可关闭。[Microsoft：Dialogs and flyouts](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/) 当前项目使用的 WPF UI 4.3.0 确实提供基于 WPF `Popup` 的 `Wpf.Ui.Controls.Flyout`，[WPF UI：Flyout API](https://wpfui.lepo.co/api/Wpf.Ui.Controls.Flyout.html)，所以实现并不困难。

但完整 DemandSeries 详情不是轻量内容：它包含多组可滚动表格、复制命令、完整证据跳转和自动刷新状态。放进 Flyout 会产生弹层内嵌滚动、焦点圈定、意外 light-dismiss 和遮挡列表的问题。可接受的边界是：Flyout 只展示 SeriesId、状态、当前 Demand、最新时间等 5–8 个摘要字段，并提供“打开完整详情”；不要把现有详情面板整体搬进去。

模态 `ContentDialog` 更不合适。微软明确说明 modal dialog 会阻断应用窗口交互，应保留给必须立即确认或必须阅读的问题，而不是日常对象查阅。[Microsoft：Dialogs and flyouts](https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/) WPF UI 的 `ContentDialogHost` 也明确管理 interaction blocking。[WPF UI：Controls API](https://wpfui.lepo.co/api/Wpf.Ui.Controls.html)

## 可访问性与键盘契约

无论采用 seam button、stacked drill-in、Flyout 或独立窗口，都应满足：

- icon-only button 必须有随状态变化的 `AutomationProperties.Name` 和 tooltip，名称描述动作而不是重复“按钮”角色；状态若使用 ToggleButton，应让 UIA 暴露 Toggle pattern。
- Tab 顺序跟随视觉顺序：列表 → splitter/折叠按钮 → 详情。Enter/Space 激活聚焦命令；微软也说明 Enter 在 list/grid item 上可承担额外打开动作，而 Space 保留 selection。[Microsoft：Keyboard interactions](https://learn.microsoft.com/en-us/windows/apps/develop/input/keyboard-interactions)
- 收起详情后，不让焦点留在已 `Collapsed` 的详情子元素；焦点留在可见的 seam/pull-tab 命令。重新展开时不要偷走列表焦点。
- ContextMenu 可作为 Shift+F10/Menu key 的冗余入口，但不能替代可见主入口。双击不能成为唯一入口。
- Flyout 打开后把焦点移入首个可操作项，Tab 不可落到被遮挡内容；Esc/点外关闭后把焦点还给触发按钮或原行。
- stacked drill-in 的详情页必须提供左上“返回列表”，返回时恢复筛选、页码、滚动偏移、selected SeriesId 和原单元格焦点。微软规定 Back 应返回上一导航位置，并建议入口位于左上。[Microsoft：Back navigation](https://learn.microsoft.com/en-us/windows/apps/develop/ui/navigation/navigation-history-and-backwards-navigation)
- Inspector 窗口标题包含 SeriesId，首次打开聚焦详情标题或首个命令，保留标准 Close；关闭后焦点返回触发行。
- 使用 WPF/WPF UI 原生控件和现有 AutomationProperties，避免造 `ControlType.Custom`。微软指出自定义 UIA 类型会让客户端无法预期其结构、键盘交互和支持模式。[Microsoft：WPF custom-control UI Automation](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control)

## 实现落点与后续验证

若采用首选 seam chevron，预计落点如下：

1. 在 `WatchWorkspaceWindow.xaml` 中删除主列表 header 的 `DemandSeriesDetailVisibilityToggle` 及其 `Auto` 控制列，把新 icon button 放入 `DemandSeriesMasterDetailSplitter` 所在 seam 的 overlay 层；为收起态增加不参与布局测量的 pull-tab。
2. 在 `WatchWorkspaceWindow.xaml.cs` 中复用现有 `_demandSeriesExpandedMasterHeight`、`_demandSeriesExpandedDetailHeight` 与 `ApplyDemandSeriesDetailVisibility()`；改为 command/button 状态驱动，并补焦点恢复与快捷键。不要改变 snapshot selection 或自动刷新逻辑。
3. 保留稳定 AutomationId，或在测试和 UIA 契约中一次性迁移到新名称；增加“按钮不在 master/detail 内容测量列中”“收起/展开恢复比例”“收起时焦点不落入隐藏详情”的非像素测试。
4. UI journey 应验证：真实鼠标仍可拖动 splitter；button 的 32 epx 区域只执行折叠，其余 seam 仍拖动；键盘和 UIA 均可收起/恢复；1440×900、1920×1080、窄窗、高对比度下按钮不遮分页内容。

本次仅完成调研，没有改产品代码或测试，也没有运行 Tier 2 / Tier 3。后续若实现，必须继续遵循 [Fluent UI rules](../../../docs/agents/fluent-ui.md) 和 [Golden WPF renderer](../../../docs/agents/golden-renderer.md)：先跑 Tier 1；涉及 XAML/布局/UIA 的真实预览要在黄金机执行，展示最终预览并取得用户明确批准后，才能进入候选稳定或基线流程。
