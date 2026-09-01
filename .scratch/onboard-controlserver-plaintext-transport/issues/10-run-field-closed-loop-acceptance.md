# 在明文候选上完成真车闭环现场验收

Type: task
Mode: HITL
Status: resolved
Blocked by: 09

## Question

用户 2026-08-31 选定验收规格为**真车闭环**，不接受仅隔离实例建会话作为等价。本票在候选上
复跑一次完整 WIRE_TO_GATE 闭环，规格对齐上一轮票 29 那次（generation 8、操作员 `S0020310`、
`Stage=Completed`）。

**候选已由票 09 更新**：用 `C:\Users\szy\Desktop\w2g-rc-20260901b-19ce7db`（服务端
`19ce7db70893afea6c6361988c3bc612d77569d0`），不是票 08 冻结的那个。原因见票 08 的「更正」节。

**票 09 转给本票的一条**：`DEMAND-ACCEPTED` 在票 09 记为 INCONCLUSIVE——运行时刻 MES 里 12 条
`WIRE_TO_GATE` 需求全部按名拒绝（多为 `OUT_OF_SCOPE_AREA`），没有一条满足现场条件。评估器逐条走到
判定这件事票 09 证了（`DEMAND-DECISION-REACHED`），但**「受理一条真实需求」至今未在本轮任何运行里
发生过**。本票的闭环必然要受理一条，届时把这条一并证掉；若现场同样长期取不到合格需求，先具名排查
现场条件（区域绑定、电量策略、包装容量唯一性、站点存在性）再谈闭环。

必须走通并取证的：受理 → 取货 → 多仓装货 → 发车安全检查 → `TO_GATE` 移动 → 关卡批量卸货 →
原子完成，`Stage=Completed`、`SessionGeneration` 全程稳定、两条真单各建一次且审计齐全、
`Load`／`Unload` 均 `Committed`。

本轮特有的关注点——传输层换了，要专门看：

- 安全闸门在**明文**形态下仍然在移动中拦、停稳后自动放行而不卡死旅程（票 14 证过 TLS 形态，本轮
  必须重证，因为安全投影的传输方式变了）；
- 会话在整个闭环中不因明文传输出现异常断连或代次跳变；
- HMI 操作记录跟随业务节点（沿用票 29 的截图取证方式）。

前置与安全约束：

- 需要用户到场并给出明确的**现场安全 GO**，正数 `dispatchGeneration`（避免与既有真单撞 `upperId`，
  注意 `upperId` 含 demandId，新 demand 用 `1` 不会撞，重跑同一 demand 才须换代次）；
- RIoT owner 不提供技术支持也不修改 RIoT 程序，遇 RIoT 侧异常按既有边界处理，不作为本轮阻断；
- 判定 RIoT 可达只能用返回 body 的 HTTP 往返，不能用 ping 或 TCP connect（Clash 全局模式会让后者
  对任意主机全绿）。

失败处理：若闭环未走通，据实记录停在哪一段与原因，区分「本轮改造引入」与「本目录脚手架缺陷」
（票 14 的 gen4／5／6 是后者）。**不得以隔离实例结果替代**，也不得把部分走通表述为闭环完成。

## Answer

**闭环走通。** generation 8 于 2026-09-01 11:11:13 在明文候选
`w2g-rc-20260901b-19ce7db`（服务端 `19ce7db` ＋ 车载端 `238b46e` ＋ `protocol-v0.1.1`）上完成
`Stage=Completed`、`BlockReasonCode` 为空。逐条证据在服务端仓
`evidence/g3/20260901-issue10-field-closed-loop/SUMMARY.md`（提交 `ControlServer_MVP@17aec50`），
此处只留结论与偏差。

### 0. 「取不到合格需求」这个担忧不成立，票 09 那条转交项一并更正

开跑前用 `Invoke-Ticket10Preflight.ps1` 把「MES 里有没有合格需求」变成只读可查的：按
`JourneyRuntimeEngine` 的静态闸门顺序逐条判定，只做 GET，不动库、不建单。10:55 快照 15 条
`WIRE_TO_GATE` 里 3 条通过全部静态闸门，开跑前复跑到 6 条。

同时更正票 09：它记的 12 条分布是 `OUT_OF_SCOPE_AREA=10 + AREA_STATION_NOT_FOUND=1 +
BATTERY_POLICY_NOT_SATISFIED=1`，而 `BATTERY_POLICY_NOT_SATISFIED` 在引擎里排在 area、
AREA_EQP 唯一性、站点解析、包装容量**之后**，所以那一刻**其实有一条需求通过了全部静态闸门**，
卡住它的是电量策略（`minimumBatteryPercent: 30`，或车在充电），不是需求池空。票正文里
「若现场同样长期取不到合格需求，先具名排查现场条件」的预案因此没有触发。

### 1. 闭环与两条真单

Demand `f37a0950-…`（`Q26084908-12|WIRE_TO_GATE`，AREA `N2-13`、EQP `3QHS6015`、PACKAGE
`TO-252-2L(4R)`），取货站 `N2-13_N3-13`/29，关卡 `关卡`/210，两筐落 1、2 号仓，全程 11 分 25 秒。
`SessionGeneration` 全程 1（车载端日志里「上层会话已建立：generation=1」只出现一次，12 分钟内无
重连、无代次跳变）。两条真单 `W2G-…-PICKUP-8`／`W2G-…-GATE-8` 各建一次、各五步审计齐全、
`RiotDispatchAuditEvents=10` 无重复建单；`Load`／`Unload` 均 `Committed`。

**`DEMAND-ACCEPTED` 本轮第一次绿**：`AcceptedDemands=1`，票 09 转过来的那条就此关掉。

### 2. 明文形态下的安全闸门（本票的必须重证项）

两条腿各出现一次「移动中拦、停稳放行」，且都是自动恢复、没有卡死旅程：取货腿
`10:59:59→11:03:12` 挂在 `ONBOARD_SESSION_NOT_READY` / `DEPARTURE_SAFETY_NOT_READY`，
`11:03:32` 自动回 `Ready/READY`；关卡腿 `11:07:27→11:10:48` 同形态，`11:11:13` 回 Ready 并落
`Completed`。安全投影本身走明文 HTTP，556 次 GET 全部 200。

### 3. 「本轮真的没有 TLS」用运行自己没写过的观测

进程自报 `Onboard NDJSON listener started on 192.168.200.1:58705; transport=plaintext` 与
`Now listening on: http://192.168.200.1:58707`；车载端 `environment=Production` 绑非 loopback，
是被 `IsForbiddenProductionHost` 检过的事实。另加：四个证书存储的**排序指纹集合摘要**起止零变动
（44/1/42/1 张）、run root 递归零密钥材料文件、27190 行服务端日志 ＋ 146 行车载端日志搜
`Schannel|SslStream|AuthenticationException|X509|certificate|https://` 命中 0。启动脚本还显式清掉
四个过时键的环境变量注入点（键名出现即算存在，空值注入同样算）。

红侧 **8/8**：四个检测器各双向，跑的是 `Stop-Ticket10FieldRun.ps1 -DetectorsOnly` 同一份文件而
非复刻。指纹那条特意让**数量不变**只换一张——计数式检测器看不见这种变化。

### 4. 生产环境与只读仓

生产服务 PID **8632** 全程未漂移、三个监听地址起止一致（按**服务 PID** 取监听，不按进程名）。
隔离实例用 58705/58707，收尾 `portsReleased=True`。车载端仓写入仍为零：用的是候选包里打好的
车载端，身份取自 `release-manifest.json`。

### 5. 三条据实记录，不计入结论

- **`HW-REAL-IO` 仍 INCONCLUSIVE**。用户选定 IO 输入为八仓模拟器（同票 14）。车载端日志里的
  开锁脉冲与逐次 DO／锁 DI／光幕 DI 变化是真实 Modbus 往返，但对端是模拟器。真实 IO 模块、
  接线、锁与光幕的资格本票**未取得**，按票 09 的具名外部资格原样保留。
- **HMI 截图未采集**，票正文要求的票 29 式截图取证方式未复现。业务节点记录改由
  `gen8/onboard.log` 承担（会话建立、子批录入轮询、两装两卸的完整 IO 序列）。**这是取证方式的
  偏离，不是等价替换**；票 11 若需要截图须另行补采。
- **一个先于本轮存在的产品缺陷**：旅程完成后 `11:11:16/:18/:20` 三次轮询各抛
  `BusinessIdentityConflictException: Accepted demand replay does not match its original order
  intent.`（`WireToGateStore.cs:235`），日志记 `Journey runtime iteration failed closed`。成因是
  该 demand 仍在 MES 目录里、引擎按新 `MovementLegId` 找不到既有 `OrderIntent`。**不是本轮改造
  引入的**——调用链与传输层无关，且 TLS 期的票 14 gen7 完成之后出现同一条
  `failed closed`（`evidence/g3/20260830-issue14-field-closed-loop/gen7/host.out.excerpt.log:340`
  起）。它 fail-closed、未污染本次结果，但会让运行期在完成后无法再受理**其他**合格需求。已具名，
  归另起一轮。

收尾时 `11:11:26` 的 `Onboard connection ended with a protocol or transport error.` ＋
`SocketException (10054)` 是收尾脚本杀车载端进程所致，发生在完成之后；装货辅助日志 3 行
`unparsable response` 是它自己 curl 解析的瞬时失败，已自重试成功，仓位终态正确。

## Comments

### 2026-09-01 开跑前只读预检（不动车、不建单、不改状态）

脚本与留档：`8005-agv-control-server/evidence/g3/20260901-issue10-field-closed-loop/`
（`Invoke-Ticket10Preflight.ps1`、`preflight-20260901T1055.txt`）。只做 GET：MesIngest 需求目录、
MesIngest `SUBLOT_BOX_COUNT`、RIoT `GET /api/imap/v1/mapInfo/stations/25`（20260827-map25-readiness
已登记为批准的只读操作）。包装容量按 `PackageCapacitySeed` 在本地复算，未查库。

**结论：合格需求此刻存在，票 09 的取不到需求不是常态。** `catalogRevision=5966` 时 15 条
`WIRE_TO_GATE` 里 **3 条通过全部静态闸门**：

| demandId | area | 取货站 | package | 容量 | 箱数 | 预计筐数 |
| --- | --- | --- | --- | --- | --- | --- |
| `2334d2dc…` | N13-4 | `N13-4_N14-4`/84 | TO-247-2L-A | 6 | 10 | 2 |
| `cf90fcd8…` | N5-5 | `N4-5_N5-5`/37 | TO-252-2L(6R) | 4 | 6 | 2 |
| `f37a0950…` | N2-13 | `N2-13_N3-13`/29 | TO-252-2L(4R) | 5 | 10 | 2 |

其余 11 条 `OUT_OF_SCOPE_AREA`（area 不以 `N` 开头）、1 条 `AREA_STATION_NOT_FOUND`（N23-6 在
map 25 上无 AreaNamedMachineStation）。目录每分钟在变（探测期间 revision 5962→5966、条数
253→252→…），**上表是快照不是预约**，开跑当时须重跑预检取当时的合格条目。

**对票 09 那条转交项的更正**：票 09 记的 12 条判定是
`OUT_OF_SCOPE_AREA=10 + AREA_STATION_NOT_FOUND=1 + BATTERY_POLICY_NOT_SATISFIED=1`。
`BATTERY_POLICY_NOT_SATISFIED` 在引擎里排在 area／eqp 唯一性／站点解析／包装容量**之后**
（`JourneyRuntimeEngine.ValidateDynamicFacts`），所以那一刻其实**有一条需求通过了全部静态闸门**，
卡住它的是动态事实里的电量策略，不是需求池。于是本票的现场前置多一条具名项：
**车辆不得处于 `CHARGING`，且 `batteryPercent ≥ 30`**（`minimumBatteryPercent: 30`）。
「MES 里长期取不到合格需求」这一假设**不成立**，不需要按票正文那样先具名排查现场条件。

预检覆盖不到、只能现场判的动态闸门（`ValidateDynamicFacts` 全序）：`ONBOARD_FACTS_NOT_READY`、
`ONBOARD_DEPARTURE_UNSAFE`、`RIOT_VEHICLE_NOT_AVAILABLE`、`RIOT_VEHICLE_BINDING_MISMATCH`、
`RIOT_VEHICLE_NOT_IDLE`、`RIOT_VEHICLE_MAP_MISMATCH`、`RIOT_VEHICLE_FACT_STALE`、
`BATTERY_FACT_UNKNOWN`、`BATTERY_POLICY_NOT_SATISFIED`、`RIOT_VEHICLE_NOT_STOPPED`、
`RIOT_VEHICLE_ORDER_OCCUPIED`，以及其后的 `TASK_TYPE_NOT_ALLOWED_AT_STATION`。

环境核对（同刻）：生产服务 `8005 AGV ControlServer` Running、PID 8632、听 58005/58007；
MesIngest Running、听 5088；候选根 `C:\Users\szy\Desktop\w2g-rc-20260901b-19ce7db` 在位；
两个仓工作树干净（本仓 `c8fc6e3f`，服务端 `a0f1b3f`）。

顺带记一条 harness 事实：RIoT 的 `CallApiKey` 是按 **`Authorization: Bearer <key>`** 发的，不是
同名请求头——试 `CallApiKey` / `X-Call-Api-Key` / `apiKey` 三种头名都回 401。SDK 里只留了
`BearerPrefix` 这一处线索。
