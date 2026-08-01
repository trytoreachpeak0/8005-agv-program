# 04 — SQL schema 升级事务化，失败不留半迁移

**What to build:** Host 对既有库执行 schema 升级时，DDL/权限步骤在失败时不得留下不可用的半迁移状态；成功路径仍幂等、可重复，且不 DROP/重建丢失永久 GONE/DemandId 历史。

**Blocked by:** None — can start immediately

**Status:** done

## Parent / References

- Issue: `.scratch/mes-ingest-watch-operations/issues/14-schema-migration-config-and-upgrade-package.md`（验收：失败不留半迁移）
- Spec: `.scratch/mes-ingest-watch-operations/spec.md`（升级/保留）
- ADR: `docs/adr/mes/0008-full-source-snapshot-incremental-local-projection.md`
- Handoff finding: Highest priority #4

不重新定义升级包内容或 Oracle 只读边界；本票补齐原子性/失败语义缺口。

## Repro

1. 从 Phase-1 schema fixture 启动升级。
2. 在靠后的 DDL 或权限步骤注入失败（或使用无足够权限的登录）。
3. 检查库对象/版本标记是否处于“部分应用”状态；修复条件后重跑升级。

期望失败态（现状）：DDL 批无显式事务，后期失败可留下半迁移。

## Regression tests

- [x] 升级中途失败：库可识别为未完成升级（或已回滚到升级前一致点），不得出现“版本已升但对象缺失/半套列”
- [x] 失败后条件恢复再跑：升级完成且保留 DemandId、VISIBLE/GONE、pause、alerts、poll health（沿用 ticket 14 fixture 断言）
- [x] 成功路径重复执行仍幂等
- [x] 仍禁止以 DROP/重建方式清空 TransportDemand 历史

## Acceptance criteria

- [x] 失败不留半迁移（事务回滚或等价安全重入策略，与 ticket 14 验收一致）
- [x] 成功升级保留永久历史；幂等重跑通过
- [x] 自动升级测试覆盖失败注入 + 恢复重跑

## Comments

- 2026-08-01: Wrapped `EnsureSchema` in an explicit SQL transaction so mid-upgrade failure rolls back to the pre-upgrade consistent point (no half columns/objects; schema version not advanced). Covered by `Mid_upgrade_failure_leaves_no_half_migration_and_recovers_on_rerun`; `UPGRADE.md` updated for transactional semantics.
