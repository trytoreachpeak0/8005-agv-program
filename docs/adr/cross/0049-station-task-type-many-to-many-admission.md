# 站点与任务类型采用多对多准入关系

同事初稿 §2.2 将站点、任务和业务有效性判断归服务端，§5.1 规定操作员输入 SUBLOT。项目允许某些站点接受不属于本站点原始任务列表的 SUBLOT，但是否允许取决于任务类型，而不是任务原本来自哪个站点。

服务端收到 Sublot 后先全局解析唯一 DemandId 和其冻结的 taskType，再通过 StationTaskTypeAdmission 判断当前 stationId 是否允许该 taskType。准入关系以单一多对多表或等效集合保存：

`StationTaskTypeAdmission(stationId, taskType)`

`(stationId, taskType)` 为唯一键。存在记录表示允许；记录缺失、stationId 未知、taskType 缺失或未知均默认拒绝，并返回稳定原因码 `TASK_TYPE_NOT_ALLOWED_AT_STATION`。不根据 DemandId 原任务站点自动允许或拒绝。

配置入口以站点为视角展示“当前站点允许的任务类型”，但底层不再维护一份 taskType→stations 反向配置；需要查询某任务类型可在哪些站点处理时，从同一关系反向查询。

车载端不接收完整准入配置，只提交 SUBLOT 和当前站点上下文并显示服务端结果。某 DemandId 在任一允许站点被接受并建立 SublotReservation 后，全局进入该操作，原任务列表及其它站点快照由服务端同步更新。

准入配置变更的生效边界遵守 ADR-cross-0050：服务端在 OperationCommitPoint 前按当前版本再次校验并冻结 AdmissionDecisionSnapshot；指令发出后的当前操作不被后续配置变化撤销。

准入关系的第一版维护方式遵守 ADR-cross-0051：存入服务端数据库，由软件人员通过受控脚本或导入维护，不在车载端或业务界面编辑。

**Status**: accepted

**Considered Options**:
- 按任务原站点白名单判断（拒绝：实际规则取决于任务类型，同类任务可由多个站点处理）
- 同时维护 station→taskTypes 与 taskType→stations 两套配置（拒绝：双写容易产生不一致）
- 使用 `(stationId, taskType)` 单一多对多关系，界面按站点展示（采纳）

**Consequences**:
- 服务端需要站点与稳定 taskType 代码的关系表及唯一约束。
- 未配置默认拒绝，新增任务类型或站点不会意外获得处理权限。
- CurrentStopWorklistSnapshot 只展示本次停靠已纳入的作业；不在清单中的 SUBLOT 也可以提交，由服务端全局解析并执行准入检查，接受后再通过更高版本快照纳入清单。
- 任务准入与 SublotReservation 是两个连续检查：允许该类型不等于该 DemandId 当前可重复执行。
- 后续接口确认稿应在 §5.1 和 §14 增加跨站点 SUBLOT 输入与任务类型准入规则。
