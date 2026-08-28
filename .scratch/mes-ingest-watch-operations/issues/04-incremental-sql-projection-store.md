# 04 — SQL Server 投影增量持久化并移除 GONE 热路径

**What to build:** 用差异写入替换当前每轮 DELETE + 全量重插 TransportDemands/TaskTypePauses；永久 GONE 保留可查，但正常轮询只处理 VISIBLE 和必要对账状态。

**Blocked by:** 03 — 分阶段耗时遥测（提供前后基线；实现可并行起步）

**Status:** done

- [x] 成功轮询只 INSERT 新 Demand、UPDATE 实际变化行、UPSERT pause；未变化行零写入
- [x] 禁止清空并重建 dbo.TransportDemands / dbo.TaskTypePauses
- [x] 正常 GetState/Reconcile 输入不加载全部 GONE；reappear 按 TASK_TYPE+SUBLOT 索引检查历史
- [x] GONE 业务字段形成后不可变，不在以后轮询反复重写
- [x] 每轮状态差异与 Alert/ChangeFeed 所需变化可在明确事务边界内一致提交
- [x] 为并发 Watch/API 查询缩短进程 gate 和 SQL transaction 持有时间
- [x] 保留重启 barrier、DisappearCount、PausedZeroDrop 既有语义
- [x] SQL Server 集成测试证明一条变化不会重写无关 Demand，且 API 不见半状态

## Comments

- This is a persistence optimization, not a change to full MES snapshot reconciliation semantics.
- 2026-07-31: Incremental ReplaceState (INSERT/UPDATE/UPSERT), GetState VISIBLE-only, HasGoneTransportDemandKey for reappear, GONE immutable, projection+alerts same transaction, indexes for TaskType+Sublot / Status+Dates+DemandId / GoneAt+DemandId. ChangeFeed append itself remains ticket 06.
