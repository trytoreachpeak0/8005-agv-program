# MesIngestWatch V2：WPF 图表与设计系统组件决策

研究日期：2026-08-04  
适用目标：`MesIngest.Watch`（当前为 `net8.0-windows`）

## 决策摘要

采用以下组合：

1. **图表直接依赖：固定使用 `ScottPlot.WPF 5.1.59`。** 用于性能趋势、P50/P95/Max 时间序列、阈值线和异常时间窗。通过一个项目内适配器封装，不让 ScottPlot 类型进入 ViewModel 或领域模型。
2. **阶段瀑布/单轮时间线：自行实现原生 WPF 只读控件。** 四个阶段数量固定、语义强，使用 `ItemsControl`/`Grid`、文本和比例段即可；同时提供数值表，不用图表库承担焦点、UI Automation 和精确读数。
3. **设计系统：自行实现小型、项目内的原生 WPF 设计系统。** 使用 `ResourceDictionary` 管理颜色、字号、间距、圆角、状态与显式控件样式；导航、分页、筛选、表格继续基于原生 `ListBox`、`Button`、`DataGrid` 等。**V2 不引入 WPF-UI、MaterialDesignInXAML 或 MahApps.Metro。**
4. **大数据策略不交给控件“硬扛”。** 服务端游标分页负责数据虚拟化；趋势 API 按显示时间范围返回合适时间桶，客户端最多绘制与像素宽度同量级的数据。WPF 原生行/列虚拟化只负责已经取回的一页。
5. **图表不是唯一信息载体。** 每张图都有可键盘访问的摘要、图例和同源数据表；颜色之外还使用文字、线型、符号和严重级别名称。

这套组合只有一个新增的直接 UI 包依赖，既满足趋势分析，又避免让通用主题库接管全部控件模板、可访问性和虚拟化行为。

## 约束与选择标准

本次组件选择按以下优先级判断：

- 默认手动刷新、可选按页自动刷新；渲染不能重新引入持续刷新或动画循环。
- 1 小时、24 小时、7 天、30 天和长期聚合趋势需要流畅缩放、悬停和阈值定位。
- P50/P95/Max 与四段链路耗时是运维分析，不需要商业 BI 图形体系。
- `VISIBLE`/`GONE`、Alert、Trace 表采用服务端分页；UI 只显示有限页。
- 键盘、UI Automation、Narrator、高对比度与 125%–200% DPI 必须能验收。
- 许可证应允许闭源/商用部署，升级面和维护风险可控。

## 图表库比较

| 方案 | 当前状态（截至 2026-08-04） | 能力与性能 | 风险 | 结论 |
|---|---|---|---|---|
| **ScottPlot.WPF** | NuGet 最新稳定版为 **5.1.59**，2026-06-22 发布，直接支持 `net8.0-windows`，MIT；官方定位就是交互式显示大型数据集。[NuGet](https://www.nuget.org/packages/ScottPlot.WPF/) [官方仓库与许可证](https://github.com/ScottPlot/ScottPlot) | DateTime 轴、散点/信号线、FillY 区间、阈值线、范围/条形图齐全；官方示例声明 Signal 图可交互显示百万点，实时数据可复用固定数组；并提供并发修改/渲染锁的明确说明。[DateTime 轴](https://scottplot.net/cookbook/5/AxisAndTicks/) [百万点 Signal 示例](https://scottplot.net/cookbook/5/ScottPlotQuickstart/) [实时数据](https://scottplot.net/faq/live-data/) [异步与锁](https://scottplot.net/faq/async/) | 基于 SkiaSharp 绘图，图内文字/数据点不会天然成为 WPF UIA 子元素；5.0→5.1 曾因 SkiaSharp 升级产生高级 API 破坏性变化。官方仓库当前也说明匿名外部贡献受限，存在维护者集中风险。[5.1 变更](https://scottplot.net/changelog/) [仓库维护说明](https://github.com/ScottPlot/ScottPlot) | **采用并封装。** 在性能、功能和依赖规模之间最合适；精确锁版本，通过适配器隔离升级风险。 |
| LiveCharts2 WPF | NuGet 最新稳定版为 **2.0.5**，2026-06-18 发布，MIT，项目活跃。[NuGet](https://www.nuget.org/packages/LiveChartsCore.SkiaSharpView.WPF/) | XAML/MVVM 体验好，自动观察集合变化；变化默认以 10 ms 节流。官方支持 Skia CPU/GPU 渲染。[工作原理](https://livecharts.dev/docs/wpf/2.0.0/Overview.How%20it%20works) | 官方安装文档明确称 GPU 视图目前不如 CPU 稳定，并建议 WPF 项目指定最低 Windows TFM；其商业 Backers 包又明确以“改善性能”为卖点。对本项目“默认不自动刷新、性能优先”的需求，自动变化/动画体系没有明显收益。[安装与 GPU 说明](https://livecharts.dev/docs/wpf/2.0.0/overview.installation) [商业包说明](https://livecharts.dev/home/buy) | **不采用。** 若未来需求转为动画化业务大屏再重新评估。 |
| OxyPlot.Wpf | 最新稳定版仍为 **2.2.0**（2024-09-03），MIT，支持 .NET 6 及以上。[NuGet](https://www.nuget.org/packages/OxyPlot.Wpf) [许可证](https://oxyplot.readthedocs.io/en/latest/introduction/license.html) | API 简单，2D 图、Tracker 和导出功能成熟。[官方文档](https://oxyplot.readthedocs.io/en/latest/) | 发布频率明显低于另外两项；官方仓库仍有 WPF 百万点性能问题记录，且维护者在 2.2.0 发布讨论中说明可投入时间有限。[性能问题](https://github.com/oxyplot/oxyplot/issues/1865) [发布讨论](https://github.com/oxyplot/oxyplot/discussions/2071) | **不采用。** 对新的性能分析工作台，没有理由选择维护和大数据证据较弱的方案。 |

### ScottPlot 在 V2 中的使用边界

采用 ScottPlot 不等于让页面直接操作 `WpfPlot`：

- 新建项目内 `TrendChartView`/`ITrendChartRenderer` 边界；输入只接受项目自己的不可变 `TrendSeries`、`TimeBucket`、`ThresholdBand` 等 DTO。
- ViewModel 不引用 `ScottPlot.*`；单元测试只测趋势投影、分位数选择、时间桶和颜色/线型语义。
- 图表只在页面加载且数据版本变化时渲染。离开页面停止渲染，不使用 `CompositionTarget.Rendering` 或高频定时器；微软指出持续订阅 `CompositionTarget.Rendering` 会使 WPF 持续动画，应及时解绑。[WPF 性能建议](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-other-recommendations)
- 聚合、排序、抽样和数组构造在线程池完成；只把最终不可变数组与一次刷新请求切回 Dispatcher。若后台修改绘图状态，按 ScottPlot 官方建议锁定 `Plot.Sync`。[ScottPlot 异步说明](https://scottplot.net/faq/async/)
- 1h/24h/7d/30d 优先请求后端适配的时间桶。365 天的 5 分钟点约 105,120 个/序列，必须由 API 或客户端降采样后再绘制，不能因库宣称“百万点”就传入所有序列原始点。
- 时间序列使用 DateTime 轴；P50/P95 用两条线并可用 FillY 表示区间，Max 独立线；ScottPlot 官方已经提供 DateTime、FillY 和 filled-error 组合能力。[DateTime](https://scottplot.net/cookbook/5/AxisAndTicks/) [FillY](https://scottplot.net/cookbook/5.0/) [Filled Error](https://scottplot.net/cookbook/5/FillY/FilledError/)
- 默认关闭图表动画和不必要交互；保留平移、框选/滚轮缩放、重置视图和最近点读数。交互必须有按钮/快捷键替代，不能只依赖鼠标。

## 阶段瀑布/时间线为何自行实现

单轮 trace 固定为四组：MES 读取、接入处理、本地投影、Watch 展示。它本质上是一个**可读的比例条 + 精确数值表**，不是任意数据探索图。

项目内控件应包含：

- 同一水平轴上的四个连续段，段宽按耗时比例计算，并设置可感知的最小宽度；
- 每段名称、绝对毫秒、占总耗时百分比和 warning/error 状态；
- 下方始终存在四行精确值表，键盘与屏幕阅读器无需进入绘图表面；
- 等待/轮询间隔单列展示，不混入处理总耗时；
- 极端长段可截断显示但必须用文字标明真实值；
- 颜色只强化状态，段标签、图案/边框和文字同时传达语义。

ScottPlot 官方虽然有水平 Range/Stacked Range 图，能够画这种形状，[范围图示例](https://scottplot.net/cookbook/5/Bar/StackedRangeHorizontal/)，但让 Skia 图形承担四个语义段会额外制造 UIA、键盘和精确文本读取问题。固定四段用原生 WPF 实现更小、更可测。

## 设计系统比较

| 方案 | 当前状态 | 优点 | 不采用的原因 |
|---|---|---|---|
| **项目内原生 WPF ResourceDictionary** | WPF 本身随 .NET 8，原生控件已有 UI Automation peer；应用资源可共享样式，并可用 `DynamicResource`/`SystemColors` 响应系统颜色。[应用资源性能](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-application-resources) [WPF 自定义控件 UIA](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control) | 最小依赖、工业风可精确控制、保留原生控件键盘/UIA/虚拟化，升级面由项目掌握。 | **采用。** 需要团队自己维护少量令牌和样式，但这正是 V2 已明确要通过原型评审锁定的产品资产。 |
| WPF-UI | 最新稳定 **4.3.0**（2026-05-04），支持 .NET 8，MIT，导航/主题/Fluent 控件完整。[NuGet](https://www.nuget.org/packages/wpf-ui/) [官方仓库](https://github.com/lepoco/wpfui) | `NavigationView` 和现代 Fluent 外观开箱即用。 | 16.42 MB NuGet 包会接管大量基础元素；NuGet 将多个近期旧版本标为“critical bugs”弃用。六页只读运维台不需要这一整套外壳，而且 Fluent 视觉并不等于项目已确认的高密度工业设计。 |
| MaterialDesignInXAML | 最新稳定 **5.3.2**（2026-05-01），支持 .NET 8，MIT，维护活跃。[NuGet](https://www.nuget.org/packages/MaterialDesignThemes/) [官方仓库](https://github.com/MaterialDesignInXAML/MaterialDesignInXamlToolkit) | 控件覆盖广、主题与图标完整。 | 19.51 MB 包并引入 `MaterialDesignColors`、`Microsoft.Xaml.Behaviors.Wpf`；Material 交互和动效语言与克制、高密度的工业运维台不匹配。 |
| MahApps.Metro | 最新稳定 **2.4.11**（2025-09-13），MIT；3.0 仍停留在 RC。[NuGet](https://www.nuget.org/packages/MahApps.Metro) | 成熟、使用面广、MetroWindow 和基础样式齐全。 | 稳定包主要目标仍是旧 .NET Core 3.0/Framework 并依赖 ControlzEx；V2 不需要自定义窗口外壳，采用它会增加模板和升级负担。 |

### 本地设计系统的最小范围

只构建本产品实际需要的语汇，不创建通用 UI 框架：

- **令牌：** 背景/表面/边框/文本、success/warning/error/offline、字号、行高、间距、圆角、焦点环、图表调色板；令牌使用 `DynamicResource`。
- **基础样式：** 主/次/危险按钮、文本输入、ComboBox、CheckBox、Tab/分段选择、DataGrid、ToolTip、ScrollBar、Dialog；尽量 `BasedOn` 原生样式并保留默认 AutomationPeer。
- **组合组件：** 左侧导航、页面标题/新鲜度条、KPI 卡、状态徽标、显式查询栏、游标分页器、空/错误/离线状态、详情抽屉、阶段时间线。
- **窗口：** 使用标准 WPF `Window` 和系统标题栏，不在 V2 自绘窗口框架。
- **图标：** 仅为六个导航项和少数状态维护小型本地图形；图标必须伴随文字或 `AutomationProperties.Name`，不可单独表达命令。

## 可访问性结论

第三方图表库不能替代应用级可访问性设计。ScottPlot 5 使用 SkiaSharp 绘图，[官方版本说明](https://scottplot.net/faq/version-5.0/)；微软说明图形中的文字不会自动被辅助技术读取，必须提供等价 `AutomationProperties.Name` 或语义摘要。[Windows 可访问文本要求](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessible-text-requirements)

因此 V2 应强制：

- 每张图设置明确的自动化名称和当前筛选/时间范围摘要；图后紧邻同源的“查看数据”表。
- 图例是普通 WPF 控件，不把唯一图例烘焙进 Skia 图面；P50/P95/Max 除颜色外使用不同线型和文字。
- 阈值、异常点和离线状态都有文本；默认文本对比度至少 4.5:1，并在高对比度主题中验证。微软的 2026 检查表同时要求键盘、名称、对比度、Narrator 与 CI 回归检查。[可访问性检查表](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-checklist)
- 自制组合控件尽量由原生控件组合；如果派生为自定义 `Control` 且承载可操作/必要信息，则实现 `FrameworkElementAutomationPeer`。WPF 的 `Grid`/`Canvas` 等布局元素本身没有 AutomationPeer。[WPF UI Automation](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/ui-automation-of-a-wpf-custom-control)
- 自动化验收包含完整 Tab 顺序、箭头键、Enter/Space、Narrator、200% DPI、高对比度和只用键盘完成趋势筛选与 trace 下钻。

## 虚拟化与大数据性能结论

需要区分三层：

1. **服务端数据虚拟化：** Demand、Alert、Trace 使用已经决定的游标分页，每次仅返回当前页；趋势端点按时间范围和目标桶数聚合。微软明确指出 WPF 原生控件没有内置数据虚拟化，因此不能用 UI 虚拟化替代分页。[WPF 控件性能](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls)
2. **WPF UI 虚拟化：** `DataGrid.EnableRowVirtualization=true`、`EnableColumnVirtualization=true`；列表设置 `VirtualizingStackPanel.IsVirtualizing=true` 与 `VirtualizationMode=Recycling`。DataGrid 默认会只创建视口内行并回收离屏行。[DataGrid 行虚拟化](https://learn.microsoft.com/en-us/dotnet/api/system.windows.controls.datagrid.enablerowvirtualization) [Recycling 示例](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/how-to-improve-the-scrolling-performance-of-a-listbox)
3. **图表数据预算：** 根据可用像素宽度选择时间桶/降采样，不在图表中保留不可见的全历史明细。图表销毁或页面离开时解绑事件和释放大数组，缓存只保留当前与相邻时间范围。

样式实现不得意外关闭虚拟化。微软列出的常见关闭条件包括直接添加容器、混用容器类型、`CanContentScroll=false` 或显式关闭 `IsVirtualizing`。[WPF 控件性能](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls)

## 许可证与供应链

- `ScottPlot.WPF 5.1.59` 与 ScottPlot 仓库使用 MIT 许可证；NuGet 依赖链包含 ScottPlot、SkiaSharp/HarfBuzz 等组件。ScottPlot 包元数据列出了 SkiaSharp 与原生资产依赖。[ScottPlot NuGet](https://www.nuget.org/packages/ScottPlot/) [ScottPlot LICENSE](https://github.com/ScottPlot/ScottPlot/blob/main/LICENSE)
- 实施时锁定精确版本并生成 `THIRD-PARTY-NOTICES`，包含所有最终发布产物里的传递依赖许可证；禁止浮动版本。
- 每次升级 ScottPlot 或 SkiaSharp 都跑图表截图、DPI、内存、长时间刷新和 UI 自动化门禁。5.1 已证明底层 SkiaSharp 大版本可能影响高级 API，适配器是必要边界，而非装饰性抽象。
- WPF-UI、MaterialDesignInXAML、MahApps.Metro 本身虽都是 MIT，但本次不采用，许可证宽松不是增加运行时依赖的充分理由。

## 实施前原型门禁

票据 04 的可运行原型应验证，而不是只凭库宣称通过：

1. 使用 ScottPlot 画 4 个阶段、每阶段 P50/P95/Max 的代表性视图；分别测试 1k、10k、100k 点/序列与 100%、150%、200% DPI。
2. 模拟 Host 30 秒响应和连续取消/切换范围；窗口导航、取消和筛选输入始终可用，旧请求不得覆盖新图。
3. 连续执行 500 次手动/定时刷新，验证无请求重入、无事件订阅泄漏、托管和原生内存不持续增长。
4. 对 100 行 DataGrid 验证响应后 300 ms 呈现目标，并确认行/列虚拟化仍开启。
5. 用 FlaUI/UIA 检查导航、图例、数据表、阶段时间线和分页器；图表至少暴露名称与摘要，所有精确值可从同源表读取。
6. 运行浅色、Windows 高对比度和离线/错误/空状态截图评审；不能因主题切换丢失焦点环、阈值或状态文字。

若 ScottPlot 在代表性 100k 点、200% DPI 或 500 次刷新测试中达不到性能/稳定性门槛，保留相同 `ITrendChartRenderer` 边界，才回到 LiveCharts2 做同一套基准；不要让两套图表库同时进入生产应用。

## 最终采用清单

| 能力 | 决定 |
|---|---|
| 趋势、P50/P95/Max、阈值/异常窗口 | `ScottPlot.WPF 5.1.59`，精确锁版，经内部适配器使用 |
| 单轮四阶段瀑布/时间线 | 原生 WPF 本地组合控件 + 精确数值表 |
| 导航、主题、基础控件 | 原生 WPF + 项目内 `ResourceDictionary` 设计令牌/显式样式 |
| Demand/Alert/Trace 大表 | 原生 `DataGrid` + 行列虚拟化 + 服务端游标分页 |
| 图表可访问性 | 本地图例、摘要、同源数据表、线型/文字冗余表达 |
| WPF-UI / MaterialDesignInXAML / MahApps.Metro | V2 不引入 |
| LiveCharts2 / OxyPlot | V2 不引入；仅在 ScottPlot 原型失败时重新评估 LiveCharts2 |

