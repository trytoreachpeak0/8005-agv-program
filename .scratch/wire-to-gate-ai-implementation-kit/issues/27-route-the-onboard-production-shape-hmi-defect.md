# 处置生产形态下车载端 HMI 不反映 WIRE_TO_GATE 且无恢复出口

Type: grilling
Mode: HITL
Status: resolved
Blocked by:

## Question

票 14 的现场闭环在 RC 的生产形态下走通了业务，同一轮暴露出车载端 HMI 的一个可用性缺陷：站点操作
一旦落进 `RecoveryRequired`，现场操作员在随包 HMI 上没有任何前进或撤销的手段，且整个 WIRE_TO_GATE
业务过程不进 HMI 的状态横幅与操作记录。

缺陷归车载端仓，该仓对 agent 只读，因此本仓不保存缺陷正文、复现步骤、修复或测试。

需要用户决定走哪条路：转交王昆在车载端仓修复、指定一个明确可写的跟踪目的地、还是判定为本轮 MVP
可接受的已知限制并写进发布说明。决定之前不在任何仓库写入缺陷记录或修复。

Owning repository: https://github.com/trytoreachpeak0/8005-agv-onboard-hmi

Routing status: read-only for agents；**已由 owner 受理**。可见性半边修复于
`OnboardHmi_MVP@31263b1`；恢复出口半边经证实非车载端可单独修复，判为本地图范围外。
本仓对该仓全程零写入。

Impact on this ticket: 不阻断票 14 的闭环结论（generation 7 已 `Completed`），但阻断「随包 HMI
对现场操作员可用」这一条资格结论。

转交件（仓外）：`C:\Users\szy\Desktop\致王昆20260830车载端生产形态HMI缺陷.md`

现场证据（服务端仓，本项目自有）：`8005-agv-control-server@9daeef4` 的
`evidence/g3/20260830-issue14-field-closed-loop/SUMMARY.md`。

## Answer

**转交件起了作用，路由决定由现实作出，不需要另指可写目的地。** 本会话开工时只读 fetch 车载端仓，
发现 `OnboardHmi_MVP` 已从 `304e6ad` 前进到 `31263b1`（Kun Wang，2026-08-30 20:06:48 +0800，即现场
闭环 19:26 之后），单提交 `Fix production W2G HMI status and recovery visibility`，10 文件 +622/−12，
含 `WireToGateHmiPresentationTests.cs`（114 行）与 `SafetyRulesTests.cs` 的 28 行新断言。本仓对该仓
**全程零写入**（仅 fetch 与只读阅读），缺陷正文、修复与测试都在 owner 仓，本票只留路由指针。

**缺陷的两半性质不同，必须分开结论。**

**可见性半边：已修复，但不在本 RC 内。** owner 把横幅与「任务系统」状态改由正式上层会话驱动，不再
依赖恒 false 的 `DisabledRuleGateway`；子批录入、仓位操作阶段、结果确认、恢复阻断与可靠重放均投影
进操作记录；批量操作在八仓卡片上同时标识全部目标仓位，失败后保持「需要管理员恢复」而不退回
「连接中」。**本 RC 的车载端二进制建自 `304e6ad`，不含该修复**，故本资产行为不变，需要它必须重建
候选。本会话**未构建也未运行**该修复——本 RC 不含它，验了不改变本轮任何结论；下次重建候选时连同
验证更有价值（用户确认）。

**恢复出口半边：不是车载端缺陷，是跨端结果身份缺口。** owner 在
`docs/W2G_PRODUCTION_HMI_RECOVERY_GAP.md` 中把它弹回服务端，并给出四点约束。**这四点已在我们自己
可写的 `ControlServer_MVP@9daeef4` 上逐条读代码核对，全部属实**：

| owner 断言 | 服务端位置 | 结论 |
| --- | --- | --- |
| `RESUME_AFTER_REPAIR` 不推进 `forcedRecoveryGeneration` | `OnboardRecoveryCoordinator.cs:357` —— `AdvanceForcedRecoveryGenerationAsync` 只在 `FORCED_MECHANICAL_RECOVERY` 分支内被调 | 属实 |
| 同 attempt 的新结果被判内容冲突 | `WireToGateStore.cs:1352-1372` —— replay 查询命中 `(SlotOperationAttemptId, ForcedRecoveryGeneration)` 分支后，`ResultId` 不同即抛 `ProtocolContentConflictException` | 属实 |
| 重放原结果被按 replay 忽略 | 同上，五个字段全同则返回 `Replay` | 属实 |

因此 `SlotOperationResumeCommand` 在当前协议下**没有可收敛的结果身份**：修好物理状态后发同 attempt
的新结果被判冲突，重放原结果被忽略，两条路都不让 workflow 收敛。**车载端保持 fail-closed 是当前唯一
正确的行为，不是占位。** 收敛需要两端先选定 owner 给出的三个方案之一（resume 命令带新
operation/result identity；服务端在活动 `recoveryActionId` 下允许同 attempt 的授权替代结果；协议新增
独立 resume result 并明确它如何关闭原 `OperationResult`），涉及协议仓变更与两名负责人批准。
**AI 不代批跨端契约**，且本地图的 Destination 在票 15 已成立、发布时六条已知限制已被接受，故该缺口
判为本地图 **Out of scope**，作为 RC 之后的独立一轮（用户确认）。

**收掉票 15 留下的唯一尾巴。** 线上 Release 说明的已知限制第 1 项原写「去向尚未落定；落定后回补」，
现已按上述事实改写为 1a／1b 两段（保留第 1 项编号，第 2～6 项不重排）：1a 说明本资产内问题仍在、
修复在 `31263b1` 但不在本资产内、需要它必须重建候选；1b 说明它不是车载端可单独修复的缺陷、列出三个
候选方案与「涉及协议仓变更与两名负责人批准，判为本 RC 范围外」，并写明在方案选定并通过带 demand 的
联合回归之前现场处置须走人工流程。

改动**只在包外**，包内 868 条哈希与三个资产一字未动。执行顺序按交接件规矩：先改规划仓逐字副本
`release/w2g-mvp-rc-0.1.0-release-notes.md`，再用它同步线上，不两头各写。**四条回读取证**：
改前线上正文与 `git show HEAD:` 的副本逐字一致（唯一差异是线上多一个结尾空行），证明副本本来就忠实；
改后回读线上与本地 `VERBATIM MATCH`；三个资产仍 `release-manifest.json 171955 / SHA256SUMS.txt 98898
/ w2g-rc-20260830-81cb9cf.zip 123976762`，全部 `uploaded`；tag 对象仍是 `0c4d1103…`（与票 15 记录同）。
比对器**证明会响**——本地副本翻一个字符（`31263b1`→`31263b2`）即 `DIFFERS as expected`。

**给 owner 的答复件已写在仓外**：`C:\Users\szy\Desktop\致王昆20260830车载端HMI修复确认与恢复收敛缺口处置.md`。
内容三件：修复已收到但本轮未验及其理由；四点服务端约束核对属实、fail-closed 不必改；三选一判为本轮
范围外、**不代选任何一个**，并明说不要等我们的答复动手。不进任何仓库。

未触产品代码，故未跑 tier 1。
