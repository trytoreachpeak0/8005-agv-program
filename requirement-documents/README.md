# 需求文档 Obsidian Vault 使用说明

本目录已按 Obsidian vault 的方式重新组织，用来承载完整的 `Business Rule → Use Case → Functional Requirement → Test Case` 需求追溯链，以及横切约束 FR 的 `Non-Functional Requirement`。首次使用请先看第 5 节「首次打开步骤」。

## 1. 目录结构

```
requirement-documents/
├─ .obsidian/                     Obsidian 配置与插件（已内置 Dataview、Templater）
├─ _templates/                    Templater 笔记模板（新建 UC/BR/FR/NFR/TC 时自动套用）
├─ _attachments/                  图片等附件统一存放位置
├─ 00-vision/                     愿景、范围与系统上下文
│  ├─ vision-and-scope.md         业务愿景、范围与限制
│  └─ system-context.md           系统上下文图及外部交互边界
├─ 01-stakeholders/               干系人与角色清单（未改动）
├─ 02-business-rules/             业务规则 BR-001 ~ BR-008
├─ 03-use-cases/                  用例 UC-001 ~ UC-038，按业务领域拆分到 10 个子文件夹（uc-template-guide.md 仍放在根目录）
│  ├─ 01-site-operations/         站点作业与任务执行（UC-001~003、005、006、010）
│  ├─ 02-slot-and-hardware/       仓位与格口硬件（UC-011、014~018、039）
│  ├─ 03-agv-fleet-management/    AGV 车辆管理：多仓位模型、接入、启停、配置、归档、车队看板（UC-013、019~022、038）
│  ├─ 04-transport-task-dispatch/ 搬运任务分发：MES 同步、任务分配、下发 RIOT、持续监听到站（UC-007、008、009、023）
│  ├─ 05-agv-charging/            AGV 充电：充电策略配置与手动派车充电（UC-012、037）
│  ├─ 06-area-station-mapping/    AREA—地图站点映射维护与 RIOT 路网同步（UC-024、UC-045）
│  ├─ 07-workflow-engine/         流程模板与工作流引擎（UC-025~029）
│  ├─ 08-user-and-access/         用户与权限管理（UC-030~033）
│  ├─ 09-logs-and-audit/          日志、追溯与审计（UC-034~036）
│  ├─ 10-safety-and-interlock/    跨场景安全联锁（UC-004，贯穿 AGV 全生命周期，不局限于某一具体站点操作）
│  └─ 11-agv-parking/             AGV 空闲返回停靠点（UC-040、041），结构参照 05-agv-charging 单独成组
├─ 04-functional-requirements/    功能需求 FR-001、FR-002 ...（含 fr-template-guide），按 03-use-cases 同名的 11 个业务领域拆到子文件夹
│  ├─ 01-site-operations/         FR-001~014
│  ├─ 02-slot-and-hardware/       FR-015~021
│  └─ 03-agv-fleet-management/ ~ 11-agv-parking/  暂空（占位 README，待对应 UC 拆出 FR）
├─ 05-test-cases/                 测试用例 TC-001、TC-002 ...，按其验证的 FR 所在业务领域拆到子文件夹
│  ├─ 01-site-operations/         TC-001~041
│  ├─ 02-slot-and-hardware/       TC-042~063
│  └─ 03-agv-fleet-management/ ~ 11-agv-parking/  暂空（占位 README，待对应领域补充 FR/TC）
├─ 06-traceability/               追溯矩阵总览（Dataview 自动生成）、FR/NFR/TC 分类规则
├─ 07-customer-deliverables/      面向客户的需求讨论稿（中文 Markdown 源与 Word）
├─ 08-non-functional-requirements/ 非功能需求 NFR-001、NFR-002 ...（含 nfr-template-guide），按质量属性 category 拆到 11 个子文件夹
│  ├─ availability/               NFR-001
│  ├─ auditability/               NFR-002
│  └─ performance/ ~ operability/ 其余 9 个质量属性类别，暂空（占位 README）
```

> `04-functional-requirements`、`05-test-cases`、`08-non-functional-requirements` 的分类规则、完整映射表见 [[classification-rules|06-traceability/classification-rules.md]]。

> 说明：`08-non-functional-requirements/` 文件夹名较长，上方对齐略有压缩，仅为排版限制，不影响实际路径。

建议首次阅读时先查看 [[vision-and-scope|愿景与范围]]，再查看 [[system-context|系统上下文与边界]]；后者用于快速了解本系统与 MES、RCS/RIOT、AGV、IO 模块及现场用户之间的交互关系。

## 2. ID 与命名规范

| 类型 | ID 格式 | 文件名格式（小写短横线） | 示例 |
| --- | --- | --- | --- |
| Business Rule 业务规则 | `BR-001` | `br-001-xxx.md` | `br-001-用户培训有效性.md` |
| Use Case 用例 | `UC-001` | `uc-001-xxx.md` | `uc-001-load-completed-lot-into-slot.md` |
| Functional Requirement 功能需求 | `FR-001` | `fr-001-xxx.md` | `fr-001-xxx.md` |
| Non-Functional Requirement 非功能需求 | `NFR-001` | `nfr-001-xxx.md` | `nfr-001-xxx.md` |
| Test Case 测试用例 | `TC-001` | `tc-001-xxx.md` | `tc-001-xxx.md` |
| Decision Record 决策记录 | `DR-001` | `dr-001-xxx.md` | `dr-001-tech-stack.md` |

- 编号统一 3 位数字，方便未来扩展且排序整齐。
- 文件名统一小写 + 短横线（kebab-case），不用空格，符合工作区的 `8005-workspace/file-naming-convention/文件命名规范.md`，也避免 Obsidian 按最短路径解析链接时出现重名歧义。
- 每篇笔记的 frontmatter 里都有 `id` 字段和 `aliases: ["UC-001"]`，所以在别的笔记里直接输入 `[[UC-001` 也能被 Obsidian 搜索到（别名搜索），不需要记住完整文件名。

## 3. 引用方式：wikilink

不再使用原来的反引号文件名（如 `` `UC-2-Confirm Task Completion.md` ``），统一改为 Obsidian wikilink，可点击跳转、可在 Backlinks 面板看到反向引用：

```markdown
[[uc-002-confirm-task-completion|UC-002]]
```

显示效果只有 `UC-002`，点击后跳转到对应文件。所有 5 篇 UC 文档中原本的"关联用例""正文引用其他 UC"处均已替换为这种写法。

后续新增 BR/FR/NFR/TC 时，Origin/Related/Verification 等字段也统一用这种写法，例如：

```markdown
**Origin:** [[br-001-xxx|BR-001]]
**Related Use Case:** [[uc-002-confirm-task-completion|UC-002]]
**Related NFR:** [[nfr-001-service-availability|NFR-001]]
**Verification:** [[tc-001-xxx|TC-001]]
```

## 4. Frontmatter 字段约定

每篇笔记顶部都有 YAML frontmatter，用于 Dataview 自动生成追溯矩阵，字段含义：

| 字段 | 说明 |
| --- | --- |
| `id` | 唯一编号，如 `UC-001` |
| `type` | 固定值：`use-case` / `business-rule` / `functional-requirement` / `non-functional-requirement` / `test-case` |
| `title` | 中英文标题 |
| `status` | `draft`（草稿）/ `reviewed`（已评审）/ `approved`（已确认），可自行扩展 |
| `category` | 仅 NFR：质量属性类别（如 `availability` / `auditability`） |
| `related_uc` / `related_br` / `related_fr` / `related_nfr` / `related_tc` | 关联的其他条目 ID 数组，例如 `["UC-002", "UC-003"]` |
| `aliases` | 别名，固定填 ID 本身，方便快速链接和搜索 |

**只要这些字段维护正确，`06-traceability/traceability-matrix.md` 里的表格会自动更新，不需要手工同步。**

## 5. 首次打开步骤（重要）

1. 用 Obsidian 打开 vault 时选择 **本 `requirement-documents` 文件夹本身**作为 vault 根目录（不是它的上级目录）。
2. Obsidian 新 vault 默认开启"限制模式 Restricted Mode"，会阻止所有第三方插件运行。首次打开后：
   - 进入 `设置 → 第三方插件 Community plugins`
   - 点击 **关闭限制模式 Turn off Restricted Mode**
   - 确认列表中 `Dataview` 和 `Templater` 均已启用（本次已经把插件文件和启用配置放好，正常情况下关闭限制模式后就是启用状态）
3. 打开 `06-traceability/traceability-matrix.md`，确认能看到 Dataview 表格正常渲染（而不是显示原始代码块文字），说明 Dataview 生效。
4. 在 `03-use-cases` 文件夹里右键 → 新建笔记，确认会自动弹出编号/标题输入框并套用模板，说明 Templater 生效。

## 6. 各能力对应的插件

| 能力 | 依赖插件 | 类型 | 说明 |
| --- | --- | --- | --- |
| Wikilink 点击跳转、Backlinks 反向引用面板、Graph View 关系图谱 | 无需额外插件 | Obsidian 核心（`backlink`、`graph`、`outgoing-link`） | 已在 `.obsidian/core-plugins.json` 中启用 |
| 新建笔记时套用模板、按目录自动匹配模板、弹窗填写编号 | **Templater** (`templater-obsidian`) | 第三方社区插件 | 已下载安装到 `.obsidian/plugins/templater-obsidian/`，模板文件夹已指向 `_templates/`，并按目录（02/03/04/05/08）自动关联对应模板 |
| 追溯矩阵表格自动生成、覆盖率检查查询 | **Dataview** (`dataview`) | 第三方社区插件 | 已下载安装到 `.obsidian/plugins/dataview/` |
| （暂缓，未启用）Canvas 可视化追溯链 | Obsidian 内置 Canvas 核心插件 | Obsidian 核心 | 按你的要求本次先不做，需要时随时可加 |
| （暂缓，未启用）块级引用 `^blockid` 精确定位段落 | 无需插件，Obsidian 核心能力 | - | 按你的要求本次先不做 |

## 7. 本次已完成的迁移

- `03-use-cases` 下原来的 5 个文件（文件名含空格，如 `UC-1-Load Completed Lot into Slot.md`）已全部删除，替换为新命名 + frontmatter + wikilink 版本：
  - `uc-001-load-completed-lot-into-slot.md`
  - `uc-002-confirm-task-completion.md`
  - `uc-003-agv-arrives-at-designated-station.md`
  - `uc-004-slot-door-safety-interlock.md`
  - `uc-005-retrieve-mis-stored-product-from-slot.md`
- 原文内容未做实质性改动，只做了三类替换：① 编号 `UC-1`→`UC-001`（以此类推）；② 反引号文件名引用 → wikilink；③ 补充 frontmatter。
- 检查过 `00-vision/vision-and-scope.md`、`01-stakeholders/stakeholders-and-user-classes.md`、`user case.md`，均未引用过旧的 UC 文件名，因此未做改动。
- `03-use-cases` 下 UC-001 ~ UC-037 已按业务领域拆分到子文件夹（见第 1 节目录结构），仅移动文件位置，不改动任何正文内容或 frontmatter。之所以不需要同步修正其他文档里的双链引用或 Dataview 查询，是因为：
  1. `.obsidian/app.json` 中 `newLinkFormat: "shortest"`，`[[uc-001-xxx|UC-001]]` 这类链接按"全局唯一文件名"解析，与文件夹路径无关；
  2. `06-traceability/traceability-matrix.md` 里 Dataview 的 `from "03-use-cases"` 查询默认递归包含子文件夹；
  3. Templater 的 `folder_templates` 里 `"folder": "03-use-cases"` 对子文件夹同样按路径前缀生效，之后在子文件夹里新建笔记仍会自动套用 `template-use-case.md`。
- 2026-07-13：原 `03-agv-fleet-and-dispatch/`（UC-007、008、012、013、019~024、037）按用户要求进一步拆分为 4 个子文件夹，原 `04-workflow-engine/`~`07-safety-and-interlock/` 依次顺移为 `07-workflow-engine/`~`10-safety-and-interlock/`：
  - `03-agv-fleet-management/`（车辆管理）：UC-013、019、020、021、022——AGV 本体档案、启停、配置、归档、车队看板。
  - `04-transport-task-dispatch/`（任务分发）：UC-007、008、023——搬运任务从 MES 同步、分配到具体 AGV、下发 RIOT 的业务流转。
- 2026-07-13：`UC-009 持续监听移动任务直到AGV到站` 由 `01-site-operations/` 移入 `04-transport-task-dispatch/`——该 UC 是本地服务器内部轮询 RIOT 移动任务状态的过程，直接衔接 `UC-008` 下发之后、`UC-003` 到站处理之前的阶段，属于任务分发链路的一部分，而非现场人员的站点作业。
  - `05-agv-charging/`（充电相关）：UC-012、037——充电策略配置与手动派车充电；经与用户确认单独成组，不并入车辆管理或任务分发。
  - `06-area-station-mapping/`（地图相关）：UC-024——AREA—地图站点映射维护；经与用户确认单独成组，不并入任务分发。
- 2026-07-13：新增 `UC-038 维护多仓位AGV模型`（放入 `03-agv-fleet-management/`）与 `BR-008 AGV Slot Model Versioning`，解决"接入 AGV 时未定义多仓位类型"的问题；型号支持多版本（发布不可变、AGV 接入时绑定快照、接入后不允许更换型号，做法参照 `BR-005` 流程模板版本），并同步修订了 `UC-019`（接入时改为选择模型版本、自动生成仓位实例）、`UC-020`（仓位结构改为只读展示，移除编辑入口）、`BR-002`（补充仓位数据来源说明）。
- 2026-07-13：新增 `UC-039 维护仓位—IO点位映射配置`（放入 `02-slot-and-hardware/`），解决 `UC-018` 自述"不负责映射配置最初如何生成/录入"留下的缺口——此前没有任何 UC 覆盖仓位到 DO/DI 点位映射数据本身的创建/修改/删除，只有测试/核对类 UC；本次补齐配置录入环节，作为 `UC-015`/`UC-016`/`UC-017`/`UC-018` 的更底层前提。
- 2026-07-13：经用户确认，删除 `vision-and-scope.md` 原 2.1 节"主要特性 Major features"整段功能树（含"驻点发料""补料"等未确认属于本项目范围的内容），该节内容与本项目实际确认需求不符；后续如需重新梳理主要特性清单，应以已确认的 UC/BR 为准逐条重建，不再保留旧版功能树。经用户进一步确认：驻点发料、补料两项能力本项目不做，不建 UC；"低电量自动回充""AGV 空闲返回停靠点"仍属于本项目范围，分别处理如下两条。
- 2026-07-13：新增 `UC-040 维护 AGV 停靠点配置`、`UC-041 空闲AGV自动返回停靠点`（均放入新建的 `11-agv-parking/`）与 `BR-009 停靠点分配与排队规则`，解决 `vision-and-scope.md` 原功能树"系统辅助任务：……返回驻点……"此前无任何 UC 落地的缺口；结构参照 `UC-037`/`BR-007`充电桩配置与选桩排队的既有拆分方式（配置类 UC + 执行类 UC + 排队 BR）。经确认：触发时机为 AGV 一空闲即立即判断；停靠点选择采用候选集合 + FIFO 排队（区别于充电桩的电量优先）；本 UC 与 `UC-008`（自动派车）、`UC-012`（手动充电）竞争同一个"AGV 空闲"触发窗口，优先级最低，不做抢占。
- 2026-07-13：新增 `UC-042 处理AGV途中故障并改派或终止关联任务`（放入 `04-transport-task-dispatch/`），解决“AGV 离站在途后报障或离线，车上任务如何安全收尾”的缺口——`UC-006` 覆盖离站前清空并取消，`UC-028` 只覆盖流程步骤层面的通用异常处置。本 UC 当前仅为初稿骨架，TBD 事项较多（故障状态机、终止后产品如何继续送达、应急开锁权限等），需要后续与用户逐项确认。
- 2026-07-13："服务器/系统重启后，本地任务—AGV绑定—仓位占用—RCS/RIOT在途任务的整体对账恢复"经确认属于可以按 UC 建模的场景（参照 `UC-009` 系统内部过程作为 primary_actor 的先例），但内容涉及面广，经用户确认暂缓，先记录缺口，留待后续与其他子系统设计稳定后再补建 UC。
- 2026-07-14：将 `mes/AGV系统业务与MES任务模型.md`（及接口确认文档）中已确认的 MES 业务规则正式融入本 vault 追溯体系，不修改 `mes/` 原始文件：
  - 新增 [[br-012-mes-task-idempotency-and-reconciliation|BR-012]]（幂等键、固定延迟轮询、字段冻结、消失对账、`PAUSED_ZERO_DROP`、重启基线、只读安全）、[[br-013-multi-basket-loading|BR-013]]（权威花篮数量、批量开门与 SUBLOT—仓位占用模型）、[[br-014-transport-task-types-and-fixed-stations|BR-014]]（现为六类任务类型与五个固定区域站点）。
  - 重写 [[uc-007-sync-transport-task-from-mes|UC-007]]，用上述 BR 替换原 TBD；[[uc-001-load-completed-lot-into-slot|UC-001]] 增加备选流程 1.2；[[uc-010-unload-completed-lot-at-destination-station|UC-010]] 关闭“是否回传 MES”TBD 并引用 BR-013/014；[[br-001-dispatch-task-range|BR-001]] 补充复合停靠与上下游等待；[[br-002-agv-allocation-eligibility|BR-002]] / [[uc-023-allocate-transport-tasks-to-agv|UC-023]] 补充第 5 类最高优先级与无响应升级。
  - [[br-003-area-station-mapping|BR-003]] 两表模型已与 mes 文档第 10 节一致，无需结构性改写。
  - 同日新增 `07-customer-deliverables/`，产出面向客户的中文需求讨论稿（Markdown 源 + Word）。
- 2026-07-14：新增 [[br-015-path-cost-and-dispatch-ranking|BR-015]]（路径成本与派车排序权衡）与 [[uc-045-sync-map-topology-from-riot|UC-045]]（从 RIOT 同步地图路网）：本系统只读缓存站点+可通行路径，用最短路径成本作为派车排序因子之一（与紧急度/等待时长等一并权衡）；向 RIOT 下发仍只指定目的地。同步修订 [[br-002-agv-allocation-eligibility|BR-002]] 候选排序第 4 条、[[uc-023-allocate-transport-tasks-to-agv|UC-023]]、[[uc-008-dispatch-move-order-to-riot|UC-008]] Assumption，以及 [[system-context|system-context]] 边界说明。
- 2026-07-14：定稿 FR/NFR 文档规范（Karl 可验证写法 + Obsidian Templater/Dataview 惯例）：更新 `_templates/template-functional-requirement.md`（含 Rationale、GWT、`related_nfr`），新建 `_templates/template-non-functional-requirement.md` 与目录 `08-non-functional-requirements/`；新增 [[fr-template-guide|FR 模板说明]]、[[nfr-template-guide|NFR 模板说明]]；黄金样例 [[fr-001-sublot-task-validity-and-dispatch-range-check|FR-001]] / [[fr-002-slot-unlock-occupancy-confirm-and-state-persist|FR-002]]（自 UC-001）、[[nfr-001-service-availability|NFR-001]] / [[nfr-002-audit-completeness-and-retention|NFR-002]]；追溯矩阵增加 NFR 总览与覆盖率查询。
- 2026-07-14：将 `04-functional-requirements`、`05-test-cases`、`08-non-functional-requirements` 由单层平铺目录改为按分类拆子文件夹：FR/TC 按 `related_uc`/`related_fr` 归属的 UC 业务领域拆到与 `03-use-cases` 同名的 11 个子文件夹（现有 21 篇 FR、63 篇 TC 全部落在 `01-site-operations`、`02-slot-and-hardware` 两域，其余 9 域暂空占位）；NFR 按 `category` 质量属性拆到 11 个子文件夹（现有 2 篇 NFR 分别落在 `availability`、`auditability`）。分类规则、完整映射表新增于 [[classification-rules|06-traceability/classification-rules.md]]。三处 `README.md`（04/05/08 各自根目录）与本文件目录结构一并更新；因 wikilink 按文件名短路径解析、Dataview `from` 查询递归包含子文件夹，本次搬动未修改任何链接或查询语句。
- 2026-07-31：新增 [[uc-046-handle-station-departure-wait-timeout|UC-046]]、[[fr-031-station-departure-wait-timeout-and-auto-closure|FR-031]] 与 TC-103～TC-112：可装货站点进入 StationDepartureWaiting 后由服务端按默认 5 分钟（可站点覆盖）倒计时；无人操作到期原子取消本站尚未开始任务并安全转往下一站。同步将 UC-002/FR-003/FR-004 改为本站结束语义，并按 ADR-cross-0054 改为 LoadBatch 物理闭环后自动提交、StopClosureCommit 前允许追加审计的原仓位纠错。

## 8. 模板复用：子项目如何使用本目录的模板

本仓库下的子项目（如 `slots-simulator/requirement-documents/`）如果也想按同样的规范写需求文档，**不需要各自复制一份模板**——所有模板统一维护在本目录 `_templates/`，子项目里只放一个不含实际内容、指向本目录对应模板的占位文件。这样任何模板改动只需要改这一处，不会出现同一份模板散落在多个位置、改了一处忘了改另一处的情况。

- `_templates/template-decision-record.md`（`DR-xxx` 决策记录）就是因为 `slots-simulator` 子项目需要记录"经与用户确认"的技术/范围决策而新增的模板类型，虽然目前本目录还没有实际的 `DR-xxx` 文档，但模板统一放在这里，供任何子项目复用。
- 因为 Obsidian 的 Templater 插件按"vault"生效，子项目如果是独立打开的 vault（而不是把整个仓库根目录当作一个 vault 打开），无法通过插件配置直接跨 vault 引用这里的模板文件、自动弹窗填充——这种情况下模板复用停留在"人工照抄结构、内容不重复维护两份"的层面，不是 Templater 自动化层面的复用。如果需要真正的跨目录自动化模板填充，需要把整个仓库根目录作为同一个 vault 打开，并在 Templater 设置里把子项目对应目录也映射到本目录的模板文件。

## 9. 尚未处理，留待后续

- `05-test-cases` 目前只有说明性 `README.md` 与 Templater 骨架，尚无真实 TC；FR/NFR 黄金样例的 `related_tc` 仍为空，待补测试后再回填。
- `04-functional-requirements` / `08-non-functional-requirements` 目前仅有模板、指南与黄金样例，其余 UC 尚未批量拆 FR/NFR。
- `01-stakeholders/stakeholders-and-user-classes.md` 里有一处引用写的是 `01-vision-scope.md`，但实际文件名是 `vision-and-scope.md`（历史遗留的文件名不一致），本次未涉及 UC 迁移范围，故未修改，但转成 wikilink 后 Obsidian 会明显提示这是"未解析链接"，建议后续顺手修一下。
- `user case.md`（根目录下的早期草稿）里的 `UC-01` 编号体系和正式 `03-use-cases` 里的编号是两套东西，目前未做统一，如果要统一建议后续单独讨论。
