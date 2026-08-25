# MesIngest 有界存储与低内存运行规格书

Status: ready-for-agent

Seams (confirmed): 以“脚本化 MesTaskUnionRound → 生产 Host/领域逻辑 → 真实 SQL Server → 唯一 V2 HTTP 契约 → reference consumer / Watch 查询客户端”为主要端到端验收 seam；以可控时间与脚本化轮次验证轮询、退避、刷新和保留边界；以隔离的旧库/新库与一次性 MesIngestCutoverRun 验证切换及拒删安全；以生产规模数据和并发轮询/读取负载验证容量、内存和查询门禁。Watch 呈现沿用 ScriptedFakeHost → 生产 MesIngestWatch seam，只有实际 UI 改动才按仓库规则另行进入获批的 Tier 2。

## Problem Statement

MesIngest 当前把每轮完整 MES 快照的原始观测和结构化历史持续写入本地 SQL Server，却没有完整的在线历史淘汰边界。现场实测 DemandRawObservation 约每 14 秒增加约 600 行、约 3.5 GB/天，主要对象已约 4.49 GB；同时当前态 Browse 路径仍可能对全部 DemandRawObservation 排名或扫描，使常用读取成本随历史线性增长。结果不是单纯的进程内存泄漏，而是无界数据增长、无界热查询、过密轮询和过密刷新共同放大 SQL Server 内存、磁盘、查询授予、spill 与超时风险。

把 SQL Server max server memory 压到 800 MB 已实证导致 Error 701、17300/17312 和 Host 连接失败，因此不能用不可运行的内存上限掩盖数据与查询问题。现场又明确选择 SIMPLE 恢复模式且不做数据库备份，意味着必须把详细历史保留、事务日志、磁盘压力、数据库丢失后的身份风险和计划切换的不可恢复删除都变成显式契约。

用户需要 MesIngest 在约 2 GB 进程级运行包络和有限磁盘中持续工作，同时保持完整 MES 快照的缺席权威、当前 ExternallyReadableDemandCatalog 的安全含义、活跃 DemandSeries 的完整结构化证据、冻结读取的一致性以及归档业务键永不重新外读的结论。系统还必须在一次 30–60 分钟停机窗口内以空库和精确新契约整体切换，并在全部机械门禁通过后由一次性程序自动删除精确旧库，而不是让日常 Host 永久持有删库权限。

## Solution

将 MesIngest 改为具有明确资源、调度、读取、保留、恢复和切换边界的单一 V2 系统。生产 SQL Server 常态 max server memory 默认 1536 MB，sqlservr 稳态目标约不超过 2 GB；只有受控维护期才允许临时提升到 2048 MB，800 MB 被明确列为禁止配置。Host 采用固定 60 秒 start-to-start、单飞且不补跑的 MES 轮询；连续失败按 60、120、300 秒退避。Watch 只刷新当前可见页，当前健康页使用 30 秒档，历史/审计页使用 60 秒档，Inspector 不拥有独立 Timer 或 API 会话。

当前态与历史态使用分离的物理读取路径。常用当前读取只依赖当前物化投影、当前条件和维护好的计数，禁止扫描或排名 DemandRawObservation 历史；历史详情和冻结 snapshot 按对象或页有界读取。所有冻结响应绑定同一 HistoryEpoch 与 ProjectionCommit，并来自不阻塞投影写入的提交一致视图。

DemandRawObservation 自所属 PollTrace 完成起保留精确 15×24 小时。当前物化状态和活跃 DemandSeries 的结构化世代、事件、错误链不按年龄拆散；DemandSeries 首次满足 RetentionEligibleDemandSeries 后再保留 15×24 小时，并以完整历史图为单位清理。清理 Series 时，在同一事务内先幂等写入永久 ArchivedDemandKeyTombstone，再删除详细历史；归档键以后重现仍属于 LONG_GONE_BUT_VISIBLE，且永不进入 ExternallyReadableDemandCatalog。Host 每小时以有行数和时间预算的小事务推进幂等清理，失败可续且不得阻塞轮询。

数据库存储剩余低于 15% 时产生严重告警；低于 10% 时，Host 必须在下一次 MES 查询之前进入 StoragePressurePause，保留最后成功投影但不取得新快照、不推进缺席判定。恢复只能由数据库主机上的授权运维人员通过 MesIngestLocalAdministration 明确提交。非计划丢库或不可恢复重建创建新的 HistoryEpoch，并使 ExternallyReadableDemandCatalog 与执行承诺读取返回 503 INGEST_NOT_CURRENT，直到提交 HistoryResetAcknowledgement。

新库使用 SIMPLE 恢复模式，不创建完整、差异或事务日志备份。DemandRawObservation 主要聚集和非聚集索引默认使用 PAGE 压缩；热字段、筛选列和临时结构采用基于真实数据门禁的有界类型，原始证据保持无损，超界值形成显式异常而不是截断。只有 15 天容量或热路径门禁仍失败时，才重新评估 ObservationPayload、ObservationSet 或 Span 内容寻址模型。

切换时同时提升精确 contractVersion 与 schemaVersion，继续只发布唯一 /api/v2。先在独立空库和整包 Host、Watch、reference consumer 上完成新 schema、带安全余量的快速容量预测和加速并发稳定性门禁，再在一次停机窗口中停止旧 Host、建立新 HistoryEpoch、从旧库只播种 ArchivedDemandKeyTombstone、验证新库并运行连续三轮成功投影。完整 15 天物化或长时间 soak 只在快速门禁出现风险信号，或用户为正式现场切换明确要求时升级执行；长跑固定为 4 小时或 24 小时，并从原始分钟级资源时间线与逐 API 末段 phase 复算实际覆盖，不能信任单一汇总时长。唯一 CutoverRunId 标识的一次性 MesIngestCutoverRun 使用临时提升权限；只有墓碑、版本、投影、主要 Watch API、外部目录和精确旧库身份等同窗门禁全部通过，才自动删除显式旧库。失败必须禁止删除、退出且不后台重试，删除证据写到数据库外和 Windows 事件日志。

## User Stories

1. 作为现场运维工程师，我希望 SQL Server 常态 max server memory 默认为 1536 MB，以便在已知可运行的内存范围内服务 MesIngest。
2. 作为现场运维工程师，我希望 sqlservr 稳态进程目标约不超过 2 GB，以便为 Host、Watch 和操作系统保留可用内存。
3. 作为维护人员，我希望只有受控维护窗口才允许把 max server memory 临时提高到 2048 MB，以便执行压缩、索引或切换维护而不永久扩大常态预算。
4. 作为维护人员，我希望维护结束后自动或按明确步骤恢复 1536 MB 常态配置，以便临时调整不会遗留为生产默认。
5. 作为部署工程师，我希望 800 MB 被配置校验和运行手册明确拒绝，以便不重复触发已经实证的 Error 701 与连接故障。
6. 作为运维工程师，我希望能够观测 SQL Server 已提交内存、workspace memory、grant 等待和 spill，以便判断资源门禁是否真实满足。
7. 作为 MES 数据管理员，我希望 Host 继续读取客户批准的完整 MES_TASK_UNION 快照，以便缺席判断仍有完整集合权威。
8. 作为系统，我希望 MES 轮询以固定 60 秒 start-to-start 调度，以便写入率和接入节奏可预测。
9. 作为系统，我希望任何时刻最多运行一轮 MES 查询与投影，以便慢轮次不会产生并发重叠和提交竞争。
10. 作为系统，我希望错过的轮询槽位不补跑，以便慢轮次结束后不会用突发追赶放大数据库压力。
11. 作为系统，我希望一轮执行超过计划间隔时只在该轮完成后进入下一个可用调度点，以便仍保持单飞语义。
12. 作为运维工程师，我希望连续失败按 60、120、300 秒退避且上限保持 300 秒，以便故障期间降低对 MES 和 SQL Server 的压力。
13. 作为运维工程师，我希望成功轮次恢复正常 60 秒节奏，以便暂时故障不会永久降低数据新鲜度。
14. 作为运维工程师，我希望轮询失败、退避级别、下一次允许启动时间和最后成功轮次可观测，以便准确解释接入空窗。
15. 作为系统，我希望轮询、退避和取消都使用可控时间 seam 验证，以便边界测试不依赖真实等待。
16. 作为 Watch 用户，我希望只有当前可见页运行自动刷新，以便后台页面不制造无价值查询。
17. 作为 Watch 用户，我希望概览和当前接入关注页默认使用 30 秒刷新档，以便常用健康状态及时更新。
18. 作为 Watch 用户，我希望需求系列、资格审计和错误检索页默认使用 60 秒刷新档，以便较重的冻结查询保持有界。
19. 作为 Watch 用户，我希望每次自动刷新只重取当前页而不下载全部结果，以便 UI 与 Host 成本不随历史增长。
20. 作为 Watch 用户，我希望切换页面时旧页计时器停止且目标页按其自身档位工作，以便页面状态互不干扰。
21. 作为 Watch 用户，我希望 Inspector 只消费主页面已经取得的冻结 presentation，不拥有独立 Timer、Host client、缓存或 snapshot，以便同一调查不会产生第二套读取节奏。
22. 作为 Watch 用户，我希望刷新失败或取消继续保留最后成功窗口并明确显示其时间，以便空白界面不会伪装成没有数据。
23. 作为运维工程师，我希望当前态读取只依赖当前物化投影、当前条件和维护好的计数，以便常用查询不扫描详细历史。
24. 作为运维工程师，我希望任何当前态 SQL 都禁止对 DemandRawObservation 全历史执行排名、排序或无界扫描，以便逻辑读不随 15 天历史线性增长。
25. 作为 Watch 用户，我希望概览从专用当前聚合或同一 ProjectionCommit 的缓存读取，以便概览不通过完整历史 Browse 间接计算。
26. 作为 Watch 用户，我希望当前 DemandSeries、CurrentIngestAttention、ReadabilityAudit 和目录读取拥有稳定的服务端筛选与有界分页，以便客户端不下载全表。
27. 作为审计人员，我希望历史详情按对象边界读取，以便查看一条 Series 或 PollTrace 不必扫描无关历史。
28. 作为审计人员，我希望历史列表按冻结 snapshot、稳定排序和有界页读取，以便翻页成本和结果身份可解释。
29. 作为 API 消费者，我希望当前态和历史态共享相同领域含义但使用不同物理查询计划，以便性能优化不改变业务结论。
30. 作为运维工程师，我希望当前热查询在空库和代表性历史样本下具有近似稳定的逻辑读，并以保守模型外推更大规模，以便快速证明查询已与历史容量解耦。
31. 作为运维工程师，我希望执行计划和实际 IO 证据证明历史回退分支只在需要时触发，以便不能仅凭 SQL 文本宣称热查询已优化。
32. 作为系统，我希望所有查询临时结构按真实字段长度和行数有界，以便内存授予不会因无界类型被放大。
33. 作为系统，我希望热路径不得以客户端本地筛选、当前页计数或本地排序替代服务端语义，以便结果和性能都可证明。
34. 作为 Watch 用户，我希望一个冻结响应中的列表、分面、计数和详情都解释同一 ProjectionCommit，以便并发轮询期间不会混入新旧事实。
35. 作为 Watch 用户，我希望每个冻结响应明确携带 HistoryEpoch，以便旧纪元 snapshot 或 cursor 不能挂到新纪元。
36. 作为系统，我希望冻结读取不阻塞投影写入，以便 Watch 调查不会延迟固定轮询。
37. 作为系统，我希望冻结读取来自提交一致视图，而不是在普通 ReadCommitted 下拼接多语句结果，以便一致性不是时间上的巧合。
38. 作为数据库维护人员，我希望若选择 Snapshot Isolation，就把 tempdb 版本存储纳入 2 GB 内存与数据库容量实测，以便一致性机制不会转移资源风险。
39. 作为系统，我希望长 Serializable 事务不是默认实现，以便读取不会用阻塞换取一致性。
40. 作为 API 消费者，我希望跨 HistoryEpoch、ProjectionCommit、筛选或契约复用的 snapshot/cursor 被明确拒绝，以便身份不能被静默重新解释。
41. 作为审计人员，我希望 DemandRawObservation 自所属 PollTrace CompletedAt 起完整保留 15×24 小时，以便近期原始证据有精确 Host UTC 边界。
42. 作为审计人员，我希望 RawObservationAvailabilityWindow 不使用 MES DATES、自然月或本地午夜，以便保留判断不受源业务时间和时区影响。
43. 作为审计人员，我希望保留窗口内的原始行按原样完整返回，以便重复、空值和非法值不会被任选、补值或截断。
44. 作为 Watch 用户，我希望已过期的 PollTrace、冻结 snapshot 或历史对象返回 410 MES_INGEST_HISTORY_EXPIRED，以便过期不被误解为不存在或空集合。
45. 作为 Watch 用户，我希望 410 响应公布当前最早可用 Host UTC 历史边界，以便能够调整查询范围。
46. 作为系统，我希望当前物化状态不因年龄被清理，以便当前目录和运维视图始终可解释。
47. 作为审计人员，我希望活跃 DemandSeries 的结构化世代、事件、错误链和当前条件不按年龄拆散，以便活跃生命周期保持完整。
48. 作为系统，我希望只有已归档、当前 Demand 不为 VISIBLE 或 LONG_GONE_BUT_VISIBLE 且无活动条件或错误期间的 Series 才成为 RetentionEligibleDemandSeries，以便清理资格符合领域语义。
49. 作为系统，我希望 RetentionEligibleDemandSeries 自首次满足资格的 Host UTC 时点再保留 15×24 小时，以便详细历史不会在归档瞬间消失。
50. 作为系统，我希望任何新观测、条件或事件都取消 Series 的清理倒计时，以便重新活跃的历史图不会被误删。
51. 作为系统，我希望可清理 Series 以完整详细历史图为单位删除，以便不会留下残缺世代、事件或错误链。
52. 作为系统，我希望清理 Series 时在同一事务中先幂等写入 ArchivedDemandKeyTombstone 再删除详细历史，以便任何失败都不会遗忘归档身份。
53. 作为系统，我希望墓碑写入或详细删除任一步失败时整笔事务回滚，以便不存在安全空窗。
54. 作为外部消费者，我希望墓碑对应的 TransportDemandKey 后来重现仍为 LONG_GONE_BUT_VISIBLE 且永不进入 ExternallyReadableDemandCatalog，以便旧归档业务键不能重新外读。
55. 作为数据最小化负责人，我希望 ArchivedDemandKeyTombstone 只保存判断键身份、原 Series 与归档结论所需的最小事实，以便永久记录不变成另一份详细历史。
56. 作为运维工程师，我希望 Host 单实例后台流程每小时检查并推进历史清理，以便保留边界持续执行且不依赖 SQL Server Agent。
57. 作为运维工程师，我希望清理以可配置行数和时间预算的小事务运行，以便轮询优先且单批不会长期持锁。
58. 作为运维工程师，我希望清理幂等、可中断、失败可续，并暴露进度与最后错误，以便重启或故障后安全恢复。
59. 作为运维工程师，我希望清理失败形成 Current Attention，但只有存储达到门槛才进入 StoragePressurePause，以便普通维护故障不被误报为接入暂停。
60. 作为运维工程师，我希望 SQLSERVERAGENT 和外部计划任务不拥有业务历史清理，以便保留、墓碑和 schema 契约随 Host 一起发布。
61. 作为运维工程师，我希望数据库所在卷剩余空间低于 15% 时出现严重告警，以便在接入暂停前有明确处置窗口。
62. 作为系统，我希望剩余空间低于 10% 时在下一轮 MES 查询之前进入 StoragePressurePause，以便不会取得无法可靠持久化的新快照。
63. 作为 Watch 用户，我希望 StoragePressurePause 期间仍能读取最后成功投影、诊断和可用历史，以便能够调查并恢复环境。
64. 作为外部消费者，我希望 StoragePressurePause 期间当前目录和执行承诺读取返回 503 INGEST_NOT_CURRENT，以便陈旧事实不会被当作当前事实。
65. 作为系统，我希望暂停期间不查询 MES、不推进缺席判定、不伪造 GONE，以便接入空窗被诚实表达。
66. 作为运维工程师，我希望空间回升不会自动恢复轮询，以便数据库健康与空间恢复经过人工确认。
67. 作为授权运维人员，我希望只能通过 MesIngestLocalAdministration 恢复 StoragePressurePause，以便高风险状态变更有明确本地权限边界。
68. 作为 Watch 用户，我希望 Watch 只显示暂停原因、最后成功时间、最早可用历史和精确本地恢复指引，不提供恢复按钮，以便保持业务只读边界。
69. 作为数据库管理员，我希望新库固定使用 SIMPLE 恢复模式，以便事务日志能够在无备份策略下正常重用。
70. 作为数据库管理员，我希望系统不创建完整、差异或事务日志备份，以便符合已选择的最低磁盘维护策略。
71. 作为运维工程师，我希望监控 LDF 实际大小、增长和 log reuse wait，以便 SIMPLE 模式不能掩盖日志异常。
72. 作为运维工程师，我希望非计划数据库丢失后建立空库和新的 HistoryEpoch，以便系统不把身份丢失伪装成普通重启。
73. 作为外部消费者，我希望非计划重建后持续收到 503 INGEST_NOT_CURRENT，直到 HistoryResetAcknowledgement 已提交，以便旧墓碑丢失风险被人工接受。
74. 作为授权运维人员，我希望 HistoryResetAcknowledgement 记录执行身份、目标 HistoryEpoch、前后状态、时间和风险接受，以便恢复动作可审计。
75. 作为 Watch 用户，我希望确认前仍可查看新纪元建立进度、HistoryEpoch、最早历史和恢复指引，以便故障恢复可被观察。
76. 作为系统，我希望 RestartBarrier、成功轮次或磁盘恢复都不能代替 HistoryResetAcknowledgement，以便不同安全状态不会混用。
77. 作为系统，我希望计划切换和非计划重建都创建新 HistoryEpoch，但只有非计划身份丢失要求风险确认，以便两种路径的安全依据清晰。
78. 作为安全负责人，我希望 HistoryResetAcknowledgement 和 StoragePressurePause 恢复不暴露为远程 Watch 写 API，以便不扩大攻击面。
79. 作为安全负责人，我希望直接修改 SQL 表不构成合法确认或恢复，以便审计边界不能被绕过。
80. 作为数据库管理员，我希望 DemandRawObservation 主要聚集和非聚集索引在正式 schema 中默认使用 PAGE 压缩，以便降低已实证的主要增长来源。
81. 作为数据库管理员，我希望空库建表、schema 校验和代表性压缩样本都证明 PAGE 压缩存在，以便压缩不是部署后的手工漂移。
82. 作为审计人员，我希望原始证据字段保持无损，以便容量优化不会通过截断改变证据。
83. 作为系统，我希望超出已验证字段边界的源值形成显式异常并停止不安全解释，以便有界类型不会静默损坏数据。
84. 作为性能工程师，我希望热字段、筛选列、索引键和临时表宽度由真实数据分布与上限门禁决定，以便内存授予保持可控。
85. 作为架构师，我希望 ObservationPayload、ObservationSet 和 Span 暂不成为首版依赖，以便先用读取分离、保留和压缩解决已知问题。
86. 作为架构师，我希望只有 15 天容量或热查询门禁失败时才重新打开内容寻址方案，以便复杂度由证据驱动。
87. 作为 API 消费者，我希望此次行为改变同时提升精确 contractVersion 与 schemaVersion，以便旧语义不能沿用相同身份。
88. 作为 API 消费者，我希望系统继续只发布唯一 /api/v2 和 /openapi/v2.json，以便不长期维护 V2/V3 双路由。
89. 作为部署工程师，我希望 Host、Watch 和 reference consumer 作为一个精确契约包共同切换，以便不出现混合版本业务解释。
90. 作为部署工程师，我希望切换前在独立空库上完成新 schema、压缩、保留、查询和整包兼容验证，以便不在旧生产库原地试错。
91. 作为部署工程师，我希望代表性样本以 30% 安全余量外推后满足 15 天最终容量硬上限；70% 与增长非线性只形成 advisory warning，而触及硬上限或关键证据不确定时 fail closed，以便日常门禁快速且风险接受可审计。
92. 作为部署工程师，我希望现场切换被限制在一次 30–60 分钟计划停机窗口，以便停止、验证和删除属于同一可审计运行。
93. 作为系统，我希望新库除 ArchivedDemandKeyTombstone 外不迁移旧当前态或详细历史，以便不制造无法证明的新领域事实。
94. 作为安全负责人，我希望墓碑播种以数量和稳定哈希证明旧库全部已归档键已进入新库，以便旧键安全结论不会遗漏。
95. 作为部署工程师，我希望一次性 MesIngestCutoverRun 由唯一 CutoverRunId 标识，以便所有门禁和删除证据属于同一运行。
96. 作为安全负责人，我希望日常 Host 账号永远没有删库权限，以便运行缺陷不能扩大为不可恢复删除。
97. 作为安全负责人，我希望 MesIngestCutoverRun 只在执行期间获得临时提升权限并在结束后撤销，以便实例级权限不长期存在。
98. 作为安全负责人，我希望旧库删除目标必须是显式名称、非系统库、非新库并匹配预期 schema、contract 和解析后的 SQL 数据目录，以便程序不能猜测或通配删除。
99. 作为安全负责人，我希望删除前证明旧 Host 已停止且旧库没有业务连接，以便不会删除仍在服务的数据库。
100. 作为部署工程师，我希望删除前连续三轮 MES 投影成功且主要 Watch API、外部目录和新契约身份全部通过，以便启动成功不会被误当作切换成功。
101. 作为部署工程师，我希望任一同窗门禁失败时禁止删除、保留新旧库、退出且不后台重试，以便失败状态可供检查并需要新的明确运行。
102. 作为审计人员，我希望删除前在数据库外生成不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志，以便数据库删除后仍有门禁和身份记录。
103. 作为数据保护负责人，我希望切换证据不包含 DemandRawObservation 或其它业务原文，以便证据文件不是数据库备份或敏感数据副本。
104. 作为部署工程师，我希望旧库删除后只允许在新库和新契约上向前修复，以便不可用的回滚路径不会出现在操作流程中。
105. 作为运维工程师，我希望常用 Watch API 在代表性压缩负载下 P95 小于 2 秒、P99 小于 5 秒，以便现场调查保持可用。
106. 作为运维工程师，我希望负载期间没有 Error 701、持续 RESOURCE_SEMAPHORE 或不可接受 spill，以便低内存目标不是以不稳定换来的。
107. 作为运维工程师，我希望通过 30–45 分钟高强度并发压力和加速的 24 小时逻辑周期证明锁、版本存储、清理和调度能共同工作，并在资源趋势异常时升级长时间 soak。
108. 作为容量负责人，我希望 15 天逻辑已用空间不超过 12 GB、物理数据库文件不超过 16 GB、LDF 目标不超过 2 GB，以便部署适配现场磁盘预算。
109. 作为容量负责人，我希望代表性样本的增长以 30% 安全余量外推后不超过 15 天门槛，以便快速阻断明显失败。
110. 作为运维工程师，我希望容量报告分别展示表、索引、PAGE 压缩、墓碑、版本存储和日志占用，以便总量变化可以定位。
111. 作为开发者，我希望真实 SQL Server Tier 1 运行显示 Failed: 0、Skipped: 0，以便 SQL 行为没有被 82 个静默跳过的集成测试遗漏。
112. 作为维护者，我希望所有验收证据记录配置、schema/contract、HistoryEpoch、数据规模、并发模型和 skip 数，以便结果可重复且不能脱离运行上下文。

## Implementation Decisions

- 本规格是对既有 NewMesIngestContract 的资源与有界历史扩展；领域身份、完整 MesTaskUnionRound、DemandSeries、ExternallyReadableDemandCatalog、CurrentIngestAttention 和 Watch 业务只读边界继续有效。
- ADR-mes-0020 至 ADR-mes-0030 是本规格的设计权威。本规格补充可验收行为、默认配置、切换步骤和门禁，不复制或重新解释 ADR 全文。
- SQL Server 常态 max server memory 默认 1536 MB，sqlservr 稳态目标约不超过 2 GB。受控维护期上限为 2048 MB，结束后恢复常态；800 MB 是已知不可运行配置，必须拒绝。
- Host 轮询改为固定 60 秒 start-to-start 单飞调度。慢轮次不重叠、不补跑；连续失败使用 60、120、300 秒退避，上限 300 秒，成功后恢复正常节奏。
- Watch 自动刷新继续沿用按视图隔离、单飞、不排队、最后成功窗口原子替换的状态机，但默认档位改为：Overview 与 CurrentIngestAttention 30 秒，DemandSeries、ReadabilityAudit 与 ErrorSearch 60 秒。只有当前可见页运行，且只重取当前页。
- Inspector 继续沿用既有 modeless 单窗口协调边界，不拥有 Host client、Timer、refresh loop、独立缓存或 snapshot；主页面刷新后通过协调器推送同一冻结上下文的不可变 presentation。
- 读取模块在物理上分成 Current Read Model 与 Historical/Frozen Read Model。当前路径只能访问当前物化投影、当前条件、维护计数和专用概览聚合；不得扫描或排名 DemandRawObservation 历史。
- 历史路径必须按单对象或稳定页有界。服务端负责筛选、精确计数、稳定排序、keyset cursor 和历史边界；Watch 不下载全表或以当前页推导总数。
- 冻结列表、分面、计数、详情和原始证据读取必须绑定同一 HistoryEpoch 与 ProjectionCommit。实现可以在短事务版本化读取与不可变快照读模型之间选择，但必须通过真实 tempdb、执行计划和并发门禁；长 Serializable 不是默认方案。
- DemandRawObservation 的 RawObservationAvailabilityWindow 是从所属 PollTrace CompletedAt 起精确 15×24 小时。普通成功/失败 PollTrace 使用 Host CompletedAt；关闭错误使用 EndedAt；RetentionEligibleDemandSeriesWindow 同样从首次满足资格的 Host UTC 时点起精确 15×24 小时。均不使用 MES DATES、自然月或本地午夜。
- 当前物化状态和活跃 DemandSeries 的结构化图不按年龄拆散。RetentionEligibleDemandSeries 的任何新观测、条件或事件都会取消清理计时；再次满足资格时重新建立资格时点。
- 历史过期使用 410 MES_INGEST_HISTORY_EXPIRED，并返回最早可用 Host UTC 边界。只有从未存在的当前身份才使用既有未找到语义；不得用 404、200 空集合或残缺对象表示已知过期历史。
- ArchivedDemandKeyTombstone 是唯一允许永久保留的已清理 MesIngest 业务记录，只保存 TransportDemandKey、原 Series 身份、归档结论和安全判断所需的最小版本化事实。
- 清理单个 Series 的原子边界固定为：同一事务内幂等写墓碑，再删除该 Series 完整详细历史图，再提交。批次预算不得拆开这个边界。
- Host 以单实例后台清理器每小时运行。批次行数、单次时间预算和检查间隔是运维配置，不改变 15 天领域语义；默认值由容量基线票据在真实 SQL Server 上选择并冻结。
- 清理器必须幂等、可取消、失败可续且轮询优先。清理失败进入 Current Attention；只有卷空间达到阈值时才触发 StoragePressurePause。
- 存储监控针对数据库实际数据卷。低于 15% 产生严重告警；低于 10% 在查询 MES 之前进入 StoragePressurePause。暂停不取得新快照、不推进缺席、GONE 或归档判断。
- StoragePressurePause 期间 Watch 诊断与历史读取继续服务，ExternallyReadableDemandCatalog 与执行承诺读取返回 503 INGEST_NOT_CURRENT。空间回升不自动恢复，恢复只由 MesIngestLocalAdministration 提交。
- MesIngestLocalAdministration 是数据库主机上的本地 CLI/PowerShell 管理边界。HistoryResetAcknowledgement 和 StoragePressurePause 恢复都记录执行身份、目标 HistoryEpoch、前后状态、原因和 Host UTC 时间；Watch 不提供写按钮或远程管理 API。
- 新库固定 SIMPLE 恢复且无数据库备份。系统仍监控 LDF 大小、增长与 log reuse wait；禁止 FULL 恢复但不做日志备份的组合。
- 计划空库切换与不可恢复重建都创建新 HistoryEpoch。非计划重建因墓碑身份丢失必须保持外部当前读取 503，直到明确的 HistoryResetAcknowledgement；该确认不声称恢复旧墓碑。
- 所有 snapshot、cursor、目录条件身份和 API 响应都携带或绑定 HistoryEpoch。旧纪元缓存、cursor 和 snapshot 不能跨纪元复用。
- DemandRawObservation 主要聚集与非聚集索引在正式 schema 中默认 PAGE 压缩；空库 bootstrap、schema validation 和发布门禁都校验该属性。
- 当前投影字段、筛选列、索引键和临时结构使用经真实数据验证的有界类型。DemandRawObservation 原始证据保持无损；超界输入形成可诊断异常，不截断、不回填、不任选。
- 首版不建设 ObservationPayload、ObservationSet 或 Span 内容寻址层。只有 15 天容量或当前态逻辑读门禁失败，才以新的证据和 ADR 重新开启该设计。
- 同时提升 NewMesIngestContract 的精确 contractVersion 与 schemaVersion，并更新完整 capability ID/version 集合与 OpenAPI。继续只发布唯一 /api/v2 和 /openapi/v2.json，不提供长期并行 V3。
- Host、Watch 与 reference consumer 必须以精确版本整包切换。任何 contract、schema 或 capability 身份不一致都在业务读取前失败，不能做缺字段或旧 DTO 降级。
- 新库不迁移旧当前投影、PollTrace、DemandRawObservation、DemandSeries、事件或错误历史；计划切换只从旧库播种已归档 TransportDemandKey 的 ArchivedDemandKeyTombstone。
- 切换顺序固定为：只读重建旧环境反馈环；在独立空库验证新包、快速容量预测和加速并发稳定性；按风险信号或用户明确要求升级完整规模/长时间验证；计划 30–60 分钟停机；停止旧 Host；创建新库与 HistoryEpoch；播种并证明墓碑；启动精确新包；连续完成三轮成功投影；验证 contract/schema、主要 Watch API、ExternallyReadableDemandCatalog 和 reference consumer；验证精确旧库身份；生成外部证据；自动删除旧库；撤销临时权限并结束运行。
- MesIngestCutoverRun 必须由唯一 CutoverRunId 标识，且全部门禁、证据与删除属于同一运行。日常 Host 不包含、调用或持有删库能力。
- 删除目标必须同时满足：显式旧库名；不是系统库或新库；匹配预期旧 schema/contract；数据文件位于解析后的预期 SQL 数据目录；旧 Host 已停止且没有业务连接；墓碑数量与稳定哈希一致；所有门禁属于当前 CutoverRunId。禁止通配、前缀和自动猜测。
- 任一切换门禁失败都禁止删除、保留新旧库、以失败退出且不后台重试。删除失败同样保留可检查状态；再次尝试必须由操作员发起新的明确 MesIngestCutoverRun。
- 删除前在数据库外写不可覆盖的 JSON/Markdown 证据并写 Windows 事件日志，记录实例、旧/新库身份、HistoryEpoch、版本、墓碑证明、三轮投影、接口检查、执行账号和时间。证据不得包含业务原文，也不构成备份。
- 旧库删除后没有历史或版本回滚路径，后续故障只在新库与新契约上向前修复。
- 运行遥测至少覆盖：SQL Server 配置与进程内存、workspace/grant、Error 701、RESOURCE_SEMAPHORE、spill、当前态逻辑读、查询延迟、轮询节奏与退避、清理进度与失败、最早可用历史、HistoryEpoch、StoragePressurePause、数据库逻辑已用空间、MDF/NDF/LDF 物理大小、压缩状态与 log reuse wait。
- 默认发布门禁固定为：代表性压缩负载下常用 Watch API P95 < 2 秒、P99 < 5 秒；没有 Error 701、持续 RESOURCE_SEMAPHORE 或不可接受 spill；当前态逻辑读不随代表性历史规模增长；30–45 分钟高强度并发压力和加速 24 小时逻辑周期稳定；带 30% 安全余量的 15 天预测必须低于逻辑已用空间 12,288 MB、物理数据库文件 16,384 MB、LDF 2,048 MB 三项最终硬上限。预测达到或超过任一最终硬上限、证据缺失、样本超过 250,000 条、PAGE 压缩不确定或清理完整性不确定时 fail closed；达到 70% 或增长呈非线性只记录 advisory warning，不再阻断发布或强制升级。该容量政策由用户于 2026-08-25 明确接受风险后覆盖原门禁；用户仍可在正式现场切换前明确要求升级。
- 2026-08-22 的 Host、SQL Server 和已部署程序集状态只是旧诊断事实。实施第一张票必须先用只读检查重新确认当前服务、进程、版本、端点、数据库、配置和错误反馈环，不能把交接观察当作现状。

## Testing Decisions

- 好测试只观察外部行为和持久化契约：给定轮次、时间、存储状态、数据库身份和 API 请求，断言提交结果、HTTP 状态、公开 DTO、可见 SQL 状态、资源证据和不可恢复动作是否发生。不得以私有方法调用、SQL 文本片段或内部类结构代替行为证明。
- 主要端到端 seam 使用脚本化 MesTaskUnionRound 驱动生产 Host 与领域逻辑，写入真实 SQL Server，再通过唯一 V2 HTTP API 由 reference consumer 和 Watch 查询层读取。此 seam 负责覆盖当前/历史分离、HistoryEpoch、410/503、墓碑、目录安全和提交一致性。
- 调度 seam 使用可控 TimeProvider、可阻塞/失败的轮次源和生产轮询协调器，证明固定 60 秒 start-to-start、单飞、超时轮次不重叠、不补跑、60/120/300 秒退避、成功复位和取消停止。
- Watch seam 使用 ScriptedFakeHost 与生产 Watch workspace/refresh coordinator，证明仅当前页计时、30/60 秒默认映射、单飞、不排队、失败保留最后成功窗口，以及 Inspector 没有独立查询或 Timer。
- 历史保留测试在精确边界前一 tick、边界时刻和边界后一 tick 验证 RawObservationAvailabilityWindow 与 RetentionEligibleDemandSeries 计时；同时覆盖新观测/条件/事件取消资格，以及使用 Host UTC 而非 MES DATES。
- 墓碑原子性测试必须在墓碑写入、详细历史删除和事务提交之间注入失败，证明任一失败均回滚；重试后只有一个墓碑且完整图恰好清理一次。
- LONG_GONE_BUT_VISIBLE 测试必须跨清理、Host 重启和后来同键重现，证明旧 Series 身份仍可判定、Watch 可见、目录永不外读。
- 历史过期测试必须区分“从未存在”与“曾存在但已过期”，验证 410 MES_INGEST_HISTORY_EXPIRED、最早可用边界以及 404/空集合不会替代过期语义。
- 冻结读取并发测试在列表、分面、计数和详情之间提交新轮次，证明旧响应完全属于旧 ProjectionCommit、新响应完全属于新提交，且写入不被读取阻塞。若使用 Snapshot Isolation，还要采集 tempdb 版本存储。
- 当前态查询测试在相同当前投影、空库与代表性历史样本下采集实际执行计划、STATISTICS IO/TIME 和 spill，证明 DemandRawObservation 历史逻辑读为零或有严格对象级上限，并以保守模型外推更大规模。
- 清理调度测试证明每小时检查、小事务预算、取消、失败可续、轮询优先与 Current Attention；不以 SQL Server Agent 或外部计划任务触发业务删除。
- StoragePressurePause 测试使用可控卷空间 seam，分别覆盖 15% 边界、10% 边界、查询前暂停、暂停期间不调用 MES、不推进缺席、诊断可读、外部当前读取 503、空间回升不自动恢复和本地管理恢复审计。
- HistoryEpoch 测试覆盖计划切换、非计划丢库、普通 Host 重启三类路径，证明只有前两者产生新纪元，只有非计划身份丢失要求 HistoryResetAcknowledgement，且旧 snapshot/cursor/cache 全部被拒绝。
- 本地管理测试从授权/未授权身份运行，证明目标 HistoryEpoch、状态前置条件、审计内容与幂等行为正确，且 Watch/API/直接 SQL 修改不能冒充合法操作。
- Schema 测试在空数据库 bootstrap 后验证 SIMPLE 恢复、精确 schemaVersion、有界字段、所有要求的 PAGE 压缩索引和墓碑结构；在已有错误 schema、错误压缩或超界数据时必须失败且不静默修补。
- 压缩与容量默认测试使用生产分布的代表性样本，实测每轮、每行、表、聚集索引、非聚集索引、墓碑、版本存储和 LDF 增量，以 30% 安全余量外推 15 天。预测达到或超过逻辑 12,288 MB、物理 16,384 MB 或 LDF 2,048 MB，或样本、PAGE 压缩、清理完整性证据不确定时 fail closed；70% 与增长非线性必须保留为 advisory warning，但不强制物化完整规模。
- 性能负载默认测试在 SQL Server 常态 1536 MB 配置下运行 30–45 分钟高强度并发压力，以验证专用加速 profile 增加轮询、当前页 Watch 读取、冻结详情、每小时清理与 reference consumer 条件目录读取的操作次数，并用可控时间跨越 24 小时逻辑边界；验收 P95/P99、Error 701、RESOURCE_SEMAPHORE、spill、资源趋势、锁等待、tempdb、日志与轮询遗漏。出现风险信号时升级 4 小时或 24 小时真实 soak；长时间运行不再是日常实现关闭的默认前置条件。
- 2048 MB 维护配置只在独立维护场景测试，并证明结束后恢复 1536 MB。800 MB 配置测试只验证配置拒绝或前置门禁，不重新把生产负载运行到已知故障状态。
- Cutover seam 只使用隔离的临时旧库/新库和明确测试实例。分别让每一个门禁单独失败，证明精确旧库未删除、系统库/新库/错误目录/错误版本/活动连接目标均被拒绝、没有后台重试。
- Cutover 成功测试证明墓碑数量与哈希、连续三轮投影、主要 Watch API、ExternallyReadableDemandCatalog、reference consumer、contract/schema 和旧库身份同属一个 CutoverRunId；只有随后才删除测试旧库并生成数据库外证据与 Windows 事件。
- Cutover 证据测试验证不可覆盖、无业务原文、包含要求身份与门禁摘要，并证明临时删库权限在成功、失败和异常退出后都被撤销。
- 既有测试 prior art 优先复用：SingleFlightPollLoopTests 用于单飞调度，ProjectionCommitAtomicityConcurrencyTests 用于提交与读栅栏，DemandSeriesFrozenSnapshotTests 用于冻结身份，TwelveHourArchiveAndLongGoneVisibleTests 用于归档重现，ExternallyReadableDemandCatalogTests 用于目录安全，EmptyDatabaseBootstrapTests 用于空库 schema，RetiredContractAndCutoverSafetyTests 与 CutoverDrillScriptTests 用于删库边界，WatchV2AutoRefreshTests 与 WatchOverviewSnapshotTests 用于刷新和概览。
- 涉及 SQL 的 Tier 1 必须使用真实 SQL Server 环境，先通过 run-tests skill 获取准确命令，并确认最终结果 Failed: 0、Skipped: 0；只看到 Failed: 0 不能证明 82 项 SQL 集成测试已运行。
- “完整测试套件”按仓库规则只表示 Tier 1 MesIngest.Tests。若实现实际修改 Watch UI、XAML、Wpf.Ui、UI Automation、DPI 或视觉基线，必须先读取 Fluent/Golden 规则，并在说明成本、获得用户同意后运行最窄 Tier 2；不主动进入 Tier 3。
- 每个性能或容量结论必须保存可重复证据：构建身份、contract/schema、SQL Server 版本与配置、HistoryEpoch、数据规模、压缩状态、查询参数、并发模型、持续时间、逻辑读、延迟分位、资源等待和测试 skip 数。

## Out of Scope

- 修改客户批准的 MES_TASK_UNION SQL、Oracle 索引、视图、DDL、CDC 或其它客户数据库对象。
- 用增量 Oracle 查询替代完整快照，或改变现有缺席权威、RestartBarrier、PausedZeroDrop 和 TaskTypeProtection 领域语义。
- 通过 800 MB SQL Server 上限、截断原始证据、丢弃失败证据或降低正确性来达到内存目标。
- 在首版实现 ObservationPayload、ObservationSet、Span 或其它内容寻址去重模型；只有容量或热查询门禁失败才重新决策。
- 为旧 contract/schema/DTO 保持兼容、增加长期 /api/v3、支持新旧 Host/Watch/reference consumer 混跑或原地迁移旧详细历史。
- 创建数据库完整、差异或事务日志备份，或在旧库删除后提供历史/版本回滚。
- 让日常 Host、Watch、远程 API、SQL Server Agent 或外部计划任务拥有删库、确认历史重置、恢复 StoragePressurePause 或业务清理权限。
- 把 Watch 改成生产操作 HMI、添加高风险恢复按钮，或给 Inspector 增加独立刷新会话。
- 重新设计已经接受的 Watch 视觉结构；若状态呈现需要 UI 修改，必须沿用现有生产 UI 与已接受原型权威，并另走获批 Tier 2。
- 主动运行 Tier 2、Tier 3、推广视觉基线或在真实生产数据库上执行切换删除。
- 清理、重置、覆盖或归属当前工作区中与本规格无关的 SQL、Watch、测试、原型和 artifact 在途改动。

## Further Notes

- 相关设计权威为 ADR-mes-0020（StoragePressurePause）、0021（同窗空库切换）、0022（有界历史与墓碑）、0023（SIMPLE 无备份）、0024（Host 清理）、0025（HistoryEpoch 与确认）、0026（当前/历史物理路径）、0027（冻结一致性）、0028（本地管理）、0029（精确 V2 身份）和 0030（一次性自动删旧库）。
- ADR-mes-0022 已取代永久保留 GONE 明细、永久错误历史和永久关键原文的旧决定；ADR-mes-0008 中完整 Oracle 源快照、本地差异投影与有界读取仍有效。
- 旧增长诊断中对 Browse 快速路径的局部优化和 PAGE 压缩估算是基线证据，不是本规格已经实现的证明。当前 Browse 仍有用户在途改动，实施时必须重新采集真实执行计划和差分边界。
- 工作区在本规格发布前已经很脏。本规格只新增 issue-tracker 文档，不修改生产代码、配置、服务、数据库、测试或现有 ADR。
- 后续适合用 to-tickets 按 blockers-first 拆分：反馈环与基线 → 当前态热查询 → 轮询/刷新 → 新 schema/压缩 → 有界清理与墓碑 → HistoryEpoch/API/本地管理 → Watch 状态呈现 → CutoverMode → 端到端验证。
