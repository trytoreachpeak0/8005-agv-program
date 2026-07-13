# 需求文档 Obsidian Vault 使用说明

本目录已按 Obsidian vault 的方式重新组织，用来承载完整的 `Business Rule → Use Case → Functional Requirement → Test Case` 需求追溯链。首次使用请先看第 5 节「首次打开步骤」。

## 1. 目录结构

```
requirement-documents/
├─ .obsidian/                     Obsidian 配置与插件（已内置 Dataview、Templater）
├─ _templates/                    Templater 笔记模板（新建 UC/BR/FR/TC 时自动套用）
├─ _attachments/                  图片等附件统一存放位置
├─ 00-vision/                     愿景、范围与系统上下文
│  ├─ vision-and-scope.md         业务愿景、范围与限制
│  └─ system-context.md           系统上下文图及外部交互边界
├─ 01-stakeholders/               干系人与角色清单（未改动）
├─ 02-business-rules/             业务规则 BR-001 ~ BR-007
├─ 03-use-cases/                  用例 UC-001 ~ UC-037，按业务领域拆分到 6 个子文件夹（uc-template-guide.md 仍放在根目录）
│  ├─ 01-site-operations/         站点作业与任务执行（UC-001~006、009、010）
│  ├─ 02-slot-and-hardware/       仓位与格口硬件（UC-011、014~018）
│  ├─ 03-agv-fleet-and-dispatch/  AGV 车队调度与充电（UC-007、008、012、013、019~024、037）
│  ├─ 04-workflow-engine/         流程模板与工作流引擎（UC-025~029）
│  ├─ 05-user-and-access/         用户与权限管理（UC-030~033）
│  └─ 06-logs-and-audit/          日志、追溯与审计（UC-034~036）
├─ 04-functional-requirements/    功能需求 FR-001、FR-002 ...（骨架已建好，内容待补充）
├─ 05-test-cases/                 测试用例 TC-001、TC-002 ...（骨架已建好，内容待补充）
└─ 06-traceability/               追溯矩阵总览（Dataview 自动生成）
```

建议首次阅读时先查看 [[vision-and-scope|愿景与范围]]，再查看 [[system-context|系统上下文与边界]]；后者用于快速了解本系统与 MES、RCS/RIOT、AGV、IO 模块及现场用户之间的交互关系。

## 2. ID 与命名规范

| 类型 | ID 格式 | 文件名格式（小写短横线） | 示例 |
| --- | --- | --- | --- |
| Business Rule 业务规则 | `BR-001` | `br-001-xxx.md` | `br-001-用户培训有效性.md` |
| Use Case 用例 | `UC-001` | `uc-001-xxx.md` | `uc-001-load-completed-lot-into-slot.md` |
| Functional Requirement 功能需求 | `FR-001` | `fr-001-xxx.md` | `fr-001-xxx.md` |
| Test Case 测试用例 | `TC-001` | `tc-001-xxx.md` | `tc-001-xxx.md` |
| Decision Record 决策记录 | `DR-001` | `dr-001-xxx.md` | `dr-001-tech-stack.md` |

- 编号统一 3 位数字，方便未来扩展且排序整齐。
- 文件名统一小写 + 短横线（kebab-case），不用空格，符合项目已有的 `file-naming-convention/文件命名规范.md`，也避免 Obsidian 按最短路径解析链接时出现重名歧义。
- 每篇笔记的 frontmatter 里都有 `id` 字段和 `aliases: ["UC-001"]`，所以在别的笔记里直接输入 `[[UC-001` 也能被 Obsidian 搜索到（别名搜索），不需要记住完整文件名。

## 3. 引用方式：wikilink

不再使用原来的反引号文件名（如 `` `UC-2-Confirm Task Completion.md` ``），统一改为 Obsidian wikilink，可点击跳转、可在 Backlinks 面板看到反向引用：

```markdown
[[uc-002-confirm-task-completion|UC-002]]
```

显示效果只有 `UC-002`，点击后跳转到对应文件。所有 5 篇 UC 文档中原本的"关联用例""正文引用其他 UC"处均已替换为这种写法。

后续新增 BR/FR/TC 时，Origin/Related/Verification 等字段也统一用这种写法，例如：

```markdown
**Origin:** [[br-001-xxx|BR-001]]
**Related Use Case:** [[uc-002-confirm-task-completion|UC-002]]
**Verification:** [[tc-001-xxx|TC-001]]
```

## 4. Frontmatter 字段约定

每篇笔记顶部都有 YAML frontmatter，用于 Dataview 自动生成追溯矩阵，字段含义：

| 字段 | 说明 |
| --- | --- |
| `id` | 唯一编号，如 `UC-001` |
| `type` | 固定值：`use-case` / `business-rule` / `functional-requirement` / `test-case` |
| `title` | 中英文标题 |
| `status` | `draft`（草稿）/ `reviewed`（已评审）/ `approved`（已确认），可自行扩展 |
| `related_uc` / `related_br` / `related_fr` / `related_tc` | 关联的其他条目 ID 数组，例如 `["UC-002", "UC-003"]` |
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
| 新建笔记时套用模板、按目录自动匹配模板、弹窗填写编号 | **Templater** (`templater-obsidian`) | 第三方社区插件 | 已下载安装到 `.obsidian/plugins/templater-obsidian/`，模板文件夹已指向 `_templates/`，并按目录（02/03/04/05）自动关联对应模板 |
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
- `03-use-cases` 下 UC-001 ~ UC-037 已按业务领域拆分到 6 个子文件夹（见第 1 节目录结构），仅移动文件位置，不改动任何正文内容或 frontmatter。之所以不需要同步修正其他文档里的双链引用或 Dataview 查询，是因为：
  1. `.obsidian/app.json` 中 `newLinkFormat: "shortest"`，`[[uc-001-xxx|UC-001]]` 这类链接按"全局唯一文件名"解析，与文件夹路径无关；
  2. `06-traceability/traceability-matrix.md` 里 Dataview 的 `from "03-use-cases"` 查询默认递归包含子文件夹；
  3. Templater 的 `folder_templates` 里 `"folder": "03-use-cases"` 对子文件夹同样按路径前缀生效，之后在子文件夹里新建笔记仍会自动套用 `template-use-case.md`。

## 8. 模板复用：子项目如何使用本目录的模板

本仓库下的子项目（如 `slots-simulator/requirement-documents/`）如果也想按同样的规范写需求文档，**不需要各自复制一份模板**——所有模板统一维护在本目录 `_templates/`，子项目里只放一个不含实际内容、指向本目录对应模板的占位文件。这样任何模板改动只需要改这一处，不会出现同一份模板散落在多个位置、改了一处忘了改另一处的情况。

- `_templates/template-decision-record.md`（`DR-xxx` 决策记录）就是因为 `slots-simulator` 子项目需要记录"经与用户确认"的技术/范围决策而新增的模板类型，虽然目前本目录还没有实际的 `DR-xxx` 文档，但模板统一放在这里，供任何子项目复用。
- 因为 Obsidian 的 Templater 插件按"vault"生效，子项目如果是独立打开的 vault（而不是把整个仓库根目录当作一个 vault 打开），无法通过插件配置直接跨 vault 引用这里的模板文件、自动弹窗填充——这种情况下模板复用停留在"人工照抄结构、内容不重复维护两份"的层面，不是 Templater 自动化层面的复用。如果需要真正的跨目录自动化模板填充，需要把整个仓库根目录作为同一个 vault 打开，并在 Templater 设置里把子项目对应目录也映射到本目录的模板文件。

## 9. 尚未处理，留待后续

- `02-business-rules`、`04-functional-requirements`、`05-test-cases` 三个目录目前只有说明性 `README.md`，没有真实内容——因为这些业务规则/功能需求/测试用例目前还不存在，需要你后续补充实际内容后才能让追溯矩阵有东西可展示。
- `01-stakeholders/stakeholders-and-user-classes.md` 里有一处引用写的是 `01-vision-scope.md`，但实际文件名是 `vision-and-scope.md`（历史遗留的文件名不一致），本次未涉及 UC 迁移范围，故未修改，但转成 wikilink 后 Obsidian 会明显提示这是"未解析链接"，建议后续顺手修一下。
- `user case.md`（根目录下的早期草稿）里的 `UC-01` 编号体系和正式 `03-use-cases` 里的编号是两套东西，目前未做统一，如果要统一建议后续单独讨论。
