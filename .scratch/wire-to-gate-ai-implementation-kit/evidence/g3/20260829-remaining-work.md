# 2026-08-29 剩余工作与阻断评估

配套文档：[`20260829-proven-state.md`](20260829-proven-state.md)（已证明的部分）。

本文不做乐观估计。截止已第二次顺延至 2026-08-30 17:00，范围与完成定义未变。下面逐段说明还差
什么、卡在谁那里。

> 2026-08-29 深夜更新：原文写于当日午后，彼时旅程停在 `AwaitingSublot`。此后子批录入、装货、
> 发车安全检查、`TO_GATE` 移动、关卡到站五段已在现场走通，本文按当前状态重写。

## 一句话

**WIRE_TO_GATE 端到端闭环已在现场走通**：受理 → 建单 → 取货移动 → 到站认定 → 三条快照确认 →
子批录入 → 装货 → 发车安全检查 → `TO_GATE` 移动 → 关卡到站 → 关卡批量卸货 → 四事实原子完成，
旅程终态 `Completed`，全程 1 分 58 秒。

**但这只是八类 G3 向量中的一条**（正常端到端旅程）。票据 10 要求的其余七类仍未在当前双端 commit
下的现场覆盖，正式 W2G-IS-00～07 的 G3 与 RC 继续 `INCONCLUSIVE`。

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
| 关卡批量卸货（多仓位单命令）| **已走通** | `Unload` `Committed`，结果 `COMPLETED` |
| 原子完成（UnloadBatch + StopClosureCommit + Demand success + 租约释放）| **已走通** | 四事实同一时刻提交，租约已释放 |

其中「关卡批量卸货」还叠着一个已知情况：车载执行器逐门串行开锁
（`ValidateCommand` 接受 1～8 仓位，`ExecuteExclusiveAsync` 串行执行），与模拟器
`maxOpenDoors: 1` 一致；这满足"一条命令覆盖多仓位"，但现场是否符合作业预期需要业务确认。

## 已解除：关卡工作单 revision 冲突

`gate` 与 `fullloop` 两次运行到达关卡后分别出现 35 次与 74 次 `ProtocolProblem`，原因码全部是
`SNAPSHOT_REVISION_CONTENT_CONFLICT`，被拒消息全部是 `CurrentStopWorklistSnapshot`；卸货命令排在
被拒快照之后，从未被对端取到。修复 `ControlServer_MVP@3d8b00c` 已于 `gen3` 现场验证：
`ProtocolProblem` 归零、`ProtocolOutbox` 全部 `unacked = 0`、旅程到达 `Completed`。

## 剩余的 G3 向量

票据 10 要求 W2G-IS-00～07 覆盖八类向量。当前只有第一类有当前双端 commit 下的现场结果：

| 向量 | 现场状态 | 已有的非现场证据 |
| --- | --- | --- |
| 正常端到端旅程 | **PASS**（`gen3`） | — |
| 重复／乱序／延迟 | 未覆盖 | 「重复」有 staged G3 probe（绑 `ea3050d`）；乱序／延迟无 |
| 不同内容冲突 | 未覆盖 | staged G3 probe 的同 ID 异内容稳定冲突（绑 `ea3050d`）|
| 断联安全收尾 | 未覆盖 | 八片 G2 |
| 进程崩溃重启 | 未覆盖 | `20260826-staged-no-movement`（绑 `cc6e2b9`）|
| 结果重放 | 未覆盖 | `RecoveryStateReport` 首 Ack 丢失重放（绑 `264e98b`）；`OperationResult` 首结果重放无 |
| RIoT UNKNOWN 对账 | 部分 | `20260829-authorized-single-real-create` 的 PRE/POST UNKNOWN 审计链，未作为 G3 向量正式记录 |
| 恢复分支 | 未覆盖 | 恢复命令族八片 G2（绑 `ea3050d`）|

**关键判断：这七类里没有一类需要真实移动。** 需要真车的是「正常端到端旅程」，已经做完。其余都是
故障注入与进程控制，可在 loopback 隔离环境完成——`scripts/run-staged-g3.ps1` 已有 TLS fault
proxy、drop／duplicate／异内容探针与精确克隆机制。

该 runner 的两处缺口是实打实的工作量，不是配置修改：

1. **绑定过期**：默认绑 `ControlServer ea3050d` + `Onboard 15c6387`，需更新到 `3d8b00c` +
   `304e6ad`，并重跑既有向量。
2. **消息面过窄**：drop／重放探针只针对 `RecoveryStateReport`，未覆盖 `SlotOperationCommand`、
   `OperationResult`、`PreDepartureSafetyCheck` 等业务消息，而票据要的「结果重放」正是后者。

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

端到端闭环已经走通，**性质变了**：此前每一轮都在解跨端未定义约定，现在剩的是把已实现的行为在
故障向量下逐条证明。这类工作可预期性高得多——它不依赖现场、不依赖操作员、不动车，失败模式也
不再是「两端对同一字段理解不同」。

但**量不小**：七类向量、八个切片，加上 runner 本身要更新绑定与扩展消息面。且票据 10 之后还串着
11 → 13 → 14 → 12 → 15 五张票（发布候选、真实适配器与部署边界、验收、授权发布、交接）。

因此判断为：**2026-08-30 17:00 的截止，完整 RC 仍不可能达成**。闭环走通是实质里程碑，但路线图
明确禁止把它表述为 MVP 完成——完成定义要求关键重复、断联、重启和恢复场景通过，那正是剩下的七类。

## 建议的下一步顺序

1. ~~王昆就快照 revision 去重键给出决定并实现~~ —— 已完成（`OnboardHmi_MVP@304e6ad`）。
2. ~~复跑取货到站，确认推进到 `AwaitingSublot`~~ —— 已完成（`ControlServer_MVP@1b9ed3b`）。
3. ~~子批录入、装货、发车安全检查、`TO_GATE`、关卡到站~~ —— 已完成
   （`ControlServer_MVP@f48e616`，证据 `20260829-load-to-gate-field-verify`）。
4. ~~用 `3d8b00c` 跑一轮完整闭环~~ —— 已完成（证据 `20260829-closed-loop-gen3`）。
5. **把 `run-staged-g3.ps1` 的绑定更新到 `3d8b00c` + `304e6ad` 并重跑既有向量**。这是最便宜的
   一步：不动车、不需要现场，直接把「重复」「异内容冲突」「恢复报告重放」三条从旧 commit 抬到
   当前 commit。
6. **扩展 drop／重放探针到业务消息面**（`SlotOperationCommand`、`OperationResult`、
   `PreDepartureSafetyCheck`），覆盖票据要求的「结果重放」与「断联安全收尾」。
7. 补「乱序／延迟」与「恢复分支」两类向量的现场或隔离结果。
8. 期间把六处协议未定义字段整理成一次协议修订，走两人批准——这一项独立于上面，可并行。
