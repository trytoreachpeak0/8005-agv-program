# 调研：清洗间送焊线、氮气柜送焊线/键合在 MES 数据与现场地图上的实际形态

- 票据：trytoreachpeak0/8005-agv-program#66（地图 #64）
- 调研日期：2026-09-14；方式：只读仓库内既有证据，离线，未访问工厂 MES、RIoT 或任何服务
- 本文只陈述事实与可追溯的推论，**不做产品决定**

## 引用版本

| 标记 | 仓库 | 引用点 |
| --- | --- | --- |
| **[A]** | `8005-agv-program` | `origin/main` = `d0eaf5d5` |
| **[M]** | `8005-mes-ingest` | `origin/main` = `acc6bad` |
| **[D]** | `8005-agv-program` | `e33c208^`（`requirement-documents/简易需求文档.md` 被删除前一版；删除提交 `e33c208`，2026-09-01，"drop the superseded draft requirements"；首次加入 `dbc541a`，2026-07-13） |
| **[C]** | `8005-agv-program` | `7abf7cb5`（2026-07-27） |

凡写「本调研统计」的数字，都是对所引文件按列计数得到的，不是文件里原有的数字。
标「推论」的段落是从 SQL 字面条件推出来的，没有 MES 数据验证。

## 结论速览

1. **SQL 条件层面，六类里没有任何一类显式捞取「清洗完工」或「氮气柜出柜」。**唯一有可能在不知情时顺带捞到这两段行的是 `STAGING_TO_WIRE`：它的条件不限制产品当前在哪（只看 `step IN ('焊线','键合') AND task='入站'`），输出里也没有取货位置列。两段流程的 MES 行是否会落进这个条件，取决于 MES 怎么表示这两段流转，仓库里查不到。
2. **「氮气柜送焊线/键合」在仓库里有两种互不相同的读法，两种读法在 SQL 上的结果相反。**
   - 读法甲：它是旧稿 5.2.2「装片完工送焊线氮气柜」的回程。5.2.2 的 MES 条件与 `DIE_TO_WIRE_STAGING` 逐字相同，所以这段回程在结构上就是 `STAGING_TO_WIRE`。
   - 读法乙：它是 `WIRE_TO_NITROGEN` 入柜后再上焊线2的那一段。仓库里「由 `STAGING_TO_WIRE` 覆盖」的说法没有来源、未获批准，而且与 SQL 字面矛盾：`STAGING_TO_WIRE` 只认 `焊线`/`键合`，不含 `焊线2`。
3. **旧稿 5.2.5、5.2.6 没有进入六类，不是某张票决议排除的，而是「IT 从未提供 SQL + 旧稿被整体退役」造成的缺席。**票 13 决议、`CONTEXT.md`、需求基线 v1.1.0 都没有出现「清洗」。
4. **mapId 25 上既没有清洗间，也没有氮气柜或派工待送区。**206 个站点 = N/T 前缀的机台命名站点 + 1 个 `关卡`。「派工待送区」与「焊线氮气柜」是否同一物理点，仓库里的命名沿革指向「可能是」，但需求基线 REQ-0334 把二者建模为不能共站的两个功能。地图上两者都没有，无从核对。

---

## 问题 1：旧 SQL 与现行六类 SQL 的条件对照

### 1.1 旧 SQL 快照里与这两个流程有关的文件

- 旧程序 SQL 快照是研究用原样快照，不是正式查询（[A] `mes/sources/legacy-program-sql/2026-07-16/README.md:3`）。
- **清洗间**：只有一个文件 `清洗间送焊线.txt`，一行 SQL，登记为 `supporting` 类（[A] `mes/sources/legacy-program-sql/2026-07-16/source-manifest.json:5-7`），不在 20 条 SQL 的静态分类表里（[A] `.../catalog.csv:2-21` 只列 `.sql` 文件）。
  - 仓库盘点记录的文件时间是 `2026-06-23T12:10:48Z`（[A] `.scratch/current-requirements-baseline/evidence/material-inventory/material-inventory.tsv:331`）。
- **氮气柜作为取货端**：**没有任何旧 SQL。**
  - 名为 `烘箱完工送焊线氮气柜/` 的目录只有两个文件：`HKSPEC.sql`、`RecodByLoc.sql`（[A] `.../catalog.csv:2-3`）。
  - 这两个文件查的都是 `STEP LIKE '装片烘烤%' AND task='入站'`，也就是**送往烘箱**的批次（[A] `.../烘箱完工送焊线氮气柜/HKSPEC/HKSPEC.sql:20-22`；[A] `.../RecodByLoc/RecodByLoc.sql:18-20`），不是从氮气柜取货。
  - 目录名与内容不符。
- mes-ingest 的旧 SQL 研究计划只笼统提到要研究「旧程序曾如何判断……氮气柜……任务」（[M] `experiments/definitions/legacy-program-sql-research/plan.md:11`），没有给出结论。

### 1.2 `清洗间送焊线.txt` 的取数条件

原文见 [A] `mes/sources/legacy-program-sql/2026-07-16/清洗间送焊线.txt:1`，逐项拆开如下：

| 项 | 原文条件 | 说明 |
| --- | --- | --- |
| 数据源 | `v_irobot_info A inner join v_irobot_info B on A.PRDLOT=B.PRDLOT` | 自连接，同一批号的两条记录 |
| 起点事件 | `A.step='清洗完工'` | 输出 `CONCAT('QX',A.EQPID)`，即「QX + 清洗设备号」 |
| 终点事件 | `B.step='焊线派工'` | 输出 `B.EQPID`、`B.LOCID`，即派工的焊线设备与位置 |
| 终点位置白名单 | `substr(B.LOCID,1,3) in ('A1-',…,'A19','B20','B21')` | 只保留 A1～A19、B20、B21 |
| 时间 | `A.DATES > to_date('06/23/2026 09:01:58','YYYY/MM/DD HH24:MI')` | 写死的日期；日期串是 `MM/DD/YYYY HH:MI:SS`，格式模板却是 `YYYY/MM/DD HH24:MI`，两者不一致（未执行验证） |

补充事实：

- `v_irobot_info` 在两个仓库中**只出现在这一个文件里**（本调研对 [A]、[M] 全库检索 `irobot`）。
- `清洗完工`、`焊线派工` 这两个 step 值同样只在这个文件里出现。

### 1.3 现行六类的条件（[M] `queries/mes-task-union/query.sql`）

| 分支 | 主表 `v_fw_wip_sublot` 条件 | 来源机台条件（`fw_eqpres_eqpinformation.step`） | 行号 |
| --- | --- | --- | --- |
| `DIE_TO_WIRE_STAGING` | `step IN ('焊线','键合')`，`task='入库'` | `='装片'` | `:13`，`:40`，`:42`，`:49` |
| `DIE_TO_OVEN` | `step IN ('装片烘烤','装片压力烘烤')`，`task='入站'` | `='装片'` | `:54`，`:81`，`:83`，`:90` |
| `WIRE_TO_GATE` | `step IN ('焊线关卡')`，`task='入库'` | `IN ('焊线','键合')` | `:95`，`:122`，`:124`，`:131` |
| `WIRE_TO_OPTICAL` | `step IN ('三光检验')`，`task='完工'` | `IN ('焊线','键合')` | `:136`，`:163`，`:165`，`:172` |
| `STAGING_TO_WIRE` | `step IN ('焊线','键合')`，`task='入站'` | **无**（`EQP` 是目标机台） | `:177`，`:189`，`:190` |
| `WIRE_TO_NITROGEN` | `step = '焊线2'`，`task='入库'` | `='焊线'` | `:196`，`:223`，`:225`，`:232` |

- 统一输出列只有 `TASK_TYPE, SUBLOT, AREA, EQP, STEP, DATES, PACKAGE`（[M] `query.sql:7`），**没有「产品当前所在位置」列**。
- 六个分支的 step 字面值合起来是：`焊线`、`键合`、`装片烘烤`、`装片压力烘烤`、`焊线关卡`、`三光检验`、`焊线2`。其中没有 `清洗…` 或任何表示出柜的值。

### 1.4 清洗间送焊线：逐条对照

| 旧条件 | 六类里有无对应 | 事实 |
| --- | --- | --- |
| 视图 `v_irobot_info` | 无 | 六类全部读 `v_fw_wip_sublot` + `fw_wip_trans`。两视图的关系在仓库中无记录。 |
| `A.step='清洗完工'` | 无 | 六类没有以清洗为来源的条件。`DIE_TO_WIRE_STAGING` 要求最后完工机台 `step='装片'`（[M] `query.sql:49`）。 |
| `B.step='焊线派工'` | 字面上无；语义上最接近 `STAGING_TO_WIRE` | `STAGING_TO_WIRE` 的 `step IN ('焊线','键合') AND task='入站'`，`EQP` 为目标机台（[M] `query.sql:189-190`）；BR-014 说它的「终点为查询结果中 EQP/AREA 映射到的指定焊线或键合机台」（[A] `requirement-documents/02-business-rules/br-014-transport-task-types-and-fixed-stations.md:34`）。 |
| `B.LOCID` 前缀 A1～B21 | 无 | 2026-07-24 的 672 行六类样本里，**没有任何 AREA 以 A 或 B 开头**（本调研统计，[A] `mes/samples/mes-task-union/latest.csv`）。旧程序说明把机台 `area` 对应到本地 `StationInfo.Loc_id`（[A] `.../通用查询/GetMESLocIDByEQP/GetMESLocIDByEQP.md:30`），但这是旧程序本地表，不能证明 `v_irobot_info.LOCID` 与 MES `AREA` 同义。 |

**推论（未验证）：**

- 如果清洗完工的批次被派往焊线机台时，在 `v_fw_wip_sublot` 里表现为 `step='焊线'`、`task='入站'`，它会被 `STAGING_TO_WIRE` 捞到。
  - 原因：该分支不限制来源，输出也无位置列（[M] `query.sql:7`，`:177-190`）。
  - 这时系统会按规则把取货端当成「派工待送区」固定站（[A] `br-014-transport-task-types-and-fixed-stations.md:34`），而产品实际在清洗架上。
- 如果清洗设备在 `fw_eqpres_eqpinformation` 里的 `step` 不是 `装片`，清洗完工后**不会**生成 `DIE_TO_WIRE_STAGING` 行（[M] `query.sql:49`）。
- 上面两个「如果」，仓库都给不出答案。

**样本侧事实：**

- 2026-07-24 那次 10 轮执行在 2 分钟内完成（[M] `evidence/runs/run-20260724T065749Z-c9b74a48bb/execution-log.md:3`，`:29`）。
- 每轮 672 行（[M] 同文件 `:8`，`:26`；[A] `mes/samples/mes-task-union/latest.meta.json:9-11`）。
- `STEP` 列只出现 `装片烘烤`、`装片压力烘烤`、`焊线`、`焊线关卡`、`焊线2`、`三光检验` 六个值（本调研统计），**没有清洗相关 step**。这与 SQL 条件本身一致，所以不能据此判断清洗批次是否混在 `STAGING_TO_WIRE` 里。

### 1.5 氮气柜送焊线/键合：逐条对照

仓库里「氮气柜 → 机台」有两种读法，下面分别对照。

**读法甲：5.2.6 是 5.2.2「装片完工送焊线氮气柜」的回程**

- 旧稿 5.2.2 的触发条件是：「MES 中 `step` 为「焊线」或「键合」、`task='入库'` 且未关闭」，起点装片设备，终点焊线氮气柜（[D] `requirement-documents/简易需求文档.md:96`，`:17`）。
  - 这与 `DIE_TO_WIRE_STAGING` 的条件逐字相同：`step IN ('焊线','键合')`、`task='入库'`、来源 `装片`（[M] `query.sql:40`，`:42`，`:49`）。
  - 客户 IT 该分支原稿的注释只写「装片完工送焊线键合的产品」，没有写终点名（[A] `mes/sources/customer/2026-07-16/mes-task-original-queries/01_DIE_TO_WIRE_STAGING.sql:1`）。
  - 现行文档把这条的终点称为「焊线/键合派工待送区」（[A] `requirement-documents/07-customer-deliverables/客户需求讨论稿-多仓位AGV系统.md:104`）。
- 旧稿 5.2.6「焊线区氮气柜 → 焊线/键合机台」（[D] `简易需求文档.md:21`，`:147-158`）与 `STAGING_TO_WIRE`「派工待送区 → 指定焊线/键合机台」在结构上一一对应。后者条件为 `step IN ('焊线','键合') AND task='入站'`（[M] `query.sql:189-190`）。
- **在这个读法下，5.2.6 的 MES 行就是 `STAGING_TO_WIRE` 的行。**现行模型只是把取货端记成「派工待送」功能而不是「氮气柜」功能。
- 样本里 `STAGING_TO_WIRE` 有 246 行，`STEP` 全部是 `焊线`，没有 `键合`；`DIE_TO_WIRE_STAGING` 的 105 行也全部是 `焊线`（本调研统计，[A] `mes/samples/mes-task-union/latest.csv`）。

**读法乙：「氮气柜」是 `WIRE_TO_NITROGEN` 的终点，出柜后再上焊线2**

- `CONTEXT.md` 的原话：「PDA 扫码入柜后该行从 MES 快照消失；之后再上 WireBond2 由既有 `STAGING_TO_WIRE` 覆盖，不另建任务类型」（[A] `CONTEXT.md:1659`）。同样的话还出现在：
  - [A] `mes/docs/AGV系统业务与MES任务模型.md:132`
  - [A] `mes/docs/宿迁长电AGV项目MES数据接口需求确认.md:40`
  - [A] `requirement-documents/02-business-rules/br-014-transport-task-types-and-fixed-stations.md:35`
- **这句话与 SQL 字面矛盾：**
  - `CONTEXT.md` 自己定义「WireBond2……MES 的 step 名就是 `焊线2`」（[A] `CONTEXT.md:1651`），「WireBond1……MES 机台侧 step 名为 `焊线`（不是 `焊线1`）」（[A] `CONTEXT.md:1647`）。
  - `WIRE_TO_NITROGEN` 按 `step='焊线2' AND task='入库'` 捞「等待焊线2」的批次（[M] `query.sql:223`，`:225`）。
  - `STAGING_TO_WIRE` 只认 `step IN ('焊线','键合')`（[M] `query.sql:189`），**不含 `焊线2`**。
  - **推论（未验证）**：前三类分支的共同模式是「主表 `step` = 批次排队等待的下一工序」。照此类推，派往焊线2 机台的批次应表现为 `step='焊线2'`、`task='入站'`，按字面不会被 `STAGING_TO_WIRE` 捞到。
- 这句话的出处与状态：
  - 首次写入是 [C] `CONTEXT.md:140` 与 [C] `mes/docs/AGV系统业务与MES任务模型.md:132`（提交 `7abf7cb5`，2026-07-27）。
  - 需求基线的原子候选把它标为 `mixed-internal-summary; customer-source and confirmed labels remain unsupported`、`not-approved`（[A] `.scratch/current-requirements-baseline/evidence/atomic-candidates/R01-R13-consolidated-atomic-candidates.tsv:160`）。
  - **仓库里没有客户或 IT 的原文支持它。**客户 IT 的第 6 类原稿只写「PDA 入柜后本行从快照消失」，没提出柜之后怎么办（[A] `mes/sources/customer/2026-07-24/mes-task-original-queries/06_WIRE_TO_NITROGEN.sql:1-3`）。
- 样本只能说明快照当时的情况，证明不了「不存在」：
  - 10 轮、2 分钟内，`WIRE_TO_NITROGEN` 91 个 SUBLOT 与 `STAGING_TO_WIRE` 246 个 SUBLOT 交集为 0（本调研统计，[M] `evidence/runs/run-20260724T065749Z-c9b74a48bb/results/MES_TASK_UNION-round-001.csv` 至 `-010.csv`）。
  - 样本里也没有任何 `STEP='焊线2'` 的 `STAGING_TO_WIRE` 行。

**键合**

- `WIRE_TO_NITROGEN` 明确不含键合：注释见 [M] `query.sql:195`，来源机台限定 `='焊线'` 见 [M] `query.sql:232`；`CONTEXT.md` 称「仅焊线工艺有分道，键合无对等的 1/2」（[A] `CONTEXT.md:1647`）。
- 所以「氮气柜送键合」只可能对应读法甲（`STAGING_TO_WIRE` 的 `step='键合'` 部分）。按读法乙，六类里没有键合产品入氮气柜的来源行。

**附带事实（与票 13 未证明项 2 有关，不改判）**

- 票 13 决议认为 `WIRE_TO_NITROGEN` 的注释「焊线1机台」与 `WHERE step='焊线2'` 内部不一致（[A] `.scratch/8005-full-product/issues/13-answer.md:345-346`）。
- 按 `CONTEXT.md:1646-1651` 的词条，`step='焊线2'` 是「焊线1 完工后等待焊线2」的状态，来源机台 `step='焊线'` 才是焊线1。这与 `DIE_TO_WIRE_STAGING`「主表 step = 下一工序，机台 step = 完工工序」的写法一致（[M] `query.sql:40`，`:49`）。

---

## 问题 2：需求文档对 5.2.5、5.2.6 的描述，以及为什么没进六类

### 2.1 旧稿《简易需求文档》（已删除）

- 场景表（[D] `requirement-documents/简易需求文档.md:14-21`）：
  - 「清洗间送焊线机台｜存储清洗完工物料的架子 → 焊线机台｜触发：MES 中存在清洗完工送焊线任务」（`:20`）
  - 「氮气柜送焊线/键合机台｜焊线区氮气柜 → 焊线/键合机台｜触发：MES 中存在氮气柜送焊线/键合任务」（`:21`）
- 5.2.5（[D] `:134-145`）：「该场景用于清洗完工物料送焊线机台。**MES 查询条件、核验参数和回写方式需 IT 补充。**」起点为清洗完工物料架，终点为目标焊线机台。
- 5.2.6（[D] `:147-158`）：「该场景用于焊线区氮气柜中的物料送至焊线或键合机台。……**具体 MES 查询条件、核验参数和回写方式需 IT 补充。**」
- 对照：5.2.1、5.2.2 写了具体 step/task 条件和 IT 提供的 SQL 文件名（[D] `:80`，`:84`，`:96`，`:100`）；5.2.3～5.2.6 都没有。
- 旧稿的使用区域包含「烘烤间、氮气柜、AOI、清洗架」（[D] `:11`），站点配置含「清洗架」（[D] `:225`）。
- 整份旧稿在 `e33c208`（2026-09-01）以「drop the superseded draft requirements」删除。

### 2.2 `requirement-documents/user case.md`

- 角色：R-03 WIP 搬运员负责「装片完工到焊线氮气柜、氮气柜到焊线/键合机台之间的物料交接确认」，对应 5.2.2、5.2.6（[A] `requirement-documents/user case.md:11`）；R-05 清洗操作员是 5.2.5 起点（`:13`）；R-06 焊线设备操作员是 5.2.5 终点（`:14`）。
- 待确认：R-03 与 R-05 是否同一人兼任（`:21`）。整理后的版本已答复为「现场由同一批人员按班次兼任」（[A] `requirement-documents/01-stakeholders/stakeholders-and-user-classes.md:21`）。
- 用例列表：「清洗间送焊线机台：R-05 → R-06」（`:54`），「氮气柜送焊线/键合机台：R-03 → R-06/R-07」（`:55`）。
- 终点卸货用例 UC-010 注明是从这份文件的「氮气柜送焊线/键合机台」等场景拆出来的（[A] `requirement-documents/03-use-cases/01-site-operations/uc-010-unload-completed-lot-at-destination-station.md:122`）。

### 2.3 `requirement-documents/07-customer-deliverables/`

- Markdown 源稿**没有 5.2.x 编号，也没有清洗或氮气柜取货的场景**。
  - §3.4 只列六类（[A] `客户需求讨论稿-多仓位AGV系统.md:100-111`）。
  - 「清洗」只出现在角色表 R-05 一行（`:125`）。
- 残留的旧说法：R-03 仍写「装片完工到焊线氮气柜、氮气柜到焊线/键合机台之间的交接确认」（`:123`）；同一文档 §3.4 已把第 1、5 类写成「派工待送区」（`:104`，`:108`）。
- 术语表：「派工待送区｜装片完工后产品暂存的固定区域，供焊线/键合工序叫料；也是第 5 类任务的起点」（`:1344`）。
- Word 版（2026-07-14，由 pandoc 从源稿生成，[A] `07-customer-deliverables/README.md:8`）的正文是「五类任务」「四个固定区域（派工待送区、烘箱间、关卡区、三光区）」。R-03、R-05 两行与源稿相同，同样没有清洗场景（本调研解压 `word/document.xml` 检索）。
- 仓库术语表仍保留这两个场景名：
  - 「清洗间送焊线机台｜`scenarioCleaningToWire`｜场景 5.2.5」（[A] `glossary/terminology-glossary.md:124`）
  - 「氮气柜送焊线/键合机台｜`scenarioNitrogenCabinetToMachine`｜场景 5.2.6」（`:125`）
  - 「清洗间｜清洗完工物料架所在区域」（`:119`）
  - 「氮气柜｜焊线区/关卡氮气柜」（`:116`）
  - 「装片完工送焊线氮气柜｜`WIRE_BOX`」（`:77`，`:121`）

### 2.4 为什么没进六类：仓库里能找到的事实链

**仓库里没有任何一条记录明确决定「不做 5.2.5、5.2.6」。**能找到的是以下几条事实：

1. **旧稿本身把 SQL 留给 IT 补**（[D] `:136`，`:149`）。
2. **六类 SQL 都是客户 IT 提供的**，查询对象和筛选条件由 IT 批准（[A] `mes/docs/宿迁长电AGV项目MES数据接口需求确认.md:8`）。
   - 2026-07-16 归档了五类原稿（[A] `mes/sources/customer/2026-07-16/mes-task-original-queries/README.md:5`），2026-07-24 追加第六类（[A] `mes/sources/customer/2026-07-24/mes-task-original-queries/README.md:5`）。
   - 这六份原稿都没有以清洗或氮气柜为取货端的查询。
3. **2026-07-17 的待处理清单只追了第六类 SQL**：「跟进第六类任务 SQL（焊线1完工→焊线氮气柜）」「是否并入现有 UNION」。没有任何清洗相关待办（[A] `mes/docs/待处理事项清单-MES-RIOT-应用.docx`，本调研解压检索；原子候选见 [A] `.scratch/current-requirements-baseline/evidence/atomic-candidates/R01-R13-post-conflict-question-review.tsv:15-21`）。
4. **需求基线把 5.2.5、5.2.6 的「需 IT 补充」归为待解问题**：PCR-0163、PCR-0164（[A] `R01-R13-post-conflict-question-review.tsv:164-165`）。之后旧稿被整体删除（`e33c208`）。
5. **票 13 决议没有讨论清洗**（全文检索「清洗」0 次，[A] `.scratch/8005-full-product/issues/13-answer.md`）。它把五个公共站点功能当作与工厂 SQL「完全闭环，无一多余无一缺失」（`:40-41`）。
6. **`CONTEXT.md` 没有「清洗」词条。**
   - 五种公共站点功能是「派工待送、烘箱、关卡、三光和氮气柜」（[A] `CONTEXT.md:867`）。
   - `WIRE_TO_NITROGEN` 词条用「出柜后……由 `STAGING_TO_WIRE` 覆盖，不另建任务类型」处理了「氮气柜 → 焊线」这一段（`:1659`），这是仓库里唯一一处。
   - `MesAreaEndpoint` 规定 AREA 机台端只在 `STAGING_TO_WIRE` 中是终点（`:1199`）。
7. **需求基线 v1.1.0 全文没有「清洗」**；五种功能只出现在 REQ-0324（[A] `requirements/baselines/current-requirements-v1.1.0.md:18780`）。

---

## 问题 3：现场地图

### 3.1 mapId 25 的站点

- 来源是 RIoT 实测：`GET /api/imap/v1/mapInfo/stations/25`，2026-09-03 19:10（+08:00）采集（[A] `rcs/riot-behavior-lab/evidence/rounds/2026-09-03-round-43/runs/004-stations-map-25.json:2`）。
  - 站点数 206（[A] 同轮 `runs/999-summary.json:7`）。
  - 被移除站点为空（[A] 同轮 `runs/007-removed-station-map-25.json:21`）。
- 本调研从 `004` 的响应体中提取 `name`，共 206 个：
  - `N…` 前缀的机台命名站点，如 `N1-1`、`N2-1_N3-1`
  - `T…` 前缀的机台命名站点，如 `T01-01`、`T02-02_T02-03_T03-02`
  - 唯一一个非机台名：`关卡`
- **没有任何站名包含「清洗」「氮气」「待送」「烘箱」「三光」。**
- 这与已有调查一致：206 = 205 个 AREA 命名机台站 + 1 个关卡（[A] `.scratch/8005-full-product/evidence/map-topology-observed-facts.md:65-85`）。用户 2026-09-03 确认烘箱间、三光区、氮气柜、派工待送区物理存在，但 AGV 路网只测绘了焊线区到关卡这一段（[A] `.scratch/8005-full-product/issues/13-answer.md:133-135`）。
- 8005 的配置只钉在 mapId 25（[A] `map-topology-observed-facts.md:48-59`）。

### 3.2 RIoT 证据里其它地方出现的「清洗」

- **地图 27、28 上有名为 `清洗间` 的站点**（id 29）：[A] `rcs/riot-behavior-lab/evidence/rounds/2026-07-20-round-5/runs/C2-stations-map-27.json:300`；[A] `.../C2-stations-map-28.json:300`。
  - 行为实验曾在 map 28 上对它下过移动单（[A] `rcs/riot-behavior-lab/evidence/rounds/2026-07-20-round-16/runs/S2-BC-create.json:88`，`:134`）。
  - 这两张图名为 `新基测试2` / `新基测试2opt`（[A] `map-topology-observed-facts.md:31-32`），不是 8005 配置使用的 mapId 25。
  - 仓库里没有证据说明这个测试图站点与 8005 现场的清洗间有关系。
- **RIoT 车辆组名里有「清洗多仓位2」**，设备 `尊阳-多仓位1` 属于该组（[A] `rcs/riot-behavior-lab/evidence/rounds/2026-08-04-round-42/runs/010-default.json:562`，`:568-570`）。这只是车辆分组名，不是站点。

### 3.3 六类样本的 AREA 与 mapId 25 的对照（本调研统计）

对照方法：2026-07-24 样本（[A] `mes/samples/mes-task-union/latest.csv`）的 AREA，与 mapId 25 站名按 `_` 拆开后的 333 个名字（2026-09-03）逐字比对。两份数据相隔约六周。

| TASK_TYPE | 行数 | AREA 前缀分布 | AREA 能在 mapId 25 站名里找到的行数 |
| --- | --- | --- | --- |
| `STAGING_TO_WIRE`（AREA=目标焊线/键合机台） | 246 | C 59，D 75，M 1，N 16，Q 90，S 5 | 14 |
| `WIRE_TO_NITROGEN`（AREA=焊线1 完工机台） | 91 | C 5，D 3，N 70，Q 12，S 1 | 61 |
| `DIE_TO_WIRE_STAGING`（AREA=装片完工机台） | 105 | N 105 | 73 |

- 六类样本里 AREA 以 A、B、T 开头的行数都是 0。
- 这说明：`STAGING_TO_WIRE` 的目标机台绝大多数不在 mapId 25 当前的机台命名站点里。
- 旧清洗 SQL 的终点白名单（A1～B21）也没有出现在样本 AREA 里（见 1.4，LOCID 与 AREA 是否同义未知）。

### 3.4 「派工待送区」与「焊线氮气柜」是否可能是同一个点

仓库**无法判定**，证据在两个方向上都有。

**指向「可能是同一处」的命名沿革：**

- 旧稿 5.2.2 的终点「焊线氮气柜」，其 MES 条件与 `DIE_TO_WIRE_STAGING`（终点「派工待送区」）逐字相同（[D] `:96`；[M] `query.sql:40-49`）。
- 客户讨论稿同一份文档里，§3.4 叫「派工待送区」（`:104`，`:108`），角色表 R-03 仍叫「焊线氮气柜 / 氮气柜到焊线/键合机台」（`:123`）。
- 派工待送区在术语表里的定义是「装片完工后产品暂存的固定区域，供焊线/键合工序叫料」（[A] `客户需求讨论稿-多仓位AGV系统.md:1344`）。旧稿 5.2.2 对焊线氮气柜的定义是「进入焊线或键合工序前的氮气柜暂存」（[D] `:96`）。两者用途相同。
- 旧程序目录名「烘箱完工送焊线氮气柜」（[A] `mes/sources/legacy-program-sql/2026-07-16/catalog.csv:2`）说明焊线氮气柜也接收烘箱完工的产品。
- 第六类在 2026-07-17 的待办里写作「焊线1完工→**焊线氮气柜**」（[A] `R01-R13-post-conflict-question-review.tsv:15`，`:21`）。也就是说，`WIRE_TO_NITROGEN` 的终点当时也叫焊线氮气柜。

**指向「被建模为两处」的规定：**

- REQ-0324 把「派工待送」和「氮气柜」列为两种 `PublicStationFunction`（[A] `requirements/baselines/current-requirements-v1.1.0.md:18780`）。
- REQ-0334：「同一 Station 不得同时承担多个 PublicStationFunction；未来确需复用时须以新的现场物理和作业证据重新批准，不可以普通配置放行」（[A] `current-requirements-v1.1.0.md:19360`）。
- 客户讨论稿把两者列为两个固定区域（[A] `客户需求讨论稿-多仓位AGV系统.md:111`，`:1285`）。

**地图：**mapId 25 上两者都不存在（见 3.1），无法用站点坐标或站名核对。

---

## 问题 4：必须问客户或工厂 IT 才能定的问题

| # | 问谁 | 问题 | 为什么仓库里答不了 |
| --- | --- | --- | --- |
| 1 | 工厂 IT | 清洗完工、待上焊线的批次，在 `v_fw_wip_sublot` 里依次是什么 `step`/`task`？派到焊线机台时是否就是 `step='焊线'`、`task='入站'`？清洗设备在 `fw_eqpres_eqpinformation.step` 里登记的值是什么？ | 六类样本和所有 SQL 都没有清洗相关 step（1.4）。唯一的清洗查询读的是另一个视图。这决定这段流程是否已被 `STAGING_TO_WIRE` 顺带捞到。 |
| 2 | 工厂 IT | `v_irobot_info` 是什么视图，和 `v_fw_wip_sublot` 什么关系？`清洗完工`、`焊线派工` 的含义？`LOCID` 与 `AREA` 是否同义？`A1-`～`B21` 是哪些位置？这条旧查询现在是否仍在用？ | 该视图在两个仓库里只出现在一份未分类的 `.txt` 里，没有 DDL、样本或说明；日期格式串还与字面值不一致（1.2）。 |
| 3 | 工厂 IT | WireBond1 完工入氮气柜（PDA 入柜）之后，批次的 `task` 变成什么？被派往焊线2 机台时，是否表现为 `step='焊线2'`、`task='入站'`？ | `STAGING_TO_WIRE` 只认 `焊线`/`键合`（[M] `query.sql:189`）。仓库里「由 `STAGING_TO_WIRE` 覆盖」的说法未获批准、无客户来源（1.5）。样本只有 2 分钟内的 10 轮，看不到一个批次的完整生命周期。 |
| 4 | 客户 | 「氮气柜送键合和焊线」说的是哪一个氮气柜：装片完工后暂存的焊线区氮气柜（即现在的派工待送区？）、焊线1 完工后暂存的氮气柜，还是关卡氮气柜？键合产品会不会进氮气柜？ | 文档里「焊线氮气柜」同时指 5.2.2 的终点和第六类的终点，「氮气柜」又分「焊线区/关卡」两种（3.4、2.3）。两种读法在 SQL 上的结果相反（1.5）。 |
| 5 | 客户 / 现场 | 「派工待送区」和「焊线氮气柜」在现场是否是同一处、同一组柜子？`WIRE_TO_NITROGEN` 的终点柜与派工待送区是否同一处？ | 两者都不在 mapId 25 上，无从核对；命名沿革指向同一处，但 REQ-0334 按两处建模（3.4）。 |
| 6 | 客户 / 现场 | 清洗间（清洗完工物料架）在哪？是否会测绘进 mapId 25，还是在别的图上？取货点是一个固定点还是多个架位？ | mapId 25 没有清洗相关站点。叫 `清洗间` 的站点只在 `新基测试2`/`新基测试2opt` 测试图上，归属不明（3.1、3.2）。 |
| 7 | 客户 | 客户第 4 条说的「集中装货后送机台」，目的机台是否只限 mapId 25 已测绘的机台？ | `STAGING_TO_WIRE` 样本 246 行里只有 14 行的目标 AREA 能在 mapId 25 站名里找到（3.3）。「按目的机台装到对应一侧」的范围取决于现场实际服务哪些机台区。 |
