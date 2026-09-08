# 14 — 服务端实现协议 v2，并逐个复核测试与重打 trait

**做什么：** 让控制服务端说 v2。身份三元组、消息面、错误码、schema URI 段全部跟上批次 1
冻结的面，同时把 165 处 `[Trait("IntegrationSlice", …)]` 从 `W2G-IS-NN` 重打成 `FP-IS-NN`。

身份三元组（规格 6.1）：

| 项 | v1 | v2 |
| --- | --- | --- |
| `protocolVersion` | 1 | **2** |
| `profileId` | `WIRE_TO_GATE_MVP` | **`AGV_FULL_PRODUCT`** |
| schema `$id`／`$ref` URI 段 | `wire-to-gate/v1` | **`agv-full-product/v2`** |

面的规模：消息 54 → **63**，错误码 43 → **54**，向量 19 → **31**。

> **错误码那个数 2026-09-08 更正过：不是 45，是 54。**规格 3.2 与票 09 写的「43 → 45」写在
> 票 06 冻结之时——那时只查出控制端 3 个表外码。控制服务端 `9eb2397`（架构测试落地）标题
> 即「顺便发现表外码是 14 个不是 3 个」：3 个是笔误，另 11 个是实现表达了协议没有的区分
> （协议只有一个 `RECOVERY_SCOPE_MISMATCH`，服务端分了事件／需求／操作员三种）。**用户
> 2026-09-04 定：那 11 个钉住，归宿是协议 v2 的错误码面。**其中 9 个进注册表，另 2 个
> （`RECOVERY_SESSION_CLOSED`、`FORCED_RECOVERY_GENERATION_MISMATCH`）是纯内部码，在
> `ToSessionReadinessReasonCode` 边界映射到注册表已有的 `RECOVERY_SESSION_NOT_OPEN` 与
> `FORCED_RECOVERY_GENERATION_STALE`，不入表。故 43 ＋ 2（票 06 冻结的 `SLOT_CONFIGURATION_*`）
> ＋ 9 ＝ **54**，与 `fp/v2-candidate` 的 `errors/error-codes.json` 实测一致，`appendOnly`
> 不破（0 删除）。架构测试的 `PinnedDeviations` 现为空集，14 个全部收口。

**重打标必须与「v2 变更后逐个复核测试」合并进行，不得单列**（规格第 3.3 节第 4 项）。
理由是重打标那一刻正是逐个看过每条测试的时刻，分成两次就等于看两遍还漏一遍。规格记的
是 161 个 trait，服务端实测 165 处引用，**以实测为准**，并在完成时记下实际数字。

**没有可沿用的通过结论。** `RELEASE-CANDIDATE.md` 第 12 节末写着 `W2G-IS-00`～`07` 与 RC
目前仍为 `INCONCLUSIVE`——描述这次切换时不得暗示存在可沿用的通过结论。

**冲突边界：** 本票与轨 B（票 06～13）并行。轨 B 的四条能力轨全是单端（服务端↔RIoT 或
服务端内部），不产生新协议消息，文件重叠小。若与轨 B 撞在同一文件，以轨 B 的能力代码为
准，本票只改协议身份与消息形状。

**前置：** 批次 1 完成（协议 v2 候选生成 ＋ G1 通过）。**2026-09-08 已满足，前置解除。**
协议仓 `fp/v2-candidate`（HEAD `f6ee75d`，已推送）即 v2 候选：`protocolVersion 2`、
`profileId AGV_FULL_PRODUCT`、63 消息、54 错误码、31 向量、16 切片。G1 于 2026-09-08
在协议仓 self-hosted runner 上实跑通过（run
[34212719223](https://github.com/trytoreachpeak0/8005-agv-protocol/actions/runs/34212719223)，
node v24.20.0）：`status PASS`、`failures []`、69 schema／63 消息／63 valid／1548 invalid／
31 向量／16 切片，与仓内 `evidence/g1-result.json` 逐字段一致。**这是 G1 第一次在这条分支
上真正执行**——此前所有 g1 运行都在 `main`，而 `evidence/g1-result.json` 的 `checkedAt` 是
`g1-validate.mjs` 里的硬编码常量，本身不构成执行证据。

**批次 1 四条出口 2026-09-08 全部绿**，见 `../batch-1-exit-verification.md`。其中「生成器可
重跑且输出确定」这条当天上午一度被误判为缺口（以为升级后的生成器只在 `vm01`），下午查明
它早在 2026-09-04 就提交在 `fp/generator-v2` 上，只是没合进 `main`；合并后在 `vm01` 上补做
了两条验证：`--verify-determinism` 报 1754 文件 0 分歧，且用它新产的树与 `fp/v2-candidate`
逐文件比对 1753/1754 逐字节相同，差异恰好是分叉台账第 6 节的生成后手工步骤。

**状态：** done（2026-09-08，见 [`14-answer.md`](14-answer.md)）

**开工时查出三处票据与实测不符，用户 2026-09-08 逐条裁定**，两条改写了下面的验收文字：

| # | 票据原文 | 实测 | 裁定 |
| --- | --- | --- | --- |
| 1 | 63 条消息「缺一条即为未完成」 | 12 条在 `src/` 零命中，其中 9 条所属切片被规格 7.2 排在批次 3～8 | vendored 注册表 ＋ 钉住缺口，不把批次 3～8 的活拉进批次 2 |
| 2 | 「并集等于全集，两两交集为空」 | 441 个测试方法里 300 个无切片 trait（规格 7.5 自列十类）、40 个带 2～4 个 | 改成「切片面上的闭合」三条子判据 |
| 3 | 身份表的 `tag protocol-v1.0.0` | 该 tag 在协议仓不存在，规格 6.6 第 6 条要 attestation | 照抄候选事实，`ApprovalStatus = SUPERSEDING_CANDIDATE`；`tag` 仍写 `protocol-v1.0.0`，因为 schema 要求 `minLength 1` ＋ `^protocol-v`，留空会让三条会话消息非法 |

- [x] 三项身份全部切到 v2，代码里不残留 v1 的 `profileId` 或 URI 段
      —— URI 段那半条服务端**根本不带**（grep 零命中），空真，如实记录
- [x] 63 条消息、**54** 个错误码在服务端有对应实现~~，缺一条即为未完成~~
      —— **按裁定 1 改为注册表 ＋ 钉住**。错误码 54/54 逐个相等（票 09 已做完）；63 条里 51 条
      在 `src/` 具名，12 条逐条钉住写明归属批次或替代行为。**票据字面的「缺一条即为未完成」
      未达成**
      —— **形状那一半是收尾复审才查出来的**：服务端发的三条 C_TO_O 快照仍是 v1 形状，7 处违反
      自己冻结的 schema（顶层多 `demandId`、leg 缺三个必填字段、`legType` 发 `TO_GATE`、
      `stopRole` 发 `GATE`、完全不发 `activePurpose`）。全部改对，并 vendor 协议 schema 整棵树
      新增 `ProtocolPayloadShapeArchitectureTests` 守住
- [x] 全部 `IntegrationSlice` trait 重打为 `FP-IS-NN`，实际处理数量记录在完成说明里
      —— **实测 186 处**（票据写 165、规格写 161），复核后 196 处
- [x] 重打标过程中逐条复核测试：每条测试确认仍断言它该断言的东西，改动逐条可解释
      —— 查出 8 条向量声称落在错误切片 ＋ 1 条一个切片都没有的测试，五处处置**只加不删**
- [x] ~~`dotnet test --filter` 按新 trait 的分区**无遗漏无重复**（16 个切片的并集等于全集，
      两两交集为空）~~ **按裁定 2 改为「切片面上的闭合」**
      —— 实测 583 个 test case：16 条 filter 选中 251 条目、去重 186、重复 65、未选中 397。
      **票据字面的两半都不成立且不该成立**
- [x] L1 全绿 —— `586 passed / 0 failed / 0 skipped`（原基线 569 ＋ 17 条新守卫）
- [x] 完成说明中不出现「沿用已通过结论」这类表述
      —— 反向加硬了 `RELEASE-CANDIDATE.md` 第 12 节末那句

**三条缺陷记在 `8005-agv-control-server/docs/defects/20260908-v2-identity-shipped-over-v1-payloads-and-an-empty-slice-gate.md`**：D-1 v1 形状的报文（7 处）、D-2 空切片的绿门禁、D-3 九个身份常量无人核对。

**其中 D-2 是本票才可能出现的**：切片家族从 8 扩到 16 之后，`dotnet test --filter`
选不中任何测试时退出码为 0，`test-wire-to-gate.ps1` 会把它写成 `"status": "PASS"`——实测
`-Slice FP-IS-09`（零实现零测试）拿到了一份绿的 G2 结果。已改为建目录前先数、选中 0 条即拒绝。
