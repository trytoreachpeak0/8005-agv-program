# 建立基线条目与变更提案模板

Type: task
Status: resolved
Blocked by: 09

## Question

如何把已确认的存储模型、永久需求 ID、`Current Requirement`/`Evidence` 双层结构、版本元数据、批准记录和变更门禁固化为一致的基线条目模板与变更提案模板，以便后续盘点和批准工作不丢失必要证据？

## Answer

已把前置票据确定的治理规则固化为三个可复制、可逐项检查的模板资产：

- [当前需求基线版本模板](../evidence/templates/baseline-record-template.md)：定义目标版本元数据、相对上一版本的 Added/Modified/Deprecated 清单，以及逐条 `REQ-NNNN` 的 `Current Requirement`/`Evidence` 双层记录。Evidence 强制保留原始路径、精确位置、逐字摘录、版本、SHA-256、来源日期、适用范围与权威链；合并、消歧或重写必须记录转换链、AI 参与、冲突处理和绑定精确文本的条目批准。
- [当前需求基线发布记录模板](../evidence/templates/baseline-release-record-template.md)：作为版本文件的不可变旁置记录，绑定完整版本文件、文件 SHA-256、对应 Git commit、带说明 Git tag 和具名版本批准记录，并记录版本分类、变更提案和唯一当前指针。旁置设计避免版本文件保存自身哈希或包含自身的 commit 所造成的循环引用。
- [需求变更提案模板](../evidence/templates/change-proposal-template.md)：固定 add/modify/deprecate、相关永久 ID、原文本、拟议完整文本、精确 diff、理由、来源与范围证据、跨车载端/服务端/共同协议/其他需求的影响、冲突/HITL 结果、版本影响和最终批准记录；末尾按既定顺序设置七道门禁，批准前不能进入当前基线。

候选版本只使用 `-draft.N` 文件名。内容冻结并计算 SHA-256 后，由最终批准人批准该精确内容；发布到最终文件名时不得改变任何字节。正式状态由旁置发布记录和 Git 证据共同证明，不能由候选文件自称已批准。已分配的永久需求 ID 不复用，语义修改保留 ID，本质替代使用新 ID 和 `Supersedes`，废弃 ID 保留而不删除。

领域词汇检查未发现需要写入 `CONTEXT.md` 的新项目业务术语：这些模板是本地图新建立的需求治理记录，不是已恢复的 AGV 领域事实，因此保持在地图证据资产中。

结构校验已通过：三个文件存在；基线模板具备永久 ID、`Current Requirement`、`Evidence` 与条目批准；发布记录具备四项正式发布凭据且无自身哈希/commit 回填；变更模板具备所有必填区块和七道门禁；三个文件均无行尾空白。
