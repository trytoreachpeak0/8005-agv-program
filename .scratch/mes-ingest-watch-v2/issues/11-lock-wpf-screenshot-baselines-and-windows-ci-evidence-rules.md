# 固定 WPF 截图基线与 Windows CI 证据规则

Type: grilling
Status: resolved
Blocked by: 02, 13

## Question

基于已选择的 FlaUI.UIA3、Verify.Xaml 和重新批准的 MES 任务/IngestAlert 简化原型，正式实现应固定哪些视口尺寸、DPI/缩放与主题截图基线，采用怎样的交互式 Windows runner 拓扑，并在失败时保留哪些证据、如何复核基线及治理 flaky test，才能形成稳定且可追溯的 CI 门禁？

## Comments

- 2026-08-07 人工确认视觉基线矩阵：`Verify.Xaml` 将 `1440×900` 与 `2560×1440`、100% DPI、浅色主题、中文环境作为 required 页面基线；FlaUI 真实窗口仅固定 `1440×900` 客户区终态截图，连续稳定 50 次后再升级为 required；125%/150% DPI 只做布局与 UIA 功能烟测，不做像素比较；深色主题不进入 V2。
- 2026-08-07 人工确认 runner 拓扑：使用一台专用 Windows 11 交互式 VM，桌面固定 `1920×1080`、100% DPI，专用低权限账户自动登录；runner 以用户进程而非 Windows Service 运行，整机并发固定为 1；禁止睡眠、屏保和自动锁屏，固定中文区域、浅色主题、字体、时区、Windows/.NET 补丁与渲染模式；先形成单机金镜像，不预建多机池。
- 2026-08-07 人工确认两阶段运行落点：当前开发机上的 Hyper-V VM 只用于 POC 与基线校准；正式 required gate 部署到专用、常开的 Hyper-V 主机。正式 VM 从已校准金镜像创建，并以 GitHub Actions self-hosted `watch-ui` runner 的交互式用户进程运行。
- 2026-08-07 人工确认失败证据规则：每个失败的 UI/视觉 job 上传压缩证据包，包含 expected/actual/diff PNG、Verify received XAML、关键步骤截图、完整 UIA tree、Watch 日志与标准输出/错误、fake Host 请求时间线与脱敏响应摘要、测试步骤/异常/超时和完整环境清单；仅在崩溃或无响应时附加进程 dump。PR 失败证据保留 30 天，`main` 与发布门禁证据保留 180 天，批准后的 PNG/XAML 基线随 Git 永久版本化；测试只使用假数据，证据不得包含密钥或生产数据。
- 2026-08-07 人工确认视觉基线更新治理：CI 不得自动接受 `received` 文件；基线只能在已校准 `watch-ui` runner 上通过显式流程生成，且同一快照连续 10 次完全一致后才能提出更新。基线 PR 必须包含原因、关联规格/票据、before/after/diff 拼图和环境清单，并由非提交者批准；涉及交互、文案、信息层级或状态色时还需产品/业务评审。runner 镜像升级与产品 UI 改动必须分开提交并触发全量复核；仓库只提交批准后的 baseline，不提交 received、临时 diff 或失败证据包。
- 2026-08-07 人工确认 flaky-test 治理：required test 首次失败保持红色，重跑只能诊断、不得覆盖首次失败；晋升 required 前连续通过 50 次。失败分类为产品、测试或 runner/环境缺陷；同一测试在连续 20 次中有 2 次、或滚动 100 次中有 3 次非产品失败即判 flaky。隔离必须带负责人、修复票据和最长 7 天期限；关键旅程隔离前须补稳定低层覆盖。禁止全局像素容差或大面积 mask，局部例外须有证据和独立评审；修复后连续通过 50 次才恢复 required。
- 2026-08-07 人工确认截图基线清单：`1440×900` 覆盖概览的健康/活动告警或退化/离线陈旧，MES 任务的 VISIBLE 已选详情/GONE 已选详情/空/加载/失败保留旧结果，IngestAlert 的活动已选详情/已解除历史/空/加载/失败保留旧结果，以及设置的默认/校验错误；假数据覆盖六类 `TASK_TYPE`、七个 MES 输入字段、TransportDemand 投影、六类真实 IngestAlert code 和中文长文本。`2560×1440` 只为四页各保留一个正常已加载基线。FlaUI 真实窗口只保留冷启动概览、VISIBLE/GONE 分页及任务详情、Alert→Demand 定位、慢请求取消保留旧结果、离线恢复五个高价值终态截图。
- 2026-08-07 人工确认 GitHub 门禁拆分：`watch-vm-tests` 在普通 Windows runner 上实现后立即 required；`watch-xaml-visual` 与 `watch-ui-journeys` 在专用 `watch-ui` runner 连续稳定 50 次后 required；`watch-window-visual` 先作非阻断观察 check，单独连续稳定 50 次后再 required。每个 self-hosted job 先验证镜像版本、活动桌面、分辨率、DPI、主题、区域、字体和渲染模式，不符即失败；程序集与整机均禁用并行。
- 2026-08-07 最终范围修订：当前只需要本机自动化测试，不建设 GitHub Actions、自托管 CI runner、分支保护、专用常开主机或云端门禁。本决定覆盖上述正式 runner、两阶段运行落点和 GitHub required-check 讨论；Hyper-V 仅保留为未来出现无法消除的本机渲染噪声时的可选隔离手段。

## Answer

MesIngestWatch V2 当前采用**本机 Windows 自动化验收**，不把 GitHub CI 作为实现或交接前提。正式实现应提供一个统一的本机入口，在已登录的交互式 Windows 会话中依次串行运行四组验收套件：`watch-vm-tests`、`watch-xaml-visual`、`watch-ui-journeys` 与 `watch-window-visual`。入口先检查活动桌面、分辨率、DPI、浅色主题、中文区域、字体和渲染模式；视觉环境不符时应直接报告差异并停止视觉套件，而不是产生新基线。程序集及桌面交互均不得并行。

视觉基线固定如下：

- `Verify.Xaml` 在 100% DPI、浅色主题和中文环境下，以 `1440×900` 覆盖概览的健康/退化或活动告警/离线陈旧，MES 任务的 VISIBLE 已选详情/GONE 已选详情/空/加载/失败保留旧结果，IngestAlert 的活动已选详情/已解除历史/空/加载/失败保留旧结果，以及设置的默认/校验错误；假数据覆盖六类 `TASK_TYPE`、七个 MES 输入字段、TransportDemand 投影字段、六类真实 IngestAlert code 与中文长文本。
- `2560×1440` 只为概览、MES 任务、IngestAlert 和设置各保留一个正常已加载页面基线。
- FlaUI 真实窗口只保留五个 `1440×900` 客户区终态：冷启动概览、VISIBLE/GONE 分页及任务详情、Alert→Demand 定位、慢请求取消并保留旧结果、离线后恢复连接。
- 125%/150% DPI 只做布局与 UIA 功能烟测，不作像素比较；深色主题不进入 V2。

基线只能通过显式本机更新流程生成，CI 或测试程序均不得自动接受 `received` 文件。同一快照连续运行 10 次完全一致后才能提出更新；更新须带原因、关联规格/票据、before/after/diff 拼图和环境清单，并由非提交者复核，涉及交互、文案、信息层级或状态色时还须取得产品/业务确认。仓库只保存批准后的 PNG/XAML baseline，不保存 received、临时 diff 或失败证据。

每次失败在本机输出压缩证据包：expected/actual/diff PNG、Verify received XAML、关键步骤截图、完整 UIA tree、Watch 日志与标准输出/错误、fake Host 请求时间线与脱敏响应摘要、测试步骤/异常/超时及环境清单；仅崩溃或无响应时附进程 dump。普通失败证据默认保留 30 天，人工标记的发布验收证据保留 180 天；测试只使用假数据，证据不得包含密钥或生产数据。

所有套件在成为本机发布门禁前须连续通过 50 次。失败首次出现即保持失败，重跑只用于诊断；同一测试在连续 20 次中有 2 次、或滚动 100 次中有 3 次非产品失败即判 flaky。隔离必须带负责人、修复票据和最长 7 天期限，关键旅程隔离前须补稳定低层覆盖；禁止全局像素容差或大面积 mask。修复后连续通过 50 次才恢复为本机发布门禁。

本期不要求创建 VM。若以后本机更新、显卡或字体变化造成无法稳定复现的视觉噪声，再把相同入口迁入固定 Hyper-V 金镜像；该迁移不改变测试契约，也不自动引入 GitHub CI。
