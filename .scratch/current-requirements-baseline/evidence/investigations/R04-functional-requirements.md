# R04 功能需求材料调查

## 边界、身份与方法

本资产只调查[material-inventory.tsv](../material-inventory/material-inventory.tsv) 中 `batch_id=R04` 的 41 行：31 份 FR、8 份“暂无 FR”领域占位 README、1 份 FR 模板指南和 1 份根索引。对清单每一路径重新执行 `Get-FileHash -Algorithm SHA256 -LiteralPath <path>`：**41/41 匹配，0 哈希漂移**；字节数、快照 `git_status` 和 `last_write_utc` 仍以清单为准。下表使用 SHA-256 前 12 位，完整值可在清单逐行对账。

调查依据[01 权威与分类证据规则](../../issues/01-authority-and-classification-evidence-rules.md)、[04 需求批准的条目粒度](../../issues/04-atomic-requirement-approval-granularity.md)与[06 历史回溯边界](../../issues/06-current-baseline-history-boundary.md)。方法为：

1. 逐文件读取 frontmatter、Description、Origin、Acceptance Criteria (AC)、Related、Verification 和 Notes；对 `related_uc`/`related_br` 中 28 个唯一 ID 在 `requirement-documents` 内反查，**28/28 有对应源文件，0 断链**。
2. 使用 `git log --follow --format='%h|%aI|%an|%s' --name-status -- <path>` 回溯必要形成历史。根索引在 `96eb203` (2026-07-13 08:32 +08:00) 引入；FR-001∼030、8 份占位、指南及当前索引结构于 `ecd0fd8` (2026-07-15 12:58) 成批形成；`493ac5a` (2026-07-31 18:33) 实质改写 FR-002∼014、16/17/19/21 并新增 FR-031。
3. 每份 FR 的 AC 是后续原子分类的起始指针，不自动是最终原子粒度；一个 AC 若同时含硬件、动作、错误处置和审计，仍须拆分。R04 共有 **146 个 AC 候选**。

## 批准与派生共性结论

- 31/31 FR 均为 `status: draft`，`created_by`/`updated_by` 均是内部编辑元数据；未发现任何“具名授权人 + 批准日期 + 适用范围 + 具体版本/哈希”证据。**Git 作者/提交者、`draft`/`accepted`/Origin 标签、内部 ADR 状态、已关联 TC 或代码现状都不是需求批准。**
- 31 份 FR 均是从 UC/BR/ADR 拆解的**内部派生功能要求候选**，不是原始客户输入。22/31 有独立 `Origin` 节；FR-003∼007、11∼013、16 缺少 `Origin` 节，只能从 frontmatter/Related/Notes 恢复派生关系，追溯链弱一级。
- FR-003∼007、11∼013 在 `493ac5a` 中改成 StopClosure/LoadCorrection/OperationSession 等新语义；Notes 明说旧语义被 ADR-cross-0054/0055 替代或保留编号以维持链接。[ADR-cross-0054](../../../../docs/adr/cross/0054-auto-load-commit-with-pre-departure-correction.md)、[ADR-cross-0055](../../../../docs/adr/cross/0055-server-owned-station-departure-wait-timeout.md) 虽标 `accepted`，但未附本次基线规则要求的业务授权批准链，只能证明内部设计派生/替代历史。

## 41/41 文档级证据矩阵

编码：`96`=`96eb203`，`ec`=`ecd0fd8`，`49`=`493ac5a`。“无批准”只表示本批证据不足，不表示内容错误或已废弃。

| # | 固定材料（SHA 前 12）/历史 | 来源与派生关系 | 批准、当前适用性与后续原子指针 |
|---:|---|---|---|
| 01 | [FR-001](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-001-sublot-task-validity-and-dispatch-range-check.md) `a63fc423be38`；`ec` | Origin: UC-001 + BR-001 | `draft`、无批准；站点作业内部派生候选；按 AC-1∼4 拆任务存在/范围/服务失败。 |
| 02 | [FR-002](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-002-slot-unlock-occupancy-confirm-and-state-persist.md) `e67684f850cc`；`ec→49` | UC-001/004/014 + BR-013；后期大幅改写硬件恢复语义 | `draft`、无批准；高相关但安全/补偿混合；按 AC-1∼16 逐条拆开锁、光幕、占用、补偿决策与恢复。 |
| 03 | [FR-003](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-003-confirm-completion-eligibility-check.md) `6a7072536249`；`ec→49` | 无 Origin 节；Related 指 UC-002/046，Notes 指 ADR-0054/0055 替代旧语义 | `draft`、无批准；当前是 StopClosure 内部派生版；AC-1∼3。 |
| 04 | [FR-004](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-004-batch-task-completion-session-closure-and-non-reversibility.md) `4f34327fada4`；`ec→49` | 无 Origin；UC-002/046 + FR-003/013/031，Notes 明示 LoadBatch 替代旧“批量确认” | `draft`、无批准；内部 StopClosureCommit 设计；AC-1∼4 拆原子提交/会话/投影/移动失败。 |
| 05 | [FR-005](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-005-mis-stored-retrieval-eligibility-check.md) `ba4726149cbd`；`ec→49` | 无 Origin；Related 指 UC-005/FR-006，为 LoadCorrection 重写 | `draft`、无批准；内部纠错授权候选；AC-1∼2。 |
| 06 | [FR-006](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback.md) `5114f3db3d3a`；`ec→49` | 无 Origin；UC-005/004/006 + FR-005/007/031，为原仓位纠错/待重放设计 | `draft`、无批准；AC-1∼6 分联锁、单仓、重放、Pending、出口、自动重开。 |
| 07 | [FR-007](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-007-task-cancellation-eligibility-check-and-state-rollback.md) `a68a4c65a9e8`；`ec→49` | 无 Origin；UC-006 + FR-006，为离站前清空/取消重写 | `draft`、无批准；AC-1∼10 含任务终态、硬件闭环、多 SUBLOT 隔离与补偿权限，必须继续拆分。 |
| 08 | [FR-008](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-008-destination-station-auto-identify-and-batch-unlock.md) `b6cd2f5524eb`；`ec→49` | Origin: UC-010/004 + BR-013/014 | `draft`、无批准；卸货内部派生候选；AC-1∼6。 |
| 09 | [FR-009](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation.md) `a84dc7ee55a0`；`ec→49` | Origin: UC-010 + BR-013；Related 另指 UC-044 | `draft`、无批准；卸货残留/回滚候选；AC-1∼2。 |
| 10 | [FR-010](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-010-arrival-status-update-and-operation-panel-navigation.md) `701bbbcb942f`；`ec→49` | Origin: UC-003 + BR-001 | `draft`、无批准；到站投影/HMI 内部派生；AC-1∼7。 |
| 11 | [FR-011](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-011-identity-and-role-verification-via-mes.md) `93dbc4bd5528`；`ec→49` | 无 Origin；Related 只指 UC-043，正文新增 8005 装货开/卸货关策略 | `draft`、无批准；项目级身份策略须特别追回具名业务/IT 批准；AC-1∼4。 |
| 12 | [FR-012](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-012-session-establishment-reuse-and-lock-stage-transition.md) `56a57678899c`；`ec→49` | 无 Origin；UC-043/001/005/010/044，混合生产操作员与 R-09 独立审批身份 | `draft`、无批准；会话/绑定内部设计；AC-1∼5。 |
| 13 | [FR-013](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-013-session-termination-rules.md) `e8fa72726ab2`；`ec→49` | 无 Origin；UC-043/002/006/046 + FR-004/011/012/031 | `draft`、无批准；会话结束/恢复内部设计；AC-1∼4。 |
| 14 | [FR-014](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration.md) `4fe50e146f6c`；`ec→49` | Origin: UC-044 + UC-004；Related 另指 UC-010/002 | `draft`、无批准；残留仓位恢复候选；AC-1∼4。 |
| 15 | [FR-031](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-031-station-departure-wait-timeout-and-auto-closure.md) `69484156ab84`；`49` | Origin 自述 2026-07-30∼31 “需求确认会话” + UC-046 + ADR-0055；会话未导出/具名 | `draft`、无批准；内部超时自动结束候选；AC-1∼12，默认 5 分钟及 HMI 阈值优先追原始决定。 |
| 16 | [FR-015](../../../../requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-015-slot-monitoring-dashboard-display-and-refresh.md) `fd47600ad362`；`ec` | Origin: UC-011 | `draft`、无批准；硬件看板内部派生；AC-1∼2。 |
| 17 | [FR-016](../../../../requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-016-slot-enable-disable-batch-eligibility-and-state-update.md) `bd9df8d49efd`；`ec→49` | 无 Origin；Related 只指 UC-014，后期改写为管理状态 + 车载可操作性 | `draft`、无批准；内部状态模型；AC-1∼4，将立即/待生效/硬件故障/批量结果拆开。 |
| 18 | [FR-017](../../../../requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-017-slot-door-unlock-open-test-and-result-recording.md) `a6ffae552466`；`ec→49` | Origin: UC-015 | `draft`、无批准；硬件测试能力候选；AC-1∼3。 |
| 19 | [FR-018](../../../../requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-018-slot-light-curtain-function-test.md) `999d4ea4a140`；`ec` | Origin: UC-016 | `draft`、无批准；光幕测试能力候选；AC-1∼4。 |
| 20 | [FR-019](../../../../requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-019-slot-door-state-detection-test.md) `1d38c8eb2561`；`ec→49` | Origin: UC-017 | `draft`、无批准；锁反馈/闩合测试候选；AC-1∼4；不用测试通过反推需求正确。 |
| 21 | [FR-020](../../../../requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-020-bidirectional-io-point-mapping-verification.md) `54c87508a160`；`ec` | Origin: UC-018 | `draft`、无批准；IO 点位核对能力候选；AC-1∼3。 |
| 22 | [FR-021](../../../../requirement-documents/04-functional-requirements/02-slot-and-hardware/fr-021-slot-to-io-point-mapping-create-modify-validation.md) `5f2b14ff9d54`；`ec→49` | Origin: UC-039；下游依赖 FR-020 | `draft`、无批准；映射维护能力候选；AC-1∼3。 |
| 23 | [FR-022](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-022-slot-model-draft-field-and-layout-validation.md) `b9f233de0603`；`ec` | Origin: UC-038 + BR-008 | `draft`、无批准；车队模型草稿校验候选；AC-1∼5。 |
| 24 | [FR-023](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-023-slot-model-publish-with-dual-authentication-and-immutable-versioning.md) `eb69554a831b`；`ec` | Origin: UC-038 + BR-008 | `draft`、无批准；发布/二次认证/不可变版本候选；AC-1∼4。 |
| 25 | [FR-024](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-024-slot-model-retire-with-dual-authentication-and-historical-reference-preservation.md) `3636ffb7e73c`；`ec` | Origin: UC-038 + BR-008 | `draft`、无批准；停用/历史引用保留候选；AC-1∼3。 |
| 26 | [FR-025](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-025-agv-registration-eligibility-and-slot-model-version-validation.md) `a367b1873538`；`ec` | Origin: UC-019；Related BR-002/008 | `draft`、无批准；AGV 接入资格/模型版本候选；AC-1∼4。 |
| 27 | [FR-026](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-026-atomic-agv-record-creation-slot-instance-generation-and-audit-logging.md) `dbef8d3f895c`；`ec` | Origin: UC-019 + BR-008；Related 另指 BR-002 | `draft`、无批准；档案/仓位实例原子创建候选；AC-1∼2 仍需拆创建、回滚和审计。 |
| 28 | [FR-027](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-027-agv-enable-disable-state-transition-and-pending-effect-handling.md) `201734b6cd7c`；`ec` | Origin: UC-013；Related BR-002 | `draft`、无批准；AGV 启停/待生效候选；AC-1∼5。 |
| 29 | [FR-028](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-028-agv-dispatch-profile-update-eligibility-and-persistence.md) `534426abe57c`；`ec` | Origin: UC-020；Related BR-002/008 | `draft`、无批准；调度配置维护候选；AC-1∼4。 |
| 30 | [FR-029](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-029-agv-archive-eligibility-check-and-state-transition.md) `0ff294b8a110`；`ec` | Origin: UC-021；Related BR-002 | `draft`、无批准；AGV 归档资格/状态迁移候选；AC-1∼4。 |
| 31 | [FR-030](../../../../requirement-documents/04-functional-requirements/03-agv-fleet-management/fr-030-agv-fleet-dashboard-display-and-eligibility-reasoning.md) `ce066e951945`；`ec` | Origin: UC-022；Related BR-002 | `draft`、无批准；车队看板/可分配原因候选；AC-1∼3。 |
| 32 | [04-transport-task-dispatch/README.md](../../../../requirement-documents/04-functional-requirements/04-transport-task-dispatch/README.md) `2b288f6ad5ed`；`ec` | 只指向 UC-007/008/009/023/042 和分类规则，明示“暂无 FR” | 无批准对象；**占位索引/完整性缺口记录**，不生成功能需求；后续从所列 UC 拆分。 |
| 33 | [05-agv-charging/README.md](../../../../requirement-documents/04-functional-requirements/05-agv-charging/README.md) `5c4ec9ed7505`；`ec` | 指 UC-012/037，明示暂无 FR | 无批准对象；**占位索引**，不生成需求。 |
| 34 | [06-area-station-mapping/README.md](../../../../requirement-documents/04-functional-requirements/06-area-station-mapping/README.md) `f1524213b582`；`ec` | 指 UC-024/045，明示暂无 FR | 无批准对象；**占位索引**，不生成需求。 |
| 35 | [07-workflow-engine/README.md](../../../../requirement-documents/04-functional-requirements/07-workflow-engine/README.md) `7133c8d6bd83`；`ec` | 指 UC-025∼029，明示暂无 FR | 无批准对象；**占位索引**，不生成需求。 |
| 36 | [08-user-and-access/README.md](../../../../requirement-documents/04-functional-requirements/08-user-and-access/README.md) `918ddbb467e8`；`ec` | 指 UC-030∼033，明示暂无 FR | 无批准对象；**占位索引**，不生成需求。 |
| 37 | [09-logs-and-audit/README.md](../../../../requirement-documents/04-functional-requirements/09-logs-and-audit/README.md) `d9c2944a6d32`；`ec` | 指 UC-034∼036，明示暂无 FR | 无批准对象；**占位索引**，不生成需求。 |
| 38 | [10-safety-and-interlock/README.md](../../../../requirement-documents/04-functional-requirements/10-safety-and-interlock/README.md) `0f74cb956732`；`ec` | 指 UC-004，并记录其仅作 FR-002/006/008/009/014 次要关联，暂无主派生 FR | 无批准对象；**占位/追溯结构说明**，不独立生成安全需求。 |
| 39 | [11-agv-parking/README.md](../../../../requirement-documents/04-functional-requirements/11-agv-parking/README.md) `95c7dc7a1af7`；`ec` | 指 UC-040/041，明示暂无 FR | 无批准对象；**占位索引**，不生成需求。 |
| 40 | [fr-template-guide.md](../../../../requirement-documents/04-functional-requirements/fr-template-guide.md) `56dd687c05f6`；`ec` | `type: template-guide,status: reference`；以 FR-001/002 为范例规定 BR→UC→FR→TC、Origin、G/W/T 和粒度 | 无业务批准对象；**纯写作/记录指南**，可约束形式但不表达系统功能要求。 |
| 41 | [04-functional-requirements/README.md](../../../../requirement-documents/04-functional-requirements/README.md) `ad99bf90ceba`；`96→ec` | 根索引：模板、指南、“黄金样例”、frontmatter 追溯与领域分类 | 无业务批准对象；**导航/编辑索引**；“黄金样例”是写作参考，不赋予 FR-001/002 批准性。 |

## 结论、当前适用性与后续证据请求

1. **文档级分类：**31 份为内部派生的 draft 功能要求候选，8 份为占位/完整性索引，1 份为写作指南，1 份为目录入口。**0/41 是可证明的原始需求载体，0/41 可由本批证据批准进入当前基线。**
2. **当前适用性：**31 份 FR 可作为当前仓库设计/测试追溯的候选中间层，但不能因下游 TC 存在、实现相符或 ADR `accepted` 而反推为正确需求。FR-003∼014/016/017/019/021/031 的 `49` 版本应与 `ec` 旧版语义隔离，旧版不得默认继承新版的任何确认，反之亦然。
3. **原子化路由：**以 146 个 AC 为定位指针，每条记录 Description/AC 原文、R04 哈希、对应 UC 流程及 BR 条款；将权限、安全联锁、状态迁移、幂等/原子性、错误处置、HMI 呈现和审计分成可独立判断的条目。Verification 中的 TC 只是验证指针，不是批准证据。
4. **后续证据请求：**为每个上游 UC/BR 及 2026-07-30∼31 “需求确认会话”补齐原始记录、具名授权人、日期、适用 8005/车型/站点/发布阶段范围和哈希；为 MES 身份/权限、RIoT 状态、IO/锁/光幕、默认 5 分钟、二次认证和补偿决策另行取得相应权威方证据。若合格来源在同范围冲突，建立独立 HITL 票，本调查不自行裁决。
