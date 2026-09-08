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

**批次 1 有一条出口未达成，但不阻塞本票**：「生成器可重跑且输出确定」。升级后的
`generate-protocol-candidate.mjs`（规格 3.2 的 11 项输出点）只存在于 `vm01`，从未回到任何
仓库；本机三份副本字节相同且都是 v0.1.1 版（`profileId WIRE_TO_GATE_MVP`、
`protocolVersion 1`、`candidateVersion 0.1.0`），写出的 `g1-validate.mjs` 仍是 8 切片 ＋
`runner/` schema 的老契约。本票依赖的是协议仓里**已有的** v2 内容，不依赖生成器本身。

**状态：** ready-for-agent

- [ ] 三项身份全部切到 v2，代码里不残留 v1 的 `profileId` 或 URI 段
- [ ] 63 条消息、**54** 个错误码在服务端有对应实现，缺一条即为未完成
- [ ] 全部 `IntegrationSlice` trait 重打为 `FP-IS-NN`，实际处理数量记录在完成说明里
- [ ] 重打标过程中逐条复核测试：每条测试确认仍断言它该断言的东西，改动逐条可解释
- [ ] `dotnet test --filter` 按新 trait 的分区**无遗漏无重复**（16 个切片的并集等于全集，
      两两交集为空）
- [ ] L1 全绿
- [ ] 完成说明中不出现「沿用已通过结论」这类表述
