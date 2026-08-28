# 18 — Watch 单 Host 非视觉会话与刷新内核

**What to build:** 让 Watch 在连接一个 Host 后，以严格契约版本和单一会话代次读取新版概览、需求系列、资格审计、错误检索、AREA 与当前关注能力；切换 Host、查询变化、慢请求或失败时，都不会把旧 Host、旧查询或迟到响应的数据混入当前窗口，并始终保留最后一份可明确标识来源的成功快照。

**Blocked by:** 17 — 冻结完整新版 API/OpenAPI 契约、旧端点暂留

**Status:** ready-for-human

- [x] ScriptedFakeHost 通过与生产相同的 HTTP、DTO、鉴权、契约检查、分页和会话入口驱动全部新版读取能力，不增加页面专用测试旁路。
- [x] 应用新 Host、凭据或契约版本时会取消旧请求、提升会话代次，并清空旧 Host 的业务快照、游标、查询、选择和详情；新连接失败或契约不匹配时不会继续显示旧 Host 数据。
- [x] Watch 要求 Host 与客户端契约版本严格匹配，且能把鉴权失败、契约不匹配、网络失败和服务端查询错误区分为可观察状态。
- [x] 数据视图自动刷新始终开启，设置只能改变各视图间隔；加载和刷新期间继续保留最后成功快照，失败时同时标明该快照时点、失败时点和陈旧状态。
- [x] 响应只有在 Host 会话、规范化页面查询和请求代次都仍匹配时才能替换成功快照；取消或迟到响应不能覆盖更新的数据。
- [x] 查询变化、快照游标无效或翻页失败时保留旧查询对应的结果并明确失败，不把旧结果冒充新条件第一页。
- [x] 刷新成功后按 SeriesId 或 DemandId 重选仍命中的对象；对象不再命中时清除详情并给出可观察原因。
- [x] 可控测试覆盖 Host 切换、慢请求、取消、迟到响应、失败保留、陈旧标记、契约不匹配、查询变化和选择重定位；本票不修改 XAML、UI Automation、DPI 或视觉基线，也不以黄金机运行作为非视觉逻辑的默认反馈环。

## Implementation evidence

- `MesIngestV2ApiClient` 使用生产 HTTP/Bearer/correlation/timeout 路径读取
  `/api/v2/contract` 及 Overview、DemandSeries、ReadabilityAudit、ErrorSearch
  （含受限原始证据）和 CurrentIngestAttention；发现身份严格比较 version、
  schema 17 与完整 capability 集，每份业务快照再次校验 contractVersion。
- `WatchV2WorkspaceSession` 在应用连接设置时同步发布空的新 Host generation，
  统一清除五类视图的查询、快照、选择与详情。Host、规范化查询、请求及选择
  四层代次门阻止取消、迟到或跨 Host 响应提交。
- 刷新状态分别保存 pending/committed/failed query、最后成功与失败时点、
  failure code 和陈旧性；查询、分页或 410 快照失败保留旧成功快照，不自动
  回退并伪装成新第一页。
- 自动刷新协调器通过可控一次性 `ITimer` 实际驱动五类 workspace refresh；
  配置只有 10/30/60/300 秒间隔，single-flight 丢弃忙时 tick，完成后从完整
  间隔重新计时。
- 确定性 focused suites：V2 client 14/14、自动刷新 16/16、workspace + 真实
  Kestrel ScriptedFakeHost surface 23/23；独立 Standards 与 Spec 复审均 PASS。
- Release 构建 0 warning / 0 error。完整 solution 只运行一次：本票所在 Watch
  UI 测试项目 105 passed / 27 个预期环境 skip / 0 failed；总解中另有 3 个与
  `HEAD` 完全相同的既有失败（安装文档 V1 字样断言、日期敏感日志保留测试、
  一次性桌面 UIA 失败；其中 UIA 定向复跑通过），未扩大本票修改范围。
- 本票未修改 XAML、UI Automation、DPI 或视觉基线；新版生产 shell 接线由票
  19 负责，因此未运行黄金机。
