# 当前需求基线版本模板

> 使用规则：本文件只定义版本化需求内容。候选实例的文件名必须使用 `current-requirements-v<version>-draft.<n>.md`；最终批准人按文件 SHA-256 批准冻结内容后，才能以完全相同的字节发布为 `current-requirements-v<version>.md`。正式状态由不可变的旁置发布记录证明，不能靠本文件自称“approved”。`requirements/current-baseline.md` 只能指向正式发布版本；发布后本文件不可修改。

## 版本元数据

- Target Baseline Version: `v<major>.<minor>.<patch>`
- Previous Approved Version: `<none | v<major>.<minor>.<patch>>`
- Intended File: `requirements/baselines/current-requirements-v<major>.<minor>.<patch>.md`
- Prepared At: `<YYYY-MM-DDTHH:mm:ssZ>`
- Applicable Scope: `<本版本整体适用的车辆、站点、子系统、业务场景、生命周期阶段或其他边界>`

## 相对上一批准版本的变化

### Added

- `<REQ-NNNN — 一行摘要；无则写 None>`

### Modified

- `<REQ-NNNN — 一行摘要及获批变更提案链接；无则写 None>`

### Deprecated

- `<REQ-NNNN — 一行摘要、替代项（如有）及获批变更提案链接；无则写 None>`

## Requirements

<!-- 每项可独立判断的需求复制一份下列条目。文件是证据载体，不自动成为一个不可拆分的批准单元。 -->

### `REQ-NNNN` — `<稳定、简短的标题>`

- Lifecycle: `<active | deprecated>`
- Scope: `<车载端 | 服务端 | 共同协议 | 跨域 | 其他；以及车辆、站点、业务场景、生命周期阶段等适用边界>`
- Introduced In: `v<major>.<minor>.<patch>`
- Last Meaning Change In: `v<major>.<minor>.<patch>`
- Supersedes: `<none | REQ-NNNN[, REQ-NNNN...]>`
- Deprecated In: `<none | v<major>.<minor>.<patch>>`
- Change Proposal: `<none（首版恢复）| 获批变更提案的仓库相对链接>`

#### Current Requirement

<后续开发与 spec 必须遵守的唯一规范文本。若 Lifecycle 为 deprecated，明确写明该要求已废弃且不再形成当前义务；不得删除旧 ID。>

#### Evidence

##### 原始证据

- Source: `<原始材料的仓库相对路径或稳定外部标识>`
- Exact Location: `<标题、段落、表格、页码、行号或其他可复核定位>`
- Verbatim Extract: `<支持本需求的原始摘录；不得用 AI 概括替代>`
- Source Version: `<文档版本、Git commit、会议记录版本或等价标识>`
- Snapshot SHA-256: `<64 位十六进制哈希；外部证据不适用时说明可复核方式>`
- Source Date: `<可核查日期或 unknown>`
- Source Scope: `<该证据明确适用的范围；未知时不得猜测>`
- Source Authority: `<具名来源人或组织及其角色；未知时写 unknown>`

<!-- 有多项原始证据时重复“原始证据”块，不得把多个来源压成不可追溯的概括。 -->

##### 规范文本形成方式

- Derivation: `<verbatim | merged | disambiguated | reworded>`
- Transformation Trace: `<verbatim 时写 none；否则逐项链接输入证据并说明语义如何保持>`
- AI Involvement: `<none | generated | modified>`
- Conflict Assessment: `<none found | apparent—范围/版本证据链接 | resolved real conflict—HITL 票据链接>`

##### 条目批准记录

- Approver: `<具名最终批准人>`
- Approved At: `<YYYY-MM-DDTHH:mm:ssZ>`
- Approved Scope: `<批准覆盖的精确适用范围>`
- Approved Text Identity: `<本条 Current Requirement 的 SHA-256，或绑定其精确版本/差异的等价标识>`
- Approval Evidence: `<票据、会议记录或等价证据的仓库相对链接>`
- Authority Evidence: `<若非本次默认最终批准人，链接其授权范围证据；否则写 map decision>`

---

## 冻结内容检查

- [ ] 每个有效条目都有唯一且永久的 `REQ-NNNN`；ID 无业务分类含义、未复用。
- [ ] 每个条目都同时具有唯一规范性的 `Current Requirement` 与可复核的 `Evidence`。
- [ ] 合并、消歧或重写的文本已标明 AI 参与，并获得最终批准人对精确文本的逐条批准。
- [ ] 已知真实冲突均已通过所链接的 HITL 决策解决；疑似冲突未被擅自解释。
- [ ] 相对上一版本的新增、修改、废弃与获批变更提案可相互核对。
- [ ] 版本号与变化类型一致；任何可能改变含义的变化均未使用补丁版本。
- [ ] 候选文件已经冻结并计算 SHA-256；批准后发布到最终路径时不改变任何字节。
- [ ] 旁置发布记录将绑定最终文件、SHA-256、对应 Git commit、带说明 Git tag 和版本批准证据。
- [ ] 正式发布完成后才将 `requirements/current-baseline.md` 的唯一指针更新到本版本。

