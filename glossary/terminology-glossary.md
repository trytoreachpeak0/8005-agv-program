# Terminology Glossary / 项目术语表

> **Scope 适用范围：** 本项目（8005 多仓位 AGV）全部文档、Use Case、接口设计与程序代码。
> **Purpose 目的：** 统一中英文术语，避免同一概念在不同文档或代码里出现多种叫法。
> **Maintenance 维护：** 新增术语时先查本表；若表中无对应项，先补充本表再写入其他文档或代码。

---

## How to Use 使用说明

| 场景 | 规则 |
| --- | --- |
| 中文需求/说明文档 | 使用「中文」列的标准译名 |
| 英文 Use Case / 对外接口文档 | 使用「English」列的标准译名 |
| 程序代码（变量、类、枚举、API 字段） | 优先使用「Code Identifier」列；若无则按 English 转 `camelCase` / `PascalCase` / `SCREAMING_SNAKE_CASE` |
| MES / RIOT 等外部系统已有字段 | 以外部系统字段名为准，在本表「Notes」中注明来源，不强行改名 |

**优先级：** 本表 > 各文档自行翻译 > 口头习惯叫法。

---

## 1. System & Architecture 系统与架构

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 多仓位 AGV | multi-slot AGV | `multiSlotAgv` | 项目核心设备；8 个仓位。英文统一写作 **multi-slot AGV**，与「slot（仓位）」术语一致 |
| 工控机 | industrial PC | `industrialPc` | 触控屏 Win10 工控机，负责现场操作与 IO 控制；原称「上位机」，不再使用 |
| 服务器 | server | `server` | 负责任务管理、MES 对接、RIOT 调度 |
| RIOT | RIOT | `riot` | 斯坦德 AGV 调度平台；通过 HTTP 接口调用 |
| RCS | RCS (Robot Control System) | `rcs` | 机器人调度/控制系统统称；本项目具体实例为 RIOT |
| MES | MES (Manufacturing Execution System) | `mes` | 制造执行系统；任务来源与状态核验、回写 |
| IO 模块 | IO module | `ioModule` | 康耐德 IO 模块，控制仓位电子锁与读取光幕 |
| 站点 | station | `station` | AGV 地图上的停靠/作业点位 |
| 站点映射 | station mapping | `stationMapping` | MES 机台/区域与 AGV 地图站点的对应关系 |

---

## 2. Equipment & Hardware 设备与硬件

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 仓位 | slot | `slot` | AGV 上单个载货格口；不再使用 bay |
| 仓位门 / 仓门 | slot door | `slotDoor` | 仓位物理柜门 |
| 电子锁 | lock | `lock` | 每个仓位配备；有开关反馈 |
| 光幕 | light curtain | `lightCurtain` | 检测仓位是否有遮挡 |
| DI 信号 | digital input (DI) | `di` | 数字输入，如锁状态、光幕状态 |
| DO 信号 | digital output (DO) | `do` | 数字输出，如开锁指令 |
| 充电桩 | charging station | `chargingStation` | AGV 自动充电设施 |
| 弹匣盒 | magazine box | `magazineBox` | 芯片载具；原称「弹匣」「弹夹」，统一使用「弹匣盒」，不再单独使用 magazine |
| 金属篮 / 篮筐 | metal basket | `metalBasket` | 多个弹匣盒的集合搬运单位；一车最多 8 篮，一篮最多放 4 个弹匣盒 |

---

## 3. Business & MES 业务与 MES

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 子批号 | sublot | `sublot` | MES 唯一编号；扫码/手输均以此为准。**不要**在代码中混用 `lotNo`、`batchNo` |
| 工单 | work order | `workOrder` | 现场扫码载体；条码内容对应 sublot |
| 产品批次 | product lot | `productLot` | MES 字段；任务去重键之一 |
| 机台号 | machine number | `machineNo` | MES 字段 `machine_no`；任务去重键之一 |
| 完工时间 | finish time | `finishTime` | MES 字段 `finish_time`；任务去重键之一 |
| 工序 | step | `step` | MES 工序，如「装片烘烤」「焊线」「键合」 |
| 任务类型（MES） | task | `task` | MES 字段，如 `入站`、`入库` |
| 区域 | area | `area` | MES 机台区域；用于映射 AGV 站点 |
| 搬运类型 | move type | `moveType` | 系统内部枚举，用于装料核验 |
| 装料核验 | load verification | `loadVerification` | 装车前按 sublot + moveType 校验 MES 状态 |
| 回写 | write-back / post-back | `writeBack` | 搬运完成后更新 MES 或提示人工操作 |

### Move Type 枚举（搬运类型）

| 中文场景 | English | Code Identifier | MES / 业务对应 |
| --- | --- | --- | --- |
| 装片完工送烘烤 | die attach finish to bake | `BAKE` | `moveType='BAKE'` |
| 装片完工送焊线氮气柜 | die attach finish to wire bonding N₂ cabinet | `WIRE_BOX` | `moveType='WIRE_BOX'` |

> 其他场景的 `moveType` 值待 IT 确认后补充。

---

## 4. Task & State 任务与状态

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 搬运任务 | transport task / handling task | `transportTask` | 从 MES 生成本地任务后下发 RIOT |
| 移动任务 | move order / move task | `moveOrder` | 下发给 RIOT 的 AGV 移动指令 |
| 任务状态：新建 | New | `NEW` | 已创建，待派车 |
| 任务状态：执行中 | Executing | `EXECUTING` | 已派车，执行中 |
| 任务状态：完成 | Done | `DONE` | 搬运完成 |
| 任务状态：缺失 | Missing | `MISSING` | AGV 到达后未找到应搬物料 |
| 任务状态：异常 | Exception | `EXCEPTION` | MES/RIOT/IO/核验异常 |
| 任务状态：已取消 | Cancelled | `CANCELLED` | 人工取消 |
| 去重 | deduplication | `deduplication` | 按 `productLot + machineNo + finishTime` 或 MES 事务 ID |
| 轮询 | polling | `polling` | 服务器定时查询 MES 待搬运数据 |

---

## 5. Process Areas & Scenarios 工序区域与搬运场景

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 装片 | die attach | `dieAttach` | 装片设备/区域 |
| 烘烤 / 烘箱 | bake / oven | `bake` | 烘烤间 |
| 焊线 | wire bonding | `wireBonding` | 焊线工序/机台 |
| 键合 | bonding | `bonding` | 键合工序/机台（与焊线并列出现） |
| 氮气柜 | N₂ cabinet / nitrogen cabinet | `nitrogenCabinet` | 焊线区/关卡氮气柜 |
| 关卡 | checkpoint | `checkpoint` | 关卡氮气柜 |
| AOI | AOI (Automated Optical Inspection) | `aoi` | 自动光学检测 |
| 清洗间 | cleaning area | `cleaningArea` | 清洗完工物料架所在区域 |
| 装片完工送烘烤 | die attach finish to bake | `scenarioDieAttachToBake` | 场景 5.2.1 |
| 装片完工送焊线氮气柜 | die attach finish to wire N₂ cabinet | `scenarioDieAttachToWireBox` | 场景 5.2.2 |
| 焊线/键合完工送关卡 | wire/bond finish to checkpoint | `scenarioWireToCheckpoint` | 场景 5.2.3 |
| 焊线/键合完工送 AOI | wire/bond finish to AOI | `scenarioWireToAoi` | 场景 5.2.4 |
| 清洗间送焊线机台 | cleaning area to wire bonding machine | `scenarioCleaningToWire` | 场景 5.2.5 |
| 氮气柜送焊线/键合机台 | N₂ cabinet to wire/bond machine | `scenarioNitrogenCabinetToMachine` | 场景 5.2.6 |

---

## 6. Roles & Actors 角色与参与者

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 生产操作员 | production operator | `productionOperator` | Use Case Actor；机台 OP |
| 装片设备操作员 | die attach operator | `dieAttachOperator` | 角色 R-01 |
| 烘烤设备操作员 | bake operator | `bakeOperator` | 角色 R-02 |
| WIP 搬运员 | WIP handler | `wipHandler` | 角色 R-03 |
| 关卡检验员 | checkpoint inspector | `checkpointInspector` | 角色 R-04 |
| 清洗操作员 | cleaning operator | `cleaningOperator` | 角色 R-05 |
| 焊线设备操作员 | wire bonding operator | `wireBondingOperator` | 角色 R-06 |
| 键合设备操作员 | bonding operator | `bondingOperator` | 角色 R-07 |
| AOI 检验员 | AOI inspector | `aoiInspector` | 角色 R-08 |
| 班组长 | shift leader / team leader | `shiftLeader` | 角色 R-09；任务取消、核验特批 |
| 生产管理者/车间主任 | production manager / shop floor supervisor | `productionManager` | 角色 R-10 |
| 设备/电气维护人员 | equipment / electrical maintenance engineer | `equipmentEngineer` | 角色 R-11 |
| IT/软件维护人员 | IT / software maintenance engineer | `itEngineer` | 角色 R-12 |
| AGV 运维/调度管理员 | AGV operations / dispatch administrator | `agvDispatchAdmin` | 角色 R-13 |

> 完整角色清单与场景对应见 `requirement-documents/01-stakeholders/stakeholders-and-user-classes.md`。

---

## 7. UI & Operations 界面与操作

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 扫码 | scan (barcode) | `scan` | 扫描工单条形码获取 sublot |
| 手输 | manual entry | `manualEntry` | 扫码异常时允许；需人工确认 |
| 装料 / 装篮 | load / loading | `load` | 将金属篮装入仓位 |
| 卸料 / 卸篮 | unload / unloading | `unload` | 从仓位取出金属篮 |
| 开锁 | unlock | `unlock` | 锁打开 |
| 关锁 | lock | `lock` | 锁关闭（与名词 lock 同词，语境区分） |
| 发车 | dispatch / depart | `dispatch` | AGV 前往下一站点 |
| 异常提示 | error notification | `errorNotification` | MES/RIOT/IO/核验失败提示 |
| 可用仓位 | available slot | `availableSlot` | 界面显示当前可装货的仓位 |

---

## 8. Verification & Error Codes 核验与错误码

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 核验通过 | verification passed | `OK` | 允许装料 |
| 未找到 sublot | sublot not found | `NG_LOT_NOT_FOUND` | MES 未找到该 sublot |
| sublot 已关闭 | sublot closed | `NG_LOT_CLOSED` | 禁止装料 |
| 工序错误 | step error | `NG_STEP_ERROR` | 工序不符合搬运类型 |
| 任务类型错误 | task error | `NG_TASK_ERROR` | task 不符合搬运类型 |
| 搬运类型错误 | move type error | `NG_MOVE_TYPE_ERROR` | moveType 参数错误 |

---

## 9. Document & Requirements 文档与需求工程

| 中文 | English | Code Identifier | Notes 备注 |
| --- | --- | --- | --- |
| 用例 | use case | `useCase` | 如 UC-1 |
| 参与者 | actor | `actor` | Use Case 中的操作主体 |
| 正常流程 | normal flow | `normalFlow` | 主成功路径 |
| 备选流程 | alternative flow | `alternativeFlow` | 分支路径 |
| 异常流程 | exception flow | `exceptionFlow` | 错误/异常路径 |
| 利益相关方 | stakeholder | `stakeholder` | 项目干系人 |
| 愿景与范围 | vision and scope | `visionAndScope` | 对应 `vision-and-scope.md` |

---

## Change Log 变更记录

| Date 日期 | Change 变更 | Author 作者 |
| --- | --- | --- |
| 2026-07-07 | 初始版本，整理系统、设备、MES、任务、场景、角色等核心术语 | — |
| 2026-07-07 | 「弹匣/弹夹」与「弹匣盒」合并为弹匣盒，代码统一 `magazineBox` | — |

---

## Pending Terms 待确认术语

以下术语在不同文档中叫法尚未完全统一，确认后移入正式表格：

| 待确认项 | 当前叫法 | 建议统一为 | 说明 |
| --- | --- | --- | --- |
| 批号 vs 子批号 | 批号条形码 / sublot | **sublot** | UC-1 描述中「批号」建议改为「子批号（sublot）」 |
| 格口 vs 仓位 | 格口 / 仓位 | **slot（仓位）** | vision 文档用「格口」，业务文档用「仓位」；代码与英文统一 `slot` |
