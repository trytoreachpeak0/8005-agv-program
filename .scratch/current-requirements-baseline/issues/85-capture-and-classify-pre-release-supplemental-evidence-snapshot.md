# 固定并分类首版发布前补充证据快照

Type: task
Status: resolved
Blocked by: 84

## Question

在不修改初始证据快照和任何原始需求材料的前提下，固定 2026-08-03 初始快照之后至本任务采集截止点新增或变化的全部需求性材料，形成可重复核验的 PreReleaseSupplementalEvidenceSnapshot；逐文件记录 Git/工作区身份、SHA-256、来源、适用范围和分类，并验证「决定首版基线如何处理初始快照后的替代性需求」所批准的四份规格身份未漂移。

任务必须：

- 宽口径发现补充窗口内全部需求性材料，不只采集四份已知规格；
- 把当前规范候选、支持/批准证据、实现/验收证据和历史/已替代材料明确分流，且不因补拍自动升级批准状态；
- 对四份已批准规格逐一核对 Git blob 与 SHA-256；若任一字节漂移，停止把新字节视为已批准并生成精确差异与重新批准入口；
- 记录补充快照截止时间、Git HEAD、分支、工作区状态、逐文件哈希、发现错误和可重复采集方式；
- 输出首版候选形成所需的来源层叠与 PreBaselineSourceSupersession 清单，并指出补充快照之后的材料必须重新开门或进入后续版本。

## Evidence

- [决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)
- [固定初始需求证据快照](10-capture-initial-evidence-snapshot.md)
- [建立当前需求性材料的无损清单](11-inventory-current-requirement-materials.md)

## Answer

已于 2026-08-24T12:53:54.5583914+08:00 至 2026-08-24T12:54:32.3916218+08:00（UTC 04:53:54.5583914–04:54:32.3916218）在分支 `codex/continue-wayfinder-map`、HEAD `4e2205ad5fde874c320ef90b7148ee99121d4129` 上固定 **PreReleaseSupplementalEvidenceSnapshot**。初始快照保持原样；本任务只新增独立补充层，没有修改任何原始需求材料。

### 补充窗口与完整性

- 以初始快照的 1,809 条路径及 SHA-256 为不可变对照，沿用其宽口径文档型扩展集合，并补充纳入 `.trx` 验收记录；排除依赖、构建缓存目录和补充快照自身输出目录。
- 共固定 9,319 条新增、变化或删除记录：新增 9,263、修改 55、删除 1。唯一删除项为 `mes/ingest/csharp/pack/openapi/v1.json`，仅归类为实现/验收现状证据，不据此推断契约要求被批准废弃。
- 每条均记录 `change_kind`、Git 工作区状态、HEAD/index blob（存在时）、当前与初始 SHA-256、字节数、最后修改时间、来源、适用范围、分类和批准效果；所有记录的 `approval_effect` 均为 `none-by-capture`。
- 分类结果为：规范候选 5、支持/批准证据 270、实现/验收证据 8,981、历史/已替代证据 63。独立复核确认 9,319 条路径零重复、现存项零缺失、删除项确已不存在、分类零空白、补充输出零自引用、发现错误为 0。

### 四份获批规格身份核验

逐份同时复核了 HEAD blob、index blob、工作区 `git hash-object` 与 SHA-256；四份规格均与[决定首版基线如何处理初始快照后的替代性需求](84-decide-first-baseline-treatment-of-post-snapshot-superseding-requirements.md)绑定身份完全一致，漂移为 0：

- `.scratch/new-mes-ingest/spec.md`：blob `9104575426c60f71ed8020d3d231c3332e2c0589`，SHA-256 `bca9c428b2ece1db6a672619b1fd78ba7391f0bd42ee07c27cdd56670d3c9f6f`。
- `.scratch/mes-ingest-bounded-storage-low-memory/spec.md`：blob `099feeef433a0b356c41c90e221ee7d5bafcface`，SHA-256 `23a096283e3ec0c478b588f8881c01eb1d228aebd250758eed9725601deda1e6`。
- `.scratch/mes-ingest-watch-area-live-sync/spec.md`：blob `c6050a6102abc6b24f330187af7010fad15736b4`，SHA-256 `8466e81a262ff76fe8c7e28bc9df65aad884520066411f796cb409078488a4a0`。
- `.scratch/demand-series-inspector-e/spec.md`：blob `2b4a2b326a3df2635e56977b22feb8686d0c0cca`，SHA-256 `c0f2274ee14e07d1b84535933b7c01a43b6bbd98f3f17891022db59cdf663657`。

因此无需生成漂移差异或重新批准入口；以后任一字节变化都会使生成器以非零状态退出，变化字节不得继承本次批准。

### 来源层叠与分流结论

- 已把《新版 MesIngest 整体替换规格书》登记为基础当前来源；有界存储规格只覆盖 GONE/错误历史、原始证据保留、恢复、容量和低内存存储边界；AREA 实时同步规格只覆盖 `AreaFilterProfile`；Inspector E 只覆盖 DemandSeries 详情信息架构；[回流并核对 MesIngestWatch V2 运维定义](81-reconcile-mes-ingest-watch-v2-operability-definitions.md)只携带已明确核对的跨版本一致边界。
- 上述关系已逐层记录为 **PreBaselineSourceSupersession**；旧 Phase 1、旧 V2、旧数据库/契约/Watch/`IngestAlert` 语义及其它历史实现记录保持历史身份，不创建虚构的旧永久 REQ。
- 补充窗口还发现 `mes/queries/mes-task-union/README.md` 是初始快照后变化且尚未绑定批准的第五份规范候选。补拍不批准它；其来源、当前适用性以及首版去留须在独立 HITL 票中决定。
- 补充快照截止时间之后新增或变化的需求性材料，不得静默进入冻结的 `v1.0.0` 候选；最终批准前必须显式重开补充快照并重验差异与绑定批准，否则进入正式发布后的后续版本变更门禁。

### Assets

- [补充快照说明](../evidence/pre-release-supplemental-snapshot/snapshot.md)
- [逐文件补充证据清单](../evidence/pre-release-supplemental-snapshot/supplemental-evidence-manifest.tsv) — SHA-256 `8e1e4636cd30983ad8968cd2d9d5265abfa6bda00c3bddabbccf06c5c20c261a`
- [四份获批来源身份核验](../evidence/pre-release-supplemental-snapshot/approved-source-validation.tsv) — SHA-256 `90ba9cc8de553e36037394d929c946493705a011f4e55247dddd8ff8ad287d3e`
- [首版前来源替代清单](../evidence/pre-release-supplemental-snapshot/pre-baseline-source-supersession.tsv) — SHA-256 `74ba5dc652fc798edf7bd0004ac43fa3b71538bcf711b5bc381c2cafceafb977`
- [原始工作区状态](../evidence/pre-release-supplemental-snapshot/worktree-status.txt)
- [发现错误记录](../evidence/pre-release-supplemental-snapshot/discovery-errors.txt)
- [可重复采集与核验脚本](../evidence/pre-release-supplemental-snapshot/capture-and-verify.ps1) — SHA-256 `649bc17d334109c42712f77b6cf42444b21632a84405df0edea5de523227394a`
