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
`integrationSliceCount 16`、`trajectoryCount 31`）。**本票不依赖生成器**，只读协议仓已有的
`index.json` 与两端测试标注，因此批次 1 那条未达成的生成器出口不阻塞它。

**状态：** ready-for-agent

- [ ] 一条架构测试断言每个 `vectorId` 有具名测试对应，删掉一条测试能让它变红
- [ ] 同一条测试断言不存在指向不存在 `vectorId` 的测试标注，改错一个 id 能让它变红
- [ ] 断言的向量清单从协议仓的 `index.json` 读取，测试里不出现手抄的第二份清单
- [ ] 测试在 headless runner 上跑，不需要桌面
- [ ] 测试不挂任何 `IntegrationSlice` trait
