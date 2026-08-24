# 27 — 通过快速容量预测门禁

**What to build:** 在完整新包和压缩 schema 上用代表性生产分布样本快速测量空间增长，以 30% 安全余量外推 30 天，并只在预测接近门槛或证据不确定时升级完整规模验证。

**Blocked by:** 26 — 完成整包切换演练.

**Status:** ready-for-human

- [x] 直接复用 Ticket 02 固定分布、证据入口和真实压缩 schema；只生成不超过 250,000 条 RawObservation 的固定样本，覆盖活跃/归档 Series、错误、墓碑与清理。
- [x] 实测每轮、每行、表、聚集索引、非聚集索引、PAGE 压缩、墓碑、版本存储、tempdb 影响和 LDF 增量，并以 30% 安全余量外推 30 天。
- [ ] 外推结论证明逻辑已用空间不超过 12 GB、物理数据库文件不超过 16 GB、LDF 目标不超过 2 GB。
- [x] 任一预测达到对应门槛的 70%、增长非线性、样本不足、压缩或清理证据不确定时，快速门禁必须失败并升级完整规模验证。
- [x] 验证 RawObservation 和 RetentionEligibleDemandSeries 清理已执行，活跃 Series 没有被按年龄拆散。
- [x] 记录 SIMPLE 恢复、log reuse wait、自动增长、清理批次默认值、max server memory、模型输入、公式和误差余量，使结果可重放。
- [x] 正常快速路径不物化约 1.11 亿条 30 天观测、不新建容量工具，目标在 45 分钟内完成；若门禁失败，阻断发布并形成重新评估内容寻址方案的证据。
- [x] 开发期只运行聚焦容量模型测试，关闭时运行一次真实 SQL Server Tier 1，最终 Failed: 0、Skipped: 0。

## Comments

- 2026-08-25：在 Ticket 02 既有 `validation/Invoke-ScaleAndQueryEvidence.ps1` public seam 上增加快速容量模式，没有新建容量工具；固定 seed 8005、14 秒/轮、600 条/轮、600 Series、70% 活跃/30% 归档/10% 活动错误，入口在连接 SQL 前拒绝超过 250,000 行。clean build `89c54eed2f0f64284a6fbd5f587a0d9e0f6eefb9`、`sourceDirty=false`，Host SHA-256 `b224fde5b5cced91c00d5b9f7647a65072007e0a320fc3e4ffff0f5052fc0485`，contract/schema `2026.08.new-mes-ingest.v2.1/28`。
- 2026-08-25：真实 SQL 为本机默认实例服务 `LAB-WIN-01/MSSQLSERVER`（连接与 `SERVERPROPERTY(ServerName)` 为 `LAB-WIN-01`，default InstanceName），SQL Server `16.0.1190.2`、compatibility `160`、SIMPLE、max server memory `1536 MB`、非 LocalDB。baseline `scale-20260824T212917Z-e6d66c5f`；样本 `scale-20260824T212942Z-78243ac8`，415 历史轮 + 当前轮，精确 `249,600` RawObservation；未物化 `111,085,200` 行。
- 2026-08-25：样本逻辑增长 `36.367185 MB`，即 `0.087631771 MB/轮`、`0.000146052952 MB/行`；30 天模型为 `185,142` 轮/`111,085,200` 行。含 30% 余量和 180 个墓碑的逻辑预测 `21,094.459 MB`，物理文件按 `72 MB + n*64 MB` 预测 `21,128 MB`，LDF 预测 `343.190 MB`；对应门槛 70% 为 `8,601.6/11,468.8/1,433.6 MB`。段速率比 `2.42778 > 1.20`，因此以 `CAPACITY_GROWTH_NONLINEAR`、`CAPACITY_LOGICAL_70_PERCENT_ESCALATION`、`CAPACITY_PHYSICAL_70_PERCENT_ESCALATION` fail closed。第三项容量上限证明未满足并保持未勾选；发布阻断，必须由人工批准/安排已有 `ProfileDays 30` 完整规模路径；只有完整规模仍失败才重新评估内容寻址。
- 2026-08-25：三个 DemandRawObservation 聚集/非聚集索引均为 PAGE；墓碑实测 25 行、两个 allocation 各 `0.015625 MB` used，并按固定 180 归档 Series +30% 预测 `0.2925 MB`。database version-store 峰值 `136.8125 MB`、+30% `177.85625 MB`；tempdb version-store 峰值 `140.6875 MB`、+30% impact `182.89375 MB`。LDF 由 8 MB baseline 增至 load/query 200 MB、cleanup 物理峰值 `263.992 MB`，增量 `255.992 MB`、used peak `64.293 MB`、final log reuse wait `NOTHING`；数据/LDF 均固定 64 MB 自动增长。
- 2026-08-25：生产清理只把检查间隔加速到 1 秒，发布默认仍为 `3600s / 210,000 raw rows / 25 whole Series / 15s`。删除 `249,600/249,600` RawObservation、`25/25` eligible Series，写 25 tombstone，raw/eligible 残留 `0/0`。活跃图前后都是 1,500 facts，420 Series/420 generation-bearing demands/480 events/60 conditions/60 error periods/60 evidence，SHA-256 同为 `661d764938228dba93fe2ef936fa873bfbc7200bf78a6a889915b6db8297f376`，split 0。
- 2026-08-25：聚焦容量模型最终 `21 passed / 0 failed / 0 skipped`。唯一一次 Tier 1 从 `mes/ingest/csharp` 经精确 `dotnet test MesIngest.Tests` 包装运行：`882 passed / 0 failed / 0 skipped / total 882`，exit 0，11m05s；TRX SHA-256 `e2922066b447538f4f65999bb317aed5177c9c7362e538c604958cc4527a1d9e`。本轮新建测试库残留 0；五个无 session 的 Ticket01 库在本轮开始前已存在，未越权删除。最终双轴 review：Standards 0 / Spec 0；Ticket 28 scope 0。无 Watch UI 改动，Tier 2/3 不适用且未运行。紧凑证据见 `evidence/ticket27-fast-capacity-2026-08-25/`，完整 ShowPlan/raw bundle 本机见 `mes/ingest/csharp/.artifacts/ticket27-clean-evidence-2026-08-25/`。
