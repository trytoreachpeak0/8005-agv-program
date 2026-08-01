# 09 — REAPPEAR 详情暴露先前 GONE DemandId

**What to build:** 当同一业务键 GONE 后再次出现并分配新 DemandId 时，`REAPPEAR_AFTER_GONE` 的结构化详情必须包含先前 GONE 的 DemandId 与新 DemandId，供 Watch 详情与定位使用。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

## Parent / References

- Spec: `.scratch/mes-ingest-watch-operations/spec.md`（REAPPEAR 保存旧/新 DemandId）
- Issues:
  - `.scratch/mes-ingest-phase-1/issues/02-demand-lifecycle-appear-gone-reappear.md`
  - `.scratch/mes-ingest-watch-operations/issues/10-ingest-alert-incident-model.md`
  - `.scratch/mes-ingest-watch-operations/issues/11-watch-alert-detail-and-unified-events.md`
- Handoff finding: REAPPEAR details cannot obtain previous GONE DemandId

不重新定义 reappear 生命周期；本票补齐 alert details 所需历史身份。

## Repro

1. 使某 TASK_TYPE+SUBLOT 进入 GONE，记录旧 DemandId。
2. 再次完整成功快照出现该键，生成新 DemandId 与 `REAPPEAR_AFTER_GONE`。
3. 读 Alert details / Watch 详情投影，查看是否含旧 DemandId。

期望失败态（现状）：store 只暴露“是否有历史”布尔，reconciler 仅见当前可见态，详情缺旧 Id。

## Regression tests

- [ ] Reconciler/store：REAPPEAR alert details 含 previousGoneDemandId（或契约字段名）与 new DemandId
- [ ] Watch 详情投影展示并可复制旧/新 Id；“定位 Demand”对旧 Id 给出历史/筛选提示（沿用 ticket 11）
- [ ] 无历史的首次 CREATED 不误报 REAPPEAR、不填伪造旧 Id

## Acceptance criteria

- [ ] `REAPPEAR_AFTER_GONE` 详情可取得先前 GONE DemandId
- [ ] API/Watch 展示与 spec 一致
- [ ] 生命周期与详情投影测试覆盖 GONE→再出现对照
