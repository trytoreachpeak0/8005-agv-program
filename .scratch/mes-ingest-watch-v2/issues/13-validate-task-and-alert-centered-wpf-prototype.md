# 验证以 MES 任务与 IngestAlert 为中心的简化 WPF 原型

Type: prototype
Status: resolved
Blocked by: 07

## Question

在不再包含性能分析、诊断、trace 或诊断导出的前提下，怎样用概览、MES 任务/TransportDemand、IngestAlert 和必要设置组成最小可用的 WPF 信息架构，并用真实六类 TASK_TYPE、七列 MES 字段、TransportDemand 投影字段和六类 IngestAlert 假数据验证页面层级、表格列、筛选、详情与跳转？

## Comments

2026-08-07 已形成待人工评审的 throwaway WPF 原型，代码入口为 [MesIngest.Watch.Prototype](../../../mes/ingest/csharp/MesIngest.Watch.Prototype/README.md)，截图集为 [task-alert-review](../prototype/task-alert-review/)：

- A「健康优先四页」：概览、MES 任务 / TransportDemand、IngestAlert、设置以左侧导航组织，启动页首先回答接入健康、活动告警与 VISIBLE Demand。
- B「MES 任务工作台」：六类 TASK_TYPE 常驻，强调七个 MES 输入字段与本地 TransportDemand 投影的分层。
- C「告警上下文常驻」：只读活动 IngestAlert 队列常驻右侧，跨页面保留异常上下文。

假数据覆盖真实六类 TASK_TYPE、七个 MES 字段、本地投影字段与真实六类 IngestAlert code；性能/诊断/trace/诊断导出和告警处置均已排除。已通过 `dotnet build --no-restore`，并在 2560×1440 与 1440×900 截图中检查宽表、详情区、长 code 与导航换行。人工评审最终选择方案 A。

## Answer

2026-08-07 人工评审选择 A「健康优先四页」作为 MesIngestWatch V2 产品壳：使用左侧导航组织概览、MES 任务 / TransportDemand、IngestAlert 和设置；概览首先展示 Host 接入状态、活动 IngestAlert 数量和 VISIBLE TransportDemand 数量，使现场实施与运维工程师能在约 10 秒内判断接入是否健康及是否需要下钻。

B 与 C 不作为全局壳，也不保留常驻任务或告警侧栏：B 的六类 TASK_TYPE 入口吸收到 MES 任务页的显式筛选与任务构成中；C 的告警快速入口、Alert → Demand 跳转和异常上下文吸收到概览与 IngestAlert 页。这样既保留两者有价值的局部交互，又给七列 MES 字段和 TransportDemand 投影宽表留下最大空间。

正式规格须维持原型验证的范围边界：Host 连接失败是 Watch 连接状态而不是 IngestAlert；只展示 Core 实际产生的六类 IngestAlert；Alert 全程只读；性能分析、诊断、trace、遥测上报、诊断导出和告警处置均不进入 V2。1440×900 下宽表允许水平滚动，但选中行的 MES 输入与本地投影详情必须持续可见。

完整三方案原型及截图作为主要证据保存在 throwaway 分支 `codex/prototype-mes-ingest-watch-v2-task-alert`，提交 `6cfdc5fa7e8792f53f35df81c44539e9653ecb65`；当前工作树中的原型文件不应直接提升为生产实现。
