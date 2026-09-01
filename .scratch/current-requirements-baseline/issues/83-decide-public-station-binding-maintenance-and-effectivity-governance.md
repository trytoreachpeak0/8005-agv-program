# 决定公共业务点绑定的维护与生效治理

Type: grilling
Status: resolved
Blocked by: 77, 79

## Question

在当前不提供 AREA 显式覆盖、每张 Map 上每种 PublicStationFunction 必须显式绑定唯一 FixedTaskStation 的模型下，谁负责识别、录入、复核和批准公共业务点绑定；Map 投运前是否必须补齐该图所需功能，绑定如何版本化、生效、回滚和审计，地图站点改名、删除、重建或任务类型所需功能变化时如何检测失效，已有 TransportDemand 如何保持冻结边界，且哪些操作需要二次认证或额外审批？

## Evidence rows

`R01-A0747`、`R01-A0748`，以及《决定复合运输、分区与多 SUBLOT 组合边界》中已批准的 PublicStationFunction / FixedTaskStation 边界和《决定 AREA 显式覆盖的维护与生效治理》的用户澄清。

## Comments

### 2026-08-24 — 用户批准第一轮推荐值

用户确认本轮全部采用推荐值：

- 公共站点规范绑定键为 `mapId + PublicStationFunction`；TASK_TYPE 只通过受控关系引用功能，不重复保存站点。
- Map 可先进入目录，但只有当前启用任务类型所需的全部 PublicStationFunction 都完成有效绑定后，这些任务类型才可在该 Map 投运；不强迫配置未启用功能。
- MaintenanceAdministrator 负责现场识别与核对，SystemAdministrator 负责录入、修改、激活和回滚；SystemAdministrator 可独立完成核对与激活，不增加双人审批或基线最终批准人逐值批准。
- MaintenanceAdministrator 或 SystemAdministrator 均可立即暂停可疑绑定；恢复必须由 SystemAdministrator 重新校验并激活。
- 同一 Station 默认不得同时绑定多个 PublicStationFunction；未来如确需复用，须以新的现场物理与作业证据重新批准，不作为普通配置放行。

### 2026-08-24 — 用户批准第二轮及后续推荐值

用户确认本票以及后续 HITL 继续使用代理明确展示的推荐值。本票因此按推荐值收敛不可变绑定集版本、原子激活与重校验回滚、地图变化失效分类、TASK_TYPE 功能规则版本、TransportDemand 冻结边界、敏感动作二次认证、结果未知对账和完整审计。

## Answer

经用户作为当前基线最终批准人确认，8005 的公共业务点绑定、投运、变更、失效与审计遵守以下边界：

1. **规范绑定键是 `mapId + PublicStationFunction`。** TASK_TYPE 只通过受控的任务类型—功能规则引用 PublicStationFunction，不按 TASK_TYPE 重复维护站点值。每张 Map 每种功能最多一个 FixedTaskStation，且同一 Station 不得同时承担多个 PublicStationFunction；未来确需复用时须以新的现场物理和作业证据重新批准，不可以普通配置放行。
2. **Map 目录可见不等于公共站点就绪。** MapPublicStationRequirementSet 是该 Map 当前获准启用的任务类型所实际依赖的 PublicStationFunction 集合。相关任务类型只有在全部需求功能具有有效绑定后才可投运；不强迫每张 Map 配齐尚未启用的其余功能，也不允许为缺失功能填入默认站点。
3. **现场核对与配置激活遵守现有两级管理员权限。** MaintenanceAdministrator 可识别公共功能、核对实际物理用途与目录中的具体 Station，但不可编辑或激活绑定；SystemAdministrator 负责录入、修改、激活、恢复和回滚。SystemAdministrator 可独立完成核对与激活，不新增双人审批链，也不要求当前基线最终批准人逐个批准现场站点值。
4. **每张 Map 以完整不可变绑定集版本生效。** PublicStationBindingSetVersion 保留该 Map 完整的功能—Station 绑定、MapPublicStationRequirementSet、所依赖的任务类型规则版本和 MapStationCatalogSnapshot 修订。草稿、复制和校验不影响运行；候选只能整图原子激活，任一失败都不得部分发布、逐功能切换或混用新旧版本。
5. **激活必须 fail-closed 验证完整性。** 候选必须使用当前新鲜的 MapStationCatalogSnapshot，确认 Map 与 Station 身份存在且有效、站点与 Map 同图、同图同功能唯一、同一 Station 未复用多功能、当前需求功能全部完整，并具有绑定站点的现场用途核对记录。目录不新鲜、任一结果未知或任一规则冲突时均不得激活。
6. **敏感生效动作要求新鲜二次认证，但不增加另一批准人。** 激活新版本、重新激活被暂停绑定、回滚，以及移除当前生效绑定或缩改任务类型范围时，SystemAdministrator 必须使用当前密码重新认证并明确确认影响预览。草稿编辑、校验、影响预览和立即暂停不要求二次认证。
7. **可疑绑定可以立即收紧，恢复必须严格重验。** MaintenanceAdministrator 或 SystemAdministrator 均可对明确 Map 与 PublicStationFunction 提交 PublicStationBindingHold，立即阻断对该功能发起新的站点使用，不等待二次认证或批准。只有 SystemAdministrator 在完成现场核对、当前目录校验和二次认证后才可重新激活；暂停不自动到期，也不删除绑定身份与历史。
8. **目录变化按稳定身份与语义风险分类。** 同一 `mapId + stationId` 只改名时，名称不改变 Station 身份，但可能表示现场用途变化，因此自动暂停相关绑定的新使用并要求现场复核；Map 在同一 `mapId` 下改名时暂停该 Map 的全部公共站点绑定并复核。Station 删除、停用或换 `stationId`，以及 Map 删除或换 `mapId`时，原绑定立即失效；同名新身份仍是新 Station/Map，禁止按名称自动重绑。
9. **变化影响以必要范围收敛。** 单一站点变化只阻断依赖受影响 PublicStationFunction 的新使用，其余已验证功能继续运行；Map 身份或名称变化则按上述边界处理全图。系统无法自动发现“Map/Station 身份和名称均未变但物理用途已改变”；现场发现此情况时必须立即暂停相关绑定。首次投运、上述目录变化、任务类型规则变化、现场用途变化报告或人工暂停均触发复核；不设置无证据支持的定期重复审批。
10. **任务类型—功能关系本身也必须版本化。** TaskTypePublicStationRuleVersion 固定每个受支持 TASK_TYPE 使用的 PublicStationFunction 及其在运输中是起点还是终点。新任务类型或关系变更只有在相关 Map 的绑定版本已满足新功能需求时才可激活；规则与绑定在同一发布门禁内校验，不允许先放行缺失固定站点的 TASK_TYPE。
11. **TransportDemand 冻结规则、站点和所依赖版本。** 新建 TransportDemand 记录其 TaskTypePublicStationRuleVersion、PublicStationBindingSetVersion 与 ResolvedTransportStation；后续规则、绑定或名称变化不重写、迁移或重新解析既有任务。旧站身份仍存在、目录新鲜且未被暂停时，既有任务可继续使用冻结站点；冻结站点失效或被暂停时，尚未创建的新 RIoT move 必须阻断并记录精确原因。
12. **已存在的 RIoT 订单不被配置变化自动取消。** 已建单或正在执行的移动继续按 OrderRef 观察、对账和收敛；目录、绑定、规则或暂停变化不自动改单、换站、换图或取消。后续尚未建单的停靠继续遵守当前新鲜目录、绑定暂停与 RouteCost 门禁。
13. **回滚是受控的新激活，不是历史覆盖。** SystemAdministrator 只可选择旧不可变版本的内容，在当前新鲜目录、当前任务类型功能规则和完整现场核对下重新校验，并作为一次新的激活记录生效。回滚仍只影响之后创建的 TransportDemand，不回写已有任务。
14. **激活结果未知时不猜测生效版本。** 激活、恢复或回滚超时、断联或返回矛盾结果时，相关 Map 暂停新的公共站点使用；系统必须读取实际生效版本、版本身份和完整内容完成对账，禁止以请求成功、本地预期或部分功能状态表示整图已生效。
15. **全部操作和变化证据必须不可改写地审计。** 在票据 71 已批准字段之外，记录 Map、PublicStationFunction、变更前后 Station 身份与名称、目录修订、新旧规则与绑定版本、影响预览、变更理由、现场核对证据、活动任务影响数量、校验结果、激活/暂停/恢复/回滚请求及最终对账结论；成功、失败、超时和结果未知同等保留。记录至少在线保留 180 天，仍被配置版本、TransportDemand、审计或未关闭异常引用时不得删除。
16. **本票批准治理规则，不伪造实际站点值或实现设计。** `R01-A0747`、`R01-A0748` 只证明旧材料曾留下“现场建图后填写具体站点”的未批准待办；当前证据不包含 `RIOT-8005-RUNTIME` 各 Map 的具体公共站点身份，因此本票不声称任一 Map 已投运就绪。具体界面、API、事务、存储表、密码重验技术、部署和验收属于后续正式 spec、系统设计与实施，不进入本次需求基线决定。

上述已批准词汇与边界已同步到根 [`CONTEXT.md`](../../../CONTEXT.md)。本票没有新增可在当前 Wayfinder 目的地内独立解决的问题；具体实现设计继续遵守地图的 Out of scope。
