# 06 — 切换 DemandSeries 当前与冻结读取

**What to build:** 让 DemandSeries 的当前浏览和冻结调查完整迁入新的 current/historical read seam：当前页与当前详情不扫描原始历史，冻结列表、计数、分页和详情绑定同一纪元与提交。

**Blocked by:** 05 — 引入 HistoryEpoch 内部身份.

**Status:** ready-for-agent

- [ ] 当前 DemandSeries 列表、精确计数、筛选和当前详情只依赖当前物化投影、当前条件和维护字段。
- [ ] 当前路径不得对 DemandRawObservation 全历史执行排名、排序或无界扫描。
- [ ] 冻结列表、cursor、直接定位和详情明确绑定 HistoryEpoch、ProjectionCommit、规范化筛选与稳定顺序。
- [ ] 历史详情按一个 Series 的对象边界读取，不下载或扫描无关 Series。
- [ ] 既有 VISIBLE、GONE、LONG_GONE_BUT_VISIBLE、AREA 范围、分页和详情语义保持不变。
- [ ] 复用 Ticket 02 的证据入口和数据分布，不为本票新建规模生成器；只建立空库与两个固定种子的小型历史样本，最大样本不超过 250,000 条 DemandRawObservation。
- [ ] 在真实 SQL Server 上采集实际执行计划、STATISTICS IO/TIME、内存授予和 spill；当前路径必须不访问 DemandRawObservation 历史，或只执行具有严格对象键上限的 seek。
- [ ] 正常路径不生成完整 7/15 天数据；若计划仍扫描/排名历史、ActualRowsRead 或逻辑读随小样本增长、出现异常 grant/spill、参数计划退化或证据不完整，门禁失败并升级规模验证。
- [ ] 正常验证只运行聚焦 DemandSeries/契约/执行计划测试和一次真实 SQL Server Tier 1，不运行 Tier 2、Tier 3 或额外发布演练，验证部分目标在 45 分钟内完成。
- [ ] 使用 run-tests skill 取得命令，并以最终 Failed: 0、Skipped: 0 关闭。
