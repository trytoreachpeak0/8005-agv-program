# 05 — 零字节 CSV 视为 Incomplete，不推进 presence

**What to build:** CSV 快照源在读到零字节（或等价“尚未写完”的空文件）时，必须得到 Incomplete / `POLL_INCOMPLETE`，不得当作成功空快照去推进消失计数或 GONE。

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

## Parent / References

- Spec: `.scratch/mes-ingest-phase-1/spec.md`（失败/不完整轮次不得错误变更 presence）
- Issues:
  - `.scratch/mes-ingest-phase-1/issues/15-row-parse-errors-as-incomplete.md`
  - `.scratch/mes-ingest-phase-1/issues/03-mes-data-quality-diagnostics.md`
- Handoff finding: Other confirmed — zero-byte CSV

不重新定义 Incomplete vs Failure 分类；本票把零字节文件纳入 Incomplete 输入。

## Repro

1. 投影中已有若干 VISIBLE。
2. 将 CSV 路径替换为 0 字节文件（模拟截断写窗），跑一轮 poll。
3. 观察 outcome、alert 与 VISIBLE/GONE 是否变化。

期望失败态（现状）：零字节被当成成功空快照，可能推进消失/GONE。

## Regression tests

- [ ] 0 字节 CSV → `Incomplete` + `POLL_INCOMPLETE`，presence 不变
- [ ] 合法空表头+无数据行（若契约区分“完整空结果”）行为与 0 字节对照明确，测试锁定
- [ ] 写完后的正常非空/空结果快照仍按既有成功路径工作
- [ ] Oracle 路径不因本票被误改为拒绝合法空结果集（仅钉 CSV 截断语义）

## Acceptance criteria

- [ ] 零字节 CSV 不产生成功空对账副作用
- [ ] 分类为 Incomplete / 数据质量，而非链路 Failure（除非 IO 真失败）
- [ ] 源与 runner 回归测试覆盖；既有缺列/坏行 Incomplete 用例仍绿
