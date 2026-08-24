# 决定 MES 运输候选的业务纳入与排除边界

Type: grilling
Status: resolved
Blocked by: 63

## Question

在当前 8005 六类只读 MES 查询范围内，交接班部分完工、扣留出站部分完工、共晶/低温共晶、新厂前线订单、PACKAGE 未覆盖和设备资料缺失等情况，哪些应成为运输候选、哪些必须排除或阻断；每项规则在缺少权威 AREA/EQP/PACKAGE/状态字段证据时应保持未知、fail-closed 还是允许具名人工确认，且哪些只是查询实现证据而不能写成业务需求？

## Evidence rows

`R01-A0045`、`R01-A0047`、`R01-A0048`、`R01-A0051` 及其在票据 63 复核账中的关联证据。

## Answer

经用户作为当前基线最终批准人逐项确认，8005 的 MES 运输候选与后续执行资格采用以下边界：

1. **工厂 IT SQL 是候选集合边界。** MesIngest 执行工厂 IT 正式提供的全厂六类 MES SQL；SQL 返回集是权威候选集，未返回的记录直接忽略。MesIngest 不重建被内连接或其它 SQL 条件排除的任务，不为设备主资料缺失另建旁路查询或告警。对 SQL 的信任必须逐版本绑定提供方、接收日期与 SHA-256；任务类型、输出字段或筛选语义变化时重新审查，不能把当前信任延伸到未知版本。
2. **字段完整性采用单行隔离。** 当前七列为 `TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、PACKAGE`；只有 `AREA` 允许为空，其余六列必填。任一必填值缺失时形成 IngestAlert，只阻断该行的创建或刷新，其他正常行继续；同键已有 TransportDemand 保持冻结值且该轮不计作消失。缺少任一必需列，或整轮查询失败、不完整时，整轮不改变已有投影。
3. **SQL 已返回的 MES 状态不再由项目猜测。** 交接班部分完工、扣留出站部分完工等记录只要由受信任 SQL 返回且字段完整，就按普通 TransportDemand 处理；8005 不追加状态二次过滤。现有 SQL、历史 run、旧程序行为和当前代码只作实现/观察证据，除本票明确批准的边界外不能反推新的业务筛选。
4. **全厂 Demand 与老厂执行范围分层。** 工厂 SQL 读取全厂数据，所有合格返回行均生成并保留 TransportDemand；新厂不属于 8005 执行范围，但不在 MesIngest 删除。8005 在选任务阶段使用 `OldFactoryExecutionAreaRegistry` 正向判断唯一的 MES AREA 机台端点；明确不在名册内的全厂任务正常跳过、不报警，端点无法解析时才形成 TransportSelectionAlert 并阻断执行。
5. **每个 Demand 只有一个 MES AREA 端点。** `STAGING_TO_WIRE` 中 `EQP + AREA` 表示终点；其余五类任务中表示起点。另一端由 8005 按 TASK_TYPE 配置为 `FixedTaskStation`，使用项目站点身份而非 AREA 格式；不得要求两个端点都命中 AREA 名册，也不得根据 STEP 猜测方向。
6. **共晶与低温共晶在选任务阶段排除。** 项目维护 `TransportExecutionExcludedArea` 列表；MES AREA 机台端点命中时仍保留 TransportDemand，但不得派车或装货。该判断不在 MesIngest 执行。
7. **PACKAGE 缺值与容量未覆盖分层处理。** `PACKAGE` 空值属于字段完整性失败，由 MesIngest 单行报警并隔离；PACKAGE 有值但没有匹配到已批准容量规则时，TransportDemand 继续保留，由 8005 任务/装货准备模块形成 LoadPreparationAlert，在仓位分配和开锁前阻断。该模块逐 DemandId 保存 `PACKAGE、TASK_TYPE、SUBLOT、AREA、EQP、STEP、DATES、首次发现、最后发现、当前是否仍未覆盖`，并按 PACKAGE 汇总当前/累计受影响需求数、首次/最后发现时间及 TASK_TYPE 分布；相同需求按轮次更新而不重复插入，规则补齐后关闭告警但永久保留历史。
8. **AREA→EQP 唯一性是选任务门禁。** 当前客户数据允许一个 AREA 对应多台机，客户后续将调整为 AREA 与机台一一对应。8005 需要独立的 `AreaEqpUniquenessMonitor`，针对老厂 AREA 名册直接查询设备主数据，不按工序过滤；每个 AREA 必须恰好返回一个 EQP。结果为零、多台、查询失败或超过新鲜度期限时，保留 TransportDemand，产生选任务告警并暂停新的相关选任务，已在执行中的任务不受影响；服务启动、名册变更时立即检查，并按可配置周期重复检查。EQP→AREA 的反向唯一性由客户 MES 自身卡控，8005 不重复验证。
9. **旧 SQL 只提供查询原型。** [`GetEqpnoByArea.sql`](../../../mes/sources/legacy-program-sql/2026-07-16/通用查询/GetEqpnoByArea/GetEqpnoByArea.sql) 的 SHA-256 为 `4eaee07989a0e2e9d3b7c296c8148c16a807cd52eae2dc100a0784c5787f78b0`，证明可从 `fw_eqpres_eqpinformation` 按 AREA 查询 EQP；其中 `step = '装片'` 不属于新监控器的唯一性条件，旧程序 `ExecuteScalar` 只取首行的行为也不得复用，因为它会掩盖多 EQP 冲突。

上述决定已同步为根 [`CONTEXT.md`](../../../CONTEXT.md) 中的统一领域词汇。`AreaEqpUniquenessMonitor`、未覆盖 PACKAGE 明细/汇总以及现有 MesIngest 单行隔离行为的代码实现均属于后续正式 spec 与开发阶段，不在本地图内实施。

## Supersession note

本票关于独立老厂 AREA 正向名册、共晶/低温共晶排除名单及唯一性监控输入范围的决定，后续由[决定复合运输、分区与多 SUBLOT 组合边界](65-decide-composite-transport-zoning-and-multi-sublot-boundary.md)统一收敛为 DispatchZoneAreaAssignment；其余全厂候选投影、字段完整性、PACKAGE 和 MES 状态边界保持有效。
