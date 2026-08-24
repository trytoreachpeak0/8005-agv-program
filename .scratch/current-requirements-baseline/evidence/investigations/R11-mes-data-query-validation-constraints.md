# R11 MES 数据、查询与工厂验证约束调查

## 范围、口径与结论

本报告只调查无损清单 `batch_id=R11` 的 11 份材料：1 个离线分析入口、1 个查询目录、1 份工厂首轮清单、4 份查询契约、1 个 MES 总入口、1 份可执行容量表、1 份容量表生成视图、1 份参考数据说明。清单原始记录见 `.scratch/current-requirements-baseline/evidence/material-inventory/material-inventory.tsv:201-205,303-310`，批次角色统计为 `candidate-acceptance=1`、`candidate-data-constraint=9`、`template-or-index=1`（`.scratch/current-requirements-baseline/evidence/material-inventory/batches.md:47`）。

逐文件重算 SHA-256 后与固定清单 **11/11 一致**；调查时对 11 条路径执行 `git status --short` 均无输出。批准判断遵循当前基线规则：权威需求必须同时绑定**具名授权人、可核查日期、适用范围、具体版本/哈希或等价记录**，文件位置、实现、措辞和表面合理性均不能赋予权威性（`.scratch/current-requirements-baseline/issues/01-authority-and-classification-evidence-rules.md:13-22`）；同一文档中的原子条目还须分别记录来源链和确认状态（`.scratch/current-requirements-baseline/issues/04-atomic-requirement-approval-granularity.md:13-19`）。

结论：

- **当前需求基线可批准项：0/11。** 11 份材料都没有同时给出具名授权人、授权日期、批准范围和所批准版本。Git 作者 Zhengyu Shao 只证明提交主体；`source=客户提供`、`status=active`、勾选 `[x]`、查询元数据 `requires_approval=false` 和 run `status=completed` 均不是批准记录。
- **外部数据约束候选主要有三组：** 客户 SQL 快照所指向的表/视图、绑定参数、输出字段和筛选；PACKAGE→单篮最大料盒数的 28 条映射；特定工厂 Oracle 环境中观察到的字段、行数和耗时。前两组仍缺具名客户来源与版本批准；第三组只是限定环境现状。
- **验收条件候选集中在工厂清单和查询失败语义。** 7 字段、六分支计数差异为 0、无硬失败、10 轮平均 ≤5 秒/最大 ≤10 秒等是可独立判断的候选；工厂清单中的勾选和值只能证明清单作者记录了结果，须回到 run 证据核验，也不能自动批准阈值本身。
- **派生查询/应用设计必须与外部约束拆开。** `MES_TASK_UNION` 的统一 7 列、`UNION ALL`、幂等硬失败；`SUBLOT_BOX_COUNT` 失败时阻止装载；操作员无结果不建会话；Schema 字典查询的固定输出；容量 exact/prefix 匹配，均含仓库内整合或产品策略。客户源快照可支持追溯，不能证明客户逐条批准了这些派生语义。
- **索引/生成视图不形成独立要求。** `mes/README.md` 和 `mes/catalog/queries.md` 是导航与 SSOT 规则；`package-basket-capacity.md` 是 CSV 的生成视图；`mes/analysis/README.md` 是工具接口说明。它们可定位材料，不能把被指向材料升级为权威需求。
- **三份 2026-07-24 run 只能证明特定环境现状。** manifest 固定了 `MES_TASK_UNION` SQL 哈希、Windows Server、Python 与 Oracle 驱动模式并记录实际行数/耗时，但 `recorded_by` 和 `recorded_at` 仍是占位符（例如 `mes/evidence/runs/run-20260724T065719Z-61b2cebcf4/run-manifest.json:2-8,26-35,57-71`）。这些 run 不证明其他 Schema、账号、数据库版本、数据时点或未来查询版本，也不批准业务需求。

## Git 状态勘误与版本形成史

### 工厂首轮清单按 `tracked-clean` 追踪

原始无损清单把 `mes/docs/工厂首轮执行与回传清单.md` 记为 `untracked`（`material-inventory.tsv:205`）。追加勘误证明这是 `core.quotepath=true` 导致 Unicode 路径比对失败的假阳性：该路径存在于固定 HEAD `1469d6309d00b0abb792f6cd686aed68286e638e`，捕获字节与固定 HEAD blob 一致，R11 的 1 条受影响路径必须由 `untracked` 覆盖为 `tracked-clean`（`.scratch/current-requirements-baseline/evidence/initial-snapshot/git-status-correction.md:3-24,28-41`）。逐路径覆盖记录给出的 fixed HEAD blob 为 `6a34c12941d468dd3332a08751c571e50dff38eb`；本次重算工作树 SHA-256 为 `8305057b...47fa`，与清单一致。勘误只恢复 Git 身份，不改变内容角色、哈希、批准状态或权威等级。

对该文件执行 `git log --follow --find-renames=50%` 得到两段可追踪历史：

1. `5718541aa0588389ee6e7f93f422d14badffc45f`，2026-07-16 22:04:27 +08:00，作者 Zhengyu Shao：新建五分支、全未勾选的首次验证清单，要求客户 IT 批准文件、bundle/回传哈希及外置配置。
2. `ffe1f49e70ade8a9e2e2ef74fc922e5ce7c8917c`，2026-07-27 08:19:02 +08:00，作者 Zhengyu Shao：改为六分支，删除必需的客户批准文件和传输 SHA-256，全部回填为 `[x]`，写入三次 run、673/672 行、六分支差异 0、平均 2.91 秒/最大 3.50 秒及 PACKAGE 未覆盖统计。

这段历史证明当前清单是“执行计划 + 结果回填”的混合文档，并发生过实质授权/证据规则变化；它不证明谁授权删除批准文件与哈希要求，也不证明提交作者拥有客户 IT 或验收批准权限。

### 其余 10 份材料

- 11 份材料都在 `5718541` 形成或迁入当前结构。
- `mes/catalog/queries.md` 与 `mes/queries/mes-task-union/README.md` 在 `ffe1f49` 增加第六类 `WIRE_TO_NITROGEN`；前者同时把 Schema 核验范围从“五类”改为一般运输任务，后者把五类契约改成六类。
- `mes/queries/schema-introspection/README.md` 与 `mes/queries/sublot-box-count/README.md` 在 `493ac5a89cb89daf1f8c090ef6091b8d006180be`（2026-07-31）实质修改：前者从五类改为六类；后者把“查询失败回退现场扫码”改为“失败/非正数/容量不唯一时阻止装载且不得回退”。后者是可观察业务行为变化，不能只按文件首次形成日判断版本。
- `mes/analysis/README.md`、`mes/queries/operator-identity/README.md`、`mes/README.md` 和三份 reference 材料只有 `5718541` 一条文件历史。其“2026-07-16 迁移快照”是文档自述；仓库内没有附上原始客户花篮表、具名交付记录或逐行转换清单来独立证明无损迁移。

## 一手来源、批准与环境核验

### 查询来源链

- `MES_TASK_UNION` 指向 2026-07-16 五类和 2026-07-24 第六类客户 SQL 快照；两份来源说明都把其用途限定为差异比较、需求研究和实验基线，明确不得作为生产运行时依赖或回退副本（`mes/sources/customer/2026-07-16/mes-task-original-queries/README.md:3-17`；`mes/sources/customer/2026-07-24/mes-task-original-queries/README.md:3-17`）。它们没有具名客户提供人、接收时间记录、客户批准范围或客户批准的 SQL 哈希。
- `OP_OPERATOR_IDENTITY` 和 `SUBLOT_BOX_COUNT` 的来源说明称其来自客户提供、接口确认文档及旧 SQL，并把 2026-07-16 `query.sql` 定义为来源快照（`mes/sources/customer/2026-07-16/operator-identity/README.md:3-11`；`mes/sources/customer/2026-07-16/sublot-box-count/README.md:3-11`）。正式 SQL 与来源 SQL 的可执行语句相同，但注释已由“五类”更新为“六类”，所以应视为可追踪派生版本，而非未经证明的客户原稿原样执行。
- `MES_SCHEMA_INTROSPECTION` 没有客户 SQL 原稿；目录明确称其为仓库内部编制（`mes/catalog/queries.md:10`）。因此其查询形状是本地核验设计；未来取得的 Oracle 字典结果才是限定环境的外部事实。
- 接口确认文档只概括称“客户 IT 提供并批准查询对象、业务筛选条件和生产执行窗口”（`mes/docs/宿迁长电AGV项目MES数据接口需求确认.md:5-10`），但同文档仍把 7 字段查询最终版本/执行计划/客户批准列为待确认（`:166-174`），且要求现场执行先取得所需批准、保存哈希（`:186-194`）。该概括不能替代批准四要素。

查询 catalog 当前仍把四个 QUERY_ID 的“最后证据”写为“尚未迁入”，并明确这不表示已通过或未通过现场验证（`mes/catalog/queries.md:5-12`）。仓库实际已有三份 `mes/evidence/runs/run-20260724...`，所以 catalog 可作 QUERY_ID/来源索引，**不能作为完整证据索引或验证状态结论**。

### PACKAGE 容量来源链

`mes/reference/package-basket-capacity.csv:1-29` 含 28 条 active 规则：27 条 exact、1 条 `TOLL-` prefix；机械核验未发现重复 pattern、非正容量或非法 match type。每行 source 都只写“客户提供花篮容量对照表（2026-07-16迁移）”。`mes/reference/README.md:3-5` 同样称其为客户对照表迁移快照，`:16-26` 则定义 exact 优先、最长 prefix、区分大小写和禁止模糊推断。

现有材料没有：原始对照表文件/哈希、具名提供人与授权身份、交付/批准日期、适用厂区/产品/车型/生效期、28 条逐行转换对账或变更记录。尤其 `TOLL-` 被表达为 prefix，而其余 27 条为 exact；在原表缺失时不能证明“前缀”是客户原意还是迁移解释。当前活跃样本只有 120 个去重 PACKAGE，672 行中 494 行未匹配（`mes/samples/mes-task-union/package-coverage/summary.md:5-12`），所以 28 条表不能被称为工厂 PACKAGE 全集；接口确认文档也仍把完整覆盖与 `TOLL-` 边界列为待确认（`mes/docs/宿迁长电AGV项目MES数据接口需求确认.md:176-185`）。

`package-basket-capacity.md` 自述由 CSV 自动生成且不可手工编辑（`:1-5`），28 条数据行与 CSV 当前一致；它是审阅视图，不是第二个规则源，也不能得到独立批准。`mes/analysis/README.md:23-39` 定义的覆盖分析只是离线工具：输入是已有 `MES_TASK_UNION.csv`，输出匹配/未匹配报告；分析结果能证明某个输入快照对当前规则的覆盖率，不能发现全量 PACKAGE 或批准容量值。

### 工厂 run 能证明什么

清单写入的三个 run 均可在仓库核验：

- phase1 `run-20260724T065719Z-61b2cebcf4`：manifest 记录 SQL SHA-256 `54a140ad...39ae`、673 行、2.933 秒和 completed（`run-manifest.json:36-47,57-72`）；质量报告记录 7 字段相关空值为 0、硬失败为否、重复键/跨任务冲突为 0，但 673 个 DATES 全部“无法解析”，并出现短 AREA `N`（`reports/mes-task-union-quality.md:3-19`）。清单把日期问题称为不影响硬失败，这只是当前报告逻辑/解释，不是客户批准的日期口径。
- compare `run-20260724T065734Z-7342006d71`：同一合并 SQL 返回 672 行；六个来源分支分别在之后执行，六类 count difference 均为 0（`reports/customer-baseline-counts.csv:1-7`）。来源 README 已警告分支与合并查询不是同一时刻快照，因此 count 相等只支持该次近时点观察，不能证明逐行永久等价或同一快照语义。
- performance `run-20260724T065749Z-c9b74a48bb`：10 轮均 672 行，平均 2.9137194 秒、最大 3.49858 秒，满足报告中两个目标（`reports/mes-task-union-performance.json:1-7`）。它只验证该次环境和 SQL 哈希，不能批准 5/10 秒阈值，也不能外推数据库负载变化后的性能。

三份 manifest 的环境均记录 Windows Server 2016、Python 3.14.6、`python-oracledb 4.0.1`、thick mode（例如 phase1 `run-manifest.json:26-35`），但未固定 Oracle 数据库版本、数据库/实例身份、Schema、只读账号权限范围、数据库时区或执行窗口批准。`approval`/`experiment_record` 中 `recorded_by="<你的名字>"`、`recorded_at="<ISO8601 时间>"` 仍为模板值，`status=self-run`（`:2-8,49-55`）；所以三份 run 的具名批准证据为 **0/3**。

### 批准与完整性规则存在冲突

当前工厂清单明确“不再要求客户批准文件”且“不必校验 SHA-256”（`mes/docs/工厂首轮执行与回传清单.md:3-8`），当前实验计划也说数据库/Schema/账号/执行窗口由执行人自行确认、不再要求客户批准文件（`mes/experiments/definitions/mes-task-union-validation/plan.md:28-33`）。但同一计划仍把 catalog 批准版本/哈希和客户批准六分支列为输入（`:21-26`），接口确认文档则要求先取得批准并保存每个文件 SHA-256（`mes/docs/宿迁长电AGV项目MES数据接口需求确认.md:186-194`）。

必须把两个问题分开：

1. 某个只读实验是否可由现场执行人自行授权，是运行/安全授权问题；
2. 查询契约、业务筛选、性能阈值和容量表能否进入当前需求基线，是需求批准问题。

即使前者决定“不需要客户批准文件”，也不能自动回答后者。当前材料还没有具名决策人说明哪条证据规则被替代、替代日期/范围/版本为何；这是后续应建立 HITL 裁决的真实治理冲突，本报告不自行排序，也不恢复旧规则或批准新规则。

## 逐文件调查台账

分类代码：`X` = 外部数据约束候选；`A` = 验收/可观察业务条件候选；`D` = 派生查询或应用设计；`I` = 索引/生成视图；`E` = 只证明限定现状的证据入口。一个文件可同时具有多个角色。以下 11 项批准四要素均不齐全，批准范围均为空。

| 文件、固定身份与历史 | 来源/版本/适用环境 | 分类与当前项目范围 |
| --- | --- | --- |
| `mes/analysis/README.md:1-47`<br>SHA `dfcf58e4228083b811eb9670e0e897efb3f648ec93581645892a1d254a7bf4a7`<br>`5718541` 形成 | 仓库内 Python 标准库离线分析入口；要求输入含 PACKAGE，输出四种覆盖报告。无客户来源、版本批准或运行环境绑定。 | `D/E`：只服务当前项目的离线 PACKAGE 覆盖与规则生成；不是 MES 在线契约，不证明容量正确或 PACKAGE 全集。 |
| `mes/catalog/queries.md:1-12`<br>SHA `1a52a46a3fd689c74a3cf481897d824ac2eb64277500b1e7fb99fec36ee4be80`<br>`5718541` 形成，`ffe1f49` 加第六类 | 汇总四个 QUERY_ID、参数、输出和客户快照入口；“最后证据”字段已落后于当前 run。 | `I`：当前仓库查询导航/SSOT 索引；不形成独立外部约束，也不证明验证状态。 |
| `mes/docs/工厂首轮执行与回传清单.md:1-117`<br>SHA `8305057b5f665d02b4891d88d3cf66afcc9b9f141757a19f7339c35bc91447fa`<br>原记 untracked，勘误后 tracked-clean；`5718541` 初版，`ffe1f49` 实测回填版 | 本机准备 + 工厂 Windows/Oracle thick 执行 + 本机导入；覆盖六类、7 字段、质量、六分支 count、10 轮性能和 PACKAGE 活跃覆盖。批准/哈希要求在第二版被移除且无替代决定证据。 | `A/E`：候选验收条件与 2026-07-24 三次 run 摘要混合；只适用于该 SQL/环境/数据时点。全量 PACKAGE 明确未完成（`:109-117`）。不能把 `[x]` 批量批准为基线。 |
| `mes/queries/mes-task-union/README.md:1-20`<br>SHA `e8b7ed1c34d7d541f2833fc66a34a361c3ba818fa9b6df0daf36e93268d255f0`<br>`5718541` 五类，`ffe1f49` 六类 | 来源为 7/16 五分支、7/24 第六分支快照；正式运行环境是 Oracle 单语句只读查询。未绑定客户批准 SQL 哈希/Schema/版本。 | `X/D/A`：表/字段/筛选及六类候选属外部约束；统一 7 列、UNION ALL、应用幂等硬失败和过滤分层属派生设计/业务条件。适用于当前项目六类运输接入，不适用于 PACKAGE 全集、历史事件流或其他查询。 |
| `mes/queries/operator-identity/README.md:1-15`<br>SHA `6a99258034b5be9d85d064258c896a709de30f49ac86e893917d83be814abcdc`<br>`5718541` 形成 | 7/16 客户来源快照指向 `mv_fw_username.usercode/username`；正式 Oracle 只读绑定查询。未见脱敏实验 run 或具名批准。 | `X/D/A`：参数/字段候选为外部数据契约；无结果不建会话、仅解析身份不声明岗位权限是当前产品边界。适用操作员身份/审计，不可扩张为岗位授权。 |
| `mes/queries/schema-introspection/README.md:1-14`<br>SHA `a3ae14c569b25bddacfbc46819733ad024ffa1826b30c138ad34a48634efdc31`<br>`5718541` 五类，`493ac5a` 六类 | 仓库内部编制的 Oracle 字典只读查询，无客户原稿；当前 catalog 没有迁入证据。 | `D/E`：固定字段字典输出和未找到保留行是核验设计；实际执行结果才是某用户/Schema/时区的现状。不能用声明长度替代业务值范围，也不能用样本最大值缩短模型；高负载实际最大值扫描不在本查询范围。 |
| `mes/queries/sublot-box-count/README.md:1-15`<br>SHA `486802d634605a446aedd46e6f14b5ca77dd2b17b458dc640c64e98fd7ea9be2`<br>`5718541` 形成，`493ac5a` 改失败语义 | 7/16 客户来源快照指向 `fw_wip_box_his.lot/box/step`；正式 Oracle 绑定只读查询。未见独立脱敏 run 或批准版本。 | `X/D/A`：MAX_BOX_COUNT 查询候选为外部数据契约；结合冻结 PACKAGE 计算 ExpectedBasketCount、失败阻止分配/开锁且不回退，是 7/31 派生业务行为。仅用于操作员输入 SUBLOT 后的 V1 装载，不参与六类轮询或取消运输任务。 |
| `mes/README.md:1-51`<br>SHA `63d550a52f0aea953183ce4c3b5301ca533e42ab4fd07714a7918916379e1f0f`<br>`5718541` 形成 | 定义 docs/queries/sources/experiments/evidence/samples/reference/tools 分层、QUERY_ID 和 SQL SSOT。 | `I`：当前仓库 MES 资料与运行入口治理；不是客户需求。它要求回传导入后才能声称现场通过（`:40-42`），但不提供批准主体或具体证据版本。 |
| `mes/reference/package-basket-capacity.csv:1-29`<br>SHA `3214f6e849861de452c4132f0f733f20f657a9149dd05953ccc956deab766ece`<br>`5718541` 形成 | 自述为客户表 2026-07-16 迁移；28 条 active 规则。缺原表、提供人、厂区/产品/生效期、转换对账和批准哈希。运行环境是本地 ExpectedBasketCount/离线覆盖，不直接查询 MES。 | `X/A`：28 个容量值和 TOLL- 前缀是外部数据候选；匹配失败必须停止装载是另一个验收/业务条件。当前覆盖不完整，禁止称全集或擅自补值。CSV 是唯一可执行规则源。 |
| `mes/reference/package-basket-capacity.md:1-37`<br>SHA `af7b8c13b0371877bebd9f4e08eb695be1b6b2c9b9000c5836cf1a719a0ac586`<br>`5718541` 形成 | 由上述 CSV 自动生成的 28 行审阅视图，内容来源完全从属于 CSV。 | `I`：重复/派生视图，不独立批准、不作为运行时规则源；引用时应绑定 CSV 哈希。 |
| `mes/reference/README.md:1-43`<br>SHA `8860a80469bd0fb97f91112b7339199fa50b74243768ee4015c92a0479185f5c`<br>`5718541` 形成 | 仓库内参考数据 schema、exact/prefix 算法和生成流程说明；来源仍只有“客户对照表迁移”概括。 | `D/A/I`：匹配算法、禁止模糊推断和 CSV SSOT 是派生执行/安全护栏；适用于当前项目 V1 PACKAGE 容量换算。它不能证明 28 个值或 `TOLL-` 边界已获客户批准。 |

## 待拆分的原子候选

后续不应整份批准任何 R11 文件，至少拆成以下独立条目：

1. `MES_TASK_UNION` 六个 TASK_TYPE 各自的客户对象、筛选条件和业务含义；统一 7 列与字段类型/时区；使用 `UNION ALL` 和语句级一致性快照。
2. `TASK_TYPE+SUBLOT` 重复键、跨任务冲突、关卡/三光互斥、EQP/DATES/PACKAGE/AREA 空值与异常各自的阻断级别；不要把质量报告当前“硬失败”实现当批准。
3. 轮询/实验的只读、顺序、轮间 10 秒、5/10/30 秒阈值、连续失败停止与适用数据库负载范围；实验执行授权和需求验收阈值分别批准。
4. `SUBLOT_BOX_COUNT` 的表字段、MAX 统计口径、空/非正/超时语义；ExpectedBasketCount 计算、冻结 PACKAGE、失败禁止分配/开锁、禁止现场数量回退。
5. `OP_OPERATOR_IDENTITY` 的工号/姓名字段、无结果/重复/超时处理、隐私脱敏和“身份解析不等于岗位授权”。
6. Schema 核验的必需对象/字段清单、声明长度/精度/可空性、目标数据库/Schema/用户/时区；把内部查询形状与现场发现结果分开。
7. 28 条 PACKAGE 容量逐条值、exact/prefix 类型、适用产品/厂区/生效期和 `TOLL-` 边界；未覆盖项的责任人、补表流程和版本变更治理。
8. 工厂验收证据包的强制内容、传输完整性、批准/自运行记录、脱敏、导入和签字规则；明确 7/16 版批准+哈希要求是否被 7/27 版正式替代。

## 后续证据请求

1. 客户 IT/业务方提供每个正式 QUERY_ID 的具名批准人及授权身份、批准日期、适用厂区/Oracle 实例/Schema/账号权限/执行窗口，以及绑定 `query.sql` SHA-256 或 Git commit；`requires_approval=false` 只能解释 runner 行为，不能替代此记录。
2. 补齐六个客户分支原稿的交付记录和哈希，说明第六类何时生效；把正式合并 SQL 与六个源分支做可审计语义差异，而不只比较单次 count。
3. 提供 PACKAGE 原始客户对照表及哈希、具名提供/批准人、逐行迁移对账和版本变更记录；逐条确认 27 exact、1 prefix，尤其 `TOLL-` 的字面边界，并明确当前 100 个未匹配 PACKAGE 的补表责任与期限。
4. 为三份 run 补真实 `recorded_by`、`recorded_at`、执行授权记录、Oracle DB 版本/实例/Schema/时区/账号权限范围和执行窗口；保留原 run 不覆盖，采用追加证明或新 run。
5. 对“无需批准文件/无需传输 SHA-256”与“必须批准/保存哈希”的冲突建立 HITL 票，由具名安全/客户 IT/项目验收责任人决定适用范围、替代关系和生效版本；不要由本次调查自行选择。
6. catalog 的“最后证据”应在后续治理工作中绑定具体 run_id、查询 SQL 哈希和结论范围；本报告不修改 catalog。为 `OP_OPERATOR_IDENTITY`、`SUBLOT_BOX_COUNT`、`MES_SCHEMA_INTROSPECTION` 分别补独立只读实验与脱敏证据，避免用 `MES_TASK_UNION` run 代证。
7. 最终基线只收入经人工确认的原子条目；run、样本、生成视图、测试和当前实现继续作为验证附件，不反向赋予需求权威性。
