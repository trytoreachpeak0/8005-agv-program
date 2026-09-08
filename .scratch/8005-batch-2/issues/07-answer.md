# 票 07 决议：五个 `imap` 具名 Facade 已交付，SDK 发 `0.2.0-fp.2`，服务端已升包

Resolved: 2026-09-07
Resolves: `07-riot-sdk-imap-facade-and-release.md`

## 结论一句话

**三步走完**：`riot-sdk` 新增五个具名 Facade（C# ＋ Python 双端）→ 发 `0.2.0-fp.2` →
`8005-agv-control-server` 升 vendored 包。**票 12（引擎）现在可以直接消费具名 Facade 取路网，
不必碰 `.Raw`。**

三处证据：SDK 侧 **C# 92 passed / Python 88 passed ＋ 1 skipped**；服务端 **L1 308 passed /
0 failed**，其中 `RiotSdkPackageProvenanceTests` 3 条按新版本号重新绑定后仍绿；服务端 `src/`
下 `.Raw` **零命中**（全仓也是零）。

## 交付内容

### 一、五个具名 Facade

| C# | Python | 端点 |
| --- | --- | --- |
| `ListEdgesAsync` | `list_edges` | `GET /api/imap/v1/mapInfo/edges/{mapId}` |
| `ListStationDetailsAsync` | `list_station_details` | `GET /api/imap/v1/mapInfo/stations/{mapId}` |
| `ListRemovedEdgesAsync` | `list_removed_edges` | `GET /api/imap/v1/mapResource/removedEdge/{mapId}` |
| `ListRemovedStationsAsync` | `list_removed_stations` | `GET /api/imap/v1/mapResource/removedStation/{mapId}` |
| `ListEdgeGroupsAsync` | `list_edge_groups` | `GET /api/imap/v1/mapEdgeGroup/all` |

`removedEdgeDetail` 未实现，`CP-0001` 明确不批。

领域类型在 `RIoT.Sdk.Core`／`riot_sdk.core.route_graph`：`MapEdge`、`MapStationDetail`、
`RemovedEdge`、`RemovedStation`、`MapEdgeGroup`。**线格式不外溢**——产品代码看到的全是具名
领域类型。

**与票据的一处偏离：`stations/{mapId}` 早就有 Facade 了。**既有的 `ListStationsAsync` 走
Kiota 生成模型，只能拿到 `id` 与 `name`（这两个键恰好不带下划线所以对得上），**拿不到
`edge_id` 与 `pos.x`**——而那正是引擎做站点到节点定位所必需的。所以新增的是
`ListStationDetailsAsync`，旧方法一字未动，两者并存。

### 二、反序列化：票据说三处怪癖，实测是四处

前三处票据已列（snake_case、`s_node`／`e_node`、站点侧键名字面带点），**第四处票据没记，补在
这里**：`mapEdgeGroup/all` 的 result 是 `map<组名, list>` 而不是数组，且**该端点用 camelCase**
（与同一服务的 `edges`／`stations` 相反），时间戳 `"2024-06-26 10:57:58"` **不是 ISO 8601**。

这一处决定了实现路线。改 `specs/imap.json` 让 Kiota 生成正确键名能解决前三处，**解决不了第四
处**——Kiota 为那个 map 外层生成的 result 类是个只有 `AdditionalData` 的空壳，`gmtCreate` 用
`GetDateTimeOffsetValue()` 解析那个格式会失败。而改 `specs/` 是双端共享契约，会把两端生成层
一起卷进来，范围反而更大。

落地形态：**URL 与鉴权仍走生成层**（`ToGetRequestInformation()` ＋
`SendPrimitiveAsync<Stream>`），只有 body 解析是手写的。决定、代价与未实测项写进
`ADR-sdk-0009`，索引已更新。

**代价如实记**：线格式的知识现在有两处——`specs/imap.json`（spec 的说法）与五个 reader（现场
的说法），两者不一致且不会自动对齐。RIoT 升级改了键名时编译不失败、测试不变红，除非有人重跑
一轮 Round 43 式的实采。三条缓解：必需字段 **fail-closed**（读不到就抛，不静默返回空图或跳过
元素——静默会让调用方在一张缺边的图上派车）；两种拼写都接受；**测试夹具是 Round 43 的逐字响
应体**，不是手编样例。

### 三、测试

C# `RouteGraphFacadeTests` 与 Python `test_route_graph_facade.py` 同构，各 14 条：四处怪癖各有
覆盖、三条 fail-closed、边界（空数组／空对象／业务失败码），外加一条 **URL 断言**。

**URL 那条是补上的一个真实盲区**：这五个方法绕过生成模型手工路由，而夹具 handler 对任何路径
都返回同一个 body——URL 拼错不会有任何症状。加上断言后立刻抓到一个我自己的错（`mapEdgeGroup`
的空结果形态判定过严），也顺带证明了五个 URL 与 `REQ-0146` 批准的清单逐字一致。

## 中途撞上的事：SDK 主线与生产包分叉（用户批准扩大范围）

**升包时编译失败在 `OrderSnapshot` 找不到**，与本票改动无关。查下来：

`0.1.0-controlserver.2` 是从旧仓库 `8005---AGV` 的分支
`codex/riot-sdk-controlserver-integration`（commit `e708f874`）打的，**那个分支从未合回 SDK
主线**——`riot-sdk` 建仓以来 14 个 commit 的全历史里搜不到 `OrderSnapshot`。也就是说
**riot-sdk 的源码此前打不出 control-server 正在消费的那个包**，只是没人重新打过包，所以从未
暴露。

缺的 12 个 API，control-server **全部在用**，没有只搬一半的空间。**用户 2026-09-07 批准在本票
内双端补齐**：

- `RIoT.Sdk.Core`：`OrderSnapshots.cs`、`OrderStatePage.cs`、`VehicleFacts.cs`
- Facade：`FindOrderByUpperIdAsync`、`ListOrdersByStatesAsync`、`GetVehicleCardAsync`、
  `GetVehicleExecutionFactsAsync`、`ListStationsStrictAsync`
- 另带 `RiotSession` 的自有 no-retry `HttpClient` 与 `SendRawAsync`、`RiotAuthClient` 的
  no-redirect 传输与取消／超时区分
- 八个测试文件（三个新增，五个是主线版的严格超集，例如 `GetOrderByUpperIdFacadeTests` 从
  1 个 `[Fact]` 变 13 个）

搬运是干净的：**生成层源文件与 `specs/imap.json` 的哈希都逐字一致**，差异只在手写层。

**`csproj` 一律没动，这一条是有意的。**备份版的 csproj 硬编码 `TargetFramework`、
`LangVersion=latest`、内联 `Version=`、指向旧仓库 URL，`Tests.csproj` 还用
**xunit 2.5.3 ＋ coverlet.collector**——那些正是工作区工具链基线（`ADR-cross-0056`）明令禁止
的，`Directory.Build.targets` 会以 `W2G0056` 让构建失败。照搬会当场炸。

## 两件顺带发现

### 一、Python 的 `base_url` 缺陷，随搬运自动修好了

`HttpxRequestAdapter.__init__` 接受 `base_url` 参数但第 90 行只从 httpx client 读，传进去的值
被丢弃。生产路径 `RiotSession(options)` 不传 client 时，`RiotOptions.base_url` 对**所有**生成
客户端失效，请求会落到 OpenAPI 描述里硬编码的 `172.19.206.222:8888`——那恰好就是生产 RIoT 地
址，所以从没暴露过。

发现时以为是独立缺陷，用户也决定「只记录不改」。**结果它是同一个分叉的一部分**：备份版的
`session.py` 早就修了（`self._adapter.base_url = options.base_url.rstrip("/")`，还带一段解释注
释），只是没合回主线。搬运把修复一并带回，两端的 URL 断言因此都恢复成了完整 URL 而不只是路径。

### 二、map25 一个边组都没有

`mapEdgeGroup/all` 在生产 RIoT 上非空，但**全部属于别的 Map**（9／14／19／22），8005 的作业地
图 map25 一条都没有。而且**一个组名可以跨多个 Map**（「老厂电梯」同时在 map14 与 map19），所以
`(GroupName, MapId)` 才是标识，领域类型两者都带。

**这对票 12 有直接影响**：规格 5.6 说「`mapEdgeGroup` 指纹变化即进陈旧态」，而 map25 的指纹当
前是**空集**——陈旧判定必须能处理「从空到非空」，不能把空集当作「还没取到」。按用户决定，这条
只记录在此，未改票 12 的票据正文。

## 一个教训：版本号被污染就作废，别复用

`0.2.0-fp.1` 我打过两次，内容不同（第二次在主线补齐之后）。第二次打完构建**仍然**报
`OrderSnapshot` 找不到——因为第一份 `fp.1` 已经进了本机 NuGet 全局包缓存，`restore` 不会重新
解压同名同版本的包。

包目录 README 里那句 "Do not replace a package while retaining this version" 不是形式主义，它
防的就是这个。作废该号改用 `0.2.0-fp.2`，并清掉了缓存里被污染的 `fp.1`。

**版本号选 `0.2.0-fp.*` 而不是 `0.1.0-controlserver.3`**：minor 位表示新增公开 API，后缀换成
`fp` 是为了让它不被误读成 MVP 线那条序列的下一版——MVP 线仍钉在 `0.1.0-controlserver.2`，两条
线的 feed 目录并存，旧目录按 immutable 约定保留不删。

## 验收清单

- [x] 五个方法在 Facade 层有具名实现，返回领域类型而非生成客户端的原始 DTO
- [x] 反序列化的怪癖在 SDK 内部处理，每处有测试覆盖（**四处，不是三处**，见上）
- [x] 五个方法各有 Facade 测试，与既有 Facade 测试同形态（并补了一条 URL 断言）
- [x] SDK 发一版，版本号可被 `Directory.Packages.props` 精确引用（`0.2.0-fp.2`）
- [x] `8005-agv-control-server` 的 vendored 包升到新版，`RiotSdkPackageProvenanceTests` 仍绿
- [x] 服务端 `src/` 下 `.Raw` 仍是零命中，本票未引入首个命中
- [ ] **假 RIoT 侧（票 03）的五个端点与真 SDK 的调用形状对得上，L2 可用**——票 03 未开工，
      这条现在只完成了一半：真 SDK 的调用形状已由 URL 断言逐字固定（见下方给票 03 的指针），
      对不对得上要等票 03 做完才能验。

## 给下游票的指针

**票 03（假 RIoT 扩能力面）**——五个端点的调用形状已固定，照这个实现即可：

```
GET /api/imap/v1/mapInfo/edges/{mapId}
GET /api/imap/v1/mapInfo/stations/{mapId}
GET /api/imap/v1/mapResource/removedEdge/{mapId}
GET /api/imap/v1/mapResource/removedStation/{mapId}
GET /api/imap/v1/mapEdgeGroup/all
```

返回形状**直接抄 Round 43 的逐字响应体**，路径
`repos/8005-agv-program/rcs/riot-behavior-lab/evidence/rounds/2026-09-03-round-43/runs/`
的 `003`／`004`／`005`／`007`／`008`。C# 测试
`csharp/RIoT.Sdk.Tests/RouteGraphFacadeTests.cs` 里已经把它们裁剪成了可直接复用的夹具常量。
**注意四处怪癖必须原样复现**，否则假 RIoT 与真 SDK 对不上：`edges` 用 snake_case 且是
`s_node`／`e_node`，`stations` 的键名带点，`mapEdgeGroup/all` 用 camelCase ＋ 组名为键的对象
＋ 非 ISO 时间戳。

**票 12（引擎）**——`ADR-sdk-0009` 记了两件它需要知道的事：`removedEdge`／`removedStation` 的
非空形态**从未实测**（map25 一直是空），以及 `MapEdge.CostMm` 与 `getRouteCostsBy` 的
`costs` 同量纲**是推断不是实测**（Round 43 没在同一对起终点上同时取过两者）。引用时按规格
8.8 的表述规则处理，别写成已证实。

## 遗留

- **`ValidateRepositoryCommitForPack` 这个 MSBuild target 没搬。**备份版的 csproj 里有它（打包
  时缺 `RepositoryCommit` 就报错），是个防止打出无 provenance 包的好守卫，但它裹在那份不能照
  搬的 csproj 里。本次打包手工传了 commit 并逐个核对了 nuspec，所以不阻塞——想要这个守卫的话
  另开一张票，按当前基线的写法重写。
- **`riot-sdk` 与 `8005-agv-control-server` 都只提交在本地 worktree，未推送。**
