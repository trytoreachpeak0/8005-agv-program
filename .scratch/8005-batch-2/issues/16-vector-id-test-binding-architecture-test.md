# 16 — `vectorId` ↔ 具名测试绑定架构测试

**做什么：** 让 CI 上一条测试持续证明：协议冻结的每个 `vectorId` 都有一条具名测试对应，
反过来每条声称对应向量的测试都指向一个真实存在的 `vectorId`。做完之后，「31 个向量都被
测了」不再靠人数数。

v2 的向量从 19 条扩到 **31 条**，切片家族表从 8 行改 16 行，`vectorIds` 条目合计 34、
去重 31。这条测试就是这个「34 引用 / 31 去重 / 无遗漏无多余」的机器守卫。

**不挂任何簇。** 规格第 14 节待办第 5 项把它与两条 `reasonCode ∈ 注册表` 架构测试、
RIoT 白名单架构测试并列为三条「CI 上一条测试绿」的横切守卫。两条 `reasonCode` 架构测试
属批次 1，本票只做 `vectorId` 这条。

**冲突边界：** 独立测试文件，不碰产品代码。与票 14／15 并行——它读协议仓的 `index.json`
与两端的测试标注，批次 1 一落地就能写。

**前置：** 批次 1 完成（`index.json` 有 v2 的 16 行切片表与 31 条向量）。**2026-09-08 已满足，
前置解除。**`fp/v2-candidate` 的 `integration-slices/index.json` 实测 `schemaVersion 2.0.0`、
**16** 条切片（`FP-IS-00`～`15`），`vectors/` 实测 **31** 个目录；G1 在 CI 上对这两个数各有
一条断言并通过（run
[34212719223](https://github.com/trytoreachpeak0/8005-agv-protocol/actions/runs/34212719223)，
`integrationSliceCount 16`、`trajectoryCount 31`）。**批次 1 四条出口已于 2026-09-08 全部
收口**，见 `../batch-1-exit-verification.md`。

**开工前先知道两件实测事实**（2026-09-08 查证，票据原文没写）：

1. **两端目前一条 `vectorId` 标注都没有。**`grep -rn "CV-[A-Z]"` 在
   `8005-agv-control-server/tests/` 与 `8005-agv-onboard-hmi/tests/` 上零命中。现有的只有
   187 处 `[Trait("IntegrationSlice", "W2G-IS-NN")]`（票 14 会重打成 `FP-IS-NN`）。
   **所以本票不是「写一条测试」，是「先建立 31 条绑定，再写守卫它的测试」**——那条测试要有
   东西可断言，绑定必须先存在。
2. **控制端没有 vendor 协议仓。**`vendor/` 下只有 `8005-agv-program` 与 `nuget`。而验收
   第三条要求「清单从协议仓的 `index.json` 读取，测试里不出现手抄的第二份清单」——
   **怎么让测试读到 `index.json` 是本票的第一个设计决定。**样板是
   `RiotCallAllowlistArchitectureTests`：它 vendor 了
   `vendor/8005-agv-program/docs/riot-call-allowlist.md` 并用 `ApprovedAllowlistSha256`
   钉住字节，`RepositoryRoot()` 靠向上找 `ControlServer.sln` 定位。

`index.json` 的形状：`slices[].vectorIds[]`，**16 切片 / 34 条目 / 31 去重**，与
`vectors/` 的 31 个目录双向无遗漏。三条向量跨切片共享（`CV-MANUAL-CHARGING-RETURN`、
`CV-OPERATION-RESULT-UNKNOWN-RECONCILE`、`CV-SESSION-RECONNECT-DURING-RECOVERY`）——
**断言要按去重后的 31 数，不是 34。**

**状态：** resolved（2026-09-08，见 [16-answer.md](16-answer.md)）—— 20/31 绑定到具名测试，
11 条按规格 7.2 钉住（切片属批次 3～8，服务端实测零实现）。控制端 L1
`569 passed / 0 failed / 0 skipped`。**车载端未做**，用户 2026-09-08 定为另开票。

- [x] 一条架构测试断言每个 `vectorId` 有具名测试对应，删掉一条测试能让它变红
- [x] 同一条测试断言不存在指向不存在 `vectorId` 的测试标注，改错一个 id 能让它变红
      （形态偏离：落地为同一测试**类**里的两个 `[Fact]`，见 16-answer.md 第五节，待裁定）
      —— **2026-09-14 用户裁定认可现状**：「同一条测试」按同一个架构测试类理解，不算偏离，代码不动
- [x] 断言的向量清单从协议仓的 `index.json` 读取，测试里不出现手抄的第二份清单
- [x] 测试在 headless runner 上跑，不需要桌面
- [x] 测试不挂任何 `IntegrationSlice` trait
