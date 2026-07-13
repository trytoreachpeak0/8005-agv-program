---
id: UC-001
type: use-case
title: "Load Completed Sublot into Slot 放入子批次完工产品到仓位"
status: draft
priority: high
created_by: "ZhengyuShao 邵正宇"
updated_by: "ZhengyuShao 邵正宇"
created: 2026-07-08
updated: 2026-07-09
primary_actor: "Production Operator 生产操作员（按场景引用 R-01~R-08，见 [[stakeholders-and-user-classes|干系人与用户角色清单]]）"
secondary_actor: MES
frequency: "Depending on the production speed of the products in the factory and the number of multi-slot AGVs, generally there will be multiple instances within an hour. 根据工厂里产品生产速度和多仓位AGV的数量决定，一般来说一个小时内会有多次"
related_uc: ["UC-002", "UC-003", "UC-004", "UC-005", "UC-006", "UC-007", "UC-010", "UC-011", "UC-014"]
related_br: ["BR-001"]
aliases: ["UC-001"]
---

# UC-001 Load Completed Lot into Slot 放入完工批次产品到仓位

## Description 描述

The production operator scans the sublot barcode on the work order or manually enters the sublot. The multi-slot AGV opens the available slot(s) required to store this batch of completed products (one or more). After placing the products into the slot(s), the production operator manually closes the slot door(s). 生产操作员扫描工单上的子批号条形码或者手动输入子批号，多仓位AGV打开存放这批完工产品所需空闲仓位（一个或多个），生产操作员存放产品后手动关闭仓位仓门。

## Trigger 触发条件

The multi-slot AGV arrives at the designated station, and the production operator needs to transport the completed sublot products to the specified destination. 多仓位AGV到达指定站点，且生产操作员需要运送子批次完工产品到指定位置

## Precondition 前置条件

**System & Interface 系统与接口**

1. MES is online. MES 在线
2. The multi-slot AGV has available slot(s). 多仓位 AGV 存在空闲仓位

**Equipment & Hardware 设备与硬件**

3. The IO module is communicating normally. IO 模块通信正常
4. All slot doors are in the closed state. 所有仓位仓门均处于关闭状态

**Task & Data 任务与数据**

5. At least one transport task exists for this station and has been synced from MES into the local database — this is the reason the multi-slot AGV arrived here. The specific sublot is not yet known at this point; it will be identified after the operator scans or enters it. 该站点存在至少一个已从 MES 同步到本地数据库的搬运任务（多仓位 AGV 正是因为该任务才到达此站点），此时尚不确定具体是哪个子批号，需等操作员扫码/输入后才能确定

**Personnel & Authorization 人员与权限**

6. The production operator has permission to scan and load. 生产操作员具备扫码/装料操作权限

> 目标仓位的电子锁是否关闭、光幕是否无遮挡，需要在确定目标仓位后才能判断（到站时尚不知道具体仓位），因此不作为本 UC 的 Precondition，而是在 Normal Flow 中"打开仓位"步骤里作为系统开锁前的检查项。

> 核验子批号时，以"该子批号对应的搬运任务是否属于本次 AGV 派车所关联的任务范围"为准，而不是要求"任务的目标站点严格等于操作员当前所在的物理站点"：由于相邻站点物理距离很近，一次派车可能同时涵盖多个相邻站点各自的搬运需求（例如同一次派车里同时包含 A、B 两个相邻站点的任务），操作员可以在车辆停靠 A 点时，提前装载本次派车任务范围内、属于相邻 B 点的产品，不需要等车辆真正到达 B 点。但如果子批号对应的任务完全不属于本次派车的任务范围（例如距离较远、未被分配进本次派车的 C 点任务），即使该任务在系统中确实存在，也判定核验不通过，不允许装料（见 Normal Flow 第 1.2 条、Exception Flow E1.2）。评判标准不是站点之间的物理距离远近，而是该任务是否已被分配进本次派车的任务范围内；"本次派车任务范围"具体如何生成与维护，见 [[br-001-dispatch-task-range|BR-001]]。

> 子批号当前的 MES 工序、任务类型是否与搬运类型（moveType）匹配（对应 [[terminology-glossary|术语表]] 第 8 节的 `NG_STEP_ERROR`/`NG_TASK_ERROR`/`NG_LOT_CLOSED` 等核验错误码），由服务器在从 MES 同步、生成本地任务记录时校验：只有工序、任务类型等信息已经满足对应搬运类型要求的子批号，才会被同步为本地任务，并在生成时就带上对应的搬运类型（moveType）标记。因此，只要任务已经出现在本地数据库中，其工序/任务类型必然已经满足要求，本 UC 扫码环节（见 1.1、1.2）不需要重复核验 MES 工序/任务类型，只需核验该任务记录是否仍然有效（见 1.1）以及是否属于本次派车范围（见 1.2）。

> "MES 在线"为何仍是本 UC 的 Precondition：本地数据库需要持续从 MES 读取最新数据以保持同步更新（如任务、子批号状态等），若 MES 掉线，本地数据库中的任务数据会逐渐变旧、无法反映 MES 侧最新状态，操作员基本无法继续可靠地执行装载任务。这与 [[uc-002-confirm-task-completion|UC-002]] 不同："确认完成"只操作本地数据库、不依赖 MES 实时在线，两者对 MES 在线的依赖程度不一样。

## Postcondition 后置条件

**Equipment & Hardware 设备与硬件**

1. The electronic lock of the target slot returns to the locked state after the door is closed. 目标仓位电子锁在仓门关闭后恢复锁闭状态
2. The light curtain confirms that the door is closed and the slot is occupied, consistent with the system record. 光幕检测确认仓门已关闭且仓位内确有产品，占用状态与系统记录一致

**Task & Data 任务与数据**

3. The target slot status changes from "Idle" to "Occupied", and the slot–sublot mapping is recorded. 目标仓位状态由“空闲”变为“已占用”，并记录该仓位与子批号的对应关系
4. The load operation (operator, sublot, slot number, timestamp) is logged in the local database for traceability. 本次装载操作（操作员、子批号、仓位号、时间戳）被记录到本地数据库，用于后续追溯
5. After the slot door is closed, the task status remains in progress and is not automatically marked as completed. Final completion of the task is triggered separately by [[uc-002-confirm-task-completion|UC-002]]; if the operator needs to retrieve a mis-stored product before confirming, that is handled by [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]. 仓门关闭后，任务状态保持进行中，不会自动标记为完成；任务的最终完成由 [[uc-002-confirm-task-completion|UC-002]] 单独触发，若操作员在确认完成前需要取出存错的产品，则由 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 处理

## Assumption 假设

1. The production operator will only place the corresponding completed product(s) into the slot after scanning the barcode or manually entering the sublot; non-product items will not be placed into the slot. 生产操作员扫码（或手动输入子批号）后，仅会将对应的完工产品存放到仓位中，不会放入非产品类的其他东西。

## Normal Flow 正常流程

### 1.0 Load Completed Lot into Slot by SubSlot Barcode 
1. 生产操作员扫描工单上的子批号完工产品条形码
   1.1 系统核验该子批号是否存在对应的、尚未完成也未被取消的任务记录：若在本地数据库（含服务器同步的 MES 数据）中查不到该子批号、识别到手动输入格式错误，或该子批号对应的任务已经是"已完成（Done）"或"已取消（Cancelled）"状态，均判定核验不通过（见 Exception Flow E1.1）
   1.2 系统核验该任务是否属于本次 AGV 派车所关联的任务范围：不要求任务的目标站点严格等于操作员当前所在的物理站点（同一次派车可能涵盖多个相邻站点的任务），但若该任务完全不属于本次派车范围（如实际是距离较远、未被分配进本次派车的其他站点任务），也判定核验不通过（见 Exception Flow E1.2）
   1.3 系统核验是否存在满足数量要求的空闲仓位：已通过 [[uc-014-enable-disable-slot|UC-014]] 禁用的仓位不计入可分配的空闲仓位范围（见 Exception Flow E1.3）
2. 多仓位AGV打开其空闲仓位
   2.1 系统核验仓门是否已正常打开（见 Exception Flow E2.1）
   2.2 系统/生产操作员核验该仓位是否确实为空，与系统记录的"空闲"状态一致（见 Exception Flow E2.2）
3. 生产操作员放入子批号完工产品
   3.1 系统监控该仓位开启时长，若长时间未关闭仓门则触发超时提示/告警（见 Exception Flow E3.1）
4. 生产操作员关闭仓位
   4.1 系统通过光幕检测确认该仓位内确实存放了产品，若光幕未检测到产品，则转异常处理（见 Exception Flow E4.1）
   4.2 若生产操作员关门后发现产品放错或数量不符，需重新打开该仓位处理（见 Exception Flow E4.2，转 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]）



## Alternative Flow 备选流程

### 1.1 Load Completed Lot into Slot by keyboard input
1. 生产操作员手动输入子批号
   1.1 系统核验该子批号是否存在对应的、尚未完成也未被取消的任务记录：若在本地数据库（含服务器同步的 MES 数据）中查不到该子批号、识别到手动输入格式错误，或该子批号对应的任务已经是"已完成（Done）"或"已取消（Cancelled）"状态，均判定核验不通过（见 Exception Flow E1.1）
   1.2 系统核验该任务是否属于本次 AGV 派车所关联的任务范围：不要求任务的目标站点严格等于操作员当前所在的物理站点（同一次派车可能涵盖多个相邻站点的任务），但若该任务完全不属于本次派车范围（如实际是距离较远、未被分配进本次派车的其他站点任务），也判定核验不通过（见 Exception Flow E1.2）
   1.3 系统核验是否存在满足数量要求的空闲仓位：已通过 [[uc-014-enable-disable-slot|UC-014]] 禁用的仓位不计入可分配的空闲仓位范围（见 Exception Flow E1.3）
2. 多仓位AGV打开其空闲仓位
   2.1 系统核验仓门是否已正常打开（见 Exception Flow E2.1）
   2.2 系统/生产操作员核验该仓位是否确实为空，与系统记录的"空闲"状态一致（见 Exception Flow E2.2）
3. 生产操作员放入子批号完工产品
   3.1 系统监控该仓位开启时长，若长时间未关闭仓门则触发超时提示/告警（见 Exception Flow E3.1）
4. 生产操作员关闭仓位
   4.1 系统通过光幕检测确认该仓位内确实存放了产品，若光幕未检测到产品，则转异常处理（见 Exception Flow E4.1）
   4.2 若生产操作员关门后发现产品放错或数量不符，需重新打开该仓位处理（见 Exception Flow E4.2，转 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]）

> 与 `1.0` 正常流程相比，本备选流程仅第 1 步的输入方式不同（手动输入子批号，而非扫描条形码），其余步骤及系统检查点完全一致。

## Exception Flow 异常流程

以下每条异常均以 `E<步骤号>` 编号，与 Normal Flow / Alternative Flow 中触发该异常的具体步骤一一对应（例如 `E1.3` 对应第 1.3 步"核验空闲仓位数量"失败的情形）：

* E1.1 子批号无有效任务（查不到 / 格式错误 / 任务已完成或已取消）
* E1.2 搬运任务不属于本次派车范围
* E1.3 仓位实际上不够
* E2.1 仓门开锁失败（电子锁/机械故障）
* E2.2 打开仓门后实际里面有东西
* E3.1 生产操作员长时间不关门
* E4.1 关门后光幕检测仓位内无产品
* E4.2 关门后发现产品放错或数量不符

### E1.1 子批号无有效任务
1. 生产操作员扫描工单条形码或手动输入子批号
2. 系统按第 1.1 步核验，出现以下任一情况：
   2.1 在本地数据库（含服务器同步的 MES 数据）中未找到该子批号，或识别到手动输入的子批号格式错误
   2.2 找到该子批号，但其对应的任务已经是"已完成（Done）"或"已取消（Cancelled）"状态
3. 系统提示"子批号不存在、格式错误，或对应任务已完成/已取消"，拒绝继续装载流程
4. 生产操作员重新核对并扫描条形码，或重新手动输入；若确认条形码模糊/损坏导致无法扫描识别，改走 Alternative Flow（手动输入子批号）重试；若任务确实已完成/已取消，联系班组长确认是否需要在 MES 侧另行处理

### E1.2 搬运任务不属于本次派车范围
1. 生产操作员扫描工单条形码或手动输入子批号
2. 系统按第 1.2 步核验，发现该子批号确实存在对应的、尚未完成也未被取消的搬运任务，但该任务不属于本次 AGV 派车所关联的任务范围（例如该任务对应的是距离较远、未被分配进本次派车的其他站点）
3. 系统提示核验不通过，拒绝为该子批号分配仓位
4. 生产操作员核对子批号或站点，确认是否扫错产品；若确认该产品确实需要在本站点处理，联系班组长确认任务分配是否需要调整

### E1.3 仓位实际上不够
1. 系统按第 1.3 步核验该子批号所需仓位数量，发现当前空闲仓位数量（已排除被 [[uc-014-enable-disable-slot|UC-014]] 禁用的仓位）不满足该子批号的装载需求
2. 系统提示生产操作员"空闲仓位不足"，不为该子批号分配仓位，不允许继续装载流程
3. 生产操作员可等待其他仓位释放（如其他任务确认完成或取出产品）后重新扫描子批号重试，或联系班组长协调处理；若怀疑是仓位被误禁用导致空闲仓位不足，需联系具备禁用/启用仓位权限的人员（见 [[uc-014-enable-disable-slot|UC-014]]）核实是否需要重新启用

### E2.1 仓门开锁失败
1. 系统在 Normal Flow 第 2 步下发目标仓位开锁指令
2. 系统按第 2.1 步核验仓门状态，发现该仓位仓门未能在规定时间内正常打开
3. 系统提示该仓位开锁异常，将该仓位标记为"异常锁定"，暂停对该仓位的后续操作
4. 若存在其他空闲仓位，系统为该子批号重新分配空闲仓位，提示生产操作员改用新仓位继续装载；若无其他空闲仓位，提示生产操作员联系设备/电气维护人员（R-11）处理
5. 设备/电气维护人员排查并修复电子锁/机械故障后，解除该仓位的"异常锁定"状态，恢复其为可用仓位

### E2.2 打开仓门后实际里面有东西
1. 系统打开系统记录中为"空闲"状态的目标仓位
2. 生产操作员按第 2.2 步核验，发现该仓位内实际已存放有物品，与系统记录的"空闲"状态不一致
3. 生产操作员暂停向该仓位装载，并上报该仓位状态异常
4. 系统将该仓位标记为"异常锁定"，暂停分配该仓位，等待核实该仓位实际占用情况与系统记录不一致的原因（如历史装载记录未正确关闭、人工误放等）
5. 核实并处理完毕（清空仓位或更正系统记录）后，方可解除"异常锁定"，恢复该仓位的正常使用

### E3.1 生产操作员长时间不关门
1. 生产操作员打开仓位、放入产品后，长时间未关闭仓门
2. 系统按第 3.1 步监控，检测到该仓位开启时长超过预设阈值
3. 系统触发超时提示/告警（如现场提示音、界面告警、上报班组长），提醒生产操作员尽快完成装载并关闭仓门
4. TBD 待定：若长时间仍无响应，是否需要进一步升级告警、标记该仓位/任务异常或触发其他处理机制，待补充

### E4.1 关门后光幕检测仓位内无产品
1. 生产操作员关闭仓位仓门
2. 系统按第 4.1 步通过光幕检测该仓位，发现该仓位内实际没有检测到产品
3. 系统提示该仓位装载异常，要求生产操作员重新打开该仓位确认
4. 生产操作员重新打开该仓位，确认并补放产品后再次关闭仓门
5. 系统重新执行"关门→光幕核验"检查（即重新执行第 4.1 步），直至光幕确认仓位内确有产品

> 本条异常本身不视为存错/取错，不属于 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 范围，因为对应任务尚未被判定为"已装载"。

### E4.2 关门后发现产品放错或数量不符
1. 生产操作员关闭仓位仓门并完成光幕核验（第 4.1 步）后，按第 4.2 步发现存入的产品实际放错或数量不符
2. 生产操作员判断需要取出已存入的产品进行更正
3. 转 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]] 处理：取出产品后，如仍需装载，重新回到本 UC 的 Normal Flow 或 Alternative Flow 装载

> 不在本 UC 范围内处理，具体取出流程见 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]。

---

## Notes 备注

* `1.0` represents the **Normal Flow**. `1.0` 表示**正常流程**。
* `1.1` represents an **Alternative Flow** branching from the normal flow. `1.1` 表示从正常流程分支出的**备选流程**。
* Each Exception Flow is labeled `E<step number>`, corresponding one-to-one with the specific Normal/Alternative Flow step (or sub-step) whose failure triggers it (e.g. `E1.2` corresponds to the failure of step 1.2). 每条 Exception Flow 均以 `E<步骤号>` 编号，与触发该异常的具体 Normal/Alternative Flow 步骤（或子步骤）一一对应（如 `E1.2` 对应第 1.2 步核验失败的情形）。
* 「任务确认完成」与「取出存错产品」已从本 UC 的 Postcondition 中拆出，分别独立为 [[uc-002-confirm-task-completion|UC-002]] 和 [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]：这两者都是由操作员另外主动发起、有各自独立触发条件和流程的场景，而"到站期间继续扫描其他子批号装载其他仓位"则视为本 UC 在同一次到站期间的重复执行，不单独建 UC。

## Related Use Cases 关联用例

* [[uc-002-confirm-task-completion|UC-002]]：本 UC 完成一次装载（关闭仓门）后，任务并不会自动完成，需操作员另外执行该 UC 手动确认完成。
* [[uc-003-agv-arrives-at-designated-station|UC-003]]：本 UC 的 Trigger 依赖 AGV 到达并停稳，具体到站过程见该 UC。
* [[br-001-dispatch-task-range|BR-001]]：本 UC 中"子批号核验需限定在本次派车所关联的任务范围内"（见 Precondition 备注、Normal Flow 第 1.2 条）所依赖的"本次派车任务范围"如何生成与判定（如一次派车是否可涵盖多个相邻站点），由该业务规则定义。
* [[uc-004-slot-door-safety-interlock|UC-004]]：本 UC 装卸过程中"AGV 是否移动"的安全联锁检查，由该 UC 统一处理，不在本 UC 的 Precondition 中重复定义。
* [[uc-005-retrieve-mis-stored-product-from-slot|UC-005]]：若操作员在确认任务完成前发现存错产品需要取出，由该 UC 处理，不在本 UC 范围内。
* [[uc-006-cancel-transport-task-upon-arrival|UC-006]]：若操作员在开始本 UC 的装载流程之前，发现促使 AGV 到达本站点的任务已经不需要运送，应转该 UC 取消任务，不需要走完本 UC 的装载流程。
* [[uc-007-sync-transport-task-from-mes|UC-007]]：本 UC Precondition 第 5 条依赖的"已从 MES 同步到本地数据库的搬运任务"（及其 moveType 标记），正是由该 UC 生成；本 UC 扫码核验环节不重复核验 MES 工序/任务类型，正是因为已由 UC-007 在生成时完成校验。
* [[uc-010-unload-completed-lot-at-destination-station|UC-010]]：本 UC 与该 UC 是方向相反的一对——本 UC 是起点站"扫码装入仓位"，UC-010 是终点站"系统自动开仓、取出存料"，两者共享同一批次产品、同一次 AGV 行程的前后两端；若同一次到站既要装载新任务又要取出已到货的任务，操作员可分别执行本 UC 与 UC-010，最后统一通过 [[uc-002-confirm-task-completion|UC-002]] 确认完成。
* [[uc-011-view-slot-monitoring-dashboard|UC-011]]：本 UC 装载完成后记录的仓位-子批号映射关系、以及 Exception Flow（E2.1/E2.2）产生的"异常锁定"状态，均会实时体现在该 UC 提供的仓位监控看板中，供班组长/生产管理者查看；该 UC 为纯只读展示，不影响本 UC 的流程本身。
* [[uc-014-enable-disable-slot|UC-014]]：本 UC 第 1.3 步核验"是否存在满足数量要求的空闲仓位"时，需排除已被该 UC 禁用的仓位，不将其计入可分配范围；若因仓位被禁用导致空闲仓位不足，转 Exception Flow E1.3 处理。

## Other Information 其他信息

