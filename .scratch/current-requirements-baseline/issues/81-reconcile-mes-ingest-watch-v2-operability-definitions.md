# 回流并核对 MesIngestWatch V2 运维定义

Type: task
Status: resolved
Blocked by: 73

External blocker cleared: `origin/codex/factory-validation` 提交 `fbd251df78bb996e0a624db65bc8e6840eff4bf8` 中“定义端到端延迟可观测契约”“识别现有 IngestAlert 与 MES 任务形态”“定义流畅刷新、游标分页与取消模型”“汇编 V2 产品与交互规格”及最终“确认 V2 实现交接”均已解决。

## Question

在 `origin/codex/factory-validation` 的「MesIngestWatch V2 产品与交互规格路线图」中「定义端到端延迟可观测契约」「定义 Alert、Demand 诊断与导出边界」「定义流畅刷新、游标分页与取消模型」及其规格汇编均关闭后，如何逐项核对并回流其中已明确批准的 MesIngest 轮询、刷新、告警生命周期、诊断和日志留存定义，同时保持 MesIngestWatch 运维台与 8005 车队/仓位看板、全系统业务审计及车载技术日志的范围分离；若来源票据仍开放、只有 Notes、原型或实现默认值，则不得据此升级为当前需求基线结论？

## Context

- 来源地图：`origin/codex/factory-validation:.scratch/mes-ingest-watch-v2/map.md`
- 待核对票据：`06-define-end-to-end-latency-observability-contract.md`、`07-define-alert-demand-diagnostics-and-export-boundary.md`、`08-define-responsive-refresh-paging-and-cancellation-model.md`、`09-assemble-v2-product-and-interaction-specification.md`
- 关联当前证据：`R01-A1915`、`R01-A1923`、`R01-A2951`、`R01-A3047` 中属于 MesIngest/MesIngestWatch 的部分，以及回流时可证明直接关联的后续证据。

## Comments

- 2026-08-06：核验 `origin/codex/factory-validation` 提交 `a115ed4ac7de804b92ffaba8a9da8f0e6515dfc4`；上述四张来源票据均仍为 `Status: open`，不满足本票“来源定义与规格汇编均关闭后再回流”的前提。未采纳来源地图 Notes、原型或实现默认值，本票撤销领取并继续等待外部分支决定。

- 2026-08-24：重新核验来源提交 `fbd251df78bb996e0a624db65bc8e6840eff4bf8`，四张来源票及最终交接均已关闭，外部阻塞解除。逐项核对时发现旧 V2 最终规格已把中间可观测性票据裁出目标，当前工作树又存在明确整体替代旧 IngestAlert、旧保留和旧刷新语义的《新版 MesIngest 整体替换规格书》；因此不能整包回流旧 V2。完整身份、范围和处置见[核对记录](../evidence/mes-ingest-watch-v2-operability-reconciliation-2026-08-24.md)。

## Answer

已完成逐项回流核对，并把来源提交、各票 blob、最终规格、后续替代规格和当前词汇冲突固定在[《MesIngestWatch V2 运维定义回流核对》](../evidence/mes-ingest-watch-v2-operability-reconciliation-2026-08-24.md)。结论如下：

1. **只回流跨版本一致且未被替代的运维边界。** MesIngestWatch 是单 Host、业务只读的 MES 接入运维台，不拥有或修改业务投影，不执行调度、装卸或生产命令；Host 切换、规范化查询变化和新请求必须以会话/查询/请求代次作废迟到响应；加载、刷新或查询失败保留最后成功快照并明确其时点、失败和陈旧状态；IngestAlert 或其后续替代投影在 Watch 中均只读，不提供确认、指派、备注或手工关闭；Watch 自身连接、超时、契约或解码故障不成为 MesIngest 业务异常。
2. **不回流旧 V2 已裁出或已被后续规格替代的定义。** 「定义端到端延迟可观测契约」虽曾关闭，但旧 V2 最终规格已经把性能页、诊断页、PollTrace/WatchRefreshTrace/PerformanceState 产品面、遥测上报、诊断包、30/365 天和 2 GiB 预算裁出本期目标。后续《新版 MesIngest 整体替换规格书》又明确废弃旧六类 `IngestAlert` incident、旧已解除告警 365 天保留、旧 cursor/Feed 语义，并把自动刷新从“默认关闭、可选开启”改为“数据视图始终开启”。这些旧值不得因历史批准而冒充首版当前要求。
3. **四条关联原始记录不被静默升级。** `R01-A2951` 没有获得 MesIngest 查询 MES 的批准周期，Watch 的 10/30/60/300 秒界面刷新不能代替它；`R01-A1915` 的 MES 告警部分不能再采用已被替代的旧 incident 模型；`R01-A1923` 不产生跨调用统一“重试 N 次”；`R01-A3047` 不能从已裁出的中间票据取得 Watch 本机日志数字。车队/仓位看板 2 秒刷新、服务端业务/管理员审计至少 180 天和车载技术日志至少 30 天仍按[决定监控新鲜度、告警升级、重试与日志留存规则](73-decide-monitoring-freshness-alert-retry-and-log-retention.md)独立成立。
4. **新浮现的版本治理问题单独进入前沿。** 初始快照后、首版发布前出现的替代规格应进入 `v1.0.0`、后续主版本还是其它可审计边界，不能由本任务代替最终批准人决定；已新建[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)，用于固定补充快照、批准身份、适用范围和 `Supersedes` 关系。

本票没有修改 `CONTEXT.md`：当前根词汇表已经使用后续 MesIngest 模型，回写旧 incident 定义会破坏唯一术语入口；新增治理决定尚未获得用户批准，也不应提前写入词汇表。
