# 选择 WPF 自动化与视觉回归测试栈

Type: research
Status: resolved
Blocked by: None

## Question

基于官方文档、源码和维护状态，MesIngestWatch V2 应采用哪套 WPF UI 自动化、截图视觉回归与 Windows CI 方案，才能覆盖关键操作旅程并稳定充当合并门禁；现有 FlaUI.UIA3 适合保留到什么程度？

## Answer

研究报告：[WPF 自动化与视觉回归测试栈](../research/02-wpf-automation-and-visual-regression-stack.md)

决定采用 `FlaUI.UIA3 5.0.0` 负责真实关键旅程，采用 `Verify.Xaml 4.2.1` 负责确定性 WPF 页面 XAML/PNG 快照，并在独立的 xUnit v3 UI 测试项目中运行；真实窗口截图作为少量高价值终态回归。Windows UI 门禁运行在固定环境、100% DPI、自动登录且不作为服务运行的专用自托管交互式 runner 上，整机串行。Appium/WinAppDriver、White 和 FlaUI.WebDriver 不采用；Microsoft `winapp ui` 仍处 Public Preview，仅保留为诊断/试验候选。先在原型与目标 runner 连续运行至少 50 次并完成视觉噪声校准，再将全窗口像素回归升级为 required check。
