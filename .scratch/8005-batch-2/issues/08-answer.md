# 票 08 决议：白名单有守卫了，判定做在 IL 上，清单靠字节副本跨仓

Resolved: 2026-09-08
Resolves: `08-riot-whitelist-architecture-test.md`

## 结论一句话

**`tests/ControlServer.Tests/RiotCallAllowlistArchitectureTests.cs`**（control-server
`fp/v2-impl`，commit `d509f5b`），7 条测试，第一次写完即绿，跑在 CI 的 headless runner 上，
不需要桌面、不需要真 RIoT。

| 项 | 值 |
| --- | --- |
| 测试文件 | `tests/ControlServer.Tests/RiotCallAllowlistArchitectureTests.cs` |
| 清单副本 | `vendor/8005-agv-program/docs/riot-call-allowlist.md`（逐字节） |
| 副本 SHA-256 | `dec0bc1046f3f7c969ca53bd332708fe4668ded5370aa308c584305222d7bcee` |
| 刷新说明 | `vendor/8005-agv-program/README.md` |
| 新增测试 | 7 条 |
| 全量套件 | **395 passed / 0 failed / 0 skipped**（原 388 ＋ 7） |
| 证据 | `evidence/allowlist-guard/20260908-ticket08/` |
| trait | **无**。不挂 `IntegrationSlice`，不挂 `FP-C4` |

守卫住的当前基准，与 `docs/riot-call-allowlist.md` 第四节逐条吻合：**13 个 Facade 方法、
12 个端点，全部 ⊆ 清单第一节的 26 条；`.Raw` 零命中。**

## 自行定案：跨仓取用 = 逐字节副本 ＋ 哈希

这是票据留给本票的唯一一个决定。**采纳了票 02 的推荐做法**，理由与它给的一致，另加一条它没
说的：

- 文档在 `8005-agv-program`，测试在 `8005-agv-control-server`，两个独立克隆。CI 上
  `actions/checkout` 只取一个仓，**读兄弟目录在 headless runner 上不成立**——不是不方便，是
  那个目录根本不存在。
- 没有 submodule，也没有把文档打成包的通路。副本是清单能到达 control-server 的唯一方式。
- **哈希是它不算「第二份手抄清单」的全部依据**：手抄清单会悄悄漂移，按字节绑定的副本不会。
  副本被改一个字符，`TheVendoredAllowlistIsTheApprovedDocumentByteForByte` 立刻红。

放在 `vendor/8005-agv-program/docs/riot-call-allowlist.md`，**路径镜像上游**，这样它从哪来是
写在路径里的，不靠人记。与 vendored SDK 包同一个 `vendor/` 根，也是同一个模式。

三条随之而来的处置：

1. **哈希只钉在测试里一处**（`ApprovedAllowlistSha256`）。`README.md` 记来源提交与刷新步骤，
   **不重复哈希**——两处写同一个值就是两处会不一致。
2. **`.gitattributes` 给这个目录挂了 `-text`。**哈希按字节绑定，checkout 时的行尾转换会让摘要
   漂移。两个仓库都已有先例（program 的证据 TSV 与最终规格、control-server 的 RC 产物）。
3. **副本与上游没有自动同步，也不可能有**——CI 看不到另一个仓库。上游动了白名单就要有人跑
   `README.md` 里那四步。这是这条测试的主要维护成本，票据原文已经说了「接受它」。

哈希口径**是文件字节的 SHA-256**，与 git blob 的内容摘要一致（实测 `git show <blob> | sha256sum`
吻合），**不是**加了 `blob <len>\0` 前缀的那个 git 对象 id。交接文档里写的
「git blob SHA-256」指的就是前者，别按后者去算。

## 判定做在 IL 上，不做在源码文本上

**这是本票最重要的一个技术决定，也是把它写绿的关键。**

票 02 已经指出朴素 grep 会给三条假红（`src/` 下 `.Raw` 的三处文本命中全是注释，三处都在说
「不要用它」）。真正动手时又发现反方向的问题同样严重：Facade 的调用形态是
`riotSession.Tasks.GetRouteCostAsync(...)`，而 `session.` 这个前缀在 `src/` 下有六十多行
与 RIoT 毫无关系（`SessionGeneration`、恢复会话、连接会话）。**文本层两个方向都不可靠。**

做法是读四个产品程序集的元数据表，用 in-box 的 `System.Reflection.Metadata`：

```csharp
using PEReader image = new(file);
MetadataReader metadata = image.GetMetadataReader();
foreach (MemberReferenceHandle handle in metadata.MemberReferences) { ... }
```

**编译器发出的成员引用是一次调用，注释不是。**取 `MemberReference` 的 parent 是
`TypeReference`、且该类型的 `ResolutionScope` 解析到 `RIoT.Sdk.Facade` 或 `RIoT.Sdk.Generated`
的那些，就是产品代码对 RIoT 的全部触碰面，一条不多一条不少。

不需要新包（`System.Reflection.Metadata` 在 net8.0 共享框架里），不需要 Roslyn 语义模型，
不需要能编译一份快照。整个扫描器两个函数、约 40 行。

**扫描对象是测试输出目录里的产品程序集**（`AppContext.BaseDirectory`），不是 `src/*/bin/`
——后者要猜配置和 RID，前者由测试宿主保证就是刚构建出来的那一份。

## 两条断言的形状

### 一、`.Raw` 零命中：两条腿

```
ProductCodeReachesRiotOnlyThroughNamedFacades
```

- **腿一**：`RIoT.Sdk.Facade` 类型上名为 `get_Raw` 的成员引用。即使结果被丢弃、一个生成类型都
  没被命名，它也在。
- **腿二**：程序集引用表里出现 `RIoT.Sdk.Generated`。`.Raw` 返回的就是生成客户端，用它必然把
  那个程序集拖进引用表。

腿二不是「以防万一」，**它本身就是一条规则**：白名单第二节把「生成客户端直接调用」列为不批，
理由是重新生成 SDK 不自动扩权。

顺带查实的一件事让腿二在当前 SDK 上没有误报面：**获批清单里每一个 Facade 方法都只返回
`RIoT.Sdk.Core` 类型**；Facade 里唯一会把生成类型泄进调用方签名的公共成员，是三个 `Raw` 属性
和 `DeviceClient` 那两个被第二节明确拒批的方法（`ListDevicesAsync`、
`GetDeviceStatusStatisticsAsync`）。这条性质**没有写成断言**——它只影响「测试会不会因为错误的
理由变红」，真出事时十分钟能查明，不值得一条长期维护的断言。SDK 升级后若有获批方法开始泄漏
生成类型，症状会是腿二报一条读起来不对劲的红。

### 二、实际调用 ⊆ 获批清单：默认拒绝

```
EveryRiotCallProductCodeMakesIsOnTheAllowlist
```

`RIoT.Sdk.Facade` 上被引用的成员，凡不在放行清单里的，都必须出现在白名单第一节某一行的
Facade 列里。**放行清单只有四个，全是产品代码今天真的在用的导航成员**：`.ctor`、`get_Maps`、
`get_Order`、`get_Tasks`。

**第一版写了九个**，把 `get_Device`、`get_Options`、`get_TokenProvider`、`Dispose`、
`DisposeAsync` 也预先放了进去，理由是「将来会用到，免得平白红一次」。自审时删掉了五个：
**默认拒绝的清单里预先放行没人用的成员，等于替一个还没人想过的调用提前免检。**将来第一次用
`get_Device` 的代价是这里加一行，而那一次红正是该有人看一眼的时刻。

**`get_Raw` 永远不会进那个清单。**它和 `get_Maps` 一样是属性访问器，所以「忽略属性访问器」
这条看起来很自然的捷径，正好会放跑白名单唯一明确禁止的那个逃逸口。实验 A 里它同时触发两条
断言，就是这个设计的直接结果。

## 清单解析：十几行正则，格式即契约

按文档第四节定的解析约定，一字未改：

- 只扫第一节（`## 一、` 到下一个 `## `）。第二节「明确不批」的行第一格是自由文本，本来就不会
  混淆；限定节次是第二道保险。
- 获批行 = 第一格**恰好**是一个 HTTP 方法，第二格是反引号包裹的路径。
- 第二格取第一个反引号 token，按 `?` 截断查询串。
- 第三格抓全部反引号包裹的 `*Async` 名字，去掉 `RiotSession.` 这类类型前缀（两条鉴权行是这么
  写的）。

实测解析出 **26 条**，与文档一致。

**解析测试里的两条否定断言是承重的**：`/api/task/v1/route/dynamicRouteCost`（第二节的不批表）
和 `/api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey}`（第 3.2 节正文）都是
写在同一个文件里的真路径，**任何一条出现在解析结果里，都意味着节次边界失守、清单悄悄变宽了**。

`REQ-0168` 那个端点因此是本票用到的第二个正面样本，只是用法与交接文档设想的相反：它没有 Facade
实现（文档 3.3 已登记），产品代码**调不到它**，所以不能拿它做「加一个调用会变红」的用例；
它真正证明的是**解析器没把它当成获批**。

## 四个「人为变红」实验都真的改了产品代码

证据在 `evidence/allowlist-guard/20260908-ticket08/`，每次实验都真的改 `src/`、真的重新构建、
跑完 `git checkout --` 还原。

| 实验 | 加了什么 | 结果 |
| --- | --- | --- |
| A | `riotSession.Maps.Raw` | 2 红：`.Raw` 检查 ＋ 子集检查（`get_Raw`） |
| B | `riotSession.Order.PriorityExecAsync(...)` | **1 红**：只有子集检查，`.Raw` 检查保持绿 |
| C | `riotSession.Device.ListDevicesAsync(...)` | 2 红，且两条说的都对 |
| D | `mkdir src/ControlServer.Experiment` | 1 红：`EverySourceProjectIsInTheScannedSet` |

**实验 B 是最有说服力的一个**：它证明两条断言互不牵连，子集检查独立成立。用
`PriorityExecAsync` 而不是编一个假方法，是因为它在 Facade 里真的存在、第二节又明确写着
「只保留为未来候选」——**在 Facade 里从来不是授权依据**，这正是白名单要说的话。

**实验 D 堵的是最容易无声漏掉的口子。**扫描的四个程序集是钉死的（`ProductAssemblies`），
`src/` 下新加一个项目本来会落在全部断言之外，而绿色的跑分不会告诉任何人。
`EverySourceProjectIsInTheScannedSet` 拿目录列表与那个数组对账。

留在仓库里的两条永久无用性测试用注入集合的形式跑同样的逻辑，与邻居
`ProtocolReasonCodeArchitectureTests` 的写法一致。**`.Raw` 那条无用性测试是拿本测试程序集当
样本跑的**——文件末尾的 `RawEscapeSample` 是整个仓库里唯一一处 `.Raw`，永不被调用，存在的
意义就是让扫描器有一个真的会命中的对象。把样本写进产品代码（哪怕只是临时）本身就是违规。

## 不挂 trait，这一条按票据原文执行

项目里 186 处 `[Trait("IntegrationSlice", ...)]`，**这 7 条一个都不挂**，也不属于任何业务簇。
规格 3.3 第 8 项的理由成立：挂上 `FP-C4` 的话，`FP-C4` 一延后，整个 RIoT 调用面的守卫跟着延后。

CI 侧无需改动：`test.yml` 跑 `dotnet test` 全量，不按 trait 过滤，所以不带 trait 的测试照跑。

## 验收对账

| 票据条目 | 结果 |
| --- | --- |
| 一条架构测试断言 `src/` 下 `.Raw` 零命中，人为加一个能变红 | ✅ `ProductCodeReachesRiotOnlyThroughNamedFacades`；实验 A |
| 一条架构测试断言实际调用集合 ⊆ 获批清单，人为加一个清单外端点能变红 | ✅ `EveryRiotCallProductCodeMakesIsOnTheAllowlist`；实验 B |
| 清单从票 02 的产品文档取得，测试里不出现第二份手抄清单 | ✅ 逐字节副本 ＋ SHA-256；解析规则用文档第四节定的契约 |
| 测试在 CI 的 headless runner 上跑，不需要桌面、不需要真 RIoT | ✅ 纯读文件与读程序集元数据，无进程、无网络、无 WPF |
| 不挂任何 `IntegrationSlice` trait，也不属于任何业务簇 | ✅ |

零偏离。

## 给下游票的指针

- **票 10（`FP-C11` RIoT 订单命令面）会是第一个撞上这条守卫的票。**1.3 那四个 `commandType`
  对应的 Facade 方法（`CancelOrderAsync`／`OrderHoldAsync`／`OrderContinueAsync`／
  `HangContinueAsync`）**都已在白名单第一节里**，所以调用它们不会变红；但它们挂在
  `session.Tasks` 上，`get_Tasks` 已在放行清单里，也不会红。**`PriorityExecAsync` 会红**，
  别顺手用。
- **急停落地时**（票 19 / `W1`）：`TriggerEmergencyStopAsync`／`CancelEmergencyStopAsync` 在
  `DeviceClient` 上，**`get_Device` 目前不在放行清单里**，第一次用会红一次。那一行照加，
  不是缺陷。
- **充电建单落地时**：`CreateMoveOrderAsync` 要在 `riot-sdk` 里扩出形态二。扩 Facade 不会
  影响这条守卫（方法名不变）；改用 `.Raw` 会立刻红，那正是应有的行为。
- **白名单一旦变更**（例如把 3.1 的急停端点补进基线、或把 `REQ-0168` 的诊断端点显式加进
  1.1），刷新副本与 `ApprovedAllowlistSha256` 是同一个动作的两半，步骤在
  `vendor/8005-agv-program/README.md`。**清单收紧时可能打出真的越界**，那不是测试写错。
- **票 16（`vectorId` 测试绑定架构测试）** 与本票同形：也是横切守卫、也要跨仓取一份契约。
  这里的副本 ＋ 哈希模式可以照搬，`vendor/` 下再加一个镜像上游路径的目录即可。
