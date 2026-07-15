---
type: reference
title: "FR / NFR / TC Classification Rules FR / NFR / TC 分类规则"
status: reference
created: 2026-07-14
updated: 2026-07-14
aliases: ["classification-rules", "分类规则", "FR/NFR/TC 分类规则"]
---

# FR / NFR / TC 分类规则

> 本文档是**说明性质的参考文档**（不是一条需求条目本身），记录 `04-functional-requirements/`、`05-test-cases/`、`08-non-functional-requirements/` 三个目录下按子文件夹分类的规则，以及每个分类子文件夹目前收录了哪些文档。新增 FR/NFR/TC 时应先查阅本文档判断归属哪个子文件夹；仅在确实出现无法归类的新场景时才新增分类（并回来更新本文档）。

## 1. 为什么要分类

`03-use-cases/` 此前已经按 11 个业务领域拆分成子文件夹（见根 [[../README|README]] 第 1 节）。FR/TC 是从具体 UC 派生出来的，天然可以按同一套业务领域归档；但 NFR 是横切多个 UC/FR 的质量属性约束，不适合按业务领域分，改用质量属性类别分类更符合其本质。分类之后：

- 浏览某个业务领域时，可以在 `03-use-cases/<domain>/`、`04-functional-requirements/<domain>/`、`05-test-cases/<domain>/` 三处平行目录里看到完整的 UC→FR→TC 链条。
- NFR 按质量属性归档后，评审某类质量目标（如可用性）时可以直接进入 `08-non-functional-requirements/availability/` 一次性看全。

移动文件本身不影响任何 wikilink（Obsidian `newLinkFormat: "shortest"` 按文件名短路径解析，与目录无关），也不影响 `06-traceability/traceability-matrix.md` 里的 Dataview 查询（`from "04-functional-requirements"` 等默认递归包含子文件夹）。

## 2. FR 分类规则

**取 frontmatter `related_uc` 数组中第一个 UC 编号所属的 `03-use-cases` 领域子文件夹，作为该 FR 的归类目录**（子文件夹命名与对应 UC 领域完全一致）。

- 一篇 FR 可能同时关联多个不同领域的 UC（例如同时涉及安全联锁 UC-004），此时以第一个列出的 UC（即该 FR 主要派生自的那个 UC）为准，其余为次要关联，不影响归类。
- 新建 FR 时，先确定它主要派生自哪个 UC，再对照下方 §4 映射表找到对应目录。
- 如果某个领域目录下暂无 FR，会有一份占位 `README.md` 说明"暂无文档，待补充"；新增第一篇 FR 时直接放进该目录，占位 `README.md` 可以保留也可以删除。

## 3. TC 分类规则

**取 frontmatter `related_fr` 数组中第一个 FR 所在的分类目录，与该 FR 同域存放**；如果 TC 尚未关联任何 FR（极少见），才回退到"TC 自身 `related_uc` 第一项所属领域"的规则。

- 这样保证同一目录下 FR 与验证它的 TC 总是相邻，便于并排查阅；由于 TC 的 FR 本身就是按 UC 领域分类的，两条规则在实践中不会产生矛盾。

## 4. FR / TC 与 UC 业务领域映射表

| 领域子文件夹 | 对应 UC | 现有 FR | 现有 TC |
| --- | --- | --- | --- |
| `01-site-operations` | UC-001/002/003/005/006/010/043/044 | FR-001~014（14 篇） | TC-001~041（41 篇） |
| `02-slot-and-hardware` | UC-011/014~018/039 | FR-015~021（7 篇） | TC-042~063（22 篇） |
| `03-agv-fleet-management` | UC-013/019~022/038 | FR-022~030（9 篇） | TC-064~097（34 篇） |
| `04-transport-task-dispatch` | UC-007/008/009/023/042 | 暂无 | 暂无 |
| `05-agv-charging` | UC-012/037 | 暂无 | 暂无 |
| `06-area-station-mapping` | UC-024/045 | 暂无 | 暂无 |
| `07-workflow-engine` | UC-025~029 | 暂无 | 暂无 |
| `08-user-and-access` | UC-030~033 | 暂无 | 暂无 |
| `09-logs-and-audit` | UC-034~036 | 暂无 | 暂无 |
| `10-safety-and-interlock` | UC-004 | 暂无（UC-004 目前只作为多篇 FR 的次要关联用例出现，未有 FR 以其为首个关联 UC） | 暂无 |
| `11-agv-parking` | UC-040/041 | 暂无 | 暂无 |

> 领域子文件夹的命名、编号与 `03-use-cases/` 下的 11 个子文件夹严格一致，参见根 [[../README|README]] 第 1 节。

## 5. NFR 分类规则

**按 frontmatter `category`（质量属性）字段归入同名子文件夹**，取值范围沿用 `nfr-template-guide.md` §2 中已定义的 11 个标准类别：`performance` / `availability` / `reliability` / `security` / `safety` / `usability` / `scalability` / `maintainability` / `auditability` / `compatibility` / `operability`。

- NFR 是横切约束，不按 UC 业务领域分类；`related_uc`/`related_fr` 字段仍照常登记横切到哪些条目，只是目录归属看 `category`。
- 如果确实出现现有 11 个类别都无法覆盖的新质量属性，才新增分类子文件夹，并同步更新本节列表与 `nfr-template-guide.md` §2。

## 6. NFR 质量属性分类表

| 分类子文件夹 | 说明 | 现有 NFR |
| --- | --- | --- |
| `availability` 可用性 | 生产班次内业务服务可用性等指标 | NFR-001 |
| `auditability` 可审计性 | 关键操作审计完整性与留存 | NFR-002 |
| `performance` 性能 | 响应时间、吞吐量等 | 暂无 |
| `reliability` 可靠性 | 故障率、MTTR、数据一致性 | 暂无 |
| `security` 安全性（信息安全） | 认证强度、权限校验、加密 | 暂无 |
| `safety` 功能安全 | 故障安全响应时间、失败默认拒绝 | 暂无 |
| `usability` 易用性 | 界面易用性、培训上手时间 | 暂无 |
| `scalability` 可扩展性 | 仓位/AGV/任务数增长时的扩展能力 | 暂无 |
| `maintainability` 可维护性 | 配置变更成本、日志可诊断性 | 暂无 |
| `compatibility` 兼容性/互操作性 | 与 MES/RCS/RIOT/IO 模块对接 | 暂无 |
| `operability` 可运维性 | 部署、监控、告警、运维值守 | 暂无 |

## 7. 目录根目录保留文件

以下文件与具体分类无关，继续保留在各自目录的根层级，不下沉到子文件夹：

- `04-functional-requirements/README.md`、`fr-template-guide.md`
- `05-test-cases/README.md`
- `08-non-functional-requirements/README.md`、`nfr-template-guide.md`

## 8. 变更记录

- 2026-07-14：首次拆分。将 21 篇 FR、63 篇 TC 按 §4 映射表迁入对应 UC 业务领域子文件夹；将 2 篇 NFR 按 §6 分类表迁入对应质量属性子文件夹；本文档随迁移一并创建。
- 2026-07-14：`03-agv-fleet-management` 域（UC-013/019/020/021/022/038）新增 FR-022~030（9 篇）、TC-064~097（34 篇），直接落位到对应分类子文件夹（未经历"根目录再迁移"步骤）；`FR-022~028` 关联 `NFR-002`，`FR-029`（UC-021 归档）、`FR-030`（UC-022 只读看板）不关联，详见 `nfr-002-audit-completeness-and-retention.md` Notes。§4 映射表随之更新，两个占位 `README.md` 已删除。
