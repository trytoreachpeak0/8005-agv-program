# 需求变更提案模板

> 使用规则：每个提案只描述一组可由最终批准人独立判断的精确变化。提案在全部门禁通过并批准前始终是候选内容，不得修改已批准基线，也不得进入 `requirements/current-baseline.md`。

## 提案元数据

- Proposal ID: `<CHANGE-YYYY-NNNN 或仓库票据标识>`
- Status: `<draft | evidence-verified | impact-reviewed | awaiting-HITL | awaiting-approval | approved | rejected | released>`
- Operation: `<add | modify | deprecate>`
- Related Requirement ID: `<add 时写 new；modify/deprecate 时写 REQ-NNNN>`
- Base Approved Baseline: `v<major>.<minor>.<patch>`
- Target Baseline: `v<major>.<minor>.<patch>[-draft.<n>]`
- Proposer: `<具名人员或系统>`
- Proposed At: `<YYYY-MM-DDTHH:mm:ssZ>`

## 精确变化

### Current Requirement

<add 时写 none；modify/deprecate 时逐字复制当前批准基线中的规范文本，并链接原条目。>

### Proposed Requirement

<add/modify 时写拟议的完整规范文本；deprecate 时明确写明废弃后的当前义务及 Supersedes/替代关系。>

### Exact Diff

```diff
<当前批准文本与拟议完整文本之间的精确差异；add/deprecate 也必须能明确看出增加或撤销的义务>
```

### Reason

<为什么需要这项变化；事实与建议分开陈述。>

## 来源与适用范围验证

- Source: `<原始材料路径或稳定外部标识>`
- Exact Location: `<标题、段落、表格、页码、行号或其他精确定位>`
- Verbatim Extract: `<支持变化的原始摘录>`
- Source Version: `<文档版本、Git commit、会议记录版本或等价标识>`
- Evidence SHA-256: `<64 位十六进制哈希；不适用时说明稳定复核方式>`
- Source Date: `<可核查日期或 unknown>`
- Source Authority: `<具名来源人或组织及其角色；未知时写 unknown>`
- Proposed Scope: `<车载端、服务端、共同协议、跨域或其他，以及车辆、站点、业务场景、生命周期阶段等边界>`
- Scope Evidence: `<证明上述范围的精确证据；没有证据时明确写 unresolved>`
- Authority/Approval Evidence: `<证明来源权威或授权范围的记录；没有时明确写 unresolved>`
- Verification Result: `<verified | unresolved | rejected>`

<!-- 有多项来源时复制上述字段，保留逐项版本、定位、哈希、范围和权威链。 -->

## 影响分析

| Area | Impact | Affected requirements/artifacts | Required follow-up |
|---|---|---|---|
| OnboardHmi / 车载端 | `<none | summary>` | `<REQ ID 或路径>` | `<none | action/ticket>` |
| ControlServer / 服务端 | `<none | summary>` | `<REQ ID 或路径>` | `<none | action/ticket>` |
| Common protocol / 共同协议 | `<none | summary>` | `<REQ ID 或路径>` | `<none | action/ticket>` |
| Other requirements / 其他需求 | `<none | summary>` | `<REQ ID>` | `<none | action/ticket>` |

### Compatibility and versioning

- Meaning Change: `<yes | no，并说明依据>`
- Compliance Result Invalidated: `<yes | no，并说明依据>`
- Required Version Change: `<major | minor | patch>`
- Version Rationale: `<新增且不改变既有义务 / 修改、废弃、范围改变或旧合规失效 / 仅错字、链接、证据定位或元数据>`

## 冲突分析

- Compared Requirements/Evidence: `<REQ ID 与证据链接>`
- Result: `<no conflict | apparent conflict | suspected conflict | real conflict>`
- Basis: `<仅可用可核查的版本、范围等证据解释表面冲突；不得以时间较新作为替代证据>`
- Unresolved Questions: `<none | 逐项列出>`
- HITL Decision Ticket: `<none | grilling ticket link>`
- HITL Resolution Evidence: `<none | resolution link>`

## 最终批准

- Decision: `<pending | approved | rejected>`
- Approver: `<具名最终批准人；AI 不得填写为批准人>`
- Approved/Rejected At: `<YYYY-MM-DDTHH:mm:ssZ>`
- Approved Scope: `<批准覆盖的精确适用范围>`
- Approved Exact Diff Identity: `<Exact Diff 的 SHA-256 或绑定该精确差异的等价标识>`
- Approval Evidence: `<票据、会议记录或等价证据链接>`
- Authority Evidence: `<若非本次默认最终批准人，链接其授权范围证据；否则写 map decision>`
- Decision Notes: `<none | 附加限制；不得暗中改变已批准差异>`

## 变更门禁

- [ ] `1. Proposal`：操作类型、相关需求 ID、基线版本、原文本、拟议文本、精确差异和理由完整。
- [ ] `2. Source & Scope`：来源、版本、精确位置、哈希、权威链和适用范围已验证。
- [ ] `3. Impact & Conflict`：车载端、服务端、共同协议、其他需求、版本影响及冲突已分析。
- [ ] `4. HITL`：所有真实或无法排除的冲突均已有独立 HITL 决策，或明确记录为无需 HITL。
- [ ] `5. Final Approval`：最终批准人已批准绑定身份的精确差异和适用范围。
- [ ] `6. New Version`：已把获批差异生成到新的候选基线版本，并完成版本级复核与发布凭据。
- [ ] `7. Current Pointer`：新版本正式发布后，才更新 `requirements/current-baseline.md` 的唯一指针。

## 发布结果

- Released Baseline: `<pending | v<major>.<minor>.<patch>>`
- Requirement ID Result: `<new REQ-NNNN | retained REQ-NNNN | deprecated REQ-NNNN; superseded by REQ-NNNN | not released>`
- Versioned File: `<pending | requirements/baselines/current-requirements-v<major>.<minor>.<patch>.md>`
- File SHA-256: `<pending | 64 位十六进制哈希>`
- Git Commit: `<pending | 40 位 commit>`
- Annotated Git Tag: `<pending | requirements-baseline-v<major>.<minor>.<patch>>`
- Current Pointer Updated At: `<pending | YYYY-MM-DDTHH:mm:ssZ>`
