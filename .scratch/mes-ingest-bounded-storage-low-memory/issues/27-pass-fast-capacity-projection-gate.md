# 27 — 通过快速容量预测门禁

**What to build:** 在完整新包和压缩 schema 上用代表性生产分布样本快速测量空间增长，以 30% 安全余量外推当前 15 天统一历史保留窗口；70% 与非线性作为 advisory warning，只有触及最终硬上限或关键证据不确定时 fail closed。

**Blocked by:** 26 — 完成整包切换演练.

**Status:** ready-for-human

- [x] 直接复用 Ticket 02 固定分布、证据入口和真实压缩 schema；只生成不超过 250,000 条 RawObservation 的固定样本，覆盖活跃/归档 Series、错误、墓碑与清理。
- [x] 实测每轮、每行、表、聚集索引、非聚集索引、PAGE 压缩、墓碑、版本存储、tempdb 影响和 LDF 增量，并以 30% 安全余量外推 15 天。
- [x] 外推结论证明逻辑已用空间不超过 12 GB、物理数据库文件不超过 16 GB、LDF 目标不超过 2 GB。
- [x] 预测达到或超过逻辑 12,288 MB、物理 16,384 MB、LDF 2,048 MB 任一最终硬上限，或证据缺失、样本超限、PAGE 压缩/清理完整性不确定时 fail closed；70% 与增长非线性保留为 advisory warning。
- [x] 验证 RawObservation 和 RetentionEligibleDemandSeries 清理已执行，活跃 Series 没有被按年龄拆散。
- [x] 记录 SIMPLE 恢复、log reuse wait、自动增长、清理批次默认值、max server memory、模型输入、公式和误差余量，使结果可重放。
- [x] 正常快速路径不物化约 5554 万条 15 天观测、不新建容量工具，目标在 45 分钟内完成；若门禁失败，阻断发布并形成重新评估内容寻址方案的证据。
- [x] 开发期只运行聚焦容量模型测试，关闭时运行一次真实 SQL Server Tier 1，最终 Failed: 0、Skipped: 0。

## Comments

- 2026-08-25：在 Ticket 02 既有 `validation/Invoke-ScaleAndQueryEvidence.ps1` public seam 上增加快速容量模式，没有新建容量工具；固定 seed 8005、14 秒/轮、600 条/轮、600 Series、70% 活跃/30% 归档/10% 活动错误，入口在连接 SQL 前拒绝超过 250,000 行。clean build `89c54eed2f0f64284a6fbd5f587a0d9e0f6eefb9`、`sourceDirty=false`，Host SHA-256 `b224fde5b5cced91c00d5b9f7647a65072007e0a320fc3e4ffff0f5052fc0485`，contract/schema `2026.08.new-mes-ingest.v2.1/28`。
- 2026-08-25：真实 SQL 为本机默认实例服务 `LAB-WIN-01/MSSQLSERVER`（连接与 `SERVERPROPERTY(ServerName)` 为 `LAB-WIN-01`，default InstanceName），SQL Server `16.0.1190.2`、compatibility `160`、SIMPLE、max server memory `1536 MB`、非 LocalDB。baseline `scale-20260824T212917Z-e6d66c5f`；样本 `scale-20260824T212942Z-78243ac8`，415 历史轮 + 当前轮，精确 `249,600` RawObservation；未物化 `111,085,200` 行。
- 2026-08-25：样本逻辑增长 `36.367185 MB`，即 `0.087631771 MB/轮`、`0.000146052952 MB/行`；30 天模型为 `185,142` 轮/`111,085,200` 行。含 30% 余量和 180 个墓碑的逻辑预测 `21,094.459 MB`，物理文件按 `72 MB + n*64 MB` 预测 `21,128 MB`，LDF 预测 `343.190 MB`；对应门槛 70% 为 `8,601.6/11,468.8/1,433.6 MB`。段速率比 `2.42778 > 1.20`，因此以 `CAPACITY_GROWTH_NONLINEAR`、`CAPACITY_LOGICAL_70_PERCENT_ESCALATION`、`CAPACITY_PHYSICAL_70_PERCENT_ESCALATION` fail closed。第三项容量上限证明未满足并保持未勾选；发布阻断，必须由人工批准/安排已有 `ProfileDays 30` 完整规模路径；只有完整规模仍失败才重新评估内容寻址。
- 2026-08-25：三个 DemandRawObservation 聚集/非聚集索引均为 PAGE；墓碑实测 25 行、两个 allocation 各 `0.015625 MB` used，并按固定 180 归档 Series +30% 预测 `0.2925 MB`。database version-store 峰值 `136.8125 MB`、+30% `177.85625 MB`；tempdb version-store 峰值 `140.6875 MB`、+30% impact `182.89375 MB`。LDF 由 8 MB baseline 增至 load/query 200 MB、cleanup 物理峰值 `263.992 MB`，增量 `255.992 MB`、used peak `64.293 MB`、final log reuse wait `NOTHING`；数据/LDF 均固定 64 MB 自动增长。
- 2026-08-25：生产清理只把检查间隔加速到 1 秒，发布默认仍为 `3600s / 210,000 raw rows / 25 whole Series / 15s`。删除 `249,600/249,600` RawObservation、`25/25` eligible Series，写 25 tombstone，raw/eligible 残留 `0/0`。活跃图前后都是 1,500 facts，420 Series/420 generation-bearing demands/480 events/60 conditions/60 error periods/60 evidence，SHA-256 同为 `661d764938228dba93fe2ef936fa873bfbc7200bf78a6a889915b6db8297f376`，split 0。
- 2026-08-25：聚焦容量模型最终 `21 passed / 0 failed / 0 skipped`。唯一一次 Tier 1 从 `mes/ingest/csharp` 经精确 `dotnet test MesIngest.Tests` 包装运行：`882 passed / 0 failed / 0 skipped / total 882`，exit 0，11m05s；TRX SHA-256 `e2922066b447538f4f65999bb317aed5177c9c7362e538c604958cc4527a1d9e`。本轮新建测试库残留 0；五个无 session 的 Ticket01 库在本轮开始前已存在，未越权删除。最终双轴 review：Standards 0 / Spec 0；Ticket 28 scope 0。无 Watch UI 改动，Tier 2/3 不适用且未运行。紧凑证据见 `evidence/ticket27-fast-capacity-2026-08-25/`，完整 ShowPlan/raw bundle 本机见 `mes/ingest/csharp/.artifacts/ticket27-clean-evidence-2026-08-25/`。
- 2026-08-25：用户后续将所有实际历史保留统一为 15 天。RawObservation 与
  RetentionEligibleDemandSeries 使用精确 Host UTC 15×24 小时；Watch 本地连接/延迟日志默认 15 天；
  ErrorSearch 的 `LAST_30_DAYS` 被 `LAST_15_DAYS` 取代。破坏性 API 变化随整包提升为
  contract/schema `2026.08.new-mes-ingest.v2.2/29`、`ERROR_SEARCH` capability `2.1`。
- 2026-08-25：clean product commit `87d401b3b39a8dea32bc330f9d0d38f5d0bd28d2`，Host
  SHA-256 `eb67d27e1b4b5abb0f29134aea1cacbf03f099acf3ab9256bcbfdf5c4f4f502d`。同一
  `LAB-WIN-01/MSSQLSERVER` 默认真实实例为 SQL Server `16.0.1190.2`、compat 160、SIMPLE、
  max server memory 1536 MB、非 LocalDB。baseline `scale-20260825T071241Z-52633e35`；样本
  `scale-20260825T071312Z-9547f8cb`，415 历史轮/249,000 历史行 + 当前 600 行 = 249,600。
- 2026-08-25：15 天目标 `floor(15*86400/14)=92,571` 轮/55,542,600 历史行。沿用实测
  `36.367185 MB` 增长、`0.087631771 MB/轮`、`0.000146052952 MB/行` 与 30% 余量，预测逻辑
  `10,548.651 MB`、物理 `10,568 MB`、LDF `343.190 MB`；最终上限均满足，但逻辑超过 70%
  的 `8,601.6 MB` 且段速率比 `2.42778 > 1.20`，故以 `CAPACITY_LOGICAL_70_PERCENT_ESCALATION`
  与 `CAPACITY_GROWTH_NONLINEAR` fail closed。发布仍阻断，需人工批准/安排已有 `ProfileDays 15`
  完整规模路径；本轮没有物化约 5554 万行。
- 2026-08-25：三个 Raw 索引均为 PAGE；清理删除 `249,600/249,600` Raw 和 `25/25`
  eligible Series、写 25 墓碑，残留 `0/0`。活跃图前后同为 1,500 facts、420 Series，split 0，
  SHA-256 不变。database version-store 峰值 `136.8125 MB`（+30% `177.85625`）；tempdb 峰值
  `140.25 MB`（+30% `182.325`）；LDF 物理峰值 `263.992 MB`、增量 `255.992 MB`，cleanup 后
  log reuse wait `ACTIVE_TRANSACTION`。数据/LDF 固定 64 MB 自动增长；清理发布默认仍为
  `3600s / 210,000 / 25 / 15s`；新建 scale 数据库残留 0。

## Golden WPF checklist for the 15-day follow-up

- [x] Read `docs/agents/golden-renderer.md` and `docs/agents/fluent-ui.md`.
- [x] Ran un-narrowed `watch-production-preview` through the interactive golden task.
- [ ] User approved the final real-window ErrorSearch preview.
- [x] Recorded the unique evidence directory and all named skips.
- [x] Cleaned scheduled tasks/processes, rechecked 1920x1080 / 96 DPI, and restored the VM to Off.

- 2026-08-25：Tier 2 `watch-production-preview` passed：`watch-vm-tests` 146 passed/0 failed/
  5 named fixture-only skips；`watch-ui-journeys` 1/0/0。环境为 GPT-WIN11 interactive Session 1、
  1920x1080、96 DPI、light/zh-CN/China Standard Time/SoftwareOnly；task/process 残留 0，未提升
  candidate/baseline。生产 journey 已展开时间范围并断言/捕获可见的“最近 15 天”；人工仍需查看
  `06a-error-search-15-day-window.png` 最终预览。紧凑证据见
  `evidence/ticket27-15-day-retention-2026-08-25/`；完整 raw/golden 路径见该目录 README。
- 2026-08-25：首次全套 Tier 1 保留为红证据：879 passed/3 failed/0 skipped；暴露两处旧 30 天
  earliest-boundary 测试期望和一处 OpenAPI capability enum 旧期望。精确修正并通过聚焦回归后，
  正式关闭 Tier 1 在 `LAB-WIN-01/master`（SQL Server major 16、compatibility 160、非 LocalDB）为
  882 passed/0 failed/0 skipped，exit 0，12m35s；TRX SHA-256
  `e5171b9f21e393e906acd03ebc2298429952fba78bc595f0d0dedf315c91610b`。最终双轴 review：
  Standards `No findings` / Spec `No findings`；Ticket 28 diff 0，旧 30 天 tracked evidence diff 0。
  本轮 scale 库残留 0；五个零 session 的 Ticket01 库在本轮前已存在，未越权删除。Tier 3 未运行，
  因未提升候选/基线且人工预览批准仍待完成。
- 2026-08-25：用户明确接受 15 天容量预测风险并要求放宽门禁、直接复用既有实测数据，不新增或
  重跑容量证据。门禁现保留 30% safety margin 与最终硬上限 logical `12,288 MB` / physical
  `16,384 MB` / LDF `2,048 MB`；只有预测达到或超过任一硬上限，或证据缺失、样本超过
  `250,000`、PAGE 压缩不确定、清理完整性不确定时 fail closed。原 70% 阈值与增长非线性仍
  如实输出 `CAPACITY_LOGICAL_70_PERCENT_ESCALATION`、`CAPACITY_GROWTH_NONLINEAR` advisory
  warnings，但不再阻断发布或强制 full-scale。
- 2026-08-25：直接按既有 15 天实测 `249,600` 行、415 历史轮、30% 余量重新判读：logical
  `10,548.651 < 12,288 MB`、physical `10,568 < 16,384 MB`、LDF
  `343.190 < 2,048 MB`，且三个 Raw 索引 PAGE、清理 `249,600/249,600` Raw 与 `25/25`
  eligible Series、残留 `0/0`、活跃图 split `0`，因此新政策下 capacity gate 通过。旧 30 天与
  旧 15 天 fail-closed 证据及其评论保持历史事实、未修改。本次范围
  覆盖明确禁止新测试与证据运行；已启动的聚焦测试在执行阶段被中止，Tier 1/2/3/full-scale
  均未运行，未创建数据库或新证据目录。Golden preview candidate 仍未提升为 baseline；依仓库
  规则，整票在用户明确批准既有最终真实窗口预览前保持 `ready-for-human`，不冒充视觉验收。
