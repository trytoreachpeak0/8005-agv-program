# 完整产品制图前置状态（2026-09-03 探查）

本文件只固定制图那一次会话需要的状态，避免重复探查。它不是决策记录，
不构成任何批准；地图画出后，权威转移到 `map.md` 与 `issues/`。

## 目标

把当前的 WIRE_TO_GATE MVP，按 `requirements/baselines/current-requirements-v1.0.0.md`
的全部 348 条需求，演进成完整产品。

## 已走过的链（这张图占第 2 格的位置，范围换成全量）

| 地图 | 票 | 产出 |
| --- | --- | --- |
| `current-requirements-baseline` | 184 | v1.0.0 基线，348 条 |
| `wire-to-gate-mvp` | 14 | MVP 规格 + 348 行适用性剖面 + `W2G-IS-00`～`07` |
| `wire-to-gate-ai-implementation-kit` | 29 | 把 MVP 规格变成可运行 RC —— 现有代码的来源 |
| `onboard-controlserver-plaintext-transport` | 13 | 明文期双端传输 |

需求层不需要动：v1.0.0 的 348 条 Lifecycle 全部 `active`，指针与 tag 已固定。
缺的是一份覆盖全量的**实施范围与顺序规格**，以及随后的实施图。

## 绑定身份

- 基线：`requirements/baselines/current-requirements-v1.0.0.md`
- 基线 SHA-256：`5e409953dc24d3acbe399e1babf761fbf12c005662f59a0eac5fd240038d6fba`
- Content commit：`b9f321228b534a3b316d3ac1abede05176ed6a70`
- Tag：`requirements-baseline-v1.0.0`
- MVP 剖面 TSV：`.scratch/wire-to-gate-mvp/evidence/final-requirement-applicability-profile.tsv`
- 剖面 SHA-256：`0678fddb8cb0dc4b1df620257ac7076fc8658e3bda828f0de5c6e9f0fe0461de`

## 348 条的现状

MVP 剖面四分类：直接必须 85、交互／安全依赖 101、首期延后 31、本场景不适用 131。

MVP 之外的 162 条（131 + 31）按 TSV 的 `OriginalScope` 聚类，不是一个整体：

| 归属 | 不适用 | 延后 | 合计 |
| --- | --- | --- | --- |
| MesIngest / MesIngestWatch | 84 | 16 | 100 |
| 8005 AGV 主项目 | 47 | 15 | 62 |

那 100 条标「不适用」的含义是**与 WIRE_TO_GATE 旅程无关**，不是「未实现」。
它们属于 `8005-mes-ingest`，该仓已有四张自己的地图（`new-mes-ingest` 28 票、
`mes-ingest-bounded-storage-low-memory` 28 票、`demand-series-inspector-e` 7 票、
`mes-ingest-watch-area-live-sync` 12 票），1100 个测试，CI/CD 已落地。
抽样佐证：REQ-0090 是 Save 的 `expectedFingerprint` 乐观并发，REQ-0100 是 UI
线程切换，REQ-0125 是 Inspector 的 Series 头部，REQ-0145 是 Fluent UI 规范。

62 条 AGV 主项目条目的性质（抽样）：REQ-0175 充电异常不得误触发暂停、
REQ-0285 充电中断双向隔离、REQ-0289/0293 等待点专用与单车独占、
REQ-0311/0318 归档恢复、REQ-0256 账号生命周期、REQ-0266 配置审计。
即：多车调度 + 自动充电桩 + AGV 生命周期 + 配置／账号治理面。

## 现有实现状态

- `8005-agv-control-server`：`ControlServer.{Domain,Application,Infrastructure,Host}`；
  `evidence/{g2,g3,rc}`；G3 证据最新 2026-09-01；`docs/defects/` 开着 5 个，
  最新 `20260903-onboard-safety-facts-frozen-at-session-start.md`。
- `8005-agv-protocol`：切片板 `integration-slices/index.json`（`W2G-IS-00`～`07`），
  `ProtocolVersion` 1，`WireToGateMvpProtocolProfile` allowlist，明文期，
  两端无协商无降级。仓库 private，改动须开 issue @SocialKKKK。
- `8005-agv-onboard-hmi`：**对 agent 只读**，归 Kun Wang。MVP 收尾票 14 记录
  「车载端开发同事未评审、未批准」。
- 工具链基线：ADR-0056，SDK 8.0.424、`net8.0`、xunit.v3。

## 这张图要回答的（初始票据草案）

1. **348 条的全量实施剖面。**MVP 那份是四分类；全量版要的是 N 个实施批次
   与批次间依赖，而不是再来一次「适不适用」。
2. **MesIngest 那 100 条归位。**先核对 `8005-mes-ingest` 现状，判定各条是
   已实现、在途还是未开始，再决定是否纳入本图。不要重做已完成的。
3. **区分「推翻架构前提」与「纯增量」。**单车→多车并发、人工充电→充电桩
   调度、单 Map→跨地图，这三样要重做 ControlServer 的选择与分配核心，是
   重构；账号／配置／报表治理面是增量。两类的实施路径不同，不能混排。
4. **协议 v2 的完整消息面，一次设计完。**逐条加需求逐次发 release 会反复
   作废两端 G2 证据。需在本图内冻结 v2 的消息面、错误码与向量范围。
5. **切片家族。**`W2G-IS-00`～`07` 是 MVP 的。全量需要新的编号体系，并明确
   与既有八个切片的关系（沿用、替换还是并存）。
6. **验收方式。**P0～P7 是一次受控试运行的顺序，只证明单次旅程。完整产品
   需要另一套验收边界与证据要求。
7. **与 Kun Wang 的分工与排期。**多车相关改动在车载端的量大于服务端，而该仓
   对本工作区只读。需在本图内决定协议 v2 的联合设计方式与双人批准节奏。

## 明确不属于这张图

- 不写代码，不改 v1.0.0 基线，不动 `requirements/current-baseline.md` 指针。
- 不替 Kun Wang 决定车载端实现，不代签任何 protocol release。
- MVP 剖面 TSV 的既有分类不在本图重写；全量剖面是新增的一层，不是对它的修订。
