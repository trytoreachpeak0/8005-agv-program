# R05 现场操作验收场景调查

## 调查边界与方法

本报告只调查 [material-inventory.tsv](../material-inventory/material-inventory.tsv) 第 1608～1674 行中 `batch_id=R05` 的 67 份现场操作 TC；不把其它批次材料混入结论。逐文件以 PowerShell `Get-FileHash -Algorithm SHA256 -LiteralPath <path>` 重算：**67/67 与清单固定 SHA-256 匹配，0 漂移**；清单中的 67 行也全部仍为 `tracked-clean`。下表显示 SHA-256 前 12 位，完整值仍由固定清单保存。

证据判断遵循[权威与分类规则](../../issues/01-authority-and-classification-evidence-rules.md)、[原子批准粒度](../../issues/04-atomic-requirement-approval-granularity.md)和[历史回溯边界](../../issues/06-current-baseline-history-boundary.md)：具名授权人、日期、适用范围与具体版本或等价对象必须同时可核查；Git 作者、提交信息、`status` 字段、文内“用户确认/需求确认”、实现现状和表面合理性都不构成批准。调查使用仓库当前文档、逐路径 `git log --follow`、相关 FR/UC/BR/ADR 和当前代码测试引用作为一手证据，没有使用二手总结替代源文件。

## 结论

- **已批准验收标准：0/67。** 67 份 TC 均为 `status: draft`，没有 Source/Origin 节、具名批准人、批准日期、批准动作、批准范围或绑定本文件哈希/提交的记录。它们引用的 13 份 FR（FR-002～014、FR-031）及相关 UC 也全部仍是 `draft`。
- **待送审的验收场景候选：67/67。** 每份都给出前置条件、步骤、预期结果和具体 FR/AC 指针，形式上适合作为原子验收讨论入口；这只说明可评审性，不说明内容真实、当前适用或已批准。
- **内部派生草稿：67/67。** [测试用例目录说明](../../../../requirement-documents/05-test-cases/README.md)第 5～10 行明确 TC 是由 FR 的 Given/When/Then 派生并通过 `related_fr`/`related_uc` 建立追踪；R05 没有任何 TC 直接指向客户合同、签批件、原始会议/对话或现场执行记录。
- **设计推演成分显著：至少 29/67。** `493ac5a` 一次新增的 TC-017、TC-098～123 直接固化了取消抑制、服务端原子提交、并发裁决、恢复授权、即时二次认证、受控原因码等内部架构/状态机设计；TC-020/021 还把 Modbus `0x0F` 与跨模块并行作为预期行为。这些是有价值的设计验证草案，但必须分别取得业务、安全、运维或接口责任人的范围确认。
- **当前测试执行证据：0/67。** 这些文件只有设计字段，没有执行人、环境/软硬件版本、执行时间、实际结果、Pass/Fail、缺陷号或附件。全仓检索 R05 TC 编号，代码测试中无对应引用；匹配只出现在 TC、FR、README/分类说明。现有 MesIngest 与 RIoT SDK 自动化测试不能被推定为执行了这些现场场景。
- **当前适用性：对当前 8005 内部模型高度相关，但未获基线权威。** 现行 `CONTEXT.md` 与 `accepted` 的 cross ADR 使用同一套 LoadBatch、StopClosureCommit、LoadCompensationDecision、StationDepartureWaiting 等语言，且未发现后来明确废弃这 67 份当前内容的证据；不过 ADR 的 `accepted` 没有记录具名授权人、批准日期/范围或批准对象哈希，因此只能证明仓库内部设计决定，不能升级为客户验收批准。
- **AI 分类：无直接证据。** 未发现能把某个 TC 具体版本绑定到 AI 生成/修改行为的记录，所以不能擅自归为“AI 生成或修改但尚未确认”；在现有证据下统一归为“可追溯到未批准内部上游的派生草稿”。

## Git 形成历史

`git log --follow` 只形成三组：

- **H1（31 份）：** `ecd0fd8`（2026-07-15 12:58 +08:00，Zhengyu Shao）首次纳入，`493ac5a`（2026-07-31 18:33 +08:00，同一作者）改写。包括 TC-001～016、TC-020/021、TC-023、TC-027～037、TC-041。
- **H2（27 份）：** 仅 `493ac5a` 新增。包括 TC-017、TC-098～123。文件 frontmatter 的 `created` 日期不等于可核查的首次 Git 形成日期。
- **H3（9 份）：** 仅 `ecd0fd8` 新增，之后无 Git 修改。包括 TC-018/019、TC-022、TC-024～026、TC-038～040。

`ecd0fd8` 的提交说明主要描述 RCS Insight/SDK 验证套件，`493ac5a` 的说明是记录车载—服务端权威和站点操作 ADR；两者都没有批准动作、批准范围或外部签批附件。提交者与文档作者只能证明形成历史，不能证明需求权威。

## 上游派生链与批准范围

| 上游 | R05 中显式验证 | 可核查来源链与性质 | 批准/适用结论 |
|---|---|---|---|
| [FR-002](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-002-slot-unlock-occupancy-confirm-and-state-persist.md) | TC-113～118、120、122、123 | 指向 UC-001/004/014、BR-013，并与 [ADR-cross-0036](../../../../docs/adr/cross/0036-load-batch-commit-and-hardware-fault-hold.md)、[ADR-cross-0039](../../../../docs/adr/cross/0039-operator-starts-server-authorized-load-compensation.md)、[ADR-cross-0054](../../../../docs/adr/cross/0054-auto-load-commit-with-pre-departure-correction.md)一致 | FR/UC 为 draft；ADR 为内部 accepted 设计，无合格业务批准链。仅适合作为装货、故障保持、恢复与补偿候选。 |
| [FR-003](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-003-confirm-completion-eligibility-check.md)、[FR-004](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-004-batch-task-completion-session-closure-and-non-reversibility.md) | TC-001～006 | 由 UC-002/046 派生；当前语义明确被自动 LoadBatch 提交与 StopClosureCommit 重塑，并与 [ADR-cross-0055](../../../../docs/adr/cross/0055-server-owned-station-departure-wait-timeout.md)一致 | 是当前内部整站结束候选，不是已批准验收。原“批次人工确认”语义已被内部设计替换，必须按当前原子条目重新确认。 |
| [FR-005](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-005-mis-stored-retrieval-eligibility-check.md)、[FR-006](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-006-multi-slot-unlock-retrieval-and-occupancy-rollback.md) | TC-007～014 | 由 UC-005 派生，并吸收 ADR-cross-0054 的提交后、整站结束前原仓位纠错边界 | 当前内部纠错模型候选；无操作员/生产负责人对次数、权限、原仓位限制的批准。 |
| [FR-007](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-007-task-cancellation-eligibility-check-and-state-rollback.md) | TC-015～017、098～102、119 | 由 UC-006 派生，并具体化 [ADR-cross-0046](../../../../docs/adr/cross/0046-load-task-cancellable-until-departure-after-full-clearance.md)、[ADR-cross-0047](../../../../docs/adr/cross/0047-demand-id-identifies-station-task-and-cancellation.md)、[ADR-cross-0052](../../../../docs/adr/cross/0052-onboard-clears-before-server-finalizes-load-cancellation.md) | 当前内部取消/抑制设计候选；无生产、MES、调度和安全范围的共同批准。 |
| [FR-008](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-008-destination-station-auto-identify-and-batch-unlock.md)、[FR-009](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-009-post-close-light-curtain-confirm-occupancy-rollback-and-residue-escalation.md) | TC-018～024 | 由 UC-010/004/044 与 BR-013/014 派生；TC-020/021加入具体 IO 批量策略 | 当前内部卸货/批量开锁候选；Modbus 批量语义同时需要硬件/IO 责任人确认，不能仅由业务批准覆盖。 |
| [FR-010](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-010-arrival-status-update-and-operation-panel-navigation.md) | TC-025～026 | 由 UC-003/009 与 BR-001 派生 | 仅覆盖 AC-1/2；FR 自己明确 AC-3～7 尚无 TC。到站与界面候选未获批准，且覆盖不完整。 |
| [FR-011](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-011-identity-and-role-verification-via-mes.md)、[FR-012](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-012-session-establishment-reuse-and-lock-stage-transition.md)、[FR-013](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-013-session-termination-rules.md) | TC-027～037、121 | 由 UC-043 及 UC-001/002/005/006/010/044/046 派生，包含“8005 装货核验、卸货不核验”、Sublot 绑定、掉线恢复和审批身份分离 | 项目特定身份/权限候选；没有客户 IT、生产、信息安全或角色授权人批准。FR-012 AC-3/4 没有精确 `Verifies` 对应 TC。 |
| [FR-014](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-014-slot-reopen-residue-clearance-confirm-and-state-restoration.md) | TC-038～041 | 由 UC-044/010/004 派生 | 当前内部残留清除候选；反复自动弹锁、无强制放行上限及 UNKNOWN 恢复需要现场安全确认。 |
| [FR-031](../../../../requirement-documents/04-functional-requirements/01-site-operations/fr-031-station-departure-wait-timeout-and-auto-closure.md) | TC-103～113 | Origin 写“2026-07-30～31 需求确认会话”、UC-046、ADR-cross-0055，但没有会话原件、参与人/授权、确认内容或版本绑定 | 当前内部离站超时设计候选；默认 5 分钟、60/10 秒颜色、无声音、不可续时等均需按项目/站点范围逐项确认。 |

所有上游 FR 和所列 UC 的 frontmatter 都是 `draft`。部分 UC 备注写“经与用户确认”或“已确认”，FR-031 写“需求确认会话”，但没有具名用户身份、其授权范围、原始对话/会议、确认日期与确认对象版本，因此只可作为来源线索。ADR `Status: accepted` 表示内部架构决定当前被采用；在本次治理规则下，它不能替代业务需求或验收标准批准。

## 67/67 逐文件证据矩阵

结论编码：**C1**＝直接镜像 draft FR/AC 的未批准验收草案，当前未执行；**C2**＝除 C1 外还显著固化内部 ADR/状态机/接口设计，须拆分业务与设计批准范围，当前未执行。每一行均已核对文件全文、固定哈希、Git 历史与显式 `Verifies`；“当前适用”仅指与仓库当前内部模型未见冲突，不是基线批准。

| 固定文件 | SHA-256 前 12 / 历史 | 显式派生对象 | 场景范围 | 证据结论 |
|---|---|---|---|---|
| [TC-001](../../../../requirement-documents/05-test-cases/01-site-operations/tc-001-pending-slot-exists-pass.md) | `43855625b247` / H1 | FR-003 AC-1 | 无剩余任务时结束资格 | C1 |
| [TC-002](../../../../requirement-documents/05-test-cases/01-site-operations/tc-002-no-pending-slot-reject.md) | `a085fcda33c0` / H1 | FR-003 AC-2 | 有剩余任务时二次确认 | C1 |
| [TC-003](../../../../requirement-documents/05-test-cases/01-site-operations/tc-003-door-or-curtain-mismatch-reject.md) | `d7654d162734` / H1 | FR-003 AC-3 | 未收敛/未知阻断整站结束 | C1 |
| [TC-004](../../../../requirement-documents/05-test-cases/01-site-operations/tc-004-batch-confirm-success-and-record.md) | `e9eb15d41eef` / H1 | FR-004 AC-1 | StopClosureCommit 原子提交/回滚 | C1 |
| [TC-005](../../../../requirement-documents/05-test-cases/01-site-operations/tc-005-session-closure-on-confirm.md) | `a24a2e08abb5` / H1 | FR-004 AC-2 | 整站提交立即结束会话 | C1 |
| [TC-006](../../../../requirement-documents/05-test-cases/01-site-operations/tc-006-confirm-non-reversible.md) | `cd04d3447618` / H1 | FR-004 AC-4 | 发车失败不撤销整站结束 | C1 |
| [TC-007](../../../../requirement-documents/05-test-cases/01-site-operations/tc-007-retrieval-eligibility-pass.md) | `1dc47afac3b1` / H1 | FR-005 AC-1 | 原仓位纠错授权通过 | C1 |
| [TC-008](../../../../requirement-documents/05-test-cases/01-site-operations/tc-008-retrieval-eligibility-reject.md) | `41e45164edc1` / H1 | FR-005 AC-2 | 不合法纠错拒绝 | C1 |
| [TC-009](../../../../requirement-documents/05-test-cases/01-site-operations/tc-009-retrieval-move-interlock-block.md) | `3bb2c3076ec9` / H1 | FR-006 AC-1 | 移动联锁阻断纠错开锁 | C1 |
| [TC-010](../../../../requirement-documents/05-test-cases/01-site-operations/tc-010-retrieval-batch-unlock-success.md) | `0445af6c0df5` / H1 | FR-006 AC-2 | 纠错只开原仓位 | C1 |
| [TC-011](../../../../requirement-documents/05-test-cases/01-site-operations/tc-011-retrieval-unlock-timeout-lockout.md) | `ee2c476250eb` / H1 | FR-006 AC-3 | 原仓位重放成功 | C1 |
| [TC-012](../../../../requirement-documents/05-test-cases/01-site-operations/tc-012-retrieval-slot-unexpectedly-empty-lockout.md) | `f03c832d5638` / H1 | FR-006 AC-4 | 正确产品不可得进入待重放 | C1 |
| [TC-013](../../../../requirement-documents/05-test-cases/01-site-operations/tc-013-retrieval-close-curtain-clear-rollback.md) | `acff6c618e69` / H1 | FR-006 AC-5 | 待重放只允许继续或取消 | C1 |
| [TC-014](../../../../requirement-documents/05-test-cases/01-site-operations/tc-014-retrieval-residue-reopen-required.md) | `2d9ea5f8c08b` / H1 | FR-006 AC-6 | 纠错目标态不符自动弹锁 | C1 |
| [TC-015](../../../../requirement-documents/05-test-cases/01-site-operations/tc-015-cancel-eligible-success.md) | `6a7644844a09` / H1 | FR-007 AC-1 | 未装货任务直接取消 | C1 |
| [TC-016](../../../../requirement-documents/05-test-cases/01-site-operations/tc-016-cancel-invalid-state-reject.md) | `43232ddeb668` / H1 | FR-007 AC-9 | 离站或非法状态拒绝取消 | C1 |
| [TC-017](../../../../requirement-documents/05-test-cases/01-site-operations/tc-017-cancel-loaded-batch-clear-success.md) | `e56b7e9021c9` / H2 | FR-007 AC-2/3 | 已装货批量清空后取消 | C2 |
| [TC-018](../../../../requirement-documents/05-test-cases/01-site-operations/tc-018-destination-auto-identify-list.md) | `10549ebed0e9` / H3 | FR-008 AC-1 | 自动识别待取料清单 | C1 |
| [TC-019](../../../../requirement-documents/05-test-cases/01-site-operations/tc-019-destination-move-interlock-block.md) | `2e695347ebe6` / H3 | FR-008 AC-2 | 移动联锁拒绝卸货开锁 | C1 |
| [TC-020](../../../../requirement-documents/05-test-cases/01-site-operations/tc-020-destination-batch-unlock-success.md) | `c3835a32b2db` / H1 | FR-008 AC-3/6 | Modbus 分组批量开锁成功 | C2 |
| [TC-021](../../../../requirement-documents/05-test-cases/01-site-operations/tc-021-destination-unlock-timeout-lockout.md) | `68d42ff1ecb2` / H1 | FR-008 AC-4/6 | 多模块部分成功/未知恢复 | C2 |
| [TC-022](../../../../requirement-documents/05-test-cases/01-site-operations/tc-022-destination-content-mismatch-lockout.md) | `e2a2cc909037` / H3 | FR-008 AC-5 | 实物不符异常锁定 | C1 |
| [TC-023](../../../../requirement-documents/05-test-cases/01-site-operations/tc-023-destination-close-curtain-clear-rollback.md) | `73f098ac22ce` / H1 | FR-009 AC-1 | 卸货清空后回滚占用并记录 | C1 |
| [TC-024](../../../../requirement-documents/05-test-cases/01-site-operations/tc-024-destination-residue-escalate-to-uc044.md) | `199b20aca02a` / H3 | FR-009 AC-2 | 残留转 UC-044 | C1 |
| [TC-025](../../../../requirement-documents/05-test-cases/01-site-operations/tc-025-arrival-status-updated-to-arrived.md) | `be6d02adac24` / H3 | FR-010 AC-1 | 到站状态更新 | C1 |
| [TC-026](../../../../requirement-documents/05-test-cases/01-site-operations/tc-026-operation-panel-auto-navigation.md) | `9b96fd5968f6` / H3 | FR-010 AC-2 | 操作面板自动跳转 | C1 |
| [TC-027](../../../../requirement-documents/05-test-cases/01-site-operations/tc-027-active-session-exists-reject-new-verification.md) | `8df9224d5b27` / H1 | FR-011 AC-3 | 活动 Sublot 拒绝换工号 | C1 |
| [TC-028](../../../../requirement-documents/05-test-cases/01-site-operations/tc-028-identity-and-role-verification-pass.md) | `99e07265985a` / H1 | FR-011 AC-1 | MES 身份/岗位核验通过 | C1 |
| [TC-029](../../../../requirement-documents/05-test-cases/01-site-operations/tc-029-identity-not-found-or-mes-error-reject.md) | `20160d193e4e` / H1 | FR-011 AC-2 | 身份、权限或 MES 异常拒绝 | C1 |
| [TC-030](../../../../requirement-documents/05-test-cases/01-site-operations/tc-030-insufficient-role-permission-reject.md) | `c1841a228db8` / H1 | FR-011 AC-4 | 8005 卸货不要求工号 | C1 |
| [TC-031](../../../../requirement-documents/05-test-cases/01-site-operations/tc-031-session-established-after-verification-pass.md) | `65a1c1c4641a` / H1 | FR-012 AC-1 | 建立并持久化操作员上下文 | C1 |
| [TC-032](../../../../requirement-documents/05-test-cases/01-site-operations/tc-032-session-reuse-without-reverification.md) | `adfef0296009` / H1 | FR-012 AC-2 | 跨 Sublot 复用工号 | C1 |
| [TC-033](../../../../requirement-documents/05-test-cases/01-site-operations/tc-033-first-door-operation-triggers-lock-stage.md) | `1bc566b67d4b` / H1 | FR-012 AC-2 | Sublot 内固定操作员 | C1 |
| [TC-034](../../../../requirement-documents/05-test-cases/01-site-operations/tc-034-uc006-cancel-does-not-affect-session.md) | `bad12f2eef75` / H1 | FR-013 AC-1 | 无进展/掉线/重启保持上下文 | C1 |
| [TC-035](../../../../requirement-documents/05-test-cases/01-site-operations/tc-035-uc002-confirm-completion-ends-session-normally.md) | `74e36ee04a19` / H1 | FR-013 AC-2 | 完成 Sublot 后保留工号并可换人 | C1 |
| [TC-036](../../../../requirement-documents/05-test-cases/01-site-operations/tc-036-unlocked-stage-manual-early-end-session.md) | `4189c32c9943` / H1 | FR-013 AC-3 | StopClosureCommit 清除会话 | C1 |
| [TC-037](../../../../requirement-documents/05-test-cases/01-site-operations/tc-037-locked-stage-reject-manual-end-session.md) | `496c489a54fa` / H1 | FR-013 AC-4 | 未结 Sublot 禁止本地强清 | C1 |
| [TC-038](../../../../requirement-documents/05-test-cases/01-site-operations/tc-038-move-interlock-reject-unlock.md) | `a532c47588b4` / H3 | FR-014 AC-1 | 移动联锁拒绝残留仓重开 | C1 |
| [TC-039](../../../../requirement-documents/05-test-cases/01-site-operations/tc-039-slot-reopen-success.md) | `e78b1f2b289a` / H3 | FR-014 AC-2 | 残留仓重开成功 | C1 |
| [TC-040](../../../../requirement-documents/05-test-cases/01-site-operations/tc-040-reclose-curtain-confirm-clear-restore-idle.md) | `b484708608b0` / H3 | FR-014 AC-3 | 清空后恢复空闲并记录 | C1 |
| [TC-041](../../../../requirement-documents/05-test-cases/01-site-operations/tc-041-reclose-residue-remains-require-reopen-again.md) | `10673ab1076c` / H1 | FR-014 AC-4 | 残留仍在则反复重开 | C1 |
| [TC-098](../../../../requirement-documents/05-test-cases/01-site-operations/tc-098-cancel-occupancy-mismatch-auto-reopen.md) | `f0fe7ba0822b` / H2 | FR-007 AC-4 | 取消清空目标态闭环 | C2 |
| [TC-099](../../../../requirement-documents/05-test-cases/01-site-operations/tc-099-postcommit-cancel-preserves-history.md) | `424c0b9ae294` / H2 | FR-007 AC-5 | 提交后取消保留历史 | C2 |
| [TC-100](../../../../requirement-documents/05-test-cases/01-site-operations/tc-100-cancel-one-sublot-preserves-another.md) | `dc164aae3923` / H2 | FR-007 AC-6 | 多 Sublot 取消隔离 | C2 |
| [TC-101](../../../../requirement-documents/05-test-cases/01-site-operations/tc-101-cross-sublot-operation-serialization.md) | `58e3e0455c1e` / H2 | FR-007 AC-7 | 跨 Sublot 物理操作串行 | C2 |
| [TC-102](../../../../requirement-documents/05-test-cases/01-site-operations/tc-102-cancelled-slots-reused-for-new-sublot.md) | `e451a2e3b2bf` / H2 | FR-007 AC-8 | 取消释放与业务键抑制 | C2 |
| [TC-103](../../../../requirement-documents/05-test-cases/01-site-operations/tc-103-departure-wait-start-and-visual-warning.md) | `f0b404a199ff` / H2 | FR-031 AC-1/3/4 | 5 分钟等待与 60/10 秒视觉提醒 | C2 |
| [TC-104](../../../../requirement-documents/05-test-cases/01-site-operations/tc-104-full-interval-reset-on-business-progress.md) | `23e2d9f96007` / H2 | FR-031 AC-2 | 有效进展后完整重新计时 | C2 |
| [TC-105](../../../../requirement-documents/05-test-cases/01-site-operations/tc-105-timeout-cancels-unstarted-tasks-atomically.md) | `69c32b731df2` / H2 | FR-031 AC-5 | 超时原子取消未开始任务 | C2 |
| [TC-106](../../../../requirement-documents/05-test-cases/01-site-operations/tc-106-partial-load-inactivity-alert-only.md) | `f7a413ca08a7` / H2 | FR-031 AC-7 | 部分装货超时只告警 | C2 |
| [TC-107](../../../../requirement-documents/05-test-cases/01-site-operations/tc-107-unload-blocks-departure-wait.md) | `e4c5adb82998` / H2 | FR-031 AC-8 | 待卸任务阻断离站等待 | C2 |
| [TC-108](../../../../requirement-documents/05-test-cases/01-site-operations/tc-108-disconnect-invalidates-deadline.md) | `74e0f2bb07e5` / H2 | FR-031 AC-9 | 断联使截止时间失效 | C2 |
| [TC-109](../../../../requirement-documents/05-test-cases/01-site-operations/tc-109-operation-vs-timeout-race.md) | `25938f2759aa` / H2 | FR-031 AC-6 | 操作与超时竞态 | C2 |
| [TC-110](../../../../requirement-documents/05-test-cases/01-site-operations/tc-110-post-closure-routing-without-next-stop.md) | `60d7e769b112` / H2 | FR-031 AC-11 | 无下一站的载货/空载分流 | C2 |
| [TC-111](../../../../requirement-documents/05-test-cases/01-site-operations/tc-111-stop-closure-handoff-before-movement.md) | `3034a13f8865` / H2 | FR-031 AC-10 | 会话/投影/安全核验先于移动 | C2 |
| [TC-112](../../../../requirement-documents/05-test-cases/01-site-operations/tc-112-movement-failure-does-not-reopen-stop.md) | `62f10342fa85` / H2 | FR-031 AC-12 | 移动失败不重开本站 | C2 |
| [TC-113](../../../../requirement-documents/05-test-cases/01-site-operations/tc-113-load-batch-auto-commit-and-wait-reset.md) | `ee9c4df34a11` / H2 | FR-002 AC-5、FR-031 AC-2 | LoadBatch 自动提交与重计时 | C2 |
| [TC-114](../../../../requirement-documents/05-test-cases/01-site-operations/tc-114-load-hardware-fault-holds-without-replacement-or-auto-clear.md) | `31bfbac4df4c` / H2 | FR-002 AC-4/4.1 | 硬件故障保持、不换仓/不自动清空 | C2 |
| [TC-115](../../../../requirement-documents/05-test-cases/01-site-operations/tc-115-hardware-signal-recovery-still-requires-manual-confirmation.md) | `688c201c3832` / H2 | FR-002 AC-4.2 | 信号恢复仍需维护确认和服务端授权 | C2 |
| [TC-116](../../../../requirement-documents/05-test-cases/01-site-operations/tc-116-production-operator-cannot-confirm-hardware-recovery.md) | `41e4970cf2af` / H2 | FR-002 AC-4.3 | 普通生产操作员越权恢复拒绝 | C2 |
| [TC-117](../../../../requirement-documents/05-test-cases/01-site-operations/tc-117-supervisor-decides-load-compensation.md) | `1aef362e8541` / H2 | FR-002 AC-4.4 | R-09 整批清空决定 | C2 |
| [TC-118](../../../../requirement-documents/05-test-cases/01-site-operations/tc-118-maintenance-confirmation-cannot-replace-compensation-decision.md) | `fd8dcf27a226` / H2 | FR-002 AC-4.5 | 维护确认与生产决定分权 | C2 |
| [TC-119](../../../../requirement-documents/05-test-cases/01-site-operations/tc-119-hardware-fault-cannot-bypass-compensation-decision-via-normal-cancel.md) | `ac7c38fd8370` / H2 | FR-007 AC-10 | 普通取消不得绕过补偿决定 | C2 |
| [TC-120](../../../../requirement-documents/05-test-cases/01-site-operations/tc-120-compensation-decision-requires-step-up-authentication.md) | `23ad9c7eeba7` / H2 | FR-002 AC-4.6/4.6.1 | 单次强绑定即时二次认证 | C2 |
| [TC-121](../../../../requirement-documents/05-test-cases/01-site-operations/tc-121-supervisor-approval-does-not-replace-sublot-operator.md) | `a01e2e5905f0` / H2 | FR-012 AC-5 | 审批人不替换 Sublot 操作员 | C2 |
| [TC-122](../../../../requirement-documents/05-test-cases/01-site-operations/tc-122-compensation-decision-requires-controlled-reason-code.md) | `2bae6e7c8126` / H2 | FR-002 AC-4.7 | 受控补偿原因码 | C2 |
| [TC-123](../../../../requirement-documents/05-test-cases/01-site-operations/tc-123-load-compensation-cancels-transport-demand.md) | `2e2c5743bccb` / H2 | FR-002 AC-4.8 | 补偿清空后取消并抑制搬运需求 | C2 |

## 追踪质量与当前覆盖异常

1. **名称漂移：** TC-001/002 的文件名与当前“无/有剩余任务”语义近似反向；TC-011、013、021、030、033～037 的文件名仍保留旧的超时、回滚、权限或会话阶段语义，而标题/正文已改为新的原仓位重放、部分成功、卸货不核验、Sublot 绑定和 StopClosureCommit 模型。哈希固定了当前正文，但文件名会误导按路径追踪。
2. **README 与覆盖事实不一致：** 目录说明称一条 AC 对应一条 TC，并声称站点域已有 FR/TC 覆盖；实际存在一条 TC 覆盖多个 AC（TC-017、020、021、103、113、114、120），也存在缺口。FR-010 明示 AC-3～7 尚无 TC；FR-012 AC-3/4 无精确 `Verifies` 指针。
3. **`related_tc` 与 `Verifies` 不完全一致：** FR-004 把 TC-105/111/112 列为相关，FR-013 把 TC-111/112 列为相关，但这些 TC 的 `Verifies` 只写 FR-031；不能据此宣称 FR-004 AC-3 或 FR-013 的交叉行为已被明确覆盖。
4. **执行与设计未分层：** 当前 TC 文档没有“计划/已执行”、环境、证据附件、结果或缺陷字段。应把“验收标准候选”“可执行测试规范”“某版本执行记录”建成不同对象，避免把预期结果误读为观察结果。

## 后续原子证据请求

1. 对每个拟进入基线的 FR/AC—TC 对提供具名业务授权人、授权角色、确认日期、8005 项目/车辆/站点/阶段范围和确认对象哈希；不能用整份目录或 Git 提交一次性批准 67 项。
2. 对身份、R-09/R-11、二次认证、原因码和会话规则，取得客户 IT、生产管理、设备维护和信息安全各自职责范围内的确认；兼任角色也须说明授权来源。
3. 对 Modbus `0x0F`、跨模块并行、锁 DI/光幕、自动弹锁、UNKNOWN 恢复与无强制放行次数上限，取得电气/机械/功能安全责任人的硬件版本、站点条件和风险评审。
4. 对 5 分钟默认值、站点覆盖、60/10 秒颜色、无声音与不可续时，提供原始确认会话并明确是项目默认、站点覆盖还是现场可配置参数。
5. 修复上述文件名与追踪缺口后，为每次实际执行另存不可变记录：TC 哈希、被测软件/固件/IO 映射/车辆/站点版本、执行人/时间、实际结果、Pass/Fail、日志/照片/缺陷链接。执行通过仍不能反向替代需求批准。
