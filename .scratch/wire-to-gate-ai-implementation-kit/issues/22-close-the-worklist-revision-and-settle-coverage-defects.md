# 修掉跨趟 worklist revision 与两处 settle 的回归缺口

Type: task
Mode: HITL
Status: open
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
