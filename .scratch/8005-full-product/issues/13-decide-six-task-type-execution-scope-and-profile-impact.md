# 决定六类 MES 运输任务的执行范围，及其对 348 行剖面的影响

Type: grilling
Status: open
Blocked by: 03
Blocks: 06, 09

## Question

用户 2026-09-03 在票 03 的 Q9 定下：**完整产品要执行全部六类 MES 运输任务，不止
`WIRE_TO_GATE` 一类**（档 ii，改判了本会话推荐的档 i）。本票承接这个决定，把它的范围、
工程内容与剖面影响定完。

这张票是从票 03 拆出来的，因为它牵动的条目**不在 62 条里**，而在 186 条「批次 0 已覆盖」里。

### 触发本票的事实

`REQ-0003`、`REQ-0150`、`REQ-0181`、`REQ-0184` 都写着**六类** MES 运输任务，
`TransportDemandKey` 即 `TASK_TYPE + SUBLOT`。四条在剖面
`evidence/full-product-implementation-profile-draft.tsv` 里全标 `FP-B0 批次 0（MVP 已覆盖）`，
但它们的 `ControlServerImpact` 列写的是「执行 **WIRE_TO_GATE** 字段、站点和容量准入」
——**只覆盖六分之一**。62 条里没有任何一簇承载「执行其余五类」（簇分布：186 批次 0 +
100 MesIngest 范围外 + 62 分入 `FP-C1` 到 `FP-C8`）。

**这是本图第三次遇到同一现象**：能力藏在「批次 0 已覆盖」的条目里，实现却是单一形态的
退化版。前两次是多车（票 02 查出「348 条里无一条要求多辆车」）与 `REQ-0190`、`REQ-0194`
（票 03 查出准入表只有站点维度、无车辆维度）。**本票必须假定还有第四次**，逐条复核而不是
抽查。

### 开工前必须先查的事实

票 03 的经验是「找事实是 agent 的活，只有决策才问用户」，三个 `Explore` 子 agent 推翻了三条
原有假设。本票同样**不查就问会得到低质量的答案**。至少要查清：

1. **六类任务的实际名字。**基线里**只有 `STAGING_TO_WIRE` 有名字**——
   `WIRE_TO_GATE` 在 `requirements/baselines/current-requirements-v1.0.0.md` 里
   **出现次数为 0**，它是 MVP 阶段的命名（协议 `profileId` 与 `workType`），不是基线的任务
   类型名。其余五类的名字在工厂 IT 提供的 `MES_TASK_UNION` SQL 里，去 `8005-mes-ingest`
   查（该仓可读，四张地图、1100 个测试、已落地 CI/CD）。
2. **MesIngest 当前摄取几类。**`REQ-0181` 说「MesIngest 执行工厂 IT 正式提供的全厂六类 MES
   SQL；SQL 返回集是权威候选集」。若 MesIngest 已摄取六类而 ControlServer 只执行一类，那
   候选集里另外五类现在**去哪了**——被过滤、被忽略、还是根本没进目录？这决定本票是「加执行」
   还是「加摄取 + 加执行」。
3. **`REQ-0184` 的方向语义。**原文：「`STAGING_TO_WIRE` 中 EQP + AREA 表示终点；其余五类
   任务中表示起点。另一端由 8005 按 `TASK_TYPE` 配置为 `FixedTaskStation`」。当前实现把
   起点解析成 AREA 正则（`MapStationResolver.cs:10-12`、`:33-50`）、终点固定为「关卡」
   （`appsettings.json:53`）——**正好是「其余五类」的方向**。`STAGING_TO_WIRE` 是反的。
   要查清这个反转在代码里牵动哪些位置。
4. **锁死在一类的位置。**票 03 已查到四处：协议 `workType` 的 `const`
   （`schemas/messages/CurrentStopWorklistSnapshot.schema.json:87-91`）、
   `appsettings.json` 的 `allowedWorkTypes`、`StationTaskTypeAdmission` 的 taskType 在
   `JourneyRuntimeEngine.cs:75` 硬编码、`gateStationId` 单一固定终点。**要穷举，不要止步于这四处。**
5. **186 条批次 0 里有多少条是「只覆盖一类」的退化实现。**这是本票最重的一项，也是票 09
   要用的输入。

### 须回答

1. **六类各自的执行范围**：六类是否全部进完整产品，还是分批（例如先做与 `WIRE_TO_GATE`
   同方向的四类，`STAGING_TO_WIRE` 因方向反转单独一批）。每一档的准入不变量是什么。

2. **`FixedTaskStation` 的按类配置形态**：`REQ-0184` 要求「另一端由 8005 按 `TASK_TYPE`
   配置为 `FixedTaskStation`」。当前是单个 `gateStationId` 标量。六类各有自己的固定端点，
   配置形态怎么变，与票 03 已定的 `vehicles` 数组（Q5 甲）是同一套配置机制还是分开。

3. **剖面影响**：186 条批次 0 里哪些条目其实只覆盖了一类。逐条复核的口径是什么——全部 186
   条重看一遍，还是只看与 `TASK_TYPE`、站点方向、准入相关的子集？复核结果怎么在 348 行剖面
   里表达：改 `Batch` 列、加注释列，还是新增一列区分「已实施形态」与「完整产品形态」？
   **注意 `map.md` 的零遗漏口径是 348 条逐条一行，不得因为「批次 0 已覆盖」就跳过复核。**

4. **协议影响**：`workType` 的 `const` 解除为六类 enum 是 breaking（`docs/release-governance.md:11`
   明列 enum 变更为 breaking）。六类的枚举值取什么——MES 的原始 `TASK_TYPE` 字面值，还是
   8005 自己的命名？`profileId` 当前 `const` 为 `WIRE_TO_GATE_MVP`，完整产品是否随之改名
   （改名会牵动 54 条消息 schema 各自内联的那份副本）。**输出清单给票 06，本票不改 schema。**

5. **与票 03 四条的衔接**：票 03 已定 `REQ-0202`（优先级带）、`REQ-0203`（防饥饿跨类升级）、
   `REQ-0189`（`SublotTaskTypeConflict`）、`REQ-0190`（`agvId × taskType` 表）**因本决定成为
   活代码**。本票须确认这四条的实施形态不需要再改，或指出需要改的地方。

6. **批次归属**：六类执行面是独立批次，还是并入票 03 定下的 `B2 → (B1+B4) → B3 → B5` 序列。
   它与哪几条不变量有关——按票 02 的判据，「执行其余五类」是否推翻了某条架构不变量，还是
   纯增量（在既有 fail-closed 资格链上放宽一个谓词）。**这一判定直接决定它在票 09 里的位置。**

7. **验收边界的输入**：六类任务在现场是否都有真实物料可跑。若某几类在验收期无法在现场触发，
   证据形态归票 08，但本票须点名是哪几类、为什么。

### 已知边界

- 本票不改 v1.0.0 基线。六类是基线**已有**的事实（`REQ-0003`、`REQ-0150`、`REQ-0181`、
  `REQ-0184` 四条都在说六类），不是新需求，因此**不派生新需求条目**，与票 03 的
  `REQ-0190`、`REQ-0194` 情形同类。
- 本票不改协议消息面，只输出清单给票 06。
- 本票不决定批次顺序，那是票 09；但须给出「是否推翻不变量」的判定，那是票 09 排序的输入。
- 本票不决定车载端实现方式。车载端归 Kun Wang，其仓库对本工作区只读。
- MesIngest 侧若需改动，归 `8005-mes-ingest`，那是一个健康的、有自己四张地图与 CI/CD 的仓库；
  本票只判「要不要它改」与「改什么」，不重排它的既有工作。
