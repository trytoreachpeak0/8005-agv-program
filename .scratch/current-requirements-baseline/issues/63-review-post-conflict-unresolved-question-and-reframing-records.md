# 复核冲突决定后仍待问题解决或重构的 241 条记录

Type: task
Status: resolved
Blocked by: 56, 57, 58, 59, 62

## Question

在四个跨批次真实冲突及无联网充电桩失败触发边界均已得到明确决定后，如何对 [R01–R13 合并原子候选总账](../evidence/atomic-candidates/R01-R13-consolidated-atomic-candidates.tsv) 中 `review_disposition=hold-for-question-or-reframing` 的 241 条记录进行零遗漏、零静默改写的逐条复核，区分已被已批准决定覆盖、重复/只作证据、已超出当前目的地、可以当即精确表述为 HITL 问题、仍须重新原子化或仍缺证据的记录；应输出哪些可重建复核账、覆盖统计和失败式核验，并只将仍能精确表述且会改变候选需求的问题毕业为新的 HITL 子票据？

## Answer

已对固定输入 SHA-256 `b176262228842f6e5564f1f5d227321bb28932e498b254890a48cff952fd37f4` 中全部 241 条 `hold-for-question-or-reframing` 记录完成一对一复核，并建立以下规范产物：

- [冲突决定后问题复核账](../evidence/atomic-candidates/R01-R13-post-conflict-question-review.tsv)：逐条保留候选身份、原声明、上下文、原处置和指纹，追加复核处置、上下文指针、理由及复核指纹；不改写上游总账。
- [复核覆盖摘要](../evidence/atomic-candidates/R01-R13-post-conflict-question-review-summary.json)：记录输入哈希、批次/来源覆盖、处置统计、已决覆盖和新 HITL 票覆盖。
- [重建与失败式核验脚本](../evidence/atomic-candidates/build_and_verify_post_conflict_question_review.py)：固定输入哈希和 241 行边界，核验一对一覆盖、原批准状态、允许处置全集、子票元数据和候选到子票映射；输出采用临时文件原子替换。

逐条处置结果为：

| 复核处置 | 行数 | 结果 |
| --- | ---: | --- |
| `graduate-hitl-question` | 86 | 经一次错路由更正后收敛为 17 个仍会改变候选需求的精确 HITL 问题 |
| `duplicate-or-evidence-only` | 98 | 标题、分类标签、历史待办/阻塞、问题索引、重复标签或收敛说明只作证据 |
| `needs-evidence-before-candidacy` | 26 | 缺目标环境、接口、字段、配置值或版本绑定事实，不由批准人猜测 |
| `needs-atomic-reframing` | 16 | 混合已决/未决、业务/实现或多个业务后果，按指针拆向原子问题 |
| `out-of-current-destination` | 9 | UI/实现/历史交付和实验工具边界留在当前目的地外 |
| `covered-by-approved-decision` | 6 | 由已批准的运输取消抑制、MES 只读或 8005 仓位硬件决定覆盖 |

86 条原子问题只毕业到以下问题票，未预写答案：

- [决定 MES 运输候选的业务纳入与排除边界](64-decide-mes-transport-candidate-inclusion-and-exclusion-boundary.md)
- [决定复合运输、分区与多 SUBLOT 组合边界](65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)
- [决定派车评分、路网成本与无车响应升级规则](66-decide-dispatch-ranking-route-cost-and-no-response-escalation.md)
- [决定同站多任务取消与人工选任务开门边界](67-decide-same-station-cancellation-and-operator-task-opening.md)
- [决定到站拒收、取消与完工后纠错边界](68-decide-destination-rejection-cancellation-and-post-completion-correction.md)
- [决定故障车辆隔离、货物处置与人工越权边界](69-decide-faulted-agv-isolation-cargo-handling-and-manual-override.md)
- [决定安全联锁失败升级与紧急停止边界](70-decide-safety-interlock-failure-escalation-and-emergency-stop.md)
- [决定人员登录、维护操作与高风险权限边界](71-decide-human-login-maintenance-and-high-risk-permission-boundary.md)
- [决定仓位模型与 IO 映射配置、验证和启用门禁](72-decide-slot-io-mapping-activation-and-maintenance-policy.md)
- [决定监控新鲜度、告警升级、重试与日志留存规则](73-decide-monitoring-freshness-alert-retry-and-log-retention.md)
- [决定账户恢复与密码增强策略](74-decide-account-recovery-and-password-hardening-policy.md)
- [决定充电阈值、配置变更与异常生命周期](75-decide-charging-threshold-configuration-and-abnormal-lifecycle.md)
- [决定空闲返回、停靠点资格与调度竞争边界](76-decide-idle-return-parking-point-eligibility-and-arbitration.md)
- [决定地图拓扑同步与历史快照产品边界](77-decide-map-topology-sync-and-snapshot-product-boundary.md)
- [决定归档 AGV 的恢复与身份连续性](78-decide-archived-agv-restoration-and-identity-continuity.md)
- [决定 AREA 显式覆盖的维护与生效治理](79-decide-area-override-maintenance-and-effectivity-governance.md)
- [决定 RIoT 建单未确认时任务绑定、重试与释放边界](80-decide-riot-order-creation-uncertainty-binding-retry-release.md)

本次复核没有删除、合并、改写或批准任何来源声明，没有分配永久需求 ID，也没有把缺证据项转成让用户猜测的 HITL 问题。所有新票均为 `grilling`、仅含问题，并在本票解决前以原生 `Blocked by: 63` 关系挂接；本票解决后它们共同成为新的可处理 frontier。

2026-08-05 后续核对发现 `R03-A1571`（RIoT 建单未确认后的绑定保留、释放或重试）误挂在《决定同站多任务取消与人工选任务开门边界》。该行未被改写、批准或改变处置，仅把上下文指针迁移到《决定 RIoT 建单未确认时任务绑定、重试与释放边界》；因此 HITL 票总数由 16 更正为 17，86 条毕业记录和其它统计不变。
