# 修掉跨趟 worklist revision 与两处 settle 的回归缺口

Type: task
Mode: HITL
Status: resolved
Blocked by: 21

## Question

票据 21 的 Standards + Spec 复核在 `ea8dc98..ee54988` 中发现两个真产品代码缺陷，均未被任何票的
验收条件覆盖、也未被 tier 1 保护。如何在不扩大范围的前提下修掉它们，并让每一处修复都有一条
「回退即变红」的回归测试？

两条缺陷的完整判据、失败场景与核实过程见
[票 21 的 `## Answer`](21-review-the-unreviewed-server-and-runner-changes.md)，此处不复述。

### 一、`worklistRevision` 从不持久化（跨趟）

`WorklistRevision` 唯一写入点是 `WireToGateStore.cs:1811` 的 `ToRuntimeRow`，恒为 `1`，全仓无
写回；gate 的 `+ 1`（`JourneyRuntimeEngine.cs:711`）是读时算的。runtime 行按 `DemandId` 建，
所以同一 AGV 的第二趟 demand 把 revision 重置回 1，与 ADR-cross-0048「针对当前 AGV 与站点单调
递增并由服务端持久化」冲突。

**先解一个未知数，再定方案。** 车载端是否在会话间重置已采用 revision，决定这条是「第二趟必然
复发 `3d8b00c` 的连接被拆」还是「跨重连侥幸绕过」。车载端仓对 agent 只读，本项目内无法确证。
两条可行路径，任选其一即可继续：

- 由用户向王昆确认车载端 `CurrentStopWorklistSnapshot` 的采用与拒绝判据（按什么 key、
  会话间是否重置）；
- 或用一次双 demand 的 staged 运行直接证伪——合成对端可复用票 18／19 建立的注入能力。

拿到答案前不要选定修复形态。候选方向（不预设结论）：把 revision 提升为 per (AgvId, StationId)
的持久计数器；或让 runtime 行创建时继承该车已发出的最高 revision。前者更贴 ADR 原文，后者改动小。

### 二、`f48e616` 的四处 settle 只有两处有回归保护

四处 `SettleAnsweredCommandAsync` 在 `JourneyRuntimeEngine.cs` 行 395／409／455／492。现有测试
只断言前两处，且主动断言 `Assert.Contains("PreDepartureSafetyCheck", stillPending)`。删除行 455
的 settle 调用，tier 1 全绿——而那正是该 commit message 自述的现场故障本体
（`thirty-one generations in four minutes`）。

这一条不依赖任何外部确认，可以独立先做：补两条断言，覆盖行 455（safety check 被回答后应 settle）
与行 492（unload command 被回答后应 settle）。既有测试
`DepartureSafetyAnsweredPromptlyIsJudgedWhileItIsStillValid` 与 `RunToGateUnloadAsync` 已经走到
那两处之后，只是没看 outbox，扩断言即可，不必新建 fixture。

### 完成判据

- 每处修复都有一条回归测试，且**先证明它会变红**再证明它变绿——按本路线三条方法论的第三条，
  「绿断言在被证明会变红之前不构成证据」；
- 缺陷二的两条断言在删除对应 settle 调用时各自变红；
- 缺陷一的修复能在一次双 demand 的运行（或等价测试）中证明第二趟的 worklist 被车载端接受；
- 收尾按 AGENTS.md 的产品改动要求：Release 0 warning／0 error、`dotnet format`、tier 1 且核对
  skip 数（不是只看 `Failed: 0`）；
- 证据归 ControlServer 仓，本票只留路由指针。

### 注意

- 不动车、不建单、不使用现场凭据。缺陷二完全不需要这些。
- 车载端仓与协议仓不在本票范围：前者只读，后者审批门禁。
- 本票挡住票 12（授权发布）。票 21 的前提是「在授权正式发布之前」完成复核，这两个缺陷是该复核
  的产出，因此必须在发布前收口或由用户明确接受风险后放行。

### 不在本票范围

票 21 记录的五项脚本／证据层偏差（票 20 的 `-CommitBindingSource` 漂移口、票 11 的断言无机器可读
记录与证据产物缺失、发布脚本扫描结果不设闸、三个 runner 的重复函数）都不触及产品代码，不需
tier 1。若要处理，另开一票，不要并进本票——那会让一次 tier 1 同时承载产品与脚本两类改动。

## Answer

两个缺陷都已修复，各自的回归测试都**先证红再证绿**。产品改动、测试与主要证据留在
ControlServer 仓，本票只留决策记录与路由指针。

### 路由指针

```
Owning repository: https://github.com/trytoreachpeak0/8005-agv-control-server
Owner artifact: evidence/g2/20260830-issue22-revision-and-settle/SUMMARY.md
Published branch/commit: ControlServer_MVP@127b137（修复+测试）、@0e4d471（G2 证据）
Impact on this ticket: 已收口；票 12 不再被本票阻断
```

推送尚未执行——属对外动作，待用户明确同意后再推。

### 一、缺陷一：动手前那个未知数，用只读检查解掉了

票据原文把「车载端是否在会话间重置已采用 revision」列为必须先解的未知数，并给了两条路径
（向王昆确认 / 双 demand staged 运行）。**两条都不需要**：`8005-agv-onboard-hmi` 对 agent 只读，
但只读检查与 fetch 是允许的。fetch 后直接读 `OnboardHmi_MVP@304e6ad`——王昆 2026-08-29 的
`Fix snapshot revision replay across sessions`，本地克隆停在更早的 `bbfbc52`，那正是把这个冲突
交接出来的那次提交。

判据（车载端仓，全部只读取证，未写入该仓任何内容）：

| 事实 | 位置 |
| --- | --- |
| 已采用快照持久在 SQLite，键**只有 MessageType**——无 demand、无 session | `SqliteWireToGateJournal.cs` 的 `ON CONFLICT(MessageType)` |
| 全仓对该表无任何 DELETE | `git grep WireToGateAppliedJourneySnapshots` 只有 CREATE/SELECT/INSERT |
| 更低 revision → `SNAPSHOT_REVISION_REGRESSION` | `SqliteWireToGateJournal`、`WireToGateSessionClient.ApplyJourneyRevision` |
| 相同 revision 且 payload 规范化哈希不同 → `SNAPSHOT_REVISION_CONTENT_CONFLICT` | 同上 |
| 两种拒绝都先发 protocol problem **再 rethrow**，连接被拆 | `ApplyJourneySnapshotAsync` 的 catch |
| 断连只清内存副本 | `CloseConnectionAsync`、接收循环 catch 里的 `ResetJourneyProjection()` |
| **每次重连在 SessionHello 之前从 journal 还原** | `RestorePersistedJourneyProjectionAsync` |

**答案：车载端不在会话间重置已采用 revision，也不按 demand 重置。** 所以这条不是「跨重连侥幸绕过」，
是**第二趟必然被拒**；而且形态比票据推测的更硬——是 `SNAPSHOT_REVISION_REGRESSION`（1 < 2），
不是内容冲突。304e6ad 修的是**相同** revision 下的假冲突（改用 payload 规范化哈希），
**更低** revision 那条路径它没碰、也不该碰。

### 二、缺陷一的范围比复核所述宽一条流变三条

`ToRuntimeRow` 把**三个** revision 都写死为 1：`VehicleBusinessRevision`、`WorklistRevision`、
`PlanRevision`，分别落在 `VehicleBusinessStateSnapshot`／`CurrentStopWorklistSnapshot`／
`UpcomingStopPlanSnapshot`。车载端按 MessageType 分别记账，所以第二趟三条流同时回退。
票 21 只点名了 worklist 一条——只修那一条，另外两条照样拆连接。

### 三、修复形态与被否掉的候选

新 runtime 行的三个 revision 从该 `AgvId` 已存储的最高值 **+2** 起算
（`WireToGateStore.SeedSnapshotRevisionsAsync`）。+2 的依据是发布形状本身：一趟旅程在取货站发出
其存储值、在关卡站发出该值 +1，故下一趟必须从 +2 开始。

- 幂等重放走早退分支，`Matches(runtime, journey)` 不比较 revision，不受影响；
- 同一 `VehicleKey` 的并发被车辆租约排他挡住；
- runtime 行全仓无删除点，所以「已存储的最高值」是持久事实，不依赖任何新表或迁移。

**候选「per (AgvId, StationId) 持久计数器」被否**。票据说它「更贴 ADR 原文」，但对上真实车载端是
错的：车载端按 MessageType 记账，不按站点；按站点各自计数会让同一趟的取货与关卡双双落在 1，
正是 `3d8b00c` 修掉的那次同 revision 冲突。ADR-cross-0048 里「针对当前 AGV 与站点单调递增」的
可实现读法只有一个——**针对该 AGV 的该条快照流单调递增，站点靠 payload 的 `stationId` 区分**；
ADR 自己那句「当前站点变化后，旧 stationId 的快照即使 revision 更高也不能覆盖新站点界面」
也是这个意思。

### 四、缺陷二

新增 `CommandsAnsweredAfterTheGateDepartureAreSettledToo`：跑到 `Completed` 后断言
`PreDepartureSafetyCheckMessageId` 与 `UnloadCommandMessageId` 都不在未确认 outbox 中。
既有测试停在安全检查**尚未被回答**的时刻并主动断言它仍然 pending，这是对的——缺的是被回答之后。

### 五、可证伪性（方法论第三条）

| 变异 | 结果 |
| --- | --- |
| 去掉 `SeedSnapshotRevisionsAsync` 调用 | 红，实际序列 **`[1, 2, 1]`** |
| 删除安全检查那处 settle | 红，messageId `8a850d01-…` |
| 删除卸货命令那处 settle | 红，messageId `bda91f23-…` |

两条 settle 断言的失败 messageId 不同，故互相独立，不是一条覆盖两处。
revision 断言按 messageId 去重后再判断——fixture 的 peer 从不 ACK，未确认 outbox 行每轮迭代都被
重发，只有首次发送才对应一次 revision 分配。

### 六、收尾门禁

| 项 | 结果 |
| --- | --- |
| Release 构建 | 0 warning / 0 error |
| `dotnet format --verify-no-changes` | 干净 |
| 全量测试（Release） | 230 passed / 0 failed / **0 skipped** |
| 八片 G2 | 全部 PASS，绑 `127b137` + `protocol-v0.1.1@1531489e`，manifest 哈希回读一致 |

先提交（`127b137`）后跑 G2，`implementationCommit` 由脚本从工作树读回而非重述；证据再提交
（`0e4d471`）。未动车、未建单、未触 RIoT、未用现场凭据、未动已安装服务。

### 七、本票范围外的两项新发现

1. **ACK 丢失会造成同样的 regression**：某条快照的 ACK 若丢失，它会在更高 revision 的快照之后被
   重发，真实对端同样判 `SNAPSHOT_REVISION_REGRESSION`。这属可靠重发顺序，不属 revision 分配，
   本轮未处理。要处理请另开一票。
2. **车载端与 ADR 的一处偏差**：ADR-cross-0048 原文是「更低 revision 丢弃并返回当前已采用版本」，
   车载端实现是抛异常 + 拆连接。归 `8005-agv-onboard-hmi`（对 agent 只读），本仓不修、
   也未写入该仓；需要一个明确可写的跟踪目的地或由用户直接通知王昆——与交接文档「需要用户决定」
   第 1 条同类。
