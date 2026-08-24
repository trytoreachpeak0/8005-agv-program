# R03 用例材料调查

## 边界、固定身份与勘误

本报告只调查 [material-inventory.tsv](../material-inventory/material-inventory.tsv) 中 `batch_id=R03` 的 48 行：46 份 `type: use-case` 的 UC、1 份模板指南和 1 份空白待办文件。使用 `Get-FileHash -Algorithm SHA256 -LiteralPath <path>` 对当前工作树逐件重算，**48/48 与固定清单的 SHA-256 匹配，0 漂移**。下表显示前 12 位，完整哈希、字节数与捕获时间仍以清单为准。

调查前先应用 [git-status-corrections.tsv](../initial-snapshot/git-status-corrections.tsv)：[可能有哪些 user case.md](../../../../requirement-documents/03-use-cases/%E5%8F%AF%E8%83%BD%E6%9C%89%E5%93%AA%E4%BA%9Buser%20case.md) 虽在原始快照中被记为 `untracked`，但正确身份是 `tracked-clean`。固定 HEAD `1469d6309d00b0abb792f6cd686aed68286e638e` 中的 `git ls-tree` 返回 blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`，与勘误一致；其 Git 形成史因此没有被跳过。

方法：逐件读取 frontmatter、描述/流程/备注/TBD/关联 UC 与 BR；对每个路径运行 `git log --follow`；反查文档自述的 [原始 user case](../../../../requirement-documents/user%20case.md)、[愿景与范围](../../../../requirement-documents/00-vision/vision-and-scope.md)、[MES 任务模型](../../../../mes/AGV%E7%B3%BB%E7%BB%9F%E4%B8%9A%E5%8A%A1%E4%B8%8EMES%E4%BB%BB%E5%8A%A1%E6%A8%A1%E5%9E%8B.md)、[干系人角色](../../../../requirement-documents/01-stakeholders/stakeholders-and-user-classes.md) 及 [BR 目录](../../../../requirement-documents/02-business-rules/README.md)。

## 批准四要素与分类口径

本调查把可核查批准定义为同时具有：**具体决定内容、具名且具权限的批准人、批准日期、适用范围与精确版本/哈希**。结果是：

- 46/46 UC 的 frontmatter 都是 `status: draft`；`created_by`/`updated_by`、Git 作者或提交信息只能证明内部编辑史，不是业务批准。
- 多份备注写有“经与用户确认”、“已确认”或“与 RIOT 确认”，但都未同时附上原始会话/纪要、具名人员与授权角色、日期及本次固定哈希/适用 8005 范围，因此 **0/46 有合格批准链**。这些短语是后续证据请求的索引，不是本调查可代为追认的批准。
- 下表分类：`C`=有可评审的用户目标/现场场景，可作为**送审 UC 候选**；`I`=由缺口、其他 UC/BR/ADR 或系统内部步骤扩展出的**内部设计推演**；`G`=写作指南；`T`=空白待办。`C` 只表示适合让权威方逐项审查，**不表示已批准**。

Git 历史缩写：`96`=`96eb203` (2026-07-13 首次提交)，`0b`=`0b2246c` (2026-07-13 需求/工作流扩展)，`1d`=`1db3e93` (2026-07-14 AGV 用例批量新增)，`48`=`48a74dc` (2026-07-14 地图/模型/规则扩展)，`ec`=`ecd0fd8` (2026-07-15 RIOT/环境验证扩展)，`49`=`493ac5a` (2026-07-31 车载—服务端权威与站点作业大幅改写)。“→”仅表示该文件在这些提交中的变更序列，不赋予提交批准效力。

## 48/48 文档级证据矩阵

### 01 现场作业（9/9）

| 材料（SHA 前 12）/历史 | 原始来源、范围与 BR 派生 | 分类、当前适用性与证据缺口 |
|---|---|---|
| [UC-001](../../../../requirement-documents/03-use-cases/01-site-operations/uc-001-load-completed-lot-into-slot.md) `2eb915704d97`；`96→0b→48→ec→49` | 由原始站点搬运场景和 UC/BR 持续扩展；关联 BR-001/012/013/014；范围是起点装货、多花篮/多仓位、自动 LoadBatch 提交 | `C`；当前内部站点装货主候选，`49` 已改写旧的手工确认/单仓语义；1 个 TBD，整个新版本须重新送审。 |
| [UC-002](../../../../requirement-documents/03-use-cases/01-site-operations/uc-002-confirm-task-completion.md) `00e4d1ea89c4`；`96→0b→ec→49` | 从原装货结束场景演化为结束当前站装货；无 `related_br` | `C`；`49` 版是 StationDeparture/StopClosure 候选，旧“批次人工确认”语义已被替代；不得继承旧版确认。 |
| [UC-003](../../../../requirement-documents/03-use-cases/01-site-operations/uc-003-agv-arrives-at-designated-station.md) `6131ca69ef26`；`96→0b→48→49` | 从 UC-001 拆分，又把轮询到站拆给 UC-009；BR-001；当前只覆盖可信到站事件后的状态/投影/HMI | `C`；可送审“到站后用户看到什么”，但软件权威投影属内部设计；1 TBD，边界须与 UC-009 一起审。 |
| [UC-005](../../../../requirement-documents/03-use-cases/01-site-operations/uc-005-retrieve-mis-stored-product-from-slot.md) `b8dad821f105`；`96→0b→48→ec→49` | 从 UC-001 放错异常拆分；后续改为 LoadCorrection/原仓位重放；无 `related_br` | `C`；可送审的现场纠错候选，但 `49` 内部状态机不能由“放错需取出”反推已批准。 |
| [UC-006](../../../../requirement-documents/03-use-cases/01-site-operations/uc-006-cancel-transport-task-upon-arrival.md) `d99f3254a682`；`96→0b→48→ec→49` | 从到站取消场景演化为离站前按 DemandId 清空并取消；无 `related_br` | `C`；取消用户目标可送审；`49` 的硬件闭环、多 SUBLOT 隔离和抑制语义是内部细化。 |
| [UC-010](../../../../requirement-documents/03-use-cases/01-site-operations/uc-010-unload-completed-lot-at-destination-station.md) `727d84c8dfd5`；`96→0b→48→ec→49` | 文档明说从根 [user case.md](../../../../requirement-documents/user%20case.md) 的工艺起终点场景拆分；BR-013/014；范围是终点自动识别与卸货 | `C`；这是直接送审价值最高的 UC 之一，但根原始文件本身也无批准链；3 TBD，`49` 已改写卸货完成语义。 |
| [UC-043](../../../../requirement-documents/03-use-cases/01-site-operations/uc-043-verify-identity-and-manage-operation-session.md) `338b82a1c9ed`；`ec→49` | 后期为 UC-001/002/005/006/010 补的身份核验和操作会话；无 BR | `I`；`49` 版是 8005 装货身份/会话内部设计；必须由生产、MES/IT、权限责任方送审，不是原始客户用例。 |
| [UC-044](../../../../requirement-documents/03-use-cases/01-site-operations/uc-044-reopen-slot-after-incomplete-retrieval.md) `2fe7f7bdc580`；`ec→49` | 从 UC-010 旧 E4.1 残留异常拆分；无 BR | `I`；作为卸货闭环子流程仍当前被 FR/TC 引用，但“无强制放行上限、自动重开”需安全与现场专项审查。 |
| [UC-046](../../../../requirement-documents/03-use-cases/01-site-operations/uc-046-handle-station-departure-wait-timeout.md) `d1cb766bd7d6`；`49` | 仅在车载—服务端权威改写中形成；无 BR；范围是 StationDepartureWaiting 超时内部过程 | `I`；与 FR-031/ADR-0055 一起是当前内部超时方案，不是可证明的用户目标；默认时间/HMI/自动结束需逐项送审。 |

### 02 仓位与硬件（7/7）

| 材料（SHA 前 12）/历史 | 原始来源、范围与 BR 派生 | 分类、当前适用性与证据缺口 |
|---|---|---|
| [UC-011](../../../../requirement-documents/03-use-cases/02-slot-and-hardware/uc-011-view-slot-monitoring-dashboard.md) `212495ce9b6a`；`96→0b→49` | 自述来自用户对仓位状态看板的讨论；无 BR；只读监控 | `C`；用户目标可送审；3 TBD，显示字段、可见范围、刷新频率未定。 |
| [UC-014](../../../../requirement-documents/03-use-cases/02-slot-and-hardware/uc-014-enable-disable-slot.md) `2bf87510f464`；`96→0b→48→49` | 仓位管理用户目标；无 BR；`49` 将管理可用性与物理事实分离 | `C`；可送审启停规则，但 Actor 仍“待定”，状态模型是内部候选。 |
| [UC-015](../../../../requirement-documents/03-use-cases/02-slot-and-hardware/uc-015-slot-door-unlock-open-test.md) `7a5f4325d17a`；`96→0b→48→49` | 自述为用户提出的开锁/弹开测试；无 BR | `C`；硬件维护场景可送审；必须与 UC-004 安全联锁、UC-039 点位前提一起审。 |
| [UC-016](../../../../requirement-documents/03-use-cases/02-slot-and-hardware/uc-016-slot-light-curtain-function-test.md) `cb653b589118`；`96→0b→49` | 自述为用户提出的光幕功能测试；无 BR | `C`；场景可送审；2 TBD，主参与者仍未最终确认。 |
| [UC-017](../../../../requirement-documents/03-use-cases/02-slot-and-hardware/uc-017-slot-door-state-detection-test.md) `c1b094aa68a0`；`96→0b→49` | 仓锁反馈/闩合识别测试；无 BR；`49` 吸收“无独立门磁”内部结论 | `C`；维护测试候选；需硬件/IO 责任人确认信号能力与适用车型。 |
| [UC-018](../../../../requirement-documents/03-use-cases/02-slot-and-hardware/uc-018-io-point-mapping-verification-test.md) `dd1965f4af48`；`96→0b→48→49` | 自述为用户提出的 IO 映射双向核对；无 BR | `C`；场景可送审；2 TBD，Actor/是否自动化未定，不得用现有测试通过反推需求正确。 |
| [UC-039](../../../../requirement-documents/03-use-cases/02-slot-and-hardware/uc-039-maintain-slot-io-point-mapping.md) `b9e6e0e74159`；`48→49` | 为填补 UC-018 假定“映射已存在”的建表/维护缺口而新增；无 BR | `I`；当前是设备接入闭环的内部候选；6 TBD，包含待核对是否阻断业务、二次认证等未决策项。 |

### 03 AGV 车队管理（6/6）

| 材料（SHA 前 12）/历史 | 原始来源、范围与 BR 派生 | 分类、当前适用性与证据缺口 |
|---|---|---|
| [UC-013](../../../../requirement-documents/03-use-cases/03-agv-fleet-management/uc-013-enable-disable-agv.md) `835e08ba1846`；`96→0b→1d` | 自述为用户提出的本系统车辆启停；无 BR | `C`；可送审，但 4 TBD 且 Actor 暂定；“待生效不中断当前任务”需单独确认。 |
| [UC-019](../../../../requirement-documents/03-use-cases/03-agv-fleet-management/uc-019-register-agv-from-rcs.md) `9a94e7194e79`；`0b→1d→48` | 接入 AGV 目标，后因用户提出多仓位模型而改写；BR-002/008 | `C`；可送审车辆接入与模型绑定；2 TBD，归档恢复等边界未定。 |
| [UC-020](../../../../requirement-documents/03-use-cases/03-agv-fleet-management/uc-020-maintain-agv-dispatch-profile.md) `99fb50c10570`；`0b→1d→48` | AGV 调度配置，仓位结构已被 UC-038/BR-008 模型快照替代；BR-002/008 | `C`；只应送审当前 `48` 的可编辑字段；3 TBD，旧手工维护仓位语义不再适用。 |
| [UC-021](../../../../requirement-documents/03-use-cases/03-agv-fleet-management/uc-021-archive-agv.md) `64cbde288954`；`0b→1d` | 本地 AGV 归档；BR-002 | `C`；可送审；2 TBD，恢复/外部 RCS 状态边界缺证据。 |
| [UC-022](../../../../requirement-documents/03-use-cases/03-agv-fleet-management/uc-022-view-agv-fleet-and-availability.md) `5236a42f1ff7`；`0b→1d` | 车队可见性和 BR-002 分配原因 | `C`；看板目标可送审；1 TBD，展示字段/刷新与权限范围需定稿。 |
| [UC-038](../../../../requirement-documents/03-use-cases/03-agv-fleet-management/uc-038-maintain-agv-slot-model.md) `b90314fae668`；`48` | 自述来自用户在 UC-019 讨论中提出的多仓位模型；BR-002/008 | `C`；场景可送审，但 Draft/Published/Retired、不可变快照、二次认证是内部设计细化，需运维/硬件/安全权威方分项确认。 |

### 04 运输任务与派发（5/5）

| 材料（SHA 前 12）/历史 | 原始来源、范围与 BR 派生 | 分类、当前适用性与证据缺口 |
|---|---|---|
| [UC-007](../../../../requirement-documents/03-use-cases/04-transport-task-dispatch/uc-007-sync-transport-task-from-mes.md) `3698770e3790`；`96→0b→1d→ec→49` | 系统内部 MES 轮询/投影；自述吸收 [MES 任务模型](../../../../mes/AGV%E7%B3%BB%E7%BB%9F%E4%B8%9A%E5%8A%A1%E4%B8%8EMES%E4%BB%BB%E5%8A%A1%E6%A8%A1%E5%9E%8B.md)；BR-001/003/012/014 | `I`；是当前内部 MES ingest 候选，不是人的用例；1 TBD，MES 契约/只读边界必须由 MES 责任方审。 |
| [UC-008](../../../../requirement-documents/03-use-cases/04-transport-task-dispatch/uc-008-dispatch-move-order-to-riot.md) `4039759a3073`；`96→0b→1d→48→ec` | 从 UC-003/007/BR-001 排除的 RIOT 下发环节拆分；BR-001/015 | `I`；当前是调度—RIOT 内部契约候选；1 TBD，“每车 RIOT 队列 0/1”等声称无合格原始批准。 |
| [UC-009](../../../../requirement-documents/03-use-cases/04-transport-task-dispatch/uc-009-monitor-move-order-until-arrival.md) `4e50a9c982c0`；`96→0b→1d→49` | 从 UC-003 拆出轮询直到可信到站；BR-001 | `I`；是 UC-003 前置技术流程；1 TBD，轮询、超时、到站语义需 RIOT 契约证据。 |
| [UC-023](../../../../requirement-documents/03-use-cases/04-transport-task-dispatch/uc-023-allocate-transport-tasks-to-agv.md) `d82c95312790`；`0b→1d→ec` | 系统内部任务分配；BR-001/002/014/015 | `I`；主要是算法/状态机推演，4 TBD；不应以 UC 文档形式掩盖 BR-001/002/015 未决的决策。 |
| [UC-042](../../../../requirement-documents/03-use-cases/04-transport-task-dispatch/uc-042-handle-agv-fault-and-reassign-or-terminate-tasks.md) `944b856398ab`；`48→49` | 为填补车辆离站后故障处置缺口新增；引用 MES 模型的“首仓开始装货”；BR-001/002 | `I`；12 处 TBD，文档自述为“初稿骨架”；故障状态、应急开锁、人工搬运和二次认证均不可直接进基线。 |

### 05–11 充电、地图、工作流、权限、日志、安全与停靠（19/19）

| 材料（SHA 前 12）/历史 | 原始来源、范围与 BR 派生 | 分类、当前适用性与证据缺口 |
|---|---|---|
| [UC-012](../../../../requirement-documents/03-use-cases/05-agv-charging/uc-012-manually-dispatch-agv-to-charge.md) `28d317e8b576`；`96→0b→1d→48` | 自述为用户提出的空闲车手动充电；BR-007；明确不含低电自动回充 | `C`；手动目标可送审；9 TBD，RIOT 充电接口、阈值和异常处置未闭合。 |
| [UC-037](../../../../requirement-documents/03-use-cases/05-agv-charging/uc-037-maintain-agv-charging-strategy-configuration.md) `92bfe6345343`；`0b→1d` | 自述为用户提出的充电策略配置；BR-007；不含自动充电执行 | `C`；配置目标可送审；5 TBD，“电量优先且不抢占已充电车”等内容需原始记录。 |
| [UC-024](../../../../requirement-documents/03-use-cases/06-area-station-mapping/uc-024-maintain-area-station-mapping.md) `e5ba9b098540`；`0b→1d→48→ec` | AREA—站点命名解析/显式覆盖；BR-001/003/015 | `I`；地图数据模型内部候选，1 TBD；需用实际 RIOT 地图契约和厂区 AREA 权威表审查。 |
| [UC-045](../../../../requirement-documents/03-use-cases/06-area-station-mapping/uc-045-sync-map-topology-from-riot.md) `5d4630b8d335`；`ec` | 填补“需最短路成本但无拓扑同步”的内部缺口；BR-002/003/015 | `I`；7 TBD，属地图/路径成本技术设计草案，不是可直接送审的人员用例。 |
| [UC-025](../../../../requirement-documents/03-use-cases/07-workflow-engine/uc-025-maintain-workflow-template.md) `859d4880dcbd`；`0b→1d` | 工作流模板管理；BR-004/005/006 | `I`；内部编排平台候选；虽无 TBD 字样，仍无原始客户目标或批准链。 |
| [UC-026](../../../../requirement-documents/03-use-cases/07-workflow-engine/uc-026-select-template-and-create-workflow-instance.md) `408299ca1a0c`；`0b→1d→48` | 由 BR-003/004/005/006 派生的实例创建 | `I`；系统内部过程，无原始用户来源；应随模板选择/版本绑定原子决策送审。 |
| [UC-027](../../../../requirement-documents/03-use-cases/07-workflow-engine/uc-027-execute-workflow-steps.md) `065d9853aae9`；`0b→1d` | 由 BR-001/002/003/005/006 和步骤目录派生 | `I`；编排用例，文档自述不取代原子 UC；不应单独当作客户需求。 |
| [UC-028](../../../../requirement-documents/03-use-cases/07-workflow-engine/uc-028-handle-workflow-step-exception.md) `cbe177b11c8c`；`0b→1d` | 由 BR-002/003/005/006 派生的步骤级重试/人工介入/终止 | `I`；异常策略内部候选；无批准链，且需与 UC-042 任务级故障分界。 |
| [UC-029](../../../../requirement-documents/03-use-cases/07-workflow-engine/uc-029-view-workflow-instance-progress.md) `78550740ee36`；`0b→1d` | 由 BR-004/005/006 派生的流程进度查看 | `I`；可见性需求可再整理成送审候选，但当前主要是内部模型展示，无原始来源。 |
| [UC-030](../../../../requirement-documents/03-use-cases/08-user-and-access/uc-030-maintain-user-account.md) `e3ff9ad327fa`；`0b→1d→ec` | 账号管理；BR-010/011 | `I`；常规内部管理能力，无项目客户/信息安全原始决定；需 IT/安全送审。 |
| [UC-031](../../../../requirement-documents/03-use-cases/08-user-and-access/uc-031-maintain-role-and-permission.md) `32c699a9c499`；`0b→1d→ec` | 角色与权限管理；BR-010 | `I`；内部 RBAC 推演，需具名业务/安全责任人批准角色矩阵。 |
| [UC-032](../../../../requirement-documents/03-use-cases/08-user-and-access/uc-032-assign-user-roles.md) `5ce7d6f61a37`；`0b→1d→ec` | 用户角色分配；BR-010 | `I`；内部 RBAC 操作流程；没有权限所有者、双人复核或适用范围证据。 |
| [UC-033](../../../../requirement-documents/03-use-cases/08-user-and-access/uc-033-login-and-session-management.md) `67094351a7e7`；`0b→1d→ec` | 配置端登录/会话；BR-011 | `I`；安全机制内部候选，与 UC-043 现场 MES 身份会话不是同一范围；需分开审。 |
| [UC-034](../../../../requirement-documents/03-use-cases/09-logs-and-audit/uc-034-query-and-export-audit-logs.md) `d811416a0e4a`；`0b→1d→ec` | 安全/合规审计查询；无 BR | `I`；可再整理为利益相关方送审候选，但当前无合规权威来源、保留周期/脱敏批准。 |
| [UC-035](../../../../requirement-documents/03-use-cases/09-logs-and-audit/uc-035-query-material-handling-history.md) `e55c08115449`；`0b→1d` | 从 UC-001/002/005/006/010 的 Postcondition 事件派生的只读追溯 | `I`；业务查询目标可后续送审，但当前的查询键、权限范围与保留义务均为内部派生。 |
| [UC-036](../../../../requirement-documents/03-use-cases/09-logs-and-audit/uc-036-query-and-stream-system-logs.md) `c6ca2cee7991`；`0b→1d` | 技术日志实时查看；无 BR | `I`；运维/排障内部能力；敏感字段、脱敏、可见组件范围需 IT/安全权威方确认。 |
| [UC-004](../../../../requirement-documents/03-use-cases/10-safety-and-interlock/uc-004-slot-door-safety-interlock.md) `3b0bb4b8c6ae`；`48` | 从 UC-001 开门时移动异常拆分成全局软件安全联锁；BR-002 | `I`；5 TBD；查询/轮询拒绝、暂停/恢复/取消是安全关键内部方案，且文档明说无硬件联锁；必须单独安全送审，不能因“与 RIOT 确认”就批准。 |
| [UC-040](../../../../requirement-documents/03-use-cases/11-agv-parking/uc-040-maintain-agv-parking-point-configuration.md) `c9ca1052d743`；`48` | 从 [vision-and-scope.md](../../../../requirement-documents/00-vision/vision-and-scope.md) “返回驻点”填补配置缺口；BR-009 | `C`；停靠点配置可送审；3 TBD，保存前是否禁用车辆等未定。 |
| [UC-041](../../../../requirement-documents/03-use-cases/11-agv-parking/uc-041-return-idle-agv-to-parking-point.md) `98a1037dc6f0`；`48` | 从同一愿景条目填补自动执行缺口；BR-009 | `C`；“空闲返驻点”目标可送审；7 TBD，与 UC-008/012 的竞争、锁和重试是内部设计。 |

### 指南与待办（2/2）

| 材料（SHA 前 12）/历史 | 原始来源与范围 | 分类、当前适用性与证据缺口 |
|---|---|---|
| [可能有哪些 user case.md](../../../../requirement-documents/03-use-cases/%E5%8F%AF%E8%83%BD%E6%9C%89%E5%93%AA%E4%BA%9Buser%20case.md) `e3b0c44298fc`；`96` | 0 字节空文件；勘误后为 `tracked-clean`；固定 HEAD blob 为 Git 空 blob `e69de29…` | `T`；只能证明曾创建一个用例头脑风暴/待办路径；**无任何可恢复的场景、来源、范围或批准内容**，不能生成需求。 |
| [uc-template-guide.md](../../../../requirement-documents/03-use-cases/uc-template-guide.md) `c28f3e41cf01`；`96` | `type: template-guide,status: reference`；规定 frontmatter、正常/备选/异常流程及 Notes 的写法 | `G`；只是内部写作/结构参考；指南中说可用 Notes 记录“用户澄清”，但 Notes 不会自动成为批准证据，也不表达系统需求。 |

## 横向派生与当前适用性

1. **可送审不等于可入基线。** 上表的 `C` 为 22 份场景/目标级候选；`I` 为 24 份内部设计推演。两类都是 `draft`、都无合格批准链；`I` 中的安全、权限、MES/RIOT 契约和状态机不应以“UC 已写好”代替相应权威方的原子批准。
2. **原始材料链强弱不一。** UC-010 明确指向根 `user case.md`；UC-040/041 指向愿景功能树；UC-007/042 指向 MES 模型。其余多数只在自身 Notes 声称“用户提出/确认”，或从其他 UC/BR 拆分/补缺，缺少可独立复核的原始会话。[BR 调查](R02-requirements-framing-and-business-rules.md) 也已证明 BR 自身不是可批准的原始来源，因此 `related_br` 只提供派生链，不提升权威等级。
3. **`49` 是显著的语义替代点。** UC-001/002/003/005/006/010/043/044/046 被重构为 LoadBatch、LoadCorrection、StationOperationGuard、StopClosure/StationDeparture 与车载投影；UC-011/014–018/039 被对齐物理占用、锁 DI、IO 有效性和管理可用性；UC-042 也被改写故障后抑制语义。旧提交可用于说明“为什么改”，**不得与当前哈希混合为一个已确认版本**。下游 [R04 功能需求调查](R04-functional-requirements.md) 已显示这一替代继续派生到 FR-003–014/031，仍不产生批准。
4. **TBD 是范围警告，不是小修饰。** UC-042 (12)、UC-012 (9)、UC-041/045 (7)、UC-039 (6)、UC-004/037 (5) 的 TBD 集中在故障、充电、地图、IO、安全和竞争策略，这些材料只能作为讨论骨架。没有 TBD 字样的文档也不因此获得批准。

## 结论与后续证据请求

- **覆盖与分类：**48/48 材料已逐份记录；22 份 `C` 送审候选，24 份 `I` 内部设计推演，1 份 `G` 指南，1 份 `T` 空白待办。**0 份被本调查提前批准。**
- **证据请求：**对每个 `C` 以当前 R03 SHA-256 为版本边界，请具名生产/运维/安全/客户责任人按流程步骤批准或驳回，记录日期和适用车型/站点/阶段。对每个 `I`，先拆成可独立决策的 BR/FR/接口/安全条目，再找相应权威方；不要把 Git/ADR/TC/代码现状当作批准人。
- **待追回原件：**优先请求文档中所称的用户/RIOT 确认会话、MES 任务模型的决策记录、地图/充电/锁/光幕/IO 契约和 2026-07-30–31 站点作业改写的原始会议材料。若无法找回，就对当前哈希执行新一轮显式审查，不从“已确认”短语推定历史批准。
