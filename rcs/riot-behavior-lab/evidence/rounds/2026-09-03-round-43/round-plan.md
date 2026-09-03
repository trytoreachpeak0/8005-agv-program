# Round 43（2026-09-03）— 路网边表能否支撑站到站路径代价自算（生产 RIoT，mapId 25）

## 问题

- `GET /api/imap/v1/mapInfo/edges/{mapId}` 的现场线格式是 camelCase 还是 snake_case？Kiota 生成层
  （`Edge.cs` 反序列化键 `cost`/`snode`/`enode`/`isBackEdge`/`limitV`/`limitW`）能否直接反序列化，
  还是会像 `Station` 一样字段对不上？
- `Edge.cost` 的实际取值范围是多少？它与 `getRouteCostsBy` 返回的 `costs`（明确「单位mm」）
  是否同量纲？
- 站点只有 `edge_id`（挂在边上）而没有 node 字段，一条边又挂多个站点。用 `edge_id` +
  `station_offset` 能否把站点无歧义地定位到图上，从而支持站到站最短路？
- 用边表自算的最短路，能否复现 RIoT 自己在**同一轮、同一张图**上给出的 `queryNearEnd` 选择？
- 移除边、移除站点、边组合约束在 mapId 25 上是否非空？动态路由代价当前是否为空？

## 背景与动机

`8005-agv-program` 完整产品路线图票 03 在 2026-09-03 定档时，一度依据「RIoT 查不到站到站的
路径成本」把 `REQ-0196`（执行途中受控追加）、`REQ-0198`（顺路取货按最大晚到量约束）与
`REQ-0197` 的换序半判为「门禁建好但恒拒」。用户指出边表接口存在后复核发现该前提不成立：
`Edge` 带 `snode`/`enode`/`cost`，`Station` 带 `edgeId`，原则上可自建图求最短路。

用户同时确认 **RIoT 的路径规划算法就是跑最短路**，因此自算结果与 RIoT 一致不是近似，
而是同算法同数据——前提是上面几个问题都得到肯定回答。本轮为这三条需求的形态判定取证。

`edges/{mapId}` 是实验卡 **C3**（`experiments/catalog.md:21`、`:221-235`），风险等级只读，
自 Round 1 起状态一直是「未执行」。本轮执行它。

## 环境与证据边界

**本轮目标是 8005 生产 RIoT `http://172.19.206.222:8888`，不是此前各轮的跨项目测试环境
`http://172.10.1.72:8888`。**这是本轮与 Round 1～42 最重要的差别，直接决定了对照数据的取法：

- **mapId 25（`老厂前线new`）只存在于生产 RIoT。**Round 5／15／16 在 map28／29 留下的
  `queryNearEnd` 与 `getRouteCostsBy` 观测属于**另一套 RIoT**，**不得**用作本轮的对照，
  也不得跨环境比较数值。
- 因此**本轮自造对照**：同一次执行内，先让 RIoT 自己回答若干组 `queryNearEnd`／
  `queryNearestStart`，再拉同一张图的边表，离线复现它的选择。对照与被验数据同环境、同时刻，
  没有跨轮次或跨环境的效度问题。
- 凭据从环境变量 `CONTROL_SERVER_RIOT_CALL_API_KEY` 读取（与控制服务端 `appsettings.json` 的
  `RIoT.callApiKeyEnvironmentVariable` 同源），**不写入 `environment.local.json`**——那份文件
  绑的是测试环境，本轮不改动它。证据中不保存密钥、token 或可复用凭据。
- **路由前提**：控制端的 Clash TUN 会让 `172.19.x.x` 的探测结果失真（自己应答 ICMP、
  本地完成 TCP 握手，使不存在的主机看起来可达、所有端口看起来开放）。执行前必须确认
  `Find-NetRoute -RemoteIPAddress 172.19.206.222 | Select-Object -First 1 InterfaceAlias`
  的结果**不是** `Clash`；是则先装 bypass 路由
  （`remote-ops/factory-server/scripts/01-control-host-route.ps1 -Prefix ...`）。
  脚本会在第一步自检并在命中 Clash 时直接停止。

## 批准范围

**这是生产环境，三台 AGV 正在执行真实运输任务。**本轮全部为只读查询，分两段，
第二段可以整段跳过而不影响主判定。

**段一（不涉及任何车辆）**——地图元数据与纯拓扑查询：

- `GET` imap 的边表、站点、移除边、移除站点、边组合。
- `POST /api/task/v1/route/queryNearEnd`、`queryNearestStart`：方法是 POST 但**语义只读**，
  入参只有 `mapId` 与站点 id，**不接受车辆参数**，Round 15 已在测试环境验证无副作用。
- `GET /api/task/v1/route/`、`getCostUnit`：动态代价只读。

**段二（机会性，涉及一台车的 key）**——`POST getRouteCostsBy` 的量纲对照：

- 只在**车辆当前不在执行订单**且**停在 mapId 25 的某个已知站点**时采集，且**只传一台车的
  deviceKey**。该接口在 Round 15／16／41 多次执行且未观察到副作用。
- 车在执行订单、不在该图、或不在站上，则整段跳过，主判定不受影响
  （量纲改判为「本轮未证明」）。

**明令不做**：不建单、不取消订单、不移动任何车辆、不改变车辆启用或急停状态、不编辑或删除
地图与站点、不清除动态路由代价（两个 `DELETE .../dynamicRouteCost*` 仍属未测且本轮不测）、
不为凑对照数据干预任何车辆。

## 步骤

1. 路由自检（非 Clash）与 build 记录，确认目标环境身份。
2. `GET /api/imap/v1/mapInfo/edges/25` —— 本轮主目标，保存**未经解析的原始 body**，
   以便离线判断线格式。
3. `GET /api/imap/v1/mapInfo/stations/25` —— 同期站点快照，同样保存原始 body。
4. `GET /api/imap/v1/mapResource/removedEdge/25`、`removedEdgeDetail/25`、`removedStation/25`。
5. `GET /api/imap/v1/mapEdgeGroup/all` —— 确认外层 key 的实际含义，以及 mapId 25 是否有条目。
6. `GET /api/task/v1/route/`、`GET /api/task/v1/route/getCostUnit`。
7. **自造对照集**：从第 3 步的真实站点里取若干组，跑 `queryNearEnd` 与 `queryNearestStart`，
   记录 RIoT 的每一组选择。组合由脚本按确定性规则从站点表生成并写入证据，不预先硬编码
   ——因为 mapId 25 的站点 id 集合本轮之前未知。
8. 段二机会性量纲对照（见批准范围）。

## 判定门槛

本轮**只采证据，不在脚本内做图算法**。最短路复现是离线分析。

- **线格式**：原始 body 的键名若为 snake_case（`is_back_edge`／`limit_v`／`snode`），
  则 Kiota 生成层**不可直接使用**，须自定义反序列化——这是一个确定的工程结论，不是失败。
  判据是站点接口的已知事实：测试环境实测返回 `edge_id`／`station_offset`／`enter_pos.x`，
  而 `Station.cs:122-149` 的键是 `edgeId`／`stationOffset`／`enterPosX`。
- **站点定位**：若 `station_offset` 的语义无法从数据自证（例如同边多站的 offset 全为 0），
  则站到站自算**当前不可行**，如实记录，不猜测语义。
- **算法一致性**：第 7 步的每一组 `queryNearEnd`／`queryNearestStart`，自算最短路必须
  复现 RIoT 的同一选择。**全中**判为一致；**任一组不中**即判为不一致，并记录不中的那组，
  不做「大体一致」这类表述。对照组数量不足 5 组时，判定降级为「初步一致，样本不足」。
- **量纲**：仅当段二采到数据时判定。自算的「车所在站→目标站」代价与实采 `costs` 同量级
  且误差可解释，判为同量纲；数量级不符则判为不同量纲，且**不得**再把 `Edge.cost` 与
  `getRouteCostsBy` 的结果混用。段二跳过则记为「本轮未证明」，**不得**用另一套 RIoT 的
  Round 16 数据替代。
- 任何一项数据缺失、接口失败或结果自相矛盾，一律 fail-closed 记为未证明，
  不沿用其它轮次或其它环境的观测冒充本轮结论。

## 停止条件

- 路由自检命中 Clash TUN：立即停止，不做任何请求。
- baseUrl 与预期不符：立即停止，不做任何请求。
- 连续 3 次请求失败：停止后续步骤，保留已采证据。
- 段二发现车辆正在执行订单：跳过整段，不等待、不干预。
- 若发现任何请求产生了副作用（车辆状态、订单、地图发生变化）：立即停止，
  按 `README.md` §6 走人工干预流程，完整记入 `execution-log.md`。

## 产出

- `runs/` 下每个请求一份记录，含原始 body。
- `execution-log.md` 记录实际执行的请求、返回摘要与判定结果。
- 结论若成立，写入 `knowledge/behavioral-contracts.md` 新契约 **BC-MAP-003**，
  并回填 `experiments/catalog.md` 的 C3 状态。
- 判定结果回填 `8005-agv-program/.scratch/8005-full-product/issues/03-answer.md` 的 Q12，
  据以确定 `REQ-0196`／`REQ-0198`／`REQ-0197` 换序半的最终形态。
