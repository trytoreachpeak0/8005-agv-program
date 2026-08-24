# 补齐并验证 QUEUEING 长期滞留原因诊断 API

Type: task
Status: resolved
Blocked by: 58

## Question

取得用户提供的长期 QUEUEING 原因诊断 API 及其目标环境、build、鉴权和 schema 证据，在受控只读条件下验证请求标识、响应字段与枚举、原因覆盖、状态新鲜度、错误与结果未知行为，并至少覆盖车辆距可执行路线过远、车辆状态不可执行、车辆未启用、可恢复软件急停和其它/未知原因；据实形成原因到“等待自然恢复、获批自动恢复、阻断转人工”的诊断映射。测试结果只补充证据，不自动扩大 RIoT 控制白名单或降低安全门槛。

## Comments

- 2026-08-04：用户提供接口 `GET /api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey}`，并指定后续在 riot-behavior-lab 对应 RIoT 版本验证。
- 2026-08-04：本地核对确认接口在 8005 的 `rcs/riot_swagger/task.json`（SHA-256 `050A612E21EBE01B95D6FA35CA54D592BD83E108B69F5EB0703D8B903274D6D1`）及 lab Round 7 从测试环境捕获的 `swagger-task.json`（SHA-256 `53CDA75CDEF0DF07C8FCBD476ACB540C90B2A2A02DF9839680CB49D9360F56BD`）中均存在；用户此前已把 lab 环境绑定为 RIoT build `2.2.0.30`。
- 2026-08-04：静态契约摘要为“订单模拟分配”，使用 Authorization header，两个必填 path 参数均为 string；成功响应为 `ResponseMsg<VehicleNotAssignReason>`，其中 `result.reason` 是自由文本 string、`result.suggestList` 是 string 数组，没有受控原因枚举。现有生成 SDK 已能发出该 GET 并反序列化两字段。
- 2026-08-04：现有 lab 证据只证明 `2.2.0.30` 环境暴露了该契约；未找到对该 endpoint 的实际调用结果或不同阻断原因样例。后续测试必须验证 `orderKey` 的实际标识口径、自由文本稳定性、建议是否可机器执行、无原因/错误/超时行为及该 GET 是否确实无副作用。
- 2026-08-04：用户确认这是 RIoT 原生诊断，并批准 `reason/suggestList` 只作诊断证据；不得直接把 `suggestList` 当动作授权，自动恢复仍须经过版本绑定的批准映射及独立状态、安全核验。
- 2026-08-04：本票已认领并完成 Round 39 离线准备，新增 Q-040、只读实验卡 E5、轮次计划与 GET-only 脚本；PowerShell 语法及只读范围静态检查通过。用户说明当前尚未连接实验环境，因此未发出任何 HTTP 请求、未产生现场状态变化，票据保持 claimed，等待用户连接后继续。
- 2026-08-04：用户连接实验环境后完成 Round 39 只读执行。测试车前后均为 IDLE/ON_LINE 且无 QUEUEING；8 个历史场景的三类订单身份共 24 次均返回 `code=0` 但诊断为“订单不存在”，未知车辆为“车辆不存在”，无/假鉴权为 HTTP/业务 401。返回无原因码、枚举、状态版本或时间字段，历史记录不能还原原 QUEUEING 原因。已形成缺失订单、缺失车辆、鉴权失败和其它未知文本的 fail-closed 人工映射，但五类实时原因仍未覆盖；本票保持 claimed，等待人工逐场景制造实时 QUEUEING 或另行批准受控写实验。
- 2026-08-04：用户确认唯一测试车为“新基测试300c协作1”并批准受控建单、取消、调度上下线、软件急停与解除。Round 40 已实测调度下线原因及软件急停下的宽泛不可分配原因，确认字符串 `orderId` 才是项目 `orderKey`；发现车辆原因会短路订单校验、取消后在短路未解除时文本不变，且 `suggestList` 可能建议越权的系统级 RIoT 重启。两个场景均安全善后，最终测试车 IDLE/ON_LINE/OK、无非终态订单。票据仍保持 claimed，仅待人工制造离路线过远及可选硬件/其它不可执行场景。
- 2026-08-04：用户人工把测试车移离路线并保持静止；Round 41 在 location RUNNING、六站均 `-1/unreachable` 的独立证据下捕获稳定原因“以车当前的坐标为起点,以订单目的地为终点,无法规划路径”。订单已取消，车辆仍静止、IDLE/ON_LINE/OK 且无非终态订单。该原因映射为保持阻断并人工恢复到路网，绝不按建议自动取消、重建或移动。票据继续 claimed，等待用户把车恢复到路线并完成只读收尾。
- 2026-08-04：用户首次回复已恢复路线后，只读门禁发现车辆仍为 `UNMOVABLE / CONTROL_STATE_ERR`；收尾脚本在路线探针前停止，未执行任何写入。等待用户恢复解抱闸/控制开关后再次只读复核。
- 2026-08-04：用户复位 MOVABLE 后，第二次只读收尾确认车辆 CONTROL_STATE_OK/IDLE/ON_LINE/OK、速度 0、无非终态订单，map 30 六站全部恢复 `costs>0 / ok`。Round 41 完整恢复闭环通过。

## Answer

用户于 2026-08-04 批准并共同完成 Round 39～41 后，形成以下版本绑定结论：

1. **环境、鉴权与静态契约。** 本结论绑定测试环境 `RIOT-CROSS-PROJECT-TEST`、RIoT build `2.2.0.30` 和唯一测试车“新基测试300c协作1”。接口为 `GET /api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey}`，使用 `Authorization: Bearer <CallApiKey>`；无鉴权和假鉴权均为 HTTP 401、业务 `code=401`。静态 schema 与实测都只有自由文本 `reason` 和字符串数组 `suggestList`，没有原因码、受控枚举、观测时间或状态版本。
2. **项目请求身份固定为字符串 `orderId`。** 车辆恢复可分配后，已取消订单的字符串 `orderId` 仍被识别并返回“订单是非可调度状态”；数值记录 id、`upperId` 和随机 key 均返回“订单不存在”。8005 不得用数值 id 或 `upperId` 调用该接口。
3. **诊断有优先级短路，`code=0` 不是可执行授权。** 车辆 OFF_LINE 时，真实三种身份、随机 key 以及已取消订单都会先返回“车辆处于调度下线状态”；因此单次原因不证明所有输入层级均有效，也不一定随订单事件立即变化。`code=0` 只表示接口成功返回一条诊断，车辆不存在、订单不存在同样可以是 `code=0`。
4. **文本稳定性只在已测窗口内成立。** 调度下线、软件急停下宽泛不可分配、离路线过远和订单不存在分支各自重复三次时文本一致；接口没有版本或时间字段，调用方仍必须保存原始响应并同步读取独立订单与车态，不能把自由文本当永久枚举。
5. **原因映射如下，`suggestList` 永远不是动作授权：**
   - “车辆处于调度下线状态”：独立核验 `integrationLevel=OFF_LINE`。只有禁用由8005自身造成、原因已消除且安全可证明时，才按既有批准恢复 ON_LINE；人工、外部或来源未知时阻断转人工。
   - “车辆处于非空闲的状态,不可分配订单”：Round 40 的实际独立状态为 `procState=IDLE + emergencyState=CAN_RECOVER`，证明该文本是宽泛不可分配类，不能直接识别或解除急停。只有独立证明为8005自身软件急停且满足既有安全门槛时才可解除；否则阻断转人工。
   - “以车当前的坐标为起点,以订单目的地为终点,无法规划路径”：独立核验订单仍 QUEUEING、身份和目标匹配，且 `getRouteCostsBy=-1/unreachable`。保持阻断并由人工把车辆恢复到可达路网；不得自动移动、Cancel、重建、换号或 PriorityExec。
   - “订单是非可调度状态”：保持阻断并对账订单终态；即使建议重启 RIoT，也不得执行系统级重启或自动重建。
   - “订单不存在”“车辆不存在”、HTTP/业务 401 及任何其它未知/变化文本：保持相应订单级或车辆级阻断，保留原文并转人工。
6. **安全与副作用边界。** Round 39 的 GET-only 前后快照未观测到业务状态变化，但这不证明服务端内部绝对无副作用。Round 40/41 只在用户明确授权的唯一测试车上制造状态，所有测试订单均取消；调度和软件急停状态均恢复。最终只读复核确认车辆 `MOVABLE / CONTROL_STATE_OK / IDLE / ON_LINE / OK / LOCATION_STATE_RUNNING / MT_FINISHED`、速度 0、无非终态订单，map 30 六站全部恢复可达。

证据保存在 [`Round 39`](../../../rcs/riot-behavior-lab/evidence/rounds/2026-08-04-round-39/)、[`Round 40`](../../../rcs/riot-behavior-lab/evidence/rounds/2026-08-04-round-40/) 和 [`Round 41`](../../../rcs/riot-behavior-lab/evidence/rounds/2026-08-04-round-41/)；已验证行为契约为 [`BC-ORDER-019`](../../../rcs/riot-behavior-lab/knowledge/behavioral-contracts.md#bc-order-019-queueing-原因诊断的身份短路与安全边界round3940)。本结论不扩大 RIoT 控制白名单，也不降低既有状态、安全、来源证明和结果回查门槛。
