# 当前需求基线恢复与版本化治理

Label: wayfinder:map

## Destination

建立首个版本化的“当前需求基线”：在不修改、合并、删除或重写原始需求文档的前提下，只收录经最终批准、来源与适用范围可核查、且已消除已知真实冲突的需求条目，作为后续车载端、服务端与共同协议 spec 的可信输入；同时建立以后新增、修改、废弃需求并发布新基线版本的治理方式。

## Notes

- 本地图只规划并恢复需求基线，不设计系统、不编写正式 spec、不开发代码。
- 使用 `grilling` 处理一切需要业务判断或最终批准的决定；AI 不得代替批准人回答。
- 使用 `domain-modeling` 检查领域词汇，但现有 `CONTEXT.md` 与 ADR 在完成来源和批准状态验证前不自动视为权威需求。
- 证据盘点采用宽口径：当前工作目录中的全部需求性材料，加上验证其来源、批准状态、适用范围、废弃关系或冲突所必需的历史证据。
- 当前 Git 基点（制图时观察）：分支 `szy_document_dev`，HEAD `1469d6309d00b0abb792f6cd686aed68286e638e`。正式证据快照由独立票据生成。
- 当前工作区已有未提交代码修改；它们属于用户现有工作，只登记为工作区状态，不作为正确需求，也不得被本地图工作覆盖。
- 地图与票据是本次新建的治理记录，不代表相关规则在历史上已经存在。

## Decisions so far

- [确定权威等级与分类证据规则](issues/01-authority-and-classification-evidence-rules.md) — 权威性只能来自具名、范围明确且版本绑定的可核查批准证据，不能由文档外观、时间或代码行为推断。
- [确定需求证据盘点边界](issues/02-requirement-evidence-universe.md) — 盘点当前仓库全部需求性材料，并仅在验证当前状态所需时追溯历史或外部引用。
- [确定当前基线的最终批准人](issues/03-final-baseline-approver.md) — 本次基线默认且唯一最终批准人为用户本人，除非其明确认可其他人的授权范围。
- [确定需求确认的条目粒度](issues/04-atomic-requirement-approval-granularity.md) — 默认按可独立判断的需求条目确认，不把整份文档自动视作同一权威单元。
- [确定冲突判定与升级规则](issues/05-conflict-classification-and-hitl-escalation.md) — 只有证据证明范围或版本不同才能判为表面冲突；真实冲突逐项进入 HITL。
- [确定当前基线的历史回溯边界](issues/06-current-baseline-history-boundary.md) — 不恢复完整历史基线，只按需追溯验证当前文档所必需的历史证据。
- [确定当前文档集合的快照方式](issues/07-current-document-snapshot-method.md) — 以实际工作目录、Git 基点、工作区状态和逐文件哈希共同固定盘点对象。
- [确定版本化基线模式](issues/08-versioned-baseline-model.md) — 固定每个已批准版本而非永久冻结需求；未来变更经审查后发布新的当前基线版本。
- [决定基线版本的存储与变更治理形式](issues/09-baseline-release-storage-and-change-governance.md) — 采用不可变版本快照、唯一当前指针、三段式版本号、四项发布凭据、永久需求 ID 与受控变更门禁。
- [固定初始需求证据快照](issues/10-capture-initial-evidence-snapshot.md) — 已固定 Git 基点、原始工作区状态及 1,809 个候选文档的版本控制状态与 SHA-256，独立复核无差异。
- [建立当前需求性材料的无损清单](issues/11-inventory-current-requirement-materials.md) — 1,809 条快照材料已零漏项路由为 13 个候选调查批次、5 个现状证据批次和 1 个仓库治理批次。
- [建立基线条目与变更提案模板](issues/12-create-baseline-record-templates.md) — 已把双层需求记录、永久 ID、独立发布凭据和七步变更门禁固化为可复核模板。
- [调查客户、项目协议与原始需求输入](issues/13-investigate-customer-project-source-materials.md) — R01 的 19 份材料均已逐件分类，但现有证据不足以在文档级批准任何当前需求。

## Not yet specified

- 证据调查完成后，生成文档级与原子需求级分类票据；在此之前不预判任何材料的权威等级。
- 冲突扫描完成后，把每一项需要业务判断的真实冲突分别生成 HITL grilling ticket；尚未知晓冲突内容，当前不能预先切票。
- 候选基线条目形成后，按可审查批次生成最终批准票据；只有批准结果可以进入首个基线版本。
- 批准完成后，生成首个可独立阅读、保留统一规范文本与不可变原始证据的当前需求基线版本；具体发布任务等待候选条目与批准批次明确后再生成。

## Out of scope

- 车载端、服务端和共同协议的正式 spec 编写。
- 系统设计、架构选择、接口设计和代码开发。
- 将当前代码行为自动认定为正确需求。
- 修改、合并、删除或静默改写任何原始需求文档。
- 为来源未知、范围不明或缺少批准证据的内容补全背景或猜测含义。
- 恢复与验证当前需求无关的完整项目历史。
