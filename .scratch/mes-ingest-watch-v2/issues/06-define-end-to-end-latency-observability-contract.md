# 定义端到端延迟可观测契约

Type: grilling
Status: open
Blocked by: 01

## Question

怎样定义轮询与 Watch 请求的结构化 trace、阶段边界、correlation、数据年龄、阈值、P50/P95/最大值、30 天原始与 365 天聚合保留及只读查询契约，才能准确分析 MES→MesIngestWatch 延迟，又不把统计异常混入 IngestAlert？
