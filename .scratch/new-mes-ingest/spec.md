# 新版 MesIngest 整体替换规格书

Status: ready-for-agent

Seams (confirmed): 以“脚本化 `MesTaskUnionRound` → 生产 Host/领域逻辑 → 真实 SQL Server → 版本化 HTTP API”为主要端到端验收 seam；以 `ScriptedFakeHost` → 生产 `MesIngestWatch` → UI Automation / 黄金机视觉验证为客户端 seam。纯单元测试只补时间边界、游标、错误目录与资格规则等难以从最高 seam 精确覆盖的行为。

## Problem Statement

现有 MesIngest Phase 1 能够把 MES 行投影为 `VISIBLE` / `GONE` 的 `TransportDemand`，但它以首次字段冻结、`IngestAlert` incident、`DemandChangeFeed` 和旧读取 DTO 为核心。现场现在需要解释一条搬运候选从首次出现、字段实时变化、数据异常、消失、重现到归档的完整过程；需要在不隐藏异常原始数据的前提下，只向外部程序开放当前可安全解释的 Demand；还需要按错误分类追查已经恢复的历史，并从同一投影时点核对资格、概览和详情。旧模型无法可靠表达这些事实，继续兼容或迁移旧记录会制造无法证明的 `DemandSeries`、资格与错误历史。

新版还必须解决以下运维问题：完整 `MES_TASK_UNION` 中的空值、非法值、重复键、同一 SUBLOT 多 WorkType 和无法归属的原始行不能被任选、补值或静默丢弃；Oracle 失败、不完整结果、服务重启及 `PausedZeroDrop` 保护不能伪造 Demand 消失；外部消费者不应维护会过期的 ChangeFeed 镜像；Watch 不应把当前关注项、永久错误历史、外部可读资格和 Dispatch 范围混为一谈。

## Solution

停机切换时，以空 SQL Server 数据库和全新版本化契约整体部署新版 MesIngest。Windows Service 继续通过一条只读 `MES_TASK_UNION` Oracle 语句获取六类运输候选，把每个完整成功 `MesTaskUnionRound` 原子对账为 `DemandSeries`、多代 `TransportDemand`、不可变 `DemandSeriesEvent`、当前条件、错误期间、资格投影、当前接入关注项和 `CatalogRevision`。执行失败或结构不完整的轮次只留下可追溯 `PollTrace`，不得修改 Demand、Series 或目录。

每个可识别的 `SUBLOT + WorkType` 形成一条永久可追溯的 `DemandSeries`。源字段不再冻结：唯一原始观测下的 `AREA`、`EQP`、`STEP`、`DATES`、`PACKAGE` 按成功轮次实时更新，并把有意义的变化记为事件；空值、非法值和重复多行保持真实形态，生成可诊断错误并阻断外部读取，但仍完整提供给 Watch。Demand 在有缺席权威的完整成功轮次中转为 `GONE`，连续 GONE 满 12 小时后归档；归档前重现产生同一 Series 的新 Demand 世代，归档后重现仍可供 Watch 查看，但永不进入外部可读目录。

MesIngest 对外发布当前完整 `ExternallyReadableDemandCatalog`。只有处于 `VISIBLE`、原始观测唯一、必填字段有效、没有当前数据异常且 Series 未归档的 Demand 才能进入目录。目录成员或成员业务值变化时才递增 `CatalogRevision`；外部消费者通过条件读取获得完整当前目录或 `304 Not Modified`，不再消费 ChangeFeed、Cursor 或持久业务镜像，并在自己的执行承诺点最终重读、保存 `AcceptedDemandSnapshot` 和可靠 `OrderIntent`。

新版 `MesIngestWatch` 是单 Host、业务只读的 WPF 运维客户端，信息架构为：概览、需求系列、资格审计、错误检索、AREA 筛选、接入告警，以及导航页脚中的 Host 状态与设置。Host 为概览、错误检索和资格审计提供冻结且内部一致的服务端快照；Watch 只负责查询、呈现、本机 AREA 显示配置和有限的技术遥测，不拥有或修改业务投影。

## User Stories

1. 作为现场实施工程师，我希望 MesIngest 作为 Windows Service 常驻运行，以便关闭 Watch 后仍持续轮询、投影和提供 API。
2. 作为现场实施工程师，我希望生产源使用客户批准的单条 `MES_TASK_UNION`，以便六个 UNION ALL 分支属于同一语句级一致性快照。
3. 作为 MES 数据管理员，我希望程序不修改客户 SQL、不创建 Oracle DDL、索引、视图或 CDC，以便接入保持严格只读边界。
4. 作为部署工程师，我希望 Oracle 默认使用 Thin 模式，并能通过配置切换 Thick + Instant Client，以便适配现场 Oracle 11g 而不修改业务代码。
5. 作为开发者，我希望文件与脚本化快照源可以替代 Oracle 驱动同一轮次 seam，以便在无法连接工厂 MES 时复现实证场景。
6. 作为系统，我希望每次轮询拥有稳定 `PollTraceId`、查询版本、结果类型、行数和规范化内容摘要，以便完整追踪一次不可重复的因果记录。
7. 作为系统，我希望相同 `PollTraceId` 与相同内容重放完全幂等，以便重试不重复创建 PollTrace、事件或投影。
8. 作为系统，我希望相同 `PollTraceId` 绑定不同内容时拒绝整次操作，以便幂等标识不能被重新解释。
9. 作为运维工程师，我希望 Oracle 执行失败形成可追溯 `FAILURE`，且现有投影保持不变，以便读取故障不会伪造业务变化。
10. 作为运维工程师，我希望列契约或结果结构不完整形成可追溯 `INCOMPLETE`，且现有投影保持不变，以便部分结果不会冒充完整快照。
11. 作为系统，我希望结构完整但字段值异常的原始行仍属于成功轮次，以便其它可识别业务键可以继续被真实投影。
12. 作为系统，我希望一个成功轮次的 Demand、Series、事件、当前条件、资格、目录修订和 PollTrace 在同一 SQL 事务中提交，以便任何读取都不会看到半轮状态。
13. 作为系统，我希望规范化原始行多重集合后再比较内容，以便数据库返回顺序变化不制造虚假变更事件。
14. 作为运维工程师，我希望成功轮次明确解除持续的 PollRun 失败或不完整问题，以便当前接入关注项能反映已经恢复的事实。
15. 作为运维工程师，我希望缺少 SUBLOT 或 TASK_TYPE 的原始行作为 `UnassignedMesObservation` 保存到 PollRun 证据，以便无法成键的源数据不会静默丢失。
16. 作为系统，我希望 `UnassignedMesObservation` 不生成猜测性的 DemandSeries，以便原始行不会被错误归入相似任务。
17. 作为运维工程师，我希望未归属观测的出现、内容变化和清除成为真实关注事件，以便判断问题当前是否仍存在。
18. 作为系统，我希望 `TransportDemandKey` 严格由 SUBLOT 与 WorkType 组成，以便同一 SUBLOT 在不同工序类型中保持独立生命周期。
19. 作为系统，我希望第一次观察到一个 `TransportDemandKey` 时创建稳定 `SeriesId` 的 `DemandSeries`，以便后续世代和事件属于同一可追溯生命周期。
20. 作为运维工程师，我希望 DemandSeries 展示 SUBLOT、WorkType、开始时间、生命周期、当前出现状态和最后序列，以便快速理解候选处于何种阶段。
21. 作为系统，我希望每条 Series 的事件使用严格单调 `SeriesSequence`，以便同一 Series 内的事实具有稳定顺序。
22. 作为系统，我希望只在首次发生、事实变化、条件消失或状态转换时写 `DemandSeriesEvent`，以便相同轮询观测不会膨胀为噪声历史。
23. 作为审计人员，我希望 `DemandSeriesEvent` 永久保留其 PollTrace、发生时间、主体、版本化 payload 和投影提交身份，以便历史可以重建和解释。
24. 作为系统，我希望首次看到业务键时创建第一代稳定 `DemandId`，以便本地系统能精确引用某一 Demand 世代。
25. 作为系统，我希望归档前 GONE Demand 重现时创建同一 Series 的下一代 Demand，并引用上一代 DemandId，以便重现不是对旧实例的静默复活。
26. 作为运维工程师，我希望在 Series 详情中查看所有 Demand 世代及前后继关系，以便比较每次出现的源数据和资格变化。
27. 作为系统，我希望一个成功且有缺席权威的完整轮次未包含当前业务键时把当前 VISIBLE Demand 转为 GONE，以便缺席语义基于完整快照而非计时猜测。
28. 作为系统，我希望 Demand 转为 GONE 时保留最后真实看见时间，并单独记录 GONE 确认时间，以便缺席轮次不会覆盖 `DemandLastSeenAt`。
29. 作为系统，我希望 DemandSeries 连续 GONE 满 12 小时后，在下一次有缺席权威的完整成功轮次中归档，以便短时重现和长期消失有明确边界。
30. 作为系统，我希望 GONE 计时使用 Host 的成功轮次 UTC 证据，而不是 MES `DATES`，以便生命周期不受源业务时间含义影响。
31. 作为运维工程师，我希望归档前重现清除 GONE 过程并继续同一 Series，以便临时消失不会被当成新的 Series。
32. 作为系统，我希望归档后同键重现形成 `LongGoneButVisible`，并在原 Series 中创建新的 Watch 可见 Demand，以便异常实时数据不会被隐藏。
33. 作为外部消费者，我希望归档后重现的 Demand 永远不能进入外部可读目录，以便已结束生命周期不会被自动恢复为新派车候选。
34. 作为系统，我希望服务重启后自动进入 RestartBarrier，而不是让调用方传入“可否判定缺席”的布尔值，以便缺席权威不能被绕过。
35. 作为系统，我希望重启后的第一轮完整结果只建立基线，第二轮结束保护，第三轮起才允许确认缺席，以便冷启动空快照不会清空现有 Demand。
36. 作为运维工程师，我希望 RestartBarrier 的进入、基线完成和权威恢复都留下事件，以便重启后的 GONE 行为可解释。
37. 作为系统，我希望某 WorkType 从健康非零基线骤降为零时进入 `PausedZeroDrop` / TaskTypeProtection，以便可疑全空结果不批量标记 GONE。
38. 作为系统，我希望 TaskTypeProtection 只阻断对应 WorkType 的缺席权威，以便其它 WorkType 正常对账。
39. 作为运维工程师，我希望保护期间的成功空轮次不推进 Demand GONE 或 Series 归档，以便保护具有真实业务效果。
40. 作为系统，我希望连续两轮健康非零结果后解除对应保护，且下一完整轮才恢复缺席权威，以便恢复过程不会在同一轮自相矛盾。
41. 作为运维工程师，我希望保护进入、恢复进度和解除都成为当前关注项及概览动态，以便能够解释某类 Demand 为什么没有消失。
42. 作为运维工程师，我希望每个可识别业务键的一轮全部原始行作为 `DemandRawObservation` 保存，以便空值和重复记录都有直接证据。
43. 作为系统，我希望同键只有一条原始行时形成可信的 `LiveMesFieldSet`，以便当前 MES 值可以结构化读取。
44. 作为系统，我希望同键有两条或更多原始行时仍只创建一个 Demand，并保存全部行，以便不任选一行制造虚假单值投影。
45. 作为运维工程师，我希望重复行恢复为唯一行时继续更新同一个 Demand 世代，以便数据修复不会制造无必要的新 Demand。
46. 作为系统，我希望 AREA、EQP、STEP、DATES、PACKAGE 在唯一观测下随成功轮次实时更新，以便 Watch 和外部目录反映当前 MES 事实。
47. 作为审计人员，我希望实时字段变化形成带 before/after 的事件，以便可以追溯某个 Demand 的源值演变。
48. 作为系统，我希望当前字段变为 NULL 或空白时保存真实空值，而不是回填历史值，以便数据问题不被旧投影掩盖。
49. 作为系统，我希望 `DATES` 作为 `MesSourceDate` 原值处理，而不是解释为 Series 开始时间、Host 观测时间或链路延迟，以便时间语义准确。
50. 作为系统，我希望 `STEP` 表示 MES 下一工序且不进入业务键，以便工序字段变化不错误创建新 Series。
51. 作为系统，我希望 MesArea 只接受领域格式 `^[A-Z][1-9][0-9]?-[1-9][0-9]?$`，以便非法前导零或非规范区域不会被静默正规化。
52. 作为运维工程师，我希望同一 SUBLOT 同轮出现在多个 WorkType 时，每个复合键仍形成独立 Series 和 Demand，以便真实来源数据完整可查。
53. 作为系统，我希望同 SUBLOT 多 WorkType 在每个受影响 Demand 上形成结构化异常并阻断外部读取，以便外部程序不会自行猜测正确工序。
54. 作为系统，我希望多 WorkType 冲突恢复后，在仍可见的相关 Series 上明确关闭对应错误，以便当前条件与历史事实均准确。
55. 作为运维工程师，我希望所有数据异常都不会阻止 Demand 生成或进入 WatchDemandProjection，以便坏数据可见、可诊断、可核验。
56. 作为系统，我希望 `DemandSeriesCurrentCondition` 由事件推导且不拥有独立 incident 身份，以便当前状态和历史事实不会形成两套真相。
57. 作为系统，我希望第一版错误目录固定发布 `REQUIRED_MES_FIELD_MISSING`、`INVALID_MES_FIELD_FORMAT`、`DUPLICATE_TRANSPORT_DEMAND_KEY`、`SUBLOT_MULTIPLE_WORK_TYPES` 和 `LONG_GONE_BUT_VISIBLE`，以便 Host 与 Watch 使用相同稳定代码。
58. 作为运维工程师，我希望错误按 `DATA_COMPLETENESS`、`DATA_FORMAT`、`OBSERVATION_CONFLICT`、`LIFECYCLE_CONFLICT` 唯一主分类，以便导航和分面计数不会因客户端不同而漂移。
59. 作为系统，我希望已发布 SeriesErrorCode 不换义、不复用且不静默重分类，以便历史在新版本中仍能按原含义解释。
60. 作为系统，我希望新增错误规则只从部署生效时产生事实，不回扫制造部署前历史，以便审计时间可信。
61. 作为系统，我希望错误期间由 `SeriesId + SeriesErrorCode + Target + SubjectKind` 唯一标识，以便同一条件持续存在时不会每轮新建错误。
62. 作为系统，我希望错误证据值或关联 WorkType 集合变化只追加期间证据而不切断期间，以便条件身份与诊断内容分离。
63. 作为系统，我希望完整成功轮次提供反证后，以 `CONDITION_CLEARED` 或 `DEMAND_GONE` 关闭错误期间，以便数据修复与对象消失得到不同解释。
64. 作为系统，我希望 FAILURE、INCOMPLETE、Host 断联或 Watch 刷新失败都不能关闭错误期间，以便缺少证据不会被称为恢复。
65. 作为部署工程师，我希望空库上线后的首个完整成功轮次以 `BOOTSTRAPPED_CURRENT_CONDITION` 建立当时的错误，以便不推测旧系统中的开始时间。
66. 作为审计人员，我希望 Series 错误期间和证据永久保留，不受旧 IngestAlert 365 天清理规则影响，以便归档 Series 的历史仍可查询。
67. 作为外部消费者，我希望只读取当前完整 `ExternallyReadableDemandCatalog`，以便不必持久化和恢复 DemandChangeFeed Cursor。
68. 作为外部消费者，我希望目录不接受 WorkType、AREA、车辆、地图或站点筛选参数，以便 MesIngest 发布统一事实而不混入 Dispatch 范围。
69. 作为外部消费者，我希望首次读取获得完整目录和 `CatalogRevision`，以便可以建立可随时丢弃的当前缓存。
70. 作为外部消费者，我希望使用上一 `CatalogRevision` 条件读取，目录未变时获得 `304 Not Modified`，以便减少无意义传输。
71. 作为系统，我希望目录只有在成员集合或成员业务值改变时递增一次修订，以便无变化轮次不制造版本噪声。
72. 作为系统，我希望目录修订与本轮所有业务投影在同一事务提交，以便消费者不会看到新 Revision 配旧数据。
73. 作为外部消费者，我希望目录项包含 DemandId、SeriesId、TransportDemandKey、世代、DemandRevision、时间和当前可信 MES 字段，以便可精确判断并引用候选。
74. 作为系统，我希望只有 VISIBLE、唯一原始观测、必填字段有效、没有当前数据异常且 Series 未归档的 Demand 成为 `ExternallyReadableDemand`，以便资格是集中且可审计的契约。
75. 作为外部消费者，我希望不合格 Demand 从目录移除但仍保留在 Watch 和审计中，以便安全边界不会销毁诊断事实。
76. 作为 Dispatch 开发者，我希望在执行承诺点最终读取当前 Demand 和 Revision，并原子保存 `AcceptedDemandSnapshot` 与 `OrderIntent`，以便后续源变化不会改写历史决策证据。
77. 作为 Dispatch 开发者，我希望远程建单超时复用同一幂等键收敛结果，以便结果未知不会导致重复订单。
78. 作为 Dispatch 开发者，我希望本地取消继续以 TransportDemandKey 永久抑制，而不回写 MesIngest，以便接入事实与调度决策保持分离。
79. 作为运维工程师，我希望资格审计列出每一个已生成 Demand 世代，包括 VISIBLE、GONE、已归档和 LongGoneButVisible，以便当前目录之外的原因也能被解释。
80. 作为运维工程师，我希望资格审计分别显示 `READABLE` 与 `NOT_READABLE`，以便资格不与 VISIBLE/GONE 生命周期混淆。
81. 作为运维工程师，我希望不可读 Demand 展示全部稳定 `ReadabilityBlocker`，而不只显示一条错误消息，以便能够完整解释资格结论。
82. 作为运维工程师，我希望第一版阻断目录覆盖 `DEMAND_GONE`、`SERIES_ARCHIVED`、`LONG_GONE_BUT_VISIBLE`、`DUPLICATE_TRANSPORT_DEMAND_KEY`、`SUBLOT_MULTIPLE_WORK_TYPES`、`REQUIRED_MES_FIELD_MISSING` 和 `INVALID_MES_FIELD_FORMAT`，以便资格与领域错误有明确映射。
83. 作为运维工程师，我希望列表使用 Host 选择的稳定主要阻断原因，同时详情保留全部原因，以便摘要易读又不丢失事实。
84. 作为运维工程师，我希望资格审计在一个冻结 `ReadabilityAuditSnapshot` 中返回列表、精确总数、资格分面、原因分面和详情，以便翻页期间不会混入新提交。
85. 作为运维工程师，我希望一个 Demand 可计入多个原因分面但不可读总数仍按 Demand 去重，以便统计不会被机械相加误读。
86. 作为运维工程师，我希望资格审计支持资格、WorkType、阻断原因、DemandId 和 SUBLOT 筛选，以便从总体快速缩小到具体对象。
87. 作为运维工程师，我希望资格审计默认先列不可读项，再按主要原因、最后看见时间和 DemandId 稳定排序，以便最需要诊断的对象优先。
88. 作为运维工程师，我希望审计默认每页 100、最多 200，并由 Host 在筛选后返回精确总数，以便数据量有界且计数可信。
89. 作为运维工程师，我希望资格游标绑定快照、规范化筛选、AREA 范围、固定顺序和契约版本，以便不能跨条件错误复用。
90. 作为运维工程师，我希望无效、过期或不匹配的资格游标明确失败并保留旧结果，以便客户端不会静默冒充第一页。
91. 作为运维工程师，我希望资格详情包含全部检查、原始观测冲突、所属 Series、PollTrace、投影提交和 CatalogRevision，以便可以从结论追到证据。
92. 作为运维工程师，我希望从资格项跳转需求系列时携带 SeriesId、DemandId 和来源快照摘要，以便目标页能够说明当前事实是否已变化。
93. 作为运维工程师，我希望错误检索能按主分类找到曾发生过该错误的所有 DemandSeries，包括已经恢复的历史，以便排查重复或长期问题。
94. 作为运维工程师，我希望错误检索默认查看截至查询时点最近 7×24 小时，同时可选最近 24 小时、30 天和全部历史，以便常用范围快捷且含义精确。
95. 作为运维工程师，我希望错误窗口使用 UTC 半开区间 `[from, to)`，以便边界不会重复计数且不依赖本地午夜。
96. 作为运维工程师，我希望错误检索默认同时包含 ACTIVE 与 ENDED，并可显式筛选状态，以便历史页不会把已恢复问题隐藏掉。
97. 作为运维工程师，我希望错误检索支持分类、错误码、活动状态、时间、SeriesId、DemandId 和 SUBLOT 条件，以便按问题和对象两个方向定位。
98. 作为运维工程师，我希望 SeriesId、DemandId、错误码精确匹配而 SUBLOT 使用不区分大小写包含匹配，以便标识查询规则可预测。
99. 作为运维工程师，我希望错误结果以 DemandSeries 去重，并保留跨 Demand 世代的所有命中期间和证据，以便列表数量不会被事件数量放大。
100. 作为运维工程师，我希望错误结果按 ACTIVE 优先、最近匹配证据时间降序、SeriesId 升序稳定排列，以便翻页结果稳定且当前问题优先。
101. 作为运维工程师，我希望错误检索冻结 `ErrorSearchAsOf`，并让列表、分面、状态、分页和详情共用该时点，以便查看过程中不会前后矛盾。
102. 作为运维工程师，我希望错误页默认每页 100、最多 200，并返回精确 Series 总数，以便无需从第一页估算总体。
103. 作为运维工程师，我希望错误游标绑定完整筛选、固定顺序、ErrorSearchAsOf 和契约版本，以便篡改或跨查询复用会明确失败。
104. 作为运维工程师，我希望错误详情只展示当前筛选真正命中的期间和证据，并标明跨出窗口的期间边界，以便证据不被裁剪或混入无关错误。
105. 作为运维工程师，我希望诊断证据默认包含字段、观测值、规则、DemandId/WorkType、证据时间和 PollTrace，以便无需读取任意日志即可解释问题。
106. 作为安全负责人，我希望完整原始观测只能按需、有大小上限且通过敏感字段白名单读取，以便诊断能力不会成为数据泄露通道。
107. 作为运维工程师，我希望成功且零命中的错误查询只表示该条件下没有历史，而不自动宣称系统健康，以便空结果不被误解。
108. 作为运维工程师，我希望错误检索不受当前 AreaFilterProfile 静默影响，以便 AREA 缺失或非法的错误不会被隐藏。
109. 作为运维工程师，我希望接入告警页只展示当前 `CurrentIngestAttention`，以便当前处置入口不被已恢复历史淹没。
110. 作为运维工程师，我希望接入告警可包含活动 Series 错误、PollRunFailure、TaskTypeProtection 和未归属观测等全局问题，以便所有当前接入风险有统一入口。
111. 作为运维工程师，我希望接入告警中的 Series 项直接引用稳定错误身份并下钻错误检索，以便不再复制一套 fingerprint incident 生命周期。
112. 作为运维工程师，我希望已结束的 Series 错误只留在错误检索而不留在当前告警，以便“当前”和“历史”语义清楚。
113. 作为现场运维工程师，我希望概览在一个 `WatchOverviewSnapshot` 中汇总需求系列、资格、活动错误、当前关注项和近期动态，以便十秒内判断态势。
114. 作为现场运维工程师，我希望概览各摘要共享同一投影提交身份和时间，以便不同时间点的卡片不会伪装成一个当前状态。
115. 作为现场运维工程师，我希望 Series 摘要返回当前 AREA 范围内的精确总数、Tracking/Archived 分面、GONE 和 LongGoneButVisible 关注数量，以便从生命周期角度理解全局。
116. 作为现场运维工程师，我希望资格摘要返回同一审计口径下的 Demand 总数、READABLE 和 NOT_READABLE 数，以便分子分母来自同一快照。
117. 作为现场运维工程师，我希望错误摘要显示不受 AREA 配置影响的当前 ACTIVE Series 数和最近 7 天命中过的 Series 数，以便当前风险与近期历史同时可见。
118. 作为现场运维工程师，我希望关注摘要显示当前项的精确总数、类型和严重度构成，以便知道当前需要处理什么。
119. 作为现场运维工程师，我希望概览只展示最近 24 小时最新五条真实状态转换，并按时间与稳定事件 id 排序，以便动态列表不是每轮轮询噪声。
120. 作为现场运维工程师，我希望概览卡片和子摘要携带明确目标查询跳转到对应页面第一页，以便下钻不会依赖目标页隐含默认值。
121. 作为现场运维工程师，我希望概览刷新失败时整份保留上一成功快照并标注快照时点、失败时间和当前连接状态，以便不混合新旧卡片。
122. 作为现场运维工程师，我希望概览无近期动态时只显示“近期无重点动态”，而不据此宣称系统健康，以便结论不超出证据。
123. 作为 Watch 用户，我希望一次只连接一个 Host，切换 Host 时使旧请求、缓存、选择和快照全部失效，以便旧 Host 数据不会串入新会话。
124. 作为 Watch 用户，我希望 Host 与 Watch 必须使用相同 API 契约版本，以便客户端不会对新字段和新状态做旧版降级解释。
125. 作为 Watch 用户，我希望导航包含概览、需求系列、资格审计、错误检索、AREA 筛选和接入告警，并在页脚提供紧凑 Host 状态与设置，以便信息架构与领域职责一致。
126. 作为 Watch 用户，我希望需求系列页能浏览 Tracking、GONE、Archived 与归档后可见状态，并查看 Demand 世代、生命周期节点和事件流，以便完整解释一条业务键。
127. 作为 Watch 用户，我希望需求系列与资格审计共享当前 AreaFilterProfile，以便用同一现场 AREA 范围核对对象和资格。
128. 作为 Watch 用户，我希望 AreaFilterProfile 是当前 Windows 用户的本地命名 TXT 配置，以便现场可维护显示范围且不修改 Host 业务状态。
129. 作为 Watch 用户，我希望 AREA 筛选采用已选的主从编辑布局，左侧保留配置列表，右侧展示文件内容、验证、保存和应用状态，以便管理多个配置时不丢上下文。
130. 作为 Watch 用户，我希望草稿 AREA 配置通过 MesArea 格式、重复项和空项校验后才能应用，以便非法范围不会产生误导性页面结果。
131. 作为 Watch 用户，我希望切换或保存 AREA 配置后，需求系列、资格审计和概览相关摘要重新查询，以便范围变化即时可见。
132. 作为外部消费者，我希望 AreaFilterProfile 不改变 WatchDemandProjection、外部资格、CatalogRevision 或 Dispatch AREA 范围，以便本地显示配置没有业务副作用。
133. 作为 Watch 用户，我希望不可信 AREA 的 Demand 只在“全部 AREA”资格审计中出现，而不借历史 AREA 命中配置，以便当前范围查询不伪造可信值。
134. 作为 Watch 用户，我希望错误检索与接入告警不被 AreaFilterProfile 过滤，以便位置异常和全局问题始终可见。
135. 作为 Watch 用户，我希望数据页自动刷新始终开启且只在设置中配置间隔，以便界面保持最新而不出现“忘记开启”的隐患。
136. 作为 Watch 用户，我希望加载和刷新保留最后成功快照，并以非阻塞状态显示进行中，以便慢 Host 不清空可用信息。
137. 作为 Watch 用户，我希望刷新失败保留上一成功查询、快照和选择，并明确标注陈旧与失败，以便旧结果不会冒充新筛选结果。
138. 作为 Watch 用户，我希望刷新成功后按 SeriesId 或 DemandId 重选仍命中的对象，不再命中时清除详情并提示，以便详情不会指向旧快照对象。
139. 作为 Watch 用户，我希望服务端在筛选后分页、计数和稳定排序，Watch 不下载全部历史本地处理，以便历史增长不会拖垮客户端。
140. 作为 Watch 用户，我希望分页控件展示准确总数和总页数，并支持上一页、下一页及直接页码跳转，由 Host 在同一冻结快照内解析位置，以便可导航且不破坏快照一致性。
141. 作为 Watch 用户，我希望所有列表、筛选、详情、错误和状态均有稳定 UI Automation 名称和键盘焦点，以便可访问性工具与正式旅程测试可靠操作。
142. 作为 Watch 用户，我希望状态始终以文字或图标表达而不只靠颜色，以便高对比度和色觉差异下仍可理解。
143. 作为 Watch 用户，我希望时间以本地绝对时间为主并可复制带偏移量值，以便现场沟通不依赖模糊相对时间。
144. 作为 Watch 用户，我希望错误检索使用已选的“分类导航 + 证据详情”三列布局，并让三列共享上下边界填满内容高度，以便从分类到 Series 再到证据的关系清晰。
145. 作为 Watch 用户，我希望概览使用已选的“页面摘要卡 + 跨页重点动态”布局，Host 状态保持紧凑全局状态，以便业务态势而非连接信息成为主内容。
146. 作为 Watch 用户，我希望生产 UI 使用 WPF UI 的 FluentWindow、TitleBar、NavigationView、Card、InfoBar 和主题资源，以便产品保持原生、克制和一致。
147. 作为 Watch 用户，我希望 1440×900 为主设计基线，2560×1440 合理扩展，720 epx 最小宽度及 125%/150% DPI 能重排或滚动，以便常用现场显示环境不裁切关键操作。
148. 作为安全负责人，我希望 Watch 业务接口保持只读，唯一允许的写入是受控、白名单、追加且幂等的 WatchRefreshTrace 遥测入口，以便技术观测不会演变为业务命令通道。
149. 作为安全负责人，我希望 WatchRefreshTrace 不包含凭据、任意日志、原始敏感数据或业务修改字段，以便遥测最小化。
150. 作为部署工程师，我希望本地默认只绑定 loopback，非本机访问必须启用共享密钥并保护配置，以便只读 API 不等于公开 API。
151. 作为部署工程师，我希望 Oracle、SQL Server 与 API 凭据只存在于现场配置、环境变量或外部凭据引用中，以便秘密不进入仓库、发布包模板和日志。
152. 作为部署工程师，我希望发布包包含 Service、Watch、唯一正式查询副本、空配置模板、安装/卸载脚本、版本化 OpenAPI 和验证说明，以便现场可复制部署和核验。
153. 作为发布负责人，我希望新版上线前明确停止旧 Host、Watch 和所有外部消费者，以便不会出现新旧契约混合运行。
154. 作为发布负责人，我希望在确认精确目标实例并完成现场备份后删除旧 MesIngest 数据库，由新版建立空库，以便不把不可证明的旧记录迁入新模型。
155. 作为发布负责人，我希望新历史只从首个完整成功 MesTaskUnionRound 开始，以便 DemandSeries 和错误期间都有可证明起点。
156. 作为发布负责人，我希望回退只能恢复整套旧部署和其独立数据库备份，以便不尝试让新 Host 读取旧 schema 或旧 Watch 读取新 API。
157. 作为测试工程师，我希望同一套脚本化轮次通过生产 Host、真实 SQL Server 和版本化 API 验证领域行为，以便最高 seam 覆盖事务、持久化和对外契约。
158. 作为测试工程师，我希望重启测试在第一、第二、第三个成功空轮次分别验证基线、权威恢复和 GONE，以便 RestartBarrier 的边界不可被回归。
159. 作为测试工程师，我希望完整覆盖唯一行、空字段、非法 AREA、重复行换序、跨 WorkType、GONE、归档、归档后重现、FAILURE、INCOMPLETE 和 PollTrace 重放，以便关键状态机有端到端证据。
160. 作为测试工程师，我希望在真实 SQL Server seam 中验证投影事务失败不会留下半提交、CatalogRevision 不倒退且重启后历史一致，以便存储可靠性不只由内存测试证明。
161. 作为测试工程师，我希望 API 契约测试验证精确计数、快照身份、筛选、稳定顺序、游标绑定、304、错误码和大小上限，以便消费者行为可独立实现。
162. 作为测试工程师，我希望 Watch 通过 ScriptedFakeHost 驱动生产查询和状态接口，以便延迟、失败、取消、迟到响应、Host 切换和快照陈旧可确定性复现。
163. 作为测试工程师，我希望 WPF 视觉变更先在黄金机生成真实预览并由用户确认，再稳定运行和提升基线，以便视觉验收不由本地桌面截图替代。
164. 作为测试工程师，我希望所有 WPF UI 旅程在校准的 1920×1080、96 DPI、zh-CN、浅色主题、SoftwareOnly 环境中运行，并在一次性离线克隆验证 125%/150% DPI，以便结果可重复。
165. 作为发布负责人，我希望工厂验证分别证明 Oracle 只读查询、SQL Server 持久化、Service 独立于 Watch、API 鉴权、目录条件读取和关键 Watch 页面，以便本机通过不被误写成现场通过。

## Implementation Decisions

- 遵循 ADR-mes-0006 的边界：MesIngest 只拥有 MES 接入事实和外部可读目录，不拥有 DispatchTask、取消抑制、车辆、站点、路线、RIoT Order 或派车决策。
- 遵循 ADR-mes-0007 的技术栈：全 C#、.NET 8 Windows Service、WPF 薄客户端、SQL Server 投影、Kestrel API；Oracle 默认 Thin，Thick + Instant Client 仅为配置切换。
- 正式 `MES_TASK_UNION` 仍是六类任务的开发与发布唯一查询原稿；生产代码不得复制一份会漂移的 SQL，也不得按六个分支分别查询。
- `MesTaskUnionRound` 只有 `SUCCESS`、`FAILURE`、`INCOMPLETE` 三类结果。只有 SUCCESS 能进入业务投影事务；字段值异常属于 SUCCESS 数据证据，而不是 INCOMPLETE。
- `PollTraceId` 及其规范化内容摘要构成轮次幂等边界；相同 id、相同内容不产生副作用，相同 id、不同内容是契约冲突。
- 每个 SUCCESS 使用一个 ProjectionCommit 原子提交轮次涉及的 PollTrace、DemandSeries、TransportDemand、DemandSeriesEvent、当前条件、错误期间、资格投影、当前接入关注项和 CatalogRevision。
- 原始行按稳定规范化内容排序后作为多重集合比较；数据库返回顺序本身不构成业务变化。
- 缺少 SUBLOT 或 TASK_TYPE 的行形成 UnassignedMesObservation 并归 PollRun 所有；其它可识别行继续投影，不能因为局部坏行把完整成功轮次降级成部分失败。
- DemandSeries 由大小写与空白规则明确的 TransportDemandKey（SUBLOT + WorkType）唯一标识。实现必须在契约中固定比较规则，Host、SQL 唯一约束和 Watch 查询使用同一规则，不在各层自行正规化。
- DemandSeries 第一次本地观察时开始，稳定 SeriesId 永不因 GONE、重现或归档后可见而更换。Series 内事件按单调 SeriesSequence 排序。
- TransportDemand 是 DemandSeries 内的一代实例。当前 Demand GONE 后，归档前再次观察同键创建下一代 DemandId；原 Demand 永久保留并由 predecessor 关系连接。
- 当前 VISIBLE Demand 的唯一原始行实时形成 LiveMesFieldSet；AREA、EQP、STEP、DATES、PACKAGE 每次有意义变化都更新当前值并写事件。新版不保留 FrozenMesFieldSet 或 FIELD_DRIFT 语义。
- DuplicateTransportDemandKeyObservation 保存同键的全部规范化原始行，不选主行、不拼接字段、不生成多条 Demand；恢复唯一时继续当前 Demand 世代。
- WorkType 来自 TASK_TYPE 并参与业务键；同一 SUBLOT 多 WorkType 各自形成独立 Series，同时在全部受影响当前 Demand 上形成冲突证据。
- Demand 缺席只能由模块根据完整 SUCCESS、RestartBarrier 和 TaskTypeProtection 内部计算权威；任何调用方均不得传入可绕过保护的 `absenceAuthority` 布尔值。
- 服务启动进入两轮重启保护：第一轮完整结果建立基线，第二轮结束保护，下一轮才拥有缺席权威。保护阶段仍可创建/更新可见 Demand，但不能推进 GONE 或归档。
- PausedZeroDrop / TaskTypeProtection 沿用每 WorkType 健康非零基线和连续两轮健康非零恢复规则；保护解除后的下一完整轮才恢复该类型的缺席权威。
- 有缺席权威的首个完整成功缺席轮次即把当前 Demand 标为 GONE；不再沿用旧版“连续两轮缺席才 GONE”的实现。DemandLastSeenAt 保持最后真实看见时间，GoneConfirmedAt 单独记录。
- DemandSeries 从 GoneConfirmedAt 起连续 GONE 满 12 小时后，只能在后续有缺席权威的完整成功轮次中归档。
- 归档是不可逆生命周期转换。归档后重现继续原 Series 并创建新的 Watch Demand 世代，但产生 LONG_GONE_BUT_VISIBLE 且永久阻断该 Demand 外部读取。
- SeriesErrorCatalog 由领域契约版本化发布。第一版五个代码和四个主分类固定；代码可以新增或 deprecated，但不得换义、复用、改主分类、改作用域或回扫重写旧历史。
- DemandSeriesCurrentCondition 是 DemandSeriesEvent 的当前投影，不是聚合根；IngestAlert 也不再拥有 Series 错误的独立 incident 生命周期。
- DemandSeriesErrorPeriod 从事件推导并永久保留。Demand 级错误不得跨 DemandId 延续，Series 级错误可以跨世代但必须保留逐世代证据。
- Series 错误证据使用 Host 在完整成功轮次中的 UTC 时间；不使用 MesSourceDate 或 Watch 本机时间确定期间边界。
- 错误期间只由完整 SUCCESS 的明确反证以 CONDITION_CLEARED 或 DEMAND_GONE 结束；故障、断联、取消和刷新失败都没有结束错误的权威。
- ExternallyReadableDemand 的判定由领域层集中执行：VISIBLE、唯一观测、全部必填字段有效、无当前数据异常、Series 未归档。Watch 和外部消费者不得复制规则。
- ReadabilityBlockerCatalog 与 SeriesErrorCatalog 分离。阻断码解释“为什么当前不能外读”，错误码解释“Series 曾发生何种错误”；一个 Demand 可同时有多个阻断原因。
- ExternallyReadableDemandCatalog 始终包含全范围的当前合格 Demand，不接受 Dispatch 的 WorkType/AREA/车辆/站点参数。目录按 DemandId 稳定输出。
- CatalogRevision 是单调版本，仅在目录成员或成员业务值变化时递增；同一轮多项变化只产生一个新修订。外部读取支持 ETag/条件请求及 304。
- 新契约删除 DemandChangeFeed、bootstrap high-watermark 和 `SYNC_CURSOR_EXPIRED`。外部消费者的目录缓存必须可丢弃；业务持久化从 AcceptedDemandSnapshot、OrderIntent 和自身任务状态开始。
- 外部消费者在执行承诺点必须最终读取并保存不可变 AcceptedDemandSnapshot、CatalogRevision 与接受时间；MesIngest 不负责消费者的事务、RIoT 幂等调用或来源变化复核状态机。
- WatchDemandProjection 包含全部 Demand、原始观测、实时字段、当前条件和资格，不按外部可读性过滤。
- ReadabilityAuditSnapshot 绑定 ProjectionCommit 身份并携带当时 CatalogRevision；CatalogRevision 不能代替审计快照，因为始终不可读 Demand 的原因变化可能不改变目录。
- 资格审计的筛选、精确计数、分面、稳定顺序、分页和详情均在 Host 端基于同一快照完成。默认 100、最大 200；无效/过期游标明确失败。
- ErrorSearchSnapshot 由 Host 在 ErrorSearchAsOf 从永久 DemandSeriesEvent 重建。列表、分面、活动状态、分页和详情必须共享该时点；默认窗口为精确最近 7×24 小时。
- 错误历史查询结果按 DemandSeries 去重，固定 ACTIVE 优先、最近证据降序、SeriesId 升序；第一版不提供任意列排序，不提供导出。
- CurrentIngestAttention 只表示当前运维关注，可投影活动 Series 错误、PollRunFailure、TaskTypeProtection 和无法归属 Series 的问题；它不保存已恢复 Series 错误副本。
- WatchOverviewSnapshot 由 Host 从一个 ProjectionCommit 原子计算并返回所有业务摘要和最近动态。AREA 配置名称与本地状态由 Watch 单独叠加，不能伪装成 Host 快照字段。
- OverviewAttentionEvent 只来自真实领域转换；概览返回最近 24 小时最新五条，不用静态总数变化或每轮观测制造动态。
- Host 提供版本化契约发现、Poll 健康/证据、概览、DemandSeries 列表与详情、Demand 世代与事件、资格审计、错误目录与错误检索、CurrentIngestAttention、ExternallyReadableDemandCatalog 等有界读取能力。具体 URI 在 API 设计票中定稿，但同一能力不得同时维护新旧 DTO。
- 所有历史和审计读取在 Host 端筛选、计数、稳定排序及有界分页。Watch 不下载全表，不用当前页计算总数或分面。用户页码跳转由 Host 在冻结快照上下文内解析，不由客户端本地切片冒充。
- Watch 维持单 Host 会话。应用新 Host 或凭据时取消旧请求、提升会话代次、清空全部业务快照和选择，再进行契约检查；失败时不展示旧 Host 数据。
- Watch 使用 WPF UI 4.x 和既定 Fluent 设计系统。已选信息架构以及需求系列/资格审计方向、AREA Variant A、Error Search Variant A、Overview Variant A 是生产信息层级依据；原型 XAML、假数据和硬编码不得直接进入生产。
- AreaFilterProfile 是当前 Windows 用户的本地 TXT-backed 命名配置。它只作为需求系列、资格审计和概览相关摘要的 Host 查询条件；不改变错误检索、接入告警、外部资格、CatalogRevision 或 Dispatch 范围。
- Watch 所有数据视图自动刷新始终开启；设置只调整间隔。刷新采用成功快照原子替换，加载/失败保留上一成功快照，迟到响应必须同时匹配 Host 会话、页面查询和请求代次。
- Watch 业务 API 保持只读。若保留 WatchRefreshTrace，则只能通过独立受控入口追加白名单技术证据，必须鉴权、幂等、限流、限制大小并拒绝任意日志或业务字段。
- SQL Server schema、API、DTO、OpenAPI、Host、Watch 和外部消费者作为一个新契约版本同时切换，不提供旧 schema/API 适配器或新旧混跑模式。
- 按 ADR-mes-0017 执行空库切换：人工确认目标、停机和备份后删除旧数据库，由新 Host 建立新 schema；运行时代码和 Watch 不得自动删除数据库。
- 新系统不迁移旧 TransportDemand、冻结字段、IngestAlert incident、DemandChangeFeed、PollHealth 或历史 DTO。首个完整 SUCCESS 是所有新 Series 与错误 bootstrap 的最早可证明起点。
- 回退是部署级整体恢复：停止新版，恢复旧程序、旧配置和独立旧数据库备份；不允许新程序连接旧库或旧程序连接新库。
- 安全边界延续本机默认绑定、远程绑定强制共享密钥、凭据外置、日志脱敏和工厂返回包脱敏；OpenAPI 文档可独立发布，但业务数据端点必须遵循访问控制。
- 数据持续增长通过 SQL Server 差异写入、必要索引、事件不可变追加、当前投影表和有界查询控制；不得每轮加载/重写全部历史或在 Watch 本地分页。

## Testing Decisions

- 好测试只断言可观察行为：给定轮次、时间、重启/保护状态和查询，验证提交后的 API、持久化重启结果、事件顺序、资格、目录修订和 Watch 展示；不绑定内部私有类、表连接顺序或控件树偶然结构。
- 主要验收 seam 已由用户确认：脚本化 MesTaskUnionRound 进入生产 Host/领域入口，写入真实 SQL Server，再经正式版本化 HTTP API读取。它是领域、事务、schema、持久化和 API 契约的首选集成测试入口。
- 该主要 seam 至少覆盖：首次唯一观测、无变化轮次、实时字段变化、必填字段缺失/恢复、非法 AREA/恢复、重复行 A/B 与 B/A 顺序交换、恢复唯一、同 SUBLOT 多 WorkType/恢复、未归属行、GONE、12 小时归档、归档前重现、归档后重现、FAILURE、INCOMPLETE、PollTrace 幂等重放与内容冲突。
- 重启权威测试必须持久化一条 VISIBLE Demand，重启 Host 后依次提交三个空 SUCCESS，并从 API 证明前两轮不 GONE、第二轮仅恢复权威、第三轮才 GONE；不得用纯内存构造替代这一发布门禁。
- TaskTypeProtection 测试必须证明：目标类型进入保护、保护空轮不 GONE、其它类型仍正常、两轮非零恢复只解除保护、随后空轮才 GONE，且所有进度事件和概览/关注摘要一致。
- 原子性测试必须在成功事务的多个阶段注入 SQL 失败，证明 Rollback 后 PollTrace 幂等账本、Series、Demand、事件、当前条件、CatalogRevision 和目录均无半提交；重试同一完整轮次只能提交一次。
- SQL Server 并发测试必须证明单飞轮询、同一业务键约束、SeriesSequence、CatalogRevision 单调性和读取快照不会在两个提交间撕裂。
- Catalog 测试必须证明首次完整正文、同 Revision 的 304、成员进入/退出、成员实时值变化、无变化轮、同轮多成员变化只增一次，以及目录绝不接受 Dispatch 范围参数。
- 外部消费者契约测试使用一个最小 reference consumer，证明目录缓存可丢弃、重启后无需 Cursor、最终读取能发现资格/值变化，并且 AcceptedDemandSnapshot 不会被后续目录刷新改写。Dispatch 状态机本身不进入 MesIngest 测试范围。
- ErrorSearch API 测试必须使用可控 TimeProvider 覆盖 UTC 半开边界、24h/7d/30d 滚动窗口、全部历史、ACTIVE/ENDED、条件恢复与 Demand GONE、跨世代证据、分面排除自身维度、固定排序、精确总数、游标篡改与跨筛选复用。
- ReadabilityAudit API 测试必须覆盖多阻断原因、主要原因优先级、原因分面重叠、资格与生命周期正交、AREA 精确范围、不可信 AREA 仅在全部范围、快照绑定、CatalogRevision 不变但审计快照变化，以及详情与列表同一提交。
- Overview API 测试必须在同一提交制造 Series、资格、错误、关注项和动态变化，证明所有摘要共享快照身份；刷新期间下一轮提交不得混入旧快照详情。动态只取 24 小时内五条并稳定排序。
- CurrentIngestAttention 测试必须证明活动 Series 错误只引用稳定错误身份、已结束错误从当前页消失但仍可在错误检索找到，PollRunFailure/TaskTypeProtection/UnassignedMesObservation 可作为非 Series 当前关注显示。
- API 契约测试必须验证契约版本严格匹配、字段语义、UTC/offset、错误响应、认证、默认/最大页大小、精确计数、稳定排序、大小限制、ETag/304 和 OpenAPI 与运行时一致。
- 纯领域单元测试只补主 seam 难以高密度穷举的规则：MesArea 格式、TransportDemandKey 比较、原始行规范化摘要、错误身份键、错误目录演进、资格主要原因优先级、时间区间相交、游标签名/绑定和序列边界。
- Oracle 源测试使用 fake executor 验证一条 SQL、命令超时、列/类型映射、Thin/Thick 配置和密码脱敏；真实 Oracle 11g 只在工厂探针与验证包中验收，CI 不伪造现场通过。
- 发布前 SQL Server 门禁必须在与现场兼容的真实 SQL Server 版本运行全套主要 seam；LocalDB 或内存 store 只能作为开发反馈，不能代替发布证据。
- Watch 客户端 seam 使用既有 ScriptedFakeHost，并通过与生产相同的 HTTP/DTO/会话接口注入概览、Series、审计、错误、AREA 与关注场景；不得为测试增加绕过鉴权、取消、快照或分页规则的页面专用接口。
- Watch 状态测试覆盖 Host 切换、契约不匹配、自动刷新、慢请求、取消、迟到响应、失败保留、陈旧标记、查询变更、快照游标错误、选择重定位、AREA 配置校验和范围外导航确认。
- WPF 非像素测试优先验证页面功能、键盘、焦点、UI Automation Name、标题栏、导航、分页、直接跳页、详情、InfoBar、剪贴板和高对比度语义，不依赖屏幕坐标。
- 所有修改 Watch UI、XAML、Wpf.Ui 控件、布局、UI Automation、DPI 或视觉基线的实现票，必须逐项包含黄金 WPF renderer checklist，并先阅读 Fluent 与黄金渲染规则。
- 视觉验收只能在校准的 `gpt_win11` 交互桌面执行。先跑非像素回归，再生成真实黄金机预览给用户明确批准；之后生成新候选、连续 10 次 PNG/XML 字节一致、记录 before/after/diff，最后提升批准基线并再跑 10 次 `0 received`。
- 125% 和 150% DPI 使用一次性离线 Hyper-V 克隆验证；不得改变校准 VM、使用 RDP/Enhanced Session 或以 PowerShell Direct 截图。验证后清理任务、进程、克隆并复核原 VM 为 96 DPI。
- 安装/升级测试必须证明发布包不携带真实凭据、查询只有一份正式副本、模板完整、Service 与 Watch 可独立启动、Watch 关闭不停止 Host、远程绑定缺少 secret 时拒绝启动或拒绝数据访问。
- 空库切换演练在一次性数据库上验证：停止消费者、备份、确认精确实例、删除旧库、新建新 schema、首轮 bootstrap、整包回退。测试和安装脚本不得对未确认实例执行 DROP。
- 工厂验收分别记录 Oracle Thin 探针、必要时 Thick 复验、多轮完整轮询、SQL 持久化重启、目录 Revision/304、主要读取 API、Watch 六页、关闭 Watch 后 Service 继续，以及脱敏证据哈希；未执行项必须明确为 skip，不能宣称现场签字通过。

## Out of Scope

- DispatchTask 的选择、认领、派车、装卸、车辆/站点/地图/路径、RIoT Order 状态机、人工来源变化复核和取消抑制实现；本规格只定义 MesIngest 向这些消费者提供的事实边界。
- 迁移、转换或伪造旧 TransportDemand、永久 GONE、FrozenMesFieldSet、IngestAlert incident、DemandChangeFeed、PollHealth 或旧 DTO 历史。旧库只作为独立备份用于整包回退。
- 兼容旧 schema、旧 API、旧 OpenAPI、旧 Watch 或旧外部消费者；不提供混合版本运行、双写、影子同步或滚动升级。
- 旧版 `FIELD_DRIFT`、`REAPPEAR_AFTER_GONE`、`DUPLICATE_RECONCILE_KEY` incident 和已恢复告警 365 天保留语义；新版以 LiveMesFieldSet、Demand 世代、SeriesErrorPeriod 和 CurrentIngestAttention 替代。
- DemandChangeFeed、有限保留 ledger、high-watermark bootstrap 和 410 Cursor 过期恢复；新版外部同步只使用完整目录 + CatalogRevision 条件读取。
- 修改客户 Oracle SQL、增加 DDL/索引/视图/CDC、将六个分支拆为独立查询，或以未经授权的 MES 数据库优化掩盖慢查询。
- Watch 中创建、修改、删除 TransportDemand，确认/指派/备注/手工关闭告警，或执行任何生产和调度命令。
- 多 Host 聚合、跨站点集中大盘、Host 自动发现、Web/WinUI/移动端客户端和深色主题重新设计。
- 错误历史导出、全量原始行同步导出、任意日志上传、诊断包和可编辑错误/阻断目录；如现场确认需要，必须另行定义权限、脱敏、快照和容量契约。
- 性能分析专页、图表、PerformanceState 告警和新的遥测产品面；仅保留受控 WatchRefreshTrace 架构边界，不把它作为本规格业务验收前提。
- 用 AreaFilterProfile 改变外部可读资格、CatalogRevision、Dispatch AREA 白名单或 AREA→站点映射；它只影响 Watch 显示查询。
- 将资格审计扩展为历史回放或 Dispatch 可派审计；第一版只解释一个冻结投影提交中的每个 Demand 世代当前资格。
- 为第一版 Error Search 增加 AREA 隐式范围、任意列排序或严重度筛选；五个首版错误码严重度均为 ERROR，DTO 保留该属性即可。
- 自动删除现场旧数据库；数据库删除始终是停机、备份、确认精确目标后的人工部署操作。

## Further Notes

- 本规格使用 `CONTEXT.md` 的最新统一领域语言；实现和票据不得退回 `DemandSeriesIssue`、冻结字段、告警 incident、Feed Sequence 等已明确避免的旧词。
- 适用决策为 ADR-mes-0006 至 ADR-mes-0017。其中 ADR-mes-0017 对旧版升级/兼容语义具有最终约束：新版整体替换旧数据库和契约；ADR-mes-0008/0009 中针对旧模型的 GONE 读取与 DemandChangeFeed 方案不构成新版兼容要求。
- 已选 Fluent 原型只确定信息架构和视觉层级，不是生产实现。AREA、错误检索和概览的用户选择分别为 Variant A；任何生产视觉变化仍需新的黄金机预览批准。
- 规格已按用户确认的最高测试 seam 编写。后续拆票应优先形成贯穿 Round → Host → SQL Server → API 的 tracer bullet，再扩展各领域能力和 Watch 页面，避免先建立多套低层 seam。
- 当前工作树包含用户的未提交代码、ADR、领域文档、原型和测试改动。本规格作为新的 tracker 条目独立发布，不修改、覆盖或声明这些在途改动已完成。

