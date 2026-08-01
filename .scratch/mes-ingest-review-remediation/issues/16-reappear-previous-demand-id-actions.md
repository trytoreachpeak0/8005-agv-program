# 16 — REAPPEAR 详情可操作先前 DemandId

**What to build:** `REAPPEAR_AFTER_GONE` 详情除展示新旧 DemandId 外，还须让操作员能够分别复制和定位先前 GONE 实例与新实例；历史实例不可见或已超出默认窗口时，应给出明确的历史/筛选提示，而不是静默改为定位新实例。

**Blocked by:** None — can start immediately

**Status:** done

- [x] REAPPEAR 详情将 previousDemandId 与 newDemandId 投影成两个明确、不会混淆的操作目标
- [x] 操作员可分别复制旧 ID 与新 ID，且既有 Copy summary / Details JSON 行为不回归
- [x] 定位旧 ID 时按该精确 ID 查询；若实例为 GONE、超出当前窗口或不可见，显示可执行的历史/筛选提示
- [x] 定位新 ID 继续进入当前 VISIBLE 实例；不得因旧 ID 查找失败而静默改用新 ID
- [x] 非 REAPPEAR 或缺少 previousDemandId 的告警不显示无效的旧实例操作
- [x] ViewModel 与轻量 UI 测试覆盖旧/新复制、旧/新定位、历史提示和缺少旧 ID 的对照场景

## Comments

- 2026-08-01: Implemented distinct Previous GONE / New VISIBLE DemandId targets in `AlertDetailViewModel` and `AlertDetailWindow`, with independent copy and exact locate actions. Exact lookup continues through `GET /api/demands/{demandId}`; missing/out-of-window results explicitly direct the operator to Host history, filters, and the GoneAt window without substituting another DemandId. Added ViewModel, STA WPF, clipboard-boundary, exact-client-path, and locate-hint regressions. `dotnet build MesIngest.sln --no-restore` succeeded with 0 warnings/errors; full suite passed 411/411.
