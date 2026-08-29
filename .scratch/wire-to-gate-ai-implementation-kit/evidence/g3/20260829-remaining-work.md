# 2026-08-29 剩余工作与阻断评估

配套文档：[`20260829-proven-state.md`](20260829-proven-state.md)（已证明的部分）。

本文不做乐观估计。截止已第二次顺延至 2026-08-30 17:00，范围与完成定义未变。下面逐段说明还差
什么、卡在谁那里。

> 2026-08-29 深夜更新：原文写于当日午后，彼时旅程停在 `AwaitingSublot`。此后子批录入、装货、
> 发车安全检查、`TO_GATE` 移动、关卡到站五段已在现场走通，本文按当前状态重写。

## 一句话

WIRE_TO_GATE 已在现场走通到**关卡到站、待卸货**：受理 → 建单 → 取货移动 → 到站认定 → 三条快照
确认 → 子批录入 → 装货 → 发车安全检查 → `TO_GATE` 移动 → 关卡到站。旅程停在
`AwaitingUnloadResult`。**仅剩关卡批量卸货与四事实原子完成两段未走通**，且已定位到精确原因、
修复已提交（`3d8b00c`）但尚未现场复跑。

## 已解除的阻断：快照 revision 与重连的契约冲突（2026-08-29 晚）

原判定为「当前硬阻断」的那条**定性过头了**：它真实存在，但不是第一因。实际是两个独立缺陷叠加，
且第一因在服务端。

**第一因（服务端）**：服务端把快照 payload 作为 CLR 对象一次性序列化，`DateTimeOffset` 转换器
绕过 encoder 原样写出时区的 `+`；车载端把行解析为 payload 仍是 `JsonElement` 的信封后重新
序列化，该字符必经 encoder 转义。JSON 语义相同、字节不同，而服务端的 ack 校验要求逐字节复现，
所以到站后**第一条** `SnapshotAppliedAck` 就被拒、连接被拆。对端在协议规定的类型形状下不可能
满足该要求。已用离线只读字节取证坐实（车载 ack 哈希 = 服务端 wire 把 `+` 换成六字符 unicode
转义后的哈希）。

**第二因（车载端）**：重连后同一 revision 因整信封哈希变化被拒。王昆已在
`OnboardHmi_MVP@304e6ad` 修复——同一 revision 的业务一致性改用递归规范化的 **payload**
SHA-256，`appliedContentSha256` 仍返回完整信封哈希以兼容服务端 outbox。

两处缺一不可，现已合并验证通过：`SessionHello` 由 22 次降为 1 次，快照确认由 0/3 变为 3/3。
证据：[`到站之后首次走通`](https://github.com/trytoreachpeak0/8005-agv-control-server/blob/1b9ed3b/evidence/g3/20260829-arrival-to-sublot-field-verify/SUMMARY.md)。

协议 `SnapshotAppliedAck.schema.json` 仍只把 `appliedContentSha256` 声明为 `Sha256` 类型而
**未说明覆盖范围**——两端现在靠一致的实现互通，不是靠契约。该项仍列入下面的未解决项。

## 业务段现状

| 段 | 状态 | 证据 |
| --- | --- | --- |
| Sublot 提交与准入复检 | **已走通** | `SublotSubmitted` 1 条，`ConsumedSublotMessageId` 已落值 |
| `AwaitingLoadResult`（装货、解锁与锁反馈）| **已走通** | `Load` `Committed`，结果 `COMPLETED`、`HistoricalOnly=0` |
| 离站前安全检查（`PreDepartureSafetyCheck`）| **已走通** | `ConsumedSafetyResultMessageId` 已落值 |
| `TO_GATE` 移动 | **已走通** | `order-2093690819126099968` `CONFIRMED`，目的站 210，`CreateAttemptCount=1` |
| 关卡到站 | **已走通** | 旅程进入 `AwaitingUnloadResult` |
| 关卡批量卸货（多仓位单命令）| **未走通** | 见下节 |
| 原子完成（UnloadBatch + StopClosureCommit + Demand success + 租约释放）| 未到达 | 上一段 |

其中「关卡批量卸货」还叠着一个已知情况：车载执行器逐门串行开锁
（`ValidateCommand` 接受 1～8 仓位，`ExecuteExclusiveAsync` 串行执行），与模拟器
`maxOpenDoors: 1` 一致；这满足"一条命令覆盖多仓位"，但现场是否符合作业预期需要业务确认。

## 唯一的技术阻断：关卡工作单 revision 冲突（已修复，待现场复跑）

`gate` 与 `fullloop` 两次运行到达关卡后分别出现 35 次与 74 次 `ProtocolProblem`，原因码全部是
`SNAPSHOT_REVISION_CONTENT_CONFLICT`，被拒消息全部是 `CurrentStopWorklistSnapshot`。

取货与关卡的工作单站点不同、角色不同、停靠点不同，却都以 revision 1 发出
（`fullloop` 结束时 `WorklistRevision` 仍为 `1`）。对端按类型与 revision 判定快照身份，**正确地**
把第二条读作「内容未变」并拒绝，连接随之断开、重连、再拒绝。`fullloop` 的 outbox 直接坐实后果：
`CurrentStopWorklistSnapshot`、`UpcomingStopPlanSnapshot`、`SlotOperationCommand` 各 2 条、
各有 1 条未确认——**卸货命令排在被拒快照之后，从未被对端取到**，关卡段无从开始。

修复 `ControlServer_MVP@3d8b00c`：revision 改为参数，关卡停靠点按其同级投影既有的方式推进。
已过完整测试 228/228（0 skip）与绑定自身的八片 G2（137 个筛选测试、0 skip），**尚未现场复跑**。

复跑要一轮完整闭环、再动两次车，且必须把 `JourneyRuntime__dispatchGeneration` 推进到 `3`——
第 1、2 代的 `PICKUP`／`GATE` 订单在 RIoT 均已终结，沿用会直接对账确认而不动车。

## 其它未解决项

1. **`PACKAGE_CAPACITY_NOT_UNIQUE`** —— 仍有封装缺精确 boxes-per-basket 规则，需具名业务
   负责人提供或批准，非技术问题。当前有多条 `ELIGIBLE` 可绕开，不阻断，但现场若正好要跑
   那条封装就会被挡。
2. **`MT_NA` 与安全谓词** —— 车辆重启或人工挪动后 `movementState` 为 `MT_NA`，Round-41 谓词
   要求 `MT_FINISHED`，因此每次重启／人工挪车后都需先跑一次 RIoT 移动订单才能开工。当前
   判断这不是产品缺陷（Behavior Lab 无契约支持把 `MT_NA` 视为安全停稳），但它是每日开工的
   实际摩擦，值得单独做一轮实验把语义定下来。
3. **协议未定义字段** —— 已累计**六处**：`supportsBatchUnlock`、两个快照的发送节奏与新鲜度、
   `appliedContentSha256` 覆盖范围、`resultContentSha256` 序列化口径、
   `PreDepartureSafetyCheckResult.correlationId` 关联对象、`validUntil` 最短有效期。其中四处
   同源于一个成因：`DateTimeOffset` 转换器原样写出时区的 `+`，而 `JsonElement` 重序列化会把它
   转义成六字符 unicode 转义——两端语义相同、字节不同。建议在协议仓补齐定义，该仓为审批门禁，
   需两名负责人批准。

## 对截止日期的判断

当日深夜又推进五段，旅程已到关卡待卸货，**只剩两段**且技术阻断已定位并修复。但
`3d8b00c` 尚未现场复跑，而复跑本身可能像前六次一样暴露新的跨端未定义约定——当日六次运行里有
五次各暴露一处。

因此判断为：**剩余部分是一到两轮完整闭环的量级，前提是复跑不再暴露新的跨端分歧**。在
`3d8b00c` 现场验证通过、卸货与四事实原子完成走通之前，不得把当前状态表述为 MVP 完成；
路线图本身也明确禁止这种表述。

## 建议的下一步顺序

1. ~~王昆就快照 revision 去重键给出决定并实现~~ —— 已完成（`OnboardHmi_MVP@304e6ad`）。
2. ~~复跑取货到站，确认推进到 `AwaitingSublot`~~ —— 已完成（`ControlServer_MVP@1b9ed3b`）。
3. ~~子批录入、装货、发车安全检查、`TO_GATE`、关卡到站~~ —— 已完成
   （`ControlServer_MVP@f48e616`，证据 `20260829-load-to-gate-field-verify`）。
4. **用 `3d8b00c` 跑一轮完整闭环**，确认关卡工作单不再被拒、卸货命令被取到、四事实原子完成。
   需要：`dispatchGeneration = 3`、真实操作员身份、两个方向各一次现场物理安全 GO 与逐次建单
   授权。车辆现停在关卡站点 210。
5. 期间把六处协议未定义字段整理成一次协议修订，走两人批准。
