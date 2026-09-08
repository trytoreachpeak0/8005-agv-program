# 票 02 决议：白名单成了产品文档，26 个端点逐条可判定，三处缺口如实登记

Resolved: 2026-09-08
Resolves: `02-riot-call-whitelist-as-product-doc.md`

## 结论一句话

**`8005-agv-program/docs/riot-call-allowlist.md`**（commit `3bc055c4`，分支 `fp/batch-2`），
26 个获批端点逐条列出 HTTP 方法 ＋ 路径 ＋ 基线载体 ＋ 具名 Facade ＋ 服务端当前是否在用。

它是**汇编，不是新授权**——规范内容全部来自已批准的基线条目，文档比基线宽的地方是错误而不是
扩权。这一句是整份文档的定位，也是下面所有决定的依据。

| 项 | 值 |
| --- | --- |
| 路径 | `docs/riot-call-allowlist.md` |
| git blob SHA-256 | `dec0bc1046f3f7c969ca53bd332708fe4668ded5370aa308c584305222d7bcee` |
| 批准人／维护者 | Zhengyu Shao |
| 依据基线 | `v1.1.0`（`5fe4b701…fb53`） |
| 获批端点 | 26（实测解析，第二节「明确不批」零误匹配） |
| 服务端当前实际调用 | 12 个端点、13 个 Facade 方法，**全部 ⊆ 清单**；`src/` 下 `.Raw` 零命中 |

## 先回答交接文档留的那个问题

**「预留五个 `imap` 端点的位置，增列归票 07」这条分工已经落空，票 02 直接写进清单。**

分工的前提是波次顺序（P 波票 02 → Q 波票 07）。实际执行顺序反了：票 07 在 2026-09-07 先完成，
当时白名单文档还不存在，它没有可增列的地方，也确实没增列。而票 04 落地基线时，
**`REQ-0146` 的正文已经含了那五个端点**（v1.1.0 实测确认）。

所以现在的状态是：基线已经含、Facade 已经有、引擎已经在调，唯独没有文档。「留位置」这个动作
没有对象。**照基线抄进清单是唯一正确的写法**——留个空位反而会让票 08 的架构测试一上来就红，
而那五个端点是有需求依据且已批准的。

## 落在哪，为什么在那

| 候选 | 否决理由 |
| --- | --- |
| `docs/adr/cross/00XX-*.md` | ADR 是决策记录，写完就不动；白名单要持续维护 |
| `requirements/` 下 | 那里是批准过的不可变基线与提案归档，汇编不属于 |
| **`docs/riot-call-allowlist.md`** | ✅ 与 `collaboration-workflow.md`、`wire-to-gate-test-automation.md` 并列——都是持续维护的规范文档 |

命名遵循工作区 `file-naming-convention/`（lowercase kebab-case）。

**写在 `8005-fp/8005-agv-program`（`fp/batch-2`）这个 worktree**，不动禁区里的
`repos/8005-agv-program/`。这条路径是票 04 建的，用户 2026-09-07 明示批准。

## 自行定案的五件事

### 一、票据 37 不加指针，也不改一个字

票据验收第 6 条要求「原工作票据里的白名单副本留下指针指向新位置」。**没做，这是与票据的一处
明确偏离**，理由是硬的：

票据 37 被 `REQ-0146`／`REQ-0147`／`REQ-0148`／`REQ-0149` 四条的 Evidence 段落按
`Snapshot SHA-256 = 205a1c4bd5760e3f5a50de3eec050d5d8e99eec4ab74a789e005c22bf4a9c664` 绑定。
**实测吻合**：

```bash
git show HEAD:.scratch/current-requirements-baseline/issues/37-*.md | sha256sum
# 205a1c4bd5760e3f5a50de3eec050d5d8e99eec4ab74a789e005c22bf4a9c664
```

加一行指针就让四条基线条目的证据指纹全部失效，那是一次要走变更提案流程的动作，代价与收益完全
不成比例。

**而验收条目的意图已经达成，只是达成方式不同。**「不留第二份**可编辑**的真相」担心的是有人去
改票据 37 里的白名单副本。事实是它**已经不可编辑**了——哈希绑定就是那把锁，改了会被基线校验
抓到。这一点以前没人写下来，现在写在新文档的「规范层级」一节里，并明确了三层顺序：
需求基线 > 本文档 > 票据 37（冻结证据）。

指针放在了**可编辑的地方**：`CONTEXT.md` 的鉴权节（不被基线哈希绑定，实测 0 处引用）。

### 二、开放引用展开成六条，展开即封闭

`REQ-0146` 那句「具体包括**当前 Facade 使用的地图/车辆/订单查询**」是规格点名的病灶。展开成：

```
GET /api/imap/v1/mapInfo/getALLMapInfoExcludeMapJson    ListMapsAsync
GET /api/task/vehicles/getAllVehicleSimpleInfo          GetDispatchableVehiclesAsync
GET /api/task/vehicles/getVehicleInfoByDeviceKey        GetVehicleCardAsync
GET /api/order/v1/orderRecord/detailByUpperId/{upperId} GetOrderByUpperIdAsync / FindOrderByUpperIdAsync
GET /api/order/v1/orderRecord/detailByOrderId/{orderId} GetOrderByOrderIdAsync
GET /api/order/v1/orderRecord                           ListOrdersByStatesAsync
```

**这一步是全文唯一可能被读成扩权的地方**，所以证据必须硬：

- **时点锚定 2026-08-24**（基线 `v1.0.0` 批准日）。反射
  `vendor/nuget/riot-sdk/0.1.0-controlserver.2/RIoT.Sdk.Facade.dll` 的元数据，**恰好 38 个
  `*Async` 方法**——与规格 9.2 写的「38 个」逐字吻合，证明它就是批准时点的那一份。上面六条全在
  其中，**没有一条是后加的**。
- **按类别收窄，不按「Facade 里所有查询」。**那句话的三个词是「地图／车辆／订单」，所以
  `ListDevicesAsync`（`GET /api/device/v1/devices`）与 `GetDeviceStatusStatisticsAsync` 被排除
  ——`CONTEXT.md` 的 `ObservationAndComputationCall` 词条明写「设备全量清单、日志、配置、原始物
  模型和管理查询不属于本层」。**Facade 里有它们，白名单不批它们**，这条差异本身就说明「在
  Facade 里」从来不是授权依据。
- **展开之后那句引用作废。**将来新增的 Facade 查询方法不因为「在 Facade 里」而获批。

### 三、急停端点没有基线载体，如实登记而不是补授权

`POST /api/device/v1/command/sync/service/{deviceKey}/{serviceId}` 只在票据 37 里有。基线的
`REQ-0246`／`REQ-0248` 只写动作名 `triggerEmergency`／`cancelEmergency`，**不写路径**——全基线
搜 `api/device/v1/command/sync/service` 零命中。

**这是白名单里唯一一条没有基线载体的获批调用，而它是后果最重的那一条。**

处置：写进文档第三节，建议下一次变更提案补进基线。**汇编不能代替那个动作**——如果文档自己给它
一个载体，那就正好犯了「文档比基线宽」的错。

### 四、还查出两处缺口，一并登记

- **`REQ-0168` 指定的端点不在票据 37 的封闭清单里。**基线写着「用户指定
  `GET /api/task/vehicles/queryVehicleNotAssignOrder/{deviceKey}/{orderKey}` 作为长期 `QUEUEING`
  原因诊断」，而票据 37 说「白名单到此封闭」。读法应是「更晚的、用户指定的补充」，但
  **文档不替基线做这个判断**——它没进第一节的清单，所以产品代码现在调用它就是越界，票 08 会因
  此变红，那是应有的行为。要用它，走变更流程显式加进去。
- **五个获批端点没有 Facade 实现**：`GET /api/version/v1/infos`、
  `GET /api/task/v1/route/curRemainCost/{orderKey}`、`GET /api/task/v1/route/getCostUnit`、
  `POST /api/task/v1/order/route/{vehicleKey}`，加上上面那个诊断端点。**获批不等于已实现**，
  要用先加具名 Facade，不是用 `.Raw` 绕。

### 五、清单的机器可读形态：表格本身，不另建数据文件

票 08 要「清单从票 02 的产品文档取得，测试里不出现第二份手抄清单」。做法是**把表格行格式定成
契约**，写进文档第四节：

- 获批行 = 表格行且**第一格恰好是一个 HTTP 方法**，第二格是反引号包裹的路径
- 「明确不批」表的第一格是自由文本（`DELETE /api/…` 连写或一句描述），因此不会混淆
- `{…}` 按占位符匹配；`?` 之后的查询串不算路径

**实测过**：第一节解析出 26 条，第二节误匹配 0 条。

否掉了「单独出一个 `.json`／`.tsv` 数据文件」——那就是两份真相，而人读的表格与机器读的文件不
一致时没有任何机制会发现。

## 撞到的三个坑

### `.Raw` 的朴素 grep 会误报

`src/` 下 `.Raw` 有 **3 处文本命中，全部是注释**——`RouteGraphPorts.cs:17`、
`HttpRiotRouteCostProbe.cs:14`、`HttpRouteGraphSource.cs:13`，三处都在说「不要用它」。票 07 决议
说的「零命中」指的是零调用，那是对的；但**票 08 若照着文本 grep 写断言，一上来就是三条假红**。
判定必须在语法层面做（Roslyn 语法树，或至少剥掉注释）。已写进文档第四节。

### `riot-sdk` 主线的历史查不出方法的引入时点

想核实 `GetVehicleCardAsync` 等是不是 2026-08-24 就存在，`git log -S` 只查到 2026-09-07 的
`e9b7411`「把 controlserver 集成分支的 12 个 API 合回主线」——因为那些方法此前只活在一个从未合
回主线的分支上（交接文档记过这件事）。

**时点证据只能从 vendored 包里取**：反射
`vendor/nuget/riot-sdk/0.1.0-controlserver.2/` 的 DLL 元数据。`Assembly.LoadFrom` 会因为依赖缺
失抛 `ReflectionTypeLoadException`，改成直接读 DLL 字节、正则抓元数据字符串堆里的
`[A-Z][A-Za-z0-9]{3,60}Async`，得到干净的 38 个。

### 基线里带具体端点的条目只有六条

想找「白名单的全部基线载体」时，第一反应是搜 Source 指向票据 37 的条目（得到 `REQ-0146`～
`0149` 四条）。但那不完整也不精确——真正该搜的是**基线正文里出现 `/api/` 的条目**，结果是六条：
上面四条加 `REQ-0078`（MesIngest，与 RIoT 无关）与 `REQ-0168`。第四节那个缺口就是这么查出来的。

## 验收对账

| 票据条目 | 结果 |
| --- | --- |
| 落在正式文档路径下，有明确维护者 | ✅ `docs/riot-call-allowlist.md`，维护者与批准人写在头部表格 |
| 清单逐条可判定，不留开放引用 | ✅ 26 条，每条 HTTP 方法 ＋ 路径；那句「当前 Facade 使用的…」已展开并作废 |
| 补上充电订单形态 `move + act(78,1)` | ✅ 与运输形态并列成表，带 Round 24 实测出处；并记下 `CreateMoveOrderAsync` 建不出它 |
| 写明必须走具名 Facade、不得 `.Raw`，载体是 `REQ-0309` | ✅ 第二节末尾，并说明 `REQ-0309` 比票据 37 稳、引用时优先引它 |
| 与 `REQ-0294` 引用关系干净，不互指 | ✅ **文档引基线**，单向。基线一字未改（改它要走 CP） |
| 原票据留指针，不留第二份可编辑的真相 | ⚠️ **偏离**：不加指针，理由见自行定案一。目标由哈希绑定达成，指针放在 `CONTEXT.md` |
| 预留五个 `imap` 端点的位置（本票不增列） | ⚠️ **偏离**：直接写进清单。分工前提已落空，理由见开头 |

两处偏离都不是少做，是做法变了；理由都写在上面。

## 给下游票的指针

**票 08（白名单架构测试）现在可以开工，前置已解除。**它需要的五样东西都在：

1. **清单来源**：`docs/riot-call-allowlist.md` 第一节，解析约定在第四节，实测可解析。
2. **当前基准**：12 个实际调用端点全部 ⊆ 清单，`.Raw` 零调用。**测试写完第一次就该是绿的。**
3. **`.Raw` 的判定要在语法层面做**，否则三处注释就是三条假红。
4. **跨仓取用是它要解决的问题，不是本票的。**文档在 `8005-agv-program`，测试在
   `8005-agv-control-server`，两个独立克隆；而票 08 要求测试跑在 CI 的 headless runner 上，那里
   只 checkout 一个仓，**读兄弟目录在 CI 上不成立**。推荐做法是 control-server 里 vendor 一份
   副本 ＋ 断言上面那个 SHA-256（`dec0bc10…bcee`），与 vendored SDK 包的
   `SHA256SUMS` 是同一个模式——副本不一致会立刻被发现，因此不算「第二份手抄清单」。最终形态由
   票 08 定。
5. **越界的正面样本现成**：`REQ-0168` 的 `queryVehicleNotAssignOrder` 在基线里但不在清单里，
   拿它做「人为加一个清单外端点能让测试变红」的用例，比编一个假端点真实。

**票 10（`FP-C11` RIoT 订单命令面）**：1.3 那四个 `commandType` 是它的全部授权，第五个不存在；
`PriorityExec` 在 Facade 里但**只是未来候选**，不要顺手用。

**充电建单落地时**（`FP-C1` 相关）：`CreateMoveOrderAsync` 要扩出形态二，**扩 Facade 不是改用
`.Raw`**；目标桩必须来自人工录入的名册，RIoT 侧没有任何字段能标识充电桩。

**下一次变更提案**：把急停端点补进基线是它该带上的一条。
