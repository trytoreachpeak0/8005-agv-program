# 拆分并分类仓位、硬件与车队验收的原子候选

Type: task
Status: resolved
Blocked by: 34, 40

## Question

依据总账 [R06 候选组](../evidence/document-classification/R01-R13-candidate-groups.tsv)固定的 52 份未阻塞测试草案，如何按场景级验收声明拆分原子条目，保留 FR/UC/BR 上游和执行证据缺口，并完成去重、范围、冲突和批准隔离；同时依“决定 R06 上游漂移旧稿的版本归属与去留”保留 `TC-044`～`TC-047` 为绑定旧 `FR-016` 的未批准历史证据，并以新身份建立当前“立即禁用”、“待禁用”、“启用不覆盖车载硬件不可操作”和“批量独立结果”未批准验收候选，而不修改、复用或把旧 TC 当作当前候选？

## Answer

已完成总账固定的 52/52 份 R06 当前测试草案的场景级拆分与证据分类，规范主数据为 [R06 原子候选分类账](../evidence/atomic-candidates/R06-atomic-candidates.tsv)，可重建汇总为 [R06 原子候选摘要](../evidence/atomic-candidates/R06-atomic-candidates-summary.json)，旧稿版本隔离为 [R06 漂移历史证据账](../evidence/atomic-candidates/R06-drifted-historical-evidence.tsv)，拆分边界、字段与处置路线见 [原子候选分类说明](../evidence/atomic-candidates/README.md)，另提供 [XLSX 审阅副本](../../../outputs/019fca8e-d853-7022-9f17-f8973206bf37/R06-atomic-candidates.xlsx)。

- `TC-042`～`TC-043` 与 `TC-048`～`TC-097` 共形成 225 条场景记录：54 条前置、59 条动作、60 条结果与 52 条验证指针；52 份来源均覆盖四种角色并保留 TC、FR、UC、路径、SHA-256、精确位置与完整上下文。
- 仓位硬件/IO/安全、操作界面、RIoT/RCS 接口、身份认证、车队配置生命周期、业务验收与内部状态/事务派生已分开分类；处置路线分别为追踪证据 52、内部设计隔离 6、车队责任人批准 49、接口责任人批准 11、产品/操作责任人批准 35、安全/硬件责任人批准 54、身份/安全责任人批准 6、上游来源与明确批准 16。
- 所有 52 份草案均固定为未执行证据：没有构建、环境、执行人、时间、实际结果、Pass/Fail 或附件哈希；这些缺口逐条保留在 `approval_gap`，没有把预期结果、`draft`、Git 历史或 FR/UC 指针误作批准或执行结果。
- `TC-044`～`TC-047` 未修改、未复用且未进入当前候选；历史证据账把它们固定到旧提交 `ecd0fd89c51c6602eda13f37b7c2e9fe181e5aad`、各自 TC blob 与旧 `FR-016` blob，四条记录继续是 `not-approved` 的历史验收草案。
- 当前 `FR-016`（总账 `R04-17`、SHA-256 `bd9df8d49efd21941ec36aade3976ca4a0e1ff58eb64cf2626a3796b8ca35920`）的 AC-1～AC-4 已分别建立 `R06-N001`～`R06-N004`，覆盖“立即禁用”、“待禁用”、“启用不覆盖车载硬件不可操作”和“批量独立结果”；这些是新身份，不是旧 TC 的改写、替换身份或批准继承。
- `AD-R06-001` 固定旧稿与当前语义的版本隔离，`EX-R06-001` 固定执行证据缺口，`SB-R06-001` 固定 AGV 启停与仓位启停的对象边界。229 条记录全部 `not-approved`、零永久 `REQ-NNNN`；14 条后出现记录只标记精确重复，没有合并语义近似项，也没有发现必须在其余批次原子化之前新增的独立 HITL 冲突票。

独立失败式 `--verify-only` 通过：`total=229`、`scenario_rows=225`、`new_identity_candidates=4`、`sources=52`、`historical_sources=4`、`duplicates=0`、`approval_upgrades=0`、`exact_duplicate_rows=14`、`evidence_or_scope_rows=72`。XLSX 的 Summary 公式为 229/225/4/4，三类指针命中 4/52/21，53 个来源（含当前 `FR-016` 来源）全部 `OK`，公式错误扫描为零，并完成四张工作表与 Candidates 首尾区域的视觉检查。

本票只分类和隔离既有证据，没有批准新的领域词汇或业务决定，因此未修改根 `CONTEXT.md`。
