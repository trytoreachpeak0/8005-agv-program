# 选择 WPF 图表与设计系统组件

Type: research
Status: resolved
Blocked by: None

## Question

基于官方文档、源码、许可证、可访问性、虚拟化和大数据量性能，MesIngestWatch V2 的趋势图、阶段瀑布/时间线、主题与基础控件应采用哪些 WPF 组件，哪些能力应自行实现而不引入第三方依赖？

## Answer

采用 [`ScottPlot.WPF 5.1.59`](../research/03-wpf-chart-and-design-system-components.md) 作为唯一新增的直接 UI 包依赖，经项目内适配器用于趋势、P50/P95/Max、阈值和异常时间窗；四阶段瀑布/时间线、设计令牌、导航、状态、分页和基础样式均使用原生 WPF 在项目内实现。大表使用服务端游标分页加 `DataGrid` 行列虚拟化，趋势按像素预算聚合/降采样；每张 Skia 图必须配套原生 WPF 图例、语义摘要和同源数据表。V2 不引入 WPF-UI、MaterialDesignInXAML、MahApps.Metro、LiveCharts2 或 OxyPlot；原型需以 100k 点、200% DPI、500 次刷新、UIA/高对比度门禁验证 ScottPlot，失败时才在同一适配器边界下重新基准 LiveCharts2。
