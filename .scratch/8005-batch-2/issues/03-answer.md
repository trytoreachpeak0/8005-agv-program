# 票 03 决议：假 RIoT 扩到能承载四条能力轨，合成车载端支持三实例

Resolved: 2026-09-07
Resolves: `03-fake-riot-capability-surface.md`

## 结论一句话

四项全部落地：**五个 `imap` 只读端点**（形状照 Round 43 逐字复现）、**订单命令面**（只记录、
不模拟后果）、**多车种子**、**合成车载端三实例**。

证据：**L1 334 passed / 0 failed**（新增 9 条，**用真 SDK 打假 RIoT**）；**L2 四条合成场景
全 PASS**，含新增的 `three-synthetic-peers`。

## 四项各自的落地

### 一、五个 `imap` 只读端点

`mapInfo/stations/{mapId}` **原本就有**，只返回 `{id, name}`；这次把它补成真实 RIoT 的完整
一行（加 `edge_id`、`pos.x`／`pos.y`／`pos.yaw`、`station_offset`、`type`、`desc`、
`user_define_properties`）。旧的目录 Facade 只读 `id`／`name`，加字段不影响它——有一条测试
专门盯这点。另外四个是新增，落在新文件 `tools/ControlServer.FakeRiot/RiotRouteGraphPlane.cs`。

**四处怪癖一处不改**（票据只列了三处，第四处是票 07 补的）：`edges` 是 snake_case 且
`s_node`／`e_node`；`stations` 的位置键字面带点；`mapEdgeGroup/all` 是 camelCase、以组名为键
的对象；它的时间戳不是 ISO 8601。

**`removedEdgeDetail` 故意不实现。**`CP-0001` 明确不批它，产品代码伸手过去应该在这里就 404，
而不是悄悄能用。有一条测试盯着这个 404。

### 二、订单命令面

**六个命令实际只需两条路由**——这是读 SDK 实现才看清的，票据按"六个端点"写：

| 路由 | 覆盖 |
| --- | --- |
| `POST /api/task/v1/order/command/{orderId}` | `CMD_ORDER_CANCEL`／`CMD_ORDER_HELD`／`CMD_ORDER_CONTINUE_FROM_HELD`／`CMD_ORDER_CONTINUE_FROM_HANG`，靠 body 的 `commandType` 区分 |
| `POST /api/device/v1/command/sync/service/{deviceKey}/{serviceId}` | `triggerEmergency`／`cancelEmergency`，靠路径段区分 |

**只记录调用，不模拟业务后果**——`OrderHold` 不会把订单挪到 `HELD`。这是规格的定案，也是对
的：控制服务端的对账必须靠读回终态来确认，一个替你把后果做掉的替身，会让一个从不对账的服务
端也过关。

记录是每次调用一行（命令类型、目标、逐字参数、时刻），进控制面 `snapshot` 的
`commandInvocations`。有一条测试连发两次 `OrderHold` 并断言拿到**两行**——「调了一次还是两次」
因此是可判定的，不是靠信任。

急停那条还复现了真实服务的一个坑：**body 缺 `thingsProperties` 时返回 `00002` ＋
`java.lang.NullPointerException`**，不是结构化错误。少传的调用方在这里就得挨打。

### 三、多车种子

`AdditionalVehicleKeys` 默认空，所以**既有场景面对的仍是原来那支单车队**。测试里配三台，三台
各答各的身份、各自 IDLE。

**与 `remote-ops/fleet.md` 不矛盾**：种子用的是测试用 key（`BROKERX-TEST-000N`），不冒充任何
真车的 `deviceKey`，所以谈不上与车队登记册冲突。真车身份进 L2 是票 18 的事。

### 四、合成车载端三实例

`FakeOnboard` 本来就是"一进程一台车"，缺的是编排器：它把端口、`instanceId`、`agvId` 全写死
了。现在按 setup 的 `OnboardPeers` 起 N 个进程，**默认一个，且第一个的端口与 `instanceId`
保持原值**，既有场景的证据布局一字未变。

新场景 `three-synthetic-peers` 把三台都拉起来，断言三个进程、三个端口、三个各报各的 `agvId`。
合成车载端的 `snapshot` 因此新增了 `agvId` 字段——没有它，一个进程替另一个回答是看不出来的。

**进程隔离不是省事**：会话不串如果靠一个进程里三份状态互相不踩，证的是那份代码记得分开；三个
进程各连各的，不串是结构上的。

## 跑起来才发现的两件事

### 一、服务端一次只服务一条车载连接

三台车拉起来之后，第二台停在 `DISCONNECTED`。根因在
`src/ControlServer.Host/Transport/OnboardTcpServer.cs`：

```csharp
while (!stoppingToken.IsCancellationRequested)
{
    using TcpClient client = await listener.AcceptTcpClientAsync(stoppingToken)...;
    await HandleClientAsync(client, stoppingToken)...;   // 同步等待，处理完才接下一个
}
```

**accept 循环是串行的**，所以同一时刻只有一台车的会话是活的，其余排队。

**这不是本票的 bug，是票 09 第 1 项要换掉的单车传输层**（票 09 原话：「`OnboardPeer.Attach`
的 N 会话——同时持有多台车的会话，会话之间不串」）。本票因此把验收拆成两半：合成侧三实例已
证；服务端同时持有三条会话留给票 09。

场景里写了一条断言**钉住当前边界**（`L2-3P-06`：服务端此刻只有第一台车的会话行）。票 09 做完
它会变红，而**它红得对**——那是在提醒边界移动了，改掉即可。

### 二、PowerShell 的单元素数组会被 `if` 表达式的管道展开

改完编排器，**三 peer 场景过了，三条既有的单 peer 场景全红**，报
`You cannot call a method on a null-valued expression`。

```powershell
# 错的
$peerSpecs = if ($cond) { @($setup.OnboardPeers) } else { @(@{ AgvId = $agvId }) }
# 对的
$peerSpecs = @(if ($cond) { $setup.OnboardPeers } else { @{ AgvId = $agvId } })
```

`if` 块的输出走管道，**单元素数组被展开成那个 Hashtable 本身**。`$peerSpecs.Count` 恰好也是
1（Hashtable 的键数），循环照跑一轮，`$peerSpecs[0]` 却是按键 `0` 查表 → `null`。三元素的那
条不会被展开，所以偏偏是它过了。

**编排器的 `catch` 现在记 `ScriptStackTrace`**，就是这次为定位它加的：没有行号，这种错要靠
二分找。

## 验收清单

- [x] 五个 `imap` 端点在假 RIoT 上可用，返回形状与真实 RIoT 的键名约定一致
      （用真 SDK 的五个具名 Facade 打过，不是自说自话）
- [x] 六个订单命令端点可用，每次调用被记录（时刻、参数、次数），且不改变假 RIoT 的车辆或
      订单业务状态
- [x] 调用记录可从 L2 场景断言，能区分「调了两次」与「调了一次」
- [x] 假 RIoT 能同时呈现三台车，车辆身份与 `remote-ops/fleet.md` 的映射不矛盾（用测试用 key，
      不冒充真车）
- [~] `FakeOnboard` 三实例可同时建立会话并各自推进，会话之间不串
      —— **合成侧已证**（三进程、三端口、三身份，互不冒充）；**服务端同时持有三条会话做不到**，
      accept 循环串行，属票 09
- [x] 既有 L2 场景全部回归通过，合成装置的旧行为一字未变
      （`normal-load`、`session-established-while-moving`、`load-result-requires-recovery`
      全 PASS；L1 334 passed）

## 一处边界说明

票 03 的冲突边界写着「只动 `tools/` 下的合成装置目录与 L2 装置装配，不动 `src/` 与 `tests/`
下的产品代码与产品测试」。我在 `tests/` 下**新增**了
`FakeRiotRouteGraphTests.cs`——它测的是**合成装置**（用真 SDK 打假 RIoT），不是产品，且是新
文件、没碰任何既有测试。`src/` 一行未动。

## 给下游票的指针

**票 10（命令面接入）**——两条路由已就位，`commandInvocations` 就是对账断言的读取面。注意
急停的 body 必须带 `messageId` 与 `thingsProperties`，否则假 RIoT 按真实服务的样子返回
`00002` ＋ NPE。

**票 12（引擎）**——默认种子给了一张 6 节点 8 边的有向图（只有两条边有反向），三个站点分别
落在 node 1／3／5，站点坐标与节点坐标完全相同，所以坐标投影的残差是 0。真实 map25 的最大残差
是 4 mm，所以这里是简化，不是另一套规则。移除集与边组默认空——**那正是 map25 的真实状态**。

**票 09（B2 多车）**——编排器的 `OnboardPeers` 已经能起三台；服务端那道串行 accept 是你要改
的第一样东西。改完把 `three-synthetic-peers` 的 `L2-3P-06` 换成"三行会话"，并把两个
`WaitForReady = $false` 去掉。

## 遗留

- 改动只提交在本地 worktree（`03fb252`），未推送。
