# 固定可观测数据物理存储与版本化 API DTO

Type: grilling
Status: resolved
Blocked by: 06

## Question

在已确认的 PollTrace、WatchRefreshTrace、PerformanceState、保留/容量、上传去重、跨机校准与只读查询契约下，SQL Server 应采用怎样的表、键、索引、分桶/直方图、迟到数据修正、聚合/清理作业与容量核算，并怎样版本化遥测写入 DTO、observability 查询 DTO 及现有 Demand/Alert/PollHealth 的观察元数据，才能稳定迁移、幂等执行并通过 OpenAPI/契约门禁？

## Answer

2026-08-07 用户将 MesIngestWatch V2 范围收缩为识别和查看现有 MES 任务与 IngestAlert，明确删除性能分析和诊断部分。本票的 trace、PerformanceState、遥测写入、聚合/保留存储与 observability DTO 均已超出新 Destination，按 out of scope 关闭，未做物理 schema 决策。
