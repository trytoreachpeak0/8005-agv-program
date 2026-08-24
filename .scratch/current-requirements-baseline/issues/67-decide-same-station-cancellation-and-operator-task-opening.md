# 决定同站多任务取消与人工选任务开门边界

Type: grilling
Status: resolved
Blocked by: 63

## Question

同一站点同时存在多个运输需求时，操作员取消的是需求、SUBLOT、仓位还是整次停靠，如何继承已批准的永久抑制规则；“不扫码选任务开门”是否与扫码并存、由谁使用、如何避免误选并保留何种责任和审计证据？

## Evidence rows

`R01-A0098`、`R01-A0099`、`R01-A0120`、`R01-A0122` 及已由票据 56 覆盖的相关取消证据。

## Answer

用户于 2026-08-05 逐项批准以下结论：

1. **同站取消继续沿用既有 DemandId 与永久抑制边界。** 操作员选择并取消一个 DemandId 对应的完整运输需求；未装任务使用空范围完成，部分装或已自动提交任务必须清空该 LoadBatch 的全部目标仓位。取消对象不是单个仓位、SUBLOT 文本或整次停靠，完成后仍以 `CANCELLED_BY_OPERATOR` 终结 DemandId，并永久抑制对应 TransportDemandKey。同车其它 DemandId、Sublot 与仓位不受影响。
2. **系统支持两种能力，但运行界面不同时提供两种入口。** 服务端维护项目级、带版本的 `LoadTaskEntryMode`，其值只能为：
   - `SUBLOT_ENTRY`：车载界面只提供扫码或键盘输入 SUBLOT；
   - `WORKLIST_SELECTION`：车载界面只提供从最新 CurrentStopWorklist 选择待装 DemandId。
   所有 8005 车辆和站点使用同一当前配置，车载端不得自行切换或同时显示两套入口。
3. **入口模式按装货开始边界冻结。** 参数变更不改变已经开始的 Sublot、OperationSession 绑定或仓位操作；后续尚未开始的装货使用新的配置版本。`WORKLIST_SELECTION` 是配置启用后的正式入口，不要求操作员逐次选择“条码不可读”等备用原因。
4. **普通现场操作员可以使用，不增加班组长逐次审批。** 只有当前站点具有相应作业权限、已按 OperatorVerificationPolicy 完成个人身份核验的 R-01～R-08 现场操作员可以使用 WorklistTaskSelection；确认后该操作员按既有 OperationSession 规则绑定本 Sublot。R-09 不需逐次批准，也不能仅凭班组长身份代替实际装货操作员。
5. **禁止一点即开门。** 操作员先选择一个当前可开始的待装 DemandId，界面再独立展示完整 SUBLOT、任务类型、起点、终点和 ExpectedBasketCount，并要求操作员明确确认已与实物标签核对。无需再次输入 SUBLOT 尾码，否则会退化为键盘输入入口。
6. **最终门禁仍由服务端掌握。** 确认后服务端必须以最新 worklistRevision 重新校验操作员、OperationSession、AGV、站点、DemandId、任务状态、availableActions、容量、仓位资格及不存在其它活动物理操作；任何过期、冲突、未知或不可执行结果均拒绝开门并下发最新清单，车载端不得信任旧界面状态。
7. **责任按可证明的控制链划分。** 系统负责清单正确性、完整展示、权限和最新状态复核，以及保证实际启动的 DemandId 与确认页一致。系统控制链完整且正确、事后又能证明实际装入了其它 SUBLOT 时，事件分类为 OperatorConfirmationMismatch 并关联确认操作员；该记录本身不证明确认人就是实际放货人，也不自动形成纪律或法律责任。界面、清单、服务端校验或任务—仓位绑定错误属于系统控制失败；实物标签、实际放货人或控制链无法还原时保持责任待查。
8. **每次 WorklistTaskSelection 形成不可修改的业务审计。** 最低记录包括入口模式及配置版本、操作员个人身份与当时角色、身份核验引用、OperationSession、AGV、站点、DemandId、TransportDemandKey、完整 SUBLOT、确认页展示的任务类型/起终点/ExpectedBasketCount、worklistRevision、选择/确认/服务端裁决时间、裁决结果与拒绝原因；通过时继续关联 SlotOperationAttemptId、目标仓位及后续装货、纠错、取消或错料事件。结构化事实足以复核，不强制保存界面截图或录像。
9. **入口模式变更同样受审计。** 每次修改 LoadTaskEntryMode 都保存修改人、修改前后值、原因、时间和配置版本；具体哪些维护角色可修改，由后续《决定人员登录、维护操作与高风险权限边界》统一决定，本票不重复预设。

上述结论解决 `R01-A0098`、`R01-A0099`、`R01-A0120` 与 `R01-A0122`。复核时发现原先一并路由到本票的 `R03-A1571` 实际讨论 RIoT 建单未被确认后的任务绑定、释放和重试，与同站取消或装货入口无关；该证据已迁移到开放票据[决定 RIoT 建单未确认时任务绑定、重试与释放边界](80-decide-riot-order-creation-uncertainty-binding-retry-release.md)，本票不宣告解决该问题。
