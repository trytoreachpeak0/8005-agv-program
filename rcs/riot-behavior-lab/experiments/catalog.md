# 测试目录（Test Catalog）

本文件是**可复用**的实验定义：研究问题、前置条件、程序、结构预期、待验证行为、反例、风险等级和人工干预可能性。这些内容不承载任何一轮的实际结果。

**具体某一轮跑到哪一步、结果是什么，不在本文件里**，见 [`evidence/rounds/<该轮>/round-plan.md`](../evidence/rounds/) 和 [`evidence/rounds/<该轮>/execution-log.md`](../evidence/rounds/)。

约定：下文 `{{baseUrl}}` / `{{testVehicleKey}}` 均从 [`environment.local.json`](../environment.local.json) 读取；订单命名建议带 `riot-behavior-lab-<编号>-<timestamp>` 前缀，便于事后检索。`code == 0` 目前只作为待逐模块验证的成功假设，不作为全平台既定事实。

---

## 1. 总览表

| 类别 | 编号 | 测试项 | 只读/写 |
|---|---|---|---|
| A 鉴权连通性 | A1 | 登录拿 token | 只读 |
| A 鉴权连通性 | A2 | 调用密钥直接访问业务接口 | 只读 |
| B 设备/车辆状态 | B1 | 车辆清单、非车过滤、名称→deviceKey | 只读 |
| B 设备/车辆状态 | B2 | `getVehicleInfo`：位置/电量/任务状态 | 只读 |
| C 地图/站点/路网 | C1 | 地图列表 `mapInfo/all` | 只读 |
| C 地图/站点/路网 | C2 | 单图站点 stations/{mapId} | 只读 |
| C 地图/站点/路网 | C3 | 边/路网 `edges/{mapId}` | 只读 |
| C 地图/站点/路网 | C4 | 地图关系 Map Relation | 只读 |
| D 调度只读 | D1 | 路径成本 `getRouteCostsBy` | 只读 |
| D 调度只读 | D2 | Route Controller 全套 GET/POST（禁 DELETE） | 只读/写-查询 |
| E 移动订单 | E1 | 创建一个移动订单 | 写 |
| E 移动订单 | E2 | 监控订单直到到站 | 只读（依赖 E1） |
| E 移动订单 | E3 | 对进行中订单做 interrupt | 写 |
| E 移动订单 | E4 | 按车查积压订单并清队后再派 | 写 |
| F 充电调度 | F1 | 指定该车充电 | 写 |
| G 停靠 | G1 | 空闲返停靠点 | 写 |
| H 启停设备 | H1 | disable 测试车 | 写 |
| H 启停设备 | H2 | enable 测试车（收尾） | 写 |

某一轮要测哪些、跳过哪些、批准到什么程度，记在该轮的 `round-plan.md` 里。实验优先级由 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) 驱动。

---

## 2. 依赖顺序图

```mermaid
flowchart TB
  A2["A2 调用密钥直接访问"]
  A1["A1 登录拿 token"]
  A2 --> B1
  A1 -.->|"备用鉴权路径"| B1
  B1 --> B2
  B1 --> C1 --> C2
  C1 --> C3
  C1 --> C4
  B2 --> D1
  B2 --> E1
  C2 --> E1
  E1 --> E2 --> E3
  E3 --> E1b["再走一次完整 E1→E2（不中断，作对照）"]
  E1b --> H1H2["H1 disable / H2 enable（收尾）"]
  F1["F1 充电调度（默认不接入主线，按需单独接上）"]
  G1["G1 停靠（默认不接入主线，按需单独接上）"]
```

**排序理由**：当前 P0 先确认 A2（调用密钥）能否替代每次登录；A1 保留为对照/备用。A/B/C/D 只读、互不影响，先摸清字段；E1 需要 C2 有效站点和 B2 车辆当前状态才能选安全目的地；E3 验证完后补一次不中断完整流程作对照；H 放最后，因为 disable 会挡住后续接单。F1/G1 默认不接入主线，是否本轮测由 `round-plan.md` 决定。

---

## 3. 已核实状态枚举（来自 swagger / Kiota 注释，非猜测）

这些不是根据经验猜的，是直接读 `rcs/riot-sdk/csharp/RIoT.Sdk.Generated/**` 里 Kiota 生成代码上保留的 XML doc 注释找到的——这些注释原样来自 `rcs/riot_swagger/{order,task}.json` 里各字段的 `description`。它们的证据等级是 `SCHEMA`，只说明静态契约声明，不代表现场已经观测到。

| 来源 | 字段/枚举 | 取值 |
|---|---|---|
| `OrderRecordObject.OrderState` | `orderState` | 1 QUEUEING, 2 CANCELLED, 3 EXECUTING, 4 FAILED, 5 SUCCESS, 6 DELETED, 7 PAUSED, 8 SUSPENDED, 9 HANG, 10 队列优先执行 |
| `OrderRecordObject.OrderType` | `orderType` | 1 NORMAL, 2 CHARGE, 3 CMD（停靠）, 4 MAINTAIN |
| `VehicleTaskInfo_procState` | `procState` | `AWAITING_ORDER`, `IDLE`, `PROCESSING_ORDER`, `INNER_PAUSE`, `IN_CANCEL`, `USER_FORCE_IDLE`, `USER_FORCE_IDLE_FINISHED`, `INNER_FORCE_IDLE`, `UNAVAILABLE` |
| `OrderCommandDTOObject_commandType` | 订单命令 | `CMD_ORDER_CANCEL`, `CMD_ORDER_HELD`, `CMD_ORDER_REJECTED`, `CMD_ORDER_CONTINUE_FROM_HANG` / `_HELD` / `_REJECTED`, `CMD_ORDER_JUMP_FROM_HANG` |

**已知缺口**：枚举只说明「有哪些状态」，未写清转移条件（例如 `interrupt` 会落到 `PAUSED` 还是 `HANG`）。观察结果先进入 [`../evidence/`](../evidence/)，经过复核后再进入 [`../knowledge/state-model.md`](../knowledge/state-model.md)，不把单次观察直接改写成静态枚举事实。

---

## 4. 卡片字段模板

每条卡片固定包含下列字段（顺序勿打乱）：

```
#### <编号> <名称>
- 测试意图：…
- 前置条件：…
- 测试程序：…
- 预期结果：…
- 反例/边界（负面路径）：…（无则写「无」并说明为何这条不需要）
- 风险等级：只读 / 写-可逆 / 写-需人工复核
- 人工干预：无 | 可能需要：…（触发则按 README §6 停住）
```

**这些字段都是目录级别的固定设计，不含任何具体某一轮的执行结果**——执行结果、时间戳、真实调用摘要，记在对应轮次的 `execution-log.md` 里，通过编号对应回本文件的卡片。

「人工干预」写法：

- `无`：正常路径不需要人；中途出意外仍可按 [`README.md`](../README.md) §6 临时升级为 `等待人工`。
- `可能需要：…`：已知常见阻塞点，触发即在当轮改状态并停写操作。

「反例/边界」写法（见 [`fixtures/README.md`](../fixtures/README.md) 了解反例产物如何变成 mock 素材）：

- 每条反例写清楚「输入什么」+「期待的失败表现」（业务失败码 / 4xx，而不是 500、崩溃、或误伤其它车/订单）。
- 反例的核心价值是**安全边界验证**：对写接口（E1/E3/H1/H2），反例专门测「传一个不存在/不合法的 key 会不会被系统悄悄兜底到别的车」——这类反例本身风险极低（预期是失败、不产生真实副作用），但一旦系统行为不符合预期就是重大发现，必须记下来即使标「失败」，并按 [`safety-boundaries.md`](../governance/safety-boundaries.md) 处理。
- 反例执行后同样落一份 fixture（命名与 schema 见 [`fixtures/README.md`](../fixtures/README.md)），作为以后写 SDK 单测时「异常路径 mock」的素材，不止是「正常路径 mock」的补充。

---

#### A1 登录拿 token

- **测试意图**：确认现场鉴权可用，后续所有调用有有效 Bearer token；对应 SDK `POST /api/auth/v1/admin/login`。
- **前置条件**：本机可访问 `baseUrl`；账号密码见 [`../environment.local.json`](../environment.local.json)。
- **测试程序**（只读）：
  1. `POST {{baseUrl}}/api/auth/v1/admin/login`，body 含 username / password。
  2. 或跑既有冒烟：`RIOT_SMOKE=1` + 同组环境变量后执行 `rcs/riot-sdk/scripts/smoke-csharp.ps1` / `smoke-python.ps1`（冒烟还会顺带打设备列表）。
- **预期结果**：返回非空 access token（及 refresh 若有）；HTTP 成功；无 401/502。
- **反例/边界**：
  1. 密码错误（用户名对、密码错）→ 期待：登录不成功，不应返回可用 token。
  2. （可选）缺失字段/空 body → 期待 4xx 或业务失败码。
- **风险等级**：只读
- **人工干预**：可能需要：本机到现场网络不通 / 浏览器也登不上时，由用户确认 VPN/现场网络或账号是否变更。

---

#### A2 调用密钥直接访问业务接口

- **测试意图**：验证 RIoT 网页「调用密钥设置」中的长期密钥，能否在**不调用** `POST /api/auth/v1/admin/login` 的前提下，以 `Authorization: Bearer <callApiKey>` 访问业务只读接口；对应假设 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) Q-015。
- **前置条件**：本机可访问 `baseUrl`；`environment.local.json` 中已配置 `callApiKey`（来自网页调用密钥，勿提交仓库）。
- **测试程序**（只读）：
  1. **正例**：不登录。对同一只读探针 `GET {{baseUrl}}/api/imap/v1/mapInfo/all` 设置头 `Authorization: Bearer {{callApiKey}}` 并请求。
  2. **对照正例（可选）**：同一密钥再打 `GET {{baseUrl}}/api/device/v1/devices`（分页默认即可），确认不止地图模块可用。
  3. **反例-无鉴权**：同一探针去掉 `Authorization`。
  4. **反例-伪造密钥**：`Authorization: Bearer invalid-call-key-riot-behavior-lab`。
  5. 全程禁止调用 `admin/login`；禁止任何写接口。
- **预期结果**：
  - 正例：HTTP 与业务层均表明鉴权通过（记录实际 `httpStatus`、业务 `code`、是否返回非空业务数据）。
  - 反例：鉴权失败且无业务数据泄露；记录失败是 HTTP 401/403 还是 HTTP 200 + 业务失败码。
- **反例/边界**：见测试程序步骤 3、4；本卡不测密钥刷新、权限范围差异、过期密钥（若后续需要另开实验卡）。
- **风险等级**：只读
- **人工干预**：可能需要：密钥已在网页侧禁用/轮换，或本机网络不通时由用户确认。

---

#### B1 车辆清单、非车过滤与名称→deviceKey

- **测试意图**：弄清系统里有哪些**可调度车辆**；确认设备列表会混入非车设备；验证能否用车辆名解析到 `deviceKey`。对应 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) Q-016 / Q-017。
- **前置条件**：A2 或 A1 通过（优先 A2 调用密钥路径）。
- **测试程序**（只读）：
  1. `GET {{baseUrl}}/api/device/v1/devices?current=1&pageSize=100`（注意：本现场 `pageSize` 比 `size` 更可靠拉全量；`current+size` 翻页可能重复第 1 页）。
  2. `GET {{baseUrl}}/api/task/vehicles/getAllVehicleKeys`
  3. `GET {{baseUrl}}/api/task/vehicles/getAllVehicleSimpleInfo`（期望直接给出 `deviceName`↔`deviceKey`）
  4. 对照：`GET {{baseUrl}}/api/task/vehicles/getAllTaskVehicles`（富对象；标识字段位置另行记录）
  5. 交叉：device 列表 − task 车辆 key 集 = 非调度设备样本；记录其 `productKey` / `deviceType`。
  6. 名称解析正例：用已知测试车 `deviceName` 在 simpleInfo 结果中精确匹配，得到 `deviceKey`，并与 `environment.local.json` 的 `testVehicleKey` 对照。
  7. 名称解析反例：用不存在的车名匹配，期待 0 命中。
- **预期结果**：
  - 能得到可调度车辆集合（本现场观测口径：出现在 task 车辆接口中的 key）。
  - 能证明 devices 接口含非车设备，不能直接当“车辆列表”。
  - 能证明（或证伪）`deviceName → deviceKey` 在本现场可唯一解析。
- **反例/边界**：
  1. 不存在的车辆名 → 0 命中，不得模糊匹配到其它车。
  2. （若出现重名）记录为重大契约风险：禁止只按名称派车。
- **风险等级**：只读
- **人工干预**：可能需要：用户确认测试车在网页上的显示名，或确认某台“像车”的设备是否应纳入调度。

---

#### B2 getVehicleInfo：位置 / 电量 / 任务状态

- **测试意图**：拿到调度视角与设备物模型运行态，确认当前图/站/电量/任务态；对应 Round6 结论 BC-STATE-001。
- **前置条件**：B1 通过；车已上线；优先 A2 调用密钥。
- **测试程序**（只读）：
  1. **调度面**：`GET {{baseUrl}}/api/task/v1/task/getVehicleInfo/{{testVehicleKey}}` → 关注 `vehicleTaskInfo.procState`、`vehicle.currentStation`、**`vehicle.previousState.mapName`**（不要只扫顶层）。
  2. **物模型面**：`GET {{baseUrl}}/api/device/v1/runtime/properties/{{testVehicleKey}}` → 关注 `mapName`、`stationNo`、`sysState`、`movementState`、`multiLoadState`、`batteryPercentage`。
  3. **不要**把 `GET /api/device/v1/runtime/status/{{testVehicleKey}}` 当主状态源（仅 online）。
  4. 用 `mapName` 在 C1 地图清单中精确反查 `mapId`。
  5. 记录在站/离站对照：若 `currentStation`/`stationNo` 为 **0** 且 `noStation=true`，记为离站（见 BC-STATE-002），同时仍应读到 `mapName` 与坐标。
- **预期结果**：能读到地图名并解析出 mapId；能区分在站（正整数站号）与离站（0）；两面关键字段可对照。
- **反例/边界**：
  1. `getVehicleInfo/{deviceKey}` 传不存在的 key → 期待失败或空，不得串车。
  2. `getVehicleInfoByDeviceKey` 本现场曾返回 `code=00002`，不作为主路径。
- **风险等级**：只读
- **人工干预**：可能需要：急停未复位、手自动模式不对、定位丢失时由用户改车态。

---

#### C1 地图列表 mapInfo/all

- **测试意图**：拿到现场有效地图清单（`mapId` ↔ 地图名），供后续选站与建单；对应 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) Q-018。
- **前置条件**：A2 或 A1 通过（优先 A2）；B1 建议已完成（便于对照测试车）。
- **测试程序**（只读）：
  1. `GET {{baseUrl}}/api/imap/v1/mapInfo/all`（证据中剥离 `mapJson` 几何，只保留 id/name 等摘要）。
  2. 对照轻量接口（若可用）：`GET {{baseUrl}}/api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson`。
  3. 可选：用测试车 `deviceKey` 查只读车辆信息，记录地图相关字段（若有），作为“车当前在哪张图”的线索，不作为本卡唯一通过条件。
- **预期结果**：`code == 0`；至少一条有效地图；产出完整 `mapId`/地图名列表。
- **反例/边界**：
  1. 不带 Authorization 直接请求 → 期待 `401`（A2 已覆盖时可引用，不必每轮重打）。
- **风险等级**：只读
- **人工干预**：可能需要：用户确认后续派车拟用的地图名/`mapId`（尤其多图现场）。

---

#### C2 有效站点 stations/{mapId}

- **测试意图**：读取单图有效站点清单（`stationId`↔站名等），作为建单目的地前置；对应 [`../hypotheses/open-questions.md`](../hypotheses/open-questions.md) Q-019。
- **前置条件**：C1 通过；已有候选 `mapId`（用户指定，或按测试命名/历史线索选取，如本现场 26–29）。
- **测试程序**（只读）：
  1. `GET {{baseUrl}}/api/imap/v1/mapInfo/stations/{{mapId}}`，保存站点摘要（id/name/类型/坐标等标量；剥离超大嵌套）。
  2. 可选：`GET {{baseUrl}}/api/imap/v1/mapInfo/{{mapId}}` 单图摘要（无 mapJson）。
  3. 可选：`GET {{baseUrl}}/api/imap/v1/mapInfo/{{mapId}}/{{stationId}}` 单站探针。
  4. 反例：不存在的 `mapId`（如 `0`）。
  5. 若车辆有 `currentStation`，记录该站是否出现在候选图站点列表中（交叉线索，不单独定论绑图）。
- **预期结果**：`code == 0`；得到可枚举的站点列表与字段结构；能说明如何用站名/站号选目的地。
- **反例/边界**：
  1. 非法 `mapId` → 空列表或业务失败码，不应兜底返回其它地图站点。
- **风险等级**：只读
- **人工干预**：可能需要：用户确认测试用 `mapId` 与安全目的站（写操作前必须拍板）。

---

#### C3 边 / 路网 edges/{mapId}

- **测试意图**：确认路网边数据可查，后续理解路径成本 / 多仓位连通性时有底。
- **前置条件**：C1 通过；同一 `mapId`。
- **测试程序**（只读）：`GET {{baseUrl}}/api/imap/v1/mapInfo/edges/{{mapId}}`。
- **预期结果**：`code == 0`；边列表非空（或明确空但可解释）；抽查与 C2 站点连通相关的边字段结构。
- **反例/边界**：
  1. 传不存在的 `mapId` → 期待：空列表或业务失败码，同 C2。
- **风险等级**：只读
- **人工干预**：无
- **状态**：**已执行 Round 43**（2026-09-03，生产 RIoT `172.19.206.222:8888` map25）。结论见 `knowledge/behavioral-contracts.md` 的 **BC-MAP-003** 与 **BC-ROUTE-002**：边表可支撑站到站代价自算（23/23 复现 RIoT 的择站选择），但线格式是 snake_case 且 `s_node`／`e_node` 与 Kiota 模型对不上，须自定义反序列化；图是有向的。另发现 `queryNearEnd` 遇不可达站点抛 kernel NPE。

---

#### C4 地图关系 Map Relation

- **测试意图**：摸清多仓位/多地图如何组织（地图关系），对应项目「多仓位」组织方式。
- **前置条件**：C1 通过。
- **测试程序**（只读）：
  1. `GET {{baseUrl}}/api/imap/v1/mapRelation/all`
  2. 必要时再 `GET /api/imap/v1/mapRelation/`（分页查询）。
- **预期结果**：`code == 0`；记录关系条目条数与关键字段（关联的 mapId 等）；即使为空也算通过（说明现场可能单图），在执行日志注明。
- **反例/边界**：无（纯列表查询，无可构造的有意义反例；异常路径已被 C1/C2 的鉴权与非法 mapId 覆盖）。
- **风险等级**：只读
- **人工干预**：无

---

#### D1 路径成本 getRouteCostsBy

- **测试意图**：验证 `POST /api/task/v1/route/getRouteCostsBy` 为指定车到指定站给出代价/可达性。对应 Q-026 / BC-ROUTE-001。
- **前置条件**：B2、C2 通过；已知车辆 key 与目标站点；`deviceKeys` 仅含测试车。
- **测试程序**（只读）：body `{mapId, stationId, deviceKeys:[testVehicleKey]}`。
- **预期结果**（Round15）：`code==0`；`deviceCostsList[].costs` 非负 mm + `ok`，或 `-1` + unreachable（跨图常见）。
- **反例/边界**：跨图目的站 → `-1`；假 deviceKey 记录返回形态。
- **风险等级**：只读
- **人工干预**：无（若持续不可达，升级到 C2 的人工选站）

---

#### D2 Route Controller GET/POST（禁 DELETE）

- **测试意图**：摸清 Route 分组可读接口形态与业务场景；禁止 `DELETE dynamicRouteCost*`。对应 Q-026。
- **前置条件**：用户指定研究地图（如 map28 新基测试2opt）；安全边界仅本车。
- **测试程序**：
  1. `GET /api/task/v1/route/`、`GET .../getCostUnit`
  2. `POST getRouteCostsBy`（目标图多站 + 当前图对照）
  3. `POST queryNearEnd` / `queryNearestStart`（目标图拓扑）
  4. `GET curRemainCost/{orderKey}`（假单；可选 EXECUTING 采样）
- **预期结果**（Round15）：Near* 不依赖车在图；costs 跨图 -1；动态 GET 可空；remain 未执行时为 MAX 哨兵。
- **反例/边界**：Near* 空候选 → NPE；非法 map 可能 `result=null`。
- **风险等级**：只读（查询类 POST）；若为 remain 临时建单则写-可逆（须 cancel）
- **人工干预**：若需 EXECUTING remain，可能需把车放到目标图/站上。

---

#### E1 创建一个移动订单

- **测试意图**：验证指定车辆创建移动订单；确认 `appointVehicleKey` 生效、不会派到别的车。对应 Q-001 / Q-011；契约 BC-ORDER-001 / BC-ORDER-002。
- **前置条件**：B2 车空闲可接单；**`integrationLevel=ON_LINE` 且 `enable=true`**；C2 已选定同图安全目的站；当轮写操作已获批准。
- **测试程序**（写，Round7 已验证主路径）：
  1. **主路径**：`POST {{baseUrl}}/api/order/v1/add/byDefaultMissions`，至少包含：
     - `appointVehicleKey`: `{{testVehicleKey}}`（必须）
     - `isAppointEnable`: `1`
     - `lockStatus`: `0`
     - `mission`: `[{ "type":"move", "mapId": <mapId>, "destination": <stationId> }]`
     - `orderName` / `upperId`: 前缀 `riot-behavior-lab-E1-{{timestamp}}`
  2. **对照（本现场失败）**：`POST /api/task/v1/order` 多种 body 曾 NPE——不要当主路径，除非新证据翻案。
  3. 记录返回的 `orderId`；用 `detailByUpperId` 复查。
- **预期结果**：`code == 0`；`executeVehicleKey` 为本测试车；`orderState` 进入 `1` 或 `3`；车侧可出现 `PROCESSING_ORDER` / `MT_RUNNING`。
- **反例/边界**（**安全边界核心验证**——预期都是"创建失败"，不产生真实副作用，风险实际很低）：
  1. `appointVehicleKey` 指向一个**不存在或已离线**的 key → 期待：创建失败/报错，**绝不能被系统"自动兜底"派给测试车之外任何其它在线车**（这是 `safety-boundaries.md` 第 1 条的直接验证，一旦系统真派了车，是严重发现，必须立刻记录并升级人工，不再继续 E 系列）。
  2. `appointMapId` 与 `mission` 里站点不属于同一地图 → 期待：创建失败，不应派车走错图。
- **反例/边界**（Round10 已测）：
  1. 传**不存在**的 `appointVehicleKey` → **仍会 `code=0` 进 QUEUEING**（BC-ORDER-007）；必须立即 cancel，并视为安全边界发现。
  2. **省略** `appointVehicleKey` → 同上会进队列；禁止业务依赖“系统拒绝”。
  3. 非法 `mapId`/`destination` → `0660003` 目的地站点不存在，未落库。
  4. 相同 `upperId` 重复提交 → `0610008` 订单已存在（BC-ORDER-004）。
- **风险等级**：写-可逆（可用 cancel 收尾；勿用全局清理接口；**勿用 interrupt 当纯 move 暂停**）
- **人工干预**：可能需要：发单前确认车旁无人/无障碍、车已自动模式；若车被非本轮订单占用且 API 取消失败，由用户在 UI 清障后再发；**若反例真的派车给了别的车，立刻停止并等待人工介入**。

---

#### E2 监控订单直到到站

- **测试意图**：观察订单状态机真实流转到完成；验证轮询/查询路径可用。
- **前置条件**：E1 成功并持有 `orderId`。
- **测试程序**（只读，依赖 E1）：
  1. 轮询其一或组合：
     - `GET /api/order/v1/orderRecord/detailByOrderId/{{orderId}}`
     - `GET /api/order/v1/orderRecord?executeVehicleKey={{testVehicleKey}}&...`
     - `GET /api/task/v1/task/getVehicleInfo/{{testVehicleKey}}`
  2. 间隔建议 2–5s，直到终态或超时（超时阈值实测时写明，建议 ≤ 数分钟；超时则记失败并考虑 cancel）。
- **预期结果**：`orderState` 最终为 `5 SUCCESS`；过程中可出现 `1 QUEUEING` → `3 EXECUTING`；完成后车 `procState` 回到 `IDLE` / `AWAITING_ORDER`；目的站与 E1 一致或可解释。
- **反例/边界**：无独立反例（本条是纯监控；异常路径——中断、越权、无效订单——分别由 E3 与 E1 的反例覆盖）。
- **风险等级**：只读（监控本身）
- **人工干预**：可能需要：车中途被挡/急停/交通管制导致长时间不前进时，由用户现场处置或确认可 cancel；AI 先尝试 API cancel，失败再等用户。

---

#### E3 对进行中订单做 interrupt

- **测试意图**：**重点验证未知语义**——`POST /api/task/v1/order/interrupt` 实际把 `orderState` / `procState` 打到哪（`PAUSED` vs `HANG` 等），以及是否需后续 `CMD_ORDER_CONTINUE_FROM_*` 才能恢复。
- **前置条件**：再创建一笔短距移动订单（同 E1 约束），且订单已进入 `3 EXECUTING`、车在移动中（勿等 SUCCESS）。
- **测试程序**（写）：
  1. 创建订单（同 E1，`orderName` 带 `riot-behavior-lab-E3-...`）。
  2. 确认 `orderState == 3 EXECUTING` 后立刻：`POST {{baseUrl}}/api/task/v1/order/interrupt`，body `InterruptOrderDtoObject`：
     - `orderId`: 当前订单
     - `pause`: `true`（先测暂停车辆语义；完整 body 记入执行日志）
     - `missions`: 按现场需要可空或附后续 mission——**第一次建议最小字段**，以观察默认行为
  3. 立即查订单详情 + `getVehicleInfo`，记录 `orderState`、`procState`。
  4. 若落入可恢复态，按需用 `POST /api/task/v1/order/command/{{orderKey}}` 发 `CMD_ORDER_CONTINUE_FROM_HELD` / `CMD_ORDER_CONTINUE_FROM_HANG` 或 `CMD_ORDER_CANCEL` 收尾，**避免车长期挂起**。
  5. E3 结束后：再跑一次**完整 E1→E2（不中断）**作对照，确认车恢复正常（见顺序图 `E1b`）。
- **预期结果**（Round9/10）：对**纯 move** 执行中，`interrupt`（`pause` true/false）均业务失败 `code=100036`，状态不变——须记实。需要暂停时改用 `CMD_ORDER_HELD` / `CONTINUE_FROM_HELD`（BC-ORDER-006）。取消用 `CMD_ORDER_CANCEL` 或 `order/v1/operate`。含 `act` 执行中的 interrupt 仍待测。
- **反例/边界**：
  1. 对一个**已是终态**（SUCCESS/CANCELLED）的订单发 interrupt → 期待：业务失败，不应报成功、不应影响测试车当前其它订单。
  2. 传一个**不存在**的 `orderId` → 期待：报错，不应误中断测试车正在执行的其它订单。
- **风险等级**：写-需人工复核（状态机语义以实测为准；必须善后）
- **人工干预**：可能需要：interrupt/command 后车长期挂起或现场不安全时，由用户 UI/车端强制恢复；善后完成前不进入对照 E1→E2。

---

#### E4 按车查积压订单并清队后再派

- **测试意图**：验证如何列出指定车的非终态订单（含 QUEUEING 积压），取消队列/挂起单后新单可生效。对应 Q-025；契约 BC-ORDER-013。
- **前置条件**：测试车 `ON_LINE`；mapId=29 短距可跑；写操作已批准。
- **测试程序**：
  1. 建单 A 等到 `EXECUTING`，再连续建 B/C → 期望 B/C 为 `QUEUEING` 且 `executeVehicleKey="--"`。
  2. 对照查询：
     - `GET /api/order/v1/orderRecord?executeVehicleKey={{testVehicleKey}}&filterByState=1&filterByState=3&filterByState=7&filterByState=9`
     - 同接口加 undoc `appointVehicleKey`（预期不可靠）
     - `filterByState=1,3,7,9` 后客户端按本车 `appointVehicleKey`/`executeVehicleKey` 过滤
  3. 可选：对 A `CMD_ORDER_HELD`。
  4. 对 QUEUEING/HELD（按需含 EXECUTING）`CMD_ORDER_CANCEL`，等到 `IDLE`。
  5. 再建新单 N，确认可进入 `EXECUTING`。
- **预期结果**（Round14）：`executeVehicleKey` 过滤漏 QUEUEING；`appointVehicleKey` 查询参数不可靠；客户端过滤可检出积压；清队后新单可执行。
- **反例/边界**：只依赖 `executeVehicleKey` 清队 → 会漏掉 `execute=--` 的队列单。
- **风险等级**：写-可逆（cancel 收尾；只操作本车指定单）
- **人工干预**：若清队后车长期非 IDLE，由用户 UI 确认现场后再继续。

---

#### E5 QUEUEING 长期滞留原因只读诊断

- **测试意图**：验证 `GET /api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey}` 的真实标识、鉴权、响应与错误契约，对应 Q-040。
- **前置条件**：目标环境和 build 已绑定；仅使用 `environment.local.json` 中的测试车；本轮不得包含任何写接口。
- **测试程序**（只读）：
  1. 保存测试车信息和当前 `QUEUEING(1)` 列表的前置快照；只在客户端按 `appointVehicleKey`/`executeVehicleKey` 收敛到测试车。
  2. 优先对当前测试车 QUEUEING 订单尝试其字符串 `orderId`；没有当前样本时，使用已有轮次中已终结的测试车订单，分别探测字符串 `orderId`、数值 id 与 `upperId`。
  3. 对未知订单、未知车辆、无鉴权和假鉴权做只读反例；逐次保存时间、脱敏请求、HTTP 状态、业务包装及完整响应。
  4. 若获得 `code=0` 且 `result` 非空的有效组合，对同一组合重复调用至少三次，比较 `reason` 与 `suggestList`，并检查是否存在服务端观测时间或状态版本。
  5. 再次保存车辆信息和当前 QUEUEING 列表；比较前后可观测状态，任何未知变化立即停止。
- **预期结果**：只据实确认已出现的原因文本和建议；未出现的场景保持未验证。自由文本或未知文本一律不得升级为自动动作映射。
- **反例/边界**：历史订单结果不能冒充其创建时的原因；没有新鲜度字段时不能假定响应对应哪个状态时点；接口名和 GET 方法本身不能单独证明无副作用。
- **风险等级**：只读。
- **人工干预**：若当前没有所需 QUEUEING 场景，结束本轮并把缺口交给后续经明确批准的受控场景轮次，不现场制造状态。

---

#### F1 指定该车充电

- **测试意图**：验证 `POST /api/task/v1/order/charge/{vehicleKey}` 为指定车生成充电订单（`orderType=2 CHARGE`）。
- **前置条件**：车空闲；现场有可用充电站；本条写操作已获用户单独授权。
- **测试程序**（写）：`POST {{baseUrl}}/api/task/v1/order/charge/{{testVehicleKey}}`（body 若 schema 需要则按 swagger 补全）。
- **预期结果**：`code == 0`；出现充电订单且执行车为本车；后续可观察到充电相关状态（勿强行打断其他车）。
- **反例/边界**：`vehicleKey` 传不存在设备 → 期待报错，不误发给其它车。
- **风险等级**：写-需人工复核
- **人工干预**：可能需要：确认充电桩空闲、线缆/对接安全。
- **默认不接入主线**：是否某一轮测这条，由该轮 `round-plan.md` 决定；默认跳过，需要用户单独授权才执行。

---

#### G1 空闲返停靠点

- **测试意图**：验证一键停靠 `POST /api/task/vehicles/park` 仅作用于测试车（或可按 key 限定的 body）。
- **前置条件**：车空闲；确认请求不会变成「全部车辆停靠」；本条写操作已获用户单独授权。
- **测试程序**（写）：`POST {{baseUrl}}/api/task/vehicles/park`，body 必须能限定到 `{{testVehicleKey}}`（schema 为自由 object——**实测前先只读确认 UI/文档等价参数**；若无法单车限定则放弃调用）。
- **预期结果**：仅测试车生成停靠类订单/行为（`orderType=3 CMD` 若产生订单）；其他车无变化。
- **反例/边界**：body 里 key 传不存在设备 → 期待报错，不误停其它车。
- **风险等级**：写-需人工复核
- **人工干预**：可能需要：无法用 API 单车限定时放弃调用，改由用户确认 UI 是否有单车停靠入口。
- **默认不接入主线**：是否某一轮测这条，由该轮 `round-plan.md` 决定；默认跳过，需要用户单独授权才执行。

---

#### H1 disable 测试车

- **测试意图**：验证单车禁用后不再接单；确认 path 级 `deviceKey` 生效、不影响其他车。
- **前置条件**：E 系列（含对照 E1→E2）已完成；车当前无进行中订单（或已终态）。
- **测试程序**（写）：`POST {{baseUrl}}/api/device/v1/devices/disable/{{testVehicleKey}}`。
- **预期结果**：`code == 0`；随后 B1/B2 可见该车为禁用；尝试（可选、仅本车）创建订单应失败或不再被调度；**其他车状态不变**。
- **反例/边界**（**安全边界核心验证**）：
  1. `deviceKey` 传一个不存在的设备 → 期待：报错，**绝不能误禁用测试车之外的其它任何车**；若真的影响了其它车，立刻停止、走人工升级并立即用 enable 恢复受影响的车。
- **风险等级**：写-可逆（必须立刻做 H2）
- **人工干预**：无（若 disable 后异常，优先 H2 enable；仍失败再等用户 UI 恢复；反例出现误伤其它车则立刻升级人工）

---

#### H2 enable 测试车（收尾）

- **测试意图**：恢复测试车可用，作为收尾，避免留下禁用状态。
- **前置条件**：H1 已执行。
- **测试程序**（写）：`POST {{baseUrl}}/api/device/v1/devices/enable/{{testVehicleKey}}`。
- **预期结果**：`code == 0`；车重新 enable；`procState` 回到可接单类状态；结束时测试车可用。
- **反例/边界**：
  1. `deviceKey` 传不存在的设备 → 期待：报错，不影响测试车或其它车的启用状态（与 H1 反例对称）。
- **风险等级**：写-可逆
- **人工干预**：可能需要：API enable 失败时由用户在 UI 重新启用，避免测试车留下禁用。

---

## 5. 与其他资料的关系

- 接口路径来自 [`../../riot_swagger/`](../../riot_swagger/)，并与 [`../../riot-sdk/`](../../riot-sdk/) 中已生成模块交叉核对。
- 静态来源只提供 `SCHEMA` 证据；现场结果进入 [`../evidence/`](../evidence/)，已复核语义进入 [`../knowledge/`](../knowledge/)。
- `riot-sdk` 冒烟最小联调见 [`../../riot-sdk/docs/smoke-test.md`](../../riot-sdk/docs/smoke-test.md)——那份验证的是“SDK 能不能跑通”，本目录验证的是“RIoT 真实行为是什么”，两者互补。
