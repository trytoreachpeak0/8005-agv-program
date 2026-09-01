# R08 跨域词汇与架构决定调查

## 结论

R08 固定清单共 57 份材料：2 份候选词汇载体与 55 份跨域 ADR。2026-08-03 复算 SHA-256 后，57/57 与[无损材料清单](../material-inventory/material-inventory.tsv)一致，且这些源文件均无工作区修改。

没有一份材料具备当前基线治理规则要求的完整批准四要素。`accepted` 只说明 ADR 文件内的内部状态；Git 作者只说明提交者；二者都不能证明具名业务授权人批准了某个版本、范围和日期。因此，本批次不能直接向当前需求基线贡献“已确认需求”。

按当前证据分类：

- [CONTEXT.md](../../../../CONTEXT.md) 与 ADR 0003–0055 的当前快照，共 54 份，有同一提交的 Cursor 共同署名，属于“AI 生成或修改但尚未确认”。
- ADR 0001–0002 与[旧术语表](../../../../glossary/terminology-glossary.md)，共 3 份，能恢复编辑者和提交历史，但不能恢复决定来源与批准链，属于“来源未知”。
- 55 份 ADR 中，保守筛出 16 份同时含业务/项目约束候选和设计决定，2 份以领域定义或物理事实假设为主并派生设计，37 份为设计/架构/实现决定。这个分类只决定后续应向谁核实，不赋予权威性。
- ADR 0038 与 0045 有明确替代证据，当前仅作历史材料；其余 `accepted` ADR 只能视为当前仓库内部设计候选。ADR 0018 与 0055 存在未解释的会话清除冲突；ADR 0046 仍残留已被 0054 删除的“待整批确认”阶段。

## 范围与判定规则

调查边界由[票 20](../../issues/20-investigate-cross-domain-vocabulary-and-decisions.md)与材料清单中 `batch_id=R08` 固定，不增删文件。当前需求基线只按需回溯来源、批准、范围、替代与冲突，不恢复完整演变史，遵守[票 06](../../issues/06-current-baseline-history-boundary.md)。

权威判断采用[票 01](../../issues/01-authority-and-classification-evidence-rules.md)的四要素：具名授权人、可核查日期、明确适用范围、绑定具体版本/commit/会议记录或等价证据。文档须按可独立判断的条目拆分，见[票 04](../../issues/04-atomic-requirement-approval-granularity.md)。疑似冲突不能仅凭时间新旧自行解释，见[票 05](../../issues/05-conflict-classification-and-hitl-escalation.md)。

内容分类如下；同一文件可以有多个标签：

- `V`：仅用于沟通的一致命名、别名或禁用同义词。
- `DM`：领域实体、身份、生命周期或不变量的定义。
- `BR?`：业务流程、现场约束、权限、策略、产品范围或验收行为候选；问号表示尚无业务批准。
- `PF`：需要硬件/现场证据核实的物理事实假设。
- `DD`：软件边界、协议、存储、状态机、安全机制、UI 或其它设计/实现决定。

仓库自己的领域文档规范要求以根 [CONTEXT.md](../../../../CONTEXT.md) 为领域用语入口、以 `docs/adr/` 保存决定，且工作产出应采用 CONTEXT 定义的术语（`docs/agents/domain.md:7-9,29`）。这能证明材料对仓库内部协作仍有用途，不能证明业务批准。

## 身份、历史与来源链

| 组 | 文件 | 可恢复历史 | 来源/提出主体 | 接受主体与版本绑定 | 治理分类 |
| --- | --- | --- | --- | --- | --- |
| H1 | CONTEXT | 3 次提交：`e6dc9ea`（2026-07-23）→ `ffe1f49`（2026-07-27）→ `493ac5a`（2026-07-31） | Git 作者/提交者均为 Zhengyu Shao；最新提交有 `Co-authored-by: Cursor`。不能把编辑者当决定提出者 | 无 `Accepted by`、批准日期或批准记录；声明覆盖项目也不是授权人确认的范围；没有批准记录绑定当前 SHA | AI 生成或修改但尚未确认 |
| H2 | ADR 0001–0002 | 各 2 次提交：`e6dc9ea` → `ffe1f49` | Git 作者为 Zhengyu Shao；文件未注明来源或提出人。0002 的 Lab 说法有仓库实验佐证，但 ADR 未绑定具体实验轮次 | `Status: accepted` 无主体、日期、范围、版本；Git 提交不构成批准 | 来源未知 |
| H3 | ADR 0003–0055 | 每份仅 1 次提交，均由 `493ac5a` 于 2026-07-31 同批创建；提交说明为“Document onboard-server authority and station operation rules as ADRs.”，并有 `Co-authored-by: Cursor` | Git 作者为 Zhengyu Shao、AI 共同作者为 Cursor。26 份写“同事初稿 §…”，但没有初稿路径、标题、作者、日期、hash 或版本，故不能识别所称同事或逐节核验 | 51 份写 `accepted`，0038/0045 写 `superseded`；全部缺少接受人、接受日期、批准范围和批准记录到文件版本的绑定 | AI 生成或修改但尚未确认；0038/0045 另为明确历史材料 |
| H4 | 术语表 | 3 次提交：`96eb203`（2026-07-13）→ `0b2246c`（2026-07-13）→ `ecd0fd8`（2026-07-15） | Git 作者为 Zhengyu Shao。表内初始两条变更作者为空，后两条署名 ZhengyuShao（`glossary/terminology-glossary.md:195-202`） | 编辑日志没有批准动作；无批准人、批准范围与版本绑定 | 来源未知 |

`493ac5a` 的共同作者信息是 AI 参与的直接证据。它不是否定内容正确性的证据，但按票 01，在具体版本尚无授权人确认时必须归为“AI 生成或修改但尚未确认”。

ADR 0002 的经验事实可以回溯到行为实验，例如 `CONTINUE_FROM_HELD` 的 `100020` 见 `rcs/riot-behavior-lab/evidence/rounds/2026-07-22-round-37/execution-log.md:20`，`CONTINUE_FROM_HANG` 的 `100021` 见 `rcs/riot-behavior-lab/evidence/rounds/2026-07-20-round-11/execution-log.md:49`。这只支持“两个命令不能混用”的观测，不批准“第一版 SDK 如何封装”的设计决定。

## 批准四要素审计

| 要素 | 57 份材料中的证据 | 结论 |
| --- | --- | --- |
| 具名授权人 | 有 Git 作者、共同作者、术语表编辑者和运行时角色 R-09/R-11；没有任何人以本批材料批准人的身份出现 | 0/57 满足 |
| 可核查批准日期 | 有文件提交日期和术语表变更日期；没有批准动作发生日期 | 0/57 满足 |
| 批准范围 | CONTEXT 与术语表自称项目范围，ADR 目录表示跨域设计范围；没有授权人确认这些范围 | 0/57 满足 |
| 版本绑定 | 当前 SHA 和 Git commit 可恢复；没有确认记录把批准动作绑定到任一 SHA/commit/会议版本 | 0/57 满足 |

因此不能把 `accepted`、`采纳`、文件完整程度、Git 作者、较新时间戳、代码现状或当前文档引用当成业务批准。

## 逐份核验矩阵

SHA 列显示清单中完整 SHA-256 的前 12 个十六进制字符；本次已逐份以完整值复算并取得 57/57 一致。`H1`–`H4` 对应上节来源历史。适用性列中，“内部当前”只表示仓库未给出替代证据且领域导航仍把它当现行协作材料，不表示需求已批准。

| 材料 | SHA-256 前 12 | 历史 | 内容分类 | 当前适用性与范围判断 |
| --- | --- | --- | --- | --- |
| [CONTEXT](../../../../CONTEXT.md) | `221b4e6942ba` | H1 | V + DM + BR? + DD | 内部当前词汇入口；混入大量规范规则与协议细节，不能整份当词汇或已批准需求 |
| [ADR-cross-0001](../../../../docs/adr/cross/0001-v1-facade-shaped-for-mes-dispatch.md) | `f5d4342d791a` | H2 | DD | 内部当前 SDK/Facade 设计；无业务批准 |
| [ADR-cross-0002](../../../../docs/adr/cross/0002-hang-continue-named-facade.md) | `9c93adaada95` | H2 | DD | 内部当前 SDK 设计；有实验线索但无决定批准 |
| [ADR-cross-0003](../../../../docs/adr/cross/0003-onboard-disconnect-safe-finish-and-server-resume.md) | `e365cf79cb5e` | H3 | DD | 内部当前断联安全设计 |
| [ADR-cross-0004](../../../../docs/adr/cross/0004-onboard-hmi-exclusive-io-authority.md) | `c7c5f1ea9322` | H3 | DD | 内部当前 IO 权威边界设计 |
| [ADR-cross-0005](../../../../docs/adr/cross/0005-slot-physical-and-business-state-authority.md) | `f5522671734f` | H3 | DD | 内部当前事实权威边界设计 |
| [ADR-cross-0006](../../../../docs/adr/cross/0006-onboard-minimal-recovery-journal.md) | `4083071d2e5a` | H3 | DD | 内部当前恢复持久化设计 |
| [ADR-cross-0007](../../../../docs/adr/cross/0007-stable-slot-identity-and-maintenance-io-config-change.md) | `841ab89482c9` | H3 | DD | 内部当前仓位身份/配置换版设计 |
| [ADR-cross-0008](../../../../docs/adr/cross/0008-onboard-departure-safety-server-movement-control.md) | `2767ab6afad4` | H3 | DD | 内部当前安全与移动职责设计 |
| [ADR-cross-0009](../../../../docs/adr/cross/0009-fresh-safety-check-before-each-movement.md) | `45d7bf2d5791` | H3 | DD | 内部当前发车安全核验设计 |
| [ADR-cross-0010](../../../../docs/adr/cross/0010-automatic-movement-intervention-on-safety-revocation.md) | `d433fddb95e6` | H3 | DD | 内部当前安全失效介入设计 |
| [ADR-cross-0011](../../../../docs/adr/cross/0011-tiered-riot-stop-on-departure-safety-revocation.md) | `63bd310ac610` | H3 | DD | 内部当前分级停车设计 |
| [ADR-cross-0012](../../../../docs/adr/cross/0012-persisted-movement-guard-during-station-operation.md) | `09d8fb6aec27` | H3 | DD | 内部当前移动阻断设计 |
| [ADR-cross-0013](../../../../docs/adr/cross/0013-progress-is-telemetry-result-commits-per-slot.md) | `aef9b0cfb241` | H3 | DD | 内部当前遥测/结果语义设计 |
| [ADR-cross-0014](../../../../docs/adr/cross/0014-durable-command-acceptance-and-same-operation-reconciliation.md) | `4ba1caadc71f` | H3 | DD | 内部当前可靠接受/对账设计 |
| [ADR-cross-0015](../../../../docs/adr/cross/0015-no-generic-cancel-load-recovers-unload-must-complete.md) | `bea94b5337c8` | H3 | BR? + DD | 含装货可补偿、卸货必须完成的业务过程候选；设计仍内部当前 |
| [ADR-cross-0016](../../../../docs/adr/cross/0016-slot-command-is-irrevocable-commit-point.md) | `d315f8a86a8f` | H3 | DD | 内部当前不可撤回承诺点设计 |
| [ADR-cross-0017](../../../../docs/adr/cross/0017-restart-resumes-only-from-proven-checkpoint.md) | `057b5f661184` | H3 | DD | 内部当前重启恢复设计 |
| [ADR-cross-0018](../../../../docs/adr/cross/0018-project-wide-operator-verification-enabled.md) | `248ee95ba848` | H3 | BR? + DD | 身份核验策略为业务候选；清除时点与 0055 冲突，当前语义待查 |
| [ADR-cross-0019](../../../../docs/adr/cross/0019-onboard-technical-logs-server-business-audit.md) | `c2ab696fbaa9` | H3 | DD | 内部当前日志/审计职责设计 |
| [ADR-cross-0020](../../../../docs/adr/cross/0020-io-config-drafts-and-maintenance-activation.md) | `23f393085cc4` | H3 | DD | 内部当前 IO 配置生命周期设计 |
| [ADR-cross-0021](../../../../docs/adr/cross/0021-server-consumes-capabilities-not-io-configuration.md) | `71358da6d399` | H3 | DD | 内部当前车载/服务端接口边界设计 |
| [ADR-cross-0022](../../../../docs/adr/cross/0022-capability-full-sync-on-connect-reliable-on-change.md) | `a58274fb7dd9` | H3 | DD | 内部当前能力同步设计 |
| [ADR-cross-0023](../../../../docs/adr/cross/0023-one-fenced-connection-session-per-agv.md) | `6a1eb60f3a51` | H3 | DD | 内部当前连接 fencing 设计 |
| [ADR-cross-0024](../../../../docs/adr/cross/0024-per-agv-connection-credential.md) | `33057fd607a0` | H3 | DD | 内部当前车辆凭证设计 |
| [ADR-cross-0025](../../../../docs/adr/cross/0025-pinned-self-signed-tls-and-per-agv-secret.md) | `9a158215651d` | H3 | DD | 内部当前 TLS/密钥实现决定 |
| [ADR-cross-0026](../../../../docs/adr/cross/0026-hold-system-movement-on-onboard-connection-loss.md) | `c2320a9cba84` | H3 | DD | 内部当前断链停车设计 |
| [ADR-cross-0027](../../../../docs/adr/cross/0027-two-second-heartbeat-six-second-liveness-timeout.md) | `5d19a1321656` | H3 | DD | 内部当前协议时序决定；2 秒/6 秒无批准与验证绑定 |
| [ADR-cross-0028](../../../../docs/adr/cross/0028-connected-session-requires-explicit-business-readiness.md) | `2a8075f92001` | H3 | DD | 内部当前业务就绪门控设计 |
| [ADR-cross-0029](../../../../docs/adr/cross/0029-unified-five-step-recovery-handshake.md) | `5ed5580cff20` | H3 | DD | 内部当前恢复握手设计 |
| [ADR-cross-0030](../../../../docs/adr/cross/0030-uniform-ndjson-protocol-envelope.md) | `883fbd6653bf` | H3 | DD | 内部当前协议外壳设计 |
| [ADR-cross-0031](../../../../docs/adr/cross/0031-integer-protocol-version-with-exact-match.md) | `fb09aa1335f8` | H3 | DD | 内部当前协议版本设计 |
| [ADR-cross-0032](../../../../docs/adr/cross/0032-explicit-message-delivery-classes.md) | `00ffdbbec59f` | H3 | DD | 内部当前交付语义设计 |
| [ADR-cross-0033](../../../../docs/adr/cross/0033-onboard-publishes-abstract-safety-state-changes.md) | `b09f212523d6` | H3 | DD | 内部当前安全状态发布设计 |
| [ADR-cross-0034](../../../../docs/adr/cross/0034-heartbeat-versions-detect-safety-state-gaps.md) | `a13205fbb686` | H3 | DD | 内部当前状态缺口检测设计 |
| [ADR-cross-0035](../../../../docs/adr/cross/0035-server-orders-slots-onboard-executes-array-order.md) | `ff361d8595f4` | H3 | DD | 内部当前仓位排序/批量执行设计 |
| [ADR-cross-0036](../../../../docs/adr/cross/0036-load-batch-commit-and-hardware-fault-hold.md) | `aadda359e63a` | H3 | DM + BR? + DD | LoadBatch 整体原子性与故障处置是业务候选；设计内部当前 |
| [ADR-cross-0037](../../../../docs/adr/cross/0037-unload-batch-clears-business-state-only-after-all-empty.md) | `fb94c20dc408` | H3 | BR? + DD | 8005 卸货清空粒度为项目策略候选；设计内部当前 |
| [ADR-cross-0038](../../../../docs/adr/cross/0038-new-slot-operation-attempt-id-after-compensated-load-retry.md) | `0f909ceebfc1` | H3 | DD | `Status` 明确被 0039 取代；仅历史适用 |
| [ADR-cross-0039](../../../../docs/adr/cross/0039-operator-starts-server-authorized-load-compensation.md) | `51a61005c258` | H3 | BR? + DD | R-09 决策权限、原因与补偿流程为业务候选；内部当前 |
| [ADR-cross-0040](../../../../docs/adr/cross/0040-internal-light-curtain-is-slot-occupancy-evidence.md) | `8df1e07ec459` | H3 | PF + DD | “仓内光幕可证明占用”需硬件/现场证据；派生设计内部当前 |
| [ADR-cross-0041](../../../../docs/adr/cross/0041-one-basket-per-physical-slot.md) | `fe3b57209f4e` | H3 | DM + BR? + DD | 一仓一篮是物理/业务约束候选；内部当前 |
| [ADR-cross-0042](../../../../docs/adr/cross/0042-sublot-is-load-input-and-server-resolves-task.md) | `b3af82b14f3a` | H3 | DM + BR? + DD | 输入物为 Sublot、无“总任务码”是领域/业务候选；内部当前 |
| [ADR-cross-0043](../../../../docs/adr/cross/0043-server-enforces-global-sublot-reservation.md) | `66992da73f8f` | H3 | BR? + DD | Sublot 全局唯一占用是业务不变量候选；内部当前 |
| [ADR-cross-0044](../../../../docs/adr/cross/0044-baskets-have-no-individual-identity.md) | `c4853ee79045` | H3 | DM + BR? + DD | 花篮无身份是现场/领域约束候选；内部当前 |
| [ADR-cross-0045](../../../../docs/adr/cross/0045-load-final-confirmation-and-precommit-correction.md) | `914d94797312` | H3 | BR? + DD | `Status` 明确被 0054 取代；仅历史适用 |
| [ADR-cross-0046](../../../../docs/adr/cross/0046-load-task-cancellable-until-departure-after-full-clearance.md) | `ea41792a5081` | H3 | BR? + DD | 取消资格/整批清空为业务候选；总体内部当前，但第 44 行残留已删除阶段 |
| [ADR-cross-0047](../../../../docs/adr/cross/0047-demand-id-identifies-station-task-and-cancellation.md) | `e8ed975f7ef1` | H3 | DM + DD | DemandId/TransportDemandKey 身份语义与抑制设计；内部当前 |
| [ADR-cross-0048](../../../../docs/adr/cross/0048-versioned-current-stop-worklist-snapshot.md) | `c6dfc6bdc8a1` | H3 | DD | 内部当前服务端投影设计 |
| [ADR-cross-0049](../../../../docs/adr/cross/0049-station-task-type-many-to-many-admission.md) | `d2b025f4fc96` | H3 | BR? + DD | 站点/任务类型准入规则是业务配置候选；内部当前 |
| [ADR-cross-0050](../../../../docs/adr/cross/0050-admission-policy-frozen-at-operation-commit.md) | `d9232aac773d` | H3 | DD | 内部当前准入快照/承诺点设计 |
| [ADR-cross-0051](../../../../docs/adr/cross/0051-admission-policy-stored-in-server-db-no-v1-ui.md) | `e1912e1806a8` | H3 | DD | 内部当前存储/首版 UI 范围设计 |
| [ADR-cross-0052](../../../../docs/adr/cross/0052-onboard-clears-before-server-finalizes-load-cancellation.md) | `b04491fd1a08` | H3 | BR? + DD | 取消必须先物理清空的业务流程候选；内部当前 |
| [ADR-cross-0053](../../../../docs/adr/cross/0053-onboard-upcoming-stop-plan-and-vehicle-overview.md) | `dd6f265a785d` | H3 | BR? + DD | 现场需展示后续站点/车辆概览是产品行为候选；内部当前 |
| [ADR-cross-0054](../../../../docs/adr/cross/0054-auto-load-commit-with-pre-departure-correction.md) | `13b50a5a5fcd` | H3 | BR? + DD | 自动提交与离站前纠错是业务过程候选；明确取代 0045 |
| [ADR-cross-0055](../../../../docs/adr/cross/0055-server-owned-station-departure-wait-timeout.md) | `0a6688b4c663` | H3 | BR? + DD | 5 分钟、不可延期、取消终态和 UI 告警是业务/产品候选；与 0018 冲突待查 |
| [术语表](../../../../glossary/terminology-glossary.md) | `5c7dca1fe4e0` | H4 | V + DM + BR? + DD | 仍 tracked，但与 CONTEXT 重叠且有待确认术语；不宜作为权威需求源 |

## 词汇载体不是需求批准载体

[CONTEXT.md](../../../../CONTEXT.md) 第 3 行自称统一领域用语，但内容不止命名。例如：

- 部署角色定义是沟通词汇（`CONTEXT.md:9-19`）。
- LoadBatch、Sublot、DemandId 等是领域定义（`CONTEXT.md:209-215,527-529`）。
- 一仓一篮、装卸身份核验、取消/卸货/超时规则是业务或现场约束候选（`CONTEXT.md:157-163,253-267,297-350`）。
- NDJSON 外壳、2 秒心跳/6 秒失联、Modbus 写法等是实现或架构决定（`CONTEXT.md:81-83,89-91,113-130`）。

因此不能因文件名为 CONTEXT 就把全部内容降格为“仅沟通”，也不能把其中规范语句整体升级为需求。应按条目分别追溯：命名可继续用于内部沟通；领域定义需领域负责人确认；业务约束需业务授权人确认；实现决定由技术责任人管理，并在受业务约束影响时保留追踪关系。

[旧术语表](../../../../glossary/terminology-glossary.md) 第 3–5 行声称覆盖全部文档、Use Case、接口与代码，第 18 行又自称优先于其它文档，但这只是文件自述，不是批准证据。它还同时写入架构角色、硬件数量/能力、流程规则、角色权限与错误码（`glossary/terminology-glossary.md:22-177`），并在第 206–213 行保留“批号/子批号”“格口/仓位”待确认项。仓库领域导航现在指向根 CONTEXT，而术语表没有明确废弃或被 CONTEXT 取代的记录；两者适用范围重叠，当前只能登记为来源/范围待查，不能凭 CONTEXT 较新就自行排序。

## 替代、冲突与当前适用性

### 有充分替代证据

- ADR 0038 第 9 行明确写 `superseded by ADR-cross-0039`；其“补偿后重试使用新 attempt id”只作历史材料。
- ADR 0045 第 21 行明确写 `superseded by ADR-cross-0054`。0054 第 13 行明确删除 `AWAITING_LOAD_CONFIRMATION` 与 `LoadFinalConfirmation`，故 0045 的最终确认模型只作历史材料。

时间更新本身不用于推导其它替代关系。

### 需追溯或 HITL 的不一致

1. **操作员上下文清除时点**：ADR 0018 第 5 行写“只有用户主动离站后才清除工号”；ADR 0055 第 3 行写手动或超时 `StopClosureCommit` 后关闭会话并清除上下文，CONTEXT 第 350 行也采用后者。0018 和 0055 同属 `493ac5a`，没有可用提交先后解释，也无明确 supersession。两者在自动超时场景不能同时满足，须查来源；不能自行用编号较大覆盖编号较小。
2. **已删除阶段残留**：ADR 0046 第 44 行仍把“待整批确认”列为 `canCancel=true` 阶段，但 ADR 0054 第 13 行明确删除该阶段。0046 的主体段落已经采用“自动提交 + StopClosureCommit”新模型（第 10、25 行），故更像同一版本内的残留措辞；在修正源 ADR 前应登记语义待查。
3. **双词汇入口**：术语表宣称项目级优先级，仓库领域导航则以 CONTEXT 为入口；没有具名的替代或范围分工决定。应由领域负责人确认唯一入口、两者关系和具体版本。

### 需要外部确认的高价值业务候选

以下并非已确认需求，而是应优先提交业务/现场授权人逐条确认的候选：

- 装货需核验身份、卸货不核验，以及会话清除边界（0018、0055）。
- 一个 Sublot 是一个 LoadBatch、整批原子提交；8005 卸货清空粒度（0036、0037）。
- R-09 补偿决定权限、原因码与审计（0039）。
- 一仓一篮、输入就是 Sublot、花篮无独立身份、同 Sublot 全局唯一占用（0041–0044）。
- 装货取消资格、全量清空、自动提交、离站前纠错与 5 分钟超时（0046、0052、0054、0055）。
- 站点与任务类型的多对多准入规则，以及车载端需展示的业务信息（0049、0053）。

ADR 0040 的“仓内光幕可以证明占用/空仓”还需要硬件图纸、I/O 定义、现场试验或设备责任人确认，不能由架构 ADR 单独确立物理事实。

## 建议的后续证据动作

1. 向 ADR 0003–0052 所称“同事初稿”的持有人索取原文件，并固定标题、作者、日期、适用项目/车辆、版本或 hash；把 26 份节号引用逐一解析到具体原文。
2. 对上述高价值业务候选建立原子条目，让具名业务/现场授权人分别确认或否决，并绑定当前 SHA 或后续修订版本；不要批量批准整个 CONTEXT 或整组 ADR。
3. 由技术责任人确认纯 `DD` 条目的技术状态、适用软件版本和替代关系；业务批准与技术 accepted 分开记录。
4. 为 0018/0055 的会话清除冲突、0046 的残留阶段和双词汇入口建立来源追溯；若仍不能排除冲突，按票 05 升级 HITL。
5. 对 0040、0041、0044 的硬件/现场断言补充设备证据；对 0002 保留具体 Lab 轮次和环境绑定。代码实现只能作为一致性证据，不能反向赋予需求权威性。

## 可复核性

本调查执行了以下只读核验：

- 从 TSV 精确筛选 `batch_id=R08`，得到 57 份、角色分布 `candidate-vocabulary=2`、`candidate-decision=55`。
- 对 57 个路径逐个执行 SHA-256 并与清单完整值比较，结果 57/57 相同。
- 对每个路径执行 `git log --follow`，并对关键提交执行 `git show --format=fuller --no-patch`，恢复上述作者、日期、共同作者和提交说明。
- 搜索 R08 文件中的批准/作者/状态/替代字段；未发现具名 `Accepted by` 或等价批准记录。
- 搜索“同事初稿/初稿 §”，55 份 ADR 中有 26 份使用该表述，但各 ADR 均未给出可解析的源文件身份和版本。
- 复核 R08 源路径的工作区状态，均无当前修改；调查没有修改 CONTEXT、术语表、ADR、issue 或 map，也没有创建提交。

