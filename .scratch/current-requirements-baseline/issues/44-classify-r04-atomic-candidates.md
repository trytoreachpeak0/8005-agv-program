# 拆分并分类功能需求的原子候选

Type: task
Status: resolved
Blocked by: 34

## Question

依据总账 [R04 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 31 份候选文档，如何按功能声明与验收条件拆分原子条目，保留 UC/BR 上游指针，并在进入批准前完成证据分类、适用范围记录、重复/派生检查和冲突路由？

## Answer

已完成 31/31 份 R04 `draft` FR 的原子拆分与证据分类，规范主数据为 [R04 原子候选分类账](../evidence/atomic-candidates/R04-atomic-candidates.tsv)，拆分边界、字段、冲突/版本登记与复核方式见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fca67-9fff-7980-b212-daf354e681dd/R04-atomic-candidates.xlsx)。

- 共形成 1,192 条可独立复核记录；Description 按句界拆分，146 个 AC 标题只作定位证据，每个 Given、When、Then 及其可独立判断分句分别记录来源路径、原 SHA-256、行号、章节、声明、完整上下文、适用范围、类别、处置路线、重复/派生关系、冲突指针和批准缺口。
- 31 个来源逐份固定 frontmatter 的 23 个唯一 UC 和 5 个唯一 BR 上游指针，并保留 FR/NFR 关联与调查形成历史；缺少 Origin 节的 FR 没有因此丢失 Related 指针，也没有被自动提升证据强度。
- Rationale、Origin、Related、Verification、Notes 与 AC 标题共 555 条只作 `evidence-only`；635 条功能/验收候选进入 `needs-upstream-source-and-explicit-approval`，1 条明确消息标识实现细化进入 `exclude-from-requirement-approval`，1 条运输需求抑制边界进入 `hold-for-conflict-decision`。
- 功能候选已按前置、触发、结果、权限、安全联锁、状态迁移、原子性/一致性、错误处置、HMI 与审计等独立判断维度分类；TC 覆盖、ADR `accepted`、Git 作者、`draft` 和当前实现均未被当作批准。
- `CF-R01-001` 命中 1 条同一 SUBLOT 跨任务类型的永久抑制边界；`AD-R04-001` 直接命中 4 条替代历史证据，并把 R04-02～15、17、18、20、22 共 18 份来源绑定为 `ecd0fd8→493ac5a` 版本范围。它们补足既有冲突/版本线索，但没有暴露需在跨批次去重前新增的独立 HITL 票。
- 所有 1,192 条记录的 `approval_state` 均为 `not-approved`，没有分配永久 `REQ-NNNN`；49 条后出现记录只按规范化声明指纹标为精确重复，没有合并语义近似项。
- XLSX 的 Summary、Source Coverage、Conflict Register 与 Candidates 四张表已核验：31 个来源全部 `OK`，公式错误扫描为零，并完成四张表及 Candidates 首尾区域的视觉检查。

失败式 `--verify-only` 已独立通过：`total=1192`、`sources=31`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=49`、`conflict_rows=5`；31 个来源当前 SHA-256 与固定值一致，重建结果与主账逐字段一致，并固定验证 146 个 AC 定位。

本票只分类现有证据，没有批准新的领域词汇或业务决定，因此未修改根 `CONTEXT.md`。
