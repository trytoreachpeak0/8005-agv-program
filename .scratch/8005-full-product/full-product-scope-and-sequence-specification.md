# 8005 完整产品实施范围与顺序规格

| 项 | 值 |
| --- | --- |
| 状态 | **已批准**（2026-09-04） |
| 批准人 | Zhengyu Shao **一人**。Kun Wang 未评审、未批准，见第 0 节 |
| 产出 | wayfinder 地图《8005 完整产品实施范围与顺序路线图》票 01～15 |
| 日期 | 2026-09-04 |
| 覆盖 | `requirements/baselines/current-requirements-v1.0.0.md` 全部 348 条 |

**批准的范围就是本规格，不含 `CP-0001`。**需求变更提案是第 12.2 节的节点 2，与本规格的批准
（节点 1）是两次独立批准；`CP-0001` 的状态见第 9 节表格。在它获批之前，实施图不得据修订文
开工，引擎相关切片的验收证据按 8.8 第 3 条的写法记录偏离。

---

## 0. 这份文档是什么，不是什么

**是**：完整产品从今天到投运的范围与顺序判定。它对 v1.0.0 的 348 条需求逐条给出实施批次
归属，给出批次间依赖、协议 v2 的冻结面、切片家族编号、验收边界与证据要求，以及一份需求
变更提案。实施图据此开工。

**不是**：实施计划、日历排期、代码、需求基线的修订。本规格不改 v1.0.0 基线，不动
`requirements/current-baseline.md` 指针，不切 protocol release，不代任何人批准任何东西。

**批准的性质必须如实理解**：本规格由**用户单人批准**。Kun Wang（`8005-agv-onboard-hmi`
与 `slots-simulator` 的仓库所有者、`8005-agv-protocol` 的共同维护者）**未评审、未批准**本
规格的任何部分，包括协议 v2 的设计面。协议仓推送后按 notify-after-change 规则开 issue
`@SocialKKKK` 通知，**通知不是批准**。本规格及其任何派生物**不得表述为已获双方同意**。

**这份规格里的每一条结论都能追溯到一张已解决的票据**，追溯路径写在每节末尾。逐条的推理、
反证与被推翻的预设留在票据决议里，本规格只给结论与它的依据指针。

---

## 1. 身份绑定

### 1.1 需求基线

| 项 | 值 |
| --- | --- |
| 路径 | `requirements/baselines/current-requirements-v1.0.0.md` |
| Baseline SHA-256 | `5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba` |
| content commit | `b9f321228b534a3b316d3ac1abede05176ed6a70`（2026-08-24，`requirements: freeze current baseline v1.0.0 content`） |
| tag | `requirements-baseline-v1.0.0` → 上述 commit |
| 条目数 | 348，Lifecycle 全部 `active` |
| 变更历史 | **零次**。348 条全部 `Change Proposal: none（首版恢复）`，基线头部 `相对上一批准版本的变化` 段下 Modified 与 Deprecated 均为 `None` |

**tag 是补打的，这一点须记录。**汇编时查实该 tag 在本地与远端**都不存在**
（`git ls-remote --tags origin` 零输出），基线头部却已经引用了它。用户 2026-09-04 决定
补打 annotated tag 指向 `b9f3212`，理由是三项身份（SHA-256／content commit／tag）里只有
tag 不随历史重写漂移——而本项目已经因为历史重写丢过一次 commit 指针（见 1.3）。

### 1.2 本规格引用的证据

| 项 | 值 |
| --- | --- |
| 348 行实施剖面 | `.scratch/8005-full-product/evidence/full-product-implementation-profile-draft.tsv` |
| 剖面 SHA-256 | `aa5b1117b7159b2c53be7beb37ebaf55ffdeab94a3596383f4b3b4ecbeb3ac34` |
| 剖面形态 | 348 行 ＋ 1 行表头 = 349 行，**11 列**，349 个 LF、0 个 CRLF，220,819 字节 |
| 现场地形事实 | `.scratch/8005-full-product/evidence/map-topology-observed-facts.md`（Round 43 实测） |
| 票据决议 | `.scratch/8005-full-product/issues/NN-answer.md`，N = 01～09、11～15 |

**本规格自身的 SHA-256 不写在正文内**——文档记录自己的哈希是自指的，改一个字符就自我
证伪。它记在 `issues/10-answer.md` 里，与本规格的定稿版本一一对应。这一处是汇编时的自
行定案，理由与代价见第 16 节。

### 1.3 三处外部身份指针的状态

三者共性是**需求文本引用了一个位置或存续不由本项目控制的外部身份**。逐条处置：

| # | 出处 | 现状 | 处置 |
| --- | --- | --- | --- |
| 1 | 基线头部的 `requirements-baseline-v1.0.0` | 本地与远端都不存在 | **补打 annotated tag**（1.1） |
| 2 | `REQ-0157` 绑定的 commit `420c96c2f961aaffa42a5443fa42e6585b1c993f` | 在 `8005-mes-ingest` 对象库中**不存在**（2026-09-02 拆仓重写历史所致）；基线记的路径 `mes/queries/mes-task-union/` 与实际路径 `queries/mes-task-union/` 不一致 | **不修复，如实登记**。`query.sql` 的 SHA-256 仍完全吻合（`54a140ad…39ae`）——**断的是指针，不是内容**。重写过的历史无法复活一个 commit；内容身份完好即该条的实质约束未失效。本规格不改基线，故此处只登记正确读法 |
| 3 | `REQ-0294` 正文引用的「现有白名单」 | 实际指向 `.scratch/current-requirements-baseline/issues/37-decide-riot-api-allowlist-and-call-safety-boundary.md`——**另一张已完成地图的工作票据** | **登记为实施图待办**（第 14 节第 6 项）：把 RIoT 调用白名单提升为产品文档，并补上票 04 查出的第二种建单形态。汇编时查实该文件**在 `origin/main` 上被 git 跟踪**，故「被清理就没有权威副本」的风险低于票 12 的估计；真正的问题是**它的身份是工作票据而非产品文档，且内容已过时** |

第 3 项「内容已过时」的具体所指：获准的 RIoT 建单调用**从一种形态变成两种**——普通搬运与
空闲返回是**单段 move**，前往充电桩是 **`move(目标桩) + act(78, param1=1)`**（离桩的
`act(78,2,0)` 由 RIoT 自动插入）。vendored facade 的 `CreateMoveOrderAsync` 内部写死单元素
`Mission` 数组、`Type = "move"`，**建不出充电订单**。白名单文档逐条列举的获批调用里没有第
二种形态。

*追溯：票 01、票 12 第 1.7 节、票 04 的 Q11 与 1.6、票 13 第二段输入、票 09。*

---

## 2. 全量 348 条剖面

### 2.1 呈现方式：引用而不复制

**348 条的逐条归属不抄进本规格正文**，由上述 TSV 承载，本规格引用它的路径与 SHA-256。

理由：抄一份必然产生第二份真相，而剖面在本图中被改判过七次（见 2.3）；一份带哈希的引用
既满足「逐条一行、零遗漏」的口径，又不会漂移。这是汇编时的自行定案，代价是读者要开一个
TSV，收益是永远不会出现「规格里写 `BATCH-5`、TSV 里写 `BATCH-6`」这种事。

### 2.2 剖面的列结构

| # | 列 | 含义 |
| --- | --- | --- |
| 1 | `RequirementId` | `REQ-NNNN` |
| 2 | `Title` | 基线标题 |
| 3 | `OriginalScope` | MVP 剖面的原始范围判定 |
| 4 | `MvpFinalClassification` | MVP 的最终归类 |
| 5 | `ControlServerImpact` | 控制服务端影响串 |
| 6 | `OnboardHmiImpact` | 车载端影响串 |
| 7 | `SharedProtocolImpact` | 协议影响串 |
| 8 | `FullProductCluster` | 完整产品业务簇（`FP-B0`／`FP-C1`～`FP-C14`／`OOS-MI-1`～`4`） |
| 9 | `ClusterBasis` | 归簇依据 |
| 10 | **`Batch`** | 实施批次，机器可核的 enum |
| 11 | `Batch0FormNote` | **批次 0 判定在什么形态下成立** |

`Batch` 的取值集合：`BATCH-0`｜`BATCH-2`｜`BATCH-3`｜`BATCH-4`｜`BATCH-5`｜`BATCH-6`｜
`BATCH-7`｜`BATCH-8`｜`DEFERRED`｜`OUT-OF-SCOPE`。

**没有 `BATCH-1`，这是对的。**批次 1 是协议冻结面落地，它是票 06 的产物而不是需求条目，在
348 条上不产生任何一行——与票 02 判定的 B2（多车，348 条里无一条要求它）同理。**只按 348
行排批次会整项遗漏**，故第 3.3 节单列十项无条目载体的工程。

**第 11 列 `Batch0FormNote` 是本图的一项独立产出，不是备注。**它记的是「MVP 剖面当时的判
定没有错，是形态变了」。本图共**十一次**发现「能力藏在批次 0 条目里、而实现是退化形态」，
逐次都因为 MVP 的单车、单任务类型、单密钥、单会话语境下那个判定成立。这一列使每一次改判
都留下可复核的痕迹，而不是只留一个改后的批次号。

### 2.3 批次 0 的数字变过六次，取最新值

**批次 0 = 117**，不是任何早期票据正文里的 186。改判链：

```
186（票 01）→ 167（票 13）→ 166（票 12）→ 164（票 04）→ 146（票 05）→ 117（票 09）
```

对称地，**待排期 = 131**：62 → 81 → 82 → 84 → 102 → 131。

**引用任何早期票据正文中的计数都必须先核对本节。**七张票据逐次改判，早期正文里的数字全部
过时；本图对此的纪律是不回溯改旧票据，所以那些数字仍留在原处。

### 2.4 计数闭合（汇编时实测复核）

| `Batch` | 条数 |
| --- | --- |
| `BATCH-0` | 117 |
| `BATCH-2` | 14 |
| `BATCH-3` | 26 |
| `BATCH-4` | 17 |
| `BATCH-5` | 10 |
| `BATCH-6` | 17 |
| `BATCH-7` | 6 |
| `BATCH-8` | 19 |
| `DEFERRED` | 22 |
| `OUT-OF-SCOPE` | 100 |
| **合计** | **348** |

**闭合式是三项相加，不是四项**：批次 0 的 117 ＋ 待排期的 131 ＋ 范围外的 100 = 348，
其中**待排期 131 已经包含延后的 22**（批次 2～8 共 109 ＋ 延后 22）。把延后的 22 再单独加
一次会得出 370，那是错的。

### 2.5 业务簇分布（汇编时实测复核）

| 簇 | 条数 | 批次 |
| --- | --- | --- |
| `FP-B0` 批次 0 候选（MVP 已覆盖） | 117 | 0 |
| `FP-C1` 自动充电桩调度与充电失败治理 | 19 | 8 |
| `FP-C2` 多车与多任务调度 | 18 | 2（`REQ-0207` 一条）＋ 6（其余 17） |
| `FP-C3` 车载 Worklist 选任务模式 | 6 | 7 |
| `FP-C4` 空闲返回与等待点 | 10 | 5 |
| `FP-C5` AGV 归档恢复与身份连续性 | 7 | 3 |
| `FP-C6` 账号权限与密码治理 | 8 | 延后 |
| `FP-C7` 配置生效治理与回滚 | 14 | 3 |
| `FP-C8` 看板与观测 | 3 | 3 |
| `FP-C9a` 六类任务执行与公共站点绑定 | 8 | 4 |
| `FP-C9b` 公共站点绑定运维治理 | 9 | 4 |
| `FP-C10` 人员认证与账号 | 8 | 延后 |
| `FP-C11` RIoT 订单命令面与故障隔离 | 10 | 2 |
| `FP-C12` 维护开门模式 | 6 | 延后 |
| `FP-C13` 建单前置门禁与目录可用性 | 3 | 2 |
| `FP-C14` 审计留存与导出 | 2 | 3 |
| `OOS-MI-1` Inspector E 信息架构 | 30 | 范围外 |
| `OOS-MI-2` AreaFilterProfile 编辑与实时同步 | 26 | 范围外 |
| `OOS-MI-3` MesIngest 服务与外部可读目录 | 18 | 范围外 |
| `OOS-MI-4` GONE 明细与存储边界 | 26 | 范围外 |
| **合计** | **348** | |

*追溯：票 01、票 09 的 Q4 与 3.1、票 13 第一段输入。*

---

## 3. 实施批次与依赖图

### 3.1 九个批次 ＋ 一个延后集

| 批次 | 主题 | 条目 | 簇构成 |
| --- | --- | --- | --- |
| **0** | MVP 已覆盖，引用已批准的 MVP 规格 | 117 | `FP-B0` |
| **1** | **协议 v2 候选生成与 G1 通过** | 0 | —（无条目载体） |
| **2** | 两条并行轨：**轨 A** 协议 v2 两端实现与 `FP-IS-00`～`07` 重证；**轨 B** 服务端调度地基 | 14 | `FP-C11` 10 ＋ `FP-C13` 3 ＋ `FP-C2` 的 `REQ-0207` 1 |
| **3** | 治理面单端工程 | 26 | `FP-C7` 14 ＋ `FP-C5` 7 ＋ `FP-C8` 3 ＋ `FP-C14` 2 |
| **4** | 六类任务执行与公共站点绑定 | 17 | `FP-C9b` 9 ＋ `FP-C9a` 8 |
| **5** | 车辆用途占有与空闲返回（B1＋B4） | 10 | `FP-C4` 10 |
| **6** | 多停靠计划与途中追加换序（B3） | 17 | `FP-C2` 其余 17 |
| **7** | 车载 Worklist 选任务（B5） | 6 | `FP-C3` 6 |
| **8** | 自动充电桩调度与充电失败治理 | 19 | `FP-C1` 19 |
| **延后** | 三个整簇 | 22 | `FP-C10` 8 ＋ `FP-C6` 8 ＋ `FP-C12` 6 |
| **范围外** | MesIngest 四簇 | 100 | `OOS-MI-1`～`4` |

划分依据全部可验证，不含主观体量均衡：不变量推翻顺序（票 02）、新识别的 I6／I7、协议 v2
冻结面作为跨端能力的硬前置、切片 `prerequisites`（票 07）、四个横切大件的自然位置、现场
前置。

### 3.2 批次 1 的选定

**批次 1 = 协议 v2 候选生成与 G1 通过**（用户 2026-09-04 定）。内容全部无条目载体：

1. 生成器 `.scratch/wire-to-gate-ai-implementation-kit/tools/generate-protocol-candidate.mjs`
   升级，**11 项输出点**：四个顶层常量（`BASE_ID`／`candidateVersion`／`profileId`／
   `protocolVersion`）、`integration-slices/index.json`（`schemaVersion` 与 `definition`
   块）、`manifest/release.json`、`tools/g1-validate.mjs`、`tools/finalize-manifest.mjs`、
   `compatibility/` 两个、`docs/` 三篇、`package.json`；**新写** `schemas/governance/` 三
   个 schema 与 `vectors/CV-DEMAND-ACCEPT-TO-PICKUP/`；**删除** `approvals/release-approval.json`
   的写出。
2. 消息面 54 → **63**，错误码 43 → **45**，向量 19 → **31**，切片家族表由 8 行改 **16 行**。
3. 票 06 交来的三条实现缺陷：三个不在注册表里的错误码改名、删 `appsettings.json:9` 的死配
   置、`ManualChargingReturnToServiceRequested`／`Result` 两端实现。
4. 票 06 交来的两条架构测试：两端各一条「源码里所有 reasonCode 字面量 ∈ 注册表 enum」。
5. **删 `runner/` 两个 schema**（票 08），必须在同一次候选生成里做——它改 content manifest
   哈希，而哈希进 attestation 与 tag。

**体量可行性有实测支撑，不是估的。**票 06 曾判「重生成约 1500 个 invalid 样例、而仓库里没
有生成器」是 v2 落地的最大单项；票 07 查出生成器存在（595 行，写出整棵树），票 09 在
`vm01` 上实跑：**一次 `node` 调用产出 1504 个文件，与协议仓 v0.1.1 的 1516 个文件逐字节比
对，相同 1493 个**，含 `examples/` 全部 1395（54 valid ＋ 1341 invalid）、全部 57 个 schema、
19 个向量的 38 个文件。**那 1341 个 invalid 样例不是工作量**，真实提前量是改那个 66 KB
`.mjs` 的 11 项输出点。

**引用票 06 的 3.7 第 2 项时必须带上这条纠正。**本图不回溯改旧票据，`06-answer.md` 里那句
估算原样留着，但它已被实测推翻。

**批次 1 不含**两端实现 v2、`FP-IS-00`～`07` 重证、161 个 trait 重打标——那三项在批次 2
轨 A。**冻结面落地与两端跟上是两件事。**

### 3.3 十项无条目载体的工程

| # | 工程 | 批次 |
| --- | --- | --- |
| 1 | 协议 v2 候选生成（生成器 11 项输出点、9 条新消息、错误码 45、向量 31、切片表 16 行） | 1 |
| 2 | 三条实现缺陷修复 ＋ 两条 reasonCode 架构测试 | 1 |
| 3 | 协议 v2 两端实现 | 2 轨 A |
| 4 | 161 个 `[Trait("IntegrationSlice", ...)]` 重打标（**必须与「v2 变更后逐个复核测试」合并进行，不单列**） | 2 轨 A |
| 5 | **B2 多车**（13 项：`OnboardPeer.Attach` 的 N 会话、`MT_WAIT_FOR_CHECKPOINT` 识别、单 worker 按车串行 ＋ 每车超时预算、`agvId × taskType` 表、区→车硬集合） | 2 轨 B |
| 6 | **`RouteGraphSnapshot` 路网成本引擎** ＋ `riot-sdk` 新增五个具名 Facade 方法 ＋ 发一版 ＋ 控制服务端升 vendored 包 | 2 轨 B |
| 7 | **RIoT 订单命令面**（`CANCEL`／`OrderHold`／`OrderContinue`／`HangContinue`／`triggerEmergency`／`cancelEmergency`，继承 `RIoTRetryReconciliation` 对账语义） | 2 轨 B |
| 8 | **RIoT 白名单架构测试**（`src/` 下 `.Raw` 零命中 ＋ 调用集合 ⊆ 获批清单）。**不挂 `FP-C4`**——否则 `FP-C4` 一延后，整个 RIoT 调用面的守卫跟着延后 | 2 轨 B |
| 9 | **版本化配置快照与不可改写审计**（`FP-C7`／`FP-C9b`／`FP-C5` 三簇共用） | 3 |
| 10 | `STAGING_TO_WIRE` 启用（推翻 I6，`BuildRouteEvidenceId` 起终点互换编译期静默） | 4 第二阶段 |

### 3.4 批次间依赖：一个 DAG，不是一条链

```
        ┌──────────────┐
        │  1  协议 v2  │───────┐
        └──────┬───────┘       │
               │               │
      ┌────────▼────────┐      │
      │ 2 轨A v2两端实现 │      │
      │   FP-IS-00～07   │      │
      └────────┬────────┘      │
               │               │
   ┌───────────┼───────────┐   │
   │           │           │   │
┌──▼────────┐  │      ┌────▼───▼──┐
│ 3 治理面  │  │      │ 4 六类任务 │
└──┬────────┘  │      └────┬──────┘
   │           │           │
   └───────────┼───────────┘
               │
   ┌───────────▼──────┐        ┌──────────────────┐
   │ 5 用途占有+空闲返回│◄───────│ 2 轨B 调度地基    │
   └───────────┬──────┘        └────────┬─────────┘
               │                         │
   ┌───────────▼──────┐                  │
   │ 6 多停靠计划 B3   │◄─────────────────┘
   └───────────┬──────┘
               │
   ┌───────────▼──────┐      ┌──────────────┐
   │ 7 车载选任务 B5   │─────►│ 8 自动充电    │
   └──────────────────┘      └──────────────┘
```

**十一条边，每条都归约到一条已推翻的不变量、一条协议前置、一条切片 `prerequisites` 或一条
现场前置**，没有一条是「先做这个更稳妥」：

| 边 | 理由 |
| --- | --- |
| 2轨A ← 1 | 两端不可能实现一个还没冻结的 schema 面 |
| 3 ← 2轨A | **只约束证据，不约束实施**：`FP-C7`／`FP-C8` 的服务端代码可以立刻开工，但 `FP-IS-14`／`FP-IS-15` 的 `prerequisites` 是 `FP-IS-00`，联调证据要等 v2 重证 |
| 4 ← 1 | `workType` 用 MES 原始字面值是 breaking，必须落在 v2 里 |
| 4 ← 3 | `FP-C8` 看板必须先于 `FP-C9b` 的 `REQ-0340`「可疑绑定立即收紧」入口——看板是本期唯一人机界面；配置快照大件同样先于 `FP-C9b` |
| 5 ← 2轨B | 票 02 的 `B2 → (B1+B4)`；`REQ-0292` 要求同一份新鲜快照原子取得车辆与等待点，而快照新鲜度由单 worker 串行保证 |
| 5 ← 4 | `REQ-0204` 归 B4 后，B4 的落地依赖 `FP-C9a` 先提供 `FixedTaskStation` 绑定抽象——公共业务点独占的单位就是它，而它零实现 |
| 6 ← 2轨B | 引擎给边际成本与可达性；命令面给有界删除（`REQ-0197` 删已建单停靠要先 `CANCEL`）；`REQ-0164` 的 0/1 门禁要求 `CANCEL` **完成对账**后才能建新单 |
| 6 ← 5 | 票 02 的 `(B1+B4) → B3` |
| 7 ← 6 | 票 02 的 `B3 → B5`；`FP-IS-09 ← FP-IS-08`（没有多 Demand 计划就没有可选的任务） |
| 8 ← 5 | `REQ-0178` 清桩用等待点集合；且**正常充电完成后离桩也要靠取得新用途**，其中一条就是空闲返回 |
| 8 ← 2轨B | `REQ-0170` 改派前要 `CANCEL` 旧 HANG、`REQ-0178` 清桩前要确认取消终态，都要命令面 |
| 8 ← 7 | **仅证据边**：`FP-IS-13 ← FP-IS-12`。实施上 8 不依赖 7 的车载选任务 |

**可并行的**：批次 1 与批次 2 轨 B 完全独立（一个在协议仓与生成器上，一个在服务端 `src/`
上）；批次 3 的服务端实施与批次 2 全程并行；批次 4 与批次 5 在各自前置满足后可并行。

**严格串行的只有 `2轨B → 5 → 6 → 7`**，它由不变量推翻顺序决定，不可重排。

### 3.5 批次内的顺序约束（不得倒置）

| 约束 | 批次 |
| --- | --- |
| `REQ-0171`（独占充电桩名册）先于 `REQ-0170`（改派） | 8 |
| `REQ-0289`（专用等待点登记）先于 `REQ-0293` | 5 |
| `FP-C9a` 先于 `STAGING_TO_WIRE` 那一批 | 4 |
| `FP-C8` 看板先于 `FP-C9b` 的 `REQ-0340` | 3 → 4 |
| 版本化配置快照与审计大件先于 `FP-C7`／`FP-C9b`／`FP-C5` | 3 |
| **`REQ-0259` 的 IO 完整性门禁必须与三台现有车的 IO 录入同批落地** | 3 |
| 命令面的 `CANCEL` 必须完成对账才能建新单 | 2 轨 B → 6 |

**`REQ-0259` 的表述必须取收窄后的版本。**基线原文两处都写「**整车**」——「全部仓位必须具
有完整并经实际核对的 `SlotIoBinding`，**整车**才达到 `SlotConfigurationReadiness`，在此之
前**整车**不得取得业务就绪」；`REQ-0263` 的「不允许抽样」也是**在一台车之内**（禁的是一台
车里抽几个仓测），不是「三台车不能分批」。

所以门禁是**每车判定**，三台车可以逐台推进，处置是 **W1 窗口内「先核对后启用」**：门禁在
第一台车核对通过之后再上线，**零停产**。

**「三台现有车会同时失去业务就绪」这个说法只在「先启用后核对」这一种排法下成立，而那种排
法没有任何需求依据**——`REQ-0259` 只规定「未达 readiness 不得业务就绪」，没规定门禁必须先
于核对上线。票 09 的 3.3 与票 08 票据正文里读起来像不可避免的那句，取本节的纠正版。

### 3.6 每个批次的现场前置与投运参数

| 批次 | 现场前置 | 投运前须批准的参数 |
| --- | --- | --- |
| 1 | 无 | 无 |
| 2 | 无 | `REQ-0302`：目录同步周期与最大允许未确认时长（两个值，后者须大于前者） |
| 3 | 三台车的 IO 录入与逐仓现场核对 | 无 |
| 4 | 四个公共站点功能在 `mapId` 25 上尚不存在，验收期只有 `WIRE_TO_GATE` 能真实触发 | 无 |
| 5 | 等待点尚未测绘进 RIoT 地图 | `REQ-0289` 的等待点登记 |
| 6 | 无 | `REQ-0203` 防饥饿阈值；`REQ-0198` 每区途中追加最大允许值 |
| 7 | 无 | 无 |
| 8 | **三个充电桩物理上还没安装**；装完后哪些 id 是充电桩**只能问用户** | `REQ-0171` 独占充电桩名册；`REQ-0282` 的 `ChargingPolicyVersion` |

充电桩身份**永远不可从 RIoT 观测推导**：8005 自建充电机制下充电桩是普通站点（用 RIoT 本体
充电机制才需要把站点设成充电桩 `type`），`ProjectExclusiveChargingStationRegistry` 是唯一
来源且不可交叉校验。已确认不会有其它项目的车占用 8005 的充电桩，故站点占位判据只需覆盖本
项目车辆。

*追溯：票 09 的 Q1～Q6 与 3.1～3.4、票 08 的 1.9 与 3.3、票 04、票 12、票 13。*

---

## 4. 重构与增量的分类与排序规则

### 4.1 判据

**判据是「推翻一条有代码或契约位置的现行架构不变量」**，不是主观的「改动大不大」。

| 不变量 | 内容 | 对应判据 | 识别于 |
| --- | --- | --- | --- |
| I1 | 车辆占用必由 Demand 引起 | B1 | 票 02 |
| I2 | 单车单 journey | B2 | 票 02 |
| I3 | 单 Demand 两段固定行程 | B3 | 票 02 |
| I4 | 站点无独占 | B4 | 票 02 |
| I5 | 车载对 Demand 只读 | B5 | 票 02 |
| I6 | 站点任务类型准入必在装货腿检查并冻结 | — | **票 13 补充识别** |
| I7 | 车载持有并声明自身仓位配置，服务端只记录不裁决 | — | **票 05 补充识别** |

I6 的代码位置：`WireToGateStore.cs:795-800` 明文
`"Only LOAD may carry a complete station/task admission identity."`，而准入表键在 AREA 机
台站上——`STAGING_TO_WIRE` 方向反转后 AREA 站是卸货端，故推翻 I6。
I7 的代码位置：车载 `Configuration.cs:270-272` 两个硬编码默认值
`SlotModelVersion="eight-slot-v1"` 与 `ActiveSlotConfigurationVersion="eight-slot-modbus-v1"`，
由 `WireToGateSessionClient.cs:402-403` 自报给服务端，而服务端 `SlotTemplate`／
`ActiveSlotConfiguration`／`SlotConfigurationVerification`／`VehicleConfigurationMaintenance`
等八个标识符全部零命中；`REQ-0258`（服务端是唯一权威维护入口）与现状**方向相反**。

**这套判据集被发现不完整三次**（I6、I7，以及票 12 查出 B1 的定义条款载体缺失），三次都是
补充识别而非推翻票 02。`CONTEXT.md` 的措辞是「已识别五条」，不是穷举封闭。

### 4.2 分类结论

票 02 当时的 62 条判为 **16 条重构、46 条增量**，逐条无遗漏。此后待排期条目增至 131 条，
新进入的条目按同一判据归类，逐条归属见剖面 TSV 的第 9 列 `ClusterBasis` 与票 02 决议的逐条表。

**全新能力不等于重构**——充电 17 条里 13 条是建在新原语之上的增量。

### 4.3 排序规则

**不用「重构整体先于增量」**，用：**每条增量不早于它所依赖的那条不变量的推翻**。这条规则
使 23 条治理面增量可以从第一天并行，而不必等在任何重构后面。

**重构内部顺序固定为 `B2 → (B1+B4 一起) → B3 → B5`**，落到批次即 2 → 5 → 6 → 7。

两条必须记住的纠正：**充电依赖的是等待点而非多车调度**（`REQ-0178`）；**348 条里没有任何
一条要求「系统支持多辆车」**，B2 因此无需求条目载体，只出现在第 3.3 节的工程表里。

*追溯：票 02 全文、票 13 的修订段、票 05 的 I7、票 12 的修订段。*

---

## 5. 各业务面的范围决定

每一面写清做什么、不做什么，以及不做的是**延后**还是**范围外**。形态的定义见第 11 节。

### 5.1 多车并发、车辆占用与 Worklist 执行模型（`FP-C2`／`FP-C3`，批次 2／6／7）

**做**：B2 全开（多车并发）、B3 档 2（多停靠计划与途中追加换序）、B5 幅度 1（车载选任务）。
16 条全部有归属（9 重构／7 增量），**无一条延后到本图之外**。

具体定案：选车走**档 β**（真实路径成本 ＋ 零容差）；防饥饿机制实施而阈值留空；`REQ-0185`
复用 `AdmissionPolicy` 版本化；N 车配置用 `vehicles` 数组；B5 只推翻 select；多车用**单
worker 按车串行 ＋ 每车超时预算**；**唯一性从 lease 表下移到 `OrderIntents`**（
`DispatchUniquenessGuard` 因此一字不改仍成立）；`REQ-0328` 取集合 B 且仅未取货；
`REQ-0219` 取五字段回显；`OperationSession` 每 Demand 一个。

**途中追加与换序按完整能力实施**（票 14 依 Round 43 实测定案，撤销了票 03 的 fail-closed
形态）：边际成本用**计划锚**（自插入位的前一站起算）——车当前位置到计划下一站那一段在插入
前后完全相同、做差必然抵消，故计划锚是**精确值不是近似**；**可达性权威迁到自建图**；
`REQ-0197` 两半合并成一行。

**不做**：无。本面无延后条目。

### 5.2 自动充电桩调度与充电失败治理（`FP-C1`，批次 8）

**做**：全链路自动化、清桩闭环一次做完、备用桩改派进本期。**19 条一条不延后。**

`FP-C1` 整簇在控制服务端**零实现**（20 个标识符全零命中，`src/` 里含 `Charg` 的只有 3 行）。

具体定案：分配核心共用但排序键不合并（先判用途再选资源）；充满不主动腾桩（RIoT 机制如此）；
四个人工动作按「对象里有没有车」分两端，协议增量压到两对消息；名册走受控预置配置不做 UI。

**名册为空取「退化到 `ManualChargingHold`」而非静默**——与等待点的处置不对称是因为后果不
同：车原地不动无害，车退出服务不能无声。

**充电订单不是单段 move**（见 1.3 第 3 项），这是本面最大的工程发现。

**不做**：无延后条目。

### 5.3 治理面增量（`FP-C5`／`FP-C6`／`FP-C7`／`FP-C8`／`FP-C10`，批次 3 与延后）

**做**：`FP-C7` 连地基一起做（14 条）、`FP-C5` 做最小闭环（7 条）、`FP-C8` 看板做（3 条）、
`FP-C9b` 保留在本期。
**延后**：`FP-C10` 人员认证与账号整簇 8 条、`FP-C6` 账号权限与密码治理整簇 8 条。

**一条口径必须立住：完整产品没有任何人员认证。**这不是「砍掉了可调条目、账号密码继续靠部
署时预置配置管理」——查实**没有账号也没有密码可以「继续」**：控制服务端 `src/` 里
`SystemAdministrator`／`MaintenanceAdministrator`／`AdministratorAccount`／`PasswordHash`／
`LoginSession` 全部零命中，28 张持久化表既无账号表也无管理员审计表；唯一的管理员身份是消
息 payload 里的 `administratorRole` 字符串，唯一的认证是 `OnboardRecoveryCoordinator.cs:1006`
对一个环境变量做定时安全比较——**全场共用一个密钥、不识别人、也不区分角色**，持有密钥者可
以自称 `SYSTEM_ADMINISTRATOR`。车载端同样零命中，`operatorId` 来自环境变量、
`AdministratorRole` 硬编码为 `MAINTENANCE_ADMINISTRATOR`。

**由此得出的界面规则**：无认证前提下，人机界面上**只允许 fail-safe 方向的动作**。暂停、收
紧、阻断可以长在界面上；恢复、激活、回滚、投运一律走受控预置配置 ＋ 版本化审计。理由是前
者最坏后果是运力下降，后者最坏后果是绕过安全门禁。配套的判断标准是**「变更时机能不能等停
机窗口」，不是「频率高不高」**。**本期唯一的人机界面是 `REQ-0268` 的看板**，它也是控制服
务端历史上第一个界面（`ControlServer.sln` 11 个工程里没有任何 WPF／Blazor／Razor）。

其余定案：配置审计取版本级不可变完整快照（字段级差异按需计算不另存）；回滚影响边界统一为
「各消费者在自己的冻结点固化版本」；AGV 生命周期取两个正交维度，且业务可用性是 fail-closed
谓词链的**派生量**不是可写状态；`REQ-0185` 与 `REQ-0212` 的两份名单**不做运行期在线修改**
——它们复用的 `AdmissionPolicy` 机制已经就是部署期配置 ＋ 版本化审计（本图唯一一处「现状
即结论」）。

### 5.4 六类任务执行与公共站点绑定（`FP-C9a`／`FP-C9b`，批次 4）

**做**：六类 MES 运输任务的执行能力**一次建齐**，投运范围由现场绑定逐类 fail-closed 决定。

六类真名（工厂 IT SQL 六个 `UNION ALL` 分支的硬编码字面量）：`DIE_TO_WIRE_STAGING`、
`DIE_TO_OVEN`、`WIRE_TO_GATE`、`WIRE_TO_OPTICAL`、`STAGING_TO_WIRE`、`WIRE_TO_NITROGEN`。
**`WIRE_TO_GATE` 不是「MVP 阶段的命名」**，它就是 MES 的真实 `TASK_TYPE` 之一；自造的是
`profileId` 的 `WIRE_TO_GATE_MVP`。

**摄取侧无事可做**——MesIngest 已全量摄取六类、无任何 `TASK_TYPE` 过滤，本簇是「只加执行」。

**承载它的不是新需求**，而是 348 行里被误判批次 0 的 17 条公共站点绑定条目（整簇零实现：
`PublicStationFunction`／`FixedTaskStation`／`PublicStationBindingSetVersion`／
`TaskTypePublicStationRuleVersion`／`MapPublicStationRequirementSet`／`PublicStationBindingHold`
六个标识符在控制服务端 `src/` 全部零命中，被一个 `gateStationId` 标量在事实上顶替）。

其余定案：六类走**同一套配置驱动机制**而非六份代码分支（方向是规则里的字段不是 `if/else`）；
治理取乙档（数据模型 ＋ fail-closed 校验落地为 `FP-C9a` 8 条，版本化／暂停／回滚／审计为
`FP-C9b` 9 条）；**`STAGING_TO_WIRE` 单列后一批**（风险隔离，不是省事）。

### 5.5 空闲返回与等待点独占（`FP-C4`，批次 5）

**做**：B1 取得独立的 `VehiclePurposeClaims` 新表（主键 `VehicleKey`）取代 lease 表；B4 取
`(MapId, StationId)` 复合键、一行两状态、离点证据释放；空闲返回作为一个停靠进入计划，为此
给停靠加**第三个正交维度 `StopPurposeCategory`**（`BUSINESS`／`WAITING_POINT`／`CHARGER`）。

`Purpose` 四值枚举一次定全：`TRANSPORT`／`CHARGING`／`CLEARING_MAINTENANCE`／`IDLE_RETURN`。
不加隔离级别，改为捕获唯一约束冲突。`REQ-0291` 全量重评全量实现。`REQ-0294` 取架构测试
（横切工程，不属 `FP-C4`）。

**等待点数量 `n` 不写进规格**：`REQ-0289` 的登记表述为配置驱动的可空集合
（`MapWaitingPointPool`）。现场事实是 Round 43 实测 mapId 25 的 206 个站 `type` 恒为 1、
`desc`／`param`／`udp` 全空、站名只有 `N#-#`／`T##-##`／`关卡` 三形态，**没有一个是等待点
或充电桩**——等待点物理上在厂区但尚未测绘进 RIoT 地图。

**离点确认证据组合没有需求条目载体**，作为实施决策加注、不表述为需求：基线只定了到点确认
（`REQ-0295`），离点侧只有 `REQ-0293` 一句「确认车辆实际离点后才释放」。票 12 定的四项组合
（`currentMap` 仍是本图 ＋ `currentPosition` 不再精确匹配 ＋ 车辆处于运动态 ＋ 证据新鲜无冲
突）是实施决策，与 B2 无需求条目载体是同一类情况。

**`byDefaultMissions` 是 URL 路径段不是请求体字段**：请求体字段叫 `mission`（单数、数组、
必填），响应侧才叫 `missions`。基线 `REQ-0294` 与 `CONTEXT.md:751` 的写法在代码语境下会被
读成字段名，此处只记录正确读法，不改基线。

### 5.6 路网成本引擎与建单前置门禁（`RouteGraphSnapshot`，批次 2 轨 B）

**做**：新建 `RouteGraphSnapshot` 路网成本引擎。它是本图最大的单端工程之一，且**不属任何
簇、没有切片**（单端：服务端↔RIoT）。

快照形态：**双周期刷新 ＋ fail-closed**——设计态按 `gmtUpdate` ＋ 10 分钟 TTL 兜底，运行态
移除集独立 10 秒周期；`mapEdgeGroup` 指纹变化或动态代价由空变非空即进陈旧态。

**引擎成为派车链路的硬依赖，快照陈旧即本轮不派车。**它不可用时失去的不只是成本排序层（那
一半可退到 `DeterministicDispatchTieBreak`），可达性那一半没有退路。**排期上引擎是可与 B2
并行的旁路大件，但必须先于任何多车派车能力上线。**

**建单前置 `RouteCost` 门禁保留**，这一条收窄了票 14 的「`getRouteCostsBy` 一律退出」。分工
不是折衷，是两个 API 各自能力的自然归属：选车阶段问「站 A 到站 B」，`getRouteCostsBy` 起点
恒为车当前位置、答不了，用自建图；建单前置问「这台车此刻能不能到那个站」，**那正好就是
`getRouteCostsBy` 唯一能答的问题**。五条基线条目明文要求它：`REQ-0147`／`REQ-0293`／
`REQ-0302`／`REQ-0305`／`REQ-0345`，而该门禁在 `src/` 里 `RouteCost` **零命中**——从没实现
过。两个证据源分歧时**阻断建单并告警**。`queryNearEnd`／`queryNearestStart` 的全面退出不变。

**RIoT 调用白名单已正式扩五个 `imap` 只读端点**（用户 2026-09-04 批准），且**产品代码必须
走具名 Facade**，不得使用 `.Raw`。落地形态是在 `riot-sdk` 里新增具名 Facade 方法（自定义反
序列化落在 SDK 内部：snake_case、`s_node`／`e_node`、站点侧键名字面带点）。这给引擎添了一
段真实提前量：**`riot-sdk` 要发一版、控制服务端要升 vendored 包**。

**`REQ-0309` 里的第二条 Edge 禁止不冲突，不进 `CP-0001`。**该条写着「缺失能力**不得**以手
工录入、**Edge 数据**或未授权接口补洞」。论证：该句主语是「目录」，禁的是目录同步能力有缺
失时拿 Edge 顶替目录；`RouteGraphSnapshot` 不顶替目录——目录仍由 `MapStationCatalogSnapshot`
承担，引擎是独立的可达性与成本证据面。**这个论证必须留在规格里，否则下一个人会重新撞上同
一条。**反向收益：`REQ-0309` 同一句还写着「只能经已批准的 RIoT Map/Station 只读调用面和
**具名 Facade** 获取目录」——这是「产品代码必须走具名 Facade」的第二个需求载体，而且比那份
scratch 白名单票据稳。

### 5.7 RIoT 订单命令面与故障隔离（`FP-C11`，批次 2）

**做**：接入 `CANCEL`／`OrderHold`／`OrderContinue`／`HangContinue`／`triggerEmergency`／
`cancelEmergency`，继承 `RIoTRetryReconciliation` 对账语义。

这一簇的退化形态含**安全能力**：`OrderHold`／`OrderContinue`／`HangContinue`／`CancelOrder`／
`triggerEmergency`／`cancelEmergency`／`EmergencyStop` 两端源码**全部零命中**，
`VehicleFaultIsolation`／`FaultedVehicle` 同样零。**MVP 的阻断只作用于 8005 自己的派车与仓
门，不作用于 RIoT 订单与车辆急停**——进入阻断只会停止建新单、按不住已发出的订单，无法证明
停车时不会自动触发急停。

**一个同名不同物的陷阱**：服务端 5 处 `DispatchDisable` 全是 `CreateDispatchDisabled`
（8005 自己的建单开关），与 `REQ-0167` 说的 RIoT 侧车辆 `DispatchDisable` 是两回事。

该发现已按用户 2026-09-04 的决定在 `8005-agv-control-server` 开缺陷单
（[`8005-agv-control-server#1`](https://github.com/trytoreachpeak0/8005-agv-control-server/issues/1)），
交 MVP 侧判断是否影响当前 P0～P7 试运行。**本规格不代 MVP 侧作答。**

### 5.8 维护开门模式（`FP-C12`，延后）

**延后整簇 6 条**（`REQ-0225`～`REQ-0230`，用户 2026-09-04 定）。三条理由：`REQ-0226` 要求
在车载端**即时重新认证**而本期无认证模型；它的业务目的（光幕漏检导致产品锁在仓内、需要人
开仓取出）**已有一条路**——`ExceptionRecoverySession`（160 命中）加强制机械取出
（`ForcedMechanical` 13 命中），两者在服务端都真实实现了；做它需要新协议消息，等于当场推
翻票 06 刚做的一次冻结并把已定为批次 1 的 v2 撑大。

**延后不是作废**，Lifecycle 仍 `active`。

### 5.9 跨 Map 运输（范围外）

**判为本图 Out of scope，Destination 不变，基线不动。**详见第 13.2 节。

*追溯：票 03、票 14、票 04、票 05、票 13、票 12、票 15、票 11、票 09 的 1.7～1.9。*

---

## 6. 协议 v2 冻结面

**冻结强度：设计面已冻结、可据以实施；不等于「可发布」。**切一个 `ProtocolRelease` 还欠的
东西见 6.6。

### 6.1 身份三元组

| 项 | v1 | v2 |
| --- | --- | --- |
| `protocolVersion` | 1 | **2** |
| `profileId` | `WIRE_TO_GATE_MVP` | **`AGV_FULL_PRODUCT`** |
| `releaseVersion` | `0.1.1` | **`1.0.0`** |
| schema `$id`／`$ref` URI 段 | `wire-to-gate/v1` | **`agv-full-product/v2`** |
| tag | `protocol-v0.1.1` | `protocol-v1.0.0` |

**`ProtocolVersion` 2 ＋ release major 同升不是选择**——`docs/release-governance.md` 第 9 条
明写这十一类变更强制两者同升。`AGV_FULL_PRODUCT` 与 `WIRE_TO_GATE_MVP` 同构：阶段名，不带
版本号，版本活在 `protocolVersion` 与 `protocolReleaseVersion` 里。

### 6.2 消息面：63 条

| 类 | 条数 | 内容 |
| --- | --- | --- |
| 沿用且 payload 一字不改 | **49** | 只随身份三元组与 URI 改 |
| payload 变更 | **5** | `UpcomingStopPlanSnapshot`、`CurrentStopWorklistSnapshot`、`CapabilitySnapshot`、`SafetyStateSnapshot`（记录用，payload 不改）、`VehicleBusinessStateSnapshot` |
| 新增 | **9** | 见下 |
| **合计** | **63** | denylist 11 条不动 |

九条新增全部取「**单条 `Result` 带 `outcome` enum ＋ 可空 `problem`**」范式，不取
「Accepted／Rejected 拆两条」范式——后者省下 4 条 schema 与约 100 个样例：

| # | 消息 | 方向 | 交付类别 |
| --- | --- | --- | --- |
| 1 | `DemandSelectionRequested` | O_TO_C | REQUEST |
| 2 | `DemandSelectionResult` | C_TO_O | RESPONSE |
| 3 | `UnableToChargeFieldConfirmationRequested` | O_TO_C | REQUEST |
| 4 | `UnableToChargeFieldConfirmationResult` | C_TO_O | RESPONSE |
| 5 | `ManualStationClearanceConfirmationRequested` | O_TO_C | REQUEST |
| 6 | `ManualStationClearanceConfirmationResult` | C_TO_O | RESPONSE |
| 7 | `SlotConfigurationActivationCommand` | C_TO_O | **RELIABLE**，`recoveryRole` 新增 `SLOT_CONFIGURATION` |
| 8 | `SlotConfigurationActivationResult` | O_TO_C | **RELIABLE**，`PENDING_RESULT_REPLAY` |
| 9 | `OnboardAlarmSnapshot` | O_TO_C | **SNAPSHOT** |

**7／8 必须走 RELIABLE 而不是 REQUEST/RESPONSE**：`REQ-0264` 的「不能猜测成功」正是
`PENDING_RESULT_REPLAY` 存在的理由；用 RESPONSE 就没有补报语义，断线即丢。

**告警走快照而非事件流**：`REQ-0269` 禁「已过期」展示状态，而事件流断线重连那段正是它。
**告警 code 不复用 `ErrorCode`**——开放集合塞进封闭 enum 等于每个故障码发一次 breaking。

主要 payload 变更：`UpcomingStopPlanSnapshot` 的 `legs.maxItems` 2 → **9**、新增
`stopPurposeCategory`／`demandId`／`publicStationFunction`、`legType` 改
`["TO_PICKUP","TO_DROPOFF"] | null`、顶层 `demandId` 去掉、dedup 键改 `["planRevision"]`；
`CurrentStopWorklistSnapshot` 的 `items.maxItems` 1 → **8**、`workType` 改六值 MES 原始字面
值、`stopRole` 改 `["PICKUP","DROPOFF"]`、dedup 键改 `["worklistRevision"]`。**两个快照的
dedup 键统一改用 revision**，因为 `items[].demandId` 在 `maxItems` 1→8 之后变成多值键、语义
无定义。`CapabilitySnapshot` 新增 `activeSlotConfigurationFingerprint`（`REQ-0264`／
`REQ-0266` 本期就要指纹，54 个 schema 里 `fingerprint` 零命中）。`slotStates` 保持定长 8。

### 6.3 类型层与错误码

新增四个 `$defs`：`StopPurposeCategory`（三值）、`PublicStationFunction`（五值）、
`TransportTaskType`（六值，MES 原始字面值）、`AlarmEntry`。新增而非内联，是因为前两个各要
出现在两条消息里，内联会制造第二份真相。

**错误码 43 → 45**（`appendOnly` 不破）。**不为控制端那三个表外码开口**——
`PROTOCOL_RELEASE_MISMATCH`／`RECOVERY_AUTHENTICATION_REQUIRED`／
`RECOVERY_SESSION_ALREADY_OPEN` 判为实现缺陷，改名。

**它们一直没被抓到，是因为两端都不做运行期 schema 校验**：两个实现仓的依赖清单里没有任何
JSON Schema 库。据此要求两端各加一条**「reasonCode 字面量 ∈ 注册表」架构测试**——那是「协
议仓的 enum」与「实现真正发出的字节」之间目前**唯一缺失的一条校验**。

### 6.4 向量与切换规则

**向量 20 → 31**，命名沿用 `CV-<场景名>` 不带编号，`productAssertions` 由
`W2G-IS-01` 的特例推广为**全量必填**。切片绑定见第 7 节。

**不引入版本协商**：沿用精确 `ProtocolVersion` ＋ 精确 `ProtocolReleaseIdentity`，两端同一
个 CD 包同窗口替换，窗口内旧版车被**带期望身份地拒绝**——版本错配是一条带完整期望身份的说
明性错误，不是「连接被拒而无解释」。

### 6.5 协议向量的绑定强度：弱绑定，如实记录

**协议向量从未被任何东西机械执行过。**五套断言执行器全查过——`run-staged-g3.ps1` 2899 行、
`run-staged-g3-restart.ps1` 930 行、`run-demand-bearing-g3-vectors.ps1` 771 行、`scripts/l2/`
1307 行——`vectorId` 与 `input.ndjson`／`expected.json` **全部零命中**；`test-wire-to-gate.ps1`
只把 `vectorId` 写进 `gate-result.json`。**近 6000 行 PowerShell 加 268 项 xunit，没有一套读
协议向量文件。**

**决定不建第五套执行器**（用户 2026-09-04 定）：删 `runner/` 两个 schema，改用一条「每个
`vectorId` 在实现仓有同名具名测试」的架构测试，把人写的引用变成机械可检查的绑定。

**代价如实记录**：G2 的「向量即判据」**永久是弱绑定**——机械保证的是「这条向量有对应测
试」，不是「它的字节被执行过」。

### 6.6 实施图还欠什么才能切一个 `ProtocolRelease`

1. 写 schema：54 条改身份三元组 ＋ 5 条改 payload ＋ 9 条新增 ＋ 类型层 4 个新 `$defs`。
2. **重生成 examples 树**——由生成器机械产出，**不是最大单项**（3.2 已推翻票 06 的估算）。
3. 写 31 个向量的 `input.ndjson` ＋ `expected.json`，全部带 `productAssertions`。
4. 改十处门禁硬编码（`g1-validate.mjs` 的 `requiredVectors`／切片全表／
   `worklistItems.maxItems`／顶层 `demandId` 可空、`runner-contract.schema.json` 的 slice
   pattern、`ControlServer.Conformance/Program.cs:11` 的同一 regex 第二份副本、
   `ProtocolCandidateIdentity.cs` 的 9 个常量、删 `appsettings.json:9`）。
   **`g1-validate.mjs` 硬编码了 v1 的形状**：第 25 行的 `worklistItems?.maxItems===1` 与
   「顶层 `demandId` 必须支持 null」与本图定案**直接冲突**，不同步改则 G1 必红。
5. `pnpm manifest:finalize` ＋ `pnpm g1` 跑绿。
6. **两名产品负责人的外部 attestation ＋ annotated tag `protocol-v1.0.0`**（见第 12 节）。
7. 两端实现 ＋ `CONTROL_SERVER_G2` ＋ `ONBOARD_HMI_G2` ＋ `G3`。

### 6.7 治理文档的陈旧与一处未证项

**两类要分开表述，不要混成一句「治理有问题」。**

**陈旧的是叙述性文档，发布身份本身健全**：`protocol-v0.1.1` 的 annotated tag 已经打了（记
着四个 SHA-256），而 `docs/candidate-limitations.md` 仍写着「两人批准之后 `protocol-v0.1.1`
才能被创建」；`compatibility/report.json` 的 `status` 是 `SUPERSEDING_CANDIDATE`、
`ProtocolCandidateIdentity.ApprovalStatus` 是 `APPROVED_RELEASE`、`manifest.status` 是
`CONTENT_SNAPSHOT`，三处口径不一。

**一处未证项**：`protocol-v0.1.1` 的 attestation 是外部 GitHub Release Asset，**本图未核验
其内容**——tag message 里记着它的 SHA-256（`89f67c82…`），结构上流程走过了，但两名批准人
是谁、签名是否真实存在，本图未证。

*追溯：票 06 全文、票 07 的 1.5 与 1.8、票 08 的 1.3 与 Q2、票 09 的 1.5。*

---

## 7. 切片家族 `FP-IS-NN`

### 7.1 新旧关系：替换

**取 `FP-IS-NN`（`^FP-IS-[0-9]{2}$`），16 个切片，替换 `W2G-IS-00`～`07`。**

三种备选里**两种不成立、一种做不到**：「替换会作废证据链」不成立——证据由
`ProtocolReleaseIdentity` 换代作废，与编号无关；「沿用难区分证据」不成立——`gate-result.json`
有六项发布身份，真实代价是永久名实不符 ＋ trait 歧义；「并存」结构上做不到——schema 锁
`minItems/maxItems: 8`，且 v1 的 `index.json` 活在不可变 tag 里，一个仓一个路径，**并存就是
替换换个说法**。

**批次与业务簇都不进 id**：批次是循环依赖（批次由票 09 定而票 09 被票 07 阻塞），业务簇是
稳定性（本图已改判簇归属五次，而 id 活在 161 个测试 trait 与不可变证据目录里）。业务面由
`definition.scope` 承担。

### 7.2 家族全表

| id | seq | prereq | `definition.scope` | 面 | 批次 |
| --- | --- | --- | --- | --- | --- |
| `FP-IS-00` | 0 | — | `SESSION_HANDSHAKE_RECOVERY_AND_SNAPSHOT` | FP-B0 | 2 轨 A |
| `FP-IS-01` | 1 | 00 | `DEMAND_ACCEPTANCE_AND_TO_PICKUP` | FP-B0 | 2 轨 A |
| `FP-IS-02` | 2 | 01 | `STATION_PICKUP_AND_MULTI_SLOT_LOAD` | FP-B0 | 2 轨 A |
| `FP-IS-03` | 3 | 02 | `PREDEPARTURE_SAFETY_AND_RESULT_RECONCILE` | FP-B0 | 2 轨 A |
| `FP-IS-04` | 4 | 03 | `DESTINATION_BATCH_UNLOAD` | FP-B0 | 2 轨 A |
| `FP-IS-05` | 5 | 00 | `CONNECTION_LOSS_SAFE_FINISH` | FP-B0 | 2 轨 A |
| `FP-IS-06` | 6 | 00 | `RELIABLE_DELIVERY_AND_RESULT_REPLAY` | FP-B0 | 2 轨 A |
| `FP-IS-07` | 7 | 00 | `EXCEPTION_RECOVERY_AND_MANUAL_RETURN` | FP-B0 | 2 轨 A |
| `FP-IS-08` | 8 | 04 | `MULTI_STOP_JOURNEY_PLAN` | FP-C2 | 6 |
| `FP-IS-09` | 9 | 08 | `ONBOARD_WORKLIST_SELECTION` | FP-C3 | 7 |
| `FP-IS-10` | 10 | 01 | `TASK_TYPE_ADMISSION_FAIL_CLOSED` | FP-C9a | 4 |
| `FP-IS-11` | 11 | 10 | `REVERSED_DIRECTION_JOURNEY` | FP-C9a | 4（第二阶段） |
| `FP-IS-12` | 12 | 04 | `WAITING_POINT_IDLE_RETURN` | FP-C4 | 5 |
| `FP-IS-13` | 13 | 12 | `AUTOMATIC_CHARGING_CYCLE_AND_CLEARANCE` | FP-C1 | 8 |
| `FP-IS-14` | 14 | 00 | `SLOT_CONFIGURATION_ACTIVATION` | FP-C7 | 3 |
| `FP-IS-15` | 15 | 00 | `ONBOARD_ALARM_SNAPSHOT` | FP-C8 | 3 |

**核对**：`vectorIds` 条目合计 34，去重 **31**，与协议 v2 冻结的 31 条恰好相等，无遗漏无多
余。共享 3 例全部沿用 v1。`sequence` 0～15 连续，`prerequisites` 一律指向更小的 `sequence`。
**切片顺序与批次顺序全部一致，无矛盾。**

**「面」列与「批次」列只写在本规格里，不进 `index.json`。**协议仓的 `index.json` 只记契约
事实（id、`sequence`、`prerequisites`、`vectorIds`、`gates`、`definition`）；「`FP-IS-13`
属批次 8」是本图的**计划事实**，写进协议仓意味着一次重新排期变成一次协议变更，而协议变更
要作废两端的门禁证据。

### 7.3 门禁模型不增不减，现场验收不进门禁

门禁仍是四道：`G1 / CONTROL_SERVER_G2 / ONBOARD_HMI_G2 / G3`。`gates` 是每切片相同的
`const`，而现场前置逐簇不同（桩没装、等待点没测绘），**故现场验收不进门禁模型**，它有自己
的证据目录（第 8.4 节）。

`definition` 由可选改**全部必填**；`demandRepresentation` 的三个 `const` 重写为
`authorityModel`（`onboardMode` 由单值改数组，四个取值）——原形态三个字段全是 `const`，充
电／激活／告警切片一个都填不进去。

### 7.4 旧家族证据的引用式（原样保留）

> 批次 0 的跨端能力证据 = `protocol-v0.1.1` 下 `W2G-IS-00`～`W2G-IS-07` 的
> `CONTROL_SERVER_G2` / `ONBOARD_HMI_G2` / `G3` 结果，
> 由 `gate-result.json` 的 `protocolTag` ＋ `protocolRepositoryCommit` ＋ 三个哈希唯一定位。

`FP-IS-00`～`07` 与 `W2G-IS-00`～`07` **一一对应**，关系是「**v2 下的重证**」而不是「可以沿
用的通过结论」——`ConformanceRunIdentity` 词条已规定任一绑定分量变化都必须建立新运行。

**而且根本没有通过结论可以沿用。**`8005-agv-control-server/docs/RELEASE-CANDIDATE.md` 第 12
节末原文：「W2G-IS-00～07 与 RC 目前仍为 `INCONCLUSIVE`，八类 G3 向量各有证据不等于八个切片
通过」。**描述重证时不得暗示存在可沿用的通过结论。**

### 7.5 无切片的十类工作

切片家族**不覆盖完整产品的全部工作**。以下十类没有切片，排期与验收时**不能靠切片计数覆盖**：

| # | 工作 | 无切片的理由 |
| --- | --- | --- |
| 1 | `FP-C2` 的多车并发（B2 那一半） | 保形向量是单会话格式，`steps[]` 无车辆维度，**结构上不可表达** |
| 2 | `FP-C5` AGV 归档恢复与身份连续性 | 单端；恢复入口不在看板、不在车载端 |
| 3 | `FP-C9b` 公共站点绑定运维治理 | 单端；其唯一线上后果 fail-closed 准入已由 `FP-IS-10` 覆盖 |
| 4 | `FP-C6` 账号权限与密码治理 | 延后 |
| 5 | `FP-C10` 人员认证与账号 | 延后 |
| 6 | `RouteGraphSnapshot` 引擎 | 单端（服务端↔RIoT） |
| 7 | 看板本体（`REQ-0268`／`REQ-0269`） | 单端（服务端↔人）；告警的车载端来源那一半由 `FP-IS-15` 覆盖 |
| 8 | `FP-C11` RIoT 订单命令面与故障隔离 | 单端（服务端↔RIoT） |
| 9 | `FP-C13` 建单前置门禁与目录可用性 | 服务端内部门禁 |
| 10 | `FP-C14` 审计留存与导出 | 服务端内部留存 |

（票 09 曾写「七类变九类」，票 08 纠正为**十类**：票 07 的七类 ＋ 票 09 新增的 `FP-C11`／
`FP-C13`／`FP-C14`。不影响任何结论——出口按单端／双端分，不按计数分。）

*追溯：票 07 全文、票 08 的 1.5 与 1.12、票 09 的 Q5。*

---

## 8. 验收边界与证据要求

### 8.1 先认清三层测试模型：它已经建成并在跑

**完整产品的验收边界不是本图发明的。**`8005-agv-program/docs/wire-to-gate-test-automation.md`
定义的 **L1／L2／L3 三层模型已经建成并在跑**，本图做的是把九个批次的出口挂到这三层上。

| 层 | 是什么 | 实体 |
| --- | --- | --- |
| **L1** | 进程内单元与集成测试 | ControlServer 268 项 |
| **L2** | **半实物**：真 ControlServer ＋ 真车载端 WPF ＋ 真 `slots-simulator` 真 Modbus ＋ 假 RIoT ＋ 假 MesIngest | `8005-agv-control-server/scripts/l2/` **1307 行 pwsh**、两套装置、8 个场景、`evidence/l2/` 下 **52 份证据**，合成 4 条每次 push 进 CI |
| **L3** | 现场 | 跑通一次，2026-09-03 止于装载 |

**两套装置不可互换**：合成对端没有 IO、journal、操作员与本地时钟新鲜度判定；真装置的车载
端与模拟器绑死（没有 Modbus 则八仓全报 `UNKNOWN`，`departureSafe` 恒 false）。

**L2 是唯一能看见跨端时序的自动化层**，且它的证据形状（`SUMMARY.md` ＋ `assertions.json` ＋
`timeline.jsonl` ＋ `logs/` ＋ `snapshots/`）沿用 G3、可直接进门禁体系。它的
`assertions.json` 的 `identity` 块已含 `controlServerCommit` ＋ `onboardHmiCommit` ＋
`slotsSimulatorCommit`。

**引用该文档时取 `main` 版（491 行）。**

### 8.2 每个批次的默认出口

**三条同时成立：**

1. **L1 绿**：该批次涉及的单元与集成测试全部通过，**且新能力有新增覆盖**（不允许「没有新
   测试也算绿」）。
2. **L2 绿**：该批次的新场景在 CI 上**连续三次通过**。三连跑的纪律沿用黄金渲染机的既定标
   准，理由相同——L2 涉及跨进程时序，一次通过区分不了「正确」与「这次恰好排上了」。
3. **门禁绿**：该批次绑定的切片（若有）四道门禁全 PASS，`gate-result.json` 绑定精确
   `ProtocolReleaseIdentity`。

**无切片的十类工作出口只有前两条**，排期时按工程项逐项列出。

### 8.3 逐批次验收出口

| 批次 | 默认出口 | 现场 |
| --- | --- | --- |
| **0** | 引用已批准的 MVP 规格与剖面证据，**不重验** | MVP 自己的现场验收（软前置） |
| **1** | G1 通过（候选态，用 tracked 空白模板）；**生成器可重跑且输出确定**（同输入两次生成逐字节相同）；两条 `reasonCode ∈ 注册表` 架构测试绿；`runner/` 两个 schema 已删且 manifest 哈希随之更新 | 无 |
| **2 轨 A** | `FP-IS-00`～`07` 各一遍 `CONTROL_SERVER_G2` ＋ `ONBOARD_HMI_G2` ＋ `G3` 全 PASS；161 个 trait 重打标后 `dotnet test --filter` 的分区**无遗漏无重复** | 无 |
| **2 轨 B** | L1 ＋ **合成 3 车 L2** 绿；RIoT 白名单架构测试绿；引擎快照双周期刷新与陈旧态 fail-closed 有 L2 证据；命令面在 L2 上证明「该调用时调用了、参数正确、只调一次」 | **W1 的空载急停演练** |
| **3** | 默认三条 ＋ `FP-IS-14`、`FP-IS-15` 两切片四门禁 | **W1 的逐车逐仓 IO 核对** |
| **4** | 默认三条 ＋ `FP-IS-10`、`FP-IS-11` 四门禁 ＋ 三条机制正确性判据（8.5） | 无 |
| **5** | 默认三条 ＋ `FP-IS-12` 四门禁 | **W2 的等待点**（前提：已测绘） |
| **6** | 默认三条 ＋ `FP-IS-08` 四门禁 | **W2 的多车分阶段放开** |
| **7** | 默认三条 ＋ `FP-IS-09` 四门禁 | 无 |
| **8** | 默认三条 ＋ `FP-IS-13` 四门禁 ＋ **L2 的 2 桩 3 车争用证据**（8.5） | **W3 的完整充电周期与清桩闭环** |

**批次 2 的两轨出口独立**：轨 B 不阻塞轨 A，但两轨都完成才算批次 2 完成。

#### 执行记录：批次 2 于 2026-09-09 由用户宣告完成

**上面 8.3 那张表是 2026-09-04 批准的文本，本节不改动它**，只记录实际达成的形态
以及它与表格原文的差异。票据与证据在 `.scratch/8005-batch-2/`。

| 轨 | 出口 | 达成 |
| --- | --- | --- |
| 轨 B | 票 18 | 2026-09-08 `resolved`，八条验收全过 |
| 轨 A | 票 17 | 2026-09-09 `done`，九条验收全勾 |

🔴 **轨 A 的达成形态与表格原文有一处差异，宣告完成即接受它：**

表格原文要求「`FP-IS-00`～`07` 各一遍 `CONTROL_SERVER_G2` ＋ `ONBOARD_HMI_G2` ＋ `G3` 全 PASS」。
**两道 G2 确实八片全 PASS。`G3` 不是八片**：

- `FP-IS-00`／`04`／`05`／`06` 有 G3 面且 `formalSlicePass=true`；
- **`FP-IS-01`／`02`／`03`／`07` 本批次没有 G3 面**——四个 G3 runner 里一次都不出现。
  用户 2026-09-09 裁定**如实记录、不补四个新场景**，所以它们不发证据，
  记在每份 `run-result.json` 的 `slicesWithoutSurfaceThisBatch`；
- `FP-IS-04`／`05` 的通过以一条**已知豁免**为前提：被恢复的现场库记的历史 `protocolCommit`
  是 `protocol-v0.1.1`，任何 v2 身份的运行对它都过不了。用户同日裁定豁免，
  票 24 把该项从断言里拆成如实记录（`fieldStoreProvenance`），前六项仍是断言且全过。

表格原文的第二条判据「161 个 trait 重打标后 `dotnet test --filter` 的分区无遗漏无重复」
**已由票 14 满足**（实测形态见 `14-answer.md`）。

**轨 B 现场栏那项（W1 的空载急停演练）未做，且不阻塞**：票 19 逐字写着不要因它挂起整个
批次 2，而 8.4 里 W1 窗口的门槛是**批次 3 代码就绪**。票 19 仍是 `ready-for-agent`，
随 W1 窗口补齐。

**另外三件仍然悬着，宣告完成不掩盖它们**：八份 `ONBOARD_HMI_G2` 的 `g1Status` 仍是
`SKIPPED`（用户裁定不重出）；三份 G3 `run-result.json` 里 `fullG3` 与 `releaseCandidate`
仍是 `INCONCLUSIVE`，**批次 2 的完成不含 RC**；票 20／21／22／23／24 不在本规格的批次 2
范围里，批次归属至今未定。

#### 补记：2026-09-13 在已发布的 `protocol-v1.0.0` 上复核

上面的执行记录写于 2026-09-09，那时协议还是候选身份。2026-09-12 协议两次改 manifest，
当天发布为 `protocol-v1.0.0`（注释 tag 指向 `9f22db8`，`APPROVED_RELEASE`）。按
`docs/release-governance.md`，绑旧身份的门禁与 L2 证据从此不再是现行证据，两轨出口要在发布身份上
重新成立。**本节只记复核结果，不改 8.3 的表格，不改上面的执行记录，也不改宣告完成这件事。**

**结论：两轨出口在 `protocol-v1.0.0` 上都重新成立，与 2026-09-09 的形态相同。**

| 轨 | 出口判据 | 在 `protocol-v1.0.0` 上 | 证据（`8005-agv-control-server` `fp/v2-impl`，另注明的除外） |
| --- | --- | --- | --- |
| 轨 A | `CONTROL_SERVER_G2` 八片 | 全部 `PASS`，服务端 `6b21662` | `evidence/g2/20260912-protocol-v1.0.0-6b21662/FP-IS-00`～`07` |
| 轨 A | `ONBOARD_HMI_G2` 八片 | 全部 `PASS`，脚本内 `g1Status` 均为 `PASS`，车载端 `98f4e06` | `8005-agv-onboard-hmi` 的 `evidence/g2/20260912-protocol-v1.0.0-98f4e06/FP-IS-00`～`07` |
| 轨 A | `G3` | `FP-IS-00`／`06` 在主 runner 与进程重启 runner 上 `PASS`，`FP-IS-04`／`05` 在需求线路 runner 上 `PASS`，均 `formalSlicePass=true`；`FP-IS-01`／`02`／`03`／`07` 仍记在 `slicesWithoutSurfaceThisBatch` | `evidence/g3/20260912-protocol-v1.0.0-staged-harness-a1243a8`、`…-restart-harness-a1243a8`、`…-demand-bearing-harness-a1243a8` |
| 轨 B | 合成 3 车 L2；陈旧态 fail-closed；命令面三条断言 | CI run 34701119449（`a1243a8`）23/23 `PASS`，`three-vehicle-exit`、`command-surface-order-hold`、`route-graph-staleness` 各连续 3/3；每份身份为 `protocol-v1.0.0@9f22db8`，`batchId` 为 `batch-2` | `evidence/l2/20260912-ci-34701119449-*`，轨 B 那九份 2026-09-13 从 CI artifact 原样入库（`65bffc0c`） |
| 轨 B | L1；RIoT 白名单架构测试 | 服务端 699 passed / 0 skipped（`6b21662`，含 `RiotCallAllowlistArchitectureTests`） | `docs/batch-3-v2-exit-report.md` 第一节 |

`a1243a8` 相对 `6b21662` 只改了 G3 runner 的默认值与证据，`src/`、`tests/` 未动，所以 L2 与门禁测的是
同一份产品代码。

**9 月 9 日那几条限定，现状如下：**

- **`G3` 不是八片**：不变。
- **`FP-IS-04`／`05` 依赖现场库历史那条豁免**：不变。这一轮 `fieldStoreProvenance.matchesBoundProtocolCommit`
  仍如实为 `false`，真正的解仍是重采一次 v2 现场运行。
- **八份 `ONBOARD_HMI_G2` 的 `g1Status` 是 `SKIPPED`**：**已解决**，这一轮八份都是 `PASS`。
- **不含 RC**：仍成立。`protocol-v1.0.0` 已发布，但三份 G3 `run-result.json` 的 `fullG3` 与
  `releaseCandidate` 仍是 `INCONCLUSIVE`。
- **票 20～24 的批次归属**：仍未定。
- **W1 的空载急停演练（票 19）**：仍未做，**改挂到生产切到 v2 线的那次现场窗口**（用户 2026-09-13 定）。
  W1 窗口 2026-09-13 已经开过，但为了不等切 v2，做在生产现有的 v0.3.0 库上；急停代码只在 v2 线，
  那次窗口里演练本来就做不了。前置仍是两条：生产跑上 v2 线；RIoT 侧有人能把一张在途单置为终态 FAILED。
  它和 `8005-agv-control-server#44`（切 v2 前对齐光幕极性常量）同属切 v2 前后的待办。

**另登记一处文档与实现的偏离，不改文档**：`docs/riot-call-allowlist.md` 1.5 节写的 `triggerEmergency`
触发条件（仓门未安全锁闭时移动、无单可 `OrderHold`）在实现里没有对应路径，实现只在「在途单被报 FAILED
且证不出停住」时升级，见 `.scratch/8005-batch-2/issues/19-answer.md` 第四节。那段文字是已批准需求
`REQ-0246` 的汇编，改它等于改产品规则；服务端的白名单架构测试也钉着这份文档的 SHA-256。
`8005-agv-control-server#1` 同日评论了现状，保持打开。

#### 补记：2026-09-14 批次 2 收尾——轨 A 的 `G3` 补齐八片

用户 2026-09-13 要求补完 `FP-IS-01`／`02`／`03`／`07` 的 G3 面、勾完本表后关闭批次 2。**本节只记结果，不改 8.3 的表格与上面两节。**

**结论：轨 A 表格原文那一格第一次按原文成立——`FP-IS-00`～`07` 各一遍两道 G2 ＋ G3 全 `PASS`，`G3` 是八片。**
轨 B 的现场项（W1 空载急停演练）仍未做，用户 2026-09-14 再次确认维持挂到生产切 v2 的现场窗口，是批次 2 **唯一**的欠账。

| 轨 | 出口判据 | 结果 | 证据（`8005-agv-control-server` `fp/b2-close`，另注明的除外） |
| --- | --- | --- | --- |
| 轨 A | `CONTROL_SERVER_G2` | 十片全部 `PASS`，服务端 `052759bc`，`APPROVED_RELEASE` | `evidence/g2/20260914-protocol-v1.0.0-052759bc/` |
| 轨 A | `ONBOARD_HMI_G2` | 十片全部 `PASS`，车载端 `8d19fee`（产品代码同 G3 绑定的 `b960108`），`g1Status` 均为 `PASS` | `8005-agv-onboard-hmi` `w2g/b3-on-v2` 的 `evidence/g2/20260914-protocol-v1.0.0-8d19fee/` |
| 轨 A | `G3` | **八片全部 `formalSlicePass=true`**：`FP-IS-01`／`02`／`03`／`07` 在新的 journey runner（80 条断言）；`FP-IS-00`／`06` 在主 runner 与进程重启 runner；`FP-IS-04`／`05` 在需求线路 runner。四份 `run-result.json` 的 `slicesWithoutSurfaceThisBatch` 都为空 | `evidence/g3/20260914-protocol-v1.0.0-{journey,staged,restart,demand-bearing}-052759bc/` |
| 轨 A | trait 分区无遗漏无重复 | 不变，已由票 14 满足 | `14-answer.md` |
| 轨 B | 合成 3 车 L2 三连；陈旧态 fail-closed；命令面三条断言 | CI run 34815736635 第 2 次尝试（`7327ef3a`，产品代码同 `052759bc`）job `success`，26 次运行全 `PASS`：`three-vehicle-exit`（22 条判据）、`command-surface-order-hold`（20 条）、`route-graph-staleness`（13 条）、`emergency-stop-single-trigger`（14 条）各连续 3/3，每份身份 `protocol-v1.0.0@9f22db8`、`APPROVED_RELEASE`、`batch-2`。逐场景证据从 artifact 原样入库。同日较早的 run 34807641700 场景同样全过，但因 artifact 存储配额已满只留下运行日志，原样保留 | `evidence/l2/20260914-ci-34815736635-*`（总览见 `…-run/SUMMARY.md`） |
| 轨 B | L1；RIoT 白名单架构测试 | CI run 34807639494 第 2 次：722 passed / 0 failed（第 1 次是 runner 连不上 NuGet，未编译）；本地同一产品代码 722 passed | 同上目录的 `test-run-34807639494-attempt2.log` |

**journey runner 是什么、为什么算正式通过。**真服务端、真车载端（WPF，UI Automation 驱动操作员动作）、真仓位模拟器，
RIoT 与 MES 用仿真对端；十条 L2 场景的判据映射成 G3 断言后按归属表分片。等级名 `JOURNEY_SIMULATED_COUNTERPARTS`，
「真跑、对端仿真」算正式切片通过是用户 2026-09-13 的裁定。

**补 G3 面时撞出的产品缺陷，两端都先修再出证**（修复前红／修复后绿的测试随各自 G2 出证，缺陷单在服务端 `docs/defects/`）：

- 服务端：到站前先发计划（`5293c43f`）；离站等待，默认 5 分钟（`6e8dea5a`，用户 2026-09-13 定按规格补）；迟到结果不重开已取消装载（`1312a512`）；
  出发前检查过期后作废并以新身份重问（`6c252816`、`11f3d69d`）；状态未知结果跨会话对账（`e62b136d`）；恢复原操作带原命令哈希（`d2a19c7a`，用户裁定改服务端）；
  恢复收尾后回到就绪（`e6b92ee3`）。
- 车载端（`w2g/b3-on-v2`）：出发前检查过期回 `PREDEPARTURE_CHECK_EXPIRED`；状态未知结果记待结清并补发（`3fb8a6e`）；
  「强制机械恢复」「充电后返回服务」两个操作员入口（`f14f8af`，用户裁定补界面入口）。

**同日有一次 journey 运行失败，原样留在本机未入库**：绑定先指向 `1b1f3dd7` 时，两条 `FP-IS-02` 场景在按确认框时中止（车载端确认框不在前台，
L2 驱动只会 UIA Invoke），四片同判 `FAIL`。红在编排器不在产品；修在 `052759bc`（`src/`、`tests/` 零差异），四个 runner 与服务端 G2 全部在它上面重跑。

**9 月 9 日那几条限定，现状如下：**

- **`G3` 不是八片**：**已解决。**
- **`FP-IS-04`／`05` 依赖现场库历史那条豁免**：不变，`matchesBoundProtocolCommit` 仍如实为 `false`。
- **不含 RC**：仍成立，四份 `run-result.json` 的 `fullG3` 与 `releaseCandidate` 仍是 `INCONCLUSIVE`。
- **票 20～24 的批次归属**：仍未定。
- **W1 的空载急停演练（票 19）**：仍未做，前置不变（生产跑上 v2 线；RIoT 侧有人能把在途单置为 FAILED）。
  用户 2026-09-14 确认维持挂到生产切 v2 的现场窗口，不因它挂起批次 2 的关闭。

### 8.4 三个现场窗口与证据目录

窗口按**现场前置就绪**排，不按批次号排——两处现场前置（桩安装、等待点测绘）的时间不由本
项目控制。

| 窗口 | 门槛 | 内容 | 出口判据 |
| --- | --- | --- | --- |
| **W1 车辆资格** | 批次 3 代码就绪 | ① 三台车**逐台**逐仓 IO 核对（每台 8 仓，不抽样）；② 每台核对通过后放行 `SlotConfigurationReadiness`；③ 一次**空载**受控急停演练 | 三台车各自取得 readiness 且审计留痕；急停演练中 RIoT 侧确实停车，且 8005 侧只发一次调用 |
| **W2 多车与等待点** | 批次 6 代码就绪 ＋ 等待点已测绘 | ① 多车分阶段 1 → 2 → 3 车，每阶段一个完整路径；② 空闲返回等待点独占 | 三个阶段各自严格清场且完整路径成功；三车阶段有观察员记录；等待点独占的一行两状态与离点证据释放在现场可观测 |
| **W3 自动充电** | 批次 8 代码就绪 ＋ 三桩已安装并录入名册 | ① 一个完整充电周期含预占与释放；② 清桩闭环；③ `REQ-0174` 失败码 407802 的目标环境取证 | 充电周期端到端成功且 `VehiclePurposeClaim` 的占有与释放可观测；清桩闭环走通一次；**首次自动充电有人跟随全程** |

**批次 1、2 轨 A、4、7 完全不占现场窗口。W1 的顺序不得倒置：先核对，后启用门禁**（3.5）。

证据目录：

| 层 | 目录 | 格式 |
| --- | --- | --- |
| L1 | 不单独归档 | CI 日志 ＋ trx |
| L2 | `8005-agv-control-server/evidence/l2/<日期>-<场景>-<序号>/` | `SUMMARY.md` ＋ `assertions.json` ＋ `timeline.jsonl` ＋ `logs/` ＋ `snapshots/` |
| G2 | `evidence/g2/<日期>-<描述>/<FP-IS-NN>/` | `gate-result.json` |
| G3 | `evidence/g3/<日期>-<描述>/` | `SUMMARY.md` ＋ 断言逐条结果 ＋ 精确 commit 绑定 |
| RC | `evidence/rc/<日期>-<描述>/` | 安装结果 JSON ＋ 诊断日志 ＋ 卸载结果 JSON |
| **现场窗口** | **`evidence/field/<日期>-<窗口号>-<描述>/`（新增）** | 与 L2 同形状 ＋ 现场记录与照片指针 |

**新增 `evidence/field/` 而不复用 `evidence/g3/`**：G3 是门禁，现场窗口不是门禁；同目录会让
「切片通过」与「现场验收通过」混淆。

四条保留策略全部沿用已有纪律：`-EvidenceRoot` 必须是不存在的目录；**红的证据不允许被绿的重
跑覆盖**；跑失败时 stage root 不删；**证据目录只增不改**（纠正写新目录 ＋ 在 `SUMMARY.md` 里
指向被纠正的那份）。

`assertions.json` 的 `identity` 块在完整产品下**加两项**：`protocolReleaseIdentity`（v2 的
三元组）与 `batchId`。前者使 L2 证据能像 G2 一样按协议换代作废，后者使证据能回答「这是哪个
批次的出口证据」。

### 8.5 四类「自然运行取不到」的证据

共同点是**当前配置凑巧使规则不触发**。**不得默认「不触发即通过」**：

| 条目 | 为什么现场取不到 | 证据来源 |
| --- | --- | --- |
| `REQ-0172`／`REQ-0173` 充电排队与预占不可抢占 | 现场 3 桩 3 车，争用永不发生 | **L2 合成装置配 2 桩 3 车**，桩数 < 车数，争用必然发生 |
| 「充满电的车占着桩饿死低电车」 | 同上 | 同一个 L2 配置覆盖 |
| `FP-C9a` 三条 | 四个公共站点功能不在 `mapId` 25 的 206 个站里 | ① fail-closed 正确拒绝：L2 可取；② 绑定完备时正确放行：L2 双 Fake；③ `REQ-0187` 唯一性跨类型：L2 构造 |
| 等待点独占 | 等待点尚未测绘进 RIoT 地图 | 机制在 L2 取证，物理验收放 W2 |

**四条都不得归入 `证据受限实施`**——那个形态要求「判据依赖的外部证据当前不可得而**恒**走保
守分支」，而这四条的证据都可得，只是不在现场那条路上，补测绘或改配置后无需改代码即可取证。

**`REQ-0174` 的失败码 407802 单独处置**：出处只有 Round 24，范围是「仅测试车；map30」，不是
`RIOT-8005-RUNTIME`。判为**验收项而非投运前置**——`ConfirmedUnableToCharge` 的严格系统事实在
目标环境证据缺失期间走保守分支，**W3 窗口内首次现场充电失败时补证**。**这同样不是
`证据受限实施`**——它不是「恒」走保守分支，是补证后转正。

### 8.6 五处「投运前须批准」的参数，三种不同的后果

**不能一律写成「未批准不得投运」**：

| 参数 | 条目 | 批次 | 表述 |
| --- | --- | --- | --- |
| 目录同步周期与最大允许未确认时长 | `REQ-0302` | 2 | **硬阻断**：无已批准值时依赖 Map/Station 的业务不得启用；出口含**未配置时确实阻断**的负向证据 |
| 防饥饿阈值 | `REQ-0203` | 6 | **降级不是阻断**：未配置时继续累计等待年龄但不执行跨任务类型升级 |
| 每区途中追加最大允许值 | `REQ-0198` | 6 | **范围限制**：零或未配置表示**本区禁止**途中追加，**不继承全项目默认值**；负向证据逐区取 |
| 独占充电桩名册 | `REQ-0171` | 8 | **退化不是阻断**：名册为空时退化到 `ManualChargingHold` 且**不静默** |
| `ChargingPolicyVersion` | `REQ-0282` | 8 | **硬阻断**：无已批准版本的车辆不得投运，逐车判定 |

**三条硬阻断的出口都必须含一条负向证据**：把参数拿掉，证明它真的阻断了。只证明「配好之后
能跑」证不出阻断存在。

### 8.7 失败与回退

1. 批次代码**不回退**。
2. 未通过的能力用**受控预置配置关掉**，方向必须是 fail-safe（关掉的后果是运力下降或功能不
   可用，不能是绕过安全门禁）。
3. 已通过的能力**留着**。
4. **安全类缺陷不允许带病投运**——`FP-C11` 的三条自动急停、`REQ-0259` 的 IO 完整性门禁、
   `REQ-0263` 的逐仓核对属于这一类。
5. 关掉一个能力时**必须重新检查它的下游**：`2轨B → 5 → 6 → 7` 是一条不变量硬链，关掉链上
   一环等于关掉它下游的全部。

**这给实施图一条硬约束**：每个能力必须有一个能单独关掉它、且不影响其它能力的开关。这不是
免费的——本图已识别出至少一处天然耦合（`FP-C4` 的等待点独占是 `FP-C1` 充电桩分配的前置）。

### 8.8 三条不得含糊的表述

1. **本图的范围与顺序由用户单人批准**，Kun Wang 事后按 notify-after-change 通知，**不得表
   述为已获双方同意**。
2. **完整产品的验收证据里不会有任何人员认证项**（`FP-C10` 与 `FP-C6` 全部延后），且**不得
   表述为「权限已在批次 0 验收过」**——批次 0 的权限骨架两端零实现，唯一的认证是一个全场共
   用的环境变量。
3. **`CP-0001` 未获批准前，引擎相关切片的验收证据里不得出现「符合 `REQ-0298`」这类表述。**
   批准前的正确写法是：「实施形态与基线 `REQ-0298` 原文存在一条已知且已记录的偏离，偏离的
   处置见 `CP-0001`」。

*追溯：票 08 全文、票 09 的 3.4。*

---

## 9. 需求变更提案 `CP-0001`

**这是 v1.0.0 的第一份需求变更提案。**348 条全部是 `Change Proposal: none（首版恢复）`，基
线头部 Modified 与 Deprecated 都是 `None`。

| 项 | 值 |
| --- | --- |
| 编号 | `CP-0001`（规则：`CP-NNNN`，四位十进制，不把年份或批次编进 id） |
| 状态 | **待用户批准** |
| 目标版本 | 下一个基线版本（版本号是发布时的事） |
| 修订项 | 两条：`REQ-0298` 重写、`REQ-0146` 增列五个 `imap` 只读端点 |
| 执行 | **本图不执行**，不动 `requirements/baselines/` 下任何文件，不动 `requirements/current-baseline.md` 指针 |

### 9.1 修订项一：`REQ-0298` 重写

**基线原文：**

> 当前产品只同步 Map/Station 目录，不同步本地路网。 MapStationCatalogSnapshot 覆盖
> RIOT-8005-RUNTIME 当前全部有效 Map 及每张 Map 的全部 Station，用于 AREA 命名机台站点解析、
> FixedTaskStation 绑定、配置校验和变化检测。Edge、几何路网、本地最短路与动态交通状态均不
> 进入本产品事实；派车可达性和路径成本继续使用已批准的实时 RIoT RouteCost 证据边界。

**建议修订文本：**

> 目录与路网是两份各自具名的产品事实。 MapStationCatalogSnapshot 覆盖 RIOT-8005-RUNTIME
> 当前全部有效 Map 及每张 Map 的全部 Station，用于 AREA 命名机台站点解析、FixedTaskStation
> 绑定、配置校验和变化检测，**它不承载 Edge**。RouteGraphSnapshot 另行自 RIoT 取得并持有
> 某张 Map 的完整有向站点图，由设计态（边、站点及其到节点的定位）与运行态（当前被移除的边
> 与站点）合成，是站到站路径代价与 StationReachability 判定的唯一依据。几何路网、动态路由
> 代价及其它动态交通状态仍不进入本产品事实。建单前对具体车辆到具体站点的可达确认继续使用
> 已批准的实时 RIoT RouteCost 证据边界。两份事实各自具名、互不冒充，任一不可用时按其自身的
> fail-closed 规则阻断相关动作。

**修订说明（供批准人核对）：**

1. **保留了原条目真正在保护的三件事**：目录快照的完整性边界（它仍不承载 Edge，故
   `REQ-0300` 的全量原子发布、`REQ-0301` 的内容指纹一字不动）、几何路网仍排除、动态交通状
   态仍排除。
2. **`removedEdge` 不是「动态交通状态」**，是边的存在性；修订文本把它明确划进
   `RouteGraphSnapshot` 的运行态，不留歧义。
3. **末句「各自具名、互不冒充」直接回应 `REQ-0207`**（「任何弱替代值都不得冒充 RIoT
   RouteCost」）——自建图算出的值不叫 RouteCost，两个证据源在不同阶段各司其职，故
   **`REQ-0207` 不需要修订**。
4. `###` 标题行随首句改写。

**为什么要改而不是遵守它**：理由不是「我们要违反它」，而是它的来源票据白纸黑字写着的两条
理由今天都已失效。`REQ-0298` 是我方 2026-08-24 的**自批边界决定**（来源票 77，
`Source Authority: 用户本人`、`AI Involvement: none`、`Derivation: verbatim-list-item`），
票 77 第一轮取证逐字写着排除 Edge 的两条理由——「**现有材料仍未证明**目标运行环境的 Edge
返回权限、完整性、变化语义与跨版本稳定性」与「当前需求基线**不必为了既有派车规则先**承诺本
地完整路网图」。前三项已由 Round 43 填补；第二条的语气本就是「不必先承诺」这句范围声明。
规范化时逐字抄了以「当前产品」开头的 Answer 首条，**把时点限定丢掉后剩下一句读起来绝对的禁
止**。

**一条诱人的捷径被否掉**：不能拿 `REQ-0309` 的「API 与数据结构留给后续设计」覆盖
`REQ-0298`——全基线只有 `REQ-0199` 与 `REQ-0309` 两条自我豁免，二者都是所属票据的**末条范
围分离声明**，而 `REQ-0298` 是**首条事实范围声明**；且 `REQ-0309` 豁免的是「怎么实现」不是
「哪些事实进入产品」。

### 9.2 修订项二：`REQ-0146` 增列五个 `imap` 只读端点

在具名清单尾部增列：

> `GET /api/imap/v1/mapInfo/edges/{mapId}`、`GET /api/imap/v1/mapInfo/stations/{mapId}`、
> `GET /api/imap/v1/mapResource/removedEdge/{mapId}`、
> `GET /api/imap/v1/mapResource/removedStation/{mapId}` 和
> `GET /api/imap/v1/mapEdgeGroup/all`。

**五个，不是四个。**第五个 `removedStation` 由票 09 补入（用户 2026-09-04 批准）：
`CONTEXT.md` 的 `RouteGraphSnapshot` 词条本来就写着运行态是「当前被移除的边**与站点**」，词
条一直是对的，缺的是白名单里那个具体端点。**`removedEdgeDetail` 不批**，引擎用不上。

**为什么必须显式增列，而不是靠「当前 Facade 使用的地图查询」这个开放引用**：那句话里的「当
前」指的是 2026-08-24 那个时点的 Facade，而这五个端点当时不在、现在也不在（vendored
`RIoT.Sdk.Facade` 的 38 个 `*Async` 方法里没有任何边表方法）。让一个安全边界靠一处时点歧义
承载扩权，正是「白名单是一份纯文档、编译期运行期测试期三处都没有守卫」的同一个毛病。**变更
面从一条扩到两条，换的是白名单的可判定性。**

### 9.3 提案的边界：只动两条

| 条目 | 为什么不动 |
| --- | --- |
| `REQ-0207` | 「不得冒充 RIoT RouteCost」约束的是**证据强度与命名**，不是 endpoint。自建图各自具名即合规 |
| `REQ-0147`／`REQ-0293`／`REQ-0302`／`REQ-0305`／`REQ-0345` | 建单前置 RouteCost 门禁**保留**（5.6） |
| `REQ-0199`／`REQ-0309` | 是豁免声明本身，修订 `REQ-0298` 不影响它们 |
| `REQ-0300`／`REQ-0301` | 约束的是目录快照，修订后目录仍不承载 Edge |
| `REQ-0309` 的第二条 Edge 禁止 | 论证不冲突（5.6） |

### 9.4 未批准前的约束

**提案未批准前，实施图不得据修订文开工。**引擎相关切片的验收证据在批准前的正确表述见
8.8 第 3 条。

`REQ-0298` 与 `REQ-0146` 在剖面里**按正常条目排期**：`FullProductCluster` 仍是 `FP-B0`、
`Batch` 仍是 `BATCH-0`（它们是范围边界声明，被推翻的是边界线的位置不是实施状态），修订由
`CP-0001` 承载。

*追溯：票 15 的 Q1、3.1、3.3，票 09 的 1.2 与 1.3。*

---

## 10. 需求变更执行流程（最小定义）

**这一节是本规格新定的，此前不存在。**v1.0.0 至今零次变更，**格式**在基线头部已定死，但没
有任何文档规定谁在什么时候把提案变成下一个版本、要不要重算 Baseline SHA-256 与 tag。
`CP-0001` 会是第一份，没有流程它落不了地。

用户 2026-09-04 决定在本规格里定一节最小流程，**不另立正式治理文档**。

### 10.1 提案的形态

一份提案是一个 `CP-NNNN`，含：状态、目标版本、逐条修订项（每项给**基线原文 ＋ 建议修订文
＋ 修订说明**）、以及**提案边界**（哪些相关条目经核查不需要修订，附理由）。提案可以在批准
前继续增加修订项——`CP-0001` 的修订项二就从四个端点扩到了五个。

### 10.2 谁批

**用户一人批准**，与本规格同一个批准人。需求基线是本项目自己的产物（`REQ-0298` 本身就是我
方 2026-08-24 自批的边界决定），不涉及第二方签名。

**这与 protocol release 的双人 attestation 是两件不同的事**，不要混淆：需求基线的批准是单
人，协议 release 的批准是两名不同产品负责人且 AI 与 CI 不能批准（第 12 节）。

### 10.3 何时批

**在实施图动到该提案所涉条目之前**，不必等到批次开工。具体到 `CP-0001`：引擎在批次 2 轨 B
上线，故 `CP-0001` 应在批次 2 开工前批准；未批准而批次 2 已开工时，按 8.8 第 3 条的表述记录
偏离，**不阻断实施**。

### 10.4 批准后做什么

1. 在基线头部 `相对上一批准版本的变化` 段的 `Modified` 下加一行，逐条列出被修订的条目。
2. 改被修订条目的三个字段：`Current Requirement`（换成修订文）、`Last Meaning Change In`
   （换成新版本号）、`Change Proposal`（从 `none（首版恢复）` 换成 `CP-NNNN`）。
3. 版本号按语义递增：**修订既有条目的文义 → minor**（v1.0.0 → v1.1.0）；只改措辞不改文义
   → patch；删除或作废条目 → major。`CP-0001` 两条都改文义，故目标是 **v1.1.0**。
4. **重算 Baseline SHA-256**，写进基线头部。旧值不删——头部保留一份版本→哈希的对照表，
   因为已归档的证据引用的是旧哈希。
5. **打新的 annotated tag `requirements-baseline-v1.1.0`** 指向承载修订的那个 content
   commit。**旧 tag 不动、不移动、不删除**——它是已归档证据的锚。
6. 提案文件本身归档进 `requirements/change-proposals/CP-NNNN.md`，状态改为已批准并记录批准
   日期与批准人。

### 10.5 一条纪律

**不回溯修改已归档的证据去匹配新基线。**证据绑定的是它当时的基线哈希；基线换版后，旧证据
仍然有效地证明它当时证明的那件事。需要重证时建立新运行——这与 `ConformanceRunIdentity` 对
协议证据的规定同构。

**本节四处（版本号语义、哈希对照表、旧 tag 不动、提案归档路径）是汇编时的自行定案**，理由
与代价见第 16 节。

---

## 11. 表述规则：四种合法形态

**「不做」在本图只有两种合法形态：延后，或本图范围外。**另有两种不是「不做」但极易被读错的
形态。四种逐一定义，规格与其派生物必须严格区分：

| 形态 | 定义 | 实例 |
| --- | --- | --- |
| **延后** | 条目在 Destination 之内但本图未排入批次。**Lifecycle 仍 `active`** | 22 条：`FP-C10` 8 ＋ `FP-C6` 8 ＋ `FP-C12` 6 |
| **本图范围外** | 条目或动作在 Destination 之外，归别的工作 | 100 条 MesIngest ＋ 跨 Map 运输这个动作 |
| **`需求变更待批`** | 条目**要实施，而且要按与基线文本不同的形态实施**。本图输出变更提案，提案批准前不改基线 | 2 条，同属 `CP-0001`：`REQ-0298`、`REQ-0146` |
| **`证据受限实施`** | 门禁与代码路径完整实现、要排批次要写代码要有验收证据，只是判据依赖的外部证据当前不可得而**恒**走需求自身规定的保守分支。**它是「已实施」不是「不做」** | **本图零实例** |

**三条纪律：**

1. **延后不得表述为需求作废、废弃或「本期不需要」**，只能写「本图未排入批次，条件是 X」。
   348 条 Lifecycle 全部 `active`，本图不改基线，因此任何范围收窄都不得表述为需求作废。
2. **`证据受限实施` 在本图没有任何实例**，不得给它造实例。它最初的三个候选（`REQ-0196`／
   `REQ-0198`／`REQ-0197` 换序半）已由票 14 依 Round 43 实测改判为**完整实现**。三处「机制
   建齐、现场证明不了」——map 25 当前没有任何边组、`FP-C9a` 的四个公共功能不在现场、等待点
   未测绘——**都不是这个形态**，因为它们的证据不可得是**现场尚未具备**造成的，具备后无需改
   代码。词条保留只是因为后续可能产生新实例。
3. **`需求变更待批` 的条目按正常条目排期**，`Batch` 列不因它变化。

**另有两种「已实施但不完整」的形态，必须逐半写清、不得整条归入任一形态：**

- **部分实施**：`REQ-0254` 是「协议 v1 的 `administratorRole` 两值枚举已冻结且服务端已校
  验」实施 ＋「身份由客户端自报」延后；`REQ-0339` 是「明确确认影响预览」实施 ＋「使用当前
  密码新鲜二次认证」延后（**明确排除用共享密钥冒充二次认证**）。
- **退化实施**：`REQ-0311` 的恢复权限只属系统管理员，本期无该实体，退化为「恢复入口不在看
  板、不在车载端，只在受控运维流程里」。

**还有两类容易被读成别的东西：**

- **否定性需求**（`REQ-0273` 不建立泄露找回或强制重置流程、`REQ-0326` 覆盖治理不属当前需
  求）：写成「本决定明文排除」。不能因为「不实施」就让它们在 348 行里缺席，也不能被读成遗漏。
- **改判**（最易被读错的一类）：`FP-C10` 那 8 条、`FP-C7` 的 8 条地基、`FP-C8` 的 2 条显示
  规则，原本标着「批次 0 已实施」。**必须写清此前判定成立于什么形态、为何不成立**，否则读
  者会以为是新增范围。这正是剖面第 11 列 `Batch0FormNote` 的用途。

*追溯：map Notes 第 18、35 条；票 15 的 Q4；票 09 的 Q6；票 05 第三节；票 03；票 14。*

---

## 12. 分工与批准路径

### 12.1 分工

| 侧 | 归属 | 说明 |
| --- | --- | --- |
| `8005-agv-control-server` | Zhengyu Shao | 含看板本体——控制服务端历史上第一个界面 |
| `8005-agv-protocol` | Zhengyu Shao 单独决定内容 | 每次推送开 issue @`SocialKKKK`；**打 tag 仍需两名不同产品负责人** |
| `8005-agv-onboard-hmi` | **开发在我方，仓库写权限仍在 Kun Wang** | 形态：我方开 `w2g/*` 分支提 PR，对方评审合并。**已有先例并跑通**（PR #5，2026-09-04 同日一小时内评审合并） |
| `slots-simulator` | 同上 | 完整产品需要它扩多实例支持；本期不建真装置多车，故本期不需要 |

### 12.2 批准路径：从本规格到 v2 release

| 节点 | 谁 | 批什么 |
| --- | --- | --- |
| 1 | 用户 | **本规格**——单人批准，即本图 Destination 达成 |
| 2 | 用户 | **需求变更提案 `CP-0001`**。未批准前不得据修订文开工 |
| 3 | — | 批次 1 落地：协议 v2 候选生成 ＋ **候选态 G1**（用 tracked 空白模板） |
| 4 | Zhengyu Shao | 推送 `8005-agv-protocol`，**同一任务内**开 issue @`SocialKKKK`，如实说明**这会作废对方全部 `ONBOARD_HMI_G2` 证据** |
| 5 | **Zhengyu Shao ＋ Kun Wang** | v2 release 的 attestation：两名不同产品负责人对**同一 commit 与 content manifest hash** 签名。`g1-validate.mjs` 第 27 行实打实校验 `new Set(approvals.map(a=>a.ownerId)).size===2`，**AI 与 CI 不能批准** |
| 6 | — | 打 annotated tag `protocol-v1.0.0`，发布 attestation 作为 Release Asset |

**第二名产品负责人是 Kun Wang。**事实依据：他在场、活跃，并在 2026-09-04 同日完成过一次评
审合并。**本规格不改 `docs/release-governance.md`**——改它等于自我豁免「不代签任何 protocol
release」那条。

**`@SocialKKKK` 的通知发生在节点 4，不在本规格批准时。**本图只产决策、不产代码、不推协议
仓，**闭图本身不触发 notify-after-change**。

*追溯：票 08 的 1.8 与 3.8、票 06 的第 6 问。*

---

## 13. 明账

### 13.1 MesIngest 的 100 条为何在范围外

`OOS-MI-1` Inspector E 信息架构 30 条、`OOS-MI-2` AreaFilterProfile 编辑与实时同步 26 条、
`OOS-MI-3` MesIngest 服务与外部可读目录 18 条、`OOS-MI-4` GONE 明细与存储边界 26 条。

它们在 MVP 剖面里标「本场景不适用」，含义是**与 WIRE_TO_GATE 旅程无关**而非未实现。归
`8005-mes-ingest`，该仓已有四张地图（`new-mes-ingest`、
`mes-ingest-bounded-storage-low-memory`、`demand-series-inspector-e`、
`mes-ingest-watch-area-live-sync`）、1100 个测试与已落地的 CI/CD。

**本规格不重排一个健康仓库的既有工作，只留这一行指针。**

### 13.2 跨 Map 运输（范围外，原文照录）

> **跨 Map 运输**（票 11 判定）。v1.0.0 的 348 条无一条要求它，`REQ-0191`／`REQ-0192`／
> `REQ-0193` 明文将运输两端限定在同一 Map，三条均已在批次 0 实施。现场当前为单图作业
> （`mapId` 25 `老厂前线new`，3 台 AGV 与全部机台、关卡、独占充电桩、等待点均在该图）。若
> 将来现场扩为多图作业，放开跨 Map 运输须先经需求变更流程处置 `REQ-0193`，属独立的后续工
> 作，不在本规格的批次序列内。

这段只描述要走哪条流程，**不预测将来会不会放宽**，因此不构成在规格里预告一次未经批准的需求
变更。`REQ-0193` 是对现实的准确描述而非限制；「单 Map→跨地图」作为第三大重构的前提**正式作
废**，重构只剩两项。

### 13.3 MVP 作为软前置

本规格假定 WIRE_TO_GATE MVP 会通过现场验收，批次 0 直接引用已批准的 MVP 规格与剖面证据、
**不重验**。MVP 的收尾与 P0～P7 现场试运行执行不在本规格范围内，它们有自己的图与证据链。

**一条纠正**：地图 Notes 第 4 条记的「`8005-agv-control-server/docs/defects/` 当前 5 个未闭
合缺陷」**已过时**——6 个文件全部 `fixed` 或 `resolved`。这不改变范围外判定，但软前置一节不
必再为它留余量。

### 13.4 车载端开发同事未评审、未批准

见 0 节与 8.8 第 1 条。**不重复，但不得省略。**

### 13.5 协议 v2 正式 release 的双人签名门禁不变

见 12.2 节点 5。**AI 与 CI 不能批准。**本规格不修改 `docs/release-governance.md`。

### 13.6 本图不产代码

批次 1 及其后任何批次的代码实施、部署与发布归随后的实施图。本规格是判断，不是执行。

---

## 14. 实施图待办登记

**以下八项由本图产生、但不由本图执行。**它们不是需求条目，不占 348 行的任何一行，实施图开
工时要逐项接住：

| # | 事项 | 何时 |
| --- | --- | --- |
| 1 | **删 `runner/` 两个 schema**，必须在批次 1 的候选生成里一并做——它改 content manifest 哈希，而哈希进 attestation 与 tag；它不在冻结的三个面里，删它不动那三个面 | 批次 1 |
| 2 | **接跨仓桌面锁**：`8005-agv-control-server` 拷一份 `Invoke-WithDesktopLock.ps1`（名字 `Global\W2G-InteractiveDesktop` 才是契约，代码不是），且 **`8005-mes-ingest` 那把锁要从快速失败改为带超时等待**——CI 作业该排队，不该因为撞上另一个仓的调度就变红。**这是本图唯一一处对 `8005-mes-ingest` 的改动要求**，不违反范围外判定：那条排除的是它的 100 条需求与既有工作，不是它作为 CI 基础设施的一部分 | 批次 2 前 |
| 3 | **假 RIoT 扩能力面**：五个 `imap` 只读端点、订单命令面（**只记录调用，不模拟业务后果**）、多车种子 | 批次 2 |
| 4 | **`riot-sdk` 新增五个具名 Facade 方法并发一版**，控制服务端升 vendored 包 | 批次 2 轨 B |
| 5 | **`vectorId` ↔ 具名测试绑定架构测试** ＋ 两条 `reasonCode ∈ 注册表` 架构测试 ＋ RIoT 白名单架构测试，三条都是「CI 上一条测试绿」，不挂任何簇 | 批次 1／2 |
| 6 | **把 RIoT 调用白名单提升为产品文档**，并补上第二种建单形态（充电订单 `move + act(78,1)`）。当前权威副本是另一张地图的工作票据（1.3 第 3 项） | 批次 2 前 |
| 7 | **`REQ-0271` 的「可导出」定为 CSV ＋ JSON 两种**——CSV 因为审计导出的实际消费者是人和 Excel，JSON 因为它要能被下一次审计工具机械读回。不做 PDF | 批次 3 |
| 8 | **三台车的 IO 录入与逐仓现场核对**与 `REQ-0259` 门禁启用同批，顺序是**先核对后启用** | 批次 3 / W1 |

---

## 15. 交叉核验结果

汇编时实测复核，不是照抄票据：

| 核验项 | 方法 | 结果 |
| --- | --- | --- |
| 剖面行数 | `wc -l` | 349（348 ＋ 表头）✓ |
| 剖面字节 | `wc -c` | 220,819 ✓ |
| 剖面哈希 | `sha256sum` | `aa5b1117…ac34`，与票 09 定稿一致 ✓ |
| 列数 | 字段计数 3828 ÷ 348 | 每行 **11** 列 ✓ |
| `Batch` 分布 | `cut -f10 \| sort \| uniq -c` | 117＋14＋26＋17＋10＋17＋6＋19＋22＋100 = **348** ✓ |
| 簇分布 | `cut -f8 \| sort \| uniq -c` | 二十个簇合计 **348** ✓ |
| 批次↔簇对应 | 逐批次比对 | 批次 2 = 10＋3＋1、批次 3 = 14＋7＋3＋2、批次 4 = 9＋8、延后 = 8＋8＋6、范围外 = 30＋26＋18＋26，**全部吻合** ✓ |
| 切片↔向量 | 34 条引用去重 | **31**，与协议 v2 冻结的 31 条相等 ✓ |
| 切片顺序↔批次顺序 | 逐条比对 `prerequisites` | 无矛盾 ✓ |
| 每处结论可追溯 | 逐节标注 | 15 张已解决票据，无孤立结论 ✓ |

**一处笔误已纠正**：票 09 的 Q4 与 4.2 写「348 行 12 列」「`Batch` 列（第 12 列）」，实测
TSV 是 **11 列**，`Batch` 是**第 10 列**，`Batch0FormNote` 才是第 11 列（与票 13 的说法一
致）。本规格取实测值。这不影响任何结论。

---

## 16. 本规格自行定案的设计细节

按地图 Notes 第 32 条，以下五处由汇编会话自行定案、**未经用户逐条确认**，理由与代价一并记录：

1. **348 条不抄进规格正文，改为引用 TSV ＋ SHA-256。**理由见 2.1。选错的代价是「改一次呈现
   形态」。
2. **本规格自身的 SHA-256 记在 `10-answer.md` 而不是正文内。**文档记录自己的哈希是自指的。
   代价是读者要多开一个文件。
3. **需求变更的版本号语义（改文义 → minor，只改措辞 → patch，删除条目 → major）、基线头部
   保留版本→哈希对照表、旧 tag 不动、提案归档到 `requirements/change-proposals/`。**四处都
   是流程细节，选错的代价是「改一次流程文本」；不定则 `CP-0001` 落不了地。
4. **`REQ-0157` 的 commit 指针断裂判为「不修复、如实登记」。**重写过的历史无法复活一个
   commit，而内容身份（`query.sql` 的 SHA-256）完好。代价是基线里留着一个解析不了的 commit
   引用，收益是不为此动基线。
5. **RIoT 白名单提升为产品文档列为实施图待办，本图不执行。**本图不产代码也不搬文档；执行它
   要决定放哪、谁维护、与 `REQ-0294` 的引用怎么改，那是需求治理面的工作。代价是白名单在实
   施图开工前仍指向一份工作票据。

---

## 17. 票据索引

本规格的每一条结论都追溯到下列已解决票据之一。逐条推理、被推翻的预设、未证明项与决策归属
留在各自决议中。

| 票 | 主题 | 决议 |
| --- | --- | --- |
| 01 | 建立全量 348 条实施剖面底稿 | [`01-answer.md`](issues/01-answer.md) |
| 02 | 重构／增量判据、分类与排序规则 | [`02-answer.md`](issues/02-answer.md) |
| 03 | 多车并发、车辆占用与 Worklist 执行模型 | [`03-answer.md`](issues/03-answer.md) |
| 04 | 自动充电桩调度与充电失败治理 | [`04-answer.md`](issues/04-answer.md) |
| 05 | 治理面增量（账号权限、配置审计、AGV 生命周期、看板） | [`05-answer.md`](issues/05-answer.md) |
| 06 | 协议 v2 消息面、错误码与向量的一次冻结 | [`06-answer.md`](issues/06-answer.md) |
| 07 | 完整产品切片家族与 `W2G-IS-00`～`07` 的关系 | [`07-answer.md`](issues/07-answer.md) |
| 08 | 验收边界、证据要求与分工排期 | [`08-answer.md`](issues/08-answer.md) |
| 09 | 实施批次划分与批次间依赖，348 行定稿 | [`09-answer.md`](issues/09-answer.md) |
| 10 | 本规格的汇编与批准 | [`10-answer.md`](issues/10-answer.md) |
| 11 | 跨 Map 运输的去留 | [`11-answer.md`](issues/11-answer.md) |
| 12 | 空闲返回与等待点的独占语义 | [`12-answer.md`](issues/12-answer.md) |
| 13 | 六类 MES 运输任务的执行范围 | [`13-answer.md`](issues/13-answer.md) |
| 14 | 途中追加与换序的形态（依 Round 43 实测） | [`14-answer.md`](issues/14-answer.md) |
| 15 | `REQ-0298` 与 `RouteGraphSnapshot` 的冲突处置 | [`15-answer.md`](issues/15-answer.md) |

领域词条见 `8005-agv-program/CONTEXT.md`；跨端权威边界见 `docs/adr/cross/`；三层测试模型见
`docs/wire-to-gate-test-automation.md`（取 `main` 版，491 行）。
