# 11 — Alert 非模态详情与统一事件查看

**What to build:** 让操作员通过双击/Enter/右键查看结构化 IngestAlert 详情，并在同一入口查看 Host Alert 与 Watch 本地连接事件但不混淆来源。

**Blocked by:** 02 — Watch 本地事件账本; 10 — IngestAlert 问题实例

**Status:** done

- [x] 双击 Alert、Enter、右键“查看详情”均打开可调整大小的非模态窗口
- [x] 主 Watch 在详情打开时继续刷新；所查看 Alert 以 AlertId 更新或明确显示历史快照
- [x] 公共区显示 code/severity/source/active-resolved/first-last/count/business identity
- [x] FIELD_DRIFT 用字段对比表；其余代码用结构化键值/行列表，不只显示 raw JSON
- [x] 提供复制摘要、复制 Details JSON、复制 DemandId
- [x] 有 DemandId 时可定位/查询 TransportDemand；找不到时显示明确历史/筛选提示
- [x] 统一事件入口可筛选 `Host IngestAlert` / `Watch Connection Event`，来源始终可见
- [x] 提供“打开本地日志目录”，但不尝试把 Watch 事件上传 Host
- [x] ViewModel 测试覆盖各 code 的 details projection、legacy details 和 null

## Comments

- “Unified” means one viewing surface, not one persistence store or one domain type.
- 2026-07-31: Implemented AlertDetailsProjection / AlertDetailViewModel / UnifiedWatchEvent seams with tests; non-modal AlertDetailWindow; Events window with source filter; journal ReadRecent; exact DemandId locate via `/api/demands/{id}`.
