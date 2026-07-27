# 01 — 录制快照到只读 API 的最小纵切片

**What to build:** 用工厂录制的 MES 快照文件跑一轮无界面宿主，首次出现的 reconcile 键生成带稳定 DemandId、已冻结 MES 字段的 VISIBLE TransportDemand，经内存投影后可通过只读 HTTP 列出/获取；含六种 TASK_TYPE、上线基线时间过滤、PACKAGE 原样保留，并建立 Reconciler 与 HTTP 契约测试骨架。

**Blocked by:** None — can start immediately

**Status:** done

- [x] 录制快照文件可作为 MesSnapshotSource 输入，无需连接 Oracle
- [x] 首次出现的 TASK_TYPE+SUBLOT 创建 VISIBLE TransportDemand 并分配 DemandId
- [x] 首次可见时冻结 TASK_TYPE、SUBLOT、EQP、AREA、STEP、DATES、PACKAGE 等投影字段
- [x] 六种 TASK_TYPE（含 WIRE_TO_NITROGEN）按相同规则投影
- [x] 上线基线前的记录不进入 VISIBLE；过滤在应用层完成，不改客户 SQL
- [x] PACKAGE 原样冻结保留，不因 package-universe 未完成而阻断创建
- [x] 只读 HTTP 可列出/按 DemandId 获取当前需求
- [x] Reconciler 与 HTTP 契约测试覆盖本票行为

## Comments

- 2026-07-27: Implemented under `mes/ingest/csharp` (Core + Host + Tests). Formal seams: `TransportDemandReconciler`, `/api/demands`. File CSV source + in-memory store; one-shot on startup. Factory `latest.csv` dates are mostly pre-2026-08-01 — override `MesIngest__GoLiveBaseline` for local demos.
