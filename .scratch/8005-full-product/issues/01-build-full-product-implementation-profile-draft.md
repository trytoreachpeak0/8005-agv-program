# 建立全量 348 条实施剖面底稿

Type: task
Status: closed

## Question

以 `requirements/baselines/current-requirements-v1.0.0.md`（SHA-256 `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`，content commit `b9f321228b534a3b316d3ac1abede05176ed6a70`，tag `requirements-baseline-v1.0.0`）与 MVP 剖面 TSV（`.scratch/wire-to-gate-mvp/evidence/final-requirement-applicability-profile.tsv`，SHA-256 `0678fddb8cb0dc4b1df620257ac7076fc8658e3bda828f0de5c6e9f0fe0461de`）为唯一输入，产出一份 348 行、零遗漏的实施剖面底稿，供后续全部票据引用。

这是机械工作，不是决策：本票不判定任何条目该做还是不该做，不划批次，不改 MVP 剖面的既有四分类。它要交付的是一张让后续 grilling 票有据可依的表。

底稿至少须包含：

1. 每条需求的 `RequirementId`、标题、`OriginalScope`、MVP 剖面的 `FinalClassification`，以及从 MVP 剖面继承的 `ControlServerImpact` / `OnboardHmiImpact` / `SharedProtocolImpact` 三列——票 02 判定重构／增量归属、票 06 冻结协议 v2 消息面都直接依赖这三列。
2. 一列 `FullProductCluster`：把 348 条分入互斥且穷尽的实施簇。MVP 已覆盖的 186 条（直接必须 85 + 交互／安全依赖 101）统一归入批次 0 候选簇；MesIngest 系 100 条统一归入本图 Out of scope 簇；AGV 主项目的 62 条（不适用 47 + 首期延后 15）按业务面分簇。分簇依据必须逐条可追溯到需求文本或 `OriginalScope`，不得凭印象归类。
3. 分簇结果须经交叉核验：各簇计数相加等于 348，且 MesIngest 簇恰为 100、AGV 非 MVP 簇恰为 62、批次 0 候选簇恰为 186。任一处对不上即为底稿有缺陷，须先修正再交付。
4. 对以下两点给出明确结论，因为它们是地图 **Not yet specified** 中已登记、必须由本票清掉的迷雾：跨地图（单 Map→多 Map）相关条目落在哪个簇——是 AGV 62 条中的一簇、票 03 的一部分，还是本就在批次 0 的 186 条内；以及 62 条中是否存在既不属于既有七簇（自动充电桩与充电失败治理、多车与多任务调度、车载 Worklist 选任务模式、空闲返回与等待点、AGV 生命周期与归档恢复、账号权限密码治理、配置治理与看板）又无法归类的剩余条目。

底稿以 TSV 落在 `.scratch/8005-full-product/evidence/`，并记录其自身的 SHA-256。批次列在本票留空，由票 09 定稿时填写。

### 已知边界

- 本票不修订 MVP 剖面 TSV 的既有分类。全量剖面是新增的一层，不是对它的修订。
- 本票不判定 MesIngest 那 100 条的实现状态。地图已将其判为 Out of scope，本票只做归簇与计数核验。
- 本票不产生任何需求基线变更，不动 `requirements/current-baseline.md` 指针。
